# Path: scaffold/artisans/shadow_clone/network.py
# =========================================================================================
# == THE NETWORK ORACLE (V-Ω-TOTALITY-V20000.9-ISOMORPHIC)                               ==
# =========================================================================================
# LIF: 10,000,000,000,000 | ROLE: SPATIAL_NETWORK_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_NETWORK_V20000_SAB_RESONANCE_2026_FINALIS
# =========================================================================================

import socket
import random
import time
import os
import threading
import gc
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple, Any, Final
from contextlib import closing

# [ASCENSION 1]: SUBSTRATE SENSING
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("NetworkOracle")


class NetworkBinder:
    """
    =================================================================================
    == THE NETWORK ORACLE (V-Ω-TOTALITY)                                           ==
    =================================================================================
    LIF: ∞ | The Sovereign Navigator of the Local Aether.
    """

    # [PHYSICS CONSTANTS]
    _cache: Dict[int, Tuple[float, bool]] = {}
    _cache_lock = threading.RLock()
    CACHE_TTL: Final[float] = 0.5
    PRIVILEGED_ZONE: Final[int] = 1024

    @staticmethod
    def is_port_in_use(port: int, host: str = '127.0.0.1') -> bool:
        """
        =============================================================================
        == THE RITE OF THE PROBE (BIPHASIC)                                        ==
        =============================================================================
        Performs a deep-tissue scry of a port's vitality.
        """
        if not port or port <= 0:
            return False

        # --- MOVEMENT I: CHRONOCACHE PERCEPTION ---
        now = time.time()
        with NetworkBinder._cache_lock:
            if port in NetworkBinder._cache:
                ts, state = NetworkBinder._cache[port]
                if now - ts < NetworkBinder.CACHE_TTL:
                    return state

        # --- MOVEMENT II: THE RESONANCE TEST ---
        # 1. Listener Probe: See if anyone is actively speaking
        is_bound = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.05)  # Ultra-fast scry
                is_bound = s.connect_ex((host, port)) == 0
        except:
            pass

        if is_bound:
            with NetworkBinder._cache_lock:
                NetworkBinder._cache[port] = (now, True)
            return True

        # 2. Binding Probe: Detect kernel-level locks or TIME_WAIT status
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # [ASCENSION 5]: POSIX Hardening
                if os.name != 'nt':
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                s.bind((host, port))
                # If we reached here, the port is truly Vacant.
                with NetworkBinder._cache_lock:
                    NetworkBinder._cache[port] = (now, False)
                return False
        except (OSError, PermissionError):
            # Port is held by the system or another soul
            with NetworkBinder._cache_lock:
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
        =============================================================================
        == THE RITE OF HARMONIC RESONANCE (PARALLEL SEARCH)                        ==
        =============================================================================
        LIF: 100x | Searches for an available frequency in the digital spectrum.
        """
        # [ASCENSION 6]: PRIVILEGE GUARD
        if start < cls.PRIVILEGED_ZONE:
            Logger.warn(f"Plea for port {start} is in the Restricted Zone. Shifting to High Grounds.")
            start = 3000

        search_space = list(range(start, start + max_attempts))
        if strategy == "random":
            random.shuffle(search_space)

        # [ASCENSION 4]: METABOLIC GOVERNANCE
        # Determine batch size based on thread health.
        batch_size = 50

        Logger.verbose(f"Initiating Parallel Scry. Spectrum: {start}-{start + max_attempts}...")

        for i in range(0, len(search_space), batch_size):
            batch = search_space[i:i + batch_size]

            # [ASCENSION 11]: FAULT-ISOLATED SWARM
            with ThreadPoolExecutor(max_workers=len(batch), thread_name_prefix="OracleScry") as executor:
                future_map = {executor.submit(cls.is_port_in_use, p): p for p in batch}

                results: List[Tuple[int, bool]] = []
                for future in as_completed(future_map):
                    p = future_map[future]
                    try:
                        results.append((p, future.result()))
                    except Exception as e:
                        Logger.debug(f"Scry Fracture at port {p}: {e}")
                        results.append((p, True))  # Assume occupied if scry fails

                # Maintain causality for sequential strategy
                results.sort(key=lambda x: x[0])

                for port, in_use in results:
                    if not in_use:
                        Logger.success(f"Network Resonance established: [bold cyan]:{port}[/bold cyan]")
                        return port

            # [ASCENSION 8]: Descrpitor Drain
            # Small yield to allow OS to recycle socket descriptors
            time.sleep(0.01)
            gc.collect(1)

        raise ArtisanHeresy(
            f"Network Schism: No vacant frequencies perceived in range {start}-{start + max_attempts}.",
            severity=HeresySeverity.CRITICAL,
            suggestion="Terminate redundant Shadow Clones or expand the scry-range via --port."
        )

    @staticmethod
    def identify_hostage_taker(port: int) -> Optional[Dict[str, Any]]:
        """
        =============================================================================
        == THE GAZE OF THE HOSTAGE (FORENSIC PID RESOLUTION)                      ==
        =============================================================================
        [ASCENSION 1]: Differentiates between Iron and Ether planes.
        """
        if not PSUTIL_AVAILABLE:
            # [ETHER_REALM_FALLBACK]: WASM cannot scry process tables.
            return None

        try:
            # Scry net connections for the target port
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    if conn.pid:
                        process = psutil.Process(conn.pid)
                        return {
                            "pid": conn.pid,
                            "name": process.name(),
                            "status": process.status(),
                            "cmdline": " ".join(process.cmdline()),
                            "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2)
                        }
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
            pass
        return None

    @staticmethod
    def scry_interfaces() -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE INTERFACE TOPOLOGY (V-Ω-SPATIAL-MAPPING)                            ==
        =============================================================================
        """
        interfaces = []
        try:
            if PSUTIL_AVAILABLE:
                for name, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            interfaces.append({
                                "name": name,
                                "ip": addr.address,
                                "is_loopback": addr.address.startswith('127.'),
                                "substrate": "IRON"
                            })
            else:
                # WASM Fallback: Virtualize the loopback reality
                interfaces.append({
                    "name": "lo0",
                    "ip": "127.0.0.1",
                    "is_loopback": True,
                    "substrate": "ETHER"
                })
        except Exception as e:
            Logger.error(f"Topology Map fractured: {e}")

        return interfaces

    @classmethod
    def verify_protocol_vitality(cls, port: int, path: str = "/", timeout: float = 2.0) -> bool:
        """
        =============================================================================
        == THE WARM GAZE (L7 HEARTBEAT)                                           ==
        =============================================================================
        Performs a protocol-level handshake to ensure the reality is responsive.
        """
        import http.client
        try:
            # [THE CURE]: Closeable connection to prevent FD leakage
            with closing(http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)) as conn:
                # We use HEAD to minimize metabolic tax
                conn.request("HEAD", path)
                res = conn.getresponse()
                return res.status < 500
        except Exception:
            return False

    @classmethod
    def get_forensic_report(cls, port: int) -> str:
        """
        =============================================================================
        == THE MERKLE PORT SEAL (DIAGNOSTIC PROCLAMATION)                         ==
        =============================================================================
        """
        hostage = cls.identify_hostage_taker(port)
        if hostage:
            return (
                f"Heresy: Port {port} is held hostage by [bold red]'{hostage['name']}'[/] (PID: {hostage['pid']}). "
                f"Metabolism: {hostage['memory_mb']}MB. Status: {hostage['status'].upper()}."
            )

        is_up = cls.is_port_in_use(port)
        if is_up:
            return f"Port {port} is [yellow]OCCUPIED[/] by an unperceived soul (Kernel lock or Permission block)."

        return f"Port {port} is [green]VACANT[/]. Resonance confirmed for manifestation."


# --- GLOBAL CONDUIT ---
def get_oracle() -> NetworkBinder:
    """Summons the singleton instance of the Network Oracle."""
    return NetworkBinder()
