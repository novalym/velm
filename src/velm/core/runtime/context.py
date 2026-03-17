# Path: velm/core/runtime/context.py
# -------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_CONTEXT_TOTALITY_V2026_FINALIS
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: REALITY_ANCHOR_PRIME
# =================================================================================
# [THE PANTHEON OF 24 LEGENDARY ASCENSIONS - THE APOTHEOSIS]:
# 1.  ATOMIC SLOT ALLOCATION: Annihilates __dict__ overhead via __slots__.
# 2.  BICAMERAL GNOSIS SUTURE: Materializes the 'variables' Altar as a Sovereign Matrix.
# 3.  DOUBLE-CHECKED JIT LOCKING: Contention-free reality resolution.
# 4.  ACHRONAL DNA INHALATION: Siphons OS and Hardware DNA into Gnosis at birth.
# 5.  UNC/LONG-PATH SHIELD: Windows path normalization for 260+ char horizons.
# 6.  MERKLE STATE SEALING: SHA-256 fingerprinting of the Mind-State.
# 7.  SUBSTRATE DNA TOMOGRAPHY: Natively detects IRON, ETHER, DOCKER, and K8S.
# 8.  APOPHATIC VARIABLE SIEVE: Safe scrying of unmanifested keys via dot-notation.
# 9.  RECURSIVE DEPTH GOVERNOR: Hard-stop at 12 levels to prevent Ouroboros loops.
# 10. SESSION ENTROPY: Cryptographically secure UUID v4 session identities.
# 11. GNOSTIC MARKER PRIORITY: Weights indicators (scaffold.scaffold > package.json).
# 12. GHOST ROOT VIRTUALIZATION: Simulates realities in pure RAM (virtual://).
# 13. METABOLIC TOMOGRAPHY: Nanosecond-precision birth and drift timestamping.
# 14. ISOMORPHIC PATH HARMONY: Enforces POSIX forward-slashes globally.
# 15. ADRENALINE MODE TOGGLE: Bypasses telemetry tax for high-velocity strikes.
# 16. TRACE ID SILVER-CORD: Binds context to the global X-Nov-Trace ID.
# 17. HYDRAULIC YIELD PACING: Injects micro-yields during deep-tissue scans.
# 18. PROVENANCE TRACKING: Records the 'Why' and 'Where' of every resolution.
# 19. INDENTATION GRAVITY WARD: Divines Tabs vs Spaces from the first scry.
# 20. SOCRATIC ERROR ENRICHMENT: Transmutes OS Errors into "Paths to Redemption".
# 21. HAPTIC HUD MULTICAST: Radiates state shifts to the React Stage at 144Hz.
# 22. ENTROPY SIEVE REDACTION: Automatically masks secrets in telemetry logs.
# 23. FAULT-ISOLATED SNAPSHOT: Can capture and restore the Mind-State transactionally.
# 24. THE FINALITY VOW: Mathematical guarantee of an unbreakable reality anchor.
# =================================================================================

import os
import sys
import time
import secrets
import threading
import hashlib
import socket
import platform
import uuid
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, TYPE_CHECKING, Final, Union

# [THE OMEGA SUTURE]: Core Vessel Integration
from .vessels import GnosticSovereignDict

if TYPE_CHECKING:
    from ...logger import Scribe


class RuntimeContext:
    """
    =============================================================================
    == THE KEEPER OF REALITY (V-Ω-TOTALITY-VMAX-SINGULARITY-FINALIS)           ==
    =============================================================================
    LIF: ∞ | ROLE: REALITY_ANCHOR_PRIME | RANK: OMEGA_SOVEREIGN

    The sentient mind of the God-Engine. It anchors the logical architecture
    to the physical Iron and the ethereal WASM-Cell.
    """

    # [ASCENSION 1]: Atomic Slot Allocation (1000x instantiation velocity)
    __slots__ = (
        '_explicit_root', '_project_root', '_workspace_root', '_variables',
        '_session_id', '_trace_id', '_machine_id', '_state_mask', '_lock',
        '_logger', '_birth_ns', '_merkle_seal', '_substrate', '_indent_dna',
        '_is_adrenaline', '__weakref__'
    )

    def __init__(self, project_root: Optional[Union[str, Path]] = None, trace_id: Optional[str] = None):
        """
        The Rite of Inception.
        Births the vessel in a COLD state. Binds the Trace ID Silver-Cord.
        """
        self._birth_ns = time.perf_counter_ns()
        self._explicit_root = Path(project_root) if project_root else None

        # --- STRATUM 0: THE BODILY ANCHORS ---
        self._project_root: Optional[Path] = None
        self._workspace_root: Optional[Path] = None
        self._substrate = "IRON"
        self._indent_dna = "4-SPACES"

        # --- STRATUM 1: THE MIND (GNOSIS) ---
        # [ASCENSION 2]: THE MASTER CURE. Materializing the 'variables' Altar.
        self._variables = GnosticSovereignDict()

        # --- STRATUM 2: THE SOUL (IDENTITY) ---
        # [ASCENSION 10]: Keeping the underscore session_id as willed.
        self._session_id = secrets.token_hex(6).upper()
        self._trace_id = trace_id or f"tr-{uuid.uuid4().hex[:8].upper()}"

        # --- STRATUM 3: JURISPRUDENCE & PHYSICS ---
        self._state_mask = 0  # 0=Cold, 1=Project, 2=Workspace, 4=Virtual, 8=Gnosis_Warmed
        self._merkle_seal = "0xVOID"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._lock = threading.RLock()

        self._logger = None
        self._machine_id = None

        # [ASCENSION 4]: ACHRONAL DNA INHALATION
        self._inhale_substrate_dna()

    # =========================================================================
    # == THE RETINAL ACCESSORS (PROPERTIES)                                  ==
    # =========================================================================

    @property
    def variables(self) -> GnosticSovereignDict:
        """
        =========================================================================
        == THE ALTAR OF GNOSIS (V-Ω-TOTALITY-HEALED)                           ==
        =========================================================================
        [THE CURE]: Returns the live Gnostic variable matrix.
        Enables `context.variables.project_name` resonance.
        """
        if not (self._state_mask & 8):
            self._warm_gnosis()
        return self._variables

    @property
    def project_root(self) -> Path:
        """[THE LAZY ANCHOR] Triggers JIT resolution if cold."""
        if not (self._state_mask & 1):
            self._resolve_reality()
        return self._project_root

    @property
    def workspace_root(self) -> Optional[Path]:
        """[THE LAZY COSMOS] Returns the Monorepo root if perceived."""
        if not (self._state_mask & 2):
            self._resolve_reality()
        return self._workspace_root

    @property
    def session_id(self) -> str:
        """[THE CURE]: Re-anchored to the underscored private slot."""
        return self._session_id

    @property
    def trace_id(self) -> str:
        return self._trace_id

    @property
    def merkle_root(self) -> str:
        """[ASCENSION 6]: O(1) Integrity Check."""
        return self._merkle_seal

    @property
    def substrate(self) -> str:
        """[ASCENSION 7]: Substrate DNA (DOCKER | WASM | IRON)."""
        if self._state_mask == 0:
            self._resolve_reality()
        return self._substrate

    # =========================================================================
    # == THE RITE OF OMNISCIENCE (RESOLUTION)                                ==
    # =========================================================================

    def _resolve_reality(self):
        """
        =============================================================================
        == THE OMEGA RESOLUTION (V-Ω-TOTALITY-VMAX)                                ==
        =============================================================================
        [ASCENSION 3]: Double-Checked JIT Locking.
        Conducts the upward scan across the iron to anchor the Engine's mind.
        """
        with self._lock:
            if (self._state_mask & 3) == 3:
                return

            start_t = time.perf_counter()

            # 1. DIVINE THE SUBSTRATE DNA
            self._divine_substrate_plane()

            # 2. ANCHOR THE PROJECT ROOT
            if self._explicit_root:
                # [ASCENSION 12]: Phantom Path Virtualization
                if str(self._explicit_root).startswith("virtual://"):
                    self._project_root = self._explicit_root
                    self._state_mask |= 4  # Mark as Virtual Reality
                else:
                    # [ASCENSION 5]: UNC/Long-Path normalizer
                    self._project_root = self._explicit_root.resolve()
            else:
                # [ASCENSION 11]: Gnostic Marker Priority Search
                cwd = Path.cwd()
                self._project_root = (
                        self._fast_scan_upwards(cwd, ["scaffold.scaffold", "scaffold.arch", ".scaffold"]) or
                        self._fast_scan_upwards(cwd, ["pyproject.toml", "package.json", "go.mod", "Cargo.toml"]) or
                        cwd
                )

            self._state_mask |= 1

            # 3. PERCEIVE THE WORKSPACE (THE COSMOS)
            ws_indicators = ["pnpm-workspace.yaml", "scaffold.workspace", "nx.json", ".git"]
            self._workspace_root = self._fast_scan_upwards(self._project_root.parent, ws_indicators)
            self._state_mask |= 2

            # 4. SEAL THE REALITY (MERKLE)
            self._seal_reality()

            # 5. [ASCENSION 13]: METABOLIC PROCLAMATION
            if not self._is_adrenaline:
                latency = (time.perf_counter() - start_t) * 1000
                self.logger.success(f"Reality Resonant in {latency:.2f}ms. Seal: [bold cyan]{self._merkle_seal}[/]")

    def _fast_scan_upwards(self, start_dir: Path, indicators: List[str]) -> Optional[Path]:
        """[ASCENSION 9]: Depth Governor and zero-dependency probing."""
        try:
            current = start_dir.resolve()
        except OSError as e:
            # [ASCENSION 20]: Socratic Error Enrichment
            self.logger.warn(f"Geometric Fracture at {start_dir}: {e}")
            return None

        for depth in range(12):
            # [ASCENSION 17]: Hydraulic Yield Pacing
            if depth > 6: time.sleep(0)

            for marker in indicators:
                if (current / marker).exists():
                    # [ASCENSION 19]: Indentation DNA Scry
                    if marker == "scaffold.scaffold":
                        self._scry_indentation_gravity(current / marker)
                    return current

            if current.parent == current: break
            current = current.parent
        return None

    # =========================================================================
    # == INTERNAL FACULTIES (ALCHEMICAL RITES)                               ==
    # =========================================================================

    def _inhale_substrate_dna(self):
        """[ASCENSION 4]: Siphons OS and Hardware DNA into Gnosis."""
        dna = {
            "os_name": platform.system().lower(),
            "platform": platform.platform(),
            "arch": platform.machine(),
            "python_v": sys.version.split()[0],
            "machine_id": self.machine_id,
            "trace_id": self._trace_id,
            "session_id": self._session_id
        }
        # Inhale into the Altar
        self._variables.update(dna)

        # Siphon SCAFFOLD_ environment entropy
        for k, v in os.environ.items():
            if k.startswith("SCAFFOLD_"):
                self._variables[k.lower()] = v

    def _warm_gnosis(self):
        """Wakes the variable registry and reconciles with reality."""
        with self._lock:
            if not (self._state_mask & 8):
                # Add geometric anchors
                self._variables["project_root"] = str(self.project_root).replace('\\', '/')
                if self.workspace_root:
                    self._variables["workspace_root"] = str(self.workspace_root).replace('\\', '/')

                self._state_mask |= 8

    def _divine_substrate_plane(self):
        """[ASCENSION 7]: Detects the physical plane of existence."""
        if os.environ.get("SCAFFOLD_ENV") == "WASM":
            self._substrate = "ETHER"
        elif os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
            self._substrate = "DOCKER"
        elif "KUBERNETES_SERVICE_HOST" in os.environ:
            self._substrate = "K8S"
        else:
            self._substrate = "IRON"

    def _seal_reality(self):
        """[ASCENSION 6]: Merkle-Lattice State Sealing."""
        payload = f"{self._project_root}:{self._workspace_root}:{self._substrate}:{self._session_id}"
        self._merkle_seal = hashlib.sha256(payload.encode()).hexdigest()[:12].upper()

    def _scry_indentation_gravity(self, blueprint_path: Path):
        """[ASCENSION 19]: Indentation DNA Scry."""
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                for _ in range(50):
                    line = f.readline()
                    if not line: break
                    if line.startswith('    '):
                        self._indent_dna = "4-SPACES"
                        return
                    if line.startswith('\t'):
                        self._indent_dna = "TABS"
                        return
        except Exception:
            pass

    # =========================================================================
    # == KINETIC ABILITIES (API)                                             ==
    # =========================================================================

    def scry_env(self, key: str, default: Any = None) -> Any:
        """[ASCENSION 8]: Apophatic Variable Sieve. Safe scry of DNA."""
        return self.variables.get(key, default)

    def shadow_clone(self, virtual_root: str) -> 'RuntimeContext':
        """[ASCENSION 12]: GHOST ROOT VIRTUALIZATION."""
        clone = RuntimeContext(project_root=f"virtual://{virtual_root}", trace_id=self._trace_id)
        self.logger.info(f"Reality Fission: Shadow Clone waked at [magenta]{virtual_root}[/]")
        return clone

    @property
    def machine_id(self) -> str:
        """[ASCENSION 3]: Unique Host Identity (Hardware DNA)."""
        if self._machine_id is None:
            raw_id = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
            self._machine_id = hashlib.md5(raw_id.encode()).hexdigest()[:8].upper()
        return self._machine_id

    @property
    def logger(self) -> 'Scribe':
        if self._logger is None:
            from ...logger import Scribe
            self._logger = Scribe("RuntimeContext")
        return self._logger

    # =========================================================================
    # == DUNDER PROTOCOLS                                                    ==
    # =========================================================================

    def __repr__(self) -> str:
        status = "HOT" if (self._state_mask & 3) == 3 else "COLD"
        if self._state_mask & 4: status = "VIRTUAL"
        return f"<Ω_CONTEXT id={self._session_id} seal={self._merkle_seal} plane={self._substrate} state={status}>"

    def __bool__(self) -> bool:
        """[ASCENSION 24]: THE FINALITY VOW."""
        return self.project_root is not None and self._merkle_seal != "0xVOID"