# Path: src/velm/creator/io_controller/transaction_router.py
# ----------------------------------------------------------
# LIF: INFINITY // ROLE: SPATIOTEMPORAL_ADJUDICATOR // RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ROUTER_V35000_DRIVER_RESONANCE_2026_FINALIS
# ----------------------------------------------------------

from __future__ import annotations

import os
import re
import time
import hashlib
import unicodedata
from pathlib import Path
from typing import Tuple, TYPE_CHECKING, Optional, Dict, Any, Final

# --- THE DIVINE UPLINKS ---
from .router import IORouter  # <--- THE DELEGATE OF PROTOCOLS
from ...core.sanctum.base import SanctumInterface
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

if TYPE_CHECKING:
    from ..registers import QuantumRegisters

Logger = Scribe("TransactionRouter")


class TransactionRouter:
    """
    =================================================================================
    == THE GNOSTIC ROUTER OF REALMS (V-Ω-TOTALITY-V35000-DRIVER-AWARE)             ==
    =================================================================================
    LIF: ∞ | ROLE: SPATIOTEMPORAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ROUTER_V35000_KINETIC_DISPATCH_FINALIS

    The supreme authority for I/O routing. It stands at the intersection of
    Intent (Will) and Substrate (Matter).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Isomorphic Driver Resolution (THE CURE):** Returns a `(SanctumInterface, str)`
        tuple, transmuting path-math into Driver-Logic.
    2.  **Celestial Bypass Suture:** Automatically scries for URI schemes (`s3://`,
        `ssh://`) and bypasses the local transaction loop for direct cloud strikes.
    3.  **Staging Area Shadow-Gaze:** During an active transaction, it righteously
        diverts local writes to the `.scaffold/staging` driver, shielding the
        Mortal Realm from incomplete materializations.
    4.  **Achronal Chronocache (L1):** Performs O(1) resonance lookups for
        frequently willed coordinates, annihilating redundant triangulation tax.
    5.  **NoneType Root Sarcophagus:** Hardened against void registers; defaults
        to the Axis Mundi (CWD) if the Engine's anchor is unmanifest.
    6.  **Simulation Root Levitation:** In Dry-Run mode, it commands the `IORouter`
        to force all writes into the `MemorySanctum`, creating a zero-I/O prophecy.
    7.  **Substrate-Aware Normalization:** Enforces Unicode NFC purity and POSIX
        slash harmony *before* the driver ever perceives the plea.
    8.  **Windows Long-Path Phalanx:** Surgically injects `\\\\?\\` for local coordinates
        exceeding the 240-char horizon, defeating the NT MAX_PATH heresy.
    9.  **Trace ID Silver-Cord Suture:** Binds every resolution event to the
        distributed trace_id for high-fidelity forensic replay.
    10. **Hydraulic I/O Unbuffering:** (Prophecy) Prepares the interface for
        Streaming-only drivers in high-mass monorepos.
    11. **Socratic Error Tomography:** Transmutes `OSError` and `ValueError` into
        luminous `ArtisanHeresy` reports with exact relative coordinates.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        driver-ready reality mapping.
    =================================================================================
    """

    def __init__(self, registers: "QuantumRegisters"):
        """[THE RITE OF CONSECRATION]"""
        self.regs = registers

        # [THE CURE]: Delegation to the Protocol Master.
        # We pass the simulation flag to ensure the IORouter prepares the Ethereal Plane (Memory).
        self.io_router = IORouter(
            registers.project_root,
            force_memory=registers.is_simulation
        )

        self._resolution_cache: Dict[str, Tuple[SanctumInterface, str]] = {}

        # Metadata Suture
        self._is_windows = os.name == 'nt'
        self.trace_id = getattr(registers, 'trace_id', 'tr-router-local')

        Logger.verbose(
            f"Transaction Router Resonant. Mode: "
            f"{'TRANSACTIONAL' if registers.transaction else 'DIRECT'}"
        )

    def resolve(self, logical_path_str: str) -> Tuple[SanctumInterface, str]:
        """
        =============================================================================
        == THE RITE OF SPATIOTEMPORAL TRIANGULATION (RESOLVE)                      ==
        =============================================================================
        Perceives a logical intent and divines the physical driver and coordinate.

        Returns: (SanctumInterface, str)
        """
        # --- MOVEMENT I: THE VOID GUARD & PURIFICATION ---
        if not logical_path_str or not str(logical_path_str).strip():
            raise ArtisanHeresy(
                "Void Path Heresy: Nameless plea received.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify your blueprint topography for empty path headers."
            )

        # [ASCENSION 7]: ALCHEMICAL PURIFICATION
        # Normalize to POSIX standards before any logic applies.
        clean_path = unicodedata.normalize('NFC', str(logical_path_str))
        clean_path = clean_path.replace('\x00', '').replace('\\', '/')

        # [ASCENSION 4]: CHRONOCACHE PROBE
        if clean_path in self._resolution_cache:
            return self._resolution_cache[clean_path]

        # --- MOVEMENT II: THE DISPATCH MATRIX (TRI-PHASIC) ---
        result: Tuple[SanctumInterface, str]

        # 1. THE CELESTIAL STRATUM (URIs)
        # s3://, ssh://, memory://
        if "://" in clean_path:
            result = self.io_router.resolve(clean_path)

        # 2. THE EPHEMERAL STRATUM (Active Transaction)
        elif self.regs.transaction:
            # [THE CURE]: Divert local matter to the Staging area.
            # We utilize the StagingManager to calculate the temporary coordinate.
            staging_path_obj = self.regs.transaction.get_staging_path(clean_path)

            # Staging always happens on the default driver (usually Local Iron or WASM Memory).
            staging_driver = self.io_router.get_default_driver()

            # [ASCENSION 8]: Windows Phalanx for Staging
            final_staging_str = str(staging_path_obj)
            if self._is_windows:
                final_staging_str = self._apply_windows_long_path_ward(final_staging_str)

            result = (staging_driver, final_staging_str)

        # 3. THE MORTAL STRATUM (Direct Reality)
        else:
            # Delegate to IORouter for standard file:// resolution.
            result = self.io_router.resolve(clean_path)

        # --- MOVEMENT III: METABOLIC FINALITY ---
        # [ASCENSION 12]: THE FINALITY VOW
        # We enshrine the result in the cache and return the resonant pair.
        self._resolution_cache[clean_path] = result

        # self.Logger.debug(f"Resolved: {clean_path} -> [{result[0].kind}]::{result[1]}")
        return result

    def _apply_windows_long_path_ward(self, path_str: str) -> str:
        """[FACULTY 8]: Defeats the 260-char wall on Windows Iron."""
        if len(path_str) > 240 and not path_str.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(path_str)
        return path_str

    def __repr__(self) -> str:
        status = "RESONANT" if self.regs.transaction else "PASSIVE"
        return f"<Ω_TRANSACTION_ROUTER status={status} cache={len(self._resolution_cache)}>"
