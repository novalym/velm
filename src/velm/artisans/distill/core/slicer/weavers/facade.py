# Path: scaffold/artisans/distill/core/slicer/weavers/facade.py
# -----------------------------------------------------------

from pathlib import Path
from typing import List, Dict, Type

from .base_strategy import BaseWeaveStrategy
from .contracts import WeaveContext
from .python_strategy import PythonWeaveStrategy
from ..contracts import CodeSegment, RelevanceLevel, SymbolNode
from ......logger import Scribe

Logger = Scribe("SurgicalWeaverFacade")


class SurgicalWeaverFacade:
    """
    =============================================================================
    == THE SURGICAL WEAVER (V-Ω-FACADE-ULTIMA)                                 ==
    =============================================================================
    The High Priest of Reconstruction. It is a pure Conductor.
    1. Detects Language.
    2. Summons the correct Weaving Strategy from the Pantheon.
    3. Bestows the complete Gnostic Context upon the Strategy.
    4. Proclaims the final, surgically reconstructed scripture.
    """

    def __init__(self):
        self.strategies: Dict[str, Type[BaseWeaveStrategy]] = {
            ".py": PythonWeaveStrategy,
            # Prophecy: Future artisans will be consecrated here.
            # ".js": JavaScriptWeaveStrategy,
            # ".ts": TypeScriptWeaveStrategy,
        }

    def weave(self, file_path: Path, content: str, scores: Dict[str, RelevanceLevel],
              graph_roots: List[SymbolNode]) -> str:
        """The Grand Rite of Weaving."""
        lines = content.splitlines()

        # --- MOVEMENT I: THE GATHERING OF SEGMENTS ---
        # This logic remains pure: it identifies the high-level blocks to keep.
        segments = self._collect_segments(graph_roots, scores)

        if not segments:
            return f"# [Surgical Slicer] No symbols matched the focus in '{file_path.name}'.\n# Original size: {len(lines)} lines."

        merged_segments = self._merge_segments(segments)

        # --- MOVEMENT II: THE GNOSTIC TRIAGE & DELEGATION ---
        # The Facade perceives the language and summons the specialist.
        strategy_class = self.strategies.get(file_path.suffix.lower())

        if not strategy_class:
            # Fallback to the humble, comment-based weaver for unknown tongues.
            Logger.warn(f"No specialized weaver for '{file_path.suffix}'. Using comment-based fallback.")
            return self._weave_with_fallback(lines, merged_segments)

        # --- MOVEMENT III: THE DIVINE COMMUNION ---
        # The specialist is born and bestowed with the full Gnostic context.
        strategy = strategy_class()
        context = WeaveContext(
            file_path=file_path,
            lines=lines,
            scores=scores,
            graph_roots=graph_roots,
            merged_segments=merged_segments
        )

        try:
            return strategy.weave_segments(context)
        except Exception as e:
            Logger.error(f"A paradox shattered the '{strategy_class.__name__}'. Falling back. Heresy: {e}")
            return self._weave_with_fallback(lines, merged_segments)

    def _collect_segments(self, nodes: List[SymbolNode], scores: Dict[str, RelevanceLevel]) -> List[CodeSegment]:
        """Recursively gathers all code segments that must be preserved."""
        segments: List[CodeSegment] = []
        for node in nodes:
            score = scores.get(node.name, RelevanceLevel.IRRELEVANT)

            if score in (RelevanceLevel.FOCUSED, RelevanceLevel.DEPENDENCY):
                segments.append(CodeSegment(node.start_line, node.end_line, "", score, node))
            elif score == RelevanceLevel.STRUCTURAL:
                segments.append(CodeSegment(node.start_line, node.signature_end_line, "", score, node))
                # Gaze into the children for more relevant souls.
                segments.extend(self._collect_segments(node.children, scores))
        return segments

    def _merge_segments(self, segments: List[CodeSegment]) -> List[CodeSegment]:
        """Merges overlapping or adjacent segments into a single, unified reality."""
        if not segments:
            return []

        segments.sort(key=lambda s: s.start_line)
        merged = [segments[0]]
        for next_seg in segments[1:]:
            current = merged[-1]
            # Merge if they touch or overlap
            if current.end_line >= next_seg.start_line - 1:
                current.end_line = max(current.end_line, next_seg.end_line)
                # The highest relevance wins.
                if next_seg.relevance.value > current.relevance.value:
                    current.relevance = next_seg.relevance
            else:
                merged.append(next_seg)
        return merged

    def _weave_with_fallback(self, lines: List[str], merged_segments: List[CodeSegment]) -> str:
        """The original, humble weaver for unknown or failed languages."""
        output_lines: List[str] = []
        last_line_idx = 0
        for seg in merged_segments:
            if seg.start_line > last_line_idx + 1:
                skipped = seg.start_line - last_line_idx - 1
                if skipped > 0:
                    indent = self._detect_indent(lines[seg.start_line - 1])
                    output_lines.append(f"{indent}# ... [Collapsed {skipped} lines] ...")

            start, end = max(0, seg.start_line - 1), min(len(lines), seg.end_line)
            output_lines.extend(lines[start:end])
            last_line_idx = end

        if last_line_idx < len(lines):
            skipped = len(lines) - last_line_idx
            output_lines.append(f"# ... [Collapsed {skipped} lines] ...")

        return "\n".join(output_lines)

    def _detect_indent(self, line: str) -> str:
        import re
        match = re.match(r"^(\s*)", line)
        return match.group(1) if match else ""

