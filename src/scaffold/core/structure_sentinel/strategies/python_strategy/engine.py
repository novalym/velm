# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/engine.py
# ----------------------------------------------------------------------------------------------------------

import time
import traceback
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Tuple, Callable, Any

from ..base_strategy import BaseStrategy
from .structural.engine import StructuralFaculty
from .semantic.engine import SemanticFaculty
from .frameworks import FrameworkFaculty
from .testing.engine import TestingFaculty

if TYPE_CHECKING:
    from .....core.kernel.transaction import GnosticTransaction


class PythonStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE PYTHON HIVE-MIND (V-Ω-RESILIENT-PIPELINE-ULTIMA)                    ==
    =============================================================================
    LIF: INFINITY

    The Sovereign of the Python Cosmos.
    It orchestrates a pantheon of specialist faculties via a fault-tolerant,
    telemetry-aware pipeline. It ensures that the failure of a single Gnostic
    sense does not blind the entire organism.
    """

    def __init__(self):
        super().__init__("Python")

        # The Faculties are forged at birth
        self.structural = StructuralFaculty(self.logger)
        self.semantic = SemanticFaculty(self.logger)
        self.frameworks = FrameworkFaculty(self.logger)
        self.testing = TestingFaculty(self.logger)

        # The Pipeline Definition
        # (Name, Faculty Method, Requires Source File?)
        self.pipeline: List[Tuple[str, Callable, bool]] = [
            ("Structural Integrity", self.structural.ensure_structure, False),
            ("Semantic Registration", self.semantic.register_symbols, True),
            ("Framework Wiring", self.frameworks.wire_components, True),
            ("Test Mirroring", self.testing.ensure_test_shadow, True),
        ]

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        """
        The Grand Rite of Consecration.
        Dispatches the file to all faculties through the Resilience Ward.
        """
        start_time = time.monotonic()
        self.logger.verbose(f"The Python Hive-Mind gazes upon: [cyan]{file_path.name}[/cyan]")

        # 1. The Gnostic Triage
        # Determine if we are dealing with a source file or a structural entity
        is_source_file = (
                not file_path.is_dir()
                and file_path.suffix == '.py'
                and file_path.name != '__init__.py'
        )

        results = {"success": 0, "skipped": 0, "failed": 0}

        # 2. The Execution Pipeline
        for name, rite, requires_source in self.pipeline:
            # Skip source-only rites for directories or __init__.py
            if requires_source and not is_source_file:
                results["skipped"] += 1
                continue

            # The Resilience Ward
            try:
                rite_start = time.monotonic()
                rite(file_path, project_root, transaction)
                duration = (time.monotonic() - rite_start) * 1000

                # We log only if the rite took significant time or changed state (faculties handle their own success logs)
                # self.logger.verbose(f"   -> {name}: Completed in {duration:.2f}ms")
                results["success"] += 1

            except Exception as e:
                # The Unbreakable Ward: Capture the heresy, log it, but do not halt.
                results["failed"] += 1
                self.logger.warn(f"   -> [bold red]Paradox in {name}:[/bold red] {e}")
                self.logger.verbose(f"      Traceback: {traceback.format_exc()}")

        # 3. The Luminous Summary
        total_duration = (time.monotonic() - start_time) * 1000
        if results["failed"] > 0:
            self.logger.warn(
                f"Consecration complete with warnings in {total_duration:.2f}ms. "
                f"(Success: {results['success']}, Failed: {results['failed']}, Skipped: {results['skipped']})"
            )
        else:
            self.logger.verbose(
                f"Consecration absolute in {total_duration:.2f}ms."
            )