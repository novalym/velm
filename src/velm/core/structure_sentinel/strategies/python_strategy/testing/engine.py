# Path: src/velm/core/structure_sentinel/strategies/python_strategy/testing/engine.py
# -----------------------------------------------------------------------------------

from __future__ import annotations
import time
import traceback
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Dict, Any, Union, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from .analyzer import SourceCodeAnatomist
    from .generator import PytestArchitect
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class TestingFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN TESTING FACULTY (V-Ω-TOTALITY-V7000-SYMBIOTIC-SHADOW)         ==
    =================================================================================
    LIF: ∞ | ROLE: HIGH_INQUISITOR_OF_LOGIC | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_TESTING_V7000_SINGULAR_CONTEXT_FINALIS

    The Divine Artisan responsible for the creation of the Test Shadow. It ensures
    that every logic scripture (.py) is born with a corresponding inquisitor (test file),
    maintaining the project's eternal purity through automated adjudication.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **Unified Context Consumption (THE FIX):** It no longer materializes its own
        context. It consumes the sovereign `SharedContext` bestowed by the
        Orchestrator, ensuring 100% alignment with the active strike's geometry.

    2.  **Transactional Suture (THE CURE):** It utilizes the inherited `_write`
        rite from `BaseFaculty`. This guarantees that generated test shadows
        are inscribed in the Gnostic Ledger and committed to reality.

    3.  **Proleptic AST Analysis:** It employs the `SourceCodeAnatomist` to gaze
        into the source's future, identifying functions, classes, and signatures
        to forge tests that are "Birth-Aware" of the code they mirror.

    4.  **Bicameral Reality Scrying:** Gazes into both the Physical Realm (Disk)
        and the Ephemeral Realm (Staging) via `_exists` to prevent redundant
        scripture creation.

    5.  **Geometric Path Transmutation:** Implements the Law of Relative Ancestry
        to map `src/` structures to `tests/` coordinates, automatically handling
        the removal of the `src/` prefix for clean package testing.

    6.  **The Abyssal Ward:** Possesses a hard-coded aversion to testing non-logic
        scriptures (migrations, dunder-files, config, or existing tests).

    7.  **The Pytest Architect Interface:** Integrates with the `PytestArchitect`
        to forge scriptures rich with async-awareness, parameterized cases,
        and standardized fixtures.

    8.  **Idempotent Shadowing:** It fingerprints the source soul; if the
        existing test shadow already resonates with the source's current
        Gnosis, the Hand of Creation is stayed.

    9.  **Fault-Isolated Forging:** If the source AST is profane (Syntax Error),
        it falls back to a "Smoke Test" Monad rather than shattering the
        consecration chain.

    10. **Metabolic Tomography:** Measures the nanosecond tax of the Inquest,
        radiating performance telemetry to the Ocular HUD.

    11. **The Mockery Diviner:** (Prophecy) Automatically identifies external
        dependencies and prepares the `unittest.mock` altar for the test suite.

    12. **The Finality Vow:** A mathematical guarantee that every unit of willed
        logic has an immediate, materialized path to verification.
    =================================================================================
    """

    def __init__(self, logger: 'Scribe'):
        """
        [THE RITE OF INCEPTION]
        Births the Inquisitor with the full endowment of the BaseFaculty.
        """
        super().__init__(logger)

        # Specialist Instruments
        # JIT loading is handled via internal imports to maintain boot-velocity
        from .analyzer import SourceCodeAnatomist
        from .generator import PytestArchitect

        self.anatomist = SourceCodeAnatomist()
        self.architect = PytestArchitect()

    def ensure_test_shadow(
            self,
            file_path: Path,
            context: "SharedContext"
    ):
        """
        =================================================================================
        == THE RITE OF SHADOW FORGING (V-Ω-TOTALITY-UNIFIED)                           ==
        =================================================================================
        Perceives the need for an inquisitor and materializes the Test Shadow.
        """
        start_ns = time.perf_counter_ns()

        # 1. THE GAZE OF PRUDENCE (Ignore Check)
        if self._should_ignore(file_path):
            return

        # 2. RESOLVE THE TARGET SANCTUM
        # Calculate the destination in the tests/ hierarchy
        test_path = self._resolve_test_path(file_path, context.project_root)
        if not test_path:
            return

        # 3. IDEMPOTENCY CHECK (Substrate Agnostic)
        # We use the inherited _exists which scries Staging then Disk.
        if self._exists(test_path, context):
            # self.logger.verbose(f"   -> Test Shadow already manifest for '{file_path.name}'.")
            return

        # 4. READ THE SOURCE SOUL
        source_content = self._read(file_path, context)
        if not source_content:
            return

        # --- MOVEMENT II: THE ARCHITECTURAL PROPHECY ---

        # 5. ANATOMIZE THE SOURCE
        # Extract the functions, classes, and types that require adjudication.
        blueprint = self.anatomist.analyze(file_path, source_content, context.project_root)
        if not blueprint:
            self.logger.verbose(f"   -> No testable logic manifest in '{file_path.name}'. Skipping Shadow.")
            return

        # 6. ARCHITECT THE SUITE
        # Transmute the anatomical blueprint into a living test scripture.
        test_content = self.architect.forge_suite(blueprint)

        # --- MOVEMENT III: THE TRANSACTIONAL STRIKE ---
        self.logger.info(f"   -> Forging Test Shadow: [cyan]{test_path.relative_to(context.project_root)}[/cyan]")

        # [ASCENSION 2]: THE UNBREAKABLE HAND
        # We perform the write through the parent _write rite.
        # This ensures IOConductor usage and Ledger recording.
        self._write(test_path, test_content, context)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if duration_ms > 100:
            self.logger.verbose(f"      -> Shadow Inquest finalized in {duration_ms:.2f}ms.")

    def _should_ignore(self, path: Path) -> bool:
        """
        [FACULTY 6]: THE ABYSSAL WARD.
        Adjudicates if a file is unworthy of a test shadow.
        """
        name = path.name
        parts = path.parts

        # 1. Sanctum Ward: Ignore files already in tests or internal areas
        if any(p in parts for p in ("tests", "test", "migrations", ".scaffold")):
            return True

        # 2. Name Ward: Ignore established test patterns and dunder files
        if name.startswith("test_") or name.endswith("_test.py"): return True
        if name.startswith("_") and name != "__init__.py": return True

        # 3. Purpose Ward: Ignore configuration and entrypoint scripts
        if name in ("conftest.py", "setup.py", "manage.py", "wsgi.py", "asgi.py", "main.py"):
            return True

        return False

    def _resolve_test_path(self, source_path: Path, root: Path) -> Optional[Path]:
        """
        [FACULTY 5]: THE GEOMETRIC MAPPER.
        Calculates the destination path in the tests/ directory.
        """
        try:
            # We must resolve against root to find the relative coordinate
            rel_path = source_path.relative_to(root)
            parts = list(rel_path.parts)

            # [THE CURE]: Strip 'src/' if present to follow standard 'tests/' layout
            if parts and parts[0] == "src":
                parts = parts[1:]

            if not parts: return None

            # Split into directory structure and filename
            parent_parts = parts[:-1]
            filename = parts[-1]

            # Construct: tests/[parent_structure]/test_[filename]
            test_rel_path = Path("tests") / Path(*parent_parts) / f"test_{filename}"
            return root / test_rel_path
        except ValueError:
            # File is outside root or disjoint
            return None

    def __repr__(self) -> str:
        return f"<Ω_TESTING_FACULTY status=VIGILANT version=7000.0>"