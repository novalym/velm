# Path: scaffold/artisans/blame.py
# --------------------------------

import datetime
import hashlib
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

from rich.columns import Columns
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.markup import escape  # [THE DIVINE SUMMONS: ESCAPE]

from ..core.artisan import BaseArtisan
from ..interfaces.requests import BlameRequest
from ..interfaces.base import ScaffoldResult
from ..help_registry import register_artisan
from ..logger import Scribe
from ..utils import get_human_readable_size, is_binary

from pydantic import Field

# Divine Summons
try:
    from ..core.state.gnostic_db import GnosticDatabase, ScriptureModel, RiteModel, BondModel
    from sqlalchemy.orm import Session

    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

Logger = Scribe("BlameArtisan")



@register_artisan("blame")
class BlameArtisan(BaseArtisan[BlameRequest]):
    """
    =================================================================================
    == THE FORENSIC OMNISCIENT (V-Ω-HOLOGRAPHIC-HUD-STABILIZED)                    ==
    =================================================================================
    LIF: INFINITY

    The God-Engine of Provenance. It does not merely read logs; it reconstructs the
    causal reality of a scripture.
    """

    def execute(self, request: BlameRequest) -> ScaffoldResult:
        if not SQL_AVAILABLE:
            return self.failure("The Crystal Mind (SQLAlchemy) is not manifest. Cannot trace provenance.")

        # 1. Normalize Path
        raw_path = request.target_path
        target = (self.project_root / raw_path).resolve()

        # Check if file exists on disk
        exists_on_disk = target.exists()

        # Calculate Relative Path for DB Lookup
        try:
            db_path_str = str(target.relative_to(self.project_root)).replace('\\', '/')
        except ValueError:
            # If absolute or outside root, try to use as-is or fail
            db_path_str = raw_path

        self.logger.verbose(f"Querying Crystal Mind for: [cyan]{escape(db_path_str)}[/cyan]")

        try:
            db = GnosticDatabase(self.project_root)
            session = db.session

            # 2. The Gnostic Query
            record = (
                session.query(ScriptureModel)
                .filter(ScriptureModel.path == db_path_str)
                .first()
            )

            # [FACULTY 10] The Fuzzy Pathfinder
            if not record:
                # Try finding by filename only
                fuzzy_matches = session.query(ScriptureModel).filter(
                    ScriptureModel.path.like(f"%{Path(db_path_str).name}")
                ).limit(3).all()

                if fuzzy_matches:
                    suggestions = "\n".join([f"- {m.path}" for m in fuzzy_matches])
                    return self.failure(
                        f"Scripture '{db_path_str}' not found in the Crystal Mind.",
                        suggestion=f"Did you mean one of these?\n{suggestions}"
                    )
                return self.failure(f"Scripture '{db_path_str}' is unknown to the Gnostic Database.")

            # 3. Harvest Gnosis
            created_rite = session.query(RiteModel).get(record.created_by) if record.created_by else None
            updated_rite = session.query(RiteModel).get(record.updated_by) if record.updated_by else None

            # [FACULTY 3] The Causal Web
            dependencies = [b.target_path for b in record.dependencies]
            dependents = [b.source_path for b in record.dependents]

            # 4. [FACULTY 2] The Drift Sentinel
            drift_status = "UNKNOWN"
            live_hash = "N/A"
            if exists_on_disk:
                if record.is_binary:
                    drift_status = "BINARY (Unchecked)"
                else:
                    try:
                        content_bytes = target.read_bytes()
                        live_hash = hashlib.sha256(content_bytes).hexdigest()
                        if live_hash == record.content_hash:
                            drift_status = "PURE"
                        else:
                            drift_status = "DRIFTED"
                    except Exception:
                        drift_status = "UNREADABLE"
            else:
                drift_status = "VANISHED"

            # 5. [FACULTY 11] The Machine Interface
            # Use the renamed field
            if request.json_output:
                return self._render_json(record, created_rite, updated_rite, dependencies, dependents, drift_status)

            # 6. [FACULTY 1] The Holographic HUD (TUI Render)
            self._render_holograph(
                record, created_rite, updated_rite, dependencies, dependents,
                drift_status, target, exists_on_disk
            )

            return self.success("Gnostic Provenance Revealed.")

        except Exception as e:
            return self.failure(f"Crystal Mind Paradox: {e}")
        finally:
            if 'session' in locals(): session.close()

    def _render_holograph(self, record, created, updated, deps, dependents, drift, real_path, exists):
        """Forges the Cinematic Dashboard."""

        # --- PANEL 1: THE IDENTITY MATRIX (Top Left) ---
        id_table = Table(box=None, padding=(0, 1), show_header=False, expand=True)
        id_table.add_column("Key", style="bold cyan", justify="right")
        id_table.add_column("Value", style="white")

        id_table.add_row("Path", escape(record.path))
        id_table.add_row("Language", f"[{'blue' if record.language == 'python' else 'green'}]{record.language}[/]")
        id_table.add_row("Size", get_human_readable_size(record.size_bytes or 0))
        id_table.add_row("Permissions", f"[magenta]{record.permissions}[/]")

        drift_style = "bold green" if drift == "PURE" else "bold red" if drift in ("DRIFTED",
                                                                                   "VANISHED") else "dim yellow"
        id_table.add_row("Reality State", f"[{drift_style}]{drift}[/{drift_style}]")

        id_panel = Panel(id_table, title="[bold]Identity Matrix[/bold]", border_style="cyan")

        # --- PANEL 2: THE CHRONICLE OF RITES (Top Right) ---
        rites_table = Table(box=None, padding=(0, 1), show_header=True, expand=True, title_style="bold magenta")
        rites_table.add_column("Epoch", style="dim")
        rites_table.add_column("Rite", style="bold white")
        rites_table.add_column("Architect", style="yellow")
        rites_table.add_column("Time", style="green")

        if created:
            rites_table.add_row(
                "Genesis",
                escape(created.name),
                escape(created.architect),
                self._human_time(created.timestamp)
            )

        if updated and (not created or updated.id != created.id):
            rites_table.add_row(
                "Transfiguration",
                escape(updated.name),
                escape(updated.architect),
                self._human_time(updated.timestamp)
            )
        elif not updated and not created:
            rites_table.add_row("-", "Unknown Origin", "-", "-")

        if updated and updated.command_line:
            cmd_text = Text(f"\n$ {updated.command_line}", style="dim italic")
        elif created and created.command_line:
            cmd_text = Text(f"\n$ {created.command_line}", style="dim italic")
        else:
            cmd_text = Text("")

        rites_panel = Panel(
            Group(rites_table, cmd_text),
            title="[bold magenta]Chronicle of Rites[/bold magenta]",
            border_style="magenta"
        )

        # --- PANEL 3: THE WEB OF CAUSALITY (Middle) ---
        web_grid = Table.grid(expand=True, padding=1)
        web_grid.add_column(ratio=1)
        web_grid.add_column(ratio=1)

        dep_tree = Tree("[bold]Dependencies (Imports)[/bold]")
        if deps:
            for d in deps[:5]: dep_tree.add(f"[dim]{escape(d)}[/dim]")
            if len(deps) > 5: dep_tree.add(f"[italic]...and {len(deps) - 5} more[/italic]")
        else:
            dep_tree.add("[dim]None[/dim]")

        impact_tree = Tree("[bold]Impact (Dependents)[/bold]")
        if dependents:
            for d in dependents[:5]: impact_tree.add(f"[bold red]{escape(d)}[/bold red]")
            if len(dependents) > 5: impact_tree.add(f"[italic]...and {len(dependents) - 5} more[/italic]")
        else:
            impact_tree.add("[dim]None (Safe to excise)[/dim]")

        web_grid.add_row(dep_tree, impact_tree)
        web_panel = Panel(web_grid, title="[bold yellow]Causal Web[/bold yellow]", border_style="yellow")

        # --- PANEL 4: THE SOUL PREVIEW (Bottom) ---

        # [THE FIX] This logic is now fortified against empty or unreadable files.
        preview_content = "[dim]File vanished from reality.[/dim]"
        if exists:
            if record.is_binary:
                preview_content = "[bold red]Binary Content (Omitted)[/bold red]"
            else:
                try:
                    # Safely read up to 15 lines without using `next()`
                    lines = []
                    with open(real_path, 'r', encoding='utf-8', errors='replace') as f:
                        for i, line in enumerate(f):
                            if i >= 15:
                                lines.append("...")
                                break
                            lines.append(line)

                    preview_text = "".join(lines)

                    if not preview_text.strip():
                        preview_content = Text("File is empty.", style="dim italic", justify="center")
                    else:
                        lexer = record.language if record.language and record.language != 'unknown' else 'text'
                        preview_content = Syntax(preview_text, lexer, theme="monokai", line_numbers=True)

                except Exception as e:
                    preview_content = f"[red]Could not read file preview: {e}[/red]"

        try:
            posix_path = real_path.as_posix()
        except:
            posix_path = str(real_path).replace('\\', '/')

        subtitle_text = f"[dim][link=vscode://file/{posix_path}]Click to Open[/link][/dim]"

        soul_panel = Panel(
            preview_content,
            title=f"[bold green]Soul Preview: {escape(record.path)}[/bold green]",
            border_style="green",
            subtitle=subtitle_text
        )

        # --- FINAL ASSEMBLY ---
        layout = Layout()
        layout.split_column(
            Layout(name="top", ratio=1),
            Layout(name="middle", ratio=1),
            Layout(name="bottom", ratio=2)
        )
        layout["top"].split_row(
            Layout(id_panel, name="left"),
            Layout(rites_panel, name="right")
        )
        layout["middle"].update(web_panel)
        layout["bottom"].update(soul_panel)

        self.console.print(layout)

    def _human_time(self, dt: datetime.datetime) -> str:
        """[FACULTY 5] The Temporal Relative."""
        if not dt: return "Unknown"
        now = datetime.datetime.now(datetime.timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        diff = now - dt
        seconds = diff.total_seconds()

        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        else:
            return f"{int(seconds // 86400)}d ago"

    def _render_json(self, record, created, updated, deps, dependents, drift):
        """[FACULTY 11] The Machine Interface."""
        data = {
            "path": record.path,
            "status": drift,
            "integrity": {
                "stored_hash": record.content_hash,
                "size": record.size_bytes,
                "permissions": record.permissions
            },
            "lineage": {
                "created": {
                    "rite_id": created.id if created else None,
                    "name": created.name if created else None,
                    "timestamp": created.timestamp.isoformat() if created else None,
                    "architect": created.architect if created else None
                } if created else None,
                "last_updated": {
                    "rite_id": updated.id if updated else None,
                    "name": updated.name if updated else None,
                    "timestamp": updated.timestamp.isoformat() if updated else None,
                    "architect": updated.architect if updated else None
                } if updated else None
            },
            "graph": {
                "dependencies": deps,
                "dependents": dependents
            }
        }
        import json
        print(json.dumps(data, indent=2))
        return self.success("JSON Proclaimed.")