# Path: scaffold/artisans/weave/weaver.py
# ---------------------------------------

import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

from rich.prompt import Confirm

from ...core.alchemist import get_alchemist
from ...core.kernel.transaction import GnosticTransaction
from ...core.kernel.archivist import GnosticArchivist
from ...contracts.data_contracts import ScaffoldItem, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import WeaveRequest
from ...logger import Scribe
from ...parser_core.parser import ApotheosisParser
from ...utils import (
    atomic_write,
    resolve_gnostic_content_v2,
    perform_alchemical_resolution,
    is_binary
)
from ...communion import conduct_sacred_dialogue, GnosticPlea, GnosticPleaType
from ...artisans.patch.mutators import GnosticMutator
from ...artisans.patch.contracts import MutationOp

Logger = Scribe("GnosticWeaver")


class GnosticWeaver:
    """
    =================================================================================
    == THE OMNISCIENT WEAVER (V-Ω-SYNTHESIZE-THEN-INSCRIBE)                        ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The Weaver's mind is now whole. It is the God-Engine of Architectural Composition.
    It understands the **Law of Synthesis**: before touching the mortal realm, it
    forges the complete soul of the file in memory, merging templates, seeds, and
    mutations into a single, luminous reality.

    ### THE PANTHEON OF 13 ASCENDED FACULTIES:

    1.  **The Law of Synthesis:** It never performs a partial write. It calculates
        the final state of a file (Base + Mutation) in memory before inscription.
    ...
    12. **The Safety Interlock:** It raises a Critical Heresy if a mutation operator
        is unrecognized, preventing the catastrophic "Default to Overwrite" behavior.
    13. **The Parser Healer:** Checks raw scripture for missed operators (`+=`) and
        self-corrects to prevent accidental overwrites.
    =================================================================================
    """

    def __init__(self, engine, project_root: Path):
        self.engine = engine
        self.project_root = project_root
        self.alchemist = get_alchemist()
        from ..template_engine import TemplateEngine
        self.template_engine = TemplateEngine(project_root=self.project_root, silent=True)

    def conduct(self, archetype_path: Path, request: WeaveRequest) -> ScaffoldResult:
        """The Grand Rite of Weaving."""
        is_simulation = request.dry_run or request.preview
        if not request.force and not is_simulation: self._check_git_cleanliness()

        # --- MOVEMENT I: THE PARSING OF THE ARCHETYPE ---
        parser = ApotheosisParser(grammar_key='scaffold')
        try:
            _, items, commands_tuple, _, blueprint_vars, dossier = parser.parse_string(
                archetype_path.read_text(encoding='utf-8'), file_path_context=archetype_path
            )
            commands = [cmd for cmd, _ in commands_tuple]
        except Exception as e:
            raise ArtisanHeresy(f"The Archetype's soul is void or profane: {e}", child_heresy=e)

        # --- MOVEMENT II: THE GATHERING OF GNOSIS ---
        request.variables['target_dir'] = request.target_directory or "."
        known_keys = set(request.variables.keys()) | set(blueprint_vars.keys())
        missing_vars = dossier.required - known_keys
        unified_gnosis = {**blueprint_vars, **request.variables}

        if missing_vars and not request.non_interactive:
            pleas = [GnosticPlea(key=var, plea_type=GnosticPleaType.TEXT, prompt_text=f"Enter value for '{var}'") for
                     var in sorted(list(missing_vars))]
            success, user_gnosis = conduct_sacred_dialogue(pleas=pleas, title=f"Weaving {archetype_path.stem}")
            if not success: raise ArtisanHeresy("The Rite was stayed by the Architect.")
            unified_gnosis.update(user_gnosis)

        # --- MOVEMENT III: THE ALCHEMICAL RESOLUTION ---
        final_vars = perform_alchemical_resolution(dossier, unified_gnosis, blueprint_vars)
        parser.variables = final_vars

        rebased_items = self._rebase_and_predict_collisions(items, final_vars, request.target_directory or ".")

        collisions = [p for p, _ in rebased_items if p.exists()]
        self._perform_guarded_execution(collisions, request, context=f"weave_{archetype_path.stem}")

        # --- MOVEMENT IV: THE TRANSACTIONAL SYMPHONY ---
        created_artifacts: List[Artifact] = []
        with GnosticTransaction(self.project_root, f"Weave {request.fragment_name}", archetype_path,
                                use_lock=True, simulate=is_simulation) as tx:
            for final_path, item in rebased_items:
                artifact = self._weave_single_item(item, final_path, final_vars, archetype_path, tx, is_simulation,
                                                   request.force)
                if artifact:
                    created_artifacts.append(artifact)

            if commands and not request.no_edicts:
                self._conduct_maestro_edicts(commands, (self.project_root / (request.target_directory or ".")),
                                             final_vars, tx, request.silent, is_simulation)

        # --- MOVEMENT V: THE PURIFICATION AND REGISTRATION ---
        if not is_simulation and not request.no_edicts:
            self._lint_woven_artifacts(created_artifacts)

        if not is_simulation:
            self._register_weave(request.fragment_name, final_vars, created_artifacts)

        return self.engine.success(
            f"Weave complete. {len(created_artifacts)} artifacts processed.",
            artifacts=created_artifacts
        )

    def _rebase_and_predict_collisions(self, items: List[ScaffoldItem], final_vars: Dict, target_dir: str) -> List[
        Tuple[Path, ScaffoldItem]]:
        """A pure helper to calculate final paths before the transaction starts."""
        rebased = []
        target_base = (self.project_root / target_dir).resolve()
        for item in items:
            if not item.path: continue
            transmuted_path_str = self.alchemist.transmute(str(item.path), final_vars)
            clean_path = transmuted_path_str.strip().strip('"\'')
            final_path = (target_base / clean_path).resolve()
            rebased.append((final_path, item))
        return rebased

    def _weave_single_item(self, item: ScaffoldItem, abs_path: Path, variables: Dict, archetype_path: Path,
                           tx: GnosticTransaction, is_simulation: bool, force: bool) -> Optional[Artifact]:
        """
        The Alchemist of Synthesis. Performs Synthesis, Adjudication, and Inscription.
        """
        if item.is_dir:
            if not is_simulation: abs_path.mkdir(parents=True, exist_ok=True)
            return Artifact(path=abs_path, type="directory", action="created")

        # --- MOVEMENT I: THE SYNTHESIS OF THE SOUL ---
        final_content = ""
        action_taken = InscriptionAction.CREATED

        try:
            # [FACULTY 13] The Parser Healer (Critical Safety Net)
            # If the parser failed to detect the mutation op, we check the raw scripture.
            if not item.mutation_op and item.raw_scripture:
                stripped = item.raw_scripture.strip()
                if "+=" in stripped and not stripped.startswith(("#", "//")):
                    Logger.verbose(f"Weaver healed a Parser Heresy: Detected implicit '+=' in '{item.path.name}'.")
                    item.mutation_op = "+="
                elif "-=" in stripped:
                    item.mutation_op = "-="
                elif "~=" in stripped:
                    item.mutation_op = "~="
                elif "^=" in stripped:
                    item.mutation_op = "^="

            # 1. Determine the Mutation Payload
            mutation_payload = None
            if item.mutation_op:
                # [THE FAILSAFE PURIFICATION]
                raw_payload = item.content or ""
                # Replace \""" with """
                raw_payload = re.sub(r'\\"{3}', '"""', raw_payload)
                raw_payload = re.sub(r'(?:\\"|\\"){3}', '"""', raw_payload)
                raw_payload = re.sub(r'(?:\\\\"|\\\\"){3}', '"""', raw_payload)

                mutation_payload = self.alchemist.transmute(raw_payload, variables)

                # [THE RITE OF TEMPORARY VOID]
                original_item_content = item.content
                item.content = None

                # 2. Resolve Base Content (from Template, Seed, or restored '::' definition)
            base_soul_vessel = resolve_gnostic_content_v2(
                item, self.alchemist, self.template_engine, variables,
                sanctum=archetype_path.parent, source_override_map={}
            )
            base_content = self.alchemist.transmute(base_soul_vessel.untransmuted_content, variables)

            # [THE RESTORATION]
            if item.mutation_op:
                item.content = original_item_content

            # 3. The Gnostic Decision (Synthesize vs Mutate Disk)
            if item.mutation_op:
                action_taken = InscriptionAction.TRANSFIGURED

                # A. The Gaze upon Reality
                if abs_path.exists():
                    # Reality exists. We mutate the living soul on disk.
                    original_content = abs_path.read_text(encoding='utf-8', errors='replace')
                    target_content = original_content
                else:
                    # B. The Synthesis in the Void (New File from Base + Mutation)
                    if base_content:
                        target_content = base_content
                    else:
                        self.Logger.warn(
                            f"Mutation target '{abs_path.name}' is a void. Forging new scripture from empty soul.")
                        target_content = ""

                    action_taken = InscriptionAction.CREATED

                # C. The Application of Will
                op_val = item.mutation_op.strip()
                append_val = MutationOp.APPEND.value
                prepend_val = MutationOp.PREPEND.value

                if op_val == append_val or op_val == "+=":
                    final_content = GnosticMutator.apply_text_append(target_content, mutation_payload)
                elif op_val == prepend_val or op_val == "^=":
                    final_content = GnosticMutator.apply_text_prepend(target_content, mutation_payload)
                elif op_val == MutationOp.SUBTRACT.value or op_val == "-=":
                    final_content = GnosticMutator.apply_regex_subtract(target_content, mutation_payload)
                elif op_val == MutationOp.TRANSFIGURE.value or op_val == "~=":
                    final_content = GnosticMutator.apply_regex_transfigure(target_content, mutation_payload)
                else:
                    # [THE SAFETY INTERLOCK]
                    raise ArtisanHeresy(
                        f"Unknown Mutation Operator: '{item.mutation_op}'. The Weaver refuses to guess.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Use += (Append), -= (Subtract), or ~= (Transfigure)."
                    )

            else:
                # No mutation. The soul is simply the resolved Base Content.
                # This IS an overwrite/create operation.
                final_content = base_content

        except Exception as e:
            raise ArtisanHeresy(f"Synthesis failed for '{item.path.name}': {e}", child_heresy=e)

        # --- MOVEMENT II & III: ADJUDICATION & INSCRIPTION ---
        write_result = atomic_write(
            target_path=abs_path,
            content=final_content,
            logger=Logger,
            sanctum=self.project_root,
            transaction=tx,
            force=force,
            verbose=not is_simulation,
            dry_run=is_simulation
        )

        if write_result.success:
            if action_taken != InscriptionAction.CREATED:
                write_result.action_taken = action_taken
            tx.record(write_result)

        if item.permissions and not is_simulation:
            tx.record_edict(f"chmod {item.permissions} {abs_path}")

        return Artifact(
            path=abs_path,
            type="file",
            action=write_result.action_taken.value if write_result.success else "FAILED",
            size_bytes=write_result.bytes_written,
            checksum=write_result.gnostic_fingerprint
        )

    # ... (remaining methods unchanged)
    def _perform_guarded_execution(self, collisions: List[Path], request: WeaveRequest, context: str = "weave"):
        if not collisions or request.force or request.dry_run or request.preview: return
        archivist = GnosticArchivist(self.project_root)
        if request.non_interactive:
            archivist.create_snapshot(collisions, reason=f"auto_{context}")
            return
        if Confirm.ask("[bold question]Forge a safety snapshot before proceeding?[/bold question]", default=True):
            archivist.create_snapshot(collisions, reason=f"manual_{context}")

    def _check_git_cleanliness(self):
        if (self.project_root / ".git").exists():
            import subprocess
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project_root).decode()
                if status.strip():
                    Logger.warn("Git Sentinel: Sanctum is dirty. Uncommitted changes may be mixed with Weave.")
            except:
                pass

    def _register_weave(self, archetype: str, variables: Dict, artifacts: List[Artifact]):
        registry_path = self.project_root / ".scaffold" / "weaves.json"
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        record = {"timestamp": time.time(), "archetype": archetype, "variables": variables,
                  "files_touched": [str(a.path.relative_to(self.project_root)) for a in artifacts]}
        history = []
        if registry_path.exists():
            try:
                history = json.loads(registry_path.read_text())
            except:
                pass
        history.append(record)
        registry_path.write_text(json.dumps(history, indent=2))

    def _conduct_maestro_edicts(self, commands: List[str], target_base: Path, variables: Dict, tx: GnosticTransaction,
                                silent: bool, is_simulation: bool):
        from ...core.maestro import MaestroConductor as MaestroUnit
        from ...creator.registers import QuantumRegisters
        from ...core.sanctum.local import LocalSanctum
        vars_with_context = variables.copy()
        vars_with_context["SCAFFOLD_TARGET_DIR"] = str(target_base)
        regs = QuantumRegisters(sanctum=LocalSanctum(target_base), project_root=target_base, transaction=tx,
                                gnosis=vars_with_context, silent=silent, dry_run=is_simulation)
        maestro = MaestroUnit(regs, self.alchemist)
        for cmd in commands:
            maestro.execute(cmd)
            tx.record_edict(cmd)

    def _lint_woven_artifacts(self, artifacts: List[Artifact]):
        import shutil, subprocess
        files = [str(a.path) for a in artifacts if a.type == 'file' and a.action != 'FAILED']
        if not files: return
        if shutil.which("ruff"):
            py_files = [f for f in files if f.endswith('.py')]
            if py_files:
                subprocess.run(["ruff", "check", "--fix"] + py_files, cwd=self.project_root, stderr=subprocess.DEVNULL)
        if shutil.which("prettier"):
            js_files = [f for f in files if f.endswith(('.js', '.ts', '.tsx', '.json', '.md'))]
            if js_files:
                subprocess.run(["prettier", "--write"] + js_files, cwd=self.project_root, stderr=subprocess.DEVNULL)