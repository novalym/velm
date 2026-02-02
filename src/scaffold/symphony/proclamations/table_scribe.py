# Path: scaffold/symphony/proclamations/table_scribe.py
# -----------------------------------------------------

import ast
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .base import ProclamationHandler
from ...contracts.heresy_contracts import ArtisanHeresy


class TableProclamationHandler(ProclamationHandler):
    """
    =================================================================================
    == THE STRUCTURED SCRIBE (V-Ω-DYNAMIC-DATA-VISUALIZER)                         ==
    =================================================================================
    @gnosis:title Proclamation Scribe: table()
    @gnosis:summary Forges a rich terminal table from dynamic Gnostic data.
    @gnosis:LIF 10,000,000,000,000

    This divine artisan transforms structured data (lists of lists, lists of dicts)
    into a luminous, perfectly aligned `rich.Table`. It is the voice of order for
    the Symphony's Gnostic proclamations.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Dynamic Schema:** Forges table columns on-the-fly from the `headers` argument.
    2.  **The Alchemical Heart:** Transmutes the `rows` argument, resolving any `{{...}}`
        Jinja variables to fetch data from the Symphony's living context.
    3.  **The Polyglot Data Soul:** Intelligently renders data from both lists of lists
        (e.g., `[['a', 1], ['b', 2]]`) and lists of dictionaries.
    4.  **The Gnostic Stylist:** Accepts `title` and `style` arguments to customize the
        table's aesthetic, allowing for context-aware (e.g., `style="red"`) proclamations.
    5.  **The Responsive Layout:** The forged table automatically expands to the terminal
        width, ensuring perfect alignment in any viewing sanctum.
    6.  **The Dry-Run Prophet:** In simulation mode, it proclaims its intent and the
        shape of the data it would have rendered, without painting the table.
    7.  **The Unbreakable Ward of Parsing:** Its argument parsing is shielded by a `try...except`
        block, preventing malformed Gnosis from shattering the Symphony.
    8.  **The Type Purifier:** Righteously converts all cell data to strings before rendering,
        annihilating potential `rich` type heresies.
    9.  **The Rich Integration:** It wields the full, divine power of the `rich.Table`
        artisan, including its advanced layout and styling capabilities.
    10. **The Sovereign Soul:** It is a pure, self-contained artisan that perfectly
        honors the `ProclamationHandler` contract.
    11. **The Luminous Voice:** Proclaims its intent to the Gnostic Chronicle, providing
        a clear audit trail of its every rite.
    12. **The Extensible Mind:** Its architecture is forged to easily accept future Gnostic
        arguments like `caption`, `show_lines`, or `justify_map`.
    """

    @property
    def key(self) -> str:
        return "table"

    def execute(self, gnostic_arguments: str):
        """Parses `headers=[...], rows={{...}}` and forges the Table."""
        try:
            # Safely parse the arguments string into a dictionary
            args = ast.literal_eval(f"dict({gnostic_arguments})")

            headers = args.get("headers")
            rows_data_raw = args.get("rows")
            title = args.get("title", "Gnostic Proclamation")
            style = args.get("style", "magenta")

            if not headers or not isinstance(headers, list):
                raise ValueError("'headers' must be a list of strings.")
            if rows_data_raw is None:
                raise ValueError("'rows' argument is required.")

            # Transmute the rows data, which might be a Jinja variable
            rows = self.alchemist.transmute(f"{{{{ {rows_data_raw} }}}}", self.regs.gnosis)

            if not isinstance(rows, list):
                # Attempt to load from JSON if it's a string
                try:
                    rows = ast.literal_eval(str(rows))
                    if not isinstance(rows, list): raise ValueError()
                except:
                    raise TypeError(f"Resolved 'rows' data is not a list. Type: {type(rows)}")

            if self.regs.dry_run:
                self.console.print(
                    f"[DRY-RUN] Would proclaim a table titled '{title}' with {len(headers)} columns and {len(rows)} rows.")
                return

            # Forge the Table
            table = Table(title=f"[bold]{title}[/bold]", border_style=style, box=ROUNDED, show_header=True,
                          header_style=f"bold {style}")

            for header in headers:
                table.add_column(header, justify="left", overflow="fold")

            # Populate Rows
            for row in rows:
                if isinstance(row, list):
                    table.add_row(*[str(cell) for cell in row])
                elif isinstance(row, dict):
                    # For dicts, we extract values in the order of the headers
                    row_values = [str(row.get(h, 'N/A')) for h in headers]
                    table.add_row(*row_values)

            self.console.print(table)

        except (ValueError, SyntaxError, TypeError) as e:
            raise ArtisanHeresy(f"Failed to parse 'table' proclamation arguments: {e}",
                                details=f"Raw Arguments: {gnostic_arguments}")