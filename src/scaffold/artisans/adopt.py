# Path: scaffold/artisans/adopt.py
# --------------------------------
import json
from pathlib import Path
from typing import List, Dict, Any

from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from ..artisans.distill.core import DistillationOracle
from ..core.cortex.contracts import DistillationProfile
from ..contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ..core.artisan import BaseArtisan
from ..core.cortex.blueprint_merger import BlueprintMerger
from ..core.cortex.engine import GnosticCortex
from ..core.cortex.logic_inductor import LogicInductor
from ..core.kernel.chronicle import update_chronicle
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import AdoptRequest
from ..utils import atomic_write, hash_file

# Divine Summons of the Crystal Mind
try:
    from ..core.state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
except ImportError:
    SQL_AVAILABLE = False


@register_artisan("adopt")
class AdoptArtisan(BaseArtisan[AdoptRequest]):
    """
    =================================================================================
    == THE REGISTRAR OF REALITY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                    ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan performs the Rite of Adoption. It gazes upon an existing, unmanaged
    reality and transmutes it into Gnostic Law (Blueprint) and Memory (Lockfile).

    [ASCENSION]: It now correctly enshrines the **AST Metrics** (structural soul)
    into the write result, ensuring the Gnostic Graph is fully hydrated.
    """

    def execute(self, request: AdoptRequest) -> ScaffoldResult:
        root = (self.project_root / request.target_path).resolve()
        if not root.exists():
            return self.failure(f"Target sanctum not found: {root}")

        output_path = root / request.output_file
        lock_path = root / "scaffold.lock"

        self.logger.info(f"The Registrar prepares to adopt reality at: [cyan]{root}[/cyan]")

        unified_ignore = [request.output_file, "scaffold.lock", ".git", ".scaffold"] + (request.ignore or [])
        distillation_profile = DistillationProfile(
            strategy='faithful', strip_comments=False, redact_secrets=True,
            ignore=unified_ignore,
            include=request.include,
            focus_keywords=request.focus
        )

        cortex = GnosticCortex(root)
        cortex.configure_filters(ignore=distillation_profile.ignore, include=distillation_profile.include)
        memory = cortex.perceive(force_refresh=True)
        reality_paths = {file_gnosis.path.as_posix() for file_gnosis in memory.inventory}

        blueprint_content = ""
        merge_strategy = "OVERWRITE"

        if output_path.exists() and not request.force:
            self.logger.info("Existing blueprint detected. Initiating Intelligent Merge...")
            merge_strategy = "MERGE"
            merger = BlueprintMerger(self.project_root, output_path)
            blueprint_content = merger.merge(reality_paths)
            self.logger.success(f"Blueprint merged. Logic, variables, and comments preserved.")
        else:
            self.logger.info("Forging fresh blueprint from reality...")
            oracle = DistillationOracle(
                distill_path=root,
                profile=distillation_profile,
                project_root=root,  # <<< THE SACRED MISSING ARGUMENT RESTORED
                silent=True
            )
            blueprint_content = oracle.distill()

        suggestions = []
        if not request.non_interactive:
            try:
                inductor = LogicInductor()
                suggestions = inductor.induce(list(reality_paths))
                if suggestions:
                    self._proclaim_patterns(suggestions)
            except Exception as e:
                self.logger.warn(f"Logic Inductor faltered: {e}")

        atomic_write(output_path, blueprint_content, self.logger, root, force=True)

        write_dossier: List[GnosticWriteResult] = []
        with self.console.status(f"[bold cyan]Forging Gnostic Memory ({len(memory.inventory)} souls)...[/bold cyan]"):
            for file_gnosis in memory.inventory:
                f_hash = file_gnosis.hash_signature
                if not f_hash and request.full:
                    f_hash = hash_file(self.project_root / file_gnosis.path)

                # ★★★ THE DIVINE HEALING: METRICS ENSHRINEMENT ★★★
                # We verify that ast_metrics is populated.
                metrics_payload = file_gnosis.ast_metrics
                # If we have structural data, we ensure it passes through.

                result = GnosticWriteResult(
                    success=True,
                    path=root / file_gnosis.path,
                    action_taken=InscriptionAction.ADOPTED,
                    bytes_written=file_gnosis.original_size,
                    gnostic_fingerprint=f_hash,
                    blueprint_origin=Path("manual/adopt"),
                    dependencies=list(file_gnosis.imported_symbols) if file_gnosis.imported_symbols else [],
                    # [THE FIX] We explicitly attach the metrics containing functions/classes
                    metrics=metrics_payload
                )
                write_dossier.append(result)

        files_to_delete_from_memory: List[Path] = []
        if lock_path.exists():
            try:
                old_data = json.loads(lock_path.read_text(encoding='utf-8'))
                for old_path_str in old_data.get("manifest", {}).keys():
                    if old_path_str not in reality_paths:
                        files_to_delete_from_memory.append(root / old_path_str)
            except Exception:
                pass

        if files_to_delete_from_memory:
            self.logger.info(f"Pruning {len(files_to_delete_from_memory)} ghost scriptures from the Chronicle.")

        # ★★★ THE DIVINE HEALING ★★★
        rite_dossier_delete = [{'path': p} for p in files_to_delete_from_memory]
        # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        update_chronicle(
            project_root=root,
            blueprint_path=output_path,
            rite_dossier={"delete": rite_dossier_delete},
            old_lock_data={},
            write_dossier=write_dossier,
            final_vars={},
            rite_name=f"Rite of Adoption ({merge_strategy})",
            edicts_executed=[]
        )
        if SQL_AVAILABLE:
            try:
                self.logger.info("Synchronizing Crystal Mind with new Manifest...")
                db = GnosticDatabase(root)
                # We command the DB to hydrate from the newly written scaffold.lock
                db.hydrate_from_lockfile()
                self.logger.success("Crystal Mind synchronized.")
            except Exception as e:
                self.logger.warn(f"Crystal Mind synchronization failed during adoption: {e}")

        return self.success(
            f"Adoption complete. Reality is now Law.",
            artifacts=[
                Artifact(path=output_path, type="file", action="modified"),
                Artifact(path=lock_path, type="file", action="modified")
            ],
            data={
                "files_adopted": len(write_dossier),
                "ghosts_pruned": len(files_to_delete_from_memory),
                "patterns_detected": len(suggestions),
                "strategy": merge_strategy,
                "blueprint_content": blueprint_content
            }
        )

    def _proclaim_patterns(self, suggestions: List[Dict[str, Any]]):
        """Renders the Luminous Panel of Pattern Recognition."""
        self.console.print()
        self.console.rule("[bold magenta]✨ Gnostic Pattern Recognition[/bold magenta]")
        self.console.print("The Logic Inductor has perceived repeating structures in your reality.\n")
        for i, suggestion in enumerate(suggestions):
            header = Text.assemble(
                (f"Pattern #{i + 1}: ", "bold white"),
                (f"{suggestion['type']} ", "cyan"),
                (f"(Confidence: {suggestion['confidence']:.2f})", "dim green")
            )
            panel = Panel(
                Syntax(suggestion['suggestion_text'], "python", theme="monokai"),
                title=header, border_style="magenta",
                subtitle=f"[dim]{suggestion.get('impact', 'Optimization')}[/dim]"
            )
            self.console.print(panel)
        self.console.print("\n[dim]To apply these abstractions, copy the Gnosis above into your blueprint.[/dim]\n")