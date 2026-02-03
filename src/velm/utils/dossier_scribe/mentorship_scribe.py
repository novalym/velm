import random
from typing import List, Optional
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.markup import escape

# The Scribe now drinks from the one true wellspring of Gnostic wisdom.
from ...gnosis import ARCHITECTURAL_QUOTES

class MentorshipScribe:
    """
    =================================================================================
    == THE SCRIBE OF THE FINAL WORD (V-Ω-ETERNAL-APOTHEOSIS. THE DUAL SOUL)        ==
    =================================================================================
    This divine artisan is the one true Scribe for the Dossier's final proclamation.
    It possesses a dual soul:

    1. The Mentor's Voice: If it perceives Gnostic guidance, it forges a luminous
       Panel to proclaim the path to greater purity.
    2. The Oracle's Voice: If the Mentor is silent, it performs a sacred communion
       with the eternal Grimoire of Architectural Wisdom and proclaims a single verse.
    =================================================================================
    """

    def __init__(self, guidance: Optional[List[str]]):
        self.guidance = guidance

    def forge(self) -> Panel | Align:
        """The one true rite of forging for this Scribe."""
        if self.guidance:
            # --- The Mentor's Voice ---
            content = Text("The Gnostic Mentor has perceived a path to greater purity:\n", style="yellow")
            for i, suggestion in enumerate(self.guidance, 1):
                content.append(f"\n  {i}. ")
                content.append(Text.from_markup(suggestion))

            return Panel(
                content,
                title="[bold yellow]✨ Mentor's Guidance[/bold yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
        else:
            # --- The Oracle's Voice (Fallback) ---
            quote = random.choice(ARCHITECTURAL_QUOTES)
            return Align.center(Text(f'"{escape(quote)}"', style="dim italic"), vertical="middle")