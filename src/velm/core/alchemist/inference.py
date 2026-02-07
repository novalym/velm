# Path: src/velm/core/alchemist/inference.py
# ------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_GRAPH_RESOLVER | RANK: OMEGA_SUPREME
# AUTH: Ω_ALCHEMIST_INFERENCE_V200_SINGULARITY_TOTALITY
# =========================================================================================

import logging
import hashlib
import json
import re
from functools import lru_cache
from typing import Dict, Any, Set, TYPE_CHECKING, Protocol, List, Tuple, Union

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...utils.gnosis_discovery import OmegaInquisitor
    from .engine import DivineAlchemist


# --- THE CONTRACT OF THE SIBLINGS ---
class AlchemicalHost(Protocol):
    """The Sacred Protocol defining the interface between the Mind and the Hand."""

    def _get_inquisitor(self) -> 'OmegaInquisitor': ...

    def transmute(self, scripture: str, context: Dict[str, Any]) -> str: ...


class InferenceMixin:
    """
    =================================================================================
    == THE INFERENCE ENGINE (V-Ω-TOTALITARIAN-CONVERGENCE)                         ==
    =================================================================================
    The divine mind of variable discovery and topological resolution.
    =================================================================================
    """

    def _get_inquisitor(self) -> 'OmegaInquisitor':
        """Must be manifest in the Host."""
        raise NotImplementedError("InferenceMixin requires a Host with _get_inquisitor")

    def transmute(self, scripture: str, context: Dict[str, Any]) -> str:
        """Must be manifest in the Host."""
        raise NotImplementedError("InferenceMixin requires a Host with transmute")

    @lru_cache(maxsize=8192)
    def discover_variables(self, scripture: str, context_key: str = ".scaffold") -> Set[str]:
        """
        [FACULTY 3, 7, 11]: RECURSIVE SCRYING.
        Scries a string for Gnostic symbols, pruning noise and isolating roots.
        """
        if not scripture or not isinstance(scripture, str):
            return set()

        # [PRUDENCE GATE]: Fast-check for alchemical sigils.
        if '{{' not in scripture and '{%' not in scripture:
            return set()

        inquisitor = self._get_inquisitor()
        try:
            # Command the Oracle to gaze upon the context
            found_vars = inquisitor._contextual_gaze(scripture, context_key)

            # [ASCENSION 11]: ATTRIBUTE ROOT ISOLATION
            # Filter out numeric literals and Jinja2 built-ins.
            roots = {v.split('.')[0] for v in found_vars if v and not v[0].isdigit()}

            # [ASCENSION 6]: HEURISTIC PRUNING
            JINJA_NOISE = {
                'range', 'dict', 'list', 'cycle', 'set', 'get', 'none',
                'true', 'false', 'default', 'snake', 'slug', 'pascal', 'camel',
                'var_start', 'var_end'
            }
            return {r for r in roots if r.lower() not in JINJA_NOISE}

        except Exception:
            # [FACULTY 7]: THE NONE-TYPE SARCOPHAGUS
            return set()

    def resolve_gnostic_graph(self, initial_gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        =================================================================================
        == THE OMEGA CONVERGENCE REACTOR (V-Ω-TOTALITY-V200.0)                         ==
        =================================================================================
        [THE CURE]: This algorithm implements Totalitarian Convergence. It treats
        variable resolution as a thermodynamic process. It repeatedly transmutes
        the entire set until bitwise stability (Entropy=0) is reached.
        """
        # --- MOVEMENT I: INITIALIZATION ---
        # 'resolved_vars' represents the Manifest Reality (Grounded Matter).
        # We seed it with the initial input to allow Sovereign Shadowing.
        resolved_vars = initial_gnosis.copy()
        self.Logger.info("Alchemist: Initiating Totalitarian Convergence Reactor.")

        # --- MOVEMENT II: THE RITE OF DISCOVERY ---
        # We scan the entire multiverse once to identify the Prophecies.
        prophecies: Dict[str, str] = {}
        for key, value in initial_gnosis.items():
            if isinstance(value, str) and ('{{' in value or '{%' in value):
                prophecies[key] = value

        if not prophecies:
            return resolved_vars

        # Map the causal bonds between prophecies
        dependencies: Dict[str, Set[str]] = {
            key: self.discover_variables(value)
            for key, value in prophecies.items()
        }

        # --- MOVEMENT III: THE CONVERGENCE REACTOR ---
        # [ASCENSION 8]: Topological Depth Warden.
        max_reactor_cycles = len(prophecies) + 30

        for cycle in range(max_reactor_cycles):
            # 1. Capture the State of the Multiverse (Entropy Check)
            state_hash = hashlib.sha256(str(sorted(resolved_vars.items())).encode()).hexdigest()

            drifted = False
            # Stable snapshot of the context for this specific reactor cycle
            context_for_cycle = resolved_vars.copy()

            # 2. THE ALCHEMICAL SWEEP
            # [ASCENSION 10]: Deterministic Resonance.
            for key in sorted(prophecies.keys()):
                prophecy_scripture = prophecies[key]
                required_souls = dependencies.get(key, set())

                # [ASCENSION 5]: SOVEREIGN SELF-SHADOWING (THE CURE)
                # A variable is ready for transmutation if:
                # A. All its external dependencies are manifest in 'resolved_vars'.
                # B. If it depends on itself, an initial literal soul must exist.

                can_resolve = True
                for soul in required_souls:
                    if soul not in resolved_vars:
                        can_resolve = False
                        break

                    if soul == key:
                        # Self-reference detected. Check for a literal ancestor.
                        ancestor = initial_gnosis.get(key)
                        if isinstance(ancestor, str) and ('{{' in ancestor or '{%' in ancestor):
                            # Ancestor is also a prophecy. This is a lethal loop.
                            can_resolve = False
                            break

                if can_resolve:
                    try:
                        # [THE TRANSMUTATION STRIKE]
                        # We mask self-referencing variables with their initial state
                        # to allow Jinja2's shadowing logic (like default()) to function.
                        if key in required_souls:
                            context_for_cycle[key] = initial_gnosis[key]

                        # Execute the alchemical transmutation
                        manifested_matter = self.transmute(prophecy_scripture, context_for_cycle)

                        # [ASCENSION 18]: THE OUROBOROS CAGE
                        if len(str(manifested_matter)) > 1_000_000:
                            raise ArtisanHeresy("Metabolic Overflow: Variable length exceeded 1MB.")

                        if manifested_matter != resolved_vars.get(key):
                            resolved_vars[key] = manifested_matter
                            drifted = True

                    except Exception as e:
                        # Non-fatal during early passes as dependencies might be late
                        pass

            # 3. ADJUDICATE STABILITY
            new_state_hash = hashlib.sha256(str(sorted(resolved_vars.items())).encode()).hexdigest()

            if new_state_hash == state_hash and not drifted:
                self.Logger.success(f"Gnostic Graph reached stability in {cycle + 1} reactor cycles.")
                break
        else:
            # REACTOR OVERLOAD: Stasis reached but braces remain.
            # Perform a forensic biopsy to identify the circularity.
            self._proclaim_stasis_heresy(resolved_vars, dependencies)

        # --- MOVEMENT IV: THE OMEGA-PASS (FINAL FLATTENING) ---
        # [ASCENSION 4]: THE CURE FOR ESCAPED TAGS
        # We perform one final recursive flattening pass to annihilate
        # any remaining braces (like {{ var_start }}).
        self.Logger.verbose("Alchemist: Commencing the Omega-Pass (Final Flattening).")

        for _ in range(10):  # Max 10 levels of meta-nesting
            drifted = False
            for key, value in resolved_vars.items():
                if isinstance(value, str) and ('{{' in value or '{%' in value):
                    try:
                        flattened = self.transmute(value, resolved_vars)
                        if flattened != value:
                            resolved_vars[key] = flattened
                            drifted = True
                    except Exception:
                        pass
            if not drifted: break

        # --- MOVEMENT V: THE FINAL SANITY SCRY ---
        # [ASCENSION 12]: THE FINALITY VOW
        for k, v in resolved_vars.items():
            if isinstance(v, str) and ('{{' in v or '}}' in v):
                self.Logger.warn(f"Lattice Leak: Variable '$$ {k}' contains unrendered Gnostic sigils.")

        return resolved_vars

    def _proclaim_stasis_heresy(self, context: Dict[str, Any], dependencies: Dict[str, Set[str]]):
        """[ASCENSION 15]: FORENSIC PARADOX TOMOGRAPHY."""
        conflicts = []
        for k, v in context.items():
            if isinstance(v, str) and ('{{' in v or '{%' in v):
                deps = dependencies.get(k, set())
                conflicts.append(f"  - '$$ {k}' waits for: {list(deps)}")

        raise ArtisanHeresy(
            "Gnostic Ouroboros: The variable graph has failed to reach bitwise stability.",
            details="The following variables are trapped in a lethal loop or missing a literal base:\n" + "\n".join(
                conflicts),
            severity=HeresySeverity.CRITICAL,
            suggestion="Verify that variables are not referencing each other in a circle (A->B, B->A) without an initial literal soul from the CLI or Parent."
        )

# == SCRIPTURE SEALED: THE ALCHEMIST'S MIND IS OMEGA TOTALITY ==