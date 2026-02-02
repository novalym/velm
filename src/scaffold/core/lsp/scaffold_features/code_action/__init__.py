# Path: core/lsp/scaffold_features/code_action/__init__.py
# --------------------------------------------------------

"""
=================================================================================
== THE HALL OF REDEMPTION (V-Ω-SCAFFOLD-CODE-ACTION-V12)                       ==
=================================================================================
The restorative center of the Gnostic Mind.
Provides specialized healers and refactorers for the Scaffold tongue.
=================================================================================
"""

from .engine import ScaffoldCodeActionEngine
from .providers.syntax_medic import SyntaxMedicProvider
from .providers.artisan_bridge import ArtisanBridgeProvider
from .providers.refactor_surgeon import RefactorSurgeonProvider
from .providers.neural_healer import NeuralHealerProvider

__all__ = [
    "ScaffoldCodeActionEngine",
    "SyntaxMedicProvider",
    "ArtisanBridgeProvider",
    "RefactorSurgeonProvider",
    "NeuralHealerProvider"
]