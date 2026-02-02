# Path: scaffold/artisans/patch/artisan.py
# ----------------------------------------

import difflib
from collections import defaultdict
from typing import Dict, List, Any
from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from .contracts import MutationOp, MutationEdict
from .mutators import GnosticMutator
from .parser import PatchParser
from ...contracts.data_contracts import InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.artisan import BaseArtisan
from ...core.kernel.transaction import GnosticTransaction
from ...creator.io_validators import SyntaxInquisitor
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import PatchRequest
from ...utils import atomic_write, hash_file

# --- THE JURISPRUDENCE ASCENSION ---
from ...core.jurisprudence.adjudicator import VowAdjudicator
from ...core.jurisprudence.contracts import AdjudicationContext


class PatchArtisan(BaseArtisan[PatchRequest]):
    """
    =================================================================================
    == THE GNOSTIC SURGEON (V-Ω-SEMANTIC-AWARE-ULTIMA)                             ==
    =================================================================================
    LIF: ∞ (THE MASTER OF MUTATION)

    The Master of Mutation. Now ascended to perceive the **Semantic Selector**.
    It distinguishes between a crude text append and a surgical AST insertion.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **The Semantic Switch:** If an Edict carries a `semantic_selector` (e.g. `@inside`),
        the Surgeon delegates to the `SemanticRouter` via `GnosticMutator`.
    2.  **The Adjudicator's Pause:** Before any cut is made, it runs `??` Vows against
        the *virtual state* of the file in memory.
    3.  **The Anchor Hash:** Verifies the file hasn't drifted before touching it.
    4.  **The Transactional Womb:** All cuts happen in a rollback-safe transaction.
    5.  **The Syntax Guard:** Validates the file *after* mutation to ensure no
        syntax errors were introduced.
    """

    def execute(self, request: PatchRequest) -> ScaffoldResult:
        # [ASCENSION]: AD-HOC MUTATION TRIAGE
        # If the Architect specifies --prepend or --append, we treat 'patch_path'
        # as the TARGET FILE, not a patch scripture.
        # We perform a safe getattr to handle Pydantic models gracefully.
        prepend_content = getattr(request, 'prepend', None)
        append_content = getattr(request, 'append', None)

        # Flag to track if we are in Ad-Hoc mode
        is_ad_hoc = False
        patch_path = Path(request.patch_path)  # Default, might be overwritten or virtualized

        if prepend_content or append_content:
            is_ad_hoc = True
            # --- MODE A: AD-HOC SURGERY (Direct Injection) ---
            target_file = request.patch_path  # In this mode, the arg is the target
            edicts = []

            if prepend_content:
                edicts.append(MutationEdict(
                    path=target_file,
                    mutation_op=MutationOp.PREPEND,
                    content=prepend_content,
                    line_num=0
                ))

            if append_content:
                edicts.append(MutationEdict(
                    path=target_file,
                    mutation_op=MutationOp.APPEND,
                    content=append_content,
                    line_num=0
                ))

            variables = request.variables
            patch_name = "Ad-Hoc Mutation"

            # For ad-hoc, patch_path refers to the target file, but GnosticTransaction expects a blueprint path.
            # We use a virtual path for the transaction log.
            patch_path = Path("ad-hoc-mutation.patch")

        else:
            # --- MODE B: SCRIPTURE INTERPRETATION (Standard) ---
            patch_path = (self.project_root / request.patch_path).resolve()
            if not patch_path.is_file():
                return self.failure(f"Patch scripture not found: {patch_path}")

            content = patch_path.read_text(encoding='utf-8')
            parser = PatchParser(request.variables)
            edicts, variables = parser.parse(content, patch_path)
            patch_name = patch_path.name

            # In standard mode, parser.dossier is available
            parser_dossier = parser.dossier

        # Handle dossier for ad-hoc mode
        if is_ad_hoc:
            parser_dossier = {}

        self.logger.info(f"The Surgeon perceives {len(edicts)} edict(s) of mutation.")

        # --- MOVEMENT II: THE GROUPING OF INTENT ---
        edicts_by_file = defaultdict(list)
        for edict in edicts:
            edicts_by_file[edict.path].append(edict)

        targets = [self.project_root / p for p in edicts_by_file.keys()]
        self.guarded_execution(targets, request, context="patch")

        is_simulation = request.dry_run or getattr(request, 'preview', False)

        # --- MOVEMENT III: THE TRANSACTIONAL SYMPHONY ---
        with GnosticTransaction(
                self.project_root,
                f"Patch: {patch_name}",
                patch_path,
                simulate=is_simulation
        ) as tx:

            for rel_path, file_edicts in edicts_by_file.items():
                target_path = self.project_root / rel_path

                # 1. Load Reality
                current_content = ""
                if target_path.exists():
                    current_content = target_path.read_text(encoding='utf-8')

                # [Anchor Hash Check]
                if file_edicts[0].anchor_hash and target_path.exists():
                    current_hash = hash_file(target_path)
                    if not current_hash.startswith(file_edicts[0].anchor_hash):
                        raise ArtisanHeresy(
                            f"Anchor Mismatch for '{rel_path}'. "
                            f"Expected {file_edicts[0].anchor_hash}, found {current_hash[:8]}. "
                            "The file has drifted; patching is unsafe."
                        )

                # 2. Apply Mutations in Memory (The Virtual Buffer)
                working_content = current_content
                action_taken = InscriptionAction.TRANSFIGURED

                for edict in file_edicts:
                    # --- MOVEMENT IV: THE RITE OF ADJUDICATION ---
                    if edict.vows:
                        context = AdjudicationContext(
                            project_root=self.project_root,
                            variables=variables,
                            file_content_buffer=working_content,  # <--- The Virtual Reality
                            target_file_path=target_path
                        )
                        adjudicator = VowAdjudicator(context)

                        for vow_str in edict.vows:
                            self.logger.verbose(f"Adjudicating Vow for {rel_path}: {vow_str}")
                            adjudicator.adjudicate(vow_str, line_num=edict.line_num)
                    # ---------------------------------------------

                    # Variable Injection
                    injection_vars = variables.copy()
                    injection_vars['original'] = working_content

                    if edict.content:
                        fragment = self.engine.alchemist.transmute(edict.content, injection_vars)
                    else:
                        fragment = ""

                    # --- THE GNOSTIC DISPATCH (SEMANTIC VS TEXTUAL) ---

                    if edict.mutation_op == MutationOp.DEFINE:
                        working_content = fragment
                        action_taken = InscriptionAction.CREATED

                    elif not target_path.exists():
                        self.logger.warn(f"Skipping mutation on void '{rel_path}'.")
                        continue

                    # [THE DIVINE BRANCH: SEMANTIC SURGERY]
                    elif edict.semantic_selector:
                        self.logger.verbose(f"Performing Semantic Surgery on '{rel_path}' ({edict.semantic_selector})")
                        try:
                            working_content = GnosticMutator.apply_semantic_insert(
                                original=working_content,
                                fragment=fragment,
                                selector=edict.semantic_selector,
                                file_path=target_path
                            )
                            action_taken = InscriptionAction.SYMBIOTIC_MERGE
                        except Exception as e:
                            # Fallback or hard fail? Hard fail ensures we don't corrupt code.
                            raise ArtisanHeresy(f"Semantic Surgery Failed on '{rel_path}': {e}",
                                                line_num=edict.line_num, child_heresy=e)

                    # [STANDARD TEXTUAL / REGEX SURGERY]
                    elif edict.mutation_op == MutationOp.APPEND:
                        if edict.is_structural:
                            working_content = GnosticMutator.apply_structural_merge(
                                working_content, fragment, target_path.suffix
                            )
                            action_taken = InscriptionAction.SYMBIOTIC_MERGE
                        else:
                            working_content = GnosticMutator.apply_text_append(working_content, fragment)

                    elif edict.mutation_op == MutationOp.PREPEND:
                        working_content = GnosticMutator.apply_text_prepend(working_content, fragment)

                    elif edict.mutation_op == MutationOp.SUBTRACT:
                        working_content = GnosticMutator.apply_regex_subtract(working_content, fragment)

                    elif edict.mutation_op == MutationOp.TRANSFIGURE:
                        working_content = GnosticMutator.apply_regex_transfigure(working_content, fragment)

                # 3. The Syntax Guard
                if working_content != current_content:
                    is_pure, heresy = SyntaxInquisitor.adjudicate(working_content, target_path.suffix)
                    if not is_pure:
                        raise ArtisanHeresy(f"Syntactic Heresy generated in '{rel_path}': {heresy}")

                    # The Luminous Diff
                    if getattr(request, 'preview', False):
                        self._proclaim_diff(current_content, working_content, str(rel_path), action_taken.value)

                    # 4. Atomic Write
                    atomic_write(
                        target_path=target_path,
                        content=working_content,
                        logger=self.logger,
                        sanctum=self.project_root,
                        transaction=tx,
                        dry_run=is_simulation
                    )

            # Finalization
            artifacts = [
                Artifact(path=res.path, type='file', action=res.action_taken.value, size_bytes=res.bytes_written)
                for res in tx.write_dossier.values()
            ]

            # [ASCENSION]: Use tx.tx_id if available, else generate one for robustness
            tx_id = getattr(tx, 'tx_id', "ad-hoc")

            self._proclaim_success(Path(patch_name), tx.write_dossier, tx.edicts_executed, tx.context, parser_dossier,
                                   tx_id)
            return self.success(
                f"Surgical patch '{patch_name}' applied successfully.",
                artifacts=artifacts
            )

    def _proclaim_success(self, patch_path: Path, write_dossier: Dict, edicts: List, gnosis: Dict, parser_dossier: Any,
                          rite_id: str):
        """
        Ascension Rite: Forges the final proclamation, mirroring the TransmuteArtisan.
        """
        from types import SimpleNamespace
        from ....utils.dossier_scribe import proclaim_apotheosis_dossier

        # 1. Calculate the Transmutation Plan (Required for the Diff)
        plan = {"create": [], "update": [], "delete": [], "move": {}}
        for res in write_dossier.values():
            if res.action_taken == InscriptionAction.CREATED:
                plan['create'].append({'item': None, 'path': res.path})
            elif res.action_taken == InscriptionAction.TRANSFIGURED:
                plan['update'].append({'item': None, 'path': res.path, 'diff': res.diff, 'old_content': None})
            # Patch doesn't usually do explicit delete/move, but we ensure plan is complete.

        # 2. Forge Telemetry Registers
        registers = SimpleNamespace(
            get_duration=lambda: time.monotonic() - self.start_time,
            files_forged=len(plan.get('create', [])),
            sanctums_forged=0,
            bytes_written=sum(r.bytes_written for r in write_dossier.values()),
            no_edicts=False,
            project_root=self.project_root,
            transaction=SimpleNamespace(tx_id=rite_id, edicts_executed=edicts)  # Mock transaction for TelemetryScribe
        )

        # 3. Forge Context & Proclaim
        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis={
                "project_type": "Patch Rite",
                "blueprint_path": patch_path.name,
                **gnosis
            },
            project_root=self.project_root,
            next_steps=[f"Inspect changes: scaffold history inspect {rite_id[:8]}"],
            title="Surgical Patch Applied",
            subtitle=f"Scripture '{patch_path.name}' was transfigured.",
            # CRITICAL: Bestow the Transmutation Plan Gnosis
            transmutation_plan=plan
        )

    def _proclaim_diff(self, old: str, new: str, filename: str, action: str):
        """Renders a beautiful diff to the console."""
        diff_gen = difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=""
        )
        diff_text = "".join(diff_gen)

        if diff_text:
            panel = Panel(
                Syntax(diff_text, "diff", theme="monokai", word_wrap=True),
                title=f"[bold yellow]Prophecy: {filename} ({action})[/bold yellow]",
                border_style="yellow"
            )
            self.console.print(panel)
        else:
            self.console.print(f"[dim]No visual changes for {filename} ({action})[/dim]")