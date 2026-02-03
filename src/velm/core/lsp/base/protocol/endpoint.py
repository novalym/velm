# Path: core/lsp/base/protocol/endpoint.py
# ----------------------------------------


import logging
import threading
import json
import time
import errno
import uuid
import sys
import traceback
from typing import Optional, Callable, Any, Dict, List, Union, BinaryIO

# --- GNOSTIC INTERNAL UPLINKS ---
from .framing import KineticBuffer
from .streams import LspStream, StdioStream
from .telemetry import ProtocolTelemetry
from .constants import DEFAULT_CHUNK_SIZE, SILENT_METHODS
from ..rpc import (
    Request, Response, Notification, JsonRpcMessage,
    MessageConverter, GnosticSerializer,
    JsonRpcError, ErrorCodes
)

Logger = logging.getLogger("JsonRpcEndpoint")


class JsonRpcEndpoint:
    """
    =============================================================================
    == THE HYDRODYNAMIC GOVERNOR (V-Ω-TOTALITY-V12-RAW)                        ==
    =============================================================================
    LIF: INFINITY | ROLE: TRANSPORT_ORCHESTRATOR

    The Supreme Orchestrator of the binary siphon. It manages the lifecycle
    of the connection, transmuting raw bytes from the OS Pipe into Gnostic Intent.

    [ASCENSION]: Hardened to handle raw OS Reads and emit First Breath Telemetry.
    """

    def __init__(
            self,
            reader: Optional[BinaryIO] = None,
            writer: Optional[BinaryIO] = None,
            stream: Optional[LspStream] = None,
            traffic_logger: Optional[Callable[[Dict, str], None]] = None
    ):
        """
        [THE POLYMORPHIC CONSTRUCTOR]
        Directly addresses the 'server.py' call-site while preserving the
        higher-level stream abstraction.
        """
        # [ASCENSION 1]: STREAM RESOLUTION
        if stream:
            self.stream = stream
        else:
            # We wrap the provided (or default) buffers in the Stdio conduit
            self.stream = StdioStream(reader=reader, writer=writer)

        self.telemetry = ProtocolTelemetry(transport_type=self.stream.name())
        self.buffer = KineticBuffer(self.telemetry)
        self.traffic_logger = traffic_logger
        self.running = False

        self.on_request: Optional[Callable[[Request], Any]] = None
        self.on_notification: Optional[Callable[[Notification], None]] = None
        self.on_response: Optional[Callable[[Response], None]] = None

        self._write_lock = threading.RLock()

    def start(self):
        """
        [THE RITE OF COMMUNION]
        Enters the eternal read loop. This call blocks the calling thread.
        """
        self.running = True
        self.telemetry.is_connected = True

        # [ASCENSION 2]: PROCLAIM VITALITY TO STDERR
        # This is the signal Electron looks for to confirm the Python process didn't die on import.
        sys.stderr.write(f"[Endpoint] 🟢 Neural Siphon Active: {self.stream.name()}\n")
        sys.stderr.flush()

        try:
            while self.running:
                # 1. PROCESS ACCUMULATED MATTER
                # Loop until the KineticBuffer is exhausted of complete messages
                # This handles "Packet Coalescence" where multiple JSONs arrive in one read.
                while True:
                    msg_bytes = self.buffer.extract_message()
                    if not msg_bytes:
                        break
                    self._ingest_matter(msg_bytes)

                # 2. READ NEW MATTER FROM THE VOID
                try:
                    chunk = self.stream.read(DEFAULT_CHUNK_SIZE)
                except (IOError, OSError) as e:
                    # Handle "Interrupted System Call" (EINTR) which occurs under heavy load
                    if getattr(e, 'errno', None) == errno.EINTR:
                        continue
                    Logger.error(f"Hardware Pipe Fracture: {e}")
                    break

                # [ASCENSION 3]: EOF HANDLING
                if chunk is None:
                    sys.stderr.write("[Endpoint] Input stream reached Absolute Zero (EOF). Reality Dissolving.\n")
                    Logger.info("Input stream reached Absolute Zero (EOF).")
                    break

                # [ASCENSION 4]: NON-BLOCKING YIELD
                # If using non-blocking I/O, we might get empty bytes. Sleep to save CPU.
                if chunk == b"":
                    time.sleep(0.001)
                    continue

                # [ASCENSION 5]: FIRST BREATH TELEMETRY
                # If we see the Header, we know the Bridge works.
                if b"Content-Length" in chunk:
                    # Determine size for logging
                    size = len(chunk)
                    # Only log the first few handshakes to avoid spam
                    if self.telemetry.msgs_in < 5:
                        sys.stderr.write(f"[Endpoint] ⚡ Received Header Frame ({size} bytes)\n")
                        sys.stderr.flush()

                # Update Telemetry and Feed the Buffer
                self.telemetry.bytes_in += len(chunk)
                self.buffer.feed(chunk)

        except Exception as catastrophic_failure:
            self.telemetry.errors += 1
            sys.stderr.write(f"[Endpoint] 💥 Layer Collapse: {catastrophic_failure}\n")
            traceback.print_exc(file=sys.stderr)
            Logger.critical(f"Endpoint Layer Collapse: {catastrophic_failure}", exc_info=True)
        finally:
            self.stop()

    def _ingest_matter(self, data: bytes):
        """
        [THE TRANSMUTATION RITE - TRACED]
        """
        start_ns = time.perf_counter_ns()
        try:
            raw = GnosticSerializer.decode(data)

            # [FORENSIC]: Log every incoming method and its ID
            if isinstance(raw, dict):
                method = raw.get('method', 'response')
                req_id = raw.get('id', 'notif')
                sys.stderr.write(f"[Endpoint:IN] 📥 Method: {method} | ID: {req_id} | Size: {len(data)}b\n")
                sys.stderr.flush()

            msg = MessageConverter.from_dict(raw)
            if isinstance(raw, list):
                for item in msg: self._dispatch_one(item)
            else:
                self._dispatch_one(msg)

            self.telemetry.msgs_in += 1
        except Exception as e:
            sys.stderr.write(f"[Endpoint:ERR] 💥 Ingestion Fracture: {e}\n")
            sys.stderr.flush()
            self.telemetry.errors += 1



    def _dispatch_one(self, msg: JsonRpcMessage):
        """Routes a single model to its consecrated handler."""
        if isinstance(msg, Request):
            if self.on_request: self.on_request(msg)
        elif isinstance(msg, Notification):
            if self.on_notification: self.on_notification(msg)
        elif isinstance(msg, Response):
            if self.on_response: self.on_response(msg)

    # =========================================================================
    # == TRANSMISSION RITES (EGRESS)                                         ==
    # =========================================================================

    def send_response(self, req_id: Any, result: Any = None, error: Any = None, trace_id: Optional[str] = None):
        """
        [THE RITE OF REVELATION]
        Transmits a response, surgically injecting causality markers.
        """
        if error:
            if isinstance(error, JsonRpcError):
                resp = error.to_response(req_id)
            else:
                # [THE FIX]: Use build_error
                resp = Response.build_error(req_id, ErrorCodes.INTERNAL_ERROR, str(error))
        else:
            # [THE FIX]: Use build_success
            # [ASCENSION 8]: CAUSAL TRACE PROPAGATION
            resp = Response.build_success(req_id, result, trace_id)

        self._send(resp)

    def send_notification(self, method: str, params: Any):
        """Projects a fire-and-forget signal across the void."""
        notif = Notification(method=method, params=params)
        self._send(notif)

    def send_request(self, method: str, params: Any, req_id: Optional[Any] = None):
        """Summons a request from the Server to the Client."""
        rid = req_id if req_id is not None else f"srv-{uuid.uuid4().hex[:6]}"
        req = Request(id=rid, method=method, params=params)
        self._send(req)

    def _send(self, msg: Any):
        """
        [THE ATOMIC WRITE - TRACED]
        """
        try:
            body = GnosticSerializer.encode(msg)
            length = len(body)
            header = f"Content-Length: {length}\r\n\r\n".encode("ascii")

            # [FORENSIC]: Log exactly what we are pushing back to Monaco
            method = getattr(msg, 'method', 'response')
            sys.stderr.write(f"[Endpoint:OUT] 📤 Sending: {method} | Size: {length}b\n")
            sys.stderr.flush()

            with self._write_lock:
                self.stream.write(header + body)
            self.telemetry.bytes_out += (len(header) + length)
            self.telemetry.msgs_out += 1
        except Exception as e:
            sys.stderr.write(f"[Endpoint:ERR] 💥 Egress Fracture: {e}\n")
            sys.stderr.flush()

    def send_raw(self, msg: Dict[str, Any]):
        """
        =============================================================================
        == THE RAW INJECTION PORT (V-Ω-HYDRODYNAMIC-EGRESS)                        ==
        =============================================================================
        LIF: 100x | Dispatches a pre-forged Gnostic response directly to the
        physical stream, bypassing standard high-level validation for maximum speed.
        """
        self._send(msg)

    def stop(self):
        """
        [THE FINAL RELEASE]
        Dissolves the reality and releases all physical handles.
        """
        with self._write_lock:
            if not self.running:
                return
            self.running = False
            self.telemetry.is_connected = False

            try:
                self.stream.close()
                sys.stderr.write("[Endpoint] 🔒 Neural Siphon Sealed.\n")
            except:
                pass