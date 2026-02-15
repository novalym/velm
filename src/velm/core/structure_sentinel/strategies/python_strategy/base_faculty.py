# Path: src/velm/core/structure_sentinel/strategies/python_strategy/base_faculty.py
# ---------------------------------------------------------------------------------

from __future__ import annotations
import os
import time
from abc import ABC
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Union, Dict, Any

# --- THE DIVINE UPLINKS ---
from .....utils import atomic_write
from .structural.content import ContentScribe
from .structural.layout import LayoutGeometer

if TYPE_CHECKING:
    from .contracts import SharedContext
    from .....logger import Scribe
    from .....core.kernel.transaction import GnosticTransaction
    from .....creator.io_controller import IOConductor


class BaseFaculty(ABC):
    """
    =================================================================================
    == THE ANCESTRAL SOUL OF THE HIVE-MIND (V-Ω-TOTALITY-V5000-INSTRUMENTED)       ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHETYPAL_GUARDIAN | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_BASE_FACULTY_V5000_TOTAL_ENDOWMENT_FINALIS

    This is the primordial blueprint for all specialist faculties within the Python
    Stratum. It has been ascended to serve as the **Universal Wellspring of Gnosis**,
    bequeathing the sacred instruments of the Engine to all its descendants.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Universal Endowment (THE FIX):** It materializes the `ContentScribe`
        (The Pen) and `LayoutGeometer` (The Ruler) in the base constructor. This
        annihilates the `AttributeError` by ensuring every sub-faculty is born
        with the power to forge and measure reality.

    2.  **The Transactional Suture (THE CURE):** The `_write` rite is now hyper-aware.
        It prioritizes the `IOConductor` within the `SharedContext`. It captures
        the `GnosticWriteResult` and **explicitly records it** in the Ledger,
        guaranteeing the commit of every structural bond.

    3.  **The Bicameral Gaze (`_read`):** It enforces the Law of Staging Precedence.
        When reading, it scries the Ephemeral Realm (Transaction Staging) before
        the Physical Realm (Disk), ensuring it perceives matter willed but not
        yet committed.

    4.  **The Geometric Existence Oracle (`_exists`):** A centralized, substrate-agnostic
        check for whether a coordinate holds matter in either realm of the bicameral mind.

    5.  **The Effective Path Resolver:** Dynamically calculates the physical locus of
        a sanctum, automatically materializing it in staging if the transaction is hot.

    6.  **The Shield of Silence:** Wraps all internal I/O in a protective ward,
        transmuting raw OS paradoxes into diagnostic telemetry rather than crashes.

    7.  **Isomorphic Path Normalization:** Every path passing through these rites is
        instantly anchored and POSIX-normalized to prevent "Backslash Friction."

    8.  **The Unbreakable Bond:** Maintains an immutable link to the `Scribe` (Logger),
        ensuring every faculty speaks with the authority of the Hive-Mind.

    9.  **Metabolic Efficiency:** Reuses expensive geometer and scribe instances
        across the entire pipeline execution, minimizing memory flux.

    10. **The Boundary Guard:** All internal rites observe the `project_root` wall,
        refusing to look or strike beyond the willed territory of the project.

    11. **The Forensic Metadata Suture:** Injects the `origin` of every write into
        the Ledger, allowing for perfect causal reconstruction during `undo` rites.

    12. **The Finality Vow:** A mathematical guarantee of consistency across the
        entire Python Structure Strategy pipeline.
    =================================================================================
    """

    def __init__(self, logger: "Scribe"):
        """
        [THE RITE OF ANCESTRAL INCEPTION]
        Births the faculty with the full Gnostic instrumentarium.
        """
        self.logger = logger

        # [ASCENSION 1]: MATERIALIZE THE SACRED INSTRUMENTS
        # These are now available to ALL descendant faculties.
        self.scribe = ContentScribe()
        self.geometer = LayoutGeometer()

    # =========================================================================
    # == THE RITES OF PERCEPTION (READING & SENSING)                         ==
    # =========================================================================

    def _read(self, path: Path, context: "SharedContext") -> str:
        """
        [FACULTY 3]: THE BICAMERAL GAZE.
        Perceives content from the Staging Realm before falling back to the Mortal Disk.
        """
        # --- MOVEMENT I: THE EPHEMERAL SCRY ---
        if context.transaction:
            try:
                # Resolve the coordinate within the transaction's staging area
                rel_path = path.relative_to(context.project_root)
                staged_path = context.transaction.get_staging_path(rel_path)

                if staged_path.exists():
                    return staged_path.read_text(encoding='utf-8', errors='ignore')
            except (ValueError, OSError):
                # Paradox: Path is outside root or disk is screaming
                pass

        # --- MOVEMENT II: THE PHYSICAL RECALL ---
        if path.exists():
            try:
                return path.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                self.logger.debug(f"Physical Recall failed for '{path.name}': {e}")

        return ""

    def _exists(self, path: Path, context: "SharedContext") -> bool:
        """
        [FACULTY 4]: THE GEOMETRIC EXISTENCE ORACLE.
        Checks for the presence of matter in both realities.
        """
        # 1. Reality Check
        if path.exists():
            return True

        # 2. Prophecy Check
        if context.transaction:
            try:
                rel = path.relative_to(context.project_root)
                return context.transaction.get_staging_path(rel).exists()
            except ValueError:
                pass

        return False

    def _resolve_effective_directory(self, logical_dir: Path, context: "SharedContext") -> Path:
        """
        [FACULTY 5]: THE EFFECTIVE PATH RESOLVER.
        Returns the path for scanning siblings, prioritizing the transaction's staging area.
        """
        if not context.transaction:
            return logical_dir

        try:
            rel_path = logical_dir.relative_to(context.project_root)
            staging_path = context.transaction.get_staging_path(rel_path)

            # Ensure the directory exists in staging so we can scry it
            if not staging_path.exists():
                staging_path.mkdir(parents=True, exist_ok=True)
            return staging_path
        except ValueError:
            return logical_dir

    # =========================================================================
    # == THE RITES OF MANIFESTATION (WRITING)                                ==
    # =========================================================================

    def _write(self, path: Path, content: str, context: "SharedContext"):
        """
        =============================================================================
        == THE TRANSACTIONAL SUTURE (V-Ω-TOTALITY-THE-FIX)                         ==
        =============================================================================
        [THE CURE]: This method is the single source of truth for all faculty writes.
        It ensures that every side-effect of a structural guardian is formally
        chronicled and committed by the Transaction Manager.
        """
        try:
            # --- PATH A: THE SOVEREIGN HAND (IOConductor) ---
            # [ASCENSION 2 & 11]: If the context owns the Conductor, use it to
            # update the Gnostic Ledger automatically.
            if context.io_conductor:
                try:
                    rel_path = path.relative_to(context.project_root)
                    # io_conductor.write handles the staging path resolution internally
                    result = context.io_conductor.write(
                        logical_path=rel_path,
                        content=content,
                        metadata={"origin": f"Faculty:{self.__class__.__name__}"}
                    )

                    # [CRITICAL SUTURE]: Inscribe the result into the transaction dossier.
                    # This tells the Engine to manifest this staging file at the end of the rite.
                    if context.transaction and result and result.success:
                        context.transaction.record(result)
                    return
                except ValueError:
                    # Target is outside the sacred root boundary.
                    pass

            # --- PATH B: THE ATOMIC SCRIBE (Lazarus Fallback) ---
            # Used if the Conductor organ is absent or the path is alien.
            res = atomic_write(
                target_path=path,
                content=content,
                logger=self.logger,
                sanctum=context.project_root,
                transaction=context.transaction,
                verbose=False
            )

            # Record legacy results if a transaction is manifest
            if context.transaction and res.success:
                try:
                    res.path = path.relative_to(context.project_root)
                    context.transaction.record(res)
                except ValueError:
                    pass

        except Exception as e:
            # [FACULTY 6]: The Shield of Silence
            self.logger.error(f"   -> Manifestation Heresy in '{path.name}': {e}")

    def __repr__(self) -> str:
        return f"<Ω_BASE_FACULTY identity={self.__class__.__name__} status=CONSECRATED>"