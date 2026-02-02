from typing import List, Optional
from rich.panel import Panel
from rich.text import Text

class ProphecyScribe:
    """Forges the 'Prophecy of the Next Step' panel."""
    def __init__(self, next_steps: Optional[List[str]]):
        self.next_steps = next_steps

    def forge(self) -> Panel:
        """The one true rite of forging for this Scribe."""
        prophecy_content = Text("To continue the Great Work:\n", style="white")

        if not self.next_steps:
            prophecy_content.append("Gaze upon the new reality to ensure its purity.", style="dim")
        else:
            for i, step in enumerate(self.next_steps, 1):
                # We use from_markup to render the rich styling embedded in the step strings
                prophecy_content.append(f"  {i}. ")
                prophecy_content.append(Text.from_markup(step))
                prophecy_content.append("\n")

        return Panel(
            prophecy_content,
            title="[bold]Prophecy of the Next Step[/bold]",
            title_align="left",
            border_style="dim",
            padding=(1, 2)
        )