# Path: scaffold/core/state/snapshot.py
from pathlib import Path
import json
from .contracts import GnosticState
from .store import Store

class GnosticSnapshot:
    """The Chronomancer. It freezes and thaws reality."""

    @staticmethod
    def freeze(session_id: str) -> GnosticState:
        """Perceives the current state and forges an immutable GnosticState vessel."""
        return GnosticState(
            session_id=session_id,
            variables=Store.get_all()
        )

    @staticmethod
    def persist(state: GnosticState, path: Path):
        """Inscribes a frozen reality to a scripture on disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(state.model_dump_json(indent=2), encoding='utf-8')

    @staticmethod
    def thaw(path: Path) -> GnosticState:
        """Resurrects a reality from a scripture."""
        if not path.exists():
            raise FileNotFoundError("Cannot thaw a void.")
        state_data = json.loads(path.read_text(encoding='utf-8'))
        return GnosticState(**state_data)