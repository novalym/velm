# Path: scaffold/artisans/telepresence/shadow_vault.py
# --------------------------------------------------
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple

from ...logger import Scribe
from ...utils import atomic_write
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("ShadowVault")


class ShadowFile:
    """A single atom of virtual matter."""

    def __init__(self, path: str, content: bytes, progenitor: str):
        self.path = path
        self.content = content
        self.progenitor = progenitor
        self.created_at = time.time()
        self.size = len(content)


class ShadowVault:
    """
    =================================================================================
    == THE SHADOW VAULT (V-Ω-ETHEREAL-PLANE-ULTIMA-FINALIS)                        ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: E)($@#()()

    The Sovereign in-memory filesystem for Gnostic Telepresence.
    It holds the 'Dreams' of the AI before they are materialized to 'Matter'.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        # [FACULTY 1]: Session Singularity
        # _vault[session_id][rel_path] -> ShadowFile
        self._vault: Dict[str, Dict[str, ShadowFile]] = {}

        # [FACULTY 3]: Entropy Quota Guard
        self._global_size_limit = 512 * 1024 * 1024  # 512MB default
        self._current_global_size = 0

        self._lock = threading.RLock()

    def write(self, session_id: str, rel_path: str, data: bytes, progenitor: str = "AI_COPILOT"):
        """[THE RITE OF DREAMING] Inscribes bytes into the virtual layer."""
        clean_path = rel_path.replace('\\', '/').lstrip('/')

        with self._lock:
            # Check Quotas
            if self._current_global_size + len(data) > self._global_size_limit:
                raise ArtisanHeresy("Vault Overflow: The Ethereal Plane is saturated.")

            if session_id not in self._vault:
                self._vault[session_id] = {}

            # Update size tracking
            old_file = self._vault[session_id].get(clean_path)
            if old_file:
                self._current_global_size -= old_file.size

            new_file = ShadowFile(clean_path, data, progenitor)
            self._vault[session_id][clean_path] = new_file
            self._current_global_size += new_file.size

            Logger.verbose(f"L{session_id[:8]}: Scripture '{clean_path}' inscribed in shadow.")

    def read(self, session_id: str, rel_path: str, transparent: bool = False) -> Optional[bytes]:
        """
        [THE RITE OF PERCEPTION]
        If 'transparent' is True, it will look through the shadow to the disk.
        """
        clean_path = rel_path.replace('\\', '/').lstrip('/')

        with self._lock:
            shadow = self._vault.get(session_id, {}).get(clean_path)
            if shadow:
                return shadow.content

            if transparent:
                phys_path = self.root / clean_path
                if phys_path.exists() and phys_path.is_file():
                    return phys_path.read_bytes()

            return None

    def list_dir(self, session_id: str, rel_dir: str) -> Set[str]:
        """Returns the names of all virtual files within a specific directory."""
        clean_dir = rel_dir.replace('\\', '/').strip('/')
        names = set()

        with self._lock:
            session = self._vault.get(session_id, {})
            for path in session.keys():
                p_obj = Path(path)
                # Check if file is inside the requested dir
                if clean_dir == "" or str(p_obj.parent).replace('.', '') == clean_dir:
                    names.add(p_obj.name)
        return names

    def materialize(self, session_id: str, rel_path: str) -> int:
        """
        [FACULTY 5]: THE RITE OF MATERIALIZATION.
        Flushes a shadow file (or all files in a subdir) to physical disk.
        """
        count = 0
        clean_target = rel_path.replace('\\', '/').lstrip('/')

        with self._lock:
            session = self._vault.get(session_id, {})
            # Identify candidates (exact match or subtree)
            targets = [p for p in session.keys() if p == clean_target or p.startswith(clean_target + "/")]

            for path in targets:
                shadow = session.pop(path)
                self._current_global_size -= shadow.size

                # [FACULTY 8]: Conflict Detection
                # (Future: Compare shadow.created_at with disk.mtime)

                dest = self.root / path
                dest.parent.mkdir(parents=True, exist_ok=True)

                # Final Materialization
                atomic_write(dest, shadow.content, None, self.root, encoding=None)
                count += 1

        return count

    def purge_session(self, session_id: str):
        """[FACULTY 11]: Surgical Purge."""
        with self._lock:
            session = self._vault.pop(session_id, {})
            for f in session.values():
                self._current_global_size -= f.size
            Logger.info(f"Session {session_id[:8]} returned to the void.")

    def get_stats(self) -> Dict[str, Any]:
        """Proclaims the current mass of the Ethereal Plane."""
        with self._lock:
            return {
                "active_sessions": len(self._vault),
                "total_shadow_files": sum(len(s) for s in self._vault.values()),
                "total_memory_bytes": self._current_global_size,
                "utilization": f"{(self._current_global_size / self._global_size_limit) * 100:.2f}%"
            }

    def scry_metadata(self, session_id: str, rel_path: str) -> Optional[Dict[str, Any]]:
        """[FACULTY 10]: Simulates FileStat for virtual entries."""
        with self._lock:
            shadow = self._vault.get(session_id, {}).get(rel_path)
            if not shadow: return None

            return {
                "size": shadow.size,
                "mtime": shadow.created_at * 1000,
                "progenitor": shadow.progenitor,
                "is_shadow": True
            }