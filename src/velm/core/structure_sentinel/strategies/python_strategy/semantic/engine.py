# Path: core/structure_sentinel/strategies/python_strategy/semantic/engine.py
# ---------------------------------------------------------------------------

from __future__ import annotations
import time
import traceback
import threading
import collections
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .harvester import SymbolHarvester
from .weaver import ImportWeaver
from .guardian import ApiGuardian
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class SemanticFaculty(BaseFaculty):
    """
    =================================================================================
    == THE OMEGA SEMANTIC FACULTY (V-Ω-TOTALITY-V100M-GRANULAR-SYNC)               ==
    =================================================================================
    LIF: ∞ | ROLE: HIGH_PRIEST_OF_MEANING | RANK: OMEGA_SOVEREIGN
    """

    _GLOBAL_FILE_LOCKS: Dict[str, threading.RLock] = collections.defaultdict(threading.RLock)
    _GLOBAL_LOCKS_MUTEX = threading.Lock()

    def __init__(self, logger: 'Scribe'):
        super().__init__(logger)
        self.harvester = SymbolHarvester()
        self.weaver = ImportWeaver(logger)
        self.guardian = ApiGuardian(logger)

    def _get_target_lock(self, target_path: Path) -> threading.RLock:
        path_key = str(target_path.resolve())
        with self._GLOBAL_LOCKS_MUTEX:
            return self._GLOBAL_FILE_LOCKS[path_key]

    def register_symbols(
            self,
            file_path: Path,
            context: "SharedContext"
    ):
        """
        =================================================================================
        == THE RITE OF SYMBOLIC CONSECRATION (V-Ω-TOTALITY-UNIFIED)                    ==
        =================================================================================
        """
        # =========================================================================
        # ==[ASCENSION 13]: THE APOPHATIC SELF-REFLECTION WARD (THE CURE)       ==
        # =========================================================================
        # Mathematically prevents Anomaly III (The Ouroboros Import Loop).
        # `__init__.py` and `__main__.py` represent pure architectural geometry;
        # they must NEVER harvest their own souls and inject them as self-imports.
        if file_path.name in ("__init__.py", "__main__.py"):
            self.logger.verbose(f"Laminar Ward: '{file_path.name}' is exempt from auto-harvesting its own soul.")
            return

        # 1. THE GAZE OF PERCEPTION (READ SOURCE)
        content = self._read(file_path, context)
        if not content:
            return

        # 2. THE HARVEST OF THE SOUL
        symbols = self.harvester.harvest(file_path, content)
        if not symbols:
            return

        # 3. LOCATE THE TARGET SCRIPTURE
        init_path = file_path.parent / "__init__.py"

        # 4. ACQUIRE SURGICAL LOCK
        file_lock = self._get_target_lock(init_path)

        with file_lock:
            self._conduct_injection_rite(init_path, file_path.stem, symbols, context)

    def _conduct_injection_rite(self, init_path: Path, module_name: str, symbols: List[str], context: "SharedContext"):
        """
        Surgically weaves symbols into the __init__.py soul via the transactional hand.
        """
        original_content = self._read(init_path, context)
        current_content = original_content

        #[ASCENSION 14]: VOID CONSECRATION
        if not current_content.strip():
            gnosis = getattr(context.transaction, 'context', {}) if context.transaction else {}
            is_root_pkg = self.geometer.is_root_package(init_path.parent, context.project_root)
            license_header = self.scribe.get_license_header(context.project_root)
            effective_dir = self._resolve_effective_directory(init_path.parent, context)

            current_content = self.scribe.forge_init(
                directory=effective_dir,
                is_root=is_root_pkg,
                license_header=license_header,
                package_name=init_path.parent.name,
                gnosis=gnosis
            )
            original_content = ""

        #[ASCENSION 15]: Ensure annotations are warded for modern typing.
        current_content = self._ensure_future_sight(current_content)

        # [ASCENSION 16]: Inject the 'from .module import Symbol' edicts.
        current_content = self.weaver.weave(current_content, module_name, symbols)

        # [ASCENSION 17]: Reconstruct the __all__ list via the ApiGuardian.
        current_content = self.guardian.guard(current_content, symbols, context)

        # [ASCENSION 18]: Idempotency check.
        if current_content == original_content:
            return

        self.logger.success(
            f"   -> Semantic Integration: [cyan]{module_name}[/] -> [white]{init_path.name}[/] #SUCCESS"
        )

        self._write(init_path, current_content, context)

    def _ensure_future_sight(self, content: str) -> str:
        """[ASCENSION 19]: THE FUTURE SIGHT."""
        if "from __future__ import annotations" in content:
            return content

        lines = content.splitlines()
        insert_idx = 0
        in_docstring = False
        docstring_quote = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                insert_idx = i + 1
                continue
            if stripped.startswith("#"):
                insert_idx = i + 1
                continue

            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    in_docstring = True
                    docstring_quote = stripped[:3]
                    if stripped.count(docstring_quote) >= 2 and len(stripped) > 3:
                        insert_idx = i + 1
                        break
                    continue

            if in_docstring:
                if docstring_quote in stripped:
                    in_docstring = False
                    insert_idx = i + 1
                    break
                continue

            break

        lines.insert(insert_idx, "from __future__ import annotations")

        if insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, "")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Ω_SEMANTIC_FACULTY status=RESONANT mode=GRANULAR_SUTURE version=100000.0>"