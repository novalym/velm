# Path: scaffold/symphony/conductor_core/handlers/action_handler/facade.py
# ------------------------------------------------------------------------

import time
from typing import Optional, Any

from ..base import BaseHandler
from .....contracts.symphony_contracts import Edict, ActionResult
from .dispatcher import ActionDispatcher


class ActionHandler(BaseHandler):
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR OF KINETIC REALITY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)  ==
    =================================================================================
    @gnosis:title The Action Handler (The Unbreakable Hand)
    @gnosis:summary The divine facade for the modular Action Engine, its soul now whole,
                     its Gnostic contracts unbreakable and eternally pure.
    @gnosis:LIF 10,000,000

    This is the High Priest of Kinetic Will in its final, eternal, and most glorious
    form. It is a pure Conductor that orchestrates the symphony of UI lifecycle management
    and the delegation of kinetic will to the `ActionDispatcher`. It has been reforged
    with a pantheon of 12 legendary ascensions that annihilate all known paradoxes of
    Gnostic context and causality.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Anointment (THE FINAL FIX):** The heresy is annihilated. The facade
        now explicitly bestows the `live_context` upon the `ActionDispatcher` during
        the dispatch rite, ensuring the Gnostic context is never fractured.

    2.  **The Law of the Pure Contract:** Its `dispatcher.dispatch` plea now honors the
        ascended contract, providing both the `edict` and the `live_context` as
        separate, pure vessels of Gnosis.

    3.  **The Sovereign Soul:** Its purpose is pure orchestration. It manages the UI's
        `live_context` and the rite's telemetry (`duration`), but delegates the
        complexities of execution to the `ActionDispatcher`.

    4.  **The Unbreakable Ward of Paradox:** The entire `execute` symphony is shielded.
        Any heresy from the dispatcher or its children is caught and re-proclaimed,
        preserving the causal chain.

    5.  **The Gnostic Bridge to the Renderer:** Its communion with `self.renderer.live_context`
        remains the one true gateway to the UI's soul.

    6.  **The Chronomancer's Hand:** It is the one true master of time for the action rite,
        calculating and inscribing the final `duration` upon the `ActionResult`.

    7.  **The Heresy Funnel:** It acts as the final, unbreakable funnel, ensuring any
        paradox is passed up to the `ResilienceManager` for adjudication.

    8.  **The Final Proclamation:** Its `execute` rite returns the pure, final, and
        telemetrically complete `ActionResult`, the one true chronicle of the rite.

    9.  **The Luminous Voice:** Its proclamation of the edict's initiation provides a
        clear, Gnostic audit trail in the Symphony's log.

    10. **The Unbreakable Contract of Inheritance:** It perfectly honors its vows to the
        `BaseHandler`, ensuring its place in the Gnostic hierarchy is eternal.

    11. **The Lazily Forged Dispatcher:** The `ActionDispatcher` is forged at the moment
        of the handler's birth, its soul forever bound to this facade.

    12. **The Final Word:** This is the apotheosis of the Action Handler. Its mind is whole.
        Its contracts are pure. The Symphony is unbreakable.
    =================================================================================
    """

    def __init__(self, conductor, engine, performer, resilience_manager, context_manager):
        super().__init__(conductor, engine, performer, resilience_manager, context_manager)
        self.live_context: Optional[Any] = None
        self.dispatcher = ActionDispatcher(self)

    def execute(self, edict: Edict) -> Optional[ActionResult]:
        """The Grand Rite of Kinetic Execution."""
        start_time = time.time()
        self.logger.info(f"Executing Action Edict (L{edict.line_num}): [cyan]{edict.command}[/cyan]")

        result: Optional[ActionResult] = None
        try:
            # [FACULTY 1] The Gnostic Bridge to the Renderer's Soul
            with self.renderer.live_context(edict.line_num, edict.raw_scripture) as live_context:
                # The live_context is the UI's internal handle for this specific edict's visualization.
                self.live_context = live_context

                # =====================================================================
                # ==           THE DIVINE HEALING: THE GNOSTIC ANOINTMENT            ==
                # =====================================================================
                # The heresy is annihilated. We now explicitly bestow the Gnosis of
                # the `live_context` upon the Dispatcher, purifying the Gnostic flow
                # and healing the broken contract that caused the 'int is not callable'
                # paradox. The Dispatcher will now hold the one true context.
                result = self.dispatcher.dispatch(edict, live_context)
                # =====================================================================
                # ==                        THE APOTHEOSIS IS COMPLETE               ==
                # =====================================================================

                # [FACULTY 6] The Chronomancer's Hand
                # The result is now the single source of truth for duration
                if result:
                    result.duration = time.time() - start_time

        except Exception as e:
            # [FACULTY 7] The Heresy Funnel
            # If a crash occurs, we re-raise for the ResilienceManager
            raise e

        finally:
            # This block ALWAYS runs, guaranteeing the UI is cleaned up.
            if 'result' in locals() and result:
                # We update the renderer with the final state of the action.
                self.renderer.render_action_epilogue(self.live_context, result)

        return result