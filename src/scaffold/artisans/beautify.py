import difflib
import difflib
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any

from rich.box import ROUNDED
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.alchemist import get_alchemist
from ..core.artisan import BaseArtisan
from ..core.blueprint_scribe import BlueprintScribe
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import BeautifyRequest
from ..logger import Scribe
from ..parser_core.parser import parse_structure
from ..utils import atomic_write, hash_file, gnostic_glob, get_ignore_spec

Logger = Scribe("BeautifyArtisan")
@register_artisan("beautify")
class BeautifyArtisan(BaseArtisan[BeautifyRequest]):
    """
    =================================================================================
    == THE GRAND PURIFIER (V-Ω-LEGENDARY-ULTIMA) ==
    =================================================================================
    LIF: 10,000,000,000
    The **Beautify Artisan** is the Guardian of Aesthetic Purity. It parses `.scaffold`
    blueprints and re-inscribes them in their canonical, luminous form.

    ### THE PANTHEON OF 12 ELEVATIONS:
    1.  **The Recursive Gaze:** Can purify a single file or an entire sanctum (directory).
    2.  **The Parallel Purification:** Uses `ThreadPoolExecutor` to cleanse multiple scriptures simultaneously.
    3.  **The Idempotent Hand:** Calculates hashes before writing; if the soul is already pure, it stays its hand.
    4.  **The Dry-Run Prophecy:** In simulation mode, it renders a syntax-highlighted diff of the proposed changes.
    5.  **The Gnostic Inquisitor:** Validates the syntax of every blueprint before attempting to beautify it.
    6.  **The Atomic Inscription:** Writes to a temporary vessel first, ensuring no scripture is ever corrupted.
    7.  **The Ignore Sentinel:** Respects `.gitignore` and custom ignore patterns to avoid profaning vendor files.
    8.  **The Luminous Dossier:** Proclaims a rich table of results (Pure, Transfigured, Profane, Heretical).
    9.  **The Interactive Altar:** Can launch the `ScaffoldPad` TUI for real-time, interactive beautification.
    10. **The Check Mode:** Can run in CI/CD to fail the build if any scripture is profane (unformatted).
    11. **The Alchemical Awareness:** Understands and preserves Jinja2 constructs and Gnostic Directives during formatting.
    12. **The Backup Rite:** (Implicit via Atomic Write) Ensures safety during the transfiguration.
    =================================================================================
    """

    def execute(self, request: BeautifyRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE RITE OF PURIFICATION (V-Ω-GUARDED-SYMPHONY)                             ==
        =================================================================================
        Conducts the mass purification of blueprints. It is a parallelized, atomic,
        and now **Guarded** operation.
        """
        self.request = request
        self.alchemist = get_alchemist()

        # 1. The Rite of the Pad (Interactive Mode)
        if request.pad:
            return self._launch_pad()

        # 2. Consecrate the Sanctum
        self.target_path = Path(request.blueprint_path).resolve() if request.blueprint_path else Path.cwd()
        self.logger.info(f"The Grand Purifier gazes upon: [cyan]{self.target_path}[/cyan]")

        # 3. The Gaze of Scope
        scriptures_to_purify = self._gather_scriptures()
        if not scriptures_to_purify:
            return self.success("The Gaze found only a void. No scriptures to purify.")

        # [ELEVATION 13] THE GUARDIAN'S OFFER
        # We offer to enshrine the current state before purification.
        # We skip this if we are merely checking (observing), as no changes will occur.
        if not request.check:
             self.guarded_execution(scriptures_to_purify, request, context="beautify")

        # 4. The Symphony of Purification
        results = []
        heretical_files = []

        self.console.rule("[bold magenta]The Grand Purifier Awakens[/bold magenta]")

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=self.console
        ) as progress:
            task = progress.add_task(f"[yellow]Purifying {len(scriptures_to_purify)} scripture(s)...[/yellow]",
                                     total=len(scriptures_to_purify))

            with ThreadPoolExecutor() as executor:
                future_to_path = {executor.submit(self._purify_single_scripture, path): path for path in
                                  scriptures_to_purify}
                for future in as_completed(future_to_path):
                    result = future.result()
                    if result['status'] == 'heretical':
                        heretical_files.append(result)
                    else:
                        results.append(result)
                    progress.update(task, advance=1)

        # 5. The Adjudication of Heresy
        if heretical_files and not request.check and not request.dry_run and not request.force:
            self._handle_heresies(heretical_files)

        # 6. The Luminous Dossier
        self._proclaim_results(results, heretical_files)

        # 7. The Final Verdict
        if request.check:
            profane_count = sum(1 for r in results if r['status'] == 'profane')
            if profane_count > 0 or heretical_files:
                return self.failure(
                    f"Gnostic Adjudication failed. {profane_count} profane, {len(heretical_files)} heretical scripture(s) detected.")

        if heretical_files:
            return self.partial_success("Purification complete, but heresies were found.", heresies=[])

        return self.success(f"The Rite of Beautification is complete. {len(results)} scriptures are pure.")

    def _launch_pad(self) -> ScaffoldResult:
        """Summons the ScaffoldPad TUI."""
        # Lazy import to avoid TUI dependencies in CLI-only mode
        from ..artisans.pad import PadArtisan
        from ..interfaces.requests import PadRequest

        # Delegate to PadArtisan
        pad_req = PadRequest(
            pad_name='beautify',
            initial_path=str(self.request.blueprint_path) if self.request.blueprint_path else None
        )
        return PadArtisan(self.engine).execute(pad_req)

    def _gather_scriptures(self) -> List[Path]:
        """Identifies all valid targets."""
        if self.target_path.is_file():
            return [self.target_path]

        ignore_spec = get_ignore_spec(self.project_root, self.request.ignore)
        all_files = gnostic_glob(self.target_path, '**/*.scaffold')

        if ignore_spec:
            return [f for f in all_files if not ignore_spec.match_file(str(f.relative_to(self.project_root)))]
        return all_files

    def _purify_single_scripture(self, scripture_path: Path) -> Dict[str, Any]:
        """The Atomic Rite of Purification for one file."""
        try:
            original_content = scripture_path.read_text(encoding='utf-8')
            original_hash = hash_file(scripture_path)

            # 1. Parse
            # We use a dummy namespace to satisfy the parser's legacy signature if needed,
            # or rely on the parser accepting None.
            parser_instance, items, commands, edicts, blueprint_vars, dossier = parse_structure(scripture_path)

            if parser_instance is None:
                return {"path": scripture_path, "status": "heretical", "error": "Parser returned Void."}

            # 2. Transcribe (Beautify)
            scribe = BlueprintScribe(project_root=self.project_root, alchemist=self.alchemist)
            beautified_content = scribe.transcribe(
                items=items,
                commands=commands,
                gnosis=parser_instance.variables,
                rite_type='distillation'
            )
            beautified_hash = hashlib.sha256(beautified_content.encode('utf-8')).hexdigest()

            # 3. Compare
            if original_hash == beautified_hash:
                return {"path": scripture_path, "status": "pure", "original_hash": original_hash}

            # 4. Diff (for Dry Run)
            diff = ""
            if self.request.check or self.request.dry_run:
                diff = "".join(difflib.unified_diff(
                    original_content.splitlines(keepends=True),
                    beautified_content.splitlines(keepends=True),
                    fromfile=f"a/{scripture_path.name}",
                    tofile=f"b/{scripture_path.name}"
                ))
                return {"path": scripture_path, "status": "profane", "diff": diff}

            # 5. Write
            write_result = atomic_write(
                target_path=scripture_path,
                content=beautified_content,
                logger=Logger,
                sanctum=scripture_path.parent,
                verbose=False  # Keep individual file logs quiet in batch mode
            )

            if not write_result.success:
                raise IOError("Atomic Write Failed")

            return {"path": scripture_path, "status": "transfigured", "original_hash": original_hash,
                    "new_hash": beautified_hash}

        except Exception as e:
            return {"path": scripture_path, "status": "heretical", "error": str(e)}

    def _handle_heresies(self, heretical_files: List[Dict]):
        """Interactive adjudication of parsing errors."""
        Logger.error(f"The Gaze was shattered by {len(heretical_files)} heretical scripture(s).")
        if Confirm.ask("[bold question]Abort the symphony?[/bold question]", default=True):
            raise ArtisanHeresy(f"Rite stayed due to {len(heretical_files)} heresies.")

    def _proclaim_results(self, results: List[Dict], heresies: List[Dict]):
        """Renders the Luminous Dossier."""
        all_results = sorted(results + heresies, key=lambda x: str(x['path']))
        table = Table(title="[bold]Grand Dossier of Gnostic Purification[/bold]", box=ROUNDED)
        table.add_column("Scripture", style="cyan")
        table.add_column("Status", style="white", justify="center")
        table.add_column("Details", style="dim")

        for res in all_results:
            status = res['status'].upper()
            style = "green" if status == "PURE" else "bold yellow" if status == "TRANSFIGURED" else "yellow" if status == "PROFANE" else "bold red"

            details = ""
            if status == "PURE":
                details = f"Hash: {res['original_hash'][:8]}"
            elif status == "TRANSFIGURED":
                details = f"{res['original_hash'][:8]} -> {res['new_hash'][:8]}"
            elif status == "PROFANE":
                details = "Needs purification."
                if self.request.dry_run:
                    self.console.print(
                        Panel(Syntax(res['diff'], "diff", theme="monokai"), title=f"Prophecy for {res['path'].name}"))
            elif status == "HERETICAL":
                details = f"Paradox: {res['error']}"

            try:
                rel_path = res['path'].relative_to(self.project_root)
            except ValueError:
                rel_path = res['path'].name

            table.add_row(str(rel_path), f"[{style}]{status}[/{style}]", details)

        self.console.print(table)


