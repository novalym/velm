# Path: core/lsp/scaffold_features/linter/registry.py
# ---------------------------------------------------

from typing import List, Any

# --- THE PANTHEON OF LAWS ---
from .rules.syntax_law import SyntaxLaw
from .rules.bond_law import GnosticBondLaw
from .rules.security_law import SecurityLaw
from .rules.geometry_law import GeometricPurityLaw
from .rules.complexity_law import ComplexityLaw
from .rules.artisan_inquest import ArtisanInquestRule

# --- THE ANCESTRAL CONTRACT ---
from ...base.features.linter.contracts import LinterRule

class LawRegistry:
    """
    =============================================================================
    == THE CODEX OF LAWS (V-Ω-SCAFFOLD-REGISTRY-SILENT)                        ==
    =============================================================================
    The central library of Scaffold-specific static analysis rules.
    """

    def __init__(self, server: Any):
        self.server = server
        self._custom_rules: List[LinterRule] = []

        # [ASCENSION]: TYPE HALLUCINATION BYPASS
        # We define the list without a strict generic type hint here to silence
        # the IDE's covariance confusion. The inheritance chain IS valid at runtime.
        self.core_laws = []

        # 1. The Law of Syntax ($$ / {{ }})
        self.core_laws.append(SyntaxLaw())

        # 2. The Law of Bonds (Path existence)
        self.core_laws.append(GnosticBondLaw(server))

        # 3. The Law of Security (Secrets)
        self.core_laws.append(SecurityLaw())

        # 4. The Law of Geometry (Whitespace)
        self.core_laws.append(GeometricPurityLaw())

        # 5. The Law of Entropy (Complexity)
        self.core_laws.append(ComplexityLaw())

        # 6. The Bridge to the Daemon (Adrenaline)
        self.core_laws.append(ArtisanInquestRule(server))

    def register_rule(self, rule: LinterRule):
        """Allows external consumers (Plugins) to add new laws."""
        self._custom_rules.append(rule)

    def get_rules(self, language_id: str) -> List[LinterRule]:
        """
        [THE JUDICIAL SELECTION]
        Returns the active laws for the given tongue.
        Explicitly typed return ensures downstream consumers know these are LinterRules.
        """
        # Runtime concatenation is valid because all items share the ancestor.
        return self.core_laws + self._custom_rules