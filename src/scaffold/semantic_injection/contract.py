# scaffold/semantic_injection/contract.py

"""
=================================================================================
== THE CONTRACT OF SEMANTIC WILL (V-Ω-BASE)                                    ==
=================================================================================
LIF: 10,000,000,000

This scripture defines the `SemanticDirective`, the atomic unit of the Semantic
Cortex. Every directive (e.g., `@git/python`, `@crypto.uuid`) must implement
this contract to be perceived by the God-Engine.
=================================================================================
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DirectiveSignature:
    """
    The Gnostic signature of a directive.
    Example: @git/python(force=true)
    """
    namespace: str  # e.g., 'git', 'crypto'
    name: str  # e.g., 'python', 'random'
    args: List[Any]  # Positional arguments
    kwargs: Dict[str, Any]  # Keyword arguments


class BaseDirectiveDomain(ABC):
    """
    A Domain is a collection of related directives (e.g., The 'Git' Domain).
    It serves as a namespace container to organize the Gnosis.
    """

    @property
    @abstractmethod
    def namespace(self) -> str:
        """The prefix for this domain (e.g., 'git', 'crypto')."""
        pass

    @abstractmethod
    def help(self) -> str:
        """Proclaims the purpose of this domain to the Architect."""
        pass

    def execute(self, directive_name: str, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        The Router of Will. It dispatches the execution to the specific
        method within the domain matching `directive_name`.
        """
        # Gnostic Routing: Look for a method named `_directive_{name}`
        handler_name = f"_directive_{directive_name}"

        if not hasattr(self, handler_name):
            raise NotImplementedError(
                f"The domain '{self.namespace}' does not know the rite of '{directive_name}'."
            )

        handler = getattr(self, handler_name)
        return handler(context, *args, **kwargs)


# =================================================================================
# == THE EXCEPTION OF SEMANTIC HERESY                                            ==
# =================================================================================
class SemanticHeresy(Exception):
    """Raised when a micro-directive fails or is malformed."""
    pass