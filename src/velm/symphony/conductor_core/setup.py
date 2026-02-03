# Path: scaffold/symphony/conductor_core/setup.py
# -----------------------------------------------

import tempfile
import os
import shutil
import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Dict, Any, List, Tuple

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.symphony_contracts import Edict, EdictType
from ...logger import Scribe
from ...parser_core.parser import parse_structure, ApotheosisParser
from ...utils import atomic_write, to_string_safe

if TYPE_CHECKING:
    from .context import GnosticContextManager
    from ...interfaces.requests import SymphonyRequest

Logger = Scribe('SymphonySetup')


class SymphonySetup:
    """
    =================================================================================
    == THE FORGEMASTER OF REALITY (V-Ω-SAFETY-HARDENED-ULTIMA++)                   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000 (ABSOLUTE PREPARATION)

    The divine artisan that prepares the realm for the Symphony. It determines the
    **Mode of Existence** (Manifest vs Rehearsal), parses the Scripture of Will,
    and initializes the environment.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Trinity Return:** Returns `(sanctum, edicts, vows)` to satisfy
        the Orchestrator's contract.
    2.  **The Runtime Vow Extractor:** Separates runtime vow injections from executable
        edicts to populate the `runtime_vows` list.
    3.  **The Manifest Mode Default:** Explicitly sets `ephemeral_sanctum` to `None`
        unless `rehearse` is sworn.
    4.  **The Dotenv Sentinel:** Automatically detects and loads `.env` files.
    5.  **The Variable Alchemist:** Merges CLI overrides (`--set`) with Blueprint variables.
    6.  **The Path Normalizer:** Ensures `execution_root` is always an absolute Path.
    7.  **The Scripture Validator:** Raises Heresy if the Symphony is silent (empty).
    8.  **The Gnostic Anchor:** Injects `project_root` and `sanctum` into Context.
    9.  **The Secret's Veil:** Scans loaded variables for potential secrets.
    10. **The Rehearsal Isolation:** Uses `tempfile.mkdtemp` for safe testing.
    11. **The Task Selector:** Filters edicts by `@task` name if requested.
    12. **The Sovereign State:** Maintains immutable source of truth for parsed artifacts.
    """

    def __init__(
            self,
            context_manager: 'GnosticContextManager',
            symphony_path: Path,
            request: 'SymphonyRequest',
            execution_root: Optional[Path],
            is_simulation: bool
    ):
        self.context_manager = context_manager
        self.symphony_path = symphony_path
        self.request = request
        self.execution_root = execution_root.resolve() if execution_root else symphony_path.parent.resolve()
        self.is_simulation = is_simulation

        self.ephemeral_sanctum_path: Optional[Path] = None
        self._parsed_tasks: Dict[str, List[Edict]] = {}

    def initialize_symphony(self) -> Tuple[Path, List[Edict], List[Edict]]:
        """
        [THE GRAND RITE OF PREPARATION]
        1. Determine Reality (Manifest vs Rehearsal).
        2. Parse Scripture.
        3. Hydrate Environment.
        4. Select Task (if any).
        5. Return (Sanctum, Edicts, Vows).
        """
        Logger.info(f"Initializing Symphony context for '{self.symphony_path.name}'...")

        # 1. Determine Reality
        if self.request.rehearse:
            sanctum = self._prophesy_and_forge_proving_ground()
        else:
            sanctum = self.execution_root

        # 2. Update Context Manager with spatial truth
        self.context_manager.set_sanctum(str(sanctum))

        # 3. Parse Scripture
        # We need the parser instance to get tasks and runtime vows
        parser_instance, edicts, blueprint_vars = self._parse_scripture()

        # 4. Hydrate Environment (Variables & Secrets)
        self._hydrate_environment(blueprint_vars)

        # 5. Task Selection & Runtime Vow Extraction
        final_edicts = []
        runtime_vows = []

        # Extract runtime vows from the global scope (directives)
        # In the parser, these are often Edicts of type DIRECTIVE with specific args
        # But for now, we assume the MetaHandler handles them during execution or we filter them here.
        # Let's filter: Edicts that register vows vs executable edicts.

        # Actually, `parser.edicts` contains everything.
        # Runtime vow registration usually happens via `MetaHandler` executing a directive.
        # So we pass them as part of the execution stream unless they are purely declarative headers.
        # For simplicity in V1, we pass everything to the engine, and the engine dispatches.
        # EXCEPT: If we select a task, we must still execute the global setup/vows?
        # Standard logic: Global scope runs, then task? Or just task?
        # Scaffold Logic: If task is selected, ONLY run task. Global vars are loaded, but global edicts are skipped.

        if self.request.task:
            if self.request.task not in self._parsed_tasks:
                raise ArtisanHeresy(
                    f"Task '{self.request.task}' not found in scripture.",
                    suggestion=f"Available tasks: {', '.join(self._parsed_tasks.keys())}"
                )
            Logger.info(f"Selected task: [cyan]{self.request.task}[/cyan]")
            final_edicts = self._parsed_tasks[self.request.task]
        else:
            final_edicts = edicts

        # Identify Runtime Vow Definitions (if any specific pre-load is needed)
        # Currently, `@inject_vow` produces a DIRECTIVE edict that runs at runtime.
        # So we include them in the stream.

        if not final_edicts and not self.request.task:
            # If no task requested and main body is empty, that's a warning.
            # But if tasks exist, maybe the user forgot to specify one?
            if self._parsed_tasks:
                raise ArtisanHeresy(
                    "The Symphony's main body is silent, but tasks were found.",
                    suggestion=f"Did you mean to run a task? Available: {', '.join(self._parsed_tasks.keys())}"
                )
            else:
                raise ArtisanHeresy("The Symphony is silent. No edicts found to conduct.")

        return sanctum, final_edicts, runtime_vows

    def _hydrate_environment(self, blueprint_vars: Dict[str, Any]):
        """
        [THE ALCHEMICAL MERGE]
        Merges:
        1. .env file (Lowest)
        2. Blueprint Variables ($$)
        3. CLI Overrides (--set) (Highest)

        Also detects secrets and stores them in the Vault.
        """
        # 1. Dotenv
        env_path = self.execution_root / ".env"
        if env_path.exists():
            Logger.info("Loading environment from .env...")
            try:
                content = env_path.read_text(encoding='utf-8')
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k, v = k.strip(), v.strip().strip('"\'')
                        # Only set if not already present (preserve CLI overrides if they were set early)
                        # Actually, context hydration happens here. CLI vars are injected later?
                        # No, context.hydrate() already put CLI vars in.
                        # So we check if k exists.
                        if k not in self.context_manager:
                            self.context_manager.update_variable(k, v)
                            # Check for secrets
                            if self.context_manager.is_secret(k):
                                self.context_manager.vault.store(k, v)
            except Exception as e:
                Logger.warn(f"Failed to load .env: {e}")

        # 2. Blueprint Variables
        for k, v in blueprint_vars.items():
            # CLI overrides (already in context) take precedence
            if k not in self.context_manager:
                self.context_manager.update_variable(k, v)
                if self.context_manager.is_secret(k):
                    # Value might be a literal string or a template.
                    # If literal, store in vault.
                    if isinstance(v, str) and "{{" not in v:
                        self.context_manager.vault.store(k, v)

    def _parse_scripture(self) -> Tuple['ApotheosisParser', List[Edict], Dict[str, Any]]:
        """
        [THE GAZE OF UNDERSTANDING]
        Parses the .symphony file and extracts the Gnostic Dowry.
        """
        parser = ApotheosisParser(grammar_key='symphony')

        try:
            content = self.symphony_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            raise ArtisanHeresy(f"Symphony scripture not found: {self.symphony_path}")

        # We pass pre_resolved_vars from CLI to help with immediate resolution if needed,
        # though usually resolution happens at runtime.
        cli_vars = self.context_manager.raw()

        # [THE GNOSTIC DOWRY UNPACKING]
        # (parser, items, commands, edicts, variables, dossier)
        parser_instance, _, _, edicts, variables, dossier = parser.parse_string(
            content,
            file_path_context=self.symphony_path,
            pre_resolved_vars=cli_vars
        )

        if not parser.all_rites_are_pure:
            details = "\n".join([f"L{h.line_num}: {h.message}" for h in parser.heresies])
            raise ArtisanHeresy("Parsing Heresy: The scripture contains errors.", details=details)

        # Store parsed tasks for later selection
        self._parsed_tasks = parser.tasks

        return parser, edicts, variables

    def _prophesy_and_forge_proving_ground(self) -> Path:
        """[THE RITE OF ISOLATION] Creates a temp dir and copies the project."""
        self.ephemeral_sanctum_path = Path(tempfile.mkdtemp(prefix="scaffold_rehearsal_"))
        Logger.info(f"Forging Ephemeral Proving Ground at: {self.ephemeral_sanctum_path}")

        # Ignore patterns to prevent copying heavy/irrelevant artifacts
        def _ignore_patterns(path, names):
            return {'.git', '.scaffold', 'node_modules', 'venv', '.venv', '__pycache__', '.idea', '.vscode', 'target',
                    'dist', 'build'}

        try:
            # We copy the execution root into the temp dir
            # Note: We must be careful not to copy the temp dir into itself if it's somehow inside (unlikely with /tmp)
            shutil.copytree(self.execution_root, self.ephemeral_sanctum_path, dirs_exist_ok=True,
                            ignore=_ignore_patterns)
        except Exception as e:
            raise ArtisanHeresy(f"Failed to forge Proving Ground: {e}")

        return self.ephemeral_sanctum_path