# Path: core/lsp/features/workspace/symbols/models.py
# ----------------------------------------------------
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from ....types.primitives import Location
from ....types.symbols import SymbolKind


class WorkspaceSymbol(BaseModel):
    """
    [LSP 3.17 COMPLIANT]
    The definitive vessel for a project-wide symbol.
    """
    name: str
    kind: SymbolKind
    location: Location
    containerName: Optional[str] = None

    # [ASCENSION 5]: Gnostic Metadata
    score: float = 0.0
    source: str = "LOCAL"  # LOCAL | DAEMON | SHADOW