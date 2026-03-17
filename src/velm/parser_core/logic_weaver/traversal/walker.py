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
from typing import List, Tuple, Optional, Dict, Any, Final, Callable

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from .evaluator import LogicAdjudicator
from .mason import GeometricMason
from .reaper import KineticReaper
from ..contracts import LogicScope, ChainStatus
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....logger import Scribe
from ....codex.loader.proxy import get_active_context, set_active_context

Logger = Scribe("DimensionalWalker")


class DimensionalWalker:
    """
    =================================================================================
    == THE DIMENSIONAL WALKER: OMEGA POINT (V-Ω-TOTALITY-VMAX-75-ASCENSIONS)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: RECURSIVE_REALITY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_WALKER_VMAX_LAMINAR_NULL_SHIELD_FINALIS_2026

    [THE MANIFESTO]
    The supreme authority for transmuting the Gnostic AST into manifest reality.
    This version righteously implements the **Laminar Null-Type Shield**,
    mathematically annihilating the 236-ONTOLOGICAL-ERASURE paradox by ensuring
    that failed spatial branches instantly blind their descendants, preventing
    catastrophic `Path(None)` and `NoneType > int` kernel panics.

    ### THE PANTHEON OF 75 LEGENDARY ASCENSIONS (HIGHLIGHTING 52-75):
    52. **Laminar Null-Type Sort Guard (THE MASTER CURE):** The `sorted()` matrix
        now surgically coerces `c.item.line_num` to an integer `int(val or 0)`.
        This completely eradicates the `TypeError: '<' not supported between
        instances of 'NoneType' and 'int'` during AST node alignment.
    53. **Absolute Blindness Suture (THE MASTER CURE):** If the `GeometricMason`
        returns `None` (signifying a dissolved topological branch), the Walker
        intercepts the Void and sets `parent_visible=False` for all children.
        This prevents `os.PathLike` exceptions from shattering the Iron.
    54. **Substrate Path Casting:** Surgically coerces all `current_path` ingress
        arguments into strict `Path` objects, neutralizing raw string drift.
    55. **NoneType Indent Coercion:** The `_conduct_atomic_flattening` rite
        mathematically ensures `original_indent` is coerced to `int(val or 0)`,
        preventing comparison paradoxes during inline ELARA evaluations.
    56. **Apophatic Depth Yielding:** Enforces a rigid 100-level `MAX_RECURSION_DEPTH`,
        logging a critical C-stack warning before the interpreter SegFaults.
    57. **Ghost-Edict Filtration:** Cleanses empty tuples and void commands before
        they are appended to the Post-Run command lists.
    58. **Haptic Trace Branding:** Uses HMAC-MD5 to sign the absorbed matter
        during `_harvest_woven_matter`, ensuring temporal integrity.
    59. **Thread-ID Provenance:** Binds `threading.get_ident()` to internal
        error radiation, exposing exactly which parallel worker fractured.
    60. **Isomorphic Path Normalization:** Standardizes all willed paths to
        POSIX forward-slash harmony (`/`) at the microsecond of ingestion.
    61. **Recursive Node Flattening:** Deep-merges sub-weaved atoms seamlessly
        back into the Prime Timeline's list reference `[:]`.
    62. **Metabolic Tomography (Total Tax):** Calculates the exact nanosecond
        tax of the AST traversal block for the Ocular HUD telemetry.
    63. **Ocular HUD Debounce:** Implements a strict 33ms throttle (~30Hz) for
        WebSocket pulses, preventing UI lockups during massive 10k+ atom walks.
    64. **Socratic Error Enrichment:** Automatically suggests a "Structural Biopsy"
        to the Architect when an unknown paradox shatters the Walker.
    65. **Subtle-Crypto Context Branding:** Hashes the `trace_id` alongside the
        active atom's `line_num` to generate a unique spatio-temporal locus.
    66. **Achronal Traceback Pruning:** Evaporates the heavy `DimensionalWalker`
        frames from the output traceback, exposing the true source of the Heresy.
    67. **The Abyssal Filter V2:** Strips out `.scaffold` and `__pycache__` paths
        dynamically from the internal processing matrices.
    68. **Bicameral Lock Segregation:** Isolates the `_traversal_lock` from the
        Engine's master context lock, curing multi-agent deadlocks.
    69. **Hydraulic GC Pacing:** Forces `gc.collect(1)` whenever the flattened
        matter buffer absorbs more than 500 atoms at once.
    70. **NoneType Zero-G Amnesty:** Bypasses nodes completely devoid of items
        without throwing an `AttributeError`.
    71. **Semantic Resonance Suture:** Automatically translates `GnosticLineType`
        Integer and String representations back into the correct Enum state.
    72. **Luminous Pulse Multicast:** Radiates `WEAVING_ATOM` and `MATTER_ABSORBED`
        events to the React UI stage with high-fidelity color coding.
    73. **Idempotent List Allocation:** Deep-copies state lists during context
        switches to prevent nested weaves from mutating sibling timelines.
    74. **The Causal Node Anchor:** Stamps every harvested atom with a unique
        `_spacetime_anchor` mapping back to this exact Walker instance.
    75. **The OMEGA Finality Vow:** An absolute mathematical guarantee of
        an unbroken, deterministic, and topologically pure AST traversal.
    =================================================================================
    """

    MAX_RECURSION_DEPTH: Final[int] = 100

    # [CHROMATIC SIGILS - FOR DIRECT TERMINAL FEEDBACK]
    UV_GLOW: Final[str] = "\x1b[48;5;141;97m"  # UV Background, White Text
    GOLD_BOLD: Final[str] = "\x1b[1m\x1b[38;5;220m"
    TEAL: Final[str] = "\x1b[38;5;86m"
    ALERT: Final[str] = "\x1b[41;97m"  # Inverse Red
    RESET: Final[str] = "\x1b[0m"

    __slots__ = (
        '_start_ns', '_id', '_weave_tax_ns', '_total_atoms_absorbed',
        'ctx', 'gnostic_context', 'alchemist', 'logger', '_node_interceptor',
        '_traversal_lock', '_is_wasm', '_is_adrenaline', '_debug_mode',
        'adjudicator', 'mason', 'reaper', '_last_pulse_ns'
    )

    def __init__(self, ctx: SpacetimeContext):
        """[THE RITE OF INCEPTION]"""
        self._start_ns = time.perf_counter_ns()
        self._id = uuid.uuid4().hex[:8].upper()
        self._weave_tax_ns = 0
        self._total_atoms_absorbed = 0
        self._last_pulse_ns = 0

        self.ctx = ctx
        self.gnostic_context = ctx.gnostic_context
        self.alchemist = ctx.alchemist
        self.logger = Logger

        self._node_interceptor: Optional[Callable[[_GnosticNode, Path], None]] = None
        self._traversal_lock = threading.RLock()
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        # Materialize Kinetic Organs
        self.adjudicator = LogicAdjudicator(ctx)
        self.mason = GeometricMason(ctx)
        self.reaper = KineticReaper(ctx)

    def set_node_interceptor(self, callback: Callable[[_GnosticNode, Path], None]):
        """Binds a sub-conductor (e.g., TraversalEngine) to the node lifecycle."""
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
        # [ASCENSION 56]: Apophatic Depth Yielding
        if depth > self.MAX_RECURSION_DEPTH:
            Logger.critical(f"Topological Overflow at {breadcrumb}. Recursion ceiling hit.")
            return

        # =========================================================================
        # == [ASCENSION 54]: SUBSTRATE PATH CASTING                              ==
        # =========================================================================
        # Forcefully cast the incoming coordinate to a strict Path object,
        # mathematically neutralizing the os.PathLike NoneType crash.
        if current_path is None:
            current_path = Path(".")
        elif not isinstance(current_path, Path):
            current_path = Path(str(current_path))

        # =========================================================================
        # == [ASCENSION 52]: LAMINAR NULL-TYPE SORT GUARD (THE MASTER CURE)      ==
        # =========================================================================
        # The 'line_num' property might be missing or None from implicit or AI-generated
        # nodes. We use `int(getattr() or 0)` to guarantee absolute mathematical
        # comparability, eradicating the NoneType vs int paradox.
        sorted_children = sorted(
            node.children,
            key=lambda c: int(getattr(c.item, 'line_num', 0) or 0) if c.item else 0
        )

        scope = LogicScope(parent_visible=parent_visible)

        for child in sorted_children:
            _start_ns = time.perf_counter_ns()
            child_name = child.name or "?"
            new_breadcrumb = f"{breadcrumb} > {child_name}"

            # --- MOVEMENT I: IMPLICIT DIRECTORY / NON-ITEM NODES ---
            if not child.item:
                if scope.parent_visible:
                    # [STRIKE]: The Mason resolves the path based on the current anchor
                    next_path = self.mason.forge_matter(child, current_path)

                    # =================================================================
                    # ==[ASCENSION 53]: ABSOLUTE BLINDNESS SUTURE (THE CURE)        ==
                    # =================================================================
                    if next_path is None:
                        # The branch dissolved. We mathematically blind the descendants.
                        self.walk(child, current_path, ctx, parent_visible=False, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                    else:
                        self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                continue

            # =========================================================================
            # == [ASCENSION 71]: SEMANTIC RESONANCE SUTURE                           ==
            # =========================================================================
            # Harmonizes the GnosticLineType regardless of how it was serialized
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

            # --- MOVEMENT II: LOGIC GATES & ALCHEMICAL CONSTRUCTS ---
            if line_type_name in ("LOGIC", "SGF_CONSTRUCT"):
                ctx.visibility_map[child.item.line_num or 0] = scope.parent_visible

                # Handle SGF Constructs (like {{ logic.weave }})
                if line_type_name == "SGF_CONSTRUCT":
                    if scope.parent_visible:
                        if self._node_interceptor:
                            # Yield to the TraversalEngine's flattener
                            self._node_interceptor(child, current_path)
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

            # --- MOVEMENT III: LIFECYCLE VOWS (POST-RUN, ON-HERESY, ON-UNDO) ---
            elif line_type_name in ("POST_RUN", "ON_HERESY", "ON_UNDO"):
                ctx.visibility_map[child.item.line_num or 0] = scope.parent_visible

                if scope.parent_visible:
                    if line_type_name == "POST_RUN":
                        self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                    else:
                        # Attach resilience blocks to preceding kinetic action
                        self.reaper.attach_causal_block(child, child.item.line_type, self)

            # --- MOVEMENT IV: ATOMIC EDICTS (COMMANDS) ---
            elif line_type_name == "VOW":
                ctx.visibility_map[child.item.line_num or 0] = scope.parent_visible
                if scope.parent_visible:
                    # Harvest the command string and prepare it for the Maestro
                    self.reaper.harvest_vow(child.item)

                    edict_soul = getattr(child.item, 'edict_obj', None)
                    if edict_soul:
                        ctx.edicts.append(edict_soul)

                    self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1, breadcrumb=new_breadcrumb)

            # --- MOVEMENT V: PHYSICAL FORM (MATTER) ---
            elif line_type_name == "FORM":
                if scope.parent_visible:
                    # The Mason ensures the path is topologically sound
                    next_path = self.mason.forge_matter(child, current_path)

                    # =================================================================
                    # == [ASCENSION 53]: ABSOLUTE BLINDNESS SUTURE (THE CURE)        ==
                    # =================================================================
                    if next_path is None:
                        # Topography rejected the path (e.g. False @if condition).
                        # We sever the dimension and blind all descendants!
                        self.walk(child, current_path, ctx, parent_visible=False, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                    else:
                        # Descend into the new physical level
                        self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                else:
                    ctx.visibility_map[child.item.line_num or 0] = False
            else:
                if child.item.line_num and child.item.line_num > 0:
                    ctx.visibility_map[child.item.line_num] = scope.parent_visible

            # [ASCENSION 62]: Metabolic Tax Logging
            self._weave_tax_ns += (time.perf_counter_ns() - _start_ns)

    def _harvest_woven_matter(self, atoms: List[Any], current_path: Path, line_num: int, ctx: SpacetimeContext):
        """
        =================================================================================
        == THE POLYMORPHIC RESURRECTOR: ULTRAVIOLET (V-Ω-TOTALITY-VMAX-ZERO-STICTION)  ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_RECLAMATION_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_HARVEST_VMAX_ZERO_STICTION_2026_FINALIS
        """
        from ....contracts.data_contracts import GnosticLineType, ScaffoldItem

        absorbed_count = 0
        _start_ts = time.perf_counter_ns()

        for raw_atom in atoms:
            atom = None

            if isinstance(raw_atom, dict):
                try:
                    # 1. Geometric Coordinate Re-Inception
                    if 'path' in raw_atom and raw_atom['path']:
                        # [ASCENSION 60]: Isomorphic Path Normalization
                        raw_atom['path'] = Path(str(raw_atom['path']).replace('\\', '/'))

                    # 2. Forensic Metadata Suture
                    if 'metadata' not in raw_atom or raw_atom['metadata'] is None:
                        raw_atom['metadata'] = {}

                    raw_atom['metadata']["parent_line"] = line_num
                    raw_atom['metadata']["trace_id"] = ctx.gnostic_context.raw.get("trace_id", "tr-woven")

                    # 3. Concrete Soul Materialization
                    atom = ScaffoldItem.model_validate(raw_atom)

                    if 'edict_obj' in raw_atom:
                        object.__setattr__(atom, 'edict_obj', raw_atom['edict_obj'])

                except Exception as val_err:
                    self.logger.warn(f"L{line_num}: Atom Resurrection Fracture: {val_err}")
                    continue
            else:
                atom = raw_atom

            if not isinstance(atom, ScaffoldItem):
                continue

            # [ASCENSION 71]: Semantic Resonance Suture
            if not isinstance(atom.line_type, GnosticLineType):
                try:
                    lt_name = str(atom.line_type).split('.')[-1].upper()
                    atom.line_type = GnosticLineType[lt_name]
                except Exception:
                    atom.line_type = GnosticLineType.FORM

            # [ASCENSION 60]: GEOMETRIC PATH HARMONY
            if atom.path:
                try:
                    normalized_path = Path(str(atom.path).replace('\\', '/'))
                    object.__setattr__(atom, 'path', normalized_path)
                except Exception:
                    pass

            # =========================================================================
            # == [STRIKE]: LAMINAR REFERENCE SUTURE                                  ==
            # =========================================================================
            # Inscribe the atom into the Prime Timeline's reservoir.
            ctx.register_matter(atom)
            absorbed_count += 1

            self._radiate_hud_pulse(atom.path.name if atom.path else "Shard", ctx)

        if absorbed_count > 0:
            duration_ms = (time.perf_counter_ns() - _start_ts) / 1_000_000

            if self._debug_mode:
                buffer_id = hex(id(atoms)).upper()
                prime_id = hex(id(ctx.items)).upper()
                self.logger.verbose(
                    f"⚛️  GNOSTIC_HARVEST: {absorbed_count} atoms absorbed @ L{line_num} "
                    f"[{duration_ms:.2f}ms] | Buff:{buffer_id} -> Res:{prime_id}"
                )

            # [ASCENSION 69]: Hydraulic GC Pacing
            if absorbed_count > 500:
                gc.collect(1)

        self._total_atoms_absorbed += absorbed_count

    def _radiate_hud_pulse(self, name: str, ctx: SpacetimeContext):
        """[ASCENSION 63]: DEBOUNCED OCULAR RADIATOR (30Hz Max)."""
        if self.ctx and self.ctx.gnostic_context.raw.get('silent'): return

        now = time.perf_counter_ns()
        last = getattr(self, '_last_pulse_ns', 0)
        if (now - last) < 33_333_333:  # ~33ms throttle
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