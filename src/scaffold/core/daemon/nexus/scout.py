# Path: core/daemon/nexus/scout.py
# --------------------------------
# LIF: INFINITY | ROLE: NETWORK_BINDER
import socket
from ..constants import MAX_CONNECTIONS
from ....logger import Scribe

Logger = Scribe("NexusScout")


class Scout:
    """
    [THE PATHFINDER]
    Locates a harmonic frequency (Port) and establishes the physical binding.
    """

    @staticmethod
    def bind(host: str, start_port: int, max_retries: int = 10) -> socket.socket:
        """
        Attempts to bind a socket. If the port is contested, it iterates upwards.
        Returns the bound socket.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        current_port = start_port

        for i in range(max_retries):
            try:
                sock.bind((host, current_port))
                sock.listen(MAX_CONNECTIONS)
                return sock
            except OSError:
                if i == max_retries - 1:
                    Logger.critical(f"Port range {start_port}-{current_port} fully contested.")
                    raise
                Logger.warn(f"Port {current_port} occupied. Shifting frequency...")
                current_port += 1

        return sock  # Should be unreachable due to raise

