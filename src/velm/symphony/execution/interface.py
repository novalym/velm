# Path: scaffold/symphony/execution/interface.py
# ----------------------------------------------

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Any, Union, List, Optional, Dict
from rich.text import Text
from ...contracts.symphony_contracts import Edict, ActionResult


class KineticInterface(ABC):
    """
    =================================================================================
    == THE SACRED CONTRACT OF KINETIC WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)       ==
    =================================================================================
    @gnosis:title The Kinetic Interface (The Unbreakable Vow of Action)
    @gnosis:summary The divine, abstract soul of all kinetic artisans, its contract now
                     reforged to command the new, Gnostically-aware Kinetic Titan.
    @gnosis:LIF 10,000,000,000,000

    This is the unbreakable Gnostic contract for all artisans that perform kinetic rites.
    It has been ascended to its final, eternal form, shattering the ancient laws that bound
    it to the profane, untransmuted `edict`. It is the pure, Gnostic scripture of will.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Unbreakable Plea (THE FINAL FIX):** The `perform` rite's contract has been
        reforged. It now demands the pure, final, transmuted `command` string as its
        primary Gnosis, annihilating the `TypeError` heresy for all time.

    2.  **The Chronomancer's Ward:** The contract now includes a `timeout` vow, bestowing
        upon all kinetic rites the power to guard against eternal, hanging processes.

    3.  **The Gnostic Environment Alchemist:** The contract now accepts `env_overrides`,
        allowing for the surgical injection of Gnostic context into a child process's soul.

    4.  **The Sandbox Prophecy:** The contract now accepts a `permissions` vessel, a sacred
        prophecy for a future ascension where the Titan can forge sandboxed realities.

    5.  **The Pure Gnostic Contract:** As an `ABC`, its vows remain unbreakable. Any future
        kinetic artisan *must* honor this new, more powerful contract.

    6.  **The Unbreakable Vow of Return:** It continues to vow that it will always return a
        pure `ActionResult` vessel, providing a consistent chronicle of reality.

    7.  **The Luminous Scripture:** Its documentation has been ascended to reflect the new,
        richer parameters, mentoring future architects on how to commune with it.

    8.  **The Sovereign Soul:** Its soul remains abstract. It defines *what* must be done,
        not *how*, preserving the architectural purity of its adherents.

    9.  **The Gnostic Triage of Voice:** The `verbose_ui` vow remains, preserving the bridge
        to the cinematic renderers and honoring the need for both silent and luminous rites.

    10. **The Conduit of Souls:** The `inputs` vow remains, ensuring the `stdin` of a process
        can always be fed with Gnosis.

    11. **The Unbreakable Return Code Gaze:** The `get_last_return_code` vow is preserved,
        its vessel now a pure `Optional[int]` for greater type safety.

    12. **The Final Word:** This is the apotheosis of the kinetic contract. The schism is healed.
        The architecture is eternal.
    =================================================================================
    """

    @abstractmethod
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
        Executes the final, transmuted command within the Sanctum.

        Args:
            command: The pure, final, Gnostically-transmuted command string to execute.
            edict: The original vessel of will, for metadata and context (e.g., `capture_as`).
            sanctum: The directory where the rite is conducted.
            inputs: A list of strings to inject into the process's soul (stdin).
            live_context: The UI context passed back to the callback.
            stream_callback: The function to invoke for every line of output.
            verbose_ui: If True, summons the Cinematic Dashboard.
            timeout: An optional timeout in seconds for the rite.
            env_overrides: A dictionary of environment variables to inject.
            permissions: A dictionary defining sandboxing rules (a future prophecy).

        Returns:
            ActionResult: The crystallized outcome of the rite.
        """
        pass

    @abstractmethod
    def get_last_return_code(self) -> Optional[int]:
        """Returns the exit code of the most recent rite, or None if no rite was run."""
        pass