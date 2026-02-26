# Path: src/velm/core/kernel/transaction/volume_shifter/shifter/engine.py
# -----------------------------------------------------------------------

import os
import sys
import time
import threading
import signal
import subprocess
import random
from pathlib import Path

from ......logger import Scribe
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

from .immunity import ImmunityMatrix
from .robust_rename import AtomicRenamer
from .swap import ContentWeaver

Logger = Scribe("VolumeShifter:Kinetic")


class KineticShifter:
    """
    =================================================================================
    == THE KINETIC SHIFTER: OMEGA POINT (V-Ω-TOTALITY-V64-LEGENDARY-ASCENDED)      ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_TRANSMUTATION_HAND | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SHIFTER_V64_OMNISCIENT_GHOST_SUTURE_FINALIS

    The Unbreakable Hand of the Achronal Flip. It governs the atomic swapping of
    Active (Blue) and Shadow (Green) realities.

    ### THE PANTHEON OF 64 LEGENDARY ASCENSIONS (HIGHLIGHTS):
    1.  **The Directory Replace Exorcism (THE CURE):** Surgically drops the `0x1`
        flag during `MoveFileExW` if the source is a directory, annihilating the
        Windows Error 5 that prevented `.git` translocation.
    2.  **The Absolute Immunity Lift (THE CURE):** The Shifter now perceives if
        the Holy Ground (`.git`) is unmanifest. If so, it lifts its own immunity
        ward, allowing the Shadow Volume to natively establish the repository.
    3.  **Modular Organ Decapitation:** The monolith is shattered into `swap.py`,
        `robust_rename.py`, and `immunity.py` for infinite scalability.
    4.  **Native Handle Exorcism:** Employs `psutil` to hunt down and assassinate
        background processes holding file locks during a forced flip.
    5.  **Achronal Geometric Normalization:** Universal UNC prefixing (`\\\\?\\`).
    6.  **Bicameral Restoration Phalanx:** A dual-pass rollback strategy.
    7.  **Signal Shielding (The Uninterruptible Vow):** Ignores SIGINT (Ctrl+C).
    8.  **The Tombstone Suture (Ghost Rename):** Bypasses `WinError 32` via `.ghost`.
    ... [The lore continues through 64 levels of Gnostic Transcendence]
    =================================================================================
    """

    def __init__(self, root: Path):
        """[THE RITE OF INCEPTION]"""
        try:
            root_resolved = root.resolve()
            root_str = str(root_resolved).replace('\\\\?\\', '')
            self.root = Path(root_str).resolve()
        except (OSError, ValueError):
            self.root = Path(".").resolve()

        self.force: bool = False
        self.Logger = Logger
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.is_windows = os.name == 'nt'
        self._mutex = threading.RLock()

        # --- THE INTERNAL ORGANS ---
        self.immunity = ImmunityMatrix(self.Logger)
        self.renamer = AtomicRenamer(self.Logger, self.is_windows, self.is_wasm)
        self.weaver = ContentWeaver(self.Logger, self.immunity, self.renamer, self.root, self.is_wasm)

        self.Logger.debug(
            f"Kinetic Hand materialised. Anchor: [cyan]{self.root.name}[/cyan] | "
            f"Substrate: {'ETHER' if self.is_wasm else 'IRON'}"
        )

    def perform_rename_flip(self, active: Path, shadow: Path, legacy: Path, tx_id: str = "VOID"):
        """
        =============================================================================
        == THE RENAME STRATEGY (THE ACHRONAL SWAP)                                 ==
        =============================================================================
        Standard for local filesystems. It provides the highest degree of atomicity.
        """
        with self._mutex:
            active = Path(self.renamer._canonize_path(active))
            legacy = Path(self.renamer._canonize_path(legacy))
            shadow = Path(self.renamer._canonize_path(shadow))

            active.parent.mkdir(parents=True, exist_ok=True)

            # [TOPOLOGICAL PARADOX WARD]
            is_paradox = False
            try:
                if legacy.is_relative_to(active) or active.resolve() == Path.cwd().resolve() or (
                        active / ".scaffold").exists():
                    is_paradox = True
            except Exception:
                if str(legacy).startswith(str(active)) or active.resolve() == Path.cwd().resolve():
                    is_paradox = True

            if is_paradox:
                self.Logger.verbose(
                    f"[{tx_id[:8]}] Topological Paradox perceived (CWD/Root Lock). Engaging Surgical Content Swap.")
                self.weaver.surgical_content_swap(active, shadow, legacy, tx_id, self.force)
                self.renamer.evaporate_ghosts()
                return

            # --- STANDARD ROOT FOLD (For isolated Sub-Directories) ---
            original_sigint = None
            if not self.is_wasm:
                try:
                    original_sigint = signal.getsignal(signal.SIGINT)
                    signal.signal(signal.SIGINT, signal.SIG_IGN)
                except (ValueError, AttributeError):
                    pass

            try:
                # MOVEMENT I: DISPLACEMENT
                if active.exists():
                    try:
                        self.renamer.robust_rename(active, legacy)
                    except Exception as e:
                        raise ArtisanHeresy(
                            "Displacement Fracture: Could not move active reality to legacy buffer.",
                            details=f"Path: {active} | Error: {type(e).__name__}: {e}",
                            severity=HeresySeverity.CRITICAL
                        )

                # MOVEMENT II: ASCENSION
                try:
                    self.renamer.robust_rename(shadow, active)

                    if os.name == 'posix':
                        try:
                            dir_fd = os.open(str(active.parent), os.O_RDONLY)
                            os.fsync(dir_fd)
                            os.close(dir_fd)
                        except Exception:
                            pass

                except Exception as e:
                    self.Logger.critical(
                        f"[{tx_id[:8]}] Ascension Fracture during flip: {e}. Initiating Emergency Rollback...")
                    if legacy.exists() and not active.exists():
                        try:
                            self.renamer.robust_rename(legacy, active)
                            self.Logger.success("Emergency Rollback successful. Previous reality restored.")
                        except Exception as rollback_err:
                            self.Logger.critical(f"FATAL PARADOX: Emergency Rollback failed: {rollback_err}")
                    raise ArtisanHeresy("Reality Flip Failed", child_heresy=e, severity=HeresySeverity.CRITICAL)

            finally:
                if original_sigint is not None and not self.is_wasm:
                    try:
                        signal.signal(signal.SIGINT, original_sigint)
                    except (ValueError, AttributeError):
                        pass
                self.renamer.evaporate_ghosts()

    def perform_symlink_flip(self, link_path: Path, shadow: Path, legacy: Path):
        """
        =============================================================================
        == THE SYMLINK STRATEGY (POINTER SWAP & JUNCTION FALLBACK)                 ==
        =============================================================================
        """
        link_path = Path(self.renamer._canonize_path(link_path))
        shadow = Path(self.renamer._canonize_path(shadow))
        temp_link = link_path.with_suffix(f".tmp_link_{random.randint(1000, 9999)}")

        try:
            if self.is_windows:
                try:
                    os.symlink(shadow, temp_link, target_is_directory=True)
                except OSError as e:
                    if getattr(e, 'winerror', 0) == 1314:
                        self.Logger.warn("Symlink Privilege Denied. Devolving to NTFS Junction Point...")
                        res = subprocess.run(f'cmd.exe /c mklink /J "{temp_link}" "{shadow}"', shell=True,
                                             capture_output=True)
                        if res.returncode != 0:
                            raise ArtisanHeresy("Privilege Heresy: Symlink and Junction creation failed.",
                                                severity=HeresySeverity.CRITICAL)
                    else:
                        raise e
            else:
                os.symlink(shadow, temp_link)

            os.replace(temp_link, link_path)

        except Exception as e:
            if temp_link.exists():
                try:
                    if temp_link.is_dir() and not temp_link.is_symlink():
                        os.rmdir(temp_link)
                    else:
                        temp_link.unlink()
                except:
                    pass
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy("Symlink Flip Failed", child_heresy=e, severity=HeresySeverity.CRITICAL)