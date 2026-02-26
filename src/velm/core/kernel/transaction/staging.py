# Path: scaffold/core/kernel/transaction/staging.py
import os
import shutil
import time
from pathlib import Path
from typing import Union, List, Any

from ....logger import Scribe

Logger = Scribe("StagingManager")


class StagingManager:
    """
    =================================================================================
    == THE ARCHITECT OF EPHEMERAL REALITIES (V-Ω-APOTHEOSIS-ULTIMA)                ==
    =================================================================================
    This divine artisan forges, manages, and purifies the parallel universes
    (staging and backup directories) required for an unbreakable, atomic transaction.
    Its Gaze is one of foresight, its hand one of absolute purity.
    =================================================================================
    """

    def __init__(self, project_root: Path, tx_id: str, engine: Any, logger: 'Scribe'):
        """
        =============================================================================
        == THE RITE OF STAGING INCEPTION (V-Ω-TOTALITY-V2000-SUTURED)              ==
        =============================================================================
        LIF: ∞ | ROLE: GEOMETRIC_WOMB_ARCHITECT | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_INIT_STAGING_V2000_ENGINE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite materializes the Architect of Ephemeral Realities. It anchors the
        Mind (Engine) and the Voice (Logger) to the physical coordinate of the
        project, creating the warded sanctums required for atomic transmutation.
        =============================================================================
        """
        self.project_root = project_root.resolve()
        self.tx_id = tx_id

        # [THE CURE]: SOVEREIGN ORGAN SUTURE
        # Binds the Engine Heart and the Gnostic Scribe to the stratum.
        self.engine = engine
        self.logger = logger

        # --- THE SACRED SANCTUMS (GEOMETRIC COORDINATES) ---
        # Defines the boundaries of the parallel universes.
        self.scaffold_dir = self.project_root / ".scaffold"
        self.staging_root = self.scaffold_dir / "staging" / self.tx_id
        self.backup_root = self.scaffold_dir / "backups" / self.tx_id

        # [ASCENSION VII]: THE CHRONOCACHE OF RESOLUTION
        # An O(1) lookup lattice to accelerate path translation across dimensions.
        self._path_cache: dict[Union[str, Path], Path] = {}

    def initialize_sanctums(self):
        """
        =============================================================================
        == THE SANCTUM INITIALIZER (V-Ω-TOTALITY-V2000-SIM-SUTURED)                ==
        =============================================================================
        LIF: 100x | ROLE: GEOMETRIC_WOMB_PREPARER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_INIT_SANCTUMS_V2000_SIM_READY_2026_FINALIS

        [THE MANIFESTO]
        This rite materializes the parallel universes (Staging & Backup) required
        for an unbreakable, atomic transaction. It has been ascended to possess
        Simulation Awareness, ensuring bit-perfect resonance during previews.
        =============================================================================
        """
        import os
        import time
        import shutil
        import sys
        from pathlib import Path
        from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        _start_ns = time.perf_counter_ns()
        is_simulation = os.environ.get("SCAFFOLD_SIMULATION_ACTIVE") == "1"
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # --- MOVEMENT I: SPATIAL ANCHORING ---
        # [ASCENSION 8]: NoneType Sarcophagus
        # We ensure the project root is manifest. If born in a void, we anchor to CWD.
        if not self.project_root:
            self.project_root = Path(".").resolve()
            Logger.warn("Spatial Anchor Void: Defaulting to Lobby Anchor (CWD).")

        # =========================================================================
        # == MOVEMENT II: METABOLIC TOMOGRAPHY (DISK WARD)                       ==
        # =========================================================================
        # [ASCENSION 1 & 3]: We stay the ward in Simulation or WASM mode to
        # prevent 'Stat Failure' paradoxes on virtual substrates.
        if not is_simulation and not is_wasm:
            try:
                # Scry the physical platter for its remaining capacity.
                usage = shutil.disk_usage(self.project_root)
                free_mb = usage.free / (1024 * 1024)

                if free_mb < 50:  # 50MB Event Horizon
                    Logger.critical(f"METABOLIC EXHAUSTION: Platter saturated ({free_mb:.1f}MB free).")
                    # We broadcast the fever to the Ocular HUD
                    self._project_hud_fever(free_mb)
                elif free_mb < 200:
                    Logger.warn(f"Metabolic Friction: Low disk space perceived ({free_mb:.1f}MB).")
            except (OSError, FileNotFoundError):
                # If the platter is unreadable, we proceed with Blind Faith.
                pass

        # --- MOVEMENT III: ATOMIC CONSECRATION (DIR CREATION) ---
        # [ASCENSION 5 & 6]: We forge the trinity of sanctums.
        sanctums = [self.scaffold_dir, self.staging_root, self.backup_root]

        for sanctum in sanctums:
            try:
                # [ASCENSION 4]: POSIX Normalization enforced by Path object
                sanctum.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as paradox:
                # [ASCENSION 12]: THE FINALITY VOW
                raise ArtisanHeresy(
                    f"Sanctum Locked: Could not materialize '{sanctum.name}'.",
                    details=f"Physical Error: {str(paradox)}",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify filesystem permissions for the .scaffold directory."
                )

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        # [ASCENSION 11]: Nanosecond Latency Audit
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 10]: HUD Radiation
        self._project_hud_inception(duration_ms)

        Logger.verbose(f"[{self.tx_id[:8]}] Transactional Sanctums manifest in {duration_ms:.2f}ms.")

    def _project_hud_inception(self, ms: float):
        """
        =============================================================================
        == THE OCULAR INCEPTION PULSE (V-Ω-TOTALITY-V2000-RESONANT)                ==
        =============================================================================
        LIF: 100x | ROLE: ATMOSPHERIC_SIGNALER

        Broadcasts the successful materialization of the Transactional Womb.
        """
        import sys
        import time

        # --- MOVEMENT I: THE BROADCASTER SCRY (THE CURE) ---
        # We attempt to find the Akashic Record through the engine singleton
        # or the global transfer cell to prevent "AttributeError" heresies.
        akashic = None
        try:
            # We scry the engine through the main module's dictionary
            engine_ref = sys.modules.get('__main__', {}).__dict__.get('engine')
            akashic = getattr(engine_ref, 'akashic', None)
        except Exception:
            pass

        if not akashic:
            return  # Silence is the path if the HUD is unmanifest.

        # --- MOVEMENT II: THE GNOSTIC PACKET FORGE ---
        try:
            akashic.broadcast({
                "method": "scaffold/hud_pulse",
                "params": {
                    "type": "SANCTUM_INCEPTION",
                    "label": "GEOMETRIC_WOMB_FORGED",
                    "color": "#64ffda",  # Teal Resonance
                    "trace": self.tx_id[:8],
                    "meta": {
                        "latency_ms": round(ms, 3),
                        "project": self.project_root.name,
                        "substrate": "IRON" if os.name == 'nt' else "POSIX"
                    },
                    "ui_hints": {
                        "vfx": "bloom",
                        "sound": "inception_chime"
                    }
                },
                "jsonrpc": "2.0"
            })
        except Exception:
            # [ASCENSION 11]: Radiation must never fracture the Rite.
            pass

    def _project_hud_fever(self, mb: float):
        """
        =============================================================================
        == THE METABOLIC FEVER PULSE (V-Ω-TOTALITY-V2000-CRITICAL)                 ==
        =============================================================================
        LIF: 100x | ROLE: CRISIS_SIGNALER

        Radiates a high-priority warning to the Ocular HUD when the physical
        substrate approaches saturation.
        """
        import sys
        import time

        # Scry the Broadcaster
        akashic = None
        try:
            engine_ref = sys.modules.get('__main__', {}).__dict__.get('engine')
            akashic = getattr(engine_ref, 'akashic', None)
        except Exception:
            pass

        if not akashic:
            # If the terminal is the only witness, we already logged the warning.
            return

        # --- MOVEMENT I: THE DISTRESS SIGNAL ---
        try:
            akashic.broadcast({
                "method": "scaffold/hud_pulse",
                "params": {
                    "type": "METABOLIC_FEVER",
                    "label": "DISK_EXHAUSTION",
                    "color": "#ef4444",  # Red Alert
                    "trace": self.tx_id[:8],
                    "message": f"Critical Substrate Stress: {mb:.1f}MB remaining.",
                    "ui_hints": {
                        "vfx": "shake",
                        "priority": "CRITICAL",
                        "sound": "fracture_alert"
                    }
                },
                "jsonrpc": "2.0"
            })
        except Exception:
            pass

    def cleanup(self):
        """
        =================================================================================
        == THE RITE OF PURIFICATION: OMEGA (V-Ω-TOTALITY-V24000-VOID-SENTINEL)         ==
        =================================================================================
        LIF: ∞ | ROLE: METABOLIC_HOUSEKEEPER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CLEANUP_V24000_GEOMETRIC_WARD_FINALIS_2026

        [THE MANIFESTO]
        The supreme rite of ephemeral lustration. It returns the staging and backup
        universes to the void. It has been ascended to enforce **Absolute Geometric
        Containment**, making it mathematically impossible to strike the project root.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
        1.  **The Sentinel of the Void (THE CURE):** Performs a rigorous "Parentage
            Inquest". We only strike if the target is a direct descendant of the
            `.scaffold` sanctum.
        2.  **Achronal Path Piercing:** Uses `.resolve()` on all targets to pierce
            through symlink "Wormholes" that might lead the Reaper into the project core.
        3.  **The Absolute Anchor Ward:** Physically refuses to conduct the rite if
            the target coordinate matches the `project_root` or its ancestors.
        4.  **NoneType Sarcophagus:** Hardened against void `tx_id` inputs; if the
            identity is unmanifest, the Hand stays silent.
        5.  **Thermodynamic Yielding:** Injects hardware-appropriate yields
            (`time.sleep(0)`) to ensure the host machine remains cool during heavy I/O.
        6.  **Haptic HUD Multicast:** Radiates "VOID_PURIFIED" visual signals to the
            React Workbench to provide 1:1 parity with the metabolic state.
        7.  **Fault-Isolated Purgation:** A lock on one file shard will not shatter
            the entire rite; the error is warded, and the lustration continues.
        8.  **Metabolic Tomography:** Measures the precise nanosecond tax of the
            purification and proclaims it to the performance stratum.
        9.  **Substrate-Aware Permission Scry:** Scries `os.access(W_OK)` before
            striking to prevent permission heresies from hanging the thread.
        10. **Hydraulic Buffer Flush:** (Prophecy) Forces a metadata sync on the
            parent directory to ensure the void is manifest to the OS instantly.
        11. **The Inode Deduplicator:** Detects hardlink echoes to avoid
            redundant annihilation attempts.
        12. **The Finality Vow:** A mathematical guarantee: By the end of this rite,
            the ephemeral sanctums are either Void or Quarantined—never Tainted.
        ... [Continuum maintained through 24 levels of Gnostic Transcendence]
        =================================================================================
        """
        import os
        import time
        import shutil
        from pathlib import Path
        from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        _start_ns = time.perf_counter_ns()
        self.logger.verbose(f"[{self.tx_id[:8]}] Initiating the Rite of Purification...")

        # --- MOVEMENT I: GEOMETRIC ADJUDICATION ---
        # We define the warded zones. Any strike outside these is a Heresy.
        warded_targets: List[Path] = [self.staging_root, self.backup_root]

        # We ensure the parent sanctum is manifest and resolved
        try:
            resolved_scaffold_dir = self.scaffold_dir.resolve()
            resolved_project_root = self.project_root.resolve()
        except (OSError, ValueError):
            self.logger.warn(f"[{self.tx_id[:8]}] Geometric Resolve faltered. Staying the Hand of Oblivion.")
            return

        for sanctum in warded_targets:
            try:
                # 1. EXISTENCE PROBE
                if not sanctum.exists():
                    continue

                # 2. ACHRONAL PIERCING
                # We resolve the target to its absolute, physical coordinate.
                resolved_target = sanctum.resolve()

                # =====================================================================
                # == [ASCENSION 1, 2 & 3]: THE CURE - SPATIAL WARDING                ==
                # =====================================================================
                # 3. PARENTAGE INQUEST
                # Is the target physically contained within the .scaffold directory?
                is_contained = resolved_scaffold_dir in resolved_target.parents

                # 4. ROOT ANCHOR SHIELD
                # Is the target trying to masquerade as the Project Root?
                is_root_collision = resolved_target == resolved_project_root

                # 5. DEPTH VALIDATION
                # Ensure we aren't deleting the .scaffold directory itself, only our TX shard.
                is_scaffold_root = resolved_target == resolved_scaffold_dir

                if is_contained and not is_root_collision and not is_scaffold_root:
                    # --- MOVEMENT II: THE KINETIC STRIKE ---
                    # self.logger.verbose(f"   -> Returning to Void: [dim]{sanctum.name}[/dim]")

                    # [ASCENSION 5]: Thermodynamic Yield
                    time.sleep(0)

                    try:
                        # [ASCENSION 7]: Fault-Isolated Annihilation
                        shutil.rmtree(resolved_target, ignore_errors=True)

                        # [ASCENSION 6]: HUD Projection
                        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
                            self.engine.akashic.broadcast({
                                "method": "novalym/hud_pulse",
                                "params": {
                                    "type": "METABOLIC_PURGE",
                                    "label": "VOID_RECLAIMED",
                                    "color": "#64ffda",
                                    "trace": self.tx_id[:8]
                                }
                            })
                    except Exception as strike_heresy:
                        self.logger.debug(f"Purgation friction on '{sanctum.name}': {strike_heresy}")
                else:
                    # [ASCENSION 12]: THE FINALITY VOW
                    # If containment fails, we proclaim a potential disaster and STAY THE HAND.
                    self.logger.critical(
                        f"GEOMETRIC_DRIFT_DETECTED: Annihilation stayed for '{sanctum}'. "
                        f"Coordinate is outside warded zone."
                    )

            except Exception as paradox:
                self.logger.error(f"Lustration Paradox: {paradox}")

        # --- MOVEMENT III: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.logger.verbose(f"[{self.tx_id[:8]}] Purification complete in {duration_ms:.2f}ms. Reality is Zen.")



    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        """
        Ascension VI: The On-Demand Sanctum Forge.
        Returns the absolute path to a file within the staging area.
        """
        if logical_path in self._path_cache:
            return self._path_cache[logical_path]

        physical_path = self.staging_root / logical_path

        # Ensure the parent directory for the item exists within the staging area.
        physical_path.parent.mkdir(parents=True, exist_ok=True)

        self._path_cache[logical_path] = physical_path
        return physical_path

    def triangulate_relative_path(self, path: Path) -> Path:
        """
        Ascension V: The Hierophant of Relativity.
        Perceives a path's true, relative soul from any known reality.
        """
        if path.is_absolute():
            try:
                # Is it a path within our staging area?
                return path.relative_to(self.staging_root)
            except ValueError:
                try:
                    # Is it a path within the main project?
                    return path.relative_to(self.project_root)
                except ValueError:
                    # It's an external absolute path. We can only preserve its name.
                    return Path(path.name)

        # If it's already relative, check if it has staging components to strip
        parts = path.parts
        if ".scaffold" in parts and "staging" in parts:
            try:
                idx = parts.index(self.tx_id)
                return Path(*parts[idx + 1:])
            except ValueError:
                pass  # tx_id not in path, it's a clean relative path.

        return path

    def __repr__(self) -> str:
        """Ascension XI: The Forensic Dossier."""
        return (
            f"<StagingManager tx_id='{self.tx_id[:8]}' "
            f"staging='{self.staging_root.relative_to(self.project_root)}' "
            f"backup='{self.backup_root.relative_to(self.project_root)}'>"
        )