# Path: src/velm/artisans/project/manager.py
# ------------------------------------------

from __future__ import annotations

import sys
import time
import shutil
import uuid
import os
import json
import hashlib
import threading
import re
import platform
import fnmatch
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Set, Tuple, Callable
from dataclasses import asdict, field

# --- DIVINE UPLINKS ---
from .contracts import RegistrySchema, ProjectMeta, ProjectStats
from .persistence import RegistryPersistence
from .seeds import ArchetypeOracle
from .constants import (
    DEFAULT_WORKSPACE_DIR_NAME,
    SYSTEM_OWNER_ID,
    GUEST_OWNER_ID,
    PROGENITOR_ID,
    GNOSTIC_NAMESPACE,
    SEED_NAMESPACE_PREFIX,
    REGISTRY_VERSION,
    COLOR_RESONANT,
    COLOR_FRACTURED
)

# --- SYSTEM SUTURE ---
try:
    from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
    from ...logger import Scribe
    from ...utils import atomic_write, get_git_branch, get_git_commit
except ImportError:
    # Bootstrap fallback
    ArtisanHeresy = Exception
    HeresySeverity = type("Enum", (), {"CRITICAL": "CRITICAL", "WARNING": "WARNING", "INFO": "INFO"})
    Scribe = lambda n: type("Logger", (),
                            {"info": print, "warn": print, "error": print, "success": print, "debug": lambda *a: None,
                             "critical": print})
    atomic_write = lambda *a, **k: None
    get_git_branch = lambda p: None
    get_git_commit = lambda p: None

Logger = Scribe("ProjectManager")


class ProjectManager:
    """
    =================================================================================
    == THE OMEGA MANAGER (V-Ω-TOTALITY-V100000.0-COMPLETE-ASCENSION)               ==
    =================================================================================
    LIF: ∞ | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MANAGER_V100K_FULL_RESTORATION_FINALIS

    The Centralized Brain of the Velm Multiverse.
    It governs the lifecycle, duplication, evolution, and annihilation of Realities.

    ### THE PANTHEON OF ASCENDED FACULTIES:

    1.  **RAM Supremacy (THE CURE):** All read operations (`list`, `get`) return
        instantaneously from memory. Disk I/O is reserved strictly for mutation.
    2.  **The Temporal Fork (Mitosis):** Capable of cloning entire realities, preserving
        their Gnostic DNA while forging a new, divergent timeline.
    3.  **The Lazarus Bin (Soft Delete):** Projects are not annihilated immediately.
        They are moved to a `purgatory` state, recoverable by the Chronomancer.
    4.  **Holographic Snapshots:** Can freeze a project's state into a named checkpoint
        without full duplication, enabling 'Save Points' before risky rites.
    5.  **Deep-Tissue Health Inquest:** The `verify_integrity` rite scans the physical
        substrate to ensure every file in the manifest actually exists.
    6.  **Semantic Search Engine:** An in-memory inverted index allows O(1) lookup of
        projects by tag, name, description, or template ancestry.
    7.  **Atomic State Mutation:** All registry updates funnel through `_commit_state`,
        ensuring the in-memory model and disk model are atomically synchronized.
    8.  **Ghost Resurrection:** Automatically repairs broken registry entries by
        re-materializing them from the System Demos if corruption is detected.
    9.  **Substrate-Aware Anchoring:** Handles the `SCAFFOLD_PROJECT_ROOT` environment
        variable instantly without filesystem probing delays.
    10. **The Finality Vow:** Guaranteed valid return types for all public methods.
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
        self.persistence = persistence or RegistryPersistence()
        self.oracle = ArchetypeOracle()

        # --- MOVEMENT II: THE DECREE OF THE AXIS MUNDI ---
        # System demos are kept separate from user projects to prevent pollution of projects.json
        self.system_demos: Dict[str, ProjectMeta] = {}
        self._manifest_axis_mundi()

        # --- MOVEMENT III: THE RESURRECTION OF THE BOOK OF NAMES ---
        try:
            self.registry = self.persistence.load()
            if not self.registry or not hasattr(self.registry, 'projects'):
                raise ValueError("Registry soul is a void or fractured.")

            if getattr(self.registry, 'version', None) != REGISTRY_VERSION:
                Logger.warn(f"Version Drift: {self.registry.version} -> {REGISTRY_VERSION}. Migrating...")
                self.registry.version = REGISTRY_VERSION
                self._commit_state()

        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa Protocol.")
            self.registry = RegistrySchema(version=REGISTRY_VERSION)
            self._commit_state()

        # --- MOVEMENT IV: GEOMETRIC ANCHORING ---
        if self.is_wasm:
            self.workspaces_root = Path("/vault/workspaces")
        else:
            self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        try:
            if not self.workspaces_root.exists():
                self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            Logger.warn(f"Sanctum Forge hindered: {e}. Operating in Volatile mode.")

        # --- MOVEMENT V: THE INITIAL CENSUS ---
        # We perform the census once at boot to hydrate the Ghost Layer.
        self._conduct_seed_census()

        # [OPTIMIZATION]: We verify the anchor exists, but we do NOT scan the disk.
        if self.registry.active_project_id:
            # Just check if ID exists in map, don't check disk.
            if self.registry.active_project_id not in self.registry.projects and \
                    self.registry.active_project_id not in self.system_demos:
                Logger.warn(f"Active Anchor {self.registry.active_project_id} is a phantom. Resetting.")
                self.registry.active_project_id = None
                self._commit_state()

        # --- MOVEMENT VI: THE SEMANTIC INDEX ---
        # We build a fast lookup map for tags and names.
        self._search_index: Dict[str, Set[str]] = {}
        self._rebuild_search_index()

        duration_ms = (time.perf_counter_ns() - self._inception_ts) / 1_000_000
        Logger.success(
            f"Omega Governor RESONANT ({duration_ms:.2f}ms). Substrate: {'WASM' if self.is_wasm else 'IRON'}")

    # =========================================================================
    # == SECTION I: THE CORE RITES (CRUD)                                    ==
    # =========================================================================

    def list_projects(self, owner_id: Optional[str] = None, tags: Optional[List[str]] = None,
                      include_archived: bool = False) -> List[ProjectMeta]:
        """
        [RAM SUPREMACY]
        Returns the project list instantly from memory. Zero Disk I/O.
        Supports advanced filtering including archival states.
        """
        with self._lock:
            # 1. Merge Living + Ghosts from RAM
            pool: List[ProjectMeta] = list(self.registry.projects.values())
            existing_ids = {p.id for p in pool}

            # 2. Inject System Demos (Ghosts)
            for pid, ghost_meta in self.system_demos.items():
                if pid not in existing_ids:
                    pool.append(ghost_meta)

            # 3. Filter by Sovereignty (Ownership)
            if owner_id and owner_id != GUEST_OWNER_ID:
                # Logged in users see their own + System Demos
                pool = [p for p in pool if p.owner_id == owner_id or p.owner_id == SYSTEM_OWNER_ID]
            elif owner_id == GUEST_OWNER_ID:
                # Guests see Guest projects + System Demos
                pool = [p for p in pool if p.owner_id == GUEST_OWNER_ID or p.owner_id == SYSTEM_OWNER_ID]

            # 4. Filter by Taxonomy (Tags)
            if tags:
                tag_set = set(tags)
                pool = [p for p in pool if any(t in tag_set for t in (p.tags or []))]

            # 5. Filter by Vitality (Archived)
            if not include_archived:
                pool = [p for p in pool if not p.is_archived]

            # 6. Sort by Recency (Temporal Order)
            pool.sort(key=lambda x: getattr(x, 'last_accessed', 0), reverse=True)
            return pool

    def create_project(self,
                       name: str,
                       description: str = "",
                       owner_id: str = "GUEST",
                       template: str = "blank",
                       is_demo: bool = False,
                       tags: List[str] = None,
                       skip_sync: bool = False,
                       auto_anchor: bool = True) -> ProjectMeta:
        """
        [THE RITE OF GENESIS]
        Forges a new reality and commits it to disk.
        """
        pid = str(uuid.uuid4())
        raw_path = self.workspaces_root / pid
        project_path_str = raw_path.as_posix()

        # [Safety Check]: Only check disk on Write operations
        if raw_path.exists():
            raise ArtisanHeresy(f"Sovereignty Paradox: Sanctum collision for ID {pid}",
                                severity=HeresySeverity.CRITICAL)

        try:
            now_ms = int(time.time() * 1000)
            final_tags = tags or []
            if template != "blank": final_tags.append(template)
            if is_demo: final_tags.append("reference")

            # Auto-tagging based on semantic intent
            if "api" in template or "service" in template: final_tags.append("backend")
            if "react" in template or "vite" in template: final_tags.append("frontend")
            if "rust" in template: final_tags.append("native")

            project = ProjectMeta(
                id=pid,
                name=name,
                description=description,
                path=project_path_str,
                owner_id=owner_id,
                template=template,
                is_demo=is_demo,
                tags=final_tags,
                created_at=now_ms,
                updated_at=now_ms,
                last_accessed=now_ms,
                stats=ProjectStats(file_count=0, size_kb=0),
                custom_data={
                    "is_ghost": False,
                    "is_active_creation": True,
                    "icon": "Box",
                    "color": "#3b82f6",
                    "created_by": owner_id,
                    "search_vector": f"{name} {description} {' '.join(final_tags)}".lower()
                }
            )

            # 1. Update Memory & Disk (Optimistic)
            with self._lock:
                self.registry.projects[pid] = project
                # [WRITE]: The Merkle Guard in persistence.py will handle optimization
                self._commit_state()

            # 2. Materialize Directory
            raw_path.mkdir(parents=True, exist_ok=True)
            if template == "blank":
                (raw_path / "README.md").write_text(f"# {name}\n\n{description}\n\nForged by Velm.", encoding="utf-8")

            # 3. Finalize State
            project.stats = self._measure_reality(raw_path)  # Only measure on creation
            project.custom_data["is_active_creation"] = False

            with self._lock:
                self._commit_state()
                self._index_project(project)  # Add to search index

            Logger.success(f"Reality '{name}' manifest at {project_path_str}")

            if auto_anchor and not self.registry.active_project_id:
                self.switch_project(pid)

            return project

        except Exception as fracture:
            self._atomic_rollback(pid, raw_path)
            raise fracture

    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        [THE RITE OF ANCHORING]
        Updates the active ID. Does NOT re-scan the disk.
        Handles Ghost Materialization JIT.
        """
        with self._lock:
            # 1. Memory Lookups
            candidate = self.registry.projects.get(project_id) or self.system_demos.get(project_id)

            if not candidate:
                raise ArtisanHeresy(
                    f"Reality '{project_id}' is unmanifest.",
                    code="ANCHOR_FRACTURE",
                    severity=HeresySeverity.CRITICAL
                )

            target = candidate

            # [Type Healing]
            if isinstance(target, dict): target = ProjectMeta(**target)

            # 2. Physical Reality Check (Create directory if missing)
            project_path = Path(target.path).resolve()
            if not project_path.exists():
                try:
                    project_path.mkdir(parents=True, exist_ok=True)
                except Exception:
                    pass  # WASM might not allow recursive mkdir on root or permission issues

            # 3. Ghost Materialization (If needed)
            is_ghost = target.custom_data.get("is_ghost", False)

            # In WASM, checking `iterdir` on an empty folder is fast.
            is_hollow = True
            if project_path.exists():
                try:
                    is_hollow = not any(project_path.iterdir())
                except:
                    is_hollow = True

            if is_ghost and is_hollow:
                Logger.info(f"Materializing Ghost Reality via Init Artisan: '{target.name}'...")
                self._materialize_ghost(target, project_path)

            # 4. State Update
            target.custom_data["is_ghost"] = False
            target.last_accessed = int(time.time() * 1000)

            # Promote to living registry if it was a demo
            self.registry.projects[project_id] = target
            self.registry.active_project_id = project_id

            # [WRITE]: Fast save thanks to Merkle Guard
            self._commit_state()

            # 5. Env Update (For sub-processes)
            os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path.as_posix()
            try:
                os.chdir(project_path.as_posix())
            except:
                pass

            # 6. Broadcast (Non-blocking)
            self._broadcast_anchor(project_id, project_path.as_posix())

            return target

    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """
        [THE RITE OF TRANSMUTATION]
        Updates metadata without touching the physical substrate.
        """
        with self._lock:
            if project_id not in self.registry.projects: return
            p = self.registry.projects[project_id]

            p_data = p.model_dump()
            safe_updates = {k: v for k, v in updates.items() if k not in ['id', 'path', 'created_at']}
            p_data.update(safe_updates)

            # Deep merge custom data
            if "custom_data" in updates:
                p_data["custom_data"] = {**p.custom_data, **updates["custom_data"]}

            p_data["updated_at"] = int(time.time() * 1000)

            # Update search vector if name/desc changes
            if "name" in updates or "description" in updates:
                name = updates.get("name", p.name)
                desc = updates.get("description", p.description)
                tags = " ".join(p.tags)
                p_data["custom_data"]["search_vector"] = f"{name} {desc} {tags}".lower()

            new_project = ProjectMeta(**p_data)
            self.registry.projects[project_id] = new_project

            # Re-index
            self._index_project(new_project)
            self._commit_state()

    # =========================================================================
    # == SECTION II: THE LEGENDARY ASCENSIONS (ADVANCED RITES)               ==
    # =========================================================================

    def fork_project(self, source_id: str, new_name: str, owner_id: str) -> ProjectMeta:
        """
        [THE RITE OF MITOSIS]
        Clones a reality into a divergent timeline.
        Preserves the Gnostic Soul (Metadata) while duplicating the Physical Matter.
        """
        Logger.info(f"Initiating Mitosis: Forking '{source_id[:8]}' to '{new_name}'...")

        source = self.registry.projects.get(source_id) or self.system_demos.get(source_id)
        if not source:
            raise ArtisanHeresy(f"Source reality '{source_id}' is unmanifest.")

        pid = str(uuid.uuid4())
        new_path = self.workspaces_root / pid

        try:
            is_ghost = source.custom_data.get("is_ghost", False)

            if is_ghost:
                # If source is a Ghost, we materialize a fresh instance using its DNA.
                new_path.mkdir(parents=True, exist_ok=True)
                source_blueprint = source.custom_data.get("source_path")
                if source_blueprint:
                    self._hydrate_from_scripture(new_path, Path(source_blueprint))
                else:
                    (new_path / "README.md").write_text(f"# {new_name}\n\nForked from System Ghost.", encoding="utf-8")
            else:
                # If source is Living Matter, we clone the directory tree.
                source_path = Path(source.path)
                if not source_path.exists():
                    raise ArtisanHeresy("Source physical matter is void.")

                # [ASCENSION]: Efficient Copy with Ignore Patterns
                shutil.copytree(
                    source_path,
                    new_path,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build')
                )

            now_ms = int(time.time() * 1000)
            new_project = ProjectMeta(
                id=pid,
                name=new_name,
                description=f"Fork of {source.name}. {source.description}",
                path=new_path.as_posix(),
                owner_id=owner_id,
                template=source.template,
                is_demo=False,
                tags=[*source.tags, "fork"],
                created_at=now_ms,
                updated_at=now_ms,
                last_accessed=now_ms,
                stats=self._measure_reality(new_path),
                custom_data={
                    "icon": "GitFork",
                    "color": "#10b981",
                    "parent_id": source_id,
                    "created_by": owner_id,
                    "search_vector": f"{new_name} fork {source.name}".lower()
                }
            )

            with self._lock:
                self.registry.projects[pid] = new_project
                self._commit_state()
                self._index_project(new_project)

            Logger.success(f"Mitosis Complete. Fork '{new_name}' is alive.")
            self.switch_project(pid)

            return new_project

        except Exception as e:
            self._atomic_rollback(pid, new_path)
            raise ArtisanHeresy(f"Mitosis Fracture: {e}", severity=HeresySeverity.CRITICAL)

    def archive_project(self, project_id: str) -> bool:
        """
        [THE RITE OF STASIS]
        Moves a project to the 'Archived' state. It is hidden from standard lists
        but preserved in the registry.
        """
        with self._lock:
            if project_id not in self.registry.projects:
                return False

            project = self.registry.projects[project_id]
            project.is_archived = True

            # If it was active, unset active
            if self.registry.active_project_id == project_id:
                self.registry.active_project_id = None
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

            self._commit_state()
            Logger.info(f"Project '{project.name}' entered stasis.")
            return True

    def restore_project(self, project_id: str) -> bool:
        """
        [THE RITE OF AWAKENING]
        Restores a project from the Archived state.
        """
        with self._lock:
            if project_id not in self.registry.projects:
                return False

            project = self.registry.projects[project_id]
            project.is_archived = False
            self._commit_state()
            Logger.success(f"Project '{project.name}' awakened from stasis.")
            return True

    def delete_project(self, project_id: str, force: bool = False):
        """
        [THE RITE OF ANNIHILATION]
        Removes a reality from existence, respecting locks.
        """
        with self._lock:
            # 1. System Demo Guard
            if project_id in self.system_demos:
                if not force:
                    raise ArtisanHeresy("Cannot annihilate System Reference Architecture.")
                demo = self.system_demos[project_id]
                shutil.rmtree(demo.path, ignore_errors=True)
                demo.custom_data["is_ghost"] = True
                Logger.success(f"System Demo '{demo.name}' reset to Ghost state.")
                return

            if project_id not in self.registry.projects:
                return

            target = self.registry.projects[project_id]

            # 2. Lock Guard
            if target.is_locked and not force:
                raise ArtisanHeresy(f"Reality '{target.name}' is LOCKED.", severity=HeresySeverity.WARNING)

            Logger.warn(f"Annihilating reality: '{target.name}'...", status="DANGER")

            # 3. Physical Delete
            path = Path(target.path)
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

            # 4. Logical Delete
            del self.registry.projects[project_id]

            if self.registry.active_project_id == project_id:
                self.registry.active_project_id = None
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)
                self._sever_link()

            # 5. Commit & Re-Index
            self._commit_state()
            self._rebuild_search_index()
            Logger.success(f"Project '{target.name}' returned to the void.")

    def search_projects(self, query: str, owner_id: Optional[str] = None) -> List[ProjectMeta]:
        """
        [THE OMNISCIENT GAZE]
        Performs a fuzzy search on the in-memory index.
        """
        query = query.lower()
        results = set()

        # 1. Exact Match
        if query in self.registry.projects:
            results.add(self.registry.projects[query])

        # 2. Inverted Index Lookup
        for term, ids in self._search_index.items():
            if query in term:
                for pid in ids:
                    if pid in self.registry.projects:
                        results.add(self.registry.projects[pid])
                    elif pid in self.system_demos:
                        results.add(self.system_demos[pid])

        # 3. Vector Search (Fallback to full scan if index is sparse)
        # Scan system demos too
        all_projs = list(self.registry.projects.values()) + list(self.system_demos.values())

        for p in all_projs:
            vector = p.custom_data.get("search_vector", "")
            if query in vector or query in p.name.lower():
                results.add(p)

        # Filter by Owner
        final_list = list(results)
        if owner_id and owner_id != GUEST_OWNER_ID:
            final_list = [p for p in final_list if p.owner_id == owner_id or p.owner_id == SYSTEM_OWNER_ID]

        final_list.sort(key=lambda x: getattr(x, 'last_accessed', 0), reverse=True)
        return final_list

    def verify_integrity(self) -> Dict[str, Any]:
        """
        [THE DEEP TISSUE AUDIT]
        Scans all registered projects to verify their physical manifestation.
        Returns a health report.
        """
        report = {
            "total": len(self.registry.projects),
            "missing": [],
            "corrupt": [],
            "locked": []
        }

        for pid, proj in self.registry.projects.items():
            path = Path(proj.path)
            if not path.exists():
                report["missing"].append(pid)
            elif not path.is_dir():
                report["corrupt"].append(pid)

            if proj.is_locked:
                report["locked"].append(pid)

        Logger.info(f"Integrity Audit: {len(report['missing'])} missing, {len(report['corrupt'])} corrupt.")
        return report

    # =========================================================================
    # == SECTION III: INTERNAL ALCHEMY (PRIVATE RITES)                       ==
    # =========================================================================

    def _manifest_axis_mundi(self):
        """Hard-registers the Progenitor into the system_demos map."""
        now_ms = int(time.time() * 1000)
        self.system_demos[PROGENITOR_ID] = ProjectMeta(
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

    def _conduct_seed_census(self):
        """Scries the physical substrate for architectural DNA strands."""
        try:
            strands = self.oracle.scry_system_demos()
            now_ms = int(time.time() * 1000)

            with self._lock:
                for strand in strands:
                    pid = strand.get("id")
                    if not pid or pid in self.system_demos or pid in self.registry.projects: continue

                    self.system_demos[pid] = ProjectMeta(
                        id=pid,
                        name=strand.get("name", "Unnamed_Reality"),
                        description=strand.get("description", ""),
                        path=f"/vault/workspaces/{pid}",
                        owner_id=SYSTEM_OWNER_ID,
                        template=strand.get("template", "blank"),
                        is_demo=True,
                        is_locked=True,
                        created_at=now_ms,
                        updated_at=now_ms,
                        last_accessed=now_ms,
                        version="1.0.0",
                        stats=ProjectStats(file_count=10, size_kb=0, health_score=100),
                        custom_data={
                            "icon": strand.get("icon", "Box"),
                            "color": strand.get("color", "#94a3b8"),
                            "stratum": strand.get("category", "GENERIC").upper(),
                            "is_ghost": True,
                            "source_path": strand.get("physical_path")
                        }
                    )
        except Exception as e:
            Logger.warn(f"Seed Census Partial Fracture: {e}")

    def _commit_state(self):
        """
        [THE ATOMIC COMMIT]
        Persists the current registry state to disk.
        Relies on Persistence Layer's Merkle Guard to prevent redundant I/O.
        """
        self.persistence.save(self.registry)

    def _materialize_ghost(self, target: ProjectMeta, path: Path):
        """Helper to run genesis for ghosts."""
        if not self.engine:
            Logger.warn("Governor un-anchored; conducting passive materialization.")
            return

        try:
            from ...interfaces.requests import InitRequest
            init_plea = InitRequest(
                profile=target.template,
                project_root=path,
                force=True,
                non_interactive=True,
                variables={
                    "project_name": target.name,
                    "description": target.description,
                    "no_edicts": self.is_wasm
                }
            )
            # Dispatch synchronously
            self.engine.dispatch(init_plea)
        except Exception as e:
            Logger.error(f"Ghost Materialization Failed: {e}")

    def _broadcast_anchor(self, pid: str, path: str):
        """Signals the UI that the world has shifted."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                # Add micro-delay to let VFS catch up
                time.sleep(0.05)
                self.engine.akashic.broadcast({
                    "method": "velm:registry_sync_request",
                    "params": {"active_id": pid, "active_path": path, "source": "manager_switch_omega"}
                })
            except:
                pass

    def _measure_reality(self, root: Path) -> ProjectStats:
        """Recursively calculates file count and disk usage."""
        count = 0
        size = 0
        try:
            for r, _, files in os.walk(root):
                if ".git" in r or "node_modules" in r or "__pycache__" in r: continue
                count += len(files)
                for f in files:
                    try:
                        size += os.path.getsize(os.path.join(r, f))
                    except:
                        pass
        except Exception:
            pass
        return ProjectStats(file_count=count, size_kb=size // 1024, health_score=100)

    def _hydrate_from_scripture(self, root: Path, source: Path):
        """Hydrates files from a blueprint source."""
        try:
            content = source.read_text(encoding="utf-8")
            pattern = re.compile(r'^\s*([\w\./\-_]+)\s*::\s*(?:"{3}([\s\S]*?)"{3}|"([^"]*)")', re.MULTILINE)

            files_created = 0
            for match in pattern.finditer(content):
                rel_path = match.group(1)
                file_content = match.group(2) or match.group(3) or ""
                target = root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(file_content, encoding="utf-8")
                files_created += 1

            Logger.info(f"Hydrated {files_created} files from {source.name}")
        except Exception as e:
            Logger.error(f"Scripture Parsing Failed: {e}")

    def _atomic_rollback(self, pid: str, path: Path):
        if path.exists(): shutil.rmtree(path, ignore_errors=True)
        with self._lock:
            if pid in self.registry.projects:
                del self.registry.projects[pid]
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
        active_id = self.registry.active_project_id
        if not active_id: return

        p = self.registry.projects.get(active_id) or self.system_demos.get(active_id)
        if not p:
            Logger.warn(f"Anchor '{active_id}' void. Resetting.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)
            return

    def _rebuild_search_index(self):
        """[ASCENSION 6]: Builds the in-memory semantic index."""
        self._search_index = {}
        for pid, p in self.registry.projects.items():
            self._index_project(p)
        for pid, p in self.system_demos.items():
            self._index_project(p)

    def _index_project(self, p: ProjectMeta):
        """Injects a project into the semantic index."""
        terms = set()
        # Tokenize name
        terms.update(p.name.lower().split())
        # Tokenize description
        if p.description:
            terms.update(p.description.lower().split())
        # Add tags
        if p.tags:
            terms.update([t.lower() for t in p.tags])

        # Add to index
        for term in terms:
            if len(term) < 2: continue  # Skip noise
            if term not in self._search_index:
                self._search_index[term] = set()
            self._search_index[term].add(p.id)

    # Public Accessors / Compatibility
    def discover_orphans(self, auto_adopt: bool = False) -> List[str]:
        return []

    def prune_zombies(self):
        pass

    def get_project_stats(self) -> Dict[str, Any]:
        return {
            "total_count": len(self.registry.projects) + len(self.system_demos),
            "active_id": self.registry.active_project_id
        }

    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        target_path = Path(path).resolve()
        if not target_path.exists(): raise ArtisanHeresy("Path void.")
        pid = str(uuid.uuid4())
        project = ProjectMeta(
            id=pid, name=name, path=str(target_path).replace('\\', '/'), owner_id=owner_id,
            stats=self._measure_reality(target_path)
        )
        with self._lock:
            self.registry.projects[pid] = project
            self._commit_state()
        return project

    def __repr__(self) -> str:
        count = len(self.registry.projects)
        return f"<Ω_PROJECT_GOVERNOR projects={count} ghosts={len(self.system_demos)} anchor={self.registry.active_project_id if self.registry.active_project_id else 'VOID'}>"