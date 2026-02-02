# Path: scaffold/core/runtime/remote.py
# -----------------------------------------

import base64
import json
import os
import queue
import re
import socket
import ssl
import struct
import sys
import threading
import time
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

from ...contracts.heresy_contracts import ArtisanHeresy, Heresy
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import BaseRequest
from ...logger import Scribe

Logger = Scribe("RemoteEngine")

# --- THE GNOSTIC PROTOCOL CONSTANTS ---
PROTOCOL_VERSION = "2.2.0"
HEADER_FORMAT = "!I"  # Network byte order, unsigned int (4 bytes) for length
HEADER_SIZE = 4
COMPRESSION_THRESHOLD = 1024  # Compress if payload > 1KB


@dataclass
class BridgeTelemetry:
    """The pulse of the connection."""
    bytes_sent: int = 0
    bytes_received: int = 0
    compression_ratio: float = 0.0
    latency_ms: float = 0.0
    start_time: float = field(default_factory=time.time)


class RemoteEngine:
    """
    =================================================================================
    == THE CELESTIAL CLIENT (V-Ω-TELEPATHIC-JUGGERNAUT)                            ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Gnostic Bridge between the Architect's Terminal and the Remote Daemon.
    It handles Compression, Encryption, Multiplexing, and Artifact Teleportation.
    """

    def __init__(
            self,
            output_handler: Optional[Callable[[str], None]] = None,
            ssl_context: Optional[ssl.SSLContext] = None,
            telemetry_enabled: bool = True
    ):
        self.socket: Optional[socket.socket] = None
        self.output_handler = output_handler or self._default_handler
        self.ssl_context = ssl_context
        self.telemetry = BridgeTelemetry() if telemetry_enabled else None
        self._stop_event = threading.Event()
        self._input_queue: queue.Queue = queue.Queue()
        self._heartbeat_thread: Optional[threading.Thread] = None

    def _default_handler(self, content: str):
        """The Humble Scribe for standard output."""
        print(content)

    def connect(self, uri: str, retries: int = 3):
        """
        [ELEVATION 2 & 3] THE LAZARUS CONNECTION
        Establishes a secure bridge with exponential backoff.
        Format: host:port
        """
        host, port_str = uri.split(":")
        port = int(port_str)

        attempt = 0
        while attempt <= retries:
            try:
                raw_socket = socket.create_connection((host, port), timeout=10.0)

                # [ELEVATION 2] The Celestial Shield
                if self.ssl_context:
                    self.socket = self.ssl_context.wrap_socket(raw_socket, server_hostname=host)
                    Logger.info(f"Secure Celestial Bridge forged to [cyan]{host}:{port}[/cyan] 🔒")
                else:
                    self.socket = raw_socket
                    Logger.info(f"Plaintext Bridge forged to [cyan]{host}:{port}[/cyan]")

                self.socket.settimeout(None)  # Blocking mode for the stream

                # [ELEVATION 10] The Heartbeat Sentinel
                self._start_heartbeat()
                return

            except (socket.error, ssl.SSLError) as e:
                attempt += 1
                if attempt > retries:
                    raise ArtisanHeresy(f"Bridge collapse. Could not connect to {uri} after {retries} attempts: {e}")

                backoff = 0.5 * (2 ** (attempt - 1))
                Logger.warn(f"Connection failed ({e}). Retrying in {backoff:.1f}s...")
                time.sleep(backoff)

    def dispatch(self, request: BaseRequest) -> ScaffoldResult:
        """
        [THE GRAND RITE OF PROJECTION]
        Serializes, Compresses, Transmits, and Listens.
        """
        if not self.socket:
            raise ArtisanHeresy("No active bridge.")

        try:
            # 1. The Rite of Identification (Gnostic Handshake)
            command_name = request.__class__.__name__.replace("Request", "").lower()
            if command_name == "run": command_name = "run"

            payload = {
                "jsonrpc": "2.0",
                "method": command_name,
                "params": request.model_dump(mode='json'),
                "meta": {
                    "version": PROTOCOL_VERSION,
                    "client": "scaffold-cli",
                    "features": ["compression", "streaming", "artifacts"]
                },
                "id": f"req-{int(time.time())}"
            }

            # 2. The Rite of Transmission (Compressed)
            self._send_packet(payload)

            # 3. [ELEVATION 5] The Neural Bridge (Input Thread)
            # Starts a thread to read stdin and push to socket if interactive
            if not request.non_interactive:
                # self._start_input_forwarding()
                # (Placeholder: Requires raw mode handling on client side)
                pass

            # 4. The Telepathic Loop
            return self._listen_for_revelation()

        except KeyboardInterrupt:
            # [ELEVATION 9] The Graceful Sigil
            Logger.warn("Severing link... Sending termination sigil to remote.")
            try:
                self._send_packet({"method": "signal", "params": {"signal": "SIGINT"}})
                # Wait briefly for remote ack or logs
                time.sleep(0.5)
            except:
                pass
            return ScaffoldResult(success=False, message="Interrupted by Architect.")

        except Exception as e:
            raise ArtisanHeresy(f"Remote dispatch failed: {e}")
        finally:
            self._close()

    def _send_packet(self, data: Dict[str, Any]):
        """
        [ELEVATION 1 & 12] THE ATOMIC TRANSMITTER
        Handles JSON serialization, Zlib compression, and Length-Prefix framing.
        """
        json_bytes = json.dumps(data).encode('utf-8')

        # Compression decision
        is_compressed = False
        if len(json_bytes) > COMPRESSION_THRESHOLD:
            json_bytes = zlib.compress(json_bytes)
            is_compressed = True

        # Header: [Length (4 bytes)][Flags (1 byte)]
        # Flags: 0x01 = Compressed
        flags = 0x01 if is_compressed else 0x00

        # Use struct for binary packing: I (unsigned int), B (unsigned char)
        header = struct.pack("!IB", len(json_bytes), flags)

        self.socket.sendall(header + json_bytes)

        if self.telemetry:
            self.telemetry.bytes_sent += len(header) + len(json_bytes)

    def _listen_for_revelation(self) -> ScaffoldResult:
        """
        [THE PRISM OF RECEPTION]
        Demultiplexes the incoming stream into Logs, Artifacts, Progress, and Results.
        """
        while not self._stop_event.is_set():
            # 1. Read Header (5 bytes)
            header_data = self._recv_exact(5)
            if not header_data:
                raise ArtisanHeresy("Connection severed by remote.")

            length, flags = struct.unpack("!IB", header_data)
            is_compressed = bool(flags & 0x01)

            # 2. Read Body
            body_data = self._recv_exact(length)
            if not body_data:
                raise ArtisanHeresy("Connection severed during payload transmission.")

            if self.telemetry:
                self.telemetry.bytes_received += 5 + length

            # 3. Decompress
            if is_compressed:
                body_data = zlib.decompress(body_data)

            # 4. Deserialize
            try:
                message = json.loads(body_data)
            except json.JSONDecodeError:
                Logger.warn("Received profane (malformed) Gnosis.")
                continue

            # 5. The Prism (Routing)
            msg_type = message.get("type", "unknown")

            if msg_type == "log":
                # [ELEVATION 5] Multiplexed Output
                content = message.get("content", "")
                stream = message.get("stream", "stdout")
                # We could style stderr differently here
                self.output_handler(content)

            elif msg_type == "progress":
                # [ELEVATION 11] The Progress Proxy
                # Forward to a local progress bar handler if implemented
                # For now, we log it nicely
                # self.output_handler(f"[PROGRESS] {message.get('desc')} {message.get('percent')}%")
                pass

            elif msg_type == "artifact":
                # [ELEVATION 6] The Artifact Teleporter
                self._materialize_artifact(message)

            elif msg_type == "pong":
                # [ELEVATION 7] Chronometric Sync
                if self.telemetry:
                    rtt = (time.time() - message.get("sent_at", 0)) * 1000
                    self.telemetry.latency_ms = rtt
                    # Logger.verbose(f"Heartbeat RTT: {rtt:.2f}ms")

            elif msg_type == "result":
                # The Final Proclamation
                success = message.get("success", False)
                return ScaffoldResult(
                    success=success,
                    message=message.get("message", ""),
                    data=message.get("data"),
                    heresies=[Heresy(**h) for h in message.get("heresies", [])],
                    artifacts=message.get("artifacts", [])
                )

            elif msg_type == "error":
                raise ArtisanHeresy(f"Remote Protocol Error: {message.get('message')}")

    def _materialize_artifact(self, message: Dict[str, Any]):
        """[ELEVATION 6] Downloads a file from the stream."""
        path = message.get("path")
        content_b64 = message.get("content")
        try:
            local_path = Path(os.getcwd()) / path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            data = base64.b64decode(content_b64)
            local_path.write_bytes(data)
            Logger.success(f"Teleported artifact: {path}")
        except Exception as e:
            Logger.error(f"Failed to materialize artifact {path}: {e}")

    def _recv_exact(self, n: int) -> Optional[bytes]:
        """Helper to read exactly n bytes."""
        data = b""
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet: return None
            data += packet
        return data

    def _start_heartbeat(self):
        """[ELEVATION 10] The Sentinel that keeps the TCP state alive."""

        def _beat():
            while not self._stop_event.is_set():
                time.sleep(15)
                try:
                    if self.socket:
                        self._send_packet({"method": "ping", "sent_at": time.time()})
                except:
                    break

        self._heartbeat_thread = threading.Thread(target=_beat, daemon=True)
        self._heartbeat_thread.start()

    def _close(self):
        """The Rite of Closing."""
        self._stop_event.set()
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except:
                pass
        if self.telemetry:
            Logger.verbose(
                f"Celestial Bridge Closed. Sent: {self.telemetry.bytes_sent}B, Recv: {self.telemetry.bytes_received}B")