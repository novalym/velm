# Path: scaffold/artisans/distillation/tag_extractor.py
# -----------------------------------------------------

import re
from typing import List, Set


class TagExtractor:
    """
    =================================================================================
    == THE SEMANTIC SOUL-READER (V-Ω-SOVEREIGN)                                    ==
    =================================================================================
    A sovereign artisan that performs a lexical Gaze upon a scripture's soul to
    perceive its core purpose, extracting high-value semantic tags.
    =================================================================================
    """
    # The Gnostic Grimoire of High-Value Semantics
    KEYWORDS: Set[str] = {
        'auth', 'user', 'login', 'session', 'jwt',
        'payment', 'stripe', 'billing', 'charge', 'invoice',
        'database', 'db', 'sql', 'query', 'model', 'schema',
        'api', 'rest', 'graphql', 'route', 'controller',
        'core', 'config', 'settings', 'env',
        'service', 'util', 'helper', 'client', 'worker',
        'test', 'spec', 'mock', 'assert'
    }

    # Pre-compile the regex for hyper-performance
    KEYWORD_REGEX = re.compile(r'\b(' + '|'.join(KEYWORDS) + r')\b', re.IGNORECASE)

    def extract(self, content: str) -> List[str]:
        """The one true rite of semantic extraction."""
        if not content:
            return []

        # The Gaze is a single, hyper-performant `findall` rite.
        # We use a set to automatically handle duplicates.
        found_tags = set(self.KEYWORD_REGEX.findall(content.lower()))

        return sorted(list(found_tags))


# --- A singleton instance for universal access ---
THE_TAG_EXTRACTOR = TagExtractor()


def extract_semantic_tags(content: str) -> List[str]:
    """The public gateway to the one true Oracle of Tags."""
    return THE_TAG_EXTRACTOR.extract(content)