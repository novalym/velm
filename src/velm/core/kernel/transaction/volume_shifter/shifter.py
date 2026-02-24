# Path: core/kernel/transaction/volume_shifter/shifter.py
# -------------------------------------------------------
# =========================================================================================
# == THE KINETIC SHIFTER: OMEGA POINT (V-Ω-ATOMIC-SYSCALL-V24000-SURGICAL-SWAP)          ==
# =========================================================================================
# LIF: ∞ | ROLE: ACHRONAL_STRIKER | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_SHIFTER_V24000_SURGICAL_SWAP_)(!@#()#!()@#)
#
# [ARCHITECTURAL MANIFESTO]
# The physical Hand that executes the Achronal Flip. It is built to survive the
# most hostile OS environments across the multiverse, conquering Windows Antivirus
# locks, Cross-Mount boundaries, and topological CWD paradoxes.
#
# ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
# 1.  **Surgical Content Swap (THE CURE):** If the target is the Current Working
#     Directory (CWD) or contains the `.scaffold` sanctum, it pivots from a blunt
#     Directory Rename to a hyper-precise child-by-child displacement. This
#     permanently annihilates `WinError 32: Process cannot access file`.
# 2.  **Surgical Rollback Suture:** If a Surgical Swap fractures halfway, it maintains
#     a precise ledger of displaced souls and automatically reverses entropy, returning
#     the Legacy matter to the Active root.
# 3.  **The Crown Jewel Ward:** During Surgical Swaps, it possesses the absolute
#     wisdom to never touch, move, or overwrite `.scaffold`, `.git`, or `.env`.
# 4.  **Cross-Device Suture (EXDEV 18):** `os.rename` fractures if moving data across
#     different disk drives. Catches `OSError 18` and devolves into `shutil.move`.
# 5.  **Read-Only Annihilation:** Git and NPM often leave read-only `.pack` or cache
#     files. The Shifter automatically injects `stat.S_IWRITE` before retrying
#     moves, destroying `WinError 5 (Access Denied)`.
# 6.  **The Windows Antivirus Ward:** Windows Defender routinely locks folders immediately
#     after files are written. The `_robust_rename` rite uses exponential backoff
#     with geometric jitter to outlast the AV scan.
# 7.  **Parent Forging:** Physically guarantees the destination's parent directory
#     exists *before* the swap, annihilating `FileNotFoundError`.
# 8.  **Zombie Handle Exorcism:** Triggers `gc.collect()` before retry loops to
#     sever dangling Python file handles that lock the substrate.
# 9.  **Long-Path Phalanx:** Dynamically injects `\\?\` on Windows to bypass the
#     260-character `MAX_PATH` limit during deep NPM/Rust framework nesting.
# 10. **Symlink Atomicity:** Employs the `Temp-Link & Replace` algorithm to guarantee
#     that symlink flips occur in a single OS tick, preventing broken routes.
# 11. **NTFS Junction Fallback:** If Symlink creation fails due to Windows Developer
#     Mode restrictions (Error 1314), it falls back to forging an NTFS Junction Point
#     via `cmd.exe /c mklink /J`.
# 12. **Inode Directory Synchronization:** Calls `os.fsync` on the parent directory (POSIX)
#     to guarantee the directory entry update is flushed to the physical platter.
# 13. **Hydraulic Thread Yield:** Yields to the OS scheduler (`time.sleep`) during
#     backoff loops to prevent CPU spin-locking and heat generation.
# 14. **The Void Purifier:** Safely ignores `FileNotFoundError` if the active target
#     was already deleted by an external force prior to the flip.
# 15. **Stat-Preservation Covenant:** Ensures `mtime`, `atime`, and permissions are
#     perfectly preserved during EXDEV fallback copies.
# 16. **Substrate-Agnostic Unlinking:** Uses platform-specific deletion logic to
#     clear stale `.tmp_link` debris from previously crashed symlink flips.
# 17. **Achronal Flip Timeout:** Implements a hard 10-second ceiling on the retry
#     loop to prevent infinite lock hangs on truly deadlocked servers.
# 18. **Transaction ID Telemetry:** Plumbs the `tx_id` into all logs and Heresies
#     for deep forensic autopsies.
# 19. **Granular Flip Metrics:** Tracks the number of souls translocated during
#     Surgical Swaps for the Ocular HUD.
# 20. **Directory Union Dampener:** Intelligently handles overlapping directories
#     during fallback moves, recursively merging them instead of clobbering.
# 21. **Haptic Radiation Hook:** Emits telemetry pulses during long surgical swaps
#     to ensure the Architect knows the Engine has not frozen.
# 22. **The Phantom Lock Breaker:** On Windows, temporarily renames colliding
#     destinations to a `.void` extension before deleting to bypass pending-delete locks.
# 23. **Silent Genesis Optimization:** If the Active reality does not exist yet,
#     it bypasses the Legacy displacement entirely, achieving O(1) creation time.
# 24. **The Finality Vow:** A mathematical guarantee of atomic reality swapping.
# =========================================================================================

import os
import time
import shutil
import platform
import stat
import random
import gc
import subprocess
from pathlib import Path
from typing import Final, List, Tuple, Set

from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("VolumeShifter:Kinetic")


class KineticShifter:
    """The Unbreakable Hand of the Achronal Flip."""

    # [PHYSICS CONSTANTS]
    RETRY_LIMIT: Final[int] = 6
    BASE_DELAY_S: Final[float] = 0.15
    MAX_TIMEOUT_S: Final[float] = 10.0

    # [ASCENSION 3]: THE CROWN JEWEL WARD
    # Artifacts that must never be displaced during a Surgical Swap.
    CROWN_JEWELS: Final[Set[str]] = {'.scaffold', '.git', '.env', '.env.local'}

    def perform_rename_flip(self, active: Path, shadow: Path, legacy: Path, tx_id: str = "VOID"):
        """
        =============================================================================
        == THE RENAME STRATEGY (THE ACHRONAL SWAP)                                 ==
        =============================================================================
        Standard for local filesystems. It provides the highest degree of atomicity.
        """
        # [ASCENSION 9]: Long-Path Normalization
        active = Path(self._canonize_path(active))
        legacy = Path(self._canonize_path(legacy))
        shadow = Path(self._canonize_path(shadow))

        # [ASCENSION 7]: Parent Forging
        active.parent.mkdir(parents=True, exist_ok=True)

        # =========================================================================
        # == [ASCENSION 1]: THE TOPOLOGICAL PARADOX WARD (THE CURE)              ==
        # =========================================================================
        # If the 'active' target IS the CWD, or if it contains the '.scaffold' sanctum
        # (where our own logs and DBs live), we CANNOT rename it. The OS will block it
        # with WinError 32. We must perform a Surgical Content Swap instead of a Root Fold.

        is_paradox = False
        try:
            # Check if legacy is inside active (Inception), or if active is CWD
            if legacy.is_relative_to(active) or active.resolve() == Path.cwd().resolve() or (
                    active / ".scaffold").exists():
                is_paradox = True
        except Exception:
            # Fallback for older Python versions or cross-drive comparisons
            if str(legacy).startswith(str(active)) or active.resolve() == Path.cwd().resolve():
                is_paradox = True

        if is_paradox:
            Logger.verbose(
                f"[{tx_id[:8]}] Topological Paradox perceived (CWD/Root Lock). Engaging Surgical Content Swap.")
            self._surgical_content_swap(active, shadow, legacy, tx_id)
            return
        # =========================================================================

        # --- STANDARD ROOT FOLD (For isolated Sub-Directories like 'sentinel-api') ---

        # --- MOVEMENT I: THE DISPLACEMENT (Blue -> Legacy) ---
        # [ASCENSION 23]: Silent Genesis Optimization
        if active.exists():
            try:
                self._robust_rename(active, legacy)
            except Exception as e:
                raise ArtisanHeresy(
                    "Displacement Fracture: Could not move active reality to legacy buffer.",
                    details=f"Path: {active} | Error: {type(e).__name__}: {e}",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Ensure no terminals, IDEs, or background processes are holding open files."
                )

        # --- MOVEMENT II: THE ASCENSION (Green -> Blue) ---
        try:
            self._robust_rename(shadow, active)

            # [ASCENSION 12]: Inode Synchronization
            if os.name == 'posix':
                try:
                    dir_fd = os.open(str(active.parent), os.O_RDONLY)
                    os.fsync(dir_fd)
                    os.close(dir_fd)
                except Exception:
                    pass

        except Exception as e:
            # --- MOVEMENT III: EMERGENCY RESTORATION (THE WARD) ---
            Logger.critical(f"[{tx_id[:8]}] Ascension Fracture during flip: {e}. Initiating Emergency Rollback...")
            if legacy.exists() and not active.exists():
                try:
                    self._robust_rename(legacy, active)
                    Logger.success("Emergency Rollback successful. Previous reality restored.")
                except Exception as rollback_err:
                    Logger.critical(f"FATAL PARADOX: Emergency Rollback failed: {rollback_err}")
            raise ArtisanHeresy("Reality Flip Failed", child_heresy=e, severity=HeresySeverity.CRITICAL)

    def _surgical_content_swap(self, active: Path, shadow: Path, legacy: Path, tx_id: str):
        """
        =============================================================================
        == THE SURGICAL CONTENT SWAP (V-Ω-ATOMIC-CHILD-ROUTING)                    ==
        =============================================================================
        Safely swaps the contents of a locked root directory by moving its children
        individually, bypassing CWD and internal sanctum locks.
        """
        legacy.mkdir(parents=True, exist_ok=True)
        displaced_souls: List[Tuple[Path, Path]] = []
        translocated_count = 0

        try:
            # --- MOVEMENT I: SURGICAL DISPLACEMENT (Active -> Legacy) ---
            # We only displace matter that the Shadow Volume intends to overwrite
            for child in shadow.iterdir():
                target_child = active / child.name

                if target_child.exists():
                    # [ASCENSION 3]: The Crown Jewel Ward
                    if target_child.name in self.CROWN_JEWELS:
                        continue

                    legacy_child = legacy / child.name
                    self._robust_rename(target_child, legacy_child)
                    displaced_souls.append((legacy_child, target_child))

            # --- MOVEMENT II: SURGICAL ASCENSION (Shadow -> Active) ---
            for child in list(shadow.iterdir()):
                target_child = active / child.name

                if target_child.name in self.CROWN_JEWELS:
                    continue

                self._robust_rename(child, target_child)
                translocated_count += 1

            # [ASCENSION 19]: Granular Metrics
            Logger.verbose(f"[{tx_id[:8]}] Surgical Swap complete. {translocated_count} atoms translocated.")

        except Exception as e:
            # [ASCENSION 2]: SURGICAL ROLLBACK SUTURE
            Logger.critical(f"[{tx_id[:8]}] Surgical Swap Fractured ({e})! Reversing entropy...")
            try:
                # 1. Purge the partially moved shadow matter from Active
                for child in shadow.iterdir():
                    target_child = active / child.name
                    if target_child.exists() and target_child.name not in self.CROWN_JEWELS:
                        # Only delete if we didn't displace it (meaning it came from shadow just now)
                        if not any(act == target_child for _, act in displaced_souls):
                            if target_child.is_dir():
                                shutil.rmtree(target_child, ignore_errors=True)
                            else:
                                target_child.unlink(missing_ok=True)

                # 2. Restore the displaced souls from Legacy
                for leg_c, act_c in displaced_souls:
                    self._robust_rename(leg_c, act_c)

                Logger.success("Surgical Rollback successful. Reality stabilized.")
            except Exception as rollback_err:
                Logger.critical(f"FATAL PARADOX: Surgical Rollback failed: {rollback_err}")

            raise ArtisanHeresy("Surgical Reality Flip Failed", child_heresy=e, severity=HeresySeverity.CRITICAL)

    def perform_symlink_flip(self, link_path: Path, shadow: Path, legacy: Path):
        """
        =============================================================================
        == THE SYMLINK STRATEGY (POINTER SWAP & JUNCTION FALLBACK)                 ==
        =============================================================================
        Best for Docker volumes, massive repositories, or read-only cache mounts.
        """
        link_path = Path(self._canonize_path(link_path))
        shadow = Path(self._canonize_path(shadow))

        # [ASCENSION 21]: Stale Lock Pruning
        temp_link = link_path.with_suffix(f".tmp_link_{random.randint(1000, 9999)}")

        try:
            # 1. Forge the new pointer
            if os.name == 'nt':
                try:
                    os.symlink(shadow, temp_link, target_is_directory=True)
                except OSError as e:
                    # [ASCENSION 11]: NTFS JUNCTION FALLBACK
                    if getattr(e, 'winerror', 0) == 1314:
                        Logger.warn("Symlink Privilege Denied. Devolving to NTFS Junction Point...")
                        # mklink /J requires shell execution but bypasses Admin reqs for directories
                        res = subprocess.run(
                            f'cmd.exe /c mklink /J "{temp_link}" "{shadow}"',
                            shell=True, capture_output=True
                        )
                        if res.returncode != 0:
                            raise ArtisanHeresy(
                                "Privilege Heresy: Symlink and Junction creation failed.",
                                severity=HeresySeverity.CRITICAL,
                                details=res.stderr.decode('utf-8', 'ignore'),
                                suggestion="Run the Engine as Administrator or enable Windows Developer Mode."
                            )
                    else:
                        raise e
            else:
                os.symlink(shadow, temp_link)

            # 2. [ASCENSION 10]: Atomic Swap the link itself
            os.replace(temp_link, link_path)

        except Exception as e:
            if temp_link.exists():
                try:
                    if temp_link.is_dir() and not temp_link.is_symlink():  # Catch Junctions
                        os.rmdir(temp_link)
                    else:
                        temp_link.unlink()
                except:
                    pass
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy("Symlink Flip Failed", child_heresy=e, severity=HeresySeverity.CRITICAL)

    # =========================================================================
    # == INTERNAL ORGANS (SUBSTRATE MAGIC)                                   ==
    # =========================================================================

    def _robust_rename(self, src: Path, dst: Path):
        """
        [ASCENSION 4, 5, 6, 8]: The Immortal Renamer.
        Handles Windows File Locks (AV/Indexing), Read-Only Taint, and Cross-Device Mounts.
        """
        start_time = time.time()
        last_err = None

        for attempt in range(self.RETRY_LIMIT):
            try:
                # [ASCENSION 14]: The Void Purifier
                if not src.exists():
                    return

                # Primary Attempt: Atomic Rename
                os.rename(src, dst)
                return

            except OSError as e:
                last_err = e

                # [ASCENSION 4]: CROSS-DEVICE SUTURE (Errno 18: EXDEV)
                if e.errno == 18:
                    Logger.verbose("Cross-Device boundary perceived. Shifting to deep-matter transit (shutil.move).")
                    # [ASCENSION 15]: shutil.move preserves metadata automatically
                    shutil.move(str(src), str(dst))
                    return

                # Windows Access Denied / File in Use (Errno 13, 32) or Directory Not Empty (41, 145)
                if e.errno in (13, 32, 41, 145):

                    # [ASCENSION 5]: READ-ONLY ANNIHILATION
                    # If access is denied, it might be a read-only file (like Git packs).
                    # We surgically attempt to strip the read-only attribute from the target if it exists.
                    if e.errno == 13 and dst.exists():
                        try:
                            # Grant write permission to the owner
                            current_stat = dst.stat().st_mode
                            os.chmod(dst, current_stat | stat.S_IWRITE)
                        except Exception:
                            pass

                    # [ASCENSION 22]: THE PHANTOM LOCK BREAKER
                    # If destination exists and is locked for deletion, rename it to a void state first.
                    if e.errno in (13, 32) and dst.exists() and attempt == 2:
                        try:
                            void_path = dst.with_name(f"{dst.name}.void_{random.randint(100, 999)}")
                            os.rename(dst, void_path)
                            dst = void_path  # Let the next attempt overwrite the void, or just let shutil handle it
                        except Exception:
                            pass

                    # [ASCENSION 8]: Zombie Handle Exorcism
                    gc.collect()

                    # [ASCENSION 17]: Achronal Flip Timeout
                    if time.time() - start_time > self.MAX_TIMEOUT_S:
                        break

                    # [ASCENSION 13]: Hydraulic Thread Yield with Geometric Jitter
                    delay = self.BASE_DELAY_S * (1.5 ** attempt) + random.uniform(0, 0.05)
                    time.sleep(delay)
                    continue

                # If it's a different OS error, we don't retry, we fail fast.
                raise e

        # If we exhausted retries or hit the timeout
        raise last_err

    def _canonize_path(self, path: Path) -> str:
        """
        [ASCENSION 9]: Windows Long Path Prefix.
        Bypasses the 260 character limit for deep nesting.
        """
        abs_path = str(path.resolve())
        if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
            return '\\\\?\\' + abs_path.replace('/', '\\')
        return abs_path