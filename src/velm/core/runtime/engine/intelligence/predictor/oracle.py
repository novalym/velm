# Path: src/velm/core/runtime/engine/intelligence/predictor/oracle.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: COGNITIVE_FUSION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ORACLE_V475_TOTALITY_FINALIS
# =========================================================================================

import os
import json
import time
import threading
import hashlib
import collections
import platform
from pathlib import Path
from typing import List, Dict, Optional, Any, Union, Set, Final

# --- THE DIVINE UPLINKS ---
from .markov import ElasticMarkov
from .sage import GnosticSage
from .contracts import GnosticWeightsDossier, PredictionProphecy, HeresyState
from ......interfaces.requests import BaseRequest
from ......interfaces.base import ScaffoldResult
from ......logger import Scribe

Logger = Scribe("SovereignOracle")


class IntentPredictor:
    """
    =======================================================================================
    == THE SOVEREIGN INTENT ORACLE (V-Ω-TOTALITY-V475-FIXED)                             ==
    =======================================================================================
    LIF: ∞ | ROLE: PRECOGNITIVE_CONDUCTOR | RANK: MASTER

    The central mind of the intelligence stratum. It unifies the stochastic,
    deterministic, and semantic sub-minds into a singular persistent consciousness.
    """

    def __init__(self, persistence_root: Path, engine: Optional[Any] = None):
        """[THE RITE OF INCEPTION]"""
        self.logger = Logger
        self.engine = engine
        self.root = persistence_root
        self.memory_dir = persistence_root / ".scaffold" / "cache" / "intelligence"
        self.memory_path = self.memory_dir / "gnostic_weights.json"
        self._lock = threading.RLock()

        # --- THE ENSEMBLE ---
        # [THE FIX]: Orders [1, 2] allow learning from the very first transition
        self.markov = ElasticMarkov(orders=[1, 2], decay_factor=0.999)
        self.sage = GnosticSage()

        # --- SESSION MEMORY ---
        self._session_history: collections.deque = collections.deque(maxlen=100)
        self._last_state: HeresyState = HeresyState.VOID

        # [ASCENSION 1 & 2]: IMMEDIATE INCEPTION
        # Ensure the sanctum exists and the mind is manifest on disk immediately.
        self._ensure_sanctum()
        self._load()

        if not self.memory_path.exists():
            self.logger.verbose("Primordial Mind is a void. Conducting first Inscription.")
            self._persist()

    def _ensure_sanctum(self):
        """[ASCENSION 7]: Recursive Path Discovery."""
        try:
            if not self.memory_dir.exists():
                self.memory_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # If the physical disk is warded, we operate in the ephemeral realm (Memory only)
            Logger.debug(f"Intelligence Sanctum is read-only: {e}")

    # =========================================================================
    # == MOVEMENT I: THE RITE OF OBSERVATION (LEARN)                         ==
    # =========================================================================

    def observe_outcome(self, request: BaseRequest, result: ScaffoldResult):
        """
        [THE FEEDBACK LOOP]
        Ingests the reality of a concluded rite to evolve the Gnostic weights.
        """
        with self._lock:
            rite_name = request.__class__.__name__

            # Skip noise
            if rite_name in ("ReplayRequest", "HelpRequest", "StatusRequest", "TelemetryRequest"):
                return

            # 1. DIVINE STATE
            if not result.success:
                self._last_state = HeresyState.FRACTURED
                self._session_history.append("FRACTURE")
                self._persist()
                return

            self._last_state = HeresyState.PURE if not result.heresies else HeresyState.TAINTED

            # 2. NEURAL INSCRIPTION
            # [THE FIX]: We learn the transition from the history tail to the current rite.
            # Even if history is empty, markov.learn(orders=[1]) will now function.
            history_list = [r for r in list(self._session_history) if r != "FRACTURE"]

            # [ASCENSION 1]: Order-0 / Primordial Start Inception
            if not history_list:
                # We inject a phantom "START" to learn the first move
                self.markov.learn(["START"], rite_name, state=self._last_state)
            else:
                self.markov.learn(history_list, rite_name, state=self._last_state)

            # 3. UPDATE CHRONOLOGY
            self._session_history.append(rite_name)

            # 4. ATOMIC PERSISTENCE
            self._persist()

    # =========================================================================
    # == MOVEMENT II: THE RITE OF DIVINATION (PROPHESY)                      ==
    # =========================================================================

    def prophesy(self) -> List[str]:
        """
        ===================================================================================
        == THE GRAND PROCLAMATION (DIVINE)                                               ==
        ===================================================================================
        LIF: ∞ | The total fusion of probabilistic and deterministic foresight.
        """
        start_ns = time.perf_counter_ns()

        with self._lock:
            # 1. HARVEST GNOSTIC INPUTS
            history = [r for r in list(self._session_history) if r != "FRACTURE"]
            # If history is empty, we check the phantom START
            if not history:
                history = ["START"]

            last_rite = history[-1] if history else None

            # [ASCENSION 11]: REGISTRY VITALITY SYNC
            # Scry the registry to see what's actually manifest
            available_capabilities = {}
            if self.engine and hasattr(self.engine, 'registry'):
                available_capabilities = self.engine.registry._name_to_request

            # 2. CONSULT THE COUNCIL
            m_scores = self.markov.divine(history)
            s_scores = self.sage.advise(
                last_rite=last_rite,
                state=self._last_state,
                history=history,
                metadata={"project_type": self._divine_project_type()}
            )

            # 3. ENSEMBLE FUSION
            final_scores: Dict[str, float] = collections.defaultdict(float)
            for rite, weight in m_scores.items():
                final_scores[rite] += weight * 0.6
            for rite, weight in s_scores.items():
                final_scores[rite] += weight * 0.4

            # 4. VALIDITY FILTERING
            if available_capabilities:
                manifest_names = {r.__name__ for r in available_capabilities.values()}
                for rite in list(final_scores.keys()):
                    if rite not in manifest_names:
                        del final_scores[rite]

            # 5. THE FINAL REVELATION
            if not final_scores:
                suggestions = self.sage.SACRED_BEGINNINGS
                confidence = 0.5
            else:
                ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
                suggestions = [r[0] for r in ranked[:5]]
                confidence = ranked[0][1]

            # 6. TELEMETRY PULSE
            tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if tax_ms > 10.0:
                Logger.verbose(f"Complex Prophecy forged in {tax_ms:.2f}ms.")

            return suggestions

    # =========================================================================
    # == SECTION III: ATOMIC PERSISTENCE                                     ==
    # =========================================================================

    def _persist(self):
        """
        [ASCENSION 3 & 8]: WINDOWS-HARDENED ATOMIC PERSISTENCE.
        Ensures the intelligence is enshrined without risk of corruption.
        """
        if not self.memory_dir.exists(): return

        try:
            data = {
                "version": "4.7.5-Totality",
                "timestamp": time.time(),
                "project_type": self._divine_project_type(),
                "machine": platform.node(),
                "last_state": self._last_state.value,
                "history_tail": list(self._session_history)[-15:],
                "markov": self.markov.serialize(),
            }

            temp_path = self.memory_path.with_suffix(".tmp")

            # [ASCENSION 3]: ATOMIC WRITE RITE
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=0)
                f.flush()
                if os.name != 'nt':
                    os.fsync(f.fileno())

            # [THE FIX]: Resilient Atomic Swap for Windows
            for attempt in range(3):
                try:
                    if self.memory_path.exists():
                        self.memory_path.unlink()
                    os.replace(str(temp_path), str(self.memory_path))
                    break
                except OSError:
                    time.sleep(0.1)

            # [ASCENSION 6]: HUD BROADCAST
            self._project_hud_pulse()

        except Exception as e:
            Logger.debug(f"Persistence Fracture: {e}")

    def _load(self):
        """[THE RITE OF RECALL]"""
        if not self.memory_path.exists(): return

        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "markov" in data:
                self.markov.deserialize(data["markov"])

            self._last_state = HeresyState(data.get("last_state", "VOID"))

            # Restore history tail to maintain continuity
            tail = data.get("history_tail", [])
            self._session_history.clear()
            self._session_history.extend(tail)

            Logger.verbose(f"Intelligence Resurrected. {len(tail)} temporal nodes restored.")

        except Exception as e:
            # [ASCENSION 9]: Self-Healing Tabula Rasa
            Logger.warn(f"Intelligence corrupted: {e}. Initiating Purgation.")
            if self.memory_path.exists():
                self.memory_path.unlink()

    def _divine_project_type(self) -> str:
        if (self.root / "pyproject.toml").exists(): return "python"
        if (self.root / "package.json").exists(): return "typescript"
        if (self.root / "Cargo.toml").exists(): return "rust"
        return "generic"

    def _project_hud_pulse(self):
        """Projects the state of memory to the Ocular HUD."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MEMORY_ENSHRINED",
                        "label": "GNOSTIC_SYNC",
                        "color": "#64ffda",
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_INTENT_ORACLE history={len(self._session_history)} state={self._last_state.value}>"

# == SCRIPTURE SEALED: THE ORACLE IS THE SINGULARITY ==