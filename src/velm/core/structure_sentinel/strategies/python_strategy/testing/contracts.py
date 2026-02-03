# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/testing/contracts.py
# ---------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class ArgumentGnosis:
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None

@dataclass
class TestableUnit:
    """A function or method to be tested."""
    name: str
    is_async: bool = False
    args: List[ArgumentGnosis] = field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    is_method: bool = False
    parent_class: Optional[str] = None
    complexity: int = 1

@dataclass
class TestFileBlueprint:
    """The plan for the test file."""
    source_module: str
    units: List[TestableUnit]
    imports: List[str] = field(default_factory=list)
    has_classes: bool = False