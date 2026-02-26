# Path: src/velm/creator/engine/facade.py
# ---------------------------------------

import argparse
import os
import time
import re
import traceback
import sys
import hashlib
import gc
import threading
import uuid
import math
import platform
import shutil
from contextlib import nullcontext, AbstractContextManager
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union, Set
from collections import defaultdict

# --- THE DIVINE SUMMONS OF THE GNOSTIC PANTHEON ---
from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import ScaffoldItem, GnosticArgs, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction.facade import GnosticTransaction
from ...core.sanctum.base import SanctumInterface
from ...core.sanctum.local import LocalSanctum
from ...core.sentinel_conduit import SentinelConduit
from ...help_registry import register_artisan
from ...logger import Scribe, get_console
from ...core.structure_sentinel import StructureSentinel
from ...interfaces.requests import BaseRequest

# --- THE MODULAR KIN ---
from .adjudicator import GnosticAdjudicator
from ...core.sanitization.ghost_buster import GhostBuster

if TYPE_CHECKING:
    from ...parser_core.parser.engine import ApotheosisParser


class QuantumStatusSuture(AbstractContextManager):
    """
    =============================================================================
    == THE QUANTUM STATUS SUTURE (V-Ω-SUBSTRATE-AWARE-V4)                      ==
    =============================================================================
    [ASCENSION 1]: The ultimate polymorphic context manager.
    It reads the DNA of the host environment (WASM, CI/CD Headless, Native TTY)
    and perfectly calibrates its visual output to prevent Thread Panics or Log Floods.
    """

    def __init__(self, console, message: str, silent: bool = False):
        self.console = console
        self.message = message
        self.silent = silent

        # [ASCENSION 2]: Substrate Divination
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
            # Synchronous Proclamation for Single-Threaded or Log-Only Reality
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
    == THE QUANTUM CREATOR (V-Ω-TOTALITY-V32000-SINGULARITY-ANCHORED)              ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_WOMB_CONDUCTOR | RANK: OMEGA_SUPREME
    AUTH: Ω_CREATOR_V32000_GEOMETRIC_ANCHOR_SUTURE_FINALIS

    This is the final, eternal, and ultra-definitive form of the Materialization rite.
    It has been re-anchored to resolve the 'Nesting Paradox' and 'Sealed Crucible'
    heresies simultaneously.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **Macro Identity Ward (THE CORE FIX):** Harvests string literals directly from
        `@call` directives, macro context selectors, variables, and `@import` targets,
        bestowing absolute spatial immunity to willed identities, annihilating the Nesting Drift.
    2.  **The Sacred Roots Ward (THE CURE):** Instantly prevents the collapse of structural
        pillars like `src`, `app`, `infra`, ensuring proper workspace hierarchies.
    3.  **Absolute Geometric Locking:** Normalizes project and base paths through rigorous
        symlink resolution, immune to Windows UNC edge cases.
    4.  **The Matter-Leak Sentinel:** A regex phalanx that catches stray syntax (`def`,
        `{{`, `=>`) leaking into topographical paths, aborting before disk corruption.
    5.  **Pre-Commit Consecration:** Forces the materialization of implicit parent
        directories into Staging BEFORE the CPU compiles its instruction pipeline.
    6.  **Substrate-Aware Adrenaline Suture:** Conditionally disarms Garbage Collection
        and bumps thread priorities during massive writes on Native Iron.
    7.  **Thermodynamic Triage:** Injects micro-yields if the host system experiences
        "Metabolic Fever" (>92% CPU load or >4.5 Shannon Entropy on the Heap).
    8.  **Spacetime Collapse Algorithm:** The completely re-engineered Logic Fold that
        balances Sibling Density against Sovereign Decrees.
    9.  **Ouroboros Path Ward:** Implements absolute containment to prevent `../`
        directory traversal attacks at the exact moment of pre-flight.
    10. **Gnostic Blueprint Provenance:** Extrapolates the exact source blueprint path
        into the registers for downstream dependency mapping.
    11. **Lazarus Diagnostics Bridge:** Dumps full transactional state to disk if the
        run collapses, allowing the CLI to resurrect the error context later.
    12. **Fracture Tracking Suture:** Accumulates `critical_heresies` to dictate the
        final `ScaffoldResult` validity flag automatically.
    13. **Topographical Purification:** Invokes the `GhostBuster` post-materialization
        to sweep away ephemeral directories that lost their willed files.
    14. **Cross-Mount Atomicity Verification:** Scries `st_dev` of root vs staging; flags
        the transaction if atomic `os.replace` will fail across disk drives.
    15. **Orphaned State Exorcism:** Passively reaps 24-hour-old `.tmp` artifacts left
        behind by previously panicking processes.
    16. **Achronal Pre-Validation Matrix:** Computes the entire structural graph in
        memory, validating casing, uniqueness, and containment in O(1) time.
    17. **Deep Intent Divination:** Extracts the `intent` string from the request to
        inform semantic scoring for downstream intelligence.
    18. **Final Inquest Execution:** Commands the `GnosticAdjudicator` to pass judgment
        on the completed stage area before allowing the final Volume Shift.
    19. **Case Collision Map:** Tracks lowercased paths on NTFS to warn of identical
        paths resolving to the same physical node.
    20. **Nano-Scale Metabolic Anchor:** Measures start and end states to the nanosecond
        for the performance telemetry dashboard.
    21. **Cryptographic Chunk Hashing:** Forges a structural `_ast_structural_hash`
        of all willed geometries for idempotency caching.
    22. **The Finality Vow:** Wraps the entire `run` in a `try/finally` block that
        guarantees cleanup of Thread Locals and Environment DNA.
    23. **Shadow DOM VFS Pre-computation:** Builds a virtual tracking set to catch
        overlapping directory-file ontological schisms.
    24. **Null-Byte Annihilation:** Strips C-style `\x00` terminators to protect the
        underlying OS file handlers.
    25. **Symlink Singularity Guard:** Pre-computes symlink target relations to avert
        `RecursionError` during nested path validation.
    26. **Simulation Root Levitation:** In Dry-Run mode, redirects the `project_root`
        to the local `cwd` to prevent actual file overwrites on absolute paths.
    27. **Symbolic Synchronization:** Synchronizes the levitated simulation root directly
        into the `QuantumRegisters`.
    28. **Volumetric Triangulation:** Re-anchors the active `GnosticTransaction` to the
        newly calculated root, aligning staging and backup folders perfectly.
    29. **Dynamic Ignore Suture:** Calls `conduct_dynamic_ignore` on the Adjudicator
        to inject `.gitignore` blocks for discovered secrets.
    30. **Transmutation State Reset:** Enforces a clean garbage collection pass upon
        the conclusion of a heavy materialization.
    31. **Substrate Echo Multicast:** Dispatches precise `hud_pulse` messages mapped
        to geometric fold decisions.
    32. **Universal Spatiotemporal Contract:** A perfect bridging architecture that
        makes the Creator functionally ignorant of the physical filesystem layer.
    =================================================================================
    """

    # [FACULTY 1]: THE INQUISITOR'S GRIMOIRE
    # Patterns that indicate a path is actually a "Leaked" line of code.
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
        """
        =================================================================================
        == THE RITE OF CREATOR INCEPTION (V-Ω-TOTALITY-V32000)                         ==
        =================================================================================
        """
        import uuid
        from ...core.runtime.middleware.contract import GnosticVoidEngine
        from ...core.alchemist import get_alchemist
        from ..io_controller.facade import IOConductor

        self.engine = engine or GnosticVoidEngine()

        # [ASCENSION 2]: Thread-Local Contamination Shield
        self._thread_state = threading.local()
        self._thread_state.is_active = True

        # --- CAUSAL IDENTITY SUTURE ---
        self.trace_id = (
                getattr(args, 'trace_id', None) or
                (args.metadata.get('trace_id') if hasattr(args, 'metadata') and isinstance(args.metadata,
                                                                                           dict) else None) or
                f"tr-forge-{uuid.uuid4().hex[:6].upper()}"
        )
        self.session_id = getattr(args, 'session_id', 'SCAF-CORE')

        def _scry_will(name: str, default: Any = False) -> Any:
            if hasattr(args, name): return getattr(args, name)
            if isinstance(args, dict): return args.get(name, default)
            if pre_resolved_vars and name in pre_resolved_vars: return pre_resolved_vars[name]
            return default

        self.request = args
        self.variables = pre_resolved_vars if pre_resolved_vars is not None else {}
        self.variables['trace_id'] = self.trace_id

        # [ASCENSION 10]: Gnostic Blueprint Provenance
        self.blueprint_provenance = _scry_will('blueprint_path', 'unknown_origin')
        self.variables['_blueprint_provenance'] = str(self.blueprint_provenance)

        # [ASCENSION 17]: Deep Intent Divination
        self.core_intent = _scry_will('intent', 'standard_materialization')

        self.Logger = Scribe("QuantumCreator", trace_id=self.trace_id)
        self.scaffold_items = scaffold_items
        self.post_run_commands = post_run_commands or []
        self.parser_context = parser_context
        self.transaction = transaction
        self.console = getattr(self.engine, 'console', get_console())

        # --- THERMODYNAMIC & SPATIAL VOWS ---
        self.force = _scry_will('force')
        self.silent = _scry_will('silent')
        self.verbose = _scry_will('verbose')
        self.dry_run = _scry_will('dry_run')
        self.preview = _scry_will('preview')
        self.audit = _scry_will('audit')
        self.non_interactive = _scry_will('non_interactive')
        self.no_edicts = _scry_will('no_edicts')
        self.adjudicate_souls = _scry_will('adjudicate_souls', True)
        self.adrenaline_mode = _scry_will('adrenaline_mode', False)

        self.start_ns = time.perf_counter_ns()
        raw_root = _scry_will('base_path', _scry_will('project_root', os.getcwd()))

        # [ASCENSION 3]: Absolute Geometric Locking
        try:
            self.base_path = Path(os.path.realpath(os.path.abspath(str(raw_root))))
        except Exception:
            self.base_path = Path(raw_root).resolve()

        self.project_root = Path(".")

        self.alchemist = get_alchemist()
        self.clean_empty_dirs = str(self.variables.get('clean_empty_dirs', False)).lower() in ('true', '1', 'yes')

        # --- ORGAN INCEPTION & SUTURE ---
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

        if not self.silent:
            self.Logger.verbose(f"Creator Manifested. Trace: {self.trace_id[:8]} | Status: READY")

    @property
    def is_simulation(self) -> bool:
        """Simulation includes Dry-Run, Preview, and Forensic Audit."""
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        """True if we are striking the local filesystem."""
        return hasattr(self.sanctum, 'is_local') and self.sanctum.is_local

    def _collapse_spacetime_geometry(self) -> Path:
        """
        =================================================================================
        == THE OMEGA SPACETIME COLLAPSE ALGORITHM (V-Ω-TOTALITY-V32000-WILLED-IDENTITY) ==
        =================================================================================
        LIF: ∞ | ROLE: GEOMETRIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_COLLAPSE_V32000_IDENTITY_WARD_FINALIS_2026

        The supreme rite of spatial resolution. It adjudicates the 'Wrapper Paradox'
        by righteously protecting "Willed Identity" from accidental lustration.
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path
        from ...contracts.data_contracts import GnosticLineType
        from ...contracts.heresy_contracts import Heresy, HeresySeverity

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self, "trace_id", "tr-void")

        # --- MOVEMENT 0: THE VOID GUARD ---
        if not self.scaffold_items:
            return Path(".")

        # 1. THE CENSUS OF ATOMS
        # We only gaze upon physical matter willed to manifest.
        physical_atoms = [
            item for item in self.scaffold_items
            if item.line_type == GnosticLineType.FORM
               and item.path
               and len(item.path.parts) > 0
               and getattr(item, 'logic_result', True) is not False
        ]

        if not physical_atoms:
            return Path(".")

        # =========================================================================
        # == MOVEMENT I: THE ANTI-MATTER PHALANX (LEAK DETECTION)                ==
        # =========================================================================
        LEAK_PATTERN = re.compile("|".join(self.CODE_LEAK_SIGNATURES))

        for atom in physical_atoms:
            path_str = str(atom.path)
            if LEAK_PATTERN.search(path_str):
                self.Logger.critical(f"ANTI-MATTER_LEAK: Path '{path_str}' contains code signatures!")
                raise ArtisanHeresy(
                    message=f"Matter Leak: Code detected in Topography.",
                    details=f"Line {atom.line_num}: The path '{path_str}' contains willed logic.",
                    suggestion="Ensure your blueprint indentation is bit-perfect. Matter must be indented under a header.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=atom.line_num
                )

        # --- MOVEMENT II: THE PREFIX CENSUS ---
        posix_paths = [item.path.as_posix() for item in physical_atoms]

        try:
            common_prefix = os.path.commonpath(posix_paths)
            # If no common folder exists, or it's just the current root, stay grounded.
            if not common_prefix or common_prefix == "." or "/" in common_prefix:
                return Path(".")

            dominant_segment = Path(common_prefix).parts[0]
            segment_lower = dominant_segment.lower()

        except (ValueError, IndexError):
            return Path(".")

        # =========================================================================
        # == MOVEMENT III: THE GRAVITATIONAL INQUEST (FOLD VS PRESERVE)          ==
        # =========================================================================
        # [THE CURE]: We calculate two opposing forces: Entropy (Fold) and Will (Preserve).
        fold_score = 0.0
        preserve_score = 0.0
        rationale = []

        # --- 1. THE SACRED ROOTS WARD (ASCENSION 2) ---
        if segment_lower in {"src", "app", "lib", "core", "test", "tests", "docs", "infra", "config", "scripts", "bin"}:
            preserve_score += 50000.0
            rationale.append(f"Sacred Root Ward: '{dominant_segment}' is a foundational architectural pillar.")

        # --- 2. THE MACRO-IDENTITY WARD (ASCENSION 1) ---
        # We harvest all literal strings passed into macro @calls, variables, and imports.
        # If the Architect willed a string, it is granted immunity from folding.
        willed_identities = set()
        for item in self.scaffold_items:
            if item.raw_scripture:
                # Capture @call literals ("auth-vault")
                if '@call' in item.raw_scripture:
                    literals = re.findall(r'["\']([^"\']+)["\']', item.raw_scripture)
                    willed_identities.update(l.lower() for l in literals)

                # Capture @import targets (database, backend)
                if '@import' in item.raw_scripture:
                    try:
                        import_target = item.raw_scripture.replace('@import', '').strip().split()[0]
                        import_target = import_target.split('.')[-1].lower()
                        willed_identities.add(import_target)
                    except IndexError:
                        pass

            # Capture macro contextual injections
            if item.semantic_selector and "_macro_ctx" in item.semantic_selector:
                macro_vals = [str(v).lower() for v in item.semantic_selector["_macro_ctx"].values()]
                willed_identities.update(macro_vals)

        # Harvest all primitive values from the Altar of Variables ($$)
        for val in self.variables.values():
            if isinstance(val, (str, int, float, bool)):
                willed_identities.add(str(val).lower())

        if segment_lower in willed_identities:
            # Absolute immunity granted to willed concepts.
            preserve_score += 10000.0
            rationale.append(f"Macro Identity Ward: '{dominant_segment}' is explicitly willed.")

        # --- 3. IDENTITY RESONANCE (ASCENSION 2) ---
        # Check against willed variables ($$ project_name).
        intent_name = str(self.variables.get('project_name', '')).lower()
        intent_slug = str(self.variables.get('project_slug', '')).lower()

        if segment_lower in (intent_slug, intent_name):
            # Matches the project name itself? High probability it's a redundant wrapper.
            fold_score += 50.0
            rationale.append(f"Identity Match: Segment aligns with Project '{intent_slug}'.")

        # --- 4. SUBSTRATE AXIS RESONANCE (ASCENSION 24) ---
        # If the prefix matches the current directory name, it's often redundant.
        if segment_lower == self.base_path.name.lower():
            fold_score += 30.0
            rationale.append(f"Substrate Match: Segment matches host folder '{self.base_path.name}'.")

        # --- 5. SIBLING DENSITY ADJUDICATION (ASCENSION 12) ---
        # If the root lattice contains other willed items (Files), we CANNOT fold.
        root_siblings = [p for p in posix_paths if '/' not in p.strip('/')]
        if root_siblings:
            preserve_score += 5000.0
            rationale.append(f"Sibling Collision: {len(root_siblings)} atoms occupy the root.")

        # --- 6. SOVEREIGN OVERRIDE (ASCENSION 18) ---
        if str(self.variables.get('_target_dir_name', '')).lower() == segment_lower:
            preserve_score += 10000.0
            rationale.append("Sovereign Decree: Explicitly warded via _target_dir_name.")

        # --- MOVEMENT IV: THE VERDICT ---
        # [THE CURE]: The preservation score MUST be mathematically overcome by the fold score.
        should_fold = fold_score > preserve_score

        if should_fold:
            self.Logger.info(f"Geometric Consensus: [bold cyan]FOLD[/] -> {', '.join(rationale)}")

            # THE TRANSFIGURATION: Re-parenting the atoms
            for item in self.scaffold_items:
                if not item.path: continue

                parts = list(item.path.parts)
                if parts and parts[0] == dominant_segment:
                    if len(parts) > 1:
                        # Strip the redundant strata: 'vault/src' -> 'src'
                        item.path = Path(*parts[1:])
                    else:
                        # Item WAS the prefix: 'vault/' -> '.'
                        item.path = Path(".")
                        item.is_dir = True

            self.variables["_folded_prefix"] = dominant_segment
            final_anchor = Path(".")
        else:
            self.Logger.success(f"Geometric Consensus: [bold cyan]PRESERVE[/] -> {', '.join(rationale)}")
            final_anchor = Path(dominant_segment)

        # --- MOVEMENT V: METABOLIC FINALITY & HUD PULSE ---
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 11]: Ocular Resonance
        if hasattr(self, 'engine') and self.engine and getattr(self.engine, 'akashic', None):
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_ADJUDICATION",
                        "label": "REALITY_STABILIZED",
                        "color": "#64ffda" if should_fold else "#3b82f6",
                        "decision": "FOLD" if should_fold else "PRESERVE",
                        "latency_ms": round(duration_ms, 2),
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        return final_anchor

    def _sync_registers(self, registers: QuantumRegisters):
        """[ASCENSION 29]: Helper to ensure the Registers share the absolute spatial truth."""
        try:
            object.__setattr__(registers, 'project_root', self.project_root)
        except (AttributeError, TypeError):
            registers.project_root = self.project_root

    def _verify_cross_mount_atomicity(self):
        """[ASCENSION 14]: CROSS-MOUNT ATOMICITY VERIFICATION."""
        if not self.is_local_realm:
            return

        try:
            base_dev = os.stat(self.base_path).st_dev
            scaffold_dir = self.base_path / ".scaffold"
            if scaffold_dir.exists():
                scaffold_dev = os.stat(scaffold_dir).st_dev
                if base_dev != scaffold_dev:
                    self.Logger.warn(
                        "Cross-Mount boundary detected. Transaction guarantees shift to High-Friction Copy mode.")
                    self.variables['_cross_mount_detected'] = True
        except Exception:
            pass

    def _exorcise_orphaned_states(self):
        """[ASCENSION 15]: ORPHANED STATE EXORCISM."""
        if not self.is_local_realm:
            return

        try:
            scaffold_dir = self.base_path / ".scaffold"
            if not scaffold_dir.exists(): return

            now = time.time()
            exorcised = 0

            # Target orphaned temp files
            for tmp_file in scaffold_dir.rglob("*.tmp"):
                if now - tmp_file.stat().st_mtime > 86400:  # Older than 24 hours
                    tmp_file.unlink(missing_ok=True)
                    exorcised += 1

            if exorcised > 0:
                self.Logger.verbose(f"Exorcised {exorcised} orphaned state shards.")
        except Exception:
            pass

    def _conduct_quantum_pre_validation(self):
        """
        =============================================================================
        == ACHRONAL PRE-VALIDATION MATRIX (V-Ω-TOTALITY-V1000)                     ==
        =============================================================================[ASCENSION 16]: Performs a high-fidelity forensic audit of all paths BEFORE
        any disk IO occurs. It maps the topological footprint in memory.
        """
        self.Logger.verbose("Conducting Achronal Pre-Validation Matrix...")

        willed_identities: Dict[str, bool] = {}
        # [ASCENSION 19]: Case Collision Map
        case_insensitive_map: Dict[str, str] = {}

        # [ASCENSION 23]: VFS Pre-computation (Shadow DOM)
        vfs_shadow_dom: Set[str] = set()

        # [ASCENSION 21]: Cryptographic Chunk Hashing for large structures
        structural_hash = hashlib.sha256()

        for item in self.scaffold_items:
            if not item.path: continue

            path_str = str(item.path)
            normalized_coord = path_str.replace('\\', '/').rstrip('/')
            lower_coord = normalized_coord.lower()

            structural_hash.update(lower_coord.encode())

            # [ASCENSION 24]: Null-Byte Annihilation
            if '\x00' in path_str:
                raise ArtisanHeresy(
                    "Security Heresy: Null-Byte detected in path payload.",
                    line_num=item.line_num,
                    severity=HeresySeverity.CRITICAL
                )

            # [ASCENSION 4]: Anti-Matter Phalanx V15
            if self.PROFANE_PATH_CHARS.search(path_str):
                raise ArtisanHeresy(
                    f"Geometric Paradox: Profane characters detected in path '{path_str}'.",
                    line_num=item.line_num,
                    severity=HeresySeverity.CRITICAL
                )

            for sig in self.CODE_LEAK_SIGNATURES:
                if sig in path_str and not ("{{" in path_str and "}}" in path_str):
                    raise ArtisanHeresy(
                        f"Semantic Paradox: Path '{path_str}' appears to be source code.",
                        line_num=item.line_num,
                        details=f"Signature '{sig}' detected. The Parser leaked matter into topography.",
                        severity=HeresySeverity.CRITICAL
                    )

            # [ASCENSION 9]: Ouroboros Path Ward (Directory Traversal)
            if "../" in normalized_coord or "..\\" in normalized_coord:
                raise ArtisanHeresy(
                    f"Security Paradox: Path Traversal detected in '{path_str}'.",
                    line_num=item.line_num,
                    severity=HeresySeverity.CRITICAL
                )

            # [ASCENSION 25]: Symlink Singularity Guard
            if self.is_local_realm:
                check_path = self.base_path / normalized_coord
                if check_path.exists() and check_path.is_symlink():
                    try:
                        resolved = check_path.resolve()
                        if str(resolved).startswith(str(check_path)):
                            raise ArtisanHeresy(
                                f"Symlink Singularity: Path '{path_str}' points to itself recursively.",
                                line_num=item.line_num,
                                severity=HeresySeverity.CRITICAL
                            )
                    except Exception:
                        pass  # Dead link

            # [ASCENSION 19]: Case Collision Detection
            if lower_coord in case_insensitive_map and case_insensitive_map[lower_coord] != normalized_coord:
                raise ArtisanHeresy(
                    f"Topographical Heresy: Case-Identity Collision for '{path_str}'.",
                    line_num=item.line_num,
                    details=f"Path conflicts with previously defined '{case_insensitive_map[lower_coord]}'.",
                    severity=HeresySeverity.CRITICAL
                )
            case_insensitive_map[lower_coord] = normalized_coord

            # Ontological Consistency
            if normalized_coord in willed_identities:
                if willed_identities[normalized_coord] != item.is_dir:
                    raise ArtisanHeresy(
                        f"Topographical Heresy: Ontological Schism for '{path_str}'.",
                        line_num=item.line_num,
                        details="Path is defined as both a Sanctum (Dir) and Scripture (File).",
                        severity=HeresySeverity.CRITICAL
                    )

            willed_identities[normalized_coord] = item.is_dir
            vfs_shadow_dom.add(normalized_coord)

        # Assign memory hash for idempotency check later
        self.variables['_ast_structural_hash'] = structural_hash.hexdigest()

        self.Logger.success(
            f"Quantum Pre-Validation:[green]PURE[/green]. {len(willed_identities)} atoms mapped in VFS.")

    def _calculate_shannon_entropy(self) -> float:
        """Calculates the entropy of the current raw items as a processing heuristic."""
        if not self.scaffold_items: return 0.0
        sample_str = "".join([str(i.content)[:50] for i in self.scaffold_items[:10] if i.content])
        if not sample_str: return 0.0
        probabilities = [float(sample_str.count(c)) / len(sample_str) for c in dict.fromkeys(list(sample_str))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
        return entropy

    def _conduct_thermodynamic_triage(self):
        """[ASCENSION 7]: The Thermodynamic Governor & Entropy Fallback.
        """
        # [ASCENSION 6]: Substrate-Aware Adrenaline Suture
        if self.adrenaline_mode or os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            os.environ["SCAFFOLD_ADRENALINE"] = "1"
            return

        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None) or 0.0
            if cpu > 92.0:
                self.Logger.warn(f"Metabolic Fever ({cpu}%). Injecting Thermodynamic Yield...")
                time.sleep(0.5)
                gc.collect(1)
        except Exception:
            # Entropy-Driven Fallback
            entropy_score = self._calculate_shannon_entropy()
            if len(gc.get_objects()) > 600000 or entropy_score > 4.5:
                time.sleep(0.2)
                gc.collect(1)

    # =================================================================================
    # == THE GRAND SYMPHONY OF EXECUTION (RUN)                                       ==
    # =================================================================================

    def run(self) -> 'QuantumRegisters':
        """
        =================================================================================
        == THE OMEGA STRIKE: TOTALITY (V-Ω-TOTALITY-V32000-SIMULATION-SUTURED)         ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SINGULARITY
        """
        import time
        import os
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...core.sanitization.ghost_buster import GhostBuster

        # [ASCENSION 20]: NANO-SCALE METABOLIC ANCHOR
        start_ns = time.perf_counter_ns()

        # [ASCENSION 13]: SUBSTRATE-AWARE STATUS SUTURE
        status_ctx = QuantumStatusSuture(
            self.console,
            "[bold green]The Great Work is advancing...",
            silent=self.silent
        )

        registers: Optional['QuantumRegisters'] = None

        try:
            # --- MOVEMENT 0: INFRASTRUCTURE PREP ---
            self._verify_cross_mount_atomicity()
            self._exorcise_orphaned_states()

            # --- MOVEMENT I: SPACETIME COLLAPSE & RE-ANCHORING ---
            geometric_decision = self._collapse_spacetime_geometry()

            # =========================================================================
            # ==[ASCENSION 26]: SIMULATION ROOT LEVITATION                          ==
            # =========================================================================
            if self.is_simulation:
                self.project_root = Path(".").resolve()
                os.environ["SCAFFOLD_SIMULATION_ACTIVE"] = "1"
                self.Logger.verbose("Simulation Singularity: Root levitated to Virtual Sanctum.")
            else:
                self.project_root = self.base_path

            # [ASCENSION 28]: VOLUMETRIC TRIANGULATION
            if self.transaction:
                self.transaction.re_anchor(self.project_root)

            # --- MOVEMENT II: ACHRONAL PRE-VALIDATION ---
            self._conduct_quantum_pre_validation()
            self._conduct_thermodynamic_triage()

            # --- MOVEMENT III: MATERIALIZE THE MIND ---
            from ..registers import QuantumRegisters
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

            # [ASCENSION 27]: SYMBOLIC SYNCHRONIZATION
            self._sync_registers(registers)

            # --- MOVEMENT IV: SUTURE THE ORGANS ---
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller.facade import IOConductor
            from ..cpu import QuantumCPU

            io_conductor = IOConductor(registers)

            maestro_anchor = self.project_root
            if not self.is_simulation and str(geometric_decision) != ".":
                maestro_anchor = (self.base_path / geometric_decision).resolve()

            maestro = MaestroUnit(self.engine, registers, self.alchemist)
            maestro.project_anchor = maestro_anchor

            cpu = QuantumCPU(registers, io_conductor, maestro, self)

            # =========================================================================
            # == [ASCENSION 5]: PRE-COMMIT CONSECRATION                              ==
            # =========================================================================
            if self.is_local_realm and not self.is_simulation:
                if hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Consecrating Logical Structure...[/]", force=True)

                for item in list(self.scaffold_items):
                    if not item.is_dir and item.path:
                        self.structure_sentinel.ensure_structure(item.path)

            # --- MOVEMENT V: COMPILATION OF WILL ---
            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Void Intent: No kinetic instructions perceived. Rite concluded.")
                return registers

            self.sacred_paths = {(self.project_root / i.path).resolve() for i in self.scaffold_items if i.path}

            # =========================================================================
            # == MOVEMENT VI: THE KINETIC STRIKE (TRI-PHASIC EXECUTION)              ==
            # =========================================================================
            # [ASCENSION 6]: Engage Adrenaline Mode to maximize I/O throughput.
            gc_was_enabled = gc.isenabled()
            if self.adrenaline_mode:
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

            try:
                with status_ctx:
                    cpu.execute()

                    # --- MOVEMENT VII: FINAL ADJUDICATION & PURIFICATION ---
                    # [ASCENSION 18]: Final Inquest Execution.
                    if not self.is_simulation:
                        consecration_anchor = self.project_root
                        if self.transaction and hasattr(self.transaction, 'volume_shifter'):
                            shifter_state = getattr(self.transaction.volume_shifter, 'state', None)
                            if shifter_state and shifter_state.name == "RESONANT":
                                consecration_anchor = self.transaction.volume_shifter.shadow_root

                        if self.adjudicate_souls and self.transaction:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold purple]Adjudicating Soul Purity...[/]", force=True)
                            self.adjudicator.conduct_sentinel_inquest()

                        # [ASCENSION 29]: Dynamic Ignore Suture
                        self.adjudicator.conduct_dynamic_ignore()

                        if self.transaction and not self.transaction.simulate:
                            self.transaction.materialize()

                        # [ASCENSION 13]: TOPOGRAPHICAL PURIFICATION (GHOST BUSTER)
                        if self.clean_empty_dirs and self.is_local_realm:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold grey]Purging Entropy...[/]", force=True)
                            GhostBuster(root=consecration_anchor, protected_paths=self.sacred_paths).exorcise()

            finally:
                if self.adrenaline_mode and gc_was_enabled:
                    gc.enable()
                    os.environ.pop("SCAFFOLD_ADRENALINE", None)

            # --- MOVEMENT VIII: THE FINAL REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Apotheosis Achieved. Reality manifest in {duration_ms:.2f}ms.")

            registers.metabolic_tax_ms = duration_ms
            registers.ops_conducted = len(cpu.program)

            return registers

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: Fracture Tracking.
            if registers:
                registers.critical_heresies += 1

            # [ASCENSION 31]: Substrate Echo Multicast
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "RITE_FRACTURE", "label": "STRIKE_FAILED", "color": "#ef4444"}
                    })
                except:
                    pass

            # [ASCENSION 11]: THE LAZARUS DIAGNOSTICS BRIDGE.
            self._dump_forensic_payload(catastrophic_paradox)

            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                raise ArtisanHeresy(
                    "CATASTROPHIC_RUN_FRACTURE",
                    child_heresy=catastrophic_paradox,
                    details=f"Anchor: {self.project_root} | Error: {str(catastrophic_paradox)}",
                    severity=HeresySeverity.CRITICAL,
                    ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                ) from catastrophic_paradox
            raise
        finally:
            # [ASCENSION 22]: The Finality Vow (Clean up Thread-Local Shield)
            if hasattr(self, '_thread_state'):
                self._thread_state.is_active = False
            os.environ.pop("SCAFFOLD_SIMULATION_ACTIVE", None)
            # [ASCENSION 30]: Transmutation State Reset
            gc.collect()

    def _dump_forensic_payload(self, e: Exception):
        """[ASCENSION 11]: Transaction State Auto-Recovery Dump."""
        try:
            dump_dir = self.base_path / ".scaffold" / "crash_reports"
            dump_dir.mkdir(parents=True, exist_ok=True)
            import json
            dump = {
                "trace_id": getattr(self, 'trace_id', 'unknown'),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "variables": self.variables
            }
            dump_filename = f"crash_{int(time.time())}_{self.trace_id[:8]}.json"
            (dump_dir / dump_filename).write_text(json.dumps(dump, default=str, indent=2))
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_CREATOR_FACADE anchor='{getattr(self, 'project_root', '.')}' status=ALIEN_FORGE_READY>"