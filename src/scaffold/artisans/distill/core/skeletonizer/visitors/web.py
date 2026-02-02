# Path: scaffold/artisans/distill/core/skeletonizer/visitors/web.py
# -----------------------------------------------------------------

import re
from .base import BaseAnatomist
from ..contracts import SurgicalContext


class WebAnatomist(BaseAnatomist):
    """
    =============================================================================
    == THE WEAVER (HTML/CSS SPECIALIST)                                        ==
    =============================================================================
    """

    def __init__(self, is_style: bool = False):
        self.is_style = is_style

    def operate(self, ctx: SurgicalContext) -> str:
        if self.is_style:
            return self._skeletonize_style(ctx.content)
        return self._skeletonize_markup(ctx.content)

    def _skeletonize_markup(self, content: str) -> str:
        lines = content.splitlines()
        output_lines = [f"<!-- GNOSTIC SKELETON: {len(lines)} lines -->"]

        for line in lines:
            stripped = line.strip()
            # Heuristic: Keep structural tags
            if any(tag in stripped for tag in
                   ['<html', '<head', '<body', '<header', '<main', '<footer', '<nav', '<section', '<script', '<style']):
                output_lines.append(line)
            elif 'id="' in stripped or 'class="' in stripped:
                output_lines.append(line)
            else:
                if len(stripped) > 100 and '<' not in stripped:
                    output_lines.append(line[:80] + "... <!-- text truncated -->")
                else:
                    output_lines.append(line)
        return "\n".join(output_lines)

    def _skeletonize_style(self, content: str) -> str:
        # Simple CSS skeletonizer: Remove body of rules
        clean = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        def replace_body(match):
            selector = match.group(1).strip()
            body = match.group(2)
            lines = body.count('\n')
            if lines > 2:
                return f"{selector} {{\n    /* ... {lines} lines of styles ... */\n}}"
            return match.group(0)

        skeleton = re.sub(r'([^{]+)\{([^}]+)\}', replace_body, clean)
        return f"/* GNOSTIC SKELETON */\n{skeleton}"

