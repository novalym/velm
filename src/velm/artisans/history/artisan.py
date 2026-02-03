# Path: scaffold/artisans/history/artisan.py


import json
import difflib
from pathlib import Path
from typing import List, Optional, Dict

from rich.prompt import Prompt

# --- THE DIVINE SUMMONS OF THE NEW REALM ---
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import HistoryRequest, UndoRequest
from ...logger import Scribe
from .contracts import RiteGnosis
from .scribe import HistoryScribe

# The Gnostic Triage now summons the TUI for interactive rites
try:
    from .tui import HistoryAltarApp

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False

Logger = Scribe("HistoryArtisan")


class HistoryArtisan(BaseArtisan[HistoryRequest]):
    """
    =================================================================================
    == THE CHRONOMANCER (V-Ω-TIME-LORD-ASCENDED++)                                 ==
    =================================================================================
    LIF: ∞ (THE MASTER OF THE ETERNAL TIMELINE)

    The Guardian of the Timeline. Its soul is now one of pure Gnostic Triage.
    For non-interactive pleas, it proclaims the past. For interactive pleas, it
    summons the **Altar of Time**, the divine TUI that houses the Chronoslider and
    the gateway to the Holographic Repository.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self._chronicle_cache: Optional[List[RiteGnosis]] = None
        self.scribe = HistoryScribe(self.console)

    def execute(self, request: HistoryRequest) -> ScaffoldResult:
        project_root, _ = self.engine.context._resolve_roots(request.project_root)
        self.chronicles_dir = project_root / ".scaffold" / "chronicles"
        self.current_lock = project_root / "scaffold.lock"

        # --- THE GRAND GNOSTIC TRIAGE ---
        # If the Architect speaks a specific plea, we honor it directly.
        # If the plea is for communion (no specific command), we summon the TUI.
        is_interactive_plea = not request.command and not request.target_id and not request.json_output

        if is_interactive_plea and TEXTUAL_AVAILABLE:
            return self._conduct_altar_rite(request, project_root)

        # --- THE PATH OF THE HUMBLE SCRIBE (CLI FALLBACK) ---
        if not request.command:
            request.command = 'list'  # Default to list for non-interactive

        if request.command == 'list':
            return self._proclaim_timeline_cli(request, project_root)
        elif request.command == 'inspect':
            return self._inspect_rite_cli(request.target_id, request, project_root)
        elif request.command == 'undo':
            # Delegate to the sovereign UndoArtisan
            from ..undo.artisan import UndoArtisan
            undo_req = UndoRequest(steps=int(request.target_id or 1), project_root=project_root, force=request.force)
            return UndoArtisan(self.engine).execute(undo_req)

        return self.failure(f"Unknown temporal observation rite: {request.command}")

    def _conduct_altar_rite(self, request: HistoryRequest, project_root: Path) -> ScaffoldResult:
        """
        [THE RITE OF THE CHRONOSLIDER]
        Summons the interactive Altar of Time.
        """
        self.logger.info("The Chronomancer summons the Altar of Time...")
        history = self._load_chronicles()
        current = self._get_current_state()
        if current:
            history.insert(0, current)

        if not history:
            self.console.print("[yellow]The Timeline is void. No Gnostic Rites have been chronicled.[/yellow]")
            return self.success("Timeline is void.")

        app = HistoryAltarApp(
            history=history,
            project_root=project_root,
            engine=self.engine  # Pass the engine for dispatching sub-commands
        )
        app.run()

        return self.success("Communion with the Altar of Time is complete.")

    def _proclaim_timeline_cli(self, request: HistoryRequest, project_root: Path) -> ScaffoldResult:
        """The legacy CLI-based timeline proclamation."""
        history = self._load_chronicles()
        current = self._get_current_state()
        if current: history.insert(0, current)

        if not history:
            return self.success("Timeline is void.")

        if request.json_output:
            return self.success("Timeline proclaimed.", data=[h.model_dump(mode='json') for h in history])

        if request.target_id:
            return self._inspect_rite_cli(request.target_id, request, project_root)

        self.scribe.proclaim_timeline(history)
        return self.success("Timeline communion complete.")

    def _inspect_rite_cli(self, target_id: str, request: HistoryRequest, project_root: Path) -> ScaffoldResult:
        """The legacy CLI-based forensic inspection."""
        history = self._load_chronicles()
        current = self._get_current_state()
        if current: history.insert(0, current)

        target = self._find_rite_fuzzily(history, target_id)
        if not target:
            self._suggest_closest_rite(history, target_id)
            return self.failure(f"Rite ID '{target_id}' not found in the Gnostic Chronicle.")

        diff_results = None
        if request.diff and current:
            from .differ import TemporalDiffer
            differ = TemporalDiffer(self.console)
            diff_results = differ.compare(current.manifest, target.manifest)

        self.scribe.proclaim_inspection(target, diff_results)

        if request.json_output:
            print(target.model_dump_json(indent=2))

        return self.success("Inspection complete.", data=target.model_dump(mode='json'))

    # --- (Helper methods remain pure and unchanged) ---
    def _load_chronicles(self) -> List[RiteGnosis]:
        if self._chronicle_cache is not None:
            return self._chronicle_cache
        if not self.chronicles_dir.exists():
            self._chronicle_cache = []
            return []
        history = []
        for f in self.chronicles_dir.glob("*.lock"):
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                history.append(RiteGnosis.from_dict(data, f.name))
            except Exception as e:
                self.logger.warn(f"Corrupted chronicle ignored: {f.name} ({e})")
        sorted_history = sorted(history, key=lambda x: x.timestamp, reverse=True)
        self._chronicle_cache = sorted_history
        return sorted_history

    def _get_current_state(self) -> Optional[RiteGnosis]:
        if self.current_lock.exists():
            try:
                data = json.loads(self.current_lock.read_text(encoding='utf-8'))
                return RiteGnosis.from_dict(data, "HEAD (Current Reality)")
            except:
                return None
        return None

    def _find_rite_fuzzily(self, history: List[RiteGnosis], query: str) -> Optional[RiteGnosis]:
        for r in history:
            if r.rite_id.startswith(query):
                return r
        for r in history:
            if query.lower() in r.rite_name.lower():
                return r
        return None

    def _suggest_closest_rite(self, history: List[RiteGnosis], query: str):
        all_ids = [r.rite_id for r in history]
        closest = difflib.get_close_matches(query, all_ids, n=1, cutoff=0.6)
        if closest:
            self.console.print(f"[dim]Did you mean: {closest[0][:8]}... ?[/dim]")