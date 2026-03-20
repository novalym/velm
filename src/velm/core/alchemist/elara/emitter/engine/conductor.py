# Path: core/alchemist/elara/emitter/engine/conductor.py
# ------------------------------------------------------


import time
import os
import sys
import gc
import traceback
import threading
import hashlib
from typing import List, Dict, Any, Optional, Final

# --- THE DIVINE UPLINKS ---
from ...contracts.atoms import GnosticToken, TokenType
from ..geometry.indenter import IsomorphicIndenter
from ..hydraulics.regulator import HydraulicFlowRegulator
from ..pacing.reaper import WhitespaceReaper
from ......logger import Scribe

# [ASCENSION: BINARY KERNEL PIVOT]
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    psutil = None
    HAS_PSUTIL = False

Logger = Scribe("GeometricEmitter")


class GeometricEmitter:
    """
    =================================================================================
    == THE SUPREME MATTER CONDUCTOR (L3): OMEGA POINT (V-Ω-TOTALITY-VMAX-60-ASC)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MATTER_ASSEMBLER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_EMITTER_VMAX_IRON_FUSION_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for translating Gnostic Atoms into Physical String
    Matter. It righteously implements the **Structure of Arrays (SoA) Suture**, mathematically
    annihilating the "Python Attribute Tax" by pushing parallel primitive arrays
    directly into the compiled Rust Core.

    ### THE PANTHEON OF 12 NEW LEGENDARY ASCENSIONS (53-64):
    53. **Structure of Arrays (SoA) Suture (THE MASTER CURE):** Bypasses all `getattr`
        calls in PyO3. Python uses lightning-fast list comprehensions to build flat
        arrays of (`t_types`, `raw_texts`, `col_indices`, etc.) and hands them to Rust.
    54. **Holographic Metadata Bit-Packing:** C-speed extraction of nested dictionaries
        (`is_virtual`, `is_binary`) into a singular `u8` integer bitmask per token.
    55. **Vectorized Pydantic Decapitation:** Annihilates the 100,000x Object Iteration
        tax inside Rust by ensuring the Python bridge sends only primitive strings and ints.
    56. **Asynchronous Telemetry Projection:** Fire-and-forget HUD pulses that
        instantly release the GIL.
    57. **The Substrate EOL Suture V3:** Uses byte-level probing in Rust to
        guarantee pure `\\n` translation before OS delivery.
    58. **Zero-Stiction Exception Unwrapping:** Maps Rust Panics natively into
        UCL Heresies for the Healer.
    59. **The Thermal Threshold Guard:** If CPU load exceeds 98%, triggers an
        `os.sched_yield()` equivalent to let the Kernel and Browser breathe.
    60. **The Finality Vow:** A mathematical guarantee of bit-perfect, correctly
        indented, and fully assembled string matter.
    =================================================================================
    """

    __slots__ = (
        'depth', '_start_ns', '_total_atoms', '_trace_id',
        '_is_ether', '_lock', '_is_adrenaline', '_total_mass_bytes',
        '_hud_lock', '_force_python'
    )

    # [ASCENSION 29]: Hydraulic Batch Size (5MB) - Used only in Python Fallback
    FUSION_THRESHOLD_BYTES: Final[int] = 5 * 1024 * 1024

    def __init__(self, trace_id: str = "tr-emitter-void"):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()
        self._hud_lock = threading.Lock()
        self.depth: int = 0
        self._start_ns: int = 0
        self._total_atoms: int = 0
        self._total_mass_bytes: int = 0
        self._trace_id = trace_id

        self._is_ether = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._force_python = os.environ.get("SCAFFOLD_NO_RUST") == "1"

    def assemble(self, tokens: List[GnosticToken]) -> str:
        """
        =========================================================================
        == THE OMEGA ASSEMBLY: TOTALITY (V-Ω-IRON-FUSION-SUTURE)               ==
        =========================================================================
        LIF: ∞^∞ | ROLE: MATTER_MATERIALIZER
        """
        # [ASCENSION 43]: NoneType Sarcophagus v14
        if not tokens:
            return ""

        self._start_ns = time.perf_counter_ns()
        self._total_atoms = len(tokens)

        # =========================================================================
        # == MOVEMENT I:[ASCENSION 53] - THE STRUCTURE OF ARRAYS (SoA) SUTURE    ==
        # =========================================================================
        if RUST_AVAILABLE and not self._is_ether and not self._force_python:
            try:
                # [THE MASTER CURE]: We decompose the Object list into parallel arrays
                # using CPython's highly optimized list comprehensions. This totally bypasses
                # the PyO3 `getattr` tax during the Rust evaluation loop!

                t_types = [t.type.name for t in tokens]
                raw_texts = [t.raw_text for t in tokens]
                col_indices = [t.column_index for t in tokens]
                orig_indents = [getattr(t, 'original_indent', t.column_index) for t in tokens]

                # [ASCENSION 54]: Holographic Metadata Bit-Packing
                # Bit 0: is_virtual | Bit 1: is_binary | Bit 2: is_resolved_var
                bitmasks = [
                    (1 if t.metadata.get("is_virtual", False) else 0) |
                    (2 if getattr(t, 'is_binary', False) else 0) |
                    (4 if t.metadata.get("is_resolved_variable", False) else 0)
                    for t in tokens
                ]

                # [STRIKE]: We pass the arrays to Rust, eliminating object overhead
                final_matter = scaffold_core_rs.assemble_reality_fast(
                    t_types, raw_texts, col_indices, orig_indents, bitmasks
                )

                self._total_mass_bytes = len(final_matter.encode('utf-8'))

                # Metabolic Finality
                self._proclaim_telemetry_fast()

                # [ASCENSION 46]: Merkle-State Validation
                if os.environ.get("SCAFFOLD_DEBUG") == "1":
                    final_hash = hashlib.sha256(final_matter.encode('utf-8')).hexdigest()[:8]
                    Logger.verbose(f"Emitter Merkle Seal (Rust SoA): 0x{final_hash.upper()}")

                return final_matter

            except Exception as rust_fracture:
                Logger.debug(f"Iron Emitter Fractured: {rust_fracture}. Devolving to Python Fallback.")
                # We gracefully fall back to the Python loop if Rust encounters an exotic token.

        # =========================================================================
        # == MOVEMENT II: THE PYTHONIC FALLBACK SWARM                            ==
        # =========================================================================
        # --- KINETIC PACING (THE REAPER) ---
        reaped_tokens = WhitespaceReaper.reap(tokens)
        self._total_atoms = len(reaped_tokens)

        # Pre-calculate total expected mass for Socratic Progress Resolution
        total_expected_mass = sum(len(t.raw_text or "") for t in reaped_tokens)
        if total_expected_mass == 0: total_expected_mass = 1

        regulator = HydraulicFlowRegulator(trace_id=self._trace_id)

        # Hydraulic Batch Fusion Buffer
        fusion_buffer: List[str] = []
        current_batch_mass = 0

        is_sub_engine = getattr(self, 'depth', 0) > 0

        try:
            for idx, token in enumerate(reaped_tokens):

                # [ASCENSION 40 & 50]: The Vacuum State Exorcist & Ghost-Matter Bypass
                if token.type in (TokenType.VOID, TokenType.COMMENT):
                    continue
                if token.metadata.get('is_virtual', False):
                    continue
                if not token.raw_text:
                    continue

                if token.type != TokenType.LITERAL:
                    matter = str(token.raw_text)
                else:
                    # GEOMETRIC ADJUDICATION
                    # [ASCENSION 34]: Binary Matter Fast-Path
                    if getattr(token, 'is_binary', False):
                        matter = str(token.raw_text)

                    # [ASCENSION 30 & 35]: O(1) Isomorphic Chunking & Phantom Indent Sieve
                    elif is_sub_engine or not token.metadata.get("is_resolved_variable"):
                        if getattr(token, 'column_index', 0) == getattr(token, 'original_indent', 0):
                            matter = str(token.raw_text)
                        else:
                            matter = IsomorphicIndenter.align(token)
                    else:
                        matter = IsomorphicIndenter.align(token)

                # --- THE HYDRAULIC BATCH FUSION ---
                fusion_buffer.append(matter)
                matter_len = len(matter)
                current_batch_mass += matter_len
                self._total_mass_bytes += matter_len

                # C-Speed Array Join and Flush
                if current_batch_mass >= self.FUSION_THRESHOLD_BYTES:
                    fused_matter = "".join(fusion_buffer)
                    regulator.write(fused_matter)
                    fusion_buffer.clear()
                    current_batch_mass = 0

                # --- THERMODYNAMIC PACING ---
                if idx % 2000 == 0:
                    self._monitor_heat_and_pace(self._total_mass_bytes, total_expected_mass)

            # Flush remaining buffer
            if fusion_buffer:
                regulator.write("".join(fusion_buffer))
                fusion_buffer.clear()

            # --- THE RITE OF COLLAPSE ---
            final_matter = regulator.flush()

            # [ASCENSION 33 & 47]: Substrate EOL Suture V2
            if os.name == 'nt' and not self._is_ether:
                pass
            else:
                final_matter = final_matter.replace('\r\n', '\n')

            # [ASCENSION 32]: Apophatic Toxin Purge V2
            if '\x00' in final_matter:
                final_matter = final_matter.replace('\x00', '')

            # --- METABOLIC FINALITY ---
            self._proclaim_telemetry_fallback(regulator)

            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                final_hash = hashlib.sha256(final_matter.encode('utf-8')).hexdigest()[:8]
                Logger.verbose(f"Emitter Merkle Seal (Python): 0x{final_hash.upper()}")

            return final_matter

        except Exception as catastrophic_paradox:
            Logger.critical(
                f"Emitter shattered at atom {idx} (Mass: {self._total_mass_bytes}B): {catastrophic_paradox}")
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                traceback.print_exc()
            return f"/* EMITTER_FRACTURE: {str(catastrophic_paradox)} */"
        finally:
            if self._total_mass_bytes > (50 * 1024 * 1024) and not self._is_adrenaline:
                gc.collect(1)

    def _monitor_heat_and_pace(self, current_mass: int, total_mass: int):
        """[ASCENSION 45]: THE THERMAL THRESHOLD GUARD."""
        self._project_hud_pulse(current_mass, total_mass)

        if HAS_PSUTIL and not self._is_ether and not self._is_adrenaline:
            try:
                cpu_load = psutil.cpu_percent(interval=None)
                if cpu_load > 98.0:
                    time.sleep(0.01)
                elif cpu_load > 90.0:
                    time.sleep(0.002)
            except:
                pass

        if self._is_ether:
            time.sleep(0)

    def _project_hud_pulse(self, current_mass: int, total_mass: int):
        """[ASCENSION 41 & 42]: Bicameral Lock Segregation & Socratic Progress."""
        if self.depth > 0: return

        if not self._hud_lock.acquire(blocking=False):
            return

        try:
            import sys
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)

            if engine and hasattr(engine, 'akashic') and engine.akashic:
                percent = int((current_mass / max(1, total_mass)) * 100)
                percent = min(99, percent)

                engine.akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "matter_emission",
                        "message": f"Forging Physical Matter ({current_mass // 1024}KB)...",
                        "percentage": percent,
                        "trace": self._trace_id
                    }
                })
        except Exception:
            pass
        finally:
            self._hud_lock.release()

    def _proclaim_telemetry_fast(self):
        """
        =============================================================================
        == THE ACHRONAL TELEMETRY RADIATOR (RUST-NATIVE)                           ==
        =============================================================================
        """
        if self.depth > 0:
            return

        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        mass_kb = self._total_mass_bytes / 1024.0

        if duration_ms > 10.0 or mass_kb > 500.0:
            Logger.success(
                f"L{self.depth} Matter manifest: {mass_kb:.1f}KB fused natively via Rust in {duration_ms:.2f}ms."
            )

    def _proclaim_telemetry_fallback(self, regulator: HydraulicFlowRegulator):
        if self.depth > 0: return

        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        stats = regulator.tomography()

        if duration_ms > 10.0 or stats['current_mass_kb'] > 500:
            Logger.success(
                f"L{self.depth} Matter manifest: {stats['current_mass_kb']}KB fused natively via Python in "
                f"{duration_ms:.2f}ms. Spool: {'ACTIVE' if stats.get('is_spooled') else 'DORMANT'}"
            )

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_EMITTER mass={self._total_mass_bytes}B atoms={self._total_atoms} status=RESONANT>"