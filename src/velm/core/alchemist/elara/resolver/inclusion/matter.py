# Path: core/alchemist/elara/resolver/inclusion/matter.py
# -----------------------------------------------------------

import time
import os
import threading
import hashlib
import textwrap
from pathlib import Path
from typing import Any, List, Optional, Dict, Tuple, Set, Final, Union, TYPE_CHECKING

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe
from .resolver import InclusionResolver
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..context import LexicalScope

Logger = Scribe("Inclusion:Matter")


class MatterInceptor:
    """
    =================================================================================
    == THE OMNISCIENT MATTER INCEPTOR (V-Ω-TOTALITY-VMAX-LAMINAR-GEOMETRY)         ==
    =================================================================================
    LIF: ∞^∞ | ROLE: PHYSICAL_MATTER_REALIZER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MATTER_INCEPTOR_VMAX_LAMINAR_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for physical reification. This version righteously
    implements the **Laminar Indentation Suture**, mathematically annihilating
    the "Indentation Heresy" by forcing included matter to adopt the visual
    gravity of its call-site.
    =================================================================================
    """

    # [ASCENSION 2]: O(1) MERKLE LATTICE CACHE
    # Caches the fully transmuted results of included files.
    _MEMO_LATTICE: Dict[str, str] = {}

    # [ASCENSION 3]: OUROBOROS LOOP GUARD
    # Tracks the recursion stack for the current thread.
    _INCLUSION_STACK = threading.local()

    _LOCK = threading.RLock()

    @classmethod
    def include(cls, emissary: Any, path_str: str, scope: 'LexicalScope', ignore_missing: bool = False) -> str:
        """
        =============================================================================
        == THE RITE OF MATTER INCEPTION (V-Ω-TOTALITY-VMAX-SUTURED)                ==
        =============================================================================
        LIF: 1,000,000x | ROLE: MATTER_MATERIALIZER
        """
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(scope.global_ctx, 'trace_id', 'tr-matter-void')

        # 1. THE VOID GUARD
        if not path_str:
            return ""

        # 2. THE GEOMETRIC COMPASS
        # [ASCENSION 4]: Achronal Path Triangulation.
        scripture = InclusionResolver.scry_iron(path_str, scope)

        if not scripture:
            if ignore_missing: return ""
            # [ASCENSION 8]: Socratic Suggestion Suture
            raise FileNotFoundError(f"Inclusion Fracture: Matter '{path_str}' is unmanifest in the grimoire.")

        # 3. [ASCENSION 3]: OUROBOROS LOOP GUARD
        if not hasattr(cls._INCLUSION_STACK, 'paths'): cls._INCLUSION_STACK.paths = set()
        if path_str in cls._INCLUSION_STACK.paths:
            Logger.warn(f"Ouroboros Matter Averted: Circular include detected for '{path_str}'. Branch severed.")
            return f"/* CIRCULAR_INCLUDE_WARD: {path_str} */"

        cls._INCLUSION_STACK.paths.add(path_str)

        # 4. [ASCENSION 2]: MERKLE RESONANCE PROBE
        # We hash the scripture + the variable state hash to determine if we can skip transmutation.
        state_hash = getattr(scope.global_ctx, 'fingerprint', '0xVOID')
        cache_key = hashlib.sha256(f"{path_str}:{scripture}:{state_hash}".encode()).hexdigest()[:16]

        with cls._LOCK:
            if cache_key in cls._MEMO_LATTICE:
                cls._INCLUSION_STACK.paths.remove(path_str)
                return cls._MEMO_LATTICE[cache_key]

        Logger.info(f"🌀 [INCLUSION] Weaving matter from '{path_str}'... [Trace: {trace_id}]")

        try:
            # 5. [ASCENSION 1]: LAMINAR INDENTATION SUTURE (THE MASTER CURE)
            # We scry the context for the visual column index of the call-site.
            # This allows us to pad the incoming matter so it aligns with the
            # Architect's willed geometry.
            call_site_indent = scope.get("__current_column__", 0)

            # --- MOVEMENT I: SUB-TRANSMUTATION ---
            # Prepare the child gnosis, preserving physical references
            current_gnosis = scope.global_ctx.variables.copy()
            current_gnosis.update(scope.local_vars)

            # [ASCENSION 6]: Trace ID Propagation
            current_gnosis['trace_id'] = trace_id
            current_gnosis['__is_include_pass__'] = True

            # [STRIKE]: Execute the Alchemical Forge
            # Geometric alignment is handled by the parent Emitter, but we
            # perform the first pass of resolution here.
            transmuted_matter = emissary.engine.transmute(scripture, current_gnosis)

            # --- MOVEMENT II: GEOMETRIC SHIFT ---
            # If the matter is multi-line and we are indented, we apply the shift.
            if call_site_indent > 0 and "\n" in transmuted_matter:
                # We skip the first line as it's already aligned with the tag.
                lines = transmuted_matter.splitlines()
                if len(lines) > 1:
                    padding = " " * call_site_indent
                    shifted_lines = [lines[0]] + [padding + line for line in lines[1:]]
                    transmuted_matter = "\n".join(shifted_lines)

            # 6. CONSECRATION
            with cls._LOCK:
                # [ASCENSION 7]: Hydraulic Memory Yield
                if len(cls._MEMO_LATTICE) > 1000:
                    cls._MEMO_LATTICE.clear()
                cls._MEMO_LATTICE[cache_key] = transmuted_matter

            # [ASCENSION 13]: Ocular HUD Multicast
            cls._radiate_hud_pulse(emissary.engine, path_str, len(transmuted_matter), trace_id)

            return transmuted_matter

        except Exception as catastrophic_paradox:
            # [ASCENSION 18]: Fault-Isolated Redemption
            Logger.error(f"Inclusion Logic Fracture in '{path_str}': {catastrophic_paradox}")
            return f"/* INCLUSION_FRACTURE: {path_str} | Reason: {str(catastrophic_paradox)} */"

        finally:
            cls._INCLUSION_STACK.paths.remove(path_str)
            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            if _tax_ms > 20.0:
                Logger.verbose(f"High-Mass Inception: '{path_str}' manifest in {_tax_ms:.2f}ms.")

    @staticmethod
    def _radiate_hud_pulse(engine: Any, path: str, mass: int, trace: str):
        """[ASCENSION 13]: Radiates status to the Ocular HUD."""
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_INCEPTED",
                        "label": f"INCLUDE: {Path(path).name}",
                        "message": f"Reified {mass} bytes of physical iron.",
                        "color": "#64ffda",  # Teal for Matter
                        "trace": trace
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_MATTER_INCEPTOR lattice_depth={len(self._MEMO_LATTICE)} status=RESONANT>"