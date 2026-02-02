# Path: scaffold/artisans/distill/core/ranker/factors/resonance.py

import re
from typing import List, Set
from .....core.cortex.contracts import FileGnosis


class ResonanceJudge:
    """
    =============================================================================
    == THE ORACLE OF HARMONIC RESONANCE                                        ==
    =============================================================================
    Performs a lexical gaze upon a scripture's soul, rewarding it for resonating
    with the key symbols of the Architect's immediate plea.
    """

    def __init__(self, key_symbols: Set[str]):
        # We pre-compile a single, powerful regex for hyper-performance.
        # This creates a pattern like \b(symbol_one|symbol_two|...)\b
        if key_symbols:
            self.pattern = re.compile(r'\b(' + '|'.join(re.escape(s) for s in key_symbols) + r')\b', re.IGNORECASE)
        else:
            self.pattern = None

    def judge(self, gnosis: FileGnosis, content: str) -> float:
        """
        The Rite of Resonance. Returns a score based on the density of key symbols.
        """
        if not self.pattern or not content:
            return 0.0

        # The Gaze is a single, hyper-performant `findall` rite.
        matches = self.pattern.findall(content)

        if not matches:
            return 0.0

        # The score is a function of match count, rewarding density.
        # A logarithmic scale prevents a single noisy file from dominating.
        score = 100 * (1 + len(matches))
        return score