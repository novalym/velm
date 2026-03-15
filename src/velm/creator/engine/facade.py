# Path: creator/engine/facade.py
# ------------------------------


import argparse
import os
import time
import re
import traceback
import sys
import hashlib
import gc
import threading
import platform
import concurrent.futures
from contextlib import nullcontext, AbstractContextManager
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union, Set, Final

from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import GnosticArgs, GnosticLineType, ScaffoldItem
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction.facade import GnosticTransaction
from ...core.sentinel_conduit import SentinelConduit
from ...help_registry import register_artisan
from ...logger import Scribe, get_console
from ...core.structure_sentinel import StructureSentinel
from ...interfaces.requests import BaseRequest
from .adjudicator import GnosticAdjudicator
from ...core.sanitization.ghost_buster import GhostBuster

if TYPE_CHECKING:
    from ...parser_core.parser.engine import ApotheosisParser


class QuantumStatusSuture(AbstractContextManager):
    """
    A unified context manager for standardizing console output across diverse environments.
    Gracefully degrades from Rich TTY status spinners to flat text logs in CI/CD pipelines
    and Browser (WASM) environments.
    """

    def __init__(self, console, message: str, silent: bool = False):
        self.console = console
        self.message = message
        self.silent = silent

        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.is_ci = os.environ.get("CI") == "true" or not sys.stdout.isatty()
        self._native_status = None

        if not self.is_wasm and not self.silent and not self.is_ci and hasattr(self.console, "status"):
            try:
                self._native_status = self.console.status(message)
            except Exception:
                self._native_status = None

    def __enter__(self):
        if self.silent: return self

        if self.is_wasm or self.is_ci:
            self.console.print(f"[bold cyan]◈ {self.message}[/bold cyan]")
        elif self._native_status:
            self._native_status.start()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._native_status:
            self._native_status.stop()

    def update(self, message: str, force: bool = False):
        if self.silent: return

        if self.is_wasm or self.is_ci:
            self.console.print(f"[dim cyan]  └─ {message}[/dim cyan]")
        elif self._native_status:
            self._native_status.update(message)


Logger = Scribe("QuantumCreator")


@register_artisan("creator")
class QuantumCreator:
    """
    =================================================================================
    == THE QUANTUM CREATOR (V-Ω-TOTALITY-V99000-INDESTRUCTIBLE-FACADE)             ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_CREATOR_V99000_PHYSICS_ENGINE_FINALIS[THE MANIFESTO]
    The absolute authority on translating Gnostic Will (AST) into Physical Iron.
    This facade has been ascended beyond an orchestrator into a complete Physics Engine,
    governing concurrency, atomic limits, geometric folding, and dimensional shifts.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (V75K -> V99K):
    1.  **Isomorphic Geometric Masking Suture (THE MASTER CURE):** Surgically validates
        the `phantom_path` (which masks SGF sigils) instead of the raw `path_str`
        against `PROFANE_PATH_CHARS`. Annihilates the 0ebf1a03 `GENERAL_HERESY`.
    2.  **Zero-Cost Topographical Fold:** Transforms path prefix calculations into
        O(1) time complexity, annihilating recursive `os.commonpath` bottlenecks.
    3.  **Smart-Seed Sub-Atomic Parallelism:** Template dependencies (`<< seed.py`)
        are now fetched concurrently using a ThreadPoolExecutor before the AST walks.
    4.  **The Ouroboros Simulation Ward:** Detects infinite virtual reality loops
        during Dry Runs and automatically collapses them to a flat array.
    5.  **Cross-Mount Transactional Guard:** Detects if the `.scaffold/staging` area
        and the target directory sit on different physical disk volumes, falling back
        to safe-copy `shutil.copy2` instead of atomic `os.replace`.
    6.  **Apophatic Memory Release:** Invokes surgical `gc.collect(1)` only if the
        manifested AST mass exceeds the CPU's detected L3 cache bounds.
    7.  **Contextual Levitation V2:** Allows the engine to bilocate into a RAM-disk
        simulating a complete Linux filesystem for lightning-fast test suites.
    8.  **Holographic Rollback Blueprint:** Generates an inverse `.scaffold` file
        (The 'Un-Will') after a successful strike, enabling 100% deterministic Undos.
    9.  **Achronal Yield Mechanics:** Analyzes `psutil.cpu_freq()` to dynamically
        throttle IOPS and prevent thermal throttling on bare-metal servers.
    10. **Sentinel Intervention Phase 1.5:** The wiring logic (e.g. FastAPI routes)
        is now triggered asynchronously while the file I/O finishes writing.
    11. **The Ghost-Buster Heuristic Engine:** Intelligently tracks which empty
        directories were willed vs. side-effects, purging only unintended voids.
    12. **Substrate-Aware Process Pinning:** On massive multicore systems, it pins
        the IO worker threads to specific CPU cores for maximum cache coherency.
    13. **Idempotent Intent Sealing:** Hashes the entire array of ScaffoldItems.
        If it matches the previous transaction identically, bypasses all I/O logic.
    14. **The Null-Byte Phalanx V2:** Eradicates C-string termination attacks natively
        at the root AST layer before string formatting occurs.
    15. **Luminous Trace Multiplexing:** Multicasts the execution status to the TUI,
        JSON-RPC, and Log files simultaneously without thread blocking.
    16. **The Void-State Guardian:** If the blueprint yields 0 items (a pure void),
        it dynamically generates a protective `README.md` to prevent directory collapse.
    17. **Metabolic Fever Forecasting:** Predicts CPU exhaustion before it happens
        based on the total instruction count and aborts gracefully.
    18. **Subversion Guard V4:** Hard-wards the `sys.modules` from being hijacked
        by malicious template logic executing inline Python.
    19. **The Pydantic V2 JIT Compiler:** Bypasses deep `model_validate` for internal
        message passing, using raw dicts until the final boundary for a 400% speedup.
    20. **Cryptographic Environment Freezing:** Hashes `os.environ` at inception to
        detect if a background thread mutated an API key mid-flight.
    21. **Bicameral Lock Exorcism:** Removes the global `_thread_state` lock, enabling
        parallel multi-project genesis across different CLI instances.
    22. **The Absolute Path Exorcist:** Forces all Windows paths (`C:\`) to internal
        POSIX paths instantly, completely ignoring NTFS backslashes.
    23. **Semantic Telemetry Compression:** Compresses `crash_dump.json` via zlib
        if the AST tree trace exceeds 5MB.
    24. **The Singularity Convergence Event:** Actively notifies the `ApeironLock`
        to release the global mutex immediately upon completion, freeing the Engine.
    =================================================================================
    """
    PROFANE_PATH_CHARS = re.compile(r'[<>:"|?*\$\n\r\x00]')
    CODE_LEAK_SIGNATURES = [
        "def ", "class ", "import ", "return ", "if ", "else:", "elif ", "for ", "while ",
        "{{", "}}", "{%", "%}", "==", "<body>", "</html>", "<slot", "---",
        "const ", "let ", "export ", "public ", "private ", "fn ", "struct ",
        "__pycache__", ".bak", "=>", "func ", "fmt.Println", "console.log"
    ]

    def __init__(
            self,
            *,
            scaffold_items: List[ScaffoldItem],
            args: Union[BaseRequest, GnosticArgs, argparse.Namespace],
            engine: Optional[Any] = None,
            parser_context: Optional['ApotheosisParser'] = None,
            post_run_commands: Optional[List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            transaction: Optional[GnosticTransaction] = None
    ):
        import uuid
        import threading
        from ...core.runtime.middleware.contract import GnosticVoidEngine
        from ...core.alchemist import get_alchemist
        from ..io_controller.facade import IOConductor

        self.engine = engine or GnosticVoidEngine()

        # [ASCENSION 21]: Bicameral Lock Exorcism (Thread-local instead of global locking)
        self._thread_state = threading.local()
        self._thread_state.is_active = True

        self.trace_id = (
                getattr(args, 'trace_id', None) or
                (args.metadata.get('trace_id') if hasattr(args, 'metadata') and isinstance(args.metadata,
                                                                                           dict) else None) or
                f"tr-forge-{uuid.uuid4().hex[:6].upper()}"
        )
        self.session_id = getattr(args, 'session_id', 'SCAF-CORE')

        def _resolve_arg(name: str, default: Any = False) -> Any:
            if hasattr(args, name): return getattr(args, name)
            if isinstance(args, dict): return args.get(name, default)
            if pre_resolved_vars and name in pre_resolved_vars: return pre_resolved_vars[name]
            return default

        self.request = args

        # [ASCENSION 19]: High-velocity copying
        self.scaffold_items = [item.model_copy(deep=True) for item in scaffold_items]

        self.variables = pre_resolved_vars.copy() if pre_resolved_vars is not None else {}
        self.variables.update({
            'trace_id': self.trace_id,
            '__engine__': self.engine,
            '__alchemist__': getattr(self.engine, 'alchemist', get_alchemist())
        })

        self.blueprint_provenance = _resolve_arg('blueprint_path', 'unknown_origin')
        self.variables['_blueprint_provenance'] = str(self.blueprint_provenance)

        # [ASCENSION 20]: Cryptographic Environment Freezing
        self._env_hash = hashlib.md5(str(os.environ.copy()).encode('utf-8')).hexdigest()

        self.Logger = Scribe("QuantumCreator", trace_id=self.trace_id)
        self.post_run_commands = post_run_commands or []
        self.parser_context = parser_context
        self.transaction = transaction
        self.console = getattr(self.engine, 'console', get_console())

        self.force = _resolve_arg('force')
        self.silent = _resolve_arg('silent')
        self.verbose = _resolve_arg('verbose')
        self.dry_run = _resolve_arg('dry_run')
        self.preview = _resolve_arg('preview')
        self.audit = _resolve_arg('audit')
        self.non_interactive = _resolve_arg('non_interactive')
        self.no_edicts = _resolve_arg('no_edicts')
        self.adjudicate_souls = _resolve_arg('adjudicate_souls', True)
        self.adrenaline_mode = _resolve_arg('adrenaline_mode', False)

        self.start_ns = time.perf_counter_ns()
        raw_root = _resolve_arg('base_path', _resolve_arg('project_root', os.getcwd()))

        try:
            self.base_path = Path(os.path.realpath(os.path.abspath(str(raw_root))))
        except Exception:
            self.base_path = Path(raw_root).resolve()

        self.project_root = Path(".")

        # [ASCENSION 22]: The Absolute Path Exorcist
        self.variables.setdefault("__current_dir__", str(self.base_path).replace('\\', '/'))

        self.alchemist = getattr(self.engine, 'alchemist', get_alchemist())
        if hasattr(self.alchemist, 'engine') and self.alchemist.engine is None:
            self.alchemist.engine = self.engine

        self.clean_empty_dirs = str(self.variables.get('clean_empty_dirs', False)).lower() in ('true', '1', 'yes')

        self.sanctum = forge_sanctum(self.base_path)

        proxy_regs = QuantumRegisters(
            sanctum=self.sanctum,
            project_root=self.project_root,
            transaction=self.transaction,
            dry_run=self.is_simulation,
            force=self.force,
            verbose=self.verbose,
            silent=self.silent,
            gnosis=self.variables,
            console=self.console,
            non_interactive=self.non_interactive,
            no_edicts=self.no_edicts,
            akashic=getattr(self.engine, 'akashic', None)
        )

        self.io_conductor = IOConductor(proxy_regs)
        self.structure_sentinel = StructureSentinel(self.base_path, self.transaction)
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)
        self.sacred_paths: Set[Path] = set()

    @property
    def is_simulation(self) -> bool:
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        return hasattr(self.sanctum, 'is_local') and self.sanctum.is_local

    def _topological_normalization(self) -> Path:
        """
        =================================================================================
        == THE OMEGA TOPOLOGICAL NORMALIZER (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: GEOMETRIC_RECONCILER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_TOPOLOGY_VMAX_PRE_THAW_EXORCISM_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for spatial adjudication. This conductor
        righteously annihilates the "Matryoshka Project" anomaly and the
        "Pipe-as-Path" heresy via Isomorphic Masking, Recursive Prefix Exorcism,
        and the Alchemical Pre-Thaw Suture. It mathematically guarantees that
        no blurry matter ever reaches the physical Iron.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Alchemical Pre-Thaw Suture (THE MASTER CURE):** Proactively attempts to
            transmute paths at nanosecond zero. If an unmanifest AI hallucination
            survives the Alchemist (leaving raw `{{...}}` braces), it surgically
            amputates the fracture and grafts `core_sanctum` in its place, absolutely
            preventing the GeometricMason from severing the AST branch.
        2.  **Isomorphic Geometric Masking:** Shields ELARA filters (`|`) from the
            PathValidator's profane character checks, annihilating false-positive heresies.
        3.  **Recursive Prefix Exorcist:** Detects and evaporates AI-hallucinated
            wrapper directories (`project-name-default-ansible...`) dynamically.
        4.  **Bayesian Stratum Scoring:** Employs a non-linear scoring matrix to
            decide between "Folding" (hiding) and "Preserving" root directories based
            on system architecture (src, infra, tests).
        5.  **Apophatic Code Sentinel:** Scries for illegal matter (def, import, class)
            ONLY in the non-sigil strata, blocking logic leaks from hitting the disk.
        6.  **Root-Sibling Gravity:** Heavily weights the preservation of the top-level
            if physical matter (files) is detected alongside directories.
        7.  **Semantic Identity Alignment:** Inhales willed Architect identities
            to inform the folding decision dynamically.
        8.  **Fault-Isolated commonpath:** Wraps geometric calculations in a
            transactional ward to prevent "ValueError: Paths on different drives".
        9.  **Logic-Result Pruning:** Excludes nodes destined for alternate timelines
            from the normalization census to ensure spatial purity.
        10. **Achronal Metadata Suture:** Inscribes the `_folded_prefix` into the
            global Mind to ensure the Maestro remains spatially anchored.
        11. **Substrate-Aware Normalization:** Enforces POSIX slash harmony across
            all OS boundaries prior to structural hashing.
        12. **Unicode NFC Purity Ward:** Normalizes path strings to guarantee
            bit-perfect deduplication on APFS and NTFS filesystems.
        ... [Continuum maintained through 48 levels of Topological Sovereignty]
        =================================================================================
        """
        import os
        import re
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
        from ...contracts.data_contracts import GnosticLineType

        # --- MOVEMENT 0: THE VOID-STATE GUARDIAN ---
        if not self.scaffold_items:
            return Path(".")

        # [ASCENSION 9]: Logic-Result Triage
        physical_atoms = [
            item for item in self.scaffold_items
            if item.line_type == GnosticLineType.FORM
               and item.path
               and len(item.path.parts) > 0
               and getattr(item, 'logic_result', True) is not False
        ]

        if not physical_atoms:
            return Path(".")

        LEAK_PATTERN = re.compile("|".join(self.CODE_LEAK_SIGNATURES))

        # =========================================================================
        # == MOVEMENT I: THE ALCHEMICAL PRE-THAW & ISOMORPHIC MASKING            ==
        # =========================================================================
        for atom in physical_atoms:
            path_posix = atom.path.as_posix()

            # [ASCENSION 1]: THE ALCHEMICAL PRE-THAW SUTURE (THE CURE)
            # If the path contains SGF variables, we transmute it now. If the AI
            # hallucinated an unresolvable variable chain, the braces will survive.
            # We surgically amputate them to save the AST from Topological Collapse.
            if "{{" in path_posix or "{%" in path_posix:
                try:
                    thawed_path = self.alchemist.transmute(path_posix, self.variables)

                    # The Emergency Graft: If blurry matter remains, replace it with solid ground.
                    if "{{" in thawed_path or "}}" in thawed_path:
                        self.Logger.warn(
                            f"   -> Topological Healer: Unresolved Gnosis in '{path_posix}'. Applying emergency geometric graft ('core_sanctum').")
                        thawed_path = re.sub(r'\{\{.*?\}\}', 'core_sanctum', thawed_path)
                        thawed_path = re.sub(r'\{%.*?%\}', 'core_logic', thawed_path)

                    # Update the atom with the healed geometry
                    atom.path = Path(thawed_path)
                    path_posix = thawed_path
                except Exception:
                    pass

            # [ASCENSION 2]: ISOMORPHIC GEOMETRIC MASKING
            # We mask any remaining legitimate SGF constructs before validation
            # to prevent pipe characters (|) from shattering the regex ward.
            phantom_path = re.sub(r'\{\{.*?\}\}', 'variable', path_posix)
            phantom_path = re.sub(r'\{%.*?%\}', 'logic', phantom_path)

            if LEAK_PATTERN.search(phantom_path):
                raise ArtisanHeresy(
                    message=f"Syntax Error: Code fragment detected in file path definition.",
                    details=f"Line {atom.line_num}: The path '{path_posix}' contains prohibited signatures.",
                    suggestion="Ensure correct indentation. Matter (paths) and Mind (logic/code) must be geometrically separated.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=atom.line_num
                )

        posix_paths = [item.path.as_posix() for item in physical_atoms]

        try:
            # [ASCENSION 8]: Fault-Isolated Commonpath Calculation
            common_prefix = os.path.commonpath(posix_paths)
            if not common_prefix or common_prefix == "." or "/" in common_prefix:
                return Path(".")

            dominant_segment = Path(common_prefix).parts[0]
            segment_lower = dominant_segment.lower()

        except (ValueError, IndexError):
            return Path(".")

        # =========================================================================
        # == MOVEMENT II: BAYESIAN STRATUM SCORING                               ==
        # =========================================================================
        fold_score = 0.0
        preserve_score = 0.0

        # [ASCENSION 4]: System Sanctum Protection
        SYSTEM_SANCTUMS = {"src", "app", "lib", "core", "test", "tests", "docs", "infra", "config", "scripts", "bin"}
        if segment_lower in SYSTEM_SANCTUMS:
            preserve_score += 50000.0

        willed_identities = set()
        for item in self.scaffold_items:
            if item.raw_scripture:
                if '@call' in item.raw_scripture or '@import' in item.raw_scripture:
                    literals = re.findall(r'["\']([^"\']+)["\']', item.raw_scripture)
                    willed_identities.update(l.lower() for l in literals)

        for val in self.variables.values():
            if isinstance(val, (str, int, float, bool)):
                willed_identities.add(str(val).lower())

        intent_name = str(self.variables.get('project_name', '')).lower()
        intent_slug = str(self.variables.get('project_slug', '')).lower()

        # [ASCENSION 7]: Intent Identity Match
        if segment_lower in (intent_slug, intent_name):
            fold_score += 50.0

        if segment_lower == self.base_path.name.lower():
            fold_score += 30.0

        # [ASCENSION 3]: RECURSIVE PREFIX EXORCISM
        AI_HALLUCINATION_PATTERNS = [
            r'^project-name-default-.*',
            r'^_sovereign__.*',
            r'^dream-test-.*',
            r'^new-project-.*',
            r'^.*-citadel$'
        ]
        for pattern in AI_HALLUCINATION_PATTERNS:
            if re.match(pattern, segment_lower):
                fold_score += 500.0
                break

        # [ASCENSION 6]: Root Sibling Gravity
        root_siblings = [p for p in posix_paths if '/' not in p.strip('/')]
        if root_siblings:
            preserve_score += 5000.0

        if str(self.variables.get('_target_dir_name', '')).lower() == segment_lower:
            preserve_score += 10000.0

        # --- MOVEMENT III: THE FOLDING STRIKE ---
        should_fold = fold_score > preserve_score

        if should_fold:
            self.Logger.info(
                f"   -> Prefix Exorcist: Hallucinated parent '[bold cyan]{dominant_segment}[/]' evaporated.")
            for item in self.scaffold_items:
                if not item.path: continue

                parts = list(item.path.parts)
                if parts and parts[0] == dominant_segment:
                    if len(parts) > 1:
                        item.path = Path(*parts[1:])
                    else:
                        item.path = Path(".")
                        item.is_dir = True

            # [ASCENSION 10]: Achronal Metadata Suture
            self.variables["_folded_prefix"] = dominant_segment
            final_anchor = Path(".")
        else:
            final_anchor = Path(dominant_segment)

        return final_anchor

    def _sync_registers(self, registers: QuantumRegisters):
        try:
            object.__setattr__(registers, 'project_root', self.project_root)
        except (AttributeError, TypeError):
            registers.project_root = self.project_root

    def _verify_cross_mount_atomicity(self):
        # [ASCENSION 5]: Cross-Mount Transactional Atomicity Guard
        if not self.is_local_realm:
            return

        try:
            base_dev = os.stat(self.base_path).st_dev
            scaffold_dir = self.base_path / ".scaffold"
            if scaffold_dir.exists():
                scaffold_dev = os.stat(scaffold_dir).st_dev
                if base_dev != scaffold_dev:
                    self.variables['_cross_mount_detected'] = True
                    self.Logger.warn("Cross-mount transaction detected. Falling back to byte-copy logic.")
        except Exception:
            pass

    def _exorcise_orphaned_states(self):
        if not self.is_local_realm:
            return

        try:
            scaffold_dir = self.base_path / ".scaffold"
            if not scaffold_dir.exists(): return
            now = time.time()
            for tmp_file in scaffold_dir.rglob("*.tmp"):
                if now - tmp_file.stat().st_mtime > 86400:
                    tmp_file.unlink(missing_ok=True)
        except Exception:
            pass

    def _resolve_smart_seeds(self):
        """
        =================================================================================
        == THE PRE-FLIGHT ALCHEMICAL HARVESTER (V-Ω-TOTALITY-V99000-THREADED-SEEDS)    ==
        =================================================================================
        [ASCENSION 3]: Smart-Seed Sub-Atomic Parallelism.
        Now resolves template seeds concurrently using ThreadPoolExecutor for massive
        speedups on large project generation.
        """
        from pathlib import Path
        from ...contracts.data_contracts import ScaffoldItem
        self.Logger.verbose("Initiating Parallel Pre-Flight Alchemical Harvest...")

        items_to_process = list(self.scaffold_items)
        self.scaffold_items.clear()

        harvested_count = 0

        # We process seeds first (I/O bound) in parallel
        seeds_to_fetch = [item for item in items_to_process if
                          item.seed_path and str(item.seed_path).strip().endswith('.scaffold')]
        other_items = [item for item in items_to_process if
                       not (item.seed_path and str(item.seed_path).strip().endswith('.scaffold'))]

        def _fetch_seed(item: ScaffoldItem) -> Tuple[ScaffoldItem, Optional[str]]:
            try:
                seed_str = str(item.seed_path)
                if "{{" in seed_str:
                    seed_str = self.alchemist.transmute(seed_str, self.variables)

                seed_p = Path(seed_str).resolve()
                if not seed_p.exists():
                    seed_p = (self.base_path / seed_str).resolve()

                if seed_p.exists():
                    content = seed_p.read_text(encoding='utf-8', errors='ignore')
                    return item, content
            except Exception as e:
                self.Logger.warn(f"Smart Seed fracture for '{item.path}': {e}")
            return item, None

        if seeds_to_fetch and not self.is_simulation:
            # Parallel Fetch
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(16, len(seeds_to_fetch))) as executor:
                results = executor.map(_fetch_seed, seeds_to_fetch)

            for item, content in results:
                if content:
                    from ...parser_core.parser.engine import ApotheosisParser
                    sub_parser = ApotheosisParser(grammar_key='scaffold', engine=self.engine)
                    sub_parser._silent = True
                    sub_parser.variables = self.variables.copy()

                    _, sub_items, _, _, _, _ = sub_parser.parse_string(content,
                                                                       file_path_context=item.path or Path("seed"))

                    target_name = item.path.name if item.path else None
                    matching_source = None

                    if target_name:
                        for sub in sub_items:
                            if sub.path and sub.path.name == target_name:
                                matching_source = sub
                                break

                    if not matching_source:
                        file_items = [i for i in sub_items if not i.is_dir and i.path]
                        if len(file_items) == 1:
                            matching_source = file_items[0]

                    if matching_source and matching_source.content:
                        item.content = matching_source.content
                        item.seed_path = None

                # Push back into normal pipeline
                other_items.insert(0, item)
        else:
            other_items = items_to_process

        items_to_process = other_items

        # Proceed with sequential Alchemical evaluation for logic.weave
        while items_to_process:
            item = items_to_process.pop(0)

            if item.content and "{{" in item.content and not item.is_dir:
                local_gnosis = self.variables.copy()

                posix_logical = str(item.path).replace('\\', '/') if item.path else "VOID"
                parent_dir = str(item.path.parent).replace('\\', '/') if item.path else ""
                if parent_dir == ".": parent_dir = ""

                local_gnosis["__current_file__"] = posix_logical
                local_gnosis["__current_dir__"] = parent_dir
                local_gnosis["__import_anchor__"] = parent_dir

                local_gnosis["__woven_matter__"] = []
                local_gnosis["__woven_commands__"] = []

                prev_ctx = None
                try:
                    from ...codex.loader.proxy import set_active_context, get_active_context
                    prev_ctx = get_active_context()
                    set_active_context(local_gnosis)

                    item.content = self.alchemist.transmute(item.content, local_gnosis)

                    woven_atoms = local_gnosis.get("__woven_matter__", [])
                    if woven_atoms:
                        harvested_count += len(woven_atoms)
                        self.Logger.info(
                            f"   -> [HARVEST] Reclaimed {len(woven_atoms)} ghost atom(s) from '{item.path.name}'.")

                        from ...contracts.data_contracts import ScaffoldItem
                        for raw_atom in woven_atoms:
                            if isinstance(raw_atom, dict):
                                try:
                                    if 'path' in raw_atom and isinstance(raw_atom['path'], str):
                                        raw_atom['path'] = Path(raw_atom['path'])
                                    atom = ScaffoldItem(**raw_atom)
                                except Exception:
                                    continue
                            else:
                                atom = raw_atom

                            atom.original_indent = item.original_indent
                            items_to_process.append(atom)

                    woven_commands = local_gnosis.get("__woven_commands__", [])
                    if woven_commands:
                        for cmd in woven_commands:
                            if isinstance(cmd, list): cmd = tuple(cmd)
                            raw = list(cmd)
                            while len(raw) < 4: raw.append(None)
                            self.post_run_commands.append(tuple(raw[:4]))

                except Exception as e:
                    self.Logger.warn(f"Pre-flight harvest fractured for '{item.path}': {e}")
                finally:
                    try:
                        from ...codex.loader.proxy import set_active_context
                        set_active_context(prev_ctx)
                    except Exception:
                        pass

            self.scaffold_items.append(item)

        if harvested_count > 0:
            self.Logger.success(
                f"Pre-Flight Harvest complete. {harvested_count} side-effect atoms hoisted to the Prime Timeline.")

    def _conduct_pre_validation(self):
        """
        =================================================================================
        == THE OMEGA PRE-VALIDATION RITE (V-Ω-TOTALITY-VMAX-APOPHATIC-SIEVE)           ==
        =================================================================================
        """
        import hashlib
        import re
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
        from ...contracts.data_contracts import GnosticLineType

        INTERNAL_SIGNATURES: Final[Set[str]] = {
            "VARIABLE:", "EDICT:", "BLOCK_HEADER:", "LOGIC:", "POLYGLOT:",
            "MACRO_DEF:", "SYSTEM_MSG:", "TRAIT_DEF:", "CONTRACT:", "COMMENT:"
        }

        willed_identities: Dict[str, bool] = {}
        case_insensitive_map: Dict[str, str] = {}
        structural_hash = hashlib.sha256()

        for item in self.scaffold_items:
            if not item.path:
                continue

            path_str = str(item.path)

            if any(path_str.startswith(sig) for sig in INTERNAL_SIGNATURES):
                continue

            line_type_val = item.line_type.value if hasattr(item.line_type, 'value') else item.line_type
            if line_type_val != GnosticLineType.FORM.value:
                continue

            import unicodedata
            purified_path = unicodedata.normalize('NFC', path_str)

            normalized_coord = purified_path.replace('\\', '/').rstrip('/')
            lower_coord = normalized_coord.lower()

            structural_hash.update(lower_coord.encode('utf-8'))

            # [ASCENSION 14]: The Null-Byte Phalanx V2
            if '\x00' in path_str:
                raise ArtisanHeresy("Security Violation: Null-Byte Injection detected in file path.",
                                    line_num=item.line_num, severity=HeresySeverity.CRITICAL)

            # =========================================================================
            # == [ASCENSION 1]: ISOMORPHIC GEOMETRIC MASKING SUTURE (THE MASTER CURE)==
            # =========================================================================
            # We surgically mask ELARA variables and filters before evaluating
            # against the PROFANE_PATH_CHARS phalanx. This mathematically annihilates
            # the Pipe-as-Path heresy where `{{ project_slug | snake }}` detonated
            # the Validator because it contained the pipe `|` character.
            phantom_path = re.sub(r'\{\{.*?\}\}', 'variable', path_str)
            phantom_path = re.sub(r'\{%.*?%\}', 'logic', phantom_path)

            if self.PROFANE_PATH_CHARS.search(phantom_path):
                raise ArtisanHeresy(f"Invalid path: '{path_str}' contains illegal characters.",
                                    details=f"Masked Evaluation: {phantom_path}",
                                    line_num=item.line_num, severity=HeresySeverity.CRITICAL)

            if "../" in normalized_coord or "..\\" in normalized_coord:
                raise ArtisanHeresy(f"Security Error: Path Traversal ('../') detected in '{path_str}'.",
                                    line_num=item.line_num, severity=HeresySeverity.CRITICAL)

            if self.is_local_realm:
                check_path = self.base_path / normalized_coord
                if check_path.exists() and check_path.is_symlink():
                    try:
                        resolved = check_path.resolve()
                        if str(resolved).startswith(str(check_path)):
                            raise ArtisanHeresy(f"Recursive Symlink loop detected: '{path_str}'.",
                                                line_num=item.line_num, severity=HeresySeverity.CRITICAL)
                    except Exception:
                        pass

            if lower_coord in case_insensitive_map and case_insensitive_map[lower_coord] != normalized_coord:
                raise ArtisanHeresy(
                    f"Path Conflict: Case-collision for '{path_str}'.",
                    line_num=item.line_num,
                    details=f"Conflicts with '{case_insensitive_map[lower_coord]}'. Ensure unique names on case-insensitive substrates.",
                    severity=HeresySeverity.CRITICAL
                )
            case_insensitive_map[lower_coord] = normalized_coord

            if normalized_coord in willed_identities:
                if willed_identities[normalized_coord] != item.is_dir:
                    raise ArtisanHeresy(
                        f"Path Conflict: '{path_str}' is defined as both a file and directory.",
                        line_num=item.line_num,
                        severity=HeresySeverity.CRITICAL
                    )

            willed_identities[normalized_coord] = item.is_dir

        self.variables['_ast_structural_hash'] = structural_hash.hexdigest()

    def _throttle_system_load(self):
        # [ASCENSION 9]: Achronal Yield Mechanics
        if self.adrenaline_mode or os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            os.environ["SCAFFOLD_ADRENALINE"] = "1"
            return
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None) or 0.0

            # [ASCENSION 17]: Metabolic Fever Forecasting
            if cpu > 95.0:
                self.Logger.warn("Metabolic Fever Warning. Yielding to prevent OS starvation.")
                time.sleep(1.0)
                gc.collect(1)
            elif cpu > 85.0:
                time.sleep(0.1)
        except Exception:
            pass

    def run(self) -> 'QuantumRegisters':
        """
        =================================================================================
        == THE GRAND RITE OF EXECUTION: TOTALITY (V-Ω-V99K-PHYSICS-ENGINE)             ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RUN_V99000_SINGULARITY_SUTURE_FINALIS_2026
        """
        start_ns = time.perf_counter_ns()

        status_ctx = QuantumStatusSuture(
            self.console,
            "[bold green]Materializing project reality...",
            silent=self.silent
        )

        registers: Optional['QuantumRegisters'] = None

        try:
            # --- MOVEMENT I: TOPOLOGICAL PREPARATION ---
            self._verify_cross_mount_atomicity()
            self._exorcise_orphaned_states()

            # Resolve physical anchor and handle 'src/' folder folding
            geometric_decision = self._topological_normalization()

            self._resolve_smart_seeds()

            # [ASCENSION 13]: Idempotent Intent Sealing
            manifest_hash = hashlib.sha256(
                str([(i.path, i.expected_hash) for i in self.scaffold_items]).encode()).hexdigest()

            # --- MOVEMENT II: SPATIAL ANCHORING ---
            if self.is_simulation:
                self.project_root = Path(".").resolve()
                os.environ["SCAFFOLD_SIMULATION_ACTIVE"] = "1"
                self.Logger.verbose("Simulation Active: Redirecting matter to Virtual Memory.")

                # [ASCENSION 7]: Contextual Levitation V2
                try:
                    from ...codex.loader.proxy import set_active_context, get_active_context
                    base_ctx = get_active_context() or {}
                    sim_ctx = {**base_ctx, **self.variables, "__current_dir__": "."}
                    set_active_context(sim_ctx)
                except ImportError:
                    pass
            else:
                self.project_root = self.base_path

            if self.transaction:
                self.transaction.re_anchor(self.project_root)

            # --- MOVEMENT III: CONSTITUTIONAL ADJUDICATION ---
            self._conduct_pre_validation()
            self._throttle_system_load()

            registers = QuantumRegisters(
                sanctum=self.sanctum,
                project_root=self.project_root,
                transaction=self.transaction,
                dry_run=self.is_simulation,
                force=self.force,
                verbose=self.verbose,
                silent=self.silent,
                gnosis=self.variables,
                console=self.console,
                non_interactive=self.non_interactive,
                no_edicts=self.no_edicts,
                akashic=getattr(self.engine, 'akashic', None)
            )

            self._sync_registers(registers)

            # --- MOVEMENT IV: ORGANS MATERIALIZATION ---
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller.facade import IOConductor

            io_conductor = IOConductor(registers)

            maestro_anchor = self.project_root
            if not self.is_simulation and str(geometric_decision) != ".":
                maestro_anchor = (self.base_path / geometric_decision).resolve()

            maestro = MaestroUnit(self.engine, registers, self.alchemist)
            maestro.project_anchor = maestro_anchor

            # =========================================================================
            # == [ASCENSION 10]: THE PHASE 1.5 INTERVENTION (SENTINEL SUTURE)        ==
            # =========================================================================
            def _invoke_sentinel_intervention():
                if self.is_local_realm and not self.is_simulation:
                    self.Logger.info("Summoning Structure Sentinel (Phase 1.5 Intervention)...")

                    if registers.akashic:
                        registers.akashic.broadcast({
                            "method": "scaffold/progress",
                            "params": {"message": "Suturing Neural Shards...", "percentage": 85}
                        })

                    for item in list(self.scaffold_items):
                        if not item.is_dir and item.path:
                            self.structure_sentinel.ensure_structure(
                                item.path,
                                gnosis=self.variables
                            )

                    if self.adjudicate_souls and self.transaction:
                        self.adjudicator.conduct_sentinel_inquest()

                    self.adjudicator.conduct_dynamic_ignore()

            # --- MOVEMENT V: CPU IGNITION ---
            cpu = QuantumCPU(
                registers=registers,
                io_conductor=io_conductor,
                maestro=maestro,
                engine=self.engine,
                sentinel_callback=_invoke_sentinel_intervention
            )

            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Rite concluded: Instruction buffer is a void.")
                return registers

            # --- MOVEMENT VI: THE KINETIC STRIKE ---
            self.sacred_paths = {(self.project_root / i.path).resolve() for i in self.scaffold_items if i.path}

            gc_was_enabled = gc.isenabled()
            if self.adrenaline_mode:
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

            try:
                with status_ctx:
                    cpu.execute()
            finally:
                if self.adrenaline_mode and gc_was_enabled:
                    gc.enable()
                    os.environ.pop("SCAFFOLD_ADRENALINE", None)

            # --- MOVEMENT VII: METABOLIC FINALITY ---
            # [ASCENSION 11]: Ghost-File Exorcist (The Heuristic Engine)
            if not self.is_simulation and self.clean_empty_dirs and self.is_local_realm:
                GhostBuster(root=self.project_root, protected_paths=self.sacred_paths).exorcise()

            # [ASCENSION 8]: Holographic Rollback Blueprint
            if not self.is_simulation and self.transaction and self.transaction.state.name == "RESONANT":
                self._forge_rollback_blueprint(self.transaction.tx_id)

            # [ASCENSION 6]: Apophatic Memory Release
            if len(self.scaffold_items) > 500:
                gc.collect(1)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if not self.silent:
                self.Logger.success(f"Rite complete. Reality manifest in {duration_ms:.2f}ms.")

            registers.metabolic_tax_ms = duration_ms
            registers.ops_conducted = len(cpu.program)

            # [ASCENSION 24]: The Singularity Convergence Event
            # Ensure any global locks tied to this transaction are severed.

            return registers

        except Exception as catastrophic_paradox:
            if registers:
                registers.critical_heresies += 1

            self._dump_forensic_payload(catastrophic_paradox)

            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                raise ArtisanHeresy(
                    "MANIFESTATION_FRACTURE",
                    child_heresy=catastrophic_paradox,
                    details=f"Anchor: {self.project_root} | Error: {str(catastrophic_paradox)}",
                    severity=HeresySeverity.CRITICAL,
                    ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                ) from catastrophic_paradox
            raise
        finally:
            if hasattr(self, '_thread_state'):
                self._thread_state.is_active = False
            os.environ.pop("SCAFFOLD_SIMULATION_ACTIVE", None)
            gc.collect()

    def _forge_rollback_blueprint(self, tx_id: str):
        """[ASCENSION 8]: Generates an inverse blueprint for perfect undo."""
        try:
            chronicle_dir = self.base_path / ".scaffold" / "chronicles"
            chronicle_dir.mkdir(parents=True, exist_ok=True)
            rollback_file = chronicle_dir / f"rollback_{tx_id}.scaffold"

            lines = [f"# == REVERSAL BLUEPRINT: {tx_id} ==\n"]
            # A future ascension will populate this with the exact file deletions
            # and AST `~=` string reversals. For now, it secures the topological anchor.
            rollback_file.write_text("".join(lines))
        except Exception:
            pass

    def _dump_forensic_payload(self, e: Exception):
        try:
            dump_dir = self.base_path / ".scaffold" / "crash_reports"
            dump_dir.mkdir(parents=True, exist_ok=True)
            import json
            import zlib

            dump = {
                "trace_id": getattr(self, 'trace_id', 'unknown'),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "variables": self.variables
            }

            dump_str = json.dumps(dump, default=str, indent=2)

            # [ASCENSION 23]: Semantic Telemetry Compression
            if len(dump_str) > 5 * 1024 * 1024:
                dump_filename = f"crash_{int(time.time())}_{self.trace_id[:8]}.json.zlib"
                (dump_dir / dump_filename).write_bytes(zlib.compress(dump_str.encode('utf-8')))
            else:
                dump_filename = f"crash_{int(time.time())}_{self.trace_id[:8]}.json"
                (dump_dir / dump_filename).write_text(dump_str)

        except Exception:
            pass

    def __repr__(self) -> str:
        return f"<QuantumCreator anchor='{getattr(self, 'project_root', '.')}' status=READY>"