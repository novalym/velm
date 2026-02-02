# Path: artisans/surveyor/artisan.py
# ----------------------------------

import time
import os
from pathlib import Path
from typing import Optional, Any, Dict

# Core Uplinks
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import GrandSurveyRequest
from ...help_registry import register_artisan

# Logic Uplinks (The Brains)
from ...core.daemon.surveyor.engine import GrandSurveyor
from ...core.daemon.akashic import AkashicRecord

# UI Uplinks
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn


@register_artisan("survey")
class GrandSurveyArtisan(BaseArtisan[GrandSurveyRequest]):
    """
    =============================================================================
    == THE EYE OF THE ARGUS (V-Ω-SURVEYOR-INDEXER)                             ==
    =============================================================================
    LIF: 10,000,000 | ROLE: DISCOVERY_PRIME

    Orchestrates the indexing of the project structure.
    Now automatically triggers the [IndexerArtisan] upon completion to feed
    the Gnostic Cortex with deep symbol knowledge.
    """

    def __init__(self, context_provider: Any):
        """
        [THE UNIVERSAL CONSTRUCTOR]
        Accepts either a Nexus (Daemon mode) or an Engine (CLI mode).
        Determines identity via Duck Typing to prevent 'AttributeError'.
        """
        self.nexus = None
        self.engine = None

        # [ASCENSION 1]: POLYMORPHIC IDENTITY RESOLUTION
        if hasattr(context_provider, 'dispatcher') and hasattr(context_provider, 'ignite'):
            # We are in the Daemon
            self.nexus = context_provider
            self.engine = context_provider.engine
        elif hasattr(context_provider, 'dispatch'):
            # We are in the CLI
            self.engine = context_provider
            self.nexus = None
        else:
            # Fallback / Mock
            self.engine = context_provider

        super().__init__(self.engine)

    def execute(self, request: GrandSurveyRequest) -> ScaffoldResult:
        """
        [THE RITE OF SURVEY]
        Dispatches the survey task to the appropriate execution context.
        """
        start_time = time.perf_counter()

        # 1. Resolve Target URI
        target_uri = request.rootUri
        if not target_uri:
            # Fallback to project root or CWD
            root = request.project_root or self.get_active_root()
            if root:
                # [ASCENSION 3]: URI CANONIZATION
                path_str = str(root.resolve()).replace('\\', '/')
                if not path_str.startswith('/'):
                    path_str = '/' + path_str
                target_uri = f"file://{path_str}"
            else:
                return self.failure("No Anchor. Provide --root or open a workspace.")

        # --- PATH A: DAEMONIC DISPATCH (ASYNC RPC) ---
        if self.nexus:
            self.nexus.logger.info(f"Grand Surveyor triggered (RPC) for: {target_uri}")

            # [ASCENSION 2]: RESILIENT DISPATCH LOGIC
            pool = None
            if hasattr(self.nexus.dispatcher, 'artisan_pool'):
                pool = self.nexus.dispatcher.artisan_pool
            elif hasattr(self.nexus.dispatcher, 'pools') and hasattr(self.nexus.dispatcher.pools, 'foundry'):
                pool = self.nexus.dispatcher.pools.foundry

            if pool:
                try:
                    pool.submit(self.nexus.surveyor.conduct_survey, target_uri)

                    # [ASCENSION 13]: TRIGGER AUTO-INDEXING (DAEMON)
                    self._trigger_indexing()

                    return self.success(
                        "Survey Initiated in Background.",
                        data={"status": "ASYNC_STARTED", "target": target_uri}
                    )
                except Exception as e:
                    self.nexus.logger.error(f"Pool Submission Fracture: {e}")
                    # Fallthrough to inline execution
            else:
                self.nexus.logger.warn("Thread Pool Unreachable. Falling back to Inline Execution.")

            return self._run_inline_logic(target_uri)

        # --- PATH B: CLI STANDALONE (SYNC VISUAL) ---
        else:
            return self._run_standalone_cli(target_uri)

    def _run_inline_logic(self, target_uri: str) -> ScaffoldResult:
        """
        Executes the logic synchronously (Fail-safe for Daemon).
        """
        try:
            surveyor = self.nexus.surveyor if self.nexus else GrandSurveyor(AkashicRecord())
            report = surveyor.conduct_survey(target_uri)

            # [ASCENSION 13]: TRIGGER AUTO-INDEXING (INLINE)
            self._trigger_indexing()

            return self.success("Survey Complete (Inline)", data=report)
        except Exception as e:
            return self.failure(f"Inline Survey Fracture: {e}")

    def _run_standalone_cli(self, target_uri: str) -> ScaffoldResult:
        """
        Executes the survey in the terminal with Rich visuals.
        """
        self.console.print(Panel(f"[bold cyan]Commencing Grand Survey[/bold cyan]\nTarget: [dim]{target_uri}[/dim]",
                                 border_style="cyan"))

        akashic = AkashicRecord()
        surveyor = GrandSurveyor(akashic)

        # [ASCENSION 4]: PROGRESS PROJECTION
        with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                transient=True
        ) as progress:
            task_id = progress.add_task("Initializing...", total=None)

            def cli_feedback_hook(packet):
                if packet.get('method') == 'scaffold/progress':
                    p = packet['params']
                    progress.update(task_id, completed=p.get('percentage', 0),
                                    description=p.get('message', 'Scanning...'))

            original_broadcast = akashic.broadcast
            akashic.broadcast = cli_feedback_hook

            start = time.perf_counter()
            try:
                report = surveyor.conduct_survey(target_uri)
            except Exception as e:
                return self.failure(f"Surveyor Crashed: {e}")
            finally:
                akashic.broadcast = original_broadcast

            duration = (time.perf_counter() - start) * 1000

        if report.get('success'):
            stats = report.get('stats', {})
            grid = Table.grid(expand=True, padding=(0, 2))
            grid.add_column(style="green", justify="right")
            grid.add_column(style="bold white")

            grid.add_row("Scanned:", str(stats.get('scanned', 0)))
            grid.add_row("Cached:", str(stats.get('cached', 0)))
            grid.add_row("Heresies:", f"[red]{stats.get('heresies', 0)}[/red]")
            grid.add_row("Duration:", f"{duration:.2f}ms")

            self.console.print(Panel(grid, title="[bold green]Survey Complete[/bold green]", border_style="green"))

            # [ASCENSION 13]: TRIGGER AUTO-INDEXING (CLI)
            # In CLI mode, we skip auto-indexing by default to keep 'scaffold tree' fast,
            # unless the user requested it. But for the Daemon, it's critical.
            # Here we just log the intent.
            # self._trigger_indexing()

            return self.success("Survey Complete", data=report)
        else:
            return self.failure(f"Survey Fractured: {report.get('reason')}")

    def _trigger_indexing(self):
        """
        [ASCENSION 12]: THE NEURAL TRIGGER
        Silent dispatch of the IndexerArtisan to digest the newly discovered files.
        """
        try:
            # Lazy load to avoid cycles
            from ...interfaces.requests import IndexRequest

            # Only trigger in Daemon mode where we have a thread pool
            if self.nexus:
                self.nexus.logger.info("Triggering Background Knowledge Ingestion...")
                pool = getattr(self.nexus.dispatcher, 'artisan_pool', None)
                if pool:
                    # Fire and forget
                    pool.submit(
                        self.engine.dispatch,
                        IndexRequest(project_root=self.engine.project_root)
                    )
        except Exception as e:
            # Indexing failure is non-critical to the Survey
            if self.nexus:
                self.nexus.logger.warn(f"Auto-Index trigger failed: {e}")

    def get_active_root(self):
        from pathlib import Path
        return Path.cwd()