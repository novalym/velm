# Path: src/velm/core/kernel/transaction/volume_shifter/shifter/swap.py
# ---------------------------------------------------------------------

import os
import time
import stat
import shutil
import signal
from pathlib import Path
from typing import List, Tuple

from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .immunity import ImmunityMatrix
from .robust_rename import AtomicRenamer


class ContentWeaver:
    """
    =================================================================================
    == THE SURGICAL CONTENT WEAVER (V-Ω-TOTALITY-V64-NON-DESTRUCTIVE)              ==
    =================================================================================
    The logic engine that weaves the Shadow volume into the Active reality.
    """

    def __init__(self, logger, immunity: ImmunityMatrix, renamer: AtomicRenamer, root: Path, is_wasm: bool):
        self.Logger = logger
        self.immunity = immunity
        self.renamer = renamer
        self.root = root
        self.is_wasm = is_wasm

    def surgical_content_swap(self, active: Path, shadow: Path, legacy: Path, tx_id: str, force: bool):
        """
        [THE MANIFESTO]
        It iterates over the SHADOW (The Will). It only touches the ACTIVE reality
        if the Shadow demands that coordinate.
        """
        legacy.mkdir(parents=True, exist_ok=True)

        displaced_souls: List[Tuple[Path, Path]] = []  # [(LegacyPath, ActivePath)]
        ascended_souls: List[Path] = []  # [ActivePath]
        processed_count = 0

        self._resonate_event("SURGICAL_WEAVE_INIT", "KINETIC_EVENT", "#a855f7")

        original_sigint = None
        if not self.is_wasm:
            try:
                original_sigint = signal.getsignal(signal.SIGINT)
                signal.signal(signal.SIGINT, signal.SIG_IGN)
            except (ValueError, AttributeError):
                pass

        try:
            if not shadow.exists():
                return

            for shard in list(shadow.iterdir()):
                target_active = active / shard.name
                target_legacy = legacy / shard.name

                # =========================================================================
                # == [THE CURE]: THE ABSOLUTE IMMUNITY LIFT                              ==
                # =========================================================================
                # If the path is protected (like `.git`), we do NOT overwrite it if it exists.
                # BUT if it is UNMANIFEST (does not exist), we lift the immunity and allow
                # the Shadow Volume to materialize it natively.
                if self.immunity.is_immune(target_active) and not force:
                    if not target_active.exists():
                        self.Logger.verbose(
                            f"   -> Immunity Lifted: Holy Ground '{shard.name}' is unmanifest. Permitting inception.")
                    else:
                        self.Logger.verbose(
                            f"   -> Warded: Skipping materialization of '{shard.name}' over Holy Ground.")
                        continue

                processed_count += 1
                if processed_count % 10 == 0:
                    time.sleep(0)  # Metabolic Yield

                # --- CASE I: DIRECTORY FUSION ---
                if shard.is_dir() and not shard.is_symlink():
                    if target_active.exists() and target_active.is_dir():
                        self.Logger.verbose(f"   -> Fusing Sanctum: [dim]{shard.name}/[/dim]")
                        self.surgical_content_swap(target_active, shard, target_legacy, tx_id, force)
                        continue

                    if target_active.exists() and target_active.is_file():
                        self.renamer.robust_rename(target_active, target_legacy)
                        displaced_souls.append((target_legacy, target_active))

                # --- CASE II: SCRIPTURE COLLISION ---
                elif target_active.exists():
                    try:
                        if target_active.is_file():
                            try:
                                mode = os.stat(str(target_active)).st_mode
                                os.chmod(str(target_active), mode | stat.S_IWRITE)
                            except:
                                pass

                        self.Logger.verbose(f"   -> Displacing Collision: {shard.name} -> [Legacy]")
                        self.renamer.robust_rename(target_active, target_legacy)
                        displaced_souls.append((target_legacy, target_active))

                    except (PermissionError, OSError) as e:
                        # Recursive Devolution
                        if target_active.is_dir():
                            self.Logger.verbose(f"   -> Locus '{shard.name}' locked. Attempting Atomic Dissolution...")
                            self.surgical_content_swap(target_active, shard, target_legacy, tx_id, force)
                            continue
                        else:
                            raise e

                # --- CASE III: MATERIALIZATION ---
                try:
                    self.renamer.robust_rename(shard, target_active)
                    ascended_souls.append(target_active)
                except Exception as materialization_fracture:
                    self.Logger.error(f"   -> Ascension Fracture for '{shard.name}': {materialization_fracture}")
                    raise materialization_fracture

            self._resonate_event("SWAP_RESONANT", "STATUS_UPDATE", "#64ffda")
            return

        except Exception as catastrophic_paradox:
            self.Logger.critical(
                f"[{tx_id[:8]}] Weave Fractured: {catastrophic_paradox}. Initiating Resilient Reversal.")
            self._resonate_event("REVERSING_ENTROPY", "FRACTURE_ALERT", "#f59e0b")

            try:
                for shard in ascended_souls:
                    if shard.exists():
                        if shard.is_dir() and not shard.is_symlink():
                            shutil.rmtree(str(shard), ignore_errors=True)
                        else:
                            shard.unlink(missing_ok=True)

                restored_count = 0
                for legacy_shard, active_locus in reversed(displaced_souls):
                    if not legacy_shard.exists(): continue
                    try:
                        try:
                            os.chmod(str(legacy_shard), os.stat(str(legacy_shard)).st_mode | stat.S_IWRITE)
                        except:
                            pass

                        self.renamer.robust_rename(legacy_shard, active_locus)
                        restored_count += 1
                    except Exception as restore_err:
                        self.Logger.error(f"   -> Resurrection failed for '{active_locus.name}': {restore_err}")

                self.Logger.success(f"[{tx_id[:8]}] Rollback Concluded. {restored_count} soul(s) returned to Reality.")
            except Exception as meta_fracture:
                self.Logger.critical(f"META-HERESY: Rollback itself fractured: {meta_fracture}")

            clean_legacy_str = str(legacy).replace('\\\\?\\', '')
            clean_root_str = str(self.root).replace('\\\\?\\', '')

            try:
                display_path = Path(clean_legacy_str).relative_to(Path(clean_root_str))
            except ValueError:
                display_path = Path(clean_legacy_str)

            raise ArtisanHeresy(
                "Surgical Reality Weave Failed",
                child_heresy=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL,
                details=f"Reality stabilized via rollback. Transfigured shards preserved in: {display_path}"
            )

        finally:
            if original_sigint is not None and not self.is_wasm:
                try:
                    signal.signal(signal.SIGINT, original_sigint)
                except (ValueError, AttributeError):
                    pass

    def _resonate_event(self, label: str, type_hint: str, color: str):
        """Haptic HUD integration helper."""
        pass  # Hooked dynamically by KineticShifter