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
    == THE BLUEPRINT ADJUDICATOR (V-Ω-BENEVOLENT-MENTOR)                           ==
    =================================================================================
    LIF: 10,000,000,000 | ROLE: ARCHITECTURAL_GUIDE

    The central authority on Blueprint Validity. It has been ascended from a strict
    Judge into a wise Mentor. It distinguishes between *Functional Errors* (which break
    reality) and *Stylistic Omissions* (which merely obscure intent).

    ### THE PANTHEON OF JUDGMENTS:
    - **The Header Guide:** Encourages, but does not force, metadata for better indexing.
    - **The Snake Law:** Enforces variable naming conventions for consistency.
    - **The Geometric Law:** Prevents impossible or dangerous file paths.
    - **The Sovereign Law:** Prevents privilege escalation (`sudo`) in edicts.
    """

    # The Laws of the Grimoire Header
    REQUIRED_METADATA = {'description', 'category', 'tags'}

    VALID_CATEGORIES = {
        'backend', 'frontend', 'infrastructure', 'intelligence',
        'system', 'meta', 'fullstack', 'cli', 'library', 'database',
        'security', 'automation', 'docs', 'mobile', 'iot'
    }

    # Pre-compiled Regex Grimoire for High-Speed Scrying
    RX_HEADER_START = re.compile(r'^#\s*==+')
    RX_METADATA_KEY = re.compile(r'#\s*@(\w+):')
    RX_METADATA_VAL = re.compile(r':\s*(.+)')
    RX_SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$')
    RX_ABSOLUTE_PATH = re.compile(r'^([a-zA-Z]:|[\\/])')
    RX_SHELL_INJECTION = re.compile(r'(\;\s*rm\s+-rf)|(\|\s*bash)|(\|\s*sh)|(\$\(.*\))|(`.*`)')

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        # We summon a dedicated parser instance for the Adjudicator
        self.parser = ApotheosisParser(grammar_key="scaffold")

    def adjudicate(self, content: str, file_path: Path, enforce_metadata: bool = False) -> List[Heresy]:
        """
        The Grand Rite of Adjudication.

        Args:
            content: The raw blueprint text.
            file_path: The physical location (for context).
            enforce_metadata: If True, checks are stricter regarding registry standards.
        """
        start_time = time.monotonic()
        heresies: List[Heresy] = []

        # --- MOVEMENT I: THE SYNTACTIC INQUEST (PARSING) ---
        # We must first understand the structure before we can judge the intent.
        try:
            _, items, _, edicts, variables, dossier = self.parser.parse_string(
                content,
                file_path_context=file_path
            )

            # Inherit heresies found during parsing (Syntax Errors)
            # These are usually fatal to understanding, so we prioritize them.
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
                suggestion="Verify the structural integrity of the blueprint. Check for unbalanced braces or indentation errors."
            )]

        # --- MOVEMENT II: THE SEMANTIC INQUEST (LOGIC) ---
        # We perform deep scans on the extracted Gnostic atoms.

        # 1. The Law of the Header (Benevolent)
        heresies.extend(self._audit_metadata(content, enforce_metadata))

        # 2. The Law of State
        heresies.extend(self._audit_variables(variables))

        # 3. The Law of Geometry
        heresies.extend(self._audit_structure(items))

        # 4. The Law of Will
        heresies.extend(self._audit_edicts(edicts))

        duration = (time.monotonic() - start_time) * 1000
        Logger.debug(
            f"Adjudication of '{file_path.name}' complete in {duration:.2f}ms. Found {len(heresies)} insights.")

        return heresies

    def _audit_metadata(self, content: str, strict: bool) -> List[Heresy]:
        """
        Checks for the presence and validity of the Gnostic Header.
        Applies Benevolent Guidance.
        """
        issues = []
        lines = content.splitlines()

        # 0. The Gaze of Intent
        # Does the file *look* like it's trying to have a header?
        has_header_block = len(lines) > 0 and self.RX_HEADER_START.match(lines[0].strip())

        # 1. Header Presence (The Gentle Nudge)
        if not has_header_block:
            if strict:
                # If it's an Archetype (in archetypes/), we warn that it won't be indexed well.
                # But we do NOT mark it critical. The file is still valid.
                issues.append(Heresy(
                    message="Archetype is Anonymous (No Gnostic Header).",
                    severity=HeresySeverity.WARNING,
                    line_num=1,
                    code="UNINDEXED_ARCHETYPE",
                    suggestion="Add a header (`# == GNOSTIC ARCHETYPE: [NAME] ==`) to ensure this pattern appears correctly in the `velm init` registry."
                ))
            else:
                # Local file. A gentle Hint.
                issues.append(Heresy(
                    message="Blueprint is Anonymous.",
                    severity=HeresySeverity.HINT,  # Lowest severity
                    line_num=1,
                    code="ANONYMOUS_BLUEPRINT",
                    suggestion="Consider adding a Gnostic Header to document the intent and author of this reality."
                ))

            # If no header exists, we cannot validate tags, so we return early.
            return issues

        # 2. Metadata Tags (@key: value)
        found_tags = set()

        # Scan first 20 lines for metadata to avoid reading the whole file
        for i, line in enumerate(lines[:20]):
            match = self.RX_METADATA_KEY.search(line)
            if match:
                tag = match.group(1).lower()
                found_tags.add(tag)

                # Validation: Category Fuzzy Matching
                if tag == "category":
                    val_match = self.RX_METADATA_VAL.search(line)
                    if val_match:
                        cat_val = val_match.group(1).strip().lower()
                        if cat_val not in self.VALID_CATEGORIES:
                            # Fuzzy Match Suggestion
                            suggestion = f"Choose from: {', '.join(sorted(self.VALID_CATEGORIES))}"
                            matches = difflib.get_close_matches(cat_val, self.VALID_CATEGORIES, n=1, cutoff=0.7)
                            if matches:
                                suggestion = f"Did you mean '{matches[0]}'?"

                            issues.append(Heresy(
                                message=f"Unknown Category '{cat_val}'.",
                                severity=HeresySeverity.INFO,  # Info, not Warning. It still works.
                                line_num=i + 1,
                                code="UNKNOWN_CATEGORY",
                                suggestion=suggestion
                            ))

        # 3. Missing Tags (Completeness Check)
        # Even in strict mode, missing tags are just Information, not Warnings.
        # We want to encourage completeness, not punish brevity.
        missing = self.REQUIRED_METADATA - found_tags
        if missing:
            severity = HeresySeverity.WARNING if strict else HeresySeverity.HINT
            issues.append(Heresy(
                message=f"Metadata Incomplete. Missing: {', '.join(missing)}",
                severity=severity,
                line_num=1,
                code="INCOMPLETE_METADATA",
                suggestion="Adding '@description', '@category', and '@tags' helps the Librarian index this pattern."
            ))

        return issues

    def _audit_variables(self, variables: Dict[str, Any]) -> List[Heresy]:
        """
        Ensures variable names follow the Snake Case Law and values are sane.
        """
        issues = []

        for key, val in variables.items():
            # 1. Naming Convention
            if not self.RX_SNAKE_CASE.match(key):
                issues.append(Heresy(
                    message=f"Variable '${{ {key} }}' uses non-standard casing.",
                    severity=HeresySeverity.INFO,  # Downgraded to INFO. CamelCase variables work fine.
                    line_num=0,
                    code="NON_STANDARD_CASING",
                    suggestion=f"Convention suggests snake_case (e.g., '{key.lower()}'), but this is valid."
                ))

            # 2. Empty Values
            if val is None or val == "":
                issues.append(Heresy(
                    message=f"Variable '${{ {key} }}' is void (empty).",
                    severity=HeresySeverity.WARNING,
                    line_num=0,
                    code="VOID_VARIABLE",
                    suggestion="Provide a default value or ensure it is injected at runtime."
                ))

        return issues

    def _audit_structure(self, items: List[ScaffoldItem]) -> List[Heresy]:
        """
        Validates the physical form (File/Folder definitions).
        Checks for path safety, content injection, and logical consistency.
        """
        issues = []
        seen_paths = set()

        for item in items:
            if not item.path: continue

            path_str = str(item.path)
            clean_path = path_str.replace('\\', '/')

            # 1. Duplicate Detection
            # A blueprint cannot define the same path twice; the second overwrites the first.
            if path_str in seen_paths:
                issues.append(Heresy(
                    message=f"Duplicate path definition: '{path_str}'",
                    severity=HeresySeverity.WARNING,  # Downgraded. Overwrites are sometimes intentional.
                    line_num=item.line_num,
                    code="DUPLICATE_PATH",
                    suggestion="The second definition will overwrite the first. Merge them if possible."
                ))
            seen_paths.add(path_str)

            # 2. Security: Path Traversal (CRITICAL - Breaks Physics)
            # We use the PathSentinel, wrapping it to catch the specific exception
            try:
                PathSentinel.adjudicate(path_str)
            except Exception as e:
                issues.append(Heresy(
                    message=f"Security Violation in path '{path_str}'",
                    severity=HeresySeverity.CRITICAL,
                    line_num=item.line_num,
                    code="PATH_TRAVERSAL",
                    details=str(e),
                    suggestion="Ensure paths are relative and do not escape the sanctum."
                ))

            # 3. Absolute Path Check (CRITICAL - Breaks Portability)
            if self.RX_ABSOLUTE_PATH.match(clean_path):
                issues.append(Heresy(
                    message=f"Absolute path detected: '{path_str}'",
                    severity=HeresySeverity.CRITICAL,
                    line_num=item.line_num,
                    code="ABSOLUTE_PATH",
                    suggestion="Remove leading slashes. All paths must be relative to project root."
                ))

            # 4. Whitespace in Filenames (INFO)
            if " " in path_str and not item.is_dir:
                issues.append(Heresy(
                    message=f"Whitespace in filename: '{path_str}'",
                    severity=HeresySeverity.INFO,
                    line_num=item.line_num,
                    code="WHITESPACE_PATH",
                    suggestion="Spaces are valid but can cause issues in some shells. Consider snake_case."
                ))

            # 5. Content Injection Scan
            if item.content:
                if self.RX_SHELL_INJECTION.search(item.content):
                    # Heuristic: only flag if it looks like a script
                    is_script = path_str.endswith(('.sh', '.bash', '.py', '.js'))
                    if is_script:
                        issues.append(Heresy(
                            message=f"Potential Shell Injection Pattern in '{path_str}'",
                            severity=HeresySeverity.WARNING,
                            line_num=item.line_num,
                            code="INJECTION_RISK",
                            suggestion="Ensure variable interpolation ({{ var }}) uses the `| shell_escape` filter."
                        ))

        return issues

    def _audit_edicts(self, edicts: List[Any]) -> List[Heresy]:
        """
        Validates the Maestro's commands (%% post-run).
        Ensures automation is safe and sane.
        """
        issues = []

        for edict in edicts:
            cmd = getattr(edict, 'command', '') or ""
            line_num = getattr(edict, 'line_num', 0)

            # 1. Privilege Escalation (Sudo) - CRITICAL
            if "sudo " in cmd:
                issues.append(Heresy(
                    message="Privilege Escalation Detected ('sudo').",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num,
                    code="SUDO_HERESY",
                    suggestion="Do not require root. The Engine runs in user space."
                ))

            # 2. Omnicide Prevention - CRITICAL
            if "rm -rf /" in cmd or "rm -fr /" in cmd or "mkfs" in cmd:
                issues.append(Heresy(
                    message="Catastrophic Command Detected.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num,
                    code="OMNICIDE_HERESY",
                    suggestion="Do not attempt to annihilate the host."
                ))

            # 3. Interactive Commands in Automation - WARNING
            # Commands that wait for user input (vim, nano, less) will hang the engine.
            cmd_start = cmd.strip().split(' ')[0]
            if cmd_start in ['vim', 'vi', 'nano', 'less', 'more', 'man']:
                issues.append(Heresy(
                    message=f"Interactive Command '{cmd_start}' in automation block.",
                    severity=HeresySeverity.WARNING,
                    line_num=line_num,
                    code="INTERACTIVE_BLOCK_HERESY",
                    suggestion="This will hang the automation. Use non-interactive editors (sed/awk) or remove."
                ))

        return issues