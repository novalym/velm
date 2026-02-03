# Path: core/lsp/scaffold_features/linter/context.py
# -----------------------------------------

import re
from typing import Dict, Set, Any, List
from ...base.document import TextDocument


class AnalysisContext:
    """
    [THE STATE PERCEIVER]
    A snapshot of the scripture's reality.
    Pre-computes symbol tables and indentation maps for O(1) rule checking.
    This ensures we don't re-parse the file 50 times for 50 rules.
    """

    def __init__(self, doc: TextDocument, server: Any):
        self.doc = doc
        self.server = server
        self.engine = getattr(server, 'engine', None)

        # [ASCENSION: SYMBOL TABLE]
        # Variables defined in this file via $$
        self.defined_vars: Set[str] = set()
        # Variables used in this file via {{ }}
        self.referenced_vars: Set[str] = set()

        # [ASCENSION: GEOMETRY MAP]
        # Map[LineIndex, IndentLevel]
        self.indent_map: Dict[int, int] = {}

        # [ASCENSION: LINE CACHE]
        # Clean lines without whitespace for fast regex
        self.clean_lines: List[str] = []

        # [ASCENSION: SUPPRESSION MAP]
        # Set of line indices that should be ignored
        self.suppressed_lines: Set[int] = set()

        self._analyze_state()

    def _analyze_state(self):
        lines = self.doc.text.splitlines()
        var_def_pattern = re.compile(r'^\s*(\$\$|let|def|const)\s+([a-zA-Z_]\w*)')
        var_ref_pattern = re.compile(r'\{\{\s*([a-zA-Z_]\w*)')
        suppression_pattern = re.compile(r'#\s*gnostic:\s*(ignore|disable)', re.IGNORECASE)

        for i, line in enumerate(lines):
            stripped = line.strip()
            self.clean_lines.append(stripped)

            # Check for suppression
            if suppression_pattern.search(line):
                self.suppressed_lines.add(i)
                # If ignore is on previous line, it suppresses next line?
                # For now, inline suppression: applies to current line.

            if not stripped:
                self.indent_map[i] = 0
                continue

            # 1. Map Indentation
            indent = len(line) - len(line.lstrip())
            self.indent_map[i] = indent

            # 2. Map Definitions
            def_match = var_def_pattern.match(line)
            if def_match:
                self.defined_vars.add(def_match.group(2))

            # 3. Map References
            refs = var_ref_pattern.findall(line)
            for r in refs:
                self.referenced_vars.add(r)