# Path: scaffold/artisans/neural/tui.py
# -------------------------------------
import os
import time
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Select, Input, Label, Static, RichLog, Collapsible
from textual.screen import Screen
from textual import on, work
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax

from ...core.ai.engine import AIEngine
from ...core.ai.contracts import AIConfig
from ...settings.manager import SettingsManager


class NeuralConsoleApp(App):
    """
    =============================================================================
    == THE GNOSTIC COCKPIT (V-Ω-ASCENDED-UI-FINALIS)                           ==
    =============================================================================
    The final, ascended, interactive TUI for managing the Neural Cortex.
    """

    CSS = """
    Screen {
        overflow: hidden;
    }

    #main-container {
        layout: horizontal;
        height: 1fr;
        width: 1fr;
    }

    #config-pane {
        width: 50%;
        height: 100%;
        border-right: solid $accent;
        padding: 1 2;
    }

    #log-pane {
        width: 50%;
        height: 100%;
    }

    .section-title {
        text-align: center;
        width: 100%;
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }

    #status-header {
        dock: top;
        width: 100%;
        text-align: center;
        padding: 1;
        border-bottom: wide $primary;
        height: 5;
    }

    #config-grid {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1 2;
        margin-bottom: 1;
    }

    .label {
        text-align: right;
        color: $text-muted;
        margin-top: 1;
    }

    Input, Select {
        width: 1fr;
    }

    #test-area {
        dock: bottom;
        height: 12;
        padding: 1;
        border-top: wide $secondary;
    }

    #log {
        height: 1fr;
        border: none;
        background: $surface;
        padding: 0 1;
    }

    #actions {
        align: center middle;
        margin-top: 2;
        height: 3;
    }

    Button {
        margin: 0 1;
    }

    .status-online { color: $success; }
    .status-offline { color: $error; }
    .status-unknown { color: $warning; }
    """

    BINDINGS = [("q", "quit", "Quit"), ("s", "save_config", "Save & Apply")]

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.settings_manager = SettingsManager(engine.project_root)
        self.ai_engine = AIEngine.get_instance()
        self.current_config = self.ai_engine.config or AIConfig()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-container"):
            # --- Configuration Pane (Left) ---
            with VerticalScroll(id="config-pane"):
                yield Label("🧠 The Synaptic Console", classes="section-title")

                with Collapsible(title="Provider Configuration"):
                    with Container(id="config-grid"):
                        yield Label("Provider:", classes="label")
                        yield Select(
                            [(x, x) for x in ["openai", "anthropic", "google", "local"]],
                            value=self.current_config.provider,
                            id="provider-select"
                        )

                        yield Label("Model Name:", classes="label")
                        yield Input(value=self.current_config.model, id="model-input", placeholder="e.g. gpt-4-turbo")

                        yield Label("API Key:", classes="label")
                        yield Input(value=self.current_config.api_key or "", id="key-input", password=True)

                        yield Label("Base URL (Local/Enterprise):", classes="label")
                        yield Input(value=self.current_config.base_url or "", id="url-input",
                                    placeholder="http://localhost:1234/v1")

                with Collapsible(title="Model Parameters"):
                    with Container(id="config-grid"):
                        yield Label("Creativity (Temperature):", classes="label")
                        yield Input(value=str(self.current_config.temperature), id="temp-input")

                        yield Label("Max Tokens:", classes="label")
                        yield Input(value=str(self.current_config.max_tokens), id="tokens-input")

                with Horizontal(id="actions"):
                    yield Button("Save Configuration", id="btn-save", variant="success")
                    yield Button("Cancel", id="btn-cancel", variant="error")

            # --- Log & Test Pane (Right) ---
            with Vertical(id="log-pane"):
                yield Static(Panel("Gazing into the Noosphere...", title="[bold]Connection Status[/]"),
                             id="status-header")
                yield RichLog(id="log", wrap=True, markup=True)
                with Vertical(id="test-area"):
                    yield Label("Signal Test Protocol")
                    with Horizontal():
                        yield Input(placeholder="Send a test ping...", id="test-prompt", value="Are you online?")
                        yield Button("Transmit", id="btn-test", variant="primary")
        yield Footer()

    def on_mount(self):
        log = self.query_one("#log")
        log.write(Text("Synaptic Console Initialized. Awakening Gnostic Senses...", style="dim"))
        self.query_one("#test-prompt").focus()

        # [THE HEALING] We explicitly command the Conductor to use a thread for these synchronous rites.
        self.run_worker(self._check_provider_status, thread=True, exclusive=True, group="status_checks")
        self.run_worker(self._detect_local_services, thread=True, exclusive=True, group="discovery")

    # [THE HEALING] The profane @work decorator is annihilated.
    def _check_provider_status(self):
        import os
        provider = self.query_one("#provider-select").value
        status, message = "UNKNOWN", "Awaiting Gaze..."

        if provider in ("openai", "anthropic", "google"):
            key_name = f"{provider.upper()}_API_KEY"
            if self.query_one("#key-input").value or os.getenv(key_name):
                status, message = "ONLINE", "API key is present. Ready for communion."
            else:
                status, message = "OFFLINE", f"Heresy: The sacred key ({key_name}) is not manifest."

        elif provider == "local":
            base_url = self.query_one("#url-input").value
            if not base_url:
                status, message = "UNKNOWN", "No Base URL provided for local communion."
            else:
                import requests
                try:
                    ping_url = base_url.rsplit("/v1", 1)[0]
                    requests.get(ping_url, timeout=1.5)
                    status, message = "ONLINE", f"Communion successful with local nexus at {ping_url}."
                except requests.ConnectionError:
                    status, message = "OFFLINE", f"The local nexus at {base_url} refuses the connection."
                except Exception as e:
                    status, message = "HERESY", f"A paradox occurred during communion: {e}"

        self.call_from_thread(self._update_status_header, status, message)

    def _update_status_header(self, status: str, message: str):
        status_header = self.query_one("#status-header", Static)
        status_map = {
            "ONLINE": ("[bold green]● ONLINE[/]", "green"),
            "OFFLINE": ("[bold red]● OFFLINE[/]", "red"),
            "HERESY": ("[bold red]💀 HERESY[/]", "red"),
            "UNKNOWN": ("[bold yellow]● UNKNOWN[/]", "yellow"),
        }
        status_markup, border_color = status_map.get(status, ("[bold yellow]● UNKNOWN[/]", "yellow"))

        panel_content = Text.assemble(Text.from_markup(status_markup), Text(f"\n{message}", style="dim"))
        status_header.update(Panel(panel_content, border_style=border_color))

    # [THE HEALING] The profane @work decorator is annihilated.
    def _detect_local_services(self):
        import requests
        self.query_one("#log").write("[dim]Radar active: Scanning for local AI nexuses...[/dim]")
        local_urls = [
            ("http://localhost:11434/v1", "Ollama"),
            ("http://localhost:1234/v1", "LM Studio"),
            ("http://localhost:8080/v1", "LocalAI")
        ]
        for url, name in local_urls:
            try:
                requests.get(url.rsplit("/v1", 1)[0], timeout=0.5)
                self.call_from_thread(self._found_local_service, name, url)
            except:
                pass

    def _found_local_service(self, name: str, url: str):
        self.notify(f"Local nexus detected: {name} is online!")
        self.query_one("#log").write(f"📡 [bold green]Nexus Found:[/] {name} at {url}")

        if self.query_one("#provider-select").value == "local" and not self.query_one("#url-input").value:
            self.query_one("#url-input").value = url
            self.query_one("#log").write(f"✨ [bold magenta]Auto-linked to {name}.[/bold magenta]")
            self.run_worker(self._check_provider_status, thread=True, exclusive=True, group="status_checks")

    @on(Select.Changed, "#provider-select")
    def on_provider_change(self, event: Select.Changed):
        provider = event.value
        if provider == "openai":
            self.query_one("#model-input").value = "gpt-4o"
        elif provider == "anthropic":
            self.query_one("#model-input").value = "claude-3-opus-20240229"
        elif provider == "google":
            self.query_one("#model-input").value = "gemini-1.5-pro-latest"
        elif provider == "local":
            self.query_one("#model-input").value = "local-model"
            self.run_worker(self._detect_local_services, thread=True, exclusive=True, group="discovery")
        self.run_worker(self._check_provider_status, thread=True, exclusive=True, group="status_checks")

    @on(Button.Pressed, "#btn-save")
    def action_save_config(self):
        try:
            new_config = {
                "enabled": True, "provider": self.query_one("#provider-select").value,
                "model": self.query_one("#model-input").value, "api_key": self.query_one("#key-input").value,
                "base_url": self.query_one("#url-input").value,
                "temperature": float(self.query_one("#temp-input").value),
                "max_tokens": int(self.query_one("#tokens-input").value)
            }
            self.settings_manager.set_global("ai", new_config)
            self.ai_engine._reload_config()
            self.notify("Configuration Enshrined.", title="Success", severity="information")
            self.query_one("#log").write("[bold green]✅ Configuration Saved & Engine Reloaded.[/bold green]")
        except Exception as e:
            self.notify(f"Save Failed: {e}", severity="error")

    @on(Button.Pressed, "#btn-test")
    def action_test_signal(self):
        # [THE HEALING] The rite is now conducted via the Conductor.
        self.run_worker(self._run_test, thread=True, exclusive=True)

    @on(Input.Submitted, "#test-prompt")
    def on_submit_test(self):
        # [THE HEALING] The rite is now conducted via the Conductor.
        self.run_worker(self._run_test, thread=True, exclusive=True)

    # [THE HEALING] The profane @work decorator is annihilated.
    def _run_test(self):
        prompt = self.query_one("#test-prompt").value
        log = self.query_one("#log")
        try:
            temp_config = AIConfig(
                enabled=True, provider=self.query_one("#provider-select").value,
                model=self.query_one("#model-input").value, api_key=self.query_one("#key-input").value,
                base_url=self.query_one("#url-input").value, temperature=float(self.query_one("#temp-input").value),
                max_tokens=int(self.query_one("#tokens-input").value)
            )
            from ...core.ai.providers import get_provider
            provider = get_provider(temp_config.provider)
            if not provider:
                self.call_from_thread(log.write,
                                      f" H [bold red]Heresy:[/bold red] Provider '{temp_config.provider}' is unknown.")
                return
            provider.configure(temp_config)
            from ...core.ai.contracts import NeuralPrompt
            req = NeuralPrompt(user_query=prompt, system_instruction="Be concise and brief.")
            self.call_from_thread(log.write, f"\n[dim]Transmitting: {prompt}...[/dim]")
            full_text = ""
            for chunk in provider.stream_commune(req):
                full_text += chunk
                self.call_from_thread(log.write, Text(chunk, end=""))
            self.call_from_thread(log.write, "\n")
            self.call_from_thread(self.notify, "Signal Received.")
        except Exception as e:
            self.call_from_thread(log.write, f"\n [bold red]Transmission Failed:[/bold red] {e}")
            self.call_from_thread(self.notify, "Connection Failed", severity="error")

    @on(Button.Pressed, "#btn-cancel")
    def action_quit(self):
        self.exit()