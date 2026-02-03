# Path: scaffold/artisans/distill/core/semantics/intent.py
# --------------------------------------------------------

import re
from typing import Set, List
from .contracts import UserIntent, QueryIntent
from ...logger import Scribe

Logger = Scribe("IntentAnalyzer")


class IntentAnalyzer:
    """
    =============================================================================
    == THE DIVINER OF WILL (V-Ω-NLP-HEURISTIC-ENGINE)                          ==
    =============================================================================
    A pure, high-speed artisan that parses natural language into structured intent.
    It uses a declarative Grimoire of keywords to perform its Gaze.
    """

    KEYWORD_MAP = {
        QueryIntent.REFACTORING: ["fix", "bug", "error", "refactor", "optimize", "debug", "change", "update"],
        QueryIntent.GENERATION: ["add", "create", "implement", "new", "feature", "build", "make"],
        QueryIntent.TESTING: ["test", "verify", "assert", "mock", "spec"],
        QueryIntent.EXPLANATION: ["explain", "how", "what", "why", "describe", "document", "summarize"],
    }

    STOPWORDS = {"to", "the", "in", "for", "with", "a", "an", "is", "of", "and", "please", "can", "you", "me"}

    SYNONYMS = {
        "auth": "authentication login session user jwt oauth token permission",
        "db": "database sql model schema repository orm postgres mysql sqlite",
        "api": "route endpoint controller service rest graphql router handler",
        "ui": "component view page frontend react vue svelte css style",
        "deploy": "docker kubernetes terraform serverless ci cd pipeline",
    }

    def analyze(self, query: str) -> UserIntent:
        """Performs the Rite of Divination on the user's query."""
        if not query:
            return UserIntent(raw_query="", intent=QueryIntent.UNKNOWN)

        query_lower = query.lower()

        # 1. Divine the Intent
        detected_intent = self._divine_intent(query_lower)

        # 2. Extract Entities (Filenames, Symbols)
        entities = set(re.findall(r'\b[a-zA-Z0-9_]+\.[a-z]{2,4}\b', query))  # main.py
        entities.update(re.findall(r'\b[A-Z][a-zA-Z0-9]+\b', query))  # PascalCase
        entities.update(re.findall(r'\b[a-z]+_[a-z0-9_]+\b', query_lower))  # snake_case
        clean_entities = sorted([e for e in entities if e.lower() not in self.STOPWORDS and len(e) > 3])

        # 3. Extract Concepts
        words = set(re.findall(r'\w+', query_lower))
        concepts = sorted([w for w in words if w not in self.STOPWORDS and w not in clean_entities])

        # 4. Expand Query
        expanded_query = self._expand_query(query, concepts, clean_entities)

        Logger.verbose(f"Intent Divined: [cyan]{detected_intent.name}[/cyan] | Entities: {len(clean_entities)}")

        return UserIntent(
            raw_query=query,
            intent=detected_intent,
            entities=clean_entities,
            concepts=concepts,
            expanded_query=expanded_query
        )

    def _divine_intent(self, query_lower: str) -> QueryIntent:
        for intent, keywords in self.KEYWORD_MAP.items():
            if any(re.search(rf'\b{k}\b', query_lower) for k in keywords):
                return intent
        return QueryIntent.UNKNOWN

    def _expand_query(self, original_query: str, concepts: List[str], entities: List[str]) -> str:
        """Expands keywords into broader concepts using the SYNONYMS grimoire."""
        expanded_terms = set(concepts)
        for term in concepts:
            if term in self.SYNONYMS:
                expansion = self.SYNONYMS[term].split()
                expanded_terms.update(expansion)

        entity_boost = " ".join(entities)
        return f"{original_query} {entity_boost} {' '.join(sorted(list(expanded_terms)))}"

