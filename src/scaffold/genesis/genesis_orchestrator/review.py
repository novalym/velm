# Path: genesis/genesis_orchestrator/review.py
# --------------------------------------------
from typing import List, Dict, TYPE_CHECKING

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm

from ...contracts.heresy_contracts import Heresy
from ...logger import Scribe, get_console
from ...utils import to_string_safe

if TYPE_CHECKING:
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GenesisReview")


class ReviewMixin:
    """
    =================================================================================
    == THE ALTAR OF REVIEW (V-Ω-UI-LAYER)                                          ==
    =================================================================================
    Handles the visual proclamation of plans, summaries, and heresies.
    """

    def _display_dialogue_summary(self: 'GenesisDialogueOrchestrator', title: str, current_gnosis: Dict, keys_to_summarize: List[str]):
        """
        [GC 3: Contextual Adjudication Summary] Displays a concise summary of gathered Gnosis.
        """
        console = get_console()
        if self.non_interactive: return  # No summary in silent mode

        summary_table = Table(title=f"[bold]{title} (Summary)[/bold]", box=None, show_header=True,
                              header_style="bold magenta")
        summary_table.add_column("Variable", style="cyan")
        summary_table.add_column("Value", style="white")

        for key in keys_to_summarize:
            value = current_gnosis.get(key, "[dim]N/A[/dim]")
            # Display booleans clearly, convert Text to string
            display_value = str(value).lower() if isinstance(value, bool) else to_string_safe(value)

            # Truncate long descriptions
            if key == 'description' and len(display_value) > 50:
                display_value = f"{display_value[:47]}..."

            summary_table.add_row(key, display_value)

        self.console.print(Panel(summary_table, border_style="magenta"))
        Prompt.ask("\n[dim]Press Enter to proceed...[/dim]")
        self.console.clear()

    def _proclaim_mentorship_dossier(self: 'GenesisDialogueOrchestrator', heresies: List[Heresy], relevant_keys: List[str]):
        """
        [THE MENTOR'S VOICE] Proclaims relevant heresies/warnings.
        """
        relevant_heresies = []
        for h in heresies:
            if ":" in h.line_content:
                key = h.line_content.split(':')[0].strip()
                if key in relevant_keys:
                    relevant_heresies.append(h)

        if relevant_heresies and not self.non_interactive:
            self.console.print()
            self.console.rule("[bold yellow]The Gnostic Mentor's Prophecy[/bold yellow]", style="yellow")
            for heresy in relevant_heresies:
                self.console.print(Panel(
                    Text.from_markup(
                        f"[bold]{heresy.message}[/bold]\n\n[dim]Violated Gnosis: {heresy.line_content}[/dim]"),
                    title=f"[bold yellow]⚠️ Architectural Warning[/bold yellow]",
                    border_style="yellow",
                    padding=(1, 2)
                ))
            Prompt.ask("\n[dim]The Mentor has spoken. Press Enter to continue the Sacred Dialogue...[/dim]")
            self.console.clear()

    def _present_interactive_blueprint_review(self: 'GenesisDialogueOrchestrator', prophecies_for_review: List[Dict],
                                              prophesied_commands: List[str],
                                              adjudicated_heresies: List[Heresy]):
        """
        [THE GOD-ENGINE OF LUMINOUS REVELATION]
        The final interactive review before materialization.
        """
        # Non-Interactive Ward
        if self.non_interactive:
            Logger.info("Non-interactive mode. Bypassing interactive blueprint review.")
            # We accept all prophecies by default.
            self.prophesied_items, self.prophesied_commands, self.adjudicated_heresies = \
                self.prophesied_items, prophesied_commands, adjudicated_heresies
            return

        self.console.print(Panel(
            "The Prophet's Gaze is complete. The Altar of Final Adjudication awaits your will.",
            title="[bold magenta]Prophecy Adjudication[/bold magenta]"
        ))

        # --- MOVEMENT I: HERESIES ---
        if adjudicated_heresies:
            self.console.rule("[bold yellow]Movement I: The Gnostic Mentor's Adjudication[/bold yellow]",
                              style="yellow")
            for heresy in adjudicated_heresies:
                self.console.print(Panel(
                    Text.from_markup(
                        f"[bold]{heresy.message}[/bold]\n\n[dim]Violated Gnosis: {heresy.line_content}[/dim]"),
                    title=f"[bold yellow]⚠️ {heresy.severity.name.title()} Heresy[/bold yellow]",
                    border_style="yellow", padding=(1, 2)
                ))
            Prompt.ask("\n[dim]The Mentor has spoken. Press Enter to review the prophesied Form...[/dim]")
            self.console.clear()

        # --- MOVEMENT II: FORM (Structure) ---
        if prophecies_for_review:
            self.console.rule("[bold green]Movement II: The Prophecy of Form[/bold green]", style="green")
            items_table = Table(title="[bold]Prophesied Blueprint Items[/bold]", box=None, show_header=True,
                                header_style="bold green")
            items_table.add_column("Type", style="cyan", width=10)
            items_table.add_column("Path", style="white", ratio=3)
            items_table.add_column("Description", style="dim", ratio=4)
            items_table.add_column("Soul's Origin", style="green", ratio=2)

            for prop in prophecies_for_review:
                items_table.add_row(
                    prop.get('type', 'File'),
                    prop.get('path', 'N/A'),
                    prop.get('description', 'N/A'),
                    prop.get('action', 'Add')
                )
            self.console.print(Panel(items_table, border_style="green"))

            if not Confirm.ask("\n[bold question]Shall this prophesied Form be made manifest?[/bold question]",
                               default=True):
                Logger.warn("Architect's Will perceived: The Prophecy of Form has been stayed.")
                self.prophesied_items.clear()

            if prophesied_commands:
                Prompt.ask("\n[dim]Press Enter to review the prophesied Will...[/dim]")
                self.console.clear()

        # --- MOVEMENT III: WILL (Commands) ---
        if self.prophesied_items and prophesied_commands:
            self.console.rule("[bold cyan]Movement III: The Prophecy of Will[/bold cyan]", style="cyan")
            commands_table = Table(title="[bold]Prophesied Maestro's Edicts[/bold]", box=None, show_header=True,
                                   header_style="bold cyan")
            commands_table.add_column("#", style="magenta", justify="right", width=4)
            commands_table.add_column("Command to be Conducted", style="cyan")

            for idx, cmd in enumerate(prophesied_commands):
                commands_table.add_row(str(idx + 1), cmd)
            self.console.print(Panel(commands_table, border_style="cyan"))

            if not Confirm.ask("\n[bold question]Shall this prophesied Will be conducted?[/bold question]",
                               default=True):
                Logger.warn("Architect's Will perceived: The Prophecy of Will has been stayed.")
                self.prophesied_commands.clear()

        # --- THE FINAL VOW ---
        self.console.rule("[bold magenta]The Point of No Return[/bold magenta]", style="magenta")
        Logger.info("The Prophet's Gaze is complete. The final Gnostic Plan has been synthesized.")
        if not self.prophesied_items and not self.prophesied_commands:
            Logger.warn("The final Gnostic Plan is a void. The Rite of Genesis is gracefully concluded.")
        else:
            Prompt.ask(
                "\n[dim]Press Enter to bestow the final plan upon the Master Weaver and conclude the Genesis rite...[/dim]")
            self.console.clear()