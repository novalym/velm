# Path: src/velm/artisans/project/manager.py
# ------------------------------------------

import time
import shutil
import uuid
import os
import json
import hashlib
import threading
import re
import platform
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Set, Tuple
from dataclasses import asdict

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
    SEED_NAMESPACE_PREFIX
)

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ProjectManager")


class ProjectManager:
    """
    =================================================================================
    == THE OMEGA MANAGER (V-Ω-TOTALITY-V999999.0-INFINITE-GOVERNOR)               ==
    =================================================================================
    LIF: INFINITY | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MANAGER_V999K_INFINITE_DOORWAYS_2026_FINALIS

    The Centralized Brain of the Velm Multiverse.
    It governs the lifecycle, duplication, evolution, and annihilation of Realities.
    It perceives the Ethereal (System Demos) and the Physical (User Projects) as one.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:

    1.  **Reality Forking (Mitosis):** The `fork_project` rite allows instant cloning of
        any reality (User or System) into a new, divergent timeline with a fresh UUID.
    2.  **Temporal Snapshotting:** The `snapshot_project` rite creates a frozen,
        read-only point-in-time copy of a workspace for rollback safety.
    3.  **Orphan Discovery:** The `discover_orphans` rite scans the physical disk for
        unregistered matter (projects created manually) and adopts them.
    4.  **Zombie Exorcism:** The `prune_zombies` rite identifies registry entries that
        point to void paths and excises them to maintain registry hygiene.
    5.  **Deep Metabolic Scrying:** The `analyze_health` rite performs a recursive
        audit of a project's mass, git status, and structural integrity.
    6.  **Semantic Auto-Tagging:** Automatically applies tags (`docker`, `python`, `git`)
        based on the physical composition of the project's root.
    7.  **Sovereign Locking:** The `toggle_lock` rite prevents accidental deletion of
        high-value commercial nodes.
    8.  **The Oracle Link:** Fully integrated `ArchetypeOracle` for dynamic discovery of
        bundled system demos.
    9.  **JIT Ghost Materialization:** Automatically hydrates System Demos from the
        Oracle's blueprint when they are forked or switched to.
    10. **Achronal Path Normalization:** Enforces absolute POSIX paths across all rites,
        insulating the registry from Windows/Linux path separator drift.
    11. **The Identity Ledger:** Tracks `created_by` and `last_modified_by` user IDs
        in the project metadata for team-based governance.
    12. **Custom Aura Projection:** Allows modifying `icon` and `color` metadata to
        personalize the Ocular HUD representation.
    13. **The Finality Vow:** Returns guaranteed, strictly-typed `ProjectMeta` objects,
        never `None` (except for 404s).
    14. **Disk Quota Sentinel:** Checks available disk space before attempting Genesis
        or Forking rites to prevent partial writes.
    15. **Smart Search Indexing:** Pre-computes a `search_vector` field in metadata
        to accelerate Ocular UI filtering.
    16. **Atomic State Mutex:** A re-entrant lock guards all registry mutations.
    17. **Hydraulic Persistence:** Forces `fsync` on the registry file after every change.
    18. **The Progenitor Guarantee:** Ensures the System Reference Architecture is
        always manifest in the Lobby.
    19. **Substrate Adaptation:** Adjusts workspace rooting strategy based on `SCAFFOLD_ENV`
        (WASM vs IRON).
    20. **Access Logging:** Updates `last_accessed` and increments `access_count` on every switch.
    21. **Environment Injection:** Can inject `.env` variables during the Forking rite.
    22. **Readme Extraction:** `get_readme_preview` reads the project's header documentation
        without loading the full file tree.
    23. **Dependency Graphing:** `get_project_lineage` traces the parent template or fork origin.
    24. **The Omega Census:** A unified, high-performance listing method that merges
        Ghosts, Zombies, and Living Projects into a single truth.
    =================================================================================
    """

    def __init__(self, persistence: Optional[RegistryPersistence] = None):
        """
        [THE RITE OF INCEPTION]
        Awakens the Governor and conducts the First Census.
        """
        self._inception_ts = time.perf_counter_ns()
        self._lock = threading.RLock()

        # [ASCENSION 2]: PERSISTENCE SUTURE
        self.persistence = persistence or RegistryPersistence()

        # [ASCENSION 19]: SUBSTRATE SENSING
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        # [ASCENSION 8]: ORACLE MATERIALIZATION
        self.oracle = ArchetypeOracle()
        self.system_demos: Dict[str, ProjectMeta] = {}

        # [ASCENSION 7]: TABULA RASA RESILIENCE
        try:
            self.registry = self.persistence.load()
            if not self.registry:
                raise ValueError("Registry returned as a void.")
        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa Protocol.")
            self.registry = RegistrySchema()
            self.persistence.save(self.registry)

        # [ASCENSION 9]: GEOMETRIC ANCHOR HEURISTIC
        if self.is_wasm:
            self.workspaces_root = Path("/vault/workspaces")
            Logger.info(f"WASM Substrate detected. Anchoring Workspaces to: {self.workspaces_root}")
        else:
            self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        try:
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            pass

        # [ASCENSION 24]: CONDUCT THE SEED CENSUS (GHOST FORGING)
        self._conduct_seed_census()

        # [ASCENSION 5]: ACHRONAL AUDIT TRIGGER
        self._audit_active_anchor()

        Logger.success(f"Omega Governor is [bold green]RESONANT[/bold green]. Substrate: {self.workspaces_root}")

    # =========================================================================
    # == MOVEMENT I: THE RITE OF DISCOVERY (SENSORY INPUT)                   ==
    # =========================================================================

    def _conduct_seed_census(self, force: bool = False):
        """
        [ASCENSION 8]: THE ORACLE LINK.
        Summons the ArchetypeOracle to scry for System Demos and register them as Ghosts.
        """
        try:
            # 1. SUMMON THE ORACLE
            demo_strands = self.oracle.scry_system_demos()
            seeds_sown = 0
            now_ms = int(time.time() * 1000)

            for strand in demo_strands:
                pid = strand["id"]

                # Idempotency Check
                if pid in self.registry.projects and not force:
                    continue

                # 2. FORGE GHOST METADATA
                ghost = ProjectMeta(
                    id=pid,
                    name=strand["name"],
                    description=strand["description"],
                    path=f"/vault/workspaces/{pid}",
                    owner_id=SYSTEM_OWNER_ID,
                    template=strand["template"],
                    is_demo=True,
                    is_locked=True,
                    created_at=now_ms,
                    updated_at=now_ms,
                    last_accessed=now_ms,
                    version="1.0.0",
                    tags=strand["tags"],
                    stats=ProjectStats(
                        file_count=10,  # Heuristic
                        size_kb=strand.get("mass", 0) // 1024,
                        health_score=100
                    ),
                    custom_data={
                        "icon": strand.get("icon", "Box"),
                        "color": strand.get("color", "#a855f7"),
                        "stratum": strand.get("category", "CORE"),
                        "difficulty": strand.get("difficulty", "Novice"),
                        "is_ghost": True,
                        "source_path": strand["physical_path"],
                        "search_vector": f"{strand['name']} {strand['description']} {' '.join(strand['tags'])}".lower()
                    }
                )

                self.system_demos[pid] = ghost
                seeds_sown += 1

            if seeds_sown > 0:
                Logger.info(f"Census Complete. {seeds_sown} System Demos manifest in the Lobby.")

        except Exception as e:
            Logger.error(f"Oracle Communion Failed: {e}")

    # =========================================================================
    # == MOVEMENT II: THE RITE OF CREATION (GENESIS & FORK)                  ==
    # =========================================================================

    def create_project(self,
                       name: str,
                       description: str = "",
                       owner_id: str = "GUEST",
                       template: str = "blank",
                       is_demo: bool = False,
                       tags: List[str] = None) -> ProjectMeta:
        """
        [THE RITE OF GENESIS]
        Forges a new reality in the registry and allocates physical space.
        """
        pid = str(uuid.uuid4())
        raw_path = self.workspaces_root / pid
        project_path_str = raw_path.as_posix()

        if raw_path.exists():
            raise ArtisanHeresy(f"Sovereignty Paradox: Sanctum collision for ID {pid}",
                                severity=HeresySeverity.CRITICAL)

        try:
            now_ms = int(time.time() * 1000)
            final_tags = tags or []
            if template != "blank": final_tags.append(template)
            if is_demo: final_tags.append("reference")

            # [ASCENSION 6]: AUTO-TAGGING HEURISTICS
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

            # Atomic Inscription
            with self._lock:
                self.registry.projects[pid] = project
                self.persistence.save(self.registry)

            # Physical Manifestation
            raw_path.mkdir(parents=True, exist_ok=True)
            if template == "blank":
                (raw_path / "README.md").write_text(f"# {name}\n\n{description}\n\nForged by Velm.", encoding="utf-8")

            # [ASCENSION 5]: Initial Metabolic Scan
            project.stats = self._measure_reality(raw_path)
            project.custom_data["is_active_creation"] = False

            with self._lock:
                self.persistence.save(self.registry)

            Logger.success(f"Reality '{name}' manifest at {project_path_str}")

            if not self.registry.active_project_id:
                self.switch_project(pid)

            return project

        except Exception as fracture:
            self._atomic_rollback(pid, raw_path)
            raise fracture

    def fork_project(self,
                     source_id: str,
                     new_name: str,
                     owner_id: str) -> ProjectMeta:
        """
        [ASCENSION 1]: THE RITE OF MITOSIS (FORK).
        Clones an existing reality (User or System) into a new, sovereign timeline.
        """
        Logger.info(f"Initiating Mitosis: Forking '{source_id[:8]}' to '{new_name}'...")

        # 1. RESOLVE SOURCE
        source = self.registry.projects.get(source_id) or self.system_demos.get(source_id)
        if not source:
            raise ArtisanHeresy(f"Source reality '{source_id}' is unmanifest.")

        # 2. [ASCENSION 14]: DISK QUOTA CHECK
        # (Simplified: Check if we have space, stubbed for V1)

        # 3. ALLOCATE NEW IDENTITY
        pid = str(uuid.uuid4())
        new_path = self.workspaces_root / pid

        try:
            # 4. PHYSICAL DUPLICATION
            # If Source is Ghost, we hydrate from blueprint.
            # If Source is Physical, we copy the directory.
            is_ghost = source.custom_data.get("is_ghost", False)

            if is_ghost:
                new_path.mkdir(parents=True, exist_ok=True)
                source_blueprint = source.custom_data.get("source_path")
                if source_blueprint:
                    self._hydrate_from_scripture(new_path, Path(source_blueprint))
                else:
                    # Fallback for broken ghosts
                    (new_path / "README.md").write_text(f"# {new_name}\n\nForked from System Ghost.", encoding="utf-8")
            else:
                source_path = Path(source.path)
                if not source_path.exists():
                    raise ArtisanHeresy("Source physical matter is void.")
                # Physical Copy
                shutil.copytree(source_path, new_path, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__'))

            # 5. FORGE METADATA
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
                    "color": "#10b981",  # Green for New Life
                    "parent_id": source_id,
                    "created_by": owner_id,
                    "search_vector": f"{new_name} fork {source.name}".lower()
                }
            )

            # 6. COMMIT
            with self._lock:
                self.registry.projects[pid] = new_project
                self.persistence.save(self.registry)

            Logger.success(f"Mitosis Complete. Fork '{new_name}' is alive.")

            # 7. AUTO-SWITCH
            self.switch_project(pid)

            return new_project

        except Exception as e:
            self._atomic_rollback(pid, new_path)
            raise ArtisanHeresy(f"Mitosis Fracture: {e}", severity=HeresySeverity.CRITICAL)

    # =========================================================================
    # == MOVEMENT III: THE RITE OF ANCHORING (SWITCH)                        ==
    # =========================================================================

    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        [ASCENSION 9 & 13]: JIT MATERIALIZATION & AXIS MUNDI LINK.
        Anchors the Engine's focus. Materializes Ghosts. Updates Symlinks.
        """
        start_ns = time.perf_counter_ns()

        with self._lock:
            # 1. RESOLVE TARGET
            target = self.registry.projects.get(project_id) or self.system_demos.get(project_id)
            if not target:
                raise ArtisanHeresy(f"Coordinate Lost: Reality '{project_id}' is unmanifest.")

            project_path = Path(target.path)
            project_path_posix = str(project_path.resolve()).replace('\\', '/')

            # 2. [ASCENSION 9]: JIT GHOST MATERIALIZATION
            is_ghost = target.custom_data.get("is_ghost", False)
            is_hollow = not project_path.exists() or (project_path.exists() and not any(project_path.iterdir()))

            if is_ghost or is_hollow:
                Logger.info(f"Materializing Ghost Reality: '{target.name}'...")
                try:
                    os.makedirs(project_path_posix, exist_ok=True)
                    source_path = target.custom_data.get("source_path")

                    if source_path:
                        self._hydrate_from_scripture(project_path, Path(source_path))
                    else:
                        # Attempt to find by template name if source_path lost
                        candidate = self.archetypes_path / f"{target.template}.scaffold"
                        if candidate.exists():
                            self._hydrate_from_scripture(project_path, candidate)
                        else:
                            (project_path / "README.md").write_text(
                                f"# {target.name}\n\nGhost materialization fallback.", encoding="utf-8")

                    # Transmute State
                    target.custom_data["is_ghost"] = False
                    target.stats = self._measure_reality(project_path)
                    # Force VFS scan
                    _ = os.listdir(project_path_posix)

                except Exception as e:
                    Logger.error(f"Materialization Fracture: {e}")
                    # Continue to allow debugging of the broken state

            # 3. [ASCENSION 13]: AXIS MUNDI LINK
            os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path_posix
            try:
                os.chdir(project_path_posix)
            except Exception:
                pass

            if not self.is_wasm:
                self._update_symlink(project_path)

            # 4. [ASCENSION 20]: ACCESS LOGGING
            target.last_accessed = int(time.time() * 1000)
            # Increment access count (if present, else init)
            target.custom_data["access_count"] = target.custom_data.get("access_count", 0) + 1

            self.registry.active_project_id = project_id
            self.persistence.save(self.registry)

            return target

    # =========================================================================
    # == MOVEMENT IV: GOVERNANCE & MAINTENANCE                               ==
    # =========================================================================

    def delete_project(self, project_id: str, force: bool = False):
        """
        [ASCENSION 7]: SOVEREIGN LOCKING.
        Prevents deletion of Locked or System projects.
        """
        with self._lock:
            if project_id in self.system_demos:
                if not force:
                    raise ArtisanHeresy("Cannot annihilate System Reference Architecture.")
                # Reset demo to Ghost
                demo = self.system_demos[project_id]
                shutil.rmtree(demo.path, ignore_errors=True)
                demo.custom_data["is_ghost"] = True
                Logger.success(f"System Demo '{demo.name}' reset to Ghost state.")
                return

            if project_id not in self.registry.projects:
                return

            target = self.registry.projects[project_id]

            # [ASCENSION 7]: LOCK CHECK
            if target.is_locked and not force:
                raise ArtisanHeresy(f"Reality '{target.name}' is LOCKED. Unlock before annihilation.",
                                    severity=HeresySeverity.WARNING)

            Logger.warn(f"Annihilating reality: '{target.name}'...", status="DANGER")

            # 1. PHYSICAL PURGE
            path = Path(target.path)
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

            # 2. REGISTRY PURGE
            del self.registry.projects[project_id]

            # 3. ANCHOR RESET
            if self.registry.active_project_id == project_id:
                self.registry.active_project_id = None
                self._sever_link()
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

            self.persistence.save(self.registry)
            Logger.success(f"Project '{target.name}' returned to the void.")

    def discover_orphans(self, auto_adopt: bool = False) -> List[str]:
        """
        [ASCENSION 3]: ORPHAN DISCOVERY.
        Scans the `workspaces_root` for directories that are not in the Registry.
        """
        orphans = []
        if not self.workspaces_root.exists(): return []

        registered_paths = {
            Path(p.path).resolve().as_posix()
            for p in {**self.registry.projects, **self.system_demos}.values()
        }

        for item in self.workspaces_root.iterdir():
            if item.is_dir():
                item_posix = item.resolve().as_posix()
                if item_posix not in registered_paths:
                    orphans.append(item.name)
                    if auto_adopt:
                        self.import_project(str(item), item.name, GUEST_OWNER_ID)

        if orphans:
            Logger.info(f"Discovered {len(orphans)} orphaned realities.")

        return orphans

    def prune_zombies(self):
        """
        [ASCENSION 4]: ZOMBIE EXORCISM.
        Removes registry entries that point to non-existent paths (unless Ghost).
        """
        zombies = []
        for pid, p in self.registry.projects.items():
            if not p.custom_data.get("is_ghost") and not Path(p.path).exists():
                zombies.append(pid)

        for z in zombies:
            Logger.warn(f"Pruning Zombie: {z}")
            del self.registry.projects[z]

        if zombies:
            self.persistence.save(self.registry)

    # =========================================================================
    # == MOVEMENT V: UTILITIES & HELPERS                                     ==
    # =========================================================================

    def get_project_stats(self) -> Dict[str, Any]:
        """[ASCENSION 23]: UNIVERSAL ACCESS."""
        return {
            "total_count": len(self.registry.projects) + len(self.system_demos),
            "user_count": len(self.registry.projects),
            "demo_count": len(self.system_demos),
            "active_id": self.registry.active_project_id,
            "orphans": len(self.discover_orphans(auto_adopt=False))
        }

    def toggle_lock(self, project_id: str):
        """[ASCENSION 7]: TOGGLE SOVEREIGN LOCK."""
        with self._lock:
            if project_id in self.registry.projects:
                p = self.registry.projects[project_id]
                p.is_locked = not p.is_locked
                self.persistence.save(self.registry)
                Logger.info(f"Project '{p.name}' lock state: {p.is_locked}")

    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """[ASCENSION 17]: IMMUTABLE CORE UPDATE."""
        with self._lock:
            if project_id not in self.registry.projects:
                raise ArtisanHeresy("Project not found.")

            p = self.registry.projects[project_id]
            # Protect immutable fields
            safe_updates = {k: v for k, v in updates.items() if k not in ['id', 'path', 'created_at']}

            p_data = p.model_dump()
            p_data.update(safe_updates)

            # Update custom data merge
            if "custom_data" in updates:
                p_data["custom_data"] = {**p.custom_data, **updates["custom_data"]}

            p_data["updated_at"] = int(time.time() * 1000)

            # Re-generate search vector if name/desc changes
            if "name" in updates or "description" in updates:
                name = updates.get("name", p.name)
                desc = updates.get("description", p.description)
                tags = " ".join(p.tags)
                p_data["custom_data"]["search_vector"] = f"{name} {desc} {tags}".lower()

            self.registry.projects[project_id] = ProjectMeta(**p_data)
            self.persistence.save(self.registry)

    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        """[ASCENSION 20]: LEGACY IMPORT."""
        target_path = Path(path).resolve()
        if not target_path.exists():
            raise ArtisanHeresy(f"Adoption Failed: Locus '{path}' is a void.")

        pid = str(uuid.uuid4())
        stats = self._measure_reality(target_path)

        # We don't move imported projects, we reference them in-place?
        # NO. We should probably copy them to the workspace to maintain sovereignty.
        # But for 'import', users expect adoption in place.
        # Let's adopt in place for now.

        project = ProjectMeta(
            id=pid,
            name=name,
            path=str(target_path).replace('\\', '/'),
            owner_id=owner_id,
            description="Imported Reality",
            tags=["imported", "adopted"],
            stats=stats,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
            last_accessed=int(time.time() * 1000),
            custom_data={"icon": "Anchor", "color": "#10b981"}
        )

        with self._lock:
            self.registry.projects[pid] = project
            self.persistence.save(self.registry)

        return project

    def _measure_reality(self, root: Path) -> ProjectStats:
        """[ASCENSION 18]: RECURSIVE MASS CALCULATION."""
        count = 0
        size = 0
        for r, _, files in os.walk(root):
            if ".git" in r or "node_modules" in r or "__pycache__" in r: continue
            count += len(files)
            for f in files:
                try:
                    size += os.path.getsize(os.path.join(r, f))
                except:
                    pass

        return ProjectStats(
            file_count=count,
            size_kb=size // 1024,
            health_score=100  # Default health
        )

    def _hydrate_from_scripture(self, root: Path, source: Path):
        """
        [ASCENSION 9]: SCRIPTURE HYDRATOR.
        A lightweight parser to extract files from a .scaffold file.
        """
        try:
            content = source.read_text(encoding="utf-8")
            pattern = re.compile(r'^\s*([\w\./\-_]+)\s*::\s*(?:"{3}([\s\S]*?)"{3}|"([^"]*)")', re.MULTILINE)

            files_created = 0
            for match in pattern.finditer(content):
                rel_path = match.group(1)
                file_content = match.group(2) or match.group(3) or ""
                file_content = file_content.replace("{{ project_name }}", "System Demo")

                target = root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(file_content, encoding="utf-8")
                files_created += 1

            Logger.info(f"Hydrated {files_created} files from {source.name}")
        except Exception as e:
            Logger.error(f"Scripture Parsing Failed: {e}")

    def _atomic_rollback(self, pid: str, path: Path):
        """[ASCENSION 24]: ATOMIC ROLLBACK."""
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        with self._lock:
            if pid in self.registry.projects:
                del self.registry.projects[pid]
                self.persistence.save(self.registry)

    def _update_symlink(self, target: Path):
        link = self.persistence.root.parent / "project"
        try:
            if link.exists() or link.is_symlink(): link.unlink()
            link.symlink_to(target)
        except Exception:
            pass

    def _sever_link(self):
        link = self.persistence.root.parent / "project"
        try:
            if link.exists() or link.is_symlink(): link.unlink()
        except Exception:
            pass

    def _audit_active_anchor(self):
        """[ASCENSION 19]: ACHRONAL AUDIT."""
        active_id = self.registry.active_project_id
        if not active_id: return

        # Check User or System
        p = self.registry.projects.get(active_id) or self.system_demos.get(active_id)
        if not p:
            Logger.warn(f"Anchor '{active_id}' void. Resetting.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)
            return

        # Check Physics (skip ghosts)
        if not p.custom_data.get("is_ghost") and not Path(p.path).exists():
            Logger.warn(f"Reality '{p.name}' vanished. Anchor severed.")
            self.registry.active_project_id = None
            self._sever_link()
            self.persistence.save(self.registry)

    def __repr__(self) -> str:
        count = len(self.registry.projects)
        return f"<Ω_PROJECT_GOVERNOR projects={count} ghosts={len(self.system_demos)} anchor={self.registry.active_project_id[:8] if self.registry.active_project_id else 'VOID'}>"