# === [scaffold/artisans/distill/core/oracle/scribe/content.py] ===
import hashlib
from pathlib import Path
from typing import Iterator, Dict

from ...governance.contracts import RepresentationTier
from ...assembler.content.facade import ContentWeaver
from ...skeletonizer import GnosticSkeletonizer
from ......logger import Scribe

Logger = Scribe("ContentHerald")


class ContentHerald:
    """
    =============================================================================
    == THE WEAVER OF SOULS (V-Ω-EXECUTABLE-BLOCKS)                             ==
    =============================================================================
    Writes the actual `file :: "content"` blocks.
    Ensures headers are comments, but content is valid syntax.
    """

    def __init__(self, root: Path):
        self.root = root

    def proclaim(self, ctx) -> Iterator[str]:
        yield "# ## 📜 Sacred Scriptures\n"

        skeletonizer = GnosticSkeletonizer(ctx.profile.focus_keywords)
        weaver = ContentWeaver(
            profile=ctx.profile,
            skeletonizer=skeletonizer,
            heat_map=self._get_heat_map(ctx),
            runtime_values=self._get_runtime_values(ctx),
            perf_stats=ctx.stats.get('perf_stats')
        )

        gnosis_lookup = {f.path: f for f in ctx.memory.inventory} if ctx.memory else {}
        sorted_paths = sorted(ctx.governance_plan.keys())

        files_included = 0
        total_tokens = 0

        for path in sorted_paths:
            tier = ctx.governance_plan[path]
            if tier == RepresentationTier.EXCLUDED.value: continue

            files_included += 1
            gnosis = gnosis_lookup.get(path)
            if not gnosis: continue

            # Bind decision for the weaver
            object.__setattr__(gnosis, 'representation_method', tier)

            path_str = str(path).replace('\\', '/')

            # --- Gnostic Anchor (Navigation) ---
            path_hash = hashlib.md5(path_str.encode()).hexdigest()[:8]
            yield f"\n# @anchor: {path_hash}\n"

            # --- Local Context Header ---
            yield self._forge_file_header(gnosis, ctx)

            try:
                # Retrieve active symbols for this path (Prophecy V)
                active_symbols = ctx.active_symbols_map.get(path) if ctx.active_symbols_map else None

                # THE WEAVER SPEAKS
                block = weaver.weave(gnosis, self.root, active_symbols)

                # Sanitize delimiters to prevent syntax errors in heredocs
                block = self._sanitize_delimiters(block)

                yield block + "\n"
                total_tokens += gnosis.token_cost

            except Exception as e:
                Logger.error(f"Scribe Error on '{path}': {e}")
                yield f"# [Heresy: Could not read scripture: {e}]\n"

        # Update telemetry
        ctx.stats['files_included'] = files_included
        ctx.stats['token_count'] = total_tokens

    def _get_heat_map(self, ctx):
        if ctx.runtime_state and ctx.runtime_state.annotations:
            return {f: set(l_dict.keys()) for f, l_dict in ctx.runtime_state.annotations.items()}
        return {}

    def _get_runtime_values(self, ctx):
        if ctx.runtime_state and ctx.runtime_state.annotations:
            return ctx.runtime_state.annotations
        return {}

    def _forge_file_header(self, gnosis, ctx) -> str:
        """Forges detailed local context header."""
        path_str = str(gnosis.path).replace('\\', '/')

        # Provenance
        parts = []
        if gnosis.days_since_last_change is not None:
            parts.append(f"Modified: {gnosis.days_since_last_change}d ago")
        if gnosis.churn_score > 0:
            parts.append(f"Churn: {gnosis.churn_score}")

        # Local Causality (Ascension)
        deps = [d.split('.')[-1] for d in sorted(list(gnosis.imported_symbols))[:5]]
        if deps:
            parts.append(f"Imports: {', '.join(deps)}")

        meta_line = f" # [{' | '.join(parts)}]" if parts else ""
        return f"### `{path_str}`{meta_line}\n"

    def _sanitize_delimiters(self, block: str) -> str:
        """Rotates delimiters to prevent collisions in generated code."""
        if '"""' not in block: return block
        if '"""' in block and "'''" not in block:
            return block.replace('"""', "'''")
        if '"""' in block and "'''" in block:
            return block.replace('"""', '\\"\\"\\"')
        return block