# Path: scaffold/symphony/conductor_core/handlers/parallel_handler.py
# -------------------------------------------------------------------
from .base import BaseHandler
from ...swarm import SwarmOrchestrator
from ....contracts.symphony_contracts import Edict


class ParallelHandler(BaseHandler):
    """
    =================================================================================
    == THE LORD OF THE SWARM (V-Ω-CONCURRENCY)                                     ==
    =================================================================================
    Handles `&&` and `parallel:` blocks.
    """

    def execute(self, edict: Edict):
        """The Weaver of Multiverses."""
        workers = 4
        fail_fast = False

        # Parse args like parallel(workers=4, fail_fast=true)
        for arg in edict.directive_args:
            if '=' in arg:
                key, val = arg.split('=', 1)
                if key == 'workers':
                    workers = int(val)
                elif key == 'fail_fast':
                    fail_fast = (val.lower() == 'true')

        # Summon the Swarm Orchestrator
        # Note: SwarmOrchestrator takes the *conductor*, not the handler.
        swarm = SwarmOrchestrator(
            conductor=self.conductor,
            edicts=edict.parallel_edicts,
            workers=workers,
            fail_fast=fail_fast
        )
        swarm.conduct()