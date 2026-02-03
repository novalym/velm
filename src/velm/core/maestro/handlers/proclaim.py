# Path: scaffold/core/maestro/handlers/proclaim.py
# ------------------------------------------------

from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation


class ProclaimHandler(BaseRiteHandler):
    """
    [FACULTY 10] The Universal Voice.
    Handles the `proclaim` rite by speaking directly to the console, bypassing the shell.
    """
    def conduct(self, command: str):
        msg = ""
        # 1. Parse the message payload
        if command.startswith("%% proclaim:"):
            msg = command[12:].strip()
        elif command.startswith("proclaim:"):
            msg = command[9:].strip()
        elif command.startswith("echo "):
            msg = command[5:].strip()

        # 2. Strip outer quotes if they exist and are balanced
        if len(msg) >= 2 and msg[0] == msg[-1] and msg[0] in ('"', "'"):
            msg = msg[1:-1]

        # 3. Chronicle the Event
        ActiveLedger.record(LedgerEntry(
            actor="Maestro",
            operation=LedgerOperation.EXEC_SHELL, # Logged as a shell-like op
            reversible=False, # Proclamations are ephemeral
            forward_state={"command": f"proclaim: {msg}"}
        ))

        # 4. Proclaim with Rich Markup
        if not self.regs.dry_run:
            self.console.print(f"[bold cyan]»[/bold cyan] {msg}")

        self.logger.info(f"Proclaimed: {msg}")