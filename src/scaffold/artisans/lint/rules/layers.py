from typing import Generator, List, Dict
from sqlalchemy import text
from .base import GnosticRule
from ..contracts import LintContext, LintIssue, HeresySeverity


class LayeringRule(GnosticRule):
    """
    =============================================================================
    == THE LAYERING INQUISITOR (V-Ω-TOPOGRAPHICAL-ENFORCER)                    ==
    =============================================================================
    LIF: 10,000,000,000

    Enforces the One-Way Flow of Gnosis.
    Inner layers (Domain) must never import Outer layers (API/Infra).
    """

    id = "arch.layers"
    category = "Architecture"

    # The Sacred Topography (Lower number = More Inner/Pure)
    TOPOGRAPHY = {
        "domain": 0,
        "core": 1,
        "service": 2,
        "infra": 3,
        "api": 4,
        "cmd": 5
    }

    def check(self, context: LintContext) -> Generator[LintIssue, None, None]:
        if not context.has_crystal_mind:
            return

        # 1. We query the bonds but only between files we can categorize
        query = text("SELECT source_path, target_path FROM bonds")
        results = context.db_session.execute(query).fetchall()

        for src, dst in results:
            src_layer = self._divine_layer(src)
            dst_layer = self._divine_layer(dst)

            if src_layer is not None and dst_layer is not None:
                # THE LAW: Source Layer Rank must be >= Destination Layer Rank
                # Heresy: Outer layer rank is less than Inner (e.g. Domain(0) imports API(4))
                if src_layer < dst_layer:
                    yield LintIssue(
                        rule_id=self.id,
                        message=f"Layer Violation: Inner layer scripture imports Outer layer.",
                        path=context.project_root / src,
                        severity=HeresySeverity.CRITICAL,
                        details=f"'{src}' ({self._name(src_layer)}) imports '{dst}' ({self._name(dst_layer)})",
                        suggestion=f"Dependency must flow inwards. Move shared logic to a deeper layer."
                    )

    def _divine_layer(self, path_str: str) -> Optional[int]:
        # Heuristic: Check path parts for layer names
        parts = path_str.lower().split('/')
        for part in parts:
            if part in self.TOPOGRAPHY:
                return self.TOPOGRAPHY[part]
        return None

    def _name(self, rank: int) -> str:
        for k, v in self.TOPOGRAPHY.items():
            if v == rank: return k.upper()
        return "UNKNOWN"