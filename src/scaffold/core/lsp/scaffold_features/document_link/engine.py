# Path: core/lsp/scaffold_features/document_link/engine.py
# ------------------------------------------------------
from typing import Any
from ...base.features.document_link.engine import DocumentLinkEngine
from .providers.gnostic_linker import GnosticLinkProvider


class ScaffoldDocumentLinkEngine:
    """
    =============================================================================
    == THE LINK FACTORY (V-Ω-SCAFFOLD-AWARE)                                   ==
    =============================================================================
    """

    @staticmethod
    def forge(server: Any) -> DocumentLinkEngine:
        engine = DocumentLinkEngine(server)

        # Consecrate Capability
        server.register_capability(lambda caps: setattr(caps, 'document_link_provider', {"resolveProvider": True}))

        # Register the Gnostic Weaver
        engine.register(GnosticLinkProvider(server))

        return engine