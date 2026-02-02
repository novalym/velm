# Path: scaffold/artisans/distill/core/oracle/forensics/engine.py
# ---------------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, List, Optional

from .contracts import ForensicReport, Indictment
from .detectives import StructureDetective, TextDetective
from .....logger import Scribe

Logger = Scribe("ForensicInquisitor")


class ForensicInquisitor:
    """
    =============================================================================
    == THE FORENSIC INQUISITOR (V-Ω-FACADE-ULTIMA)                             ==
    =============================================================================
    The Sovereign Interface for the Forensic Module.
    It orchestrates the Detectives to analyze the input and updates the
    Oracle's scoring system.
    """

    def __init__(self, silent: bool = False):
        self.silent = silent

    def gaze(self, problem_input: str, file_scores: Dict[str, int]) -> Optional[str]:
        """
        The Grand Rite of Forensic Analysis.

        Args:
            problem_input: Raw string, file path, or JSON.
            file_scores: The Oracle's central scoring map (relative POSIX paths).

        Returns:
            The primary error message found (if any).
        """
        if not problem_input:
            return None

        # 1. Ingest Evidence
        raw_evidence = self._ingest(problem_input)

        # 2. Summon Detectives
        # We start by hunting for error strings within the evidence
        error_strings = []

        # Is it JSON?
        try:
            data = json.loads(raw_evidence)
            # If valid JSON, use StructureDetective to find relevant strings
            error_strings = StructureDetective.hunt(data)
        except json.JSONDecodeError:
            # If raw text, use it directly
            error_strings = [raw_evidence]

        # 3. Analyze Strings
        report = ForensicReport(raw_evidence_size=len(raw_evidence))

        for text_block in error_strings:
            # Find Paths and Lines
            new_indictments = TextDetective.investigate(text_block, Path("."))  # Root is relative
            report.indictments.extend(new_indictments)

            # Find Error Header (only keep the first/most prominent one)
            if not report.primary_error:
                report.primary_error = TextDetective.extract_error_header(text_block)

        # 4. Update Oracle Scores
        self._apply_indictments(report.indictments, file_scores)

        return report.primary_error

    def _ingest(self, input_str: str) -> str:
        """Reads file if input is a valid path, otherwise returns string."""
        # Simple heuristic check for file path
        if len(input_str) < 255:
            p = Path(input_str)
            if p.exists() and p.is_file():
                try:
                    return p.read_text(encoding='utf-8', errors='replace')
                except Exception:
                    pass
        return input_str

    def _apply_indictments(self, indictments: List[Indictment], file_scores: Dict[str, int]):
        """
        Maps found paths to the Project's canonical file list.
        """
        for indictment in indictments:
            # Normalize the indicted path to match file_scores keys
            # file_scores keys are relative POSIX paths (e.g. "src/main.py")

            indicted_clean = str(indictment.path).replace('\\', '/')

            # Fuzzy Matcher: Find if the indicted path ends with a known project file
            # e.g., Indicted: "/abs/path/to/project/src/utils.py"
            #       Known: "src/utils.py"
            #       Match!

            best_match = None

            # 1. Exact Match
            if indicted_clean in file_scores:
                best_match = indicted_clean
            else:
                # 2. Suffix Match
                for known_path in file_scores.keys():
                    if indicted_clean.endswith(known_path) or known_path.endswith(indicted_clean):
                        best_match = known_path
                        break

            if best_match:
                # Additive Scoring: If a file appears multiple times, it is very guilty.
                current_score = file_scores[best_match]
                new_score = min(100, current_score + indictment.score)
                file_scores[best_match] = new_score

                if not self.silent:
                    Logger.verbose(f"   -> Indicted [red]{best_match}[/red] (+{indictment.score}): {indictment.reason}")