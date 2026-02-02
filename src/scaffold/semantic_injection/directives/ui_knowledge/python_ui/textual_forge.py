# scaffold/semantic_injection/directives/ui_knowledge/python_ui/textual_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("textual-dashboard")
def forge_textual_dashboard(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a rich Terminal User Interface (TUI) dashboard.
    Usage: tui.py :: @ui/component(name="OpsCenter")
    """
    return dedent(f"""
        from textual.app import App, ComposeResult
        from textual.containers import Container, Grid
        from textual.widgets import Header, Footer, Static, Button, Log, Digits

        class StatusWidget(Static):
            def compose(self) -> ComposeResult:
                yield Digits("42.0", id="cpu")
                yield Static("CPU Usage %", classes="label")

        class {name}(App):
            CSS = '''
            Screen {{ layout: grid; grid-size: 2; grid-gutter: 1; padding: 1; }}
            .box {{ height: 100%; border: solid green; background: $surface; }}
            .label {{ text-align: center; color: $text-muted; }}
            #log {{ row-span: 2; }}
            '''

            BINDINGS = [("d", "toggle_dark", "Dark Mode"), ("q", "quit", "Quit")]

            def compose(self) -> ComposeResult:
                yield Header()
                yield Container(StatusWidget(), classes="box")
                yield Container(Static("Memory: 12GB / 32GB\\nDisk: 45%"), classes="box")
                yield Log(id="log", classes="box")
                yield Footer()

            def on_mount(self) -> None:
                self.query_one(Log).write_line("System initialized.")
                self.query_one(Log).write_line("Monitoring Gnostic frequencies...")

        if __name__ == "__main__":
            {name}().run()
    """).strip()