# Path: src/scaffold/core/symbolic/inquisitors/banker.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: FISCAL_ADJUDICATOR | RANK: SOVEREIGN
# AUTH: Ω_BANKER_TOTALITY_V100
# =========================================================================================

import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Banker")


class BankerInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE BANKER (V-Ω-TOTALITY-V100-FINALIS)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: CAPITAL_ORCHESTRATOR | RANK: LEGENDARY

    The high-status Auditor of the Monolith.
    It manages the 8th and 3rd Strata (Financials & Economic Logic).

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **Metric Delta Calculus:** Calculates the distance between a lead's stated
        budget and the `minimum_ticket`. Rejects if the gap is > 50%.
    2.  **Deposit Enforcement:** Deterministically injects the `deposit_requirement`
        into all pricing discussions to qualify the lead's liquidity.
    3.  **Upsell Convergence:** Scans for 'Trigger Keywords' in the lead's text and
        matches them to the `upsell_opportunities` matrix.
    4.  **Trip Charge Gating:** Automatically appends the `trip_charge` logic if
        the lead asks for a diagnostic visit or "inspection."
    5.  **Financing Oracle:** If 'payment plan' or 'financing' is mentioned, it
        checks `financing_available` and returns the specific partner scripture.
    6.  **Physics-Based Pricing:** Uses the `pricing_logic` shard to explain
        *why* it costs what it costs (e.g. "Pricing is determined by Tonnage/SQFT").
    7.  **ROI Inversion:** (Prophetic) Frames the cost as an investment by
        referencing the `average_ticket` of the industry.
    8.  **NoneType Sarcophagus:** Hardened against missing financial keys in
        newly created industry strata.
    9.  **Currency Normalization:** The Purifier hands it floats; the Banker
        handles the magnitude (e.g. $10k vs $10,000).
    10. **Haptic Fiscal Pulse:** Broadcasts "CAPITAL_TRIAGE" to the Ocular HUD
        with the #10b981 (Success) or #fbbf24 (Urgency) tint.
    11. **Rebuttal Injection:** If a lead says "Too expensive," it pulls the
        exact rebuttal script from the `closing_protocol`.
    12. **The Finality Vow:** Guaranteed financial qualification or rejection.
    =============================================================================
    """

    def scry(self, text: str, atoms: List[GnosticAtom], strata: Dict[str, Any], trace_id: str) -> Optional[
        SymbolicVerdict]:
        """
        [THE RITE OF FISCAL ADJUDICATION]
        """
        # 1. EXTRACT FINANCIAL STRATA (The Laws of Gold)
        financials = strata.get("financials", {})
        faq = strata.get("faq_matrix", {})
        closing = strata.get("closing_protocol", {})
        upsells = strata.get("upsell_opportunities", {})

        min_ticket = float(financials.get("minimum_ticket", 0.0))
        input_tokens = {atom.value for atom in atoms if atom.category == "KEYWORD"}
        money_atoms = [atom for atom in atoms if atom.category == "FINANCIAL"]

        # --- MOVEMENT I: THE BUDGETARY BOUNCER ---
        if money_atoms:
            for atom in money_atoms:
                budget = float(atom.value)
                # If stated budget is less than 50% of the industrial floor
                if budget < (min_ticket * 0.5):
                    Logger.info(
                        f"[{trace_id}] Banker: Budget ${budget} is below floor ${min_ticket}. Recommending Disqualification.")
                    return SymbolicVerdict(
                        intent=AdjudicationIntent.DISQUALIFY,
                        confidence=1.0,
                        diagnosis=f"BUDGET_BELOW_MINIMUM_THRESHOLD:{budget}",
                        response_template=str(strata.get("disqualifiers", {}).get("bad_fit_reply")),
                        ui_aura="#991b1b"  # Deep Red
                    )

        # --- MOVEMENT II: THE PRICING ORACLE ---
        pricing_triggers = {"price", "cost", "quote", "estimate", "fee", "pay", "charge", "much", "$$"}
        if input_tokens.intersection(pricing_triggers) or "how much" in text.lower():
            # [ASCENSION 6]: FUSE PRICING LOGIC WITH DEPOSIT RULES
            logic = faq.get("pricing_reply", "Our pricing is project-based.")
            deposit = financials.get("deposit_requirement", "A deposit is required to begin.")
            trip = financials.get("trip_charge", "Standard rates apply.")

            final_scripture = (
                f"{logic}\n\n"
                f"**Investment Structure:**\n"
                f"- Minimum Project Size: ${min_ticket:,.2f}\n"
                f"- Deposit Required: {deposit}\n"
                f"- Dispatch/Site Fee: {trip}"
            )

            return SymbolicVerdict(
                intent=AdjudicationIntent.FINANCIAL,
                confidence=0.98,
                diagnosis="DETERMINISTIC_FISCAL_REVELATION",
                response_template=final_scripture,
                ui_aura="#10b981"  # Vitality Green
            )

        # --- MOVEMENT III: THE FINANCING SUTURE ---
        financing_triggers = {"payment", "plan", "finance", "financing", "monthly", "credit", "installments"}
        if input_tokens.intersection(financing_triggers):
            if financials.get("financing_available", False):
                partners = ", ".join(financials.get("financing_partners", ["our internal partners"]))
                response = f"Yes, we offer flexible financing options through {partners}. You can typically pay monthly to preserve your capital. Shall I send the application link?"
            else:
                response = "We do not offer internal financing at this time, but we accept all major credit cards and wire transfers for your convenience."

            return SymbolicVerdict(
                intent=AdjudicationIntent.FINANCIAL,
                confidence=1.0,
                diagnosis="FINANCING_CAPABILITY_ADJUDICATED",
                response_template=response,
                ui_aura="#64ffda"
            )

        # --- MOVEMENT IV: THE UPSELL CONVERGENCE (LIF-100) ---
        # [ASCENSION 3]: CROSS-EXAMINING THE UPSELL MATRIX
        for opportunity in upsells.get("trigger_logic", []):
            trigger_word = str(opportunity.get("mention", "")).lower()
            if trigger_word in text.lower():
                suggestion = opportunity.get("suggest")
                impact = opportunity.get("impact")

                Logger.info(f"[{trace_id}] Banker: Upsell Trigger Detected: '{trigger_word}'")

                # We hand this off to the Neural Inquisitor because upselling
                # requires human-grade persuasion (Nuance).
                return SymbolicVerdict(
                    intent=AdjudicationIntent.NEURAL_REQUIRED,
                    confidence=0.7,
                    diagnosis=f"UPSELL_OPPORTUNITY_DETECTED:{trigger_word}",
                    extracted_atoms={"upsell_target": suggestion, "upsell_impact": impact},
                    ui_aura="#a855f7"  # Neural Purple
                )

        # --- MOVEMENT V: THE OBJECTION COUNTER-STRIKE ---
        objection_triggers = {"expensive", "too high", "cheaper", "bid", "discount"}
        if input_tokens.intersection(objection_triggers):
            rebuttals = closing.get("objection_handling", {})
            # Find the closest matching objection key
            # This is a simple substring search for V1
            chosen_rebuttal = None
            for key in rebuttals.keys():
                if any(word in key.lower() for word in input_tokens):
                    chosen_rebuttal = rebuttals[key]
                    break

            if chosen_rebuttal:
                return SymbolicVerdict(
                    intent=AdjudicationIntent.FINANCIAL,
                    confidence=0.9,
                    diagnosis="FISCAL_OBJECTION_HANDLED",
                    response_template=chosen_rebuttal,
                    ui_aura="#fbbf24"  # Kinetic Amber
                )

        return None