# Path: src/velm/creator/engine/facade.py
# ---------------------------------------
# =========================================================================================
# == THE QUANTUM CREATOR (V-Ω-TOTALITY-V1100.0-GEOMETRIC-SUTURE-FINALIS)                 ==
# =========================================================================================
# LIF: INFINITY | ROLE: REALITY_STAGE_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_CREATOR_V1100_GEOMETRIC_ANCHOR_SUTURE
# =========================================================================================

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
    == THE QUANTUM STATUS SUTURE (V-Ω-SUBSTRATE-AWARE-V3)                      ==
    =============================================================================
    [ASCENSION 1]: The ultimate polymorphic context manager.
    It reads the DNA of the host environment (WASM, CI/CD Headless, Native TTY)
    and perfectly calibrates its visual output to prevent Thread Panics or Log Floods.
    """

    def __init__(self, console, message: str, silent: bool = False):
        self.console = console
        self.message = message
        self.silent = silent

        # [ASCENSION 3]: Substrate Divination
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
    == THE QUANTUM CREATOR (V-Ω-TOTALITY-V1100.0-SINGULARITY-ANCHORED)             ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE HAND OF CREATION)

    This is the final, eternal, and ultra-definitive form of the Materialization rite.
    It has been re-anchored to resolve the 'Nesting Paradox' and 'Sealed Crucible'
    heresies simultaneously.
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
        == THE RITE OF CREATOR INCEPTION (V-Ω-TOTALITY-V1100)                          ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_WOMB_CONDUCTOR | RANK: OMEGA_SUPREME
        """
        import uuid
        from ...core.runtime.middleware.contract import GnosticVoidEngine
        from ...core.alchemist import get_alchemist
        from ..io_controller.facade import IOConductor

        self.engine = engine or GnosticVoidEngine()

        # [ASCENSION 20]: Thread-Local Contamination Shield
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

        # [ASCENSION 11]: Gnostic Blueprint Provenance
        self.blueprint_provenance = _scry_will('blueprint_path', 'unknown_origin')
        self.variables['_blueprint_provenance'] = str(self.blueprint_provenance)

        # [ASCENSION 19]: Deep Intent Divination
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

        # [ASCENSION 21]: Absolute Geometric Locking
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
        == THE SPACETIME COLLAPSE ALGORITHM (V-Ω-TOTALITY-V1000)                       ==
        =================================================================================
        [ASCENSION 2]: Resolves the 'Wrapper Paradox' using Gnostic Gravitational Consensus.
        It evaluates the Physical Substrate, Logical Intent, and Structural Ancestry
        to decide whether to 'Fold' (Strip wrapper) or 'Preserve' the root node.
        Absolutely bulletproof path resolution matrix utilizing a weighted scoring system.
        """
        start_ns = time.perf_counter_ns()

        if not self.scaffold_items:
            return Path(".")

        physical_atoms = [
            item for item in self.scaffold_items
            if item.line_type == GnosticLineType.FORM and item.path and len(item.path.parts) > 0
        ]

        if not physical_atoms:
            return Path(".")

        try:
            # Enforce POSIX string consistency for os.path.commonpath
            posix_paths = [item.path.as_posix() for item in physical_atoms]
            common_prefix = os.path.commonpath(posix_paths)

            if not common_prefix or common_prefix == ".":
                return Path(".")

            dominant_segment = Path(common_prefix).parts[0]
        except (ValueError, IndexError):
            return Path(".")

        # Core Identity Matrix
        substrate_identity = self.base_path.name.lower()
        logical_intent = {
            str(self.variables.get('project_slug', '')).lower().strip('/'),
            str(self.variables.get('project_name', '')).lower().strip('/')
        }
        ancestral_identity = str(dominant_segment).lower().strip('/')

        # --- THE GRAVITATIONAL MATRIX SCORING ---
        fold_score = 0.0
        preserve_score = 0.0
        decision_reason = "Identity Unique"

        # 1. Substrate Resonance
        if substrate_identity == ancestral_identity:
            fold_score += 10.0
            decision_reason = "Substrate Identity Match (Gravitational Fold)"

        # 2. Logical Intent Disconnect
        if ancestral_identity not in logical_intent:
            if self.force:
                fold_score += 50.0  # Force override
                decision_reason = "Forced Alien Wrapper Excision"
            else:
                preserve_score += 5.0

        # 3. Explicit Target Override (Semantic Anchor)
        if self.variables.get('_target_dir_name', '').lower() == ancestral_identity:
            preserve_score += 100.0  # Unbreakable preservation
            decision_reason = "Semantic Target Override (Preserve)"

        # The Verdict Logic
        should_fold = fold_score > preserve_score

        if should_fold:
            self.Logger.info(f"Geometric Consensus: [cyan]FOLD[/] ({decision_reason})")

            # The Rite of Folding
            for item in self.scaffold_items:
                if item.path:
                    try:
                        path_str = item.path.as_posix()
                        if path_str.startswith(dominant_segment):
                            if len(item.path.parts) > 1:
                                # Strip the first segment: 'api/main.py' -> 'main.py'
                                item.path = Path(*item.path.parts[1:])
                            else:
                                # Item was the directory itself: 'api/' -> '.'
                                item.path = Path(".")
                    except Exception:
                        continue
            final_anchor = Path(".")
        else:
            self.Logger.success(f"Geometric Consensus: [bold cyan]PRESERVE[/] ({decision_reason})")
            # We preserve the 'sentinel-api/' prefix.
            final_anchor = Path(dominant_segment)

        # Telemetry Pulse
        if hasattr(self, 'engine') and self.engine and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_ADJUDICATION",
                        "label": "SPACETIME_STABILIZED",
                        "color": "#64ffda",
                        "decision": "FOLD" if should_fold else "PRESERVE",
                        "anchor": str(final_anchor)
                    }
                })
            except Exception:
                pass

        return final_anchor

    def _sync_registers(self, registers: QuantumRegisters):
        """Helper to ensure the Registers share the absolute spatial truth."""
        try:
            object.__setattr__(registers, 'project_root', self.project_root)
        except (AttributeError, TypeError):
            registers.project_root = self.project_root

    def _verify_cross_mount_atomicity(self):
        """
        [ASCENSION 18]: CROSS-MOUNT ATOMICITY VERIFICATION.
        Checks if the base path and the staging directory are on the same physical drive.
        If they differ, OS-level atomic renames will fail (EXDEV). We flag this early
        so the VolumeShifter knows to fallback to robust copying.
        """
        if not self.is_local_realm:
            return

        try:
            base_dev = os.stat(self.base_path).st_dev
            # Check where .scaffold will be forged
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
        """
        [ASCENSION 17]: ORPHANED STATE EXORCISM.
        Pre-emptively purges `.tmp` files and stale transaction artifacts from
        previous aborted runs that bypassed the Lazarus protocol.
        """
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
        =============================================================================
        [ASCENSION 3, 4, 6, 7, 10, 13, 14, 15]: Performs a high-fidelity forensic audit
        of all paths BEFORE any disk IO occurs. It maps the topological footprint in memory.
        """
        self.Logger.verbose("Conducting Achronal Pre-Validation Matrix...")

        willed_identities: Dict[str, bool] = {}
        # [ASCENSION 6]: Case Collision Map
        case_insensitive_map: Dict[str, str] = {}

        # [ASCENSION 15]: VFS Pre-computation (Shadow DOM)
        vfs_shadow_dom: Set[str] = set()

        # [ASCENSION 14]: Cryptographic Chunk Hashing for large structures
        structural_hash = hashlib.sha256()

        for item in self.scaffold_items:
            if not item.path: continue

            path_str = str(item.path)
            normalized_coord = path_str.replace('\\', '/').rstrip('/')
            lower_coord = normalized_coord.lower()

            structural_hash.update(lower_coord.encode())

            # [ASCENSION 7]: Null-Byte Annihilation
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
                        f"Semantic Paradox: Path '{path_str}' appears to contain source code.",
                        line_num=item.line_num,
                        details=f"Signature '{sig}' detected. The Parser leaked matter into topography.",
                        severity=HeresySeverity.CRITICAL
                    )

            # [ASCENSION 10]: Ouroboros Path Ward (Directory Traversal)
            if "../" in normalized_coord or "..\\" in normalized_coord:
                raise ArtisanHeresy(
                    f"Security Paradox: Path Traversal detected in '{path_str}'.",
                    line_num=item.line_num,
                    severity=HeresySeverity.CRITICAL
                )

            # [ASCENSION 13]: Symlink Singularity Guard
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

            # [ASCENSION 6]: Case Collision Detection
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

            # Populate Shadow DOM
            vfs_shadow_dom.add(normalized_coord)

        # Assign memory hash for idempotency check later
        self.variables['_ast_structural_hash'] = structural_hash.hexdigest()

        self.Logger.success(
            f"Quantum Pre-Validation: [green]PURE[/green]. {len(willed_identities)} atoms mapped in VFS.")

    def _calculate_shannon_entropy(self) -> float:
        """Calculates the entropy of the current raw items as a processing heuristic."""
        if not self.scaffold_items: return 0.0

        # We sample the first few items to gauge complexity
        sample_str = "".join([str(i.content)[:50] for i in self.scaffold_items[:10] if i.content])
        if not sample_str: return 0.0

        probabilities = [float(sample_str.count(c)) / len(sample_str) for c in dict.fromkeys(list(sample_str))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
        return entropy

    def _conduct_thermodynamic_triage(self):
        """
        [ASCENSION 8 & 22]: The Thermodynamic Governor & Entropy Fallback.
        Forces micro-yields if the host OS is experiencing Metabolic Fever.
        """
        # [ASCENSION 5]: Substrate-Aware Adrenaline Suture
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
            # [ASCENSION 22]: Entropy-Driven Fallback
            # If psutil fails, we check object heap size AND content entropy to infer load.
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
        == THE OMEGA STRIKE: TOTALITY (V-Ω-TOTALITY-V1000.7-HEALED)                    ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SINGULARITY
        AUTH: Ω_RUN_V1000_TOTALITY_HEALED_FINALIS_2026

        [THE MANIFESTO]
        This implementation righteously annihilates the 'Nesting Heresy' and the
        'Sealed Crucible' fracture. It orchestrates the Tri-Phasic Materialization
        while ensuring the StructureSentinel acts BEFORE the timeline is frozen.
        =================================================================================
        """
        import time
        import os
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        # [ASCENSION 0]: NANO-SCALE METABOLIC ANCHOR
        start_ns = time.perf_counter_ns()

        # [ASCENSION 3]: SUBSTRATE-AWARE STATUS SUTURE
        status_ctx = QuantumStatusSuture(
            self.console,
            "[bold green]The Great Work is advancing...",
            silent=self.silent
        )

        registers: Optional['QuantumRegisters'] = None

        try:
            # --- MOVEMENT 0: INFRASTRUCTURE PREP ---
            # [ASCENSION 18]: Adjudicate cross-mount atomicity and purge orphans.
            self._verify_cross_mount_atomicity()
            self._exorcise_orphaned_states()

            # --- MOVEMENT I: SPACETIME COLLAPSE & RE-ANCHORING ---
            # [ASCENSION 1]: Adjudicate the Spacetime Decision (Fold vs Preserve)
            geometric_decision = self._collapse_spacetime_geometry()

            # =========================================================================
            # == [THE CURE]: NESTING ANNIHILATION (GEOMETRIC LOCKING)                ==
            # =========================================================================
            # Regardless of the decision, the 'project_root' for the physical creation
            # phase MUST remain at the base path. This ensures that a file willed at
            # 'sentinel-api/main.py' is written to './sentinel-api/main.py', not
            # './sentinel-api/sentinel-api/main.py'.
            self.project_root = self.base_path

            # [ASCENSION 9]: VOLUMETRIC TRIANGULATION
            # We anchor the transaction to the base_path to ensure Staging and
            # Volume folders are correctly aligned in the .scaffold sanctum.
            if self.transaction:
                self.transaction.re_anchor(self.project_root)

            # --- MOVEMENT II: ACHRONAL PRE-VALIDATION ---
            # [ASCENSION 4 & 11]: Forensic path audit and thermodynamic triage.
            self._conduct_quantum_pre_validation()
            self._conduct_thermodynamic_triage()

            # --- MOVEMENT III: MATERIALIZE THE MIND ---
            # [ASCENSION 7]: Forge the thread-local state vessel.
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

            # [ASCENSION 9]: SYMBOLIC SYNCHRONIZATION
            self._sync_registers(registers)

            # --- MOVEMENT IV: SUTURE THE ORGANS ---
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller.facade import IOConductor
            from ..cpu import QuantumCPU

            io_conductor = IOConductor(registers)

            # [THE CURE]: MAESTRO ANCHOR RESOLUTION
            # We forge a Maestro that is anchored to the logical project directory.
            # This ensures 'make install' runs in './sentinel-api/', not '.'.
            maestro_anchor = self.project_root
            if str(geometric_decision) != ".":
                maestro_anchor = (self.base_path / geometric_decision).resolve()

            maestro = MaestroUnit(self.engine, registers, self.alchemist)
            # Surgically update the maestro's project anchor to respect the wrapper decision
            maestro.project_anchor = maestro_anchor

            cpu = QuantumCPU(registers, io_conductor, maestro, self)

            # =========================================================================
            # == [THE CURE]: PRE-COMMIT CONSECRATION (SEALED CRUCIBLE FIX)           ==
            # =========================================================================
            # [ASCENSION 13]: We perform structural consecration BEFORE compilation.
            # This ensures that implicit files (like __init__.py) are added to the
            # transaction's record and created DURING the open state of the Crucible.
            if self.is_local_realm and not self.is_simulation:
                if hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Consecrating Logical Structure...[/]", force=True)

                # The Sentinel ensures the parent structure is manifest in the Staging Area
                # by scrying every willed form item.
                for item in list(self.scaffold_items):
                    if not item.is_dir and item.path:
                        self.structure_sentinel.ensure_structure(item.path)

            # --- MOVEMENT V: COMPILATION OF WILL ---
            # Compile the program, now including any implicit structural markers.
            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Void Intent: No kinetic instructions perceived. Rite concluded.")
                return registers

            self.sacred_paths = {(self.base_path / i.path).resolve() for i in self.scaffold_items if i.path}

            # =========================================================================
            # == MOVEMENT VI: THE KINETIC STRIKE (TRI-PHASIC EXECUTION)               ==
            # =========================================================================
            # [ASCENSION 5]: Engage Adrenaline Mode to maximize I/O throughput.
            gc_was_enabled = gc.isenabled()
            if self.adrenaline_mode:
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

            try:
                with status_ctx:
                    # [STRIKE]: Phase I (Form) -> Phase II (Sync) -> Phase III (Will)
                    cpu.execute()

                    # --- MOVEMENT VII: FINAL ADJUDICATION & PURIFICATION ---
                    if not self.is_simulation:

                        # Triangulate anchor for final audit (Shadow vs Root)
                        consecration_anchor = self.project_root
                        if self.transaction and hasattr(self.transaction, 'volume_shifter'):
                            shifter_state = getattr(self.transaction.volume_shifter, 'state', None)
                            if shifter_state and shifter_state.name == "RESONANT":
                                consecration_anchor = self.transaction.volume_shifter.shadow_root

                        # [ASCENSION 23]: THE FINAL INQUEST
                        if self.adjudicate_souls and self.transaction:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold purple]Adjudicating Soul Purity...[/]", force=True)
                            self.adjudicator.conduct_sentinel_inquest()

                        self.adjudicator.conduct_dynamic_ignore()

                        # FINAL LUSTRATION: Flush any remaining Gnosis to the Volume
                        if self.transaction and not self.transaction.simulate:
                            self.transaction.materialize()

                        # [ASCENSION 15]: TOPOGRAPHICAL PURIFICATION (GHOST BUSTER)
                        if self.clean_empty_dirs and self.is_local_realm:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold grey]Purging Entropy...[/]", force=True)
                            GhostBuster(root=consecration_anchor, protected_paths=self.sacred_paths).exorcise()

            finally:
                # Restore metabolic equilibrium
                if self.adrenaline_mode and gc_was_enabled:
                    gc.enable()
                    os.environ.pop("SCAFFOLD_ADRENALINE", None)

            # --- MOVEMENT VIII: THE FINAL REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Apotheosis Achieved. Reality manifest in {duration_ms:.2f}ms.")

            # [ASCENSION 24]: THE ABSOLUTE VOW OF TRUTH
            registers.metabolic_tax_ms = duration_ms
            registers.ops_conducted = len(cpu.program)

            return registers

        except Exception as catastrophic_paradox:
            if registers:
                registers.critical_heresies += 1

            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "RITE_FRACTURE", "label": "STRIKE_FAILED", "color": "#ef4444"}
                    })
                except:
                    pass

            # [ASCENSION 12]: THE LAZARUS DIAGNOSTICS BRIDGE
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
            # [ASCENSION 20]: Clean up Thread-Local Shield
            if hasattr(self, '_thread_state'):
                self._thread_state.is_active = False

    def _dump_forensic_payload(self, e: Exception):
        """[ASCENSION 12]: Transaction State Auto-Recovery Dump."""
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


