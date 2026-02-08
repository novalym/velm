# Path: src/velm/core/runtime/engine/intelligence/predictor/markov.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: PROBABILISTIC_TENSOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_MARKOV_V500_TOTALITY_FINALIS
# =========================================================================================

import time
import math
import collections
import threading
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Union, Set, Final
from .contracts import WeightNode, CognitiveStratum, HeresyState
from ......logger import Scribe
Logger = Scribe("ElasticMarkov")
class ElasticMarkov:
    """
    =======================================================================================
    == THE ELASTIC MARKOV TENSOR (V-Ω-TOTALITY-V500)                                     ==
    =======================================================================================
    LIF: ∞ | ROLE: PROBABILISTIC_ORACLE | RANK: MASTER

    The high-order brain of the Predictor. It perceives causality across a multi-strata
    temporal landscape, implementing recursive backoff and a-temporal decay.
    """

    def __init__(self, orders: List[int] = [1, 2], decay_factor: float = 0.999):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()

        # [ASCENSION 12]: MULTI-ORDER STRATIFICATION
        self.strata: Dict[int, CognitiveStratum] = {
            order: CognitiveStratum(order=order) for order in orders
        }

        self.decay_factor = decay_factor
        self._total_learning_rites = 0
        self._state_hash = hashlib.sha256(b"void").hexdigest()

    # =========================================================================
    # == MOVEMENT I: THE RITE OF NEURAL INSCRIPTION (LEARN)                  ==
    # =========================================================================

    def learn(self, history: List[str], next_rite: str, state: HeresyState = HeresyState.PURE):
        """
        Inscribes a new transition into the probabilistic fabric.
        [THE FIX]: Now fully integrated with the persistence facade.
        """
        with self._lock:
            self._total_learning_rites += 1

            # [ASCENSION 5]: GAUSSIAN DECAY
            # Naturally fade the past before writing the future
            self._apply_achronal_decay()

            for order, stratum in self.strata.items():
                if len(history) >= order:
                    # 1. FORGE CONTEXT COORDINATE
                    context = "|".join(history[-order:])

                    # 2. NAVIGATE LATTICE
                    if context not in stratum.lattice:
                        stratum.lattice[context] = {}

                    if next_rite not in stratum.lattice[context]:
                        stratum.lattice[context][next_rite] = WeightNode(
                            value=0.0,
                            frequency=0,
                            last_summoned=time.time()
                        )

                    node = stratum.lattice[context][next_rite]

                    # 3. [ASCENSION 11]: POLARIZED REINFORCEMENT
                    # Calculate weight delta based on the Heresy State
                    weight_delta = 1.0
                    if state == HeresyState.FRACTURED:
                        weight_delta = -5.0  # Massive penalty for failure
                    elif state == HeresyState.TAINTED:
                        weight_delta = 0.2  # Minimal gain for weak resonance

                    # 4. INSCRIBE
                    node.value = max(0.0, node.value + weight_delta)
                    node.frequency += 1
                    node.last_summoned = time.time()

            # [ASCENSION 21]: PERIODIC INTEGRITY SYNC
            if self._total_learning_rites % 50 == 0:
                self._evolve_state_hash(next_rite)

    # =========================================================================
    # == MOVEMENT II: THE RITE OF DIVINATION (DIVINE)                        ==
    # =========================================================================

    def divine(self, history: List[str]) -> Dict[str, float]:
        """
        Performs a weighted ensemble scry with Recursive Backoff.
        """
        with self._lock:
            ensemble_scores: Dict[str, float] = collections.defaultdict(float)

            # [ASCENSION 2]: RECURSIVE BACKOFF
            # We iterate orders from highest to lowest
            for order in sorted(self.strata.keys(), reverse=True):
                stratum = self.strata[order]
                if len(history) >= order:
                    context = "|".join(history[-order:])

                    # [ASCENSION 3]: BAYESIAN CONFIDENCE
                    # Order-2 (Context) has 4x the voting power of Order-1 (Succession)
                    order_power = math.pow(order, 2)

                    probabilities = stratum.scry(context)

                    if probabilities:
                        for rite, prob in probabilities.items():
                            ensemble_scores[rite] += prob * order_power

            return self._normalize_scores(ensemble_scores)

    # =========================================================================
    # == MOVEMENT III: THE RITE OF PERSISTENCE (THE FIX)                     ==
    # =========================================================================

    def serialize(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF SERIALIZATION (THE FIX)                                     ==
        =============================================================================
        [ASCENSION 1]: Transmutes the complex tensor into a portable JSON dossier.
        """
        with self._lock:
            serial_strata = {}
            for order, stratum in self.strata.items():
                serial_lattice = {}
                for context, targets in stratum.lattice.items():
                    serial_lattice[context] = {
                        rite: {
                            "v": node.value,
                            "f": node.frequency,
                            "ts": node.last_summoned
                        }
                        for rite, node in targets.items()
                    }
                serial_strata[str(order)] = serial_lattice

            return {
                "total_rites": self._total_learning_rites,
                "state_hash": self._state_hash,
                "strata": serial_strata,
                "timestamp": time.time()
            }

    def deserialize(self, data: Dict[str, Any]):
        """
        =============================================================================
        == THE RITE OF RESURRECTION (THE FIX)                                      ==
        =============================================================================
        [ASCENSION 1]: Restores the Markov mind from a digital artifact.
        """
        with self._lock:
            try:
                self._total_learning_rites = data.get("total_rites", 0)
                self._state_hash = data.get("state_hash", self._state_hash)

                raw_strata = data.get("strata", {})
                for order_str, lattice in raw_strata.items():
                    order = int(order_str)
                    if order in self.strata:
                        for context, targets in lattice.items():
                            self.strata[order].lattice[context] = {
                                rite: WeightNode(
                                    value=meta["v"],
                                    frequency=meta["f"],
                                    last_summoned=meta["ts"]
                                )
                                for rite, meta in targets.items()
                            }

                Logger.verbose(f"Markov Matrix Resurrected. {len(self.strata)} strata manifest.")
            except Exception as e:
                Logger.error(f"Resurrection Fracture: {e}. Mind remains at Tabula Rasa.")

    # =========================================================================
    # == INTERNAL METABOLISM                                                 ==
    # =========================================================================

    def _apply_achronal_decay(self):
        """[ASCENSION 5]: Naturally fades ancient weights."""
        for stratum in self.strata.values():
            for context in stratum.lattice:
                for node in stratum.lattice[context].values():
                    node.value *= self.decay_factor

    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        if not scores: return {}
        total = sum(scores.values())
        return {k: v / total for k, v in scores.items()}

    def _evolve_state_hash(self, salt: str):
        raw = f"{self._state_hash}:{salt}:{time.time_ns()}"
        self._state_hash = hashlib.sha256(raw.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<Ω_MARKOV_TENSOR rites={self._total_learning_rites} hash={self._state_hash[:8]}>"

# == SCRIPTURE SEALED: THE STOCHASTIC MIND IS OMEGA TOTALITY ==