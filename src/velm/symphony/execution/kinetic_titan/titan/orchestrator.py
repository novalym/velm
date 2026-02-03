# Path: scaffold/symphony/execution/kinetic_titan/titan/orchestrator.py
# ---------------------------------------------------------------------

import queue
import time
import os
import signal
from pathlib import Path
from typing import List, Callable, Any, Union, Optional, Dict

from rich.text import Text

from ...interface import KineticInterface
from ..executor import TitanExecutor
from .....contracts.symphony_contracts import Edict, ActionResult
from .....contracts.heresy_contracts import ArtisanHeresy
from .....logger import Scribe, get_console
from .....core.alchemist import get_alchemist
from .state import TitanState
from .loops import LoopConductor

Logger = Scribe('KineticTitan')


class KineticTitan(KineticInterface):
    """
    =================================================================================
    == THE KINETIC TITAN (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)                 ==
    =================================================================================
    @gnosis:title The Kinetic Titan (The Unbreakable Hand of the Symphony)
    @gnosis:summary The divine, sentient, and sovereign artisan that forges a kinetic
                     reality from the Symphony's pure will. Its soul is now whole.
    @gnosis:LIF 10,000,000,000

    This is the God-Engine of Process Execution. It orchestrates the `TitanExecutor`
    (Physics), `TitanState` (Memory), and `LoopConductor` (Observation) to perform
    the one true Kinetic Rite.
    """

    def __init__(self):
        self.console = get_console()
        self._last_return_code: Optional[int] = None

    def get_last_return_code(self) -> Optional[int]:
        return self._last_return_code

    def _forge_gnostic_environment(self, context_overrides: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        [THE ENVIRONMENT ALCHEMIST]
        Merges system env with Gnostic overrides, ensuring all values are strings.
        """
        # Start with the living system environment
        env = os.environ.copy()

        # Inject the overrides if they exist
        if context_overrides:
            for k, v in context_overrides.items():
                env[k] = str(v)  # Enforce string type for OS compatibility

        return env

    def perform(
            self,
            command: str,
            edict: Edict,
            sanctum: Path,
            inputs: List[str],
            live_context: Any,
            stream_callback: Callable[[Any, Union[str, Text]], None],
            verbose_ui: bool = False,
            timeout: Optional[int] = None,
            env_overrides: Optional[Dict[str, str]] = None,
            permissions: Optional[Dict[str, Any]] = None
    ) -> ActionResult:
        """
        The Grand Rite of Kinetic Execution.
        """
        start_time = time.time()

        # 1. Consecrate the Sanctum
        abs_sanctum = sanctum.resolve()
        if not abs_sanctum.exists():
            abs_sanctum.mkdir(parents=True, exist_ok=True)

        # 2. Forge the State Vessel
        # We create the state to hold the memory of this rite.
        state = TitanState(
            command=command,
            start_time=start_time,
            pid=None  # Will be set after ignition
        )

        # 3. Forge the Gnostic Environment
        final_env = self._forge_gnostic_environment(env_overrides)

        # 4. Summon the Executor
        executor = TitanExecutor()

        # =========================================================================
        # == [THE FIX] THE RITE OF THE LIVING CONDUIT                          ==
        # =========================================================================
        # We forge the Queue explicitly here, in the Orchestrator's scope.
        output_queue = queue.Queue()

        # We bind it to the State immediately, healing the 'NoneType' heresy.
        state.attach_queue(output_queue)
        # =========================================================================

        try:
            # 5. Ignite the Process
            # We pass the queue to the executor so it can pour the stream into it.
            executor.ignite(
                command=command,
                inputs=inputs or [],
                cwd=abs_sanctum,
                env=final_env,
                output_queue=output_queue
            )

            # Record the Identity
            state.set_pid(executor.pid())

            # 6. Conduct the Symphony of Loops
            # We act as the bridge between the Executor's stream and the UI.
            # We pass the EXPLICIT `output_queue` variable to ensure validity.
            if verbose_ui:
                LoopConductor.conduct_cinematic(
                    executor=executor,
                    output_queue=output_queue,  # Explicitly passed
                    state=state,
                    stream_callback=stream_callback,
                    live_context=live_context,
                    sanctum=abs_sanctum,
                    console=self.console
                )
            else:
                LoopConductor.conduct_raw(
                    executor=executor,
                    output_queue=output_queue,  # Explicitly passed
                    state=state,
                    stream_callback=stream_callback,
                    live_context=live_context
                )

            # 7. Harvest the Result
            # The loop ends when the process dies and the queue is empty.
            # We now ask the executor for the final truth.
            return_code = executor.returncode()

            # If the process is somehow still alive (zombie), we force a check.
            if return_code is None:
                executor.wait(timeout=1.0)
                return_code = executor.returncode()

        except KeyboardInterrupt:
            Logger.warn("Architect interrupted the kinetic rite. Terminating...")
            executor.kill()
            return_code = 130  # Standard SIGINT exit code
            state.add_line(Text("Rite Aborted by Architect", style="bold red"))

        except Exception as e:
            Logger.error(f"Kinetic Paradox: {e}")
            executor.kill()
            return_code = -1
            state.add_line(Text(f"Internal Engine Error: {e}", style="bold red"))
            raise e  # Re-raise to let the Resilience Manager handle it if needed

        finally:
            # 8. Seal the State
            # Ensure we have a return code, default to -1 if something went catastrophically wrong
            final_rc = return_code if return_code is not None else -1
            self._last_return_code = final_rc
            state.finish(final_rc)

            # Log the final duration
            duration = state.duration()
            Logger.verbose(f"Rite concluded. RC: {final_rc}. Duration: {duration:.2f}s")

        # 9. Forge the Result Vessel
        # The ActionResult is the immutable record returned to the Symphony Engine.
        return ActionResult(
            output=state.get_full_text(),
            returncode=final_rc,
            duration=state.duration(),
            command=command,
            was_terminated=(final_rc == 130 or final_rc == -1)
        )