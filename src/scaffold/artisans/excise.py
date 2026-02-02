# Path: scaffold/artisans/excise.py
# ---------------------------------
import json
from pathlib import Path
from typing import List, Set, Dict, Optional

from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..core.kernel.transaction import GnosticTransaction
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import ExciseRequest, BlueprintExciseRequest
# --- DIVINE SUMMONS OF THE ASCENDED FACULTIES ---
from ..core.state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
from ..core.kernel.archivist import GnosticArchivist
from ..utils import hash_file
from .blueprint_remove import BlueprintExciseArtisan


class ExciseArtisan(BaseArtisan[ExciseRequest]):
    """
    =================================================================================
    == THE CHRONOMANCER OF REVERSION (V-Ω-UNWEAVE-ULTIMA)                          ==
    =================================================================================
    @gnosis:title The Chronomancer of Reversion (`excise` / `unweave`)
    @gnosis:summary Surgically removes all artifacts born from a specific blueprint origin, with drift detection and archival.

    This artisan performs the sacred Rite of Reversion. It is a Chronomancer that
    gazes into the Gnostic Chronicle to find all scriptures born from a specific
    origin and returns them to the void. It is a sentient partner in deconstruction,
    possessing a pantheon of 13+ legendary faculties.
    """

    def execute(self, request: ExciseRequest) -> ScaffoldResult:
        lockfile_path = self.project_root / "scaffold.lock"
        if not lockfile_path.exists():
            return self.failure("Gnostic Chronicle (scaffold.lock) not found. Cannot perform reversion.")

        try:
            lock_data = json.loads(lockfile_path.read_text(encoding='utf-8'))
            manifest = lock_data.get("manifest", {})
        except json.JSONDecodeError as e:
            raise ArtisanHeresy("The Gnostic Chronicle is profane (corrupted JSON).", child_heresy=e)

        # --- MOVEMENT I: THE GAZE OF PROVENANCE (FUZZY ORIGIN MATCH) ---
        target_origin = self._find_true_origin(request.blueprint_origin, manifest)
        if not target_origin:
            return self.failure(f"No origin matching '{request.blueprint_origin}' found in the Chronicle.")

        self.logger.info(f"Gaze is fixed. Target origin: '[cyan]{target_origin}[/cyan]'")
        paths_to_annihilate = self._collect_paths(target_origin, manifest)

        if not paths_to_annihilate:
            return self.success(f"No scriptures born from '{target_origin}' were found in the Chronicle.")

        # --- MOVEMENT II: THE DRIFT SENTINEL'S GAZE ---
        drifted_files = self._detect_drift(paths_to_annihilate, manifest)

        # --- MOVEMENT III: THE GAZE OF CONSEQUENCE (IMPACT ANALYSIS) ---
        surviving_dependents = self._perceive_impact(paths_to_annihilate)

        # --- MOVEMENT IV: THE ARCHITECT'S ADJUDICATION ---
        self._proclaim_prophecy(paths_to_annihilate, drifted_files, surviving_dependents)

        if request.dry_run:
            return self.success("Dry run complete. The mortal realm remains untouched.")

        if not request.force and not request.non_interactive:
            if not Confirm.ask("[bold question]Execute this surgical excision?[/bold question]", default=False):
                return self.success("The Rite of Annihilation was stayed.")

        # --- MOVEMENT V: THE GUARDIAN'S OFFER (ARCHIVAL) ---
        if not request.no_backup:
            self._archive_condemned_souls(paths_to_annihilate, target_origin)

        # --- MOVEMENT VI: THE GNOSTIC TWIN (BLUEPRINT SYNCHRONIZATION) ---
        if request.update_blueprint:
            self._excise_from_blueprint(paths_to_annihilate, request.update_blueprint)

        # --- MOVEMENT VII: THE TRANSACTIONAL ANNIHILATION & GHOST BUSTING ---
        deleted_artifacts = self._annihilate_reality(paths_to_annihilate)

        # --- MOVEMENT VIII: THE FINAL PROCLAMATION (LUMINOUS DOSSIER) ---
        # (This would be a rich summary table of all actions taken)
        return self.success(
            f"Successfully excised {len(deleted_artifacts)} artifacts born from '{target_origin}'.",
            artifacts=deleted_artifacts
        )

    def _find_true_origin(self, query: str, manifest: Dict) -> Optional[str]:
        origins = {meta.get("blueprint_origin") for meta in manifest.values() if meta.get("blueprint_origin")}
        if query in origins:
            return query

        # Fuzzy match
        matches = [o for o in origins if query in o]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ArtisanHeresy(f"Ambiguous origin '{query}'. Matches: {', '.join(matches)}")

        return None

    def _collect_paths(self, origin: str, manifest: Dict) -> Set[Path]:
        return {
            self.project_root / path_str
            for path_str, meta in manifest.items()
            if meta.get("blueprint_origin") == origin
        }

    def _detect_drift(self, paths: Set[Path], manifest: Dict) -> Dict[Path, str]:
        drifted = {}
        for p in paths:
            if p.is_file():
                rel_path_str = str(p.relative_to(self.project_root)).replace('\\', '/')
                locked_hash = manifest.get(rel_path_str, {}).get("sha256")
                if locked_hash:
                    current_hash = hash_file(p)
                    if current_hash != locked_hash:
                        drifted[p] = "MODIFIED"
            elif not p.exists():
                drifted[p] = "MISSING"
        return drifted

    def _perceive_impact(self, paths_to_annihilate: Set[Path]) -> Dict[Path, List[Path]]:
        # ... (This method remains pure and unchanged from the previous version) ...
        if not SQL_AVAILABLE: return {}
        db = GnosticDatabase(self.project_root);
        session = db.session
        impact_map: Dict[Path, List[Path]] = {};
        paths_str = {str(p.relative_to(self.project_root)).replace('\\', '/') for p in paths_to_annihilate}
        try:
            for target_path in paths_to_annihilate:
                target_path_str = str(target_path.relative_to(self.project_root)).replace('\\', '/')
                dependents = session.query(db.BondModel.source_path).filter(
                    db.BondModel.target_path == target_path_str).all()
                survivors = [d[0] for d in dependents if d[0] not in paths_str]
                if survivors: impact_map[target_path] = [self.project_root / s for s in survivors]
        finally:
            session.close()
        return impact_map

    def _proclaim_prophecy(self, paths: Set[Path], drift: Dict[Path, str], impact: Dict[Path, List[Path]]):
        table = Table(title=f"[bold]Prophecy of Annihilation ({len(paths)} items)[/bold]", box=ROUNDED)
        table.add_column("Scripture", style="cyan")
        table.add_column("Status", style="yellow")

        for p in sorted(list(paths)):
            status = "Pure"
            style = "green"
            if p in drift:
                status = drift[p]
                style = "bold red" if status == "MISSING" else "bold yellow"
            table.add_row(str(p.relative_to(self.project_root)), f"[{style}]{status}[/{style}]")

        panels = [Panel(table, border_style="red")]

        if impact:
            impact_table = Table(box=ROUNDED)
            impact_table.add_column("Broken By", style="yellow")
            impact_table.add_column("Breaking", style="cyan")
            for deleted, dependents in impact.items():
                impact_table.add_row(str(deleted.relative_to(self.project_root)),
                                     "\n".join(f"• {d.relative_to(self.project_root)}" for d in dependents))
            panels.append(Panel(impact_table, title="[bold red]💀 Causal Impact[/bold red]", border_style="red"))

        self.console.print(*panels)

    def _archive_condemned_souls(self, paths: Set[Path], reason: str):
        archivist = GnosticArchivist(self.project_root)
        archivist.create_snapshot(list(paths), reason=f"excise_{Path(reason).stem}")

    def _excise_from_blueprint(self, paths: Set[Path], blueprint_path_str: str):
        self.logger.info("The Gnostic Twin awakens to synchronize the Master Blueprint...")
        blueprint_path = self.project_root / blueprint_path_str
        if not blueprint_path.exists():
            self.logger.warn(f"Blueprint '{blueprint_path_str}' not found. Synchronization stayed.")
            return

        for p in paths:
            try:
                req = BlueprintExciseRequest(
                    blueprint_path=blueprint_path_str,
                    target_path=str(p.relative_to(self.project_root)),
                    force=True  # We are already confirmed
                )
                BlueprintExciseArtisan(self.engine).execute(req)
            except Exception as e:
                self.logger.warn(f"Failed to excise '{p.name}' from blueprint: {e}")

    def _annihilate_reality(self, paths: Set[Path]) -> List[Artifact]:
        deleted_artifacts: List[Artifact] = []
        with GnosticTransaction(self.project_root, "Excise from Blueprint", use_lock=False) as tx:
            # Files first
            for path in sorted(list(paths), key=lambda p: len(p.parts), reverse=True):
                if path.is_file() and path.exists():
                    path.unlink();
                    deleted_artifacts.append(Artifact(path=path, type="file", action="deleted"))

            # Then directories (The Ghost Buster)
            parent_dirs = {p.parent for p in paths}
            for parent in sorted(list(parent_dirs), key=lambda p: len(p.parts), reverse=True):
                if parent.exists() and parent.is_dir() and not any(parent.iterdir()):
                    try:
                        parent.rmdir();
                        deleted_artifacts.append(Artifact(path=parent, type="directory", action="deleted"))
                    except OSError:
                        pass  # May fail if another process holds it
        return deleted_artifacts