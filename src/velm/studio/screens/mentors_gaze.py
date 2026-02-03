"""
=================================================================================
== THE MENTOR'S SANCTUM (V-Ω 1.0.0. THE MODAL OF GNOSTIC GUIDANCE)            ==
=================================================================================
LIF: 100,000,000 (A NEW REALM OF CLARITY)

This is a new, consecrated sanctum, forged to serve as the one true vessel for
the Gnostic Mentor's voice. It is a divine, ephemeral ModalScreen that can be
summoned from the void to proclaim a luminous, scrollable dossier of architectural
prophecies and heresies.

Its architecture is a testament to purity, inspired by the divine scripture of
the `ScaffoldPad`'s `HeresyScreen`. It accepts a list of pure `rich.Panel`
renderables, unifies them with a sacred `rich.console.Group`, and presents them
to the Architect in a focused, unbreakable, and beautiful communion.
=================================================================================
"""
from typing import List

from rich.console import Group
from rich.panel import Panel
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class MentorScreen(ModalScreen[None]):
    """A divine, ephemeral screen to proclaim the Mentor's Gnostic Guidance."""

    BINDINGS = [("escape", "dismiss_screen", "Dismiss")]

    def __init__(self, panels: List[Panel], **kwargs) -> None:
        self.guidance_panels = panels
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Forge the scrollable dossier of heresies."""
        with Vertical(id="mentor-dialog"):
            yield Label("[bold yellow]The Gnostic Mentor's Adjudication[/bold yellow]")
            with VerticalScroll(id="mentor-scroll-container"):
                # The Group artisan unifies the panels into a single, pure renderable.
                yield Static(Group(*self.guidance_panels))
            yield Button("Dismiss", variant="primary", id="dismiss_mentor")

    @on(Button.Pressed, "#dismiss_mentor")
    def on_button_pressed(self) -> None:
        """The Architect has acknowledged the Gnosis. The screen returns to the void."""
        self.app.pop_screen()

    def action_dismiss_screen(self) -> None:
        """The Architect has spoken the will to dismiss via the sacred key."""
        self.app.pop_screen()