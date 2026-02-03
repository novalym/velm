# Path: scaffold/core/maestro/handlers/tunnel.py
# ----------------------------------------------

from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation
from ....core.net.tunnel import TunnelWeaver
from ....core.system.manager import System


class TunnelHandler(BaseRiteHandler):
    """
    The artisan for forging and managing secure SSH tunnels.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tunnel_weaver = TunnelWeaver()
        System.register_shutdown_hook(self.tunnel_weaver.close_all)

    def conduct(self, command: str):
        spec = command.replace("tunnel:", "", 1).strip()

        ActiveLedger.record(LedgerEntry(
            actor="Maestro", operation=LedgerOperation.EXEC_SHELL, reversible=False,
            forward_state={"command": f"tunnel: {spec}"}, inverse_action=None
        ))

        if self.regs.dry_run:
            self.logger.info(f"[DRY-RUN] TUNNEL: {spec}")
            return

        self.tunnel_weaver.weave(spec)