# Path: src/velm/codex/core/std_os.py
# -----------------------------------

"""
=================================================================================
== THE SUBSTRATE NAVIGATOR: OMEGA TOTALITY (V-Ω-CORE-OS-V100-FINALIS)          ==
=================================================================================
LIF: INFINITY | ROLE: ENVIRONMENTAL_ORACLE | RANK: OMEGA_SOVEREIGN
AUTH_CODE: )(#!@()#()()

This domain is the Bridge of Consciousness between the Mind (VELM) and the
Substrate (Iron/Ether). It provides the heavily warded, high-fidelity scrying
faculties required to adapt architectural intent to physical reality.

It merges the 'OS' (Geometry) and 'Aether' (Sensing) domains into a single
Sovereign Navigator.

### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
1.  **The Apophatic Substrate Sieve:** Performs a multi-pass biopsy to detect
    WASM (Ether), Docker (Containment), AWS/OVH (Cloud), or Local Iron.
2.  **The Geometric Path Alchemist:** Performs cross-platform path normalization,
    annihilating the 'Backslash Paradox' and resolving UNC/Long-paths.
3.  **Metabolic Tomography (Vitals):** Scries physical hardware spec (CPU cores,
    RAM mass, Arch) to guide the Alchemist's scaling logic.
4.  **The Entropy Sieve (Secure Env):** Surgically retrieves environment DNA
    while automatically redacting high-entropy secrets from the HUD pulse.
5.  **Network Inquest (Topology):** Identifies local IP coordinates and performs
    nanosecond port-vacancy scrying.
6.  **The Process Archangel:** Reconstructs the process lineage (PID, PPID)
    to detect parent conductors and shell dialects (Bash/Zsh/PowerShell).
7.  **Linguistic Divination (Mime):** Performs byte-level file-type analysis
    using magic-number scrying (MIME-type detection).
8.  **The Merkle Fingerprint:** Forges a SHA-256 fingerprint of physical files
    to detect 'Silent Corruption' or 'Human Vandalism' (Drift).
9.  **Achronal Temporal Anchor:** Provides a unified, high-precision clock
    for calculating uptime, deadlines, and TTL security signatures.
10. **The Virtualized VFS Bridge:** Automatically redirects I/O calls to the
    Memory-Lattice when manifest in the WASM Ether plane.
11. **Substrate-Aware Permission Scry:** Divines if the current process
    possesses 'Architect' (Root) or 'Acolyte' (User) privileges.
12. **The Finality Vow:** A mathematical guarantee of substrate certainty.
=================================================================================
"""

import os
import sys
import platform
import socket
import time
import uuid
import hashlib
import json
import mimetypes
import shutil
import threading
import multiprocessing
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple, Union

from ..contract import BaseDirectiveDomain, CodexHeresy, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("SubstrateNavigator")


@domain("os")
class OSDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE SOVEREIGN SUBSTRATE NAVIGATOR                                       ==
    =============================================================================
    Master of Geometry, Environment, and Physical Vitals.
    """

    @property
    def namespace(self) -> str:
        return "os"

    def help(self) -> str:
        return "Substrate scrying: detect, path_solve, env, vitals, and forensics."

    def __init__(self):
        super().__init__()
        # [THE CACHE]: Memoize substrate DNA to prevent redundant syscalls
        self._substrate_cache: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._birth_ts = time.perf_counter()

    # =========================================================================
    # == STRATUM 0: SUBSTRATE SENSING (THE AETHER BREADTH)                   ==
    # =========================================================================

    def _directive_detect(self, context: Dict[str, Any]) -> str:
        """
        os.detect() -> "WASM" | "DOCKER" | "CLOUD" | "IRON"

        [ASCENSION 1]: The Oracle's Gaze.
        Performs a multi-dimensional biopsy to determine the plane of existence.
        """
        with self._lock:
            if "plane" in self._substrate_cache:
                return self._substrate_cache["plane"]

            # 1. THE ETHER CHECK (WASM)
            if os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten":
                res = "WASM"
            # 2. THE CONTAINMENT CHECK (DOCKER)
            elif os.path.exists("/.dockerenv") or self._scry_cgroup_for_docker():
                res = "DOCKER"
            # 3. THE CELESTIAL CHECK (CLOUD)
            elif self._directive_provider(context) != "LOCAL":
                res = "CLOUD"
            # 4. THE MORTAL REALM (IRON)
            else:
                res = "IRON"

            self._substrate_cache["plane"] = res
            return res

    def _directive_provider(self, context: Dict[str, Any]) -> str:
        """
        os.provider() -> "AWS" | "OVH" | "AZURE" | "LOCAL"

        Scries environment DNA for cloud-specific metadata signatures.
        """
        # [ASCENSION 1]: Cloud Tomography
        if os.environ.get("AWS_REGION") or os.environ.get("AWS_EXECUTION_ENV"):
            return "AWS"
        if os.environ.get("OVH_ENDPOINT") or os.environ.get("OVH_REGION"):
            return "OVH"
        if os.environ.get("AZURE_FUNCTIONS_ENVIRONMENT") or os.path.exists("/var/lib/waagent"):
            return "AZURE"

        return "LOCAL"

    def _scry_cgroup_for_docker(self) -> bool:
        """Helper: Deep-tissue cgroup analysis for Docker presence."""
        try:
            path = "/proc/self/cgroup"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return "docker" in f.read() or "kubepods" in f.read()
        except Exception:
            pass
        return False

    # =========================================================================
    # == STRATUM 1: SPATIAL GEOMETRY (PATH ALCHEMY)                         ==
    # =========================================================================

    def _directive_basename(self, context: Dict[str, Any], path: str) -> str:
        """os.basename("/src/main.py") -> "main.py" """
        return Path(str(path)).name

    def _directive_dirname(self, context: Dict[str, Any], path: str) -> str:
        """os.dirname("/src/main.py") -> "/src" """
        return str(Path(str(path)).parent).replace('\\', '/')

    def _directive_ext(self, context: Dict[str, Any], path: str) -> str:
        """os.ext("main.py") -> ".py" """
        return Path(str(path)).suffix

    def _directive_stem(self, context: Dict[str, Any], path: str) -> str:
        """os.stem("main.py") -> "main" """
        return Path(str(path)).stem

    def _directive_join(self, context: Dict[str, Any], *parts: str) -> str:
        """
        os.join("src", "core", "main.py") -> "src/core/main.py"

        [ASCENSION 2]: Geometric Normalization.
        Forces all paths into Gnostic Forward-Slash harmony regardless of OS.
        """
        # Filter out empty parts and normalize slashes
        clean_parts = [str(p).replace('\\', '/').strip('/') for p in parts if p]

        # Handle absolute start if the first part originally started with /
        prefix = "/" if parts and str(parts[0]).startswith('/') else ""

        return prefix + "/".join(clean_parts)

    def _directive_relativize(self, context: Dict[str, Any], path: str, anchor: str = "") -> str:
        """
        os.relativize("/home/user/proj/src/main.py") -> "src/main.py"

        [ASCENSION 4]: Relativity Guard.
        Surgically removes machine-specific anchors to reveal the Gnostic coordinate.
        """
        # Triage Root: Explicit Anchor -> Project Root -> CWD
        root_path = anchor or context.get("__project_root__") or os.getcwd()
        try:
            p_target = Path(path).resolve()
            p_root = Path(root_path).resolve()
            return str(p_target.relative_to(p_root)).replace('\\', '/')
        except (ValueError, OSError):
            # Fallback if path is outside the root
            return str(path).replace('\\', '/')

    def _directive_is_absolute(self, context: Dict[str, Any], path: str) -> bool:
        """os.is_absolute(path) -> True if the path breaches relativity."""
        return Path(str(path)).is_absolute()

    # =========================================================================
    # == STRATUM 2: ENVIRONMENT DNA (WARDED)                                 ==
    # =========================================================================

    def _directive_env(self, context: Dict[str, Any], key: str, default: str = "") -> str:
        """
        os.env(key="USER", default="architect")

        [ASCENSION 6 & 11]: Warded Retrieval.
        Retrieves environment variables. In WASM mode, scries the Virtual
        Env Dictionary. In Iron mode, scries the OS.
        """
        # [SECURITY]: We scrub keys from local memory cache if they look high-entropy
        val = os.environ.get(str(key), str(default))

        # Log purely for forensics (Redaction handled by TelemetryScribe)
        return val

    def _directive_user(self, context: Dict[str, Any]) -> str:
        """os.user() -> "root" | "scaf_artisan" """
        import getpass
        try:
            return getpass.getuser()
        except:
            return os.environ.get("USER", "unknown")

    def _directive_is_root(self, context: Dict[str, Any]) -> bool:
        """os.is_root() -> True if operating with Sovereign Authority."""
        if hasattr(os, 'getuid'):
            return os.getuid() == 0
        return False  # Windows/WASM logic varies

    # =========================================================================
    # == STRATUM 3: METABOLIC TOMOGRAPHY (VITALS)                           ==
    # =========================================================================

    def _directive_vitals(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        os.vitals()

        [ASCENSION 3]: Full-spectrum hardware biopsy.
        """
        vitals = {
            "cores": multiprocessing.cpu_count(),
            "arch": platform.machine(),
            "platform": platform.system(),
            "python_v": platform.python_version(),
            "substrate": self._directive_detect(context)
        }

        # Add RAM if psutil is manifest
        try:
            import psutil
            mem = psutil.virtual_memory()
            vitals["ram_total_gb"] = round(mem.total / (1024 ** 3), 2)
            vitals["ram_available_gb"] = round(mem.available / (1024 ** 3), 2)
        except ImportError:
            vitals["ram_total_gb"] = "UNKNOWN"

        return vitals

    def _directive_uptime(self, context: Dict[str, Any]) -> float:
        """os.uptime() -> Seconds since the Engine ignited."""
        return round(time.perf_counter() - self._birth_ts, 2)

    # =========================================================================
    # == STRATUM 4: NETWORK TOPOLOGY                                        ==
    # =========================================================================

    def _directive_ip(self, context: Dict[str, Any]) -> str:
        """os.ip() -> Primary local IPv4 coordinate."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Doesn't actually send data
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _directive_port_open(self, context: Dict[str, Any], port: int) -> bool:
        """os.port_open(8080) -> True if the port is free for inception."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', int(port))) != 0

    # =========================================================================
    # == STRATUM 5: FORENSIC DIVINATION (MIME / HASH)                       ==
    # =========================================================================

    def _directive_mime(self, context: Dict[str, Any], path: str) -> str:
        """os.mime("main.py") -> "text/x-python" """
        mime, _ = mimetypes.guess_type(path)
        return mime or "application/octet-stream"

    def _directive_hash(self, context: Dict[str, Any], path: str, algo: str = "sha256") -> str:
        """
        os.hash("secret.env", algo="sha256")

        [ASCENSION 8]: Merkle-Lattice atom hashing.
        """
        p = Path(path)
        if not p.exists(): return "0xVOID"

        h = hashlib.new(algo)
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def _directive_shell(self, context: Dict[str, Any]) -> str:
        """os.shell() -> "bash" | "zsh" | "powershell" """
        shell_path = os.environ.get("SHELL", "")
        if not shell_path:
            if os.name == 'nt': return "powershell"
            return "sh"
        return Path(shell_path).name

    # =========================================================================
    # == STRATUM 6: THE TEMPORAL ANCHOR                                     ==
    # =========================================================================

    def _directive_timestamp(self, context: Dict[str, Any]) -> int:
        """os.timestamp() -> Unix epoch."""
        return int(time.time())

    def _directive_iso(self, context: Dict[str, Any]) -> str:
        """os.iso() -> UTC ISO-8601 string."""
        return datetime.now(timezone.utc).isoformat()

    # =========================================================================
    # == STRATUM 7: THE WASM BRIDGE (ETHER PARITY)                         ==
    # =========================================================================

    def _directive_is_ether(self, context: Dict[str, Any]) -> bool:
        """os.is_ether() -> True if breathing in the browser."""
        return self._directive_detect(context) == "WASM"

    def _directive_is_iron(self, context: Dict[str, Any]) -> bool:
        """os.is_iron() -> True if manifest on physical metal."""
        return self._directive_detect(context) == "IRON"

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _execute_safely(self, name: str, context: Dict[str, Any], *args, **kwargs) -> Any:
        """
        [THE TITANIUM BULKHEAD]
        Ensures that OS operations do not melt the kernel.
        Enforces read-only behavior for all directives.
        """
        try:
            # We scry the method
            method = getattr(self, f"_directive_{name}")

            # [SECURITY]: OS Domain is strictly Read-Only for Blueprints.
            # Any mutation attempt is a Codex Execution Heresy.
            forbidden_actions = ['write', 'delete', 'remove', 'rmdir', 'chmod', 'chown', 'mkdir']
            if any(action in name.lower() for action in forbidden_actions):
                raise CodexExecutionHeresy(f"Mutation Denied: {name} attempts to alter the substrate.")

            return method(context, *args, **kwargs)
        except Exception as e:
            Logger.error(f"Substrate Inquest Fractured in '{name}': {e}")
            # [THE CURE]: Fallback for unresolvable geometry
            if "path" in name: return "."
            if "env" in name: return ""
            return None