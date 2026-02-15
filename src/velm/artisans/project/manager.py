# src/velm/artisans/project/manager.py
# ------------------------------------
# LIF: INFINITY | ROLE: MULTIVERSE_OVERSEER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_MANAGER_V9000_SEED_HYDRATED_FINALIS

import time
import shutil
import uuid
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from .contracts import RegistrySchema, ProjectMeta, ProjectStats
from .persistence import RegistryPersistence
from .constants import DEFAULT_WORKSPACE_DIR_NAME, SYSTEM_OWNER_ID, GUEST_OWNER_ID
from .seeds import SEED_VAULT  # [ASCENSION 1]: The DNA Vault

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ProjectManager")


class ProjectManager:
    """
    =============================================================================
    == THE OMEGA MANAGER (V-Ω-LOGIC-CORE-ASCENDED)                             ==
    =============================================================================
    The centralized brain for Multiverse Management.
    Governs the lifecycle of Realities (Projects) and their physical manifestation.
    """

    def __init__(self, persistence: Optional[RegistryPersistence] = None):
        """
        The Rite of Inception.
        Awakens the Persistence Engine and loads the Book of Names.
        """
        self.persistence = persistence or RegistryPersistence()

        # [ASCENSION 5]: Safe-Import Fallback
        # If the registry is corrupt, we do not crash; we heal.
        try:
            self.registry = self.persistence.load()
        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa.")
            self.registry = RegistrySchema()

        # Define the Physical Storage Pool for projects
        self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        # [ASCENSION 9]: Idempotent Directory Forging
        self.workspaces_root.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 2]: Achronal State Repair
        # We perform a lazy audit on boot to ensure active_project_id points to reality.
        self._audit_active_anchor()

    def _audit_active_anchor(self):
        """Ensures the active project physically exists."""
        active_id = self.registry.active_project_id
        if active_id:
            project = self.registry.projects.get(active_id)
            if not project or not Path(project.path).exists():
                Logger.warn(f"Active Anchor '{active_id}' is a ghost. Resetting to Void.")
                self.registry.active_project_id = None
                self.persistence.save(self.registry)

    # =========================================================================
    # == RITE 1: THE CENSUS (LIST)                                           ==
    # =========================================================================
    def list_projects(self, owner_id: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      include_archived: bool = False) -> List[ProjectMeta]:
        """
        The Census Rite. Returns filtered list of realities.
        """
        results = []
        for p in self.registry.projects.values():
            if not include_archived and p.is_archived:
                continue

            # [ASCENSION 6]: Owner-ID Normalization Logic
            # Guests see Guest projects + System Demos.
            # Users see Their projects + Guest projects (if unclaimed) + System Demos.
            if owner_id:
                is_owner = p.owner_id == owner_id
                is_guest = p.owner_id == GUEST_OWNER_ID
                is_system = p.owner_id == SYSTEM_OWNER_ID or p.is_demo

                if not (is_owner or (owner_id != GUEST_OWNER_ID and is_guest) or is_system):
                    continue

            if tags and not any(t in p.tags for t in tags):
                continue

            results.append(p)

        # [ASCENSION 8]: Timestamp Micro-Precision Sort
        return sorted(results, key=lambda x: x.last_accessed, reverse=True)

    # =========================================================================
    # == RITE 2: THE GENESIS STRIKE (CREATE)                                 ==
    # =========================================================================
    def create_project(self,
                       name: str,
                       description: str = "",
                       owner_id: str = "GUEST",
                       template: str = "blank",
                       is_demo: bool = False,
                       tags: List[str] = None) -> ProjectMeta:
        """
        The Rite of Genesis. Allocates space, seeds matter, and registers the soul.
        """
        # [ASCENSION 7]: Template Validation Oracle
        if template not in SEED_VAULT:
            Logger.warn(f"Template '{template}' unknown. Falling back to 'blank'.")
            template = "blank"

        pid = str(uuid.uuid4())
        project_path = self.workspaces_root / pid

        # 1. Physical Allocation
        if project_path.exists():
            raise ArtisanHeresy(f"Sanctum collision for ID {pid}", severity=HeresySeverity.CRITICAL)

        try:
            project_path.mkdir(parents=True, exist_ok=True)

            # 2. [ASCENSION 1]: ATOMIC SEED HYDRATION
            # We breathe life into the void using the Seed Bank.
            self._hydrate_sanctum(project_path, template)

            # 3. [ASCENSION 3]: METABOLIC MASS CALCULATION
            # We measure the weight of the reality we just forged.
            stats = self._measure_reality(project_path)

            # 4. Forge Metadata
            now = int(time.time() * 1000)

            # Auto-tagging based on template
            final_tags = tags or []
            if template != "blank": final_tags.append(template)
            if is_demo: final_tags.append("reference")

            project = ProjectMeta(
                id=pid,
                name=name,
                description=description,
                path=str(project_path),
                owner_id=owner_id,
                template=template,
                is_demo=is_demo,
                tags=final_tags,
                created_at=now,
                updated_at=now,
                last_accessed=now,
                stats=stats
            )

            # 5. Register
            self.registry.projects[pid] = project

            # 6. Auto-Activate if first
            if not self.registry.active_project_id:
                Logger.info(f"First reality forged. Auto-anchoring to {name}.")
                self.switch_project(pid)
            else:
                self.persistence.save(self.registry)

            Logger.success(f"Reality '{name}' ({pid}) forged from template '{template}'.")
            return project

        except Exception as e:
            # Rollback: Annihilate the partial reality
            if project_path.exists():
                shutil.rmtree(project_path)
            raise ArtisanHeresy(f"Genesis Fracture: {e}", severity=HeresySeverity.CRITICAL)

    def _hydrate_sanctum(self, root: Path, template_id: str):
        """
        [ASCENSION 1]: The Seeding Rite.
        Writes the predefined files from the Vault into the physical directory.
        """
        seed_data = SEED_VAULT.get(template_id, SEED_VAULT["blank"])

        for rel_path, content in seed_data.items():
            target = root / rel_path
            # Ensure parent directories exist (e.g. src/core/config.py)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')

    def _measure_reality(self, root: Path) -> ProjectStats:
        """
        [ASCENSION 3]: The Scale.
        Weighs the files and counts the atoms.
        """
        file_count = 0
        size_bytes = 0
        for r, _, files in os.walk(root):
            file_count += len(files)
            for f in files:
                try:
                    size_bytes += os.path.getsize(os.path.join(r, f))
                except OSError:
                    pass

        return ProjectStats(
            file_count=file_count,
            size_kb=size_bytes // 1024,
            last_integrity_check=time.time(),
            health_score=100
        )

    # =========================================================================
    # == RITE 3: THE DIMENSIONAL SHIFT (SWITCH)                              ==
    # =========================================================================
    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        The Rite of Anchoring. Shifts the active reality.
        """
        if project_id not in self.registry.projects:
            raise ArtisanHeresy("Project ID not found in registry.")

        target = self.registry.projects[project_id]

        # Update Access Time
        target.last_accessed = int(time.time() * 1000)
        self.registry.active_project_id = project_id

        # [ASCENSION 4]: SYMBOLIC LINK SOVEREIGNTY
        # We symlink /vault/project (or ~/.scaffold/current) to the project dir
        # This tells the Engine where "Current Reality" is.
        self._link_active_reality(Path(target.path))

        self.persistence.save(self.registry)
        Logger.info(f"Active Reality switched to: {target.name}")
        return target

    # =========================================================================
    # == RITE 4: THE ANNIHILATION RITE (DELETE)                              ==
    # =========================================================================
    def delete_project(self, project_id: str, force: bool = False):
        """The Rite of Annihilation."""
        if project_id not in self.registry.projects:
            raise ArtisanHeresy("Project not found.")

        target = self.registry.projects[project_id]

        # [ASCENSION 11]: DEMO IMMUTABILITY WARD
        if target.is_locked or (target.is_demo and not force):
            raise ArtisanHeresy("Cannot delete a protected/demo reality. Use --force if you are Sovereign.")

        # 1. Physical Removal
        path = Path(target.path)
        if path.exists():
            try:
                shutil.rmtree(path)
            except Exception as e:
                Logger.warn(f"Physical removal partial: {e}")

        # 2. Registry Pruning
        del self.registry.projects[project_id]

        # Handle active project deletion
        if self.registry.active_project_id == project_id:
            self.registry.active_project_id = None
            # Sever the link
            self._sever_link()

        self.persistence.save(self.registry)
        Logger.success(f"Project '{target.name}' returned to void.")

    # =========================================================================
    # == RITE 5: THE ADOPTION RITE (IMPORT)                                  ==
    # =========================================================================
    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        """Adopts an existing directory into the registry."""
        target_path = Path(path).resolve()
        if not target_path.exists():
            raise ArtisanHeresy("Target path does not exist.")

        pid = str(uuid.uuid4())

        # We do NOT move it; we reference it in place.
        stats = self._measure_reality(target_path)

        project = ProjectMeta(
            id=pid,
            name=name,
            path=str(target_path),
            owner_id=owner_id,
            description="Imported Reality",
            tags=["imported"],
            stats=stats
        )

        self.registry.projects[pid] = project
        self.persistence.save(self.registry)
        return project

    # =========================================================================
    # == RITE 6: THE TRANSMUTATION RITE (UPDATE)                             ==
    # =========================================================================
    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """Transmutes project metadata."""
        if project_id not in self.registry.projects:
            raise ArtisanHeresy("Project not found.")

        project = self.registry.projects[project_id]

        # Apply updates safely
        for k, v in updates.items():
            # [ASCENSION 11]: Protect Immutable Fields
            if k in ['id', 'path', 'created_at', 'stats']:
                continue
            if hasattr(project, k):
                setattr(project, k, v)

        project.updated_at = int(time.time() * 1000)
        self.persistence.save(self.registry)
        Logger.info(f"Metadata transmuted for '{project.name}'.")

    # =========================================================================
    # == INTERNAL ORGANS                                                     ==
    # =========================================================================

    def _sever_link(self):
        """Removes the active symlink."""
        if os.environ.get("SCAFFOLD_ENV") != "WASM": return
        link = Path("/vault/project")
        if link.is_symlink() or link.is_file():
            link.unlink()
        elif link.is_dir():
            shutil.rmtree(link)

    def _link_active_reality(self, target_path: Path):
        """
        =============================================================================
        == THE IRON ANCHOR (V-Ω-TOTALITY-V2.5-WASM-RECTIFIED)                      ==
        =============================================================================
        [THE CURE]: Forces the /vault/project coordinate to become a symlink,
        annihilating any physical directory that was created during boot noise.
        """
        if os.environ.get("SCAFFOLD_ENV") != "WASM":
            return

        link = Path("/vault/project")

        try:
            # --- MOVEMENT I: THE PURGATION ---
            # [ASCENSION 13]: If /vault/project is a real directory (not a link),
            # we must return it to the void to make room for the Gnostic Anchor.
            if link.exists():
                if link.is_symlink() or link.is_file():
                    link.unlink()
                elif link.is_dir():
                    # This is the "Boot Ghost" created by the JS layer.
                    import shutil
                    shutil.rmtree(link)
                    Logger.verbose("Boot Ghost directory purged at /vault/project.")

            # --- MOVEMENT II: THE CONSECRATION ---
            # Forge the link to the specific workspace UUID
            os.symlink(str(target_path), str(link))

            # Verify the link is breathing
            if link.exists() and link.is_symlink():
                Logger.success(f"Gnostic Anchor manifest: /vault/project -> {target_path.name}")

        except Exception as e:
            Logger.error(f"Reality Anchor Fracture: {e}")
            # [ASCENSION 14]: Emergency Fallback
            # If symlinking is forbidden by the browser, we resort to a Physical Mirror.
            import shutil
            if not link.exists():
                shutil.copytree(target_path, link)
                Logger.warn("Symlink Rite failed. Switched to Physical Mirroring.")

    def bootstrap_multiverse(self):
        """
        =============================================================================
        == THE RITE OF AUTONOMIC INCEPTION (V-Ω-TOTALITY-HEALED)                   ==
        =============================================================================
        [THE CURE]: Guarantees the existence of the Progenitor and Exhibit Demos.
        """
        # [ASCENSION 1]: Only seed if the registry is a total void.
        if len(self.registry.projects) > 0:
            if self.registry.active_project_id:
                self.switch_project(self.registry.active_project_id)
            return

        Logger.info("🌌 Primordial Void perceived. Materializing Reference Realities...")

        # 1. THE PROGENITOR LAW (The Active Exhibit)
        # We mark it as 'progenitor' so useWorkbench.ts can anchor to it by ID.
        progenitor = self.create_project(
            name="Progenitor Law",
            description="The constitutional soul of the Workbench. Explore the laws of Form and Will.",
            owner_id="SYSTEM_DEMO",
            template="progenitor",
            is_demo=True,
            tags=["core", "manifesto"]
        )

        # 2. THE CANONICAL EXHIBITS
        # These are forged but remain in the dashboard "Library"
        exhibits = [
            ("V-Omega API", "High-throughput FastAPI microservice template.", "fastapi-service", ["backend"]),
            ("Ocular Membrane", "React/Vite frontend structure.", "react-vite", ["frontend"]),
            ("Kinetic Swarm", "Distributed task orchestration demo.", "worker-swarm", ["distributed"])
        ]

        for name, desc, tmpl, tags in exhibits:
            self.create_project(
                name=name,
                description=desc,
                template=tmpl,
                owner_id="SYSTEM_DEMO",
                is_demo=True,
                tags=tags
            )

        # 3. THE FINAL ANCHOR
        # Ensure the Engine is standing on the Progenitor Law.
        self.switch_project(progenitor.id)
        Logger.success("💠 Multiverse Inception Complete. Lattice is Resonant.")

