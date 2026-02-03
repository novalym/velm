# Path: scaffold/artisans/gui/app.py
# ----------------------------------

from typing import Any, List, Dict, Optional, Type
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, ListView, ListItem, Label, Static
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.reactive import reactive
from textual import on

from ...interfaces.requests import BaseRequest


class FormScreen(Screen):
    """A dynamic form generated from a Pydantic model."""

    def __init__(self, command_name: str, request_class: Type[BaseRequest]):
        super().__init__()
        self.command_name = command_name
        self.request_class = request_class
        self.inputs = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Configure Rite: {self.command_name}", classes="title")

        with Vertical(id="form-container"):
            fields = self.request_class.model_fields
            for name, field_info in fields.items():
                # Skip internal fields
                if name in ('project_root', 'verbose', 'silent', 'force', 'dry_run', 'request_id', 'timestamp'):
                    continue

                label_text = f"{name} ({field_info.annotation.__name__})"
                if field_info.default:
                    label_text += f" [Default: {field_info.default}]"

                yield Label(label_text)

                # Simple type mapping for V1
                inp = Input(placeholder=str(field_info.default or ""), id=f"input-{name}")
                self.inputs[name] = inp
                yield inp

        with Horizontal(id="buttons"):
            yield Button("Execute", variant="success", id="btn-exec")
            yield Button("Cancel", variant="error", id="btn-cancel")
        yield Footer()

    @on(Button.Pressed, "#btn-exec")
    def execute(self):
        # Construct the Request object
        data = {}
        for name, inp in self.inputs.items():
            val = inp.value
            # Basic type conversion (Prophecy: Use Pydantic's validation)
            if val:
                data[name] = val

        try:
            req = self.request_class(**data)
            self.dismiss((self.command_name, req))
        except Exception as e:
            self.notify(f"Validation Error: {e}", severity="error")

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self):
        self.dismiss(None)


class OmniBarApp(App):
    CSS = """
    .title { text-align: center; color: $accent; text-style: bold; margin: 1; }
    #form-container { padding: 1; }
    #buttons { align: center middle; margin-top: 1; }
    Button { margin: 1; }
    Input { margin-bottom: 1; }
    """

    def __init__(self, engine, initial_filter=None):
        super().__init__()
        self.engine = engine
        self.initial_filter = initial_filter
        self.registry = engine.registry._map  # {RequestType: ArtisanInstance}
        # Invert to map Command Name -> Request Type
        # This relies on the grimoire naming convention or inspecting the artisan
        self.commands = {}
        for req_type, artisan in self.registry.items():
            # Heuristic: Get command name from Artisan Name (e.g. WeaveArtisan -> weave)
            name = artisan.name.replace("Artisan", "").lower()
            self.commands[name] = req_type

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("The Omni-Bar", classes="title")
        yield Input(placeholder="Search Rites...", id="search-box", value=self.initial_filter or "")
        yield ListView(id="results")
        yield Footer()

    def on_mount(self):
        self._update_list(self.initial_filter or "")
        self.query_one("#search-box").focus()

    @on(Input.Changed, "#search-box")
    def filter_list(self, event: Input.Changed):
        self._update_list(event.value)

    def _update_list(self, query: str):
        lv = self.query_one("#results", ListView)
        lv.clear()
        for name in sorted(self.commands.keys()):
            if query.lower() in name:
                lv.append(ListItem(Label(name), id=name))

    @on(ListView.Selected)
    def on_select(self, event: ListView.Selected):
        cmd = event.item.id
        req_class = self.commands[cmd]
        self.push_screen(FormScreen(cmd, req_class), self.handle_form_result)

    def handle_form_result(self, result):
        if result:
            self.exit(result)