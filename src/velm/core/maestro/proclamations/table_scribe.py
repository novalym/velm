# Path: src/velm/core/maestro/proclamations/table_scribe.py
# --------------------------------------------------------

from rich.table import Table
from .base import ProclamationScribe


class TableScribe(ProclamationScribe):
    """Transmutes lists of Gnosis into structured terminal grids."""

    def proclaim(self, payload: str, metadata: dict):
        headers = metadata.get("headers", "Key,Value").split(",")
        # We scry the variables for the data source
        rows_source = metadata.get("rows")
        data = self.engine.context.variables.get(rows_source, [])

        table = Table(title=metadata.get("title", "Data Manifest"), border_style="dim")
        for h in headers:
            table.add_column(h.strip(), style="cyan")

        for row in data:
            if isinstance(row, (list, tuple)):
                table.add_row(*[str(i) for i in row])
            elif isinstance(row, dict):
                table.add_row(*[str(row.get(h.strip().lower(), "")) for h in headers])

        self.console.print(table)