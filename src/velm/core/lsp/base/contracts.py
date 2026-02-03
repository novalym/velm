# Path: core/lsp/base/contracts.py
# -------------------------------
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class BaseGnosticObject:
    """
    [THE ANCESTRAL TRAIT]
    Provides consistent identification for every object within the Iron Core.
    """
    def __init__(self, name: str):
        self._gnostic_name = name

    @property
    def identity(self) -> str:
        return self._gnostic_name

    def __repr__(self):
        return f"<Gnostic:{self._gnostic_name}>"



# [ASCENSION 11]: TYPE-STRICT FOUNDATION
class CapabilityProclamation(BaseModel):
    """Vessel for dynamic capability negotiation."""
    textDocumentSync: int = 2 # Incremental
    hoverProvider: bool = False
    completionProvider: Optional[Dict[str, Any]] = None
    definitionProvider: bool = False
    documentSymbolProvider: bool = False
    codeActionProvider: bool = False
    renameProvider: Optional[Dict[str, Any]] = None
    executeCommandProvider: Optional[Dict[str, List[str]]] = None

