# Path: scaffold/core/maestro/scribe.py
# -------------------------------------

import time
import subprocess
from typing import List, Tuple, Any

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from ...logger import get_console
from ...contracts.heresy_contracts import ArtisanHeresy


class CinematicScribe:
    """
    [FACULTY 6] The Luminous Scribe.
    Orchestrates the `rich.Live` context to render the cinematic symphony of a
    running command. It receives raw output lines via a queue and transmutes them
    into a beautiful, ever-updating panel.
    """

    def __init__(self, display_command: str, console: Any):
        self.display_command = display_command
        self.console = console
        self.start_time = time.monotonic()

    def conduct(self, process: subprocess.Popen, output_queue: Any):
        """The one true rite of cinematic proclamation."""
        output_buffer = []
        try:
            with Live(self._generate_panel(output_buffer, 0.0, False),
                      refresh_per_second=10,
                      console=self.console,
                      transient=True) as live:
                while process.poll() is None or not output_queue.empty():
                    try:
                        while True:
                            stream_type, line = output_queue.get_nowait()
                            output_buffer.append((stream_type, line))
                    except Exception: # queue.Empty
                        pass

                    duration = time.monotonic() - self.start_time
                    live.update(self._generate_panel(output_buffer, duration, False))
                    time.sleep(0.05)

            # Final state after process exit
            rc = process.returncode
            duration = time.monotonic() - self.start_time
            final_panel = self._generate_panel(output_buffer, duration, True)

            if rc == 0:
                final_panel.border_style = "green"
                final_panel.title = Text.assemble(
                    ("✔ Rite Complete ", "bold green"), (f"({duration:.2f}s)", "dim")
                )
                self.console.print(final_panel)
            else:
                final_panel.border_style = "red"
                final_panel.title = Text.assemble(
                    ("✘ Rite Failed ", "bold red"), (f"(Exit {rc})", "white on red")
                )
                self.console.print(final_panel)
                full_output = "\n".join([line for _, line in output_buffer])
                raise subprocess.CalledProcessError(rc, self.display_command, output=full_output)

        except KeyboardInterrupt:
            process.kill()
            raise ArtisanHeresy("Interrupted by Architect. Child process terminated.")

    def _generate_panel(self, lines: List[Tuple[str, str]], duration: float, is_done: bool) -> Panel:
        """Forges the rich Panel for the Live display."""
        display_lines = lines[-12:] # Keep the UI snappy
        content = Text()
        for stream_type, line in display_lines:
            style = "bold red" if stream_type == 'stderr' else "white"
            content.append(line + "\n", style=style)

        spinner_widget = Spinner("dots") if not is_done else ""

        status_text = "Conducting" if not is_done else "Finished"
        title = Text.assemble(
            (f"{status_text}: {self.display_command} ", "bold cyan"),
            (f"({duration:.1f}s)", "dim white")
        )
        return Panel(Group(spinner_widget, content), title=title, border_style="blue")