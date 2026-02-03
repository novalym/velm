# Path: scaffold/artisans/run/prophet/language_oracle.py
# ------------------------------------------------------

"""
=================================================================================
== THE POLYGLOT LANGUAGE ORACLE (V-Ω-BAYESIAN-FINGERPRINTER)                   ==
=================================================================================
A divine artisan that performs a multi-stage, scored Gaze to prophesy a
scripture's one true tongue with near-mathematical certainty.
=================================================================================
"""
import re
from pathlib import Path
from typing import Optional, Tuple

from .grimoire import LANGUAGE_FINGERPRINTS, SACRED_NAME_MAP, EXTENSION_MAP
from ....logger import Scribe


class LanguageOracle:
    """Performs the Gaze of the Polyglot."""

    def __init__(self, logger: Scribe):
        self.logger = logger

    def divine(self, path: Path, content: str) -> Tuple[str, str]:
        """
        The multi-stage Gaze, from fastest to deepest.
        Returns (language, reason).
        """
        # Gaze 1: Extension (Highest Confidence)
        lang, reason = self.divine_from_path(path)
        if lang: return lang, reason

        # Gaze 2: Shebang (High Confidence)
        lang = self._gaze_upon_shebang(content)
        if lang: return lang, "Shebang"

        # Gaze 3: Content Fingerprint (The Bayesian Gaze)
        lang = self._gaze_upon_content(content)
        if lang: return lang, "Content Fingerprint"

        return "unknown_rite", "Gaze Averted"

    def divine_from_path(self, path: Path) -> Tuple[Optional[str], Optional[str]]:
        """Perceives language from filename and extension alone."""
        # Gaze 1a: Full compound suffix (e.g., .patch.scaffold)
        full_suffix = "".join(path.suffixes)
        if full_suffix in EXTENSION_MAP:
            return EXTENSION_MAP[full_suffix], f"Compound Suffix ('{full_suffix}')"

        # Gaze 1b: Simple suffix
        if path.suffix in EXTENSION_MAP:
            return EXTENSION_MAP[path.suffix], f"Suffix ('{path.suffix}')"

        # Gaze 1c: Sacred Name
        if path.name in SACRED_NAME_MAP:
            return SACRED_NAME_MAP[path.name], f"Sacred Name ('{path.name}')"

        if path.name.startswith('docker-compose'):
            return 'docker_compose', "Sacred Name ('docker-compose...')"

        return None, None

    def _gaze_upon_shebang(self, content: str) -> Optional[str]:
        """Reads the first line for #! interpreter declarations."""
        if not content: return None
        first_line = content.splitlines()[0]
        if first_line.startswith("#!"):
            if "python" in first_line: return "python"
            if "node" in first_line: return "node"
            if "bash" in first_line or "sh" in first_line: return "sh"
            # ... add more as needed
        return None

    def _gaze_upon_content(self, content: str) -> Optional[str]:
        """[FACULTY 7] The Bayesian Fingerprinter."""
        if not content: return None

        scores: Dict[str, float] = {}
        # We only scan the first 4KB for performance.
        content_sample = content[:4096]

        for lang, fingerprints in LANGUAGE_FINGERPRINTS.items():
            lang_score = 0.0
            for pattern, weight in fingerprints.items():
                if re.search(pattern, content_sample, re.MULTILINE):
                    lang_score += weight
            if lang_score > 0:
                scores[lang] = lang_score

        if not scores: return None

        best_lang = max(scores, key=scores.get)
        self.logger.verbose(f"    -> Fingerprint Gaze Scores: {scores}")
        return best_lang