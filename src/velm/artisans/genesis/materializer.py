# Path: src/velm/artisans/genesis/materializer.py
# -----------------------------------------------

from __future__ import annotations
import ast
import json
import re
import os
import platform
import sys
import time
import getpass
import shutil
import hashlib
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional, cast, Union

from rich.prompt import Confirm
from rich.markup import escape

from ...contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticArgs, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...creator import create_structure, QuantumRegisters
from ...creator.reports import GenesisReport
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GenesisRequest, BaseRequest
from ...logger import Scribe, get_console
from ...parser_core.parser import ApotheosisParser
from ...utils import atomic_write, get_git_branch, get_git_commit
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...creator.next_step_oracle import NextStepsOracle

Logger = Scribe("Materializer")

GnosticDowry = Tuple[ApotheosisParser, List[ScaffoldItem], List[str], Dict[str, Any], GnosticDossier]

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class GenesisMaterializer:
    """
    Orchestrates the final file creation sequence and ensures transactional safety.

    This class is responsible for taking the compiled AST instructions and coordinating
    with the TransactionManager to ensure that all file modifications are atomic. It also
    handles post-generation enrichment, such as DevContainer injection and README updating.
    """

    def __init__(self, engine, request: GenesisRequest, gnostic_dowry: GnosticDowry, collisions: List[Path]):
        self.engine = engine
        self.request = request
        self.parser, self.items, self.commands, self.final_vars, self.dossier = gnostic_dowry
        self.collisions = collisions
        self.logger = Logger
        self.console = get_console()
        self.project_root = request.project_root or Path.cwd()
        self.start_time = time.monotonic()

        # State tracking for telemetry and rollback mechanisms
        self.generated_files: List[Path] = []
        self.merkle_root: str = ""

    def _sys_log(self, msg: str, color: str = "45"):
        """Internal tracing for complex build sequence diagnostics."""
        if _DEBUG_MODE:
            sys.stderr.write(f"\x1b[{color};1m[DEBUG: Materializer]\x1b[0m {msg}\n")
            sys.stderr.flush()

    def conduct_materialization_symphony(self) -> ScaffoldResult:
        """
        The core execution loop for project generation.

        This manages the Two-Phase Commit process:
        1. Write all intended files to an ephemeral `.scaffold/staging` directory.
        2. Perform syntax validation on the staged files.
        3. If all validation passes, perform an atomic directory swap to finalize.
        """
        is_simulation = self.request.dry_run or self.request.preview

        # Determine if the user is creating a sub-folder or anchoring to the current working directory
        true_project_root = self._determine_true_project_root()
        tx_name = f"Build: {true_project_root.name}"
        blueprint_path = Path(self.final_vars.get('blueprint_path', 'unknown.scaffold'))

        self._sys_log(f"Starting build process. Target root: {true_project_root}", "44")
        self._sys_log(f"Files to generate: {len(self.items)}", "44")

        for idx, item in enumerate(self.items):
            content_preview = "NONE" if item.content is None else f"{len(item.content)} bytes"
            self._sys_log(
                f"  -> Item {idx}: {item.path} | Dir: {item.is_dir} | Content: {content_preview} | Seed: {item.seed_path}",
                "40")

        # Initialize the transactional context
        with GnosticTransaction(self.project_root, tx_name, blueprint_path, use_lock=True,
                                simulate=is_simulation) as tx:
            tx.context = {**self.final_vars}
            tx.context['project_root'] = str(true_project_root)
            tx.context['genesis_timestamp'] = time.time()

            gnostic_passport = GnosticArgs.from_namespace(self.request)

            self._sys_log("Invoking structure builder...", "44")

            # Normalize commands to match the required 3-tuple format for the execution engine
            normalized_commands = [(cmd, 0, None) for cmd in self.commands]
            safe_args = cast(Any, gnostic_passport)

            # Delegate the physical write operations to the Bootloader
            registers = create_structure(
                scaffold_items=self.items,
                post_run_commands=normalized_commands,
                pre_resolved_vars=self.final_vars,
                base_path=self.project_root,
                args=safe_args,
                transaction=tx
            )

            if registers.transaction:
                dossier = registers.transaction.write_dossier
                self._sys_log(f"Builder Finished. Logged {len(dossier)} entries.", "42")

                self.generated_files = []
                for path, res in dossier.items():
                    if res.success:
                        self.generated_files.append(res.path)
                    else:
                        self._sys_log(f"  -> [ERROR] {path} | Write Failed!", "41")

            if not is_simulation:
                # Execution of post-generation refinement policies
                self._validate_syntax_integrity(tx)
                self._enrich_readme_metadata(tx)
                self._ensure_dynamic_ignores(tx)
                self._consecrate_executables(tx)
                self._ensure_license(tx)
                self._analyze_overwrites(tx)
                self._inscribe_final_blueprint(true_project_root, tx)
                self._persist_genesis_state(true_project_root, tx)
                self._compute_merkle_root(tx)
                self._forge_devcontainer_scripture(true_project_root, tx)
                self._prune_empty_directories(true_project_root)

        self._proclaim_success(registers, true_project_root)

        # Map internal transaction logs to standard Artifact response models
        created_artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                created_artifacts.append(Artifact(
                    path=res.path, type="directory" if (self.project_root / res.path).is_dir() else "file",
                    action=res.action_taken.value, size_bytes=res.bytes_written, checksum=res.gnostic_fingerprint
                ))

        return ScaffoldResult(
            success=True,
            message="Project generated successfully.",
            data={
                "item_count": len(self.items),
                "variables": self.final_vars,
                "merkle_root": self.merkle_root,
                "genesis_mode": "STANDARD"
            },
            artifacts=created_artifacts
        )

    def _forge_devcontainer_scripture(self, project_root: Path, tx: GnosticTransaction):
        """
        Developer Experience (DX) Bootstrapping.
        Automatically generates a standard .devcontainer configuration based on the
        detected technology stack if requested by the user.
        """
        if not self.final_vars.get('use_devcontainer', self.final_vars.get('use_vscode', False)):
            return

        devcontainer_dir = project_root / ".devcontainer"
        try:
            devcontainer_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        self.logger.info("Generating Developer Container configuration...")

        project_slug = self.final_vars.get('project_slug', 'scaffold-project')
        project_type = self.final_vars.get('project_type', 'generic').lower()
        db_type = self.final_vars.get('database_type', 'none').lower()
        has_sidecar = db_type != 'none' or self.final_vars.get('use_redis', False)

        config = {
            "name": f"{self.final_vars.get('project_name', project_root.name)} Container",
            "containerUser": "vscode",
            "customizations": {
                "vscode": {
                    "settings": {
                        "editor.formatOnSave": True,
                    },
                    "extensions": ["GitHub.copilot", "usernamehw.errorlens"]
                }
            },
            "forwardPorts": [],
            "features": {
                "ghcr.io/devcontainers/features/common-utils:2": {"installZsh": True},
                "ghcr.io/devcontainers/features/git:1": {}
            }
        }

        # Context-aware extension injection
        if 'python' in project_type or 'fastapi' in project_type:
            config["customizations"]["vscode"]["extensions"].extend(["ms-python.python", "ms-python.vscode-pylance"])
            config["forwardPorts"].append(8000)
            if 'poetry' in project_type:
                config["postCreateCommand"] = "poetry install --no-interaction --no-root"
            else:
                config["postCreateCommand"] = "pip install -r requirements.txt"

        elif 'node' in project_type or 'react' in project_type:
            config["customizations"]["vscode"]["extensions"].extend(
                ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"])
            config["forwardPorts"].append(3000)
            config["postCreateCommand"] = "npm install"

        import json
        content = json.dumps(config, indent=4)
        atomic_write(devcontainer_dir / "devcontainer.json", content, self.logger, project_root, transaction=tx)

    def _determine_true_project_root(self) -> Path:
        """
        Determines if the generated items specify a parent directory wrapper.
        If all items share a root directory that matches the project slug, we anchor to it.
        """
        default_slug = self.final_vars.get('project_slug', 'new_project')
        if not self.items:
            return self.project_root / default_slug

        first_parts = set()
        for item in self.items:
            if item.path and item.path.parts:
                first_parts.add(item.path.parts[0])

        if len(first_parts) == 1:
            nested_root_name = list(first_parts)[0]
            if nested_root_name == default_slug:
                return self.project_root / nested_root_name

        return self.project_root

    def _validate_syntax_integrity(self, tx: GnosticTransaction):
        """
        Performs static analysis on the generated files while they are still in the staging area.
        If a template contained a severe syntax error, the transaction is rolled back before
        the user's workspace is affected.
        """
        self._sys_log(f"Validating syntax for {len(tx.write_dossier)} generated files...", "44")

        for path, result in tx.write_dossier.items():
            if not result.success: continue
            staged_path = tx.get_staging_path(path)

            if not staged_path.exists() or staged_path.stat().st_size == 0:
                continue

            if path.suffix == '.py':
                try:
                    ast.parse(staged_path.read_text(encoding='utf-8'))
                except SyntaxError as e:
                    raise ArtisanHeresy(f"Syntax Error in generated Python file '{path.name}': {e.msg}",
                                        line_num=e.lineno, severity=HeresySeverity.CRITICAL)
            elif path.suffix == '.json':
                try:
                    json.load(staged_path.open('r', encoding='utf-8'))
                except json.JSONDecodeError as e:
                    raise ArtisanHeresy(f"Malformed JSON output in '{path.name}': {e}",
                                        severity=HeresySeverity.CRITICAL)

    def _ensure_dynamic_ignores(self, tx: GnosticTransaction):
        """
        Automatically appends required exclusion paths to the .gitignore file.
        """
        ignores = set()
        for path in self.generated_files:
            if path.suffix in ['.env', '.key', '.pem', '.p12'] or path.name == '.DS_Store':
                ignores.add(path.name)
            if path.name == "scaffold.lock": ignores.add("scaffold.lock")
            if path.name == "genesis.json": ignores.add(".scaffold/genesis.json")

        if not ignores: return

        gitignore_path = self._determine_true_project_root() / ".gitignore"
        staged_gitignore = tx.get_staging_path(gitignore_path.relative_to(self.project_root))

        current_content = ""
        if staged_gitignore.exists():
            current_content = staged_gitignore.read_text(encoding='utf-8')
        elif gitignore_path.exists():
            current_content = gitignore_path.read_text(encoding='utf-8')

        new_content = current_content
        appended = False
        for item in ignores:
            if item not in current_content:
                if not appended:
                    new_content += "\n# --- Auto-generated excludes ---\n"
                    appended = True
                new_content += f"{item}\n"

        if new_content != current_content:
            atomic_write(gitignore_path, new_content, self.logger, self.project_root, transaction=tx)

    def _enrich_readme_metadata(self, tx: GnosticTransaction):
        """Injects build telemetry as HTML comments into the README."""
        readme_path = self._determine_true_project_root() / "README.md"
        is_generated = any(str(p).endswith("README.md") for p in self.generated_files)
        if not is_generated: return

        staged_readme = tx.get_staging_path(readme_path.relative_to(self.project_root))
        if staged_readme.exists():
            content = staged_readme.read_text(encoding='utf-8')
            meta_block = f"\n<!--\n  SCAFFOLD_GNOSIS:\n  timestamp: {time.time()}\n-->"
            if "SCAFFOLD_GNOSIS" not in content:
                atomic_write(readme_path, content + meta_block, self.logger, self.project_root, transaction=tx)

    def _consecrate_executables(self, tx: GnosticTransaction):
        """Heuristically applies execute permissions (+x) to shell scripts."""
        for path in self.generated_files:
            if path.suffix in ['.sh', '.bash'] or path.name in ['configure', 'bootstrap']:
                tx.record_edict(f"chmod +x {path}")
                try:
                    staged_path = tx.get_staging_path(path.relative_to(self.project_root))
                    if staged_path.exists():
                        staged_path.chmod(staged_path.stat().st_mode | 0o111)
                except Exception:
                    pass

    def _ensure_license(self, tx: GnosticTransaction):
        license_type = self.final_vars.get('license')
        if not license_type or license_type.lower() == 'none': return

        license_path = self._determine_true_project_root() / "LICENSE"
        if any(str(p).upper().endswith("LICENSE") for p in self.generated_files) or license_path.exists():
            return

        license_text = f"{license_type} License\n\nCopyright (c) {time.strftime('%Y')} {self.final_vars.get('author', 'Developer')}"
        atomic_write(license_path, license_text, self.logger, self.project_root, transaction=tx)

    def _inscribe_final_blueprint(self, true_project_root: Path, transaction: GnosticTransaction):
        from ...core.blueprint_scribe import BlueprintScribe
        chronicle_path = true_project_root / "scaffold.scaffold"

        try:
            scribe = BlueprintScribe(self.project_root)
            normalized_commands = [(cmd, 0, None, None) for cmd in self.commands]
            final_scripture = scribe.transcribe(self.items, normalized_commands, self.final_vars)

            atomic_write(chronicle_path, final_scripture, self.logger, self.project_root, transaction=transaction)

            if not _DEBUG_MODE:
                self.logger.success("Project blueprint saved to scaffold.scaffold.")
        except Exception as e:
            self.logger.warn(f"Warning: Failed to save final blueprint state: {e}")

    def _persist_genesis_state(self, true_project_root: Path, transaction: GnosticTransaction):
        state_path = true_project_root / ".scaffold" / "genesis.json"
        safe_vars = {k: v for k, v in self.final_vars.items() if
                     isinstance(v, (str, int, bool, float, list, dict, type(None)))}

        content = json.dumps({
            "variables": safe_vars, "timestamp": time.time(),
            "archetype": self.final_vars.get("profile") or "custom"
        }, indent=2)
        atomic_write(state_path, content, self.logger, self.project_root, transaction=transaction)

    def _prune_empty_directories(self, root: Path):
        """Cleans up any ephemeral folder structures generated during the build pipeline."""
        if not root.exists(): return
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            if not dirnames and not filenames:
                try:
                    Path(dirpath).rmdir()
                except OSError:
                    pass

    def _analyze_overwrites(self, tx: GnosticTransaction):
        pass

    def _compute_merkle_root(self, tx: GnosticTransaction):
        hasher = hashlib.sha256()
        for path in sorted(tx.write_dossier.keys()):
            res = tx.write_dossier[path]
            if res.success and res.gnostic_fingerprint:
                hasher.update(str(path).encode())
                hasher.update(res.gnostic_fingerprint.encode())
        self.merkle_root = hasher.hexdigest()

    def _proclaim_success(self, registers: QuantumRegisters, true_project_root: Path):
        if self.request.silent or self.request.dry_run or self.request.preview:
            return

        artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                artifacts.append(Artifact(path=res.path, type="file", action=res.action_taken.value))

        duration_ms = (time.monotonic() - self.start_time) * 1000
        total_mass = sum(a.size_bytes for a in artifacts)

        perf_metrics = {
            "duration_ms": duration_ms,
            "mass_bytes": total_mass,
        }

        try:
            cwd = Path.cwd()
            resolved_root = true_project_root.resolve()
            needs_cd = resolved_root != cwd
            relative_root = resolved_root.relative_to(cwd) if needs_cd else "."
        except ValueError:
            relative_root = true_project_root
            needs_cd = True

        final_next_steps = []
        if needs_cd:
            final_next_steps.append(f"cd {relative_root}")

        prophet = NextStepsOracle(project_root=true_project_root, gnosis=self.final_vars)
        oracle_steps = prophet.prophesy()
        for step in oracle_steps:
            if "cd " not in step:
                final_next_steps.append(step)

        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis=self.final_vars,
            project_root=true_project_root,
            next_steps=final_next_steps,
            title="Project Generated Successfully",
            subtitle=f"'{escape(true_project_root.name)}' is ready.",
            gnostic_constellation=artifacts,
            security_warnings=[],
            transmutation_plan=None,
            ai_telemetry={},
            environment_gnosis={},
            performance_metrics=perf_metrics,
            maestro_edicts=self.commands,
            audit_file_path=self.project_root / ".scaffold" / "genesis_audit.json"
        )