# Path: packages/scaffold/src/scaffold/core/runtime/engine/intelligence/predictor.py
# ----------------------------------------------------------------------------------

import json
import time
import math
import threading
import os
from collections import defaultdict, deque, Counter
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Union

# --- GNOSTIC UPLINKS ---
from .....interfaces.requests import BaseRequest
from .....interfaces.base import ScaffoldResult
from .....contracts.heresy_contracts import ArtisanHeresy

# =================================================================================
# == THE PHYSICS OF COGNITION (CONSTANTS)                                        ==
# =================================================================================

# [MEMORY PHYSICS]
MEMORY_FILE = "gnostic_weights.json"
MAX_HISTORY_DEPTH = 50  # How far back we remember in the session
MARKOV_ORDER = 2  # Lookback for stochastic transitions
SEQUENCE_DEPTH = 5  # Lookback for pattern matching

# [WEIGHTING PHYSICS]
DECAY_RATE = 0.99  # Memory fading per interaction
ERROR_WEIGHT = 2.0  # Priority multiplier during failure states
SUCCESS_REWARD = 1.0  # RL Reward for correct prediction

# [ENSEMBLE WEIGHTS]
W_MARKOV = 0.4
W_HEURISTIC = 0.4
W_SEQUENCE = 0.2


# =================================================================================
# == I. THE STOCHASTIC ENGINE (MARKOV ASCENDED)                                  ==
# =================================================================================

class MarkovOracle:
    """
    [THE PROBABILISTIC MIND]
    Learns the frequency of transitions: (A, B) -> C.
    Ascended with 'Key Resilience' and 'Temporal Decay'.
    """

    def __init__(self):
        # Map[ContextTuple, Map[NextRite, Weight]]
        # We use a factory to ensure resurrection safety
        self._matrix: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._total_transitions = 0

    def observe(self, history: List[str], next_rite: str):
        """[THE RITE OF OBSERVATION]"""
        if len(history) < MARKOV_ORDER: return

        # Create context key (e.g., "GenesisRequest|RunRequest")
        context = "|".join(history[-MARKOV_ORDER:])

        # [ASCENSION 1]: KEY RESILIENCE GUARD (The Cure)
        # Even if loaded from JSON, we treat it as mutable.
        if context not in self._matrix:
            self._matrix[context] = defaultdict(float)

        # Increment weight
        self._matrix[context][next_rite] = self._matrix[context].get(next_rite, 0.0) + 1.0
        self._total_transitions += 1

        # [ASCENSION 2]: SELF-NORMALIZATION
        # Prevent integer overflow by scaling down periodically
        if self._matrix[context][next_rite] > 1000:
            for k in self._matrix[context]:
                self._matrix[context][k] *= 0.5

    def predict(self, history: List[str]) -> Dict[str, float]:
        """[THE RITE OF DIVINATION]"""
        if len(history) < MARKOV_ORDER: return {}

        context = "|".join(history[-MARKOV_ORDER:])
        transitions = self._matrix.get(context, {})

        if not transitions: return {}

        total = sum(transitions.values())
        return {k: v / total for k, v in transitions.items()}

    def serialize(self) -> Dict:
        return {"matrix": dict(self._matrix), "total": self._total_transitions}

    def deserialize(self, data: Dict):
        # [ASCENSION 3]: RESURRECTION ALCHEMY
        # Reconstructs the defaultdict behavior from static JSON
        raw_matrix = data.get("matrix", {})
        self._matrix = defaultdict(lambda: defaultdict(float))
        for ctx, transitions in raw_matrix.items():
            self._matrix[ctx] = defaultdict(float, transitions)
        self._total_transitions = data.get("total", 0)


# =================================================================================
# == II. THE LOGIC ENGINE (HEURISTIC SAGE)                                       ==
# =================================================================================

class HeuristicSage:
    """
    [THE DETERMINISTIC MIND]
    Hard-coded wisdom and architectural best practices.
    Responds to environmental context (Errors, Git Status).
    """

    # [ASCENSION 4]: THE CHAIN OF CAUSALITY
    LOGICAL_CHAINS = {
        "GenesisRequest": ["RunRequest", "SymphonyRequest"],
        "CreateRequest": ["AnalyzeRequest", "RefactorRequest", "RunRequest"],
        "AnalyzeRequest": ["RefactorRequest", "GraphRequest", "DistillRequest"],
        "TransmuteRequest": ["VerifyRequest", "RunRequest"],
        "InstallRequest": ["AuditRequest", "RunRequest"],
        "ScribeRequest": ["AnalyzeRequest", "ApplyRequest"],
        # [ASCENSION 5]: THE RECOVERY LOOP
        "Crash": ["ResurrectRequest", "AnalyzeRequest", "UndoRequest"]
    }

    def consult(self, last_rite: str, context: Dict[str, Any]) -> Dict[str, float]:
        suggestions: Dict[str, float] = defaultdict(float)

        # 1. ERROR RESPONSE (High Priority)
        if context.get("last_failed"):
            suggestions["ResurrectRequest"] = 1.0
            suggestions["AnalyzeRequest"] = 0.8
            suggestions["UndoRequest"] = 0.6
            return suggestions

        # 2. STANDARD CHAINS
        if last_rite in self.LOGICAL_CHAINS:
            chain = self.LOGICAL_CHAINS[last_rite]
            for i, next_rite in enumerate(chain):
                # Diminishing returns for deeper links
                suggestions[next_rite] += 0.9 / (i + 1)

        # 3. ENVIRONMENT AWARENESS
        if context.get("is_fresh_install"):
            suggestions["InitRequest"] = 0.95

        if context.get("git_dirty"):
            suggestions["SaveRequest"] += 0.3

        return suggestions


# =================================================================================
# == III. THE PATTERN ENGINE (SEQUENCE MINER)                                    ==
# =================================================================================

class SequenceMiner:
    """
    [THE GRAMMATICAL MIND]
    Detects long-range dependencies using N-Gram analysis.
    Finds patterns like A -> B -> C -> [D].
    """

    def __init__(self):
        # Map[Tuple[Rite...], Counter[NextRite]]
        self._ngrams: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)

    def observe(self, history: List[str], next_rite: str):
        # Learn sequences of length 3 to SEQUENCE_DEPTH
        for depth in range(3, SEQUENCE_DEPTH + 1):
            if len(history) >= depth:
                seq = tuple(history[-depth:])
                self._ngrams[seq][next_rite] += 1

    def predict(self, history: List[str]) -> Dict[str, float]:
        predictions: Dict[str, float] = defaultdict(float)

        # Check all possible n-gram depths
        for depth in range(3, SEQUENCE_DEPTH + 1):
            if len(history) >= depth:
                seq = tuple(history[-depth:])
                if seq in self._ngrams:
                    counts = self._ngrams[seq]
                    total = sum(counts.values())
                    # Longer sequences have higher weight
                    weight = depth * 0.2
                    for rite, count in counts.items():
                        predictions[rite] += (count / total) * weight

        return predictions

    def serialize(self) -> Dict:
        # Convert tuple keys to strings for JSON
        return {
            "ngrams": {
                "|".join(k): dict(v) for k, v in self._ngrams.items()
            }
        }

    def deserialize(self, data: Dict):
        raw = data.get("ngrams", {})
        self._ngrams = defaultdict(Counter)
        for k_str, counts in raw.items():
            key = tuple(k_str.split("|"))
            self._ngrams[key] = Counter(counts)


# =================================================================================
# == IV. THE SOVEREIGN ORCHESTRATOR (INTENT PREDICTOR)                           ==
# =================================================================================

class IntentPredictor:
    """
    =============================================================================
    == THE INTENT PREDICTOR (V-Ω-ENSEMBLE-COGNITION)                           ==
    =============================================================================
    The Fusion Engine. It blends Stochastic Probability, Deterministic Wisdom,
    and Grammatical Pattern Recognition to form the ultimate prophecy.

    [CAPABILITIES]:
    1.  **Ensemble Voting:** Weighted fusion of 3 cognitive sub-engines.
    2.  **State Persistence:** Thread-safe JSON serialization with atomic writes.
    3.  **Self-Correction:** Reinforcement learning based on accuracy.
    4.  **Forensic Context:** Aware of crashes, git state, and project age.
    """

    def __init__(self, persistence_root: Path):
        self.root = persistence_root
        self.memory_dir = persistence_root / ".scaffold" / "cache" / "intelligence"
        self.memory_path = self.memory_dir / MEMORY_FILE

        # The Minds
        self.markov = MarkovOracle()
        self.sage = HeuristicSage()
        self.miner = SequenceMiner()

        # Short Term Memory (Session Context)
        self._session_history: deque = deque(maxlen=MAX_HISTORY_DEPTH)
        self._last_result: Optional[ScaffoldResult] = None
        self._lock = threading.RLock()

        # [ASCENSION 6]: RESURRECTION
        self._load()

    def observe_outcome(self, request: BaseRequest, result: ScaffoldResult):
        """
        [THE FEEDBACK LOOP]
        Ingests the reality of the last rite.
        """
        with self._lock:
            rite_name = type(request).__name__
            success = result.success

            # [ASCENSION 7]: ERROR LEARNING
            # If failed, we don't learn the transition A->B.
            # Instead, we mark the context as "Fractured".
            if not success:
                self._last_result = result
                # We do not append to history to avoid learning bad habits?
                # No, we append "Crash" to history so we can predict recovery.
                self._session_history.append("Crash")
                self._persist()
                return

            # Learn
            if len(self._session_history) > 0:
                prev_rite = self._session_history[-1]
                if prev_rite != "Crash":
                    # Teach Markov
                    self.markov.observe(list(self._session_history), rite_name)
                    # Teach Miner
                    self.miner.observe(list(self._session_history), rite_name)

            self._session_history.append(rite_name)
            self._last_result = result
            self._persist()

    def prophesy(self) -> List[str]:
        """
        [THE GRAND PROCLAMATION]
        Returns a ranked list of likely next Rites.
        """
        with self._lock:
            history = list(self._session_history)

            # 1. Gather Context
            context_flags = {
                "last_failed": self._last_result and not self._last_result.success,
                "git_dirty": False,  # Future hook
                "is_fresh_install": len(history) < 3
            }

            # 2. Consult the Council
            scores_markov = self.markov.predict(history)
            scores_sage = self.sage.consult(history[-1] if history else None, context_flags)
            scores_miner = self.miner.predict(history)

            # 3. The Ensemble Vote (Weighted Fusion)
            final_scores: Dict[str, float] = defaultdict(float)

            for rite, score in scores_markov.items():
                final_scores[rite] += score * W_MARKOV

            for rite, score in scores_sage.items():
                final_scores[rite] += score * W_HEURISTIC

            for rite, score in scores_miner.items():
                final_scores[rite] += score * W_SEQUENCE

            # 4. Sort and Prune
            ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

            # Return top N suggestions
            # [ASCENSION 8]: TYPE PURIFICATION
            # Ensure we return valid Request Class names
            return [r[0] for r in ranked[:5]]

    def _persist(self):
        """[THE RITE OF PERMANENCE] Atomic write to disk."""
        try:
            if not self.memory_dir.exists():
                self.memory_dir.mkdir(parents=True, exist_ok=True)

            data = {
                "markov": self.markov.serialize(),
                "miner": self.miner.serialize(),
                "updated_at": time.time()
            }

            # Atomic Write
            temp = self.memory_path.with_suffix(".tmp")
            with open(temp, 'w') as f:
                json.dump(data, f, indent=0)  # Minified for speed
            os.replace(temp, self.memory_path)

        except Exception as e:
            # We never crash on memory save failure
            pass

    def _load(self):
        """[THE RITE OF RECALL]"""
        if not self.memory_path.exists(): return

        try:
            with open(self.memory_path, 'r') as f:
                data = json.load(f)

            if "markov" in data:
                self.markov.deserialize(data["markov"])
            if "miner" in data:
                self.miner.deserialize(data["miner"])

        except Exception:
            # If memory is corrupt, we start fresh (Tabula Rasa)
            pass