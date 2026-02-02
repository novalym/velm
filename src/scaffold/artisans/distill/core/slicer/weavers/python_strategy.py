# Path: artisans/distill/core/slicer/weavers/python_strategy.py
# -------------------------------------------------------------

from typing import List, Dict

from .base_strategy import BaseWeaveStrategy
from .contracts import WeaveContext
from ..contracts import RelevanceLevel, SymbolNode, CodeSegment


class PythonWeaveStrategy(BaseWeaveStrategy):
    """
    =============================================================================
    == THE PYTHONIC SURGEON (V-Ω-VISUAL-CONFIRMATION)                          ==
    =============================================================================
    A specialist that weaves sliced Python code.
    Now ascends with a **Luminous Header** to prove the surgery took place.
    """

    def weave_segments(self, context: WeaveContext) -> str:
        """The Grand Rite of Pythonic Reconstruction."""
        output_lines: List[str] = []
        last_line_rendered = 0  # 1-based index

        original_line_count = len(context.lines)
        retained_line_count = 0

        # --- MOVEMENT I: THE HEADER OF INTENT ---
        # We calculate stats first to inject them into the header
        for seg in context.merged_segments:
            retained_line_count += (seg.end_line - seg.start_line + 1)

        # Determine focus labels
        focused_nodes = [n.name for n in context.graph_roots if context.scores.get(n.name) == RelevanceLevel.FOCUSED]
        focus_str = ", ".join(focused_nodes[:3])
        if len(focused_nodes) > 3: focus_str += "..."

        # Inscribe the Gnostic Seal
        output_lines.append(f"# == GNOSTIC SLICE == | Focus: [{focus_str}]")
        output_lines.append(
            f"# Retained: {retained_line_count}/{original_line_count} lines ({int(retained_line_count / original_line_count * 100)}%)")
        output_lines.append("")  # Spacer

        # --- MOVEMENT II: PRESERVE THE SACRED IMPORTS ---
        first_code_line = self._find_first_structural_node_line(context.graph_roots)

        # Preserve everything up to the first function or class definition.
        if first_code_line > 1:
            header_end_index = first_code_line - 1
            output_lines.extend(context.lines[:header_end_index])
            last_line_rendered = header_end_index

            # If we skipped lines between imports and first code, mark it
            # (Usually just whitespace, so we ignore)

        # --- MOVEMENT III: THE WEAVING OF THE BODY ---
        for seg in context.merged_segments:
            # Gaze upon the void between segments.
            if seg.start_line > last_line_rendered + 1:
                self._render_gap(output_lines, last_line_rendered, seg.start_line, context)

            # Render the blessed segment.
            # Convert 1-based lines to 0-based list indices
            start, end = seg.start_line - 1, seg.end_line
            output_lines.extend(context.lines[start:end])
            last_line_rendered = end

        # Gaze upon the final void at the end of the file.
        if last_line_rendered < len(context.lines):
            self._render_gap(output_lines, last_line_rendered, len(context.lines) + 1, context)

        return "\n".join(output_lines)

    def _find_first_structural_node_line(self, nodes: List[SymbolNode]) -> int:
        """Finds the earliest line number of a function or class."""
        if not nodes:
            return 99999
        return min(node.start_line for node in nodes)

    def _render_gap(self, output: List[str], start_line: int, end_line: int, context: WeaveContext):
        """
        [THE GNOSTIC GAP SCRIBE]
        Intelligently renders the space between preserved segments.
        """
        # Find all nodes that exist entirely within this gap.
        nodes_in_gap = self._find_nodes_in_range(start_line, end_line, context.graph_roots)

        if not nodes_in_gap:
            # It's just empty space or unstructured code. Render a simple collapse.
            skipped = end_line - start_line - 1
            if skipped > 0:
                # Use indent of previous line or default to 0
                indent = ""
                if start_line > 0 and start_line <= len(context.lines):
                    indent = self._detect_indent(context.lines[start_line - 1])

                output.append(f"{indent}# ... [Collapsed {skipped} lines of implementation] ...")
            return

        for node in nodes_in_gap:
            score = context.scores.get(node.name, RelevanceLevel.IRRELEVANT)
            indent = ""
            if node.start_line > 0:
                indent = self._detect_indent(context.lines[node.start_line - 1])

            # A STRUCTURAL node in a gap means it's a container for something we're keeping,
            # or it's a sibling we want to show as a skeleton.
            if score == RelevanceLevel.STRUCTURAL or score == RelevanceLevel.IRRELEVANT:
                # Even irrelevant top-level nodes get a skeleton in surgical mode
                # so the LLM sees the context of what was removed.

                # Render the signature
                sig_start, sig_end = node.start_line - 1, node.signature_end_line
                output.extend(context.lines[sig_start:sig_end])

                # Render the hollowed-out body
                body_indent = indent + "    "

                if node.type == 'class':
                    output.append(f"{body_indent}# ... [Body Omitted] ...")
                else:  # function or method
                    output.append(f"{body_indent}...")

    def _find_nodes_in_range(self, start: int, end: int, nodes: List[SymbolNode]) -> List[SymbolNode]:
        """A recursive Gaze to find all nodes fully contained within a line range."""
        found = []
        for node in nodes:
            # Check if node is strictly inside the gap
            if start < node.start_line and node.end_line < end:
                found.append(node)
            # Recurse
            found.extend(self._find_nodes_in_range(start, end, node.children))

        # Sort by line number
        return sorted(found, key=lambda x: x.start_line)