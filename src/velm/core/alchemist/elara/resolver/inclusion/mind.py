# Path: core/alchemist/elara/resolver/inclusion/mind.py
# -----------------------------------------------------------

import time
import threading
import hashlib
import os
from typing import List, Any, TYPE_CHECKING, Dict, Optional, Set, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe
from .resolver import InclusionResolver
from .....runtime.vessels import GnosticSovereignDict
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..context import LexicalScope

Logger = Scribe("Inclusion:Mind")


class MindInhaler:
    """
    =================================================================================
    == THE OMNISCIENT MIND INHALER (V-Ω-TOTALITY-VMAX-LAMINAR-SUTURE)              ==
    =================================================================================
    LIF: ∞^∞ | ROLE: LOGIC_INHALATION_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MIND_INHALER_VMAX_LAMINAR_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for logic inhalation. This version righteously
    implements the **Laminar Reference Suture**, mathematically annihilating the
    Snapshot Schism. It ensures that imported reality remains entangled with
    the Prime Timeline's physical matter reservoirs.
    =================================================================================
    """

    # [ASCENSION 2]: O(1) MERKLE IMPORT LATTICE
    _IMPORT_LATTICE: Dict[str, GnosticSovereignDict] = {}

    # [ASCENSION 3]: OUROBOROS LOOP GUARD
    _IMPORT_STACK = threading.local()

    _LOCK = threading.RLock()

    @classmethod
    def inhale_namespace(cls, emissary: Any, path_str: str, alias: str, scope: 'LexicalScope'):
        """
        =============================================================================
        == THE RITE OF MIND INHALATION (V-Ω-TOTALITY-VMAX-SUTURED)                 ==
        =============================================================================
        LIF: 1,000,000x | ROLE: NEURAL_ALIGNER
        """
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(scope.global_ctx, 'trace_id', 'tr-mind-void')

        # 1. THE GEOMETRIC COMPASS
        scripture = InclusionResolver.scry_iron(path_str, scope)
        if not scripture:
            raise FileNotFoundError(f"Import Fracture: Mind '{path_str}' is unmanifest in the grimoire.")

        # 2. [ASCENSION 2]: MERKLE RESONANCE PROBE
        scripture_hash = hashlib.sha256(scripture.encode()).hexdigest()[:16]
        cache_key = f"{path_str}:{scripture_hash}"

        with cls._LOCK:
            if cache_key in cls._IMPORT_LATTICE:
                Logger.verbose(f"L1 Import Cache Hit: '{path_str}' resonated instantly.")
                scope.set(alias, cls._IMPORT_LATTICE[cache_key].copy())
                return

        # 3. [ASCENSION 3]: OUROBOROS LOOP GUARD
        if not hasattr(cls._IMPORT_STACK, 'paths'): cls._IMPORT_STACK.paths = set()
        if path_str in cls._IMPORT_STACK.paths:
            Logger.warn(f"Ouroboros Import Averted: '{path_str}' was already being inhaled. Recursive loop stayed.")
            return

        cls._IMPORT_STACK.paths.add(path_str)

        Logger.info(f"🧠 [IMPORT] Inhaling logic from '{path_str}' as '{alias}'... [Trace: {trace_id}]")

        try:
            # =========================================================================
            # == MOVEMENT I: [ASCENSION 1] - THE LAMINAR REFERENCE SUTURE            ==
            # =========================================================================
            # [THE MASTER CURE]: We MUST ensure the sub-transmutation pass can see
            # the Prime Reservoirs by physical reference.
            library_context = scope.global_ctx.variables.copy()

            # Suture the physical pointers
            for reservoir in ('__woven_matter__', '__woven_commands__', '__engine__', '__alchemist__'):
                if reservoir in scope.global_ctx.variables:
                    library_context[reservoir] = scope.global_ctx.variables[reservoir]

            # 4. [ASCENSION 7]: Trace ID Silver-Cord Propagation
            library_context['trace_id'] = trace_id
            library_context['__import_context__'] = True

            # 5. THE NEURAL STRIKE
            # Conduct the sub-parse through the Engine
            # This populates 'library_context' with the exported Gnosis.
            emissary.engine.transmute(scripture, library_context)

            # 6. THE NAMESPACE CONSECRATION
            # Filter internal engine noise and wrap in the Sovereign vessel
            clean_gnosis = {k: v for k, v in library_context.items() if not str(k).startswith('__')}
            library_soul = GnosticSovereignDict(clean_gnosis)

            # [ASCENSION 2]: Enshrine in Lattice
            with cls._LOCK:
                cls._IMPORT_LATTICE[cache_key] = library_soul

            # [ASCENSION 8]: Isomorphic Namespace Mapping
            scope.set(alias, library_soul.copy())

            # [ASCENSION 11]: Ocular HUD Multicast
            cls._radiate_hud_pulse(emissary.engine, "MIND_INHALED", alias, trace_id)

            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            Logger.success(f"   -> [RESONANT] Mind '{alias}' warded in {_tax_ms:.2f}ms.")

        finally:
            cls._IMPORT_STACK.paths.remove(path_str)

    @classmethod
    def inhale_selective(cls, emissary: Any, path_str: str, targets: List[str], scope: 'LexicalScope'):
        """
        =============================================================================
        == THE RITE OF SELECTIVE DESTRUCTURING (V-Ω-TOTALITY-VMAX)                 ==
        =============================================================================
        """
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(scope.global_ctx, 'trace_id', 'tr-selective-void')

        scripture = InclusionResolver.scry_iron(path_str, scope)
        if not scripture: return

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 1] - LAMINAR REFERENCE SUTURE                ==
        # =========================================================================
        library_context = scope.global_ctx.variables.copy()
        for reservoir in ('__woven_matter__', '__woven_commands__', '__engine__', '__alchemist__'):
            if reservoir in scope.global_ctx.variables:
                library_context[reservoir] = scope.global_ctx.variables[reservoir]

        library_context['trace_id'] = trace_id

        # THE NEURAL STRIKE
        emissary.engine.transmute(scripture, library_context)

        # [ASCENSION 23]: SOCRATIC SUGGESTION SUTURE
        import difflib
        available_keys = list(library_context.keys())

        for target in targets:
            if target in library_context:
                scope.set(target, library_context[target])
                Logger.verbose(f"   -> Siphoned atom '{target}' from '{path_str}'.")
            else:
                # [ASCENSION 23]: Socratic Search
                matches = difflib.get_close_matches(target, available_keys, n=1, cutoff=0.6)
                hint = f" Did you mean '{matches[0]}'?" if matches else ""
                Logger.warn(f"L? Symbol '{target}' is unmanifest in '{path_str}'.{hint}")

        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _tax_ms > 10.0:
            Logger.verbose(f"Selective Inhalation finalized in {_tax_ms:.2f}ms.")

    @staticmethod
    def _radiate_hud_pulse(engine: Any, label: str, alias: str, trace: str):
        """[ASCENSION 11]: Radiates progress to the Ocular HUD."""
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LOGIC_INHALED",
                        "label": f"IMPORT: {alias}",
                        "message": f"Mind-State {label} converged.",
                        "color": "#a855f7",  # Purple for Logic
                        "trace": trace
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_MIND_INHALER lattice_depth={len(self._IMPORT_LATTICE)} status=RESONANT>"