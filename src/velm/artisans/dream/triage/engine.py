# artisans/dream/triage/engine.py
# -------------------------------

import logging
import time
import re
from typing import Optional, List, Pattern, Tuple

from .contracts import DreamIntent
from .patterns import IntentPatterns
from ....logger import Scribe

Logger = Scribe("Dream:IntentDiviner")


class IntentDiviner:
    """
    =============================================================================
    == THE INTENT DIVINER (V-Ω-HIERARCHICAL-SCANNER-ULTIMA)                    ==
    =============================================================================
    LIF: ∞ | ROLE: SEMANTIC_DISCRIMINATOR | RANK: OMEGA_SOVEREIGN

    The High Speed Switching Station. It takes a raw natural language string and
    categorizes it into one of the four Cardinal Directions of the Dream Artisan.

    HIERARCHY OF ADJUDICATION:
    1. INQUIRY (Questions bypass action) -> Oracle
    2. TOOLING (Specific utility verbs) -> Agentic Limb
    3. MUTATION (Change verbs) -> Agentic Limb / Neural Prophet
    4. GENESIS (Creation verbs OR Implicit Noun Phrases) -> Heuristic / Prophet
    """

    def divine(self, prompt: str) -> DreamIntent:
        """
        The Rite of Classification.
        Determines the soul of the user's plea.
        """
        start_ns = time.perf_counter_ns()
        clean_text = self._purify_input(prompt)

        intent = DreamIntent.GENESIS  # Default Fallback
        match_type = "DEFAULT_FALLBACK"

        # --- PHASE 1: THE SOCRATIC INTERCEPT (INQUIRY) ---
        # "How do I...", "Explain this...", "What is..."
        if self._scan(clean_text, IntentPatterns.INQUIRY):
            intent = DreamIntent.INQUIRY
            match_type = "INQUIRY_PATTERN"

        # --- PHASE 2: THE KINETIC FILTER (TOOLING) ---
        # "Run tests", "Zip this", "Deploy to AWS"
        # Tooling verbs are highly specific and override creation/mutation.
        elif self._scan(clean_text, IntentPatterns.TOOLING):
            intent = DreamIntent.TOOLING
            match_type = "TOOLING_VERB"

        # --- PHASE 3: THE MUTATION SCAN (MUTATION) ---
        # "Refactor this", "Rename X to Y", "Fix the bug"
        elif self._scan(clean_text, IntentPatterns.MUTATION):
            intent = DreamIntent.MUTATION
            match_type = "MUTATION_VERB"

        # --- PHASE 4: THE GENESIS SCAN (CREATION) ---
        # Explicit: "Create a react app"
        elif self._scan(clean_text, IntentPatterns.GENESIS_EXPLICIT):
            intent = DreamIntent.GENESIS
            match_type = "GENESIS_EXPLICIT"

        # --- PHASE 5: THE IMPLICIT GENESIS (NOUNS) ---
        # "FastAPI", "React Dashboard", "Python Script"
        # If no verb is present, but a Technology Noun is found, it is Genesis.
        elif self._scan(clean_text, IntentPatterns.GENESIS_IMPLICIT):
            intent = DreamIntent.GENESIS
            match_type = "GENESIS_IMPLICIT_NOUN"

        # --- PHASE 6: CONTEXTUAL GRAVITY (THE TIE-BREAKER) ---
        # If we are still unsure (or defaulted), we check the "With" clause.
        # "X with Y" usually implies creation (e.g. "React with Tailwind").
        elif " with " in clean_text or " using " in clean_text:
            intent = DreamIntent.GENESIS
            match_type = "CONTEXTUAL_GRAVITY"

        # --- TELEMETRY & RETURN ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.verbose(f"Divination: [cyan]'{prompt[:30]}...'[/cyan] -> [bold magenta]{intent.name}[/] "
                       f"({match_type}) in {duration_ms:.3f}ms")

        return intent

    def _scan(self, text: str, patterns: List[Pattern]) -> bool:
        """Runs the regex phalanx against the text."""
        for pattern in patterns:
            if pattern.search(text):
                # [DIAGNOSTIC]: Log the exact pattern that matched for debugging
                # Logger.debug(f"Matched Pattern: {pattern.pattern}")
                return True
        return False

    def _purify_input(self, text: str) -> str:
        """
        Prepares the raw string for analysis.
        1. Strips whitespace.
        2. Lowercases (Case Insensitivity).
        3. Normalizes whitespace (tabs/newlines -> space).
        """
        if not text: return ""
        cleaned = text.strip().lower()
        # Collapse multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned