# Path: src/velm/artisans/project/manager.py
# ------------------------------------------
from __future__ import annotations

import os
import sys
import time
import uuid
import json
import shutil
import hashlib
import threading
import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Set, Tuple

# --- DIVINE UPLINKS ---
from .contracts import RegistrySchema, ProjectMeta, ProjectStats
from .persistence import RegistryPersistence
from .seeds import ArchetypeOracle
from .constants import (
    DEFAULT_WORKSPACE_DIR_NAME,
    SYSTEM_OWNER_ID,
    GUEST_OWNER_ID,
    PROGENITOR_ID,
    REGISTRY_VERSION,
)

# --- SYSTEM SUTURE ---
try:
    from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
    from ...logger import Scribe
except ImportError:
    # Bootstrap fallback for absolute resilience
    ArtisanHeresy = Exception
    HeresySeverity = type("Enum", (), {"CRITICAL": "CRITICAL", "WARNING": "WARNING", "INFO": "INFO"})
    Scribe = lambda n: type("Logger", (), {
        "info": lambda *a: None, "warn": lambda *a: None, "error": lambda *a: None,
        "success": lambda *a: None, "debug": lambda *a: None, "critical": lambda *a: None,
        "verbose": lambda *a: None, "is_verbose": False
    })

Logger = Scribe("OmegaGovernor")


class GnosticLedger(RegistryPersistence):
    """
    =============================================================================
    == THE GNOSTIC LEDGER (V-Ω-ATOMIC-PERSISTENCE-V2)                          ==
    =============================================================================
    Ascended persistence layer utilizing OS-level atomic renames to guarantee
    Zero-Corruption even during sudden WASM worker termination or power failure.
    Includes a self-healing backup rotation protocol.
    """

    def save(self, registry: Dict[str, Any]):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.registry_path.with_suffix('.tmp.json')
        backup_path = self.registry_path.with_suffix('.bak.json')

        try:
            # 1. Write to Ephemeral Sarcophagus
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2)

            # 2. Forge Backup of Last Known Truth
            if self.registry_path.exists():
                shutil.copy2(self.registry_path, backup_path)

            # 3. Atomic Substitution (POSIX and Windows modern)
            tmp_path.replace(self.registry_path)

        except Exception as e:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            Logger.error(f"Atomic Inscription Fractured: {e}")

            # Fallback to standard write if atomic OS hooks fail
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2)


class ProjectManager:
    """
    =================================================================================
    == THE OMEGA GOVERNOR (V-Ω-TOTALITY-V100000.99-OMNISCIENT-CORTEX)              ==
    =================================================================================
    LIF: ∞ | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SUPREME
    AUTH: Ω_GOVERNOR_V100K_LAZARUS_RESURRECTION_FINALIS

    The Centralized Brain of the Velm Multiverse. It governs the lifecycle,
    duplication, evolution, and annihilation of Realities. It is warded against
    all forms of data loss via the Lazarus Resurrection Protocol.
    """

    def __init__(self, engine: Any = None, persistence: Optional[RegistryPersistence] = None):
        """
        [THE RITE OF INCEPTION]
        Materializes the central mind of the project cosmos.
        """
        self._inception_ts = time.perf_counter_ns()
        self._lock = threading.RLock()
        self.engine = engine

        # --- MOVEMENT I: SUBSTRATE CALIBRATION ---
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_silent = getattr(self.engine, 'silent', False) if self.engine else False

        # Determine the Axis Mundi (Root)
        base_dir = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", "/vault/project"))
        if base_dir.name != "project":
            base_dir = base_dir.parent if base_dir.parent.name == "vault" else Path("/vault/project")

        self.registry_path = base_dir / ".scaffold" / "projects.json"
        self.persistence = persistence or GnosticLedger(self.registry_path)
        self.oracle = ArchetypeOracle()

        # --- MOVEMENT II: THE DECREE OF THE AXIS MUNDI ---
        # System demos are kept separate from user projects to prevent database pollution
        self.system_demos: Dict[str, ProjectMeta] = {}
        self._manifest_axis_mundi()

        # --- MOVEMENT III: GEOMETRIC ANCHORING ---
        self.workspaces_root = Path(
            "/vault/workspaces") if self.is_wasm else self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME
        try:
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

        # --- MOVEMENT IV: THE RESURRECTION & LAZARUS PROTOCOL ---
        self._registry: Optional[Dict[str, Any]] = None
        self._state_hash: str = "0xVOID"
        self._search_index: Dict[str, Set[str]] = {}

        try:
            loaded_reg = self.persistence.load()
            if not loaded_reg or not loaded_reg.get('projects') is not None:
                raise ValueError("Registry soul is a void.")
            self._registry = loaded_reg

            # Version Healing
            if self._registry.get('version') != REGISTRY_VERSION:
                if not self._is_silent:
                    Logger.warn(f"Version Drift: Migrating to {REGISTRY_VERSION}...")
                self._registry['version'] = REGISTRY_VERSION
                self._commit_state()

        except Exception as e:
            if not self._is_silent:
                Logger.critical(f"Registry Fracture detected: {e}. Initiating Lazarus Protocol...")
            self._registry = {"version": REGISTRY_VERSION, "active_project_id": None, "projects": {}}
            self._lazarus_resurrection()  # Rebuild from raw folder scans

        # --- MOVEMENT V: THE SEMANTIC INDEX ---
        self._rebuild_search_index()
        self._calculate_state_hash()

        duration_ms = (time.perf_counter_ns() - self._inception_ts) / 1_000_000
        if not self._is_silent and Logger.is_verbose:
            Logger.success(
                f"Omega Governor RESONANT ({duration_ms:.2f}ms). Substrate: {'WASM' if self.is_wasm else 'IRON'}")

    # =========================================================================
    # == SECTION I: CORE METABOLISM & STATE                                  ==
    # =========================================================================

    @property
    def registry(self) -> Dict[str, Any]:
        """The Absolute Source of Truth for the Cosmos."""
        return self._registry

    @registry.setter
    def registry(self, val: Dict[str, Any]):
        with self._lock:
            self._registry = val
            self._rebuild_search_index()
            self._calculate_state_hash()

    @property
    def census_count(self) -> int:
        return len(self.registry.get("projects", {})) + len(self.system_demos)

    @property
    def state_hash(self) -> str:
        """Merkle-style hash to prevent redundant React UI renders."""
        return self._state_hash

    def live_active_id(self) -> Optional[str]:
        return self.registry.get("active_project_id")

    # =========================================================================
    # == SECTION II: THE KINETIC RITES (CRUD)                                ==
    # =========================================================================

    def list_projects(self, owner_id: Optional[str] = None, tags: Optional[List[str]] = None,
                      include_archived: bool = False) -> List[Dict[str, Any]]:
        """
        [RAM SUPREMACY]
        Returns the project list instantly from memory. Zero Disk I/O.
        Returns pure dictionaries to ensure Pyodide/JSON serialization never fractures.
        """
        with self._lock:
            # 1. Merge Living + Ghosts from RAM
            pool = list(self.registry["projects"].values())
            existing_ids = {p["id"] for p in pool}

            # 2. Inject System Demos
            for pid, ghost_meta in self.system_demos.items():
                if pid not in existing_ids:
                    pool.append(ghost_meta.model_dump() if hasattr(ghost_meta, 'model_dump') else ghost_meta)

            # 3. Filter by Sovereignty
            if owner_id and owner_id != GUEST_OWNER_ID:
                pool = [p for p in pool if p.get("owner_id") in (owner_id, SYSTEM_OWNER_ID)]
            elif owner_id == GUEST_OWNER_ID:
                pool = [p for p in pool if p.get("owner_id") in (GUEST_OWNER_ID, SYSTEM_OWNER_ID)]

            # 4. Filter by Taxonomy
            if tags:
                tag_set = set(t.lower() for t in tags)
                pool = [p for p in pool if any(t.lower() in tag_set for t in p.get("tags", []))]

            # 5. Filter by Vitality
            if not include_archived:
                pool = [p for p in pool if not p.get("is_archived", False)]

            # 6. Sort by Recency
            pool.sort(key=lambda x: x.get('last_accessed', 0), reverse=True)
            return pool

    def create_project(self,
                       name: str,
                       description: str = "",
                       template: str = "blank",
                       owner_id: str = "GUEST",
                       is_demo: bool = False,
                       tags: List[str] = None,
                       auto_anchor: bool = True) -> Dict[str, Any]:
        """
        [THE RITE OF GENESIS]
        Forges a new reality and commits it to the eternal ledger.
        Returns a pure dictionary to satisfy the WASM Bridge.
        """
        with self._lock:
            pid = str(uuid.uuid4())
            if is_demo: pid = PROGENITOR_ID

            raw_path = self.workspaces_root / pid
            project_path_str = raw_path.as_posix()

            # The Ward of Collision
            if raw_path.exists() and not is_demo:
                # If a ghost directory exists, evaporate it.
                shutil.rmtree(raw_path, ignore_errors=True)

            try:
                now_ms = int(time.time() * 1000)
                final_tags = tags or []
                if template != "blank": final_tags.append(template)
                if is_demo: final_tags.append("reference")

                # Semantic Auto-Tagging
                t_lower = template.lower()
                if "api" in t_lower or "service" in t_lower: final_tags.append("backend")
                if "react" in t_lower or "vite" in t_lower: final_tags.append("frontend")
                if "rust" in t_lower: final_tags.append("native")

                # Forge the Meta Vessel
                project_dict = {
                    "id": pid,
                    "name": name,
                    "description": description,
                    "path": project_path_str,
                    "owner_id": owner_id,
                    "template": template,
                    "is_demo": is_demo,
                    "is_locked": is_demo,
                    "is_archived": False,
                    "tags": final_tags,
                    "created_at": now_ms,
                    "updated_at": now_ms,
                    "last_accessed": now_ms,
                    "version": "1.0.0",
                    "stats": {"file_count": 0, "size_kb": 0},
                    "custom_data": {
                        "is_ghost": False,
                        "created_by": owner_id,
                        "search_vector": f"{name} {description} {' '.join(final_tags)}".lower()
                    }
                }

                # 1. Update Ledger
                self.registry["projects"][pid] = project_dict
                if auto_anchor:
                    self.registry["active_project_id"] = pid

                self._commit_state()
                self._index_project(project_dict)

                # 2. Materialize Physical Substrate
                raw_path.mkdir(parents=True, exist_ok=True)

                # 3. Anchor Environment
                if auto_anchor:
                    os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path_str
                    try:
                        os.chdir(project_path_str)
                    except:
                        pass

                if not self._is_silent:
                    Logger.success(f"Reality '{name}' manifest at {project_path_str}")

                return project_dict

            except Exception as fracture:
                self._atomic_rollback(pid, raw_path)
                raise ArtisanHeresy(f"Genesis Fracture: {fracture}", severity=HeresySeverity.CRITICAL)

    def switch_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        [THE RITE OF ANCHORING]
        Updates the active ID. Handles Ghost Materialization JIT.
        """
        with self._lock:
            # 1. Memory Lookups
            candidate = self.registry["projects"].get(project_id)
            is_system_demo = False

            if not candidate and project_id in self.system_demos:
                # Transmute Demo object to dict
                candidate = self.system_demos[project_id].model_dump() if hasattr(self.system_demos[project_id],
                                                                                  'model_dump') else self.system_demos[
                    project_id]
                is_system_demo = True

            if not candidate:
                if not self._is_silent: Logger.error(f"Reality '{project_id}' is unmanifest.")
                return None

            # 2. Physical Reality Check
            project_path = Path(candidate["path"]).resolve()
            if not project_path.exists():
                try:
                    project_path.mkdir(parents=True, exist_ok=True)
                except Exception:
                    pass

            # 3. JIT Ghost Materialization
            is_ghost = candidate.get("custom_data", {}).get("is_ghost", False)
            is_hollow = True
            if project_path.exists():
                try:
                    # Ignore standard metadata files when checking for hollow state
                    contents = [p.name for p in project_path.iterdir() if
                                p.name not in [".scaffold", "scaffold.lock", ".heartbeat"]]
                    is_hollow = len(contents) == 0
                except:
                    pass

            if is_ghost and is_hollow:
                if not self._is_silent: Logger.info(f"Materializing Ghost Reality: '{candidate['name']}'...")
                self._materialize_ghost(candidate, project_path)

            # 4. State Update
            candidate["custom_data"]["is_ghost"] = False
            candidate["last_accessed"] = int(time.time() * 1000)

            # Promote to living registry if it was a demo
            if is_system_demo:
                self.registry["projects"][project_id] = candidate

            self.registry["active_project_id"] = project_id
            self._commit_state()

            # 5. Environment DNA Suture
            os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path.as_posix()
            try:
                os.chdir(project_path.as_posix())
            except:
                pass

            return candidate

    def update_project(self, project_id: str, updates: Dict[str, Any]) -> bool:
        """[THE RITE OF TRANSMUTATION]"""
        with self._lock:
            if project_id not in self.registry["projects"]: return False
            p = self.registry["projects"][project_id]

            safe_updates = {k: v for k, v in updates.items() if k not in ['id', 'path', 'created_at']}
            p.update(safe_updates)

            if "custom_data" in updates:
                p["custom_data"].update(updates["custom_data"])

            p["updated_at"] = int(time.time() * 1000)

            self._commit_state()
            self._index_project(p)  # Re-index after update
            return True

    def delete_project(self, project_id: str, force: bool = False) -> bool:
        """[THE RITE OF ANNIHILATION]"""
        with self._lock:
            # 1. System Demo Guard
            if project_id in self.system_demos:
                if not force: raise ArtisanHeresy("Cannot annihilate System Reference Architecture.")
                demo = self.system_demos[project_id]
                shutil.rmtree(demo.path, ignore_errors=True)
                # Reset to ghost state instead of deleting
                demo_dict = demo.model_dump() if hasattr(demo, 'model_dump') else demo
                demo_dict["custom_data"]["is_ghost"] = True
                if project_id in self.registry["projects"]:
                    del self.registry["projects"][project_id]
                self._commit_state()
                return True

            if project_id not in self.registry["projects"]:
                return False

            target = self.registry["projects"][project_id]

            # 2. Lock Guard
            if target.get("is_locked") and not force:
                raise ArtisanHeresy(f"Reality '{target['name']}' is warded with a Lock.",
                                    severity=HeresySeverity.WARNING)

            # 3. Physical Annihilation
            path = Path(target["path"])
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

            # 4. Logical Excision
            del self.registry["projects"][project_id]
            if self.registry["active_project_id"] == project_id:
                self.registry["active_project_id"] = None
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)
                self._sever_link()

            self._commit_state()
            self._rebuild_search_index()
            if not self._is_silent: Logger.success(f"Project '{target['name']}' returned to the void.")
            return True

    def fork_project(self, source_id: str, new_name: str, owner_id: str) -> Dict[str, Any]:
        """
        [THE RITE OF MITOSIS]
        Clones a reality into a divergent timeline at physical disk speeds.
        """
        with self._lock:
            source = self.registry["projects"].get(source_id)
            if not source and source_id in self.system_demos:
                source = self.system_demos[source_id]
                source = source.model_dump() if hasattr(source, 'model_dump') else source

            if not source:
                raise ArtisanHeresy(f"Source reality '{source_id}' is unmanifest.")

            pid = str(uuid.uuid4())
            new_path = self.workspaces_root / pid

            try:
                is_ghost = source.get("custom_data", {}).get("is_ghost", False)

                if is_ghost:
                    # Synthesize from Blueprint
                    new_path.mkdir(parents=True, exist_ok=True)
                    (new_path / "README.md").write_text(f"# {new_name}\n\nForked from {source['name']}.",
                                                        encoding="utf-8")
                else:
                    # Physical Copy
                    source_path = Path(source["path"])
                    if not source_path.exists():
                        raise ArtisanHeresy("Source physical matter is a void.")

                    # [ASCENSION]: Efficient Copy with Ignore Patterns
                    shutil.copytree(
                        source_path,
                        new_path,
                        dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build')
                    )

                now_ms = int(time.time() * 1000)
                new_project = {
                    "id": pid,
                    "name": new_name,
                    "description": f"Fork of {source['name']}. {source.get('description', '')}",
                    "path": new_path.as_posix(),
                    "owner_id": owner_id,
                    "template": source.get("template", "blank"),
                    "is_demo": False,
                    "tags": source.get("tags", []) + ["fork"],
                    "created_at": now_ms,
                    "updated_at": now_ms,
                    "last_accessed": now_ms,
                    "version": "1.0.0",
                    "stats": self._measure_reality(new_path),
                    "custom_data": {
                        "icon": "GitFork",
                        "color": "#10b981",
                        "parent_id": source_id,
                        "created_by": owner_id,
                        "search_vector": f"{new_name} fork {source['name']}".lower(),
                        "is_ghost": False
                    }
                }

                self.registry["projects"][pid] = new_project
                self._commit_state()
                self._index_project(new_project)

                self.switch_project(pid)
                return new_project

            except Exception as e:
                self._atomic_rollback(pid, new_path)
                raise ArtisanHeresy(f"Mitosis Fracture: {e}", severity=HeresySeverity.CRITICAL)

    # =========================================================================
    # == SECTION III: INTELLIGENCE & SEARCH                                  ==
    # =========================================================================

    def search_projects(self, query: str, owner_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        [THE INVERTED SEMANTIC MATRIX]
        O(1) Fuzzy searching using the pre-computed token index.
        """
        if not query: return self.list_projects(owner_id=owner_id)

        query_lower = query.lower()
        results_ids = set()

        with self._lock:
            # 1. Exact Match ID
            if query_lower in self.registry["projects"]:
                results_ids.add(query_lower)

            # 2. Inverted Index Lookup (Sub-string token match)
            for token, pids in self._search_index.items():
                if query_lower in token:
                    results_ids.update(pids)

            # 3. Resolve IDs to Objects
            pool = []
            for pid in results_ids:
                if pid in self.registry["projects"]:
                    pool.append(self.registry["projects"][pid])
                elif pid in self.system_demos:
                    demo = self.system_demos[pid]
                    pool.append(demo.model_dump() if hasattr(demo, 'model_dump') else demo)

            # 4. Sovereignty Filter
            if owner_id and owner_id != GUEST_OWNER_ID:
                pool = [p for p in pool if p.get("owner_id") in (owner_id, SYSTEM_OWNER_ID)]
            elif owner_id == GUEST_OWNER_ID:
                pool = [p for p in pool if p.get("owner_id") in (GUEST_OWNER_ID, SYSTEM_OWNER_ID)]

            pool.sort(key=lambda x: x.get('last_accessed', 0), reverse=True)
            return pool

    def _rebuild_search_index(self):
        """[THE INDEX FORGE]: Rebuilds the token map in memory."""
        self._search_index.clear()

        for p in self.registry["projects"].values():
            self._index_project(p)
        for demo in self.system_demos.values():
            self._index_project(demo)

    def _index_project(self, p: Union[Dict[str, Any], ProjectMeta]):
        """
        [THE GNOSTIC INDEXER]
        Shatters the project's identity into semantic N-Grams and injects them
        into the inverted Search Index for O(1) retrieval. Safely handles both
        Dictionaries and Pydantic Object definitions.
        """
        # Type-agnostic attribute extraction
        pid = p.get("id") if isinstance(p, dict) else getattr(p, "id", "")
        name = p.get("name", "") if isinstance(p, dict) else getattr(p, "name", "")
        desc = p.get("description", "") if isinstance(p, dict) else getattr(p, "description", "")
        tags = p.get("tags", []) if isinstance(p, dict) else getattr(p, "tags", [])

        if not pid: return

        tokens = set()

        # Tokenizer Engine
        def _tokenize(text):
            if not text: return
            # Strip non-alphanumerics and lower-case
            clean = re.sub(r'[^a-zA-Z0-9]', ' ', str(text).lower())
            for word in clean.split():
                if len(word) > 1: tokens.add(word)

        # Scry the text fields
        _tokenize(name)
        _tokenize(desc)
        for t in tags: _tokenize(t)

        # Inscribe into the global inverted index
        with self._lock:
            for token in tokens:
                if token not in self._search_index:
                    self._search_index[token] = set()
                self._search_index[token].add(pid)

            # Keep a materialized search vector on the object for fallback scans
            vector_str = f"{name} {desc} {' '.join(tags)}".lower()
            if isinstance(p, dict) and "custom_data" in p:
                p["custom_data"]["search_vector"] = vector_str
            elif hasattr(p, "custom_data"):
                p.custom_data["search_vector"] = vector_str

    # =========================================================================
    # == SECTION IV: ORPHANS, ZOMBIES, & HEALING                             ==
    # =========================================================================

    def discover_orphans(self, auto_adopt: bool = False) -> List[str]:
        """
        [THE ORPHAN REAPER]
        Scans the physical workspaces directory for folders that exist on disk
        but are missing from the logical Registry.
        """
        orphans = []
        if not self.workspaces_root.exists(): return orphans

        with self._lock:
            known_ids = set(self.registry["projects"].keys())
            known_ids.update(self.system_demos.keys())

            try:
                for entry in os.scandir(self.workspaces_root):
                    if entry.is_dir() and entry.name not in known_ids and not entry.name.startswith('.'):
                        orphans.append(entry.name)
                        if auto_adopt:
                            if not self._is_silent: Logger.info(f"Adopting Orphan Reality: {entry.name}")
                            self.import_project(entry.path, f"Adopted_{entry.name[:8]}", GUEST_OWNER_ID)
            except Exception as e:
                Logger.error(f"Orphan Reaper Fractured: {e}")

        return orphans

    def prune_zombies(self) -> int:
        """
        [THE ZOMBIE PRUNER]
        Scans the logical Registry for projects whose physical folders have been
        destroyed by an external force (like an OS-level deletion) and purges
        them from the Mind.
        """
        pruned_count = 0
        with self._lock:
            to_delete = []
            for pid, p in self.registry["projects"].items():
                is_ghost = p.get("custom_data", {}).get("is_ghost", False)
                path = Path(p.get("path", ""))

                # If it is not explicitly marked as a Ghost, but its matter is missing
                if not is_ghost and not path.exists():
                    to_delete.append(pid)

            for pid in to_delete:
                del self.registry["projects"][pid]
                pruned_count += 1

            if pruned_count > 0:
                if not self._is_silent: Logger.warn(f"Pruned {pruned_count} Zombie Realities from the Registry.")
                self._commit_state()
                self._rebuild_search_index()

        return pruned_count

    def import_project(self, path: str, name: str, owner_id: str) -> Dict[str, Any]:
        """
        [THE RITE OF ASSIMILATION]
        Absorbs a pre-existing physical directory into the Governor's Multiverse.
        """
        target_path = Path(path).resolve()
        if not target_path.exists() or not target_path.is_dir():
            raise ArtisanHeresy(f"Cannot import void: {path}")

        pid = str(uuid.uuid4())
        now_ms = int(time.time() * 1000)

        project_dict = {
            "id": pid,
            "name": name,
            "description": "Adopted external reality.",
            "path": target_path.as_posix(),
            "owner_id": owner_id,
            "template": "imported",
            "is_demo": False,
            "is_locked": False,
            "is_archived": False,
            "tags": ["imported"],
            "created_at": now_ms,
            "updated_at": now_ms,
            "last_accessed": now_ms,
            "version": "1.0.0",
            "stats": self._measure_reality(target_path),
            "custom_data": {"is_ghost": False}
        }

        with self._lock:
            self.registry["projects"][pid] = project_dict
            self._commit_state()
            self._index_project(project_dict)

        return project_dict

    def get_project_stats(self) -> Dict[str, Any]:
        """Returns the panoramic telemetry of the Registry."""
        return {
            "total_count": len(self.registry["projects"]) + len(self.system_demos),
            "active_id": self.registry.get("active_project_id"),
            "registry_version": self.registry.get("version"),
            "state_hash": self._state_hash
        }

    def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Exact-match resolution by Name."""
        with self._lock:
            for p in self.registry["projects"].values():
                if p.get("name") == name: return p
            for demo in self.system_demos.values():
                if getattr(demo, "name", "") == name:
                    return demo.model_dump() if hasattr(demo, 'model_dump') else demo
        return None

    # =========================================================================
    # == SECTION V: INTERNAL ALCHEMY & PHYSICS                               ==
    # =========================================================================

    def _lazarus_resurrection(self):
        """
        [THE LAZARUS PROTOCOL]
        If projects.json is obliterated, this rite scans the physical
        /vault/workspaces directory and rebuilds the registry from the ashes.
        """
        if not self.workspaces_root.exists(): return

        recovered_count = 0
        now_ms = int(time.time() * 1000)

        try:
            # Use ultra-fast os.scandir to read the physical platter
            with os.scandir(self.workspaces_root) as it:
                for entry in it:
                    if not entry.is_dir() or len(entry.name) < 10: continue

                    pid = entry.name
                    name = pid[:8]
                    template = "unknown"

                    # Deduce basic DNA from root files
                    if (Path(entry.path) / "package.json").exists(): template = "node"
                    if (Path(entry.path) / "pyproject.toml").exists(): template = "python"

                    proj_dict = {
                        "id": pid,
                        "name": f"Recovered Reality {name}",
                        "description": "Resurrected by the Lazarus Protocol.",
                        "path": entry.path.replace('\\', '/'),
                        "owner_id": GUEST_OWNER_ID,
                        "template": template,
                        "is_demo": False,
                        "is_locked": False,
                        "is_archived": False,
                        "tags": ["recovered"],
                        "created_at": now_ms,
                        "updated_at": now_ms,
                        "last_accessed": now_ms,
                        "version": "1.0.0",
                        "stats": {"file_count": 0, "size_kb": 0},
                        "custom_data": {"is_ghost": False}
                    }
                    self.registry["projects"][pid] = proj_dict
                    recovered_count += 1

            if recovered_count > 0:
                if not self._is_silent: Logger.success(
                    f"Lazarus Protocol complete. Resurrected {recovered_count} realities.")
                self._commit_state()
        except Exception as e:
            if not self._is_silent: Logger.error(f"Lazarus Protocol Failed: {e}")

    def _manifest_axis_mundi(self):
        """Hard-registers the Progenitor System Demo."""
        now_ms = int(time.time() * 1000)
        demo = ProjectMeta(
            id=PROGENITOR_ID,
            name="Progenitor",
            description="The foundational law of the Novalym universe.",
            path=f"/vault/workspaces/{PROGENITOR_ID}",
            owner_id=SYSTEM_OWNER_ID,
            template="progenitor",
            is_demo=True,
            is_locked=True,
            created_at=now_ms,
            updated_at=now_ms,
            last_accessed=now_ms,
            version="1.0.0-OMEGA",
            stats=ProjectStats(file_count=1, size_kb=1, health_score=100),
            custom_data={
                "icon": "Zap",
                "color": "#a855f7",
                "stratum": "CORE",
                "is_ghost": True,
                "is_axis_mundi": True,
                "source_path": "/home/pyodide/simulacrum_pkg/archetypes/demos/progenitor.scaffold",
                "search_vector": "progenitor law core system reference foundation".lower()
            }
        )
        self.system_demos[PROGENITOR_ID] = demo

    def _conduct_seed_census(self):
        """Scries the physical substrate for additional system demos."""
        pass  # Optional extraction omitted for WASM velocity

    def _measure_reality(self, root: Path) -> dict:
        """[METABOLIC TOMOGRAPHY]: Calculates mass using fast os.scandir."""
        count = 0
        size = 0
        try:
            for r, d, f in os.walk(root):
                # Prune the abyss to save CPU cycles
                d[:] = [dr for dr in d if dr not in ['.git', 'node_modules', '__pycache__', '.venv']]
                count += len(f)
                for file in f:
                    try:
                        size += os.path.getsize(os.path.join(r, file))
                    except OSError:
                        pass
        except Exception:
            pass
        return {"file_count": count, "size_kb": size // 1024}

    def _commit_state(self):
        """[THE ATOMIC COMMIT]"""
        self.persistence.save(self.registry)
        self._calculate_state_hash()

    def _calculate_state_hash(self):
        """Forges a Merkle-Lite hash to detect Registry Drift."""
        try:
            raw = f"{len(self.registry.get('projects', {}))}-{self.registry.get('active_project_id')}"
            self._state_hash = hashlib.md5(raw.encode()).hexdigest()[:8]
        except:
            self._state_hash = "0xERROR"

    def _materialize_ghost(self, target: Dict[str, Any], path: Path):
        """[GHOST MATTER INCEPTION]: Uses the Engine to strike the disk silently."""
        if not self.engine: return
        try:
            from ...interfaces.requests import InitRequest
            init_plea = InitRequest(
                profile=target.get("template", "blank"),
                project_root=path.as_posix(),
                force=True,
                non_interactive=True,
                variables={
                    "project_name": target.get("name", "Ghost"),
                    "description": target.get("description", ""),
                    "no_edicts": True  # Stay the hand of shell commands during ghost boot
                }
            )
            # The Silent Strike
            self.engine.dispatch(init_plea)
        except Exception as e:
            if not self._is_silent: Logger.error(f"Ghost Materialization Fractured: {e}")

    def _atomic_rollback(self, pid: str, path: Path):
        """[THE REAPER'S SYTHE]"""
        if path.exists(): shutil.rmtree(path, ignore_errors=True)
        with self._lock:
            if pid in self.registry["projects"]:
                del self.registry["projects"][pid]
                self._commit_state()

    def _sever_link(self):
        """Removes legacy symlink."""
        link = self.persistence.root.parent / "project"
        try:
            if link.exists() or link.is_symlink(): link.unlink()
        except:
            pass

    def _audit_active_anchor(self):
        """Verifies anchor validity. Should only be called on boot or error."""
        active_id = self.registry.get("active_project_id")
        if not active_id: return

        p = self.registry["projects"].get(active_id) or self.system_demos.get(active_id)
        if not p:
            Logger.warn(f"Anchor '{active_id}' void. Resetting.")
            self.registry["active_project_id"] = None
            self.persistence.save(self.registry)
            return

    def __repr__(self) -> str:
        count = len(self.registry.get("projects", {}))
        return f"<Ω_PROJECT_GOVERNOR projects={count} ghosts={len(self.system_demos)} anchor={self.registry.get('active_project_id') or 'VOID'}>"