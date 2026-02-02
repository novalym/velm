# Path: core/lsp/features/hover/contracts.py
# ------------------------------------------
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path


@dataclass(frozen=True)
class HoverContext:
    """
    =============================================================================
    == THE VESSEL OF AURA (CONTEXT)                                            ==
    =============================================================================
    Captures the logical spacetime surrounding a cursor coordinate.
    """
    uri: str
    file_path: Path
    language_id: str
    line_text: str
    full_content: str
    position: Dict[str, int]  # {'line': int, 'character': int}
    word: str
    word_range: Dict[str, Any]
    workspace_root: Optional[Path] = None
    trace_id: str = "0xVOID"


class HoverProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF WISDOM (INTERFACE)                                      ==
    =============================================================================
    The abstract soul of a documentation source.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the knowledge source."""
        pass

    @property
    def priority(self) -> int:
        """Higher numbers appear first in the UI (0-100)."""
        return 50

    @abstractmethod
    def provide(self, context: HoverContext) -> Optional[Union[str, List[str], Dict[str, Any]]]:
        """
        The Rite of Revelation.
        Returns Markdown strings or structured data for the Hover view.
        """
        pass

