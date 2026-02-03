# Path: scaffold/artisans/shadow_clone/network.py
# -----------------------------------------------
# LIF: 10,000,000 // AUTH_CODE: @)!((!@)() // NETWORK_SOVEREIGNTY_V9.0

import socket
import random
import time
import psutil
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple, Any
from contextlib import closing

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("NetworkOracle")


class NetworkBinder:
    """
    =================================================================================
    == THE NETWORK ORACLE (V-Ω-TOTALITY-ASCENDED)                                  ==
    =================================================================================
    The Sovereign Cartographer of the Local Network. Performs deep scrying of
    ports and interfaces to ensure zero-collision reality manifestation.
    """

    _cache: Dict[int, Tuple[float, bool]] = {}
    CACHE_TTL = 0.5  # [ASCENSION 8]: 500ms TTL for state caching

    @staticmethod
    def is_port_in_use(port: int, host: str = '127.0.0.1') -> bool:
        """
        [THE RITE OF THE PROBE]
        Performs a two-stage verification of port vitality.
        """
        if not port or port <= 0:
            return False

        # Check Cache first
        now = time.time()
        if port in NetworkBinder._cache:
            ts, state = NetworkBinder._cache[port]
            if now - ts < NetworkBinder.CACHE_TTL:
                return state

        # Stage 1: Connection Probe [ASCENSION 4]
        # We attempt to connect to see if a listener is active.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)  # Ultra-fast sub-second scry
            is_bound = s.connect_ex((host, port)) == 0

        if is_bound:
            NetworkBinder._cache[port] = (now, True)
            return True

        # Stage 2: Binding Probe [ASCENSION 5]
        # We attempt to bind to catch 'Zombies' in TIME_WAIT or kernel locks.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Platform-specific socket hardening
                if os.name != 'nt':
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                s.bind((host, port))
                NetworkBinder._cache[port] = (now, False)
                return False
        except OSError:
            NetworkBinder._cache[port] = (now, True)
            return True

    @classmethod
    def find_free_port(
            cls,
            start: int = 5173,
            max_attempts: int = 500,
            strategy: str = "sequential"
    ) -> int:
        """
        [THE RITE OF HARMONIC RESONANCE]
        High-speed parallel scrying to find the first available frequency.
        [ASCENSION 1 & 3]
        """
        # [ASCENSION 9]: Privilege Guard
        if start < 1024:
            Logger.warn(f"Port range {start} is in the Privileged Zone. Shifting to High Grounds.")
            start = 3000

        search_space = list(range(start, start + max_attempts))
        if strategy == "random":
            random.shuffle(search_space)

        Logger.verbose(f"Initiating Parallel Scry. Range: {start}-{start + max_attempts}...")

        # [ASCENSION 1]: Parallel Scrying Engine
        # We scan in batches of 50 to avoid kernel descriptor exhaustion.
        batch_size = 50
        for i in range(0, len(search_space), batch_size):
            batch = search_space[i:i + batch_size]

            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                future_map = {executor.submit(cls.is_port_in_use, p): p for p in batch}

                results: List[Tuple[int, bool]] = []
                for future in as_completed(future_map):
                    p = future_map[future]
                    results.append((p, future.result()))

                # Maintain order for sequential strategy
                results.sort(key=lambda x: x[0])

                for port, in_use in results:
                    if not in_use:
                        Logger.success(f"Network Resonance established: [cyan]:{port}[/cyan]")
                        return port

        raise ArtisanHeresy(
            f"Network Schism: No available ports found in range {start}-{start + max_attempts}.",
            suggestion="Terminate redundant Shadow processes or expand the scry range."
        )

    @staticmethod
    def identify_hostage_taker(port: int) -> Optional[Dict[str, Any]]:
        """
        [ASCENSION 2]: THE GAZE OF THE HOSTAGE
        Identifies the specific process holding a port hostage.
        """
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    if conn.pid:
                        process = psutil.Process(conn.pid)
                        return {
                            "pid": conn.pid,
                            "name": process.name(),
                            "status": process.status(),
                            "cmdline": " ".join(process.cmdline())
                        }
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
            pass
        return None

    @staticmethod
    def scry_interfaces() -> List[Dict[str, str]]:
        """
        [ASCENSION 7]: THE INTERFACE TOPOLOGY
        Maps all available network realities on the host machine.
        """
        interfaces = []
        try:
            for name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interfaces.append({
                            "name": name,
                            "ip": addr.address,
                            "is_loopback": addr.address.startswith('127.')
                        })
        except Exception as e:
            Logger.error(f"Topology Map fractured: {e}")
        return interfaces

    @classmethod
    def verify_protocol_vitality(cls, port: int, timeout: float = 2.0) -> bool:
        """
        [ASCENSION 11]: THE WARM GAZE
        Performs a protocol-level handshake to ensure the server is responding.
        """
        import http.client
        try:
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
            # We use HEAD to minimize bandwidth and impact
            conn.request("HEAD", "/")
            res = conn.getresponse()
            return res.status < 500
        except Exception:
            return False
        finally:
            try:
                conn.close()
            except:
                pass

    @classmethod
    def get_forensic_report(cls, port: int) -> str:
        """
        [ASCENSION 12]: THE MERKLE PORT SEAL
        Provides a detailed diagnostic of a port's current alignment.
        """
        hostage = cls.identify_hostage_taker(port)
        if hostage:
            return (
                f"Heresy: Port {port} is held hostage by '{hostage['name']}' (PID: {hostage['pid']}). "
                f"Status: {hostage['status'].upper()}."
            )

        is_up = cls.is_port_in_use(port)
        return f"Port {port} status: {'OCCUPIED' if is_up else 'VACANT'}. Ready for manifestation."


# --- GLOBAL CONDUIT ---
def get_oracle() -> NetworkBinder:
    return NetworkBinder()