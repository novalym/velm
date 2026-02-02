# Path: scaffold/core/maestro/handlers/raw.py
# -------------------------------------------

import subprocess
from .base import BaseRiteHandler
from ..reverser import MaestroReverser
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....contracts.heresy_contracts import ArtisanHeresy


class RawHandler(BaseRiteHandler):
    """
    The artisan for conducting raw, interactive rites. It opens a direct,
    unmanaged conduit to the shell.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverser = MaestroReverser()

    def conduct(self, command: str):
        clean_command = command.replace("raw:", "", 1).strip()
        self.logger.info(f"Opening raw conduit for interactive rite: [yellow]$ {clean_command}[/yellow]")

        undo_commands = self.context.explicit_undo or self.reverser.infer_undo(clean_command, self.context.cwd)
        ActiveLedger.record(LedgerEntry(
            actor="Maestro", operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(op=LedgerOperation.EXEC_SHELL,
                                     params={"commands": undo_commands, "cwd": str(self.context.cwd)}) if undo_commands else None,
            forward_state={"command": clean_command, "cwd": str(self.context.cwd)}
        ))

        if self.regs.dry_run:
            self.logger.info(f"[DRY-RUN] RAW: {clean_command}")
            return

        try:
            subprocess.run(clean_command, shell=True, cwd=self.context.cwd, env=self.context.env, check=True)
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"Raw rite failed with exit code {e.returncode}", child_heresy=e)