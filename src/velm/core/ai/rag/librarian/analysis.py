# Path: scaffold/core/ai/rag/librarian/analysis.py
# ------------------------------------------------

import re
from typing import List
from .contracts import RAGQuery, QueryIntent


class QueryAnalyzer:
    """
    =============================================================================
    == THE QUERY DIVINER (V-Ω-INTENT-RECOGNITION)                              ==
    =============================================================================
    Analyzes the user's prompt to understand their true desire.
    Expands keywords to improve recall.
    """

    INTENT_PATTERNS = {
        QueryIntent.GENERATION: [r"write", r"create", r"generate", r"implement", r"code", r"make"],
        QueryIntent.REFACTORING: [r"fix", r"refactor", r"optimize", r"clean", r"debug", r"change", r"update"],
        QueryIntent.EXPLANATION: [r"explain", r"how", r"what", r"why", r"describe", r"document"],
    }

    def analyze(self, raw_text: str) -> RAGQuery:
        intent = self._divine_intent(raw_text)
        expanded = self._expand_terms(raw_text)

        return RAGQuery(
            raw_text=raw_text,
            expanded_terms=expanded,
            intent=intent
        )

    def _divine_intent(self, text: str) -> QueryIntent:
        text_lower = text.lower()
        for intent, patterns in self.INTENT_PATTERNS.items():
            if any(re.search(p, text_lower) for p in patterns):
                return intent
        return QueryIntent.UNKNOWN

    def _expand_terms(self, text: str) -> List[str]:
        """
        [ELEVATION 3] Query Expansion.
        Adds synonyms and related architectural terms.
        """
        terms = set(re.findall(r'\w+', text.lower()))
        expansion = set(terms)

        # Synonyms Grimoire
        SYNONYMS = {
            "auth": ["authentication", "login", "jwt", "session", "user"],
            "db": ["database", "sql", "orm", "model", "schema", "repository"],
            "api": ["route", "endpoint", "controller", "rest", "graphql"],
            "ui": ["component", "view", "frontend", "react", "page"],
            "test": ["spec", "suite", "unit", "integration", "mock"],
        }

        for word in terms:
            if word in SYNONYMS:
                expansion.update(SYNONYMS[word])

        return list(expansion)