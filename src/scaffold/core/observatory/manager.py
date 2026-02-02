# Path: scaffold/core/observatory/manager.py
# ------------------------------------------
import hashlib
import time
from pathlib import Path
from typing import List, Optional, Dict

from .contracts import ProjectEntry, ProjectType, ProjectHealth, ObservatoryState
from .store import GnosticStore
from .scanner import PlanetaryScanner
from .health import VitalityMonitor
from ...logger import Scribe

Logger = Scribe("ObservatoryManager")

class ObservatoryManager:
    """
    =============================================================================
    == THE SOVEREIGN MANAGER (V-Ω-PROJECT-REGISTRAR)                           ==
    =============================================================================
    The high-level interface for managing the known universe of projects.
    """

    def __init__(self):
        self.store = GnosticStore()

    def _generate_id(self, path: Path) -> str:
        """Creates a deterministic ID based on the absolute path."""
        # Normalize path for ID generation to prevent OS mismatch
        norm_path = str(path.resolve()).lower().replace('\\', '/')
        return hashlib.md5(norm_path.encode()).hexdigest()[:12]

    def register(self, path: str, name: Optional[str] = None) -> ProjectEntry:
        """
        [THE RITE OF CONSECRATION]
        Registers a directory as a Project in the Observatory.
        """
        abs_path = Path(path).resolve()
        # We allow registering non-existent paths if we are about to create them,
        # but ideally the directory should exist.
        if not abs_path.exists():
            # For now, we proceed to allow 'genesis' of new folders
            pass

        state = self.store.load()
        pid = self._generate_id(abs_path)

        # Update if exists, else create
        if pid in state.projects:
            entry = state.projects[pid]
            entry.last_accessed = time.time()
            entry.access_count += 1
            # Update name if provided explicitly
            if name: entry.name = name
            Logger.info(f"Project '{entry.name}' updated in Observatory.")
        else:
            # Initial Scan
            health, meta = VitalityMonitor.check_pulse(abs_path)

            # Divine Type if not known
            ptype = ProjectType.GENERIC
            if (abs_path / "pyproject.toml").exists():
                ptype = ProjectType.PYTHON
            elif (abs_path / "package.json").exists():
                ptype = ProjectType.NODE
            elif (abs_path / "Cargo.toml").exists():
                ptype = ProjectType.RUST
            elif (abs_path / "go.mod").exists():
                ptype = ProjectType.GO

            entry = ProjectEntry(
                id=pid,
                path=abs_path,
                name=name or abs_path.name,
                health=health,
                metadata=meta
            )
            entry.metadata.language = ptype
            state.projects[pid] = entry
            Logger.success(f"Project '{entry.name}' consecrated in Observatory.")

        # Auto-switch on register
        state.active_project_id = pid
        self.store.save(state)
        return entry

    def switch(self, identifier: str) -> Optional[ProjectEntry]:
        """
        Sets the active project.
        Identifier can be ID, Name, or Path.
        """
        state = self.store.load()
        target_id = None

        # 1. Try ID match
        if identifier in state.projects:
            target_id = identifier

        # 2. Try Path match
        if not target_id:
            try:
                search_path = Path(identifier).resolve()
                target_id = self._generate_id(search_path)
                if target_id not in state.projects: target_id = None
            except:
                pass

        # 3. Try Name match (Fuzzy)
        if not target_id:
            for pid, proj in state.projects.items():
                if proj.name == identifier:
                    target_id = pid
                    break

        if target_id:
            state.active_project_id = target_id
            proj = state.projects[target_id]
            proj.last_accessed = time.time()
            proj.access_count += 1
            self.store.save(state)
            Logger.info(f"Observatory focus shifted to: [cyan]{proj.name}[/cyan]")
            return proj

        Logger.warn(f"Project '{identifier}' not found in Observatory.")
        return None

    def get_active(self) -> Optional[ProjectEntry]:
        state = self.store.load()
        if state.active_project_id and state.active_project_id in state.projects:
            return state.projects[state.active_project_id]
        return None

    def list_projects(self) -> List[ProjectEntry]:
        state = self.store.load()
        # Sort by last accessed
        return sorted(state.projects.values(), key=lambda p: p.last_accessed, reverse=True)

    def scan_and_ingest(self, root: str):
        """Mass registration."""
        root_path = Path(root).resolve()
        candidates = PlanetaryScanner.scan(root_path)
        count = 0
        for path, ptype in candidates:
            # We don't overwrite names, just register paths
            self.register(str(path))
            count += 1
        return count

    def pulse(self):
        """
        Background Heartbeat.
        Updates health status of all projects.
        """
        state = self.store.load()
        changed = False
        for pid, proj in state.projects.items():
            old_health = proj.health
            new_health, new_meta = VitalityMonitor.check_pulse(proj.path)

            if new_health != old_health:
                proj.health = new_health
                proj.metadata = new_meta  # Update git info
                changed = True

        if changed:
            self.store.save(state)