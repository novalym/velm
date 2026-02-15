# Path: scaffold/jurisprudence_core/heresy_chronicles/heresy_chronicler.py
# ----------------------------------------------------------------------
import sys
import traceback
from typing import Union

from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from .living_oracle import LivingOracle
from ...contracts.heresy_contracts import SyntaxHeresy, Heresy
from ...logger import Scribe

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # We attempt to speak with the native C-extension.
    from tree_sitter import Language, Parser, Node
    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native tongue is absent, we scry the Gnostic Registry (sys.modules)
    # for the Diamond Proxy forged by the Simulacrum.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        Language = _ts.Language
        Parser = _ts.Parser
        Node = _ts.Node
        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If no soul is manifest in any realm, we forge hollow vessels.
        TREE_SITTER_AVAILABLE = False

        # We use 'type' to forge a class that mimics the expected interface
        # without inheriting from 'object', preventing subtle MRO heresies.
        Language = type("HollowLanguage", (object,), {})
        Parser = type("HollowParser", (object,), {})
        Node = type("HollowNode", (object,), {})


Logger = Scribe("HeresyChronicler")


class HeresyChronicler:
    """
    =================================================================================
    == THE UNIVERSAL HERALD OF PARADOX (V-Ω-ETERNAL-APOTHEOSIS)                    ==
    =================================================================================
    LIF: 10,000,000,000

    This divine artisan is the bridge between raw Chaos (Exceptions) and luminous
    Order. It performs a Gnostic Triage upon any paradox, summons the correct
    artisans (`LivingOracle` for `SyntaxHeresy`), and forges a beautiful,
    hyper-diagnostic Dossier. It is the one true voice of adjudication.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Gnostic Triage:** Intelligently distinguishes between `SyntaxHeresy` (from
        Sentinel/Tree-sitter), `Heresy` (from Scaffold logic), and catastrophic `Exception`.
    2.  **The Oracle's Conduit:** Correctly summons the `LivingOracle` for deep,
        contextual analysis of `SyntaxHeresy` proclamations.
    3.  **The Luminous Dossier Forge:** Its `_proclaim_syntax_heresy` rite is now a
        masterpiece, forging a multi-part, cinematic panel of Gnostic insight.
    4.  **The Causal Narrative:** The Dossier includes the Ancestor Chain and Sibling
        Context from the `LivingOracle`, revealing the heresy's place in the cosmos.
    5.  **The Mentor's Voice:** It proclaims the Heuristic Counselor's wisdom, offering
        a path to purity.
    6.  **The Code Weaver:** It weaves the profane code snippet into the Dossier with
        luminous syntax highlighting and line numbers.
    7.  **The Heresy Unifier:** It gracefully handles generic `Heresy` objects, respecting
        any pre-rendered `details_panel` they may carry.
    8.  **The Unbreakable Ward of Grace:** Its every rite is shielded. A paradox within
        the Chronicler itself will not silence it completely.
    9.  **The Polyglot Soul:** It honors the language proclaimed by the `SyntaxHeresy`,
        applying the correct syntax highlighting.
    10. **The Sovereign Mind:** Its logic is pure, stateless, and self-contained.
    11. **The Pure Contract:** Its `proclaim` rite is an unbreakable, public contract.
    12. **The Final Word:** It is the one true, definitive voice for rendering all forms
        of paradox within the Scaffold and Sentinel cosmos.
    =================================================================================
    """

    @classmethod
    def proclaim(cls, paradox: Union[SyntaxHeresy, Heresy, QueryError, Exception]) -> Panel:
        """The One True Rite. Accepts a paradox and returns a Luminous Panel."""
        try:
            if isinstance(paradox, SyntaxHeresy):
                return cls._proclaim_syntax_heresy(paradox)
            if isinstance(paradox, Heresy):
                return cls._proclaim_generic_heresy(paradox)
            if TREE_SITTER_AVAILABLE and isinstance(paradox, QueryError):
                return cls._proclaim_catastrophe(paradox, "Tree-sitter Query Paradox")
            return cls._proclaim_catastrophe(paradox, "Catastrophic, Unhandled Paradox")
        except Exception as e:
            Logger.error(f"META-HERESY: The HeresyChronicler shattered: {e}", exc_info=True)
            return Panel(Text(f"Meta-Paradox: {e}\nOriginal: {str(paradox)}", style="bold red"),
                         title="[bold red]The Chronicler Has Fallen[/bold red]")

    @staticmethod
    def _proclaim_syntax_heresy(heresy: SyntaxHeresy) -> Panel:
        """
        [THE RITE OF LUMINOUS PROCLAMATION]
        Forges the complete, hyper-diagnostic Dossier for a `SyntaxHeresy`.
        """
        # --- MOVEMENT I: THE ORACLE'S GAZE ---
        # The Oracle is born and immediately performs its Gaze.
        oracle = LivingOracle(heresy=heresy)
        dossier = oracle.divine()

        # --- MOVEMENT II: THE FORGING OF THE DOSSIER ---
        # 1. The Core Gnosis (The Heresy Itself)
        heresy_table = Table(box=None, show_header=False, padding=(0, 1))
        heresy_table.add_column(style="dim", justify="right", width=12)
        heresy_table.add_column(style="white")
        heresy_table.add_row("Heresy:", f"[bold red]{heresy.message}[/bold red]")
        heresy_table.add_row("Rule:", f"[cyan]{heresy.rule_name}[/cyan]")
        heresy_table.add_row("Severity:", f"[yellow]{heresy.severity}[/yellow]")
        if heresy.suggestion:
            heresy_table.add_row("Suggestion:", f"[green]{heresy.suggestion}[/green]")

        # 2. The Gaze of the Ancestors (Structural Context)
        ancestor_text = Text(" > ".join(dossier.get('ancestors', ['unknown'])), style="dim")

        # 3. The Mentor's Voice (Heuristic Counsel)
        counsel_text = Text(dossier.get('counsel', 'The Oracle is silent on this matter.'), style="italic")

        # 4. The Profane Scripture (The Code)
        code_snippet = Syntax(
            heresy.context_window or heresy.line_content,
            heresy.language or "text",
            theme="monokai",
            line_numbers=True,
            start_line=heresy.line_number,
            highlight_lines={heresy.line_number}
        )

        # --- MOVEMENT III: THE FINAL ASSEMBLY ---
        # All Gnosis is woven into a single, luminous Group.
        final_group = Group(
            heresy_table,
            Rule(style="dim", characters="·"),
            Text("Causal Path:", style="dim"),
            ancestor_text,
            Rule(style="dim", characters="·"),
            Text("Mentor's Counsel:", style="dim"),
            counsel_text,
            Rule(style="dim"),
            code_snippet
        )

        return Panel(
            final_group,
            title=f"[bold red]Gnostic Inquest: {heresy.rule_name}[/bold red]",
            subtitle=f"[dim]L{heresy.line_number} in {heresy.file_path}[/dim]",
            border_style="red"
        )

    @staticmethod
    def _proclaim_generic_heresy(heresy: Heresy) -> Panel:
        """
        =================================================================================
        == THE HERALD OF THE FALLEN RITE (V-Ω-FORENSIC-BRIDGE)                         ==
        =================================================================================
        A proclamation for standard heresies, now with a Gaze that perceives the
        Gnostic link to a forensic artifact and forges a clickable bridge to its soul.
        =================================================================================
        """
        if heresy.details_panel:
            return heresy.details_panel

        content_group = []

        # Core Heresy Message
        content_group.append(Text.from_markup(f"[bold red]{heresy.message}[/bold red]\n"))

        if heresy.suggestion:
            # --- [ASCENSION] THE GAZE OF THE FORENSIC LINK ---
            # We perform a Gaze upon the suggestion to see if it contains the sacred link.
            import re
            link_regex = r"forensic artifact at: (file:\/\/.*?)(?:\s|$)"
            match = re.search(link_regex, heresy.suggestion)

            if match:
                artifact_uri = match.group(1)
                # We transmute the raw suggestion into a luminous proclamation.
                suggestion_text = Text.from_markup(
                    "💡 Suggestion: A forensic dossier has been archived for this paradox.\n"
                    "   Click the link below to gaze upon its soul."
                )

                # We forge a separate, high-visibility panel for the link.
                link_panel = Panel(
                    Text.from_markup(f"[bold link={artifact_uri}]{artifact_uri}[/bold link]"),
                    title="[bold yellow]🔗 Gnostic Forensic Link[/bold yellow]",
                    border_style="yellow"
                )
                content_group.extend([suggestion_text, link_panel, Rule(style="dim")])
            else:
                # Standard suggestion proclamation
                content_group.append(Text.from_markup(f"💡 Suggestion: {heresy.suggestion}\n"))

        if heresy.details:
            content_group.append(Text.from_markup(f"\n[dim]Details:\n{heresy.details}[/dim]"))

        return Panel(
            Group(*content_group),
            title="[bold red]Gnostic Heresy[/bold red]",
            subtitle=f"[dim]Locus: {heresy.line_content}[/dim]",
            border_style="red"
        )

    @staticmethod
    def _proclaim_catastrophe(error: Exception, title: str) -> Panel:
        """A humble proclamation for unhandled exceptions."""
        tb = traceback.format_exc()
        return Panel(
            Text(f"{type(error).__name__}: {str(error)}\n\n{tb}", style="red"),
            title=f"[bold red]{title}[/bold red]",
            border_style="red"
        )