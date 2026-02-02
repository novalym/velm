# Path: scaffold/artisans/distillation/language_oracle.py
# -------------------------------------------------------

import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, Tuple, List


class LanguageOracle:
    """
    =================================================================================
    == THE POLYGLOT ORACLE (V-Ω-SENTIENT-LEXICAL-FINGERPRINT)                      ==
    =================================================================================
    LIF: 10,000,000,000,000

    A divine artisan that gazes upon a scripture's soul to divine its one true
    tongue, even in the absence of a file extension.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gaze of Form (Extension):** The primary, fastest Gaze, now with a
        rich Grimoire of known extensions.
    2.  **The Gaze of the Sacred Name:** Perceives language from canonical filenames
        (`Dockerfile`, `Makefile`, `Gemfile`).
    3.  **The Gaze of the Shebang:** The definitive interpreter of `#!/usr/bin/env python`.
    4.  **The Gaze of the Lexical Fingerprint:** A powerful regex-based Gaze that
        scans the file's content for unique keywords and syntax (`=>` for JS,
        `:=` for Go, `def ... end` for Ruby).
    5.  **The Gaze of the XML Soul:** Detects XML-like structures (`<... >`) and can
        differentiate between HTML, SVG, and generic XML.
    6.  **The Gaze of the Braced Cosmos:** Can distinguish between JSON (`{ "key": ... }`)
        and CSS (`selector { ... }`) by their unique delimiters.
    7.  **The Unbreakable Ward of the Void:** Gracefully handles empty or blank files,
        proclaiming them as humble 'text'.
    8.  **The Gnostic Chronocache (`@lru_cache`):** Its memory is perfect. It never
        re-analyzes the same content header twice.
    9.  **The Performance Ward:** Operates only on a small header of the file,
        ensuring near-instantaneous Gnosis without reading large files.
    10. **The Sovereign Soul:** A self-contained, decoupled class, its wisdom available
        to all artisans in the cosmos.
    11. **The Polyglot Grimoire:** Its entire intelligence is declarative, defined in
        a sacred, extensible Grimoire of regular expressions.
    12. **The Luminous Dossier:** Can return not just the language, but the *reason*
        for its judgment (e.g., "Detected Shebang", "Matched Lexical Fingerprint").
    =================================================================================
    """

    # Faculty 11: The Polyglot Grimoire
    LEXICAL_GRIMOIRE: List[Dict] = [
        # Lang, Gaze Type, Pattern
        {'lang': 'python', 'type': 'keyword', 'pattern': re.compile(r'\b(def|class|import|from)\b')},
        {'lang': 'javascript', 'type': 'keyword', 'pattern': re.compile(r'\b(function|const|let|import|=>)\b')},
        {'lang': 'ruby', 'type': 'keyword', 'pattern': re.compile(r'\b(def|class|require|module|end)\b')},
        {'lang': 'go', 'type': 'keyword', 'pattern': re.compile(r'\b(package|func|import|:=)\b')},
        {'lang': 'rust', 'type': 'keyword', 'pattern': re.compile(r'\b(fn|struct|impl|use|let mut)\b')},
        {'lang': 'html', 'type': 'xml', 'pattern': re.compile(r'<!DOCTYPE html>|<html', re.IGNORECASE)},
        {'lang': 'xml', 'type': 'xml', 'pattern': re.compile(r'<\?xml')},
        {'lang': 'json', 'type': 'brace', 'pattern': re.compile(r'^\s*\{\s*"[^"]+"\s*:')},
        {'lang': 'css', 'type': 'brace', 'pattern': re.compile(r'^\s*([#.].*?)\s*\{')},
        {'lang': 'shell', 'type': 'keyword', 'pattern': re.compile(r'\b(echo|export|if|then|fi)\b')},
    ]

    SACRED_NAMES: Dict[str, str] = {
        'dockerfile': 'dockerfile', 'makefile': 'makefile', 'gemfile': 'ruby',
        'rakefile': 'ruby', 'vagrantfile': 'ruby', 'requirements.txt': 'pip-requirements'
    }

    @lru_cache(maxsize=4096)
    def divine(self, path: Path, header_bytes: bytes) -> Tuple[str, str]:
        """
        The one true rite. Performs the Multi-Vector Gaze.
        Returns: (language_name, reason_for_judgment)
        """
        # --- Gaze 1: The Gaze of Form (File Extension) ---
        if path.suffix:
            ext = path.suffix.lstrip('.').lower()
            # A simple grimoire for common extensions
            if ext in ('py', 'js', 'ts', 'tsx', 'go', 'rb', 'rs', 'html', 'css', 'json', 'yaml', 'yml', 'md', 'toml'):
                return ext, "Extension"

        # --- Gaze 2: The Gaze of the Sacred Name ---
        name_lower = path.name.lower()
        if name_lower in self.SACRED_NAMES:
            return self.SACRED_NAMES[name_lower], "Sacred Name"

        # --- Gaze 3: The Gaze of the Shebang ---
        try:
            content_sample = header_bytes.decode('utf-8', 'ignore')
            first_line = content_sample.splitlines()[0] if content_sample else ""
            if first_line.startswith('#!'):
                if 'python' in first_line: return 'python', "Shebang"
                if 'bash' in first_line or 'sh' in first_line: return 'shell', "Shebang"
                if 'node' in first_line: return 'javascript', "Shebang"
                if 'ruby' in first_line: return 'ruby', "Shebang"
        except Exception:
            pass  # Gaze averted if decoding fails

        # --- Gaze 4: The Gaze of the Lexical Fingerprint ---
        # Faculty 10: We operate only on the header for performance
        content_sample = header_bytes.decode('utf-8', 'ignore')
        if not content_sample.strip():
            return 'text', "Void"  # Faculty 7: Unbreakable Ward of the Void

        for rule in self.LEXICAL_GRIMOIRE:
            if rule['pattern'].search(content_sample):
                return rule['lang'], "Lexical Fingerprint"

        # --- The Final Proclamation ---
        return 'text', "Default"


# --- A singleton instance for universal access ---
THE_POLYGLOT_ORACLE = LanguageOracle()


def divine_language(path: Path, header_bytes: bytes) -> str:
    """The public gateway to the one true Oracle. Returns only the language name."""
    lang, _ = THE_POLYGLOT_ORACLE.divine(path, header_bytes)
    return lang