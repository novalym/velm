# === [scaffold/artisans/distill/core/skeletonizer/visitors/python.py] - SECTION 1 of 1: The Pythonic Anatomist ===
import re
from typing import List, Dict
from .base import BaseAnatomist
from ..contracts import SurgicalContext
from ..utils import SurgicalUtils


class PythonAnatomist(BaseAnatomist):
    """
    =================================================================================
    == THE SERPENT (PYTHON SPECIALIST) V-Ω-VOID-AWARE                              ==
    =================================================================================
    LIF: 10,000,000,000 (THE SURGICAL REDUCTION)

    Extracts Decorators, Signatures, and Docstrings with Gnostic precision.
    It implements the **Heuristic of the Void**: Symbols not marked as 'Active'
    by the Propagator are collapsed into single-line stubs.
    """

    def operate(self, ctx: SurgicalContext) -> str:
        output_lines = []
        mode_label = "STUB" if ctx.is_stub_mode else "SKELETON"

        # 1. The Header Analysis
        # We start by summarizing the imports and globals to clear the stage.
        import_summary = SurgicalUtils.summarize_imports(ctx.dossier, "#")
        global_summary = SurgicalUtils.scan_globals(ctx.lines, r'^[A-Z][A-Z0-9_]*\s*=', "#")

        # 2. The Gnostic Census (Active vs Dormant)
        nodes = SurgicalUtils.get_sorted_nodes(ctx.dossier)

        # We perform a pre-pass to count stats for the header
        # Note: ctx.stats is mutable and shared
        for node in nodes:
            name = node.get('name', '')
            is_active = self._is_active(name, ctx)
            if is_active:
                ctx.stats.active_count += 1
            else:
                ctx.stats.dormant_count += 1

        # 3. The Gnostic Header
        output_lines.append(
            f"# == GNOSTIC {mode_label}: {len(ctx.lines)} lines original == | Active: {ctx.stats.active_count} | Dormant: {ctx.stats.dormant_count}")

        # Add the summaries
        output_lines.extend(import_summary)
        output_lines.extend(global_summary)
        output_lines.append("")  # Spacer

        # 4. The Surgical Loop
        # We iterate through the nodes. If active, we flesh them out. If dormant, we stub them.

        for node in nodes:
            name = node.get('name', '')
            is_active = self._is_active(name, ctx)

            if is_active:
                # Active: Full Skeleton (Decorators + Signature + Docstring + Structure Hint)
                output_lines.extend(self._forge_active_node(node, ctx.lines, ctx.is_stub_mode))
                output_lines.append("")  # Breathing room
            else:
                # Dormant: The One-Liner Stub (Prophecy V)
                output_lines.extend(self._forge_dormant_node(node, ctx.lines))

        return "\n".join(output_lines)

    def _is_active(self, name: str, ctx: SurgicalContext) -> bool:
        """
        Adjudicates if a symbol deserves life.
        1. If active_symbols is None (Focus File), everything is active.
        2. If name is in active_symbols (Dependency File), it is active.
        3. If name is a Sacred Symbol (__init__, main), it is active.
        """
        # [FACULTY 2] The Apophatic Filter (Stub Mode)
        if ctx.is_stub_mode:
            return True  # In interface mode, everything is "active" but rendered as stubs.

        # 1. Sacred Symbols are always kept
        if name in SurgicalUtils.SACRED_SYMBOLS:
            return True

        # 2. Semantic Resonance (Focus Keywords)
        if ctx.focus_keywords:
            # We don't check docstrings here for perf, just name
            if any(k in name.lower() for k in ctx.focus_keywords):
                return True

        # 3. Causal Necessity (Active Symbols Map)
        if ctx.active_symbols is not None:
            return name in ctx.active_symbols

        # Default: If no restriction, everything is active
        return True

    def _forge_active_node(self, node: Dict, all_lines: List[str], is_stub: bool) -> List[str]:
        """Renders the full skeleton of a living symbol."""
        start_line = node.get('start_point', [0, 0])[0]
        output = []

        # A. Decorators [FACULTY 6]
        curr = start_line - 1
        decorators = []
        while curr >= 0:
            line = all_lines[curr].strip()
            if line.startswith('@'):
                decorators.insert(0, all_lines[curr].rstrip())
                curr -= 1
            else:
                break
        output.extend(decorators)

        # B. Signature
        # We capture the definition line, handling multi-line sigs
        def_line = all_lines[start_line].rstrip()
        sig_idx = start_line
        while not def_line.strip().endswith(':'):
            sig_idx += 1
            if sig_idx >= len(all_lines): break
            def_line += "\n" + all_lines[sig_idx].rstrip()
        output.append(def_line)

        # C. Body Summary
        indent = "    "  # Assume 4 spaces for now
        doc = node.get('docstring')

        # [FACULTY 7] Docstring Distiller
        if doc and not is_stub:
            summary = doc.splitlines()[0].strip()
            if len(summary) > 60: summary = summary[:57] + "..."
            output.append(f'{indent}""" {summary} ... """')
        elif doc and is_stub:
            output.append(f'{indent}""" ... """')

        line_count = node.get('line_count', 0)

        # [FACULTY 2] Apophatic Filter
        if is_stub:
            output.append(f"{indent}...")
        else:
            # Structural Hint
            output.append(f"{indent}# ... [Body: {line_count} lines] ...")

        return output

    def _forge_dormant_node(self, node: Dict, all_lines: List[str]) -> List[str]:
        """Renders the collapsed tombstone of a dormant symbol."""
        start_line = node.get('start_point', [0, 0])[0]

        # We only want the first line of the signature
        sig_line = all_lines[start_line].strip()

        # If it's a multiline sig, we just take the first line and append '...'
        if not sig_line.endswith(':'):
            sig_line = sig_line + " ... :"

        # Add the Dormant Tag
        # e.g. "def helper_func(a, b): ... # [Dormant]"

        # Determine indentation
        original_indent = all_lines[start_line][:len(all_lines[start_line]) - len(all_lines[start_line].lstrip())]

        # We construct a one-liner representation
        if node.get('type') == 'function':
            return [f"{original_indent}{sig_line} ... # [Dormant]"]
        elif node.get('type') == 'class':
            return [f"{original_indent}{sig_line} ... # [Dormant]"]

        return [f"{original_indent}{sig_line} ... # [Dormant]"]