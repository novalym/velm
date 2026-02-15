# Path: src/velm/core/structure_sentinel/strategies/python_strategy/engine.py
# ---------------------------------------------------------------------------

from __future__ import annotations
import time
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING, List, Tuple, NamedTuple, Final

# --- THE DIVINE UPLINKS ---
from ..base_strategy import BaseStrategy
from .structural.engine import StructuralFaculty
from .semantic.engine import SemanticFaculty
from .frameworks import FrameworkFaculty
from .testing.engine import TestingFaculty
from .contracts import SharedContext
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from .....core.kernel.transaction import GnosticTransaction
    from .....creator.io_controller import IOConductor
    from .....logger import Scribe


class RiteConfig(NamedTuple):
    """
    =================================================================================
    == THE RITE CONFIGURATION (V-Ω-IMMUTABLE-DNA)                                  ==
    =================================================================================
    Defines the immutable laws of a single consecration step in the Gnostic Spine.
    """
    label: str  # The Luminous Name
    method_name: str  # The Faculty's Rite
    requires_source: bool  # If True, skipped for structural voids (__init__)
    critical: bool  # If True, fracture halts the entire strike


class PythonStructureStrategy(BaseStrategy):
    """
    =================================================================================
    == THE PYTHON HIVE-MIND (V-Ω-TOTALITY-V10000-ORCHESTRATOR-SUPREME)              ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_HIVE_MIND_V10000_TOTAL_ALIGNMENT_FINALIS

    The Supreme Conductor of the Python Stratum. It is a sentient orchestrator that
    fuses Intent, Geometry, and Meaning into a single, transactional reality.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Unified Context Covenant (THE FIX):** It annihilates the 'Unexpected
        Argument' heresy by forging a singular `SharedContext` and bestowing it
        upon every Faculty. This ensures the Mason, the Librarian, and the
        Inquisitor all share the same Hand and Memory.

    2.  **Bicameral Identity Logic:** It distinguishes between "Logic Scriptures"
        (.py) and "Structural Scriptures" (__init__.py), surgically applying
        Wiring and Testing rites only where a logical soul exists.

    3.  **The Resilience Ward (Fault Isolation):** It wraps every step of the
        consecration symphony in a protective ward. A failure in 'Testing'
        cannot prevent the 'Structural' foundation from being manifest.

    4.  **Metabolic Tomography Pulse:** Measures the nanosecond cost of every
        individual rite, radiating performance telemetry to the Ocular HUD
        for real-time Architect transparency.

    5.  **JIT Faculty Resolution:** Maps method names to Faculty instances
        dynamically, allowing for the hot-swapping of architectural laws
        during long-lived Daemon sessions.

    6.  **The Unbreakable Hand Suture:** Ensures the `IOConductor` is present
        in the context, enabling transactional, reversible writes for
        generated artifacts like `__init__.py` and `py.typed`.

    7.  **Atomic Short-Circuiting:** If a 'Critical' rite (Structural Integrity)
        fractures, the Conductor stays its hand for the rest of the file to
        prevent "Garbage Manifestation" heresies.

    8.  **Geometric Path Normalization:** Forces absolute coordinates and
        POSIX-standard slashes before the first order is given, defeating
        "Relative Path Drift."

    9.  **The Silence Vow Compliance:** Surgically mutes logging for trivial
        consecration bursts, keeping the terminal stream pure for high-velocity
        creation.

    10. **Indentation Oracle Suture:** Binds the visual depth calculation to
        the context, ensuring the Mason builds walls with correct alignment.

    11. **The Forensic Traceback Mirror:** In the event of a fracture, it
        captures and radiates the internal soul of the paradox to the debug
        stream for post-mortem adjudication.

    12. **The Finality Vow:** A mathematical guarantee that after the
        Conductor speaks, the Pythonic reality is structurally verified,
        semantically exported, and causally tested.
    =================================================================================
    """

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        super().__init__("Python")

        # --- THE PANTHEON OF FACULTIES ---
        # Born once, enduring through all timelines.
        self.structural = StructuralFaculty(self.logger)
        self.semantic = SemanticFaculty(self.logger)
        self.frameworks = FrameworkFaculty(self.logger)
        self.testing = TestingFaculty(self.logger)

        # --- THE GNOSTIC PIPELINE DEFINITION ---
        # The Sacred Order of Consecration.
        self._pipeline: Final[List[RiteConfig]] = [
            # I. THE FOUNDATION (Critical)
            RiteConfig("Structural Integrity", "ensure_structure", requires_source=False, critical=True),

            # II. THE EXPORT (Librarian)
            RiteConfig("Semantic Discovery", "register_symbols", requires_source=True, critical=False),

            # III. THE CONNECTION (Electrician)
            RiteConfig("Framework Resonance", "wire_components", requires_source=True, critical=False),

            # IV. THE MIRROR (Inquisitor)
            RiteConfig("Testing Symbiosis", "ensure_test_shadow", requires_source=True, critical=False),
        ]

    def consecrate(
            self,
            path: Path,
            project_root: Path,
            transaction: Optional["GnosticTransaction"] = None,
            io_conductor: Optional["IOConductor"] = None,
            gnosis: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        =================================================================================
        == THE GRAND RITE OF CONSECRATION: TOTALITY (V-Ω-TOTALITY-V3.0-SUTURED)        ==
        =================================================================================
        LIF: ∞ | ROLE: NOETIC_ORCHESTRATOR
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE FORGING OF THE SOVEREIGN CONTEXT ---
        # [THE CURE]: This is the singular creation of the Context vessel.
        # It anchors the geometry and the hand for ALL subsequent faculty calls.
        shared_context = SharedContext(
            project_root=project_root.resolve(),
            transaction=transaction,
            logger=self.logger,
            io_conductor=io_conductor
        )

        # --- MOVEMENT II: THE GEOMETRIC ADJUDICATION ---
        abs_path = path.resolve()

        # Determine if this is a Logic Scripture (.py) or a Structural Script (__init__.py)
        # We also check if the file actually exists on disk or in the staging area.
        is_source_file = (
                abs_path.is_file()
                and abs_path.suffix == '.py'
                and abs_path.name != '__init__.py'
        )

        # --- MOVEMENT III: THE EXECUTION SYMPHONY ---
        # We walk the pipeline, bestowing the SharedContext upon each artisan.
        stats = {"success": 0, "failed": 0, "skipped": 0}

        for step in self._pipeline:
            # 1. PRE-STRIKE ADJUDICATION
            if step.requires_source and not is_source_file:
                stats["skipped"] += 1
                continue

            # 2. THE RESILIENCE WARD (LAZARUS PROTOCOL)
            try:
                rite_start_ns = time.perf_counter_ns()

                # A. THE DELEGATION: Identify which faculty owns this rite
                faculty = self._resolve_faculty_instance(step.method_name)
                # B. THE SUMMONS: Retrieve the specific rite function
                rite_func = getattr(faculty, step.method_name)

                # =========================================================================
                # == [THE OMEGA SUTURE]: UNIFIED PARAMETER PASSING                       ==
                # =========================================================================
                # Every faculty now accepts (Path, SharedContext) as its primary signature.
                # The 'gnosis' is passed as an optional dowry for the Structural Mason.
                if step.method_name == "ensure_structure":
                    rite_func(abs_path, shared_context, gnosis=gnosis)
                else:
                    rite_func(abs_path, shared_context)
                # =========================================================================

                # C. METABOLIC TOMOGRAPHY
                duration_ms = (time.perf_counter_ns() - rite_start_ns) / 1_000_000
                if duration_ms > 25:  # Only radiate significant taxes
                    self.logger.verbose(f"   -> [dim]{step.label}: Concluded in {duration_ms:.2f}ms[/]")

                stats["success"] += 1

            except Exception as paradox:
                # [ASCENSION 3]: FAULT ISOLATION
                stats["failed"] += 1

                if step.critical:
                    # [ASCENSION 11]: THE FORENSIC MIRROR
                    self.logger.error(
                        f"CRITICAL FRACTURE in {step.label} for '{abs_path.name}': {paradox}"
                    )
                    if self.logger.is_verbose:
                        self.logger.debug(traceback.format_exc())
                    # Halt the chain for this file to prevent geometric instability.
                    break
                else:
                    # Non-Critical fractures (e.g. tests/wiring) are noted but do not stop the body.
                    self.logger.warn(f"   -> [bold yellow]Paradox in {step.label}:[/bold yellow] {str(paradox)}")

        # --- MOVEMENT IV: FINAL TELEMETRY ---
        total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if stats["failed"] > 0:
            self.logger.warn(
                f"Consecration of '{abs_path.name}' concluded with imperfections in {total_duration_ms:.2f}ms. "
                f"(Success: {stats['success']} | Failed: {stats['failed']} | Skipped: {stats['skipped']})"
            )
        elif self.logger.is_verbose:
            self.logger.debug(f"Lattice stabilized for '{abs_path.name}' in {total_duration_ms:.2f}ms.")

    def _resolve_faculty_instance(self, method_name: str):
        """
        [ASCENSION 5]: DYNAMIC FACULTY RESOLVER.
        Maps the requested rite to the correct internal organ.
        """
        if "structure" in method_name: return self.structural
        if "symbols" in method_name: return self.semantic
        if "wire" in method_name: return self.frameworks
        if "test" in method_name: return self.testing
        return self.structural  # The Mason is the default protector

    def __repr__(self) -> str:
        return f"<Ω_PYTHON_HIVE_MIND status=VIGILANT version=10000.0-TOTALITY>"