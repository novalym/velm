# Path: scaffold/shell/widgets/dossier.py

import datetime
import json
from typing import Union, Any

from rich.console import RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.traceback import Traceback
from rich.json import JSON
from textual.widgets import RichLog


class LuminousDossier(RichLog):
    """
    =================================================================================
    == THE LUMINOUS DOSSIER (V-Ω-SEMANTIC-SCROLL)                                  ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The Scroll of Truth. It does not merely record; it *interprets*.
    It transmutes raw strings into Gnostic Artifacts (JSON, Tables, Tracebacks).
    """

    def proclaim(self, content: Union[str, RenderableType]):
        """The Universal Rite of Inscription."""
        self.write(content)

    def proclaim_command(self, command: str, cwd: str):
        """
        Inscribes the User's Will.
        Format: [TIME] path ❯ command
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        line = Text()
        line.append(f"[{timestamp}] ", style="dim white")
        line.append(f"{cwd}", style="bold blue")
        line.append(" ❯ ", style="bold magenta")
        line.append(command, style="bold white")

        self.write(line)

    def proclaim_error(self, error: str, details: str = ""):
        """Inscribes a Heresy in a Luminous Red Panel."""
        content = Text(error, style="bold white")
        if details:
            content.append("\n\n")
            content.append(details, style="dim white")

        panel = Panel(
            content,
            title="[bold red]⚡ GNOSTIC HERESY DETECTED[/bold red]",
            border_style="red",
            padding=(0, 1)
        )
        self.write(panel)

    def proclaim_artifact(self, data: Any, label: str = "Gnostic Artifact"):
        """Intelligently renders complex data structures."""
        if isinstance(data, (dict, list)):
            # JSON Artifact
            try:
                json_str = json.dumps(data, indent=2)
                # We use Rich's JSON renderable for beautiful highlighting
                self.write(Panel(JSON(json_str), title=f"[cyan]{label}[/cyan]", border_style="cyan"))
            except:
                self.write(str(data))

        elif isinstance(data, Table):
            self.write(data)

        elif isinstance(data, str) and (data.strip().startswith("# ") or "```" in data):
            # Markdown Artifact
            self.write(Markdown(data))

        elif isinstance(data, Exception):
            # Traceback Artifact
            self.write(Traceback.from_exception(type(data), data, data.__traceback__))

        else:
            self.write(str(data))

    def proclaim_stream(self, line: str):
        """
        Streams raw process output with semantic tinting.
        """
        clean_line = line.rstrip()
        if not clean_line: return

        style = "white"
        lower = clean_line.lower()

        if "error" in lower or "fail" in lower:
            style = "red"
        elif "success" in lower or "done" in lower:
            style = "green"
        elif "warn" in lower:
            style = "yellow"
        elif lower.startswith("downloading") or lower.startswith("fetching"):
            style = "cyan"
        elif lower.startswith("   ->"):  # Tree structure / steps
            style = "dim white"

        self.write(Text(clean_line, style=style))

    def clear_dossier(self):
        """Rite of Purification."""
        self.clear()
        self.proclaim(Text("The slate is wiped clean. History is reborn.", style="dim italic"))