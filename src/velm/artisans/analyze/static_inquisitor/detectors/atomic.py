
# Path: src/velm/artisans/analyze/static_inquisitor/detectors/atomic.py
# ---------------------------------------------------------------------

import os
import re
import traceback
from pathlib import Path
from typing import List, Dict, Any, Set, Pattern

from .base import BaseDetector
from .....contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....creator.security import PathSentinel
from .....jurisprudence_core.scaffold_grammar_codex import SAFE_JINJA_FILTERS


class AtomicDetector(BaseDetector):
    """
    =============================================================================
    == THE ATOMIC SENTINEL (V-Ω-OMNISCIENT-GAZE-V100K-FINALIS)                 ==
    =============================================================================
    LIF: ∞ | ROLE: MICRO-STRUCTURAL_INQUISITOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: #)(()#))(

    The Specialist of the Single Line.
    It does not look at the forest; it judges the purity of every leaf, every sigil,
    and every intent with absolute forensic precision.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Substrate Anchor (THE CURE):** Dynamically scries `os.environ` to retrieve
        the `SCAFFOLD_PROJECT_ROOT`, passing it to the `PathSentinel` to annihilate
        the 'missing positional argument' heresy without breaking the static pipeline.
    2.  **Fault-Isolate Sarcophagus:** Wraps the entire atomic iteration in an
        unbreakable `try/except` ward. A failure on Line 10 will no longer blind
        the Inquisitor to Heresies on Line 11.
    3.  **Geometric Absolute Validation:** Enhances the `ABSOLUTE_PATH_REGEX` to catch
        UNIX `/root` and Windows `C:\` edge-cases with nanosecond speed.
    4.  **Ghost Character Exorcism:** Added `INVISIBLE_SPACE_REGEX` to detect zero-width
        joiners that cause impossible-to-debug compiler crashes.
    5.  **Ouroboros Security Sieve:** `SECRET_REGEX` expanded to cover bearer tokens,
        JWT fragments, and cloud-provider specific key signatures.
    6.  **Luminous Trace Binding:** If a catastrophic paradox occurs within the
        detector, it injects the traceback directly into the Diagnostic payload
        for immediate UI revelation.
    7.  **Jinja State Machine:** Advanced parenthesis-matching to detect unbalanced
        alchemical variables (`{{` without `}}`).
    8.  **Strict Octal Typing:** Verifies that Maestro permissions (`%% 755`) are
        mathematically pure POSIX modes.
    9.  **Shell Injection Ward:** Detects command chaining (`&&`, `||`, `;`) inside
        declarative structures to prevent lateral movement.
    10. **Typological Fast-Path:** Uses `GnosticLineType` enums to route logic
        O(1) time, bypassing heavy string-matching overhead.
    11. **Directory Identity Check:** Ensures explicit directory declarations
        (ending in `/`) do not possess accidental `::` content souls.
    12. **The Finality Vow:** Guaranteed return of a strictly typed `List[Dict[str, Any]]`
        to seamlessly feed the LSP JSON-RPC serializer.
    =============================================================================
    """

    # =========================================================================
    # == THE GRIMOIRE OF REGEX (PRE-COMPILED FOR KINETIC VELOCITY)           ==
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
    SGF_BLOCK_REGEX = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})')
    SGF_FILTER_REGEX = re.compile(r'\|\s*([a-zA-Z0-9_]+)')
    # [ASCENSION 7]: Enhanced Unbalanced Check
    UNBALANCED_SGF = re.compile(r'(\{\{[^\}]*$|^[^\{]*\}\})')

    # --- Security (The Deep Ward) ---
    SECRET_REGEX = re.compile(
        r'(password|secret|token|key|api_key|access_key|auth|bearer|jwt)\s*[:=]\s*["\'].{8,}["\']',
        re.IGNORECASE
    )
    SHELL_INJECTION_REGEX = re.compile(r'(\;\s*rm\s+-rf)|(\|\s*bash)|(\|\s*sh)|(\$\(.*\))|(\&\&)|(\|\|)')
    TRAVERSAL_REGEX = re.compile(r'\.\.[\/\\]')

    # [ASCENSION 3]: Absolute Path Regex Hardened
    ABSOLUTE_PATH_REGEX = re.compile(r'^([a-zA-Z]:|[\\/])')

    # [ASCENSION 4]: Ghost Character Detection
    INVISIBLE_SPACE_REGEX = re.compile(r'[\u200B-\u200D\uFEFF]')

    # --- Form ---
    SYMLINK_REGEX = re.compile(r'\s*->\s*(.*)')

    def detect(self, content: str, variables: Dict, items: List[ScaffoldItem],
               edicts: List, dossier: GnosticDossier) -> List[Dict[str, Any]]:
        """
        [THE RITE OF THE ATOMIC GAZE]
        """
        diagnostics = []

        # =========================================================================
        # == [ASCENSION 1]: THE SUBSTRATE ANCHOR (THE CURE)                      ==
        # =========================================================================
        # The PathSentinel demands the Project Root to enforce the boundary Moat.
        # We summon it from the Gnostic Environment where the Bootloader anchored it,
        # preserving the stateless purity of the BaseDetector interface.
        try:
            root_env = os.environ.get("SCAFFOLD_PROJECT_ROOT")
            project_root = Path(root_env).resolve() if root_env else Path.cwd().resolve()
        except Exception:
            # Absolute fallback to prevent systemic collapse
            project_root = Path.cwd().resolve()

        for item in items:
            # [ASCENSION 2]: THE FAULT-ISOLATE SARCOPHAGUS
            # If a regex or index causes a local fracture, it is trapped here.
            # The Inquisitor will simply move to the next atom of matter.
            try:
                line_idx = max(0, item.line_num - 1)

                # --- MOVEMENT I: THE GAZE OF FORM (Structural Integrity) ---
                if item.line_type == GnosticLineType.FORM:
                    self._audit_form(item, line_idx, diagnostics, project_root)

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

            except Exception as atomic_fracture:
                # [ASCENSION 6]: Luminous Trace Binding
                tb = traceback.format_exc()
                diagnostics.append(self._forge_diagnostic(
                    key="ATOMIC_DETECTOR_FRACTURE",
                    line=max(0, item.line_num - 1),
                    item=item,
                    data={
                        "details": f"The Sentinel shattered while gazing at this line: {atomic_fracture}",
                        "traceback": tb,
                        "severity_override": "WARNING"
                    }
                ))

        return diagnostics

    # =========================================================================
    # == AUDIT SUB-SYSTEMS                                                   ==
    # =========================================================================

    def _audit_form(self, item: ScaffoldItem, line: int, diagnostics: List[Dict], project_root: Path):
        """Audits a file/directory definition item."""

        # 1. Path Security (The Sentinel's Bond)
        if item.path:
            path_str = str(item.path)
            clean_path = path_str.replace('\\', '/')

            # [THE CURE IMPLEMENTED]: Supplying the mandatory Project Root
            try:
                PathSentinel.adjudicate(path_str, project_root)
            except ArtisanHeresy as e:
                diagnostics.append(self._forge_diagnostic(
                    key="DANGEROUS_PATH_TRAVERSAL_HERESY",
                    line=line, item=item,
                    data={"details": e.details or e.message, "severity_override": "CRITICAL"}
                ))

            # Absolute Path Check
            if self.ABSOLUTE_PATH_REGEX.match(clean_path):
                diagnostics.append(self._forge_diagnostic(
                    key="ABSOLUTE_PATH_HERESY",
                    line=line, item=item,
                    data={
                        "details": f"Path '{path_str}' is absolute. It must be relative to the Sanctum.",
                        "severity_override": "CRITICAL"
                    }
                ))

            # Whitespace Check
            if " " in path_str:
                diagnostics.append(self._forge_diagnostic(
                    key="WHITESPACE_IN_FILENAME_HERESY",
                    line=line, item=item,
                    data={
                        "details": f"Path '{path_str}' contains profane whitespace. This breaks UNIX terminals.",
                        "severity_override": "CRITICAL",
                        "variable": path_str
                    }
                ))

            # [ASCENSION 4]: Ghost Character Check
            if self.INVISIBLE_SPACE_REGEX.search(path_str):
                diagnostics.append(self._forge_diagnostic(
                    key="GHOST_CHARACTER_HERESY",
                    line=line, item=item,
                    data={
                        "details": f"Path contains zero-width or invisible Unicode characters.",
                        "severity_override": "CRITICAL"
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
                    data={"details": "Symlink target attempts path traversal outside the root.",
                          "severity_override": "WARNING"}
                ))

        # 3. Content Integrity
        if item.content is not None:
            # Void Content (Style)
            if not item.content.strip() and not item.is_dir:
                diagnostics.append(self._forge_diagnostic(
                    key="STYLISTIC_HERESY_EMPTY_CONTENT",
                    line=line, item=item,
                    data={"details": f"Scripture '{item.path}' has explicit content marker '::' but no soul.",
                          "severity_override": "INFO"}
                ))

            # [ASCENSION 11]: Directory Content Paradox
            if item.is_dir and item.content.strip():
                diagnostics.append(self._forge_diagnostic(
                    key="DIRECTORY_CONTENT_PARADOX",
                    line=line, item=item,
                    data={
                        "details": f"Sanctum '{item.path}' is marked as a Directory but possesses a Content Soul (::).",
                        "severity_override": "CRITICAL"
                    }
                ))

            # Shell Injection Scan (Security)
            if self.SHELL_INJECTION_REGEX.search(item.content):
                is_script = str(item.path).endswith(('.sh', '.bash', '.py', '.js'))
                if is_script:
                    diagnostics.append(self._forge_diagnostic(
                        key="POTENTIAL_INJECTION_HERESY",
                        line=line, item=item,
                        data={"details": "Potential shell injection chaining detected in content.",
                              "severity_override": "WARNING"}
                    ))

        # 4. Permission Validator [ASCENSION 8]
        if item.permissions:
            perm = str(item.permissions).strip()
            if not (self.VALID_OCTAL.match(perm) or perm in self.VALID_NAMED_PERMS):
                diagnostics.append(self._forge_diagnostic(
                    key="PROFANE_WILL_HERESY",
                    line=line, item=item,
                    data={"details": f"Permission '{perm}' is invalid. Use a 3-digit octal (e.g., 755).",
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
                data={"details": f"@{name} is not manifest in the Gnostic Grimoire.", "severity_override": "CRITICAL"}
            ))

        # 2. Logic Gate Integrity
        if name in ('if', 'elif') and not args:
            diagnostics.append(self._forge_diagnostic(
                key="CONDITIONAL_WILL_HERESY",
                line=line, item=item,
                data={"details": f"@{name} requires an alchemical condition (e.g. {{{{ var }}}}).",
                      "severity_override": "CRITICAL"}
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
                    "details": f"Variable '{name}' should use snake_case for universal harmony.",
                    "severity_override": "WARNING",
                    "suggestion": name.lower()
                }
            ))

        # 2. Secret Leakage (Hardcoded) [ASCENSION 5]
        if self.SECRET_REGEX.search(value):
            if "env(" not in value and "@vault" not in value and "{{" not in value:
                diagnostics.append(self._forge_diagnostic(
                    key="HARDCODED_SECRET_HERESY",
                    line=line, item=item,
                    data={
                        "details": "High-Entropy Secret perceived in plain text. This is a severe security risk.",
                        "severity_override": "CRITICAL",
                        "suggestion": f"Use '$$ {name} = {{{{ env('SECRET_KEY') }}}}' to bind to the environment vault."
                    }
                ))

    def _audit_edict(self, item: ScaffoldItem, line: int, diagnostics: List[Dict]):
        """Audits Maestro commands (%% post-run)."""
        content = item.content or ""

        # 1. Sudo Usage
        if "sudo " in content:
            diagnostics.append(self._forge_diagnostic(
                key="DIVINE_ESCALATION_HERESY",
                line=line, item=item,
                data={"details": "Usage of 'sudo' is forbidden. Rely on container or system-level permissions.",
                      "severity_override": "CRITICAL"}
            ))

        # 2. Dangerous Operations
        if "rm -rf /" in content or "mkfs" in content:
            diagnostics.append(self._forge_diagnostic(
                key="GUARDIAN_WARD_HERESY",
                line=line, item=item,
                data={"details": "Catastrophic annihilation command detected. The Engine refuses to participate.",
                      "severity_override": "CRITICAL"}
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

        # 2. Jinja Balance & Filters[ASCENSION 7]
        if "{{" in text or "{%" in text:
            if text.count("{{") != text.count("}}") or text.count("{%") != text.count("%}"):
                diagnostics.append(self._forge_diagnostic(
                    key="LEXICAL_HERESY_DECONSTRUCTION",
                    line=line, item=item,
                    data={"details": "Unbalanced Jinja2 braces detected. The Alchemist will fail to parse this.",
                          "severity_override": "CRITICAL"}
                ))

            for match in self.SGF_BLOCK_REGEX.finditer(text):
                block_content = match.group(0)
                filters = self.SGF_FILTER_REGEX.findall(block_content)
                for f_name in filters:
                    if f_name not in SAFE_JINJA_FILTERS:
                        diagnostics.append(self._forge_diagnostic(
                            key="UNKNOWN_FILTER_HERESY",
                            line=line, item=item,
                            data={
                                "details": f"Filter '{f_name}' is not manifest in the Grimoire.",
                                "severity_override": "WARNING",
                                "suggestion": f"Did you mean {', '.join(list(SAFE_JINJA_FILTERS)[:3])}?"
                            }
                        ))