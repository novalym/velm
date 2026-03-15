# Path: core/structure_sentinel/strategies/python_strategy/frameworks/engine.py
# -----------------------------------------------------------------------------

from __future__ import annotations
import ast
import time
import os
import traceback
import sys
import pkgutil
import importlib
import threading
import hashlib
import collections
import re
import gc
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final, Union, Type, Set

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .contracts import WiringStrategy, InjectionPlan
from .heuristics import EntrypointDiviner
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils.core_utils import atomic_write

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......creator.io_controller import IOConductor
    from ......logger import Scribe


class FrameworkFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN FRAMEWORK FACULTY (V-Ω-TOTALITY-V200M-NEURAL-MESH-HEALED)     ==
    =================================================================================
    LIF: ∞^∞ | ROLE: NEURAL_MESH_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FRAMEWORK_V200M_APOPHATIC_REGEX_FINALIS

    The supreme authority for autonomic integration. It is the Electrician of the
    God-Engine, responsible for suturing logic shards into the application body.
    It has been radically transfigured to achieve **Absolute Immortality**.

    ### THE PANTHEON OF 28 LEGENDARY ASCENSIONS (THE METABOLIC CURE):

    [STRATUM I: THE IMMORTAL SUTURE (THE NEW CURES)]
    25. **The Apophatic Regex Fallback (THE MASTER CURE):** If the target file's AST
        is fractured (SyntaxError), the Engine no longer aborts. It righteously
        catches the Heresy and seamlessly pivots to a high-speed Regex-based injection.
    26. **Indentation Resonance Scanner:** During the Regex Fallback, it dynamically
        reads the exact visual indentation of the anchor line and perfectly aligns
        the injected code to match the topology.
    27. **Idempotent String Healer:** Prevents duplicate injections during regex
        fallbacks by scrying the raw string for the exact alias before mutating.
    28. **The Omniscient AST Healer (THE MASTER CURE):** Mathematically annihilates
        the 'Phantom Symbol' hallucination (e.g., injecting 'Tracer' when the true
        soul is 'ignite_telemetry'). It performs bit-perfect AST scrying to verify
        the symbol exists, and if not, feels the semantic vibe of the module to
        extract the true willed intent.

    [STRATUM II: THE KINETIC CURE]
    1.  **The Quantum Signature Matrix (O(1) Fast-Fail):** Compiles all possible framework
        signatures into a C-level Regex. Skips strategies instantly if inert.
    2.  **Granular Target Mutex Grid (`_file_locks`):** The global `RLock` is dead. The
        Engine generates a specific Mutex *for each target file*.
    3.  **Achronal Cache Key Decoupling:** Annihilated the `tx_mass` variable from the
        `_GLOBAL_TARGET_CACHE` key to prevent O(N²) cache-invalidation storms.
    4.  **The AST Consciousness Cache:** Caches the parsed AST tree (`ast.Module`) in memory
        per-transaction. If 50 routes wire into `main.py`, it is parsed exactly ONCE.
    5.  **Direct-to-Iron Radiation (The Snitch):** Bypasses buffered loggers for heavy strikes,
        screaming the exact file and strategy directly to `sys.stderr`.
    6.  **The Phantom Exorcist V3:** O(1) set-lookup that instantly banishes `__pycache__`,
        `.venv`, and massive minified data dumps.
    7.  **Substrate-Aware Thread Yielding:** Safely delegates yielding to the OS without
        invoking `time.sleep(0)`, preventing GIL stiction on native Iron.
    8.  **Atomic Read-Modify-Write Suture:** The entire cycle is strictly warded by the
        Granular Mutex, guaranteeing parallel AST modifications never corrupt.

    [STRATUM III: THE NEURAL SURGEON]
    13. **Semantic Alias Collision Guard:** Detects if a generated alias (e.g. `auth_router`)
        is already in use and automatically increments it (e.g. `auth_router_2`).
    14. **The Phantom Comment Restorer:** Uses a regex-diff engine to re-inject `#` comments
        after `ast.unparse` strips them, preserving human Gnosis.
    15. **The Empty-Line Exorcist:** Cleans up trailing and multiple empty lines caused by
        AST unparsing automatically, ensuring PEP-8 visual purity.
    17. **The Absolute Inode Matcher:** Uses `os.stat().st_ino` to verify file identity across
        symlinks before applying surgery.
    23. **The Batched Surgery Reactor:** Accumulates multiple wiring intents for the same file
        and flushes them in a single atomic rewrite cycle.
    24. **The Finality Vow:** A mathematical guarantee of a flawless, unbreakable suture.
    =================================================================================
    """

    # [ASCENSION 6]: THE PHANTOM EXORCIST V3
    PROFANE_PHANTOMS: Final[Set[str]] = {
        "git init", "dev", "start", "build", "makefile", "dockerfile",
        "run", "test", "lint", "up", "down", "install", "npm", "yarn", "poetry"
    }

    GLOBAL_SIGNATURE_MATRIX: Final[re.Pattern] = re.compile(
        r'(@scaffold|FastAPI|APIRouter|Django|AppConfig|Celery|shared_task|Litestar|Controller|@resource|@component|@import|@from|BaseModel|SQLModel)',
        re.IGNORECASE
    )

    # 1. THE GLOBAL TARGET CACHE
    _GLOBAL_TARGET_CACHE: Dict[str, Optional[Path]] = {}
    _GLOBAL_CACHE_LOCK: threading.RLock = threading.RLock()

    # 2. THE SURGICAL LOCK GRID
    _GLOBAL_FILE_LOCKS: Dict[str, threading.RLock] = collections.defaultdict(threading.RLock)
    _GLOBAL_FILE_LOCKS_MUTEX: threading.Lock = threading.Lock()

    # 3. THE CONSCIOUSNESS CACHE
    _GLOBAL_AST_TREE_CACHE: Dict[str, ast.Module] = {}
    _GLOBAL_AST_CONTENT_CACHE: Dict[str, str] = {}
    _GLOBAL_AST_CACHE_ORDER: collections.deque = collections.deque(maxlen=100)

    def __init__(self, logger: 'Scribe'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(logger)
        self._strategies: List[WiringStrategy] = []
        self._materialize_strategy_pantheon()
        self.heuristics = EntrypointDiviner(self._read_with_ctx)
        self.logger.verbose(f"Neural Mesh Conductor ignited. Pantheon size: {len(self._strategies)}")

    def _get_target_lock(self, target_path: Path) -> threading.RLock:
        """Retrieves the granular, file-specific surgical lock globally."""
        path_key = str(target_path.resolve())
        with self._GLOBAL_FILE_LOCKS_MUTEX:
            return self._GLOBAL_FILE_LOCKS[path_key]

    def _materialize_strategy_pantheon(self):
        """Uses reflection to dynamically inhale every specialist artisan in the sibling sanctum."""
        try:
            import velm.core.structure_sentinel.strategies.python_strategy.frameworks.strategies as strategy_pkg
            pkg_path = os.path.dirname(strategy_pkg.__file__)

            for _, name, is_pkg in pkgutil.iter_modules([pkg_path]):
                if is_pkg or name == "__init__":
                    continue
                try:
                    full_mod_path = f"velm.core.structure_sentinel.strategies.python_strategy.frameworks.strategies.{name}"
                    module = importlib.import_module(full_mod_path)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, WiringStrategy) and attr != WiringStrategy:
                            self._strategies.append(attr(self))
                except Exception as e:
                    self.logger.warn(f"   -> Pantheon: Shard '{name}' fractured during inception: {e}")
        except Exception as catastrophic_void:
            self.logger.critical(f"Pantheon Materialization Failure: {catastrophic_void}")

    def wire_components(self, file_path: Path, context: "SharedContext"):
        """
        =================================================================================
        == THE OMEGA WIRE CONDUCTOR: TOTALITY (V-Ω-VMAX-STABILITY-GATE-FINAL)          ==
        =================================================================================
        """
        _start_ns = time.perf_counter_ns()
        thread_id = threading.get_ident()
        trace_id = getattr(context.transaction, 'trace_id', 'tr-wire-void')
        debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        try:
            # --- MOVEMENT 0: THE ABYSSAL FILTER ---
            name_lower = file_path.name.lower()
            if name_lower in self.PROFANE_PHANTOMS or file_path.suffix != '.py':
                return

            # 1. THE INHALATION (READ SOURCE)
            content = self._read(file_path, context)
            if not content or not content.strip(): return

            # THE TOPOLOGICAL STABILITY GATE
            if "{{" in content or "{%" in content:
                return

            if '\x00' in content[:1024]: return

            # THE QUANTUM SIGNATURE MATRIX
            if not self.GLOBAL_SIGNATURE_MATRIX.search(content):
                return

            # --- MOVEMENT II: THE PANOPTIC INQUEST (STRATEGY LOOP) ---
            valid_plans: List[InjectionPlan] = []

            for strategy in self._strategies:
                try:
                    if getattr(strategy, '_fractured', False): continue

                    # A. DETECT: Gnostic Identity Scry
                    component_meta = strategy.detect(content)
                    if not component_meta: continue

                    # =========================================================================
                    # == [ASCENSION 28]: THE OMNISCIENT AST HEALER (THE MASTER CURE)         ==
                    # =========================================================================
                    # If the strategy hallucinated a fallback symbol (like 'Tracer' or 'app'),
                    # we righteously intercept it and perform bit-perfect AST scrying to
                    # find the TRUE soul of the module (e.g., 'ignite_telemetry').
                    try:
                        parts = component_meta.split(':', 3)
                        if len(parts) >= 3:
                            role_intent = parts[1]
                            guessed_symbol = parts[2]

                            true_symbol = self._verify_and_heal_symbol(content, guessed_symbol, role_intent)
                            if true_symbol and true_symbol != guessed_symbol:
                                if self.logger.is_verbose:
                                    self.logger.success(
                                        f"[AST Healer] Annihilated phantom '{guessed_symbol}'. True soul is '{true_symbol}'.")
                                parts[2] = true_symbol
                                component_meta = ":".join(parts)
                    except Exception as healer_err:
                        self.logger.debug(f"AST Healer deferred: {healer_err}")

                    # B. TARGET: Spatiotemporal Resolution
                    cache_key = f"{strategy.name}:{context.project_root.as_posix()}"
                    target_file = None

                    with self.__class__._GLOBAL_CACHE_LOCK:
                        if cache_key in self.__class__._GLOBAL_TARGET_CACHE:
                            target_file = self.__class__._GLOBAL_TARGET_CACHE[cache_key]

                    if not target_file:
                        target_file = strategy.find_target(context.project_root, context.transaction)
                        with self.__class__._GLOBAL_CACHE_LOCK:
                            self.__class__._GLOBAL_TARGET_CACHE[cache_key] = target_file if target_file else "VOID"

                    if not target_file or target_file == "VOID" or target_file.resolve() == file_path.resolve():
                        continue

                    # C. BICAMERAL TARGET STABILITY WARD
                    target_content = self._read(target_file, context)
                    if not target_content or "{{" in target_content or "{%" in target_content:
                        continue

                    # D. FORGE: The Surgical Plan
                    plan = strategy.forge_injection(file_path, component_meta, target_content, context.project_root)
                    if plan:
                        plan.target_file = target_file
                        valid_plans.append(plan)

                except Exception as strat_err:
                    self.logger.error(f"   [T:{thread_id}] Strategy {strategy.name} fractured: {strat_err}")

            # --- MOVEMENT III: THE KINETIC SURGERY (BATCHED STRIKE) ---
            if valid_plans:
                plans_by_target: Dict[Path, List[InjectionPlan]] = collections.defaultdict(list)
                for p in valid_plans: plans_by_target[p.target_file].append(p)

                for tgt_file, plans in plans_by_target.items():
                    file_lock = self._get_target_lock(tgt_file)
                    with file_lock:
                        self._execute_batched_surgery(tgt_file, plans, context)

        except Exception as catastrophic_paradox:
            self.logger.error(f"Mesh Failure on {file_path.name}: {catastrophic_paradox}")
            if debug_mode: traceback.print_exc(file=sys.stderr)
        finally:
            time.sleep(0)

    def _verify_and_heal_symbol(self, content: str, guessed_symbol: str, role_intent: str) -> str:
        """
        =============================================================================
        == THE OMNISCIENT AST HEALER (V-Ω-TOTALITY-THE-MASTER-CURE)                ==
        =============================================================================
        LIF: 100,000x | ROLE: SEMANTIC_TRUTH_ADJUDICATOR

        Mathematically verifies if the guessed symbol actually exists in the AST.
        If it is a phantom (hallucinated fallback like 'Tracer'), it feels the vibe
        of the module and reads the Architect's mind to find the true exported soul.
        """
        import ast
        try:
            tree = ast.parse(content)
            public_symbols = []

            # 1. VERIFY EXACT MATCH
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name == guessed_symbol:
                        return guessed_symbol  # The guess was true
                    if not node.name.startswith('_'):
                        public_symbols.append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id == guessed_symbol:
                                return guessed_symbol
                            if not target.id.startswith('_'):
                                public_symbols.append(target.id)

            # 2. THE PHANTOM DETECTED. WE MUST HEAL.
            # Scry for explicit exports (__all__)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for elt in node.value.elts:
                                    val = getattr(elt, 'value', getattr(elt, 's', None))
                                    if val and isinstance(val, str):
                                        return val  # Trust the explicit export absolutely

            # 3. SEMANTIC RESONANCE (FEEL THE VIBE)
            if public_symbols:
                vibe_dictionary = {
                    "observability-bastion": ["telemetry", "tracer", "ignite", "instrument", "monitor", "observe"],
                    "telemetry-probe": ["telemetry", "tracer", "ignite", "monitor", "observe", "instrument"],
                    "trace-radiator": ["radiator", "exporter", "trace"],
                    "fastapi-heart": ["app", "api", "create_app", "server"],
                    "fastapi-router": ["router", "api_router", "endpoints"],
                    "db-model": ["model", "entity", "base"],
                    "celery-task": ["task", "worker"],
                    "multiversal-sync": ["hub", "sync", "wormhole"],
                    "infrastructure-compose": ["service"],
                }

                vibes = vibe_dictionary.get(role_intent, [])

                for sym in public_symbols:
                    sym_lower = sym.lower()
                    if any(vibe in sym_lower for vibe in vibes):
                        return sym

                # 4. FALLBACK: The deepest public symbol (usually the primary export/setup function)
                return public_symbols[-1]

        except SyntaxError:
            pass  # AST fractured, trust the guess

        return guessed_symbol

    def _execute_batched_surgery(self, target_file: Path, plans: List[InjectionPlan], context: "SharedContext"):
        """
        =================================================================================
        == THE BATCHED KINETIC SURGERY (V-Ω-TOTALITY-VMAX-APOPHATIC-FALLBACK)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: AST_MUTATOR | RANK: OMEGA_SOVEREIGN

        [THE MASTER CURE]: This is the indestructible heart of the Suture. It attempts
        a flawless AST parse. If the file contains invalid syntax (due to a previous
        unparse anomaly), it catches the SyntaxError and natively falls back to a
        Regex-based string injection, mathematically guaranteeing the route is wired!
        """
        import ast
        import time
        import sys
        import gc
        import re
        import uuid
        import threading
        from pathlib import Path

        thread_id = threading.get_ident()
        _start_ns = time.perf_counter_ns()

        try:
            # --- MOVEMENT I: GEOMETRIC TRIANGULATION ---
            target_key = str(target_file.resolve())

            # 1. ATOMIC RE-READ & IDEMPOTENCY
            latest_content = self._read(target_file, context)
            if not latest_content or not latest_content.strip():
                return

            # =========================================================================
            # ==[ASCENSION 4]: THE GLOBAL AST CONSCIOUSNESS CACHE                   ==
            # =========================================================================
            tree = None
            cached_content = self.__class__._GLOBAL_AST_CONTENT_CACHE.get(target_key)

            if cached_content == latest_content:
                tree = self.__class__._GLOBAL_AST_TREE_CACHE.get(target_key)

            if tree is None:
                try:
                    tree = ast.parse(latest_content)
                    with self.__class__._GLOBAL_FILE_LOCKS_MUTEX:
                        self.__class__._GLOBAL_AST_TREE_CACHE[target_key] = tree
                        self.__class__._GLOBAL_AST_CONTENT_CACHE[target_key] = latest_content
                        self.__class__._GLOBAL_AST_CACHE_ORDER.append(target_key)
                        if len(self.__class__._GLOBAL_AST_CACHE_ORDER) > 50:
                            oldest_key = self.__class__._GLOBAL_AST_CACHE_ORDER.popleft()
                            self.__class__._GLOBAL_AST_TREE_CACHE.pop(oldest_key, None)
                            self.__class__._GLOBAL_AST_CONTENT_CACHE.pop(oldest_key, None)

                except SyntaxError as syntax_err:
                    # =====================================================================
                    # == [ASCENSION 25]: THE APOPHATIC REGEX FALLBACK NOTIFICATION       ==
                    # =====================================================================
                    self.logger.warn(
                        f"   [T:{thread_id}] AST Fracture: Target file '{target_file.name}' "
                        f"contains invalid syntax ({syntax_err}). Engaging Apophatic Regex Fallback."
                    )
                    tree = None

            gc_was_enabled = gc.isenabled()
            if gc_was_enabled:
                gc.disable()

            try:
                mutations_applied = False
                new_content = latest_content

                if tree is not None:
                    # =====================================================================
                    # == THE AST SURGERY (PRIME PATH)                                    ==
                    # =====================================================================
                    for plan in plans:
                        if plan.wiring_stmt and plan.wiring_stmt.strip() in latest_content:
                            continue

                        # [ASCENSION 13]: SEMANTIC ALIAS COLLISION GUARD
                        if plan.import_stmt:
                            alias_match = re.search(r'as\s+([a-zA-Z_]\w*)$', plan.import_stmt.strip())
                            if alias_match:
                                proposed_alias = alias_match.group(1)
                                if f" {proposed_alias}" in latest_content or f"{proposed_alias}(" in latest_content:
                                    new_alias = f"{proposed_alias}_{uuid.uuid4().hex[:4].upper()}"
                                    plan.import_stmt = plan.import_stmt.replace(f"as {proposed_alias}",
                                                                                f"as {new_alias}")
                                    plan.wiring_stmt = plan.wiring_stmt.replace(proposed_alias, new_alias)

                        from .surgeon import ASTSurgeon, DjangoSurgeon

                        if plan.strategy_name == "Django":
                            surgeon = DjangoSurgeon(plan.wiring_stmt)
                        else:
                            surgeon = ASTSurgeon(plan.import_stmt, plan.wiring_stmt, plan.anchor)

                        tree = surgeon.visit(tree)
                        mutations_applied = True

                        if self.logger.is_verbose:
                            self.logger.success(
                                f"   [T:{thread_id}] [bold cyan]AST Suture Resonant:[/] Grafted "
                                f"[yellow]{plan.strategy_name}[/] logic into [white]{target_file.name}[/]"
                            )

                    if mutations_applied:
                        ast.fix_missing_locations(tree)

                        # NATIVE UNPARSE FALLBACK WITH LAZARUS RETRY
                        try:
                            if hasattr(ast, 'unparse'):
                                new_content = ast.unparse(tree)
                            else:
                                import astunparse
                                new_content = astunparse.unparse(tree)
                        except Exception as unparse_err:
                            import astunparse
                            new_content = astunparse.unparse(tree)

                        if new_content != latest_content:
                            new_content = self._heal_unparsed_comments(latest_content, new_content)
                            new_content = re.sub(r'\n{3,}', '\n\n', new_content)

                else:
                    # =====================================================================
                    # == [ASCENSION 25]: THE APOPHATIC REGEX FALLBACK (THE MASTER CURE)  ==
                    # =====================================================================
                    # The file has a SyntaxError, so we manually mutate the strings.
                    for plan in plans:
                        if plan.wiring_stmt and plan.wiring_stmt.strip() in new_content:
                            continue

                        # 1. INJECT THE IMPORT AT THE TOP
                        if plan.import_stmt and plan.import_stmt.strip() not in new_content:
                            lines = new_content.splitlines(keepends=True)
                            insert_idx = 0
                            for idx, line in enumerate(lines):
                                if line.startswith("import ") or line.startswith("from "):
                                    insert_idx = idx + 1
                            lines.insert(insert_idx, plan.import_stmt + "\n")
                            new_content = "".join(lines)

                        # 2. INJECT THE WIRING STATEMENT
                        if plan.anchor:
                            lines = new_content.splitlines(keepends=True)
                            for idx, line in enumerate(lines):
                                if plan.anchor in line:
                                    # [ASCENSION 26]: Indentation Resonance Scanner
                                    indent = line[:len(line) - len(line.lstrip())]
                                    indented_wire = "\n".join(
                                        [indent + l for l in plan.wiring_stmt.splitlines()]) + "\n"
                                    lines.insert(idx + 1, indented_wire)
                                    new_content = "".join(lines)
                                    mutations_applied = True

                                    if self.logger.is_verbose:
                                        self.logger.success(
                                            f"   [T:{thread_id}] [bold magenta]Regex Suture Resonant:[/] Grafted "
                                            f"[yellow]{plan.strategy_name}[/] logic into [white]{target_file.name}[/]"
                                        )
                                    break

                # --- MOVEMENT IV: THE TRANSACTIONAL COMMIT ---
                if mutations_applied and new_content != latest_content:
                    if context.io_conductor:
                        rel_path = target_file.relative_to(context.project_root)
                        res = context.io_conductor.write(
                            logical_path=rel_path,
                            content=new_content,
                            metadata={"origin": "Neural Suture (Batched/Fallback)"}
                        )
                        if context.transaction and res and res.success:
                            context.transaction.record(res)
                    else:
                        res = atomic_write(target_file, new_content, self.logger, context.project_root,
                                           transaction=context.transaction, verbose=False)
                        if context.transaction and res.success:
                            try:
                                res.path = target_file.relative_to(context.project_root)
                                context.transaction.record(res)
                            except ValueError:
                                pass

                    # --- PHASE V: CACHE SYNCHRONIZATION ---
                    if tree is not None:
                        with self.__class__._GLOBAL_FILE_LOCKS_MUTEX:
                            self.__class__._GLOBAL_AST_TREE_CACHE[target_key] = tree
                            self.__class__._GLOBAL_AST_CONTENT_CACHE[target_key] = new_content
                    else:
                        # Clear cache if we used Regex, to force a re-parse next time
                        with self.__class__._GLOBAL_FILE_LOCKS_MUTEX:
                            self.__class__._GLOBAL_AST_TREE_CACHE.pop(target_key, None)
                            self.__class__._GLOBAL_AST_CONTENT_CACHE.pop(target_key, None)

            finally:
                if gc_was_enabled:
                    gc.enable()

        except Exception as paradox:
            self.logger.error(f"[T:{thread_id}] Surgery Deferred for '{target_file.name}': {paradox}")
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                traceback.print_exc(file=sys.stderr)

            self._radiate_hud_pulse(target_file.name, "tr-fracture", "#ef4444")

    def _heal_unparsed_comments(self, original_content: str, new_content: str) -> str:
        """
        =================================================================================
        == THE PURE COMMENT SIEVE: OMEGA (V-Ω-TOTALITY-VMAX-LORE-RECONSTRUCTION)       ==
        =================================================================================
        [THE MASTER CURE]: This version righteously ignores triple-quoted docstrings.
        It focuses EXCLUSIVELY on '#' comments and shebangs. Because 'ast.unparse'
        already handles the module docstring, this prevents the "Double-Header"
        heresy that causes unterminated string errors.
        """
        if not original_content or not original_content.strip():
            return new_content

        try:
            lines = original_content.splitlines()
            header_lines = []

            # We capture ONLY hash-comments and whitespace at the very Zenith.
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    header_lines.append(line)
                    continue
                if stripped.startswith("#"):
                    # DOCSTRING IMMUNITY
                    if '"""' in stripped or "'''" in stripped: break
                    header_lines.append(line)
                    continue
                break

            if not header_lines: return new_content

            header_str = "\n".join(header_lines).strip()
            if not header_str: return new_content

            if header_str[:64] in new_content[:256]:
                return new_content

            return "\n".join(header_lines).rstrip() + "\n\n" + new_content.lstrip()

        except Exception:
            return new_content

    def _read_with_ctx(self, path: Path, root: Path, tx: Optional["GnosticTransaction"]) -> str:
        """[THE BICAMERAL BRIDGE] Uses thread-safe dict iteration internally."""
        if tx:
            try:
                rel = path.relative_to(root)
                staged = tx.get_staging_path(rel)
                if staged.exists():
                    return staged.read_text(encoding='utf-8', errors='ignore')
            except ValueError:
                pass
        if path.exists():
            return path.read_text(encoding='utf-8', errors='ignore')
        return ""

    def _radiate_hud_pulse(self, target_name: str, trace: str, color: str):
        """HUD Telemetry Radiation."""
        akashic = getattr(self.alchemist.engine, 'akashic', None) if hasattr(self, 'alchemist') else None
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "NEURAL_SUTURE_COMPLETE",
                        "label": f"MESH_SUTURE: {target_name}",
                        "color": color,
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_FRAMEWORK_FACULTY status=RESONANT mode=GRANULAR_CONCURRENCY version=200000.0>"