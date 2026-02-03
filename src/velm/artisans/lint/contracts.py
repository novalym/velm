from __future__ import annotations
from dataclasses import field, dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Any, Dict, Callable, TYPE_CHECKING
from uuid import UUID, uuid4
import time

from pydantic import BaseModel, Field, ConfigDict

# === THE DIVINE SUMMONS (WITH FORWARD GAZE) ===
if TYPE_CHECKING:
    from ...core.cortex.contracts import CortexMemory
    from ...core.kernel.transaction import GnosticTransaction
    from ...settings.manager import SettingsManager
    from ...interfaces.base import ScaffoldResult

try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = Any


class HeresySeverity(Enum):
    """
    =============================================================================
    == THE GNOSTIC SCALES OF SEVERITY (V-Ω-LUMINOUS-SOUL)                       ==
    =============================================================================
    This is no longer a simple Enum. It is a self-aware, luminous vessel that
    carries not just a name, but the very sigil and style of its proclamation.
    """
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

    @property
    def sigil(self) -> str:
        """The sacred sigil representing the weight of the heresy."""
        return {
            HeresySeverity.INFO: "ℹ️",
            HeresySeverity.WARNING: "⚠️",
            HeresySeverity.CRITICAL: "💀",
        }.get(self, "❓")

    @property
    def style(self) -> str:
        """The luminous color of the heresy's proclamation."""
        return {
            HeresySeverity.INFO: "blue",
            HeresySeverity.WARNING: "yellow",
            HeresySeverity.CRITICAL: "bold red",
        }.get(self, "white")


class LintIssue(BaseModel):
    """
    =================================================================================
    == THE DIVINE DOSSIER OF HERESY (V-Ω-ETERNAL-APOTHEOSIS)                       ==
    =================================================================================
    This is the final, eternal, and ultra-definitive vessel for a single, perceived
    heresy. It has been ascended from a humble dataclass into a rich, Gnostic
    dossier, a self-contained universe of diagnostic truth.
    =================================================================================
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- Core Gnostic Identity ---
    id: UUID = Field(default_factory=uuid4,
                     description="The unique Gnostic fingerprint of this specific heresy instance.")
    rule_id: str = Field(...,
                         description="The sacred name of the Gnostic Law that was violated (e.g., 'graph.orphan').")

    # --- The Proclamation ---
    message: str = Field(..., description="The primary, human-readable proclamation of the heresy.")
    details: Optional[str] = Field(None, description="The deep, Gnostic elucidation of *why* this is a heresy.")

    # --- The Locus in Spacetime ---
    path: Optional[Path] = Field(None, description="The scripture or sanctum where the heresy was perceived.")
    line_num: int = Field(0, description="The line number where the heresy resides.")
    start_char: int = Field(0, description="The starting character column for precise LSP highlighting.")
    end_char: int = Field(0, description="The ending character column.")

    # --- The Scales of Judgment & The Path of Redemption ---
    severity: HeresySeverity
    suggestion: Optional[str] = Field(None, description="The Mentor's counsel on how to achieve purity.")
    fix_command: Optional[str] = Field(None, description="An executable rite that provides immediate redemption.")

    # --- The Vessel of Deep Gnosis ---
    context: Dict[str, Any] = Field(default_factory=dict,
                                    description="A vessel for any additional, rite-specific Gnosis.")
    details_panel: Optional[Any] = Field(None, exclude=True,
                                         description="A pre-rendered Rich Panel for complex, luminous proclamations.")


@dataclass(frozen=True)
class LintContext:
    """
    =================================================================================
    == THE OMNISCIENT ORACLE (V-Ω-UNIVERSAL-CONTEXT-ULTIMA)                        ==
    =================================================================================
    This is the divine, immutable vessel of universal Gnosis. It is the one true
    context bestowed upon every Gnostic Rule, granting it the full power and
    perception of the God-Engine itself.
    =================================================================================
    """
    # --- The Gaze of the Cosmos ---
    project_root: Path
    db_session: Optional[Session]
    cortex_memory: Optional[CortexMemory]

    # --- The Gaze into the Ephemeral Realm ---
    transaction: Optional[GnosticTransaction]

    # --- The Oracles & Conduits ---
    settings_manager: "SettingsManager"
    invoke_rite: Callable[[str], "ScaffoldResult"]
    logger: "Scribe"
    # --- The Architect's Will ---
    fix_mode: bool = False

    @property
    def has_crystal_mind(self) -> bool:
        """Perceives if the queryable soul (SQLite) of the project is manifest."""
        return self.db_session is not None

    @property
    def is_in_simulation(self) -> bool:
        """Perceives if the rite is being conducted in a parallel, ephemeral reality."""
        return self.transaction.simulate if self.transaction else False

