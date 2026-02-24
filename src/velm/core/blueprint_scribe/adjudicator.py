# Path: src/velm/core/blueprint_scribe/adjudicator.py
# ---------------------------------------------------

import re
import time
import difflib
from pathlib import Path
from typing import List, Dict, Optional, Set, Any

# --- GNOSTIC UPLINKS ---
from ...parser_core.parser import ApotheosisParser
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...creator.security import PathSentinel
from ...logger import Scribe

Logger = Scribe("BlueprintAdjudicator")


class BlueprintAdjudicator:
    """
    =================================================================================
    == THE BLUEPRINT ADJUDICATOR (V-Ω-TOTALITY-V9000-JINJA-SAFE)                   ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_MENTOR | RANK: OMEGA_SOVEREIGN

    The Supreme Court of Form. It judges the Blueprint before it is allowed to become
    Reality. It distinguishes between **Structural Heresies** (Safety violations)
    and **Stylistic Sins** (Missing metadata).

    [THE CURE]: Ascended to understand the duality of Template vs. File. It cleanses
    Jinja2 syntax (`{{ var }}`) from paths before submitting them to the `PathSentinel`,
    ensuring that valid templates are not flagged as Security Violations.
    """

    # The Laws of the Grimoire Header
    REQUIRED_METADATA = {'description', 'category', 'tags'}

    VALID_CATEGORIES = {
        'backend', 'frontend', 'infrastructure', 'intelligence',
        'system', 'meta', 'fullstack', 'cli', 'library', 'database',
        'security', 'automation', 'docs', 'mobile', 'iot', 'data-science'
    }

    # Pre-compiled Regex Grimoire for High-Speed Scrying
    RX_HEADER_START = re.compile(r'^#\s*==+')
    RX_METADATA_KEY = re.compile(r'#\s*@(\w+):')
    RX_METADATA_VAL = re.compile(r':\s*(.+)')
    RX_SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$')
    RX_ABSOLUTE_PATH = re.compile(r'^([a-zA-Z]:|[\\/])')

    # [ASCENSION 4]: Enhanced Injection Detection
    RX_SHELL_INJECTION = re.compile(r'(\;\s*rm\s)|(\|\s*bash)|(\|\s*sh)|(\$\(.*\))|(`.*`)|(&&\s*sudo)')

    # [ASCENSION 1]: The Jinja Nullifier
    # Matches {{ anything }} so we can replace it with a safe placeholder.
    RX_JINJA_VAR = re.compile(r'\{\{.*?\}\}')

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        # We summon a dedicated parser instance for the Adjudicator
        self.parser = ApotheosisParser(grammar_key="scaffold")

    def adjudicate(self, content: str, file_path: Path, enforce_metadata: bool = False) -> List[Heresy]:
        """
        The Grand Rite of Adjudication.
        """
        start_time = time.monotonic()
        heresies: List[Heresy] = []

        # --- MOVEMENT I: THE SYNTACTIC INQUEST (PARSING) ---
        try:
            # We perform a dry-run parse to build the AST.
            _, items, _, edicts, variables, dossier = self.parser.parse_string(
                content,
                file_path_context=file_path
            )

            # Inherit heresies found during parsing (Syntax Errors)
            if self.parser.heresies:
                heresies.extend(self.parser.heresies)

        except Exception as e:
            # If parsing crashes, the blueprint is fundamentally broken.
            return [Heresy(
                message=f"Catastrophic Parsing Fracture: {str(e)}",
                severity=HeresySeverity.CRITICAL,
                line_num=0,
                code="PARSER_CRASH",
                details=str(e),
                suggestion="Verify structural integrity. Check for unbalanced braces or indentation."
            )]

        # --- MOVEMENT II: THE SEMANTIC INQUEST (LOGIC) ---

        # 1. The Law of the Header
        heresies.extend(self._audit_metadata(content, enforce_metadata))

        # 2. The Law of State (Variables)
        heresies.extend(self._audit_variables(variables))

        # 3. The Law of Geometry (Files/Paths)
        heresies.extend(self._audit_structure(items))

        # 4. The Law of Will (Commands)
        heresies.extend(self._audit_edicts(edicts))

        # 5. The Law of Coherence (Undefined Vars) [ASCENSION 7]
        heresies.extend(self._audit_logic_coherence(items, variables))

        duration = (time.monotonic() - start_time) * 1000
        Logger.debug(
            f"Adjudication of '{file_path.name}' complete in {duration:.2f}ms. Found {len(heresies)} insights.")

        return heresies

    def _audit_metadata(self, content: str, strict: bool) -> List[Heresy]:
        """Checks for the presence and validity of the Gnostic Header."""
        issues = []
        lines = content.splitlines()

        # 0. The Gaze of Intent
        has_header_block = len(lines) > 0 and self.RX_HEADER_START.match(lines[0].strip())

        if not has_header_block:
            if strict:
                issues.append(Heresy(
                    message="Archetype is Anonymous (No Gnostic Header).",
                    severity=HeresySeverity.WARNING,
                    line_num=1,
                    code="UNINDEXED_ARCHETYPE",
                    suggestion="Add a header (`# == GNOSTIC ARCHETYPE ==`) for indexing."
                ))
            else:
                # Local file hint
                issues.append(Heresy(
                    message="Blueprint is Anonymous.",
                    severity=HeresySeverity.HINT,
                    line_num=1,
                    code="ANONYMOUS_BLUEPRINT",
                    suggestion="Consider adding a Gnostic Header."
                ))
            return issues

        found_tags = set()
        for i, line in enumerate(lines[:20]):
            match = self.RX_METADATA_KEY.search(line)
            if match:
                tag = match.group(1).lower()
                found_tags.add(tag)

                if tag == "category":
                    val_match = self.RX_METADATA_VAL.search(line)
                    if val_match:
                        cat_val = val_match.group(1).strip().lower()
                        if cat_val not in self.VALID_CATEGORIES:
                            # [ASCENSION 8]: Fuzzy Suggestion
                            suggestion = f"Choose from: {', '.join(sorted(self.VALID_CATEGORIES))}"
                            matches = difflib.get_close_matches(cat_val, self.VALID_CATEGORIES, n=1, cutoff=0.7)
                            if matches: suggestion = f"Did you mean '{matches[0]}'?"

                            issues.append(Heresy(
                                message=f"Unknown Category '{cat_val}'.",
                                severity=HeresySeverity.INFO,
                                line_num=i + 1,
                                code="UNKNOWN_CATEGORY",
                                suggestion=suggestion
                            ))

        missing = self.REQUIRED_METADATA - found_tags
        if missing:
            severity = HeresySeverity.WARNING if strict else HeresySeverity.HINT
            issues.append(Heresy(
                message=f"Metadata Incomplete. Missing: {', '.join(missing)}",
                severity=severity,
                line_num=1,
                code="INCOMPLETE_METADATA",
                suggestion="Add missing tags for better indexing."
            ))

        return issues

    def _audit_variables(self, variables: Dict[str, Any]) -> List[Heresy]:
        """Ensures variable names follow the Snake Case Law."""
        issues = []

        for key, val in variables.items():
            # 1. Naming Convention
            if not self.RX_SNAKE_CASE.match(key):
                issues.append(Heresy(
                    message=f"Variable '${{ {key} }}' uses non-standard casing.",
                    severity=HeresySeverity.INFO,
                    line_num=0,
                    code="NON_STANDARD_CASING",
                    suggestion=f"Convention suggests snake_case."
                ))

            # 2. Void Values
            if val is None or val == "":
                issues.append(Heresy(
                    message=f"Variable '${{ {key} }}' is void (empty).",
                    severity=HeresySeverity.WARNING,
                    line_num=0,
                    code="VOID_VARIABLE",
                    suggestion="Provide a default value."
                ))

            # 3. [ASCENSION 10]: Entropy Scan (Secrets)
            if "sk_" in str(val) or "ghp_" in str(val):
                issues.append(Heresy(
                    message=f"Hardcoded Secret detected in '${{ {key} }}'.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=0,
                    code="SECRET_LEAK",
                    suggestion="Use environment variables or the @vault directive."
                ))

        return issues

    def _audit_structure(self, items: List[ScaffoldItem]) -> List[Heresy]:
        """
        Validates the physical form.
        [THE CURE]: Sanitizes Jinja variables before security checks.
        """
        issues = []
        seen_paths = set()

        for item in items:
            if not item.path: continue

            path_str = str(item.path)

            # [ASCENSION 1]: THE JINJA SANITIZER
            # We replace {{ anything }} with 'gnostic_var' to validate the structure
            # without triggering false positives on curly braces.
            clean_path_for_check = self.RX_JINJA_VAR.sub('gnostic_var', path_str)
            clean_path_for_check = clean_path_for_check.replace('\\', '/')

            # 1. Duplicate Detection
            if path_str in seen_paths:
                issues.append(Heresy(
                    message=f"Duplicate path definition: '{path_str}'",
                    severity=HeresySeverity.WARNING,
                    line_num=item.line_num,
                    code="DUPLICATE_PATH",
                    suggestion="The second definition will overwrite the first."
                ))
            seen_paths.add(path_str)

            # 2. Security: Path Traversal (CRITICAL)
            # Now we use the sanitized path.
            try:
                PathSentinel.adjudicate(clean_path_for_check, self.project_root)
            except Exception as e:
                issues.append(Heresy(
                    message=f"Security Violation in path '{path_str}'",
                    severity=HeresySeverity.CRITICAL,
                    line_num=item.line_num,
                    code="PATH_TRAVERSAL",
                    details=str(e),
                    suggestion="Ensure paths are relative and do not escape the sanctum."
                ))

            # 3. Absolute Path Check
            if self.RX_ABSOLUTE_PATH.match(clean_path_for_check):
                issues.append(Heresy(
                    message=f"Absolute path detected: '{path_str}'",
                    severity=HeresySeverity.CRITICAL,
                    line_num=item.line_num,
                    code="ABSOLUTE_PATH",
                    suggestion="Remove leading slashes."
                ))

            # 4. [ASCENSION 11]: Recursive Depth Check
            if clean_path_for_check.count('/') > 10:
                issues.append(Heresy(
                    message=f"Excessive Nesting Depth ({clean_path_for_check.count('/')}).",
                    severity=HeresySeverity.WARNING,
                    line_num=item.line_num,
                    code="COMPLEXITY_DEPTH"
                ))

        return issues

    def _audit_edicts(self, edicts: List[Any]) -> List[Heresy]:
        """Validates Maestro commands."""
        issues = []
        for edict in edicts:
            cmd = getattr(edict, 'command', '') or ""
            line_num = getattr(edict, 'line_num', 0)

            # 1. Privilege Escalation
            if "sudo " in cmd:
                issues.append(Heresy(
                    message="Privilege Escalation Detected ('sudo').",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num,
                    code="SUDO_HERESY",
                    suggestion="Do not require root."
                ))

            # 2. Omnicide
            if "rm -rf /" in cmd or "mkfs" in cmd:
                issues.append(Heresy(
                    message="Catastrophic Command Detected.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num,
                    code="OMNICIDE_HERESY"
                ))

            # 3. [ASCENSION 4]: Shell Injection
            if self.RX_SHELL_INJECTION.search(cmd):
                issues.append(Heresy(
                    message="Potential Shell Injection detected.",
                    severity=HeresySeverity.WARNING,
                    line_num=line_num,
                    code="INJECTION_RISK",
                    suggestion="Review command chaining logic."
                ))

        return issues

    def _audit_logic_coherence(self, items: List[ScaffoldItem], variables: Dict[str, Any]) -> List[Heresy]:
        """
        [ASCENSION 7]: Checks if variables used in paths/logic are actually defined.
        """
        issues = []
        defined_vars = set(variables.keys())

        # Simple regex to extract vars from strings
        rx_use = re.compile(r'\{\{\s*([a-zA-Z0-9_]+)\s*\}\}')

        for item in items:
            if not item.path: continue

            # Check variables in Path
            used_vars = rx_use.findall(str(item.path))
            for var in used_vars:
                # We skip 'now', 'uuid', etc as they might be standard library
                if var not in defined_vars and var not in ['now', 'uuid', 'random_id']:
                    issues.append(Heresy(
                        message=f"Undefined Variable '${{ {var} }}' in path.",
                        severity=HeresySeverity.WARNING,
                        line_num=item.line_num,
                        code="UNDEFINED_VAR",
                        suggestion=f"Define '$$ {var} = ...' at the top of the blueprint."
                    ))

        return issues