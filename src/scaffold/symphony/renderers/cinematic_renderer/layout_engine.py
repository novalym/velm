# Path: scaffold/symphony/renderers/cinematic_renderer/layout_engine.py
# ---------------------------------------------------------------------

from rich.layout import Layout
from .widgets import (
    HeaderWidget, FooterWidget, TimelineWidget,
    OutputWidget, ContextWidget, ResourceMonitorWidget
)
from .state import CinematicState


class GnosticLayoutEngine:
    """
    =================================================================================
    == THE ARCHITECT OF SPACE (V-Ω-ADAPTIVE-GRID)                                  ==
    =================================================================================
    Constructs the renderable view from the state.
    """

    def __init__(self):
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=1)
        )
        self.layout["main"].split_row(
            Layout(name="sidebar", ratio=1),
            Layout(name="body", ratio=3)
        )
        self.layout["sidebar"].split(
            Layout(name="timeline", ratio=2),
            Layout(name="vitals", size=6),
            Layout(name="context", size=8)
        )

        # Instantiate Widgets
        self.header = HeaderWidget()
        self.footer = FooterWidget()
        self.timeline = TimelineWidget()
        self.monitor = ResourceMonitorWidget()
        self.context = ContextWidget()
        self.output = OutputWidget()

    def render(self, state: CinematicState) -> Layout:
        """Composes the current frame."""
        self.layout["header"].update(self.header.render(state))
        self.layout["footer"].update(self.footer.render(state))

        self.layout["timeline"].update(self.timeline.render(state))
        self.layout["vitals"].update(self.monitor.render(state))
        self.layout["context"].update(self.context.render(state))

        self.layout["body"].update(self.output.render(state))

        return self.layout