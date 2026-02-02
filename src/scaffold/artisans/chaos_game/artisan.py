# Path: scaffold/artisans/chaos_game/artisan.py
# ---------------------------------------------

import time
import random
import threading
from pathlib import Path

from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ChaosGameRequest
from ...help_registry import register_artisan
from ...core.sanctum.local import LocalSanctum
from ...core.kernel.transaction import GnosticTransaction
from ...utils.invocation import invoke_scaffold_command


@register_artisan("game")
class ChaosGameArtisan(BaseArtisan[ChaosGameRequest]):
    """
    =============================================================================
    == THE CHAOS GAME (V-Ω-GAMIFIED-RESILIENCE)                                ==
    =============================================================================
    LIF: 10,000,000,000

    A daemon that tests your faith.
    Every N minutes, it performs a 'Chaos Event':
    1. Deletes a random source file.
    2. Runs the test suite.
    3. If tests FAIL -> +10 Points (Good! Tests caught it).
    4. If tests PASS -> -50 Points (Bad! Dead/Uncovered code).
    5. Restores the file (via Git or Undo).
    """

    def execute(self, request: ChaosGameRequest) -> ScaffoldResult:
        self.score = 0
        self.round = 0
        self.logger.info(f"Welcome to the Chaos Game. Interval: {request.interval}s")

        try:
            while True:
                self._game_loop()
                time.sleep(request.interval)
        except KeyboardInterrupt:
            pass

        return self.success(f"Game Over. Final Score: {self.score}")

    def _game_loop(self):
        self.round += 1

        # 1. Select a Victim
        src_files = list(self.project_root.glob("src/**/*.py"))  # Prophecy: Polyglot support
        if not src_files: return

        victim = random.choice(src_files)
        rel_victim = victim.relative_to(self.project_root)

        self.console.print(Panel(
            f"Round {self.round}: The Shadow falls upon [cyan]{rel_victim}[/cyan]...",
            title="[bold red]Chaos Event[/bold red]"
        ))

        # 2. The Strike (Delete File)
        # We use a Transaction to ensure we can rollback
        with GnosticTransaction(self.project_root, f"Chaos Round {self.round}") as tx:
            # Physically delete
            victim.unlink()

            # 3. The Adjudication (Run Tests)
            self.console.print("[yellow]Running Tests to verify impact...[/yellow]")
            # We assume 'pytest' for V1
            result = invoke_scaffold_command(["run", "pytest"], cwd=self.project_root, silent=True)

            if result.exit_code != 0:
                self.console.print("[bold green]✔ Tests Failed![/bold green] The system perceived the wound.")
                self.score += 10
            else:
                self.console.print("[bold red]✘ Tests Passed![/bold red] The code was redundant or untested.")
                self.score -= 50

            # 4. The Resurrection (Implicit Rollback via Context Manager exit)
            # We force rollback by raising an exception caught by the TX context?
            # Or we rely on the Reverser.
            # Ideally, GnosticTransaction auto-commits on success. We want to ROLLBACK always.
            # So we manually trigger rollback.
            tx.chronomancer.perform_emergency_rollback()

        self.console.print(f"Current Score: [bold magenta]{self.score}[/bold magenta]")