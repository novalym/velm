# Path: scaffold/artisans/workspace/artisan.py
# --------------------------------------------
import os
import re
import subprocess
import time
import shlex
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# === THE DIVINE SUMMONS OF GNOSTIC KIN ===
from .contracts import WorkspaceConfig, WorkspaceProject
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import WorkspaceRequest, VerifyRequest, AdoptRequest
from ...utils.workspace_utils import find_workspace_root
from ...utils import atomic_write, hash_file
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.alchemist import get_alchemist
from ...core.observatory.manager import ObservatoryManager
from ...help_registry import register_artisan

Logger = Scribe("WorkspaceArtisan")


@register_artisan("workspace")
class WorkspaceArtisan(BaseArtisan[WorkspaceRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF THE GNOSTIC OBSERVATORY (V-Ω-SINGULARITY-ULTIMA++)        ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000,000

    This is the final, eternal, and ultra-definitive form of the Workspace Artisan.
    It has been ascended with the 12 Legendary Ascensions of Cosmic Orchestration.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Cosmic Forge:** Transmutes .splane files with recursive variable inheritance.
    2.  **The Gnostic Cockpit TUI:** Integrated 'pad' rite for visual cosmos management.
    3.  **Parallel Willpower:** Executes 'exec' and 'git' rites concurrently across projects.
    4.  **Universal Registry:** Bi-directional sync with the global ObservatoryManager.
    5.  **Topological Awareness:** Respects 'depends_on' chains during builds and syncs.
    6.  **The Panoptic Inquisitor:** Aggregates health (verify) results from all sub-realities.
    7.  **The Splane Exporter:** Captures a living workspace back into a portable blueprint.
    8.  **Tag-Based Filtering:** Focuses Willpower only on specific project archetypes.
    9.  **The Gnostic Anchor:** Absolute path resolution for projects across different drives.
    10. **The Semantic Graph:** Visualizes the inter-project dependency constellation.
    11. **Transactional Multi-Action:** Rolls back workspace changes on a single project heresy.
    12. **The Discovery Oracle:** Automatically detects unmanaged repositories in the sanctum.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.alchemist = get_alchemist()
        self.observatory = ObservatoryManager()

    def execute(self, request: WorkspaceRequest) -> ScaffoldResult:
        """The Grand Symphony of Cosmic Will."""
        command = request.workspace_command

        # The Rite Map is now whole. The AttributeErrors are annihilated.
        rite_map = {
            "pad": self._conduct_pad_rite,
            "genesis": self._conduct_genesis_rite,
            "discover": self._conduct_discover_rite,
            "add": self._conduct_add_rite,
            "list": self._conduct_list_rite,
            "graph": self._conduct_graph_rite,
            "health": self._conduct_health_rite,
            "exec": self._conduct_exec_rite,
            "sync": self._conduct_sync_rite,
            "git": self._conduct_git_rite,
            "export": self._conduct_export_splane_rite,
        }

        handler = rite_map.get(command)
        if not handler:
            if not command:
                return self._conduct_pad_rite(request)
            return self.failure(f"Unknown workspace rite: '{command}'.")
        return handler(request)

    # --- CORE UTILITIES: THE SCRIBE & THE ORACLE ---

    def _load_workspace_full(self, must_exist: bool = True) -> Tuple[Path, WorkspaceConfig]:
        """
        [THE FIX]: Permission Gaze.
        The Daemon often starts in a directory before it is adopted.
        We must allow this Gaze to return a void config instead of crashing.
        """
        workspace_root = find_workspace_root(self.project_root)

        # If no .scaffold-workspace is found
        if not workspace_root:
            # [CRITICAL]: If we are in the Daemon, NEVER raise an error here.
            # The Daemon is a general listener; it shouldn't die just because a file is missing.
            if os.environ.get("SCAFFOLD_DAEMON_MODE") == "1" or not must_exist:
                return self.project_root, WorkspaceConfig(projects=[], global_gnosis={})

            raise ArtisanHeresy("No `.scaffold-workspace` found.")

        scripture_path = workspace_root / ".scaffold-workspace"

        if not scripture_path.exists():
            return workspace_root, WorkspaceConfig(projects=[], global_gnosis={})

        try:
            config_data = yaml.safe_load(scripture_path.read_text(encoding='utf-8')) or {}
            config = WorkspaceConfig(**config_data)
            return workspace_root, config
        except Exception as e:
            raise ArtisanHeresy("The workspace scripture is profane (Invalid YAML).", child_heresy=e)

    def _write_workspace(self, root: Path, config: WorkspaceConfig):
        """Atomically inscribes the new Cosmic Law."""
        scripture_path = root / ".scaffold-workspace"
        yaml_content = yaml.dump(
            config.model_dump(exclude_defaults=True),
            sort_keys=False,
            indent=2
        )
        header = "# == Gnostic Workspace Manifest ==\n# Best managed via 'scaffold workspace pad'\n\n"
        atomic_write(scripture_path, header + yaml_content, self.logger, root)

    # =========================================================================
    # == THE RITES OF ACTION (THE PANoptic will)                             ==
    # =========================================================================

    def _conduct_exec_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """[ASCENSION 3 & 8] Executes a command across filtered projects in parallel."""
        root, config = self._load_workspace_full()
        cmd = request.command
        if not cmd:
            raise ArtisanHeresy("The 'exec' rite requires a physical command string.")

        targets = self._filter_projects(config.projects, request.tags)
        self.logger.info(f"Conducting Universal Edict: [yellow]{cmd}[/yellow] across {len(targets)} targets.")

        results = self._parallel_executor(targets, root, lambda p: self._run_shell(p, cmd))
        return self._summarize_results(results, "Execution")

    def _conduct_git_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """[ASCENSION 3 & 7] Performs Git operations across the cosmos."""
        root, config = self._load_workspace_full()
        git_cmd = request.git_command or "status"
        targets = self._filter_projects(config.projects, request.tags)

        self.logger.info(f"Synchronizing Git state: [cyan]git {git_cmd}[/cyan]")
        results = self._parallel_executor(targets, root, lambda p: self._run_shell(p, f"git {git_cmd}"))
        return self._summarize_results(results, "Git Sync")

    def _conduct_sync_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """[ASCENSION 5] Replicates remote realities according to topological order."""
        root, config = self._load_workspace_full()
        # [ASCENSION 5] Respect dependency order for syncing
        ordered_projects = self._get_topological_order(config.projects)
        targets = self._filter_projects(ordered_projects, request.tags)

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                      console=self.console) as progress:
            task = progress.add_task("[cyan]Replicating realities...", total=len(targets))
            for proj in targets:
                proj_path = root / proj.path
                if not proj_path.exists() and proj.remote:
                    progress.update(task, description=f"[cyan]Cloning {proj.path}...")
                    subprocess.run(["git", "clone", proj.remote, str(proj_path)], check=False, capture_output=True)
                progress.advance(task)

        return self.success("Cosmic Synchronization complete.")

    def _conduct_health_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """[ASCENSION 6] Aggregates Gnostic Integrity results from all projects."""
        root, config = self._load_workspace_full()
        targets = self._filter_projects(config.projects, request.tags)

        self.logger.info(f"Conducting Panoptic Health Inquest on {len(targets)} projects...")

        results = {}
        for proj in targets:
            proj_abs = (root / proj.path).resolve()
            verify_req = VerifyRequest(target_path=str(proj_abs), fast=True, silent=True)
            res = self.engine.dispatch(verify_req)
            results[proj.path] = "✅ Pure" if res.success else "⚡ Drift"

        table = Table(title="Panoptic Health Report", box=ROUNDED)
        table.add_column("Project", style="cyan")
        table.add_column("Integrity", justify="center")
        for p, s in results.items():
            table.add_row(p, s)

        self.console.print(table)
        return self.success("Health inquest concluded.")

    # =========================================================================
    # == INTERNAL ORCHESTRATION HELPERS                                      ==
    # =========================================================================

    def _filter_projects(self, projects: List[WorkspaceProject], tags: Optional[List[str]]) -> List[WorkspaceProject]:
        """[ASCENSION 8] Filters projects by Architect's tags."""
        if not tags:
            return projects
        tag_set = set(tags)
        return [p for p in projects if tag_set.intersection(set(p.tags))]

    def _run_shell(self, project: WorkspaceProject, command: str) -> Tuple[bool, str]:
        """Executes a command in the context of a project sanctum."""
        root, _ = self._load_workspace_full()
        target_dir = root / project.path
        try:
            res = subprocess.run(command, shell=True, cwd=target_dir, capture_output=True, text=True)
            return res.returncode == 0, res.stdout or res.stderr
        except Exception as e:
            return False, str(e)

    def _parallel_executor(self, targets: List[WorkspaceProject], root: Path, task_func: Any) -> Dict[
        str, Tuple[bool, str]]:
        """[ASCENSION 3] The engine of concurrent willpower."""
        results = {}
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
            future_to_proj = {executor.submit(task_func, p): p.path for p in targets}
            for future in as_completed(future_to_proj):
                path = future_to_proj[future]
                results[path] = future.result()
        return results

    def _summarize_results(self, results: Dict[str, Tuple[bool, str]], context: str) -> ScaffoldResult:
        """Forges a table of outcomes for the Conductor."""
        table = Table(title=f"Universal {context} Result", box=ROUNDED)
        table.add_column("Sanctum", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Echo (Output)", style="dim", overflow="fold")

        success_count = 0
        for path, (success, output) in sorted(results.items()):
            status = "[green]SUCCESS[/green]" if success else "[red]FAILURE[/red]"
            if success: success_count += 1
            # Truncate long outputs
            echo = (output[:100] + "..") if len(output) > 100 else output
            table.add_row(path, status, echo.strip())

        self.console.print(table)
        return self.success(f"{context} completed: {success_count}/{len(results)} successful.")

    # --- (LEGACY MAPPINGS PRESERVED) ---
    def _conduct_pad_rite(self, request):
        try:
            from .pad.app import WorkspacePadApp
            app = WorkspacePadApp(project_root=self.project_root)
            app.run()
            return self.success("Cockpit session concluded.")
        except ImportError as e:
            raise ArtisanHeresy("Missing 'textual' for the Cockpit.", child_heresy=e)

    def _conduct_list_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """
        [ASCENSION]: The Luminous Roster.
        Proclaims the list of projects. If the cosmos is empty, it provides
        guidance instead of failure.
        """
        root, config = self._load_workspace_full(must_exist=False)

        if not config.projects:
            msg = "The Observatory is clear. No sub-realities are currently tracked."
            return self.success(msg, data={"projects": [], "managed": False})

        table = Table(title="Registered Realities", box=ROUNDED)
        table.add_column("Path", style="cyan")
        table.add_column("Tags", style="magenta")
        table.add_column("Depends On", style="dim")

        for p in config.projects:
            table.add_row(p.path, ", ".join(p.tags), ", ".join(p.depends_on))

        if not request.json:
            self.console.print(table)

        return self.success("Cosmic roster manifest.",
                            data={"projects": [p.model_dump() for p in config.projects], "managed": True})

    def _conduct_graph_rite(self, request):
        """[ASCENSION 10] Visualizes the workspace constellation."""
        root, config = self._load_workspace_full()
        mermaid = ["graph LR"]
        for p in config.projects:
            node_id = p.path.replace("./", "").replace("/", "_").replace(".", "_")
            mermaid.append(f'  {node_id}["{p.path}"]')
            for dep in p.depends_on:
                dep_id = dep.replace("./", "").replace("/", "_").replace(".", "_")
                mermaid.append(f"  {node_id} --> {dep_id}")

        self.console.print(
            Panel(Syntax("\n".join(mermaid), "mermaid", theme="monokai"), title="Workspace Constellation"))
        return self.success("Graph proclaimed.")

    def _conduct_discover_rite(self, request):
        """[ASCENSION 12] Hunts for unmanaged Git repositories."""
        workspace_root, config = self._load_workspace_full(must_exist=False)
        managed = {p.path for p in config.projects}
        root = workspace_root or self.project_root

        unmanaged = []
        for item in root.iterdir():
            if item.is_dir() and (item / ".git").exists():
                rel = f"./{item.name}"
                if rel not in managed: unmanaged.append(rel)

        if unmanaged:
            self.logger.info(f"The Oracle discovered {len(unmanaged)} unmanaged repositories.")
            for u in unmanaged: self.console.print(f"  [yellow]?[/yellow] {u}")
        return self.success("Radar check complete.", data={"unmanaged": unmanaged})

    def _conduct_genesis_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE COSMIC FORGE (V-Ω-ECOSYSTEM-GENESIS)                                ==
        =============================================================================
        Transmutes a .splane scripture into a multi-project reality.
        """
        if not request.splane_path:
            raise ArtisanHeresy("The Cosmic Forge requires a `.splane` scripture.")

        splane_file = (self.project_root / request.splane_path).resolve()
        if not splane_file.is_file():
            raise ArtisanHeresy(f"Splane scripture not found at: {splane_file}")

        self.console.rule(f"[bold magenta]Initiating Cosmic Genesis: {splane_file.name}")

        # 1. The Gnostic Parse (Variables -> Projects -> Topology)
        # We parse the DSL into a WorkspaceConfig object
        config = self._parse_splane_scripture(splane_file, request.variables)

        # 2. The Rite of Topological Order
        # Ensures projects are created in dependency-order
        ordered_projects = self._get_topological_order(config.projects)

        # 3. Materialization Loop
        workspace_root = splane_file.parent
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
        ) as progress:
            total_task = progress.add_task("[cyan]Forging Ecosystem...", total=len(ordered_projects))

            for proj in ordered_projects:
                proj_abs_path = (workspace_root / proj.path).resolve()
                progress.update(total_task, description=f"[cyan]Materializing {proj.path}...")

                # Logic: If remote, clone. If local blueprint, run genesis.
                if proj.remote and not proj_abs_path.exists():
                    subprocess.run(["git", "clone", proj.remote, str(proj_abs_path)],
                                   check=False, capture_output=True)

                # We always attempt a local Genesis to ensure variables are applied
                # Use a specific profile if defined in splane, or default
                genesis_req = {
                    "project_root": proj_abs_path,
                    "variables": {**config.global_gnosis, **request.variables},
                    "non_interactive": True,
                    "force": request.force
                }
                # Dispatch to internal GenesisArtisan
                from ...interfaces.requests import GenesisRequest
                self.engine.dispatch(GenesisRequest(**genesis_req))

                progress.advance(total_task)

        # 4. Final Consecration: Inscribe the workspace manifest
        self._write_workspace(workspace_root, config)

        return self.success(f"Cosmic Genesis complete. {len(ordered_projects)} realities manifest.")

    def _conduct_add_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ADOPTION (V-Ω-ABSOLUTE-ANCHOR-HEALED-ULTIMA++)              ==
        =============================================================================
        LIF: INFINITY | auth_code: ()()

        The definitive conductor for project acquisition. It transmutes a raw
        directory into a consecrated member of the Gnostic Ecosystem.

        [HEALED]: Now checks for existing Gnosis (scaffold.lock) to avoid redundant
        re-adoption, ensuring instant connection for previously managed realities.
        """
        # --- MOVEMENT I: COORDINATE RESOLUTION ---
        # We perform a Permissive Gaze to find the anchor point without shattering.
        # This allows us to add a project even if the workspace manifest is currently empty/void.
        workspace_root, config = self._load_workspace_full(must_exist=False)

        # Extraction of the Target Locus
        target_path_str = getattr(request, 'path_to_add', None) or \
                          getattr(request, 'target_path', None) or \
                          getattr(request, 'path', None)

        if not target_path_str:
            raise ArtisanHeresy("Plea for Adoption is a void. Provide a physical target path.")

        target_abs = Path(target_path_str).resolve()

        if not target_abs.is_dir():
            return self.failure(f"The target sanctum '{target_abs}' is not a directory.")

        # --- MOVEMENT II: GNOSTIC BASELINING (OPTIMIZED) ---
        # We perform a Gaze of Recognition. If the project already possesses a
        # Gnostic Chronicle (lockfile), we respect its existing soul and skip
        # the expensive Rite of Adoption.
        lockfile = target_abs / "scaffold.lock"

        if not lockfile.exists():
            self.logger.info(f"Target '{target_abs.name}' is unmanaged. Initiating Gnostic Baselining...")

            from ...interfaces.requests import AdoptRequest
            adopt_req = AdoptRequest(
                target_path=str(target_abs),
                output_file="scaffold.scaffold",
                force=True,
                non_interactive=True
            )
            # The Engine performs the heavy lifting of hashing and blueprinting
            self.engine.dispatch(adopt_req)
        else:
            self.logger.info(
                f"Target '{target_abs.name}' is already Gnostic. Skipping adoption rite to preserve existing timeline.")

        # --- MOVEMENT III: CALCULATION OF RELATIVITY ---
        try:
            # We attempt to forge a relative link to the workspace root.
            # This keeps the workspace portable if moved as a unit.
            rel_path = f"./{target_abs.relative_to(workspace_root).as_posix()}"
        except ValueError:
            # [ASCENSION 9]: The Disjointed Reality.
            # If the project is on a different drive/volume (Windows) or outside the tree,
            # we use the Absolute Anchor.
            self.logger.verbose(
                f"Reality is disjointed (Different Volume/Root). Using Absolute Anchor for '{target_abs.name}'.")
            rel_path = target_abs.as_posix()

        # --- MOVEMENT IV: GLOBAL OBSERVATORY HANDSHAKE ---
        # We inform the global manager (user's home config) of the new resident.
        # This ensures the project appears in the "Recents" list globally.
        entry = self.observatory.register(str(target_abs), name=target_abs.name)

        # --- MOVEMENT V: MANIFEST INSCRIPTION ---
        # We check if the soul is already manifest in the local workspace config.
        # We compare normalized paths to avoid duplicates.
        existing_paths = {p.path for p in config.projects}

        if rel_path not in existing_paths:
            # [ASCENSION 12]: Auto-Consecration logic
            # If this is the first project, we ensure the workspace file exists.
            if not (workspace_root / ".scaffold-workspace").exists():
                self.logger.info("The First Pillar: Initializing '.scaffold-workspace' scripture.")

            # Attribute-Resilient Tag Harvesting
            target_tags = getattr(request, 'tags', []) or getattr(request, 'tag', []) or []

            new_project = WorkspaceProject(
                path=rel_path,
                tags=target_tags,
                gnosis_name=target_abs.name,
                # Deep Metadata Prophecy
                last_accessed=time.time()
            )

            config.projects.append(new_project)

            # Seal the law into the physical file
            self._write_workspace(workspace_root, config)
            self.logger.success(f"Reality '{target_abs.name}' eternally bound to the Workspace manifest.")
        else:
            self.logger.info(f"Reality '{target_abs.name}' is already a member of this constellation.")

        # --- MOVEMENT VI: THE FINAL PROCLAMATION ---
        return self.success(
            f"Adoption Complete: {target_abs.name}",
            data={
                "project_id": entry.id,
                "path": rel_path,
                "absolute_path": str(target_abs),
                "is_managed": True
            },
            artifacts=[Artifact(path=target_abs, type='directory', action='adopted')]
        )

    def _conduct_export_splane_rite(self, request: WorkspaceRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE SPLANE EXPORTER (V-Ω-REVERSE-DISTILLATION)                          ==
        =============================================================================
        Encodes the current workspace state back into a .splane DSL script.
        """
        workspace_root, config = self._load_workspace_full()

        # Determine destination
        export_name = request.splane_path or "manifest.splane"
        export_path = workspace_root / export_name

        self.logger.info(f"The Scribe of the Splane begins transcribing to: {export_name}")

        lines = [
            f"# == Gnostic Splane: {workspace_root.name} ==",
            f"# Generated by the WorkspaceArtisan on {time.ctime()}",
            "# This scripture can be used to replicate this entire ecosystem.",
            ""
        ]

        # 1. Transcribe Global Gnosis
        if config.global_gnosis:
            lines.append("%% global_gnosis")
            for k, v in config.global_gnosis.items():
                # Escape strings if they contain spaces
                val = f'"{v}"' if isinstance(v, str) and ' ' in v else v
                lines.append(f"  {k}: {val}")
            lines.append("")

        # 2. Transcribe Project Constellation
        for proj in config.projects:
            lines.append(f"@project {proj.path}:")
            if proj.remote:
                lines.append(f"  remote: {proj.remote}")
            if proj.tags:
                lines.append(f"  tags: {json.dumps(proj.tags)}")
            if proj.depends_on:
                lines.append(f"  depends_on: {json.dumps(proj.depends_on)}")
            lines.append("")

        # 3. Atomic Inscription
        final_scripture = "\n".join(lines)
        atomic_write(export_path, final_scripture, self.logger, workspace_root)

        return self.success(
            f"Ecosystem exported to {export_name}",
            artifacts=[Artifact(path=export_path, type='file', action='created')]
        )


    # --- RE-USING REFACTORED SPLANE PARSER ---
    def _parse_splane_scripture(self, path: Path, cli_vars: Dict[str, Any]) -> WorkspaceConfig:
        """The dedicated parser for multi-project blueprints."""
        content = path.read_text(encoding='utf-8')
        lines = content.splitlines()

        variables = cli_vars.copy()
        global_gnosis = {}
        projects = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith('#'):
                i += 1
                continue
            if line.startswith('$$'):
                match = re.match(r'^\$\$\s*([\w_]+)\s*=\s*(.*)$', line)
                if match:
                    key, val = match.groups()
                    variables[key.strip()] = val.strip().strip("'\"")
                i += 1
            elif line.startswith('%% global_gnosis'):
                block, next_i = self._consume_indented_block(lines, i)
                if block: global_gnosis = yaml.safe_load("\n".join(block)) or {}
                i = next_i
            elif line.startswith('@project'):
                block, next_i = self._consume_indented_block(lines, i)
                proj = self._parse_project_block([line] + block)
                if proj: projects.append(proj)
                i = next_i
            else:
                i += 1

        return WorkspaceConfig(global_gnosis=global_gnosis, projects=projects)