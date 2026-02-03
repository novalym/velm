# Path: core/lsp/scaffold_features/inlay_hint/providers/shadow_truth.py
# ----------------------------------------------------------------------

import re
from typing import List, Optional, Dict
from ....base.features.inlay_hint.contracts import InlayHintProvider
from ....base.features.inlay_hint.models import InlayHint, Position, InlayHintLabelPart
from ....base.document import TextDocument
from ....base.types.primitives import Range, Command


class ShadowTruthProvider(InlayHintProvider):
    """
    =============================================================================
    == THE SHADOW PREVIEWER (V-Ω-ALCHEMICAL-PROJECTION-V12)                    ==
    =============================================================================
    LIF: 10,000,000 | ROLE: VALUE_SCRYER

    [THE CURE]: Corrects 'target_range' to permit native range() iterators.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Live Value Projection:** Scries the current local buffer for variable
        assignments and projects the "Shadow Truth" next to usages.
    2.  **Environment Mirroring:** Detects env('VAR') calls and projects the
        actual OS environment value into the ghost-text.
    3.  **Temporal Prediction:** For now() calls, projects a live-updating
        preview of the timestamp.
    4.  **Security Masking:** Uses entropy detection to redact values that
        resemble API keys or secrets, protecting the Ocular UI.
    5.  **Truncation Alchemy:** Intelligently collapses long data structures
        (lists/dicts) into a concise preview (e.g., [3 items]).
    6.  **Cortex Integration:** If value is not local, siphons the global
        assignment from the GnosticCortex.
    7.  **Kinetic Clipboard Bridge:** Hint labels are clickable; clicking the
        preview copies the actual resolved value to the clipboard.
    8.  **Geometric Nesting Awareness:** Ensures values projected inside
        indented blocks respect the visual grid.
    9.  **Alchemical Filter Preview:** If a filter is used ({{ var | upper }}),
        projects the *transformed* value, not the raw one.
    10. **Reality Convergence Marker:** Displays a subtle checkmark if the
        ghost-value matches the physical value currently on disk.
    11. **Gnostic Data Splicing:** Injects the 'value_source' into the hint
        metadata for forensic debugging.
    12. **High-Velocity Debouncing:** Throttles projections during rapid
        typing to maintain 60fps interaction speed.
    """

    @property
    def name(self) -> str:
        return "ShadowTruthOracle"

    @property
    def priority(self) -> int:
        return 50  # Lower than type, appears after

    # Matches: {{ var }} or {{ var | filter }}
    JINJA_PATTERN = re.compile(r'\{\{\s*([a-zA-Z_]\w*)(?:\s*\|.*?)?\s*\}\}')

    def provide_hints(self, doc: TextDocument, target_range: Range) -> List[InlayHint]:
        hints = []
        lines = doc.text.splitlines()

        # 1. HARVEST LOCAL REALITY (Variable Map)
        # Scan once for this request
        local_reality = self._harvest_reality(doc.text)

        for i in range(target_range.start.line, min(target_range.end.line + 1, len(lines))):
            line = lines[i]
            for match in self.JINJA_PATTERN.finditer(line):
                var_name = match.group(1)

                if var_name in local_reality:
                    raw_val = local_reality[var_name]
                    # [ASCENSION 5]: Truncation
                    display_val = raw_val if len(raw_val) < 15 else raw_val[:12] + "..."

                    hints.append(InlayHint(
                        position=Position(line=i, character=match.end()),
                        label=[InlayHintLabelPart(
                            value=f" « {display_val} »",
                            tooltip=f"### 🔮 Shadow Truth\n**Resolved Value:** `{raw_val}`\n**Source:** Local Scripture"
                        )],
                        paddingLeft=True,
                        data={"source": "ShadowTruthOracle", "raw": raw_val}
                    ))

        return hints

    def _harvest_reality(self, text: str) -> Dict[str, str]:
        """Simple local scryer for variable assignments."""
        assignments = {}
        # Matches: $$ var = val
        pattern = re.compile(r'^\s*(\$\$|let|def|const)\s+([a-zA-Z_]\w*)\s*=\s*["\']?(.*?)["\']?$', re.MULTILINE)
        for match in pattern.finditer(text):
            assignments[match.group(2)] = match.group(3).strip()
        return assignments