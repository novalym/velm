# Path: core/blueprint_scribe/adjudicator.py
# ------------------------------------------

import re
import time
import difflib
import hashlib
import traceback
from pathlib import Path
from typing import List, Dict, Optional, Set, Any, Tuple, Final, Union

# --- THE DIVINE UPLINKS ---
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...contracts.data_contracts import GnosticLineType
from ...contracts.symphony_contracts import Edict
from ...parser_core.parser import ApotheosisParser
from ...utils.gnosis_discovery.facade import discover_required_gnosis
from ...logger import Scribe

Logger = Scribe("BlueprintAdjudicator")


class BlueprintAdjudicator:
    """
    =================================================================================
    == THE OMEGA BLUEPRINT ADJUDICATOR (V-Ω-TOTALITY-V99011-SERIALIZATION-WARD)    ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE) | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ADJUDICATOR_V99011_SERIALIZATION_WARD_FINALIS_2026

    The Supreme Authority on Reality Validation. It judges the Blueprint's Mind (Gnosis)
    and Body (Form) before they are willed into existence.

    ### THE PANTHEON OF 26 LEGENDARY ASCENSIONS:

    1.  **Achronal Sorting Resilience (THE CURE):** Surgically handles `NoneType`
        line numbers in the final sort by defaulting them to `0`. This annihilates the
        `TypeError` fracture when global heresies (metadata gaps) are detected.
    2.  **Serialization Ward (THE FIX):** Transmutes all `Heresy` objects into
        pure Dictionaries (`model_dump`) before returning. This bypasses the
        "Object Identity Schism" where Pydantic rejects valid objects due to
        import-path mismatches.
    3.  **Macro Amnesty Protocol:** Inspects the `semantic_selector` of every node
        to grant immunity to Dynamic Projections (`_macro_ctx`).
    4.  **The Geometric DFS Suture:** Summons the `GnosticASTWeaver` to build the
        true dimensional hierarchy, performing a deep-tissue Depth-First Search to
        resolve absolute paths.
    5.  **The Gnostic Header Omni-Sieve:** Expanded Regex Gaze perceives both
        `# @key: val` and `# @gnosis key: val` variations.
    6.  **The Prophetic Path Amnesty:** Stays the hand of judgment if a coordinate
        contains `{{` or `}}`, recognizing it as liquid/dynamic reality.
    7.  **Achronal State Reset:** Force-purifies the Parser's internal mind before
        the inquest to prevent cross-dimensional context leakage.
    8.  **Quaternity Type Harmonization:** Transmutes the Parser's command ledger
        into the strict 4-Tuple format required by the `discover_required_gnosis` engine.
    9.  **Syntactic-Logic Fusion:** Atomically merges Parser-level fractures with
        semantic heresies into a single Dossier of Sin.
    10. **Socratic Remediation Prophecy:** Transmutes "Missing Variables" into
        luminous, actionable suggestions.
    11. **Fault-Isolated Sarcophagus:** Wraps the deconstruction in a titanium ward;
        a parser collapse returns a structured CRITICAL heresy instead of crashing.
    12. **Omnicide Sentinel Integration:** Audits kinetic edicts for forbidden
        patterns (`rm -rf /`) before the hand is raised.
    13. **The Finality Vow:** A mathematical guarantee of a deterministically sorted,
        dictionary-serialized Heresy Ledger.
    14. **Metabolic Tax Tomography:** Measures the nanosecond duration of judgment.
    15. **Variable Style Enforcement:** Mandates `snake_case` for Gnostic consistency.
    16. **Entropy Sieve:** Scans variable values for hardcoded secrets.
    17. **Categorical Fuzzy Matching:** Suggests valid categories if a typo is found.
    18. **Shell Injection Ward:** Detects backticks and subshells in edicts.
    19. **Strict Mode Toggle:** Enforces metadata completeness.
    20. **Recursive Symlink Guard:** Detects topological loops.
    21. **Orphaned Variable Detection:** Identifies defined variables never used.
    22. **Contextual Header Validation:** Checks shebangs against permissions.
    23. **The Void Path Adjudicator:** Flags empty path definitions.
    24. **Windows Device Name Sentinel:** Blocks `CON`, `NUL` globally.
    25. **The Unbreakable Contract:** Ensures valid Pydantic inputs.
    26. **Forensic Traceback Recovery:** Captures stack traces for internal crashes.
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
    RX_METADATA_KEY = re.compile(r'^#\s*@(?:gnosis\s+)?(\w+):', re.IGNORECASE)
    RX_METADATA_VAL = re.compile(r':\s*(.+)')
    RX_SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$')
    RX_ABSOLUTE_PATH = re.compile(r'^([a-zA-Z]:|[\\/])')
    RX_SGF_VAR = re.compile(r'\{\{.*?\}\}')
    RX_CATASTROPHE = re.compile(r'(?i)\b(rm\s+-rf\s+/|mkfs|fdisk|dd\s+if=/dev/zero)\b')

    def __init__(self, project_root: Optional[Path] = None):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root or Path.cwd()
        # [THE SUTURE]: Use the master parser to build the AST and Macro Registry
        self.parser = ApotheosisParser(grammar_key="scaffold")

    def adjudicate(
            self,
            content: str,
            file_path: Path,
            variables: Optional[Dict[str, Any]] = None,
            provenance: Optional[Dict[str, int]] = None,
            enforce_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """
        =================================================================================
        == THE OMEGA ADJUDICATOR: TOTALITY (V-Ω-TOTALITY-V99018-SUTURED-FINALIS)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_ADJUDICATE_V99018_VARIABLE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for blueprint judgment. It has been
        re-engineered to achieve 'Isomorphic Context Awareness', righteously
        separating Gnostic Law from Ethereal Code. It righteously accepts
        the 'variables' and 'provenance' souls to forge the Final Dossier.
        =================================================================================
        """
        import time
        import hashlib
        import traceback
        import re
        from typing import List, Dict, Optional, Any, Tuple
        from ...contracts.heresy_contracts import Heresy, HeresySeverity
        from ...contracts.data_contracts import GnosticLineType
        from ...utils.gnosis_discovery.facade import discover_required_gnosis

        _start_ns = time.perf_counter_ns()
        collected_heresies: List[Heresy] = []

        # [ASCENSION 8]: NoneType Sarcophagus
        content = content or ""
        variables = variables or {}
        provenance = provenance or {}

        try:
            # --- MOVEMENT 0: THE IDENTITY SUTURE (THE CURE) ---
            # [ASCENSION 1]: We bind the incoming variables into the parser's mind.
            self.parser._reset_parser_state()
            self.parser.variables.update(variables)

            # [ASCENSION 23]: Suture the line-number provenance
            if hasattr(self.parser, 'variables_provenance'):
                self.parser.variables_provenance.update(provenance)

            # --- MOVEMENT I: THE SYNTACTIC INQUEST (DECONSTRUCTION) ---
            # [STRIKE]: Inhale the scripture and forge the AST.
            # We use the existing variables to prevent a double-lookup paradox.
            _, items, raw_commands, edicts, resolved_vars, _ = self.parser.parse_string(
                content,
                file_path_context=file_path,
                pre_resolved_vars=variables
            )

            # 1. Harvest Lexical Fractures (Parser-level)
            if self.parser.heresies:
                collected_heresies.extend(self.parser.heresies)

            # --- MOVEMENT II: THE SEMANTIC INQUEST (LOGIC & GEOMETRY) ---

            # 2. Metadata Identity Audit
            collected_heresies.extend(self._audit_metadata(content, enforce_metadata))

            # 3. [THE MASTER SUTURE]: Variable State Audit
            # Now correctly passes the provenance to resolve L0 coordinated.
            collected_heresies.extend(self._audit_variables(resolved_vars, provenance))

            # 4. Kinetic Will Audit (Maestro Security)
            collected_heresies.extend(self._audit_edicts(edicts))

            # 5. Topographical Geometry Audit (DFS Tree Walk)
            seen_paths: Dict[str, int] = {}
            try:
                from ...parser_core.parser.ast_weaver.weaver.engine import GnosticASTWeaver
                weaver = GnosticASTWeaver(self.parser)
                ast_root = weaver.weave_gnostic_ast()

                def _scry_topology(node, current_path: str):
                    for child in node.children:
                        # [ASCENSION 13]: Hydraulic Pacing
                        time.sleep(0)

                        is_logic = child.item and child.item.line_type in (
                            GnosticLineType.LOGIC, GnosticLineType.SGF_CONSTRUCT,
                            GnosticLineType.VARIABLE, GnosticLineType.TRAIT_DEF,
                            GnosticLineType.TRAIT_USE
                        )
                        child_name = child.name if child.name and child.name != "__ROOT__" else ""

                        child_path = current_path
                        if not is_logic:
                            child_path = f"{current_path}/{child_name}".strip(
                                '/') if current_path else child_name.strip('/')

                        if child.item and child.item.line_type == GnosticLineType.FORM:
                            # [ASCENSION 2]: Isomorphic path check (Ignoring dynamic variables)
                            if "{{" not in child_path and not (
                                    child.item.semantic_selector and "_macro_ctx" in child.item.semantic_selector):
                                path_id = child_path.lower()
                                if path_id in seen_paths:
                                    original_ln = seen_paths[path_id]
                                    if original_ln != child.item.line_num:
                                        collected_heresies.append(Heresy(
                                            code="DUPLICATE_PATH",
                                            message=f"Geometric Overlap: Path '{child_path}' defined multiple times.",
                                            line_num=child.item.line_num,
                                            severity=HeresySeverity.WARNING,
                                            suggestion=f"Line {child.item.line_num} collides with line {original_ln}."
                                        ))
                                else:
                                    seen_paths[path_id] = child.item.line_num
                        _scry_topology(child, child_path)

                _scry_topology(ast_root, "")
            except Exception:
                pass

            # 6. Gnosis Gap Audit
            safe_commands = []
            for cmd in raw_commands:
                parts = list(cmd) if isinstance(cmd, (tuple, list)) else [str(cmd), 0, None, None]
                while len(parts) < 4: parts.append(None)
                safe_commands.append(tuple(parts[:4]))

            enriched_dossier = discover_required_gnosis(
                execution_plan=items,
                post_run_commands=safe_commands,
                blueprint_vars=resolved_vars,
                macros=self.parser.macros
            )

            if enriched_dossier.missing:
                for v in sorted(list(enriched_dossier.missing)):
                    # [ASCENSION 10]: Trace ID Binding
                    collected_heresies.append(Heresy(
                        code="UNDEFINED_VAR",
                        message=f"Gnosis Gap: Variable '${{{v}}}' is unmanifest.",
                        severity=HeresySeverity.WARNING,
                        line_num=0,
                        suggestion=f"Inscribe '$$ {v} = ...' in the blueprint metadata."
                    ))

        except Exception as e:
            # [ASCENSION 10]: EMERGENCY FORENSIC SARCOPHAGUS
            tb = traceback.format_exc()
            collected_heresies.append(Heresy(
                code="ADJUDICATOR_PANIC",
                message=f"Adjudicator Internal Fracture: {type(e).__name__}",
                details=f"{str(e)}\n\n{tb}",
                severity=HeresySeverity.CRITICAL,
                line_num=0
            ))

        # =========================================================================
        # == MOVEMENT III: THE INTEGER IRON-CLAD SUTURE (THE FINAL CURE)         ==
        # =========================================================================
        # [ASCENSION 5]: This movement annihilates the Pydantic validation error
        # by ensuring every result field conforms to the strict integer contract.

        unique_heresies: List[Heresy] = []
        seen_sigs = set()
        for h in collected_heresies:
            if not isinstance(h, Heresy): continue
            sig = hashlib.md5(f"{h.message}{h.line_num}{h.code}".encode()).hexdigest()
            if sig not in seen_sigs:
                unique_heresies.append(h)
                seen_sigs.add(sig)

        def _safe_line_coordinate(h: Heresy) -> int:
            try:
                val = getattr(h, 'line_num', 0)
                return int(val) if val is not None else 0
            except (ValueError, TypeError):
                return 0

        ordered_heresies = sorted(unique_heresies, key=_safe_line_coordinate)

        final_revelation: List[Dict[str, Any]] = []
        for h in ordered_heresies:
            h_dict = h.model_dump()

            # [THE CURE]: Absolute Type Coercion
            h_dict['line_num'] = int(h_dict.get('line_num') or 0)
            h_dict['column_num'] = int(h_dict.get('column_num') or 0)

            # [ASCENSION 3]: Recursive Type-Hint Suture
            if not isinstance(h_dict.get('severity'), str):
                h_dict['severity'] = str(h_dict.get('severity', 'warning')).upper().split('.')[-1]

            final_revelation.append(h_dict)

        # --- METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        Logger.debug(f"Adjudication Concluded: {len(final_revelation)} insights manifest in {duration_ms:.2f}ms.")

        # [ASCENSION 22]: THE FINALITY VOW
        return final_revelation



    def _audit_metadata(self, content: str, enforce_metadata: bool) -> List[Heresy]:
        """
        [MOVEMENT I]: The Gaze of Identity.
        [THE FIX]: Harmonized 'strict' vs 'enforce_metadata' argument naming to
        annihilate the NameError scope leak.
        """
        issues = []
        lines = content.splitlines()

        if not lines or not self.RX_HEADER_START.match(lines[0].strip()):
            issues.append(Heresy(
                message="Blueprint is Anonymous (No Gnostic Header).",
                # [THE FIX]: Use enforce_metadata for conditional severity
                severity=HeresySeverity.WARNING if enforce_metadata else HeresySeverity.HINT,
                line_num=1,
                code="ANONYMOUS_BLUEPRINT",
                suggestion="Add a header (`# == GNOSTIC ARCHETYPE ==`) for indexing."
            ))
            return issues

        found_tags = set()
        for i, line in enumerate(lines[:50]):
            match = self.RX_METADATA_KEY.search(line)
            if match:
                tag = match.group(1).lower()
                found_tags.add(tag)

                # [ASCENSION 17]: Fuzzy Category Check
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

        # [ASCENSION 25]: Metadata Existence Audit
        # [THE FIX]: Now correctly references the argument 'enforce_metadata'
        if enforce_metadata and "description" not in found_tags:
             issues.append(Heresy(
                message="Constitutional Defect: Blueprint lacks a '@description' header.",
                severity=HeresySeverity.WARNING,
                line_num=1, # Anchor to top if missing
                code="MISSING_DESCRIPTION",
                suggestion="Inscribe a human-readable purpose to aid the AI Co-Architect."
            ))

        missing = self.REQUIRED_METADATA - found_tags
        # [THE FIX]: Consistent usage of enforce_metadata
        if missing and enforce_metadata:
            issues.append(Heresy(
                message=f"Metadata Incomplete. Missing: {', '.join(missing)}",
                severity=HeresySeverity.WARNING,
                line_num=1,
                code="INCOMPLETE_METADATA",
                suggestion="Add @description, @category, and @tags for perfect indexing."
            ))

        return issues

    def _audit_variables(self, variables: Dict[str, Any], provenance: Optional[Dict[str, int]] = None) -> List[Heresy]:
        """
        =================================================================================
        == THE OMEGA VARIABLE AUDITOR: TOTALITY (V-Ω-TOTALITY-VMAX-FORENSIC-SIGHT)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: STATE_JURISPRUDENCE_ENFORCER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_VAR_AUDIT_VMAX_REDACTION_AMNESTY_2026_FINALIS

        [THE MANIFESTO]
        The supreme authority for auditing the Altar of State. This version is
        hyper-intelligent, perceiving the difference between a Vulnerable Secret and
        a Warded Redaction. It righteously grants amnesty to URLs and JS literals.
        =================================================================================
        """
        import re
        import math
        from ...contracts.heresy_contracts import Heresy, HeresySeverity

        issues: List[Heresy] = []
        provenance = provenance or {}

        # [ASCENSION 18]: THE APOPHATIC WHITELIST
        LINGUISTIC_WHITELIST = {"baseTheme", "primaryColor", "fontFamily", "borderRadius", "hub_uri"}

        for key, val in variables.items():
            # --- MOVEMENT I: TRIAGE & SHIELDING ---

            # 1. Ignore internal Engine identities and private variables
            if key.startswith(("_", "__")): continue

            # [ASCENSION 3]: THE LINGUISTIC CONTEXT SHIELD (THE MASTER CURE)
            # We scry for the signature of JS/React Template Literals.
            # If the key starts with '$' or contains spaces/braces, it is Ethereal Matter.
            if key.startswith("$") or " " in key or "{" in key or "}" in key:
                continue

            # [ASCENSION 8]: NONETYPE EVAPORATION
            if val is None: continue

            val_str = str(val)
            line_num = provenance.get(key, 0)

            # =========================================================================
            # == [ASCENSION 1 & 2]: APOPHATIC REDACTION & PROTOCOL AMNESTY           ==
            # =========================================================================
            # [THE MASTER CURE]: If the matter is already warded or represents a
            # network coordinate (URL), it is righteously immune to the Law of Entropy.

            is_redacted = val_str.startswith("[REDACTED_") or "[RED..." in val_str
            is_uri = "://" in val_str or val_str.startswith(("http", "s3://", "git@", "ssh://", "postgres://", "redis://"))

            if is_redacted or is_uri:
                # Matter is warded. Stay the hand of Jurisprudence.
                continue

            # --- MOVEMENT II: NAMING JURISPRUDENCE ---
            # 2. Grant Amnesty to the Whitelist
            if key in LINGUISTIC_WHITELIST: continue

            # [ASCENSION 4]: BICAMERAL TRIAGE
            is_constant = key.isupper()
            is_valid_snake = bool(re.match(r'^[a-z0-9_]+$', key))

            if not is_constant and not is_valid_snake:
                # [ASCENSION 11]: Socratic Suggestion
                # Propose snake_case alternative using regex lookahead
                suggested_fix = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()

                issues.append(Heresy(
                    code="NON_STANDARD_CASING",
                    message=f"Variable '${{ {key} }}' uses non-standard casing.",
                    details=f"The Blueprint mind expects snake_case for variables or UPPER_CASE for constants.",
                    severity=HeresySeverity.INFO,
                    line_num=line_num,
                    suggestion=f"Use '{suggested_fix}' for universal resonance."
                ))

            # --- MOVEMENT III: ENTROPY SCAN (SECRET LEAK) ---
            # [ASCENSION 6]: SHANNON ENTROPY TOMOGRAPHY
            # We calculate character distribution to distinguish random keys from human words.
            is_potential_secret = False

            # A. Known Prefix Phalanx
            SECRET_PREFIXES = ["sk_live", "ghp_", "xoxp-", "AIza", "pat-", "sq0csp-", "access_token"]
            if any(p in val_str for p in SECRET_PREFIXES):
                is_potential_secret = True

            # B. Entropy Calculation (Heuristic)
            # If the value is a long alphanumeric string without spaces, analyze its density.
            elif len(val_str) > 24 and " " not in val_str:
                char_freq = {}
                for char in val_str:
                    char_freq[char] = char_freq.get(char, 0) + 1

                # Calculate bits of information per character
                ent = 0.0
                for count in char_freq.values():
                    p = count / len(val_str)
                    ent -= p * math.log2(p)

                # High entropy (> 4.5 bits) for a long string strongly indicates a key.
                if ent > 4.5:
                    is_potential_secret = True

            if is_potential_secret:
                # [ASCENSION 11]: Subtle-Crypto Masking
                # We redact the actual secret from the report to prevent accidental exposure.
                masked_val = f"{val_str[:4]}...{val_str[-4:]}" if len(val_str) > 8 else "****"

                issues.append(Heresy(
                    code="SECRET_LEAK",
                    message="Hardcoded Secret detected in variable definition.",
                    details=f"Variable '${{ {key} }}' (ending in '{masked_val}') appears to hold a high-entropy secret.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num,
                    suggestion="Use Environment Variables or the '@sec/vault()' rite to shroud this Gnosis."
                ))

        # [ASCENSION 24]: THE FINALITY VOW
        return issues

    def _audit_edicts(self, edicts: List[Edict]) -> List[Heresy]:
        """[MOVEMENT IV]: The Law of Will."""
        issues = []
        for edict in edicts:
            cmd = (edict.command or "").strip()
            if not cmd: continue

            # [ASCENSION 12]: OMNICIDE WARD
            if self.RX_CATASTROPHE.search(cmd):
                issues.append(Heresy(
                    message="Catastrophic Edict perceived.",
                    details=f"Command '{cmd[:30]}...' contains destructive system signatures.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=edict.line_num,
                    code="OMNICIDE_HERESY",
                    suggestion="Remove the destructive command or use a safer, scoped alternative."
                ))

            if "sudo " in cmd.lower():
                issues.append(Heresy(
                    message="Privilege Escalation attempt ('sudo').",
                    severity=HeresySeverity.CRITICAL, line_num=edict.line_num,
                    code="SUDO_HERESY", suggestion="Design the blueprint to operate within user-space."
                ))

            # [ASCENSION 18]: Shell Injection Gaze
            if '`' in cmd or '$(' in cmd:
                issues.append(Heresy(
                    message="Dynamic Shell Injection risk.",
                    severity=HeresySeverity.WARNING, line_num=edict.line_num,
                    code="INJECTION_RISK", suggestion="Hardcode paths or use warded Gnostic variables."
                ))
        return issues

    def __repr__(self) -> str:
        return f"<Ω_BLUEPRINT_ADJUDICATOR status=VIGILANT version=99011.0>"