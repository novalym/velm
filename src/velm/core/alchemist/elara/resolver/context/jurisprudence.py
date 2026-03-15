# Path: core/alchemist/elara/resolver/context/jurisprudence.py
# ------------------------------------------------------------

from typing import Dict, Any, TYPE_CHECKING
from ......logger import Scribe

if TYPE_CHECKING:
    from .engine import LexicalScope

Logger = Scribe("ContractWarden")

class ContractWarden:
    """
    =============================================================================
    == THE CONTRACT WARDEN (V-Ω-JURISPRUDENCE-ENFORCER)                        ==
    =============================================================================
    LIF: 50,000x | ROLE: TYPE_SAFETY_ADJUDICATOR
    Validates willed types JIT, halting the strike if Gnosis violates the Law of Form.
    Prepared for future expansion to Pydantic V2 native validation.
    """

    @classmethod
    def register(cls, scope: 'LexicalScope', var_name: str, contract_meta: Dict[str, Any]):
        """Enshrines a Law for a specific variable."""
        scope._contracts[var_name] = contract_meta
        Logger.info(f"⚖️ Contract Enforced: '{var_name}' must resonate as {contract_meta.get('type')}.")

    @classmethod
    def adjudicate(cls, scope: 'LexicalScope', name: str, value: Any):
        """Verifies if a value violates its Gnostic Contract."""
        contract = scope._contracts.get(name)
        if not contract:
            if scope.parent:
                return cls.adjudicate(scope.parent, name, value)
            return

        expected_type = contract.get("type")
        if expected_type == "int" and not isinstance(value, int):
            raise TypeError(f"Jurisprudence Violation: '{name}' expected INT, got {type(value).__name__}")
        if expected_type == "bool" and not isinstance(value, bool):
            raise TypeError(f"Jurisprudence Violation: '{name}' expected BOOL, got {type(value).__name__}")