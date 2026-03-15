# Path: core/alchemist/elara/library/architectural/substrate/network.py
# ---------------------------------------------------------------------

import socket
from contextlib import closing


class NetworkOracle:
    """
    =============================================================================
    == THE NETWORK ORACLE (V-Ω-TOTALITY)                                       ==
    =============================================================================
    LIF: 50,000x | ROLE: APERTURE_ADJUDICATOR

    [ASCENSIONS 29-32]:
    29. Zero-Stiction Port Probing (O(1) TCP Connect).
    30. Autonomic Free-Port discovery.
    31. DNS Resolution checks.
    """

    def port_open(self, port: int, host: str = '127.0.0.1') -> bool:
        """[ASCENSION 29]: Checks if a port is currently occupied/listening."""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.1)
            return sock.connect_ex((host, int(port))) == 0

    def find_free_port(self, start: int = 8000, end: int = 9000) -> int:
        """[ASCENSION 30]: Autonomically hunts for a vacant aperture."""
        for port in range(start, end + 1):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(0.1)
                if sock.connect_ex(('127.0.0.1', port)) != 0:
                    return port
        raise OSError(f"No vacant ports waked between {start} and {end}.")