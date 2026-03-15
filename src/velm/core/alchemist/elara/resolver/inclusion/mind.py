# Path: core/alchemist/elara/resolver/inclusion/mind.py
# -----------------------------------------------------------

from typing import List, Any, TYPE_CHECKING
from ......logger import Scribe
from .resolver import InclusionResolver

if TYPE_CHECKING:
    from ..context import LexicalScope

Logger = Scribe("Inclusion:Mind")


class MindInhaler:
    """
    =============================================================================
    == THE MIND INHALER (V-Ω-TOTALITY)                                         ==
    =============================================================================
    ROLE: LOGIC_INHALATION_CONDUCTOR
    Handles {% import %} and {% from ... import %} by siphoning Gnosis into scope.
    """

    @classmethod
    def inhale_namespace(cls, emissary: Any, path_str: str, alias: str, scope: 'LexicalScope'):
        """[THE RITE OF MIND INHALATION]"""
        scripture = InclusionResolver.scry_iron(path_str, scope)
        if not scripture:
            raise FileNotFoundError(f"Import Fracture: Mind '{path_str}' is unmanifest.")

        Logger.info(f"🧠 [IMPORT] Inhaling logic from '{path_str}' as '{alias}'...")

        # 1. THE BICAMERAL FISSION
        # Spawn a child scope to isolate the library's internal state
        temp_scope = scope.spawn_child(name=f"import_{alias}")

        # 2. THE NEURAL STRIKE
        # We inhale variables by running a transmutaton on a dummy context
        library_context = scope.global_ctx.variables.copy()
        emissary.engine.transmute(scripture, library_context)

        # 3. THE NAMESPACE SUTURE
        from .....runtime.vessels import GnosticSovereignDict
        library_soul = GnosticSovereignDict(library_context)

        # [ASCENSION 5]: Ward within the alias
        scope.set(alias, library_soul)
        Logger.success(f"   -> Mind '{alias}' is now warded and resonant.")

    @classmethod
    def inhale_selective(cls, emissary: Any, path_str: str, targets: List[str], scope: 'LexicalScope'):
        """[THE RITE OF SELECTIVE DESTRUCTURING]"""
        scripture = InclusionResolver.scry_iron(path_str, scope)
        if not scripture: return

        library_context = scope.global_ctx.variables.copy()
        emissary.engine.transmute(scripture, library_context)

        for target in targets:
            if target in library_context:
                scope.set(target, library_context[target])
                Logger.verbose(f"   -> Siphoned atom '{target}' from '{path_str}'.")