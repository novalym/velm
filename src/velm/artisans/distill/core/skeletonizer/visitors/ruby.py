# === [scaffold/artisans/distill/core/skeletonizer/visitors/ruby.py] - SECTION 1 of 1: The Ruby Anatomist ===
from typing import List, Dict
from .base import BaseAnatomist
from ..contracts import SurgicalContext
from ..utils import SurgicalUtils


class RubyAnatomist(BaseAnatomist):
    """
    =============================================================================
    == THE GEM CARVER (RUBY SPECIALIST)                                        ==
    =============================================================================
    Handles `def`, `class`, `module`.
    Implements Void Heuristic: `def foo; ...; end # [Dormant]`
    """

    def operate(self, ctx: SurgicalContext) -> str:
        output_lines = []
        output_lines.append(f"# == GNOSTIC SKELETON: {len(ctx.lines)} lines original ==")
        output_lines.extend(SurgicalUtils.summarize_imports(ctx.dossier, "#"))

        nodes = SurgicalUtils.get_sorted_nodes(ctx.dossier)

        for node in nodes:
            name = node.get('name', '')
            is_active = self._is_active(name, ctx)

            if is_active:
                output_lines.extend(self._forge_active_node(node, ctx.lines, ctx.is_stub_mode))
                output_lines.append("")
                ctx.stats.active_count += 1
            else:
                output_lines.extend(self._forge_dormant_node(node, ctx.lines))
                ctx.stats.dormant_count += 1

        output_lines[0] += f" | Active: {ctx.stats.active_count} | Dormant: {ctx.stats.dormant_count}"
        return "\n".join(output_lines)

    def _is_active(self, name: str, ctx: SurgicalContext) -> bool:
        if ctx.is_stub_mode: return True
        if name in ['initialize']: return True
        if ctx.focus_keywords and any(k.lower() in name.lower() for k in ctx.focus_keywords): return True
        if ctx.active_symbols is not None: return name in ctx.active_symbols
        return True

    def _forge_active_node(self, node: Dict, all_lines: List[str], is_stub: bool) -> List[str]:
        start_line = node.get('start_point', [0, 0])[0]
        sig_line = all_lines[start_line].rstrip()

        output = [sig_line]
        line_count = node.get('line_count', 0)

        # Indent heuristic (2 spaces for Ruby)
        indent = "  "
        if sig_line.startswith("  "): indent = "    "

        if is_stub:
            output.append(f"{indent}# ...")
        else:
            output.append(f"{indent}# ... [Body: {line_count} lines] ...")

        output.append("end")
        return output

    def _forge_dormant_node(self, node: Dict, all_lines: List[str]) -> List[str]:
        start_line = node.get('start_point', [0, 0])[0]
        sig_line = all_lines[start_line].strip()

        # Collapse to one line
        # def foo(x) ... end # [Dormant]
        return [f"{sig_line} ... end # [Dormant]"]