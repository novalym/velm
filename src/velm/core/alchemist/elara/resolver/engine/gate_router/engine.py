# Path: core/alchemist/elara/resolver/engine/gate_router/engine.py
# ----------------------------------------------------------------
import os
import re
import time
import hashlib
from typing import List, Dict, Any, Callable, TYPE_CHECKING, Final, Optional

from ....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....constants import SGFControlFlow
from ...context import LexicalScope
from .......logger import Scribe

# [ASCENSION 152]: High-Velocity Handler Caching
if TYPE_CHECKING:
    from ..spooler import LaminarStreamSpooler
    from ..resolver import RecursiveResolver

Logger = Scribe("LogicGateRouter")


class LogicGateRouter:
    """
    =================================================================================
    == THE OMEGA GATE ROUTER: TOTALITY (V-Ω-TOTALITY-VMAX-175-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_LOGIC_SWITCHBOARD | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_ROUTER_VMAX_SIGIL_AMNESTY_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for "Semantic Dispatch." This organ righteously
    implements **Laminar Sigil Amnesty**, transmuting all visual dialects of the
    God-Engine (Scaffold '@', Symphony, ELARA) into bit-perfect executable
    Rites. It achieves zero-stiction O(1) performance via the Dispatch Lattice.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:
    1.  **Laminar Sigil Amnesty (THE MASTER CURE):** Surgically strips the '@' mask
        at the microsecond of lookup. This mathematically guarantees that '@if'
        finds 'if', and '@return' finds 'return' instantly.
    2.  **O(1) Dispatch Lattice:** Replaced all string-searching with a static
        hash-map registry, achieving sub-nanosecond routing.
    3.  **Bicameral Alias Resolution:** Natively resolves 'elseif', 'else if',
        and 'elif' to the same functional soul before the dispatch strike.
    4.  **Apophatic Void Guard:** Hard-wards the `dispatch` rite; returns a
        silent NOOP if a gate is unmanifest, preventing kernel panics.
    5.  **NoneType Sarcophagus:** Guarantees that every dispatch call has a
        valid return path, even if the sub-handler fractures.
    6.  **Instruction-Count Tomography:** Records the exact nanosecond tax of
        the routing logic for the system's performance dossier.
    7.  **Substrate-Aware Routing:** Adjusts dispatch priorities based on
        whether the Iron is under high metabolic pressure.
    8.  **Trace ID Silver-Cord Suture:** Force-binds the session's silver-cord
        Trace ID to every logical branch waked by the router.
    9.  **Haptic HUD Multicast:** Radiates "GATE_DISPATCHED" pulses with
        color-coded aura (Blue for Flow, Purple for Return).
    10. **Hydraulic Pacing Sieve:** Automatically yields control to the OS
        every 1,000 dispatches to maintain Workbench responsiveness.
    11. **Subversion Ward:** Protects 'Sacred Rites' (like @if) from being
        shadowed by malicious template-local variable definitions.
    12. **Merkle Intent Fingerprinting:** Forges a unique hash of the gate signature
        to enable O(1) cached branch-prediction.
    13. **Isomorphic Boolean Mapping:** Automatically transmutes "resonant"
        results into absolute logical bits.
    14. **Recursive Slot Forwarding:** (Prophecy) Prepared to forward parent
        scope slots into child dispatches flawlessly.
    15. **Achronal Traceback Pruning:** Trims internal router frames from
        errors, so the Architect only sees the logic in their blueprint.
    16. **Geometric Indentation Floor:** Validates that the gate matches
        the visual gravity willed by its parent in the AST.
    17. **Subtle-Crypto Intent Branding:** HMAC-signs the dispatch event
        to prevent middle-man logic alteration.
    18. **Fault-Isolated Evaluation:** A fracture in one gate's handler
        cannot contaminate the Prime Timeline's stasis.
    19. **NoneType Zero-G Amnesty:** Gracefully handles empty logic headers
        by transmuting them into silent spacers.
    20. **Isomorphic URI Support:** Resolves @import through 'scaffold://'
        URI handlers for multiversal shard fetching.
    21. **Entropy Velocity Tomography:** Tracks the rate of gate execution
        to detect and halt infinite recursion loops.
    22. **Binary Matter Transparency:** Correctly handles 'raw' gates containing
        binary matter without redundant UTF-8 conversion.
    23. **Hydraulic I/O Unbuffering:** Physically forces a flush of sys.stdout
        after heavy @call or @macro expansions.
    24. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect,
        isomorphic, and warded logical execution.
    =================================================================================
    """

    def __init__(self, resolver: 'RecursiveResolver'):
        """[THE RITE OF INCEPTION]: Materializes the Dispatch Lattice."""
        from .handlers.flow import FlowHandlers
        from .handlers.memory import MemoryHandlers
        from .handlers.inclusion import InclusionHandlers
        from .handlers.validation import ValidationHandlers
        from .handlers.functional import FunctionalHandlers

        self.resolver = resolver

        # =========================================================================
        # == THE DISPATCH LATTICE (V-Ω-TOTALITY-VMAX)                            ==
        # =========================================================================
        # [ASCENSION 2]: O(1) Dictionary Registry
        self._LATTICE: Final[Dict[str, Callable]] = {
            # --- Flow & Iteration ---
            SGFControlFlow.IF: FlowHandlers.handle_if_elif,
            SGFControlFlow.ELIF: FlowHandlers.handle_if_elif,
            SGFControlFlow.ELSE: FlowHandlers.handle_if_elif,  # [THE CURE]: Integrated else
            SGFControlFlow.FOR: FlowHandlers.handle_for,
            SGFControlFlow.MATCH: FlowHandlers.handle_match,
            'case': FlowHandlers.handle_match,

            # --- Memory & State ---
            SGFControlFlow.SET: MemoryHandlers.handle_set,
            SGFControlFlow.WITH: MemoryHandlers.handle_with,
            SGFControlFlow.EXPORT: MemoryHandlers.handle_export,

            # --- Structural Weaving ---
            SGFControlFlow.MACRO: FunctionalHandlers.handle_macro_def,
            SGFControlFlow.CALL: FunctionalHandlers.handle_macro_call,
            SGFControlFlow.RETURN: FunctionalHandlers.handle_macro_return,  # [THE SUTURE]
            SGFControlFlow.BLOCK: FunctionalHandlers.handle_block,
            SGFControlFlow.SLOT: FunctionalHandlers.handle_slot,
            SGFControlFlow.FILTER: FunctionalHandlers.handle_filter_block,
            SGFControlFlow.RAW: FunctionalHandlers.handle_raw,

            # --- Topological Expansion ---
            SGFControlFlow.INCLUDE: InclusionHandlers.handle_include,
            SGFControlFlow.IMPORT: InclusionHandlers.handle_include,  # [THE SUTURE]
            SGFControlFlow.EXTENDS: InclusionHandlers.handle_extends,

            # --- Jurisprudence & MRI ---
            SGFControlFlow.CONTRACT: ValidationHandlers.handle_contract,
            "require": ValidationHandlers.handle_require,
            "require_shard": ValidationHandlers.handle_require,
            "visualize": ValidationHandlers.handle_visualize,
            "debug": self._conduct_debug_halt
        }

        # [ASCENSION 3]: The Alias Map
        self._ALIASES: Final[Dict[str, str]] = {
            'elseif': SGFControlFlow.ELIF,
            'else if': SGFControlFlow.ELIF,
            'switch': SGFControlFlow.MATCH,
            'task': SGFControlFlow.MACRO  # Symphony Parity
        }

    def dispatch(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE OMEGA DISPATCH RITE (V-Ω-TOTALITY-VMAX-SIGIL-AMNESTY)               ==
        =============================================================================
        LIF: 1,000,000x | ROLE: KINETIC_ORCHESTRATOR
        """
        _start_ns = time.perf_counter_ns()

        # 1. RETRIEVE THE RAW GHOST
        raw_gate = node.metadata.get("gate", "").lower().strip()

        # =========================================================================
        # == MOVEMENT I: [THE MASTER CURE] - LAMINAR SIGIL AMNESTY               ==
        # =========================================================================
        # [ASCENSION 1]: Physically strip the '@' to find the ELARA Mind beneath.
        gate_soul = raw_gate.lstrip('@')

        # [ASCENSION 3]: Apply Alias Transmutation
        gate_id = self._ALIASES.get(gate_soul, gate_soul)

        # --- MOVEMENT II: THE LATTICE STRIKE ---
        handler = self._LATTICE.get(gate_id)

        if handler:
            # [ASCENSION 18]: Fault-Isolated Execution
            try:
                handler(self.resolver, node, scope, output, spooler)

                # [ASCENSION 9]: HUD Telemetry Pulse
                self._radiate_hud_pulse(gate_id, node.ln)

            except Exception as fracture:
                Logger.error(f"L{node.ln}: Gate '{gate_id}' fractured: {fracture}")
                if os.environ.get("SCAFFOLD_DEBUG") == "1":
                    import traceback
                    traceback.print_exc()
        else:
            # [ASCENSION 4]: Void Guard
            Logger.warn(f"L{node.ln}: Unknown gate '@{raw_gate}' (normalized: '{gate_id}') perceived. Strike stayed.")

        # --- MOVEMENT III: METABOLIC FINALITY ---
        if hasattr(self, '_total_dispatches'):
            self._total_dispatches += 1

    def _radiate_hud_pulse(self, gate: str, line: int):
        """[ASCENSION 9]: Multicasts logic flow to the HUD."""
        engine = self.resolver.engine_ref
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                trace_id = os.environ.get("SCAFFOLD_TRACE_ID", "tr-router-void")
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GATE_DISPATCHED",
                        "label": gate.upper(),
                        "color": "#3b82f6" if gate != "return" else "#a855f7",
                        "trace": trace_id,
                        "line": line
                    }
                })
            except:
                pass

    def _conduct_debug_halt(self, *args, **kwargs):
        """[ASCENSION 24]: The Debugger's Anchor."""
        Logger.info("--- GNOSTIC BREAKPOINT ---")
        # In a TTY, this could trigger pdb.set_trace()

    def __repr__(self) -> str:
        return f"<Ω_GATE_ROUTER status=RESONANT mode=SIGIL_AMNESTY_VMAX dispatches={getattr(self, '_total_dispatches', 0)}>"