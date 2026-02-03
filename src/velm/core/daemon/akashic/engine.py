# Path: core/daemon/akashic/engine.py
# -----------------------------------

import time
import json
import threading
import logging
import traceback
import os
import sys
import random
import gzip
import shutil
import atexit
import platform
from collections import deque, defaultdict
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

try:
    import psutil
except ImportError:
    psutil = None

# --- GNOSTIC INTERNAL UPLINKS ---
from .memory import ScrollOfTime
from .broadcaster import Congregation
from .envelope import EnvelopeForge
from ..serializer import gnostic_serializer
from .constants import TAG_INTERNAL, MAX_HISTORY_DEPTH, TAG_HERESY

# --- PHYSICS CONSTANTS ---
MAX_SESSION_SIZE = 100 * 1024 * 1024  # 100MB Cap
FLUSH_INTERVAL = 1.0  # 1s Batching
QUEUE_CAPACITY = 10000  # RAM Buffer
PRUNE_THRESHOLD = 2048  # Truncate payloads > 2KB
JANITOR_MAX_AGE_HOURS = 24
JANITOR_MAX_SESSIONS = 5
SUMMARY_INTERVAL = 60.0  # Summarize noise every 60s

Logger = logging.getLogger("AkashicEngine")


class SessionVault:
    """
    [THE VAULT]
    Manages the physical storage of a single execution lifecycle.
    """

    def __init__(self, base_path: Path):
        self.timestamp = int(time.time())
        self.pid = os.getpid()
        self.id = f"{self.timestamp}_{self.pid}"
        self.path = base_path / "sessions" / self.id

        self.traffic_file = self.path / "traffic.jsonl"
        self.manifest_file = self.path / "manifest.json"
        self.snapshot_file = self.path / "snapshot.json"

        self.size_bytes = 0
        self.is_sealed = False
        self.start_time = time.time()
        self.event_count = 0
        self.symlink_pointer = base_path / "latest_session"

    def initialize(self):
        try:
            self.path.mkdir(parents=True, exist_ok=True)
            self._write_header()
            self._update_pointer()
        except Exception as e:
            sys.stderr.write(f"[Akasha] ⚠️ Vault Creation Failed: {e}\n")
            self.is_sealed = True

    def _write_header(self):
        header = {
            "type": "META",
            "event": "IGNITION",
            "timestamp": time.time(),
            "pid": self.pid,
            "system": platform.system(),
            "version": "v16.0-OMEGA"
        }
        self.write(header)

    def _update_pointer(self):
        try:
            if os.name == 'nt':
                self.symlink_pointer.with_suffix(".txt").write_text(str(self.path.resolve()), encoding='utf-8')
            else:
                if self.symlink_pointer.exists() or self.symlink_pointer.is_symlink():
                    self.symlink_pointer.unlink()
                self.symlink_pointer.symlink_to(self.path)
        except:
            pass

    def write(self, data: Dict[str, Any]):
        if self.is_sealed: return

        try:
            line = json.dumps(data, default=gnostic_serializer) + "\n"
            encoded = line.encode('utf-8', errors='replace')
            size = len(encoded)

            if self.size_bytes + size > MAX_SESSION_SIZE:
                self.seal("SIZE_LIMIT_EXCEEDED")
                return

            with open(self.traffic_file, "ab") as f:
                f.write(encoded)

            self.size_bytes += size
            self.event_count += 1

        except Exception:
            self.is_sealed = True

    def seal(self, reason: str = "SHUTDOWN"):
        if self.is_sealed: return
        self.is_sealed = True

        try:
            manifest = {
                "id": self.id,
                "start": self.start_time,
                "end": time.time(),
                "duration": time.time() - self.start_time,
                "events": self.event_count,
                "size": self.size_bytes,
                "exit_reason": reason
            }
            with open(self.manifest_file, "w", encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
        except:
            pass


class AkashicRecord:
    """
    [THE AKASHIC RECORD V16-OMEGA]
    The Supreme Memory Controller.
    """

    def __init__(self, persistence_path: str = ".scaffold/akashic.jsonl", **kwargs):
        self.memory = ScrollOfTime()
        self.congregation = Congregation()

        # 1. ANCHOR REALITY
        self.root_scaffold = Path(persistence_path).resolve().parent

        # 2. INITIALIZE VAULT
        self.vault = SessionVault(self.root_scaffold)

        # 3. KINETIC PIPELINES
        self._queue: deque = deque(maxlen=QUEUE_CAPACITY)

        # 4. METABOLIC STATE
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._heresy_map: Dict[str, str] = {}

        # CONFIGURATION
        self._full_log = os.environ.get("SCAFFOLD_LOG_FULL") == "1"
        self._traffic_disabled = os.environ.get("SCAFFOLD_NO_TRAFFIC") == "1"

        # NOISE SUMMARIZER STATE
        self._noise_counter = 0
        self._last_summary_time = time.time()

        self._write_metrics = {"eps": 0.0, "latency": 0.0}
        self._start_time = time.time()

        self._run_janitor()
        self.vault.initialize()
        self._start_scribe()
        threading.Thread(target=self._hydrate_memory, name="AkashicHydrator", daemon=True).start()
        atexit.register(self.shutdown)

    def _start_scribe(self):
        self._scribe_thread = threading.Thread(target=self._scribe_loop, name="AkashicScribe", daemon=True)
        self._scribe_thread.start()

    def _run_janitor(self):
        try:
            sessions_dir = self.root_scaffold / "sessions"
            if not sessions_dir.exists(): return

            sessions = []
            for path in sessions_dir.iterdir():
                if not path.is_dir(): continue
                try:
                    parts = path.name.split('_')
                    if len(parts) >= 2:
                        ts = int(parts[0])
                        pid = int(parts[1])
                        sessions.append({"path": path, "ts": ts, "pid": pid})
                except:
                    continue

            sessions.sort(key=lambda x: x["ts"], reverse=True)
            now = time.time()
            max_age = JANITOR_MAX_AGE_HOURS * 3600

            for i, s in enumerate(sessions):
                path = s["path"]
                is_old = (now - s["ts"]) > max_age
                is_overflow = i >= JANITOR_MAX_SESSIONS
                is_zombie = psutil and not psutil.pid_exists(s["pid"]) if psutil else False
                is_current = s["pid"] == self.vault.pid

                if (is_old or is_overflow or is_zombie) and not is_current:
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass

    def broadcast(self, packet: Dict[str, Any]):
        """Ingests semantic Gnosis (State Changes)."""
        try:
            ts = time.time()
            if "jsonrpc" not in packet:
                packet.setdefault("timestamp", ts)
                rpc_packet = EnvelopeForge.wrap(packet)
            else:
                rpc_packet = packet

            if not rpc_packet: return

            if rpc_packet.get("method") == "textDocument/publishDiagnostics":
                if not self._should_log_diagnostics(rpc_packet):
                    pass

            is_heresy = rpc_packet.get("method") == "scaffold/heresy"
            self.memory.inscribe(rpc_packet, is_heresy)
            self.congregation.multicast(rpc_packet)

        except Exception:
            pass

    def _should_log_diagnostics(self, packet: Dict) -> bool:
        try:
            params = packet.get("params", {})
            uri = params.get("uri")
            diags = params.get("diagnostics", [])
            content_hash = hashlib.md5(json.dumps(diags, sort_keys=True).encode()).hexdigest()
            with self._lock:
                if uri in self._heresy_map and self._heresy_map[uri] == content_hash:
                    return False
                self._heresy_map[uri] = content_hash
                return True
        except:
            return True

    def log_traffic(self, packet: Dict[str, Any], direction: str):
        """[THE BLACK BOX RITE]"""
        if self._traffic_disabled or self.vault.is_sealed: return

        try:
            is_noise = self._is_noise(packet)

            # [ASCENSION 16]: HEARTBEAT SUMMARIZER
            if is_noise and not self._full_log:
                with self._lock:
                    self._noise_counter += 1
                return

            packet_copy = packet
            method = packet.get("method")
            params = packet.get("params", {})

            # Payload Pruning
            if method == "textDocument/didChange" and "contentChanges" in params:
                packet_copy = packet.copy()
                p_params = params.copy()
                packet_copy["params"] = p_params
                new_changes = []
                for change in params.get("contentChanges", []):
                    if "text" in change and len(change["text"]) > PRUNE_THRESHOLD:
                        new_changes.append({
                            **change,
                            "text": change["text"][:PRUNE_THRESHOLD] + f"... <{len(change['text'])} bytes>"
                        })
                    else:
                        new_changes.append(change)
                p_params["contentChanges"] = new_changes

            entry = {"t": time.time(), "d": direction, "p": packet_copy}

            with self._lock:
                if len(self._queue) < QUEUE_CAPACITY:
                    self._queue.append(entry)

        except Exception:
            pass

    def _is_noise(self, packet: Dict[str, Any]) -> bool:
        """Determines if a packet is metabolic noise."""
        method = packet.get("method", "")
        cmd = packet.get("command", "")
        params = packet.get("params", {})

        if method in ("window/logMessage", "scaffold/log", "$/heartbeat", "heartbeat", "scaffold/progress"): return True
        if cmd in ("ping", "pong") or params.get("command") == "ping": return True
        if method in ("daemon/anchor_project", "daemon/status"): return True
        # [THE FIX]: Explicitly catch shadow/status and plugins
        if cmd == "shadow" and params.get("shadow_command") == "status": return True
        if cmd == "plugins": return True
        if method in ("textDocument/hover", "textDocument/documentSymbol", "textDocument/codeAction"): return True

        return False

    def _apply_veil(self, packet: Any) -> Any:
        try:
            if isinstance(packet, list): return [self._apply_veil(i) for i in packet]
            if isinstance(packet, dict):
                new_pkt = {}
                keys = {"token", "auth_token", "api_key", "password", "secret", "credentials"}
                for k, v in packet.items():
                    if k.lower() in keys:
                        new_pkt[k] = "[REDACTED]"
                    else:
                        new_pkt[k] = self._apply_veil(v)
                return new_pkt
            return packet
        except:
            return packet

    def _scribe_loop(self):
        while not self._stop_event.is_set():
            try:
                time.sleep(FLUSH_INTERVAL)

                # [ASCENSION 16]: EMIT SUMMARY
                now = time.time()
                with self._lock:
                    pending_noise = self._noise_counter

                if pending_noise > 0 and (now - self._last_summary_time > SUMMARY_INTERVAL):
                    with self._lock:
                        summary = {
                            "t": now, "d": "SYSTEM",
                            "p": {
                                "type": "SUMMARY",
                                "msg": f"Suppressed {self._noise_counter} metabolic signals.",
                                "interval_s": SUMMARY_INTERVAL
                            }
                        }
                        self._queue.append(summary)
                        self._noise_counter = 0
                        self._last_summary_time = now

                if not self._queue: continue

                start_time = time.perf_counter()
                batch = []

                with self._lock:
                    while self._queue:
                        batch.append(self._queue.popleft())
                        if len(batch) > 1000: break

                if not batch: continue

                final_batch = []
                for item in batch:
                    try:
                        item['p'] = self._apply_veil(item['p'])
                        final_batch.append(item)
                    except:
                        continue

                if final_batch:
                    for item in final_batch:
                        self.vault.write(item)

                duration = time.perf_counter() - start_time
                self._write_metrics["latency"] = duration
                self._write_metrics["eps"] = len(batch) / duration if duration > 0 else 0

                if duration > 0.1: time.sleep(0.5)

            except Exception:
                time.sleep(2)

    def _hydrate_memory(self):
        p_path = self.root_scaffold / "akashic.jsonl"
        if not p_path.exists(): return
        try:
            with open(p_path, 'r', encoding='utf-8') as f:
                lines = deque(f, maxlen=MAX_HISTORY_DEPTH)
            for line in lines:
                try:
                    packet = json.loads(line)
                    is_heresy = packet.get("method") == "scaffold/heresy"
                    self.memory.inscribe(packet, is_heresy)
                except:
                    continue
        except:
            pass

    def perform_deferred_replay(self, witness_id: str):
        pass

    def shutdown(self):
        self._stop_event.set()
        remaining = []
        with self._lock:
            remaining = list(self._queue)
        for item in remaining:
            try:
                self.vault.write(item)
            except:
                pass
        self.vault.seal("CLEAN_EXIT")
        try:
            snap = self.memory.snapshot()
            with open(self.vault.snapshot_file, 'w') as f:
                json.dump(snap, f)
        except:
            pass
        self.congregation.close_all()

    @property
    def get_telemetry(self) -> Dict[str, Any]:
        census = self.congregation.get_census()
        return {
            "status": "ONLINE" if not self.vault.is_sealed else "SEALED",
            "session_id": self.vault.id,
            "io": {
                "eps": round(self._write_metrics["eps"], 2),
                "latency": round(self._write_metrics["latency"] * 1000, 2),
                "backlog": len(self._queue),
                "suppressed_noise": self._noise_counter
            },
            "storage": {
                "file": self.vault.traffic_file.name,
                "size_mb": round(self.vault.size_bytes / 1024 / 1024, 2)
            },
            "network": census
        }