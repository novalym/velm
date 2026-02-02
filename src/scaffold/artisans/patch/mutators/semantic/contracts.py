from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class SemanticTarget:
    """
    The located AST node where surgery will be performed.
    """
    name: str
    type: str  # 'class' or 'function'
    start_line: int
    end_line: int
    base_indent: str
    content_range: tuple[int, int]  # Byte offsets