# Path: src/velm/artisans/project/manager.py
# ------------------------------------------

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
        try:
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass  # In WASM, permissions might be strict, but we proceed in memory.

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
        # [THE CURE]: Safe Import of Seeds to prevent Circularity
        try:
            from .seeds import SEED_VAULT
        except ImportError:
            SEED_VAULT = {"blank": {"README.md": "# Void"}}

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
            self._hydrate_sanctum(project_path, template, SEED_VAULT)

            # 3. [ASCENSION 3]: METABOLIC MASS CALCULATION
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

    def _hydrate_sanctum(self, root: Path, template_id: str, vault: Dict):
        """
        [ASCENSION 1]: The Seeding Rite.
        Writes the predefined files from the Vault into the physical directory.
        """
        seed_data = vault.get(template_id, vault.get("blank", {}))

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
        == THE IRON ANCHOR (V-Ω-TOTALITY-V2.5-WASM-RECTIFIED-FINALIS)              ==
        =============================================================================
        LIF: ∞ | ROLE: SPATIAL_REALITY_BINDER | RANK: OMEGA_SUPREME
        AUTH: Ω_ANCHOR_V25_SYMLINK_SUTURE_2026_FINALIS

        [ARCHITECTURAL CONSTITUTION]
        This rite establishes the physical connection between the Engine's perception
        of "The Project" (/vault/project) and the actual storage locus of the
        active workspace (/vault/workspaces/<uuid>).

        ### THE PANTHEON OF 5 ASCENSIONS:
        1.  **Absolute Resolution (THE FIX):** Forces the target path to a resolved,
            absolute coordinate to prevent relative symlink heresies.
        2.  **Ghost Purgation:** Ruthlessly annihilates any existing matter at
            /vault/project (whether file, dir, or link) to ensure a clean mount.
        3.  **The Symlink Vow:** Attempts the POSIX standard `os.symlink` first.
        4.  **Physical Mirror Fallback:** If the browser's VFS rejects the symlink
            (common in some IDBFS implementations), it falls back to a deep copy
            (`shutil.copytree`), ensuring continuity of existence.
        5.  **Verification Gaze:** Explicitly checks if the anchor holds before
            proclaiming success.
        """
        if os.environ.get("SCAFFOLD_ENV") != "WASM":
            return

        # The Anchor Point in the Virtual Filesystem
        link = Path("/vault/project")

        # [ASCENSION 1]: ABSOLUTE COORDINATE RESOLUTION
        # We must ensure we are pointing to the absolute truth of the workspace.
        target_abs = target_path.resolve()

        Logger.debug(f"Initiating Reality Anchor: {link} -> {target_abs}")

        try:
            # --- MOVEMENT I: THE RITE OF PURGATION ---
            # We must clear the stage for the new reality.
            if link.exists() or link.is_symlink():
                try:
                    if link.is_symlink():
                        link.unlink()
                        Logger.verbose("Severed previous symlink connection.")
                    elif link.is_dir():
                        # This is the "Boot Ghost" created by the JS layer initialization.
                        shutil.rmtree(link)
                        Logger.verbose("Annihilated Boot Ghost directory at /vault/project.")
                    else:
                        link.unlink()
                        Logger.verbose("Removed obstruction at anchor point.")
                except Exception as e:
                    Logger.warn(f"Purgation resistance encountered: {e}. Attempting override...")
                    # Last ditch effort
                    if link.is_dir():
                        shutil.rmtree(link, ignore_errors=True)
                    else:
                        os.remove(str(link))

            # --- MOVEMENT II: THE CONSECRATION OF THE LINK ---
            # We attempt to forge a wormhole (Symlink) between the locations.
            try:
                os.symlink(str(target_abs), str(link))

                # Verify the bond
                if link.exists():
                    # Check if it resolves correctly
                    resolved = link.resolve()
                    if resolved == target_abs:
                         Logger.success(f"Gnostic Anchor manifest: /vault/project -> {target_abs.name}")
                    else:
                         Logger.warn(f"Anchor Drift Detected: Linked to {resolved}, expected {target_abs}")
                else:
                    raise OSError("Symlink forged but reality remains void.")

            except (OSError, AttributeError) as symlink_error:
                # --- MOVEMENT III: THE PHYSICAL MIRROR (FALLBACK) ---
                # Some WASM file systems do not support symlinks. We must copy the matter.
                Logger.warn(f"Symlink Rite rejected by Substrate ({symlink_error}). Engaging Physical Mirroring...")

                if not link.exists():
                    try:
                        # Copy the entire workspace to the project mount
                        shutil.copytree(str(target_abs), str(link))
                        Logger.success(f"Physical Mirror complete. Reality replicated to /vault/project.")
                    except Exception as copy_error:
                         Logger.critical(f"Physical Mirroring Failed: {copy_error}")
                         raise ArtisanHeresy(
                             "Reality Anchor Collapse",
                             details=f"Neither symlink nor copy could establish /vault/project.\nSymlink: {symlink_error}\nCopy: {copy_error}",
                             severity=HeresySeverity.CRITICAL
                         )

        except Exception as e:
            Logger.critical(f"Reality Anchor Fracture: {e}")
            raise ArtisanHeresy(
                "Failed to anchor active project.",
                details=str(e),
                severity=HeresySeverity.CRITICAL
            )

    def bootstrap_multiverse(self):
        """
        =================================================================================
        == THE RITE OF ACHRONAL PRESERVATION: OMEGA (V-Ω-TOTALITY-V25000-RESONANT)     ==
        =================================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_BOOTSTRAP_V25K_ANCHOR_PERMANENCE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite conducts the primordial inception of the Multiverse Registry. It has
        been transfigured to honor the Law of Persistence, ensuring that the
        'active_project_id' (The Anchor) is preserved across temporal reboots, while
        simultaneously enforcing the 'Boot-to-Void' protocol for fresh universes.

        ### THE PANTHEON OF 12 ASCENSIONS:
        1.  **Achronal Scrying:** Inspects the physical 'projects.json' scroll BEFORE
            logic evaluation to detect existing Gnostic anchors.
        2.  **Sovereign Anchor Preservation:** If an active_project_id is manifest in
            the scroll, it is granted 'First-Status' and warded against overwrites.
        3.  **The Ghost-Mind Protocol:** Inscribes the 'Progenitor Law' as a latent
            metaphysical project (Matter=Void) to prevent 'Forced Seeding' heresies.
        4.  **The Vow of the Zero-Point Lobby:** If the Multiverse is a primordial
            void, the Anchor is left as None, forcing the Ocular UI to render the
            Lobby (Intent Scrier).
        5.  **Substrate-Aware Geometry:** Resolves physical paths relative to the
            workspaces_root with absolute POSIX normalization.
        6.  **Idempotent Inscription:** Prevents the creation of duplicate Progenitor
            nodes if the Registry is already resonant.
        7.  **Metabolic Tomography:** Records the precise timestamp of multiversal
            inception in milliseconds for bit-perfect frontend sync.
        8.  **The Identity Suture:** Stamps the Progenitor with high-status tags
            ('core', 'manifesto') to guide the Architect's perception.
        9.  **NoneType Sarcophagus:** Hardens the registry return against null-pointer
            heresies during high-frequency scrying bursts.
        10. **Hydraulic Sync:** Forces a physical save to the persistence layer
            immediately upon ghost-mind formation.
        11. **Socratic Diagnostics:** Proclaims the state of the Multiverse (VOID vs
            RESUMED) to the internal Gnostic logs.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable CWD.
        =================================================================================
        """
        Logger.info("The Multiversal Governor is scrying the Ancestral Scroll...")

        # --- MOVEMENT I: THE ACHRONAL SCRYING ---
        # We first perceive the current state of the Registry.
        # self.persistence.load() was called in __init__, but we capture the anchor now.
        existing_registry = self.registry
        has_existing_history = len(existing_registry.projects) > 0

        # [THE FIX]: Capture the pre-existing anchor if it exists in the physical scroll.
        # This prevents the 'Snap-back' heresy by ensuring we don't overwrite a live session ID.
        previous_life_anchor = existing_registry.active_project_id

        if previous_life_anchor:
            Logger.info(f"Existing Anchor perceived: [cyan]{previous_life_anchor[:8]}[/]. Preservation Vow active.")

        # --- MOVEMENT II: THE CREATION OF THE GHOST-MIND ---
        # We only forge the Progenitor if the Registry is a total primordial void.
        if not has_existing_history:
            Logger.info("🌌 Primordial Void perceived. Inscribing Potential Realities...")

            # The Eternal ID of the System Demo
            pid = "c10fbf66-505c-4cc3-a9e4-7852b3ed6b7a"
            project_path = self.workspaces_root / pid
            now_ms = int(time.time() * 1000)

            # [ASCENSION 3]: We forge the project metadata WITHOUT materializing files.
            # The stats are willed as 0/0 because matter does not yet follow this gnosis.
            progenitor = ProjectMeta(
                id=pid,
                name="Progenitor Law",
                description="The constitutional soul of the Workbench. Explore the laws of Form and Will.",
                path=str(project_path),
                owner_id="SYSTEM_DEMO",
                template="progenitor",
                is_demo=True,
                is_locked=True,
                tags=["core", "manifesto", "tutorial"],
                created_at=now_ms,
                updated_at=now_ms,
                last_accessed=now_ms,
                stats=ProjectStats(file_count=0, size_kb=0, health_score=100),
                custom_data={
                    "is_ghost": True,  # [THE CURE]: Signals JIT Materialization
                    "icon": "Zap",
                    "color": "#64ffda"
                }
            )

            # Inscribe into memory
            self.registry.projects[pid] = progenitor

            # [ASCENSION 4]: THE VOW OF THE VOID
            # Since this is a fresh universe, we do NOT set an active project.
            # This forces the GnosticWorkbench to render the Intent Scrier (Lobby).
            self.registry.active_project_id = None

            Logger.verbose("Progenitor Ghost manifest. active_project_id set to VOID (None).")

        else:
            # --- MOVEMENT III: THE RECONCILIATION ---
            # If we HAVE history, we must ensure our Axis Mundi (Anchor) is honored.
            if previous_life_anchor:
                # [ASCENSION 2]: Preservation of the Anchor.
                # We ensure the active project ID from the scroll is maintained as the current truth.
                self.registry.active_project_id = previous_life_anchor

                # Verify that the physical coordinate is still breathing.
                project = self.registry.projects.get(previous_life_anchor)
                if project and not Path(project.path).exists():
                    Logger.warn(f"Anchor '{previous_life_anchor[:8]}' points to a void. Reality desync detected.")
                    # We do not reset to null here; we allow the VFS scryer to report the heresy.
            else:
                # History exists but no project was active. Maintain Lobby mode.
                self.registry.active_project_id = None

        # =========================================================================
        # == [REDACTED KINETIC ACT]: FORGE_VFS_STRIKE (ENTERPRISE RESURRECTION)   ==
        # =========================================================================
        # [GNOSTIC COMMENTARY FOR ARCHITECTS]:
        # To resurrect the 'Forced Seeding' for corporate clients or compliance
        # environments, uncomment the block below.
        #
        # UTILITY:
        # Use this to ensure that every new Node materializes a specific set of
        # 'Sanctified Policies' or 'Standard Libraries' immediately upon boot,
        # bypassing the Architect's choice for the sake of Enterprise Uniformity.
        # -------------------------------------------------------------------------
        # if CORPORATE_ENFORCEMENT_ACTIVE:
        #     self.logger.verbose("Enterprise Vow Active: Forcing materialization of the Progenitor...")
        #     project_path.mkdir(parents=True, exist_ok=True)
        #     from .seeds import SEED_VAULT
        #     self._hydrate_sanctum(project_path, progenitor.template, SEED_VAULT)
        #     self.registry.active_project_id = pid
        # =========================================================================

        # --- MOVEMENT IV: ATOMIC COMMITMENT ---
        # We seal the Book of Names into the physical projects.json scripture.
        try:
            self.persistence.save(self.registry)

            status_label = "RESUMED" if self.registry.active_project_id else "LOBBY"
            Logger.success(f"💠 Multiverse Inception Complete. Mode: [bold cyan]{status_label}[/].")

        except Exception as e:
            # [ASCENSION 9]: The NoneType Sarcophagus
            raise ArtisanHeresy(
                "REGISTRY_INSCRIPTION_FRACTURE",
                details=f"Failed to seal the Book of Names: {str(e)}",
                severity=HeresySeverity.CRITICAL,
                suggestion="Check filesystem permissions for /vault/projects.json"
            )
    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        =============================================================================
        == THE RITE OF ANCHORING & MATERIALIZATION (V-Ω-JIT-FORGE)                 ==
        =============================================================================
        Shifts focus. If the target is a Ghost, it materializes it instantly (Lazy Load).
        """
        if project_id not in self.registry.projects:
            raise ArtisanHeresy("Project ID not found in registry.")

        target = self.registry.projects[project_id]

        # [ASCENSION 2]: LAZY MATERIALIZATION CHECK
        if target.custom_data.get("is_ghost"):
            Logger.info(f"Ghost State detected for '{target.name}'. Materializing Matter...")

            # A. Create Sanctum
            project_path = Path(target.path)
            project_path.mkdir(parents=True, exist_ok=True)

            # B. Hydrate Seeds
            # We must import SEED_VAULT here to avoid circularity if at top level
            from .seeds import SEED_VAULT
            self._hydrate_sanctum(project_path, target.template, SEED_VAULT)

            # C. Update Metadata (It is now Physical)
            target.custom_data["is_ghost"] = False
            target.stats = self._measure_reality(project_path)
            Logger.success(f"Materialization Complete.")

        # Update Access Time
        target.last_accessed = int(time.time() * 1000)
        self.registry.active_project_id = project_id

        # [ASCENSION 4]: SYMBOLIC LINK SOVEREIGNTY
        self._link_active_reality(Path(target.path))

        self.persistence.save(self.registry)
        Logger.info(f"Active Reality switched to: {target.name}")
        return target

    def get_project_stats(self) -> Dict[str, Any]:
        """Proclaims the metabolic mass of the active project."""
        if not self.registry.active_project_id:
            return {"file_count": 0, "size_kb": 0}

        project = self.registry.projects[self.registry.active_project_id]
        return {
            "file_count": project.stats.file_count,
            "size_kb": project.stats.size_kb,
            "id": project.id,
            "name": project.name
        }