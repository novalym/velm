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
import platform
from contextlib import nullcontext, AbstractContextManager
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union, Set

from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import ScaffoldItem, GnosticArgs, GnosticLineType
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
    The orchestrator for validating architectural rules and executing creation pipelines.

    Responsibilities:
    - Topological Normalization: Prevents path traversal and illegal character usage.
    - Redundancy Pruning: Automatically folds redundant parent directories if they match the project name.
    - Transaction Alignment: Ensures all operations are scoped to the active project root.
    - Simulation Context: Redirects I/O to memory buffers during dry-runs.
    """

    # Restrict paths that contain shell control characters or logic directives
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
        from ...core.runtime.middleware.contract import GnosticVoidEngine
        from ...core.alchemist import get_alchemist
        from ..io_controller.facade import IOConductor

        self.engine = engine or GnosticVoidEngine()

        # Thread isolation for concurrent CLI requests
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
        self.variables = pre_resolved_vars if pre_resolved_vars is not None else {}
        self.variables['trace_id'] = self.trace_id
        self.blueprint_provenance = _resolve_arg('blueprint_path', 'unknown_origin')
        self.variables['_blueprint_provenance'] = str(self.blueprint_provenance)

        self.Logger = Scribe("QuantumCreator", trace_id=self.trace_id)
        self.scaffold_items = scaffold_items
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

        # Absolute Path Canonicalization
        try:
            self.base_path = Path(os.path.realpath(os.path.abspath(str(raw_root))))
        except Exception:
            self.base_path = Path(raw_root).resolve()

        self.project_root = Path(".")

        self.alchemist = get_alchemist()
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
        """Determines if operations should be redirected to the in-memory virtual filesystem."""
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        """Determines if the target environment is a local physical disk."""
        return hasattr(self.sanctum, 'is_local') and self.sanctum.is_local

    def _topological_normalization(self) -> Path:
        """
        Analyzes the incoming file paths to determine the true root anchor.
        If all files are wrapped in a directory matching the project name,
        it collapses the geometry to prevent redundant nesting (e.g. my-app/my-app/src).
        """
        import os
        import re

        if not self.scaffold_items:
            return Path(".")

        physical_atoms = [
            item for item in self.scaffold_items
            if item.line_type == GnosticLineType.FORM
               and item.path
               and len(item.path.parts) > 0
               and getattr(item, 'logic_result', True) is not False
        ]

        if not physical_atoms:
            return Path(".")

        # Structural Leak Detection
        # Halts execution if code fragments accidentally leaked into file path headers
        LEAK_PATTERN = re.compile("|".join(self.CODE_LEAK_SIGNATURES))

        for atom in physical_atoms:
            path_str = str(atom.path)
            if LEAK_PATTERN.search(path_str):
                raise ArtisanHeresy(
                    message=f"Syntax Error: Code fragment detected in file path definition.",
                    details=f"Line {atom.line_num}: The path '{path_str}' contains programming keywords.",
                    suggestion="Ensure correct indentation. Code content must be indented under a path header.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=atom.line_num
                )

        posix_paths = [item.path.as_posix() for item in physical_atoms]

        try:
            common_prefix = os.path.commonpath(posix_paths)
            if not common_prefix or common_prefix == "." or "/" in common_prefix:
                return Path(".")

            dominant_segment = Path(common_prefix).parts[0]
            segment_lower = dominant_segment.lower()

        except (ValueError, IndexError):
            return Path(".")

        # Evaluate if we should fold the prefix or preserve it
        fold_score = 0.0
        preserve_score = 0.0

        # Preserve common architectural root folder names
        if segment_lower in {"src", "app", "lib", "core", "test", "tests", "docs", "infra", "config", "scripts", "bin"}:
            preserve_score += 50000.0

        # Preserve explicit variable names referenced in the template
        willed_identities = set()
        for item in self.scaffold_items:
            if item.raw_scripture:
                if '@call' in item.raw_scripture:
                    literals = re.findall(r'["\']([^"\']+)["\']', item.raw_scripture)
                    willed_identities.update(l.lower() for l in literals)

                if '@import' in item.raw_scripture:
                    try:
                        import_target = item.raw_scripture.replace('@import', '').strip().split()[0]
                        import_target = import_target.split('.')[-1].lower()
                        willed_identities.add(import_target)
                    except IndexError:
                        pass

        for val in self.variables.values():
            if isinstance(val, (str, int, float, bool)):
                willed_identities.add(str(val).lower())

        if segment_lower in willed_identities:
            preserve_score += 10000.0

        intent_name = str(self.variables.get('project_name', '')).lower()
        intent_slug = str(self.variables.get('project_slug', '')).lower()

        # Fold if the prefix matches the project name exactly
        if segment_lower in (intent_slug, intent_name):
            fold_score += 50.0

        if segment_lower == self.base_path.name.lower():
            fold_score += 30.0

        # Preserve if there are peer files at the root level alongside the directory
        root_siblings = [p for p in posix_paths if '/' not in p.strip('/')]
        if root_siblings:
            preserve_score += 5000.0

        if str(self.variables.get('_target_dir_name', '')).lower() == segment_lower:
            preserve_score += 10000.0

        should_fold = fold_score > preserve_score

        if should_fold:
            for item in self.scaffold_items:
                if not item.path: continue

                parts = list(item.path.parts)
                if parts and parts[0] == dominant_segment:
                    if len(parts) > 1:
                        item.path = Path(*parts[1:])
                    else:
                        item.path = Path(".")
                        item.is_dir = True

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
        """Warns the user if the transaction spans across multiple disk partitions/drives."""
        if not self.is_local_realm:
            return

        try:
            base_dev = os.stat(self.base_path).st_dev
            scaffold_dir = self.base_path / ".scaffold"
            if scaffold_dir.exists():
                scaffold_dev = os.stat(scaffold_dir).st_dev
                if base_dev != scaffold_dev:
                    self.variables['_cross_mount_detected'] = True
        except Exception:
            pass

    def _exorcise_orphaned_states(self):
        """Cleans up temporary tracking files left behind by interrupted operations > 24 hours old."""
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

    def _conduct_pre_validation(self):
        """
        Validates all target paths in memory before any I/O begins.
        Catches case-sensitivity collisions, invalid characters, and recursive symlinks.
        """
        willed_identities: Dict[str, bool] = {}
        case_insensitive_map: Dict[str, str] = {}
        structural_hash = hashlib.sha256()

        for item in self.scaffold_items:
            if not item.path: continue

            path_str = str(item.path)
            normalized_coord = path_str.replace('\\', '/').rstrip('/')
            lower_coord = normalized_coord.lower()

            structural_hash.update(lower_coord.encode())

            if '\x00' in path_str:
                raise ArtisanHeresy("Security Violation: Null-Byte Injection detected in file path.",
                                    line_num=item.line_num, severity=HeresySeverity.CRITICAL)

            if self.PROFANE_PATH_CHARS.search(path_str):
                raise ArtisanHeresy(f"Invalid path: '{path_str}' contains illegal characters.", line_num=item.line_num,
                                    severity=HeresySeverity.CRITICAL)

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
                    details=f"Conflicts with '{case_insensitive_map[lower_coord]}'. Ensure distinct names on case-insensitive filesystems.",
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
        """Temporarily pauses the execution thread if system resources are exhausted."""
        if self.adrenaline_mode or os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            os.environ["SCAFFOLD_ADRENALINE"] = "1"
            return
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None) or 0.0
            if cpu > 92.0:
                time.sleep(0.5)
                gc.collect(1)
        except Exception:
            pass

    def run(self) -> 'QuantumRegisters':
        """
        The Core Processing Loop.
        Coordinates environment setup, validation, compilation, and execution.
        """
        start_ns = time.perf_counter_ns()

        status_ctx = QuantumStatusSuture(
            self.console,
            "[bold green]Processing build steps...",
            silent=self.silent
        )

        registers: Optional['QuantumRegisters'] = None

        try:
            self._verify_cross_mount_atomicity()
            self._exorcise_orphaned_states()
            geometric_decision = self._topological_normalization()

            if self.is_simulation:
                self.project_root = Path(".").resolve()
                os.environ["SCAFFOLD_SIMULATION_ACTIVE"] = "1"
                self.Logger.verbose("Dry-run active: Redirecting file operations to memory filesystem.")
            else:
                self.project_root = self.base_path

            if self.transaction:
                self.transaction.re_anchor(self.project_root)

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

            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller.facade import IOConductor

            io_conductor = IOConductor(registers)

            maestro_anchor = self.project_root
            if not self.is_simulation and str(geometric_decision) != ".":
                maestro_anchor = (self.base_path / geometric_decision).resolve()

            maestro = MaestroUnit(self.engine, registers, self.alchemist)
            maestro.project_anchor = maestro_anchor

            cpu = QuantumCPU(registers, io_conductor, maestro, self)

            if self.is_local_realm and not self.is_simulation:
                if hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Validating project structure...[/]", force=True)

                for item in list(self.scaffold_items):
                    if not item.is_dir and item.path:
                        self.structure_sentinel.ensure_structure(item.path)

            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("No files or commands to execute. Process finished.")
                return registers

            self.sacred_paths = {(self.project_root / i.path).resolve() for i in self.scaffold_items if i.path}

            gc_was_enabled = gc.isenabled()
            if self.adrenaline_mode:
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

            try:
                with status_ctx:
                    cpu.execute()

                    if not self.is_simulation:
                        consecration_anchor = self.project_root
                        if self.transaction and hasattr(self.transaction, 'volume_shifter'):
                            shifter_state = getattr(self.transaction.volume_shifter, 'state', None)
                            if shifter_state and shifter_state.name == "RESONANT":
                                consecration_anchor = self.transaction.volume_shifter.shadow_root

                        if self.adjudicate_souls and self.transaction:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold purple]Running security and syntax checks...[/]", force=True)
                            self.adjudicator.conduct_sentinel_inquest()

                        self.adjudicator.conduct_dynamic_ignore()

                        if self.transaction and not self.transaction.simulate:
                            self.transaction.materialize()

                        if self.clean_empty_dirs and self.is_local_realm:
                            if hasattr(status_ctx, "update"):
                                status_ctx.update("[bold grey]Cleaning up temporary files...[/]", force=True)
                            GhostBuster(root=consecration_anchor, protected_paths=self.sacred_paths).exorcise()

            finally:
                if self.adrenaline_mode and gc_was_enabled:
                    gc.enable()
                    os.environ.pop("SCAFFOLD_ADRENALINE", None)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Build completed successfully in {duration_ms:.2f}ms.")

            registers.metabolic_tax_ms = duration_ms
            registers.ops_conducted = len(cpu.program)

            return registers

        except Exception as e:
            if registers:
                registers.critical_heresies += 1

            self._dump_forensic_payload(e)

            if not isinstance(e, ArtisanHeresy):
                raise ArtisanHeresy(
                    "Execution Failed",
                    child_heresy=e,
                    details=f"Anchor: {self.project_root} | Error: {str(e)}",
                    severity=HeresySeverity.CRITICAL,
                    ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                ) from e
            raise
        finally:
            if hasattr(self, '_thread_state'):
                self._thread_state.is_active = False
            os.environ.pop("SCAFFOLD_SIMULATION_ACTIVE", None)
            gc.collect()

    def _dump_forensic_payload(self, e: Exception):
        """Writes current execution state to disk for crash analysis."""
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
        return f"<QuantumCreator anchor='{getattr(self, 'project_root', '.')}' status=READY>"
