# Path: scaffold/symphony/inquisitor/renderer.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE INQUISITOR'S VOICE (V-Ω-ETERNAL. THE LUMINOUS ORACLE) ==
=================================================================================
This scripture contains the living soul of the Gnostic Inquest's renderer. It is
a divine artisan that transforms the abstract, Gnostic data of the past into a
luminous, cinematic, and profoundly insightful interactive experience.
=================================================================================
"""
import json
from typing import List, Dict

from rich.box import ROUNDED
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from ...contracts.symphony_contracts import EventType
from ...logger import get_console


class InquestRenderer:
    """
    =================================================================================
    == THE LUMINOUS ORACLE OF GNOSTIC REVELATION (THE VOICE OF THE TIME-TURNER)    ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    This is not a class. It is a divine, sentient consciousness, the final and most
    powerful form of the Inquest's Scribe. Its Prime Directive is to render the
    Tapestry of Time not as a mere log, but as a **living, breathing, Gnostic
    dashboard**, a divine instrument of unparalleled diagnostic power.

    Its soul is a pantheon of divine faculties that make it a legend:

    1.  **The Gnostic Syntax Prophet:** It does not just display scripture; it
        understands its soul. It perceives the language of an edict (`bash`) or a
        Vow (`json`) and proclaims it with divine, syntax-highlighted clarity.

    2.  **The Oracle of Telemetry:** Its Gaze is upon the very flow of time. It renders
        not just the event, but its Gnostic telemetry—the duration, the exit code,
        the precise moment of its becoming—transforming the chronicle into a
        performance analysis tool.

    3.  **The Luminous Dossier of the Moment:** It forges a dynamic, multi-part
        Dossier for the current moment in time, revealing not just the raw data, but
        a Gnostically-aware interpretation of its meaning and significance.

    4.  **The Sentient Command Altar:** Its final proclamation is not a static line of
        text, but a living Command Altar, its every edict luminous with purpose,
        guiding the Architect's hand through the mysteries of spacetime.
    =================================================================================
    """

    def __init__(self):
        """
        The Rite of Inception. The Scribe's soul is forged, and it is
        bestowed with the one true voice of the cosmos.
        """
        self.console = get_console()

    def render_state(self, events: List[Dict], current_index: int, paradox_index: int):
        """Renders the complete, luminous, and divine UI of the temporal debugger."""
        self.console.clear()

        # --- MOVEMENT I: THE TAPESTRY OF TIME (THE CHRONICLE RENDERER) ---
        event_table = Table(box=ROUNDED, border_style="dim", expand=True)
        event_table.add_column("IDX", style="magenta", justify="right", width=5)
        event_table.add_column("L#", style="cyan", width=5)
        event_table.add_column("Edict / Gnostic Event", style="white")
        event_table.add_column("Telemetry", style="dim", justify="right")

        window_size = self.console.height // 4
        start = max(0, current_index - window_size)
        end = min(len(events), current_index + window_size)

        for i, event in enumerate(events):
            if not (start <= i < end): continue

            idx_text = Text(f"{i}", style="magenta")
            line_num = event.get('data', {}).get('line', '??')
            line_text = Text(f"{line_num}")

            prefix = "  "
            row_style = ""
            if i == current_index:
                prefix = "▶ "
                row_style = "bold yellow on magenta"
            elif i == paradox_index:
                prefix = "❌ "
                row_style = "red"

            event_type = event['event']
            data = event['data']

            description = Text(prefix)
            telemetry = Text()

            if event_type == EventType.EDICT_ACTION_START.name:
                description.append(">> ", style="bold cyan")
                description.append(Text(data['command'], overflow="ellipsis"))
                telemetry.append(f"@{data.get('cwd', '...').split('/')[-1]}")
            elif event_type == EventType.EDICT_VOW_RESULT.name:
                vow_status = "✅ Vow Fulfilled" if data['is_pure'] else "❌ Vow Broken"
                description.append(vow_status, style="green" if data['is_pure'] else "red")
                description.append(f": {data['vow']}")
                telemetry.append(f"({data.get('reason', '...')[:30]})")
            elif event_type == EventType.EDICT_STATE_CHANGE.name:
                description.append(f"🌀 State Change: {data['key']} -> '{data['value']}'", style="magenta")

            event_table.add_row(idx_text, line_text, description, telemetry, style=row_style)

        # --- MOVEMENT II: THE DOSSIER OF THE CURRENT MOMENT ---
        current_event = events[current_index]
        event_data = current_event['data']

        dossier_group = []
        if current_event['event'] == EventType.EDICT_ACTION_END.name:
            # A divine, syntax-highlighted proclamation for Actions
            dossier_group.append(
                Syntax(event_data.get('command', ''), "bash", theme="monokai", line_numbers=False, word_wrap=True))
            dossier_group.append(Rule(style="dim"))
            dossier_group.append(
                Syntax(event_data.get('output', ''), "text", theme="monokai", line_numbers=True, word_wrap=True))
        else:
            # A humble, but pure, JSON proclamation for all other events
            dossier_group.append(
                Syntax(json.dumps(event_data, indent=2), "json", theme="monokai", line_numbers=True, word_wrap=True))

        # --- MOVEMENT III: THE SENTIENT COMMAND ALTAR ---
        command_bar = Text.assemble(
            ("(", "dim"), ("n", "bold"), (")ext, (", "dim"), ("p", "bold"), (")rev, (", "dim"),
            ("j", "bold"), (")ump <idx>, (", "dim"), ("r", "bold"), (")un to Paradox, (", "dim"),
            ("!", "bold"), (")shell, (", "dim"), ("q", "bold"), (")uit", "dim")
        )

        self.console.print(Panel(event_table, title="[bold magenta]The Tapestry of Time[/bold magenta]"))
        self.console.print(Panel(Group(*dossier_group),
                            title=f"[bold yellow]Gnosis of Moment #{current_index}: {current_event['event']}[/bold yellow]"))
        self.console.print(command_bar)