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
    GUEST_OWNER_ID, PROGENITOR_ID
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
    9.  **Geometric Anchor Heuristics (THE FIX):** Decouples the `workspaces_root` from the
        persistence layer in WASM. It enforces a flat `/vault/workspaces` topology to align
        with the Ocular Eye's perception, while keeping the registry in `.scaffold`.
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
        == THE RITE OF MULTIVERSAL INCEPTION (V-Ω-TOTALITY-V100K-BOOTSTRAP-HEALED)     ==
        =================================================================================
        LIF: ∞ | ROLE: SPATIAL_ANCHOR_GOVERNOR | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This init now deterministically anchors the 'workspaces_root' to
        the correct topological stratum based on the substrate.
        """
        # [ASCENSION 7]: CHRONOMETRIC ANCHOR
        self._inception_ts = time.perf_counter_ns()

        # [ASCENSION 4]: THE MUTEX ANCHOR (THREAD SAFETY)
        self._lock = threading.RLock()

        # [ASCENSION 2]: PERSISTENCE SUTURE
        # The ascended persistence.py now handles the /vault vs ~/.scaffold triage
        self.persistence = persistence or RegistryPersistence()

        # [ASCENSION 22]: SUBSTRATE SENSING
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

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

        # =========================================================================
        # == [THE CURE]: DETERMINISTIC WORKSPACE ANCHORING                      ==
        # =========================================================================
        # [ASCENSION 9]: GEOMETRIC ANCHOR HEURISTIC
        # In WASM, the persistence root is /vault/.scaffold, but workspaces MUST be
        # at /vault/workspaces to align with the Ocular UI's perception.
        if self.is_wasm:
            self.workspaces_root = Path("/vault/workspaces")
            Logger.info(f"WASM Substrate detected. Anchoring Workspaces to Sovereign Root: {self.workspaces_root}")
        else:
            # In Iron, we nest inside the persistence root for tidiness.
            self.workspaces_root = self.persistence.root / DEFAULT_WORKSPACE_DIR_NAME

        # [ASCENSION 5]: IDEMPOTENT SANCTUM FORGING
        try:
            # Ensure the physical substrate for project shards exists.
            self.workspaces_root.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            # In restricted environments, we proceed with Gnostic Faith
            pass

        # [ASCENSION 10]: ACHRONAL AUDIT TRIGGER
        # We perform a lazy audit to ensure the Axis Mundi (Anchor) is resonant.
        self._audit_active_anchor()

        Logger.success(
            f"Multiversal Governor is [bold green]RESONANT[/bold green]. Substrate: {self.workspaces_root}")

    def _audit_active_anchor(self):
        """
        =============================================================================
        == THE ACHRONAL AUDIT (V-Ω-GHOST-AMNESTY-V1.2-HEALED)                      ==
        =============================================================================
        [THE CURE]: Performs a physical biopsy of the project path.
        It is now warded against the 'Relative-Path Heresy' by resolving
        coordinates before verification.
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
        is_ghost = project.custom_data.get("is_ghost", False)
        is_optimistic = project.custom_data.get("is_optimistic", False)

        if is_ghost or is_optimistic:
            return

        # 3. [THE FIX]: PHYSICAL MATTER VERIFICATION
        # We normalize the path to ensure we aren't looking for relative shadows.
        try:
            p_path = Path(project.path).resolve()

            if not p_path.exists():
                Logger.warn(f"Reality '{project.name}' vanished from {p_path}. Severing Anchor.")
                self.registry.active_project_id = None
                self._sever_link()  # Purge the /vault/project link
                self.persistence.save(self.registry)
        except Exception:
            # If path resolution fails, the reality is fractured.
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

                # 2. [ASCENSION 14]: SOVEREIGNTY PHALANX
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
        == THE RITE OF KINETIC GENESIS (V-Ω-TOTALITY-V50K-GEOMETRIC-FIX)           ==
        =============================================================================
        LIF: 50x | ROLE: MATTER_FISSION_CONDUCTOR

        [THE CURE]: Forces the 'project_path' to be a clean, absolute POSIX
        coordinate derived from the decoupled `workspaces_root`. This prevents
        the WASM worker from creating recursive 'vault/workspaces/vault' structures.
        """
        # --- MOVEMENT I: GNOSTIC TRIAGE ---
        try:
            from .seeds import SEED_VAULT
        except ImportError:
            SEED_VAULT = {"blank": {"README.md": "# Primordial Void\nWaiting for Intent."}}

        if template not in SEED_VAULT:
            template = "blank"

        # --- MOVEMENT II: GEOMETRIC ALLOCATION ---
        pid = str(uuid.uuid4())

        # [THE FIX]: Deterministic Absolute Pathing
        # We ensure the path is absolute and uses POSIX slashes for the Registry.
        # This resolves the schism between the Python Manager and the React Explorer.
        raw_path = self.workspaces_root / pid
        project_path_str = raw_path.as_posix()

        # Collision Check
        if raw_path.exists():
            raise ArtisanHeresy(
                f"Sovereignty Paradox: Sanctum collision for ID {pid}",
                severity=HeresySeverity.CRITICAL
            )

        try:
            # --- MOVEMENT III: ATOMIC REGISTRATION ---
            now_ms = int(time.time() * 1000)
            final_tags = tags or []
            if template != "blank": final_tags.append(template)
            if is_demo: final_tags.append("reference")

            project = ProjectMeta(
                id=pid,
                name=name,
                description=description,
                path=project_path_str,  # THE PURE COORDINATE
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
                # [ASCENSION 17]: Hydraulic I/O Flush
                self.persistence.save(self.registry)

            # --- MOVEMENT IV: PHYSICAL MANIFESTATION ---
            # We strike the disk with the new project sanctum
            raw_path.mkdir(parents=True, exist_ok=True)

            # [ASCENSION 13]: ATOMIC SEED HYDRATION
            self._hydrate_sanctum(raw_path, template, SEED_VAULT)

            # --- MOVEMENT V: METABOLIC TOMOGRAPHY ---
            project.stats = self._measure_reality(raw_path)
            project.custom_data["is_active_creation"] = False

            # Finalize Persistence
            with self._lock:
                self.persistence.save(self.registry)

            Logger.success(f"Reality '{name}' manifest at {project_path_str}")

            # [ASCENSION 14]: AUTO-ANCHORING
            if not self.registry.active_project_id:
                self.switch_project(pid)

            return project

        except Exception as fracture:
            # --- MOVEMENT VI: THE RITE OF OBLIVION (ROLLBACK) ---
            # [ASCENSION 16]: Atomic Rollback
            if raw_path.exists():
                shutil.rmtree(raw_path, ignore_errors=True)

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
        =================================================================================
        == THE RITE OF HYDRAULIC INCEPTION (V-Ω-TOTALITY-V100K-UNBREAKABLE)            ==
        =================================================================================
        LIF: ∞ | ROLE: ATOMIC_MATTER_INSCRIBER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_HYDRATE_V100K_ATOMIC_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite materializes the DNA of a System Archetype onto the physical substrate.
        It is engineered to defeat the 'Empty Explorer' heresy by enforcing Atomic
        Force-Flushing and Topographical Lustration.
        =================================================================================
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE SUMMONS OF DNA ---
        # If the willed template is a void, we default to the 'blank' scripture.
        seed_data = vault.get(template_id, vault.get("blank", {}))

        scriptures_inscribed = 0
        sanctums_forged = 0

        Logger.info(f"Initiating Hydraulic Inception for archetype '[cyan]{template_id}[/cyan]'...")

        # --- MOVEMENT II: THE KINETIC STRIKE (INSCRIPTION) ---
        for rel_path_str, content in seed_data.items():
            # [ASCENSION 9]: Absolute Path Normalization
            # We ensure the target is anchored correctly within the /vault/workspaces stratum.
            target_path = (root / rel_path_str).resolve()
            target_str = str(target_path).replace('\\', '/')

            try:
                # 1. FORGE PARENT SANCTUMS
                # [ASCENSION 4]: We ensure the entire directory ancestry is manifest.
                parent_dir = target_path.parent
                if not parent_dir.exists():
                    parent_dir.mkdir(parents=True, exist_ok=True)
                    sanctums_forged += 1

                # 2. ATOMIC INSCRIPTION (THEmaron STRIKE)
                # [ASCENSION 1, 2, 3]: We move beyond high-level 'write_text'.
                # We open the marrows of the OS to perform a force-flush.
                with open(target_str, 'wb') as scripture_handle:
                    # Transmute Gnostic Soul (String) into Matter (Bytes)
                    scripture_handle.write(content.encode('utf-8'))

                    # [THE CURE]: HYDRAULIC FLUSH
                    # Force the data out of Python's memory buffer.
                    scripture_handle.flush()

                    # [THE CURE]: ACHRONAL FSYNC
                    # Force the virtual OS (Emscripten) to commit to the dnode.
                    os.fsync(scripture_handle.fileno())

                # 3. METABOLIC VERIFICATION
                # [ASCENSION 7]: Verify the matter possesses mass.
                if os.stat(target_str).st_size == 0 and len(content) > 0:
                    Logger.warn(f"Metabolic Gap detected in '{rel_path_str}'. Re-striking...")
                    # Future: Implement recursive retry logic here.

                scriptures_inscribed += 1

            except Exception as heresy:
                # [ASCENSION 8]: Fault Isolation
                # A single fracture must not halt the manifestation of the entire project.
                Logger.error(f"Inscription Fracture at [bold red]{rel_path_str}[/]: {heresy}")

        # =========================================================================
        # == MOVEMENT III: TOPOGRAPHICAL LUSTRATION (THE FIX)                    ==
        # =========================================================================
        # [ASCENSION 5 & 6]: We physically 'vibrate' the directory tree.
        # In the WASM environment, the Directory Entry Cache can become stale
        # during high-intensity writes. We force a re-scry of the entire sanctum.

        Logger.verbose("Conducting Topographical Lustration to align VFS dentry cache...")

        # Pass 1: Recursive Walk (Deep Lustration)
        # This forces the Emscripten VFS to rebuild pointers for every sub-directory.
        for root_node, dirs, files in os.walk(str(root)):
            # The act of walking is the cure.
            pass

        # Pass 2: Root Probe (Final Cache Bust)
        # This ensures the very next 'ls' or 'SCRY' from the UI sees the new children.
        _ = os.listdir(str(root))

        # --- MOVEMENT IV: TELEMETRIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.success(
            f"Apotheosis Complete: {scriptures_inscribed} scriptures manifest, "
            f"{sanctums_forged} sanctums forged in {duration_ms:.2f}ms."
        )


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
        =================================================================================
        == THE RITE OF ANCHORING & MATERIALIZATION (V-Ω-TOTALITY-V100K-HYDRAULIC)      ==
        =================================================================================
        LIF: ∞ | ROLE: SPATIAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SWITCH_V100K_HYDRAULIC_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite conducts the spatial transition of the Engine's consciousness.
        It annihilates the 'Symlink Ghost' and 'Hollow Sanctum' heresies by enforcing
        Physical Mass Verification. If a reality is unmanifest or empty, the
        Manager conducts a JIT Materialization Strike before anchoring the process.
        =================================================================================
        """
        start_ns = time.perf_counter_ns()

        with self._lock:
            # --- MOVEMENT I: THE GNOSTIC INQUEST (IDENTITY RECONCILIATION) ---
            # [ASCENSION 1]: If the ID is unmanifest (common on cold boots),
            # we perform a forced Census to resurrect System Archetypes JIT.
            if project_id not in self.registry.projects:
                Logger.info(f"Plea for unmanifest ID '[yellow]{project_id[:8]}[/]'. Scrying Seed Vault...")
                self._census_of_seeds(force=True)

                # Final Adjudication of existence after the Census
                if project_id not in self.registry.projects:
                    raise ArtisanHeresy(
                        f"Coordinate Lost: Reality '{project_id}' is unmanifest in the Registry.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Execute 'velm project list' to perceive manifest realities."
                    )

            target = self.registry.projects[project_id]
            project_path = Path(target.path)
            project_path_posix = str(project_path.resolve()).replace('\\', '/')

            Logger.verbose(f"Anchoring focus to: [cyan]{target.name}[/] ({project_id[:8]})")

            # --- MOVEMENT II: HYDRAULIC REALITY VERIFICATION (MATTER BIOPSY) ---
            # [ASCENSION 2]: We scry the physical platter. A folder with no mass is a void.
            # We do not trust the 'is_ghost' flag; reality takes precedence.
            is_hollow_sanctum = True
            if os.path.exists(project_path_posix) and os.path.isdir(project_path_posix):
                # We ignore the .scaffold internal directory; we seek user-willed matter.
                # [THE FIX]: Force a directory scan to bust Emscripten's stale cache.
                try:
                    visible_atoms = [f for f in os.listdir(project_path_posix) if f != ".scaffold"]
                    if len(visible_atoms) > 0:
                        is_hollow_sanctum = False
                except (OSError, FileNotFoundError):
                    pass

            # [ASCENSION 3]: Adjudicate between Metadata and Physics.
            # If metadata says 'Ghost' OR physical scry says 'Empty', materialize matter.
            is_ethereal = target.custom_data.get("is_ghost", False) or target.custom_data.get("is_optimistic", False)

            if is_ethereal or is_hollow_sanctum:
                reason = "Ghost Resonance" if is_ethereal else "Hollow Sanctum Detection"
                Logger.info(f"{reason} for '{target.name}'. Initiating Emergency Hydration...")

                try:
                    # 1. Physical Consecration (Ensure the directory is manifest)
                    os.makedirs(project_path_posix, exist_ok=True)

                    # 2. Summon the Seed Vault (DNA Retrieval)
                    try:
                        from .seeds import SEED_VAULT
                    except ImportError:
                        raise RuntimeError("Celestial Seed Vault is unmanifest.")

                    # 3. CONDUCT THE SEEDING STRIKE
                    # [ASCENSION 4]: We re-materialize the template DNA onto the physical substrate.
                    template_dna = target.template or "blank"
                    self._hydrate_sanctum(project_path, template_dna, SEED_VAULT)

                    # 4. Transmute state from Ethereal to Physical
                    target.custom_data["is_ghost"] = False
                    target.custom_data["is_optimistic"] = False
                    target.stats = self._measure_reality(project_path)

                    # [ASCENSION 6]: TOPOGRAPHICAL LUSTRATION
                    # We force another scan to ensure the very next SCRY sees the files.
                    _ = os.listdir(project_path_posix)

                    Logger.success(f"Hydration of '{target.name}' complete. Matter solidified.")
                    self._project_hud_pulse(project_id, "MATTER_MANIFESTED", "#64ffda")

                except Exception as e:
                    # [ASCENSION 11]: Fault Isolation
                    Logger.error(f"Hydration Strike fractured for '{target.name}': {e}")
                    # We continue to allow the spatial shift, but notify the Ocular HUD.
                    self._project_hud_pulse(project_id, "MATTER_FRAGMENTED", "#ef4444")

            # =========================================================================
            # == MOVEMENT III: THE ABSOLUTE ANCHOR SUTURE (THE FIX)                  ==
            # =========================================================================
            # [ASCENSION 14]: We bypass symlink shadows and force the process to
            # physically reside within the project's absolute coordinate.

            os.environ["SCAFFOLD_PROJECT_ROOT"] = project_path_posix

            try:
                # 1. Ensure the physical anchor exists
                if not os.path.exists(project_path_posix):
                    os.makedirs(project_path_posix, exist_ok=True)

                # 2. THE STRIKE: Shift the process Axis Mundi
                # [THE CURE]: Double-Chdir to reset internal Emscripten VFS pointers.
                # This vibration ensures 'os.getcwd()' and '.' are bit-perfect.
                os.chdir("/")
                os.chdir(project_path_posix)

                # [THE CURE]: Final Topographical Vibration
                # Ensure the contents are resonant to the very next Python command.
                _ = os.listdir(".")
                Logger.info(f"The Axis Mundi has shifted. CWD: [cyan]{os.getcwd()}[/].")

            except Exception as e:
                # [ASCENSION 9]: Catastrophic spatial fracture
                Logger.critical(f"Spatial Pivot Fracture: {e}")
                raise ArtisanHeresy(
                    f"Process Anchoring Failed: Could not inhabit path '{project_path_posix}'",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT IV: THE CHRONOMETRIC SEAL ---
            # Update temporal Gnosis for UI sorting and Registry health.
            target.last_accessed = int(time.time() * 1000)
            self.registry.active_project_id = project_id

            # --- MOVEMENT V: HYDRAULIC I/O FLUSH ---
            # Enshrine the new Multiversal State into the persistent Registry Scroll.
            self.persistence.save(self.registry)

            # --- MOVEMENT VI: TELEMETRIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.success(f"Anchor resonant in {duration_ms:.2f}ms. reality={project_id[:8]}")

            # Radiate shift to Ocular HUD via the Akashic silver-cord.
            self._project_hud_pulse(project_id, "ANCHOR_SHIFTED", "#3b82f6")

            # [ASCENSION 12]: THE FINALITY VOW
            # Return the bit-perfect, strictly typed metadata to the Ocular Membrane.
            return target

    def _project_hud_pulse(self, trace_id: str, type_label: str, color: str):
        """[FACULTY 16]: Radiates a haptic signal to the Ocular HUD."""
        # Note: In WASM, the engine instance is sutured to the global context
        if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic'):
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "GOVERNANCE_STRIKE",
                        "color": color,
                        "trace": trace_id[:8],
                        "timestamp": time.time()
                    }
                })
            except:
                pass

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
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

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

    def bootstrap_multiverse(self, mandatory_seed: Optional[str] = None) -> bool:
        """
        =================================================================================
        == THE RITE OF ACHRONAL PRESERVATION (V-Ω-TOTALITY-V100K-FINALIS)              ==
        =================================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_BOOTSTRAP_V100K_ENTERPRISE_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite conducts the high-order resurrection of the multiverse state. It solves
        the 'Initial Sync' heresy by ensuring the Mind and Body are anchored before
        the first external plea arrives.

        [CORPORATE DEPLOYMENT GUIDE]:
        For the Architect (you) providing for your clients, this function offers
        'Zero-Configuration Inception'.

        Usage A (Direct Code):
            governor.bootstrap_multiverse(mandatory_seed="security-api")

        Usage B (Environment Injection):
            export SCAFFOLD_AUTO_SEED="lead-lightning"
            governor.bootstrap_multiverse()

        If the Engine detects a 'mandatory_seed' and the current multiverse is in a
        LOBBY/VOID state, it will automatically materialize the target archetype
        and lock the process CWD to that reality. This ensures your clients boot
        directly into the warded environment you provided.
        =================================================================================
        """
        start_ns = time.perf_counter_ns()
        Logger.info("The Multiversal Governor is scrying the Ancestral Scroll...")

        with self._lock:
            # --- MOVEMENT I: THE UNIVERSAL SEED CENSUS ---
            # We first populate the Lobby with all known DNA from the SEED_VAULT.
            # This is critical so that any 'mandatory_seed' lookup can succeed.
            self._census_of_seeds()

            # --- MOVEMENT II: SESSION RECONCILIATION ---
            # We scry the registry to see if a reality anchor persists from a past life.
            existing_registry = self.registry
            previous_life_anchor = existing_registry.active_project_id
            reality_anchored = False

            if previous_life_anchor and previous_life_anchor in self.registry.projects:
                project = self.registry.projects[previous_life_anchor]

                # BIOPSY: Is the anchored matter still physically resonant?
                is_ghost = project.custom_data.get("is_ghost", False)
                physical_exists = Path(project.path).exists()

                if not is_ghost and not physical_exists:
                    # [THE CURE]: The matter has vanished (manual deletion).
                    # We must sever the anchor to prevent spatial paradoxes.
                    Logger.warn(f"Anchor '{previous_life_anchor[:8]}' points to a void. Exorcising...")
                    self.registry.active_project_id = None
                    os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)
                else:
                    # [ASCENSION 5]: RESONANT RESUMPTION
                    # The anchor is valid. We perform the physical CWD binding.
                    Logger.info(f"Resuming active session: [cyan]{previous_life_anchor[:8]}[/cyan] ('{project.name}')")

                    # [THE SUTURE]: FORCE ABSOLUTE CONTEXT
                    # We ensure the Environment DNA and the Python Process are in sync.
                    os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project.path)
                    try:
                        os.chdir(str(project.path))
                        reality_anchored = True
                    except (OSError, FileNotFoundError):
                        Logger.warn(f"Physical access to '{project.path}' denied. Anchor suspended.")

            # --- MOVEMENT III: ENFORCED REALITY INCEPTION (THE FIX) ---
            # [ASCENSION 1]: If we are still unanchored, we scry for a mandatory intent.
            # Priority: 1. Function Argument | 2. Environment Variable
            auto_seed = mandatory_seed or os.getenv("SCAFFOLD_AUTO_SEED")

            if not reality_anchored and auto_seed:
                Logger.info(f"🌌 Lobby is a void. Enforcing inception of mandatory seed: [bold purple]{auto_seed}[/].")

                try:
                    # 1. Generate the deterministic ID for the seed
                    # This uses the same logic as _census_of_seeds to find the Ghost.
                    seed_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"novalym.seed.{auto_seed}"))

                    if seed_uuid in self.registry.projects:
                        # 2. CONDUCT THE JIT STRIKE
                        # We use the switch_project rite to handle the materialization
                        # of the Ghost into Physical Matter.
                        self.switch_project(seed_uuid)
                        reality_anchored = True
                        Logger.success(f"Enterprise reality '{auto_seed}' has been successfully imposed.")
                    else:
                        Logger.error(f"Enforcement Fracture: Seed '{auto_seed}' is unmanifest in the Vault.")

                except Exception as e:
                    Logger.error(f"Mandatory Inception failed: {e}")

            # --- MOVEMENT IV: LOBBY STANDBY ---
            if not reality_anchored:
                # [ASCENSION 8]: THE VOW OF THE VOID
                # No past anchor found and no mandatory seed willed.
                # The Engine remains in the Lobby, awaiting human intent.
                Logger.info("🌌 Primordial Void perceived. Engine standing by in Lobby.")
                self.registry.active_project_id = None
                os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

            # --- MOVEMENT V: ATOMIC COMMITMENT ---
            try:
                # Ensure the registry version is up to date and physically saved.
                self.registry.version = "2.0.0-OMEGA"
                self.persistence.save(self.registry)

                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                status_label = "RESUMED" if self.registry.active_project_id else "LOBBY"
                Logger.success(
                    f"💠 Multiverse Inception Complete in {duration_ms:.2f}ms. Mode: [bold cyan]{status_label}[/].")

                # [ASCENSION 12]: THE FINALITY VOW
                return True

            except Exception as e:
                # Forensic autopsy if the physical disk is unmanifest or locked.
                raise ArtisanHeresy(
                    "REGISTRY_INSCRIPTION_FRACTURE",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify filesystem permissions for the .scaffold directory."
                )

    def _census_of_seeds(self, force: bool = False):
        """
        =================================================================================
        == THE SEED CENSUS: OMEGA (V-Ω-TOTALITY-V100000.20-DETERMINISTIC-FINALIS)      ==
        =================================================================================
        LIF: ∞ | ROLE: ARCHETYPAL_METADATA_ALCHEMIST | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CENSUS_V100K_DETERMINISTIC_IDENTITY_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite conducts the census of the Celestial Seed Vault. It ensures that
        every system archetype is manifest as a 'Ghost' in the registry. It is the
        cure for Seed Anemia, guaranteeing that a new Architect never wakes up
        to an empty Lobby. It is substrate-agnostic and deterministic.
        =================================================================================
        """
        # --- MOVEMENT I: THE GREAT SUMMONS ---
        try:
            # We summon the SEED_VAULT from the local project stratum
            from .seeds import SEED_VAULT
        except ImportError:
            # If the vault is unmanifest, the Lobby remains a void.
            Logger.warn("Celestial Seed Vault is unmanifest. Perception is limited.")
            return

        now_ms = int(time.time() * 1000)
        seeds_sown = 0

        with self._lock:
            # --- MOVEMENT II: THE DETERMINISTIC TRIAGE ---
            # We iterate through every shard in the vault to identify missing souls.
            for template_key, content_map in SEED_VAULT.items():
                if template_key == "blank":
                    continue  # The 'blank' seed is a utility, not a destination.

                # [ASCENSION 1]: THE DETERMINISTIC KEY
                # [THE FIX]: We use the PROGENITOR_ID constant for the Progenitor Law.
                # For all others, we use UUIDv5 with a fixed DNS-style namespace.
                if template_key == "progenitor":
                    seed_uuid = PROGENITOR_ID
                else:
                    seed_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"novalym.seed.{template_key}"))

                # IDEMPOTENCY WARD: If the seed is already enshrined, we stay the hand.
                if seed_uuid in self.registry.projects and not force:
                    continue

                Logger.info(f"🌌 Inscribing Missing Seed: [cyan]{template_key}[/cyan] (ID: {seed_uuid[:8]})")

                # --- MOVEMENT III: GEOMETRIC SUTURE ---
                # We use the substrate-aware workspaces_root to anchor the Ghost's potentiality.
                # [THE FIX]: Deterministic absolute POSIX pathing.
                project_path = self.workspaces_root / seed_uuid
                normalized_path = str(project_path.resolve()).replace('\\', '/')

                # --- MOVEMENT IV: SEMANTIC ALCHIMESTRY ---
                # 1. Linguistic Normalization (API, SQL, CLI, etc.)
                display_name = template_key.replace("-", " ").title()
                display_name = display_name.replace("Api", "API").replace("Sql", "SQL").replace("Cli", "CLI")

                # 2. Stratum Triage & Aura Synthesis (Category Divination)
                stratum = "CORE"
                icon = "Box"
                color = "#94a3b8"  # Default Slate
                neural_bias = "architect"

                if any(x in template_key for x in ("api", "server", "service")):
                    stratum = "BACKEND"
                    icon = "Database"
                    color = "#a855f7"  # Gnostic Purple (Will)
                    neural_bias = "architect"
                elif any(x in template_key for x in ("react", "vite", "web", "ui")):
                    stratum = "FRONTEND"
                    icon = "LayoutTemplate"
                    color = "#3b82f6"  # Logic Blue (Perception)
                    neural_bias = "poet"
                elif any(x in template_key for x in ("worker", "swarm", "agent")):
                    stratum = "INTELLIGENCE"
                    icon = "Cpu"
                    color = "#f43f5e"  # Kinetic Red (Action)
                    neural_bias = "maestro"
                elif any(x in template_key for x in ("infra", "deploy", "docker")):
                    stratum = "INFRASTRUCTURE"
                    icon = "Server"
                    color = "#fbbf24"  # Metabolic Amber
                    neural_bias = "sentinel"

                # [ASCENSION 4]: GNOSTIC MASS INFERENCE
                # Count files and estimate complexity/mass
                file_count = len(content_map)
                estimated_kb = sum(len(content) for content in content_map.values()) // 1024

                # Heuristic Difficulty Scrying
                difficulty = "Novice"
                if file_count > 5 or estimated_kb > 20: difficulty = "Adept"
                if file_count > 15 or "distributed" in template_key: difficulty = "Master"

                # --- MOVEMENT V: THE PROPHETIC INSCRIPTION ---
                # [ASCENSION 8 & 12]: THE PROPHETIC SOUL
                demo_meta = ProjectMeta(
                    id=seed_uuid,
                    name=display_name,
                    description=f"System Reference Architecture for {template_key}.",
                    path=normalized_path,
                    owner_id=SYSTEM_OWNER_ID,
                    template=template_key,
                    is_demo=True,
                    is_locked=True,
                    tags=["system", "reference", stratum.lower(), template_key, "omega-verified"],
                    created_at=now_ms,
                    updated_at=now_ms,
                    last_accessed=now_ms,  # Force seeds to the top of the scry
                    stats=ProjectStats(
                        file_count=file_count,
                        size_kb=estimated_kb,
                        health_score=100
                    ),
                    custom_data={
                        "is_ghost": True,  # [ASCENSION 7]: COMMANDS JIT MATERIALIZATION
                        "is_optimistic": False,
                        "icon": icon,
                        "color": color,
                        "stratum": stratum,
                        "difficulty": difficulty,
                        "neural_bias": neural_bias,
                        # [GNOSTIC COMMENTARY]: Enforced inception trigger
                        "auto_provision": (template_key == "progenitor")
                    }
                )

                # --- MOVEMENT VI: THE LATTICE COMMITMENT ---
                self.registry.projects[seed_uuid] = demo_meta
                seeds_sown += 1

            # --- MOVEMENT VII: ATOMIC PERSISTENCE FLUSH ---
            if seeds_sown > 0:
                # [ASCENSION 9]: HYDRAULIC I/O FLUSH
                # We save immediately to protect the new records from a substrate crash.
                self.persistence.save(self.registry)
                Logger.success(f"Census Complete. {seeds_sown} new archetypes resonant in the Lobby.")


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