# Path: velm/parser_core/logic_weaver/traversal/engine.py
# -------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_TRAVERSAL_VMAX_INTERCEPTOR_HEALED_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# =========================================================================================

import hashlib
import sys
import time
import os
import traceback
import threading
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Final

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from .walker import DimensionalWalker
from .shadow_healer import OntologicalShadowHealer
from ..state import GnosticContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....contracts.symphony_contracts import Edict
from ....core.alchemist import DivineAlchemist
from ....logger import Scribe

# [THE OMEGA SUTURE]: Thread-Local Concurrency Control
from ....codex.loader.proxy import set_active_context, get_active_context

# =========================================================================================
# ==[ASCENSION 15]: THE QUATERNITY TYPE-SUTURE (THE MASTER CURE)                        ==
# =========================================================================================
# Mathematically enshrines the Type Alias at the Zenith of the module, ensuring the
# Python Interpreter's AST binds it globally before the @property decorators evaluate it.
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]

Logger = Scribe("GnosticTraversal")


class TraversalEngine:
    """
    =================================================================================
    == THE ENGINE OF DIMENSIONAL TRAVERSAL: OMEGA (V-Ω-HYPER-DIAGNOSTIC-VMAX)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TRAVERSAL_VMAX_SHADOW_HEALER_2026_FINALIS

    The supreme authority for transmuting the abstract AST into manifest reality.
    This version surgically repairs the Interceptor Schism and integrates the
    Ontological Shadow Healer directly into the timeline, mathematically annihilating
    the "Module vs Directory" paradox before it can touch the disk.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MAX_GNOSTIC_DEPTH: Final[int] = 100
    MAX_SUB_WEAVE_DEPTH: Final[int] = 50

    # [CHROMATIC SIGILS]
    GOLD: Final[str] = "\x1b[38;5;220m"
    UV: Final[str] = "\x1b[38;5;141m"
    ALERT: Final[str] = "\x1b[107;30m"  # INVERSE WHITE
    RESET: Final[str] = "\x1b[0m"

    def __init__(
            self,
            context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: List[Edict],
            parser_post_run: List[Tuple]
    ):
        """[THE RITE OF INCEPTION]"""
        self._init_start_ns = time.perf_counter_ns()
        self.gnostic_context = context
        self.alchemist = alchemist
        self.Logger = Logger

        # Substrate Awareness
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        # [ASCENSION 19]: Bicameral Lock Segregation
        self._traversal_lock = threading.RLock()
        self._thread_local = threading.local()
        self._weave_depth = 0

        # Forge O(1) forensic maps from the parser's linear logs
        edict_map = {e.line_num: e for e in parser_edicts}

        post_run_map = {}
        for cmd_tuple in parser_post_run:
            raw = list(cmd_tuple)
            while len(raw) < 4:
                raw.append(None)
            post_run_map[raw[1]] = tuple(raw[:4])

        # Forge the Spacetime Context (The Shared Memory Lattice)
        self.ctx = SpacetimeContext(context, alchemist, edict_map, post_run_map)

        # Materialize the Dimensional Walker
        self.walker = DimensionalWalker(self.ctx)

        # [THE SCHISM CURE]: Bind the atomic interceptor for SGF constructs
        if hasattr(self.walker, 'set_node_interceptor'):
            self.walker.set_node_interceptor(self._conduct_atomic_flattening)

    def traverse(self, node: _GnosticNode, current_path: Path):
        """
        =============================================================================
        == THE GRAND RITE OF THE KINETIC WALK (TRAVERSE)                           ==
        =============================================================================
        """
        # [ASCENSION 5]: The Thread-Safe Traversal Lock
        with self._traversal_lock:
            if getattr(self._thread_local, 'is_traversing', False):
                self.Logger.warn("Topological Paradox: TraversalEngine is already actively walking on this thread.")
                return
            self._thread_local.is_traversing = True

        _start_ns = time.perf_counter_ns()
        trace_id = self.gnostic_context.raw.get('trace_id', 'tr-void')

        # [ASCENSION 7]: The Silent Guardian Sieve
        if not self.gnostic_context.raw.get('silent'):
            sys.stdout.write(
                f"{self.GOLD}🌀[PANOPTICON] {self.RESET} Initiating Grand Walk for Trace: {self.UV}{trace_id}{self.RESET}\n")
            sys.stdout.flush()

        try:
            # --- MOVEMENT I: PRE-FLIGHT PURIFICATION ---
            if "__woven_matter__" not in self.gnostic_context.raw:
                self.gnostic_context.set("__woven_matter__", [])
            if "__woven_commands__" not in self.gnostic_context.raw:
                self.gnostic_context.set("__woven_commands__", [])

            self._thread_local.spatial_stack = []

            # --- MOVEMENT II: THE DIMENSIONAL WALK ---
            # [ZERO-STICTION STRIKE]: We walk the AST without any time.sleep or GC locks.
            self.walker.walk(node, current_path, self.ctx)

            # --- MOVEMENT III: THE FINAL MATTER SWEEP ---
            self._final_matter_sweep()

            # --- MOVEMENT IV: TOPOLOGICAL PURIFICATION ---
            self._prune_ghost_directories()

            # =====================================================================
            # ==[ASCENSION 1]: THE ONTOLOGICAL SHADOW HEALER (THE MASTER CURE)  ==
            # =====================================================================
            # [ASCENSION 2]: Topological Pre-Purification (Strip None paths)
            pure_items = [i for i in self.ctx.items if i.path is not None]

            # Extract the active project root to calculate absolute intersections
            p_root = self.gnostic_context.project_root if hasattr(self.gnostic_context, 'project_root') else None

            # Invoke the Healer
            healed_items = OntologicalShadowHealer.heal_collisions(pure_items, trace_id, p_root)

            # [ASCENSION 3]: Laminar Buffer Identity Suture
            # We use slice assignment [:] to preserve the physical memory address (id())
            # of `self.ctx.items` so the Parent Engine maintains its reference!
            self.ctx.items[:] = healed_items

            self._seal_merkle_dag()

        except Exception as e:
            # [ASCENSION 6]: Forensic Stderr Snitch (Direct-to-Iron)
            tb = traceback.format_exc()
            sys.stderr.write(f"\n{self.ALERT}💀 CATASTROPHIC TRAVERSAL FRACTURE{self.RESET}\n")
            sys.stderr.write(f"Trace: {trace_id} -> Error: {e}\n{tb}\n")
            sys.stderr.flush()

            self.Logger.critical(f"L{getattr(node.item, 'line_num', 0) if node.item else 0}: Traversal Fracture: {e}")

            # [ASCENSION 24]: The Causal Origin Suture
            self.ctx.heresies.append(Heresy(
                message="TRAVERSAL_FRACTURE",
                details=f"Paradox encountered during walk: {str(e)}\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            ))

        finally:
            with self._traversal_lock:
                self._thread_local.is_traversing = False
                self._thread_local.spatial_stack = []

            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            # [ASCENSION 23]: The Finality Vow
            if not self.gnostic_context.raw.get('silent'):
                sys.stdout.write(
                    f"{self.GOLD}✨ [SINGULARITY]{self.RESET} Walk Concluded. Atoms: {len(self.ctx.items)} | Will: {len(self.ctx.post_run_commands)} | Tax: {_tax_ms:.2f}ms\n")
                sys.stdout.flush()

    def _conduct_atomic_flattening(self, node: _GnosticNode, current_path: Path):
        """
        =============================================================================
        == THE OMEGA ATOMIC FLATTENING (V-Ω-TOTALITY-VMAX-INTERCEPTOR-HEALED)      ==
        =============================================================================[THE MASTER CURE]: This is the true executor of `logic.weave()`. We must
        apply the Retinal Anchor and Laminar Buffer Suture HERE, not in the Walker.
        """
        # --- MOVEMENT 0: SENSORY ADJUDICATION ---
        if not node.item or node.item.line_type != GnosticLineType.SGF_CONSTRUCT:
            return

        expression = node.item.sgf_expression
        if not expression:
            return

        # [ASCENSION 21]: The Null-Byte Sarcophagus
        if '\x00' in expression:
            self.Logger.warn(f"Topological Anomaly: Null-byte detected in SGF expression. Exorcising.")
            expression = expression.replace('\x00', '')

        # [ASCENSION 10]: OUROBOROS DEPTH SENTINEL
        self._weave_depth += 1
        if self._weave_depth > self.MAX_SUB_WEAVE_DEPTH:
            self.Logger.error(
                f"Topological Overflow: `logic.weave` recursion limit reached ({self.MAX_SUB_WEAVE_DEPTH}).")
            self._weave_depth -= 1
            return

        line_num = node.item.line_num

        try:
            # =========================================================================
            # == MOVEMENT I: GEOMETRIC CONTEXT PINNING (THE MASTER CURE)             ==
            # =========================================================================
            # [ASCENSION 9]: The Absolute Path Anchor
            if not isinstance(current_path, Path):
                current_path = Path(current_path)

            posix_path = str(current_path).replace('\\', '/')
            if posix_path in ("", "/", "."):
                posix_path = "."

            # Save previous spatial identities to the thread-local stack
            if not hasattr(self._thread_local, 'spatial_stack'):
                self._thread_local.spatial_stack = []

            previous_file = self.gnostic_context.get("__current_file__", "VOID")
            previous_dir = self.gnostic_context.get("__current_dir__", "VOID")
            self._thread_local.spatial_stack.append((previous_file, previous_dir))

            # Clone the Mind to isolate sub-effects
            local_mind = self.gnostic_context.raw.copy()

            # [STRIKE]: SUTURE THE ANCHORS
            local_mind["__current_file__"] = posix_path
            local_mind["__current_dir__"] = posix_path
            local_mind["__current_column__"] = node.item.original_indent

            # =========================================================================
            # == MOVEMENT II:[THE MASTER CURE] - LAMINAR BUFFER ISOLATION           ==
            # =========================================================================
            with self._traversal_lock:
                # We preserve the original Prime pointers (physical list addresses)
                prime_matter_ref = self.gnostic_context.raw.get("__woven_matter__")
                prime_commands_ref = self.gnostic_context.raw.get("__woven_commands__")

                # [ASCENSION 8]: Recursive Buffer Pruning
                isolated_matter_buffer = []
                isolated_commands_buffer = []

            local_mind["__woven_matter__"] = isolated_matter_buffer
            local_mind["__woven_commands__"] = isolated_commands_buffer

            if self._debug_mode:
                self.Logger.verbose(
                    f"L{line_num:03d}:[ISOLATION] Matter Buffer born at: {hex(id(isolated_matter_buffer))}")

            # Suture the isolated mind to the DomainProxy's thread state.
            previous_thread_ctx = get_active_context()
            set_active_context(local_mind)

            try:
                # =====================================================================
                # == MOVEMENT III: THE ZERO-STICTION STRIKE (NO YIELDS)              ==
                # =====================================================================
                # Execute the Alchemical Transmutation without blocking or sleeping
                self.alchemist.transmute(expression, local_mind)

                # =====================================================================
                # == MOVEMENT IV: RECLAMATION (MANUAL MATTER HARVEST)                ==
                # =====================================================================
                with self._traversal_lock:
                    if isolated_matter_buffer:
                        # Use a copy for iteration to ensure absolute safety
                        matter_snapshot = list(isolated_matter_buffer)
                        self.walker._harvest_woven_matter(matter_snapshot, current_path, line_num, self.ctx)

                    if isolated_commands_buffer:
                        command_snapshot = list(isolated_commands_buffer)
                        for cmd in command_snapshot:
                            raw = list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)]
                            while len(raw) < 4: raw.append(None)
                            cmd_tuple = (raw[0], line_num, raw[2], raw[3])
                            self.ctx.post_run_commands.append(cmd_tuple)

            except Exception as alchemical_paradox:
                self.Logger.error(f"L{line_num}: Construct fracture: {alchemical_paradox}")
                if self._debug_mode:
                    sys.stderr.write(
                        f"\n{self.ALERT}!!! CONSTRUCT FRACTURE !!!{self.RESET}\nL{line_num}: {expression}\n{traceback.format_exc()}\n")
                    sys.stderr.flush()

            finally:
                # =========================================================================
                # == MOVEMENT V: THE GROUNDING (STATE RESTORATION)                       ==
                # =========================================================================
                # Return to original thread context and restore Mind-State
                set_active_context(previous_thread_ctx)

                # Restore the Prime Timeline physical pointers!
                with self._traversal_lock:
                    if 'prime_matter_ref' in locals() and prime_matter_ref is not None:
                        self.gnostic_context.raw["__woven_matter__"] = prime_matter_ref
                    if 'prime_commands_ref' in locals() and prime_commands_ref is not None:
                        self.gnostic_context.raw["__woven_commands__"] = prime_commands_ref

                # [ASCENSION 11]: Idempotent Stack Management
                if getattr(self._thread_local, 'spatial_stack', []):
                    prev_file, prev_dir = self._thread_local.spatial_stack.pop()
                    self.gnostic_context.set("__current_file__", prev_file)
                    self.gnostic_context.set("__current_dir__", prev_dir)

                self._weave_depth -= 1

                # [ASCENSION 17]: Apophatic Memory Release
                if len(isolated_matter_buffer) > 500:
                    import gc
                    gc.collect(1)

        except Exception as catastrophic_paradox:
            self.Logger.critical(f"Interceptor Fracture: {catastrophic_paradox}")

    def _final_matter_sweep(self):
        """
        =============================================================================
        == THE FINAL MATTER SWEEP (V-Ω-ITERATOR-MUTATION-SHIELD)                   ==
        =============================================================================
        Ensures no residual atoms remain in the side-effect buffers.
        """
        with self._traversal_lock:
            try:
                leftovers = self.gnostic_context.raw.get("__woven_matter__")

                if leftovers and isinstance(leftovers, list) and id(leftovers) != id(self.ctx.items) and len(
                        leftovers) > 0:
                    safe_leftovers = list(leftovers)
                    self.walker._harvest_woven_matter(safe_leftovers, Path("."), 0, self.ctx)
                    leftovers.clear()

                leftover_cmds = self.gnostic_context.raw.get("__woven_commands__")
                if leftover_cmds and isinstance(leftover_cmds, list) and id(leftover_cmds) != id(
                        self.ctx.post_run_commands) and len(leftover_cmds) > 0:
                    safe_cmds = list(leftover_cmds)
                    for cmd in safe_cmds:
                        # [ASCENSION 14]: The Ghost-Edict Annihilator
                        if not cmd or not cmd[0]: continue

                        raw = list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)]
                        while len(raw) < 4: raw.append(None)
                        self.ctx.post_run_commands.append(tuple(raw[:4]))
                    leftover_cmds.clear()
            except Exception as e:
                self.Logger.warn(f"Final Matter Sweep deferred: {e}")

    def _prune_ghost_directories(self):
        """
        Bicameral Ghost-Node Pruning.
        Uses O(1) set lookups to eliminate empty implicit directories.
        """
        dir_paths = {str(item.path).replace('\\', '/').lower() for item in self.ctx.items if item.is_dir and item.path}
        file_paths = {str(item.path).replace('\\', '/').lower() for item in self.ctx.items if
                      not item.is_dir and item.path}

        populated_dirs = set()
        for fp in file_paths:
            parts = fp.split('/')
            for i in range(1, len(parts)): populated_dirs.add('/'.join(parts[:i]))

        # [ASCENSION 12]: The "Virtual File" Emancipation
        self.ctx.items = [
            item for item in self.ctx.items
            if not item.is_dir or not item.path or (
                        str(item.path).replace('\\', '/').lower() in populated_dirs) or item.metadata.get('is_virtual',
                                                                                                          False)
        ]

    def _seal_merkle_dag(self):
        """
        [ASCENSION 18]: Merkle-Lattice Finality Sealing.
        Hashes only the materialized paths and contents.
        """
        if not self.ctx.items:
            self.gnostic_context.set("__final_merkle_seal__", "0xVOID")
            return

        hasher = hashlib.sha256()
        for item in sorted(self.ctx.items, key=lambda x: str(x.path)):
            hasher.update(str(item.path).encode('utf-8'))
            if item.content:
                hasher.update(hashlib.md5(item.content.encode('utf-8')).hexdigest().encode('utf-8'))

        seal = hasher.hexdigest()[:16].upper()
        # [ASCENSION 18]: The Merkle DAG State Machine validation
        if len(seal) == 16:
            self.gnostic_context.set("__final_merkle_seal__", f"0x{seal}")
        else:
            self.gnostic_context.set("__final_merkle_seal__", "0xFRACTURE")

    @property
    def items(self) -> List[ScaffoldItem]:
        return self.ctx.items

    @property
    def post_run_commands(self) -> List[Quaternity]:
        return self.ctx.post_run_commands

    @property
    def edicts(self) -> List[Edict]:
        return self.ctx.edicts

    @property
    def heresies(self) -> List[Heresy]:
        return self.ctx.heresies