# Path: scaffold/artisans/create/artisan.py
# --------------------------------
# LIF: ∞ (ETERNAL & ABSOLUTE)
#
# HERESY ANNIHILATED: The Muffled Voice & The Fractured Conscience
# ASCENSIONS: Recursive Pathing, Test Governance, Atomic Persistence.

import subprocess
import shutil
import os
from pathlib import Path
from typing import List

from rich.prompt import Confirm

from .builder import GnosticBuilder
from .safety import CreationGuardian
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.artisan import BaseArtisan
from ...core.assembler.engine import AssemblerEngine
from ...core.kernel.transaction import GnosticTransaction
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import CreateRequest
from ...logger import Scribe
from ...creator import create_structure

Logger = Scribe("CreateArtisan")


class CreateArtisan(BaseArtisan[CreateRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF SENTIENT CREATION (V-Ω-SOVEREIGN-GUARDIAN)                ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The Alpha and the Omega of file generation, now ascended to its final form. It is
    the Sovereign Guardian, the High Priest of Ad-Hoc Creation, and a true AI
    Co-Architect, orchestrating the entire Materialization Symphony from a single,
    unbreakable sanctum of Gnostic will.

    ### THE PANTHEON OF 12 GAME-CHANGING ASCENSIONS:

    1.  **The Sovereign Guardian:** It has absorbed the full consciousness of the
        `PreFlightGuardian`. All safety checks, interactive dialogues, and pre-flight
        inquests now live here.

    2.  **The AI Co-Architect's Hand:** Can be commanded with `--ai-edit` to transmute
        boilerplate into bespoke reality.

    3.  **The Chronomancer's Vow:** The entire rite is now wrapped in a named, atomic
        `GnosticTransaction`.

    4.  **The Quantum Prophet:** Supports `--preview` for non-destructive simulation.

    5.  **The Gnostic Compass:** Possesses hyper-aware spatial intelligence for context-aware
        creation.

    6.  **The Master's Memory (`--teach`):** Summons an AI Alchemist to reverse-engineer
        Gnosis from created files.

    7.  **The Alchemical Dialogue:** Conducts JIT Sacred Dialogue for undefined template variables.

    8.  **The Sentient Weaver:** Supports `--no-assemble` to skip wiring logic.

    9.  **The Gnostic Kit Expander:** Supports `--kit` for multi-file pattern weaving.

    10. **The Polyglot Soul:** Aware of language-specific post-flight validation.

    11. **The Recursive Path Awareness (Atomic Sanctum):** Ensures all parent directories
        exist before inscription, preventing "No such file" heresies.

    12. **The Test Engine Governance:** Respects `--no-tests` to suppress shadow twins.
    """

    def execute(self, request: CreateRequest) -> ScaffoldResult:
        # 1. Consecrate the Sub-Artisans
        builder = GnosticBuilder(self.project_root, self.engine)
        guardian = CreationGuardian(self.project_root, self.console)

        is_raw_mode = request.variables.get('raw', False) or getattr(request, 'raw', False)
        is_genesis_rite = getattr(request, 'is_genesis_rite', False)

        # --- MOVEMENT I: THE FORGING OF THE PLAN (THE BUILDER'S WILL) ---
        scaffold_items = builder.forge_plan(request)
        if not scaffold_items:
            return self.success("The Void was summoned, but no form emerged.")

        # [ASCENSION XII] Test Engine Governance
        # If the Architect has spoken the Vow of No Tests, we purge them from the plan.
        if getattr(request, 'no_tests', False):
            Logger.verbose("Vow of No Tests perceived. Purging Shadow Twins...")
            original_count = len(scaffold_items)
            scaffold_items = [
                item for item in scaffold_items
                if not (item.path and (
                        str(item.path).endswith('.test.ts') or
                        str(item.path).endswith('.spec.ts') or
                        str(item.path).endswith('_test.py') or
                        str(item.path).startswith('test_')
                ))
            ]
            purged_count = original_count - len(scaffold_items)
            if purged_count > 0:
                Logger.info(f"Purged {purged_count} test scriptures from the manifest.")

        created_relative_paths = [item.path for item in scaffold_items if not item.is_dir]

        # --- MOVEMENT II: THE PRE-FLIGHT INQUEST (THE GUARDIAN'S GAZE) ---

        # 1. The Dependency Oracle
        if request.needs and not is_raw_mode:
            guardian.adjudicate_dependencies(request.needs, auto_install=request.non_interactive)

        # 2. Collision Detection
        collisions = guardian.detect_collisions(scaffold_items)

        # 3. The Git Sentinel (Annihilating the Muffled Voice Heresy)
        if not request.force and not request.dry_run and not request.preview:
            if (self.project_root / ".git").exists():
                try:
                    status = subprocess.check_output(
                        ["git", "status", "--porcelain"],
                        cwd=self.project_root,
                        text=True,
                        stderr=subprocess.DEVNULL
                    ).decode()
                    if status.strip():
                        Logger.warn("Git Sentinel: The sanctum is dirty. Uncommitted changes may be lost.")
                        if not request.non_interactive:
                            if not Confirm.ask("Proceed anyway?", default=False):
                                raise ArtisanHeresy("Rite stayed by Git Sentinel.", exit_code=0)
                except Exception:
                    pass

        # 4. The Guardian's Offer (Backup)
        self.guarded_execution(collisions, request, context="create")

        # 5. Conflict Resolution (The Architect's Will)
        if not request.force:
            scaffold_items = guardian.resolve_conflicts(scaffold_items)

        if not scaffold_items:
            return self.success("Rite stayed. No scriptures remain to be forged.")

        modified_artifacts = []

        # --- THE SYMPHONY OF MATERIALIZATION BEGINS ---
        # Only now, after all questions are answered, does the veil of the spinner descend.
        with self.console.status("[bold green]The Great Work is advancing...[/bold green]"):
            with GnosticTransaction(self.project_root, "Rite of Ad-Hoc Creation", use_lock=True) as tx:

                # --- [ASCENSION XI] ATOMIC SANCTUM MATERIALIZATION (RECURSIVE PATH AWARENESS) ---
                # Before any file is inscribed, we ensure its sanctuary exists.
                for item in scaffold_items:
                    if item.path:
                        target_abs = (self.project_root / item.path).resolve()
                        if item.is_dir:
                            if not target_abs.exists():
                                Logger.verbose(f"Materializing Sanctum: {item.path}")
                                target_abs.mkdir(parents=True, exist_ok=True)
                        else:
                            parent_sanctum = target_abs.parent
                            if not parent_sanctum.exists():
                                Logger.verbose(f"Materializing Parent Sanctum: {parent_sanctum}")
                                parent_sanctum.mkdir(parents=True, exist_ok=True)

                # --- MOVEMENT III: THE RITE OF MATERIALIZATION ---
                for item in scaffold_items:
                    builder.consecrate_permissions(item)

                create_structure(
                    scaffold_items=scaffold_items,
                    base_path=self.project_root,
                    transaction=tx,
                    args=request
                )

                # --- [ASCENSION: THE PHANTOM WRITE CHECK] ---
                # We perform a manual fsync to ensure the OS has physically engaged the platter.
                if not request.dry_run:
                    for item in scaffold_items:
                        if not item.is_dir and item.path:
                            try:
                                target_abs = (self.project_root / item.path).resolve()
                                if target_abs.exists():
                                    # Open in append mode just to get a descriptor to sync
                                    with open(target_abs, 'a') as f:
                                        f.flush()
                                        os.fsync(f.fileno())
                            except OSError:
                                pass

                # --- MOVEMENT IV: THE RITE OF ASSEMBLY ---
                if not is_raw_mode and not is_genesis_rite:
                    # Check for explicit suppression of assembly
                    if not getattr(request, 'no_assemble', False):
                        Logger.info("The Gnostic Assembler awakens to weave connections...")
                        assembler = AssemblerEngine(self.project_root)
                        modified_artifacts = assembler.assemble(
                            scaffold_items,
                            request.variables,
                            transaction=tx,
                            dry_run=request.dry_run
                        )

        # --- MOVEMENT V: POST-RITE ACTIONS ---
        created_files = [(self.project_root / p).resolve() for p in created_relative_paths]

        if request.teach and created_files:
            # [ASCENSION 13]: THE TEACHING SAFEGUARD
            # We check if the file actually exists before trying to learn from it.
            # This prevents the [WinError 2] crash if the write was blocked.
            target_file = created_files[0]
            if target_file.exists():
                builder.conduct_teaching_rite(request.teach, target_file)
            else:
                Logger.warn(
                    f"Teaching Rite Skipped: The scripture '{target_file.name}' did not materialize. (Likely blocked by Security Sentinel)")

        # [ASCENSION I] The Editor Suppression Vow
        # We check for the --no-open flag before summoning the editor.
        should_open = request.edit
        if getattr(request, 'no_open', False):
            should_open = False
            Logger.verbose("Editor summons suppressed by --no-open vow.")

        if should_open and (created_files or modified_artifacts):
            guardian.summon_editor(created_files + modified_artifacts)

        # --- MOVEMENT VI: THE LUMINOUS DOSSIER ---
        artifacts = [Artifact(path=f, type="file", action="created") for f in created_files]
        artifacts.extend([Artifact(path=f, type="file", action="modified") for f in modified_artifacts])

        mode_msg = " (Raw)" if is_raw_mode else " (Intelligent)"
        return self.success(
            f"Rite complete{mode_msg}. {len(created_files)} forged, {len(modified_artifacts)} woven.",
            data={"created": len(created_files), "modified": len(modified_artifacts)},
            artifacts=artifacts
        )