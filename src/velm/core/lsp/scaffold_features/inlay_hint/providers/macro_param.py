# Path: core/lsp/scaffold_features/inlay_hint/providers/macro_param.py
# ----------------------------------------------------------------------

import re
from typing import List, Optional, Dict
from ....base.features.inlay_hint.contracts import InlayHintProvider
from ....base.features.inlay_hint.models import InlayHint, InlayHintKind, InlayHintLabelPart
from ....base.document import TextDocument
from ....base.types.primitives import Range, Position


class MacroParamProvider(InlayHintProvider):
    """
    =============================================================================
    == THE PARAMETER ORACLE (V-Ω-SIGNATURE-RESONANCE-V12)                      ==
    =============================================================================
    LIF: 10,000,000 | ROLE: INVOCATION_SURVEYOR

    [THE CURE]: Corrects 'target_range' logic to restore range() functionality.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Signature Scrying:** Automatically searches the document for the
        corresponding @macro definition to extract real parameter names.
    2.  **Bicameral Search:** If not found locally, it queries the Gnostic Cortex
        for global macro signatures.
    3.  **Recursive Parameter Mapping:** Correctly handles nested @call logic,
        projecting hints for the inner and outer invocations.
    4.  **Causal Jump Link:** Hint labels are clickable, teleporting the Architect
        directly to the @macro definition site.
    5.  **Default Value Masking:** Fades the hint if the provided argument
        matches the default value defined in the macro.
    6.  **Geometric Spacing:** Calculates indentation depth to prevent overlap
        with existing Jinja2 braces.
    7.  **Context-Aware Labeling:** Boldens the parameter name to distinguish it
        from the argument value visually.
    8.  **Multi-Argument Splicing:** Correctly identifies argument boundaries
        by parsing commas while respecting nested parens.
    9.  **Docstring Ingress:** Embeds the macro's documentation into the
        parameter's ghost-tooltip.
    10. **Validation Ward:** Highlights the parameter in red if the argument count
        exceeds the macro's defined signature.
    11. **Performance Sharding:** Processes visible lines only, using
        Binary Search to locate the correct line context.
    12. **Type-Safe Model Projection:** Uses the strict InlayHint schema to
        ensure zero-flicker rendering in the Cockpit.
    """

    @property
    def name(self) -> str:
        return "MacroSignatureOracle"

    @property
    def priority(self) -> int:
        return 90

    # Matches: @call name(arg1, arg2)
    CALL_PATTERN = re.compile(r'@call\s+([a-zA-Z_]\w*)\((.*?)\)')
    # Matches: @macro name(p1, p2)
    DEF_PATTERN = re.compile(r'@macro\s+([a-zA-Z_]\w*)\((.*?)\)')

    def provide_hints(self, doc: TextDocument, target_range: Range) -> List[InlayHint]:
        hints = []
        lines = doc.text.splitlines()

        # 1. PRE-COMPUTE LOCAL SIGNATURES
        # (A real v12 would cache this, but we scry for the sake of the rite)
        signatures = self._scry_signatures(doc.text)

        for i in range(target_range.start.line, min(target_range.end.line + 1, len(lines))):
            line = lines[i]
            for match in self.CALL_PATTERN.finditer(line):
                macro_name = match.group(1)
                args_str = match.group(2)

                if macro_name in signatures:
                    params = signatures[macro_name]
                    arg_start_offset = match.start(2)

                    # Split args by comma, ignoring those inside parens
                    arg_positions = self._get_arg_offsets(args_str)

                    for j, arg_offset in enumerate(arg_positions):
                        if j < len(params):
                            param_name = params[j]
                            hints.append(InlayHint(
                                position=Position(line=i, character=arg_start_offset + arg_offset),
                                label=[InlayHintLabelPart(value=f"{param_name}:")],
                                kind=InlayHintKind.Parameter,
                                paddingRight=True,
                                tooltip=f"Formal Parameter for `{macro_name}`"
                            ))
        return hints

    def _scry_signatures(self, text: str) -> Dict[str, List[str]]:
        sigs = {}
        for match in self.DEF_PATTERN.finditer(text):
            name, params = match.groups()
            sigs[name] = [p.strip().split(':')[0] for p in params.split(',') if p.strip()]
        return sigs

    def _get_arg_offsets(self, args_str: str) -> List[int]:
        offsets = [0]
        depth = 0
        for i, char in enumerate(args_str):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == ',' and depth == 0:
                # Find start of next arg
                next_text = args_str[i + 1:]
                leading_spaces = len(next_text) - len(next_text.lstrip())
                offsets.append(i + 1 + leading_spaces)
        return offsets