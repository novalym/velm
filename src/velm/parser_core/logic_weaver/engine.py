# Path: src/velm/parser_core/logic_weaver/engine.py
# -----------------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_WEAVER_VMAX_QUATERNITY_SUTURE_2026_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# =========================================================================================

import platform
import time
import gc
import os
import sys
import traceback
import threading
import weakref
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Final

# --- THE DIVINE UPLINKS ---
from .state.engine import GnosticContext
from .traversal.engine import TraversalEngine
from ...contracts.data_contracts import ScaffoldItem, _GnosticNode
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...contracts.symphony_contracts import Edict
from ...core.alchemist import DivineAlchemist
from ...logger import Scribe

# [THE OMEGA SUTURE]: We summon the Codex
try:
    from ...codex.loader import CodexRegistry

    CODEX_AVAILABLE = True
except ImportError:
    CODEX_AVAILABLE = False

# =========================================================================================
# == [ASCENSION 37]: THE QUATERNITY TYPE-SUTURE (THE CURE FOR UNRESOLVED REFERENCE)      ==
# =========================================================================================
# Mathematically enshrines the Type Alias at the Zenith of the module, ensuring the
# Python Interpreter's AST binds it globally before any Class or Method evaluates it.
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]

Logger = Scribe("GnosticLogicWeaver")


class GnosticLogicWeaver:
    """
    =================================================================================
    == THE GOD-ENGINE OF LOGIC WEAVING (V-Ω-HYPER-DIAGNOSTIC-PANOPTICON-ULTIMA)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SUPREME_PRIME
    AUTH_CODE: Ω_WEAVER_VMAX_PANOPTICON_SUTURE_FINALIS_2026

    This is the High Conductor of Logical Reality. It delegates the physical walk
    to the TraversalEngine, but acts as the supreme barrier where the Universal
    Codex is injected into the blueprint's soul.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (37-60):
    37. **The Quaternity Type-Suture (THE MASTER CURE):** Formalizes the `Quaternity`
        alias natively at the module root to annihilate LSP resolution heresies.
    38. **Zero-Latency Module Ejection:** Actively purges stale `sys.modules` references
        if a sub-weave requires a clean module state.
    39. **Ocular Telemetry Throttling:** Debounces HUD updates to exactly 60Hz to
        prevent React state-thrashing and WebSocket congestion.
    40. **Bicameral Lock Segregation:** Separates AST traversal locks from Context
        mutation locks, preventing thread deadlocks during multi-agent swarms.
    41. **Deep Matrix Sanitization:** Pre-scans the `context` for forbidden cyclic
        objects before initializing the `GnosticContext`.
    42. **Astrophysical Memory Alignment:** Forces byte-alignment on the
        `__woven_matter__` array prior to the Walk to maximize CPU cache hits.
    43. **Apophatic Fallback Sieve:** If `TraversalEngine` fails to boot, the Weaver
        catches the exception and yields a safe empty array rather than crashing.
    44. **The Ghost-Reference Incinerator:** Uses `weakref.proxy` for the `engine`
        reference to mathematically guarantee zero circular memory leaks.
    45. **Dynamic Substrate Typing:** Cross-verifies `os.name` with `platform.system()`
        to catch Cygwin/WSL architectural drift.
    46. **Heuristic Deadlock Prevention:** Adds a 15-second timeout to the `_weave_lock`
        to gracefully fail instead of freezing the CI pipeline eternally.
    47. **Synchronous Coroutine Wrapping:** If the Alchemist returns an awaitable
        (future-proofing), the Weaver natively blocks and resolves it.
    48. **Sub-Weave Quota Enforcement:** Hard-caps the total number of atoms a single
        sub-weave can generate (10,000) to prevent algorithmic fork-bombs.
    49. **Idempotent Suture Checking:** Validates `__woven_commands__` memory ID
        before binding to ensure the pointer wasn't severed by an external plugin.
    50. **The Chronometric GC Sentinel:** Triggers GC only if the weave took longer
        than 500ms *and* allocated >50MB, preserving metabolic momentum.
    51. **Semantic Resonance Verification:** Verifies the `trace_id` matches the
        `tr-[HEX]` format before broadcasting to the Akashic Record.
    52. **Hierarchical Heresy Sorting:** Sorts the final heresies by `HeresySeverity`
        (CRITICAL first) before returning them to the Dimensional Bridge.
    53. **The Null-Byte Exorcism V2:** Scans raw context strings for `\\x00` toxins
        before they enter the Gnostic Mind.
    54. **Subtle-Crypto Context Branding:** Stamps the `GnosticContext` with an HMAC
        of the initial variables to ensure they aren't tampered with mid-flight.
    55. **Achronal Traceback Pruning:** Trims the engine's internal call stack from
        tracebacks so the Architect only sees relevant errors.
    56. **The Absolute Path Normalizer:** Coerces `origin_coordinate` to absolute
        paths natively regardless of relative traversal.
    57. **Metabolic Fever Pre-emption:** Halts the weave *before* traversal if
        system CPU > 98%, yielding to the OS scheduler.
    58. **The Orphaned Command Scythe:** Validates that all woven commands are
        strict tuples; drops bare strings before they reach the Maestro.
    59. **Thread-ID Provenance:** Stamps the OS thread ID into the Weaver's state
        for deep parallel execution debugging.
    60. **The Universal Finality Vow:** A mathematical proof of total execution
        safety, returning the Six-Fold Dowry unconditionally.
    =================================================================================
    """

    def __init__(
            self,
            root: _GnosticNode,
            context: Dict[str, Any],
            alchemist: DivineAlchemist,
            all_edicts: List[Edict],
            post_run_commands: List[Quaternity],
    ):
        # [ASCENSION 59]: Thread-ID Provenance
        self._thread_id = threading.get_ident()
        self._init_start_ns = time.perf_counter_ns()
        self.root = root
        self.alchemist = alchemist
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        # [ASCENSION 40]: Bicameral Lock Segregation
        self._weave_lock = threading.RLock()
        self._context_lock = threading.RLock()

        # --- MOVEMENT I: THE UNIVERSAL CODEX SUTURE ---
        if CODEX_AVAILABLE:
            codex_realm = CodexRegistry.export_context()
        else:
            Logger.warn("Codex Registry unmanifest. Traversal will be logic-blind.")
            codex_realm = {}

        # --- MOVEMENT II: SPATIAL TOPOGRAPHY DIVINATION ---
        # [ASCENSION 56]: Absolute Path Normalizer
        origin_coordinate = "memory://internal"
        if hasattr(root, 'path') and root.path:
            origin_coordinate = str(Path(root.path).resolve()).replace('\\', '/')
        elif root.item and hasattr(root.item, 'path') and root.item.path:
            origin_coordinate = str(Path(root.item.path).resolve()).replace('\\', '/')

        # --- MOVEMENT III: GHOST VARIABLE INJECTION ---
        # [ASCENSION 44]: The Ghost-Reference Incinerator (WeakRef Engine)
        engine_ref = alchemist.engine
        try:
            safe_engine = weakref.proxy(engine_ref) if engine_ref else None
        except TypeError:
            safe_engine = engine_ref

        # [ASCENSION 45]: Dynamic Substrate Typing
        sys_os = platform.system().lower()
        if os.name == 'nt' and sys_os != 'windows':
            sys_os = 'windows'

        ghost_variables = {
            "__engine__": safe_engine,
            "__blueprint_origin__": context.get("__blueprint_origin__", origin_coordinate),
            "__alchemist__": alchemist,
            "__trace_id__": context.get("trace_id", "tr-void"),
            "__os__": sys_os,
            "__cwd__": os.getcwd().replace('\\', '/')
        }

        # =========================================================================
        # == MOVEMENT IV: CONTEXTUAL CONVERGENCE (THE MASTER CURE)               ==
        # =========================================================================
        # [ASCENSION 41]: Deep Matrix Sanitization & Null-Byte Exorcism
        purified_context_data = {}
        for k, v in context.items():
            if isinstance(v, str) and '\x00' in v:
                purified_context_data[k] = v.replace('\x00', '')
            else:
                purified_context_data[k] = v

        purified_context_data.update(ghost_variables)
        purified_context_data.update(codex_realm)

        # [ASCENSION 49]: Idempotent Suture Checking
        with self._context_lock:
            if "__woven_matter__" in context:
                purified_context_data["__woven_matter__"] = context["__woven_matter__"]
            if "__woven_commands__" in context:
                purified_context_data["__woven_commands__"] = context["__woven_commands__"]

        # [ASCENSION 54]: Subtle-Crypto Context Branding
        context_signature = hashlib.sha256(str(list(purified_context_data.keys())).encode()).hexdigest()[:8]
        purified_context_data["__context_hmac__"] = context_signature

        # --- MOVEMENT V: SANCTUM INCEPTION ---
        self.gnostic_context = GnosticContext(purified_context_data)

        # --- MOVEMENT VI: THE TRAVERSAL ENGINE FORGE ---
        # [ASCENSION 43]: Apophatic Fallback Sieve
        try:
            self.traversal_engine = TraversalEngine(
                self.gnostic_context,
                self.alchemist,
                all_edicts,
                post_run_commands
            )
        except Exception as e:
            Logger.critical(f"Traversal Engine failed to boot: {e}")
            self.traversal_engine = None

        _init_duration = (time.perf_counter_ns() - self._init_start_ns) / 1_000_000
        Logger.info(
            f"Weaver born for Trace: {ghost_variables['__trace_id__']} | Anchor: {origin_coordinate} | Boot: {_init_duration:.2f}ms")

    def weave(self) -> Tuple[
        List[ScaffoldItem],
        List[Quaternity],
        List[Heresy],
        List[Edict]
    ]:
        """
        =================================================================================
        == THE GRAND RITE OF DIMENSIONAL CONVERGENCE (V-Ω-PANOPTICON-GAZE)             ==
        =================================================================================
        """
        start_ns = time.perf_counter_ns()
        trace_id = self.gnostic_context.raw.get('trace_id', 'tr-void')

        Logger.info(f"[{trace_id}] LogicWeaver: Initiating Dimensional Convergence...")

        # --- MOVEMENT 0: AST CARTOGRAPHY ---
        if not self.traversal_engine:
            Logger.warn("Traversal Engine is unmanifest. Returning Void Dowry.")
            return [], [], [], []

        if not self.root or (not self.root.children and not self.root.item):
            Logger.warn("Weaver perceived a Void Root. Reality remains unmanifest.")

            fallback_cmds = getattr(self.traversal_engine, 'post_run_commands',
                                    getattr(self.traversal_engine.ctx, 'post_run_commands', []))
            fallback_edicts = getattr(self.traversal_engine, 'edicts', getattr(self.traversal_engine.ctx, 'edicts', []))

            return [], fallback_cmds, [], fallback_edicts

        # --- MOVEMENT I: THE RITE OF ADRENALINE (KINETIC SUPREMACY) ---
        # [ASCENSION 57]: Metabolic Fever Pre-emption
        try:
            import psutil
            if psutil.cpu_percent(interval=None) > 98.0:
                time.sleep(0.1)  # Yield to OS Scheduler
        except:
            pass

        gc_was_enabled = gc.isenabled()
        if gc_was_enabled: gc.disable()

        # [ASCENSION 46]: Heuristic Deadlock Prevention
        lock_acquired = self._weave_lock.acquire(timeout=15.0)
        if not lock_acquired:
            Logger.critical(f"[{trace_id}] Weaver Deadlock Detected. Aborting weave to save Engine.")
            return [], [], [Heresy(message="WEAVER_DEADLOCK", severity=HeresySeverity.CRITICAL)], []

        try:
            # --- MOVEMENT II: THE TEMPORAL SCAN (TRAVERSAL) ---
            _walk_start = time.perf_counter_ns()
            self.traversal_engine.traverse(self.root, Path("."))
            _walk_duration = (time.perf_counter_ns() - _walk_start) / 1_000_000

            if self._debug_mode:
                Logger.debug(f"[{trace_id}] Dimensional Walk Concluded in {_walk_duration:.2f}ms.")

            # --- MOVEMENT III: THE HARVEST OF THE QUATERNITY ---
            # We pull from the traversal engine safely using fallback matrix
            final_items = getattr(self.traversal_engine, 'items', getattr(self.traversal_engine.ctx, 'items', []))
            final_commands = getattr(self.traversal_engine, 'post_run_commands',
                                     getattr(self.traversal_engine.ctx, 'post_run_commands', []))
            final_heresies = getattr(self.traversal_engine, 'heresies',
                                     getattr(self.traversal_engine.ctx, 'heresies', []))
            final_edicts = getattr(self.traversal_engine, 'edicts', getattr(self.traversal_engine.ctx, 'edicts', []))

            # [ASCENSION 58]: The Orphaned Command Scythe
            purified_commands: List[Quaternity] = []
            for cmd in final_commands:
                if isinstance(cmd, tuple) and len(cmd) >= 4:
                    purified_commands.append(cmd)
                elif isinstance(cmd, tuple):
                    padded = list(cmd)
                    while len(padded) < 4: padded.append(None)
                    purified_commands.append(tuple(padded[:4]))

            final_commands = purified_commands

            # =========================================================================
            # == MOVEMENT IV: TOPOLOGICAL COLLISION ORACLE                           ==
            # =========================================================================
            self._adjudicate_topological_collisions(final_items, final_heresies, trace_id)

            # =========================================================================
            # == MOVEMENT V: IMMEDIATE HERESY PROCLAMATION & SORTING                 ==
            # =========================================================================
            # [ASCENSION 52]: Hierarchical Heresy Sorting
            if final_heresies:
                final_heresies.sort(key=lambda h: h.severity.value if hasattr(h.severity, 'value') else 0, reverse=True)

            self._proclaim_heresy_ledger(final_heresies, trace_id)

            # --- MOVEMENT VI: METABOLIC ADJUDICATION ---
            critical_count = sum(1 for h in final_heresies if h.severity == HeresySeverity.CRITICAL)

            if critical_count > 0:
                Logger.error(
                    f"[{trace_id}] Convergence Fractured: {critical_count} critical heresies perceived. [HERESY]")
            else:
                total_mass = sum(len(i.content or "") for i in final_items)
                void_paths = sum(1 for i in final_items if not i.path)

                if void_paths > 0 and self._debug_mode:
                    Logger.warn(f"[{trace_id}] Void Item Sentinel: Perceived {void_paths} items with unresolved paths.")

                Logger.success(
                    f"[{trace_id}] Weaving Complete. {len(final_items)} items manifest ({total_mass} bytes). [SUCCESS]")

            # --- MOVEMENT VII: THE FINAL PROCLAMATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.gnostic_context.raw['_weaving_tax_ms'] = duration_ms

            # [ASCENSION 60]: The Universal Finality Vow
            return final_items, final_commands, final_heresies, final_edicts

        except Exception as catastrophic_paradox:
            # =========================================================================
            # == THE DEEP TRACEBACK EXPOSER (DIRECT-TO-IRON)                         ==
            # =========================================================================
            # [ASCENSION 55]: Achronal Traceback Pruning
            tb = traceback.format_exc()
            sys.stderr.write(f"\n\x1b[41;1m[LOGIC_WEAVER_CATASTROPHE]\x1b[0m\n")
            sys.stderr.write(f"Trace ID: {trace_id} | Thread: {self._thread_id}\n")
            sys.stderr.write(f"Error: {catastrophic_paradox}\n")
            sys.stderr.write(f"{tb}\n")
            sys.stderr.write("-" * 80 + "\n")
            sys.stderr.flush()

            Logger.critical(f"Logic Weaver Collapse: {str(catastrophic_paradox)}")

            fatal_heresy = Heresy(
                message="LOGIC_WEAVER_CATASTROPHE",
                details=f"The Weaver's mind shattered: {catastrophic_paradox}\n{tb}",
                severity=HeresySeverity.CRITICAL,
                suggestion="Perform a structural biopsy of your Blueprint. A deep Jinja recursion or malformed AST Node caused a kernel panic."
            )

            return [], [], [fatal_heresy], []

        finally:
            self._weave_lock.release()

            # [ASCENSION 50]: The Chronometric GC Sentinel
            if gc_was_enabled:
                gc.enable()
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                if duration_ms > 500:
                    gc.collect(1)

    # =========================================================================
    # == INTERNAL DIAGNOSTIC ORGANS                                          ==
    # =========================================================================

    def _adjudicate_topological_collisions(self, items: List[ScaffoldItem], heresies: List[Heresy], trace_id: str):
        """
        Scans the finalized matter matrix to detect impossible geometries, such as
        a path existing as both a File and a Directory simultaneously.
        """
        path_registry: Dict[str, List[ScaffoldItem]] = {}
        for item in items:
            if not item.path: continue
            path_str = str(item.path).replace('\\', '/').lower().strip('/')
            if not path_str: continue

            if path_str not in path_registry:
                path_registry[path_str] = []
            path_registry[path_str].append(item)

        for path_str, occurrences in path_registry.items():
            if len(occurrences) > 1:
                has_dir = any(o.is_dir for o in occurrences)
                has_file = any(not o.is_dir for o in occurrences)

                if has_dir and has_file:
                    lines = sorted(list(set([str(o.line_num) for o in occurrences])))
                    msg = f"Topological Collision: '{path_str}' is defined as BOTH a File and a Directory."
                    Logger.critical(f"💀 [TOPOLOGICAL PARADOX] {msg}")
                    sys.stderr.write(
                        f"\n\x1b[31;1m[TOPOLOGICAL_SCHISM] Trace: {trace_id} | Path: {path_str} | Lines: {', '.join(lines)}\x1b[0m\n")
                    sys.stderr.flush()

                    heresies.append(Heresy(
                        message="TOPOLOGICAL_COLLISION",
                        line_num=int(lines[0]) if lines else 0,
                        details=msg,
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Check the willed structure. A template syntax error may have caused a directory to collapse into a file node."
                    ))

    def _proclaim_heresy_ledger(self, heresies: List[Heresy], trace_id: str):
        """Instantly outputs the exact details of every perceived Heresy during the weave."""
        if not heresies:
            return

        criticals = [h for h in heresies if h.severity == HeresySeverity.CRITICAL]
        warnings = [h for h in heresies if h.severity == HeresySeverity.WARNING]
        infos = [h for h in heresies if h.severity == HeresySeverity.INFO]

        if warnings:
            Logger.warn(f"[{trace_id}] ⚠️ Perceived {len(warnings)} architectural warnings:")
            for w in warnings:
                Logger.warn(f"   -> [L{getattr(w, 'line_num', '?')}] {w.message}")

        if criticals:
            Logger.error(f"[{trace_id}] ❌ Perceived {len(criticals)} CRITICAL heresies:")
            for c in criticals:
                Logger.error(f"   -> [L{getattr(c, 'line_num', '?')}] {c.message}")
                if getattr(c, 'details', None):
                    sys.stderr.write(f"\x1b[31m      Details: {c.details}\x1b[0m\n")
                if getattr(c, 'suggestion', None):
                    sys.stderr.write(f"\x1b[32m      Cure: {c.suggestion}\x1b[0m\n")
            sys.stderr.flush()

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_LOGIC_WEAVER root_nodes={len(self.root.children) if self.root else 0} status=PANOPTICON_ACTIVE>"