# Path: core/lsp/protocol/streams.py
# ----------------------------------
# LIF: INFINITY | ROLE: PHYSICAL_IO_ABSTRACTION | RANK: SOVEREIGN
# AUTH_CODE: Ω_STREAMS_FD_LEVEL_V100
# =================================================================================

import sys
import os
import socket
import errno
import time
from abc import ABC, abstractmethod
from typing import Optional, BinaryIO, Any, Union

import logging

Logger = logging.getLogger("GnosticStream")


class LspStream(ABC):
    """
    =============================================================================
    == THE CONDUIT COVENANT (V-Ω-ABSTRACT-PHYSICS)                             ==
    =============================================================================
    The abstract contract that all physical transport mechanisms must sign.
    Ensures the high-level protocol is agnostic to the medium of transmission.
    """

    @abstractmethod
    def read(self, size: int) -> Optional[bytes]:
        """
        Reads raw binary matter from the siphon.
        Returns bytes if successful, None if the reality has dissolved (EOF).
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """
        Inscribes raw binary matter into the outgoing stream.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Seals the conduit and releases all associated physical handles.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """The Gnostic identity of this transport mechanism."""
        pass


class StdioStream(LspStream):
    """
    =============================================================================
    == THE RAW DESCRIPTOR CONDUIT (V-Ω-KERNEL-IO)                              ==
    =============================================================================
    [THE FIX]: Bypasses Python's `io.BufferedReader` / `TextIOWrapper`.
    Interacts directly with the OS File Descriptors (FD 0 and FD 1).

    This annihilates the "Buffer Bloat" and "CRLF Corruption" heresies on Windows.
    """

    def __init__(self, reader: Optional[BinaryIO] = None, writer: Optional[BinaryIO] = None):
        """
        Consecrates the Stdio conduit.
        Resolves the raw File Descriptors immediately.
        """
        try:
            # [ASCENSION 1]: RESOLVE FILE DESCRIPTORS
            # We capture the integer FDs. This is the lowest level of access.
            self._fd_in = reader.fileno() if reader else sys.stdin.fileno()
            self._fd_out = writer.fileno() if writer else sys.stdout.fileno()

            # [ASCENSION 2]: WINDOWS BINARY FORCE (REDUNDANT SAFEGUARD)
            # We re-assert binary mode at the FD level just to be absolutely safe,
            # in case the Bootloader's magic was undone by a library import.
            if sys.platform == "win32":
                import msvcrt
                try:
                    msvcrt.setmode(self._fd_in, os.O_BINARY)
                    msvcrt.setmode(self._fd_out, os.O_BINARY)
                except Exception as e:
                    # Non-fatal if already set, but worth logging to stderr for forensics
                    sys.stderr.write(f"[StdioStream] Binary Force-Set Warning: {e}\n")

        except Exception as fracture:
            Logger.critical(f"Stdio Inception Fracture: {fracture}")
            raise

    def read(self, size: int) -> Optional[bytes]:
        """
        [THE RAW SIPHON]
        Reads directly from the kernel pipe via `os.read`.
        This is unbuffered and blocks until data is available or EOF.
        """
        try:
            while True:
                try:
                    # os.read returns bytes directly from the kernel buffer.
                    # It does not wait to fill the buffer; it returns what is available.
                    chunk = os.read(self._fd_in, size)

                    if not chunk:
                        return None  # EOF (Pipe Closed)

                    return chunk

                except OSError as e:
                    # [ASCENSION 5]: INTERRUPT HANDLING
                    if e.errno == errno.EINTR:
                        continue  # Syscall interrupted, retry immediately
                    if e.errno == errno.EAGAIN:
                        return b""  # Non-blocking mode, no data yet
                    raise

        except Exception as e:
            Logger.error(f"Stdio Read Fracture: {e}")
            return None

    def write(self, data: bytes) -> None:
        """
        [THE RAW INSCRIPTION]
        Writes directly to the kernel pipe via `os.write`.
        Ensures atomic delivery via loop.
        """
        try:
            total_sent = 0
            to_send = len(data)

            # [ASCENSION 3]: ATOMIC WRITE LOOP
            while total_sent < to_send:
                try:
                    sent = os.write(self._fd_out, data[total_sent:])
                    if sent == 0:
                        raise IOError("Socket connection broken (Zero Write)")
                    total_sent += sent
                except OSError as e:
                    if e.errno == errno.EINTR:
                        continue
                    if e.errno == errno.EPIPE:
                        # [ASCENSION 6]: BROKEN PIPE IMMUNITY
                        # Client disconnected. We stop writing and return.
                        Logger.debug("Output pipe severed by host (EPIPE).")
                        return
                    raise

        except Exception as e:
            Logger.error(f"Stdio Write Fracture: {e}")
            raise

    def close(self) -> None:
        """[THE SEAL]"""
        # We generally don't close stdio FDs as it kills the process interaction,
        # but we can flush python-level buffers just in case something else wrote to them.
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except:
            pass

    def name(self) -> str:
        return "Stdio(FD)"


class SocketStream(LspStream):
    """
    [TCP/IP SOCKET]
    Used for Daemon mode, Remote Development, or Forensic Debugging.
    """

    def __init__(self, sock: socket.socket):
        self._sock = sock
        # [ASCENSION 8]: SOCKET PHYSICS TUNING
        try:
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except:
            pass

    def read(self, size: int) -> Optional[bytes]:
        try:
            chunk = self._sock.recv(size)
            return chunk if chunk else None
        except socket.timeout:
            return b""  # Treat timeout as empty, not EOF
        except OSError as e:
            Logger.debug(f"Socket Siphon Fracture: {e}")
            return None

    def write(self, data: bytes) -> None:
        try:
            self._sock.sendall(data)
        except OSError as e:
            if e.errno in (errno.EPIPE, errno.ECONNRESET):
                return
            raise

    def close(self) -> None:
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
        except:
            pass

    def name(self) -> str:
        try:
            return f"TCP:{self._sock.getpeername()}"
        except:
            return "TCP:Disconnected"


class MemoryStream(LspStream):
    """
    [THE ETHEREAL VESSEL]
    A pure-memory stream for simulation, testing, and inter-thread rites.
    """

    def __init__(self):
        self._input = bytearray()
        self._output = bytearray()
        self._closed = False

    def feed_simulated_input(self, data: bytes):
        """Allows tests to inject matter into the siphon."""
        self._input.extend(data)

    def get_simulated_output(self) -> bytes:
        """Allows tests to read the result of inscriptions."""
        out = bytes(self._output)
        self._output.clear()
        return out

    def read(self, size: int) -> Optional[bytes]:
        if self._closed: return None
        if not self._input: return b""

        chunk = self._input[:size]
        del self._input[:size]
        return bytes(chunk)

    def write(self, data: bytes) -> None:
        if self._closed: return
        self._output.extend(data)

    def close(self) -> None:
        self._closed = True

    def name(self) -> str:
        return "EtherealMemory"


# =================================================================================
# == THE UNIVERSAL CONDUIT FACTORY                                               ==
# =================================================================================

def forge_stream(mode: str = "stdio", connection: Any = None) -> LspStream:
    """
    [THE RITE OF FORGING]
    Creates the appropriate conduit based on the requested reality mode.
    """
    if mode == "socket":
        # Ensure it's a socket before wrapping
        if isinstance(connection, socket.socket):
            return SocketStream(connection)
        raise ValueError("Forge Error: Socket mode requires a valid socket object.")

    if mode == "memory":
        return MemoryStream()

    return StdioStream()