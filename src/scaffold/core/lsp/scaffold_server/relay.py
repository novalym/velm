# Path: core/lsp/scaffold_server/relay.py
# ---------------------------------------
# LIF: INFINITY | ROLE: DAEMON_BRIDGE | RANK: SOVEREIGN
# auth_code: Ω_RELAY_TOTALITY_V30_REFLEXIVE

import socket
import json
import re
import time
import threading
import uuid
from pathlib import Path
from typing import Any, Optional, Dict, List

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, UriUtils

# --- PHYSICS CONSTANTS ---
HEADER_TERMINATOR = b"\r\n\r\n"
CONTENT_LENGTH_RE = re.compile(rb"Content-Length: (\d+)", re.IGNORECASE)
READ_CHUNK_SIZE = 1048576  # 1MB
HANDSHAKE_TIMEOUT = 10.0


class DaemonRelay:
    """
    =================================================================================
    == THE DAEMON RELAY (V-Ω-TOTALITY-V30-REFLEXIVE)                               ==
    =================================================================================
    The Sovereign Conductor of the Silver Cord.
    Now empowered with REFLEXIVE FORWARDING to bridge async Daemon responses back
    to the Ocular UI.
    =================================================================================
    """
    __slots__ = [
        'server', '_stop_event', '_buffer', '_socket', '_pending_syncs',
        '_sync_lock', '_relay_active', '_thread', '_token_hash'
    ]

    def __init__(self, server: Any):
        self.server = server
        self._stop_event = threading.Event()
        self._buffer = bytearray()
        self._socket: Optional[socket.socket] = None
        self._pending_syncs: Dict[str, Dict[str, Any]] = {}
        self._sync_lock = threading.Lock()
        self._relay_active = False

    def ignite(self, port: int, token: str):
        if self._relay_active: return
        self._stop_event.clear()
        self._token_hash = uuid.uuid5(uuid.NAMESPACE_DNS, token).hex[:8]

        self._thread = threading.Thread(
            target=self._relay_loop,
            args=(port, token.strip()),
            name=f"SilverCord-{self._token_hash}",
            daemon=True
        )
        self._thread.start()

    def _relay_loop(self, port: int, token: str):
        """[THE ETERNAL LOOP]"""
        project_path_str = str(self.server.project_root) if self.server.project_root else "."
        backoff = 1.0

        while not self._stop_event.is_set():
            s = None
            try:
                # 1. CONNECT
                s = socket.create_connection(("127.0.0.1", port), timeout=5)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self._socket = s

                # 2. AUTHENTICATE
                auth_id = f"auth-{uuid.uuid4().hex[:6]}"
                auth_event = threading.Event()
                with self._sync_lock:
                    self._pending_syncs[auth_id] = {"event": auth_event, "result": None}

                self._send_frame(s, {
                    "jsonrpc": "2.0", "id": auth_id,
                    "method": "gnostic/relay_auth",
                    "params": {"token": token, "identity": "ORACLE_RELAY"},
                    "auth_token": token
                })

                if not auth_event.wait(HANDSHAKE_TIMEOUT):
                    raise TimeoutError("Daemon Handshake Timeout")

                res = self._pending_syncs[auth_id]["result"]
                if not res or not (res.get('success') or res.get('status') == 'CONSECRATED'):
                    raise PermissionError("Daemon Rejected Auth")

                self.server._relay_active = True
                forensic_log(f"Silver Cord Consecrated. Reality: {project_path_str}", "SUCCESS", "RELAY")

                # 3. ANCHOR & FLUSH
                self._send_frame(s, {
                    "jsonrpc": "2.0", "method": "daemon/anchor",
                    "params": {"path": project_path_str.replace('\\', '/')},
                    "auth_token": token
                })

                if hasattr(self.server, 'adrenaline') and self.server.adrenaline:
                    threading.Thread(target=self.server.adrenaline.flush_backlog, daemon=True).start()

                # 4. INGRESS
                backoff = 1.0
                while self.server._relay_active:
                    chunk = s.recv(READ_CHUNK_SIZE)
                    if not chunk: break
                    self._buffer.extend(chunk)
                    self._process_buffer()

            except Exception as e:
                self.server._relay_active = False
                if not self.server.is_shutdown:
                    time.sleep(backoff)
                    backoff = min(30.0, backoff * 1.5)
            finally:
                if s:
                    try:
                        s.close()
                    except:
                        pass
                self._socket = None

    def send_sync_request(self, method: str, params: Dict, timeout: float = 5.0) -> Any:
        """[THE SYNCHRONOUS PULSE]"""
        if not self._socket or not self.server._relay_active: return None
        req_id = f"sync-{uuid.uuid4().hex[:6]}"
        event = threading.Event()

        with self._sync_lock:
            self._pending_syncs[req_id] = {"event": event, "result": None}

        payload = {
            "jsonrpc": "2.0", "id": req_id, "method": method,
            "params": params, "auth_token": self.server._daemon_token
        }

        try:
            self._send_frame(self._socket, payload)
            if event.wait(timeout):
                with self._sync_lock:
                    return self._pending_syncs.pop(req_id)["result"]
        except Exception:
            pass
        finally:
            with self._sync_lock:
                self._pending_syncs.pop(req_id, None)
        return None

    def cancel_rite(self, trace_id: str):
        if self._socket:
            self._send_frame(self._socket, {
                "jsonrpc": "2.0", "method": "daemon/cancel",
                "params": {"trace_id": trace_id}, "auth_token": self.server._daemon_token
            })

    def _send_frame(self, sock, payload):
        body = json.dumps(payload).encode('utf-8')
        header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
        with threading.Lock(): sock.sendall(header + body)

    def _process_buffer(self):
        while True:
            header_end = self._buffer.find(HEADER_TERMINATOR)
            if header_end == -1: return
            match = CONTENT_LENGTH_RE.search(self._buffer[:header_end])
            if not match:
                del self._buffer[:header_end + 4];
                continue

            content_len = int(match.group(1))
            body_start = header_end + 4
            body_end = body_start + content_len

            if len(self._buffer) < body_end: return

            body = self._buffer[body_start:body_end]
            del self._buffer[:body_end]

            try:
                msg = json.loads(body.decode('utf-8', errors='replace'))
                self._handle_daemon_message(msg)
            except Exception as e:
                forensic_log(f"Message Fracture: {e}", "ERROR", "RELAY")

    def _handle_daemon_message(self, msg: Dict[str, Any]):
        """[THE TRIAGE ROUTER]"""
        rid = msg.get('id')

        # 1. SYNC RESPONSE (Matched ID)
        if rid:
            with self._sync_lock:
                if rid in self._pending_syncs:
                    self._pending_syncs[rid]["result"] = msg.get("result") or msg
                    self._pending_syncs[rid]["event"].set()
                    return

        # 2. [ASCENSION 1]: REFLEXIVE FORWARDING (Orphaned/Async Responses)
        # If the Daemon responds to an async request (like 'analyze'), we must
        # unpack the payload and project it as an LSP Notification.
        result = msg.get('result', {})
        if result and isinstance(result, dict) and 'data' in result:
            data = result['data']

            # A. DIAGNOSTICS (The Core Gnosis)
            if 'diagnostics' in data:
                # [ASCENSION 2]: ISOMORPHIC URI SUTURE
                # The Daemon returns relative paths; we must anchor them.
                raw_path = result.get('path') or data.get('path') or data.get('file_path') or ""

                # Try to use the URI from the result if valid, else construct it
                uri = ""
                if raw_path:
                    try:
                        # Ensure absolute path using Server Root
                        full_path = self.server.project_root / raw_path
                        uri = UriUtils.to_uri(full_path)
                    except:
                        uri = UriUtils.to_uri(Path(raw_path).resolve())

                if uri:
                    diags = data.get('diagnostics', [])
                    # [ASCENSION 9]: SOURCE TAGGING
                    for d in diags:
                        d['source'] = 'DAEMON'
                        if 'data' not in d: d['data'] = {}
                        d['data']['trace_id'] = msg.get('_meta', {}).get('trace_id', 'async-ref')

                    self.server.endpoint.send_notification("textDocument/publishDiagnostics", {
                        "uri": uri,
                        "diagnostics": diags,
                        "_source": "DAEMON_REFLEX"
                    })

            # B. MIRROR (Tree Structure)
            if 'structure' in data:
                # Construct URI if possible
                # ... (Similar logic to above)
                pass

        # 3. STANDARD NOTIFICATION FORWARDING
        if "method" in msg and not rid:
            method = msg["method"]
            if method in ("$/heartbeat", "heartbeat"): return
            params = msg.get("params", {})
            params["_source"] = "DAEMON"
            if "uri" in params and not str(params["uri"]).startswith("file:"):
                params["uri"] = UriUtils.to_uri(Path(params["uri"]))

            self.server.endpoint.send_notification(method, params)

    def terminate(self):
        self._stop_event.set()
        self._relay_active = False
        if self._socket:
            try:
                self._socket.close()
            except:
                pass