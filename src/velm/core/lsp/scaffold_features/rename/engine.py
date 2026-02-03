# Path: core/lsp/scaffold_features/rename/engine.py
# -------------------------------------------------
from typing import Any
from ...base.features.rename.engine import RenameEngine
from .validator import ScaffoldRenameValidator
from .mutators import LocalMutator, CortexMutator


class ScaffoldRenameEngine:
    """
    =============================================================================
    == THE SCAFFOLD RENAME ENGINE (V-Ω-INTEGRATION-V12)                        ==
    =============================================================================
    The High Priest of Transmutation.
    Factory for binding Scaffold rewrite logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> RenameEngine:
        # 1. Awake the Iron Core
        engine = RenameEngine(server)

        # 2. Consecrate the Sacred Gatekeeper
        engine.register_validator(ScaffoldRenameValidator(server))

        # 3. Register the Council of Mutators
        # Priority 100: Instant Local Rewrite
        engine.register_mutator(LocalMutator(server))

        # Priority 50: Project-Wide Causal Shockwave (via Daemon)
        engine.register_mutator(CortexMutator(server))

        return engine