# Path: scaffold/artisans/translocate_core/conductor/perception.py
# ----------------------------------------------------------------

from typing import List, Dict, Optional, TYPE_CHECKING
from pathlib import Path
import traceback  # [[[ THE DIVINE SUMMONS OF THE CHRONICLER'S SOUL ]]]

from ....contracts.heresy_contracts import ArtisanHeresy
from ..contracts import TranslocationMap
from ....logger import Scribe

if TYPE_CHECKING:
    from .engine import TranslocationConductor

# [[[ THE PREVIOUS HEALING REMAINS PURE AND CORRECT ]]]
Logger = Scribe("TranslocationPerception")


class PerceptionMixin:
    """
    =================================================================================
    == THE FACULTY OF PERCEPTION (V-Ω-INTENT-AWARE)                                ==
    =================================================================================
    Handles the `perceive_will` rite, transmuting raw intent into a Gnostic Plan.
    """

    def perceive_will(self: 'TranslocationConductor', origins: List[str] = None, destinations: List[str] = None,
                      script_path: Optional[str] = None, direct_moves: Optional[Dict[Path, Path]] = None):
        """
        =================================================================================
        == THE ORACLE OF INTENT (V-Ω-ETERNAL-APOTHEOSIS. THE PURE CONDUCTOR)           ==
        =================================================================================
        """
        try:
            # --- MOVEMENT I: THE AWAKENING OF THE GNOSTIC MIND ---
            self.cortex.perceive()

            # --- MOVEMENT II: THE FORGING OF THE GNOSTIC WILL PARSER ---
            # (Parser initialized in __init__)

            # --- MOVEMENT III: THE GNOSTIC TRIAGE & DIVINE DELEGATION ---
            moves = self.will_parser.perceive(
                origins=origins,
                destinations=destinations,
                script_path=script_path,
                direct_moves=direct_moves
            )

            # --- MOVEMENT IV: THE FINAL PROCLAMATION & ENSHRINEMENT ---
            self.translocation_map = TranslocationMap(moves=moves)

            if moves:
                Logger.success(
                    f"Oracle of Intent has perceived {len(moves)} true translocation(s). The plan is forged.")
            else:
                Logger.warn("Oracle of Intent has completed its Gaze. The translocation plan is a void.")

        except Exception as e:
            # The Unbreakable Ward: Any heresy from the Parser is caught and re-proclaimed.
            if isinstance(e, ArtisanHeresy):
                e.message = f"A paradox occurred while perceiving the translocation will: {e.message}"
                raise e

            # [[[ THE DIVINE HEALING: THE RITE OF SOUL PRESERVATION ]]]
            # The profane, soul-stripping transmutation is annihilated. We now forge
            # a new heresy vessel that carries the complete soul of the original paradox.
            raise ArtisanHeresy(
                f"A catastrophic paradox shattered the Oracle of Intent: {e}",
                child_heresy=e,
                traceback_obj=e.__traceback__
            )
            # [[[ THE APOTHEOSIS IS COMPLETE. THE TRUTH WILL NOW BE LUMINOUS. ]]]