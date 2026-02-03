from pathlib import Path
from typing import Dict, Any, Optional

from .textual import TextualMutator
from .regex import RegexMutator
from .structured import StructuredMutator
from .semantic.router import SemanticRouter
from ....contracts.heresy_contracts import ArtisanHeresy


class GnosticMutator:
    """
    =================================================================================
    == THE GNOSTIC MUTATOR (V-Ω-UNIFIED-FACADE)                                    ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Public Face of the Mutation System.
    It routes requests to the specialist artisans residing in the sub-sanctums.
    """

    @staticmethod
    def apply_text_append(original: str, fragment: str) -> str:
        """Delegates to the Textual Alchemist."""
        return TextualMutator.append(original, fragment)

    @staticmethod
    def apply_text_prepend(original: str, fragment: str) -> str:
        """Delegates to the Textual Alchemist (Shebang Aware)."""
        return TextualMutator.prepend(original, fragment)

    @staticmethod
    def apply_regex_subtract(original: str, pattern: str) -> str:
        """Delegates to the Regex Surgeon."""
        return RegexMutator.subtract(original, pattern)

    @staticmethod
    def apply_regex_transfigure(original: str, command: str, replacement_block: str = None) -> str:
        """Delegates to the Regex Surgeon."""
        return RegexMutator.transfigure(original, command, replacement_block)

    @staticmethod
    def apply_structural_merge(original: str, fragment: str, ext: str) -> str:
        """Delegates to the Structured Architect."""
        return StructuredMutator.merge(original, fragment, ext)

    @staticmethod
    def apply_semantic_insert(original: str, fragment: str, selector: Dict[str, str], file_path: Path) -> str:
        """
        Delegates to the Semantic Router.
        This is the gateway to AST-based surgery.
        """
        return SemanticRouter.dispatch(original, fragment, selector, file_path)

    # --- Internal Helpers exposed for legacy reasons if any ---
    @staticmethod
    def _deep_merge(base: Any, update: Any) -> Any:
        return StructuredMutator._deep_merge(base, update)
