# Path: artisans/analyze/static_inquisitor/detectors/atomic.py
# ------------------------------------------------------------

import re
from typing import List, Dict, Any, Set, Pattern

from .base import BaseDetector
from .....contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....creator.security import PathSentinel
from .....jurisprudence_core.scaffold_grammar_codex import SAFE_JINJA_FILTERS


class AtomicDetector(BaseDetector):
    """
    =============================================================================
    == THE ATOMIC SENTINEL (V-Ω-OMNISCIENT-GAZE-FIXED)                         ==
    =============================================================================
    LIF: 10,000,000,000,000,000,000 (THE UNBREAKABLE ATOM)

    The Specialist of the Single Line.
    It does not look at the forest; it judges the purity of every leaf, every sigil,
    and every intent with forensic precision.

    [FIX]: Replaced phantom PathSentinel call with inline regex for absolute paths.
    """

    # =========================================================================
    # == THE GRIMOIRE OF REGEX (PRE-COMPILED FOR SPEED)                      ==
    # =========================================================================

    # --- Variables ---
    VAR_DEF_REGEX = re.compile(r'^\s*\$\$\s*(?P<name>[a-zA-Z0-9_]+)\s*(?::\s*(?P<type>[^=]+))?\s*=\s*(?P<value>.*)')
    VAR_NAME_SNAKE = re.compile(r'^[a-z][a-z0-9_]*$')

    # --- Permissions ---
    PERM_REGEX = re.compile(r'^\s*%%\s*(?P<perm>.*)')
    VALID_OCTAL = re.compile(r'^[0-7]{3}$')
    VALID_NAMED_PERMS = {'executable', 'readonly', 'secret', 'public', 'bin', 'script'}

    # --- Logic ---
    LOGIC_DIRECTIVE_REGEX = re.compile(r'^\s*@(?P<name>\w+)(?P<args>.*)')
    KNOWN_DIRECTIVES = {
        'if', 'elif', 'else', 'endif',
        'for', 'endfor',
        'def', 'let',
        'include', 'import',
        'error', 'warn', 'print',
        'macro', 'endmacro', 'call',
        'task', 'endtask'
    }

    # --- Jinja Hygiene ---
    # Captures {{ ... }} and {% ... %}
    JINJA_BLOCK_REGEX = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})')
    # Captures pipe filters inside blocks: | filter_name
    JINJA_FILTER_REGEX = re.compile(r'\|\s*([a-zA-Z0-9_]+)')
    # Unbalanced braces check
    UNBALANCED_JINJA = re.compile(r'(\{\{[^\}]*$|^[^\{]*\}\})')

    # --- Security ---
    SECRET_REGEX = re.compile(
        r'(password|secret|token|key|api_key|access_key|auth)\s*[:=]\s*["\'].{8,}["\']',
        re.IGNORECASE
    )
    SHELL_INJECTION_REGEX = re.compile(r'(\;\s*rm\s+-rf)|(\|\s*bash)|(\|\s*sh)|(\$\(.*\))')
    TRAVERSAL_REGEX = re.compile(r'\.\.[\/\\]')
    # [FIX] Added Absolute Path Regex
    ABSOLUTE_PATH_REGEX = re.compile(r'^([a-zA-Z]:|[\\/])')

    # --- Form ---
    SYMLINK_REGEX = re.compile(r'\s*->\s*(.*)')

    def detect(self, content: str, variables: Dict, items: List[ScaffoldItem],
               edicts: List, dossier: GnosticDossier) -> List[Dict[str, Any]]:

        diagnostics = []

        for item in items:
            line_idx = max(0, item.line_num - 1)

            # --- MOVEMENT I: THE GAZE OF FORM (Structural Integrity) ---
            if item.line_type == GnosticLineType.FORM:
                self._audit_form(item, line_idx, diagnostics)

            # --- MOVEMENT II: THE GAZE OF LOGIC (Directives) ---
            elif item.line_type == GnosticLineType.LOGIC:
                self._audit_logic(item, line_idx, diagnostics)

            # --- MOVEMENT III: THE GAZE OF STATE (Variables) ---
            elif item.line_type == GnosticLineType.VARIABLE:
                self._audit_variable(item, line_idx, diagnostics)

            # --- MOVEMENT IV: THE GAZE OF WILL (Post-Run/Edicts) ---
            elif item.line_type == GnosticLineType.POST_RUN:
                self._audit_edict(item, line_idx, diagnostics)

            # --- MOVEMENT V: THE GAZE OF HYGIENE (Common Checks) ---
            if item.raw_scripture:
                self._audit_hygiene(item, line_idx, diagnostics)

        return diagnostics

    # =========================================================================
    # == AUDIT SUB-SYSTEMS                                                   ==
    # =========================================================================

    def _audit_form(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Audits a file/directory definition item."""

        # 1. Path Security (The Sentinel's Bond)
        if item.path:
            path_str = str(item.path)
            # Normalize slashes for regex
            clean_path = path_str.replace('\\', '/')

            try:
                PathSentinel.adjudicate(path_str)
            except ArtisanHeresy as e:
                diagnostics.append(self._forge_diagnostic(
                    key="DANGEROUS_PATH_TRAVERSAL_HERESY",
                    line=line, item=item,
                    data={"details": e.details or e.message, "severity_override": "CRITICAL"}
                ))

            # [FIX] Absolute Path Check (Inline Regex)
            if self.ABSOLUTE_PATH_REGEX.match(clean_path):
                diagnostics.append(self._forge_diagnostic(
                    key="ABSOLUTE_PATH_HERESY",
                    line=line, item=item,
                    data={"details": f"Path '{path_str}' is absolute.", "severity_override": "CRITICAL"}
                ))

            # Whitespace Check (Re-iterating for safety in the Atomic context)
            if " " in path_str:
                diagnostics.append(self._forge_diagnostic(
                    key="WHITESPACE_IN_FILENAME_HERESY",
                    line=line, item=item,
                    data={
                        "details": f"Path '{path_str}' contains profane whitespace.",
                        "severity_override": "CRITICAL",
                        "variable": path_str
                    }
                ))

        # 2. Symlink Integrity
        if item.is_symlink:
            if not item.symlink_target:
                diagnostics.append(self._forge_diagnostic(
                    key="VOID_SYMLINK_HERESY",
                    line=line, item=item,
                    data={"details": "Symlink declared ('->') but no target specified.",
                          "severity_override": "CRITICAL"}
                ))
            elif self.TRAVERSAL_REGEX.search(item.symlink_target):
                diagnostics.append(self._forge_diagnostic(
                    key="DANGEROUS_SYMLINK_HERESY",
                    line=line, item=item,
                    data={"details": "Symlink target attempts path traversal.", "severity_override": "WARNING"}
                ))

        # 3. Content Integrity
        if item.content is not None:
            # Void Content (Style)
            if not item.content.strip() and not item.is_dir:
                diagnostics.append(self._forge_diagnostic(
                    key="STYLISTIC_HERESY_EMPTY_CONTENT",
                    line=line, item=item,
                    data={"details": f"File '{item.path}' has explicit content marker '::' but no soul.",
                          "severity_override": "INFO"}
                ))

            # Shell Injection Scan (Security)
            if self.SHELL_INJECTION_REGEX.search(item.content):
                # Only flag if it looks like a script file or config
                is_script = str(item.path).endswith(('.sh', '.bash', '.py', '.js'))
                if is_script:
                    diagnostics.append(self._forge_diagnostic(
                        key="POTENTIAL_INJECTION_HERESY",
                        line=line, item=item,
                        data={"details": "Potential shell injection pattern detected in content.",
                              "severity_override": "WARNING"}
                    ))

        # 4. Permission Validator
        if item.permissions:
            perm = str(item.permissions).strip()
            if not (self.VALID_OCTAL.match(perm) or perm in self.VALID_NAMED_PERMS):
                diagnostics.append(self._forge_diagnostic(
                    key="PROFANE_WILL_HERESY",
                    line=line, item=item,
                    data={"details": f"Permission '{perm}' is invalid. Use octal (755) or named (executable).",
                          "severity_override": "WARNING"}
                ))

    def _audit_logic(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Audits logic directives (@if, @for)."""
        raw = item.raw_scripture.strip()
        match = self.LOGIC_DIRECTIVE_REGEX.match(raw)

        if not match:
            return

        name = match.group('name')
        args = match.group('args').strip()

        # 1. Unknown Directive
        if name not in self.KNOWN_DIRECTIVES:
            diagnostics.append(self._forge_diagnostic(
                key="UNKNOWN_DIRECTIVE_HERESY",
                line=line, item=item,
                data={"details": f"@{name} is not in the Gnostic Grimoire.", "severity_override": "CRITICAL"}
            ))

        # 2. Logic Gate Integrity
        if name in ('if', 'elif') and not args:
            diagnostics.append(self._forge_diagnostic(
                key="CONDITIONAL_WILL_HERESY",
                line=line, item=item,
                data={"details": f"@{name} requires a condition.", "severity_override": "CRITICAL"}
            ))

        if name == 'else' and args:
            diagnostics.append(self._forge_diagnostic(
                key="CONDITIONAL_WILL_HERESY",
                line=line, item=item,
                data={"details": "@else does not accept conditions. Did you mean @elif?",
                      "severity_override": "CRITICAL"}
            ))

    def _audit_variable(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Audits variable definitions ($$)."""
        raw = item.raw_scripture.strip()
        match = self.VAR_DEF_REGEX.match(raw)

        if not match:
            if '$$' in raw and '=' not in raw:
                diagnostics.append(self._forge_diagnostic(
                    key="MALFORMED_VARIABLE_HERESY",
                    line=line, item=item,
                    data={"details": "Variable definition missing assignment operator '='.",
                          "severity_override": "CRITICAL"}
                ))
            return

        name = match.group('name')
        value = match.group('value').strip()

        # 1. Naming Convention (Snake Case)
        if not self.VAR_NAME_SNAKE.match(name):
            diagnostics.append(self._forge_diagnostic(
                key="VAR_NAME_SNAKE",
                line=line, item=item,
                data={
                    "details": f"Variable '{name}' should be snake_case.",
                    "severity_override": "WARNING",
                    "suggestion": name.lower()
                }
            ))

        # 2. Secret Leakage (Hardcoded)
        if self.SECRET_REGEX.search(value):
            if "env(" not in value and "@vault" not in value and "{{" not in value:
                diagnostics.append(self._forge_diagnostic(
                    key="HARDCODED_SECRET_HERESY",
                    line=line, item=item,
                    data={"details": "Potential hardcoded secret detected in variable definition.",
                          "severity_override": "CRITICAL"}
                ))

    def _audit_edict(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Audits Maestro commands (%% post-run)."""
        content = item.content or ""

        # 1. Sudo Usage
        if "sudo " in content:
            diagnostics.append(self._forge_diagnostic(
                key="DIVINE_ESCALATION_HERESY",
                line=line, item=item,
                data={"details": "Usage of 'sudo' is forbidden in post-run scripts.", "severity_override": "CRITICAL"}
            ))

        # 2. Dangerous Operations
        if "rm -rf /" in content or "mkfs" in content:
            diagnostics.append(self._forge_diagnostic(
                key="GUARDIAN_WARD_HERESY",
                line=line, item=item,
                data={"details": "Catastrophic command detected.", "severity_override": "CRITICAL"}
            ))

    def _audit_hygiene(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Universal hygiene checks applicable to any line."""
        text = item.raw_scripture or ""

        # 1. Trailing Whitespace
        if text.rstrip() != text:
            diagnostics.append(self._forge_diagnostic(
                key="STYLISTIC_HERESY_WHITESPACE",
                line=line, item=item,
                data={"details": "Line contains trailing whitespace.", "severity_override": "INFO"}
            ))

        # 2. Jinja Balance & Filters
        if "{{" in text or "{%" in text:
            if text.count("{{") != text.count("}}") or text.count("{%") != text.count("%}"):
                diagnostics.append(self._forge_diagnostic(
                    key="LEXICAL_HERESY_DECONSTRUCTION",
                    line=line, item=item,
                    data={"details": "Unbalanced Jinja2 braces detected.", "severity_override": "CRITICAL"}
                ))

            for match in self.JINJA_BLOCK_REGEX.finditer(text):
                block_content = match.group(0)
                filters = self.JINJA_FILTER_REGEX.findall(block_content)
                for f_name in filters:
                    if f_name not in SAFE_JINJA_FILTERS:
                        diagnostics.append(self._forge_diagnostic(
                            key="UNKNOWN_FILTER_HERESY",
                            line=line, item=item,
                            data={
                                "details": f"Filter '{f_name}' is not in the Grimoire.",
                                "severity_override": "WARNING",
                                "suggestion": f"Did you mean {', '.join(list(SAFE_JINJA_FILTERS)[:3])}?"
                            }
                        ))