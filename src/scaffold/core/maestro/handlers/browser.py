# Path: scaffold/core/maestro/handlers/browser.py
# -----------------------------------------------

import webbrowser
import platform
from typing import Optional
from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation


class BrowserHandler(BaseRiteHandler):
    """
    =============================================================================
    == THE CELESTIAL NAVIGATOR (V-Ω-URL-OPENER)                                ==
    =============================================================================
    Handles the `@open_browser` directive.
    It acts as a "Fire-and-Forget" artisan, summoning the user's browser without
    blocking the Symphony.
    """

    def conduct(self, command: str):
        # command format: "@open_browser http://localhost:3000"
        url = command.replace("@open_browser", "", 1).strip()

        # Strip quotes if present
        if (url.startswith('"') and url.endswith('"')) or (url.startswith("'") and url.endswith("'")):
            url = url[1:-1]

        if not url:
            self.logger.warn("Browser Handler received a void URL.")
            return

        self.logger.info(f"Summoning the Celestial Navigator for: [cyan]{url}[/cyan]")

        # 1. Chronicle the Event (Non-reversible)
        ActiveLedger.record(LedgerEntry(
            actor="Maestro",
            operation=LedgerOperation.EXEC_SHELL,
            reversible=False,
            forward_state={"command": f"open_browser: {url}"}
        ))

        # 2. The Rite of Opening
        if not self.regs.dry_run:
            try:
                # We assume the standard library knows the way.
                # On WSL, this might need specific handling (e.g. wslview),
                # but Python 3.7+ handles WSL reasonably well.
                webbrowser.open(url)
                self.console.print(f"[bold green]>>[/bold green] Opened browser at {url}")
            except Exception as e:
                self.logger.error(f"Failed to open browser: {e}")