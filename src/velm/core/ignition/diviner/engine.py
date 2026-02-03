# Path: scaffold/core/ignition/diviner/engine.py
# ----------------------------------------------
# LIF: INFINITY // AUTH_CODE: @)(!@(!()@ // Ω_DIVINER_ENGINE_SINGULARITY
# SYSTEM: IDEABOX QUANTUM // MODULE: IGNITION.DIVINER
# -------------------------------------------------------------------------------------

import time
from pathlib import Path
from typing import Optional, Union, List, Tuple

# --- THE DIVINE SUMMONS: INTERNAL GNOSTIC CLUSTER ---
from ..contracts import (
    ExecutionPlan,
    IgnitionAura,
    NetworkPhysics,
    BiologicalSupport,
    DivinationResult,
    HeuristicResonance
)
from .seekers import SeekerConductor
from .heuristics.engine import BayesianBrain
from .strategies import StrategyArchitect
from ..sentinel.priest import ToolchainSentinel
from .persistence import PersistenceMatrix
from .telemetry import ForensicScribe
from .exceptions import VoidSanctumError, DivinationHeresy

from ....logger import Scribe

Logger = Scribe("IgnitionEngine")


class IgnitionDiviner:
    """
    =================================================================================
    == THE IGNITION DIVINER (ZENITH_APOTHEOSIS_FINAL)                              ==
    =================================================================================
    LIF: INFINITY | The 100% Mathematical Certainty Engine.

    The Sovereign Conductor of Inception. This engine unifies the Perception Array,
    The Bayesian Mind, and the Strategic Hand to materialize code as a living process.
    =================================================================================
    """

    def __init__(self):
        """
        [ASCENSION 17]: Initialize the internal faculty conduits.
        The Brain and Scribe are instantiated once to hold state during a rite.
        """
        self.brain = BayesianBrain()
        self.scribe = ForensicScribe()

    def divine(self,
               path: Union[str, Path],
               port: int,
               force_aura: Optional[str] = None,
               no_cache: bool = False) -> ExecutionPlan:
        """
        =============================================================================
        == THE GRAND RITE OF DIVINATION (V-Ω-TOTALITY)                           ==
        =============================================================================
        Performs a full-spectrum tomography of a directory to derive the
        optimal ExecutionPlan.
        """
        self.scribe = ForensicScribe()  # [ASCENSION 9]: Reset the chronicle for a new take
        root = Path(path).resolve()

        # [ASCENSION 61]: Forensic Capture - Guard the Gateway
        if not root.exists():
            raise VoidSanctumError(str(root))

        self.scribe.record(f"Inception initiated at: {root}")

        # --- MOVEMENT I: TEMPORAL RECALL (PERSISTENCE) ---
        # [ASCENSION 65]: Persistence Matrix Resonance
        # We attempt to resurrect the previous reality if the Merkle Seal is unbroken.
        matrix = PersistenceMatrix(root)
        if not no_cache and not force_aura:
            cached_data = matrix.recall(root)
            if cached_data:
                self.scribe.record("Temporal Resonance achieved: Recalling past Gnosis.")
                # We validate the cached data against the current contracts
                return ExecutionPlan.model_validate(cached_data)

        Logger.info(f"Conducting High-Fidelity Tomography: [cyan]{root.name}[/cyan]")

        # --- MOVEMENT II: SPATIAL TOMOGRAPHY (SEEKERS) ---
        # [ASCENSION 35]: We find the 'Logic Heart' and the 'Visual Seed' using the Seeker pack.
        conductor = SeekerConductor(root)
        logic_heart, visual_root = conductor.conduct_tomography()

        # [ASCENSION 7]: Isomorphic Path Resolution
        # Ensure the heart is expressed relative to the project root for UI clarity
        self.scribe.record(f"Logic Heart anchored: {logic_heart.relative_to(root) if logic_heart != root else 'ROOT'}")

        # --- MOVEMENT III: CEREBRAL INFERENCE (HEURISTICS) ---
        # [ASCENSION 52]: The Bayesian brain weighs all indicators from the tomographic heart.
        aura, confidence = self.brain.judge(logic_heart)
        self.scribe.record(f"Bayesian Adjudication: {aura.value} ({confidence * 100:.1f}%)")

        # --- MOVEMENT IV: SOCRATIC OVERRIDE & RECONCILIATION ---
        # [ASCENSION 54]: Respect the Architect's direct will if spoken.
        if force_aura:
            try:
                aura = IgnitionAura(force_aura)
                confidence = 1.0
                self.scribe.record(f"Socratic Override: Wavefunction collapsed to {aura}")
            except ValueError:
                Logger.warn(f"Heresy: Profane Aura override ignored: {force_aura}")

        # [ASCENSION 18]: VISUAL FALLBACK CASCADE
        # If logic is silent but matter is dense with HTML, pivot to Ocular Reality.
        if (aura == IgnitionAura.GENERIC or aura == IgnitionAura.STATIC) and confidence < 0.4:
            if (visual_root / "index.html").exists():
                aura = IgnitionAura.STATIC
                logic_heart = visual_root
                confidence = 0.7
                self.scribe.record("Logic Heart silent. Pivoting to Ocular Reality (Static).")

        # --- MOVEMENT V: STRATEGIC FORGING (STRATEGIES) ---
        # [ASCENSION 58]: Build the immutable execution sequence.
        # This handles binary resolution (npm.cmd vs npm) and port injection.
        plan = StrategyArchitect.forge(aura, logic_heart, port)
        self.scribe.record("Strategic Command Sequence forged.")

        # --- MOVEMENT VI: BIOLOGICAL AUDIT (SENTINEL) ---
        # [ASCENSION 32]: Verifying that the Lungs (node_modules/venv) are physically manifest.
        support = ToolchainSentinel.verify_biological_support(logic_heart, aura)
        self.scribe.record(f"Biological Audit: {'PURE' if support.is_installed else 'FRACTURED'}")

        # --- MOVEMENT VII: FINAL APOTHEOSIS (COMPOSITION) ---
        # [ASCENSION 96]: Assemble the final result with full decision telemetry.
        final_plan = plan.model_copy(update={
            "support": support,
            "confidence": confidence,
            "reasoning_trace": self.scribe.finalize() + self.brain.trace
        })

        # [ASCENSION 72]: Enshrine in the Temporal Vault for zero-latency recall.
        if not no_cache:
            matrix.enshrine(root, final_plan)

        # Final Proclamation
        latency = (time.perf_counter() - self.scribe.start_time) * 1000
        Logger.success(f"Apotheosis Complete: [bold]{aura.value}[/bold] manifested in {latency:.2f}ms")

        return final_plan

    # =============================================================================
    # == AUXILIARY RITES                                                         ==
    # =============================================================================

    def check_infrastructure(self, plan: ExecutionPlan) -> tuple[bool, str]:
        """
        [ASCENSION 31]: Performs a live health check on the plan's components.
        Verifies if the specific toolchain binary is functional.
        """
        tool = plan.command[0]
        exists, path, remedy = ToolchainSentinel.scry_artisan(tool)
        return exists, remedy

    def generate_dossier(self, plan: ExecutionPlan) -> DivinationResult:
        """
        [ASCENSION 1]: Transmutes a plan into a comprehensive Bayesian Dossier.
        Used by the UI to show alternative realities and confidence intervals.
        """
        return DivinationResult(
            winning_plan=plan,
            total_divination_ms=(time.time() - plan.divination_timestamp) * 1000,
            logic_heart_path=plan.cwd
        )

# [ASCENSION 12]: SOVEREIGN MODULE SEAL
# The engine is now finalized and immutable.

