# Path: core/lsp/scaffold_features/linter/rules/artisan_inquest.py
# -------------------------------------------------------

import logging
import json
import socket
import time
import uuid
import re
import os
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any

# --- GNOSTIC UPLINKS ---
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity, Range, Position
from ....base import forensic_log, UriUtils

Logger = logging.getLogger("ArtisanInquest")

# [PHYSICS CONSTANTS]
HEADER_TERMINATOR = b"\r\n\r\n"
CONTENT_LENGTH_RE = re.compile(rb"Content-Length: (\d+)", re.IGNORECASE)
DAEMON_TIMEOUT = 15.0  # Extended patience for deep analysis
CONNECT_TIMEOUT = 2.0  # Fast fail on connect
MAX_RETRIES = 2


class ArtisanInquestRule(BaseLinterRule):
    """
    =============================================================================
    == THE GNOSTIC ILLUMINATOR (V-Ω-DEEP-PACKET-INSPECTION)                    ==
    =============================================================================
    LIF: INFINITY | ROLE: DAEMON_BRIDGE | RANK: SOVEREIGN

    The definitive bridge.
    Now equipped with [TOTAL_RECALL]. It dumps the full request and response
    payloads to stderr to diagnose the "Zero Atoms" heresy.
    """

    def __init__(self, server):
        self.server = server
        self._socket: Optional[socket.socket] = None
        self._socket_lock = threading.Lock()
        self._cached_config: Optional[Dict] = None
        self._config_timestamp = 0.0

        forensic_log("The Daemonic Inquisitor is ONLINE. Deep-Packet Inspection: ACTIVE.", "SUCCESS", "INIT")

    @property
    def code(self):
        return "GNOSTIC_INQUEST"

    def validate(self, ctx) -> List[Diagnostic]:
        """[THE RITE OF REMOTE JUDGMENT]"""
        # [ASCENSION 1]: TYPE-SAFE URI HANDLING
        # Ensure we have a string, regardless of Pydantic RootModel wrappers
        uri_str = str(ctx.doc.uri)
        filename = uri_str.split('/')[-1]

        rid = f"inq-{uuid.uuid4().hex[:6]}"
        start_ns = time.perf_counter_ns()

        # Initialize defaults to prevent UnboundLocalError
        norm_project_root = "."
        rel_path = "unknown"

        forensic_log(f"[{rid}] 🟢 Starting Inquest for {filename}", "START", "INQ", trace_id=rid)

        # --- 1. SPATIAL RESOLUTION ---
        try:
            abs_fs_path = UriUtils.to_fs_path(uri_str)
            project_root = self.server.project_root

            if not project_root:
                forensic_log(f"[{rid}] 🛑 Aborting: No Project Root anchored.", "WARN", "INQ", trace_id=rid)
                return []

            norm_project_root = str(project_root).replace('\\', '/')

            # [ASCENSION 2]: PATH RELATIVITY AUDIT
            try:
                # Force strictly relative path for Daemon consumption
                rel_path = str(abs_fs_path.relative_to(project_root)).replace('\\', '/')
            except ValueError:
                # Fallback, but log it as a potential cause of "Zero Atoms"
                rel_path = str(abs_fs_path).replace('\\', '/')
                forensic_log(f"[{rid}] ⚠️ Path Relativity Fracture: File is outside root.", "WARN", "INQ", trace_id=rid)

        except Exception as e:
            forensic_log(f"[{rid}] 💥 Path Resolution Fracture: {e}", "ERROR", "INQ", trace_id=rid)
            return []

        # --- 2. FORGE THE PLEA ---
        try:
            file_size = len(ctx.doc.text or "")
            dynamic_timeout = DAEMON_TIMEOUT + (file_size / 20000.0)

            payload = {
                "jsonrpc": "2.0",
                "id": rid,
                "method": "analyze",
                "params": {
                    "file_path": rel_path,  # <--- The exact path sent to Daemon
                    "content": ctx.doc.text or "",
                    "project_root": norm_project_root,
                    "batch": False,
                    "auto_redeem": False,
                    "metadata": {
                        "source": "LSP_HYPER_INQUEST",
                        "trace_id": rid,
                        "prefer_sync": True,
                        "timeout": dynamic_timeout
                    }
                }
            }

            # [ASCENSION 3]: FULL REQUEST DUMP
            # We verify exactly what we are asking the Daemon to do.
            req_preview = json.dumps({k: v for k, v in payload['params'].items() if k != 'content'}, default=str)
            forensic_log(f"[{rid}] 📤 Request Params: {req_preview}", "NET", "TX", trace_id=rid)

        except Exception as e:
            forensic_log(f"[{rid}] 💥 Payload Forge Fracture: {e}", "ERROR", "INQ", trace_id=rid)
            return []

        # --- 3. COMMUNE (PERSISTENT) ---
        try:
            t_net_start = time.perf_counter()

            response = self._transact_persistent(payload, self.server.project_root, rid)

            net_dur = (time.perf_counter() - t_net_start) * 1000

            if not response:
                forensic_log(f"[{rid}] 🌑 NO RESPONSE from Daemon.", "ERROR", "INQ", trace_id=rid)
                return [self._forge_system_warning("Daemon Disconnected", "The Gnostic Nexus is silent.", rid,
                                                   DiagnosticSeverity.Warning)]

            if 'error' in response:
                err = response['error']
                forensic_log(f"[{rid}] ❌ Daemon Error {err.get('code')}: {err.get('message')}", "ERROR", "INQ",
                             trace_id=rid)
                return [self._forge_system_warning("Inquest Rejected", err.get('message', 'Unknown'), rid,
                                                   DiagnosticSeverity.Warning)]

            # --- 4. THE REVELATION (DEEP INSPECTION) ---
            result_body = response.get('result', {})

            # [ASCENSION 4]: RAW RESULT DUMP
            # We log keys to see if we missed 'stderr' or 'stdout' which might contain errors
            forensic_log(f"[{rid}] 📥 Result Keys: {list(result_body.keys())}", "DATA", "INQ", trace_id=rid)

            if result_body.get('status') == 'PENDING':
                forensic_log(f"[{rid}] ⏳ Inquest Deferred (Async).", "WARN", "INQ", trace_id=rid)
                return []

            # Extract Data
            data = result_body.get('data') if isinstance(result_body, dict) and 'data' in result_body else result_body

            # [ASCENSION 5]: DATA TYPE AUDIT
            if data is None:
                forensic_log(f"[{rid}] 🕊️ DATA IS NULL. Full Result: {json.dumps(result_body, default=str)[:1000]}",
                             "WARN", "INQ", trace_id=rid)
                return []

            if not isinstance(data, dict):
                forensic_log(f"[{rid}] ⚠️ Data Invalid Type: {type(data)}", "WARN", "INQ", trace_id=rid)
                return []

            raw_diagnostics = data.get('diagnostics', [])

            # [ASCENSION 6]: DIAGNOSTIC COUNT AUDIT
            total_dur = (time.perf_counter_ns() - start_ns) / 1_000_000

            if raw_diagnostics:
                forensic_log(f"[{rid}] ✨ SUCCESS: Found {len(raw_diagnostics)} Heresies. (Net: {net_dur:.1f}ms)",
                             "SUCCESS", "INQ", trace_id=rid)
                # Log first diagnostic for sanity check
                forensic_log(f"[{rid}] 👁️ First Heresy: {json.dumps(raw_diagnostics[0], default=str)}", "DATA", "INQ",
                             trace_id=rid)
            else:
                forensic_log(f"[{rid}] 🌿 CLEAN: No Heresies Found.", "SUCCESS", "INQ", trace_id=rid)

            return self._map_to_types(raw_diagnostics)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            forensic_log(f"[{rid}] 💥 Critical Inquest Fracture: {str(e)}\n{tb}", "FATAL", "INQ", trace_id=rid)
            self._close_socket()
            return [self._forge_system_warning("Inquest Crashed", str(e), rid, DiagnosticSeverity.Error)]

    def _transact_persistent(self, payload: Dict, root: Path, rid: str) -> Optional[Dict]:
        """[ASCENSION 7]: THE ETERNAL SOCKET with DOUBLE-TAP RETRY"""

        with self._socket_lock:
            # 1. Divine Config
            config = self._get_daemon_config(root, rid)
            if not config:
                forensic_log(f"[{rid}] 🚫 No Daemon Config.", "WARN", "NET", trace_id=rid)
                return None

            payload['auth_token'] = config['token']

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    # 2. Ensure Connection
                    if not self._socket:
                        if not self._connect(config, rid):
                            continue

                    # [ASCENSION 8]: VITALITY PEEK (Dead Connection Detection)
                    try:
                        self._socket.setblocking(False)
                        peek = self._socket.recv(1, socket.MSG_PEEK)
                        if peek == b'':
                            forensic_log(f"[{rid}] 💀 Socket Closed (Peek). Reconnecting...", "WARN", "NET",
                                         trace_id=rid)
                            self._close_socket()
                            if not self._connect(config, rid): return None
                    except BlockingIOError:
                        pass  # Socket alive
                    except Exception as e:
                        forensic_log(f"[{rid}] 💀 Socket Error (Peek): {e}. Reconnecting...", "WARN", "NET",
                                     trace_id=rid)
                        self._close_socket()
                        if not self._connect(config, rid): return None
                    finally:
                        if self._socket: self._socket.setblocking(True)

                    # 3. Transmit
                    body = json.dumps(payload, default=str).encode('utf-8')
                    header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')

                    self._socket.sendall(header + body)

                    # 4. Receive
                    return self._read_response(self._socket, rid)

                except (BrokenPipeError, ConnectionResetError, socket.timeout) as e:
                    forensic_log(f"[{rid}] 🔌 Link Severed ({e}). Retrying...", "WARN", "NET", trace_id=rid)
                    self._close_socket()
                    time.sleep(0.1)
                except Exception as e:
                    forensic_log(f"[{rid}] 💥 Unexpected Net Error: {e}", "ERROR", "NET", trace_id=rid)
                    self._close_socket()
                    return None

            return None

    def _connect(self, config: Dict, rid: str) -> bool:
        """[ASCENSION 9]: SOCKET PHYSICS TUNING"""
        try:
            self._socket = socket.create_connection((config['host'], config['port']), timeout=CONNECT_TIMEOUT)

            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)

            # Operational Timeout
            self._socket.settimeout(DAEMON_TIMEOUT)

            # [ASCENSION 10]: CONNECTION AUDIT
            local = self._socket.getsockname()
            peer = self._socket.getpeername()
            forensic_log(f"[{rid}] 🔗 Connected: {local} -> {peer}", "INFO", "NET", trace_id=rid)
            return True
        except Exception as e:
            forensic_log(f"[{rid}] ⛔ Connect Failed: {e}", "ERROR", "NET", trace_id=rid)
            self._socket = None
            return False

    def _read_response(self, sock: socket.socket, rid: str) -> Optional[Dict]:
        """[ASCENSION 11]: HYDRODYNAMIC BUFFER with HEADER LOGGING"""
        buffer = bytearray()

        # HEADER HUNT
        while b"\r\n\r\n" not in buffer:
            try:
                chunk = sock.recv(4096)
                if not chunk: raise ConnectionResetError("Peer closed stream")
                buffer.extend(chunk)
            except socket.timeout:
                raise socket.timeout("Header Timeout")

        header_end = buffer.find(b"\r\n\r\n")
        header = buffer[:header_end].decode('ascii')
        match = CONTENT_LENGTH_RE.search(header.encode('ascii'))

        if not match:
            forensic_log(f"[{rid}] 💀 Invalid Header: {header}", "ERROR", "NET", trace_id=rid)
            raise ValueError("Invalid Header")

        content_len = int(match.group(1))
        # forensic_log(f"[{rid}] 📏 Expecting Body: {content_len} bytes", "INFO", "NET", trace_id=rid)

        body_start = header_end + 4

        # BODY HUNT
        while len(buffer) < body_start + content_len:
            try:
                needed = (body_start + content_len) - len(buffer)
                chunk = sock.recv(min(65536, needed))
                if not chunk: raise ConnectionResetError("Peer closed during body")
                buffer.extend(chunk)
            except socket.timeout:
                raise socket.timeout(f"Body Timeout. Got {len(buffer)}/{content_len}")

        body_bytes = buffer[body_start: body_start + content_len]

        try:
            return json.loads(body_bytes.decode('utf-8'))
        except json.JSONDecodeError as e:
            raw_preview = body_bytes[:200].hex()
            forensic_log(f"[{rid}] 🧱 JSON Fracture: {e}. Raw: {raw_preview}...", "ERROR", "NET", trace_id=rid)
            return None

    def _close_socket(self):
        if self._socket:
            try:
                self._socket.close()
            except:
                pass
            self._socket = None

    def _get_daemon_config(self, root: Path, rid: str) -> Optional[Dict]:
        now = time.time()
        if self._cached_config and (now - self._config_timestamp < 5.0):
            return self._cached_config

        # 1. Server Memory (Fastest)
        if hasattr(self.server, '_daemon_port') and hasattr(self.server,
                                                            '_daemon_token') and self.server._daemon_token != 'VOID':
            return {"host": "127.0.0.1", "port": self.server._daemon_port, "token": self.server._daemon_token}

        # 2. Environment
        env_port = os.environ.get("SCAFFOLD_DAEMON_PORT")
        env_token = os.environ.get("SCAFFOLD_DAEMON_TOKEN")
        if env_port and env_token:
            return {"host": "127.0.0.1", "port": int(env_port), "token": env_token}

        return None

    def _forge_system_warning(self, title: str, message: str, rid: str, severity: DiagnosticSeverity) -> Diagnostic:
        """[ASCENSION 12]: META-HERESY"""
        return Diagnostic(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=1)),
            severity=severity,
            code="SYSTEM_ALERT",
            source="Gnostic Inquisitor",
            message=f"[{title}] {message}",
            data={"trace_id": rid}
        )

    def _map_to_types(self, raw_list: List[dict]) -> List[Diagnostic]:
        items = []
        for h in raw_list:
            try:
                line_idx = int(h.get('internal_line', h.get('line', 1) - 1))
                rng = Range(
                    start=Position(line=line_idx, character=0),
                    end=Position(line=line_idx, character=999)
                )
                items.append(Diagnostic(
                    range=rng,
                    severity=self._map_severity(h.get('severity', 2)),
                    code=str(h.get('code', 'DAEMON')),
                    message=h.get('message', 'Unknown Heresy'),
                    source="Gnostic Daemon",
                    data=h.get('data') or h
                ))
            except Exception as e:
                forensic_log(f"Skipping malformed diagnosis: {e}", "WARN", "INQ")
                continue
        return items

    def _map_severity(self, raw: Any) -> DiagnosticSeverity:
        if isinstance(raw, int):
            if 1 <= raw <= 4: return DiagnosticSeverity(raw)

        s = str(raw).upper()
        if 'CRIT' in s or 'ERR' in s or '1' in s: return DiagnosticSeverity.Error
        if 'WARN' in s or '2' in s: return DiagnosticSeverity.Warning
        if 'INFO' in s or '3' in s: return DiagnosticSeverity.Information
        return DiagnosticSeverity.Hint