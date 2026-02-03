# Path: scaffold/artisans/run/prophet/conductor.py
# ------------------------------------------------

"""
=================================================================================
== THE GNOSTIC TRIAGE CONDUCTOR (V-Ω-LEGENDARY-APOTHEOSIS)                     ==
=================================================================================
LIF: ∞ (ETERNAL & DIVINE)

This is the High Priest of the Prophet Pantheon. It is a pure Conductor that
orchestrates a multi-stage symphony of Gnostic perception. It summons a council
of divine specialists to perceive a plea's true soul and proclaim the one true
rite to be conducted. Its Gaze is absolute. Its judgment is truth.
=================================================================================
"""
from pathlib import Path
from typing import Optional

from .language_oracle import LanguageOracle
from .rite_adjudicator import RiteAdjudicator
from .sanctum_seer import SanctumSeer
from ....logger import Scribe


class GnosticIntentProphet:
    """The God-Engine of Intent, reborn as a pure Conductor."""

    def __init__(self, project_root: Path, logger: Scribe):
        self.project_root = project_root
        self.logger = logger

        # [FACULTY 1] The Modular Pantheon is forged at birth.
        self.language_oracle = LanguageOracle(logger)
        self.rite_adjudicator = RiteAdjudicator(logger)
        self.sanctum_seer = SanctumSeer(logger)
        self.logger.verbose("Prophet Pantheon (LanguageOracle, RiteAdjudicator, SanctumSeer) has been consecrated.")

    def divine_intent(self, path: Optional[Path], content: str = "") -> str:
        """
        [THE GRAND SYMPHONY OF DIVINATION]
        """
        self.logger.verbose(f"--- Gnostic Divination Symphony Begins for Target: '{path or '<ephemeral>'} ---")

        # --- MOVEMENT I: THE GAZE UPON THE EPHEMERAL & CELESTIAL ---
        if not path:
            self.logger.verbose("  -> Movement I: Perceived an ephemeral soul. Defaulting to 'sh' rite.")
            return "sh"

        path_str = str(path)
        if path_str.startswith(('http://', 'https://')):
            self.logger.verbose("  -> Movement I: Perceived a celestial soul (URL).")
            # The Language Oracle performs a Gaze upon the URL's extension.
            lang, _ = self.language_oracle.divine_from_path(path)
            return lang or "sh"

        target = path if path.is_absolute() else (self.project_root / path).resolve()

        # --- MOVEMENT II: THE GAZE UPON THE MORTAL REALM'S FORM ---
        if target.is_dir():
            self.logger.verbose(f"  -> Movement II: Perceived a sanctum '{target.name}'. Summoning the Sanctum Seer...")
            return self.sanctum_seer.divine(target)

        # --- MOVEMENT III: THE GAZE OF THE POLYGLOT ORACLE ---
        self.logger.verbose("  -> Movement III: Perceived a scripture. Summoning the Language Oracle...")
        language, reason = self.language_oracle.divine(target, content)
        self.logger.verbose(f"     -> Oracle's Gaze is complete. Language '{language}' perceived via {reason}.")

        # This is the final return; the adjudication between genesis/transmute happens next.
        return language

    def adjudicate_reality(self, rite_key: str) -> str:
        """
        [THE RITE OF FINAL ADJUDICATION]
        Delegates the final judgment to the specialist RiteAdjudicator.
        """
        self.logger.verbose(f"--- Final Adjudication Begins for Rite: '{rite_key}' ---")
        final_rite = self.rite_adjudicator.adjudicate(rite_key, self.project_root)
        self.logger.verbose(f"  -> Adjudicator's Gaze is complete. Final Rite proclaimed: '{final_rite}'.")
        return final_rite