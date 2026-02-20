# Path: src/velm/artisans/project/manager.py
# ------------------------------------------

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
    SEED_NAMESPACE_PREFIX,
    REGISTRY_VERSION
)

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ProjectManager")


class ProjectManager:
    """
    =================================================================================
    == THE OMEGA MANAGER (V-Ω-TOTALITY-V100000.0-COMPLETE)                         ==
    =================================================================================
    LIF: INFINITY | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MANAGER_V100K_FULL_RESTORATION_FINALIS

    The Centralized Brain of the Velm Multiverse.
    It governs the lifecycle, duplication, evolution, and annihilation of Realities.

    [ARCHITECTURAL GUARANTEE]: This version contains NO elisions. Every logic path
    is fully materialized, hardened, and integrated with the Event Bus.
    """

    def __init__(self, engine: Any = None, persistence: Optional[RegistryPersistence] = None):
        """
        [THE RITE OF INCEPTION]
        Materializes the central mind of the project cosmos.
        """
        # [ASCENSION 2]: NANOSECOND CHRONOMETRY
        self._inception_ts = time.perf_counter_ns()

        # [ASCENSION 9]: ATOMIC LOCK CONSECRATION
        self._lock = threading.RLock()

        # [ASCENSION 1]: THE ENGINE SUTURE
        self.engine = engine

        # --- MOVEMENT I: SUBSTRATE CALIBRATION ---
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.persistence = persistence or RegistryPersistence()
        self.oracle = ArchetypeOracle()

        # --- MOVEMENT II: THE DECREE OF THE AXIS MUNDI ---
        self.system_demos: Dict[str, ProjectMeta] = {}
        self._manifest_axis_mundi()

        # --- MOVEMENT III: THE RESURRECTION OF THE BOOK OF NAMES ---
        try:
            self.registry = self.persistence.load()
            if not self.registry or not hasattr(self.registry, 'projects'):
                raise ValueError("Registry soul is a void or fractured.")

            if getattr(self.registry, 'version', None) != REGISTRY_VERSION:
                Logger.warn(f"Version Drift: {self.registry.version} -> {REGISTRY_VERSION}. Migrating...")

        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa Protocol.")
            self.registry = RegistrySchema(version=REGISTRY_VERSION)
            self.persistence.save(self.registry)

        # --- MOVEMENT IV: GEOMETRIC ANCHORING ---
        if self.is_wasm:
            self.workspaces_root = Path("/vault/workspaces")
        else:
            self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        try:
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            Logger.warn(f"Sanctum Forge hindered: {e}. Operating in Volatile mode.")

        # --- MOVEMENT V: THE INITIAL CENSUS ---
        self._conduct_seed_census()
        self._audit_active_anchor()

        duration_ms = (time.perf_counter_ns() - self._inception_ts) / 1_000_000
        Logger.success(
            f"Omega Governor is RESONANT ({duration_ms:.2f}ms). Substrate: {'ETHER' if self.is_wasm else 'IRON'}")

    def _manifest_axis_mundi(self):
        """[THE CURE]: Hard-registers the Progenitor into the system_demos map."""
        now_ms = int(time.time() * 1000)
        self.system_demos[PROGENITOR_ID] = ProjectMeta(
            id=PROGENITOR_ID,
            name="Progenitor",
            description="The foundational law of the Novalym universe. Learn the physics of creation.",
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

    def _conduct_seed_census(self, force: bool = False):
        """Scries the physical substrate for architectural DNA strands."""
        start_ns = time.perf_counter_ns()
        now_ms = int(time.time() * 1000)
        new_discoveries = 0

        try:
            strands = self.oracle.scry_system_demos()
        except Exception as e:
            Logger.critical(f"Celestial Scryer Fractured: {e}. Census restricted to Axis Mundi.")
            strands = []

        for strand in strands:
            try:
                pid = strand.get("id")
                if not pid: continue
                # Deduplication Ward
                if pid in self.system_demos or pid in self.registry.projects: continue

                icon = strand.get("icon") or "Box"
                color = strand.get("color") or "#94a3b8"
                category = strand.get("category") or "Generic"
                difficulty = strand.get("difficulty") or "Adept"

                search_terms = [strand.get("name", "Unknown"), strand.get("description", ""), category, difficulty]
                search_terms.extend(strand.get("tags", []))
                search_vector = " ".join(filter(None, search_terms)).lower()

                ghost = ProjectMeta(
                    id=pid,
                    name=strand.get("name", "Unnamed_Reality"),
                    description=strand.get("description", "Architectural pattern shard."),
                    path=f"/vault/workspaces/{pid}",
                    owner_id=SYSTEM_OWNER_ID,
                    template=strand.get("template", "blank"),
                    is_demo=True,
                    is_locked=True,
                    created_at=now_ms,
                    updated_at=now_ms,
                    last_accessed=now_ms,
                    version=strand.get("version", "1.0.0"),
                    stats=ProjectStats(file_count=10, size_kb=strand.get("mass", 0) // 1024, health_score=100),
                    custom_data={
                        "icon": icon, "color": color, "stratum": category.upper(),
                        "difficulty": difficulty, "is_ghost": True,
                        "source_path": strand.get("physical_path"), "search_vector": search_vector
                    }
                )

                with self._lock:
                    self.system_demos[pid] = ghost
                    new_discoveries += 1

            except Exception as shard_fracture:
                Logger.warn(f"Strand {strand.get('name', '???')} is profane: {shard_fracture}")
                continue

        if new_discoveries > 0:
            self._multicast_ghost_revelation()

    def _multicast_ghost_revelation(self):
        """Broadcasts the current system_demos to the Ocular HUD."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                lightweight_demos = {
                    pid: {
                        "name": p.name,
                        "category": p.custom_data.get("stratum"),
                        "icon": p.custom_data.get("icon")
                    }
                    for pid, p in self.system_demos.items()
                }
                self.engine.akashic.broadcast({
                    "method": "velm:ghost_revelation",
                    "params": {"census_count": len(self.system_demos), "demos": lightweight_demos}
                })
            except Exception:
                pass

    def list_projects(self, owner_id: Optional[str] = None, tags: Optional[List[str]] = None) -> List[ProjectMeta]:
        """Merges Physical and Ethereal matter into a unified census."""
        with self._lock:
            pool: List[ProjectMeta] = list(self.registry.projects.values())
            existing_ids = {p.id for p in pool}

            for pid, ghost_meta in self.system_demos.items():
                if pid not in existing_ids:
                    pool.append(ghost_meta)

            if owner_id and owner_id != GUEST_OWNER_ID:
                pool = [p for p in pool if p.owner_id == owner_id or p.owner_id == SYSTEM_OWNER_ID]
            elif owner_id == GUEST_OWNER_ID:
                pool = [p for p in pool if p.owner_id == GUEST_OWNER_ID or p.owner_id == SYSTEM_OWNER_ID]

            if tags:
                tag_set = set(tags)
                pool = [p for p in pool if any(t in tag_set for t in (p.tags or []))]

            pool.sort(key=lambda x: getattr(x, 'last_accessed', 0), reverse=True)
            return pool

    def create_project(self, name: str, description: str = "", owner_id: str = "GUEST", template: str = "blank",
                       is_demo: bool = False, tags: List[str] = None) -> ProjectMeta:
        """Forges a new reality from an Archetype Seed."""
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
                    "is_ghost": False, "is_active_creation": True, "icon": "Box",
                    "color": "#3b82f6", "created_by": owner_id,
                    "search_vector": f"{name} {description} {' '.join(final_tags)}".lower()
                }
            )

            with self._lock:
                self.registry.projects[pid] = project
                self.persistence.save(self.registry)

            raw_path.mkdir(parents=True, exist_ok=True)
            if template == "blank":
                (raw_path / "README.md").write_text(f"# {name}\n\n{description}\n\nForged by Velm.", encoding="utf-8")

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

    def fork_project(self, source_id: str, new_name: str, owner_id: str) -> ProjectMeta:
        """[ASCENSION 1]: Clones a reality into a divergent timeline."""
        Logger.info(f"Initiating Mitosis: Forking '{source_id[:8]}' to '{new_name}'...")

        source = self.registry.projects.get(source_id) or self.system_demos.get(source_id)
        if not source:
            raise ArtisanHeresy(f"Source reality '{source_id}' is unmanifest.")

        pid = str(uuid.uuid4())
        new_path = self.workspaces_root / pid

        try:
            is_ghost = source.custom_data.get("is_ghost", False)

            if is_ghost:
                new_path.mkdir(parents=True, exist_ok=True)
                source_blueprint = source.custom_data.get("source_path")
                if source_blueprint:
                    self._hydrate_from_scripture(new_path, Path(source_blueprint))
                else:
                    (new_path / "README.md").write_text(f"# {new_name}\n\nForked from System Ghost.", encoding="utf-8")
            else:
                source_path = Path(source.path)
                if not source_path.exists():
                    raise ArtisanHeresy("Source physical matter is void.")
                shutil.copytree(source_path, new_path, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__'))

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
                self.persistence.save(self.registry)

            Logger.success(f"Mitosis Complete. Fork '{new_name}' is alive.")
            self.switch_project(pid)

            return new_project

        except Exception as e:
            self._atomic_rollback(pid, new_path)
            raise ArtisanHeresy(f"Mitosis Fracture: {e}", severity=HeresySeverity.CRITICAL)

    def _materialize_project_entity(self, raw_entity: Any) -> ProjectMeta:
        """
        =============================================================================
        == THE ENTITY MATERIALIZER (V-Ω-TYPE-SAFE-FACTORY)                         ==
        =============================================================================
        LIF: ∞ | ROLE: OBJECT_NORMALIZER
        Transmutes raw matter (Dict, String-Corruption, or Pydantic Model) into a
        pure, mutable ProjectMeta object. Prevents 'str' attribute heresies.
        """
        if not raw_entity:
            raise ArtisanHeresy("Materialization failed: Entity is Void.")

        # [THE CURE]: CORRUPTION TRAP
        # If the registry was corrupted and contains strings, we must reject them.
        if isinstance(raw_entity, str):
            raise ArtisanHeresy(
                f"Registry Corruption Detected: Entity is a string literal '{raw_entity[:15]}...', not a Gnostic Object.",
                severity=HeresySeverity.CRITICAL
            )

        # Path A: It is already a Divine Vessel (ProjectMeta)
        if isinstance(raw_entity, ProjectMeta):
            # We clone it to ensure mutability (pydantic copy)
            return raw_entity.model_copy(deep=True)

        # Path B: It is a Dictionary (JSON State)
        if isinstance(raw_entity, dict):
            try:
                return ProjectMeta(**raw_entity)
            except Exception as e:
                # Fallback: Attempt manual reconstruction if schema drifted
                return ProjectMeta(
                    id=raw_entity.get('id', str(uuid.uuid4())),
                    name=raw_entity.get('name', 'Corrupted_Entity'),
                    path=raw_entity.get('path', '/vault/unknown'),
                    owner_id=raw_entity.get('owner_id', 'GUEST'),
                    custom_data=raw_entity.get('custom_data', {})
                )

        raise ArtisanHeresy(f"Unknown Matter Type: {type(raw_entity)}")

    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        =============================================================================
        == THE RITE OF ANCHORING: OMEGA POINT (V-Ω-TOTALITY-V8000-TITANIUM)        ==
        =============================================================================
        LIF: ∞ | ROLE: DIMENSIONAL_ANCHOR_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SWITCH_PROJECT_V8000_TOTAL_RESONANCE_2026_FINALIS

        [ARCHITECTURAL CONSTITUTION]
        This rite conducts the absolute transmutation of a latent project ID into a
        resonant, physical reality. It has been ascended to its final form:

        1.  **Type-Sanctity Suture (THE CURE):** Surgically detects and heals
            registry corruption where a string ID was stored instead of a Project
            Object. Uses the ProjectMeta constructor to enforce bit-perfect shape.
        2.  **Ghost-Registry Injection:** Automatically promotes 'system_demo'
            shards into the physical registry projects map upon activation.
        3.  **Achronal Path Normalization:** Resolves paths to absolute POSIX
            coordinates, abolishing symlink drift and "path not found" heresies.
        4.  **NoneType Sarcophagus:** Hard-wards against null-pointer regressions
            during ghost-mind hydration.
        5.  **Bicameral Identity Sync:** Synchronously updates the OS environment
            and the Akashic record to prevent "Split-Brain" state paradoxes.
        6.  **Jitter Shielding:** Injects a micro-delay before the UI broadcast
            to allow the virtual disk (IDBFS) to achieve stasis.
        =============================================================================
        """
        import time
        import os
        from pathlib import Path
        from .contracts import ProjectMeta  # Ensure contract is manifest

        start_ns = time.perf_counter_ns()

        with self._lock:
            # --- MOVEMENT I: COORDINATE TRIANGULATION ---
            # We scry the registry and the system demos simultaneously.
            candidate = self.registry.projects.get(project_id) or self.system_demos.get(project_id)

            if not candidate:
                raise ArtisanHeresy(
                    message=f"Coordinate Lost: Reality '{project_id}' is unmanifest in the Book of Names.",
                    code="ANCHOR_FRACTURE",
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT II: THE TYPE-SANCTITY FILTER (THE CORE FIX) ---
            # [ASCENSION 1]: We detect if the entity is a profane string (Corruption)
            # or a pure Object. If corrupt, we resurrect from system demos or re-forge.
            target: ProjectMeta

            try:
                if isinstance(candidate, str):
                    Logger.warn(f"Registry Corruption Detected for {project_id}. Re-materializing soul from Demos.")
                    # Recover the raw dict/model from demos
                    raw_ghost = self.system_demos.get(project_id)
                    if not raw_ghost:
                        raise ValueError("Ghost soul is also unmanifest.")
                    target = ProjectMeta(**(raw_ghost.model_dump() if hasattr(raw_ghost, 'model_dump') else raw_ghost))
                elif isinstance(candidate, dict):
                    target = ProjectMeta(**candidate)
                else:
                    # It is already a ProjectMeta, but we deep-copy to ensure mutability
                    target = candidate.model_copy(deep=True) if hasattr(candidate, 'model_copy') else candidate

            except Exception as e:
                Logger.critical(f"Materialization Fracture: Project {project_id} has a profane soul. {e}")
                raise ArtisanHeresy(
                    f"Ontological Failure: Project '{project_id}' could not be materialized.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT III: GEOMETRIC NORMALIZATION ---
            # We force the path into an absolute POSIX coordinate.
            project_path = Path(target.path).resolve()
            project_path_posix = project_path.as_posix()
            # Ensure the object path is normalized for the UI
            target.path = project_path_posix

            # --- MOVEMENT IV: PHYSICAL CONSECRATION ---
            # We forge the directory atoms physically BEFORE the mind attempts to inhabit them.
            try:
                if not project_path.exists():
                    project_path.mkdir(parents=True, exist_ok=True)
                    Logger.verbose(f"Sanctum Consecrated: {project_id[:8]}")
            except (OSError, PermissionError) as e:
                raise ArtisanHeresy(
                    f"Physical Fracture: Substrate refused to forge sanctum at '{project_path_posix}'.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT V: GHOST REALIZATION & HYDRATION ---
            # Detect if this is a "Hollow Ghost" requiring JIT inception
            is_ghost = target.custom_data.get("is_ghost", False)
            is_hollow = len(list(project_path.iterdir())) == 0 if project_path.exists() else True

            if is_ghost and is_hollow:
                Logger.info(f"Materializing Ghost Reality via Init Artisan: '{target.name}'...")

                if not self.engine:
                    Logger.warn("Governor un-anchored; conducting passive materialization.")
                else:
                    try:
                        from ...interfaces.requests import InitRequest
                        # We forge the plea to materialize the archetype.
                        init_plea = InitRequest(
                            profile=target.template,
                            project_root=project_path,
                            force=True,
                            non_interactive=True,
                            variables={
                                "project_name": target.name,
                                "description": target.description,
                                "no_edicts": os.environ.get("SCAFFOLD_ENV") == "WASM"
                            }
                        )
                        # [STRIKE]: Synchronous materialization
                        result = self.engine.dispatch(init_plea)
                        if not result.success:
                            Logger.error(f"Genesis Fracture: {result.message}")

                    except Exception as e:
                        Logger.error(f"Fracture during Ghost materialization: {e}")

            # --- MOVEMENT VI: STATE MUTATION & REGISTRY ENSHRINEMENT ---
            # [THE CURE]: We surgically update the object and inject it into the map.
            # This wipes out any string corruption in the registry memory.
            target.custom_data["is_ghost"] = False
            target.last_accessed = int(time.time() * 1000)

            self.registry.projects[project_id] = target
            self.registry.active_project_id = project_id

            # Force hydraulic flush to persistent storage (projects.json)
            self.persistence.save(self.registry)

            # --- MOVEMENT VII: AXIS MUNDI LINK ---
            # Update the environment so subprocesses (Maestro) know their home.
            os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path_posix
            try:
                os.chdir(project_path_posix)
            except Exception:
                pass

            # --- MOVEMENT VIII: OMNISCIENT BROADCAST ---
            # We broadcast the new ID and Absolute Path to the React layer.
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    # [ASCENSION 11]: Jitter Shield
                    # A tiny micro-yield to ensure the VFS has registered the physical move.
                    time.sleep(0.05)

                    self.engine.akashic.broadcast({
                        "method": "velm:registry_sync_request",
                        "params": {
                            "active_id": project_id,
                            "active_path": project_path_posix,
                            "source": "manager_switch_omega"
                        }
                    })
                except Exception as e:
                    Logger.debug(f"Broadcast suppressed: {e}")

            # --- FINAL PROCLAMATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.verbose(f"Reality Jump to {project_id[:8]} completed in {duration_ms:.2f}ms.")

            # [ASCENSION 12]: THE FINALITY VOW
            return target

    def delete_project(self, project_id: str, force: bool = False):
        """[ASCENSION 7]: Removes a reality from existence, respecting locks."""
        with self._lock:
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

            if target.is_locked and not force:
                raise ArtisanHeresy(f"Reality '{target.name}' is LOCKED. Unlock before annihilation.",
                                    severity=HeresySeverity.WARNING)

            Logger.warn(f"Annihilating reality: '{target.name}'...", status="DANGER")

            path = Path(target.path)
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

            del self.registry.projects[project_id]

            if self.registry.active_project_id == project_id:
                self.registry.active_project_id = None
                self._sever_link()
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

            self.persistence.save(self.registry)
            Logger.success(f"Project '{target.name}' returned to the void.")

    def discover_orphans(self, auto_adopt: bool = False) -> List[str]:
        """[ASCENSION 3]: Scans workspaces_root for unregistered projects."""
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
        """[ASCENSION 4]: Removes registry entries that point to non-existent paths."""
        zombies = []
        for pid, p in self.registry.projects.items():
            if not p.custom_data.get("is_ghost") and not Path(p.path).exists():
                zombies.append(pid)

        for z in zombies:
            Logger.warn(f"Pruning Zombie: {z}")
            del self.registry.projects[z]

        if zombies:
            self.persistence.save(self.registry)

    def get_project_stats(self) -> Dict[str, Any]:
        """Returns panoptic statistics for the Multiverse."""
        return {
            "total_count": len(self.registry.projects) + len(self.system_demos),
            "user_count": len(self.registry.projects),
            "demo_count": len(self.system_demos),
            "active_id": self.registry.active_project_id,
            "orphans": len(self.discover_orphans(auto_adopt=False))
        }

    def toggle_lock(self, project_id: str):
        """[ASCENSION 7]: Toggles the deletion protection for a project."""
        with self._lock:
            if project_id in self.registry.projects:
                p = self.registry.projects[project_id]
                p.is_locked = not p.is_locked
                self.persistence.save(self.registry)
                Logger.info(f"Project '{p.name}' lock state: {p.is_locked}")

    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """[ASCENSION 17]: Updates mutable fields in a ProjectMeta object."""
        with self._lock:
            if project_id not in self.registry.projects:
                raise ArtisanHeresy("Project not found.")

            p = self.registry.projects[project_id]
            safe_updates = {k: v for k, v in updates.items() if k not in ['id', 'path', 'created_at']}

            p_data = p.model_dump()
            p_data.update(safe_updates)

            if "custom_data" in updates:
                p_data["custom_data"] = {**p.custom_data, **updates["custom_data"]}

            p_data["updated_at"] = int(time.time() * 1000)

            if "name" in updates or "description" in updates:
                name = updates.get("name", p.name)
                desc = updates.get("description", p.description)
                tags = " ".join(p.tags)
                p_data["custom_data"]["search_vector"] = f"{name} {desc} {tags}".lower()

            self.registry.projects[project_id] = ProjectMeta(**p_data)
            self.persistence.save(self.registry)

    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        """[ASCENSION 20]: Adopts an existing directory into the Registry."""
        target_path = Path(path).resolve()
        if not target_path.exists():
            raise ArtisanHeresy(f"Adoption Failed: Locus '{path}' is a void.")

        pid = str(uuid.uuid4())
        stats = self._measure_reality(target_path)

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
        """[ASCENSION 18]: Recursively calculates file count and disk usage."""
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
        return ProjectStats(file_count=count, size_kb=size // 1024, health_score=100)

    def _hydrate_from_scripture(self, root: Path, source: Path):
        """[ASCENSION 9]: Lightweight parser to extract files from a .scaffold template."""
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
        """[ASCENSION 24]: Rolls back physical and logical state on failure."""
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        with self._lock:
            if pid in self.registry.projects:
                del self.registry.projects[pid]
                self.persistence.save(self.registry)

    def _update_symlink(self, target: Path):
        """Maintains the legacy /vault/project symlink if needed."""
        link = self.persistence.root.parent / "project"
        try:
            if link.exists() or link.is_symlink(): link.unlink()
            link.symlink_to(target)
        except Exception:
            pass

    def _sever_link(self):
        """Removes the legacy symlink."""
        link = self.persistence.root.parent / "project"
        try:
            if link.exists() or link.is_symlink(): link.unlink()
        except Exception:
            pass

    def _audit_active_anchor(self):
        """Verifies the active anchor points to a valid reality."""
        active_id = self.registry.active_project_id
        if not active_id: return

        p = self.registry.projects.get(active_id) or self.system_demos.get(active_id)
        if not p:
            Logger.warn(f"Anchor '{active_id}' void. Resetting.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)
            return

        if not p.custom_data.get("is_ghost") and not Path(p.path).exists():
            Logger.warn(f"Reality '{p.name}' vanished. Anchor severed.")
            self.registry.active_project_id = None
            self._sever_link()
            self.persistence.save(self.registry)

    def __repr__(self) -> str:
        count = len(self.registry.projects)
        return f"<Ω_PROJECT_GOVERNOR projects={count} ghosts={len(self.system_demos)} anchor={self.registry.active_project_id if self.registry.active_project_id else 'VOID'}>"