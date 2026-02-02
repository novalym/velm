# Path: scaffold/artisans/simulacrum/heuristics/engine.py
from typing import Dict, Optional
import re
from .strategies import ALL_DNA


class SimulationOracle:
    """
    =============================================================================
    == THE ORACLE OF SYNTAX (V-Ω-MATHEMATICAL-ACCURACY)                        ==
    =============================================================================
    Calculates the probability distribution of a code snippet's language.
    """

    @classmethod
    def divine_language(cls, content: str, hint: str = None) -> str:
        """
        The Rite of Identification.
        Returns the language ID (e.g., 'python', 'typescript').
        """
        # 0. The Architect's Whisper (Explicit Hint Override)
        if hint and hint != "auto":
            return hint.lower()

        # 1. The Shebang Gaze (Absolute Truth)
        first_line = content.split('\n')[0].strip()
        if first_line.startswith("#!"):
            for dna in ALL_DNA:
                for bang in dna.shebangs:
                    if bang in first_line:
                        return dna.name

        # 2. The Statistical Inference (Bayesian Approximation)
        scores: Dict[str, int] = {dna.name: 0 for dna in ALL_DNA}

        # Normalize content for keyword search
        normalized = content  # Keep case for some langs, maybe lower for others?
        # Actually, keywords like 'True' in Python are case-sensitive. Keep raw.

        for dna in ALL_DNA:
            score = 0

            # A. Strong Keyword Resonance (Weight: 10)
            for kw in dna.strong_keywords:
                # Use word boundaries for accuracy
                if re.search(r'\b' + re.escape(kw), normalized):
                    score += 10

            # B. Weak Keyword Resonance (Weight: 2)
            for kw in dna.weak_keywords:
                if re.search(r'\b' + re.escape(kw), normalized):
                    score += 2

            # C. Structural Pattern Matching (Weight: 20)
            compiled = dna.compile_patterns()
            for pattern in compiled:
                if pattern.search(normalized):
                    score += 20

            scores[dna.name] = score

        # 3. The Collapse of Probability
        # Sort by score descending
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        winner, max_score = sorted_scores[0]

        # 4. Tie-Breaking & Fallbacks
        if max_score == 0:
            # If no resonance found, default to Python if it looks vaguely script-like,
            # otherwise Plain Text (which fails safe in most runners).
            # Defaulting to 'python' as per original request spec for "Safe Default"
            return "python"

        # [SPECIAL CASE]: TypeScript vs JavaScript ambiguity
        # If TS and JS are close, and TS > 0, prefer TS (superset).
        if winner == "javascript":
            ts_score = scores.get("typescript", 0)
            if ts_score > max_score * 0.5:  # If TS has significant evidence, upgrade it
                return "typescript"

        return winner