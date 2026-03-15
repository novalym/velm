# Path: src/velm/codex/__init__.py
# --------------------------------

from .contract import CodexHeresy
from .loader import CodexRegistry
from .injector import CodexInjector

# --- THE PUBLIC RITE ---
def resolve_codex_directive(directive_string: str, context: dict) -> str:
    """
    Resolves a directive string (e.g. "@Dockerfile") into content.
    """
    # Auto-Awaken
    if not CodexRegistry._is_loaded:
        CodexRegistry.awaken()

    return CodexInjector.resolve(directive_string, context)

# --- THE LEGACY SUTURE (HEALING OLD IMPORTS) ---
resolve_semantic_directive = resolve_codex_directive


__all__ = [
    "resolve_codex_directive",
    "CodexHeresy",
    "CodexRegistry",
    "CodexInjector",
    # Legacy Exports
    "resolve_semantic_directive",
]