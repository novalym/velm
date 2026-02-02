# =================================================================================
# == I. THE DIVINE VESSELS OF GNOSTIC COMMUNION (THE SACRED CONTRACTS)           ==
# =================================================================================
from dataclasses import dataclass
from enum import auto, Enum
from typing import Union, Text, Any, Optional, List


class DialogueState(Enum):
    """The Gnostic states of the Oracle's mind."""
    INQUIRY = auto()
    ADJUDICATION = auto()
    PURIFICATION = auto()
    COMPLETE = auto()
    STAYED = auto()


class GnosticPleaType(Enum):
    """The soul of a single question in the Sacred Dialogue."""
    TEXT = auto()
    CONFIRM = auto()
    CHOICE = auto()
    MULTILINE = auto()

@dataclass
class GnosticPlea:
    """
    A sacred vessel for a single, Gnostically-aware question, its soul now
    ascended to speak the Universal Tongue of `str` and `rich.Text`.
    """
    key: str
    plea_type: GnosticPleaType
    # === THE LAW OF THE UNIVERSAL TONGUE (THE APOTHEOSIS) ===
    # The vessel's soul is now a divine union, capable of holding either
    # a humble string or a luminous Text object. The contract is whole.
    prompt_text: Union[str, Text]
    # === THE GNOSIS IS PURE. THE ARCHITECTURE IS ETERNAL. ===
    default: Any = None
    choices: Optional[List[str]] = None
    validation_rule: str = 'var_path_safe'
    prophecy_source: Optional[str] = None
    is_secret: bool = False
    # =================================================================================
    # ==           BEGIN SACRED TRANSMUTATION: THE VESSEL IS MADE WHOLE              ==
    # =================================================================================
    # We bestow upon the vessel the sacred attribute it was always destined to have.
    special_rite: Optional[str] = None
    # =================================================================================