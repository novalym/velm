# Path: scaffold/artisans/run/conductor.py
# ---------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_RUN_SINGULARITY_V12
# SYSTEM: RUN_ARTISAN | ROLE: HIGH_PRIEST_OF_CONTEXT
# =================================================================================
# [ASCENSION LOG]:
# 1.  LAW OF ABSOLUTE RELATIVITY: Force-synchronizes project_root across all facets.
# 2.  EPHEMERAL SANCTUM: High-fidelity '--temp' mode with recursive conduction.
# 3.  GAZE OF THE VOID: Automatic fallback to 'init' or 'distill' for empty realities.
# 4.  POLYMORPHIC FLAG GAZE: Heals 'extra_args' list vs dict schisms.
# 5.  CHRONOMANCER'S VIGIL: Integrated self-healing loop for live development.
# 6.  TRANSACTIONAL HEART: Atomic GnosticTransactions for chronicle-altering rites.
# 7.  UNBREAKABLE WARD: Nested heresy wrapping for total forensic clarity.
# 8.  LUMINOUS HERALD: Cinematic Dossier proclamation for all transfigurations.
# 9.  GNOSTIC ANCHOR: Absolute resolution of 'true_sanctum' via request precedence.
# 10. PURE GNOSTIC CONTRACT: Strict Pydantic I/O honoring the total state.
# 11. SOVEREIGN SOUL: Logic-free conduction; total reliance on the Pantheon.
# 12. PANTHEON FORGE: Lazy-materialization of sub-artisans at the point of birth.
# =================================================================================

from pathlib import Path
import tempfile
import shutil
import os
import time
from types import SimpleNamespace
from typing import Dict, Any, List, Optional, Union

# --- THE DIVINE SUMMONS: INTERNAL GNOSTIC CLUSTER ---
from .bridge import DelegationBridge
from .prophet import GnosticIntentProphet
from .scribe import EphemeralScribe
from .vigil import ChronomancerVigil
from ..runtimes import RuntimesArtisan
from ...contracts.data_contracts import ExecutionPlan
from ...core.artisan import BaseArtisan
from ...core.kernel.transaction import GnosticTransaction
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import RunRequest, RuntimesRequest, InitRequest, DistillRequest
from ...runtime_manager import RuntimeManager
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe


class RunArtisan(BaseArtisan[RunRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF CONTEXT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                 ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE)

    The Sovereign Conductor of the `scaffold run` rite. It perceives the intent
    of the Architect and orchestrates the manifestation of reality, whether it
    be a native Gnostic rite or a polyglot foreign tongue.
    """

    def __init__(self, engine):
        """[FACULTY 12] The Pantheon Forge."""
        super().__init__(engine)
        # Artisans are anchored to the physical root, but re-consecrated during execute.
        self.prophet = GnosticIntentProphet(self.project_root, self.logger)
        self.scribe = EphemeralScribe(self.project_root, self.logger)
        self.bridge = DelegationBridge(self.engine, self.logger)
        self.runtime_manager = RuntimeManager(silent=True)
        self.runtimes_artisan = RuntimesArtisan(self.engine)

    def execute(self, request: RunRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY (V-Ω-SINGLE-PROCLAMATION-ULTIMA)                     ==
        =============================================================================
        LIF: ∞ | ROLE: SOVEREIGN_CONDUCTOR

        [THE FIX]: Implements 'Proclamation Triage'. If the delegated rite is an
        internal Gnostic Rite (Genesis, Transmute, etc.), the Conductor yields the
        stage to the specialist's built-in UI, preventing the 'Double Box' heresy.
        """
        start_time = time.monotonic()

        try:
            # --- MOVEMENT I: THE RITE OF GNOSTIC INQUISITION (`--codex`) ---
            if request.codex:
                self.logger.info("The Architect pleads for the Gnostic Codex. Delegating to the RuntimesArtisan...")
                return self.runtimes_artisan.execute(RuntimesRequest(command='codex'))

            # --- MOVEMENT II: THE EPHEMERAL SANCTUM (DRY-CLEAN) ---
            extra_args = getattr(request, 'extra_args', [])
            has_temp_in_extra = False
            if isinstance(extra_args, dict):
                has_temp_in_extra = extra_args.get('temp', False)
            elif isinstance(extra_args, list):
                has_temp_in_extra = any(arg in ['--temp', 'temp'] for arg in extra_args)

            is_temp_mode = getattr(request, 'temp', False) or has_temp_in_extra

            if is_temp_mode:
                self.logger.info("Conducting rite in an Ephemeral Sanctum (Dry-Clean Mode)...")
                with tempfile.TemporaryDirectory(prefix="scaffold-dry-clean-") as temp_dir:
                    temp_path = Path(temp_dir)
                    target_str = str(request.target) if request.target else ""

                    if target_str and (self.project_root / target_str).is_file():
                        shutil.copy2(self.project_root / target_str, temp_path / target_str)

                    new_req = request.model_copy(deep=True)
                    new_req.project_root = temp_path
                    if hasattr(new_req, 'temp'): new_req.temp = False
                    if isinstance(new_req.extra_args, dict):
                        new_req.extra_args['temp'] = False
                    elif isinstance(new_req.extra_args, list):
                        new_req.extra_args = [a for a in new_req.extra_args if a not in ['--temp', 'temp']]

                    return self.execute(new_req)

            # --- MOVEMENT III: THE RITE OF GNOSTIC RE-CONSECRATION ---
            true_sanctum = request.project_root or self.project_root
            if isinstance(true_sanctum, str):
                true_sanctum = Path(true_sanctum)

            self.engine.project_root = true_sanctum
            self.prophet.project_root = true_sanctum
            self.scribe.project_root = true_sanctum
            self.logger.verbose(f"High Priest of Context anchored to: {true_sanctum}")

            # --- MOVEMENT IV: THE GAZE OF THE VOID & APOTHEOSIS ---
            is_void_plea = not request.target or str(request.target) == "."
            if is_void_plea:
                is_empty = not any(p for p in true_sanctum.iterdir() if not p.name.startswith('.'))
                if is_empty:
                    self.logger.info("Gaze of the Void: The sanctum is empty. Summoning the `init` artisan...")
                    init_req = InitRequest.model_validate(request.model_dump())
                    return self.engine.dispatch(init_req)
                elif not (true_sanctum / "scaffold.scaffold").exists() and not (
                        true_sanctum / "scaffold.lock").exists():
                    self.logger.info(
                        "Gaze of Apotheosis: The sanctum is populated but unmanaged. Summoning `distill`...")
                    distill_req = DistillRequest.model_validate(request.model_dump(exclude={'target'}))
                    distill_req.source_path = "."
                    distill_req.output = "scaffold.scaffold"
                    return self.engine.dispatch(distill_req)

            # --- MOVEMENT V: THE SCRIBE'S UNIFIED PERCEPTION ---
            scripture_path, scripture_content, is_ephemeral_rite, language = self.scribe.perceive(request)

            # --- MOVEMENT VI: THE CHRONOMANCER'S VIGIL ---
            if request.vigil:
                vigil_artisan = ChronomancerVigil(self, scripture_path, request, true_sanctum)
                vigil_artisan.conduct()
                return self.success("The Sentinel's vigil has ended.")

            # --- MOVEMENT VII: THE PROPHET'S ADJUDICATION OF INTENT ---
            initial_rite = language or self.prophet.divine_intent(scripture_path, scripture_content)
            final_rite = self.prophet.adjudicate_reality(initial_rite)
            self.logger.info(f"Universal Conductor perceives a '[cyan]{final_rite}[/cyan]' rite.")

            # --- MOVEMENT VIII: THE GNOSTIC TRIAGE OF REALITY ---
            # Check if this is an internal rite we handle via delegation
            is_internal_gnostic = final_rite in self.bridge.DELEGATION_GRIMOIRE

            if is_internal_gnostic:
                execution_plan = ExecutionPlan(interpreter_cmd=[], strategy='internal', docker_image=None)
            else:
                execution_plan = self.runtime_manager.resolve_execution_plan(
                    language=final_rite, runtime_spec=request.runtime, sanctum=true_sanctum
                )
                strategy_label = execution_plan.strategy
                self.logger.success(
                    f"Oracle's Prophecy received: Conducting via '[green]{strategy_label}[/green]' strategy.")

            # --- MOVEMENT IX: THE TRANSACTIONAL HEART ---
            chronicle_altering_rites = {'patch', 'transmute', 'genesis', 'arch', 'form'}
            transaction_name = f"Run Scripture: {scripture_path.name}"
            if is_ephemeral_rite:
                transaction_name = f"Run Ephemeral Rite: {language or 'unknown'}"

            if final_rite in chronicle_altering_rites:
                with GnosticTransaction(true_sanctum, transaction_name, blueprint_path=scripture_path,
                                        use_lock=not request.no_lock) as tx:
                    result = self.bridge.delegate(final_rite, scripture_path, request, execution_plan)
            else:
                result = self.bridge.delegate(final_rite, scripture_path, request, execution_plan)

            # --- MOVEMENT X: THE LUMINOUS HERALD ---
            # [THE APOTHEOSIS]: We check if the inner rite already handled its own UI.
            # Internal Gnostic Rites (Genesis/Transmute) print their own beautiful boxes.
            # We ONLY print the generic Run Dossier if the rite was external (Python/Node/Shell).
            if result.success and not is_internal_gnostic and final_rite in chronicle_altering_rites:
                registers = SimpleNamespace(
                    get_duration=lambda: time.monotonic() - start_time,
                    files_forged=len(result.artifacts),
                    sanctums_forged=len([a for a in result.artifacts if a.type == 'directory']),
                    bytes_written=sum(getattr(a, 'size_bytes', 0) for a in result.artifacts),
                    no_edicts=request.no_edicts,
                )
                gnosis_context = {"project_type": f"Executed Rite: {final_rite}", **request.variables}
                proclaim_apotheosis_dossier(
                    telemetry_source=registers,
                    gnosis=gnosis_context,
                    project_root=true_sanctum,
                    title=f"✨ Rite Complete: {final_rite} ✨",
                    subtitle=f"The will inscribed in '{scripture_path.name}' is now manifest."
                )

            return result

        except Exception as e:
            if isinstance(e, ArtisanHeresy):
                e.message = f"The `run` rite was shattered by a nested heresy: {e.message}"
                raise e
            raise ArtisanHeresy(f"Catastrophic Paradox in Run Conductor: {e}", child_heresy=e)