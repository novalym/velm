# Path: scaffold/core/ignition/diviner/sentinel/priest.py
# -------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: SENTINEL_PRIEST_V1

import threading
import time
from pathlib import Path
from typing import Dict, Tuple, List, Optional

from .scanner import ArtisanScanner
from .vitality import VitalityProbe
from .biology import BiologicalAuditor
from .grimoire import TOOL_GRIMOIRE
from ..contracts import IgnitionAura, BiologicalSupport
from ....logger import Scribe

Logger = Scribe("ToolchainSentinel")


class ToolchainSentinel:
    """
    =================================================================================
    == THE HIGH PRIEST OF THE TOOLCHAIN (V-Ω-TOTALITY-ASCENDED)                    ==
    =================================================================================
    LIF: INFINITY | The Supreme Watcher of OS Matter.
    """

    # [ASCENSION 12]: ATOMIC STATE CACHE
    _cache: Dict[str, Dict] = {}
    _lock = threading.Lock()

    @classmethod
    def scry_artisan(cls, name: str) -> Tuple[bool, str, str]:
        """
        The entry point for tool verification.
        Returns (exists, path, redemption_advice).
        """
        with cls._lock:
            cached = cls._cache.get(name)
            if cached and (time.time() - cached['ts'] < 300):
                return True, cached['path'], ""

        # 1. SCAN
        path = ArtisanScanner.find_binary(name)
        if not path:
            advice = TOOL_GRIMOIRE.get(name, {}).get("redemption", f"Install {name}")
            return False, "", f"Heresy: {name} is missing. Remedy: {advice}"

        # 2. PROBE
        config = TOOL_GRIMOIRE.get(name, {})
        is_healthy, version = VitalityProbe.check_health(path, config.get("check_cmd"))

        if not is_healthy:
            return False, str(path), f"Heresy: {name} is manifest at {path} but inert ({version})."

        # 3. CACHE
        with cls._lock:
            cls._cache[name] = {"path": str(path), "ts": time.time(), "ver": version}

        return True, str(path), ""

    @classmethod
    def verify_biological_support(cls, root: Path, aura: IgnitionAura) -> BiologicalSupport:
        """
        [ASCENSION 16]: Materializes a BiologicalSupport vessel.
        """
        missing = BiologicalAuditor.audit_lungs(root, aura)

        manifest_map = {
            IgnitionAura.VITE: "package.json",
            IgnitionAura.NEXT: "package.json",
            IgnitionAura.FASTAPI: "pyproject.toml/requirements.txt",
            IgnitionAura.CARGO: "Cargo.toml"
        }

        # [ASCENSION 15]: HAPTIC REDEMPTION
        # Mapping missing parts to install commands
        remedy = None
        if "node_modules" in missing:
            remedy = "npm install"
        elif "virtual_environment" in missing:
            remedy = "python -m venv .venv && source .venv/bin/activate"

        return BiologicalSupport(
            manifest_type=manifest_map.get(aura, "generic"),
            is_installed=len(missing) == 0,
            missing_elements=missing,
            suggested_install_cmd=remedy
        )

    @classmethod
    def find_best_node_artisan(cls, root: Path) -> str:
        """
        [ASCENSION 6]: Advanced PM Triage.
        """
        if (root / "bun.lockb").exists(): return "bun"
        if (root / "pnpm-lock.yaml").exists(): return "pnpm"
        if (root / "yarn.lock").exists(): return "yarn"
        return "npm"

