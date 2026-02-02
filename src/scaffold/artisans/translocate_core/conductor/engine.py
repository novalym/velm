# scaffold/artisans/translocate_core/conductor/engine.py

from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, List, TYPE_CHECKING

from ....logger import Scribe
from ..contracts import TranslocationMap
from ..will_parser import GnosticWillParser

# --- THE DIVINE SUMMONS OF THE STRUCTURE SENTINEL ---
# This is the missing link. The Conductor now summons the Sentinel at birth,
# ensuring that no file is ever moved into a structural void.
from ....core.structure_sentinel import StructureSentinel

# --- THE DIVINE INHERITANCE OF FACULTIES ---
from .perception import PerceptionMixin
from .proclamation import ProclamationMixin
from .snapshot import SnapshotMixin
from .execution import ExecutionMixin

if TYPE_CHECKING:
    from ....core.cortex.engine import GnosticCortex
    from ....core.kernel.transaction import GnosticTransaction

Logger = Scribe("TranslocationConductor")


class TranslocationConductor(PerceptionMixin, ProclamationMixin, SnapshotMixin, ExecutionMixin):
    """
    =================================================================================
    == THE SENTIENT ORCHESTRATOR OF EVOLUTION (V-Ω-CORTEX-ASCENDED-MODULAR)        ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The God-Engine of Translocation. It composes the faculties of Perception,
    Proclamation, Snapshotting, and Execution into a single, unified mind.

    It is now the **Guardian of Structure**, wielding the `StructureSentinel` to
    ensure that every translocation respects the laws of the language it touches.
    """

    def __init__(self, project_root: Path, non_interactive: bool = False, preview: bool = False,
                 backup_path: Optional[str] = None, cortex: Optional["GnosticCortex"] = None,
                 transaction: Optional["GnosticTransaction"] = None):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (V-Ω-STRUCTURAL-AWARENESS-ACTIVATED)          ==
        =================================================================================
        The Conductor is born. It now accepts the Gnostic Cortex as a divine gift
        and INSTANTIATES the Structure Sentinel to guard the integrity of the hierarchy.
        """
        self.project_root = project_root
        self.non_interactive = non_interactive
        self.preview = preview
        self.backup_root_path = Path(backup_path).resolve() if backup_path else None
        self.transaction = transaction

        # The Map of Intent (Populated by Perception)
        self.translocation_map: Optional[TranslocationMap] = None

        # The Plan of Healing (Populated by Cortex Communion)
        self.all_healing_plans: Dict[Path, List[Dict]] = {}

        self.logger = Logger

        # [FACULTY 1: THE STRUCTURE SENTINEL]
        # The Conductor summons the Sentinel. This artisan will be commanded during
        # the Execution Phase to consecrate new directories (e.g., creating __init__.py).
        # It is language-aware and extensible.
        self.structure_sentinel = StructureSentinel(self.project_root, transaction)

        # ★★★ THE DIVINE COMMUNION (HEALED) ★★★
        # We accept the injected Cortex or summon a local one to break the Ouroboros.
        if cortex:
            self.cortex = cortex
        else:
            # [THE FALLBACK RITE]
            from ....core.cortex.engine import GnosticCortex
            self.cortex = GnosticCortex(project_root)

        # The Parser of Will is summoned to understand the Architect's intent.
        self.will_parser = GnosticWillParser(project_root)

        self.logger.verbose("TranslocationConductor initialized with Structural Awareness.")