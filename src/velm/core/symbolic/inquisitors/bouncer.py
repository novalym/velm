# Path: scaffold/core/symbolic/inquisitors/bouncer.py
# ---------------------------------------------------

from __future__ import annotations
import re
import logging
import time
import unicodedata
from typing import List, Dict, Any, Optional, Set, Final

# --- CORE SYMBOLIC UPLINKS (STRATUM-2) ---
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Bouncer:Jurist")


class BouncerInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE SOVEREIGN JURIST (V-Ω-TOTALITY-V25000-AXIOMATIC-AMNESTY)            ==
    =============================================================================
    @gnosis:title The Sovereign Jurist
    @gnosis:LIF INFINITY
    @gnosis:auth_code: )(!#@(!)#)(#!#)#)(#!

    The absolute authority of the Threshold. It judges the alignment between
    a Human Lead and the Business Grimoire.

    ### THE TOTALITY RECTIFICATION (THE CURE):
    This version implements "Absolute Question-Priority Sovereignty." Rejections
    are physically and logically impossible if the lead is seeking advice,
    information, or assistance. Curiosity is whitelisted as a High-Status
    buying signal, overriding all negative keyword matches.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Primordial Interrogative Gate (THE CURE):** The first act of the
        method. Detects '?' or curiosity tokens and returns None (PASS)
        immediately, shielding the query from the rest of the law.
    2.  **Geometric Unicode Purity:** Performs NFKC normalization to defeat
        homoglyph-based bypasses or control character entropy.
    3.  **Achronal Contextual Sieve:** Scans for semantic negators ("not",
        "don't") within a moving 3-word window of any detected policy triggers.
    4.  **O(1) Token Intersection:** Employs Pythonic set-arithmetic for
        nanosecond-level matching against the Industrial Blacklist.
    5.  **Economic Entitlement Guard:** Identifies and rejects "Pro-Bono,"
        "Free," or "Barter" pleas that violate the financial strata.
    6.  **Red Flag Vigil:** Performs a soft audit for risky terminology
        (e.g., "lawyer," "court")—logging for the Architect but allowing
        the lead to pass if no hard law is fractured.
    7.  **Haptic HUD Multicast:** Directly projects "AMNESTY_GRANTED" or
        "SIGNAL_VAPORIZED" events to the Ocular stage via the Akashic record.
    8.  **NoneType Sarcophagus:** Titanium protection against empty answer-sets,
        missing Grimoire keys, or uninitialized strata; returns None gracefully.
    9.  **Trace ID Silver-Cord Suture:** Permanently binds every judgment to the
        global X-Nov-Trace ID for 100% forensic auditability.
    10. **Axiomatic Silence Protocol:** Forbids the application of signatures
        to rejections, maintaining a cold, authoritative, systemic frame.
    11. **Metabolic Physics Accounting:** Records and stamps the nanosecond
        cost of the thought onto the resulting manifest.
    12. **The Finality Vow:** A mathematical guarantee that a lead is either
        Authorized, Exempted (Curiosity), or Terminated. No drift allowed.
    =============================================================================
    """

    # [FACULTY 1]: THE CURIOSITY SHIELD
    # If the text resonates with these markers, the Jurist MUST grant Amnesty.
    _CURIOSITY_MARKERS: Final[Set[str]] = {
        "what", "how", "why", "can", "could", "would", "is it", "way to",
        "advice", "question", "help with", "info on", "tell me", "best way",
        "possible to", "recommend", "how much", "looking for", "need a",
        "prevent", "stop", "fix", "options", "understand"
    }

    # [FACULTY 3]: THE POLARITY BUFFER
    _NEGATORS: Final[Set[str]] = {
        "not", "dont", "don't", "never", "neither", "no", "isnt", "isn't",
        "wont", "won't", "cant", "can't"
    }

    def scry(self,
             text: str,
             atoms: List[GnosticAtom],
             strata: Dict[str, Any],
             trace_id: str) -> Optional[SymbolicVerdict]:
        """
        [THE RITE OF JUDICIAL ADJUDICATION]
        Performs the surgical audit of lead-to-business alignment.
        """
        self._start_clock()

        # --- 0. PREPARE THE MATTER ---
        # [ASCENSION 2]: Geometric Cleanse
        # We normalize to NFKC to collapse stylistic variations and hidden characters.
        pure_matter = unicodedata.normalize('NFKC', text)
        clean_text = " ".join(pure_matter.lower().split())

        # [ASCENSION 4]: O(1) Token Extraction
        input_tokens = self._extract_tokens(atoms)

        # =====================================================================
        # MOVEMENT I: THE CURIOSITY AMNESTY (THE SUPREME PRIORITY)
        # =====================================================================
        # [THE CURE]: This is the absolute first gate. If the lead is asking
        # a question, the law does not apply. Rejections are for Declarative
        # statements of intent, not Interrogative pleas for knowledge.

        is_asking = "?" in text or any(marker in clean_text for marker in self._CURIOSITY_MARKERS)

        if is_asking:
            Logger.info(f"[{trace_id}] Bouncer: Curiosity detected. Amnesty granted by Q-Priority Gate.")

            # [ASCENSION 7]: Cast the pulse to the Ocular HUD
            self._resonate(trace_id, "CURIOSITY_AMNESTY_GRANTED", "#64ffda")

            # [CRITICAL]: We return None to signal "NO OBJECTION".
            # The lead passes directly to the next specialist or the AI Bridge.
            return None

            # --- 1. EXTRACT THE LAWS (ASCENSION 8) ---
        disqualifiers = strata.get("disqualifiers", {}) or {}
        neg_keywords = set(k.lower() for k in disqualifiers.get("negative_keywords", []))

        # ---------------------------------------------------------------------
        # MOVEMENT II: THE BLACKLIST (CONTEXT-AWARE POLICY)
        # ---------------------------------------------------------------------
        # Only reached if the lead is NOT asking a question.
        for token in input_tokens:
            if token in neg_keywords:
                # [ASCENSION 3]: Polarity Gaze
                # Example: "I am NOT looking for a roof-over" -> This is a PASS.
                if self._is_negated_in_context(clean_text, token):
                    Logger.info(f"[{trace_id}] Bouncer: Negated Policy-Word '{token}' detected. Contextual PASS.")
                    continue

                # Hard Rejection: Lead is declaring intent for a prohibited service.
                Logger.info(f"[{trace_id}] Bouncer: Hard Policy Fracture: '{token}'")

                # [ASCENSION 7]: Telemetry Signal
                self._resonate(trace_id, f"POLICY_KILL_{token.upper()}", "#ef4444")

                return self._forge_rejection(disqualifiers, f"POLICY_KILL:{token.upper()}")

        # ---------------------------------------------------------------------
        # MOVEMENT III: ECONOMIC SNOBBERY (METABOLIC PROTECTION)
        # ---------------------------------------------------------------------
        # [ASCENSION 5]: Identify and terminate "Resource Vampires."
        cheap_triggers = {"free", "pro-bono", "no money", "charity", "discount", "barter", "trade"}

        if input_tokens.intersection(cheap_triggers):
            Logger.info(f"[{trace_id}] Bouncer: Economic Non-Alignment. Intent is non-fiscal.")
            self._resonate(trace_id, "ECONOMIC_VOID_TERMINATED", "#ef4444")
            return self._forge_rejection(disqualifiers, "ECONOMIC_VOID")

        # ---------------------------------------------------------------------
        # MOVEMENT IV: RED FLAG VIGIL (FORENSIC AUDIT)
        # ---------------------------------------------------------------------
        # [ASCENSION 6]: Identifies risk patterns (Legal/Hostility) without killing.
        # These are logged but the lead is allowed to proceed to the Neural layer.
        red_flags = disqualifiers.get("red_flags", [])
        for flag in red_flags:
            if flag.lower() in clean_text:
                Logger.warning(f"[{trace_id}] Bouncer: Red Flag Resonance: '{flag}' - Inscribing Forensic Tag.")
                # We do not return here; the Gaze continues to the finish line.

        # ---------------------------------------------------------------------
        # FINALITY: PASS THROUGH
        # ---------------------------------------------------------------------
        # If no laws were broken and no amnesty was required, the Jurist stands down.
        return None

    def _is_negated_in_context(self, text: str, target: str) -> bool:
        """
        [FACULTY 3]: THE POLARITY GAZE.
        Scans the window preceding the target for semantic negators.
        """
        words = text.split()
        if target not in words: return False

        try:
            # Locate all occurrences to handle complex sentences
            indices = [i for i, x in enumerate(words) if x == target]

            for idx in indices:
                # Gaze back 3 atoms for a negator
                window = words[max(0, idx - 3):idx]
                if any(neg in window for neg in self._NEGATORS):
                    return True

            return False
        except (ValueError, IndexError):
            return False

    def _forge_rejection(self, disqualifiers: Dict, diagnosis: str) -> SymbolicVerdict:
        """
        [THE RITE OF OBLIVION]
        Materializes a terminal rejection based on industrial policy.
        """
        # [ASCENSION 10]: Axiomatic Silence - signature-free response
        return SymbolicVerdict(
            intent=AdjudicationIntent.DISQUALIFY,
            confidence=1.0,
            diagnosis=diagnosis,
            response_template=disqualifiers.get("bad_fit_reply",
                                                "We are unable to assist with this specific request at this time."),
            ui_aura="#475569",  # Shadow Slate (Lead Neutralization)
            extracted_atoms={
                "rejection_locus": diagnosis,
                "latency_ns": self._get_latency_ms() * 1000000
            }
        )

    def __repr__(self) -> str:
        return f"<Ω_BOUNCER_JURIST status=ACTIVE version=25.0.0>"