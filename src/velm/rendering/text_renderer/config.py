# Path: scaffold/rendering/text_renderer/config.py
# ------------------------------------------------
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from ..theme import GnosticTheme

@dataclass
class RendererConfig:
    """
    The Gnostic Configuration for the Text Renderer.
    Encapsulates all flags and context required for proclamation.
    """
    theme: GnosticTheme = field(default_factory=GnosticTheme)
    variables: Dict[str, Any] = field(default_factory=dict)
    post_run_commands: List[str] = field(default_factory=list)
    verbose: bool = False
    pure_structure: bool = False
    app_state: Optional[Any] = None  # Type hint Any to avoid circular import with AppState