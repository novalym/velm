# scaffold/artisans/replay.py

"""
=================================================================================
== THE CHRONOMANCER (V-Ω-TEMPORAL-GOD-ENGINE)                                  ==
=================================================================================
LIF: 10,000,000,000,000,000

This artisan is not a simple script runner. It is a Temporal Engine.
It allows the Architect to walk the timeline of the Daemon's traffic logs,
inspecting, editing, and resurrecting past requests.

It performs **Quantum Divergence Analysis**: comparing the result of the
resurrected rite against the historical record to detect Temporal Paradoxes
(regressions or state drifts).
=================================================================================
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional

from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import ReplayRequest


# --- THE SACRED VESSELS OF TIME ---

@dataclass
class TemporalEvent:
    """A single moment in the Gnostic Timeline."""
    index: int
    timestamp: float
    command: str
    params: Dict[str, Any]
    # Historical outcome
    was_successful: bool = True
    response_message: str = ""


@dataclass
class ReplaySession:
    """The state of the Time Machine."""
    events: List[TemporalEvent]
    cursor: int = 0
    paradoxes: List[str] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0


class ReplayArtisan(BaseArtisan[ReplayRequest]):

    def execute(self, request: ReplayRequest) -> ScaffoldResult:

        log_path = Path(request.log_path)
        if not log_path.exists():
            return self.failure(f"The Chronicle of Time ({log_path}) does not exist.")

        self.logger.info(f"Opening the Time Portal at {log_path}...")

        # 1. The Rite of Remembrance (Loading the Chronicle)
        session = self._load_chronicle(log_path, request.filter_command)
        if not session.events:
            return self.failure("The Chronicle is empty or contains no playable events.")

        self.logger.info(f"Perceived {len(session.events)} resurrection candidates.")

        # 2. The Rite of the Atomic Sandbox
        # If the user wants to rehearse, we must perform a translocation.
        # (Future expansion: Integrating with TranslocateArtisan for full sandboxing)

        # 3. The Interactive Loop of Resurrection
        console = Console()

        try:
            while session.cursor < len(session.events):
                event = session.events[session.cursor]

                # --- The Interface of Time ---
                if request.interactive:
                    action = self._present_temporal_interface(console, session, event)

                    if action == "quit":
                        break
                    elif action == "skip":
                        session.cursor += 1
                        continue
                    elif action == "edit":
                        event = self._conduct_temporal_mutation(console, event)
                    # action == "play" continues below

                # --- The Resurrection ---
                self._resurrect_event(request, session, event, console)
                session.cursor += 1

        except KeyboardInterrupt:
            console.print("\n[yellow]Time Travel interrupted by Architect.[/yellow]")

        # 4. The Final Verdict
        return self._forge_final_verdict(session)

    def _load_chronicle(self, path: Path, filter_cmd: Optional[str]) -> ReplaySession:
        """
        [THE GAZE OF THE HISTORIAN]
        Parses the raw JSONL log into structured TemporalEvents.
        """
        events = []
        idx = 0

        # We need to pair requests with responses to know historical success.
        # This simple version just reads INBOUND requests.
        # A full version would correlate IDs.

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        entry = json.loads(line)

                        # We only care about INBOUND commands
                        if entry.get("direction") != "INBOUND":
                            continue

                        # Parse the payload
                        payload = json.loads(entry.get("preview", "{}"))
                        command = payload.get("command")
                        params = payload.get("params", {})

                        # Filter System Commands
                        if command in ["ping", "shutdown", "help", "status", "capabilities"]:
                            continue

                        # Apply User Filter
                        if filter_cmd and command != filter_cmd:
                            continue

                        # Forge the Event
                        events.append(TemporalEvent(
                            index=idx,
                            timestamp=entry.get("timestamp", 0),
                            command=command,
                            params=params
                        ))
                        idx += 1

                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            self.logger.error(f"Chronicle Corruption: {e}")

        return ReplaySession(events=events)

    def _present_temporal_interface(self, console: Console, session: ReplaySession, event: TemporalEvent) -> str:
        """
        [THE CHRONOMETRIC HUD]
        Renders the current state of time and accepts the Architect's will.
        """
        # 1. Format Params nicely
        params_json = json.dumps(event.params, indent=2)

        # Mask Secrets
        if "token" in params_json or "key" in params_json:
            # Simple heuristic masking
            pass

            # 2. Build the Dashboard
        table = Table(show_header=False, box=None, expand=True)
        table.add_column("Key", style="bold cyan", width=12)
        table.add_column("Value", style="white")

        table.add_row("Event ID", f"#{event.index + 1} of {len(session.events)}")
        table.add_row("Rite", f"[bold magenta]{event.command}[/bold magenta]")
        table.add_row("Timeline", f"{time.ctime(event.timestamp)}")

        panel = Panel(
            Text.from_markup(f"{params_json}"),
            title=f"[bold yellow]Temporal Locus: {event.command}[/bold yellow]",
            subtitle="[dim]Parameters of the Past[/dim]",
            border_style="blue"
        )

        console.clear()
        console.print(table)
        console.print(panel)

        # 3. The Prompt
        options = "[bold green](p)[/bold green]lay, [bold yellow](s)[/bold yellow]kip, [bold blue](e)[/bold blue]dit, [bold red](q)[/bold red]uit"
        choice = Prompt.ask(f"Command Time: {options}", choices=["p", "s", "e", "q"], default="p")

        mapping = {"p": "play", "s": "skip", "e": "edit", "q": "quit"}
        return mapping[choice]

    def _conduct_temporal_mutation(self, console: Console, event: TemporalEvent) -> TemporalEvent:
        """
        [THE MUTABLE TIMELINE]
        Allows the Architect to rewrite history before executing it.
        """
        console.print("[bold blue]-- MUTATING TIMELINE --[/bold blue]")

        # 1. Edit Variables
        if "variables" in event.params:
            current_vars = event.params["variables"]
            console.print(f"Current Variables: {current_vars}")
            if Confirm.ask("Modify a variable?", default=False):
                key = Prompt.ask("Variable Key")
                val = Prompt.ask("New Value")
                event.params["variables"][key] = val

        # 2. Edit Target
        if "target_directory" in event.params:
            current_target = event.params["target_directory"]
            if Confirm.ask(f"Change target ({current_target})?", default=False):
                new_target = Prompt.ask("New Target")
                event.params["target_directory"] = new_target

        return event

    def _resurrect_event(self, request: ReplayRequest, session: ReplaySession, event: TemporalEvent, console: Console):
        """
        [THE RITE OF RESURRECTION]
        Re-forges the Request object and dispatches it to the Engine.
        """

        try:
            from ..core.daemon import GnosticNexus
            # 1. Identify the Contract
            request_class = GnosticNexus.REQUEST_MAP.get(event.command)
            if not request_class:
                console.print(f"[red]Heresy:[/red] Unknown rite '{event.command}'. Skipping.")
                return

            # 2. Contextual Injection
            # We must inject the CURRENT project root if the historical one is missing or invalid,
            # unless we want to exactly reproduce the past.
            # Usually, we want to apply history to the *current* context.
            invocation_params = event.params.copy()
            if request.project_root:
                invocation_params["project_root"] = request.project_root

            # 3. Force Overrides
            if request.force:
                invocation_params["force"] = True

            # 4. Forge the Request
            resurrected_request = request_class(**invocation_params)

            # 5. Dispatch
            console.print(f"[dim]Resurrecting...[/dim]")

            # We broadcast this event to the Daemon so external UIs know we are time-travelling
            # (This requires the Engine to have a reference to the Daemon, which is circular.
            #  Instead, we log a specific event that the Daemon's traffic scribe picks up.)

            result = self.engine.dispatch(resurrected_request)

            # 6. Quantum Divergence Analysis
            self._analyze_divergence(session, event, result, console)

        except ValidationError as e:
            console.print(f"[bold red]Schema Heresy:[/bold red] Historical data violates current laws.\n{e}")
            session.paradoxes.append(f"Event {event.index}: Schema Validation Failed")
        except Exception as e:
            console.print(f"[bold red]Catastrophic Paradox:[/bold red] {e}")
            session.paradoxes.append(f"Event {event.index}: Crash - {e}")

    def _analyze_divergence(self, session: ReplaySession, event: TemporalEvent, result: ScaffoldResult,
                            console: Console):
        """
        [THE DIFFERENTIAL ENGINE]
        Compares the new reality with the expected outcome.
        """
        if result.success:
            console.print(f"✅ [bold green]Resurrection Successful[/bold green]")
            session.success_count += 1

            if not event.was_successful:  # If history failed but we succeeded
                console.print(
                    f"   ✨ [bold yellow]TIMELINE HEALED:[/bold yellow] This event failed in the past but succeeds now.")
        else:
            console.print(f"❌ [bold red]Resurrection Failed[/bold red]: {result.message}")
            session.failure_count += 1

            if event.was_successful:  # If history succeeded but we failed
                console.print(
                    f"   🔥 [bold red]TEMPORAL PARADOX:[/bold red] This event succeeded in the past but fails now. REGRESSION DETECTED.")
                session.paradoxes.append(f"Event {event.index} ({event.command}): Regression")

    def _forge_final_verdict(self, session: ReplaySession) -> ScaffoldResult:
        """
        [THE FINAL PROCLAMATION]
        Summarizes the time travel session.
        """
        msg = f"Replay Complete. {session.success_count} Successes, {session.failure_count} Failures."

        if session.paradoxes:
            msg += f" {len(session.paradoxes)} PARADOXES DETECTED."
            return self.partial_success(msg, [], data={"paradoxes": session.paradoxes})

        return self.success(msg)