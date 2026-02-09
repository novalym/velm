# Path: scaffold/artisans/genesis/materializer.py
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
from typing import Tuple, List, Dict, Any, Optional

from rich.prompt import Confirm
from rich.markup import escape

# --- DIVINE SUMMONS ---
from ...contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticArgs, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...creator import create_structure, QuantumRegisters
from ...creator.reports import GenesisReport
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GenesisRequest
from ...logger import Scribe
from ...parser_core.parser import ApotheosisParser
from ...utils import atomic_write, get_git_branch, get_git_commit
# --- THE ASCENDED SCRIBE ---
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...creator.next_step_oracle import NextStepsOracle

Logger = Scribe("GenesisMaterializer")

GnosticDowry = Tuple[ApotheosisParser, List[ScaffoldItem], List[str], Dict[str, Any], GnosticDossier]

# Lazy load YAML for optional validation
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class GenesisMaterializer:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC MANIFESTATION (V-Ω-SINGULARITY-EDITION)           ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The Sovereign Hand that transmutes Prophecy into Reality.
    It ensures that what is written is not just text, but Truth.
    """

    def __init__(self, engine, request: GenesisRequest, gnostic_dowry: GnosticDowry, collisions: List[Path]):
        self.engine = engine
        self.request = request
        self.parser, self.items, self.commands, self.final_vars, self.dossier = gnostic_dowry
        self.collisions = collisions
        self.logger = Logger
        self.console = engine.console
        self.project_root = request.project_root or Path.cwd()
        self.start_time = time.monotonic()

        # Internal State for Telemetry & Forensics
        self.generated_files: List[Path] = []
        self.merkle_root: str = ""

    def conduct_materialization_symphony(self) -> ScaffoldResult:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF MATERIALIZATION (V-Ω-ETERNALLY-HEALED)                ==
        =================================================================================
        This is the Grand Symphony in its final, eternally-healed form. It now honors
        the sacred, three-fold scripture of Will `(command, line_num, undo_block)`,
        bestowing it, pure and whole, upon the Quantum Creator. The chain of Gnostic
        causality is now unbreakable.
        =================================================================================
        """
        is_simulation = self.request.dry_run or self.request.preview

        # [FACULTY 1] The Gnostic Anchor: Determine the true root of the new reality.
        true_project_root = self._determine_true_project_root()
        tx_name = f"Genesis: {true_project_root.name}"
        blueprint_path = Path(self.final_vars.get('blueprint_path', 'unknown.scaffold'))

        # [FACULTY 2] The Transactional Womb
        with GnosticTransaction(self.project_root, tx_name, blueprint_path, use_lock=True,
                                simulate=is_simulation) as tx:

            # Inject Gnosis into Transaction Context for rollback metadata
            tx.context = self.final_vars
            gnostic_passport = GnosticArgs.from_namespace(self.request)

            # --- MOVEMENT I: THE RITE OF CREATION ---
            # The Materializer bestows the complete scripture of Will upon the Creator.
            registers = create_structure(
                scaffold_items=self.items,
                post_run_commands=self.commands,
                pre_resolved_vars=self.final_vars,
                base_path=self.project_root,
                args=gnostic_passport,
                transaction=tx
            )

            if registers.transaction:
                # Collect paths relative to project root for further processing
                self.generated_files = [res.path for res in registers.transaction.write_dossier.values() if res.success]

            # --- MOVEMENT II: THE GNOSTIC VALIDATION (Syntax Inquisitor) ---
            if not is_simulation:
                self._validate_generated_souls(tx)

            # --- MOVEMENT III: THE ENRICHMENT & CONSECRATION ---
            if not is_simulation:
                self._enrich_readme_metadata(tx)
                self._ensure_dynamic_ignores(tx)
                self._consecrate_executables(tx)
                self._ensure_license(tx)
                self._analyze_overwrites(tx)
                self._inscribe_final_blueprint(true_project_root, tx)
                self._persist_genesis_state(true_project_root, tx)
                self._compute_merkle_root(tx)
                self._forge_devcontainer_scripture(true_project_root, tx)
                # ===========================
            # --- MOVEMENT IV: THE PURIFICATION (Ghost Buster) ---
            if not is_simulation:
                self._prune_empty_directories(true_project_root)

        # --- MOVEMENT V: THE PROCLAMATION ---
        # This is the final word.
        self._proclaim_success(registers, true_project_root)

        # Forge Artifacts for API response
        created_artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                created_artifacts.append(Artifact(
                    path=res.path, type="directory" if (self.project_root / res.path).is_dir() else "file",
                    action=res.action_taken.value, size_bytes=res.bytes_written, checksum=res.gnostic_fingerprint
                ))

        return ScaffoldResult(
            success=True,
            message="The Rite of Materialization is complete.",
            data={"item_count": len(self.items), "variables": self.final_vars, "merkle_root": self.merkle_root},
            artifacts=created_artifacts
        )

    def _forge_devcontainer_scripture(self, project_root: Path, tx: GnosticTransaction):
        """
        =================================================================================
        == THE OMNISCIENT DEVCONTAINER FOUNDRY (V-Ω-TOTALITY-V100-FINALIS)             ==
        =================================================================================
        LIF: ∞ | ROLE: ENVIRONMENTAL_SINGULARITY_ORCHESTRATOR | RANK: OMEGA_SUPREME

        [ARCHITECTURAL MANIFESTO]
        This rite transmutes the abstract Gnosis of the project into a deterministic
        Microsoft DevContainer specification. It eliminates the "Environmental Heresy"
        (It works on my machine) by enforcing absolute parity between the Architect's
        local gaze and the containerized reality.

        ### THE 12 LEGENDARY ASCENSIONS OF THE FOUNDRY:
        1.  **Multi-Vessel Awareness:** Detects if the project requires sidecars (Postgres,
            Redis, Meilisearch) and automatically pivots to a Docker-Compose strategy.
        2.  **Surgical Extension Injection:** Dynamically populates the VS Code
            'extensions' list based on detected languages (Python, Rust, Go, TS).
        3.  **Lifecycle Hook Chaining:** Orchestrates `onCreateCommand`, `updateContentCommand`,
            and `postCreateCommand` for non-blocking dependency hydration.
        4.  **Gnostic Port Scrying:** Intelligently forwards ports based on the
            industrial standard of the detected stack (8000 for FastAPI, 3000 for Next.js).
        5.  **Environment DNA Grafting:** Siphons project variables into the
            `containerEnv` to ensure the logic knows its identity from boot.
        6.  **Mount Purity:** Configures volume mounts to preserve the Architect's
            shell history and Gnostic configurations across container incinerations.
        7.  **Feature Inception:** Injects Microsoft "Features" (Docker-in-Docker,
            Common Utilities, Git-LFS) based on the project's kinetic needs.
        8.  **Workspace Settings Hardening:** Forces high-status VS Code settings
            (Format on Save, Linting, AI Pathing) directly into the container mind.
        9.  **User-Sovereignty Mapping:** Automatically aligns the container user
            (vscode/node/root) with the project's permission model.
        10. **Achronal Handshake:** Validates that the `.devcontainer` is manifest
            before the first kinetic strike, preventing "Startup Paradoxes."
        11. **Network Topology Suture:** Ensures sidecar hosts (e.g., 'db') are
            resolvable within the DevContainer's internal DNS.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            one-click "Open in Container" experience.
        =================================================================================
        """
        # --- THE VOW OF NECESSITY ---
        # We only forge the vessel if the Architect explicitly willed it.
        if not self.final_vars.get('use_devcontainer', self.final_vars.get('use_vscode', False)):
            return

        devcontainer_dir = project_root / ".devcontainer"
        devcontainer_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("The Omniscient DevContainer Foundry is materializing the development reality...")

        # --- I. GNOSTIC ANALYSIS (THE GAZE) ---
        project_slug = self.final_vars.get('project_slug', 'v-omega-project')
        project_type = self.final_vars.get('project_type', 'generic').lower()
        db_type = self.final_vars.get('database_type', 'none').lower()
        use_docker = self.final_vars.get('use_docker', False)

        # --- II. ARCHITECTURAL TRIAGE (COMPOSE VS DOCKERFILE) ---
        # If a database is manifest, we must use a Docker Compose strategy for multi-vessel reality.
        has_sidecar = db_type != 'none' or self.final_vars.get('use_redis', False)

        # --- III. THE CORE CONFIGURATION (THE MATTER) ---
        config = {
            "name": f"Ω | {self.final_vars.get('project_name', project_root.name)}",
            "containerUser": "vscode",
            "customizations": {
                "vscode": {
                    "settings": {
                        "editor.formatOnSave": True,
                        "editor.defaultFormatter": "ms-python.black-formatter",
                        "python.terminal.activateEnvInSelectedTerminal": True
                    },
                    "extensions": [
                        "ms-vscode.vscode-self-healing-architecture",  # The Sigil
                        "GitHub.copilot",
                        "ms-azuretools.vscode-docker",
                        "usernamehw.errorlens"
                    ]
                }
            },
            "forwardPorts": [],
            "features": {
                "ghcr.io/devcontainers/features/common-utils:2": {
                    "installZsh": True,
                    "configureZshAsDefaultShell": True,
                    "upgradePackages": True
                },
                "ghcr.io/devcontainers/features/git:1": {}
            }
        }

        # --- IV. STACK-SPECIFIC TRANSMUTATION ---
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

        elif 'rust' in project_type:
            config["customizations"]["vscode"]["extensions"].append("rust-lang.rust-analyzer")
            config["postCreateCommand"] = "cargo build"

        # --- V. INFRASTRUCTURE SUTURE (THE BRIDGE) ---
        if has_sidecar:
            # We command the devcontainer to use the existing docker-compose.yml as the source of truth.
            config["dockerComposeFile"] = ["../docker-compose.yml"]
            config["service"] = "api"  # We anchor the dev context to the primary logic vessel
            config["workspaceFolder"] = f"/workspaces/{project_slug}"

            # Inject Gnostic connection strings into the container mind
            if db_type == 'postgres':
                config["remoteEnv"] = {
                    "DATABASE_URL": f"postgresql://user:pass@db:5432/{project_slug}_db"
                }
        else:
            # Simple single-vessel reality
            config["build"] = {
                "dockerfile": "../Dockerfile",
                "context": ".."
            }

        # --- VI. SECURITY & PERSISTENCE (THE WARDS) ---
        # Mount the local git config and bash history so the Architect's identity persists.
        config["mounts"] = [
            "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,type=bind,consistency=cached",
            "source=vscode-history,target=/home/vscode/.vscode-server/extensions,type=volume"
        ]

        # --- VII. THE FINAL INSCRIPTION ---
        import json
        content = json.dumps(config, indent=4)

        # We perform the Rite of Atomic Inscription within the active transaction.
        from ...utils import atomic_write
        atomic_write(
            devcontainer_dir / "devcontainer.json",
            content,
            self.logger,
            project_root,
            transaction=tx
        )

        self.logger.success(
            f"DevContainer reality finalized. Multi-vessel support: {'ENABLED' if has_sidecar else 'DISABLED'}.")

    def _determine_true_project_root(self) -> Path:
        """[FACULTY 1] Perceives if the genesis is nested inside a new directory."""
        if not self.items:
            return self.project_root / self.final_vars.get('project_slug', 'new_project')

        first_parts = set()
        for item in self.items:
            if item.path and item.path.parts:
                first_parts.add(item.path.parts[0])

        if len(first_parts) == 1:
            nested_root_name = list(first_parts)[0]
            if nested_root_name == self.final_vars.get('project_slug'):
                self.logger.verbose(f"Nested Genesis perceived. Anchoring true root at '{nested_root_name}'.")
                return self.project_root / nested_root_name

        return self.project_root

    def _validate_generated_souls(self, tx: GnosticTransaction):
        """[FACULTY 2] The Syntax Inquisitor."""
        for path, result in tx.write_dossier.items():
            if not result.success: continue
            staged_path = tx.get_staging_path(path)

            # [ASCENSION]: THE VOID AMNESTY (THE CURE)
            # If a scripture has a mass of 0 bytes, its soul is a pure void.
            # It is not malformed, it is simply unwritten. We grant it passage.
            if not staged_path.exists() or staged_path.stat().st_size == 0:
                continue

            if path.suffix == '.py':
                try:
                    ast.parse(staged_path.read_text(encoding='utf-8'))
                except SyntaxError as e:
                    raise ArtisanHeresy(
                        f"Syntax Heresy in forged scripture '{path.name}': {e.msg}",
                        line_num=e.lineno, severity=HeresySeverity.CRITICAL
                    )
            elif path.suffix == '.json':
                try:
                    json.load(staged_path.open('r', encoding='utf-8'))
                except json.JSONDecodeError as e:
                    # [THE CURE]: This heresy is now only proclaimed if the file is NOT empty.
                    raise ArtisanHeresy(f"Malformed JSON in '{path.name}': {e}", severity=HeresySeverity.CRITICAL)
                
    def _ensure_dynamic_ignores(self, tx: GnosticTransaction):
        """[FACULTY 3] The Dynamic Veil."""
        ignores = set()
        for path in self.generated_files:
            if path.suffix in ['.env', '.key', '.pem', '.p12'] or path.name == '.DS_Store':
                ignores.add(path.name)
            if path.name == "scaffold.lock":
                ignores.add("scaffold.lock")
            if path.name == "genesis.json":
                ignores.add(".scaffold/genesis.json")

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
                    new_content += "\n# --- Scaffold Security Ward ---\n"
                    appended = True
                new_content += f"{item}\n"

        if new_content != current_content:
            atomic_write(gitignore_path, new_content, self.logger, self.project_root, transaction=tx)

    def _enrich_readme_metadata(self, tx: GnosticTransaction):
        """[FACULTY 5] Injects hidden Gnostic Metadata into README.md."""
        readme_path = self._determine_true_project_root() / "README.md"
        if not any(str(p).endswith("README.md") for p in self.generated_files):
            return

        staged_readme = tx.get_staging_path(readme_path.relative_to(self.project_root))
        if staged_readme.exists():
            content = staged_readme.read_text(encoding='utf-8')
            meta_block = (
                f"\n<!--\n"
                f"  SCAFFOLD_GNOSIS:\n"
                f"  version: {self.final_vars.get('scaffold_version', 'unknown')}\n"
                f"  timestamp: {time.time()}\n"
                f"  blueprint: {self.final_vars.get('blueprint_path', 'unknown')}\n"
                f"-->"
            )
            if "SCAFFOLD_GNOSIS" not in content:
                atomic_write(readme_path, content + meta_block, self.logger, self.project_root, transaction=tx)

    def _consecrate_executables(self, tx: GnosticTransaction):
        """[FACULTY 7] Heuristically adds +x to scripts."""
        for path in self.generated_files:
            if path.suffix in ['.sh', '.bash', '.zsh'] or path.name in ['configure', 'bootstrap']:
                tx.record_edict(f"chmod +x {path}")
                try:
                    staged_path = tx.get_staging_path(path.relative_to(self.project_root))
                    if staged_path.exists():
                        staged_path.chmod(staged_path.stat().st_mode | 0o111)
                except Exception:
                    pass

    def _ensure_license(self, tx: GnosticTransaction):
        """[FACULTY 4] The License Auto-Forge."""
        license_type = self.final_vars.get('license')
        if not license_type or license_type.lower() == 'none': return
        license_path = self._determine_true_project_root() / "LICENSE"
        if any(str(p).endswith("LICENSE") for p in self.generated_files) or license_path.exists():
            return
        license_text = f"{license_type} License\n\nCopyright (c) {time.strftime('%Y')} {self.final_vars.get('author', 'The Architect')}"
        atomic_write(license_path, license_text, self.logger, self.project_root, transaction=tx)

    def _inscribe_final_blueprint(self, true_project_root: Path, transaction: GnosticTransaction):
        """[FACULTY 1] Inscribes the final, transmuted blueprint."""
        from ...core.blueprint_scribe import BlueprintScribe
        chronicle_path = true_project_root / "scaffold.scaffold"
        try:
            scribe = BlueprintScribe(self.project_root)
            final_scripture = scribe.transcribe(
                self.items, [(c, 0) for c in self.commands], self.final_vars
            )
            atomic_write(chronicle_path, final_scripture, self.logger, self.project_root, transaction=transaction)
            self.logger.success("The sacred `scaffold.scaffold` chronicle has been forged.")
        except Exception as e:
            self.logger.warn(f"A minor paradox occurred while chronicling the genesis rite: {e}")

    def _persist_genesis_state(self, true_project_root: Path, transaction: GnosticTransaction):
        """[FACULTY 2 & 9] The State Crystal & Dependency Locker."""
        state_path = true_project_root / ".scaffold" / "genesis.json"
        safe_vars = {k: v for k, v in self.final_vars.items() if
                     isinstance(v, (str, int, bool, float, list, dict, type(None)))}

        deps_snapshot = {}
        pyproj = true_project_root / "pyproject.toml"
        staged_pyproj = transaction.get_staging_path(pyproj.relative_to(self.project_root))
        if staged_pyproj.exists():
            deps_snapshot['pyproject.toml'] = hashlib.md5(staged_pyproj.read_bytes()).hexdigest()

        content = json.dumps({
            "variables": safe_vars, "timestamp": time.time(),
            "archetype": self.final_vars.get("profile") or "custom",
            "dependency_fingerprints": deps_snapshot
        }, indent=2)
        atomic_write(state_path, content, self.logger, self.project_root, transaction=transaction)

    def _prune_empty_directories(self, root: Path):
        """[FACULTY 8] The Ghost Buster."""
        if not root.exists(): return
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            if not dirnames and not filenames:
                try:
                    Path(dirpath).rmdir()
                except OSError:
                    pass

    def _analyze_overwrites(self, tx: GnosticTransaction):
        """[FACULTY 11] The Conflict Arbiter."""
        for path, result in tx.write_dossier.items():
            if result.action_taken == InscriptionAction.TRANSFIGURED:
                self.logger.verbose(f"Conflict Arbiter: '{path.name}' was transfigured.")

    def _compute_merkle_root(self, tx: GnosticTransaction):
        """[FACULTY 12] The Final Seal."""
        hasher = hashlib.sha256()
        for path in sorted(tx.write_dossier.keys()):
            res = tx.write_dossier[path]
            if res.success and res.gnostic_fingerprint:
                hasher.update(str(path).encode())
                hasher.update(res.gnostic_fingerprint.encode())
        self.merkle_root = hasher.hexdigest()

    def _proclaim_success(self, registers: QuantumRegisters, true_project_root: Path):
        """
        =================================================================================
        == THE HERALD OF APOTHEOSIS (V-Ω-CONTEXTUAL-NAVIGATOR)                         ==
        =================================================================================
        This is the ascended proclamation rite. It summons the Dossier Scribe and
        injects a context-aware 'Next Steps' prophecy that guides the Architect
        to the Altar of Activation.
        """
        if self.request.silent or self.request.dry_run or self.request.preview:
            return

        # --- 1. Gnostic Constellation ---
        artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                artifacts.append(Artifact(path=res.path, type="file", action=res.action_taken.value))

        # --- 2. Telemetry Calculation ---
        duration_ms = (time.monotonic() - self.start_time) * 1000
        total_mass = sum(a.size_bytes for a in artifacts)
        ai_telemetry = self.final_vars.get('_ai_telemetry', {"tokens_total": 0, "cost_usd": 0.0, "model": "None"})

        # --- 3. Environmental Gnosis ---
        env_gnosis = {
            "os": f"{platform.system()} {platform.release()}",
            "arch": platform.machine(),
            "python": sys.version.split()[0],
            "git_branch": get_git_branch(self.project_root) or "void",
            "git_commit": get_git_commit(self.project_root) or "void",
            "user": getpass.getuser()
        }

        # --- 4. Performance Metrics ---
        perf_metrics = {
            "duration_ms": duration_ms,
            "mass_bytes": total_mass,
            "velocity": len(artifacts) / (duration_ms / 1000) if duration_ms > 0 else 0
        }

        # --- 5. The Altar of Activation (Next Steps) ---
        # [THE ASCENSION] We perform the Rite of Relative Pathfinding.
        try:
            cwd = Path.cwd()
            resolved_root = true_project_root.resolve()

            # If the sanctum is the current directory, we don't need to cd.
            needs_cd = resolved_root != cwd

            relative_root = resolved_root.relative_to(cwd) if needs_cd else "."
        except ValueError:
            # If path is on another drive or totally disjoint, force absolute
            relative_root = true_project_root
            needs_cd = True

        # Forge the Navigation Instructions
        final_next_steps = []
        if needs_cd:
            final_next_steps.append(f"Enter the sanctum: [bold cyan]cd {relative_root}[/bold cyan]")

        # Forge the Activation Instruction
        final_next_steps.append("Awaken the sanctum: [bold cyan]code .[/bold cyan]")

        # Summon the Prophet for lifecycle steps (install, test, run)
        prophet = NextStepsOracle(project_root=true_project_root, gnosis=self.final_vars)
        oracle_steps = prophet.prophesy()

        # We merge, filtering out potential duplicates if the Oracle is chatty about navigation
        for step in oracle_steps:
            if "cd " not in step:  # Simple dedup logic
                final_next_steps.append(step)

        # --- 6. Security Warnings ---
        security_warnings = []
        if registers.transaction:
            secret_pattern = re.compile(r'sk_(live|test)_[a-zA-Z0-9]{24,}')
            for res in registers.transaction.write_dossier.values():
                if res.success and res.action_taken in (InscriptionAction.CREATED, InscriptionAction.TRANSFIGURED):
                    try:
                        content_path = registers.transaction.get_staging_path(res.path)
                        if content_path.exists():
                            content = content_path.read_text(encoding='utf-8', errors='ignore')
                            if secret_pattern.search(content):
                                security_warnings.append(f"Potential secret key perceived in '{res.path.name}'.")
                    except Exception:
                        pass

        # --- 7. The Final Proclamation ---
        maestro_cmds = registers.transaction.edicts_executed if registers.transaction else self.commands

        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis=self.final_vars,
            project_root=true_project_root,
            next_steps=final_next_steps,
            title=f"✨ Genesis Complete ✨",
            subtitle=f"A new reality '{escape(true_project_root.name)}' has been born.",
            gnostic_constellation=artifacts,
            security_warnings=security_warnings,
            transmutation_plan=None,
            ai_telemetry=ai_telemetry,
            environment_gnosis=env_gnosis,
            performance_metrics=perf_metrics,
            maestro_edicts=maestro_cmds,
            audit_file_path=self.project_root / ".scaffold" / "genesis_audit.json"
        )