# Path: scaffold/core/guardian/sentry.py
# --------------------------------------

from pathlib import Path
from typing import List, Optional

from .contracts import SentinelVerdict, ThreatLevel, SecurityViolation
from .wards.filesystem import FilesystemWard
from .wards.syntax import SyntaxWard
from .wards.semantic import SemanticWard
from ...contracts.heresy_contracts import GuardianHeresy, HeresyThreatLevel


class GnosticSentry:
    """
    =================================================================================
    == THE GNOSTIC SENTRY (V-Ω-CITADEL-COMMANDER)                                  ==
    =================================================================================
    LIF: ∞

    The Commander of the Citadel. It receives a command, summons the Wards, aggregates
    their judgments, and issues a Final Verdict. If the verdict is HERESY, it raises
    the `GuardianHeresy` to halt the Symphony.
    """

    def __init__(self):
        self.syntax_ward = SyntaxWard()
        self.semantic_ward = SemanticWard()
        # Filesystem ward needs context (root), so we instantiate it per adjudication
        # or pass root to the method. Passing root to method is cleaner for stateless Sentry.

    def judge(self, command: str, sanctum: Path, line_num: int = 0) -> SentinelVerdict:
        """
        The Private Rite of Judgment. Returns a Verdict object.
        """
        violations = []
        fs_ward = FilesystemWard(sanctum)

        # 1. Syntax Ward
        v = self.syntax_ward.adjudicate(command, line_num)
        if v: violations.append(v)

        # 2. Semantic Ward
        v = self.semantic_ward.adjudicate(command, line_num)
        if v: violations.append(v)

        # 3. Filesystem Ward
        # We must extract potential paths from the command tokens.
        # This is heuristic.
        import shlex
        try:
            tokens = shlex.split(command)
            for token in tokens[1:]:  # Skip verb
                # Heuristic: If it looks like a path or has path separators
                if '/' in token or '\\' in token or token == '..':
                    v = fs_ward.adjudicate(token, line_num)
                    if v: violations.append(v)
        except:
            pass  # Syntax ward already caught parsing errors

        # Calculate Score
        total_threat = 0
        for v in violations:
            total_threat = max(total_threat, v.threat_level.value)

        allowed = total_threat < ThreatLevel.HIGH.value

        return SentinelVerdict(
            allowed=allowed,
            score=total_threat,
            violations=violations
        )

    def adjudicate(self, command: str, sanctum: Path, line_num: int = 0) -> str:
        """
        The Public Rite.
        Raises `GuardianHeresy` if the verdict is guilty.
        Returns the sanitized command (currently just passes through if safe).
        """
        verdict = self.judge(command, sanctum, line_num)

        if not verdict.allowed:
            # We take the most severe violation
            primary_violation = verdict.violations[0]

            # Map internal ThreatLevel to public HeresyThreatLevel
            level_map = {
                ThreatLevel.CRITICAL: HeresyThreatLevel.CRITICAL,
                ThreatLevel.HIGH: HeresyThreatLevel.HIGH,
                ThreatLevel.MEDIUM: HeresyThreatLevel.SUSPICIOUS,
                ThreatLevel.LOW: HeresyThreatLevel.SUSPICIOUS,
                ThreatLevel.SAFE: HeresyThreatLevel.SUSPICIOUS
            }

            raise GuardianHeresy(
                message=f"Sentinel Verdict: {primary_violation.reason}",
                threat_level=level_map[primary_violation.threat_level],
                details=f"Ward: {primary_violation.ward}\nContext: {primary_violation.context}",
                line_num=line_num,
                suggestion="Refactor the command to align with Gnostic Safety protocols."
            )

        return command