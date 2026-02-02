# Path: core/lsp/scaffold_features/signature_help/engine.py
# ----------------------------------------------------------
from typing import Any
from ...base.features.signature_help.engine import SignatureHelpEngine
from .providers import (
    MacroSignatureProvider,
    AlchemistSignatureProvider,
    DaemonSignatureProvider
)


class ScaffoldSignatureEngine:
    """
    =============================================================================
    == THE SCAFFOLD SIGNATURE ENGINE (V-Ω-INTEGRATION-V12)                     ==
    =============================================================================
    The High Priest of Invocations.
    Factory for binding Scaffold parameter logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> SignatureHelpEngine:
        # 1. Awake the Iron Core
        engine = SignatureHelpEngine(server)

        # 2. Consecrate and Register the Scaffold Prophets
        # Order determines the search priority (Local > Global)
        engine.register(MacroSignatureProvider(server))  # Priority 100: Local @macros
        engine.register(AlchemistSignatureProvider(server))  # Priority 90:  Built-ins
        engine.register(DaemonSignatureProvider(server))  # Priority 50:  Daemon Cortex

        return engine