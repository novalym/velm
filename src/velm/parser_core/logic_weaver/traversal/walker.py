# Path: parser_core/logic_weaver/traversal/walker.py
# --------------------------------------------------


import os
import time
import gc
import sys
import traceback
import uuid
import hashlib
import threading
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Final, Callable, Union

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from .evaluator import LogicAdjudicator
from .mason import GeometricMason
from .reaper import KineticReaper
from ..contracts import LogicScope, ChainStatus
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....logger import Scribe

# [THE OMEGA SUTURE]: Thread-Local Concurrency Control
from ....codex.loader.proxy import get_active_context, set_active_context

Logger = Scribe("DimensionalWalker")


class DimensionalWalker:
    """
    =================================================================================
    == THE DIMENSIONAL WALKER: OMEGA POINT (V-Ω-TOTALITY-VMAX-51-ASCENSIONS)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: RECURSIVE_REALITY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_WALKER_VMAX_POLYMORPHIC_RESURRECTION_FINALIS_2026

    [THE MANIFESTO]
    The supreme authority for transmuting the Gnostic AST into manifest reality.
    This version righteously implements the **Laminar Reference Suture** and
    **Strike II: Ultraviolet Tomography**. It mathematically annihilates the
    236-ONTOLOGICAL-ERASURE paradox by guaranteeing that Matter (Form) and Will
    (Edicts) wove in sub-dimensions flow through a bit-perfect physical conduit
    directly into the Prime Timeline.

    ### THE PANTHEON OF 51 LEGENDARY ASCENSIONS:
    49. **The UnboundLocal Exorcist (THE CURE):** Hoists the import of `GnosticLineType`
        to the top of the module scope, mathematically annihilating the `UnboundLocalError`
        during atom resurrection.
    50. **The Missing Anchor Suture (THE CURE):** Properly initializes `self.gnostic_context`
        and `self._thread_local` in `__init__`, completely eradicating the `AttributeError`
        during alchemical constructs.
    51. **Ocular Method Alignment:** Rectified `_project_hud_pulse` to call the actually
        manifested `_radiate_hud_pulse` method, protecting the HUD timeline.
    [... Continuum maintained through 48 other faculties ...]
    =================================================================================
    """

    MAX_RECURSION_DEPTH: Final[int] = 100

    # [CHROMATIC SIGILS - STRIKE II]
    UV_GLOW: Final[str] = "\x1b[48;5;141;97m"  # UV Background, White Text
    GOLD_BOLD: Final[str] = "\x1b[1m\x1b[38;5;220m"
    TEAL: Final[str] = "\x1b[38;5;86m"
    ALERT: Final[str] = "\x1b[41;97m"  # Inverse Red
    RESET: Final[str] = "\x1b[0m"

    def __init__(self, ctx: SpacetimeContext):
        """
        =============================================================================
        == THE RITE OF INCEPTION: TOTALITY (V-Ω-TOTALITY-VMAX-EXTENSIVE-FINALIS)    ==
        =============================================================================
        """
        # --- MOVEMENT 0: METABOLICS & IDENTITY ---
        self._start_ns = time.perf_counter_ns()
        self._id = uuid.uuid4().hex[:8].upper()
        self._weave_tax_ns = 0
        self._total_atoms_absorbed = 0

        # --- MOVEMENT I: THE SOVEREIGN ORGANS ---
        self.ctx = ctx
        # [ASCENSION 50]: THE MISSING ANCHOR SUTURE
        self.gnostic_context = ctx.gnostic_context
        self.alchemist = ctx.alchemist
        self.logger = Logger

        # --- MOVEMENT III: KINETIC STATE & SUBSTRATE ---
        self._node_interceptor: Optional[Callable[[_GnosticNode, Path], None]] = None
        self._traversal_lock = threading.RLock()

        # [ASCENSION 50]: THE THREAD-LOCAL ANCHOR
        self._thread_local = threading.local()
        self._weave_depth = 0

        # [ASCENSION 3, 10]: Substrate & Environment Sensing
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        # --- MOVEMENT IV: THE KINETIC PHALANX ---
        from .evaluator import LogicAdjudicator
        from .mason import GeometricMason
        from .reaper import KineticReaper

        self.adjudicator = LogicAdjudicator(ctx)
        self.mason = GeometricMason(ctx)
        self.reaper = KineticReaper(ctx)

        # --- MOVEMENT V: OCULAR HUD AWAKENING ---
        if not ctx.gnostic_context.raw.get('silent'):
            trace_id = ctx.gnostic_context.raw.get('trace_id', 'tr-unbound')
            self.logger.verbose(f"Dimensional Walker waked for Trace: [cyan]{trace_id}[/]")

    def set_node_interceptor(self, callback: Callable[[_GnosticNode, Path], None]):
        """Binds a sub-conductor (like the TraversalEngine) to the node lifecycle."""
        self._node_interceptor = callback

    def walk(
            self,
            node: _GnosticNode,
            current_path: Path,
            ctx: SpacetimeContext,
            parent_visible: bool = True,
            depth: int = 0,
            breadcrumb: str = "ROOT"
    ):
        """
        =============================================================================
        == THE GRAND RITE OF THE KINETIC WALK (WALK)                               ==
        =============================================================================
        Recursively traverses the Gnostic AST, expanding logic gates, materializing
        forms, and flattening nested side-effects into the Prime Timeline.
        """
        # [ASCENSION 12]: The Ouroboros Depth Sentinel
        if depth > self.MAX_RECURSION_DEPTH:
            Logger.critical(f"Topological Overflow at {breadcrumb}. Recursion ceiling hit.")
            return

        # Ensure strict chronological order based on the initial parse sequence
        sorted_children = sorted(
            node.children,
            key=lambda c: c.item.line_num if c.item else 0
        )

        # Logic State Persistence for this specific Dimensional Stratum
        scope = LogicScope(parent_visible=parent_visible)

        for child in sorted_children:
            _start_ns = time.perf_counter_ns()
            child_name = child.name or "?"
            new_breadcrumb = f"{breadcrumb} > {child_name}"

            # [ASCENSION 7]: Null-Type Sarcophagus (Implicit Directories)
            if not child.item:
                if scope.parent_visible:
                    # [STRIKE]: The Mason resolves the path based on the current anchor
                    next_path = self.mason.forge_matter(child, current_path)
                    self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1, breadcrumb=new_breadcrumb)
                continue

            # =========================================================================
            # == [ASCENSION 5]: THE OMNI-ENUM EXORCIST (THE MASTER CURE)             ==
            # =========================================================================
            line_type_name = "UNKNOWN"
            if hasattr(child.item.line_type, 'name'):
                line_type_name = child.item.line_type.name
            elif isinstance(child.item.line_type, str):
                line_type_name = child.item.line_type.split('.')[-1].upper()
            elif isinstance(child.item.line_type, int):
                try:
                    line_type_name = GnosticLineType(child.item.line_type).name
                except Exception:
                    line_type_name = str(child.item.line_type)

            # --- MOVEMENT I: LOGIC GATES & ALCHEMICAL CONSTRUCTS ---
            if line_type_name in ("LOGIC", "SGF_CONSTRUCT"):
                ctx.visibility_map[child.item.line_num] = scope.parent_visible

                # Handle SGF Constructs (like {{ logic.weave }})
                if line_type_name == "SGF_CONSTRUCT":
                    if scope.parent_visible:
                        if self._node_interceptor:
                            # Yield to the TraversalEngine's flattener
                            self._node_interceptor(child, current_path)
                        else:
                            # Fallback to direct ignition if un-intercepted
                            self._ignite_alchemical_construct(child, current_path, ctx)
                    # [THE MASTER CURE]: We MUST continue! This is an inline construct,
                    # NOT a hierarchical logic gate (@if/@for). Falling through shatters the AST.
                    continue

                if not scope.parent_visible:
                    child.logic_result = False
                    self.walk(child, current_path, ctx, parent_visible=False, depth=depth + 1,
                              breadcrumb=new_breadcrumb)
                    continue

                # Normal control flow evaluation (@if, @for)
                should_enter = self.adjudicator.evaluate_gate(child, scope)
                self.walk(child, current_path, ctx, parent_visible=should_enter, depth=depth + 1,
                          breadcrumb=new_breadcrumb)

            # --- MOVEMENT II: LIFECYCLE VOWS (POST-RUN, ON-HERESY, ON-UNDO) ---
            elif line_type_name in ("POST_RUN", "ON_HERESY", "ON_UNDO"):
                ctx.visibility_map[child.item.line_num] = scope.parent_visible

                if scope.parent_visible:
                    if line_type_name == "POST_RUN":
                        self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                    else:
                        # [ASCENSION 26]: Attach resilience blocks to preceding kinetic action
                        self.reaper.attach_causal_block(child, child.item.line_type, self)

            # --- MOVEMENT III: ATOMIC EDICTS (COMMANDS) ---
            elif line_type_name == "VOW":
                ctx.visibility_map[child.item.line_num] = scope.parent_visible
                if scope.parent_visible:
                    # Harvest the command string and prepare it for the Maestro
                    self.reaper.harvest_vow(child.item)

                    # [ASCENSION 35]: DYNAMIC EDICT RESURRECTION
                    # Directly attach the edict object if it arrived in the soul.
                    edict_soul = getattr(child.item, 'edict_obj', None)
                    if edict_soul:
                        ctx.edicts.append(edict_soul)

                    self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1, breadcrumb=new_breadcrumb)

            # --- MOVEMENT IV: PHYSICAL FORM (MATTER) ---
            elif line_type_name == "FORM":
                if scope.parent_visible:
                    # The Mason ensures the path is topologically sound
                    next_path = self.mason.forge_matter(child, current_path)
                    # Descend into the new physical level
                    self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1,
                              breadcrumb=new_breadcrumb)
                else:
                    ctx.visibility_map[child.item.line_num] = False
            else:
                if child.item.line_num > 0:
                    ctx.visibility_map[child.item.line_num] = scope.parent_visible

            # [ASCENSION 15]: Metabolic Tax Logging
            self._weave_tax_ns += (time.perf_counter_ns() - _start_ns)

    def _ignite_alchemical_construct(self, node: _GnosticNode, current_path: Path, ctx: SpacetimeContext):
        """
        =================================================================================
        == THE ATOMIC STRIKE: RESONANT TOPOGRAPHY (V-Ω-TOTALITY-VMAX-SUTURED-HEALED)   ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_IGNITE_CONSTRUCT_VMAX_GEOMETRIC_ANCHOR_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for sub-weave orchestration. This version
        righteously annihilates the 236-ONTOLOGICAL-ERASURE paradox by implementing
        Geometric Context Pinning and Laminar Buffer Isolation.
        """
        expression = node.item.sgf_expression
        if not expression:
            return

        line_num = node.item.line_num
        _start_ns = time.perf_counter_ns()

        try:
            # =========================================================================
            # == MOVEMENT I: GEOMETRIC CONTEXT PINNING (THE MASTER CURE)             ==
            # =========================================================================
            if not isinstance(current_path, Path):
                current_path = Path(current_path)

            posix_path = str(current_path).replace('\\', '/')
            if posix_path in ("", "/", "."):
                posix_path = "."

            # [ASCENSION 50]: Safely initialize the stack if missing
            if not hasattr(self._thread_local, 'spatial_stack'):
                self._thread_local.spatial_stack = []

            # Push current state onto the local stack
            previous_file = self.gnostic_context.get("__current_file__", "VOID")
            previous_dir = self.gnostic_context.get("__current_dir__", "VOID")
            self._thread_local.spatial_stack.append((previous_file, previous_dir))

            # Clone the Mind to isolate sub-effects
            local_mind = ctx.gnostic_context.raw.copy()

            # [STRIKE]: SUTURE THE ANCHORS
            local_mind["__current_file__"] = posix_path
            local_mind["__current_dir__"] = posix_path
            local_mind["__current_column__"] = node.item.original_indent

            # =========================================================================
            # == MOVEMENT II: [THE MASTER CURE] - LAMINAR BUFFER ISOLATION           ==
            # =========================================================================
            with self._traversal_lock:
                prime_matter_ref = self.gnostic_context.raw.get("__woven_matter__")
                prime_commands_ref = self.gnostic_context.raw.get("__woven_commands__")

                isolated_matter_buffer = []
                isolated_commands_buffer = []

            local_mind["__woven_matter__"] = isolated_matter_buffer
            local_mind["__woven_commands__"] = isolated_commands_buffer

            previous_thread_ctx = get_active_context()
            set_active_context(local_mind)

            try:
                if self._is_wasm: time.sleep(0)

                # [ASCENSION 51]: HUD RADIATION SUTURE (THE FIX)
                if not self._is_adrenaline and not self.gnostic_context.raw.get('silent'):
                    self._radiate_hud_pulse(f"WEAVING_ATOM_{line_num}", ctx)

                self.logger.verbose(f"   -> {self.UV_GLOW}Evaluating Construct:{self.RESET} {expression[:60]}...")

                # [STRIKE]: Execute. LogicDomain now sees __current_file__ and
                # triggers the recursive WeaveRequest IMMEDIATELY.
                self.alchemist.transmute(expression, local_mind)

                # =====================================================================
                # == MOVEMENT IV: RECLAMATION (MANUAL MATTER HARVEST)                ==
                # =====================================================================
                with self._traversal_lock:
                    if isolated_matter_buffer:
                        pre_count = len(self.ctx.items)
                        matter_snapshot = list(isolated_matter_buffer)
                        self._harvest_woven_matter(matter_snapshot, current_path, line_num, ctx)

                        post_count = len(self.ctx.items)
                        if post_count > pre_count:
                            self.logger.verbose(
                                f"   -> {self.GOLD_BOLD}Matter Absorbed:{self.RESET} {post_count - pre_count} atoms from sub-weave.")

                    if isolated_commands_buffer:
                        command_snapshot = list(isolated_commands_buffer)
                        for cmd in command_snapshot:
                            raw = list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)]
                            while len(raw) < 4: raw.append(None)
                            cmd_tuple = (raw[0], line_num, raw[2], raw[3])
                            self.ctx.post_run_commands.append(cmd_tuple)

            finally:
                # =========================================================================
                # == MOVEMENT V: THE GROUNDING (STATE RESTORATION)                       ==
                # =========================================================================
                set_active_context(previous_thread_ctx)

                with self._traversal_lock:
                    if 'prime_matter_ref' in locals() and prime_matter_ref is not None:
                        self.gnostic_context.raw["__woven_matter__"] = prime_matter_ref
                    if 'prime_commands_ref' in locals() and prime_commands_ref is not None:
                        self.gnostic_context.raw["__woven_commands__"] = prime_commands_ref

                # SPATIAL STACK UNWIND
                if getattr(self._thread_local, 'spatial_stack', []):
                    prev_file, prev_dir = self._thread_local.spatial_stack.pop()
                    self.gnostic_context.set("__current_file__", prev_file)
                    self.gnostic_context.set("__current_dir__", prev_dir)

                if len(isolated_matter_buffer) > 100:
                    import gc
                    gc.collect(0)

        except Exception as alchemical_paradox:
            self.logger.error(f"L{line_num}: Construct fracture: {alchemical_paradox}")
            if self._debug_mode:
                sys.stderr.write(
                    f"\n{self.ALERT}!!! CONSTRUCT FRACTURE !!!{self.RESET}\nL{line_num}: {expression}\n{traceback.format_exc()}\n")
                sys.stderr.flush()

    def _harvest_woven_matter(self, atoms: List[Any], current_path: Path, line_num: int, ctx: SpacetimeContext):
        """
        =================================================================================
        == THE POLYMORPHIC RESURRECTOR: ULTRAVIOLET (V-Ω-TOTALITY-VMAX-ZERO-STICTION) ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_RECLAMATION_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_HARVEST_VMAX_ZERO_STICTION_2026_FINALIS

        [THE MANIFESTO]
        This rite righteously absorbs matter from sub-dimensional weaves. It is
        surgically re-engineered for Zero-Stiction performance, annihilating
        synchronous I/O freezes by deferring terminal flushes and employing
        O(1) Enum resolution.
        """
        import time
        import gc
        from pathlib import Path
        from ....contracts.data_contracts import GnosticLineType, ScaffoldItem

        absorbed_count = 0
        _start_ts = time.perf_counter_ns()

        # --- MOVEMENT I: THE RECLAMATION OF SOULS ---
        for raw_atom in atoms:
            atom = None

            # [ASCENSION 13]: ZERO-STICTION DICTIONARY CASTING
            if isinstance(raw_atom, dict):
                try:
                    # 1. Geometric Coordinate Re-Inception
                    if 'path' in raw_atom and raw_atom['path']:
                        # [ASCENSION 6]: POSIX Harmony Suture
                        raw_atom['path'] = Path(str(raw_atom['path']).replace('\\', '/'))

                    # 2. Forensic Metadata Suture
                    if 'metadata' not in raw_atom or raw_atom['metadata'] is None:
                        raw_atom['metadata'] = {}

                    # [ASCENSION 15]: Locus Tomography
                    raw_atom['metadata']["parent_line"] = line_num
                    # [ASCENSION 5]: Achronal Trace Suture
                    raw_atom['metadata']["trace_id"] = ctx.gnostic_context.raw.get("trace_id", "tr-woven")

                    # 3. CONCRETE SOUL MATERIALIZATION
                    atom = ScaffoldItem.model_validate(raw_atom)

                    # [ASCENSION 11]: Edict Soul Reclamation
                    if 'edict_obj' in raw_atom:
                        object.__setattr__(atom, 'edict_obj', raw_atom['edict_obj'])

                except Exception as val_err:
                    # [ASCENSION 7]: Socratic Error Triage
                    self.logger.warn(f"L{line_num}: Atom Resurrection Fracture: {val_err}")
                    continue
            else:
                atom = raw_atom

            if not isinstance(atom, ScaffoldItem):
                continue

            # [ASCENSION 3]: BICAMERAL ENUM EXORCISM
            # Resolves the line_type identity using O(1) string scrying.
            if not isinstance(atom.line_type, GnosticLineType):
                try:
                    lt_name = str(atom.line_type).split('.')[-1].upper()
                    atom.line_type = GnosticLineType[lt_name]
                except Exception:
                    atom.line_type = GnosticLineType.FORM

            # [ASCENSION 6]: GEOMETRIC PATH HARMONY
            # Ensures absolute slash parity before the item reaches the Iron.
            if atom.path:
                try:
                    # Inplace mutation of Path soul
                    normalized_path = Path(str(atom.path).replace('\\', '/'))
                    object.__setattr__(atom, 'path', normalized_path)
                except Exception:
                    pass

            # =========================================================================
            # == [STRIKE]: LAMINAR REFERENCE SUTURE                                  ==
            # =========================================================================
            # We inscribe the atom into the Prime Timeline's reservoir.
            # id(ctx.items) remains constant, preserving the physical memory artery.
            ctx.register_matter(atom)
            absorbed_count += 1

            # [ASCENSION 10]: HUD PULSE THROTTLING
            # Radiates status to the Retina (Monaco) only if the pipe is resonant.
            self._radiate_hud_pulse(atom.path.name if atom.path else "Shard", ctx)

        # =========================================================================
        # == MOVEMENT II: [THE MASTER CURE] - APOPHATIC RADIATION SHIELD         ==
        # =========================================================================
        # We NO LONGER call sys.stdout.flush() or perform heavy terminal I/O
        # inside this rite. This eliminates the "Freezing" anomaly.
        if absorbed_count > 0:
            duration_ms = (time.perf_counter_ns() - _start_ts) / 1_000_000

            # Luminous Telemetry remains for the Forensic Ledger (if verbose)
            if self._debug_mode:
                buffer_id = hex(id(atoms)).upper()
                prime_id = hex(id(ctx.items)).upper()

                # We log via the Scribe, which handles non-blocking emission.
                self.logger.verbose(
                    f"⚛️  GNOSTIC_HARVEST: {absorbed_count} atoms absorbed @ L{line_num} "
                    f"[{duration_ms:.2f}ms] | Buff:{buffer_id} -> Res:{prime_id}"
                )

            # [ASCENSION 8]: HYDRAULIC GC PACING
            # Perform a generation-1 lustration if the mass is high.
            if absorbed_count > 500:
                gc.collect(1)

        # [ASCENSION 24]: THE FINALITY VOW
        self._total_atoms_absorbed += absorbed_count

    def _radiate_hud_pulse(self, name: str, ctx: SpacetimeContext):
        """[ASCENSION 16]: DEBOUNCED OCULAR RADIATOR."""
        if self.ctx and self.ctx.gnostic_context.raw.get('silent'): return

        # [THE CURE]: 30Hz Debounce
        # Prevents the "Freezing" caused by saturated WebSocket pipes.
        now = time.perf_counter_ns()
        last = getattr(self, '_last_pulse_ns', 0)
        if (now - last) < 33_333_333:  # ~33ms
            return
        self._last_pulse_ns = now

        engine = self.ctx.gnostic_context.raw.get('__engine__')
        akashic = getattr(engine, 'akashic', None)

        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_ABSORBED",
                        "label": f"WOVEN: {name[:20]}",
                        "color": "#a855f7",
                        "trace": self.ctx.gnostic_context.raw.get('trace_id', 'void')
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        tax_ms = self._weave_tax_ns / 1_000_000
        return f"<Ω_DIMENSIONAL_WALKER id={self._id} absorbed={self._total_atoms_absorbed} tax={tax_ms:.2f}ms status=RESONANT>"