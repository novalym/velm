# Path: scaffold/core/alchemist/inference.py
# ---------------------------------
from functools import lru_cache
from typing import Dict, Any, Set, TYPE_CHECKING, Protocol

from ...contracts.heresy_contracts import ArtisanHeresy

if TYPE_CHECKING:
    from ...utils.gnosis_discovery import OmegaInquisitor
    from .engine import DivineAlchemist


# --- THE CONTRACT OF THE SIBLINGS ---
class AlchemicalHost(Protocol):
    def _get_inquisitor(self) -> 'OmegaInquisitor': ...

    def transmute(self, scripture: str, context: Dict[str, Any]) -> str: ...


class InferenceMixin:
    """
    The Logic of Discovery and Graph Resolution.
    """

    def _get_inquisitor(self) -> 'OmegaInquisitor':
        raise NotImplementedError("InferenceMixin requires a Host with _get_inquisitor")

    def transmute(self, scripture: str, context: Dict[str, Any]) -> str:
        raise NotImplementedError("InferenceMixin requires a Host with transmute")

    @lru_cache(maxsize=4096)
    def discover_variables(self, *scriptures: str, context_key: str = ".scaffold") -> set:
        """
        Delegates to the OmegaInquisitor to find variables used in a string.
        """
        inquisitor = self._get_inquisitor()
        all_vars = set()
        for scripture in scriptures:
            if not scripture or not isinstance(scripture, str):
                continue
            found_vars = inquisitor._contextual_gaze(scripture, context_key)
            all_vars.update(found_vars)
        return all_vars

    def resolve_gnostic_graph(self, initial_gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        The God-Engine of Graph Resolution.
        Annihilates Ouroboros loops by topologically sorting variable dependencies.
        """
        resolved_vars = {}
        unresolved_vars = {}

        # I. Distillation
        for key, value in initial_gnosis.items():
            if isinstance(value, str) and ('{{' in value or '{%' in value):
                unresolved_vars[key] = value
            else:
                resolved_vars[key] = value

        # II. Graph Construction
        dependencies = {
            key: self.discover_variables(value)
            for key, value in unresolved_vars.items()
        }

        # III. Iterative Transmutation
        max_iterations = len(unresolved_vars) + 1
        for _ in range(max_iterations):
            if not unresolved_vars:
                break

            resolved_in_this_pass = []
            for key, value in unresolved_vars.items():
                deps = dependencies.get(key, set())

                # Adjudicate: Are all dependencies known?
                if all(dep.split('.')[0] in resolved_vars for dep in deps):
                    try:
                        resolved_vars[key] = self.transmute(value, resolved_vars)
                        resolved_in_this_pass.append(key)
                    except Exception as e:
                        raise ArtisanHeresy(
                            f"Alchemical paradox resolving '$$ {key}': {e}",
                            child_heresy=e
                        )

            if not resolved_in_this_pass:
                # IV. Ouroboros Detection (THE FIX)
                # We interpret the dependency map, NOT the value strings.
                heresy_details = "Gnostic Ouroboros (circular dependency) or Missing Gnosis detected:\n"

                # Iterate keys remaining in unresolved_vars
                for key in unresolved_vars:
                    # Look up dependencies for this key
                    deps = dependencies.get(key, set())
                    # Find which specific dependencies are missing from resolved_vars
                    missing = [d for d in deps if d.split('.')[0] not in resolved_vars]

                    if missing:
                        heresy_details += f"  - '$$ {key}' waits for missing souls: {missing}\n"
                    else:
                        # If no missing deps but still stuck, it's a circular dependency among unresolved vars
                        heresy_details += f"  - '$$ {key}' is trapped in a circular bond with: {deps}\n"

                raise ArtisanHeresy(
                    "Gnostic Paradox: The Alchemist's Gaze is trapped in an infinite loop.",
                    details=heresy_details
                )

            # Remove resolved souls from the pending set
            for key in resolved_in_this_pass:
                del unresolved_vars[key]

        return resolved_vars