# Path: artisans/analyze/core/shadow.py
# -------------------------------------

import re
from typing import Tuple, List, Dict, Any
from pathlib import Path
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType


class ShadowParser:
    """
    =============================================================================
    == THE SHADOW PARSER (V-Ω-REGEX-FALLBACK)                                  ==
    =============================================================================
    Preserves the logic of `_shadow_parse`.
    Provides best-effort structural analysis when the Apotheosis Parser shatters.
    """

    @staticmethod
    def parse(content: str) -> Tuple[List[ScaffoldItem], Dict[str, Any]]:
        items = []
        variables = {}

        for i, line in enumerate(content.splitlines()):
            stripped = line.strip()
            if not stripped: continue

            # Variable Detection ($$ var = val)
            var_match = re.match(r'^\s*(?:\$\$)?\s*([\w_]+)\s*[:=]', stripped)
            if var_match:
                name = var_match.group(1)
                variables[name] = "shadow_value"
                # Create a phantom item for the variable
                items.append(ScaffoldItem(
                    path=Path(f"$$ {name}"),
                    is_dir=False,
                    line_num=i + 1,
                    line_type=GnosticLineType.VARIABLE
                ))
                continue

            # File Detection (Path-like strings not starting with sigils)
            if not any(stripped.startswith(s) for s in ('#', '@', '%%', '>>', '??')):
                # Heuristic: Take first word
                path_part = stripped.split(' ')[0].rstrip(':')

                # Verify it looks like a path (dots or slashes)
                if path_part and ('.' in path_part or '/' in path_part):
                    is_dir = stripped.endswith(('/', ':'))
                    items.append(ScaffoldItem(
                        path=Path(path_part),
                        is_dir=is_dir,
                        line_num=i + 1,
                        line_type=GnosticLineType.FORM
                    ))

        return items, variables