# artisans/dream/agentic_limb/reflex/engine.py
# --------------------------------------------
import time
from pathlib import Path
from typing import Optional, Any
from .....logger import Scribe

from .tokenizer import GnosticTokenizer
from .phalanxes import IntentPhalanx

Logger = Scribe("Agentic:Reflex")


class DeterministicReflex:
    """
    =============================================================================
    == THE OMEGA REFLEX ENGINE (V-Ω-STRATUM-0-OMNISCIENT)                      ==
    =============================================================================
    LIF: ∞ | ROLE: ZERO_COST_ROUTER | RANK: OMEGA_SOVEREIGN

    The Brainstem of the God-Engine. It processes natural language algorithmically,
    achieving LLM-like routing without the metabolic tax or memory footprint of PyTorch.
    It is 100% WASM/Pyodide safe.
    """

    def __init__(self):
        self.tokenizer = GnosticTokenizer()

    def resolve(self, intent_text: str, root: Path) -> Optional[Any]:
        """
        The Rite of Algorithmic Mapping.
        Transforms human poetry into rigid Request Vessels.
        """
        start_ns = time.perf_counter_ns()

        # 1. The Void Check
        if not intent_text.strip():
            return None

        # 2. Tokenization, Stemming, and Extraction
        lexical_intent = self.tokenizer.analyze(intent_text)

        # 3. Phalanx Routing
        request_vessel = IntentPhalanx.route(lexical_intent)

        # 4. Metabolic Audit & Logging
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if request_vessel:
            Logger.info(f"⚡ Reflex Engaged: Mapped to [cyan]{type(request_vessel).__name__}[/] "
                        f"(Conf: {lexical_intent.confidence:.2f}) in {duration_ms:.2f}ms")

            # Log willed flags
            if lexical_intent.flags.get("dry_run"):
                Logger.verbose("   -> Gnosis: Dry-Run Mode Active")
            if lexical_intent.flags.get("force"):
                Logger.verbose("   -> Gnosis: Absolute Will (Force) Active")
            if lexical_intent.flags.get("adrenaline_mode"):
                Logger.verbose("   -> Gnosis: Adrenaline Injection Active")

            return request_vessel

        # If confidence was too low, or if it was a Socratic Question, we yield to the LLM.
        Logger.verbose(f"Reflex yielded. Intent too complex for algorithmic matrix. ({duration_ms:.2f}ms)")
        return None