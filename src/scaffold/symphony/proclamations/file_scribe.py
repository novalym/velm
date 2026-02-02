# Path: scaffold/symphony/proclamations/file_scribe.py
# ----------------------------------------------------

import ast
from pathlib import Path
from .base import ProclamationHandler
from ...utils import atomic_write


class FileProclamationHandler(ProclamationHandler):
    """The Scribe of Persistent Truth."""

    @property
    def key(self) -> str:
        return "file"

    def execute(self, gnostic_arguments: str):
        """Parses `path="...", content="..."` and writes to the sanctum."""
        try:
            # Safely parse the arguments as a Python dictionary
            args = ast.literal_eval(f"dict({gnostic_arguments})")
            path_str = args.get("path")
            content_str = args.get("content", "")

            if not path_str:
                raise ValueError("'path' argument is required.")

            # Resolve path relative to the current sanctum
            target_path = (self.regs.sanctum.root / path_str).resolve()

            # Transmute content with variables
            final_content = self.alchemist.transmute(content_str, self.regs.gnosis)

            if not self.regs.dry_run:
                atomic_write(
                    target_path,
                    final_content,
                    self.regs.logger,
                    self.regs.project_root,
                    transaction=self.regs.transaction
                )
                self.console.print(f"✒️ Inscribed Gnosis to [cyan]{path_str}[/cyan]")
            else:
                self.console.print(f"[DRY-RUN] Would inscribe Gnosis to [cyan]{path_str}[/cyan]")

        except Exception as e:
            raise ValueError(f"Failed to parse 'file' proclamation: {e}")