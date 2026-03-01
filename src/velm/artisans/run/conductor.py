# Path: src/velm/artisans/run/conductor.py
# =========================================================================================
# == THE UNIVERSAL CONDUCTOR: OMEGA TOTALITY (V-Ω-TOTALITY-V25000.77-UNBREAKABLE)        ==
# =========================================================================================
# LIF: ∞ | ROLE: KINETIC_ROOT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_RUN_V25K_77_ABSOLUTE_BYPASS_2026_FINALIS
# =========================================================================================

import re
import shlex
import time
import uuid
import tempfile
import shutil
import os
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, Any, List, Optional, Union, Callable, Set, Final

# --- THE DIVINE UPLINKS ---
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
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

# =========================================================================================
# == [THE CURE]: THE ISOMORPHIC IMPORT PHALANX                                           ==
# =========================================================================================
# Resolves the RuntimeManager coordinate across all physical and virtual substrates.
RuntimeManager = None
try:
    from ...artisans.runtimes.manager import RuntimeManager as RM

    RuntimeManager = RM
except ImportError:
    try:
        from ...runtime_manager import RuntimeManager as RM

        RuntimeManager = RM
    except ImportError:
        try:
            import runtime_manager

            RuntimeManager = runtime_manager.RuntimeManager
        except (ImportError, AttributeError):
            try:
                from velm.runtime_manager import RuntimeManager as RM

                RuntimeManager = RM
            except ImportError:
                pass


# =========================================================================================

class RunArtisan(BaseArtisan[RunRequest]):
    """
    =================================================================================
    == THE UNIVERSAL CONDUCTOR (V-Ω-TOTALITY-V25000.77-UNBREAKABLE)                ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_FORCE_MULTIPLIER | RANK: OMEGA_SOVEREIGN
    """

    # [ASCENSION 1]: THE POSIX TRANSMUTATION MATRIX
    # These identities are warded to bypass the "Scripture Existence" inquest.
    POSIX_RITES: Final[Set[str]] = {
        "rm", "ls", "mkdir", "touch", "cat", "pwd", "echo", "find", "grep", "mv",
        "chmod", "git", "npm", "poetry", "pip", "docker", "cargo", "go", "make",
        "rustc", "python", "terraform", "aws", "supabase", "curl", "wget", "tar", "zip"
    }

    def __init__(self, engine: Any):
        """
        [FACULTY 12]: THE PANTHEON FORGE.
        Constructor is a Zero-Cost Rite. All sub-artisans are birthed lazily to
        prevent 'NoneType' call-chain collapse during the WASM boot race.
        """
        super().__init__(engine)
        self.logger = Scribe("RunArtisan")
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                "pyodide" in sys.modules
        )
        # Lazy Slots
        self._prophet = None
        self._scribe = None
        self._bridge = None
        self._runtime_manager = None
        self._runtimes_artisan = None

    @property
    def prophet(self):
        if not self._prophet:
            from .prophet import GnosticIntentProphet
            self._prophet = GnosticIntentProphet(self.project_root, self.logger)
        return self._prophet

    @property
    def scribe(self):
        if not self._scribe:
            from .scribe import EphemeralScribe
            self._scribe = EphemeralScribe(self.project_root, self.logger)
        return self._scribe

    @property
    def bridge(self):
        if not self._bridge:
            from .bridge import DelegationBridge
            self._bridge = DelegationBridge(self.engine, self.logger)
        return self._bridge

    @property
    def runtimes_artisan(self):
        if not self._runtimes_artisan:
            from ..runtimes import RuntimesArtisan
            self._runtimes_artisan = RuntimesArtisan(self.engine)
        return self._runtimes_artisan

    @property
    def manager(self) -> Any:
        """[THE SUPREME FIX]: LATE-BINDING RUNTIME MANAGER."""
        if self._runtime_manager is None:
            if RuntimeManager is None:
                raise ArtisanHeresy(
                    "Substrate Fracture: 'RuntimeManager' logic unmanifest.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Ensure the Engine has finished unzipping its arsenal."
                )
            self._runtime_manager = RuntimeManager(silent=True, engine=self.engine)
        return self._runtime_manager

    # =========================================================================
    # == STRATUM III: MASTER EXECUTION RITE                                  ==
    # =========================================================================

    def execute(self, request: RunRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA EXECUTION RITE: TOTALITY (V-Ω-V25000.77-UNBREAKABLE)          ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        """
        start_time = time.monotonic()

        # --- MOVEMENT 0: IDENTITY INCEPTION ---
        trace_id = (getattr(request, 'trace_id', None) or f"tr-run-{uuid.uuid4().hex[:6].upper()}")

        try:
            # --- MOVEMENT I: THE CODEX BYPASS ---
            if getattr(request, 'codex', False):
                self.logger.info(f"[{trace_id}] Architect pleads for the Codex. Delegating...")
                return self.runtimes_artisan.execute(RuntimesRequest(command='codex', trace_id=trace_id))

            # --- MOVEMENT II: TOPOGRAPHICAL ANCHORING ---
            # [ASCENSION 9]: Absolute resolution of 'true_sanctum' via request precedence.
            true_sanctum = Path(request.project_root or self.project_root).resolve()
            target_raw = str(getattr(request, 'target', "") or "").strip()

            # [ASCENSION 18]: SUBSTRATE-AWARE ANCHORING
            self.engine.project_root = true_sanctum

            # --- MOVEMENT III: THE GAZE OF THE VOID & APOTHEOSIS ---
            if not target_raw or target_raw in (".", "./"):
                return self._conduct_void_apotheosis(request, true_sanctum, trace_id)

            # =========================================================================
            # == MOVEMENT IV: THE ABSOLUTE KINETIC BYPASS (THE CURE)                 ==
            # =========================================================================
            # [ASCENSION 1]: Threshold Bifurcation.
            # We adjudicate if this is a Command or a Scripture BEFORE language scrying.

            # 1. Matter Biopsy
            target_path = (true_sanctum / target_raw)
            is_physical_file = target_path.is_file()

            # 2. Semantic Biopsy (Matrix Search)
            try:
                # [ASCENSION 3]: The Shell-Splat Protocol
                cmd_tokens = shlex.split(target_raw)
                binary_name = cmd_tokens[0] if cmd_tokens else ""
            except Exception:
                binary_name = target_raw.split()[0] if target_raw else ""

            is_shell_edict = binary_name in self.POSIX_RITES

            # [THE STRIKE]: Direct Kinetic Bypass
            if not is_physical_file and is_shell_edict:
                # [ASCENSION 4]: Adrenaline Mode for destructive rites
                is_destructive = binary_name in ("rm", "mv", "annihilate", "purge")
                if is_destructive: self.engine.set_adrenaline(True)

                self.logger.info(f"[{trace_id}] Posix Resonance: Transmuting '{binary_name}' to Shell Strike.")

                # Construct virtual execution plan MANUALLY. Bypasses RuntimeManager scry.
                plan = ExecutionPlan(interpreter_cmd=[], strategy='shell', docker_image=None)

                try:
                    # STRIKE: Delegate directly to the bridge and RETURN INSTANTLY.
                    result = self.bridge.delegate("shell", Path(target_raw), request, plan)

                    # [ASCENSION 5]: Hydraulic VFS Sync
                    if result.success and is_destructive:
                        self.engine.dispatch("scry", {"path": str(true_sanctum), "force": True})

                    return result
                finally:
                    if is_destructive: self.engine.set_adrenaline(False)

            # --- MOVEMENT V: THE EPHEMERAL SANCTUM (DRY-CLEAN) ---
            if getattr(request, 'temp', False) or (
                    isinstance(request.extra_args, list) and '--temp' in request.extra_args):
                return self._conduct_ephemeral_strike(request, target_raw, true_sanctum)

            # --- MOVEMENT VI: THE SCRIPTURE INQUEST (STANDARD PATH) ---
            # If we reached here, the target is NOT a POSIX rite, so it MUST be a file.
            if not is_physical_file:
                # [ASCENSION 10]: Socratic Discovery Oracle
                raise ArtisanHeresy(
                    f"Scripture Unmanifest: '{target_raw}' is a void.",
                    details=f"Path searched: {target_path.as_posix()}",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"If you intended to run a shell command, verify it is in the POSIX_RITES registry.",
                    trace_id=trace_id
                )

            # --- MOVEMENT VII: THE SCRIER'S PERCEPTION ---
            scripture_path, scripture_content, is_ephemeral, language = self.scribe.perceive(request)

            # --- MOVEMENT VIII: THE CHRONOMANCER'S VIGIL ---
            if request.vigil:
                vigil_artisan = ChronomancerVigil(self, scripture_path, request, true_sanctum)
                vigil_artisan.conduct()
                return self.success("The Sentinel's vigil has concluded purely.")

            # --- MOVEMENT IX: THE PROPHET'S ADJUDICATION ---
            initial_rite = language or self.prophet.divine_intent(scripture_path, scripture_content)
            final_rite = self.prophet.adjudicate_reality(initial_rite)

            if not request.silent:
                self.logger.info(f"[{trace_id}] Universal Conductor perceives a '[cyan]{final_rite}[/cyan]' rite.")

            # --- MOVEMENT X: THE GNOSTIC TRIAGE ---
            is_internal_gnostic = final_rite in self.bridge.DELEGATION_GRIMOIRE
            if is_internal_gnostic:
                plan = ExecutionPlan(interpreter_cmd=[], strategy='internal', docker_image=None)
            else:
                # [ASCENSION 1]: LAZY MANAGER SUMMONS
                plan = self.manager.resolve_execution_plan(
                    language=final_rite, runtime_spec=request.runtime, sanctum=true_sanctum
                )

            # --- MOVEMENT XI: THE TRANSACTIONAL HEART ---
            chronicle_altering_rites = {'patch', 'transmute', 'genesis', 'arch', 'form'}
            transaction_name = f"Run: {scripture_path.name}"

            if final_rite in chronicle_altering_rites:
                with GnosticTransaction(true_sanctum, transaction_name, blueprint_path=scripture_path) as tx:
                    result = self.bridge.delegate(final_rite, scripture_path, request, plan)
            else:
                result = self.bridge.delegate(final_rite, scripture_path, request, plan)

            # --- MOVEMENT XII: THE LUMINOUS HERALD ---
            if result.success and not is_internal_gnostic and final_rite in chronicle_altering_rites:
                self._proclaim_dossier(result, final_rite, scripture_path, true_sanctum, start_time, request)

            # [ASCENSION 9]: Finality Haptics
            if result.success:
                result.ui_hints = {**getattr(result, 'ui_hints', {}), "vfx": "bloom", "color": "#64ffda"}

            return result

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW (FAIL-PATH)
            return self._handle_catastrophe(catastrophic_paradox, trace_id)

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _conduct_void_apotheosis(self, request: RunRequest, sanctum: Path, trace: str) -> ScaffoldResult:
        """[ASCENSION 6/7]: Automatically resurrects reality in empty sanctums."""
        try:
            entries = [p for p in sanctum.iterdir() if not p.name.startswith('.')]
            is_empty = len(entries) == 0
        except Exception:
            is_empty = True

        if is_empty:
            self.logger.info(f"[{trace}] Void Detected. Summoning Inception...")
            return self.engine.dispatch(InitRequest(**request.model_dump()))

        elif not (sanctum / "scaffold.scaffold").exists():
            self.logger.info(f"[{trace}] Unmanaged Reality. Summoning Distiller...")
            distill_req = DistillRequest.model_validate(request.model_dump(exclude={'target'}))
            distill_req.source_path = "."
            distill_req.output = "scaffold.scaffold"
            return self.engine.dispatch(distill_req)

        return self.failure("Intent Void: Run rite requires a target scripture or POSIX edict.")

    def _conduct_ephemeral_strike(self, request: RunRequest, target: str, sanctum: Path) -> ScaffoldResult:
        """[ASCENSION 15]: High-fidelity '--temp' mode with total cleanup."""
        self.logger.info("Conducting rite in an Ephemeral Sanctum (Dry-Clean)...")
        with tempfile.TemporaryDirectory(prefix="scaffold-dry-clean-") as temp_dir:
            temp_path = Path(temp_dir)
            if target and (sanctum / target).is_file():
                shutil.copy2(sanctum / target, temp_path / target)

            new_req = request.model_copy(deep=True)
            new_req.project_root = temp_path
            new_req.temp = False
            return self.execute(new_req)

    def _proclaim_dossier(self, result, rite, path, sanctum, start, req):
        """[ASCENSION 8]: Proclaims the cinematic success dossier."""
        registers = SimpleNamespace(
            get_duration=lambda: time.monotonic() - start,
            files_forged=len(result.artifacts),
            sanctums_forged=len([a for a in result.artifacts if a.type == 'directory']),
            bytes_written=sum(getattr(a, 'size_bytes', 0) for a in result.artifacts),
            no_edicts=req.no_edicts,
        )
        proclaim_apotheosis_dossier(
            telemetry_source=registers, gnosis={"project_type": f"Rite: {rite}", **req.variables},
            project_root=sanctum, title=f"✨ {rite.upper()} COMPLETE ✨",
            subtitle=f"The will inscribed in '{path.name}' is manifest."
        )

    def _handle_catastrophe(self, error, trace) -> ScaffoldResult:
        """[ASCENSION 12]: THE FORENSIC CORONER."""
        tb = traceback.format_exc()
        self.logger.error(f"[{trace}] Conductor Fracture: {error}")
        if isinstance(error, ArtisanHeresy): raise error
        raise ArtisanHeresy(
            f"Catastrophic Paradox in Run Conductor: {str(error)}",
            details=f"Traceback:\n{tb}", severity=HeresySeverity.CRITICAL, trace_id=trace
        )

    def __repr__(self) -> str:
        return f"<Ω_RUN_CONDUCTOR status=RESONANT substrate={'WASM' if self.is_wasm else 'IRON'}>"