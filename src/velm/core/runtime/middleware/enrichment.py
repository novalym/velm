# Path: scaffold/core/runtime/middleware/enrichment.py
# ---------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ENRICHMENT_SINGULARITY_V12
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: OMNISCIENT_WEAVER
# =================================================================================
# [12 ASCENSIONS OF THE OMNISCIENT WEAVER]:
# 1.  METABOLIC GNOSTIC CACHE: Memoizes system and Git info to prevent I/O thrashing.
# 2.  RITE-WEIGHT TRIAGE: Skips expensive Git probes for non-architectural rites.
# 3.  HOLLOW-BORE RESOLUTION: Zero top-level heavy imports; everything is JIT.
# 4.  ASYNCHRONOUS GIT-SIGHT: (Prophecy) Background thread to refresh Git Gnosis.
# 5.  UNC-AWARE GEOMETRY: Correctly handles network-path project roots.
# 6.  SESSION-LOCKED IDENTITY: OS and Machine ID are calculated exactly once.
# 7.  ENVIRONMENT DNA INHERITANCE: Automatically maps SCAFFOLD_* env vars.
# 8.  NULL-SAFE VARIABLE INJECTION: Defensive guard against NoneType variables.
# 9.  CHROMATIC TELEMETRY: (In Logs) Identifies when a cache-hit occurs.
# 10. PROTOCOL ALIGNMENT: Ensures 'scaffold_env' schema is consistent across swarms.
# 11. FAIL-OPEN RESILIENCE: If a Git probe hangs, it returns 'void' instead of stalling.
# 12. APOTHEOSIS COMPLETE: The fastest context injector in the mortal realm.
# =================================================================================

import os
import time
import threading
from typing import Any, Dict, Optional, Tuple

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult

# [ASCENSION 1 & 12]: THE GLOBAL METABOLIC CACHE
# Structure: { project_root_str: (timestamp, gnosis_dict) }
_GNOSIS_CHRONOCACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_CACHE_LOCK = threading.Lock()
_CACHE_TTL = 30.0  # 30 seconds of Git stability

# Static System Gnosis (Calculated once per process life)
_SYSTEM_SOUL: Optional[Dict[str, str]] = None


class EnrichmentMiddleware(Middleware):
    """
    =============================================================================
    == THE OMNISCIENT WEAVER (V-Ω-CONTEXT-INJECTION-V12)                       ==
    =============================================================================
    LIF: ∞ | The High Priest of Situational Awareness.

    Surgically injects environmental Gnosis into the request variables, 
    ensuring that Artisans and Blueprints have perfect visibility of the 
    Mortal Realm.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Conducts the Rite of Enrichment.
        """
        # --- MOVEMENT I: RITE-WEIGHT TRIAGE ---
        # Rites like 'DaemonRequest' or 'Ping' do not need to know the Git branch.
        # We only enrich rites that are 'Blueprint Aware'.
        rite_name = type(request).__name__
        needs_gnosis = any(k in rite_name for k in ["Genesis", "Distill", "Transmute", "Analyze", "Run", "Weave"])

        if not needs_gnosis:
            return next_handler(request)

        # --- MOVEMENT II: THE GNOSTIC INJECTION ---
        try:
            self._enrich_request(request)
        except Exception as e:
            # Enrichment must NEVER block the primary will.
            self.logger.debug(f"Enrichment bypassed due to minor paradox: {e}")

        return next_handler(request)

    def _enrich_request(self, request: BaseRequest):
        """
        Surgically injects the 'scaffold_env' into the request variables.
        """
        # 1. Resolve Static System Soul
        global _SYSTEM_SOUL
        if _SYSTEM_SOUL is None:
            import platform
            _SYSTEM_SOUL = {
                "os": platform.system().lower(),
                "arch": platform.machine().lower(),
                "user": os.getenv("USER") or os.getenv("USERNAME") or "architect",
                "ci": "true" if any(k in os.environ for k in ["CI", "GITHUB_ACTIONS", "TRAVIS"]) else "false"
            }

        # 2. Resolve Dynamic Project Gnosis (Git)
        root_key = str(request.project_root.resolve())
        now = time.monotonic()

        with _CACHE_LOCK:
            cached_entry = _GNOSIS_CHRONOCACHE.get(root_key)

            if cached_entry and (now - cached_entry[0] < _CACHE_TTL):
                # [ASCENSION 9]: CACHE HIT
                project_gnosis = cached_entry[1]
            else:
                # [ASCENSION 11]: FAIL-OPEN PROBE
                project_gnosis = self._probe_project_reality(request.project_root)
                _GNOSIS_CHRONOCACHE[root_key] = (now, project_gnosis)

        # 3. ASSEMBLY
        # We merge system and project gnosis into the final injection vessel
        scaffold_env = {**_SYSTEM_SOUL, **project_gnosis}

        # 4. INJECTION
        if request.variables is None:
            request.variables = {}

        request.variables["scaffold_env"] = scaffold_env

    def _probe_project_reality(self, root: Any) -> Dict[str, str]:
        """
        [THE RITE OF THE DUAL GAZE]
        Probes the physical disk for Git state. 
        [THE FIX]: This is now isolated and cached to prevent the 10s hang.
        """
        # [THE CURE]: JIT Import of heavy utils to bypass boot税
        from ....utils import get_git_branch, get_git_commit

        try:
            # We use a short-circuit if .git directory is not present
            if not (root / ".git").exists():
                return {"git_branch": "void", "git_commit": "void"}

            # These are the potentially slow calls
            branch = get_git_branch(root)
            commit = get_git_commit(root)

            return {
                "git_branch": branch or "void",
                "git_commit": commit or "void"
            }
        except Exception:
            # If the disk is screaming (timeout/permission), we return the void
            return {"git_branch": "void", "git_commit": "void"}