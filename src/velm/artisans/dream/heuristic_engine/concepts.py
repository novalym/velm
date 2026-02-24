# Path: artisans/dream/heuristic_engine/concepts.py
# -------------------------------------------------

"""
=============================================================================
== THE KNOWLEDGE GRAPH (V-Ω-SEMANTIC-WEB)                                ==
=============================================================================
LIF: ∞ | ROLE: QUERY_EXPANDER
A static ontology of software concepts. This allows the Heuristic Engine
to understand that "web app" might mean "react", "vue", or "html".
"""

from typing import Dict, List, Set


class ConceptGraph:
    """The Immutable Laws of Tech Relations."""

    # Maps broad intents to specific keywords used in Archetypes
    _INTENT_MAP: Dict[str, List[str]] = {
        "frontend": ["react", "vue", "svelte", "solid", "html", "css", "tailwind", "nextjs", "vite"],
        "backend": ["python", "go", "rust", "node", "express", "fastapi", "django", "gin", "actix"],
        "database": ["postgres", "mysql", "sqlite", "redis", "mongo", "prisma", "sqlalchemy"],
        "cli": ["python", "rust", "go", "click", "typer", "clap", "cobra"],
        "script": ["python", "bash", "shell", "script"],
        "api": ["rest", "graphql", "grpc", "fastapi", "express", "server"],
        "mobile": ["react-native", "flutter", "ios", "android"],
        "container": ["docker", "k8s", "kubernetes", "helm"],
        "infra": ["terraform", "tofu", "ansible", "cloudformation", "pulumi"],
        "web": ["react", "nextjs", "astro", "vue", "django", "fastapi"]
    }

    # Maps specific tech to implied tags (Bi-directional resonance)
    _IMPLICATION_MAP: Dict[str, List[str]] = {
        "nextjs": ["react", "typescript", "frontend", "web"],
        "fastapi": ["python", "api", "backend"],
        "flask": ["python", "web", "backend"],
        "actix": ["rust", "backend", "web"],
        "gin": ["go", "backend", "web"],
        "astro": ["web", "static", "frontend"],
        "tailwind": ["css", "styling", "frontend"],
        "prisma": ["db", "database", "typescript"],
        "sqlalchemy": ["db", "database", "python"]
    }

    @classmethod
    def expand_query(cls, tokens: List[str]) -> Set[str]:
        """
        [THE RITE OF EXPANSION]
        Transmutes a simple plea (e.g. "web") into a rich search vector
        (e.g. "web react nextjs astro...").
        """
        expanded = set(tokens)

        for token in tokens:
            # 1. Expand Intents (Broad -> Narrow)
            if token in cls._INTENT_MAP:
                expanded.update(cls._INTENT_MAP[token])

            # 2. Expand Implications (Specific -> Broad)
            if token in cls._IMPLICATION_MAP:
                expanded.update(cls._IMPLICATION_MAP[token])

        return expanded