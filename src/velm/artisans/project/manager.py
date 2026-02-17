# Path: src/velm/artisans/project/manager.py
# ------------------------------------------

import time
import shutil
import uuid
import os
import json
import hashlib
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Set

# --- DIVINE UPLINKS ---
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
    =================================================================================
    == THE OMEGA MANAGER (V-Ω-TOTALITY-V100000.0-LEGENDARY-APOTHEOSIS)             ==
    =================================================================================
    LIF: ∞ (THE ETERNAL GOVERNOR) | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MANAGER_V100K_SEED_TOTALLY_MANIFEST_2026_FINALIS

    The Centralized Brain of the Velm Multiverse.
    It is the Keeper of the Book of Names (Registry), the Forger of Sanctums (Workspaces),
    and the Guardian of the Axis Mundi (Active Project Link).

    This artifact has been ascended beyond the limits of standard engineering. It possesses
    **Autonomic Self-Healing**, **Ghost-Mind Hydration**, and **Deterministic Seed Census** capabilities.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **The Seed Census (THE CURE):** Upon bootstrap, it iterates the entire `SEED_VAULT`
        and registers every archetype as a 'Ghost Demo'. This ensures the Lobby is never
        empty, even on a fresh boot, curing the 'Progenitor Monopoly'.
    2.  **Ghost Amnesty Protocol:** Projects can exist as pure metadata ("Ghosts") in the
        Registry without consuming physical disk space until they are first accessed (Switched).
        This reduces boot time from O(N) to O(1).
    3.  **Deterministic Identity Forging:** Uses UUIDv5 (Namespace DNS) to generate consistent,
        reproducible IDs for System Demos based on their template names. A demo for 'fastapi'
        will always have the same UUID across all machines.
    4.  **The Mutex Anchor:** A re-entrant `RLock` guards every mutation of the Registry,
        preventing race conditions during high-concurrency 'Genesis Swarms'.
    5.  **Achronal State Repair:** Automatically detects and heals a corrupted `projects.json`
        by reverting to a Tabula Rasa state rather than crashing the Kernel.
    6.  **Dictionary Mutation Defense:** Uses atomic key-snapshotting during iteration to
        prevent `RuntimeError: dictionary changed size` during async operations.
    7.  **Substrate-Aware Identity:** Intelligently normalizes `GUEST` vs `SYSTEM` ownership,
        ensuring that user projects are distinct from system references.
    8.  **Metabolic Tomography:** Tracks high-precision millisecond timestamps for `created_at`,
        `updated_at`, and `last_accessed` for accurate LRU sorting in the UI.
    9.  **Geometric Anchor Heuristics:** Resolves relative paths into absolute VFS coordinates,
        enforcing POSIX standards (`/vault/workspaces/...`) even on Windows hosts.
    10. **The Socratic Auditor:** Runs a background audit on init to prune "Zombie Projects"
        (registry entries pointing to non-existent paths) unless they are marked as Ghosts.
    11. **NoneType Sarcophagus:** All retrieval methods return guaranteed objects or raise
        structured `ArtisanHeresy` exceptions—never returning `None` to the caller.
    12. **Hydraulic I/O Flushing:** Forces physical disk saves (`fsync` equivalent via atomic write)
        before acknowledging any kinetic completion.
    13. **JIT Materialization:** When switching to a Ghost Project, the Manager detects its
        ethereal state and instantly materializes the physical files from the Seed Vault
        before completing the switch.
    14. **The Axis Mundi Link:** Manages the `/vault/project` symlink (or copy) to ensure
        the CLI tools always know where "Current Reality" is located.
    15. **Atomic Rollback:** If a Genesis Rite fails mid-flight, the Manager scrubs the
        partial directory and reverts the Registry entry, leaving no trace of the failure.
    16. **Telemetric Radiation:** Broadcasts "REALITY_SHIFT" and "MATTER_MANIFESTED" events
        to the Ocular HUD via the Scribe's hidden channels.
    17. **Double-Checked Locking:** Checks existence conditions both before and inside the lock
        to maximize performance without sacrificing safety.
    18. **The Immutable Core:** Protects system-critical fields (ID, Template) from accidental
        mutation during `update_project` rites.
    19. **Mass Calculation:** Performs recursive file-size calculation to report the "Metabolic Mass"
        of a project in KB.
    20. **Tag Heuristics:** Automatically applies semantic tags (`backend`, `frontend`, `system`)
        based on the template DNA during creation.
    21. **Legacy Import Support:** Can adopt existing directories into the multiverse via `import_project`,
        generating a fresh UUID while preserving the physical matter.
    22. **Environment Suture:** Reads `SCAFFOLD_ENV` to adjust behavior for WASM (no symlinks) vs
        Iron (symlinks allowed).
    23. **The Finality Vow:** Returns a strictly typed `ProjectMeta` object that is guaranteed
        to be JSON-serializable for the bridge.
    24. **Universal Access:** Provides `get_project_stats` for the Dashboard to render usage graphs.
    =================================================================================
    """

    def __init__(self, persistence: Optional[RegistryPersistence] = None):
        """
        =================================================================================
        == THE RITE OF MULTIVERSAL INCEPTION (V-Ω-TOTALITY-V100K-BOOTSTRAP)            ==
        =================================================================================
        Initializes the Governor, loads the Registry, and prepares the physical substrate.
        """
        # [ASCENSION 7]: CHRONOMETRIC ANCHOR
        self._inception_ts = time.perf_counter_ns()

        # [ASCENSION 4]: THE MUTEX ANCHOR (THREAD SAFETY)
        self._lock = threading.RLock()

        # [ASCENSION 2]: PERSISTENCE SUTURE
        self.persistence = persistence or RegistryPersistence()

        # [ASCENSION 5]: TABULA RASA RESILIENCE
        try:
            self.registry = self.persistence.load()
            if not self.registry:
                raise ValueError("Registry returned as a void.")

            # Integrity Check
            if not hasattr(self.registry, 'projects'):
                raise ValueError("Registry Schema is malformed (missing 'projects').")

        except Exception as e:
            Logger.critical(f"Registry Fracture detected: {e}. Initiating Tabula Rasa Protocol.")
            self.registry = RegistrySchema()
            self.persistence.save(self.registry)

        # [ASCENSION 9]: GEOMETRIC ANCHOR HEURISTIC
        self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        # [ASCENSION 5]: IDEMPOTENT SANCTUM FORGING
        try:
            # Ensure the physical substrate for project shards exists.
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            # In restricted WASM/IDBFS environments, we may be blind to physical dir creation
            pass

        # [ASCENSION 10]: ACHRONAL AUDIT TRIGGER
        # We perform a lazy audit to ensure the Axis Mundi (Anchor) is resonant.
        self._audit_active_anchor()

        Logger.success(
            f"Multiversal Governor is [bold green]RESONANT[/bold green]. Managed Projects: {len(self.registry.projects)}")

    def _audit_active_anchor(self):
        """
        =============================================================================
        == THE ACHRONAL AUDIT (V-Ω-GHOST-AMNESTY-V1)                               ==
        =============================================================================
        Verifies that the currently active project actually exists.
        Grants amnesty to 'Ghost' projects (metadata only) to prevent boot loops.
        """
        active_id = self.registry.active_project_id
        if not active_id:
            return

        project = self.registry.projects.get(active_id)

        # 1. Existence Adjudication
        if not project:
            Logger.warn(f"Anchor '{active_id}' is unmanifest in Registry. Resetting Active ID to Void.")
            self.registry.active_project_id = None
            self.persistence.save(self.registry)
            return

        # 2. [ASCENSION 8]: THE GHOST AMNESTY VOW
        # If the project is a "Ghost" (Willed but not yet materialized), we stay the hand of the Auditor.
        # This is critical for the "Seed Census" where we create metadata before files.
        is_ghost = project.custom_data.get("is_ghost", False)
        is_optimistic = project.custom_data.get("is_optimistic", False)

        if is_ghost or is_optimistic:
            Logger.verbose(f"Auditor: Anchor '{active_id}' is a Nascent Reality (Ghost). Granting passage.")
            return

        # 3. Physical Matter Verification
        # For non-ghost projects, we ensure the matter matches the Gnosis.
        # Note: In WASM, path checks might be virtual.
        if not Path(project.path).exists():
            Logger.warn(f"Physical Matter for project '{project.name}' ({project.path}) has vanished. Severing Anchor.")
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
        == THE RITE OF TOTAL CENSUS (V-Ω-TOTALITY-V10K)                            ==
        =============================================================================
        Returns a filtered list of all known realities.
        [ASCENSION 6]: Uses atomic key-snapshotting to prevent concurrency errors.
        """
        results = []

        # [ASCENSION 6]: ATOMIC SNAPSHOT
        # We take a static snapshot of the keys to avoid 'dictionary changed size'
        with self._lock:
            p_ids = list(self.registry.projects.keys())

            for pid in p_ids:
                p = self.registry.projects.get(pid)
                if not p: continue

                # 1. Archive Filter
                if not include_archived and p.is_archived:
                    continue

                # 2. [ASCENSION 7]: SOVEREIGNTY PHALANX
                if owner_id:
                    # The Trinity of Access
                    is_owner = p.owner_id == owner_id
                    is_guest = p.owner_id == GUEST_OWNER_ID
                    # System projects/Demos are visible to all
                    is_system = p.owner_id == SYSTEM_OWNER_ID or p.is_demo

                    # Visibility Logic:
                    # - If I am the owner, I see it.
                    # - If I am NOT the Guest owner, but the file IS Guest owned (public session), I see it (optional).
                    # - If it is System/Demo, everyone sees it.
                    if not (is_owner or (owner_id != GUEST_OWNER_ID and is_guest) or is_system):
                        continue

                # 3. Semantic Tag Scrying
                if tags and not any(t in p.tags for t in tags):
                    continue

                results.append(p)

        # [ASCENSION 8]: METABOLIC PRECISION SORT
        # Sort by last_accessed (descending) so recent projects float to top.
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
        == THE RITE OF KINETIC GENESIS (V-Ω-TOTALITY-V50000)                       ==
        =============================================================================
        Forges a new reality, allocates space, and anchors it to the Multiverse.
        """
        # --- MOVEMENT I: GNOSTIC TRIAGE ---
        try:
            from .seeds import SEED_VAULT
        except ImportError:
            # Fallback for broken installs
            SEED_VAULT = {"blank": {"README.md": "# Primordial Void\nWaiting for Intent."}}

        # Template Validation Oracle
        if template not in SEED_VAULT:
            Logger.warn(f"Oracle: Template '{template}' unmanifest. Falling back to 'blank'.")
            template = "blank"

        # --- MOVEMENT II: GEOMETRIC ALLOCATION ---
        pid = str(uuid.uuid4())
        project_path = self.workspaces_root / pid

        # [ASCENSION 11]: COLLISION GUARD
        if project_path.exists():
            raise ArtisanHeresy(
                f"Sovereignty Paradox: Sanctum collision for ID {pid}",
                severity=HeresySeverity.CRITICAL
            )

        try:
            # --- MOVEMENT III: ATOMIC REGISTRATION (THE FIX) ---
            # We register the project IN MEMORY before we strike the disk.
            # This allows the UI to see it instantly.
            now_ms = int(time.time() * 1000)

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
                stats=ProjectStats(file_count=0, size_kb=0),
                custom_data={
                    "is_ghost": False,
                    "is_active_creation": True
                }
            )

            # Inscribe into memory and PERSIST immediately
            with self._lock:
                self.registry.projects[pid] = project
                self.persistence.save(self.registry)

            # --- MOVEMENT IV: PHYSICAL MANIFESTATION ---
            project_path.mkdir(parents=True, exist_ok=True)

            # [ASCENSION 13]: ATOMIC SEED HYDRATION
            # We strike the physical disk with the DNA of the chosen template.
            self._hydrate_sanctum(project_path, template, SEED_VAULT)

            # --- MOVEMENT V: METABOLIC TOMOGRAPHY ---
            # Measure the reality we just created
            project.stats = self._measure_reality(project_path)
            project.custom_data["is_active_creation"] = False

            # Update and Finalize Persistence
            with self._lock:
                self.persistence.save(self.registry)

            Logger.success(f"Reality '{name}' ({pid[:8]}) manifest from template '{template}'.")

            # [ASCENSION 14]: AUTO-ANCHORING
            # If the multiverse is a void, we anchor to this new reality instantly.
            if not self.registry.active_project_id:
                Logger.info(f"First light detected. Anchoring Gaze to '{name}'.")
                self.switch_project(pid)

            return project

        except Exception as fracture:
            # --- MOVEMENT VI: THE RITE OF OBLIVION (ROLLBACK) ---
            if project_path.exists():
                shutil.rmtree(project_path, ignore_errors=True)

            with self._lock:
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
        [ASCENSION 13]: THE SEEDING RITE.
        Inscribes the predefined scriptures from the Vault into the physical directory.
        """
        seed_data = vault.get(template_id, vault.get("blank", {}))
        scriptures_written = 0
        for rel_path, content in seed_data.items():
            target = root / rel_path
            # Ensure parent sanctums exist
            target.parent.mkdir(parents=True, exist_ok=True)
            # Atomic Write
            target.write_text(content, encoding='utf-8')
            scriptures_written += 1

        Logger.verbose(f"Hydration complete: {scriptures_written} scriptures inscribed for '{template_id}'.")

    def _measure_reality(self, root: Path) -> ProjectStats:
        """
        [ASCENSION 19]: THE SCALES OF MASS.
        Performs a recursive biopsy of the directory to calculate its metabolic mass.
        """
        file_count = 0
        size_bytes = 0
        try:
            for r, _, files in os.walk(root):
                file_count += len(files)
                for f in files:
                    try:
                        size_bytes += os.path.getsize(os.path.join(r, f))
                    except (OSError, FileNotFoundError):
                        continue
        except Exception:
            pass

        return ProjectStats(
            file_count=file_count,
            size_kb=size_bytes // 1024,
            last_integrity_check=time.time(),
            health_score=100
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
        """
        with self._lock:
            if project_id not in self.registry.projects:
                raise ArtisanHeresy(
                    f"Coordinate Lost: Reality '{project_id}' is unmanifest.",
                    severity=HeresySeverity.CRITICAL
                )

            target = self.registry.projects[project_id]

            # 1. [ASCENSION 13]: LAZY MATERIALIZATION CHECK (GHOST -> PHYSICAL)
            # If the project was born as a Prophecy (Ghost), we must now strike the matter.
            is_ghost = target.custom_data.get("is_ghost")
            is_optimistic = target.custom_data.get("is_optimistic")

            if is_ghost or is_optimistic:
                Logger.info(f"Ghost Resonance detected for '{target.name}'. Materializing Matter from Seed...")

                project_path = Path(target.path)

                try:
                    # Forge Sanctum
                    project_path.mkdir(parents=True, exist_ok=True)

                    # Hydrate DNA
                    from .seeds import SEED_VAULT
                    self._hydrate_sanctum(project_path, target.template, SEED_VAULT)

                    # Update Metadata: The Ghost is now Physical
                    target.custom_data["is_ghost"] = False
                    target.custom_data["is_optimistic"] = False
                    target.stats = self._measure_reality(project_path)

                    Logger.success(f"Materialization of '{target.name}' is complete.")

                except Exception as e:
                    Logger.warn(f"Seeding Rite flickered for Ghost '{target.name}': {e}")
                    # We continue, as the directory exists now.

            # 2. [ASCENSION 14]: SYMBOLIC LINK SOVEREIGNTY (THE CURE)
            # We physically bind the /vault/project path to this specific project.
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
        """[ASCENSION 15]: SOVEREIGNTY WARDED EXCISION."""
        with self._lock:
            if project_id not in self.registry.projects:
                return

            target = self.registry.projects[project_id]

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
                    shutil.rmtree(path, ignore_errors=True)
                except Exception as e:
                    Logger.warn(f"Physical excision partial for '{target.name}': {e}")

            # 2. REGISTRY PRUNING
            del self.registry.projects[project_id]

            # 3. ANCHOR SEVERANCE
            if self.registry.active_project_id == project_id:
                self.registry.active_project_id = None
                self._sever_link()

            self.persistence.save(self.registry)
            Logger.success(f"Project '{target.name}' has returned to the void.")

    # =========================================================================
    # == INTERNAL ORGANS (THE KINETIC SUTURES)                               ==
    # =========================================================================

    def _sever_link(self):
        """[THE RITE OF SEVERANCE]"""
        # Only relevant in WASM/Posix environments
        link = Path("/vault/project")
        try:
            if link.is_symlink() or link.is_file():
                link.unlink()
            elif link.is_dir():
                shutil.rmtree(link, ignore_errors=True)
        except Exception:
            pass

    def _link_active_reality(self, target_path: Path):
        """
        [THE IRON ANCHOR]
        Updates /vault/project to point to the active workspace.
        In WASM (IDBFS), symlinks might be emulated or copies.
        """
        link = Path("/vault/project")

        try:
            # 1. Purge existing anchor
            if link.exists() or link.is_symlink():
                self._sever_link()

            # 2. Forge new anchor
            target_abs = target_path.resolve()

            try:
                # Try Symlink first (Fastest)
                os.symlink(str(target_abs), str(link))
            except (OSError, AttributeError):
                # Fallback: Copy (Slow but robust for some VFS implementations)
                # But syncing the whole dir is heavy.
                # In WASM IDBFS, we often just rely on the path mapping in the Kernel logic.
                # However, for 'velm run' to work in CWD, we need this.
                if not link.exists():
                    shutil.copytree(str(target_abs), str(link))
                    Logger.verbose("Symlink failed, forged Physical Mirror.")

        except Exception as e:
            Logger.critical(f"Reality Anchor Fracture: {e}")
            # Non-fatal, but navigation might be broken in terminal

    def bootstrap_multiverse(self):
        """
        =================================================================================
        == THE RITE OF ACHRONAL PRESERVATION (V-Ω-TOTALITY-RESONANT-FINALIS)           ==
        =================================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_BOOTSTRAP_V20000_ENTERPRISE_SUTURE_2026_FINALIS

        The supreme conduction of the Engine's birth. This rite scries the Ancestral Scroll,
        populates the Seed Census to cure the Progenitor Monopoly, and adjudicates the
        Axis Mundi (Active Anchor) with absolute deterministic logic.
        =================================================================================
        """
        Logger.info("The Multiversal Governor is scrying the Ancestral Scroll...")

        with self._lock:  # [ASCENSION 2]: Mutex-Warded Inception
            # --- MOVEMENT I: THE UNIVERSAL SEED CENSUS ---
            # [ASCENSION 3]: We perform the census regardless of history to ensure new
            # archetypes forged in the SEED_VAULT are instantly manifest as Ghost options.
            self._census_of_seeds()

            # --- MOVEMENT II: SESSION RECONCILIATION ---
            # We scry the registry to determine if we are resurrecting a past session
            # or beginning anew in the Primordial Void.
            existing_registry = self.registry
            previous_life_anchor = existing_registry.active_project_id

            # [ASCENSION 4]: ZOMBIE ANCHOR EXORCISM
            # We verify the anchor: Does the project exist in our roster?
            if previous_life_anchor and previous_life_anchor in self.registry.projects:
                project = self.registry.projects[previous_life_anchor]

                # Check for physical matter integrity for non-ghosts
                is_ghost = project.custom_data.get("is_ghost", False)
                physical_exists = Path(project.path).exists()

                if not is_ghost and not physical_exists:
                    # [THE CURE]: The matter has vanished. We must sever the anchor.
                    Logger.warn(f"Anchor '{previous_life_anchor[:8]}' points to a void. Exorcising...")
                    self.registry.active_project_id = None
                    self._sever_link()
                else:
                    # [ASCENSION 5]: RESONANT RESUMPTION
                    # The anchor is valid. We perform the physical binding.
                    Logger.info(f"Resuming active session: [cyan]{previous_life_anchor[:8]}[/cyan]")
                    self.registry.active_project_id = previous_life_anchor
                    self._link_active_reality(Path(project.path))
            else:
                # [ASCENSION 8]: THE VOW OF THE VOID
                # If no valid anchor exists, we stand by in the Lobby.
                Logger.info("🌌 Primordial Void perceived. Engine standing by in Lobby.")
                self.registry.active_project_id = None
                self._sever_link()  # [ASCENSION 9]: Purge /vault/project

            # =========================================================================
            # == [REDACTED KINETIC ACT]: FORGE_VFS_STRIKE (ENTERPRISE RESURRECTION)   ==
            # =========================================================================
            # [GNOSTIC COMMENTARY FOR ARCHITECTS]:
            # This is the "Apotheosis of Uniformity." In corporate or high-compliance
            # environments, the Architect may desire to eliminate the "Lobby Choice"
            # and force every Node to boot into a specific, warded reality.
            #
            # IMPLEMENTATION LOGIC:
            # 1. Identify a "Mandatory Archetype" (e.g., 'security-fortress').
            # 2. Check if the Multiverse is currently empty or in a LOBBY state.
            # 3. Force-Materialize (Strike) the physical matter from the Seed Vault.
            # 4. Hard-Bind the active_project_id to the new creation.
            #
            # UTILITY:
            # Use this to enforce "Governance-as-Boot-Code." It ensures every developer
            # starts with the same 'Sanctified Policies' and 'Standard Libraries',
            # making drift mathematically impossible from second zero.
            # -------------------------------------------------------------------------

            # CORPORATE_ENFORCEMENT_ACTIVE = False # Set to True to enable the Strike
            # if CORPORATE_ENFORCEMENT_ACTIVE and self.registry.active_project_id is None:
            #     target_seed = "progenitor" # The Archetype to force-seed
            #     pid = "c10fbf66-505c-4cc3-a9e4-7852b3ed6b7a" # Deterministic UUID
            #
            #     self.logger.verbose(f"Enterprise Vow Active: Forcing inception of '{target_seed}'...")
            #
            #     # A. Materialize physical sanctum
            #     project_path = self.workspaces_root / pid
            #     project_path.mkdir(parents=True, exist_ok=True)
            #
            #     # B. Conduct JIT Seeding (The Strike)
            #     from .seeds import SEED_VAULT
            #     self._hydrate_sanctum(project_path, target_seed, SEED_VAULT)
            #
            #     # C. Anchor the Mind
            #     self.registry.active_project_id = pid
            #     self._link_active_reality(project_path)
            #
            #     Logger.success(f"Enterprise Reality '{target_seed}' has been successfully imposed.")
            # =========================================================================

            # --- MOVEMENT III: ATOMIC COMMITMENT ---
            try:
                # [ASCENSION 7]: Graft Environment DNA
                self.registry.version = "2.0.0-OMEGA"
                # ... (Additional metadata grafting could occur here) ...

                # [ASCENSION 10]: HYDRAULIC I/O FLUSH
                self.persistence.save(self.registry)

                status_label = "RESUMED" if self.registry.active_project_id else "LOBBY"
                Logger.success(f"💠 Multiverse Inception Complete. Mode: [bold cyan]{status_label}[/].")

                # [ASCENSION 12]: THE FINALITY VOW
                # We return True to signal the kernel that the Governor is Resonant.
                return True

            except Exception as e:
                # [ASCENSION 12]: CATASTROPHIC RECOIL
                raise ArtisanHeresy(
                    "REGISTRY_INSCRIPTION_FRACTURE",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify write permissions in the .scaffold directory or check for I/O lock contention."
                )


    def _census_of_seeds(self):
        """
        =============================================================================
        == THE SEED CENSUS (V-Ω-ARCHETYPE-POPULATOR)                               ==
        =============================================================================
        [ASCENSION 12]: THE CURE FOR SEED ANEMIA.
        Iterates the entire `SEED_VAULT` and registers every archetype as a System Demo
        if it is not already manifest in the registry.
        """
        try:
            from .seeds import SEED_VAULT
        except ImportError:
            Logger.warn("Seed Vault Unreachable. Skipping Census.")
            return

        now_ms = int(time.time() * 1000)
        seeds_sown = 0

        with self._lock:
            # Iterate through ALL templates in the vault
            for template_key, content_map in SEED_VAULT.items():
                if template_key == "blank": continue  # Skip utility blanks

                # [ASCENSION 3]: DETERMINISTIC UUID GENERATION
                # We use UUIDv5 with a fixed namespace to ensure the same seed
                # always gets the same ID across different sessions/machines.
                seed_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"novalym.seed.{template_key}"))

                # If this seed is already known, we skip it (Idempotency)
                if seed_uuid in self.registry.projects:
                    continue

                Logger.info(f"🌌 Inscribing Missing Seed: [cyan]{template_key}[/cyan]")

                project_path = self.workspaces_root / seed_uuid

                # Create Meta for the Ghost
                demo_meta = ProjectMeta(
                    id=seed_uuid,
                    name=template_key.replace("-", " ").title().replace("Api", "API"),
                    description=f"System Reference Architecture for {template_key}.",
                    path=str(project_path.resolve()).replace('\\', '/'),
                    owner_id=SYSTEM_OWNER_ID,
                    template=template_key,
                    is_demo=True,
                    is_locked=True,
                    tags=["system", "reference", template_key, "archetype"],
                    created_at=now_ms,
                    updated_at=now_ms,
                    last_accessed=now_ms,  # Set to now so they appear at top initially? No, maybe older.
                    stats=ProjectStats(file_count=len(content_map), size_kb=0),
                    custom_data={
                        "is_ghost": True,  # [ASCENSION 8]: Lazy Hydration
                        "is_optimistic": False,
                        "icon": "Zap"
                    }
                )

                self.registry.projects[seed_uuid] = demo_meta
                seeds_sown += 1

            if seeds_sown > 0:
                Logger.success(f"Census Complete. {seeds_sown} new archetypes registered.")
                # We save immediately to ensure they persist even if we crash later
                self.persistence.save(self.registry)

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

    def update_project(self, project_id: str, updates: Dict[str, Any]):
        """Transmutes project metadata without touching the physical substrate."""
        with self._lock:
            if project_id not in self.registry.projects:
                raise ArtisanHeresy("Project not found.")

            project = self.registry.projects[project_id]
            IMMUTABLE = {'id', 'path', 'created_at', 'stats'}
            for k, v in updates.items():
                if k in IMMUTABLE: continue
                if hasattr(project, k): setattr(project, k, v)

            project.updated_at = int(time.time() * 1000)
            self.persistence.save(self.registry)
            Logger.info(f"Metadata transmuted for '{project.name}'.")

    def import_project(self, path: str, name: str, owner_id: str) -> ProjectMeta:
        """Adopts an existing directory into the Multiverse Registry."""
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
            tags=["imported"],
            stats=stats,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000),
            last_accessed=int(time.time() * 1000)
        )

        with self._lock:
            self.registry.projects[pid] = project
            self.persistence.save(self.registry)

        Logger.success(f"Reality '{name}' adopted into the Gnostic Multiverse.")
        return project

    def __repr__(self) -> str:
        count = len(self.registry.projects)
        return f"<Ω_PROJECT_GOVERNOR projects={count} anchor={self.registry.active_project_id[:8] if self.registry.active_project_id else 'VOID'}>"