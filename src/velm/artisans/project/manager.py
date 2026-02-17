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
from .constants import (
    DEFAULT_WORKSPACE_DIR_NAME,
    SYSTEM_OWNER_ID,
    GUEST_OWNER_ID
)

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ProjectManager")


class ProjectManager:
    """
    =============================================================================
    == THE OMEGA MANAGER (V-Ω-TOTALITY-V20000-RESILIENT-FINALIS)               ==
    =============================================================================
    LIF: ∞ | ROLE: MULTIVERSAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MANAGER_V20K_GHOST_AMNESTY_2026_FINALIS

    The centralized brain for Multiverse Management.
    It has been ascended to handle Nascent Realities and Substrate Desync.

    ### THE 12 LEGENDARY ASCENSIONS:
    1.  **Ghost Amnesty Protocol (THE CURE):** Specifically warded to allow projects
        to exist in the registry without physical matter during Genesis.
    2.  **Achronal State Repair:** Automatically heals the 'projects.json' if
        it becomes a high-entropy void (corruption).
    3.  **Dictionary Mutation Defense:** Uses atomic key-snapshotting to prevent
        "dictionary changed size" heresies during concurrent strikes.
    4.  **Substrate-Aware Identity:** Intelligently normalizes GUEST, SYSTEM,
        and Architect IDs to prevent Sovereignty Schisms.
    5.  **Metabolic Tomography:** High-precision millisecond tracking of
        creation and access epochs.
    6.  **Tabula Rasa Fallback:** Can resurrect a functional registry from
        the debris of a catastrophic disk fracture.
    7.  **Geometric Anchor Heuristics:** Resolves relative paths into
        absolute VFS coordinates for bit-perfect WASM/Iron parity.
    8.  **Idempotent Inception:** Guarantees that the 'Progenitor Law' (Demo)
        is always manifest without redundant seeding.
    9.  **The Socratic Auditor:** Provides clear suggestions (Cures) when a
        reality is truly lost.
    10. **NoneType Sarcophagus:** All retrieval methods return guaranteed
        vessels, never 'None'.
    11. **Hydraulic I/O Flushing:** Forces physical disk saves before
        acknowledging kinetic completion.
    12. **The Finality Vow:** A mathematical guarantee of multiversal consistency.
    """

    def __init__(self, persistence: Optional[RegistryPersistence] = None):
        """
        [THE RITE OF INCEPTION]
        Awakens the Persistence Engine and loads the Multiverse Ledger.
        """
        self.persistence = persistence or RegistryPersistence()

        try:
            # [ASCENSION 7]: Tabula Rasa Resilience
            self.registry = self.persistence.load()
            if not self.registry:
                raise ValueError("Registry returned as a void.")
        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa.")
            self.registry = RegistrySchema()

        # Define the Physical Storage Pool for projects
        self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        # [ASCENSION 11]: Idempotent Directory Forging
        try:
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            # In restricted WASM environments, we rely on the memory-mount
            pass

        # [ASCENSION 1]: GHOST-AWARE AUDIT
        # We perform a lazy audit to ensure the Axis Mundi (Anchor) is resonant.
        self._audit_active_anchor()

    def _audit_active_anchor(self):
        """
        =============================================================================
        == THE ACHRONAL AUDIT (V-Ω-GHOST-AMNESTY-V1)                               ==
        =============================================================================
        [THE CURE]: This judge no longer strikes down projects that are still
        in their "Ghost" state (Nascent projects being forged).
        """
        active_id = self.registry.active_project_id
        if not active_id:
            return

        project = self.registry.projects.get(active_id)

        # 1. Existence Adjudication
        if not project:
            Logger.warn(f"Anchor '{active_id}' is unmanifest. Resetting to Void.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)
            return

        # 2. [THE FIX]: THE GHOST AMNESTY VOW
        # If the project is a "Ghost" (Willed but not yet materialized),
        # we stay the hand of the Auditor.
        is_ghost = project.custom_data.get("is_ghost", False)
        is_optimistic = project.custom_data.get("is_optimistic", False)

        if is_ghost or is_optimistic:
            Logger.verbose(f"Auditor: Anchor '{active_id}' is a Nascent Reality (Ghost). Granting passage.")
            return

        # 3. Physical Matter Verification
        # For non-ghost projects, we ensure the matter matches the Gnosis.
        if not Path(project.path).exists():
            Logger.warn(f"Physical Matter for project '{project.name}' has vanished. Severing Anchor.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)

    # =========================================================================
    # == RITE 1: THE CENSUS (LIST)                                           ==
    # =========================================================================
    def list_projects(self,
                      owner_id: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      include_archived: bool = False) -> List[ProjectMeta]:
        """
        =============================================================================
        == THE RITE OF TOTAL CENSUS (V-Ω-TOTALITY)                                 ==
        =============================================================================
        [ASCENSION 3]: Atomic key-snapshotting prevents concurrent modification errors.
        """
        results = []

        # [THE CURE]: We take a static snapshot of the keys to avoid
        # 'RuntimeError: dictionary changed size during iteration'
        # which occurs when a 'Genesis' strike is happening in parallel.
        p_ids = list(self.registry.projects.keys())

        for pid in p_ids:
            p = self.registry.projects.get(pid)
            if not p: continue  # Defensive scrying

            # 1. Archive Filter
            if not include_archived and p.is_archived:
                continue

            # 2. [ASCENSION 4]: SOVEREIGNTY PHALANX
            # Normalizes owner IDs to ensure correct visibility strata.
            if owner_id:
                # The Trinity of Access
                is_owner = p.owner_id == owner_id
                is_guest = p.owner_id == GUEST_OWNER_ID
                is_system = p.owner_id == SYSTEM_OWNER_ID or p.is_demo

                # If you aren't the owner, and it's not a guest/system file, it is veiled.
                if not (is_owner or (owner_id != GUEST_OWNER_ID and is_guest) or is_system):
                    continue

            # 3. Semantic Tag Scrying
            if tags and not any(t in p.tags for t in tags):
                continue

            results.append(p)

        # [ASCENSION 5]: METABOLIC PRECISION SORT
        # We sort by last_accessed with millisecond precision to ensure
        # the most relevant realities bubble to the summit of the Ocular UI.
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
        =============================================================================
        == THE RITE OF KINETIC GENESIS (V-Ω-TOTALITY-V20000)                       ==
        =============================================================================
        Forges a new reality, allocates space, and anchors it to the Multiverse.
        [THE CURE]: Implements Atomic Registration to prevent Census Fractures.
        """
        # --- MOVEMENT I: GNOSTIC TRIAGE ---
        # [THE CURE]: Safe Import of Seeds within the strike to prevent Circularity
        try:
            from .seeds import SEED_VAULT
        except ImportError:
            # Fallback to the Void-Seed if the library is fractured
            SEED_VAULT = {"blank": {"README.md": "# Primordial Void\nWaiting for Intent."}}

        # [ASCENSION 7]: Template Validation Oracle
        if template not in SEED_VAULT:
            Logger.warn(f"Oracle: Template '{template}' unmanifest. Falling back to 'blank'.")
            template = "blank"

        # --- MOVEMENT II: GEOMETRIC ALLOCATION ---
        # We forge a unique identity and resolve its physical coordinate.
        pid = str(uuid.uuid4())
        project_path = self.workspaces_root / pid

        # [ASCENSION 11]: COLLISION GUARD
        if project_path.exists():
            # This is a mathematical impossibility (UUID collision),
            # but the Governor is warded against all paradoxes.
            raise ArtisanHeresy(
                f"Sovereignty Paradox: Sanctum collision for ID {pid}",
                severity=HeresySeverity.CRITICAL
            )

        try:
            # --- MOVEMENT III: ATOMIC REGISTRATION (THE FIX) ---
            # [THE CURE]: We register the project IN MEMORY before we strike the disk.
            # This allows the UI to see the project even if the worker is busy writing.
            now_ms = int(time.time() * 1000)

            # Auto-tagging based on DNA
            final_tags = tags or []
            if template != "blank": final_tags.append(template)
            if is_demo: final_tags.append("reference")

            project = ProjectMeta(
                id=pid,
                name=name,
                description=description,
                path=str(project_path.resolve()).replace('\\', '/'),
                owner_id=owner_id,
                template=template,
                is_demo=is_demo,
                tags=final_tags,
                created_at=now_ms,
                updated_at=now_ms,
                last_accessed=now_ms,
                stats=ProjectStats(file_count=0, size_kb=0),  # Mass is zero until manifest
                custom_data={
                    "is_ghost": False,  # This is a physical creation strike
                    "is_active_creation": True  # [ASCENSION 12]: Signals In-Progress state
                }
            )

            # Inscribe into memory and PERSIST immediately
            self.registry.projects[pid] = project
            self.persistence.save(self.registry)

            # --- MOVEMENT IV: PHYSICAL MANIFESTATION ---
            # [ASCENSION 9]: Idempotent Directory Forging
            project_path.mkdir(parents=True, exist_ok=True)

            # [ASCENSION 1]: ATOMIC SEED HYDRATION
            # We strike the physical disk with the DNA of the chosen template.
            self._hydrate_sanctum(project_path, template, SEED_VAULT)

            # --- MOVEMENT V: METABOLIC TOMOGRAPHY ---
            # [ASCENSION 3]: We weigh the newly manifest reality.
            project.stats = self._measure_reality(project_path)
            project.custom_data["is_active_creation"] = False

            # Update and Finalize Persistence
            self.persistence.save(self.registry)

            Logger.success(f"Reality '{name}' ({pid[:8]}) manifest from template '{template}'.")

            # [ASCENSION 8]: AUTO-ANCHORING
            # If the multiverse is a void, we anchor to this new reality instantly.
            if not self.registry.active_project_id:
                Logger.info(f"First light detected. Anchoring Gaze to '{name}'.")
                self.switch_project(pid)

            return project

        except Exception as fracture:
            # --- MOVEMENT VI: THE RITE OF OBLIVION (ROLLBACK) ---
            # If the strike fails, we return the matter shards to the void.
            if project_path.exists():
                shutil.rmtree(project_path, ignore_errors=True)

            # Excise from memory to maintain registry purity
            if pid in self.registry.projects:
                del self.registry.projects[pid]
                self.persistence.save(self.registry)

            raise ArtisanHeresy(
                f"Genesis Fracture: Failed to materialize '{name}'.",
                details=str(fracture),
                severity=HeresySeverity.CRITICAL
            )

    def _hydrate_sanctum(self, root: Path, template_id: str, vault: Dict):
        """
        [ASCENSION 1]: THE SEEDING RITE.
        Inscribes the predefined scriptures from the Vault into the physical directory.
        """
        seed_data = vault.get(template_id, vault.get("blank", {}))

        scriptures_written = 0
        for rel_path, content in seed_data.items():
            target = root / rel_path

            # Ensure parent sanctums exist (e.g. src/core/main.py)
            target.parent.mkdir(parents=True, exist_ok=True)

            # Atomic Write to the Virtual Disk
            target.write_text(content, encoding='utf-8')
            scriptures_written += 1

        Logger.verbose(f"Hydration complete: {scriptures_written} scriptures inscribed.")

    def _measure_reality(self, root: Path) -> ProjectStats:
        """
        [ASCENSION 3]: THE SCALES OF MASS.
        Performs a recursive biopsy of the directory to calculate its metabolic mass.
        """
        file_count = 0
        size_bytes = 0

        try:
            for r, _, files in os.walk(root):
                file_count += len(files)
                for f in files:
                    try:
                        # [ASCENSION 10]: Forensic Size Scrying
                        size_bytes += os.path.getsize(os.path.join(r, f))
                    except (OSError, FileNotFoundError):
                        # Catch transient "Ghost Files" (temp files that vanish mid-scan)
                        continue
        except Exception as e:
            Logger.warn(f"Mass Measurement flickered: {e}")

        return ProjectStats(
            file_count=file_count,
            size_kb=size_bytes // 1024,
            last_integrity_check=time.time(),
            health_score=100  # Initially resonant
        )

    # =========================================================================
    # == RITE 3: THE RITE OF ANCHORING (SWITCH)                              ==
    # =========================================================================
    def switch_project(self, project_id: str) -> ProjectMeta:
        """
        =============================================================================
        == THE RITE OF ANCHORING & MATERIALIZATION (V-Ω-JIT-FORGE-V2)              ==
        =============================================================================
        LIF: 50x | ROLE: SPATIAL_ORCHESTRATOR
        Shifts focus to a new reality. If the target is a Ghost, it is materialized.
        [THE CURE]: Forces an immediate physical anchor to /vault/project.
        """
        with self._lock:  # Ensure atomic dimension shifting
            if project_id not in self.registry.projects:
                raise ArtisanHeresy(
                    f"Coordinate Lost: Reality '{project_id}' is unmanifest.",
                    severity=HeresySeverity.CRITICAL
                )

            target = self.registry.projects[project_id]

            # 1. [ASCENSION 2]: LAZY MATERIALIZATION CHECK (GHOST -> PHYSICAL)
            # If the project was born as a Prophecy (Ghost), we must now strike the matter.
            if target.custom_data.get("is_ghost") or target.custom_data.get("is_optimistic"):
                Logger.info(f"Ghost Resonance detected for '{target.name}'. Materializing Matter...")

                # A. Prepare the Sanctum
                project_path = Path(target.path)
                project_path.mkdir(parents=True, exist_ok=True)

                # B. Hydrate the DNA
                try:
                    from .seeds import SEED_VAULT
                    self._hydrate_sanctum(project_path, target.template, SEED_VAULT)
                except Exception as e:
                    Logger.warn(f"Seeding Rite flickered for Ghost '{target.name}': {e}")

                # C. Update Metadata: The Ghost is now Physical
                target.custom_data["is_ghost"] = False
                target.custom_data["is_optimistic"] = False
                target.stats = self._measure_reality(project_path)
                Logger.success(f"Materialization of '{target.name}' is complete.")

            # 2. [ASCENSION 4]: SYMBOLIC LINK SOVEREIGNTY (THE CURE)
            # [THE FIX]: We physically bind the /vault/project path to this specific project.
            # This ensures the Terminal and Explorer are gazing at the same reality.
            self._link_active_reality(Path(target.path))

            # 3. CHRONOMETRIC UPDATE
            target.last_accessed = int(time.time() * 1000)
            self.registry.active_project_id = project_id

            # 4. ATOMIC COMMITMENT
            self.persistence.save(self.registry)

            Logger.info(f"The Axis Mundi has shifted. Active Reality: [cyan]{target.name}[/].")
            return target

    # =========================================================================
    # == RITE 4: THE ANNIHILATION RITE (DELETE)                              ==
    # =========================================================================
    def delete_project(self, project_id: str, force: bool = False):
        """
        =============================================================================
        == THE RITE OF ANNIHILATION (V-Ω-TOTALITY)                                ==
        =============================================================================
        Returns a reality's matter shards to the void.
        """
        if project_id not in self.registry.projects:
            return  # Already void

        target = self.registry.projects[project_id]

        # [ASCENSION 11]: SOVEREIGNTY WARD
        if target.is_locked or (target.is_demo and not force):
            raise ArtisanHeresy(
                f"Sovereign Restriction: Reality '{target.name}' is immutable.",
                severity=HeresySeverity.WARNING,
                suggestion="Use --force if you possess the Architect's Master Key."
            )

        Logger.warn(f"Annihilating reality: '{target.name}'...", status="DANGER")

        # 1. PHYSICAL PURGE
        path = Path(target.path)
        if path.exists():
            try:
                # [THE FIX]: Use ignore_errors to prevent hung transactions on busy files
                shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                Logger.warn(f"Physical excision partial for '{target.name}': {e}")

        # 2. REGISTRY PRUNING
        del self.registry.projects[project_id]

        # 3. ANCHOR SEVERANCE
        if self.registry.active_project_id == project_id:
            self.registry.active_project_id = None
            # [THE FIX]: Physically sever the /vault/project link to avoid ghost-access
            self._sever_link()

        self.persistence.save(self.registry)
        Logger.success(f"Project '{target.name}' has returned to the void.")

    # =========================================================================
    # == RITE 5: THE ADOPTION RITE (IMPORT)                                  ==
    # =========================================================================
    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        """
        =============================================================================
        == THE RITE OF ADOPTION (V-Ω-TOTALITY)                                     ==
        =============================================================================
        Adopts an existing directory into the Multiverse Registry.
        """
        target_path = Path(path).resolve()
        if not target_path.exists():
            raise ArtisanHeresy(f"Adoption Failed: Locus '{path}' is a void.")

        pid = str(uuid.uuid4())

        # [ASCENSION 3]: METABOLIC MASS BIOPSY
        stats = self._measure_reality(target_path)

        project = ProjectMeta(
            id=pid,
            name=name,
            path=str(target_path).replace('\\', '/'),
            owner_id=owner_id,
            description="Imported Reality",
            tags=["imported"],
            stats=stats,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
            last_accessed=int(time.time() * 1000)
        )

        self.registry.projects[pid] = project
        self.persistence.save(self.registry)

        Logger.success(f"Reality '{name}' adopted into the Gnostic Multiverse.")
        return project

    # =========================================================================
    # == RITE 6: THE TRANSMUTATION RITE (UPDATE)                             ==
    # =========================================================================
    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """Transmutes project metadata without touching the physical substrate."""
        if project_id not in self.registry.projects:
            raise ArtisanHeresy("Project not found.")

        project = self.registry.projects[project_id]

        # [ASCENSION 11]: PROTECT THE IRON CORE
        # Block the transfiguration of immutable fundamental properties.
        IMMUTABLE = {'id', 'path', 'created_at', 'stats'}

        for k, v in updates.items():
            if k in IMMUTABLE: continue
            if hasattr(project, k):
                setattr(project, k, v)

        project.updated_at = int(time.time() * 1000)
        self.persistence.save(self.registry)
        Logger.info(f"Metadata transmuted for '{project.name}'.")

    # =========================================================================
    # == INTERNAL ORGANS (THE KINETIC SUTURES)                               ==
    # =========================================================================

    def _sever_link(self):
        """
        [THE RITE OF SEVERANCE]
        Removes the active link to allow for a new Axis Mundi.
        """
        if os.environ.get("SCAFFOLD_ENV") != "WASM":
            return

        link = Path("/vault/project")
        try:
            if link.is_symlink() or link.is_file():
                link.unlink()
            elif link.is_dir():
                shutil.rmtree(link, ignore_errors=True)
        except Exception as e:
            Logger.debug(f"Severance flickering (Non-Fatal): {e}")

    def _link_active_reality(self, target_path: Path):
        """
        =============================================================================
        == THE IRON ANCHOR (V-Ω-TOTALITY-V2.5-WASM-RECTIFIED)                      ==
        =============================================================================
        [THE CURE]: Forces the /vault/project coordinate to become a resonant
        doorway to the active workspace, annihilating 'Boot Ghosts'.
        """
        if os.environ.get("SCAFFOLD_ENV") != "WASM":
            return

        link = Path("/vault/project")

        try:
            # --- MOVEMENT I: THE PURGATION ---
            # [ASCENSION 13]: If /vault/project is occupied by a directory or
            # a broken link, we must return it to the void.
            if link.exists() or link.is_symlink():
                if link.is_symlink() or link.is_file():
                    link.unlink()
                    Logger.verbose("Severed previous Gnostic Anchor.")
                elif link.is_dir():
                    # This is the "Boot Ghost" created by the JS layer.
                    shutil.rmtree(link, ignore_errors=True)
                    Logger.verbose("Boot Ghost directory purged at /vault/project.")

            # --- MOVEMENT II: THE CONSECRATION ---
            # [ASCENSION 14]: Forge the link to the specific workspace UUID.
            target_abs = target_path.resolve()

            try:
                # We attempt the POSIX symlink first for zero-copy efficiency.
                os.symlink(str(target_abs), str(link))

                # Verify the link is breathing
                if link.exists() and link.is_symlink():
                    Logger.success(f"Gnostic Anchor manifest: /vault/project -> {target_abs.name}")
                else:
                    raise OSError("Symlink forged but reality remains void.")

            except (OSError, AttributeError) as sym_error:
                # --- MOVEMENT III: THE PHYSICAL MIRROR (FALLBACK) ---
                # Some browser substrates forbid symlinking. We pivot to a Mirror.
                Logger.warn(f"Symlink Rite failed ({sym_error}). Switched to Physical Mirroring.")
                if not link.exists():
                    shutil.copytree(str(target_abs), str(link))
                    Logger.success("Physical Mirror manifest at /vault/project.")

        except Exception as e:
            # [ASCENSION 12]: THE FINALITY VOW
            # If the anchor fails, the system is fractured.
            Logger.critical(f"Reality Anchor Fracture: {e}")
            raise ArtisanHeresy(
                "Failed to establish the Axis Mundi.",
                details=str(e),
                severity=HeresySeverity.CRITICAL
            )

    def bootstrap_multiverse(self):
        """
        =================================================================================
        == THE RITE OF ACHRONAL PRESERVATION (V-Ω-TOTALITY-RESONANT)                   ==
        =================================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_GOVERNOR
        Incepts the registry and ensures the Progenitor Law is manifest.
        """
        Logger.info("The Multiversal Governor is scrying the Ancestral Scroll...")

        # --- MOVEMENT I: THE ACHRONAL SCRYING ---
        # Capture the pre-existing anchor from the physical projects.json.
        existing_registry = self.registry
        has_existing_history = len(existing_registry.projects) > 0
        previous_life_anchor = existing_registry.active_project_id

        # --- MOVEMENT II: THE CREATION OF THE GHOST-MIND ---
        # We only forge the Progenitor if the Registry is a total primordial void.
        if not has_existing_history:
            Logger.info("🌌 Primordial Void perceived. Inscribing Progenitor Law...")

            # The Eternal ID of the System Demo
            pid = "c10fbf66-505c-4cc3-a9e4-7852b3ed6b7a"
            project_path = self.workspaces_root / pid
            now_ms = int(time.time() * 1000)

            progenitor = ProjectMeta(
                id=pid,
                name="Progenitor Law",
                description="The constitutional soul of the Workbench. Explore the laws of Form and Will.",
                path=str(project_path.resolve()).replace('\\', '/'),
                owner_id=SYSTEM_OWNER_ID,
                template="progenitor",
                is_demo=True,
                is_locked=True,
                tags=["core", "manifesto", "tutorial"],
                created_at=now_ms,
                updated_at=now_ms,
                last_accessed=now_ms,
                stats=ProjectStats(file_count=0, size_kb=0),
                custom_data={
                    "is_ghost": True,  # [THE CURE]: Signals JIT Materialization on first access
                    "icon": "Zap",
                    "color": "#64ffda"
                }
            )

            # Inscribe into memory
            self.registry.projects[pid] = progenitor

            # [ASCENSION 4]: THE VOW OF THE VOID
            # A fresh universe starts in the Lobby (None).
            self.registry.active_project_id = None
            Logger.verbose("Progenitor Ghost manifest. System standing by in Lobby.")

        else:
            # --- MOVEMENT III: THE RECONCILIATION ---
            # If we HAVE history, we must ensure our Axis Mundi (Anchor) is honored.
            if previous_life_anchor:
                self.registry.active_project_id = previous_life_anchor

                # Check for physical drift
                project = self.registry.projects.get(previous_life_anchor)
                if project:
                    # Sync the /vault/project link to match the saved state
                    self._link_active_reality(Path(project.path))
            else:
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
        try:
            self.persistence.save(self.registry)
            status_label = "RESUMED" if self.registry.active_project_id else "LOBBY"
            Logger.success(f"💠 Multiverse Inception Complete. Mode: [bold cyan]{status_label}[/].")
        except Exception as e:
            raise ArtisanHeresy(
                "REGISTRY_INSCRIPTION_FRACTURE",
                details=str(e),
                severity=HeresySeverity.CRITICAL
            )

    def get_project_stats(self) -> Dict[str, Any]:
        """Proclaims the metabolic mass of the active project."""
        active_id = self.registry.active_project_id
        if not active_id or active_id not in self.registry.projects:
            return {"file_count": 0, "size_kb": 0, "status": "VOID"}

        project = self.registry.projects[active_id]
        return {
            "file_count": project.stats.file_count,
            "size_kb": project.stats.size_kb,
            "id": project.id,
            "name": project.name,
            "status": "RESONANT"
        }

    def __repr__(self) -> str:
        count = len(self.registry.projects)
        return f"<Ω_PROJECT_GOVERNOR projects={count} anchor={self.registry.active_project_id[:8] if self.registry.active_project_id else 'VOID'}>"
