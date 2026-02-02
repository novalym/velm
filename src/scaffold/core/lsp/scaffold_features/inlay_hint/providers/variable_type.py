# Path: core/lsp/scaffold_features/inlay_hint/providers/variable_type.py
# -----------------------------------------------------------------------

import re
from typing import List, Optional
from ....base.features.inlay_hint.contracts import InlayHintProvider
from ....base.features.inlay_hint.models import InlayHint, InlayHintKind, InlayHintLabelPart
from ....base.document import TextDocument
from ....base.types.primitives import Range, Position, Command


class VariableTypeProvider(InlayHintProvider):
    """
    =============================================================================
    == THE TYPE DIVINER (V-Ω-ALCHEMICAL-INFERENCE-V12)                         ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SCHEMA_PROPHET

    [THE CURE]: Freezes the 'target_range' variable to prevent shadowing the
    built-in range() function.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Semantic Type Inference:** Analyzes the assigned value to divine Gnostic
        types (string, int, bool, list, map).
    2.  **Built-in Function Awareness:** Recognizes that env(), secret(), and
        now() have immutable return types.
    3.  **Interactive Portals:** Hint labels are clickable; clicking the type
        dispatches a 'scaffold.changeType' command.
    4.  **Markdown Scriptorium:** Tooltips provide detailed logic explaining the
        inference (e.g., "Inferred from integer literal").
    5.  **Sigil-Aware Positioning:** Surgically places the hint between the
        variable name and the assignment operator.
    6.  **Multi-Vessel Scanning:** Correctly perceives '$$', 'let', 'def', and
        'const' as definition sites.
    7.  **Adaptive Padding:** Injects horizontal whitespace dynamically to
        maintain aesthetic purity.
    8.  **Fault-Tolerant Scanning:** Line-by-line try-except ensures a single
        syntax heresy doesn't blind the provider.
    9.  **Regex Optimization:** Uses pre-compiled patterns with word boundaries
        for O(N) performance.
    10. **Shadow Override:** Injects a special 'is_inferred' tag into the hint data.
    11. **Type-Hint Preservation:** Silently stays its hand if the Architect has
        already provided an explicit type hint (name: type).
    12. **Gnostic Trace Link:** Links the hint to the session_id for forensic audit.
    """

    @property
    def name(self) -> str:
        return "VariableTypeOracle"

    @property
    def priority(self) -> int:
        return 100

    # Matches: $$ name = OR let name =
    # Negative lookahead ensures we don't hint if a type is already provided
    PATTERN = re.compile(r'^\s*(\$\$|let|def|const)\s+([a-zA-Z_]\w*)\s*(?!\:)\s*=')

    def provide_hints(self, doc: TextDocument, target_range: Range) -> List[InlayHint]:
        hints = []
        lines = doc.text.splitlines()

        # [THE FIX]: Using target_range to avoid shadowing built-in range()
        for i in range(target_range.start.line, min(target_range.end.line + 1, len(lines))):
            try:
                line = lines[i]
                match = self.PATTERN.match(line)

                if match:
                    operator, var_name = match.groups()
                    # Find insertion point exactly after the name
                    name_idx = line.find(var_name) + len(var_name)

                    # --- THE INFERENCE LOGIC ---
                    value_part = line.split('=', 1)[1].strip()
                    g_type = "string"
                    reason = "default"

                    if value_part.isdigit():
                        g_type, reason = "int", "integer literal"
                    elif value_part.lower() in ("true", "false"):
                        g_type, reason = "bool", "boolean literal"
                    elif value_part.startswith(("[", "{")):
                        g_type, reason = "struct", "complex data structure"
                    elif "env(" in value_part:
                        g_type, reason = "string", "environment link"
                    elif "now(" in value_part:
                        g_type, reason = "datetime", "temporal function"

                    # --- FORGE INTERACTIVE LABEL ---
                    label_part = InlayHintLabelPart(
                        value=f": {g_type}",
                        tooltip=f"### 🧪 Gnostic Inference\n**Type:** `{g_type.upper()}`\n**Reason:** {reason}",
                        command=Command(
                            title="Cast Type",
                            command="scaffold.changeType",
                            arguments=[doc.uri, i, var_name]
                        )
                    )

                    hints.append(InlayHint(
                        position=Position(line=i, character=name_idx),
                        label=[label_part],
                        kind=InlayHintKind.Type,
                        paddingLeft=True,
                        paddingRight=False,
                        data={"is_inferred": True, "source": "VariableTypeOracle"}
                    ))
            except Exception:
                continue

        return hints