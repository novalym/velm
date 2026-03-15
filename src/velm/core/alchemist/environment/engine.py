# Path: core/alchemist/environment/engine.py
# ------------------------------------------

from typing import TYPE_CHECKING, Any

from .globals_vault import SGFGlobalsVault
from .filters_vault import SGFFiltersVault
from .cache_warden import SGFCacheWarden

if TYPE_CHECKING:
    from ..engine import DivineAlchemist


class SGFEnvironment:
    """
    =================================================================================
    == THE SOVEREIGN GNOSTIC ENVIRONMENT (V-Ω-TOTALITY-VMAX-JINJA-EXORCISM)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: LEXICAL_AND_METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SGF_ENVIRONMENT_VMAX_ISO_COMPATIBLE_2026_FINALIS

    [THE MANIFESTO]
    This is the ultimate Power Move. The `SGFEnvironment` perfectly mirrors the
    API surface of the ancient Jinja2 `Environment` (providing `.globals`, `.filters`,
    and `.cache.clear()`), but it is backed entirely by our Native, High-Velocity,
    AST-aware SGF organs.

    It completely satisfies legacy introspectors (`scaffold_scribe`), heals the
    AttributeError Heresy in the Materializer, and allows the God-Engine to
    remain 100% Jinja-free forever.
    =================================================================================
    """

    __slots__ = ('alchemist', 'globals', 'filters', 'cache')

    def __init__(self, alchemist: 'DivineAlchemist'):
        """
        [THE RITE OF INCEPTION]
        Binds the three sovereign organs to the Biosphere.
        """
        self.alchemist = alchemist

        # 1. THE MIND (Dynamic Functions & Macros)
        self.globals = SGFGlobalsVault()

        # 2. THE SOUL (Polyglot Filters & Rites)
        self.filters = SGFFiltersVault()

        # 3. THE BODY (Metabolic Lustration)
        self.cache = SGFCacheWarden()

    def __repr__(self) -> str:
        return f"<Ω_SGF_ENVIRONMENT filters={len(self.filters)} globals={len(self.globals)} status=PURE>"