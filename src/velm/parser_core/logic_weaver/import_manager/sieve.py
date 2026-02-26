# Path: src/velm/parser_core/logic_weaver/import_manager/sieve.py
# ---------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SIEVE_V25000_TOTAL_RECONCILIATION_FINALIS
# ---------------------------------------------------------------

from typing import List, Dict, Tuple, Any, TYPE_CHECKING
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser


class SocraticSieve:
    """
    =============================================================================
    == THE SOCRATIC SIEVE (V-Ω-SELECTIVE-DESTRUCTURING)                        ==
    =============================================================================
    Extracts only the specific variables, macros, and traits willed by the
    Architect during an `@from x import a, b` rite.
    """

    __slots__ = ('parser',)

    def __init__(self, parser: 'ApotheosisParser'):
        self.parser = parser

    def filter_atoms(
            self,
            willed_names: List[str],
            inhaled_vars: Dict[str, Any],
            sub_p: 'ApotheosisParser',
            src_name: str,
            line: int
    ) -> Tuple[Dict[str, Any], List[Any], List[Any]]:
        """
        [FACULTY 1]: THE ALCHEMICAL FILTER.
        Keeps only the requested atoms, mapping 'a as b' aliases flawlessly.
        Returns: (FilteredVars, EmptyItems, EmptyCommands) -> Matter is suppressed.
        """
        import difflib
        final_vars = {}

        for willed in willed_names:
            # Handle "a as b" aliasing
            if " as " in willed:
                src_key, dst_key = willed.split(" as ", 1)
            else:
                src_key, dst_key = willed, willed

            src_key, dst_key = src_key.strip(), dst_key.strip()
            found_atom = False

            # 1. Search Variables
            if src_key in inhaled_vars:
                final_vars[dst_key] = inhaled_vars[src_key]
                found_atom = True

            # 2. Search Macros
            if hasattr(sub_p, 'macros') and src_key in sub_p.macros:
                self.parser.macros[dst_key] = sub_p.macros[src_key]
                found_atom = True

            # 3. Search Traits
            if hasattr(sub_p, 'traits') and src_key in sub_p.traits:
                self.parser.traits[dst_key] = sub_p.traits[src_key]
                found_atom = True

            # 4. Search Tasks
            if hasattr(sub_p, 'tasks') and src_key in sub_p.tasks:
                self.parser.tasks[dst_key] = sub_p.tasks[src_key]
                found_atom = True

            # 5. Search Contracts
            if hasattr(sub_p, 'contracts') and src_key in sub_p.contracts:
                self.parser.contracts[dst_key] = sub_p.contracts[src_key]
                found_atom = True

            # The Inquisition
            if not found_atom:
                all_available = list(inhaled_vars.keys())
                if hasattr(sub_p, 'macros'): all_available.extend(sub_p.macros.keys())
                if hasattr(sub_p, 'tasks'): all_available.extend(sub_p.tasks.keys())
                if hasattr(sub_p, 'traits'): all_available.extend(sub_p.traits.keys())

                matches = difflib.get_close_matches(src_key, all_available, n=1, cutoff=0.5)
                suggestion = f" Did you mean '[cyan]{matches[0]}[/cyan]'?" if matches else ""

                raise ArtisanHeresy(
                    message=f"Coordinate Deficiency: Atom '{src_key}' is unmanifest in '{src_name}'.{suggestion}",
                    details=f"Inhalation site: L{line + 1}. Source registry contains {len(all_available)} souls.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line + 1,
                    ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                )

        # Selective destructuring suppresses all Matter (structural items) and Logic.
        return final_vars, [], []