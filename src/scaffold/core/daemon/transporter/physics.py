# Path: scaffold/core/daemon/transporter/physics.py
# -------------------------------------------------
# LIF: INFINITY
# =================================================================================
# == THE MECHANIC (KERNEL TUNER - SHIELDED)                                      ==
# =================================================================================

import socket
import logging
from .constants import KERNEL_BUFFER_SIZE

Logger = logging.getLogger("SocketPhysics")

class SocketPhysics:
    """
    [THE SPEED OF LIGHT RITE]
    Applies low-level kernel optimizations to the raw socket file descriptor.
    Ensures the OS TCP stack is tuned for high-frequency RPC bursts.
    """

    @staticmethod
    def tune(sock: socket.socket):
        try:
            # 1. ANNIHILATE NAGLE'S ALGORITHM
            # We want packets sent NOW, not batched.
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # 2. EXPAND THE LUNGS (Kernel Buffers)
            # Increase Kernel Send/Recv Buffers to prevent syscall blocking.
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, KERNEL_BUFFER_SIZE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, KERNEL_BUFFER_SIZE)

            # 3. DETECT GHOSTS (Keep-Alive)
            # Detect severed links from crashed clients immediately.
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # 4. PLATFORM SPECIFICS (Linux/Mac Tuning)
            if hasattr(socket, 'TCP_KEEPIDLE'):
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            if hasattr(socket, 'TCP_KEEPINTVL'):
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
            if hasattr(socket, 'TCP_KEEPCNT'):
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

            # [ASCENSION]: Quick-Close
            # Allow address reuse immediately after close (prevents ADDRINUSE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        except Exception as e:
            # Physics failure is non-critical, we proceed with standard laws.
            Logger.warning(f"Physics Tuning Minor Fracture: {e}")