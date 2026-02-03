# Path: scaffold/symphony/swarm.py
# --------------------------------

import concurrent.futures
import json
import random
import re
import shutil
import threading
import time
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any, Set

# --- THE DIVINE SUMMONS OF THE LUMINOUS SCRIBE ---
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.style import Style
from rich.table import Table
from rich.text import Text

# --- THE GNOSTIC CONTRACTS ---
from ..contracts.heresy_contracts import ArtisanHeresy
from ..contracts.symphony_contracts import Edict
from ..core.runtime.remote import RemoteEngine
from ..logger import Scribe

Logger = Scribe("SwarmOrchestrator")

# --- CONSTANTS OF THE HIVE ---
MAX_RETRIES = 2
ANSI_ESCAPE_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


@dataclass
class DroneState:
    """
    =============================================================================
    == THE SOUL OF THE DRONE (V-Ω-STATE-VESSEL-ASCENDED)                       ==
    =============================================================================
    Holds the living, mutable state of a single parallel worker.
    """
    id: str
    name: str
    command: str
    status: str = "PENDING"  # PENDING, RUNNING, RETRYING, SUCCESS, FAILURE, ABORTED
    exit_code: Optional[int] = None
    start_time: float = 0.0
    end_time: float = 0.0
    log_path: Optional[Path] = None
    retry_count: int = 0

    # [ELEVATION 9] The Memory Guard (Circular Buffer for UI)
    live_buffer: deque = field(default_factory=lambda: deque(maxlen=20))
    total_lines: int = 0

    # [ELEVATION 8] Artifact Harvester
    artifacts: List[str] = field(default_factory=list)

    @property
    def duration(self) -> float:
        if self.start_time == 0.0: return 0.0
        end = self.end_time if self.end_time > 0 else time.time()
        return end - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the soul for the Neural Link."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "duration": self.duration,
            "retry_count": self.retry_count,
            "total_lines": self.total_lines
        }


class SwarmOrchestrator:
    """
    =================================================================================
    == THE GNOSTIC SWARM (V-Ω-CONCURRENT-DASHBOARD-ULTIMA)                         ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The God-Engine of Parallel Execution. It orchestrates a fleet of Drones,
    visualizes their thoughts in a TUI, broadcasts telemetry via the Neural Link,
    and chronicles their lives to disk.
    """

    def __init__(
            self,
            conductor: Any,
            edicts: List[Edict],
            workers: int = 4,
            fail_fast: bool = False
    ):
        self.conductor = conductor
        self.edicts = edicts
        self.max_workers = workers
        self.fail_fast = fail_fast

        # [ELEVATION 2] The Forensic Black Box Directory
        self.swarm_id = f"swarm_{int(time.time())}"
        self.log_dir = self.conductor.project_root / ".scaffold" / "logs" / "swarm" / self.swarm_id
        self.state_file = self.log_dir / "swarm_state.json"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # State Management
        self.drones: List[DroneState] = []
        self._abort_event = threading.Event()
        self._lock = threading.Lock()
        self.active_drone_idx: int = 0
        self.start_time: float = 0.0

        # Initialize Drones
        self._consecrate_drones()

    def _consecrate_drones(self):
        """Forges the souls of the drones before the rite begins."""
        for i, edict in enumerate(self.edicts):
            # Generate a clean filename for the log
            safe_cmd = "".join(c if c.isalnum() else "_" for c in edict.command[:30])
            log_file = self.log_dir / f"drone_{i + 1:02d}_{safe_cmd}.log"

            drone = DroneState(
                id=f"D{i + 1}",
                name=f"Drone-{i + 1}",
                command=edict.command,
                log_path=log_file
            )
            self.drones.append(drone)

    def _broadcast_pulse(self, event_type: str, payload: Dict[str, Any]):
        """
        [ELEVATION 1] THE NEURAL PULSE.
        Emits a structured signal to the Gnostic Daemon via the Scribe.
        This data is hidden from the CLI user but visible to the IDE via the Neural Link.
        """
        Logger.info(
            f"Swarm Pulse: {event_type}",
            tags=["NEURAL_LINK"],
            extra_payload={
                "type": event_type,
                "swarm_id": self.swarm_id,
                "timestamp": time.time(),
                **payload
            }
        )

    def _persist_state(self):
        """[ELEVATION 4] The State Persister."""
        try:
            data = {
                "id": self.swarm_id,
                "start_time": self.start_time,
                "drones": [d.to_dict() for d in self.drones]
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass  # Do not halt the swarm for a scribe's error

    def conduct(self) -> None:
        """
        THE GRAND RITE OF PARALLEL EXECUTION.
        Launches the TUI, the ThreadPool, and the Neural Link.
        """
        self.start_time = time.time()
        Logger.info(f"Awakening Gnostic Swarm ({len(self.drones)} drones, {self.max_workers} threads)...")
        Logger.info(f"Forensic Sanctum: [dim]{self.log_dir}[/dim]")

        # [NEURAL LINK] Signal Start
        self._broadcast_pulse("swarm_start", {
            "drone_count": len(self.drones),
            "drones": [{"id": d.id, "name": d.name, "command": d.command} for d in self.drones]
        })

        layout = self._forge_layout()

        # [ELEVATION 1] The Luminous Dashboard Context
        # We use transient=True so the dashboard disappears upon completion, replaced by the Summary.
        with Live(layout, refresh_per_second=10, screen=True, transient=True) as live:
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {}

                    # Launch Drones
                    for i, drone in enumerate(self.drones):
                        if self._abort_event.is_set(): break

                        # [ELEVATION 3] The Staggered Awakening
                        # Prevents "Thundering Herd" on the CPU/Network
                        time.sleep(0.1)

                        # Submit the Rite
                        future = executor.submit(self._execute_drone_rite, i)
                        futures[future] = i

                    # Monitor Loop
                    while futures:
                        # Check for completed futures non-blocking
                        done, not_done = concurrent.futures.wait(
                            futures.keys(),
                            timeout=0.1,
                            return_when=concurrent.futures.FIRST_COMPLETED
                        )

                        for f in done:
                            idx = futures.pop(f)
                            try:
                                f.result()  # Check for exceptions in the thread
                            except Exception as e:
                                self._record_drone_failure(self.drones[idx], e)
                                if self.fail_fast:
                                    self._abort_event.set()
                                    # Cancel pending
                                    for pending in not_done: pending.cancel()

                        # Update TUI
                        live.update(self._render_layout(layout))

                        # [NEURAL LINK] Broadcast Heartbeat (Throttled)
                        if int(time.time() * 10) % 5 == 0:  # Every 0.5s
                            self._broadcast_pulse("swarm_tick", {
                                "drones": [d.to_dict() for d in self.drones]
                            })
                            self._persist_state()

                        if self._abort_event.is_set() and not futures:
                            break

            except KeyboardInterrupt:
                # [ELEVATION 8] The Unbreakable Loop
                self._abort_event.set()
                Logger.warn("Architect's Will: Aborting Swarm...")
                # The Live context will exit, but we must ensure threads die.
                # Python threads cannot be killed, but the _abort_event will stop their loops.

        # [ELEVATION 10] The Gnostic Summary
        self._proclaim_summary()

        # [NEURAL LINK] Signal Completion
        failures = [d for d in self.drones if d.status == "FAILURE"]
        self._broadcast_pulse("swarm_end", {
            "success": not bool(failures),
            "duration": time.time() - self.start_time
        })

        # Final Adjudication
        if failures:
            raise ArtisanHeresy(
                f"The Swarm faltered. {len(failures)} drone(s) failed.",
                details=f"See logs in: {self.log_dir}"
            )

    def _execute_drone_rite(self, index: int):
        """
        The Atomic Rite for a single thread.
        Handles Retries, Output Capture, and Neural Updates.
        """
        if self._abort_event.is_set(): return

        drone = self.drones[index]
        edict = self.edicts[index]

        # [ELEVATION 12] Gnostic Context Injection
        # We create a unique environment context for this drone
        drone_context = {
            "SC_SWARM_ID": self.swarm_id,
            "SC_DRONE_ID": drone.id,
            "SC_DRONE_INDEX": str(index)
        }
        # We merge this into the conductor's context if possible,
        # or rely on the RemoteEngine to accept it.
        # For now, we assume the conductor handles variable expansion before this point,
        # or we rely on the environment variables if it's a local run.

        drone.status = "RUNNING"
        drone.start_time = time.time()
        self._broadcast_pulse("drone_update", drone.to_dict())

        # Open the Forensic Black Box
        with open(drone.log_path, "w", encoding="utf-8") as log_file:

            def _scribe_callback(content: str):
                """The Telepathic Bridge Callback."""
                if self._abort_event.is_set(): return

                # [ELEVATION 6] ANSI Purifier
                # We keep ANSI for the live buffer (rich supports it)
                # But strip it for the log file
                clean_ansi = content.rstrip()
                clean_text = ANSI_ESCAPE_REGEX.sub('', clean_ansi)

                if clean_ansi:
                    # 1. Write to Disk (Forensics)
                    log_file.write(clean_text + "\n")
                    log_file.flush()

                    # 2. Update UI Buffer (Memory Guard)
                    with self._lock:
                        drone.live_buffer.append(clean_ansi)
                        drone.total_lines += 1
                        drone.last_log = clean_text

                        # [ELEVATION 7] Interactive Focus
                        # If this drone speaks, and it is running, we might focus it
                        # (Heuristic: Focus on the most recent activity if errors appear)
                        if "error" in clean_text.lower():
                            self.active_drone_idx = index

            # [ELEVATION 2] The Quantum Retrier Loop
            attempt = 0
            while attempt <= MAX_RETRIES:
                try:
                    # [ELEVATION 5] Chaos Simulator (Dry Run)
                    if self.conductor.request.dry_run:
                        self._simulate_chaos(drone, _scribe_callback)
                        return

                    # Execute the Edict
                    if "scaffold" in edict.command and "--remote" in edict.command:
                        self._conduct_optimized_remote(edict.command, _scribe_callback)
                    else:
                        self.conductor._execute_action(edict, output_callback=_scribe_callback)

                    drone.status = "SUCCESS"
                    drone.exit_code = 0
                    self._broadcast_pulse("drone_update", drone.to_dict())
                    break  # Success, exit retry loop

                except Exception as e:
                    attempt += 1
                    _scribe_callback(f"[HERESY detected] {e}")

                    if attempt <= MAX_RETRIES:
                        drone.status = "RETRYING"
                        _scribe_callback(f"[QUANTUM RETRIER] Re-attempting rite ({attempt}/{MAX_RETRIES})...")
                        time.sleep(1 * attempt)  # Exponential backoff
                    else:
                        drone.status = "FAILURE"
                        drone.exit_code = 1
                        _scribe_callback(f"[CRITICAL FAILURE] Rite aborted after {MAX_RETRIES} retries.")
                        self._broadcast_pulse("drone_update", drone.to_dict())

                finally:
                    drone.end_time = time.time()

    def _simulate_chaos(self, drone: DroneState, scribe: Callable):
        """Simulates work with random failures for UI testing."""
        scribe("[SIMULATION] Connecting to quantum realm...")
        time.sleep(random.uniform(0.5, 2.0))
        scribe(f"[SIMULATION] Running: {drone.command}")

        for i in range(5):
            if self._abort_event.is_set(): return
            time.sleep(0.5)
            scribe(f"[SIMULATION] Step {i + 1}/5 complete. Entropy is stable.")

        # 10% chance of failure
        if random.random() < 0.1:
            raise Exception("Simulated Entropy Spike")

        scribe("[SIMULATION] Rite Complete.")
        drone.status = "SUCCESS"
        drone.end_time = time.time()

    def _conduct_optimized_remote(self, cmd_str: str, callback: Callable):
        """Directly summons the RemoteEngine to bypass CLI overhead."""
        import shlex
        parts = shlex.split(cmd_str)
        target = None;
        remote = None

        it = iter(parts)
        for arg in it:
            if arg == "run":
                target = next(it, None)
            elif arg == "--remote":
                remote = next(it, None)

        if target and remote:
            from ..interfaces.requests import RunRequest
            # Forge request
            req = RunRequest(target=target, remote=remote, project_root=self.conductor.project_root)

            # Summon Engine
            remote_engine = RemoteEngine(output_handler=callback)
            remote_engine.connect(remote)

            # Dispatch
            res = remote_engine.dispatch(req)
            if not res.success: raise Exception(res.message)
        else:
            raise ValueError("Invalid remote syntax for optimized execution")

    def _record_drone_failure(self, drone: DroneState, error: Exception):
        drone.status = "FAILURE"
        drone.end_time = time.time()
        self._broadcast_pulse("drone_update", drone.to_dict())
        with open(drone.log_path, "a") as f:
            f.write(f"\n[SWARM ABORT] {error}\n")

    # --- UI FORGING (THE LUMINOUS DASHBOARD) ---

    def _forge_layout(self) -> Layout:
        """Creates the Split-Pane UI."""
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["body"].split_row(
            Layout(name="swarm_table", ratio=2),
            Layout(name="focus_log", ratio=3)
        )
        return layout

    def _render_layout(self, layout: Layout) -> Layout:
        """Updates the UI components."""

        # 1. Header
        completed = sum(1 for d in self.drones if d.status in ("SUCCESS", "FAILURE"))
        running = sum(1 for d in self.drones if d.status == "RUNNING")
        failed = sum(1 for d in self.drones if d.status == "FAILURE")

        spinner = "🔥" if running > 0 else "✨"
        status_color = "magenta"
        if failed > 0:
            status_color = "red"
        elif completed == len(self.drones):
            status_color = "green"

        header_text = Text.assemble(
            (f"{spinner} THE GNOSTIC SWARM ", f"bold {status_color}"),
            (f"[{completed}/{len(self.drones)}] ", "bold cyan"),
            (f"Active: {running} ", "yellow"),
            (f"Failed: {failed} ", "red" if failed else "dim green"),
            (f"| Sanctum: {self.conductor.project_root.name}", "dim")
        )
        layout["header"].update(Panel(header_text, style=status_color))

        # 2. Swarm Table
        table = Table(expand=True, box=None, padding=(0, 1))
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Status", width=12)
        table.add_column("Command", style="white", ratio=1)
        table.add_column("Time", justify="right", width=8)

        for i, drone in enumerate(self.drones):
            s_style = "dim white"
            icon = "•"
            if drone.status == "RUNNING":
                s_style, icon = "bold yellow", "⚡"
            elif drone.status == "RETRYING":
                s_style, icon = "bold orange1", "⟳"
            elif drone.status == "SUCCESS":
                s_style, icon = "bold green", "✔"
            elif drone.status == "FAILURE":
                s_style, icon = "bold red", "✖"

            duration = f"{drone.duration:.1f}s"
            if drone.status == "PENDING": duration = "-"

            row_style = "reverse" if i == self.active_drone_idx else ""

            table.add_row(
                drone.id,
                Text(f"{icon} {drone.status}", style=s_style),
                Text(drone.command, overflow="ellipsis", no_wrap=True),
                duration,
                style=row_style
            )

        layout["swarm_table"].update(Panel(table, title="Drone Matrix", border_style="blue"))

        # 3. Focus Log
        active_drone = self.drones[self.active_drone_idx]
        log_text = Text()
        for line in active_drone.live_buffer:
            # We already stripped ANSI for file, but here we could keep it if we stored raw.
            # For now, simple text.
            log_text.append(line + "\n")

        layout["focus_log"].update(Panel(
            log_text,
            title=f"Neural Link: {active_drone.name}",
            subtitle=f"{active_drone.log_path.name} ({active_drone.total_lines} lines)",
            border_style="yellow"
        ))

        # 4. Footer (Global Progress)
        prog = Progress(
            SpinnerColumn(), BarColumn(bar_width=None, style="dim"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True
        )
        task_id = prog.add_task("", total=len(self.drones), completed=completed)
        layout["footer"].update(Panel(prog, style="dim", box=None))

        return layout

    def _proclaim_summary(self):
        """[ELEVATION 10] The Luminous Aggregate Report."""
        summary = Table(title="Gnostic Swarm Summary", box=None, show_lines=True)
        summary.add_column("Drone", style="cyan")
        summary.add_column("Result", style="bold")
        summary.add_column("Time", justify="right")
        summary.add_column("Retries", justify="center")
        summary.add_column("Artifact", style="dim")

        # [ELEVATION 9] Heatmap Chronometer Logic
        total_duration = sum(d.duration for d in self.drones)
        avg_duration = total_duration / len(self.drones) if self.drones else 0

        for drone in self.drones:
            res_style = "green" if drone.status == "SUCCESS" else "red"

            # Heatmap color for duration
            dur_style = "white"
            if drone.duration > avg_duration * 1.5: dur_style = "yellow"
            if drone.duration > avg_duration * 2.0: dur_style = "red"

            summary.add_row(
                drone.name,
                Text(drone.status, style=res_style),
                Text(f"{drone.duration:.2f}s", style=dur_style),
                str(drone.retry_count) if drone.retry_count > 0 else "-",
                str(drone.log_path.relative_to(self.conductor.project_root))
            )

        self.conductor.console.print(Panel(summary, border_style="green"))