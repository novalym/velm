# Path: scaffold/artisans/heal/contracts.py
# -----------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class HealingDiagnosis:
    """
    A vessel containing the Gnosis of a specific wound.
    """
    file_path: Path
    healer_name: str
    description: str
    severity: str = "WARNING"  # INFO, WARNING, CRITICAL
    fix_available: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealingResult:
    """
    The chronicle of a performed miracle.
    """
    file_path: Path
    healer_name: str
    success: bool
    changes_made: bool
    message: str
    diff: Optional[str] = None


class BaseHealer(ABC):
    """
    The Abstract Soul of a Healer.
    Specific healers (ImportHealer, StyleHealer, TypeHealer) must inherit this.
    """

    def __init__(self, project_root: Path, context: Dict[str, Any]):
        self.project_root = project_root
        self.context = context

    @property
    @abstractmethod
    def name(self) -> str:
        """The Gnostic Name of the Specialist."""
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """The file extensions this healer is sworn to protect."""
        pass

    def can_heal(self, file_path: Path) -> bool:
        """Determines if the scripture falls within this healer's jurisdiction."""
        return file_path.suffix in self.supported_extensions

    @abstractmethod
    def diagnose(self, file_path: Path, content: str) -> List[HealingDiagnosis]:
        """Perceives the wounds within the scripture."""
        pass

    @abstractmethod
    def heal(self, file_path: Path, content: str, diagnoses: List[HealingDiagnosis]) -> Tuple[str, bool]:
        """
        Performs the laying on of hands.
        Returns: (new_content, changes_were_made)
        """
        pass

