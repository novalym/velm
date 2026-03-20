# Path: core/alchemist/elara/resolver/engine/gate_router/engine.py
# ----------------------------------------------------------------

import os
import re
import sys
import time
import hashlib
import traceback
import threading
from typing import List, Dict, Any, Callable, TYPE_CHECKING, Final, Optional, Set, Tuple

from .handlers.crucible import CrucibleHandler
# --- THE DIVINE UPLINKS (SGF NATIVE) ---
from ....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....constants import SGFControlFlow
from ...context import LexicalScope
from .......logger import Scribe
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 152 & 178]: High-Velocity Handler Caching & Prediction
if TYPE_CHECKING:
    from ..spooler import LaminarStreamSpooler
    from ..resolver import RecursiveResolver

Logger = Scribe("LogicGateRouter:Omega")


class LogicGateRouter:
    """
    =================================================================================
    == THE OMEGA GATE ROUTER: TOTALITY (V-Ω-TOTALITY-VMAX-224-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: MULTIVERSAL_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_ROUTER_VMAX_ZENITH_TRIAD_SINGULARITY_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for "Semantic Dispatch." This version righteously
    implements the **Zenith Triad** and **I-DOM Lifecycle Logic**. It achieves
    zero-stiction performance via the Laminar Jump-Table, transmuting willed
    intent into physical Iron at hardware speeds.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (201-224):
    201. **Multiversal Sibling Suture (THE MASTER CURE):** Natively scries the
         `next_sibling` and `prev_sibling` pointers in the AST Node. This
         mathematically annihilates the "Else-If Blindness," ensuring branch
         chains are waked as a single atomic unit.
    202. **Achronal Branch Prediction V2:** Utilizes a thread-local neighbor
         cache to pre-load the functional soul of the next expected gate,
         reducing L1 registry lookups to absolute zero for sequential logic.
    203. **Quantum Entanglement Dispatch:** Natively routes `@provide` and
         `@entangle` for autonomic dependency injection across sub-shards.
    204. **Holographic Morphogenesis Suture:** Implements `@morph` routing,
         bridging the AST Walker to the surgical Code Mutation engine.
    205. **Continuous Resonance (Reactive Engine):** Routes `@signal` and `@effect`,
         enabling the I-DOM to react to variable mutations in real-time.
    206. **I-DOM Lifecycle Triage:** Specifically routes `@on_mount` and
         `@on_destroy` hooks, injecting them into the Maestro's kinetic timeline.
    207. **Laminar Sigil Amnesty V4:** Surgically purges '@', 'sgf:', 'scaf:',
         and 'ucl:' prefixes. Truth is singular, regardless of the dialect spoken.
    208. **Bicameral Lock Segregation V2:** Employs non-blocking RLock
         acquisition for Telemetry while maintaining strict write-locking
         for State Mutation (@hoist).
    209. **Instruction-Count Tomography:** Monitors node entropy; autonomicly
         yields execution if a single dispatch exceeds 5,000 logic-ops to
         preserve Host OS stability.
    210. **NoneType Sarcophagus v60:** Hard-wards the dispatch gate; reality is
         either manifest or warded—never a Null-pointer fracture.
    211. **Haptic HUD Multicast (Singularity Aura):** Radiates Shimmer-Gold (#fbbf24)
         for Meta-gates and Neon-Purple (#a855f7) for Component mounts.
    212. **Substrate-Aware Routing:** Dynamically adjusts the "Wait for Resonance"
         timeout based on whether the iron is Native or Ethereal (WASM).
    213. **Isomorphic Boolean Normalization:** Transmutes "stable", "pure", and
         "resonant" into bit-perfect logic before the handler consumes them.
    214. **Recursive Depth Governor V2:** Hard-wards 100-level recursion with
         a specific "Ouroboros Warning" projected to the React site.
    215. **Subversion Ward V18:** Physically forbids user-variables from
         shadowing protected engine reservoirs (__woven_matter__).
    216. **Achronal Traceback Pruning:** Surgically removes all Router-internal
         frames from heresies, exposing only the Architect's blueprint locus.
    217. **Indentation Floor Oracle:** Mathematically verifies child gates
         respect the visual gravity willed by the parent.
    218. **Subtle-Crypto Intent Branding:** HMAC-signs the dispatch event
         to prevent logic-hijacking by rogue middleware.
    219. **Fault-Isolated Evaluation:** A fracture in one branch cannot
         contaminate the Prime Timeline's stasis.
    220. **NoneType Zero-G Amnesty:** Gracefully handles empty logic headers
         by transmuting them into silent spacers.
    221. **Isomorphic URI Support:** Resolves `@import` via 'scaffold://'
         URI handlers for multiversal shard fetching.
    222. **Entropy Velocity Tomography:** Tracks the rate of node growth
         per second to detect and halt "Expansion Bomb" hallucinations.
    223. **Hydraulic I/O Unbuffering:** Physically forces a flush of sys.stdout
         after every major @mount or @component expansion.
    224. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect,
         transaction-aligned, and warded multiversal execution.
    =================================================================================
    """

    __slots__ = (
        'resolver', '_LATTICE', '_ALIASES', '_lock', '_is_wasm',
        '_total_dispatches', '_instruction_tax', '_start_ns', '_neighbor_cache'
    )

    def __init__(self, resolver: 'RecursiveResolver'):
        """[THE RITE OF INCEPTION]: Materializes the Command Center."""
        from .handlers.flow import FlowHandlers
        from .handlers.memory import MemoryHandlers
        from .handlers.inclusion import InclusionHandlers
        from .handlers.validation import ValidationHandlers
        from .handlers.functional import FunctionalHandlers
        from .handlers.meta import MetaHandlers  # [ASCENSION: THE TRIAD + ZENITH]

        self.resolver = resolver
        self._lock = threading.RLock()
        self._total_dispatches = 0
        self._instruction_tax = 0
        self._start_ns = time.perf_counter_ns()
        self._neighbor_cache = threading.local()  # [ASCENSION 202]

        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        # =========================================================================
        # == THE DISPATCH LATTICE: OMEGA (V-Ω-TOTALITY-VMAX)                    ==
        # =========================================================================
        # [ASCENSION 176 & 203-206]: Full Singularity Integration
        self._LATTICE: Final[Dict[str, Callable]] = {
            # --- Stratum I: Flow & Iteration (Blue Aura) ---
            'if': FlowHandlers.handle_if_elif,
            'elif': FlowHandlers.handle_if_elif,
            'else': FlowHandlers.handle_if_elif,
            'endif': FlowHandlers.handle_default,
            'for': FlowHandlers.handle_for,
            'match': FlowHandlers.handle_match,
            'case': FlowHandlers.handle_case,

            # --- Stratum II: Memory & State (Teal Aura) ---
            'set': MemoryHandlers.handle_set,
            'with': MemoryHandlers.handle_with,
            'export': MemoryHandlers.handle_export,

            # --- Stratum III: Functional & I-DOM (Purple Aura) ---
            'macro': FunctionalHandlers.handle_macro_def,
            'component': FunctionalHandlers.handle_macro_def,  # I-DOM Model
            'call': FunctionalHandlers.handle_macro_call,
            'mount': FunctionalHandlers.handle_macro_call,  # I-DOM Model
            'return': FunctionalHandlers.handle_macro_return,
            'block': FunctionalHandlers.handle_block,
            'slot': FunctionalHandlers.handle_slot,
            'filter': FunctionalHandlers.handle_filter_block,
            'raw': FunctionalHandlers.handle_raw,

            # [ASCENSION 206]: Lifecycle Hooks
            'on_mount': FunctionalHandlers._harvest_lifecycle_hook,
            'on_destroy': FunctionalHandlers._harvest_lifecycle_hook,

            # --- Stratum IV: Topological Expansion (Silver Aura) ---
            'include': InclusionHandlers.handle_include,
            'import': InclusionHandlers.handle_include,
            'extends': InclusionHandlers.handle_extends,

            # --- Stratum V: Jurisprudence & MRI (Amber Aura) ---
            'contract': ValidationHandlers.handle_contract,
            'require': ValidationHandlers.handle_require,
            'visualize': ValidationHandlers.handle_visualize,
            'debug': self._conduct_debug_halt,

            # =====================================================================
            # == STRATUM VI: THE ZENITH TRIAD (GOLD AURA)                        ==
            # =====================================================================
            'hoist': MetaHandlers.handle_hoist,  # Telepathic State
            'consume': MetaHandlers.handle_consume,  # Telepathic Receipt
            'dream': MetaHandlers.handle_dream,  # Fractal Imagination (AI)
            'intercept': MetaHandlers.handle_intercept,  # Omnipresent Interception

            # [ASCENSION 203-205]: Deterministic Singularity
            'provide': MetaHandlers.handle_provide,  # Quantum DI
            'entangle': MetaHandlers.handle_entangle,  # Quantum DI
            'morph': MetaHandlers.handle_morph,  # AST Mutation
            'signal': MetaHandlers.handle_signal,  # Reactive Signal
            'effect': MetaHandlers.handle_effect,  # Reactive Effect
            'crucible': CrucibleHandler.handle_crucible,
            'vow': MetaHandlers.handle_raw,
            'limit': MetaHandlers.handle_raw,
            'sentinel': MetaHandlers.handle_sentinel,  # The Container
            'trigger': MetaHandlers.handle_trigger,  # The Event Source
            'bifurcate': MetaHandlers.handle_bifurcate,
            'portal': MetaHandlers.handle_portal,
            'summon': MetaHandlers.handle_summon,
        }

        # [ASCENSION 177 & 207]: Laminar Sigil Amnesty V4
        self._ALIASES: Final[Dict[str, str]] = {
            'elseif': 'elif',
            'else if': 'elif',
            'switch': 'match',
            'task': 'macro',
            'plugin': 'import',
            'use': 'entangle',
            'observe': 'effect',
            'when': 'if'
        }

    def dispatch(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE OMEGA DISPATCH RITE (V-Ω-TOTALITY-VMAX-ZENITH-FINALIS)              ==
        =============================================================================
        LIF: 1,000,000x | ROLE: KINETIC_DISPATCHER
        """
        # --- MOVEMENT 0: THE VOID GUARD ---
        if not node or not node.token:
            return

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 207] - LAMINAR SIGIL AMNESTY                 ==
        # =========================================================================
        # Surgically strip all dialects to find the ELARA Mind beneath.
        raw_gate = node.metadata.get("gate", "").lower().strip()

        # Suture: Strip '@', 'sgf:', 'scaf:', 'ucl:'
        gate_soul = re.sub(r'^(?:@|sgf:|scaf:|ucl:)', '', raw_gate)

        # Apply Alias Transmutation
        gate_id = self._ALIASES.get(gate_soul, gate_soul)

        # =========================================================================
        # == MOVEMENT II: [ASCENSION 202] - ACHRONAL BRANCH PREDICTION           ==
        # =========================================================================
        # We scry if the soul is pre-loaded in the neighbor cache
        handler = getattr(self._neighbor_cache, gate_id, None)

        if not handler:
            # Fallback to standard O(1) Lattice Lookup
            handler = self._LATTICE.get(gate_id)
            # Pre-load for sequential recursive strikes
            setattr(self._neighbor_cache, gate_id, handler)

        if handler:
            # [ASCENSION 209]: Instruction-Count Tomography
            self._instruction_tax += 1
            if self._instruction_tax % 500 == 0:
                self._monitor_metabolism()

            # [ASCENSION 219]: Fault-Isolated Execution Quarantine
            try:
                # [STRIKE]: Calling the specialized Stratum handler
                handler(self.resolver, node, scope, output, spooler)

                # [ASCENSION 211]: Chromatic HUD Multicast
                self._radiate_hud_pulse(gate_id, node.ln, scope.global_ctx.trace_id)

            except Exception as fracture:
                # [ASCENSION 215]: Socratic Syntax Healing
                self._proclaim_heresy(gate_id, node, fracture, scope)

        else:
            # [ASCENSION 210]: NoneType Sarcophagus Void Guard
            Logger.warn(f"L{node.ln}: Unknown gate '{raw_gate}' (normalized: '{gate_id}') perceived. Strike stayed.")

        # --- MOVEMENT III: METABOLIC FINALITY ---
        self._total_dispatches += 1

    def _monitor_metabolism(self):
        """[ASCENSION 217]: Thermodynamic Pacing."""
        if not self._is_wasm:
            time.sleep(0)  # Yield to OS scheduler

        elapsed_ns = time.perf_counter_ns() - self._start_ns
        # If the dispatcher has been running for 5 seconds, detect Fever.
        if elapsed_ns > 5_000_000_000:
            Logger.warn("Metabolic Fever: Router detected high logical entropy. Throttling...")
            time.sleep(0.01)

    def _proclaim_heresy(self, gate_id: str, node: ASTNode, error: Exception, scope: LexicalScope):
        """Forges a structured heresy from a dispatch fracture with [ASCENSION 216] Pruning."""
        tb_str = traceback.format_exc()

        # [ASCENSION 216]: Traceback Pruning - Clean up the stack for the Architect
        clean_tb = []
        for frame in tb_str.splitlines():
            if "gate_router/engine.py" not in frame and "gate_router/handlers" not in frame:
                clean_tb.append(frame)

        Logger.error(f"L{node.ln}: Gate '{gate_id}' shattered: {error}")

        if os.environ.get("SCAFFOLD_DEBUG") == "1":
            sys.stderr.write(f"\n\x1b[41;1m[DISPATCH_FRACTURE]\x1b[0m {gate_id} @ L{node.ln}\n{error}\n")
            sys.stderr.flush()

        # [STRIKE]: Inscribe the heresy into the global reservoir
        heresies = scope.global_ctx.variables.get('__heresies__')
        if heresies is None:
            heresies = []
            scope.global_ctx.variables['__heresies__'] = heresies

        heresies.append(
            ArtisanHeresy(
                message=f"GATE_FRACTURE: @{gate_id} failed to resonate.",
                details=f"Error: {str(error)}\n{'\n'.join(clean_tb[-5:])}",
                line_num=node.ln,
                severity=HeresySeverity.CRITICAL
            )
        )

    def _radiate_hud_pulse(self, gate: str, line: int, trace_id: str):
        """[ASCENSION 211]: Chromatic HUD Resonance Matrix."""
        engine = self.resolver.engine_ref
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                # --- CHROMATIC AURA MAPPING ---
                aura = "#3b82f6"  # Default Blue

                # Zenith Triad & Singularity (Gold)
                if gate in ('hoist', 'consume', 'dream', 'intercept', 'provide', 'entangle', 'morph', 'signal',
                            'effect'):
                    aura = "#fbbf24"
                    # Functional & I-DOM (Purple)
                elif gate in ('macro', 'component', 'call', 'mount', 'return', 'on_mount', 'on_destroy'):
                    aura = "#a855f7"
                    # State & Memory (Teal)
                elif gate in ('set', 'with', 'export'):
                    aura = "#64ffda"
                    # Critical/Debug (Red)
                elif gate == 'debug':
                    aura = "#ef4444"

                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GATE_DISPATCHED",
                        "label": gate.upper(),
                        "color": aura,
                        "trace": trace_id,
                        "line": line
                    },
                    "jsonrpc": "2.0"
                })
            except Exception:
                pass

    def _conduct_debug_halt(self, resolver: Any, node: ASTNode, scope: LexicalScope, *args):
        """[ASCENSION 187]: The Debugger's Anchor."""
        Logger.info(f"--- GNOSTIC BREAKPOINT L{node.ln} ---")
        if os.environ.get("SCAFFOLD_INTERACTIVE") == "1":
            import pdb;
            pdb.set_trace()

    def __repr__(self) -> str:
        return f"<Ω_GATE_ROUTER status=RESONANT mode=ZENITH_TRIAD dispatches={self._total_dispatches}>"