# === [scaffold/artisans/distill/core/oracle/scribe/header.py] - SECTION 1 of 1: The Omniscient Header ===
import time
from pathlib import Path
from typing import Iterator, List
from collections import Counter

from ...governance.contracts import RepresentationTier
from ..contracts import OracleContext
from ......core.cortex.contracts import FileGnosis

# --- THE DIVINE SUMMONS OF KNOWLEDGE ---
from ...assembler.seer import DependencySeer
from .....harvest import TodoHarvester


class HeaderHerald:
    """
    =============================================================================
    == THE HERALD OF CONTEXT (V-Ω-INTELLIGENT-SYSTEM-PROMPT)                   ==
    =============================================================================
    Forges a high-fidelity System Prompt disguised as comments.
    It reveals Tech Stacks, Dependencies, Technical Debt, and User Directives.
    """

    def __init__(self, root: Path):
        self.root = root

    def proclaim(self, ctx: OracleContext) -> Iterator[str]:
        # --- 1. Gather Telemetry ---
        active_files = self._get_active_files(ctx)
        full_count = sum(1 for t in ctx.governance_plan.values() if t == RepresentationTier.FULL.value)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S UTC')
        strategy = ctx.profile.strategy.upper()

        # --- 2. Gather Deep Gnosis ---
        # Tech Stack & Dependencies (The Seer)
        seer = DependencySeer()
        stacks_str, deps_str = seer.summarize(active_files)

        # Technical Debt (The Harvester)
        harvester = TodoHarvester(self.root)
        debt_items = harvester.harvest()
        debt_count = len(debt_items)

        # Language Distribution
        lang_counts = Counter(f.language for f in active_files if f.category == 'code')
        top_langs = ", ".join([f"{l} ({c})" for l, c in lang_counts.most_common(3)])

        # --- 3. Proclaim the Banner ---
        yield "# =============================================================================\n"
        yield f"# 🏛️  GNOSTIC BLUEPRINT: {self.root.name.upper()}\n"
        yield "# =============================================================================\n"
        yield f"# 📅 Timestamp: {timestamp}\n"
        yield f"# 🎯 Strategy:  {strategy}\n"
        yield f"# 💰 Budget:    {ctx.budget_limit} tokens\n"
        yield f"# 📊 Vitality:  {len(active_files)} Files (Full: {full_count}) | {top_langs}\n"
        yield "#\n"

        # --- 4. The Prime Directive (User Context) ---
        # This allows the user to permanently teach the AI about the project's soul.
        user_context_path = self.root / ".scaffold" / "context.md"
        if user_context_path.exists():
            yield "# 🧠 PROJECT SOUL (USER DEFINED CONTEXT)\n"
            try:
                context_content = user_context_path.read_text(encoding='utf-8')
                # Indent it to keep it as comments and distinct
                for line in context_content.splitlines():
                    yield f"#    {line}\n"
            except Exception:
                yield "#    (Error reading context.md)\n"
            yield "#\n"

        # --- 5. Proclaim the Stack ---
        yield "# 🛠️  TECH STACK & DEPENDENCIES\n"
        yield f"#    {stacks_str.replace('# ', '')}\n"
        yield f"#    {deps_str.replace('# ', '')}\n"
        yield "#\n"

        # --- 6. Proclaim the Debt ---
        # Knowing where the TODOs are helps the AI avoid areas that are under construction
        if debt_count > 0:
            yield "# ⚠️  TECHNICAL DEBT SCAN\n"
            yield f"#    {debt_count} markers detected (TODO/FIXME).\n"
            # Show top 3 debt items if available to give flavor
            for item in debt_items[:3]:
                # Truncate message for cleanliness
                msg = item.message[:60] + "..." if len(item.message) > 60 else item.message
                yield f"#    - {item.type}: {msg} ({item.path.name}:{item.line_num})\n"
            if debt_count > 3:
                yield f"#    - ... and {debt_count - 3} more.\n"
            yield "#\n"

        # --- 7. Proclaim Architectural Drift (If any) ---
        if ctx.profile.diff_context:
            yield "# 📉 ARCHITECTURAL DRIFT\n"
            yield "#    Inline diffs [WAS: ...] enabled for changed lines.\n"
            yield "#\n"

        # --- 8. The AI Directive ---
        yield "# 🤖 AI DIRECTIVE\n"
        yield "#    This file is an executable Blueprint. Paths are commands.\n"
        yield "#    - `path :: \"content\"` creates/overwrites a file.\n"
        yield "#    - `path << seed` copies a file.\n"
        yield "#    - `$$ var = val` defines a variable.\n"
        yield "#    Analyze the code below to fulfill the Architect's intent.\n"
        yield "# =============================================================================\n\n"

        # --- 9. The Root Definition ---
        # This is the first executable line of the blueprint.
        yield f"$$ project_root = \"{self.root.name}\"\n\n"

    def _get_active_files(self, ctx) -> List[FileGnosis]:
        if not ctx.memory: return []
        # Filter inventory for only what is being rendered (Full, Skeleton, Summary, Stub)
        return [
            item for item in ctx.memory.inventory
            if
            ctx.governance_plan.get(item.path, RepresentationTier.EXCLUDED.value) != RepresentationTier.EXCLUDED.value
        ]