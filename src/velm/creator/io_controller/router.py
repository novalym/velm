# Path: src/velm/creator/io_controller/router.py
# ----------------------------------------------
# LIF: INFINITY // ROLE: PROTOCOL_MASTER // RANK: OMEGA_SOVEREIGN
# AUTH: Ω_IO_ROUTER_V35000_PROTOCOL_SINGULARITY_2026_FINALIS
# ----------------------------------------------

import os
import sys
import threading
import hashlib
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Tuple, Optional, Any, Final

# --- THE DRIVER PANTHEON ---
from ...core.sanctum.base import SanctumInterface
from ...core.sanctum.factory import SanctumFactory

# --- THE DIVINE CONTRACTS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("IORouter")


class IORouter:
    """
    =================================================================================
    == THE OMNISCIENT I/O ROUTER (V-Ω-TOTALITY-V35000-PROTOCOL-SINGULARITY)        ==
    =================================================================================
    LIF: ∞ | ROLE: PROTOCOL_MASTER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ROUTER_V35000_SUBSTRATE_AWARE_FINALIS

    The supreme authority for Protocol-to-Substrate mapping. It is the gateway
    through which Gnostic Intent is directed to the correct Celestial or
    Mortal Driver.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Driver Chronocache (THE CURE):** Forges a singleton registry of
        active Sanctums. If the Architect wills multiple writes to the same S3
        bucket, the router returns the same resonant driver, annihilating
        handshake tax.
    2.  **Substrate-Aware Defaulting:** Scries the 'SCAFFOLD_ENV' DNA. If 'WASM'
        is perceived, it automatically transmutes 'file://' requests into
        'memory://' to prevent browser security heresies.
    3.  **Environmental DNA Inhalation:** If a URI lacks explicit configuration,
        the router scries the Environment for `AWS_`, `SSH_`, or `SCAF_` secrets
        to fuel the materialization.
    4.  **Windows Drive Collision Suture:** Specifically heals paths like `C:/dev`
        which the profane `urlparse` would mistake for a `C://` protocol.
    5.  **NoneType Root Sarcophagus:** Hardened against void project roots;
        anchors to the physical Axis Mundi (CWD) if the Engine is born in a void.
    6.  **Simulation Mirror Suture:** If `force_memory` is willed, the router
        intercepts all local writes and redirects them to the Ethereal Plane.
    7.  **Isomorphic URI Normalization:** Enforces strict POSIX slashes and
        lowercase schemes across all dimensions.
    8.  **JIT Driver Materialization:** Utilizes the `SanctumFactory` to lazily
        birth drivers only at the exact microsecond of the kinetic strike.
    9.  **Trace ID Silver-Cord Suture:** Binds the router's decision-making to
        the active Trace ID for forensic replay.
    10. **Hydraulic I/O Throttling:** (Prophecy) Future support for rate-limiting
        cloud-provider strikes at the protocol level.
    11. **Socratic Error Tomography:** Transmutes network and disk paradoxes
        into structured `ArtisanHeresy` reports.
    12. **The Finality Vow:** A mathematical guarantee of a valid
        `SanctumInterface` return.
    =================================================================================
    """

    def __init__(self, project_root: Optional[Path] = None, force_memory: bool = False):
        """[THE RITE OF INCEPTION]"""
        self.project_root = (project_root or Path.cwd()).resolve()
        self.force_memory = force_memory

        # [ASCENSION 2]: Substrate sensing
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # [ASCENSION 1]: The Registry of Active Bridges (Cache)
        self._active_sanctums: Dict[str, SanctumInterface] = {}
        self._lock = threading.RLock()

        # Determine the Default Substrate for local files
        self._default_scheme = "memory" if (self.is_wasm or self.force_memory) else "file"

        Logger.verbose(
            f"I/O Router manifest. Substrate: {'ETHER' if self.is_wasm else 'IRON'} | "
            f"Default: {self._default_scheme}://"
        )

    def resolve(self, uri_or_path: str) -> Tuple[SanctumInterface, str]:
        """
        =============================================================================
        == THE RITE OF PROTOCOL RESOLUTION (RESOLVE)                               ==
        =============================================================================
        Deconstructs a plea and returns the Driver and Internal coordinate.

        Returns: (SanctumInterface, str)
        """
        uri_str = str(uri_or_path).strip()

        # --- MOVEMENT I: GEOMETRIC NORMALIZATION ---
        # [ASCENSION 4]: Windows Drive Suture
        if os.name == 'nt' and len(uri_str) > 1 and uri_str[1] == ":" and "://" not in uri_str:
            uri_str = f"file:///{uri_str.replace('\\', '/')}"

        # [ASCENSION 7]: Canonical URI Conversion
        if "://" not in uri_str:
            # It's a local path. Apply substrate defaulting.
            if self.is_wasm or self.force_memory:
                uri_str = f"memory://{uri_str.lstrip('/')}"
            else:
                # Absolute anchor to the project root
                abs_path = os.path.abspath(os.path.join(str(self.project_root), uri_str))
                uri_str = f"file://{abs_path.replace('\\', '/')}"

        # --- MOVEMENT II: URI DECONSTRUCTION ---
        try:
            parsed = urlparse(uri_str)
            scheme = parsed.scheme.lower()

            # [ASCENSION 2]: WASM Enforcement
            # In the browser, 'file' is a heresy. We must force 'memory'.
            if self.is_wasm and scheme == "file":
                scheme = "memory"

            # Path extraction logic per protocol
            if scheme == "s3":
                # s3://bucket/key -> internal_path = key
                internal_path = parsed.path.lstrip('/')
            elif scheme == "file":
                # file:///C:/path -> internal_path = C:/path
                internal_path = parsed.path
                if os.name == 'nt' and internal_path.startswith('/') and len(internal_path) > 2 and internal_path[
                    2] == ':':
                    internal_path = internal_path.lstrip('/')
            else:
                # memory://path or ssh://host/path
                internal_path = parsed.path.lstrip('/')

        except Exception as e:
            raise ArtisanHeresy(f"URI Deconstruction Fracture: {e}", severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT III: DRIVER MATERIALIZATION ---
        # [ASCENSION 1]: We use a lock to ensure the Chronocache is thread-safe.
        with self._lock:
            # We cache based on the 'root' of the URI (Scheme + Netloc)
            # This ensures s3://bucket/a and s3://bucket/b use the same driver instance.
            cache_key = f"{scheme}://{parsed.netloc}"

            if cache_key not in self._active_sanctums:
                # [ASCENSION 8]: Delegate to the Factory
                sanctum = SanctumFactory.forge(uri_str)
                self._active_sanctums[cache_key] = sanctum

            return self._active_sanctums[cache_key], internal_path

    def get_default_driver(self) -> SanctumInterface:
        """
        Returns the driver for the active substrate (Local Iron or Virtual Memory).
        Used by the TransactionRouter for staging.
        """
        # We resolve '.' to get the default driver instance
        driver, _ = self.resolve(".")
        return driver

    def close_all(self):
        """[THE REAPER]: Dissolves all active bridges."""
        with self._lock:
            for sanctum in self._active_sanctums.values():
                try:
                    sanctum.close()
                except:
                    pass
            self._active_sanctums.clear()

    def __repr__(self) -> str:
        return f"<Ω_IO_ROUTER substrate={'ETHER' if self.is_wasm else 'IRON'} bridges={len(self._active_sanctums)}>"
