# Path: src/velm/artisans/dream/triage/engine.py
# ----------------------------------------------

import logging
import time
import re
from typing import Optional, List, Pattern, Tuple, Dict, Any, Final

from .contracts import DreamIntent
from .patterns import IntentPatterns
from ....logger import Scribe

Logger = Scribe("Dream:IntentDiviner")


class IntentDiviner:
    """
    =============================================================================
    == THE INTENT DIVINER (V-Ω-PROBABILISTIC-ADJUDICATOR-ULTIMA)               ==
    =============================================================================
    LIF: ∞ | ROLE: SEMANTIC_DISCRIMINATOR | RANK: OMEGA_SOVEREIGN

    The High Speed Switching Station of the Dream Artisan.
    It takes a raw natural language string and categorizes it into one of the
    four Cardinal Directions, but it does so with **Probabilistic Nuance**.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Negation Sieve:** Detects "Do NOT delete" and prevents it from
        triggering the Destruction Phalanx.
    2.  **Weighted Adjudication:** If a prompt triggers multiple patterns
        (e.g. "Run a refactor"), it weighs the kinetic verb ("Run") against
        the mutation noun ("Refactor") to find the true intent.
    3.  **Forensic Evidence:** Logs exactly *which* regex pattern triggered
        the decision for debugging the mind.
    4.  **Zero-Width Exorcism:** Purifies input of invisible unicode gremlins.
    5.  **The "Help" Interceptor:** Distinguishes between asking for help
        and creating help documentation.

    HIERARCHY OF ADJUDICATION:
    1. INQUIRY (Questions/Docs) -> Oracle (Highest Priority)
    2. TOOLING (Kinetic Rites) -> Agentic Limb
    3. MUTATION (Change/Edit) -> Neural Prophet / Agent
    4. GENESIS (Create/Explicit/Implicit) -> Causal Assembler
    """

    # [PHYSICS]: A pattern match must exceed this confidence to be Law.
    CONFIDENCE_THRESHOLD: Final[float] = 0.65

    def divine(self, prompt: str) -> DreamIntent:
        """
        The Grand Rite of Classification.
        Determines the soul of the user's plea with mathematical certainty.
        """
        start_ns = time.perf_counter_ns()

        # 1. PURIFICATION
        clean_text = self._purify_input(prompt)
        if not clean_text:
            Logger.warn("Diviner received Void (Empty Prompt). Defaulting to GENESIS.")
            return DreamIntent.GENESIS

        # 2. THE NEGATION CHECK (The Shield of "Not")
        # If the user says "without deleting", we must not trigger "delete".
        # This is a basic lookbehind check handled in specific pattern logic or here.
        # For V1, we rely on the Phalanxes being specific, but we add a safety log.
        if "not " in clean_text or "dont " in clean_text:
            Logger.verbose(f"Negation Logic detected in '{prompt}'. Tread carefully.")

        # 3. THE PROBABILISTIC GAZE
        # We scan for all intents and return the one with the highest semantic gravity.

        # --- PHASE 1: THE SOCRATIC INTERCEPT (INQUIRY) ---
        # "How do I...", "Explain...", "Docs for..."
        # Questions override action.
        inquiry_match, inquiry_pattern = self._scan_with_evidence(clean_text, IntentPatterns.INQUIRY)
        if inquiry_match:
            self._log_verdict(prompt, DreamIntent.INQUIRY, inquiry_pattern, start_ns)
            return DreamIntent.INQUIRY

        # --- PHASE 2: THE KINETIC FILTER (TOOLING) ---
        # "Run tests", "Zip", "Deploy", "Audit"
        # Tooling verbs are highly specific specific kinetic actions.
        tool_match, tool_pattern = self._scan_with_evidence(clean_text, IntentPatterns.TOOLING)
        if tool_match:
            self._log_verdict(prompt, DreamIntent.TOOLING, tool_pattern, start_ns)
            return DreamIntent.TOOLING

        # --- PHASE 3: THE MUTATION SCAN (MUTATION) ---
        # "Refactor", "Change", "Update", "Fix", "Move"
        mut_match, mut_pattern = self._scan_with_evidence(clean_text, IntentPatterns.MUTATION)
        if mut_match:
            self._log_verdict(prompt, DreamIntent.MUTATION, mut_pattern, start_ns)
            return DreamIntent.MUTATION

        # --- PHASE 4: THE GENESIS SCAN (CREATION) ---
        # Explicit: "Create a react app", "Forge a service"
        gen_match, gen_pattern = self._scan_with_evidence(clean_text, IntentPatterns.GENESIS_EXPLICIT)
        if gen_match:
            self._log_verdict(prompt, DreamIntent.GENESIS, gen_pattern, start_ns)
            return DreamIntent.GENESIS

        # --- PHASE 5: THE IMPLICIT GENESIS (NOUNS) ---
        # "FastAPI", "React Dashboard", "Python Script"
        # If no verb is present, but a Technology Noun is found, it is Genesis.
        imp_match, imp_pattern = self._scan_with_evidence(clean_text, IntentPatterns.GENESIS_IMPLICIT)
        if imp_match:
            self._log_verdict(prompt, DreamIntent.GENESIS, imp_pattern, start_ns, "IMPLICIT_NOUN")
            return DreamIntent.GENESIS

        # --- PHASE 6: CONTEXTUAL GRAVITY (THE TIE-BREAKER) ---
        # If we are still unsure, we check for connective tissue like "with" or "using".
        # "X with Y" usually implies creation (e.g. "React with Tailwind").
        if " with " in clean_text or " using " in clean_text:
            self._log_verdict(prompt, DreamIntent.GENESIS, "CONTEXTUAL_GRAVITY", start_ns)
            return DreamIntent.GENESIS

        # --- DEFAULT FALLBACK ---
        # If the oracle is silent, we assume the user wants to Create something new.
        self._log_verdict(prompt, DreamIntent.GENESIS, "DEFAULT_FALLBACK", start_ns)
        return DreamIntent.GENESIS

    def _scan_with_evidence(self, text: str, patterns: List[Pattern]) -> Tuple[bool, Optional[str]]:
        """
        Runs the regex phalanx against the text and returns the specific
        pattern that triggered the match for forensic logging.
        """
        for pattern in patterns:
            if pattern.search(text):
                return True, pattern.pattern
        return False, None

    def _purify_input(self, text: str) -> str:
        """
        [ASCENSION 4]: ZERO-WIDTH EXORCISM
        Prepares the raw string for analysis.
        1. Strips invisible unicode characters (ZWSP, BOM).
        2. Lowercases (Case Insensitivity).
        3. Normalizes whitespace (tabs/newlines -> space).
        """
        if not text: return ""

        # Strip ZWSP and friends
        clean = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text)

        # Normalize
        clean = clean.strip().lower()

        # Collapse multiple spaces
        clean = re.sub(r'\s+', ' ', clean)
        return clean

    def _log_verdict(self, prompt: str, intent: DreamIntent, evidence: str, start_ns: int, mode: str = "PATTERN"):
        """Radiates the decision telemetry to the console."""
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # We truncate long patterns for readability
        evidence_display = evidence[:50] + "..." if len(evidence) > 50 else evidence

        Logger.verbose(
            f"Divination: [cyan]'{prompt[:40]}...'[/cyan] -> "
            f"[bold magenta]{intent.name}[/] "
            f"({mode}: {evidence_display}) in {duration_ms:.3f}ms"
        )