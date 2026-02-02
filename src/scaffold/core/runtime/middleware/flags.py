# Path: core/runtime/middleware/flags.py
# -----------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_FLAG_WARDEN_V99
# =================================================================================
# == THE SHIFTER (V-Ω-DYNAMIC-CAPABILITIES)                                      ==
# =================================================================================
# [PURPOSE]: Dynamic feature toggling, kill-switches, and behavioral overrides.
#
# 12 LEGENDARY ASCENSIONS:
# 1. [HIERARCHICAL MERGE]: System -> User -> Project -> Environment (Highest Wins).
# 2. [TYPE SANITIZATION]: Rigid `Path` casting prevents the 'str / str' heresy.
# 3. [CACHE MEMBRANE]: In-memory caching (5s TTL) prevents disk thrashing.
# 4. [ENV INJECTION]: `SCAFFOLD_FEAT_X` env vars automatically override files.
# 5. [KILL SWITCH]: `disable_rite_*` flags instantly halt specific execution paths.
# 6. [VARIABLE INJECTION]: `feat_*` flags are grafted into the request context.
# 7. [RUNTIME OVERRIDE]: Can force `docker` or `system` runtimes dynamically.
# 8. [CHAOS MONKEY]: (Optional) `sim_failure_rate` for resilience testing.
# 9. [JSON RESILIENCE]: Corrupt flag files are logged and ignored, not fatal.
# 10. [TELEMETRY HOOK]: Flag activations are scribed to the verbose log.
# 11. [DEFAULT FALLBACK]: Robust defaults if no configuration exists.
# 12. [POLYMORPHIC ROOT]: Handles requests with or without project context.

import os
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("FlagWarden")


class FeatureFlagMiddleware(Middleware):
    """
    The Gatekeeper of Mutable Reality.
    Intercepts every request to apply dynamic configuration overlays.
    """

    FLAGS_FILENAME = "flags.json"
    CACHE_TTL = 5.0  # Seconds

    def __init__(self, engine: Any):
        # Cache Structure: { path_key: (timestamp, flags_dict) }
        super().__init__(engine)
        self._cache: Dict[str, Any] = {}

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:

        # 1. RESOLVE PROJECT ROOT (THE FIX)
        # We perform a defensive cast to ensure we are working with a Path object.
        # This resolves the `TypeError: unsupported operand type(s) for /: 'str' and 'str'`
        project_root: Optional[Path] = None
        if hasattr(request, 'project_root') and request.project_root:
            if isinstance(request.project_root, str):
                project_root = Path(request.project_root)
            elif isinstance(request.project_root, Path):
                project_root = request.project_root

        # 2. HARVEST FLAGS (HIERARCHICAL)
        flags = self._resolve_flags(project_root)

        if not flags:
            return next_handler(request)

        # 3. THE RITE OF MODIFICATION

        # A. The Kill Switch (Block Rites)
        # Check if this specific request type has been banned
        rite_name = type(request).__name__
        # Example: "disable_ShadowCloneRequest": true
        if flags.get(f"disable_{rite_name}"):
            Logger.warn(f"Rite '{rite_name}' intercepted by Kill Switch.")
            raise ArtisanHeresy(
                f"Feature Flag Block: The '{rite_name}' is currently disabled by the Architect.",
                suggestion="Check .scaffold/flags.json or environment variables."
            )

        # B. Variable Injection (Enable Beta Features)
        # Inject any flag starting with "feat_" into the request variables
        if hasattr(request, 'variables') and isinstance(request.variables, dict):
            injected_count = 0
            for k, v in flags.items():
                if k.startswith("feat_"):
                    # Only inject if not already present (Request takes precedence? Or Flags? Let's say Flags override default)
                    if k not in request.variables:
                        request.variables[k] = str(v)
                        injected_count += 1

            if injected_count > 0:
                Logger.debug(f"Injected {injected_count} feature flags into context.")

        # C. Runtime Strategy Override
        # Allow flags to force a specific execution runtime (e.g. force docker everywhere)
        if flags.get("force_runtime"):
            target_runtime = flags.get("force_runtime")
            if hasattr(request, 'runtime'):
                old_runtime = getattr(request, 'runtime', 'auto')
                if old_runtime != target_runtime:
                    request.runtime = target_runtime
                    Logger.warn(f"Runtime Override Active: {old_runtime} -> {target_runtime}")

        # D. The Chaos Monkey (Resilience Testing)
        # Randomly fail requests if configured (Default: 0.0)
        failure_rate = float(flags.get("sim_failure_rate", 0.0))
        if failure_rate > 0:
            import random
            if random.random() < failure_rate:
                raise ArtisanHeresy("Simulated Chaos Failure (Flag Active)")

        return next_handler(request)

    def _resolve_flags(self, project_root: Optional[Path]) -> Dict[str, Any]:
        """
        Merges configuration from all dimensional layers.
        Layer 1: System Global (/etc) - Lowest Priority
        Layer 2: User Global (~/.scaffold)
        Layer 3: Project Local (.scaffold/)
        Layer 4: Environment Variables (SCAFFOLD_FLAG_*) - Highest Priority
        """
        # Cache Key based on root
        cache_key = str(project_root) if project_root else "global"
        now = time.time()

        # Check Cache
        if cache_key in self._cache:
            ts, cached_flags = self._cache[cache_key]
            if now - ts < self.CACHE_TTL:
                return cached_flags

        merged_flags = {}

        # 1. System Global (Platform dependent, simplified for now)
        # (Skipped for portability, but slot available here)

        # 2. User Global
        user_global_path = Path.home() / ".scaffold" / self.FLAGS_FILENAME
        merged_flags.update(self._read_json_safe(user_global_path))

        # 3. Project Local
        if project_root:
            local_path = project_root / ".scaffold" / self.FLAGS_FILENAME
            merged_flags.update(self._read_json_safe(local_path))

        # 4. Environment Variables
        # SCAFFOLD_FLAG_DISABLE_SHADOWCLONEREQUEST=true
        prefix = "SCAFFOLD_FLAG_"
        for k, v in os.environ.items():
            if k.startswith(prefix):
                flag_key = k[len(prefix):].lower()  # Normalize to lowercase keys

                # Type inference for Env Vars
                clean_val: Any = v
                if v.lower() == 'true':
                    clean_val = True
                elif v.lower() == 'false':
                    clean_val = False
                elif v.isdigit():
                    clean_val = int(v)

                merged_flags[flag_key] = clean_val

        # Update Cache
        self._cache[cache_key] = (now, merged_flags)
        return merged_flags

    def _read_json_safe(self, path: Path) -> Dict[str, Any]:
        """Reads a JSON file without crashing the daemon on corruption."""
        if not path.exists():
            return {}

        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception as e:
            Logger.warn(f"Corrupt Flag File Ignored ({path}): {e}")
            return {}