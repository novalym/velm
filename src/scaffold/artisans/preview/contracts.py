# Path: scaffold/artisans/preview/contracts.py
# =================================================================================
# == THE PREVIEW COVENANT (V-Ω-SCHEMA)                                          ==
# =================================================================================
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from ...interfaces.requests import BaseRequest


@dataclass
class UIElement:
    """The Atomic Unit of a UI Wireframe."""
    type: str  # 'container', 'text', 'button', 'input', 'image', 'component'
    name: str  # 'div', 'span', 'MyComponent'
    props: Dict[str, Any] = field(default_factory=dict)
    children: List['UIElement'] = field(default_factory=list)

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "props": self.props,
            "children": [c.to_dict() for c in self.children]
        }



