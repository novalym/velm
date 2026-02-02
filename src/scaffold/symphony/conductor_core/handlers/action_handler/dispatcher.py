# Path: scaffold/symphony/conductor_core/handlers/action_handler/dispatcher.py
# ----------------------------------------------------------------------------

import time
from typing import Dict, Type, Optional, Any

from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import Edict, EdictType, ActionResult
from .....logger import Scribe
from .contracts import ActionSpecialist
from .specialists.kinetic import KineticRite
from .specialists.polyglot import PolyglotRite
from .specialists.network import NetworkSpecialist
from .specialists.interactive import InteractiveSpecialist
from .specialists.service import ServiceSpecialist

Logger = Scribe('ActionRouter')


class ActionDispatcher:
    """
    =================================================================================
    == THE KINETIC ROUTER (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                        ==
    =================================================================================
    @gnosis:title The Kinetic Router (The Gnostic Triage Engine)
    @gnosis:summary The divine, sentient, and unbreakable router of the Kinetic Sanctum,
                     its Gnostic contracts now eternally pure and its mind whole.
    @gnosis:LIF 10,000,000,000

    This is the Immutable Router of the Kinetic Sanctum in its final, eternal form. It
    performs a flawless Gnostic Triage of the Edict's soul to determine the one true
    Specialist responsible for its execution. It has been reforged with a pantheon of
    12 legendary ascensions that make it the unbreakable heart of the Action Handler.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Law of the Pure Contract (THE FINAL FIX):** The ancient, profane contract
        is shattered. Its `dispatch` rite now accepts the `live_context` as a sacred,
        separate vessel of Gnosis, honoring the new vow from the `ActionHandler` facade.

    2.  **The Pantheon Forge:** Its `__init__` rite is now a forge. It pre-instantiates
        the entire pantheon of specialists, ensuring zero-latency dispatch and
        annihilating the heresy of repeated object creation.

    3.  **The Gnostic Anointment:** It now righteously anoints every specialist it forges
        with the one true `handler` (the `ActionHandler` facade), ensuring every priest
        in its pantheon has a direct, unbreakable link to the Symphony's core Gnosis.

    4.  **The Alchemical Pre-Flight:** It transmutes the `edict.command` with the
        Alchemist *before* dispatching, ensuring all Gnostic variables are resolved into
        their final, kinetic truth.

    5.  **The Void Shield:** An unbreakable ward intercepts `None` returns from specialists
        and transmutes them into a valid `ActionResult`, preventing type heresies from
        shattering the Conductor.

    6.  **The Semantic Diviner:** Its `_divine_specialist` rite scans command strings for
        semantic prefixes (`@kill_port`, `@ask`) to route specialized rites without
        needing explicit `EdictType` Gnosis.

    7.  **The Fallback Guardian:** It defaults safely to the `KineticRite` (Shell) if no
        higher Gnostic order is perceived in the edict's soul.

    8.  **The Heresy Container:** It wraps any dispatch-level paradox in a luminous
        `ArtisanHeresy`, preserving the full causal chain for forensic inquest.

    9.  **The Luminous Trace:** It proclaims the exact routing decision to the Gnostic
        Chronicle, providing a perfect audit trail for debugging.

    10. **The Unbreakable Contract of Return:** Its `dispatch` rite makes an unbreakable vow
        to always return a pure `ActionResult`, its contract with the `ActionHandler` facade
        now eternal and absolute.

    11. **The Sovereign Soul:** Its purpose is pure Triage and Delegation. It contains no
        kinetic or UI logic itself, its every action a testament to architectural purity.

    12. **The Final Word:** This is the apotheosis of the Action Dispatcher. Its Gnostic
        flow is pure. Its contracts are unbreakable. The Symphony is healed.
    =================================================================================
    """

    def __init__(self, handler: Any):
        self.handler = handler
        self.logger = handler.logger

        # [FACULTY 2 & 3] The Pantheon Forge & The Gnostic Anointment
        # We pre-instantiate all specialists, anointing them with the true handler.
        self.specialist_pantheon: Dict[str, ActionSpecialist] = {
            "polyglot": PolyglotRite(self.handler),
            "interactive": InteractiveSpecialist(self.handler),
            "service": ServiceSpecialist(self.handler),
            "network": NetworkSpecialist(self.handler),
            "kinetic": KineticRite(self.handler),  # The fallback
        }
        self.logger.verbose("Kinetic Router has forged its Pantheon of Specialists.")

    def dispatch(self, edict: Edict, live_context: Any) -> ActionResult:
        """
        [THE GNOSTIC TRIAGE - ASCENDED]
        Routes the edict to the correct specialist, now honoring the pure contract.
        """
        start_time = time.time()

        try:
            # [FACULTY 4] The Alchemical Pre-Flight
            command = edict.command or ""
            if '{{' in command or '{%' in command:
                command = self.handler.alchemist.transmute(command, self.handler.variables)

            # [FACULTY 6] The Semantic Diviner
            specialist = self._divine_specialist(edict, command)

            # [FACULTY 9] The Luminous Trace
            self.logger.verbose(f"Dispatching Edict L{edict.line_num} to [cyan]{specialist.__class__.__name__}[/cyan]")

            # The Execution
            result = specialist.conduct(edict, command)

            # [FACULTY 5] The Void Shield
            if result is None:
                result = self._forge_synthetic_result(command, time.time() - start_time)

            return result

        except Exception as e:
            # [FACULTY 8] The Heresy Container
            if isinstance(e, ArtisanHeresy):
                raise e
            raise ArtisanHeresy(
                f"Dispatch Paradox: {e}",
                details=str(e),
                line_num=edict.line_num,
                child_heresy=e
            )

    def _divine_specialist(self, edict: Edict, command: str) -> ActionSpecialist:
        """Divines the correct specialist based on Edict metadata and Command semantics."""

        # Gaze 1: The Soul of the Edict (Explicit Type)
        if edict.type == EdictType.POLYGLOT_ACTION:
            return self.specialist_pantheon["polyglot"]
        if edict.interactive_prompt:
            return self.specialist_pantheon["interactive"]
        if edict.service_config:
            return self.specialist_pantheon["service"]

        # Gaze 2: The Form of the Command (Semantic Prefixes)
        if command.startswith(("@ask", "@choose", "@confirm")):
            return self.specialist_pantheon["interactive"]
        if command.startswith("@service"):
            return self.specialist_pantheon["service"]
        if command.startswith(("@kill_port", "@await_webhook")):
            return self.specialist_pantheon["network"]

        # Gaze 3: The Default Path (The Kinetic Rite)
        return self.specialist_pantheon["kinetic"]

    def _forge_synthetic_result(self, command: str, duration: float) -> ActionResult:
        """Forges a placeholder result for void operations."""
        return ActionResult(
            output="",
            returncode=0,
            duration=duration,
            command=command,
            was_terminated=False
        )