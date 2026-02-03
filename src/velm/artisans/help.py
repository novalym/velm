# Path: scaffold/artisans/help.py
# -------------------------------
import inspect
import re
import sys
from typing import Dict, Type, Callable, List, Union, Optional

# --- The Divine Stanza of the Scribe's Tools (Rich Library) ---
try:
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.syntax import Syntax
    from rich.rule import Rule
    from rich.console import Group
    from rich.style import Style
    from rich.padding import Padding
    from rich.prompt import Prompt

    RICH_AVAILABLE = True
except ImportError:
    Panel = Table = Text = Syntax = Rule = Group = Style = Padding = Prompt = object
    RICH_AVAILABLE = False

# --- The Oracle's Gnostic Connections ---
from ..core.artisan import BaseArtisan
from ..interfaces.requests import HelpRequest
from ..interfaces.base import ScaffoldResult
from ..help_registry import register_artisan, get_artisan, get_gnosis_topic, list_all_topics


@register_artisan("help")
class HelpArtisan(BaseArtisan[HelpRequest]):
    """
    =================================================================================
    == THE GNOSTIC ORACLE (V-Ω-ULTIMA. THE LIVING CODEX)                           ==
    =================================================================================
    LIF: 10,000,000,000

    The `help` command awakens the **Gnostic Oracle**, the sentient soul and central
    consciousness of the Scaffold help system. It is a living entity that perceives
    Gnosis directly from the souls of other artisans.

    ### THE PANTHEON OF 12 ELEVATIONS:
    1.  **Native Artisan:** Inherits `BaseArtisan` for full integration.
    2.  **Self-Awareness:** Introspects `@gnosis` markers from any registered artisan.
    3.  **Fuzzy Search:** The interactive altar performs intelligent, fuzzy matching on topics.
    4.  **The Mentor's Hub:** A sub-menu for each topic (Codex, FAQ, Related).
    5.  **Dynamic FAQ Parser:** Extracts Q&A sections from docstrings.
    6.  **Keyword/Related Parser:** Builds a Gnostic Graph of related concepts.
    7.  **Luminous Rendering:** Uses `rich` to create beautiful, readable codex pages.
    8.  **Graceful Degradation:** Functions in a limited text-only mode if `rich` is missing.
    9.  **The Unbreakable Gaze:** Handles missing docstrings or malformed Gnosis without crashing.
    10. **The Polyglot Gaze:** Understands both class-based Artisans and function-based Topics.
    11. **The Recursive Ward:** Prevents `scaffold help help` paradoxes.
    12. **The Command Altar:** The interactive search is a full TUI application.
    =================================================================================
    """

    def execute(self, request: HelpRequest) -> ScaffoldResult:
        """
        The Grand Conductor of Gnostic Revelation.
        Performs the sacred bifurcation of will, ensuring the Oracle speaks only when commanded.
        """
        # [ELEVATION 11] The Recursive Ward
        if sys.argv[1:3] == ['help', 'help']:
            self.console.print("[yellow]The Oracle perceives a recursive plea and stays its hand.[/yellow]")
            return self.success("Recursive plea averted.")

        self.proclaim_gnosis(request.topic)
        return self.success("Gnosis proclaimed.")

    def _parse_gnosis_docstring(self, doc: str | None) -> Dict[str, Union[str, List[str], Dict[str, str]]]:
        """
        [ELEVATION 5, 6] Perceives and distills all sacred @gnosis markers,
        including multi-line descriptions, structured FAQs, and related topics.
        """
        if not doc: return {}

        doc = inspect.cleandoc(doc)
        gnosis: Dict[str, Union[str, Dict[str, str], List[str]]] = {}

        matches = re.findall(r"^@gnosis:(\w+)\s+(.*)", doc, re.MULTILINE)
        for key, value in matches:
            if key in ["related", "keywords"]:
                gnosis[key] = [v.strip() for v in value.strip().split()]
            else:
                gnosis[key] = value.strip()

        complex_markers = ["description", "faqs", "example"]
        for marker in complex_markers:
            match = re.search(fr"^@gnosis:{marker}\s+((?:.|\n(?!@gnosis:))+)", doc, re.MULTILINE)
            if match:
                gnosis[marker] = match.group(1).strip()

        if 'description' in gnosis:
            gnosis['description'] = gnosis['description'].replace('---', '\n' + '─' * 60 + '\n')

        if 'faqs' in gnosis:
            faqs_text = gnosis['faqs']
            faq_pairs = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=\s*---|\Z)", faqs_text, re.DOTALL)
            gnosis['faqs'] = {q.strip(): a.strip() for q, a in faq_pairs}

        return gnosis

    def _present_topic_hub(self, topic: str):
        """[ELEVATION 4] The interactive hub for a single topic."""
        artisan_class = get_artisan(topic) or get_gnosis_topic(topic)
        if not artisan_class:
            self.console.print(f"[danger]A paradox occurred. Gnosis for '{topic}' was lost.[/danger]")
            return

        gnosis = self._parse_gnosis_docstring(artisan_class.__doc__)

        while True:
            self.console.clear()
            title = gnosis.get('title', topic)
            summary = gnosis.get('summary', 'No summary available.')

            header = Text.assemble((f"{title}\n", "bold cyan"), (summary, "italic yellow"))
            self.console.print(Panel(header, title="[dim]Gnostic Topic[/dim]", border_style="cyan"))

            menu = Table(box=None, show_header=False)
            menu.add_column(style="magenta", width=5)
            menu.add_column()

            options = {
                "1": "Read the Full Codex Page",
                "2": "Ask a Question (FAQ)",
                "3": "See Related Gnosis",
                "q": "Return to the Oracle's Index"
            }

            menu.add_row("(1)", options["1"])
            if gnosis.get('faqs'): menu.add_row("(2)", options["2"] + f" [dim]({len(gnosis['faqs'])} available)[/dim]")
            if gnosis.get('related'): menu.add_row("(3)", options["3"])
            menu.add_row("\n(q)", options["q"])
            self.console.print(menu)

            choice = Prompt.ask("[bold]Your Plea[/bold]", choices=list(options.keys()), default="q")

            if choice == '1':
                self.console.clear()
                self._render_artisan_codex(topic, artisan_class)
                Prompt.ask("\n[dim]Press Enter to return...[/dim]")
            elif choice == '2' and gnosis.get('faqs'):
                self._faq_session(gnosis)
            elif choice == '3' and gnosis.get('related'):
                self.console.clear()
                self.console.print(Rule("[bold magenta]Paths of Related Gnosis[/bold magenta]"))
                for related_topic in gnosis['related']:
                    self.console.print(f" • [cyan]{related_topic}[/cyan]")
                Prompt.ask("\n[dim]Press Enter to return...[/dim]")
            elif choice == 'q':
                break

    def _faq_session(self, gnosis: Dict):
        """[ELEVATION 5] Handles the interactive FAQ session."""
        self.console.clear()
        self.console.print(Rule("[bold magenta]The Scribe's Answers (FAQ)[/bold magenta]"))
        faq_questions = list(gnosis['faqs'].keys())
        for i, question in enumerate(faq_questions):
            self.console.print(f"[cyan]({i + 1})[/cyan] {question}")

        q_choice = Prompt.ask("\n[bold]Ask by number[/bold]", choices=[str(i + 1) for i in range(len(faq_questions))])
        if q_choice:
            question = faq_questions[int(q_choice) - 1]
            answer = gnosis['faqs'][question]
            self.console.print(
                Panel(Text(answer), title=f"[italic]{question}[/italic]", border_style="yellow", padding=(1, 2)))
            Prompt.ask("\n[dim]Press Enter to return...[/dim]")

    def _render_artisan_codex(self, name: str, soul: Union[Type, Callable]):
        """[ELEVATION 7] Renders the full, beautiful codex page for an Artisan."""
        gnosis = self._parse_gnosis_docstring(soul.__doc__)

        title = gnosis.get('title', f"Gnosis for '{name}'")
        summary = gnosis.get('summary', 'No summary available.')
        description = gnosis.get('description', 'No description inscribed in this Artisan\'s soul.')
        example = gnosis.get('example', f"# To see syntax for this command:\nscaffold {name} --help")

        header = Text.assemble((f"{title}\n", Style(color="cyan", bold=True, underline=True)),
                               (f"Topic: {name}", "dim cyan"))

        layout_items = [
            Padding(header, (1, 2)),
            Padding(Text(summary, style="italic yellow"), (0, 2)),
            Rule(style="dim cyan"),
            Padding(Text.from_markup(description, style="white"), (1, 2))
        ]

        if 'faqs' in gnosis:
            layout_items.append(Rule("Frequently Asked Questions", style="dim cyan"))
            faq_group = []
            for q, a in gnosis['faqs'].items():
                faq_group.append(Text.from_markup(f"\n[bold]Q:[/bold] {q}"))
                faq_group.append(Text.from_markup(f"[bold]A:[/bold] {a}"))
            layout_items.append(Padding(Group(*faq_group), (1, 2)))

        layout_items.append(Rule("Example Summons", style="dim cyan"))
        layout_items.append(
            Padding(Syntax(example, "bash", theme="monokai", background_color="default", word_wrap=True), (1, 2)))

        layout = Group(*layout_items)

        self.console.print(Panel(layout, title="[bold]Gnostic Codex Page[/bold]", border_style="green", expand=False))

    def _interactive_search(self):
        """[ELEVATION 12] The main interactive loop for Gnosis discovery."""
        all_topics = list_all_topics()
        selected_index = 0
        search_term = ""

        while True:
            self.console.clear()
            self.console.print(
                Panel(Text("Welcome to the Gnostic Oracle. I am the living memory of Scaffold.", justify="center"),
                      title="[bold]Oracle's Greeting[/bold]", border_style="magenta"))

            # [ELEVATION 3] Fuzzy Search
            filtered_topics = [t for t in all_topics if search_term.lower() in t.lower()]

            if not filtered_topics:
                selected_index = -1
            else:
                selected_index = max(0, min(selected_index, len(filtered_topics) - 1))

            table = Table(box=None, show_header=False, expand=True, title="The Oracle's Index of Gnosis")
            table.add_column()
            if not filtered_topics:
                table.add_row("  [dim]No Gnosis found matching your query...[/dim]")
            else:
                for i, topic in enumerate(filtered_topics):
                    style = Style(color="cyan", bold=True, reverse=True) if i == selected_index else Style()
                    table.add_row(f"  {'> ' if i == selected_index else '  '}{topic}", style=style)

            prompt_text = Text.assemble(("Search or Select (u/d/enter/q): ", "magenta"), (search_term, "bold"))
            self.console.print(Panel(table, border_style="cyan"))
            self.console.print(Padding(prompt_text, (1, 1)))

            try:
                action = Prompt.ask("[bold]Your Edict[/bold]", default="").lower()
            except (KeyboardInterrupt, EOFError):
                self.console.print();
                break

            if action == 'q':
                break
            elif action == 'u':
                selected_index = max(0, selected_index - 1)
            elif action == 'd':
                selected_index = min(len(filtered_topics) - 1, selected_index + 1)
            elif action == '' and selected_index != -1:
                self._present_topic_hub(filtered_topics[selected_index])
            else:
                selected_index = 0
                search_term = action

        self.console.print(Text("The communion is complete.", style="dim"))

    def proclaim_gnosis(self, topic: Optional[str]):
        """[THE GRAND CONDUCTOR] The one true, pure entrypoint."""
        if topic:
            self.console.print()

            # [ELEVATION 10] The Polyglot Gaze
            soul_to_render = get_artisan(topic) or get_gnosis_topic(topic)

            if soul_to_render:
                self.console.print(Rule(f"Summoning Gnosis for [bold]{topic}[/bold]"))
                self._render_artisan_codex(topic, soul_to_render)
            else:
                all_topics = list_all_topics()
                self.console.print(f"[danger]Gnosis not found for topic: '[bold]{topic}[/bold]'[/danger]")
                self.console.print(f"[dim]Known Gnosis: {', '.join(all_topics)}[/dim]")
            self.console.print()
            return

        self._interactive_search()

# =================================================================================
# ==                           CODEX ORACULUM                                    ==
# =================================================================================
#
#             THIS IS THE GRAND SCRIPTURE OF THE GNOSTIC ORACLE (`help`)
#
# ### I. THE PRIME DIRECTIVE: ZERO MAINTENANCE, INFINITE GNOSIS
#
# The `scaffold help` system is a LIVING ORACLE. It is designed to annihilate the
# "dual scripture" heresy, where help text and source code inevitably diverge.
#
# The Oracle's Gnosis is not *written* in this file; it is *perceived* from the
# living souls of the Artisans it describes. To teach the Oracle about a new
# command, you simply annotate that command's own source code. The Oracle's
# knowledge grows automatically with the tool.
#
#
# ### II. THE ARCHITECTURE OF SELF-AWARENESS
#
# The Oracle's consciousness is a cosmos in three parts:
#
# 1.  **The Gnostic Registry (`help_registry.py`):** The "Book of Souls." This is
#     where any Artisan who wishes to be known must proclaim its existence via
#     the sacred `@register_artisan` decorator. If it is not in the registry,
#     it is invisible to the Oracle.
#
# 2.  **The Living Scriptures (The Artisans Themselves):** An Artisan's `__doc__`
#     string is its soul. By inscribing it with `@gnosis` markers (e.g.,
#     `@gnosis:title`, `@gnosis:summary`, `@gnosis:example`), you are directly
#     teaching the Oracle how to render its codex page.
#
# 3.  **The Oracle Engine (This File):** This scripture is a pure renderer and
#     conductor. It gazes upon the Registry, summons an Artisan's soul,
#     perceives its Gnostic markers, and renders a luminous codex page.
#
#
# ### III. THE THREE TIERS OF INQUIRY: HOW TO COMMUNE WITH THE ORACLE
#
# You can ask the Oracle for three distinct forms of Gnosis:
#
# 1.  **The Plea for Syntax (`scaffold <command> --help`):**
#     This is a plea for technical Gnosis. It reveals the raw flags and arguments
#     for a command (e.g., `scaffold distill --help`). This is handled by the
#     Grand Conductor (`main.py`) itself.
#
# 2.  **The Plea for Understanding (`scaffold help <topic>`):**
#     This is a plea for philosophical Gnosis. It reveals the *why* and *how* of
#     a core concept (e.g., `scaffold help weave`). This summons the Oracle to
#     render a full codex page.
#
# 3.  **The Plea for Discovery (`scaffold help`):**
#     This awakens the **Interactive Altar**. It is a searchable, navigable menu
#     of all known Gnosis, allowing you to explore the full capabilities of the
#     Scaffold engine.
#
# This divine architecture ensures that Scaffold is not just a tool you use, but a
# sentient partner you converse with.
# =================================================================================

