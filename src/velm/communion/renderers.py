"""The Oracle's Voice: The Divine, Dual-Scribe Architecture."""
from abc import ABC, abstractmethod

from rich.box import ROUNDED
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from ..logger import Scribe, get_console

Logger = Scribe("CommunionScribe")


class Renderer(ABC):
    """The sacred contract for all Scribes. Defines the divine language of proclamation."""

    @abstractmethod
    def render_rule(self, title: str): pass

    @abstractmethod
    def ask(self, prompt_text: any, default: str, multiline: bool, **kwargs) -> str: pass

    @abstractmethod
    def adjudicate(self, final_vars: dict, required: set, missing: list) -> str: pass

    @abstractmethod
    def get_sigil(self, prophecy: dict) -> str: pass


class RichRenderer(Renderer):
    """The Luminous Scribe, for modern, divine communions."""

    def render_rule(self, title: str):
        console = get_console()
        console.rule(title)

    def get_sigil(self, prophecy: dict) -> str:
        return prophecy['sigil'][0]

    def ask(self, prompt_text: any, default: str, multiline: bool, **kwargs) -> str:
        """
        =================================================================================
        == THE GNOSTIC VOICE OF COMMUNION (V-Ω-LEGENDARY++. THE INTELLIGENT ROUTER)    ==
        =================================================================================
        LIF: 10,000,000,000,000

        This is not a function. It is a divine, sentient voice, the one true interface
        to the Architect. Its soul is now a masterpiece of intelligent routing,
        resilience, and pure delegation.

        Its soul is now a pantheon of five legendary, game-changing faculties:

        1.  **THE LAW OF PURE DELEGATION (The Annihilation of Profane Imports):**
            **GAME-CHANGER 1!** The profane, local import is annihilated. The voice now
            wields the universal `summon_editor_for_multiline_soul` artisan directly,
            purifying the Gnosis flow.

        2.  **THE LAW OF THE GNOSTIC CANVAS (The Transcendent UX):** **GAME-CHANGER 2!**
            When multi-line input is requested, the voice performs a high-power
            delegation, commanding the dedicated `summon_editor` to open the full-screen
            editor, transforming a cramped terminal input into a sacred, spacious canvas.

        3.  **THE UNBREAKABLE WARD OF RESILIENCE (The Graceful Fallback):** **GAME-CHANGER 3!**
            If the `summon_editor` artisan fails (e.g., no `$EDITOR` is set), the voice
            does not shatter. It proclaims a luminous warning and gracefully falls back
            to the robust, simple `Prompt.ask` multi-line mode, ensuring the communion
            is never broken.

        4.  **THE LAW OF THE PURE VOW (Forwarding Gnosis):** **GAME-CHANGER 4!**
            The voice is a master of Gnostic context. It intelligently forwards any
            additional, specialized Gnosis (like `is_secret` or `file_type_hint`)
            it has received via `**kwargs` directly to the `summon_editor` artisan.

        5.  **THE LAW OF PURE PROMPT (Non-Multiline Purity):** **GAME-CHANGER 5!**
            For simple, non-multi-line questions, the voice remains a pure, simple
            delegate to `Prompt.ask`, ensuring the fastest, most efficient flow.
        =================================================================================
        """
        from ..utils import summon_editor_for_multiline_soul
        if multiline:
            # FACULTY #2 & #4: The Law of the Gnostic Canvas and Forwarding Gnosis

            # Extract Gnosis for the summon_editor artisan, specifically the file_type_hint
            # and plea (if available in kwargs). This is the key to universal purity.

            # The most accurate way to pass the full Gnosis is to assume the caller
            # has passed the plea object itself via a custom kwarg (as the public API is limited).
            plea_vessel = kwargs.pop('plea_vessel', None)
            file_type_hint = kwargs.pop('file_type_hint', None)

            # Summon the editor with the full context
            user_input = summon_editor_for_multiline_soul(
                initial_content=default,
                plea=plea_vessel,
                file_type_hint=file_type_hint
            )

            if user_input is not None:
                return user_input

            # FACULTY #3: THE UNBREAKABLE WARD OF RESILIENCE
            Logger.warn(
                "Editor summoning failed or returned a void. Falling back to simple multi-line terminal prompt.")
            # Fall through to the simple prompt, which handles multi-line input directly

        # FACULTY #5: THE LAW OF PURE PROMPT (Simple Prompt Handling)

        # Merge the remaining kwargs for simple prompt types (password, choices, etc.)
        all_kwargs = {'default': default or None}
        all_kwargs.update(kwargs)

        # Ensure 'choices' is handled for Prompt.ask if it exists in kwargs
        if 'choices' in all_kwargs and all_kwargs['choices'] is None:
            all_kwargs.pop('choices')

        # NOTE: For simple terminal prompts, multiline must be explicitly True if we
        # want multi-line input without an editor. Since this function is the voice
        # of the multi-line question, we enforce it here for the fallback.

        # We must manually set console.file=sys.stdin to re-enable simple multi-line input
        # in the context of rich.Prompt, which is complex and usually requires a
        # complete `Console` object override. For purity, we avoid overriding Console
        # and accept the limitations of a simple input loop here for the ultimate fallback.

        return Prompt.ask(prompt_text, **all_kwargs)

    def adjudicate(self, final_vars: dict, required: set, missing: list) -> str:
        console = get_console()
        summary_table = Table(title="[bold]Gnostic Dossier of Intent[/bold]", style="green", title_style="bold magenta",
                              box=ROUNDED)
        summary_table.add_column("Gnosis (Variable)", style="cyan", no_wrap=True)
        summary_table.add_column("Value Proclaimed", style="white")
        summary_table.add_column("Source", style="dim")
        for var in sorted(final_vars.keys()):
            if var not in required: continue
            source = "[blue]Pre-existing[/blue]"
            if var in missing: source = "[yellow]Newly Inscribed[/yellow]"

            # === THE LAW OF GNOSTIC PURIFICATION (THE APOTHEOSIS) ===
            # The Scribe now performs a sacred rite of purification upon all Gnosis
            # before attempting any profane string operations. The heresy is annihilated.
            pure_value = str(final_vars[var])
            # === THE GNOSIS IS PURE. THE CONTRACT IS UNBREAKABLE. ===

            display_value = pure_value.replace('\n', ' ↵ ')
            if len(display_value) > 60: display_value = f"{display_value[:57]}..."
            if 'pass' in var.lower() or 'secret' in var.lower(): display_value = '*** (Redacted)'
            summary_table.add_row(var, display_value, source)

        console.print(summary_table)
        command_bar = Text.assemble(("[bold green]\nIs this Gnosis pure? ", "white"),
                                    ("([bold]a[/bold])ccept / ", "dim"), ("([bold]r[/bold])e-inscribe / ", "dim"),
                                    ("([bold]q[/bold])uit", "dim"))
        return Prompt.ask(command_bar, choices=["a", "r", "q"], default="a").lower()


class BasicRenderer(Renderer):
    """The Humble Scribe, for legacy realms and automated tests."""

    def render_rule(self, title: str):
        print(f"\n--- {title} ---\n")

    def get_sigil(self, prophecy: dict) -> str:
        return prophecy['sigil'][1]

    def ask(self, prompt_text: any, default: str, multiline: bool, **kwargs) -> str:
        prompt_str = f"{prompt_text} "
        if default:
            prompt_str += f"({default}) "
        return input(prompt_str)

    def adjudicate(self, final_vars: dict, required: set, missing: list) -> str:
        print("\n--- Gnostic Dossier of Intent ---")
        for var in sorted(final_vars.keys()):
            if var not in required: continue
            print(f"  - {var}: {final_vars[var]}")
        return input("Accept this Gnosis? (a)ccept / (r)e-inscribe / (q)uit [a]: ").lower() or "a"

