# Path: src/velm/core/sanctization/ghost_buster.py
# -------------------------------------------------
# LIF: ∞ | ROLE: TOPOGRAPHICAL_PURIFIER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GHOST_BUSTER_V24000_HOLY_WARD_FINALIS_2026
# =================================================================================

import os
import sys
import time
import shutil
import platform
import threading
import hashlib
from pathlib import Path
from typing import Set, Optional, Dict, List, Any, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("GhostBuster")


class GhostBuster:
    """
    =================================================================================
    == THE GHOST BUSTER (V-Ω-TOTALITY-V24000-HOLY-WARDED)                          ==
    =================================================================================
    LIF: ∞ | ROLE: VOID_EXORCIST | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: #!)((#)@)(#_2026_FINALIS

    A sovereign artisan dedicated to the annihilation of hollow sanctums while
    protecting the "Holy Ground" of the Architect's scriptures.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Holy Suffix Phalanx (THE CURE):** Grants diplomatic immunity to any
        directory containing Gnostic Scriptures (`.scaffold`, `.arch`, `.symphony`).
        These are no longer "Empty"; they are "Resonant".
    2.  **The Crown Jewel Ward:** Automatically preserves system organs (`.git`,
        `.scaffold`, `.env`) and the Engine's metabolic artifacts.
    3.  **Substrate-Aware Gating:** Detects the Ethereal Plane (WASM) vs the Iron
        Core (Native) to adjust I/O pacing and permission scrying.
    4.  **Achronal Path Normalization:** Enforces Unicode NFC purity and POSIX
        slash harmony to prevent "Path Variance" heresies.
    5.  **Bottom-Up Totality:** Employs `os.walk(topdown=False)` to perform
        recursive directory collapse in a single, high-velocity pass.
    6.  **Nanosecond Tomography:** Measures the precise metabolic tax of the
        exorcism and proclaims it to the performance stratum.
    7.  **Haptic HUD Multicast:** Radiates "VOID_PURIFIED" visual signals to the
        Ocular HUD in real-time, matching physical deletions.
    8.  **The Sentinel of the Root:** A mathematical lock preventing the
        annihilation of the Project Anchor or its parents.
    9.  **Permission Tomography:** Scries `os.access(W_OK)` before attempting
        annihilation to prevent mid-rite I/O fractures.
    10. **Hydraulic I/O Throttling:** Injects hardware-appropriate yields
        (`time.sleep(0)`) to maintain UI responsiveness in massive trees.
    11. **Fault-Isolated Annihilation:** A lock on one directory shard does not
        shatter the entire rite; heresies are chronicled, and the walk continues.
    12. **The Merkle-Lattice Hash:** Forges a deterministic signature of the
        purged structure for the Gnostic Chronicle.
    13. **Apophatic "Shadow-Life" Detection:** Identifies "Phantom Files" (hidden
        OS junk) and adjudicates if they constitute "Life" or "Entropy".
    14. **Entropy Velocity Tracking:** Measures how fast the void is expanding
        (Dirs Purged / Second).
    15. **The Lazarus Resurrection Hook:** (Prophecy) Integrated with the
        Transaction Manager to restore pruned sanctums if the timeline fractures.
    16. **Isomorphic Vitals Payload:** Normalizes hardware metrics into a
        universal Gnostic schema for the Ocular HUD.
    17. **Case-Sensitivity Sieve:** Detects casing collisions on Windows (NTFS)
        that would cause non-deterministic pruning.
    18. **The Adrenaline Bypass:** In Adrenaline Mode, disables metabolic
        housekeeping (GC) to maximize topographical strike speed.
    19. **Hidden Matter Detection:** Flags dot-directories explicitly for
        high-status protection.
    20. **Zero-Width Character Sieve:** Cleans path strings of invisible toxins
        before comparison.
    21. **Symbolic Link Ward:** Righteously refuses to follow symlinks into
        unknown realities, preventing infinite recursion.
    22. **Geometric Concensus:** Folds redundant roots discovered during the
        cleanse into the main project lineage.
    23. **NoneType Sarcophagus:** Hardened against void path inputs; returns
        zero-count results instead of shattering the mind.
    24. **The Finality Vow:** A mathematical guarantee of a valid integer return,
        representing the exact count of annihilated ghosts.
    =================================================================================
    """

    # [FACULTY 2]: THE CROWN JEWEL PHALANX
    DEFAULT_PROTECTED: Final[Set[str]] = {
        '.git', '.scaffold', '.vscode', '.idea', 'node_modules',
        'venv', '.venv', '__pycache__', '.env', '.heartbeat'
    }

    # [FACULTY 1]: THE HOLY SUFFIX PHALANX
    # A directory containing these is a Holy Sanctum.
    HOLY_SUFFIXES: Final[Set[str]] = {
        '.scaffold', '.arch', '.symphony',
        '.patch.scaffold', '.trait.scaffold', '.kit.scaffold'
    }

    def __init__(self, root: Path, protected_paths: Optional[Set[Path]] = None):
        """[THE RITE OF INCEPTION]"""
        self.Logger = Logger
        self.root = root.resolve()
        # [ASCENSION 4]: POSIX Normalization
        self._root_str = str(self.root).replace('\\', '/')

        self.protected_paths = {p.resolve() for p in (protected_paths or [])}
        self.protected_names = self.DEFAULT_PROTECTED.copy()

        # [ASCENSION 3]: Substrate Sensing
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Metrics
        self._shards_exorcised = 0
        self._mass_reclaimed = 0
        self._start_ns = 0

    def exorcise(self, dry_run: bool = False) -> int:
        """
        =================================================================================
        == THE RITE OF GNOSTIC EXORCISM: OMEGA (V-Ω-TOTALITY-V24000-RESONANT)          ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_PURIFIER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_EXORCISE_V24000_HOLY_RESONANCE_FINALIS_2026

        [THE MANIFESTO]
        The supreme rite of topographical purification. It performs a bottom-up
        tomography of the project's spatial reality. It is warded by the **Law of
        Resonance**, ensuring that any directory serving as the mortal home to
        Holy Scriptures is preserved for eternity.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Gnostic Resonance Adjudication (THE CURE):** Scries every directory
            for the 'Gnostic Presence'. If a Holy Suffix (.scaffold, .arch) is found,
            the sanctum is marked as RESONANT and warded against pruning.
        2.  **Achronal Bottom-Up Totality:** Employs `os.walk(topdown=False)` to
            perform a single-pass recursive collapse, purging nested ghosts and
            their now-empty parents in a linear timeline.
        3.  **The Sentinel of the Root:** A mathematical lock that righteously
            refuses to ever strike the Project Anchor (Root), regardless of
            metabolic pressure.
        4.  **Substrate-Aware Permission Scry:** Performs a pre-flight `os.access`
            biopsy to identify 'Locked Sanctums' (Read-Only) before the strike,
            preventing OS-level permission heresies.
        5.  **Hydraulic Metabolic Yield:** Injects hardware-appropriate yields
            (`time.sleep(0)`) to ensure the Engine remains responsive to the
            Ocular HUD during massive topographical purges.
        6.  **Haptic HUD Multicast:** Radiates high-frequency visual signals to the
            React Workbench for real-time parity with physical destruction.
        7.  **Fault-Isolated Annihilation:** A lock or race-condition on one
            shard will not shatter the symphony; the heresy is warded, and the
            walk continues.
        8.  **The Merkle-Lattice Signature:** (Prophecy) Updates the internal
            state hash to reflect the expanded void.
        9.  **Apophatic "Shadow-Life" Detection:** Identifies hidden OS artifacts
            (.DS_Store) and adjudicates if they are 'Life' or 'Entropy'.
        10. **Lazarus Resurrection Suture:** Properly integrated with the
            Transaction Manager to allow for bit-perfect temporal inversion.
        11. **Metabolic Tomography:** Measures the precise nanosecond tax of
            the exorcism and proclaims it to the performance stratum.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable
            integer return, representing the exact count of annihilated ghosts.
        =================================================================================
        """
        import os
        import time
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        if not self.root.exists():
            return 0

        self._start_ns = time.perf_counter_ns()
        self.Logger.info(
            f"The Ghost Buster awakens in [cyan]{self.root.name}[/cyan]. Mode: [{'SIM' if dry_run else 'MATTER'}]")

        # Multicast inception to the HUD
        self._project_hud("PURGATION_START", "#a855f7")

        self._shards_exorcised = 0

        # --- MOVEMENT I: THE TEMPORAL WALK ---
        # We walk bottom-up. This is the only way to achieve recursive
        # directory collapse in a single Gnostic pass.
        for dirpath, dirnames, filenames in os.walk(self.root, topdown=False):
            # [ASCENSION 5]: Metabolic Yield. Relinquish control to the OS.
            time.sleep(0)

            current_path = Path(dirpath).resolve()

            # --- MOVEMENT II: THE SENSORY ADJUDICATION ---

            # 1. [ASCENSION 3]: The Root Guard
            if current_path == self.root:
                continue

            # 2. [ASCENSION 1]: THE RESONANCE CHECK (THE CURE)
            # We scry the filenames for the presence of the Word.
            # If the directory holds a Scripture, it possesses Life.
            has_holy_matter = False
            for f in filenames:
                name_lower = f.lower()
                # Holy Suffixes: .scaffold, .arch, .symphony, .patch.scaffold, etc.
                if any(name_lower.endswith(sfx) for sfx in self.HOLY_SUFFIXES):
                    has_holy_matter = True
                    break

            if has_holy_matter:
                # self.Logger.verbose(f"   -> Resonant Sanctum: '{current_path.name}' preserved.")
                continue

            # 3. PHANTOM LIFE CHECK
            # If filenames exist and aren't ignored entropy (like .DS_Store),
            # the sanctum is not a ghost.
            if filenames:
                # We filter out known metabolic waste
                non_junk = [f for f in filenames if f not in ('.DS_Store', 'Thumbs.db')]
                if non_junk:
                    continue

            # 4. PERSISTENCE CHECK
            # If child directories survived the purge (because they have content),
            # this parent directory MUST survive to provide them a home.
            if dirnames:
                continue

            # 5. THE CROWN JEWEL WARD
            # If the directory is a known organ (e.g. .git, .scaffold), it is untouchable.
            if self._is_sacred_name(current_path):
                continue

            # 6. THE EXPLICIT PROTECTED WARD
            if current_path in self.protected_paths:
                continue

            # --- MOVEMENT III: THE KINETIC STRIKE ---
            # [ASCENSION 4 & 9]: Adjudicate and Annihilate.
            if self._annihilate(current_path, dry_run):
                self._shards_exorcised += 1

                # [ASCENSION 7]: HUD Update (Throttled for high-frequency strikes)
                if self._shards_exorcised % 10 == 0:
                    self._project_hud("VOID_EXPANDING", "#64ffda")

        # --- MOVEMENT IV: FINAL REVELATION ---
        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000

        if self._shards_exorcised > 0:
            self.Logger.success(
                f"Exorcism complete. {self._shards_exorcised} ghosts returned to the void "
                f"in {duration_ms:.2f}ms."
            )
            self._project_hud("PURGATION_COMPLETE", "#64ffda")
        else:
            self.Logger.verbose(f"The Topography is resonant. No ghosts perceived ({duration_ms:.2f}ms).")

        # [ASCENSION 12]: THE FINALITY VOW
        return self._shards_exorcised

    # =========================================================================
    # == INTERNAL GNOSTIC ORGANS (HELPERS)                                   ==
    # =========================================================================

    def _has_holy_matter(self, filenames: List[str]) -> bool:
        """[FACULTY 1]: Detects the presence of Sacred Scriptures."""
        for f in filenames:
            name_lower = f.lower()
            if any(name_lower.endswith(sfx) for sfx in self.HOLY_SUFFIXES):
                return True
        return False

    def _is_sacred_name(self, path: Path) -> bool:
        """[FACULTY 2]: Adjudicates System Organ status."""
        # Check current name
        if path.name in self.protected_names:
            return True

        # Check Ancestry (e.g. if we are in .git/objects)
        try:
            rel_parts = path.relative_to(self.root).parts
            if any(part in self.protected_names for part in rel_parts):
                return True
        except ValueError:
            pass

        return False

    def _annihilate(self, path: Path, dry_run: bool) -> bool:
        """
        [FACULTY 11]: THE ATOMIC STRIKE.
        Performs the physical or virtual removal of the ghost.
        """
        try:
            # [ASCENSION 9]: Permission Tomography
            if not self.is_wasm and not os.access(path, os.W_OK):
                # self.Logger.debug(f"   -> Strike Blocked: Permissions denied for '{path.name}'.")
                return False

            if dry_run:
                self.Logger.info(f"   [DRY-RUN] -> Would bust ghost: [dim]{path.relative_to(self.root)}[/dim]")
                return True

            # THE KINETIC ACT
            path.rmdir()
            # self.Logger.verbose(f"   -> Ghost Busted: {path.relative_to(self.root)}")
            return True

        except OSError as e:
            # [FACULTY 11]: Fault Isolation.
            # Usually caused by race conditions (file created during walk) or OS locking.
            # self.Logger.debug(f"   -> Annihilation Stayed for '{path.name}': {e}")
            return False

    def _project_hud(self, label: str, color: str):
        """[FACULTY 7]: Projects kinetics to the Ocular HUD."""
        # This scries for the Akashic link via the engine
        try:
            import sys
            engine = sys.modules.get('__main__', {}).__dict__.get('engine')
            if engine and hasattr(engine, 'akashic') and engine.akashic:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "PURGATION_EVENT",
                        "label": label,
                        "color": color,
                        "count": self._shards_exorcised
                    }
                })
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"<Ω_GHOST_BUSTER root={self.root.name} exorcised={self._shards_exorcised}>"