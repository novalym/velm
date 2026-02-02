# scaffold/semantic_injection/__init__.py

"""
=================================================================================
== THE GATEWAY OF THE SEMANTIC CORTEX (V-Ω-PUBLIC-API)                         ==
=================================================================================
This is the one true entry point for the Semantic Injection system.
It exposes the `resolve_semantic_directive` function, which the Parser and
Creator artisans will call when they encounter the `@` sigil.
=================================================================================
"""
from .contract import SemanticHeresy
from .injector import SemanticInjector
from .loader import SemanticRegistry


def resolve_semantic_directive(directive_string: str, context: dict) -> str:
    """
    [THE PUBLIC RITE]
    Resolves a semantic directive string (e.g., "@git/python") into its content.

    Args:
        directive_string: The raw string starting with @.
        context: The dictionary of variables available in the current scope.

    Returns:
        The generated string content.

    Raises:
        SemanticHeresy: If resolution fails.
    """
    # Ensure the registry is awake
    if not SemanticRegistry._is_loaded:
        SemanticRegistry.awaken()

    return SemanticInjector.resolve(directive_string, context)


# Proclaim the Gnosis
__all__ = ["resolve_semantic_directive", "SemanticHeresy"]