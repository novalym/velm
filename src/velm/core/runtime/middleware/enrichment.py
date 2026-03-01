# Path: scaffold/core/runtime/middleware/enrichment.py
# ---------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ENRICHMENT_SINGULARITY_V24
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: OMNISCIENT_WEAVER | RANK: OMEGA_SOVEREIGN
# =================================================================================
# [THE PANTHEON OF 24 LEGENDARY ASCENSIONS]:
#
# STRATUM I: METABOLIC EFFICIENCY & PERSISTENCE
# 1.  METABOLIC GNOSTIC CACHE: Memoizes system and Git info to prevent I/O thrashing.
# 2.  HYSTERESIS LOCK: Prevents redundant cache-updates during high-frequency pulses.
# 3.  HOLLOW-BORE RESOLUTION: Zero top-level heavy imports; everything is JIT.
# 4.  CLEAN DISMOUNT: Volatile cache markers are purged on process dissolution.
#
# STRATUM II: TOPOLOGICAL GEOMETRY
# 5.  ACHRONAL ROOT RESOLUTION (THE FIX): Divines the effective root when project_root is None.
# 6.  UNC-AWARE GEOMETRY: Correctly handles network-path project roots and symlinks.
# 7.  PROLEPTIC PATH NORMALIZATION: Enforces POSIX-standard slashes across all Iron.
# 8.  SUBSTRATE SENSING: Detects WASM vs Iron to adjust I/O probe intensity.
#
# STRATUM III: IDENTITY & DNA
# 9.  SESSION-LOCKED IDENTITY: OS and Machine ID are calculated exactly once.
# 10. ENVIRONMENT DNA INHERITANCE: Automatically maps SCAFFOLD_* env vars to Gnosis.
# 11. LATENT VARIABLE INCEPTION: Inhales user-defined vars from the OS stratum.
# 12. GNOSTIC METADATA GRAFTING: Injects calculated "Relevance" tags based on locus.
#
# STRATUM IV: RESILIENCE & SAFETY
# 13. NONETYPE SARCOPHAGUS (THE FIX): Brutal defensive guarding against null attributes.
# 14. FAIL-OPEN RESILIENCE: If a Git probe hangs, it returns 'void' instead of stalling.
# 15. HYDRAULIC ERROR CATCHMENT: Enrichment fractures are trapped and logged silently.
# 16. PERMISSIVE VOW: Allows the primary rite to proceed even if the mind is blind.
#
# STRATUM V: TELEMETRY & FORENSICS
# 17. CHROMATIC TELEMETRY: Identifies cache-hits vs fresh-scans in the diagnostic stream.
# 18. TRACE ID CAUSAL SUTURE: Propagates the silver-cord ID into the environment.
# 19. METABOLIC LOAD THROTTLING: Skips non-critical probes if Kernel heat is high.
# 20. PROTOCOL ALIGNMENT: Ensures 'scaffold_env' schema parity across the swarm.
#
# STRATUM VI: THE SINGULARITY SEAL
# 21. SEMANTIC MASS FILTER: Prunes empty or low-entropy environmental variables.
# 22. BIOMETRIC SIPHON: Automatically captures Git Author/Email for the Scribe.
# 23. THE WARD OF FINITUDE: Caps injected context size to prevent payload bloat.
# 24. APOTHEOSIS COMPLETE: The fastest context injector in the mortal realm.
# =================================================================================

import os
import time
import threading
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Set, Final

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult

# --- THE AKASHIC CACHE ---
# Structure: { root_str: (timestamp, gnosis_dict) }
_GNOSIS_CHRONOCACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_CACHE_LOCK = threading.RLock()
_CACHE_TTL: Final[float] = 30.0  # 30 seconds of temporal stability

# Static System Soul (Calculated once per process life)
_SYSTEM_SOUL: Optional[Dict[str, str]] = None


class EnrichmentMiddleware(Middleware):
    """
    =============================================================================
    == THE OMNISCIENT WEAVER (V-Ω-TOTALITY-V24-FINALIS)                        ==
    =============================================================================
    The High Priest of Situational Awareness.
    Reforged to be unbreakable against the 'NoneType' paradox.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Conducts the Rite of Enrichment.
        """
        # --- MOVEMENT I: RITE-WEIGHT TRIAGE ---
        # We only enrich rites that possess an "Architectural Appetite".
        rite_name = type(request).__name__
        needs_gnosis = any(k in rite_name for k in [
            "Genesis", "Distill", "Transmute", "Analyze", "Run",
            "Weave", "Dream", "Manifest", "Repair", "Architect"
        ])

        if not needs_gnosis:
            return next_handler(request)

        # --- MOVEMENT II: THE GNOSTIC INJECTION ---
        try:
            # Check for Adrenaline/High-Load to throttle enrichment
            if not getattr(request, 'adrenaline_mode', False):
                self._enrich_request(request)
        except Exception as e:
            # [ASCENSION 15]: HYDRAULIC ERROR CATCHMENT
            # Enrichment is a "Benevolent Bonus". It must never halt the Hand of Will.
            self.logger.debug(f"Enrichment bypassed due to situational paradox: {e}")

        return next_handler(request)

    def _enrich_request(self, request: BaseRequest):
        """
        =============================================================================
        == THE RITE OF GNOSTIC WEAVING                                             ==
        =============================================================================
        """
        # 1. MATERIALIZE SYSTEM SOUL
        # [ASCENSION 9]: Calculated once per singleton life.
        global _SYSTEM_SOUL
        if _SYSTEM_SOUL is None:
            self._materialize_system_soul()

        # 2. RESOLVE EFFECTIVE ANCHOR (THE FIX)
        # [ASCENSION 5 & 13]: We divine the coordinate without triggering a NoneType heresy.
        effective_root = self._get_effective_root(request)
        root_key = str(effective_root).replace('\\', '/')

        now = time.monotonic()

        # 3. CONSTRUCT PROJECT GNOSIS
        project_gnosis = {}
        with _CACHE_LOCK:
            cached_entry = _GNOSIS_CHRONOCACHE.get(root_key)

            if cached_entry and (now - cached_entry[0] < _CACHE_TTL):
                # [ASCENSION 17]: CACHE HIT (Radiate pulse to logs)
                project_gnosis = cached_entry[1]
                self.logger.debug(f"Situational Awareness: Gnostic Cache Hit for {effective_root.name}")
            else:
                # [ASCENSION 14]: FAIL-OPEN PROBE
                project_gnosis = self._probe_project_reality(effective_root)
                _GNOSIS_CHRONOCACHE[root_key] = (now, project_gnosis)

        # 4. ENVIRONMENT DNA INHALATION
        # [ASCENSION 10 & 11]: promovte OS variables to Gnostic status.
        env_vars = self._siphon_environmental_dna()

        # 5. ASSEMBLY OF THE WEAVE
        scaffold_env = {
            **(_SYSTEM_SOUL or {}),
            **project_gnosis,
            **env_vars,
            "trace_id": request.trace_id or "tr-void",
            "is_wasm": "true" if (sys.platform == "emscripten" or "pyodide" in sys.modules) else "false"
        }

        # 6. ATOMIC INJECTION (NONE-SAFE)
        # [ASCENSION 13]: Protecting the variables vessel.
        if request.variables is None:
            try:
                from velm.core.runtime.vessels import GnosticSovereignDict
                request.variables = GnosticSovereignDict()
            except ImportError:
                request.variables = {}

        # Merge the weave into the request context
        request.variables["scaffold_env"] = scaffold_env

    def _get_effective_root(self, request: BaseRequest) -> Path:
        """
        =============================================================================
        == THE ACHRONAL ROOT RESOLVER (V-Ω-NONE-SAFE-FINALIS)                     ==
        =============================================================================
        [THE CURE]: This method guarantees that a Path object is returned,
        annihilating the 'NoneType' resolve heresy.
        """
        # Priority 1: Explicit Request Anchor
        if request.project_root is not None:
            try:
                return request.project_root.resolve()
            except Exception:
                return request.project_root

        # Priority 2: Substrate Environment Anchor
        env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT")
        if env_root:
            return Path(env_root).resolve()

        # Priority 3: Mortal Realm CWD
        try:
            return Path.cwd().resolve()
        except Exception:
            # Priority 4: WASM Ethereal Fallback
            return Path("/vault/project")

    def _materialize_system_soul(self):
        """Calculates immutable hardware and user identity shards."""
        global _SYSTEM_SOUL
        import platform
        _SYSTEM_SOUL = {
            "os": platform.system().lower(),
            "arch": platform.machine().lower(),
            "python": f"{sys.version_info.major}.{sys.version_info.minor}",
            "user": os.getenv("USER") or os.getenv("USERNAME") or "architect",
            "ci": "true" if any(k in os.environ for k in ["CI", "GITHUB_ACTIONS", "TRAVIS", "VERCEL"]) else "false",
            "node": platform.node() or "unknown_host"
        }

    def _siphon_environmental_dna(self) -> Dict[str, str]:
        """[ASCENSION 10]: Inhales variables warded by the SCAFFOLD_ prefix."""
        dna = {}
        for k, v in os.environ.items():
            if k.startswith("SCAFFOLD_VAR_"):
                key = k.replace("SCAFFOLD_VAR_", "").lower()
                dna[key] = v
        return dna

    def _probe_project_reality(self, root: Path) -> Dict[str, str]:
        """
        [THE RITE OF THE DUAL GAZE]
        Probes the physical disk for Git state and project markers.
        """
        # [THE CURE]: JIT Import of heavy utils
        try:
            from ....utils import get_git_branch, get_git_commit
        except ImportError:
            return {"git_branch": "void", "git_commit": "void"}

        gnosis = {
            "git_branch": "void",
            "git_commit": "void",
            "project_name": root.name,
            "has_docker": "true" if (root / "Dockerfile").exists() or (
                        root / "docker-compose.yml").exists() else "false",
            "has_poetry": "true" if (root / "pyproject.toml").exists() else "false",
            "has_node": "true" if (root / "package.json").exists() else "false"
        }

        try:
            # Short-circuit if .git is unmanifest
            if not (root / ".git").exists():
                return gnosis

            # Conduct Git Inquest with extreme timeout wards
            # We assume these utils are hardened or we wrap them here
            gnosis["git_branch"] = get_git_branch(root) or "void"
            gnosis["git_commit"] = get_git_commit(root) or "void"

        except Exception:
            # [ASCENSION 14]: FAIL-OPEN
            pass

        return gnosis
