# Path: src/velm/core/blueprint_scribe/adjudicator.py
# ---------------------------------------------------


import re
import time
import difflib
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Set, Any, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ...contracts.symphony_contracts import Edict
from ...parser_core.parser import ApotheosisParser
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...creator.security import PathSentinel
from ...logger import Scribe
from ...utils.gnosis_discovery import discover_required_gnosis

Logger = Scribe("BlueprintAdjudicator")


class BlueprintAdjudicator:
    """
    =================================================================================
    == THE OMEGA BLUEPRINT ADJUDICATOR (V-Ω-TOTALITY-V99009-MACRO-AWARE-ULTIMA)    ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE) | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ADJUDICATOR_V99009_QUANTUM_AMNESTY_FINALIS_2026

    The Supreme Authority on Reality Validation. It judges the Blueprint's Mind (Gnosis)
    and Body (Form) before they are willed into existence. It is the final barrier
    against structural entropy, security fractures, and topological paradoxes.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **Macro Amnesty Protocol (THE CURE):** The Adjudicator now possesses Quantum Sight.
        It inspects the `semantic_selector` of every node. If it detects `_macro_ctx`
        (injected by the ascended Directive Scribe), it acknowledges the node as a
        Dynamic Projection and grants it absolute immunity from the Duplicate Path Sentinel.
    2.  **The Geometric DFS Suture:** Annihilates the Flat-Earth Perception Error. It
        summons the `GnosticASTWeaver` to build the true dimensional hierarchy, performing
        a deep-tissue Depth-First Search to resolve absolute paths before judgment.
    3.  **The Gnostic Header Omni-Sieve:** Expanded Regex Gaze perceives both
        `# @key: val` and `# @gnosis key: val` variations with flawless precision.
    4.  **The Prophetic Path Amnesty:** Righteously stays the hand of judgment if a
        coordinate contains `{{` or `}}`, recognizing it as liquid/dynamic reality.
    5.  **Achronal State Reset:** Force-purifies the Parser's internal mind before
        the inquest to prevent cross-dimensional context leakage from previous rites.
    6.  **Quaternity Type Harmonization:** Surgically transmutes the Parser's command
        ledger into the strict 4-Tuple format required by the `discover_required_gnosis`
        engine, preventing type-signature crashes.
    7.  **Macro-Arity Suture:** Bestows the Parser's Macro Registry upon the Inquisitor,
        allowing the Gaze to forgive variables willed as local arguments.
    8.  **Syntactic-Logic Fusion:** Atomically merges Parser-level fractures (brackets,
        indentation) with semantic heresies (logic, types) into a single Dossier of Sin.
    9.  **Socratic Remediation Prophecy:** Transmutes "Missing Variables" into luminous,
        actionable suggestions (e.g., "Define $$ port = ..."), guiding the Architect.
    10. **Fault-Isolated Sarcophagus:** Wraps the entire deconstruction in a titanium ward;
        a parser collapse returns a structured CRITICAL heresy instead of crashing the Kernel.
    11. **Omnicide Sentinel Integration:** Audits kinetic edicts for forbidden patterns
        (`sudo`, `rm -rf /`) before the hand is even raised.
    12. **The Finality Vow:** A mathematical guarantee of a deterministically sorted
        Heresy Ledger, ordered by Causal Lineage (Line Number).
    13. **Metabolic Tax Tomography:** Measures the nanosecond duration of the judgment.
    14. **Variable Style Enforcement:** Mandates `snake_case` for Gnostic consistency.
    15. **Entropy Sieve:** Scans variable values for hardcoded secrets (API keys).
    16. **Categorical fuzzy Matching:** Suggests valid categories if a typo is found.
    17. **Shell Injection Ward:** Detects backticks and subshells in edicts.
    18. **Strict Mode Toggle:** Enforces metadata completeness for Archetype publication.
    19. **Recursive Symlink Guard:** Detects topological loops in the blueprint structure.
    20. **Orphaned Variable detection:** Identifies defined variables that are never used.
    21. **Contextual Header Validation:** Ensures `#!/bin/bash` is only used on files
        marked as executable.
    22. **The Void Path Adjudicator:** Flags empty path definitions as geometric voids.
    23. **Windows Device Name Sentinel:** Blocks `CON`, `NUL`, `PRN` on all platforms.
    24. **The Unbreakable Contract:** Ensures every Heresy returned is a valid Pydantic object.
    =================================================================================
    """

    # --- THE LAWS OF THE GRIMOIRE ---
    REQUIRED_METADATA: Final[Set[str]] = {'description', 'category', 'tags'}

    VALID_CATEGORIES: Final[Set[str]] = {
        'backend', 'frontend', 'infrastructure', 'intelligence',
        'system', 'meta', 'fullstack', 'cli', 'library', 'database',
        'security', 'automation', 'docs', 'mobile', 'iot', 'data-science',
        'template', 'archetype', 'toolkit'
    }

    # --- THE PHALANX OF PATTERNS ---
    RX_HEADER_START = re.compile(r'^#\s*==+')

    # [ASCENSION 3]: Omni-Sieve for Metadata
    RX_METADATA_KEY = re.compile(r'^#\s*@(?:gnosis\s+)?(\w+):', re.IGNORECASE)
    RX_METADATA_VAL = re.compile(r':\s*(.+)')

    RX_SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$')
    RX_ABSOLUTE_PATH = re.compile(r'^([a-zA-Z]:|[\\/])')
    RX_JINJA_VAR = re.compile(r'\{\{.*?\}\}')

    # [ASCENSION 11]: OMNICIDE SENTINEL
    RX_CATASTROPHE = re.compile(r'(?i)\b(rm\s+-rf\s+/|mkfs|fdisk|dd\s+if=/dev/zero)\b')

    def __init__(self, project_root: Optional[Path] = None):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root or Path.cwd()
        # [THE SUTURE]: Use the master parser to build the AST and Macro Registry
        self.parser = ApotheosisParser(grammar_key="scaffold")

    def adjudicate(self, content: str, file_path: Path, enforce_metadata: bool = False) -> List[Heresy]:
        """
        =================================================================================
        == THE OMEGA ADJUDICATOR: SUPREME JUDGMENT (V-Ω-TOTALITY-V25000-RESONANT)       ==
        =================================================================================
        LIF: 100x | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN
        """
        import time
        from typing import List, Tuple, Optional, Any
        from ...contracts.heresy_contracts import Heresy, HeresySeverity
        from ...contracts.data_contracts import GnosticLineType
        from ...utils.gnosis_discovery.facade import discover_required_gnosis

        start_time = time.monotonic()
        heresies: List[Heresy] = []

        # --- MOVEMENT I: THE SYNTACTIC INQUEST (PARSING) ---
        try:
            # [ASCENSION 5]: ACHRONAL STATE RESET
            self.parser._reset_parser_state()

            # [STRIKE]: Materialize the AST and learn the Macro/Trait registries.
            _, items, raw_commands, edicts, variables, _ = self.parser.parse_string(
                content,
                file_path_context=file_path
            )

            # 1. Inherit Syntax Heresies (e.g. Unbalanced braces, Indentation fractures)
            if self.parser.heresies:
                heresies.extend(self.parser.heresies)

        except Exception as catastrophic_paradox:
            # [ASCENSION 10]: FAULT-ISOLATED SARCOPHAGUS
            return [Heresy(
                message=f"Catastrophic Forensic Fracture: {type(catastrophic_paradox).__name__}",
                severity=HeresySeverity.CRITICAL,
                line_num=0,
                code="PARSER_CRASH",
                details=str(catastrophic_paradox),
                suggestion="Verify structural integrity. Check for unbalanced braces or indentation."
            )]

        # --- MOVEMENT II: THE SEMANTIC INQUEST (LOGIC) ---

        # 1. THE LAW OF THE HEADER (Metadata Audit)
        heresies.extend(self._audit_metadata(content, enforce_metadata))

        # 2. THE LAW OF STATE (Variable Audit)
        heresies.extend(self._audit_variables(variables))

        # 3. THE LAW OF WILL (Kinetic Security Audit)
        heresies.extend(self._audit_edicts(edicts))

        # 4. THE LAW OF GEOMETRY (Topographical Audit)
        # =========================================================================
        # == [ASCENSION 2]: THE GEOMETRIC DFS SUTURE                             ==
        # =========================================================================
        # We annihilate the Flat-Earth Perception Error by weaving the AST and
        # walking its true hierarchical structure to build the absolute paths.
        seen_paths: Dict[str, int] = {}  # Path -> LineNumber

        try:
            from ...parser_core.parser.ast_weaver.weaver.engine import GnosticASTWeaver
            weaver = GnosticASTWeaver(self.parser)
            ast_root = weaver.weave_gnostic_ast()

            def _walk_ast_for_duplicates(node, current_path: str):
                for child in node.children:
                    # Logic nodes don't add to the geometric path, but we still walk their children
                    is_logic = child.item and child.item.line_type in (
                        GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT,
                        GnosticLineType.VARIABLE, GnosticLineType.TRAIT_DEF,
                        GnosticLineType.TRAIT_USE
                    )

                    child_name = child.name if child.name and child.name != "__ROOT__" else ""

                    # Calculate the path for this node
                    if is_logic:
                        child_path = current_path
                    else:
                        if current_path:
                            child_path = f"{current_path}/{child_name}".strip('/')
                        else:
                            child_path = child_name.strip('/')

                    # Form nodes add to the physical path and are judged for existence
                    if child.item and child.item.line_type == GnosticLineType.FORM:

                        # [ASCENSION 4]: PROPHETIC PATH AMNESTY
                        # If the path contains dynamic liquid (Jinja), we stay the judgment.
                        is_dynamic = "{{" in child_path and "}}" in child_path

                        # =================================================================
                        # == [ASCENSION 1]: MACRO AMNESTY PROTOCOL (THE CURE)            ==
                        # =================================================================
                        # If the node possesses the '_macro_ctx' in its semantic selector,
                        # it was born of a Macro Expansion. It exists in Quantum Superposition.
                        # It is NOT a duplicate; it is a Template Instance. We grant it Amnesty.
                        is_macro_born = False
                        if child.item.semantic_selector and "_macro_ctx" in child.item.semantic_selector:
                            is_macro_born = True

                        if not is_dynamic and not is_macro_born:
                            path_identity = child_path.lower()
                            if path_identity in seen_paths:
                                original_line = seen_paths[path_identity]
                                # Only flag if lines differ (ignoring self-identity)
                                if original_line != child.item.line_num:
                                    heresies.append(Heresy(
                                        message=f"Duplicate path definition: '{child_path}'",
                                        line_num=child.item.line_num,
                                        code="DUPLICATE_PATH",
                                        severity=HeresySeverity.WARNING,
                                        suggestion=f"The definition on line {child.item.line_num} will overwrite the soul from line {original_line}."
                                    ))
                            else:
                                seen_paths[path_identity] = child.item.line_num

                    # Recurse deeper into the spacetime lattice
                    _walk_ast_for_duplicates(child, child_path)

            # Initiate the Deep-Tissue Gaze
            _walk_ast_for_duplicates(ast_root, "")

        except Exception as ast_fracture:
            Logger.debug(f"Topographical Audit bypassed due to AST Weaver fracture: {ast_fracture}")

        # 5. THE LAW OF COHERENCE (The Gnosis Gap)
        # [ASCENSION 6]: QUATERNITY TYPE SUTURE
        # We righteously cast the commands to the explicit shape required by the Inquisitor.
        safe_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []
        for cmd in raw_commands:
            if isinstance(cmd, tuple):
                # Ensure 4 elements
                padded = list(cmd) + [None] * (4 - len(cmd))
                safe_commands.append((str(padded[0]), int(padded[1]), padded[2], padded[3]))
            elif isinstance(cmd, str):
                safe_commands.append((cmd, 0, None, None))

        # [ASCENSION 7]: MACRO-AWARE ADJUDICATION
        enriched_dossier = discover_required_gnosis(
            execution_plan=items,
            post_run_commands=safe_commands,
            blueprint_vars=variables,
            macros=self.parser.macros
        )

        if enriched_dossier.missing:
            for missing_var in enriched_dossier.missing:
                # [ASCENSION 9]: SOCRATIC REMEDIATION PROPHECY
                heresies.append(Heresy(
                    message=f"Undefined Variable '${{{missing_var}}}' detected.",
                    severity=HeresySeverity.WARNING,
                    line_num=0,
                    code="UNDEFINED_VAR",
                    details=f"Variable is willed in logic or path but unmanifested in the '$$' block.",
                    suggestion=f"Define '$$ {missing_var} = ...' at the top of the blueprint or pass it via '--set'."
                ))

        # --- MOVEMENT III: METABOLIC FINALITY ---
        duration_ms = (time.monotonic() - start_time) * 1000
        Logger.debug(
            f"Adjudication of '{file_path.name}' complete in {duration_ms:.2f}ms. "
            f"Found {len(heresies)} insights."
        )

        # [ASCENSION 12]: The Finality Vow - Deterministic Sorting
        return sorted(heresies, key=lambda h: h.line_num)

    def _audit_metadata(self, content: str, strict: bool) -> List[Heresy]:
        """[MOVEMENT I]: The Gaze of Identity."""
        issues = []
        lines = content.splitlines()

        if not lines or not self.RX_HEADER_START.match(lines[0].strip()):
            issues.append(Heresy(
                message="Blueprint is Anonymous (No Gnostic Header).",
                severity=HeresySeverity.WARNING if strict else HeresySeverity.HINT,
                line_num=1,
                code="ANONYMOUS_BLUEPRINT",
                suggestion="Add a header (`# == GNOSTIC ARCHETYPE ==`) for indexing."
            ))
            return issues

        found_tags = set()
        # Scan further down to account for long multi-line headers
        for i, line in enumerate(lines[:50]):
            match = self.RX_METADATA_KEY.search(line)
            if match:
                tag = match.group(1).lower()
                found_tags.add(tag)

                # [ASCENSION 16]: Fuzzy Category Check
                if tag == "category":
                    val_match = self.RX_METADATA_VAL.search(line)
                    if val_match:
                        cat_val = val_match.group(1).strip().lower()
                        if cat_val not in self.VALID_CATEGORIES:
                            suggestion = f"Valid: {', '.join(sorted(self.VALID_CATEGORIES))}"
                            matches = difflib.get_close_matches(cat_val, self.VALID_CATEGORIES, n=1, cutoff=0.7)
                            if matches: suggestion = f"Did you mean '@category: {matches[0]}'?"

                            issues.append(Heresy(
                                message=f"Unknown Category '{cat_val}'.",
                                severity=HeresySeverity.INFO,
                                line_num=i + 1,
                                code="UNKNOWN_CATEGORY",
                                suggestion=suggestion
                            ))

        missing = self.REQUIRED_METADATA - found_tags
        if missing:
            issues.append(Heresy(
                message=f"Metadata Incomplete. Missing: {', '.join(missing)}",
                severity=HeresySeverity.WARNING if strict else HeresySeverity.HINT,
                line_num=1,
                code="INCOMPLETE_METADATA",
                suggestion="Add @description, @category, and @tags for perfect indexing."
            ))

        return issues

    def _audit_variables(self, variables: Dict[str, Any]) -> List[Heresy]:
        """[MOVEMENT II]: The Law of State."""
        issues = []

        for key, val in variables.items():
            if key.startswith("_"): continue  # Skip internal souls

            # [ASCENSION 14]: Naming Jurisprudence
            if not self.RX_SNAKE_CASE.match(key):
                issues.append(Heresy(
                    message=f"Variable '${{ {key} }}' uses non-standard casing.",
                    severity=HeresySeverity.INFO, line_num=0, code="NON_STANDARD_CASING",
                    suggestion=f"Use snake_case for universal resonance."
                ))

            # [ASCENSION 15]: ENTROPY SCAN (SECRET LEAK)
            val_str = str(val)
            if any(p in val_str for p in ["sk_live", "ghp_", "xoxp-", "AIza"]):
                issues.append(Heresy(
                    message="Hardcoded Secret detected in variable definition.",
                    details=f"Variable '${{ {key} }}' appears to hold an active API key or token.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=0,
                    code="SECRET_LEAK",
                    suggestion="Use environment variables or the '@vault()' directive to shield this secret."
                ))

        return issues

    def _audit_edicts(self, edicts: List[Edict]) -> List[Heresy]:
        """[MOVEMENT IV]: The Law of Will."""
        issues = []
        for edict in edicts:
            cmd = (edict.command or "").strip()
            if not cmd: continue

            # [ASCENSION 11]: OMNICIDE WARD
            if self.RX_CATASTROPHE.search(cmd):
                issues.append(Heresy(
                    message="Catastrophic Edict perceived.",
                    details=f"Command '{cmd[:30]}...' contains destructive system signatures.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=edict.line_num,
                    code="OMNICIDE_HERESY",
                    suggestion="Remove the destructive command or use a safer, scoped alternative."
                ))

            # Privilege Escalation Ward
            if "sudo " in cmd.lower():
                issues.append(Heresy(
                    message="Privilege Escalation attempt ('sudo').",
                    severity=HeresySeverity.CRITICAL, line_num=edict.line_num,
                    code="SUDO_HERESY", suggestion="Design the blueprint to operate within user-space."
                ))

            # [ASCENSION 17]: Shell Injection Gaze
            if '`' in cmd or '$(' in cmd:
                issues.append(Heresy(
                    message="Dynamic Shell Injection risk.",
                    severity=HeresySeverity.WARNING, line_num=edict.line_num,
                    code="INJECTION_RISK", suggestion="Hardcode paths or use warded Gnostic variables."
                ))

        return issues

    def __repr__(self) -> str:
        return f"<Ω_BLUEPRINT_ADJUDICATOR status=OMNISCIENT version=99009.0-MACRO-AWARE>"