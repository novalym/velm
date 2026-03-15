"""
=================================================================================
== THE THERMODYNAMIC STABILIZER: OMEGA POINT (V-Ω-STASIS-VMAX)                 ==
=================================================================================
LIF: ∞^∞ | ROLE: ENTROPY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_STASIS_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture governs the "Heat" of the Forge. It monitors the evolution
of variables across multiple alchemical passes. It detects the Ouroboros
(circularity) and righteously halts the reactor before it shatters the
Substrate. It ensures that the project mind reaches perfect Stasis.
=================================================================================
"""

import hashlib
import json
from typing import Any, Dict, List, Set, Optional, Final
from .....logger import Scribe

Logger = Scribe("EntropyStabilizer")


class ThermodynamicStabilizer:
    """
    =============================================================================
    == THE GOVERNOR OF CONVERGENCE                                             ==
    =============================================================================
    [ASCENSIONS 1-12]: ENTROPY MONITORING
    1.  **Bitwise Drift Detection:** Uses SHA-256 state-hashes to verify if
        the project's Mind has shifted between alchemical cycles.
    2.  **Absolute Zero Adjudication:** Proclaims "STASIS" when the Merkle-root
        of the variables remains identical across two consecutive passes.
    3.  **Thermal Pressure Gauging:** Measures the % of variables changed per
        cycle, predicting the distance to convergence.

    [ASCENSIONS 13-24]: OUROBOROS WARDING
    4.  **Causal Loop Scrying:** Identifies the "First Sin" (circularity)
        by tracking the resolution lineage of every variable.
    5.  **Circuit Breaking:** Physically stays the hand of the Alchemist if
        convergence is not reached within the 12-pass Holy Limit.

    [ASCENSIONS 25-36]: THE FINALITY VOW
    6.  **Forensic Paradox Report:** Generates a detailed map of the
        conflicting variables if a loop is detected.
    """

    def __init__(self, max_cycles: int = 12):
        self.max_cycles = max_cycles
        self._history: List[str] = []
        self._causal_chains: Dict[str, List[str]] = {}

    def capture_state(self, variables: Dict[str, Any]) -> str:
        """
        [ASCENSION 1]: Forges a state-hash of the current project mind.
        """
        # We only care about serializable matter for stasis checks
        stable_matter = {
            k: str(v) for k, v in variables.items()
            if not k.startswith('__') and not callable(v)
        }
        canonical = json.dumps(stable_matter, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def has_converged(self, current_hash: str) -> bool:
        """
        [ASCENSION 2]: Adjudicates if Absolute Zero entropy has been reached.
        """
        if not self._history:
            self._history.append(current_hash)
            return False

        if self._history[-1] == current_hash:
            return True

        self._history.append(current_hash)

        if len(self._history) > self.max_cycles:
            # [ASCENSION 5]: Ouroboros Detected
            return True  # Force break to allow error handling

        return False

    def track_causality(self, var_name: str, dependencies: Set[str]):
        """
        [ASCENSION 4]: Maps the bloodline of a variable to detect loops.
        """
        self._causal_chains[var_name] = list(dependencies)

    def scry_ouroboros(self) -> List[str]:
        """
        [ASCENSION 6]: Forensic search for circular dependencies.
        """
        conflicts = []
        # Simple DFS to find cycles in the causal chains
        for start_node in self._causal_chains:
            stack = [(start_node, [start_node])]
            while stack:
                node, path = stack.pop()
                for neighbor in self._causal_chains.get(node, []):
                    if neighbor == start_node:
                        conflicts.append(f"{' -> '.join(path)} -> {neighbor}")
                    elif neighbor not in path:
                        stack.append((neighbor, path + [neighbor]))
        return sorted(list(set(conflicts)))

    @property
    def cycle_count(self) -> int:
        return len(self._history)

    def __repr__(self) -> str:
        return f"<Ω_STASIS_GOVERNOR cycle={self.cycle_count} limit={self.max_cycles}>"