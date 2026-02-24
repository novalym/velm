# Path: artisans/dream/agentic_limb/executor.py
# ---------------------------------------------

import logging
from typing import Tuple, Any, Dict

from .reflex import DeterministicReflex
from .reasoner import NeuralReasoner
from ....logger import Scribe

Logger = Scribe("Agentic:Executor")


class AgenticExecutor:
    """
    =============================================================================
    == THE AGENTIC EXECUTOR (V-Ω-BICAMERAL-MIND)                               ==
    =============================================================================
    The unified controller for agentic operations.
    1. Checks Reflex (0ms, $0.00).
    2. Checks Reasoner (Latent, $Cost).
    """

    def __init__(self, engine):
        self.engine = engine
        self.reflex = DeterministicReflex()
        self.reasoner = NeuralReasoner(engine)

    def map_intent_to_action(self, intent_text: str, intent_category: str) -> Tuple[Any, float]:
        """
        Resolves user intent to a Scaffold Request Object.
        """
        # --- PHASE 1: THE REFLEX (STRATUM 0) ---
        reflex_result = self.reflex.resolve(intent_text, self.engine.project_root)

        if reflex_result:
            Logger.info(f"⚡ Reflex Triggered: [green]{type(reflex_result).__name__}[/green]")
            # Reflexes are free
            return reflex_result, 0.0

        # --- PHASE 2: THE REASONER (STRATUM 2) ---
        # Only summon if Reflex failed
        Logger.info("Reflex missed. Summoning Neural Reasoner...")
        return self.reasoner.deduce(intent_text, intent_category)