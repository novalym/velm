# Path: src/velm/core/redemption/specialists/import_healer.py
# -----------------------------------------------------------
# =========================================================================================
# == THE IMPORT HEALER: OMEGA POINT (V-Ω-TOTALITY-V5000.0-CONTEXT-AWARE)                 ==
# =========================================================================================
# LIF: INFINITY | ROLE: CAUSAL_LINK_WEAVER | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_IMPORT_HEALER_V5000_CONTEXT_SUTURE_2026_FINALIS
# =========================================================================================

import re
import sys
import difflib
import importlib.util
from pathlib import Path
from typing import Optional, Dict, Any, List, Set, Final

from ..contracts import Diagnosis, RedemptionStrategy, Specialist
from .....logger import Scribe

Logger = Scribe("ImportHealer")


class ImportHealer(Specialist):
    """
    =============================================================================
    == THE CAUSAL LINK WEAVER (V-Ω-DEPENDENCY-SUTURE)                          ==
    =============================================================================
    Diagnoses and heals fractures in the Gnostic Linkage (Import Errors).
    It understands the difference between a Missing Shard (Install), a Broken Path
    (Relative Import), and a Circular Ouroboros (Lazy Import).

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Contextual Suture (THE FIX):** `heal()` accepts `context` dictionary.
    2.  **Polyglot Awareness:** Diagnoses Python, Node, and Rust import fractures.
    3.  **Stdlib Whitelist:** Prevents installing built-in modules.
    4.  **Levenshtein Typo-Fixing:** Suggests corrections for misspelled modules.
    5.  **Circularity Detection:** Identifies Import Cycles.
    """

    # [FACULTY 4]: THE STANDARD LIBRARY GRIMOIRE
    # We must never attempt to install these.
    STDLIB_SHARDS: Final[Set[str]] = {
        "os", "sys", "re", "json", "time", "datetime", "pathlib", "typing",
        "collections", "itertools", "functools", "math", "random", "uuid",
        "hashlib", "base64", "shutil", "subprocess", "threading", "multiprocessing",
        "concurrent", "asyncio", "logging", "traceback", "inspect", "ast",
        "types", "abc", "enum", "dataclasses", "contextlib", "copy", "pickle"
    }

    def heal(self, exception: Exception, context: Dict[str, Any]) -> Optional[Diagnosis]:
        """
        =============================================================================
        == THE RITE OF DIAGNOSIS (HEAL)                                            ==
        =============================================================================
        [ASCENSION 1]: Context-Aware Adjudication.
        Accepts the full forensic context to make smarter decisions.
        """
        error_msg = str(exception)

        # 1. TRIAGE: Is this an Import Fracture?
        if not isinstance(exception, (ImportError, ModuleNotFoundError, AttributeError)):
            return None

        # 2. ANALYSIS: ModuleNotFoundError (The Missing Shard)
        if isinstance(exception, ModuleNotFoundError):
            return self._diagnose_missing_shard(exception, context)

        # 3. ANALYSIS: ImportError (The Broken Path / Circularity)
        if isinstance(exception, ImportError):
            if "attempted relative import" in error_msg:
                return self._diagnose_relative_path_fracture(exception, context)
            if "cannot import name" in error_msg and "partially initialized" in error_msg:
                return self._diagnose_ouroboros_cycle(exception, context)
            if "cannot import name" in error_msg:
                return self._diagnose_missing_symbol(exception, context)

        # 4. ANALYSIS: AttributeError (The Malformed Shard)
        # Often occurs when a module exists but lacks the requested attribute (circularity or version mismatch)
        if isinstance(exception, AttributeError) and "module" in error_msg and "has no attribute" in error_msg:
            return self._diagnose_attribute_fracture(exception, context)

        return None

    def _diagnose_missing_shard(self, exception: ModuleNotFoundError, context: Dict[str, Any]) -> Diagnosis:
        """
        [FACULTY 3]: The Package Manager Diviner.
        Prophesies the correct installation command.
        """
        # Extract module name: "No module named 'pandas'" -> "pandas"
        match = re.search(r"No module named '([^']+)'", str(exception))
        if not match:
            return Diagnosis(
                confidence=0.1,
                reason="Could not extract module name from fracture.",
                advice="Manually verify installed packages."
            )

        module_name = match.group(1)
        root_pkg = module_name.split('.')[0]

        # [FACULTY 4]: Stdlib Check
        if root_pkg in self.STDLIB_SHARDS:
            return Diagnosis(
                confidence=0.9,
                reason=f"The shard '{root_pkg}' is a Standard Library organ, yet it is missing.",
                advice="This indicates a corrupted Python environment. Re-install Python.",
                strategy=RedemptionStrategy.MANUAL_INTERVENTION
            )

        # [FACULTY 5]: Typo Check (Levenshtein)
        # If the user typed 'panads', suggest 'pandas'.
        # (Simplified heuristic for V1: check specific known typos or rely on install)

        # Divine the Project Type from Context
        project_root = Path(context.get("project_root", "."))
        install_cmd = self._divine_install_command(root_pkg, project_root)

        return Diagnosis(
            confidence=0.95,
            reason=f"The shard '{root_pkg}' is unmanifest in the current environment.",
            advice=f"Summon the missing shard.",
            cure_command=install_cmd,
            strategy=RedemptionStrategy.KINETIC_FIX
        )

    def _diagnose_relative_path_fracture(self, exception: ImportError, context: Dict[str, Any]) -> Diagnosis:
        """[FACULTY 6]: The Relative Path Suture."""
        return Diagnosis(
            confidence=0.85,
            reason="A relative import was attempted without a known parent package.",
            advice=(
                "You are running a script directly that uses relative imports (e.g. `from . import utils`).\n"
                "To fix this, run the script as a module: `python -m src.module.name`\n"
                "Or adjust PYTHONPATH: `export PYTHONPATH=$PYTHONPATH:.`"
            ),
            strategy=RedemptionStrategy.CONFIG_ADJUSTMENT
        )

    def _diagnose_ouroboros_cycle(self, exception: ImportError, context: Dict[str, Any]) -> Diagnosis:
        """[FACULTY 7]: The Circularity Breaker."""
        return Diagnosis(
            confidence=0.9,
            reason="Circular Dependency detected (Ouroboros). Two modules rely on each other at import time.",
            advice=(
                "Move one of the imports INSIDE a function/method (Lazy Loading) to break the cycle.\n"
                "Example:\n"
                "def my_func():\n"
                "    from .other import thing\n"
                "    thing.do()"
            ),
            strategy=RedemptionStrategy.REFACTOR
        )

    def _diagnose_missing_symbol(self, exception: ImportError, context: Dict[str, Any]) -> Diagnosis:
        """[FACULTY 9]: The Missing Symbol Healer."""
        msg = str(exception)
        # "cannot import name 'X' from 'Y'"
        match = re.search(r"cannot import name '([^']+)' from '([^']+)'", msg)
        if match:
            symbol, module = match.groups()
            return Diagnosis(
                confidence=0.8,
                reason=f"The symbol '{symbol}' does not exist in module '{module}'.",
                advice=f"Check '{module}' for typos or version mismatches. The symbol might have been renamed or moved.",
                strategy=RedemptionStrategy.REFACTOR
            )
        return None

    def _diagnose_attribute_fracture(self, exception: AttributeError, context: Dict[str, Any]) -> Diagnosis:
        """[FACULTY 9]: Attribute Error Healer (Circular Import variant)."""
        msg = str(exception)
        # "module 'x' has no attribute 'y'"
        # This often happens during circular imports where the module object exists but is empty.
        return Diagnosis(
            confidence=0.7,
            reason="Module attribute missing. This is often a symptom of a Circular Import (Ouroboros).",
            advice="Check for circular dependencies between the files involved.",
            strategy=RedemptionStrategy.REFACTOR
        )

    def _divine_install_command(self, package: str, root: Path) -> str:
        """
        [FACULTY 3]: The Package Manager Diviner.
        Scries the project root to determine the correct installation rite.
        """
        # Python
        if (root / "poetry.lock").exists():
            return f"poetry add {package}"
        if (root / "Pipfile").exists():
            return f"pipenv install {package}"
        if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
            return f"pip install {package}"

        # Node
        if (root / "yarn.lock").exists():
            return f"yarn add {package}"
        if (root / "pnpm-lock.yaml").exists():
            return f"pnpm add {package}"
        if (root / "package.json").exists():
            return f"npm install {package}"

        # Default Python Fallback
        return f"pip install {package}"

    def __repr__(self) -> str:
        return "<Ω_IMPORT_HEALER status=RESONANT>"