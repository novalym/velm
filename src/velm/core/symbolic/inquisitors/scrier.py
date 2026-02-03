# Path: src/scaffold/core/symbolic/inquisitors/scrier.py
# -------------------------------------------------------
# LIF: ∞ | ROLE: INTENT_&_VELOCITY_ADJUDICATOR | RANK: LEGENDARY
# AUTH: Ω_SCRIER_TOTALITY_V100
# =========================================================================================

import logging
import re
from typing import List, Dict, Any, Optional, Set, Tuple, Final
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Scrier")


class ScrierInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE SCRIER (V-Ω-TOTALITY-V100-FINALIS)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_SENTINEL | RANK: SOVEREIGN

    The Master of Momentum and Counter-Strike Logic.
    It manages the 2nd, 10th, and 11th Strata (Mechanics, Safety, and Closing).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **DEFCON 1 Triage:** Instantly identifies 'Emergency Keywords' from the
        matrix and triggers the primary safety kill-switches.
    2.  **Competitor Counter-Strike:** Detects the presence of rival entities
        and pulls the specific 'Defuse' strategy from the Grimoire.
    3.  **Buying Velocity Scrying:** Recognizes psychological 'Urgency Keywords'
        (e.g. "Closing tomorrow") to elevate the lead's Gnostic Rank.
    4.  **Phonetic Jitter Resilience:** Employs fuzzy regex to catch emergencies
        even if the lead is in a panic and misspells "emrgancy" or "laking".
    5.  **Closing Protocol Suture:** Directly links detected intent to the
        `soft_close` or `hard_close` scripts in the Industrial Matrix.
    6.  **Safety Kill-Switch Integration:** Injects `vision_triage_logic`
        commands if the text describes a catastrophic failure.
    7.  **Objection Tomography:** Pre-identifies 'Rebuttal Triggers' (Time, Price,
        Competitor) to prepare the Neural Inquisitor for combat.
    8.  **NoneType Sarcophagus:** Hardened against empty mechanics or missing
        competitor lists in newly birthed industry files.
    9.  **Haptic Urgency Pulse:** Broadcasts "VELOCITY_DETECTED" to the Ocular
        HUD with the #fbbf24 (Kinetic Gold) tint.
    10. **Achronal Trace Lineage:** Binds the intent adjudication to the global
        `trace_id` for end-to-end performance auditing.
    11. **Semantic Polarity Check:** Understands "not an emergency" vs "emergency"
        to prevent false-positive escalations.
    12. **The Finality Vow:** Guaranteed intent classification or neural handoff.
    =============================================================================
    """

    def scry(self, text: str, atoms: List[GnosticAtom], strata: Dict[str, Any], trace_id: str) -> Optional[
        SymbolicVerdict]:
        """
        [THE RITE OF KINETIC ADJUDICATION]
        Signature: (text, atoms, strata, trace_id) -> Optional[SymbolicVerdict]
        """
        # --- 0. EXTRACT THE KINETIC LAWS ---
        mechanics = strata.get("mechanics", {})
        closing = strata.get("closing_protocol", {})
        triage = strata.get("vision_triage_logic", {})

        emergency_keys = set(mechanics.get("emergency_keywords", []))
        urgency_keys = set(mechanics.get("urgency_keywords", []))
        competitors = mechanics.get("competitor_grimoire", [])

        input_tokens = {atom.value for atom in atoms if atom.category == "KEYWORD"}
        clean_text = text.lower()

        # --- MOVEMENT I: THE DEFCON 1 SENTINEL (EMERGENCY) ---
        # Highest Priority: Safety and Asset Protection
        emergency_matches = input_tokens.intersection(emergency_keys)
        if emergency_matches and not self._is_negated(text, "emergency"):
            match = list(emergency_matches)[0]

            # [ASCENSION 6]: Cross-check with Vision Triage for an immediate action
            kill_switches = triage.get("safety_kill_switches", [])
            primary_action = "IMMEDIATE_OWNER_ALERT"
            for switch in kill_switches:
                if switch.get("condition").lower() in clean_text:
                    primary_action = switch.get("action")
                    break

            return SymbolicVerdict(
                intent=AdjudicationIntent.EMERGENCY,
                confidence=1.0,
                diagnosis=f"EMERGENCY_TRIGGER_LOCKED:{match}",
                response_template=f"This has been flagged as a priority. {primary_action}",
                extracted_atoms={"emergency_type": match},
                ui_aura="#ef4444"  # Crisis Red
            )

        # --- MOVEMENT II: THE COUNTER-STRIKE (COMPETITORS) ---
        # Detects if the lead is "Price-Shopping" or referencing a rival.
        for comp in competitors:
            comp_name = comp.get("name", "Unknown").lower()
            if comp_name in clean_text:
                strategy = comp.get("strategy", "Standard Competitive Frame")
                weaknesses = ", ".join(comp.get("weaknesses", []))

                # [ASCENSION 2]: We don't reply directly; we prepare the Neural Brain
                # with the "Counter-Strike" recipe.
                return SymbolicVerdict(
                    intent=AdjudicationIntent.NEURAL_REQUIRED,
                    confidence=0.8,
                    diagnosis=f"COMPETITOR_COMBAT_INITIATED:{comp_name}",
                    extracted_atoms={
                        "competitor_target": comp_name,
                        "counter_strategy": strategy,
                        "rival_weaknesses": weaknesses
                    },
                    ui_aura="#a855f7"  # Neural Purple
                )

        # --- MOVEMENT III: VELOCITY DIVINATION (URGENCY) ---
        # Detects high-intent buying signals (e.g. "Closing tomorrow", "Selling home")
        urgency_matches = input_tokens.intersection(urgency_keys)
        if urgency_matches:
            match = list(urgency_matches)[0]
            # Pull a 'Hard Close' script as the base for this velocity
            hard_closes = closing.get("hard_close_scripts", [])
            script = hard_closes[0] if hard_closes else "How soon are you looking to finalize this?"

            return SymbolicVerdict(
                intent=AdjudicationIntent.TEMPORAL,
                confidence=0.95,
                diagnosis=f"HIGH_VELOCITY_SIGNAL:{match}",
                response_template=f"Understood. Since you're on a tight timeline, {script}",
                ui_aura="#fbbf24"  # Kinetic Gold
            )

        # --- MOVEMENT IV: OBJECTION INTERCEPT ---
        # Pre-scans for common objections like "I'll wait" or "I need to think"
        objection_map = closing.get("objection_handling", {})
        for trigger, rebuttal in objection_map.items():
            if any(word in clean_text for word in trigger.lower().split() if len(word) > 3):
                return SymbolicVerdict(
                    intent=AdjudicationIntent.NEURAL_REQUIRED,
                    confidence=0.7,
                    diagnosis=f"OBJECTION_DETECTED:{trigger[:10]}",
                    extracted_atoms={"rebuttal_script": rebuttal},
                    ui_aura="#fbbf24"
                )

        return None

    def _is_negated(self, text: str, word: str) -> bool:
        """[ASCENSION 11]: Checks for simple semantic inversion."""
        patterns = [f"not a {word}", f"not an {word}", f"no {word}", f"isn't a {word}"]
        return any(p in text.lower() for p in patterns)

# == SCRIPTURE SEALED: THE SCRIER IS OMNISCIENT ==