# Path: core/lsp/protocol/framing.py
# ----------------------------------

import logging
from typing import Optional
from .constants import HEADER_TERMINATOR, CONTENT_LENGTH_RE, MAX_PAYLOAD_SIZE
from .telemetry import ProtocolTelemetry

Logger = logging.getLogger("LspFraming")


class KineticBuffer:
    """
    [THE HYDRODYNAMIC VESSEL]
    A specialized byte-buffer that handles stream fragmentation,
    header parsing, and memory management with Zero-Copy intent.

    It implements a 'Slicing Rite' that consumes bytes from the front
    while appending to the back.
    """

    def __init__(self, telemetry: ProtocolTelemetry):
        self._buffer = bytearray()
        self._needed = -1  # -1 = Header Hunt, >0 = Body Hunt
        self.telemetry = telemetry

    def feed(self, chunk: bytes):
        """Ingests raw matter into the vessel."""
        self._buffer.extend(chunk)

        # [ASCENSION 1]: Peak Memory Tracking
        current_len = len(self._buffer)
        if current_len > self.telemetry.buffer_peak:
            self.telemetry.buffer_peak = current_len

    def has_data(self) -> bool:
        return len(self._buffer) > 0

    def extract_message(self) -> Optional[bytes]:
        """
        [THE SLICING RITE]
        Attempts to extract a full JSON-RPC message.
        Returns bytes if successful, None if hungry.
        """
        # PHASE 1: HEADER HUNT
        if self._needed == -1:
            header_end = self._buffer.find(HEADER_TERMINATOR)

            # If no header found yet
            if header_end == -1:
                # [SAFETY]: Sanity check buffer size to prevent infinite growth
                # If we have > 8KB of header data and still no terminator, it's garbage.
                if len(self._buffer) > 8192:
                    Logger.warning("Buffer overflow seeking header. Resyncing.")
                    self.telemetry.resyncs += 1
                    # Discard first 4KB to try and find alignment
                    del self._buffer[:4096]
                return None

                # Slice header (Zero-copy logic would use memoryview, but for headers bytearray is fast enough)
            header_bytes = self._buffer[:header_end]

            # Parse Content-Length
            match = CONTENT_LENGTH_RE.search(header_bytes)

            if not match:
                # [ASCENSION 4]: LAZARUS HEADER RESYNC
                # Malformed header. Discard up to terminator and retry.
                Logger.warning("Protocol Anomaly: Malformed Header. Resyncing stream.")
                self.telemetry.resyncs += 1
                del self._buffer[:header_end + 4]
                return self.extract_message()  # Recursive retry

            try:
                content_len = int(match.group(1))
            except ValueError:
                self.telemetry.errors += 1
                del self._buffer[:header_end + 4]
                return self.extract_message()

            # [ASCENSION 3]: MASS DENSITY GUARD
            if content_len > MAX_PAYLOAD_SIZE:
                Logger.error(f"Heresy: Payload mass ({content_len}b) exceeds threshold. Purging.")
                self.telemetry.errors += 1
                # Purge everything up to the next likely header or just flush
                del self._buffer[:header_end + 4]
                self._buffer.clear()  # Nuclear option for safety
                return None

            # Header processed. Remove it.
            del self._buffer[:header_end + 4]
            self._needed = content_len

        # PHASE 2: BODY HUNT
        if self._needed > 0:
            if len(self._buffer) >= self._needed:
                # Extract Body
                payload = bytes(self._buffer[:self._needed])  # Immutable copy
                # Remove Body
                del self._buffer[:self._needed]
                # Reset State
                self._needed = -1
                return payload

        return None  # Hunger: Need more body bytes