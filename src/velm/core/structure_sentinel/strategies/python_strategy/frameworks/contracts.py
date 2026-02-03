# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/contracts.py
# -----------------------------------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import FrameworkFaculty


@dataclass
class InjectionPlan:
    """The blueprint for a surgical insertion."""
    target_file: Path
    import_stmt: str
    wiring_stmt: str
    anchor: str  # The AST node or string to attach to
    strategy_name: str


class WiringStrategy(ABC):
    """
    The Sacred Contract for Framework Injection.
    """

    def __init__(self, faculty: 'FrameworkFaculty'):
        self.faculty = faculty

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def detect(self, content: str) -> Optional[str]:
        """Returns the variable name of the component to wire (e.g. 'router')."""
        pass

    @abstractmethod
    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """Locates the main application entry point."""
        pass

    @abstractmethod
    def forge_injection(self, source_path: Path, component_var: str, target_content: str, root: Path) -> Optional[
        InjectionPlan]:
        """
        Surgically calculates what to insert and where.
        """
        pass

