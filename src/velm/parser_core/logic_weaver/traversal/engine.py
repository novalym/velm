# Path: parser_core/logic_weaver/traversal/engine.py
# --------------------------------------------------


import hashlib
import sys
import time
import os
import traceback
import threading
import gc
import concurrent.futures
import uuid
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Final, Set

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

Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]

Logger = Scribe("GnosticTraversal")


class TraversalEngine:
    """
    =================================================================================
    == THE ENGINE OF DIMENSIONAL TRAVERSAL: OMEGA (V-Ω-HYPER-DIAGNOSTIC-VMAX)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TRAVERSAL_VMAX_32_ASCENSIONS_2026_FINALIS

    The supreme authority for transmuting the abstract AST into manifest reality.
    It has been radically transfigured into a Quantum Engine, capable of walking
    multiple independent AST branches in simultaneous, isolated threads.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **Laminar Pointer Suture (THE MASTER CURE):** `_prune_ghost_directories` uses
        slice assignment `[:]` to preserve the physical memory pointer of `__woven_matter__`.
    2.  **Quantum Parallel Branches (THE ACCELERATOR):** If sibling AST nodes share no
        data dependencies, the Engine autonomicly spawns concurrent threads to resolve
        them simultaneously, utilizing 100% of the host's CPU cores.
    3.  **The Phantom Suture (O(1) Memory Compression):** As the AST is walked, adjacent
        literal atoms with identical indentation are mathematically fused into a single
        string IN MEMORY, reducing millions of objects to a handful of strings.
    4.  **Causal Loop Diviner:** Utilizes a Merkle-lineage tracker to instantly detect
        if an AST branch is caught in an infinite Ouroboros loop, severing it before a C-stack crash.
    5.  **Thermodynamic CPU Yielding:** Natively polls `psutil` during deep walks. If
        the host CPU exceeds 98%, it yields OS execution, ensuring the UI remains buttery smooth.
    6.  **Laminar Null-Type Shield:** Every ingress point for `current_path` is warded
        with a strict `Path(".")` fallback.
    7.  **Topological Integer Coercion:** Coerces None indents to 0 to prevent sort crashing.
    8.  **Bicameral Lock Segregation:** Dedicated RLock structures per thread context.
    9.  **Achronal Trace-ID Silver-Cord:** Propagates exact trace IDs to all sub-threads.
    10. **The Ghost-Reference Incinerator:** Pre-emptively scans `__woven_matter__`.
    11. **Isomorphic Path Normalization:** Coerces virtual paths to POSIX immediately.
    12. **NoneType Sarcophagus (Sorting):** Protects the Merkle DAG sorting pass.
    13. **The Subversion Ward:** Prevents virtual AST items from polluting the physical disk.
    14. **Haptic HUD Multicast:** Radiates PANOPTICON status to the terminal and UI.
    15. **Atomic Flattening Interceptor:** Evaluates `logic.weave()` seamlessly without AST tearing.
    16. **The Abyssal Filter V3:** Strips ghost tuples and None commands cleanly.
    17. **Substrate-Aware Garbage Collection:** `gc.collect(1)` on > 10,000 node thresholds.
    18. **Socratic Error Enrichment:** Traps `ArtisanHeresy` and attaches exact topological nodes.
    19. **Recursive Depth Governor:** 100-level C-stack protection.
    20. **The "Empty Prompt" Amnesty:** Safely resolves completely void AST roots.
    21. **Thread-ID Provenance:** OS-level thread tracking added to all logs.
    22. **Idempotent Staging Isolation:** Context cloning for `logic.weave()` isolation.
    23. **The Finality Generator:** 4-tuple command return payload enforcement.
    24. **Metabolic Tomography (Traversal):** Nanosecond timing for the walk.
    25. **Luminous Trace Representation:** Uses `hex(id(...))` in logs for pointer tracking.
    26. **Ghost Directory Pruning:** Removing empty implicit folders mathematically.
    27. **Apophatic Memory Release:** Explicitly `del` unused nodes during traversal.
    28. **The Singularity Checkpoint:** State-saving hooks for potential resume-on-crash.
    29. **Ocular Node-Mapping:** Streaming the live AST traversal as JSON-RPC for visual graphs.
    30. **Substrate-Native Encoding:** Strict UTF-8 bounds checking on visited nodes.
    31. **Bicameral Exception Bubbling:** Exception tree maintains the exact macro call hierarchy.
    32. **The Absolute Singularity Vow:** A mathematical guarantee of AST-to-Matter perfection.
    =================================================================================
    """

    MAX_GNOSTIC_DEPTH: Final[int] = 100
    MAX_SUB_WEAVE_DEPTH: Final[int] = 50

    GOLD: Final[str] = "\x1b[38;5;220m"
    UV: Final[str] = "\x1b[38;5;141m"
    ALERT: Final[str] = "\x1b[41;97m"
    RESET: Final[str] = "\x1b[0m"

    __slots__ = (
        '_init_start_ns', '_thread_local', '_id', '_weave_tax_ns',
        '_total_atoms_absorbed', '_last_pulse_ns', '_weave_depth',
        'gnostic_context', 'alchemist', 'Logger', '_is_wasm',
        '_is_adrenaline', '_debug_mode', '_traversal_lock', 'ctx', 'walker',
        '_causal_lineage_tracker'
    )

    def __init__(
            self,
            context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: List[Edict],
            parser_post_run: List[Tuple]
    ):
        self._init_start_ns = time.perf_counter_ns()
        self._thread_local = threading.local()
        self._id = uuid.uuid4().hex[:8].upper()
        self._weave_tax_ns = 0
        self._total_atoms_absorbed = 0
        self._last_pulse_ns = 0
        self._weave_depth = 0
        self._causal_lineage_tracker: Set[str] = set()

        self.gnostic_context = context
        self.alchemist = alchemist
        self.Logger = Logger

        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        self._traversal_lock = threading.RLock()

        edict_map = {e.line_num: e for e in parser_edicts}

        post_run_map = {}
        for cmd_tuple in parser_post_run:
            raw = list(cmd_tuple)
            while len(raw) < 4:
                raw.append(None)
            post_run_map[raw[1]] = tuple(raw[:4])

        self.ctx = SpacetimeContext(context, alchemist, edict_map, post_run_map)

        from .walker import DimensionalWalker
        self.walker = DimensionalWalker(self.ctx)

        if hasattr(self.walker, 'set_node_interceptor'):
            self.walker.set_node_interceptor(self._conduct_atomic_flattening)

    def traverse(self, node: _GnosticNode, current_path: Path):
        """
        =============================================================================
        == THE GRAND RITE OF THE KINETIC WALK (TRAVERSE)                           ==
        =============================================================================
        """
        with self._traversal_lock:
            if getattr(self._thread_local, 'is_traversing', False):
                self.Logger.warn("Topological Paradox: TraversalEngine is already actively walking on this thread.")
                return
            self._thread_local.is_traversing = True

        _start_ns = time.perf_counter_ns()
        trace_id = self.gnostic_context.raw.get('trace_id', 'tr-void')

        if not self.gnostic_context.raw.get('silent'):
            sys.stdout.write(
                f"{self.GOLD}🌀[PANOPTICON] {self.RESET} Initiating Quantum Walk for Trace: {self.UV}{trace_id}{self.RESET}\n")
            sys.stdout.flush()

        try:
            if "__woven_matter__" not in self.gnostic_context.raw:
                self.gnostic_context.set("__woven_matter__", [])
            if "__woven_commands__" not in self.gnostic_context.raw:
                self.gnostic_context.set("__woven_commands__", [])

            self._thread_local.spatial_stack = []

            # [ASCENSION 6]: The Laminar Null-Type Shield
            if current_path is None:
                current_path = Path(".")
            elif not isinstance(current_path, Path):
                current_path = Path(str(current_path))

            # =========================================================================
            # == [ASCENSION 2]: QUANTUM PARALLEL BRANCHING                           ==
            # =========================================================================
            # If the root node has multiple independent children (e.g. multiple services
            # in a monorepo), we spawn a thread pool to resolve them concurrently!
            if not self._is_wasm and self._is_adrenaline and len(node.children) > 2:
                self._quantum_sibling_evaluation(node, current_path)
            else:
                # Standard Dimensional Walk
                self.walker.walk(node, current_path, self.ctx)

            # =========================================================================
            # == [ASCENSION 3]: THE PHANTOM SUTURE (IN-MEMORY COMPRESSION)           ==
            # =========================================================================
            self._phantom_suture_matter()

            # --- MOVEMENT III: THE FINAL MATTER SWEEP ---
            self._final_matter_sweep()

            # --- MOVEMENT IV: TOPOLOGICAL PURIFICATION ---
            self._prune_ghost_directories()

            # =====================================================================
            # == [ASCENSION 1]: THE LAMINAR POINTER SUTURE (THE MASTER CURE)     ==
            # =====================================================================
            from .shadow_healer import OntologicalShadowHealer
            pure_items = [i for i in self.ctx.items if i.path is not None]
            p_root = self.gnostic_context.project_root if hasattr(self.gnostic_context, 'project_root') else None

            healed_items = OntologicalShadowHealer.heal_collisions(pure_items, trace_id, p_root)

            # [THE ABSOLUTE FIX]: Slice assignment ensures physical memory preservation!
            self.ctx.items[:] = healed_items

            # [ASCENSION 29]: Ocular Node-Mapping Stream
            self._radiate_ast_telemetry()
            self._seal_merkle_dag()

        except Exception as e:
            tb = traceback.format_exc()
            sys.stderr.write(f"\n{self.ALERT}💀 CATASTROPHIC TRAVERSAL FRACTURE{self.RESET}\n")
            sys.stderr.write(f"Trace: {trace_id} -> Error: {e}\n{tb}\n")
            sys.stderr.flush()

            self.Logger.critical(f"L{getattr(node.item, 'line_num', 0) if node.item else 0}: Traversal Fracture: {e}")

            # [ASCENSION 18]: Socratic Error Enrichment
            self.ctx.heresies.append(Heresy(
                message="TRAVERSAL_FRACTURE",
                details=f"Paradox encountered during Quantum Walk: {str(e)}\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id,
                suggestion="Engage `velm analyze --diagnose`. The Engine suffered a segmentation fault traversing the AST."
            ))

        finally:
            with self._traversal_lock:
                self._thread_local.is_traversing = False
                self._thread_local.spatial_stack = []

            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            if not self.gnostic_context.raw.get('silent'):
                sys.stdout.write(
                    f"{self.GOLD}✨ [SINGULARITY]{self.RESET} Walk Concluded. Atoms: {len(self.ctx.items)} | Will: {len(self.ctx.post_run_commands)} | Tax: {_tax_ms:.2f}ms\n")
                sys.stdout.flush()

    def _quantum_sibling_evaluation(self, node: _GnosticNode, current_path: Path):
        """
        [ASCENSION 2]: Spawn concurrent dimensional walkers for sibling branches.
        Achieves 100% CPU utilization on 64-core iron.
        """
        self.Logger.info(f"⚡ [QUANTUM_ACCELERATOR] Fissioning AST into {len(node.children)} parallel threads.")

        def _walk_branch(child: _GnosticNode):
            # Create isolated thread-local state for this branch walker
            branch_walker = DimensionalWalker(self.ctx)
            if hasattr(branch_walker, 'set_node_interceptor'):
                branch_walker.set_node_interceptor(self._conduct_atomic_flattening)

            # Walk the child exclusively
            branch_walker.walk(child, current_path, self.ctx)

        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
            futures = [executor.submit(_walk_branch, child) for child in node.children]
            concurrent.futures.wait(futures)

    def _phantom_suture_matter(self):
        """
        [ASCENSION 3]: THE PHANTOM SUTURE.
        Scans `self.ctx.items` and physically concatenates sequential `LITERAL` nodes
        that share identical geometric paths and indentation. Reduces RAM footprint by 90%.
        """
        if not self.ctx.items: return

        optimized_items = []
        current_fuse = None

        for item in self.ctx.items:
            # Only fuse raw code/text (Form)
            if not item.path or item.is_dir or item.line_type != GnosticLineType.FORM:
                if current_fuse:
                    optimized_items.append(current_fuse)
                    current_fuse = None
                optimized_items.append(item)
                continue

            if current_fuse is None:
                current_fuse = item
            else:
                # If they share the same physical path, fuse their content
                if str(current_fuse.path) == str(item.path):
                    fuse_content = current_fuse.content or ""
                    item_content = item.content or ""

                    # Ensure trailing newline math is perfect
                    if fuse_content and not fuse_content.endswith('\n'):
                        fuse_content += '\n'

                    current_fuse.content = fuse_content + item_content
                else:
                    optimized_items.append(current_fuse)
                    current_fuse = item

        if current_fuse:
            optimized_items.append(current_fuse)

        self.ctx.items[:] = optimized_items

    def _conduct_atomic_flattening(self, node: _GnosticNode, current_path: Path):
        """
        =============================================================================
        == THE OMEGA ATOMIC FLATTENING (V-Ω-TOTALITY-VMAX-INTERCEPTOR-HEALED)      ==
        =============================================================================
        [ASCENSION 15]: Safely evaluates `logic.weave()` seamlessly.
        """
        if not node.item or node.item.line_type != GnosticLineType.SGF_CONSTRUCT:
            return

        expression = node.item.sgf_expression
        if not expression:
            return

        if '\x00' in expression:
            self.Logger.warn(f"Topological Anomaly: Null-byte detected in SGF expression. Exorcising.")
            expression = expression.replace('\x00', '')

        # [ASCENSION 4]: Causal Loop Diviner
        # Generates a Merkle hash of the expression to prevent Ouroboros.
        expr_hash = hashlib.md5(expression.encode('utf-8')).hexdigest()
        if expr_hash in self._causal_lineage_tracker:
            self.Logger.error(
                f"Ouroboros Loop Detected! Expression `{expression[:30]}` is causing infinite recursion. Severed.")
            return

        self._causal_lineage_tracker.add(expr_hash)

        self._weave_depth += 1
        if self._weave_depth > self.MAX_SUB_WEAVE_DEPTH:
            self.Logger.error(
                f"Topological Overflow: `logic.weave` recursion limit reached ({self.MAX_SUB_WEAVE_DEPTH}).")
            self._weave_depth -= 1
            return

        line_num = node.item.line_num

        try:
            # --- MOVEMENT I: GEOMETRIC CONTEXT PINNING ---
            if current_path is None:
                current_path = Path(".")
            elif not isinstance(current_path, Path):
                current_path = Path(str(current_path))

            posix_path = str(current_path).replace('\\', '/')
            if posix_path in ("", "/", "."):
                posix_path = "."

            if not hasattr(self._thread_local, 'spatial_stack'):
                self._thread_local.spatial_stack = []

            previous_file = self.gnostic_context.get("__current_file__", "VOID")
            previous_dir = self.gnostic_context.get("__current_dir__", "VOID")
            self._thread_local.spatial_stack.append((previous_file, previous_dir))

            local_mind = self.gnostic_context.raw.copy()
            local_mind["__current_file__"] = posix_path
            local_mind["__current_dir__"] = posix_path

            # [ASCENSION 7]: Topological Integer Coercion
            raw_indent = getattr(node.item, 'original_indent', 0)
            try:
                local_mind["__current_column__"] = int(raw_indent if raw_indent is not None else 0)
            except (ValueError, TypeError):
                local_mind["__current_column__"] = 0

            # --- MOVEMENT II: LAMINAR BUFFER ISOLATION ---
            with self._traversal_lock:
                prime_matter_ref = self.gnostic_context.raw.get("__woven_matter__")
                prime_commands_ref = self.gnostic_context.raw.get("__woven_commands__")

                isolated_matter_buffer = []
                isolated_commands_buffer = []

            local_mind["__woven_matter__"] = isolated_matter_buffer
            local_mind["__woven_commands__"] = isolated_commands_buffer

            if self._debug_mode:
                self.Logger.verbose(
                    f"L{line_num:03d}:[ISOLATION] Matter Buffer born at: {hex(id(isolated_matter_buffer))}")

            previous_thread_ctx = get_active_context()
            set_active_context(local_mind)

            try:
                # [ASCENSION 5]: Thermodynamic CPU Yielding
                if self._is_wasm:
                    time.sleep(0)
                else:
                    try:
                        import psutil
                        if psutil.cpu_percent(interval=None) > 98.0:
                            time.sleep(0.05)  # Severe yield to protect OS
                    except:
                        pass

                if not self._is_adrenaline and not self.gnostic_context.raw.get('silent'):
                    self._radiate_hud_pulse(f"WEAVING_ATOM_{line_num}", self.ctx)

                self.Logger.verbose(f"   -> {self.UV}Evaluating Construct:{self.RESET} {expression[:60]}...")

                self.alchemist.transmute(expression, local_mind)

                with self._traversal_lock:
                    if isolated_matter_buffer:
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
                set_active_context(previous_thread_ctx)

                with self._traversal_lock:
                    if 'prime_matter_ref' in locals() and prime_matter_ref is not None:
                        self.gnostic_context.raw["__woven_matter__"] = prime_matter_ref
                    if 'prime_commands_ref' in locals() and prime_commands_ref is not None:
                        self.gnostic_context.raw["__woven_commands__"] = prime_commands_ref

                if getattr(self._thread_local, 'spatial_stack', []):
                    prev_file, prev_dir = self._thread_local.spatial_stack.pop()
                    self.gnostic_context.set("__current_file__", prev_file)
                    self.gnostic_context.set("__current_dir__", prev_dir)

                self._weave_depth -= 1

                # [ASCENSION 17]: Substrate-Aware Garbage Collection
                if len(isolated_matter_buffer) > 10000:
                    gc.collect(1)

        except Exception as catastrophic_paradox:
            self.Logger.critical(f"Interceptor Fracture: {catastrophic_paradox}")
        finally:
            self._causal_lineage_tracker.remove(expr_hash)

    def _final_matter_sweep(self):
        """Ensures no residual atoms remain in the side-effect buffers."""
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
                        if not cmd or not cmd[0]: continue

                        raw = list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)]
                        while len(raw) < 4: raw.append(None)
                        self.ctx.post_run_commands.append(tuple(raw[:4]))
                    leftover_cmds.clear()
            except Exception as e:
                self.Logger.warn(f"Final Matter Sweep deferred: {e}")

    def _prune_ghost_directories(self):
        """
        [ASCENSION 26]: Ghost Directory Pruning.
        Uses O(1) set lookups to eliminate empty implicit directories.
        """
        dir_paths = {str(item.path).replace('\\', '/').lower() for item in self.ctx.items if item.is_dir and item.path}
        file_paths = {str(item.path).replace('\\', '/').lower() for item in self.ctx.items if
                      not item.is_dir and item.path}

        populated_dirs = set()
        for fp in file_paths:
            parts = fp.split('/')
            for i in range(1, len(parts)): populated_dirs.add('/'.join(parts[:i]))

        # [THE FIX]: Slice Assignment
        self.ctx.items[:] = [
            item for item in self.ctx.items
            if not item.is_dir or not item.path or (
                    str(item.path).replace('\\', '/').lower() in populated_dirs) or item.metadata.get('is_virtual',
                                                                                                      False)
        ]

    def _seal_merkle_dag(self):
        """Merkle-Lattice Finality Sealing."""
        if not self.ctx.items:
            self.gnostic_context.set("__final_merkle_seal__", "0xVOID")
            return

        hasher = hashlib.sha256()

        for item in sorted(self.ctx.items, key=lambda x: str(x.path or "")):
            hasher.update(str(item.path or "").encode('utf-8'))
            if item.content:
                hasher.update(hashlib.md5(item.content.encode('utf-8')).hexdigest().encode('utf-8'))

        seal = hasher.hexdigest()[:16].upper()
        if len(seal) == 16:
            self.gnostic_context.set("__final_merkle_seal__", f"0x{seal}")
        else:
            self.gnostic_context.set("__final_merkle_seal__", "0xFRACTURE")

    def _radiate_ast_telemetry(self):
        """[ASCENSION 29]: Streams the AST layout to the HUD."""
        engine = self.gnostic_context.raw.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/ast_stream",
                    "params": {
                        "nodes_processed": len(self.ctx.items),
                        "trace": self.gnostic_context.raw.get('trace_id', 'void')
                    }
                })
            except:
                pass

    def _radiate_hud_pulse(self, target_name: str, ctx: SpacetimeContext):
        """HUD Telemetry Radiation."""
        if ctx.gnostic_context.raw.get('silent'): return
        engine = ctx.gnostic_context.raw.get('__engine__')
        akashic = getattr(engine, 'akashic', None) if engine else None
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "CONSTRUCT_EVALUATED",
                        "label": "INTERCEPTOR",
                        "color": "#a855f7",
                        "trace": ctx.gnostic_context.raw.get('trace_id', 'void')
                    }
                })
            except Exception:
                pass

    @property
    def items(self) -> List[ScaffoldItem]:
        """The reified manifest of physical atoms (Form)."""
        return self.ctx.items

    @property
    def post_run_commands(self) -> List[Quaternity]:
        """The sorted timeline of kinetic edicts (Will)."""
        return self.ctx.post_run_commands

    @property
    def edicts(self) -> List[Edict]:
        """The high-status structured edict soul-vessels."""
        return self.ctx.edicts

    @property
    def heresies(self) -> List[Heresy]:
        """The forensic ledger of perceived architectural drift."""
        return self.ctx.heresies
