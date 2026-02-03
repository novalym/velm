# === [scaffold/artisans/distill/core/skeletonizer/visitors/c_style.py] - SECTION 1 of 1: The Polyglot Surgeon ===
import re
from typing import List, Dict, Optional
from .base import BaseAnatomist
from ..contracts import SurgicalContext
from ..utils import SurgicalUtils


class CStyleAnatomist(BaseAnatomist):
    """
    =============================================================================
    == THE BRACE MASON (POLYGLOT SURGEON) V-Ω-VOID-AWARE                       ==
    =============================================================================
    Handles: JS, TS, Go, Rust, Java, C, C++, C#, PHP.

    Implements the **Heuristic of the Void**:
    1. Active Symbols: Full body (or skeletonized if stub mode).
    2. Dormant Symbols: Collapsed to `signature { ... } // [Dormant]`.
    """

    def __init__(self, ext: str):
        self.ext = ext
        # Comment syntax mapping
        self.comment_char = "//"

    def operate(self, ctx: SurgicalContext) -> str:
        output_lines = []
        mode_label = "STUB" if ctx.is_stub_mode else "SKELETON"

        # 1. Gnostic Header
        output_lines.append(
            f"{self.comment_char} == GNOSTIC {mode_label}: {len(ctx.lines)} lines original == | Active: {ctx.stats.active_count} | Dormant: {ctx.stats.dormant_count}")

        # 2. Import Summary
        output_lines.extend(SurgicalUtils.summarize_imports(ctx.dossier, self.comment_char))

        # 3. Global Constants Scan (JS/TS exports, Go vars)
        if self.ext in ('.ts', '.tsx', '.js', '.jsx'):
            output_lines.extend(
                SurgicalUtils.scan_globals(ctx.lines, r'^(export\s+)?(const|let|var)\s+[A-Z][A-Z0-9_]*\s*=',
                                           self.comment_char))
        elif self.ext == '.go':
            output_lines.extend(SurgicalUtils.scan_globals(ctx.lines, r'^(var|const)\s+[A-Z]', self.comment_char))
        elif self.ext == '.rs':
            output_lines.extend(
                SurgicalUtils.scan_globals(ctx.lines, r'^(pub\s+)?(const|static)\s+[A-Z]', self.comment_char))

        nodes = SurgicalUtils.get_sorted_nodes(ctx.dossier)
        dormant_buffer = 0

        for node in nodes:
            name = node.get('name', '')
            is_active = self._is_active(name, ctx)

            if is_active:
                if dormant_buffer > 0:
                    output_lines.append(f"    {self.comment_char} ... [{dormant_buffer} dormant souls collapsed] ...")
                    dormant_buffer = 0

                output_lines.extend(self._forge_active_node(node, ctx.lines, ctx.is_stub_mode))
                output_lines.append("")  # Spacer
                ctx.stats.active_count += 1
            else:
                output_lines.extend(self._forge_dormant_node(node, ctx.lines))
                dormant_buffer = 0  # We render dormant nodes explicitly now (compactly), so no buffer needed usually.
                # However, if we want to collapse *sequential* dormant nodes into a single comment, we could.
                # Prophecy V implementation usually prefers explicit 1-liner stubs for context.
                ctx.stats.dormant_count += 1

        if dormant_buffer > 0:
            output_lines.append(f"{self.comment_char} ... [{dormant_buffer} dormant souls collapsed] ...")

        # Telemetry footer
        output_lines[0] += f" | Final Mass: {sum(len(l) for l in output_lines)} chars"
        return "\n".join(output_lines)

    def _is_active(self, name: str, ctx: SurgicalContext) -> bool:
        if ctx.is_stub_mode: return True
        if name in SurgicalUtils.SACRED_SYMBOLS: return True
        if ctx.focus_keywords and any(k.lower() in name.lower() for k in ctx.focus_keywords): return True
        if ctx.active_symbols is not None: return name in ctx.active_symbols
        return True

    def _forge_active_node(self, node: Dict, all_lines: List[str], is_stub: bool) -> List[str]:
        """Renders the full (or skeletonized) body of an active symbol."""
        start_line = node.get('start_point', [0, 0])[0]
        end_line = node.get('end_point', [0, 0])[0]

        # Heuristic: Capture signature lines
        sig_lines, body_start_idx, indent = self._extract_signature(all_lines, start_line)

        output = []
        output.extend(sig_lines)

        # If it's just a declaration without body (e.g. abstract method or interface), return
        if body_start_idx == -1:
            return output

        # Body Handling
        line_count = node.get('line_count', 0)

        # [FACULTY 2] Apophatic Filter (Stub Mode)
        if is_stub:
            output.append(f"{indent}/* ... */")
            output.append(f"{indent}}}")  # Close brace assuming C-style
        else:
            # Full Skeleton Mode: We show the content but might truncate massive bodies?
            # Actually, standard skeletonizer collapses body content.
            output.append(f"{indent}{self.comment_char} ... [Body: {line_count} lines] ...")
            output.append(f"{indent}}}")

        return output

    def _forge_dormant_node(self, node: Dict, all_lines: List[str]) -> List[str]:
        """
        [THE HEURISTIC OF THE VOID]
        Collapses the node into a single line signature + comment.
        e.g. `func processData(data string) { ... } // [Dormant]`
        """
        start_line = node.get('start_point', [0, 0])[0]

        # Get signature lines
        sig_lines, _, _ = self._extract_signature(all_lines, start_line)

        # Collapse multi-line signatures into one line for compactness?
        # Or keep multi-line sig for readability but collapse body.
        # Let's keep signature format but ensure body is inline.

        if not sig_lines: return []

        # If the last line of signature contains '{', we append the dormant marker
        last_sig = sig_lines[-1]

        if '{' in last_sig:
            # "func foo() {" -> "func foo() { ... } // [Dormant]"
            # Strip existing closing brace if present on same line (unlikely for big funcs)
            base = last_sig.rstrip()
            if not base.endswith('}'):
                sig_lines[-1] = f"{base} ... }} {self.comment_char} [Dormant]"
            else:
                sig_lines[-1] = f"{base} {self.comment_char} [Dormant]"
        else:
            # Signature didn't have brace (weird for C-style definitions).
            # Just append marker.
            sig_lines[-1] = f"{last_sig} {self.comment_char} [Dormant]"

        return sig_lines

    def _extract_signature(self, lines: List[str], start_line: int) -> tuple[List[str], int, str]:
        """
        Scans from start_line to find the opening brace `{`.
        Returns (signature_lines, index_of_brace_line, indentation_string)
        """
        sig = []
        curr = start_line
        indent = ""

        for _ in range(20):  # Scan limit
            if curr >= len(lines): break
            line = lines[curr].rstrip()
            sig.append(line)

            # Capture indentation of first line
            if curr == start_line:
                m = re.match(r"^(\s*)", line)
                indent = m.group(1) if m else ""

            if '{' in line:
                return sig, curr, indent
            curr += 1

        # Brace not found (maybe abstract? or weird formatting)
        return sig, -1, indent