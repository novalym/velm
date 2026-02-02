# === [scaffold/artisans/distill/core/oracle/scribe/manifest.py] - SECTION 1 of 1: The Luminous Cartographer ===
from pathlib import Path
from typing import Iterator

from ...governance.contracts import RepresentationTier


class ManifestHerald:
    """
    =============================================================================
    == THE CARTOGRAPHER (V-Ω-TOKEN-HEATMAP-CLARIFIED)                          ==
    =============================================================================
    Draws the map of the territory.
    Now displays BOTH the Representation Tier (`[FULL]`) AND the Token Cost (`[$$]`).
    """

    def __init__(self, root: Path):
        self.root = root

    def proclaim(self, ctx) -> Iterator[str]:
        yield "#\n# ## 🗺️ Territory Map\n# ```text\n"

        sorted_paths = sorted(ctx.governance_plan.keys())

        # Legend
        yield "# Legend: [Tier] [Cost] (Context)\n"
        yield "# [$] <100 tok | [$$] <1k | [$$$] <5k | [$!$] >5k\n#\n"

        for path in sorted_paths:
            tier = ctx.governance_plan[path]
            if tier == RepresentationTier.EXCLUDED.value: continue

            # Icons for tiers
            icon = {
                "skeleton": "☠️",
                "summary": "📝",
                "full": "✨",
                "path_only": "📍",
                "stub": "ℹ️"
            }.get(tier, "📄")

            path_str = str(path).replace('\\', '/')

            # Traceability
            reasons = ctx.context_reasons.get(path_str, [])
            unique_reasons = sorted(list(set(reasons)))
            reason_str = f"({', '.join(unique_reasons)})" if unique_reasons else ""

            # Token Heatmap
            gnosis = ctx.memory.find_gnosis_by_path(path) if ctx.memory else None
            cost = gnosis.token_cost if gnosis else 0

            if cost > 5000:
                heat = "[$!$]"
            elif cost > 1000:
                heat = "[$$$]"
            elif cost > 100:
                heat = "[$$]"
            else:
                heat = "[$]"

            # Format: Icon Path [TIER] [HEAT] (Reasons)
            # We align the columns for readability
            yield f"# {icon} {path_str:<55} [{tier.upper():<9}] {heat:<6} {reason_str}\n"

        yield "# ```\n# " + "-" * 60 + "\n\n"

