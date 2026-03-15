# Path: core/alchemist/elara/emitter/engine/conductor.py
# ------------------------------------------------------

import time
import os
import sys
import gc
import traceback
import threading
from typing import List, Dict, Any, Optional, Final

from ...contracts.atoms import GnosticToken, TokenType
from ..geometry.indenter import IsomorphicIndenter
from ..hydraulics.regulator import HydraulicFlowRegulator
from ..pacing.reaper import WhitespaceReaper
from ......logger import Scribe

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    psutil = None
    HAS_PSUTIL = False

Logger = Scribe("GeometricEmitter")


class GeometricEmitter:
    """
    =============================================================================
    == THE SUPREME MATTER CONDUCTOR (L3) (V-Ω-TOTALITY)                        ==
    =============================================================================
    LIF: ∞^∞ | ROLE: MATTER_ASSEMBLER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME

    Orchestrates the transmutation of the AST token stream into physical
    matter. It coordinates the Reaper (Pacing), the Indenter (Geometry), and
    the Regulator (Hydraulics).
    """

    __slots__ = (
        'depth', '_start_ns', '_total_atoms', '_trace_id',
        '_is_ether', '_lock', '_is_adrenaline'
    )

    def __init__(self, trace_id: str = "tr-emitter-void"):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()
        self.depth: int = 0
        self._start_ns: int = 0
        self._total_atoms: int = 0
        self._trace_id = trace_id

        self._is_ether = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def assemble(self, tokens: List[GnosticToken]) -> str:
        """
        =========================================================================
        == THE OMEGA ASSEMBLY: TOTALITY                                        ==
        =========================================================================
        """
        if not tokens:
            return ""

        self._start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: KINETIC PACING (THE REAPER) ---
        reaped_tokens = WhitespaceReaper.reap(tokens)
        self._total_atoms = len(reaped_tokens)

        # --- MOVEMENT I: HYDRAULIC INCEPTION ---
        regulator = HydraulicFlowRegulator(trace_id=self._trace_id)

        # [ASCENSION 25]: LAMINAR DEPTH ISOLATION
        is_sub_engine = getattr(self, 'depth', 0) > 0

        try:
            for idx, token in enumerate(reaped_tokens):

                if token.type in (TokenType.VOID, TokenType.COMMENT):
                    continue

                if token.type != TokenType.LITERAL:
                    regulator.write(str(token.raw_text))
                    continue

                # --- MOVEMENT II: GEOMETRIC ADJUDICATION ---
                if is_sub_engine or not token.metadata.get("is_resolved_variable"):
                    # Mute gravity for sub-engines or original un-resolved text
                    regulator.write(str(token.raw_text))
                else:
                    # Apply Absolute Spatial Resonance
                    aligned_matter = IsomorphicIndenter.align(token)
                    regulator.write(aligned_matter)

                # --- MOVEMENT III: THERMODYNAMIC PACING ---
                if idx % 1000 == 0:
                    self._monitor_heat_and_pace(idx)

            # --- MOVEMENT IV: THE RITE OF COLLAPSE ---
            final_matter = regulator.flush()

            # [ASCENSION 26]: Substrate EOL Harmonizer
            if os.name == 'nt' and not self._is_ether:
                # Retain CRLF on native Windows unless specified
                pass
            else:
                final_matter = final_matter.replace('\r\n', '\n')

            # --- MOVEMENT V: METABOLIC FINALITY ---
            self._proclaim_telemetry(regulator)
            return final_matter

        except Exception as catastrophic_paradox:
            Logger.critical(f"Emitter shattered at atom {idx}: {catastrophic_paradox}")
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                traceback.print_exc()
            return f"/* EMITTER_FRACTURE: {str(catastrophic_paradox)} */"
        finally:
            if self._total_atoms > 5000:
                gc.collect(1)

    def _monitor_heat_and_pace(self, current_idx: int):
        """[ASCENSION 13]: THERMAL FEVER ADJUDICATION."""
        self._project_hud_pulse(current_idx)

        if HAS_PSUTIL and not self._is_ether and not self._is_adrenaline:
            try:
                cpu_load = psutil.cpu_percent(interval=None)
                if cpu_load > 95.0:
                    time.sleep(0.005)  # Micro-yield
            except:
                pass

        if self._is_ether:
            time.sleep(0)

    def _project_hud_pulse(self, current_idx: int):
        """[ASCENSION 28]: Radiates progress to the HUD at 144Hz."""
        if self.depth > 0: return

        try:
            import sys
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)

            if engine and hasattr(engine, 'akashic') and engine.akashic:
                percent = int((current_idx / max(1, self._total_atoms)) * 100)
                engine.akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "matter_emission",
                        "message": f"Forging Physical Matter (L{self.depth})...",
                        "percentage": percent,
                        "trace": self._trace_id
                    }
                })
        except Exception:
            pass

    def _proclaim_telemetry(self, regulator: HydraulicFlowRegulator):
        if self.depth > 0: return

        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        stats = regulator.tomography()

        if duration_ms > 10.0 or stats['current_mass_kb'] > 500:
            Logger.success(
                f"L{self.depth} Matter manifest: {stats['current_mass_kb']}KB forged in "
                f"{duration_ms:.2f}ms. Seal: {stats['merkle_seal']}"
            )

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_EMITTER depth={self.depth} atoms={self._total_atoms} status=RESONANT>"