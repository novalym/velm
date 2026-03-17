# Path: core/structure_sentinel/strategies/python_strategy/frameworks/contracts.py
# --------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .engine import FrameworkFaculty


@dataclass
class InjectionPlan:
    """
    =============================================================================
    == THE INJECTION PLAN (V-Ω-TOTALITY-VMAX-METADATA-SUTURE)                  ==
    =============================================================================
    LIF: ∞^∞ | ROLE: SURGICAL_BLUEPRINT | RANK: OMEGA_GUARDIAN

    The absolute blueprint for a surgical insertion. It has been ascended
    to carry `metadata`, preventing the AttributeError paradox during
    Laminar Sanctuary Triage. This mathematically guarantees that the
    ASTSurgeon receives its spatial coordinates without fracturing.
    """
    target_file: Path
    import_stmt: str
    wiring_stmt: str
    anchor: str  # The AST node or string to attach to
    strategy_name: str

    # [THE MASTER CURE]: The Laminar Sanctuary Metadata Suture.
    # Defaults to an empty dict to perfectly preserve backward compatibility
    # with legacy strategies while empowering FastAPI and Panopticon.
    metadata: Dict[str, Any] = field(default_factory=dict)


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
        """Surgically calculates what to insert and where."""
        pass