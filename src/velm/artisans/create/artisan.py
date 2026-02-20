# Path: src/velm/artisans/create/artisan.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: SUPREME_MATERIALIZATION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CREATE_ARTISAN_V3000_TOTALITY_FINALIS

import subprocess
import shutil
import os
import time
import uuid
import traceback
from contextlib import nullcontext
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Final

from rich.prompt import Confirm

from .builder import GnosticBuilder
from .safety import CreationGuardian
from ...contracts.data_contracts import ScaffoldItem
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.artisan import BaseArtisan
from ...core.assembler.engine import AssemblerEngine
from ...core.kernel.transaction import GnosticTransaction
from ...interfaces.base import ScaffoldResult, Artifact

# [ASCENSION 15]: THE ALCHEMICAL UPLINK
from ...core.alchemist import get_alchemist
from ...interfaces.requests import CreateRequest
from ...logger import Scribe
from ...creator import create_structure

Logger = Scribe("CreateArtisan")


class CreateArtisan(BaseArtisan[CreateRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF SENTIENT CREATION (V-Ω-TOTALITY-V3000)                    ==
    =================================================================================
    The Alpha and the Omega of Materialization. It transmutes pure Architectural
    Will into the Matter of the Filesystem.
    """

    def execute(self, request: CreateRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND RITE OF KINETIC INCEPTION (EXECUTE)                           ==
        =============================================================================
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: ORGAN MATERIALIZATION ---
        # [ASCENSION 1, 5, 13]: Awakening the internal conductors
        builder = GnosticBuilder(self.project_root, self.engine)
        guardian = CreationGuardian(self.project_root, self.console)

        # Determine the physics of the rite
        is_raw_mode = request.variables.get('raw', False) or getattr(request, 'raw', False)
        is_simulation = request.dry_run or request.preview or request.audit
        trace_id = getattr(request, 'trace_id', f"tr-create-{uuid.uuid4().hex[:6].upper()}")

        # [ASCENSION 13]: METABOLIC TRIAGE
        # Scry the hardware load before the strike
        vitals = self.engine.watchdog.get_vitals()
        if vitals.get("load_percent", 0) > 95.0:
            return self.failure(
                message="Metabolic Panic: Host is overloaded. Strike stayed for safety.",
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT I: THE PROPHETIC FORGE (PLANNING) ---
        # [ASCENSION 15]: The Alchemist is engaged here inside builder.forge_plan
        # resolving the "Silent Clock" heresy.
        scaffold_items = builder.forge_plan(request)

        if not scaffold_items:
            return self.success("The Void was summoned, but no form was willed.")

        # [ASCENSION 12]: TEST ENGINE GOVERNANCE
        if getattr(request, 'no_tests', False):
            scaffold_items = self._purge_shadow_twins(scaffold_items)

        # --- MOVEMENT II: THE PRE-FLIGHT INQUEST (ADJUDICATION) ---

        # 1. [ASCENSION 19]: THE DEPENDENCY ORACLE
        if request.needs and not is_raw_mode:
            guardian.adjudicate_dependencies(request.needs, auto_install=request.non_interactive)

        # 2. THE COLLISION GAZE
        collisions = guardian.detect_collisions(scaffold_items)

        # 3. [ASCENSION 22]: THE GIT SENTINEL
        if not request.force and not is_simulation:
            self._adjudicate_git_status()

        # 4. THE GUARDIAN'S VOW (BACKUPS)
        # Wrap collisions in a safety ward.
        self.guarded_execution(collisions, request, context="create")

        # 5. CONFLICT RESOLUTION
        if not request.force and not request.non_interactive:
            scaffold_items = guardian.resolve_conflicts(scaffold_items)

        if not scaffold_items:
            return self.success("Rite stayed. No scriptures remain to be forged.")

        # --- MOVEMENT III: THE ATOMIC STRIKE (MATERIALIZATION) ---
        modified_artifacts: List[Path] = []

        # [ASCENSION 17]: HUD RADIATION
        self._radiate_hud_pulse("INCEPTION_START", "#64ffda", trace_id)

        try:
            # We descend into the Cinematic Live mode unless the Vow of Silence is manifest.
            status_msg = f"[bold green]Conducting Inception: {len(scaffold_items)} shards...[/]"
            with self.console.status(status_msg) if not request.silent else nullcontext():

                # [ASCENSION 3]: THE TRANSACTIONAL WOMB
                tx_name = f"Rite of Creation: {trace_id[:8]}"
                with GnosticTransaction(self.project_root, tx_name, use_lock=True, simulate=is_simulation) as tx:

                    # [ASCENSION 11]: ATOMIC SANCTUM FORGING
                    self._forge_parent_sanctums(scaffold_items)

                    # [ASCENSION 9]: CONSECRATE PERMISSIONS
                    for item in scaffold_items:
                        builder.consecrate_permissions(item)

                    # [STRIKE]: Transmute Logic into Matter
                    create_structure(
                        scaffold_items=scaffold_items,
                        base_path=self.project_root,
                        transaction=tx,
                        args=request
                    )

                    # [ASCENSION 19]: HYDRAULIC COMMITMENT
                    if not is_simulation:
                        self._force_physical_commitment(scaffold_items)

                    # --- MOVEMENT IV: THE RITE OF ASSEMBLY ---
                    # [ASCENSION 8]: Woven logic integration
                    if not is_raw_mode and not getattr(request, 'no_assemble', False):
                        modified_artifacts = self._conduct_assembly(scaffold_items, request, tx)

                    # [ASCENSION 14]: THE SKELETON EATER (FINAL LUSTRATION)
                    # The hollow-sanctum fix is applied during the tx.materialize()
                    # phase inside the kernel's committer.
                    if not is_simulation:
                        tx.materialize()

            # --- MOVEMENT V: POST-FLIGHT CONSECRATION ---

            created_relative_paths = [item.path for item in scaffold_items if not item.is_dir]
            created_files = [(self.project_root / p).resolve() for p in created_relative_paths]

            # [ASCENSION 6, 7]: THE MASTER'S MEMORY
            if request.teach and created_files:
                self._conduct_teaching_rite(builder, request.teach, created_files[0])

            # [ASCENSION 24]: THE EDITOR SUMMONS
            if request.edit and not getattr(request, 'no_open', False):
                guardian.summon_editor(created_files + modified_artifacts)

            # --- MOVEMENT VI: THE LUMINOUS DOSSIER ---
            duration_s = (time.perf_counter_ns() - start_ns) / 1_000_000_000

            # [ASCENSION 17]: HUD SUCCESS
            self._radiate_hud_pulse("INCEPTION_COMPLETE", "#10b981", trace_id)

            return self.success(
                message=f"Apotheosis achieved. {len(created_files)} forged, {len(modified_artifacts)} woven.",
                data={
                    "created_count": len(created_files),
                    "modified_count": len(modified_artifacts),
                    "duration_seconds": duration_s,
                    "trace_id": trace_id
                },
                artifacts=[Artifact(path=f, type="file", action="created") for f in created_files] +
                          [Artifact(path=f, type="file", action="modified") for f in modified_artifacts],
                ui_hints={"vfx": "bloom", "sound": "ignition_complete"}
            )

        except Exception as catastrophic_paradox:
            # [ASCENSION 24]: THE FINALITY VOW (Forensic Autopsy)
            self._radiate_hud_pulse("INCEPTION_FRACTURED", "#ef4444", trace_id)
            Logger.critical(f"Inception Symphony Fractured: {catastrophic_paradox}")

            return self.failure(
                message=f"Creation Fracture: {str(catastrophic_paradox)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake", "sound": "fracture_alert"}
            )

    # =========================================================================
    # == INTERNAL RITES (THE CONDUCTOR'S FACULTIES)                          ==
    # =========================================================================

    def _adjudicate_git_status(self):
        """[ASCENSION 22]: Git Sentinel Vigil."""
        if (self.project_root / ".git").exists():
            try:
                status = subprocess.check_output(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
                )
                if status.strip():
                    Logger.warn("Git Sentinel: The sanctum is dirty. Entropy is present.")
                    if not self.non_interactive:
                        if not Confirm.ask("Proceed with the strike anyway?", default=False):
                            raise ArtisanHeresy("Rite stayed by Git Sentinel.", exit_code=0)
            except Exception:
                pass

    def _forge_parent_sanctums(self, items: List[ScaffoldItem]):
        """[ASCENSION 11]: Atomic Path Awareness."""
        for item in items:
            if not item.path: continue
            target_abs = (self.project_root / item.path).resolve()

            # Security Ward: Verify target is within project root
            if not str(target_abs).startswith(str(self.project_root)):
                raise ArtisanHeresy(f"Sanctum Breach: Path '{item.path}' escapes the project root.")

            parent = target_abs if item.is_dir else target_abs.parent
            if not parent.exists():
                Logger.verbose(f"Forging Sanctum: {parent.relative_to(self.project_root)}")
                parent.mkdir(parents=True, exist_ok=True)

    def _force_physical_commitment(self, items: List[ScaffoldItem]):
        """[ASCENSION 19]: Inode Synchronization."""
        for item in items:
            if item.is_dir or not item.path: continue
            target_abs = (self.project_root / item.path).resolve()
            if target_abs.exists():
                try:
                    # Open and flush to force physical write-back
                    fd = os.open(target_abs, os.O_RDONLY)
                    try:
                        os.fsync(fd)
                    finally:
                        os.close(fd)
                except OSError:
                    pass

    def _conduct_assembly(self, items: List[ScaffoldItem], request: CreateRequest, tx: GnosticTransaction) -> List[
        Path]:
        """[ASCENSION 8]: Weaves the new matter into the existing tapestry."""
        Logger.info("The Gnostic Assembler awakens to weave connections...")
        assembler = AssemblerEngine(self.project_root)
        return assembler.assemble(
            items,
            request.variables,
            transaction=tx,
            dry_run=request.dry_run
        )

    def _conduct_teaching_rite(self, builder: GnosticBuilder, key: str, path: Path):
        """[ASCENSION 6]: Patterns captured for the Akasha."""
        if path.exists():
            builder.conduct_teaching_rite(key, path)
        else:
            Logger.warn(f"Teaching Rite aborted: Scripture '{path.name}' is unmanifest.")

    def _purge_shadow_twins(self, items: List[ScaffoldItem]) -> List[ScaffoldItem]:
        """[ASCENSION 12]: Adjudicates the Vow of No Tests."""
        Logger.verbose("Vow of No Tests perceived. Purging Shadow Twins...")
        return [
            i for i in items
            if not (i.path and any(str(i.path).endswith(s) for s in ('.test.ts', '.spec.ts', '_test.py')))
               and not (i.path and i.path.name.startswith('test_'))
        ]

    def _radiate_hud_pulse(self, type_label: str, color: str, trace: str):
        """[ASCENSION 17]: Atmospheric Telemetry."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "KINETIC_INCEPTION",
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_CREATE_ARTISAN substrate='IRON' status=RESONANT>"