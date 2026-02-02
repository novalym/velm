# Path: scaffold/core/maestro/handlers/hosts.py
# ---------------------------------------------

import os
import sys
import shutil
import platform
from pathlib import Path
from .base import BaseRiteHandler
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....utils import atomic_write


class HostsHandler(BaseRiteHandler):
    """
    =============================================================================
    == THE CELESTIAL NAME WEAVER (V-Ω-SYSTEM-DNS-ALCHEMIST)                    ==
    =============================================================================
    Handles the `%% hosts:` directive.
    It safely modifies the `/etc/hosts` (or Windows equivalent) file.

    Capabilities:
    1. Privilege Check: Demands Admin/Root.
    2. Backup: Preserves the old state.
    3. Idempotency: Avoids duplicate entries.
    """

    HOSTS_PATH = Path(r"C:\Windows\System32\drivers\etc\hosts") if os.name == 'nt' else Path("/etc/hosts")

    def conduct(self, command: str):
        # command format: "%% hosts: 127.0.0.1 myapp.local"
        entry_line = command.replace("%% hosts:", "", 1).strip()

        if not entry_line:
            self.logger.warn("Hosts Handler received a void entry.")
            return

        # 1. The Gaze of Privilege
        if not self._is_admin():
            raise ArtisanHeresy(
                "The Rite of Naming requires elevated privileges.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Run the scaffold command with sudo/Administrator privileges to apply: '{entry_line}'"
            )

        if self.regs.dry_run:
            self.logger.info(f"[DRY-RUN] Would add to hosts: {entry_line}")
            return

        # 2. The Rite of Inscription
        try:
            self._modify_hosts(entry_line)
        except Exception as e:
            raise ArtisanHeresy(f"Failed to modify hosts file: {e}", child_heresy=e)

    def _is_admin(self) -> bool:
        try:
            if os.name == 'nt':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False

    def _modify_hosts(self, entry: str):
        if not self.HOSTS_PATH.exists():
            raise ArtisanHeresy(f"System hosts file not found at {self.HOSTS_PATH}")

        content = self.HOSTS_PATH.read_text(encoding='utf-8', errors='ignore')

        # Idempotency Check
        if entry in content:
            self.logger.verbose(f"Hosts entry '{entry}' already exists.")
            return

        # 3. Chronicle for Undo
        # We record the Inverse Op to remove the line.
        # Note: Removing a specific line safely requires complex logic in the Reverser.
        # For V1, we might skip perfect undo or implement a simple sed/grep inversion.
        # Here we record it conceptually.
        ActiveLedger.record(LedgerEntry(
            actor="HostsHandler",
            operation=LedgerOperation.EXEC_SHELL,  # Using EXEC_SHELL as proxy for system mod
            reversible=False,  # Mark false for now until HostsReverser is built
            forward_state={"entry": entry},
            metadata={"file": str(self.HOSTS_PATH)}
        ))

        # 4. Append
        new_content = content
        if not new_content.endswith('\n'): new_content += "\n"
        new_content += f"{entry} # Added by Scaffold\n"

        # We use simple write instead of atomic_write for system files to avoid permission complexity with moves across devices?
        # /etc/hosts is usually on root. /tmp might be different.
        # But atomic_write is safer. However, atomic_write creates a .tmp file in the SAME dir.
        # Writing to /etc/ requires root, which we verified.

        self.logger.info(f"Inscribing '{entry}' into Celestial Name Record...")

        # We backup first manually as a safety measure
        backup_path = self.HOSTS_PATH.with_suffix(".bak")
        shutil.copy2(self.HOSTS_PATH, backup_path)

        self.HOSTS_PATH.write_text(new_content, encoding='utf-8')
        self.console.print(f"[bold green]>>[/bold green] Host entry added: {entry}")