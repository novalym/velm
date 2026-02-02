# Path: scaffold/core/daemon/transporter/buffer.py
# ------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_BUFFER_PYTHON_TYPE_SAFE_V999
# SYSTEM: KINETIC_STORAGE | ROLE: MEMORY_VESSEL
# =================================================================================
# == THE KINETIC BUFFER (V-Ω-HYDRODYNAMIC-TYPE-SAFE)                             ==
# =================================================================================

import logging
from typing import Optional, Dict, Any
from .constants import (
    HEADER_TERMINATOR,
    HEADER_REGEX,
    MAX_PAYLOAD_SIZE,
    BUFFER_SAFETY_CAP,
    PARANOID_LOGGING
)

Logger = logging.getLogger("KineticBuffer")


class KineticBuffer:
    """
    The High-Performance Memory Vessel (Python Edition).
    Wraps a mutable `bytearray` with safety valves and forensic instrumentation.
    Strictly handles bytes/bytearray types to prevent TypeError fractures.
    """
    __slots__ = ['_data', '_expected_length', '_total_ingested', '_peak_size', '_resync_count']

    def __init__(self):
        self._data = bytearray()
        self._expected_length: Optional[int] = None
        self._total_ingested = 0
        self._peak_size = 0
        self._resync_count = 0

    def feed(self, chunk: bytes):
        """
        [RITE OF INGESTION]
        Adds raw matter to the vessel. Safe against overflows.
        """
        try:
            if not chunk: return

            self._data.extend(chunk)
            self._total_ingested += len(chunk)

            current_len = len(self._data)
            if current_len > self._peak_size:
                self._peak_size = current_len

            # [ASCENSION 4]: FLOOD GATE PROTECTION
            if current_len > BUFFER_SAFETY_CAP:
                # If we are not tracking a body, and we have no header, we are drowning.
                # HEADER_TERMINATOR is bytes, _data is bytearray. Safe.
                if self._expected_length is None and HEADER_TERMINATOR not in self._data:
                    if PARANOID_LOGGING:
                        Logger.critical(f"🌊 Buffer Flood ({current_len} bytes). Resynchronizing.")
                    self._perform_resync()

        except Exception as e:
            Logger.error(f"FEED FRACTURE: {e}")
            self.clear()

    def try_extract_frame(self) -> Optional[bytes]:
        """
        [RITE]: EXTRACT_LSP_FRAME
        Attempts to slice a valid LSP message from the buffer.
        Returns bytes if successful, None if hungry.
        """
        try:
            # PHASE 1: HEADER RESOLUTION
            if self._expected_length is None:
                # HEADER_TERMINATOR is b'\r\n\r\n'. Safe for bytearray.find().
                sep_index = self._data.find(HEADER_TERMINATOR)

                if sep_index == -1:
                    return None  # Hunger

                # Decode Header (ASCII)
                try:
                    # Slice is a bytearray, decode turns it to str for logging/regex
                    header_bytes = self._data[:sep_index]

                    # Regex search on BYTES (rb'...')
                    match = HEADER_REGEX.search(header_bytes)
                except Exception:
                    if PARANOID_LOGGING: Logger.warning("Header Analysis Failed. Resyncing.")
                    self._perform_resync(skip_to=sep_index + 4)
                    return None

                if not match:
                    if PARANOID_LOGGING: Logger.warning("Header missing Content-Length. Resyncing.")
                    self._perform_resync(skip_to=sep_index + 4)
                    return self.try_extract_frame()  # Recursive check

                try:
                    # match.group(1) returns bytes, int() handles bytes correctly
                    content_len = int(match.group(1))
                except ValueError:
                    self._perform_resync()
                    return None

                if content_len < 0 or content_len > MAX_PAYLOAD_SIZE:
                    Logger.error(f"Profane Content-Length {content_len}. Purging.")
                    self._perform_resync()
                    return None

                self._expected_length = content_len

                # Slide Buffer past Header (O(n) memmove in CPython)
                # +4 for len(b'\r\n\r\n')
                del self._data[:sep_index + 4]

            # PHASE 2: BODY EXTRACTION
            if self._expected_length is not None:
                if len(self._data) >= self._expected_length:
                    # Extract Payload (Copy to bytes to make it immutable)
                    payload = bytes(self._data[:self._expected_length])

                    # Slide Buffer past Body
                    del self._data[:self._expected_length]

                    # Reset State
                    self._expected_length = None

                    return payload

            return None  # Wait for more mass

        except Exception as e:
            Logger.error(f"FRAME EXTRACT FRACTURE: {e}")
            self._perform_resync()
            return None

    def try_extract_raw_json(self) -> Optional[bytes]:
        """
        [RITE]: EXTRACT_RAW_DIALECT
        Attempts to find a newline-delimited JSON object.
        """
        try:
            # Search for byte newline
            newline_idx = self._data.find(b'\n')

            if newline_idx != -1:
                # Extract the line
                line = self._data[:newline_idx]

                # Advance buffer past newline
                del self._data[:newline_idx + 1]

                # Check for JSON signature '{' (ASCII 123)
                # Stripping whitespace from bytes
                stripped = line.strip()
                if stripped and stripped[0] == 123:
                    return bytes(stripped)

                # If it's garbage, we consumed it. Return None.
                return None

            return None  # Wait for newline
        except Exception:
            return None

    def peek_byte(self) -> int:
        """
        Returns the integer value of the first byte (0-255) or -1 if empty.
        Safe for comparison with ASCII integers.
        """
        if not self._data: return -1
        return self._data[0]  # bytearray indexing returns int

    def _perform_resync(self, skip_to: int = 0):
        """Aggressively discards data until a new Header boundary is found."""
        self._resync_count += 1

        # If specific skip requested
        if skip_to > 0:
            del self._data[:skip_to]
            self._expected_length = None
            return

        # Search for next terminator
        next_header = self._data.find(HEADER_TERMINATOR)
        if next_header != -1:
            # Jump to start of next header
            del self._data[:next_header]
            self._expected_length = None
        else:
            # If no header found in entire buffer, nuke everything.
            self.clear()

    def clear(self):
        del self._data[:]
        self._expected_length = None

    def has_data(self) -> bool:
        return len(self._data) > 0

    @property
    def metrics(self) -> Dict[str, Any]:
        return {
            "ingested": self._total_ingested,
            "peak": self._peak_size,
            "resyncs": self._resync_count,
            "current": len(self._data)
        }