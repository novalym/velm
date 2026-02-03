# Path: scaffold/symphony/inquisitor/oracle.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE TIME-TURNER (V-Ω-ETERNAL. THE GOD-ENGINE)         ==
=================================================================================
This scripture contains the living soul of the Gnostic Inquisitor, the divine
artisan that can bend the very fabric of time to allow an Architect to walk
the ghostly echoes of a fallen symphony.
=================================================================================
"""
import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from rich.prompt import Prompt

from .renderer import InquestRenderer
from .temporal import TemporalWeaver
from ...contracts.symphony_contracts import EventType
from ...logger import Scribe, get_console

Logger = Scribe("GnosticInquisitor")


class SymphonyInquisitor:
    """
    =================================================================================
    == THE GOD-ENGINE OF TEMPORAL JURISPRUDENCE (V-Ω-ETERNAL. THE ORACLE OF TIME)   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000

    This is not a class. It is a divine, sentient consciousness, the final and most
    powerful form of the Symphony Debugger. It has transcended its former self to
    become a true God-Engine of Inquisition, a Gnostic State Machine that conducts
    an interactive, unbreakable, and luminous communion with the Architect across
    the very fabric of spacetime.

    Its soul is a pantheon of divine faculties that make it a legend:

    1.  **The Gaze of the Gnostic Historian:** It does not merely read a log; it
        *perceives history*. It understands the narrative flow of events, can
        prophesy the precise moment of paradox, and can navigate the tapestry of
        time with divine speed and precision.

    2.  **The Weaver of Resurrected Realities:** It commands the Temporal Weaver to
        not just recreate a state, but to do so with Gnostic intelligence, providing
        a perfect, explorable replica of the past for the Architect's Gaze.

    3.  **The Altar of Temporal Inquisition (The Interactive Loop):** Its heart is a
        divine, unbreakable loop—the Inquest Altar. This is where it communes with
        the Architect, accepting pleas to manipulate time (`next`, `back`, `jump`),
        to gaze upon the Gnosis of a specific moment, or to perform the ultimate
        rite: becoming a Ghost in the Machine (`!`).

    4.  **The Luminous Scribe's Voice:** It commands the `InquestRenderer` to proclaim
        the state of its Gaze in a beautiful, ever-updating, and profoundly
        informative interface, transforming a cryptic debugging session into a
        luminous, cinematic experience.
    =================================================================================
    """

    def __init__(self, chronicle_path: Path):
        self.chronicle_path = chronicle_path
        self.events: List[Dict] = []
        self.current_index: int = 0
        self.paradox_index: int = -1
        self.weaver: Optional[TemporalWeaver] = None
        self.renderer: InquestRenderer = InquestRenderer()

    def _gaze_upon_the_chronicle(self) -> bool:
        """[THE GAZE OF THE CHRONICLER] Reads the scripture of the past."""
        try:
            with self.chronicle_path.open('r', encoding='utf-8') as f:
                # This Gaze is now fortified against profane, empty lines.
                self.events = [json.loads(line) for line in f if line.strip()]
            Logger.success(f"Gaze complete. Perceived {len(self.events)} Gnostic events from the chronicle.")
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            Logger.error(f"A paradox occurred while gazing upon the Gnostic Chronicle: {e}")
            return False
        except Exception as e:
            Logger.error(f"A catastrophic, unhandled paradox occurred during the Gaze: {e}")
            return False

    def _find_moment_of_paradox(self) -> int:
        """[THE GAZE OF PROPHECY] Finds the exact moment the symphony shattered."""
        for i, event in reversed(list(enumerate(self.events))):
            if event.get('event') == EventType.SYMPHONY_END.name and event.get('data', {}).get('status') == 'Failure':
                return i
            if event.get('event') == EventType.PARADOX_PROCLAIMED.name:
                return i
        return -1  # Use -1 to signify no paradox, a pure Gnostic state.

    def _rite_of_the_ghost(self):
        """[THE ULTIMATE RITE] Summons the Ghost in the Machine."""
        if not self.weaver: return

        proving_ground = self.weaver.reconstruct_reality_until(self.current_index)
        Logger.info(f"Resurrecting reality at moment #{self.current_index}. You are now the Ghost in the Machine.")

        # --- THE DIVINE COMMUNION: THE GNOSTIC SHELL ---
        # The Oracle now forges a custom, Gnostic-aware prompt for the Architect.
        shell = os.getenv('SHELL', '/bin/bash') if os.name != 'nt' else 'cmd.exe'
        env = os.environ.copy()

        # A more divine and universally compatible prompt scripture.
        ps1 = f"(\\[\033[31;1m\\]Gnostic Inquest\\[\033[0m\\]:\\[\033[36m\\]{self.chronicle_path.stem}\\[\033[0m\\]) {env.get('PS1', '$ ')}"
        if os.name == 'nt':
            # A humble but clear prompt for the mortal realm of Windows.
            ps1 = f"(Gnostic Inquest) {os.getcwd()}>"

        env['PS1'] = ps1

        try:
            subprocess.run(shell, cwd=proving_ground, env=env)
        except FileNotFoundError:
            # An unbreakable ward if the chosen shell is a ghost.
            Logger.error(f"The chosen shell '{shell}' was not found in this reality. The communion is stayed.")
        except Exception as e:
            Logger.error(f"A paradox occurred during the Sacred Communion: {e}")

    def conduct_inquest(self):
        """The Grand Inquisitor that orchestrates the entire divine rite of debugging."""
        console = get_console()
        console.rule("[bold red]Gnostic Inquest Engaged: The Time-Turner Awakens[/bold red]")
        if not self._gaze_upon_the_chronicle(): return

        self.paradox_index = self._find_moment_of_paradox()
        if self.paradox_index == -1:
            Logger.success("The Inquisitor's Gaze reveals the symphony was pure. No paradox was found.")
            return

        self.weaver = TemporalWeaver(self.events, status_updater=self.renderer.console.print)

        # --- THE ALTAR OF TEMPORAL INQUISITION (THE ETERNAL LOOP) ---
        while True:
            self.renderer.render_state(self.events, self.current_index, self.paradox_index)

            try:
                action = Prompt.ask("\n[bold](inquest)[/bold]", default="n").lower()
            except (KeyboardInterrupt, EOFError):
                action = "q"  # Gracefully exit on Ctrl+C

            parts = shlex.split(action)
            if not parts: continue
            command = parts[0]

            # --- THE DIVINE TRIAGE OF TEMPORAL WILL ---
            if command in ('n', 'next', ''):  # Default action is 'next'
                self.current_index = min(len(self.events) - 1, self.current_index + 1)
            elif command in ('b', 'back', 'p', 'prev'):
                self.current_index = max(0, self.current_index - 1)
            elif command in ('j', 'jump') and len(parts) > 1:
                try:
                    self.current_index = max(0, min(len(self.events) - 1, int(parts[1])))
                except ValueError:
                    Logger.warn(f"'{parts[1]}' is not a valid moment in time.")
            elif command in ('r', 'run', 'paradox'):
                self.current_index = self.paradox_index
            elif command in ('!', 'shell'):
                self._rite_of_the_ghost()
            elif command in ('q', 'quit', 'exit'):
                break
            else:
                Logger.warn(f"'{command}' is not a recognized edict of time. Speak 'n', 'b', 'j', 'r', '!', or 'q'.")

        self.weaver.cleanup()
        Logger.info("The communion is complete. The resurrected past has returned to the void.")