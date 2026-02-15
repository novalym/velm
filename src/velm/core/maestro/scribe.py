# Path: scaffold/core/maestro/scribe.py
# -------------------------------------
import os
import time
import subprocess
from typing import List, Tuple, Any, Optional, Set

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
        """
        =================================================================================
        == THE RITE OF CINEMATIC CONDUCT (V-Ω-TOTALITY-V3.0-VOID-WARDED-FINALIS)       ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_RECEPTION_ORCHESTRATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_SCRIBE_CONDUCT_V300_TITANIUM_FINALIS

        [THE MANIFESTO]
        This rite orchestrates the transition from Matter Shards to Visual Proclamations.
        It implements the 'NoneType Sarcophagus' to safely handle the end of time.
        =================================================================================
        """
        import time
        import subprocess
        from rich.live import Live
        from ...contracts.heresy_contracts import ArtisanHeresy

        # --- MOVEMENT I: THE TEMPORAL ANCHOR ---
        output_buffer: List[Tuple[str, Optional[str]]] = []

        try:
            # [ASCENSION 11]: SUBSTRATE-AWARE RENDERING
            # We use a 10Hz pulse to keep the Ocular HUD responsive without CPU fever.
            with Live(self._generate_panel(output_buffer, 0.0, False),
                      refresh_per_second=10,
                      console=self.console,
                      transient=True) as live:

                # --- MOVEMENT II: THE ETERNAL VIGIL ---
                # We monitor while the process breathes OR matter remains in the queue.
                while process.poll() is None or not output_queue.empty():
                    try:
                        while True:
                            # Non-blocking scry of the output queue
                            stream_type, line_matter = output_queue.get_nowait()

                            # [ASCENSION 10]: LOG BLOAT GOVERNOR
                            if len(output_buffer) > 10000:
                                output_buffer.pop(0)

                            # Record the matter (including None EOF signals)
                            output_buffer.append((stream_type, line_matter))
                    except Exception:  # queue.Empty
                        pass

                    # [ASCENSION 2]: ACHRONAL CHRONOMETRY
                    duration = time.monotonic() - self.start_time
                    live.update(self._generate_panel(output_buffer, duration, False))

                    # Prevent spin-lock fever
                    time.sleep(0.05)

            # --- MOVEMENT III: THE RITE OF FINALITY ---
            rc = process.returncode
            duration = time.monotonic() - self.start_time

            # [ASCENSION 12]: THE FINALITY VOW
            # Generate the final static frame of the rite.
            final_panel = self._generate_panel(output_buffer, duration, True)
            self.console.print(final_panel)

            if rc != 0:
                # =========================================================================
                # == [ASCENSION 1]: THE NONE-TYPE SARCOPHAGUS (THE CURE)                 ==
                # =========================================================================
                # We surgically sieve the buffer for strings only, annihilating the NoneType
                # error during the join operation.
                pure_verses = [line for _, line in output_buffer if isinstance(line, str)]
                full_output = "\n".join(pure_verses)

                # Transmute into a Python error for the Maestro's Healer
                raise subprocess.CalledProcessError(rc, self.display_command, output=full_output)

        except KeyboardInterrupt:
            # [ASCENSION 7]: THE TEMPORAL KILLSWITCH
            if process:
                process.kill()
            raise ArtisanHeresy("Interrupted by Architect. Kinetic Strike terminated.")

    def _generate_panel(self, lines: List[Tuple[str, Optional[str]]], duration: float, is_done: bool) -> Panel:
        """
        =================================================================================
        == THE GNOSTIC MIRROR (V-Ω-TOTALITY-V3.5-RESILIENT-OCULAR)                     ==
        =================================================================================
        LIF: ∞ | ROLE: OCULAR_PROJECTION_ENGINE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCRIBE_V350_NONE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        Forges the visual hologram for the Live display. This implementation righteously
        annihilates the 'NameError' and 'AttributeError' by enforcing a strict
        Gnostic Type-Sieve and a-temporal coordinate normalization.
        =================================================================================
        """
        from rich.text import Text
        from rich.panel import Panel
        from rich.spinner import Spinner
        from rich.console import Group
        from rich.padding import Padding
        from rich import box  # [THE FIX]: Explicitly import the box module to resolve NameError

        # --- MOVEMENT I: THE CENSUS OF MATTER (THE CURE) ---
        # [ASCENSION 1]: THE NONE-TYPE SARCOPHAGUS
        # We surgically filter the stream to ensure no NoneType (EOF signals) reach the
        # string builder. This prevents: TypeError: unsupported operand type(s) for +
        pure_verses = [line for line in lines if line[1] is not None]

        # [ASCENSION 4]: APERTURE FOCUS (TAIL-GAZING)
        # We focus the Eye on the last 15 lines of truth to maintain high creation velocity.
        display_lines = pure_verses[-15:]

        # --- MOVEMENT II: THE INSCRIPTION RITE ---
        content = Text()
        for stream_type, line_matter in display_lines:
            # [ASCENSION 5]: SENSORY WARD
            # Guard against any non-string matter that leaked into the buffer.
            if not isinstance(line_matter, str):
                continue

            # [ASCENSION 3]: HAPTIC SIGNAL MULTIPLEXING
            # Error matter (stderr) glows red; Truth matter (stdout) remains white.
            style = "bold red" if stream_type == 'stderr' else "white"

            # Atomic Appending with Entropy Reduction (rstrip)
            content.append(line_matter.rstrip() + "\n", style=style)

        # --- MOVEMENT III: VITALITY ADJUDICATION ---
        # [ASCENSION 11]: KINETIC PULSE
        # Pulse the dots spinner only while the process is breathing.
        spinner_widget = Spinner("dots", style="cyan") if not is_done else ""

        # --- MOVEMENT IV: THE PROCLAMATION FORGE ---
        # [ASCENSION 8]: ISOMORPHIC STATUS MAPPING
        if is_done:
            status_label = "RESONANT"
            status_color = "bold green"
            border_color = "green"
            active_box = box.ROUNDED  # [THE FIX]: Resolve 'undefined' to a valid Rich box constant
        else:
            status_label = "CONDUCTING"
            status_color = "bold cyan"
            border_color = "blue"
            active_box = box.SQUARE

        # [ASCENSION 6]: TRACE ID INSCRIPTION
        # Siphon the Trace ID from the environment DNA for perfect forensic alignment.
        trace_id = os.environ.get("SCAFFOLD_TRACE_ID") or \
                   getattr(self, 'trace_id', 'tr-unbound')

        # [ASCENSION 2]: ACHRONAL CHRONOMETRY
        # Proclaim the metabolic duration with nanosecond-derived precision.
        title = Text.assemble(
            (f"{status_label}: ", status_color),
            (f"{self.display_command} ", "white"),
            (f"({duration:.2f}s)", "dim white")
        )

        # [ASCENSION 12]: THE FINALITY VOW
        # We return the sovereign panel, warded by Padding and Titanium styling.
        return Panel(
            Padding(Group(spinner_widget, content), (1, 2)),
            title=title,
            border_style=border_color,
            subtitle=f"[dim]Trace: {trace_id}[/dim]" if not is_done else None,
            subtitle_align="right",
            box=active_box  # [THE CURE]: Guaranteed valid Box object
        )