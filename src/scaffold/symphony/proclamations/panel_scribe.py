# Path: scaffold/symphony/proclamations/panel_scribe.py
# -----------------------------------------------------

from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import DOUBLE

from .base import ProclamationHandler
from ...symphony.execution.kinetic_titan.semantics import SemanticGrimoire


class PanelProclamationHandler(ProclamationHandler):
    """The Scribe of the Imperial Decree."""

    @property
    def key(self) -> str:
        return "panel"  # This is the default/fallback scribe

    def execute(self, gnostic_arguments: str):
        """Forges a luminous, double-bordered panel."""

        # In this simple case, the argument is the message itself.
        final_message = self.alchemist.transmute(gnostic_arguments, self.regs.gnosis)

        clean_msg = final_message.strip()
        if len(clean_msg) >= 2 and clean_msg[0] in ('"', "'") and clean_msg[-1] == clean_msg[0]:
            clean_msg = clean_msg[1:-1]

        icon = SemanticGrimoire.divine_icon("proclaim")

        text_content = Text(clean_msg, justify="center")
        text_content.stylize("bold white")
        SemanticGrimoire.enhance(text_content)

        panel = Panel(
            text_content,
            title=f"[bold yellow]{icon} PROCLAMATION[/bold yellow]",
            border_style="magenta",
            box=DOUBLE,
            padding=(1, 2),
            expand=True
        )

        if not self.regs.dry_run:
            self.console.print(panel)