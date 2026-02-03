# Path: scaffold/symphony/polyglot/adjudicators.py

"""
=================================================================================
== THE SACRED GRIMOIRE OF FOREIGN TRUTH (V-Ω-ETERNAL. THE BOOK OF ADJUDICATORS) ==
=================================================================================
This scripture contains the living Gnosis that teaches the Symphony Conductor
how to perceive the soul of truth within the profane output of foreign rites.
Each artisan herein is a specialist, a Gnostic translator for a specific tongue.
=================================================================================
"""
import re
from typing import List, Dict, Callable

from ...contracts.symphony_contracts import Reality


class ForeignAdjudicationResult:
    """A sacred vessel for the adjudicated truth of a single foreign test."""

    def __init__(self, is_pure: bool, reason: str, source: str = "Unknown"):
        self.is_pure = is_pure
        self.reason = reason
        self.source = source


def pytest_adjudicator(reality: Reality) -> List[ForeignAdjudicationResult]:
    """
    =================================================================================
    == THE GNOSTIC INQUISITOR FOR PYTEST (LIF: INFINITY)                           ==
    =================================================================================
    This divine artisan gazes upon the raw output of a pytest rite and transmutes
    it into a pure list of Gnostic Adjudication Vessels.
    =================================================================================
    """
    results: List[ForeignAdjudicationResult] = []
    summary_line_found = False

    # Gaze for individual test results (the final character on the line)
    # This is a humble Gaze, a future ascension could parse the full verbose output.
    for line in reality.output.splitlines():
        stripped_line = line.strip()
        if not stripped_line: continue

        # Heuristic for test file lines: [ 25%] ... test_file.py::test_name
        match = re.search(r'^(?:\[\s*\d+%\s*\]\s*)?([\w\/\\]+\.py::\w+)\s*([.FEsxX])', stripped_line)
        if match:
            test_name, status = match.groups()
            if status == '.':
                results.append(ForeignAdjudicationResult(is_pure=True, reason=test_name, source="pytest"))
            elif status in 'FExsX':
                # For now, we capture a generic failure. A deeper Gaze could find the specific error line.
                results.append(
                    ForeignAdjudicationResult(is_pure=False, reason=f"{test_name} - FAILED", source="pytest"))

        if "===" in stripped_line and ("failed" in stripped_line or "passed" in stripped_line):
            summary_line_found = True

    # Final Adjudication: If no structured results were found, judge the whole rite.
    if not results and summary_line_found:
        if "failed" in reality.output or reality.returncode != 0:
            results.append(
                ForeignAdjudicationResult(is_pure=False, reason="The pytest rite proclaimed a failure in its summary.",
                                          source="pytest"))
        else:
            results.append(
                ForeignAdjudicationResult(is_pure=True, reason="The pytest rite proclaimed universal purity.",
                                          source="pytest"))

    return results


# The One True Grimoire, extensible for all future tongues.
ADJUDICATOR_GRIMOIRE: Dict[str, Callable[[Reality], List[ForeignAdjudicationResult]]] = {
    "pytest": pytest_adjudicator,
    # Future ascensions will add "jest", "go_test", etc.
}