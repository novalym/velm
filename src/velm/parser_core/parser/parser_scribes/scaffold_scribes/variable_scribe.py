# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe.py
# ------------------------------------------------------------------------------------
import json
import re
import ast
import yaml
import os
import shlex
import subprocess
import time
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple, Any, Dict, Set, Final

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import ScaffoldItem, GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
# --- THE DIVINE SUMMONS OF THE TYPE SYSTEM ---
from .....jurisprudence_core.gnostic_type_system import GnosticTypeParser
from .....utils import to_snake_case


class VariableScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF GNOSIS (V-Ω-TOTALITY-V12000-GOD-STATE)                        ==
    =================================================================================
    LIF: ∞ | ROLE: STATE_INSCRIPTION_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_VAR_SCRIBE_V12000_ALCHEMICAL_MATH_SHELL_FINALIS_2026

    This divine artisan is the Keeper of State. It perceives, validates, and
    chronicles the `$$` variable definitions. It has been Ascended to handle
    Arithmetic, Shell Execution, List Appending, and Immutable Constants.
    """

    # [ASCENSION 22]: THE REGEX GRIMOIRE
    # Captures: prefix (const/let), name, type hint, operator (=, +=, |=), and value.
    VARIABLE_DEF_REGEX: Final[re.Pattern] = re.compile(
        r"^\s*(?P<prefix>\$\$|let|const|def)\s+"
        r"(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)"
        r"(?:\s*:\s*(?P<type>[^=+\|]+))?"
        r"\s*(?P<operator>=|\+=|\|=)"
        r"\s*(?P<value>.*)$"
    )

    # [ASCENSION 5]: THE SHELL EXPANSION PATTERN
    SHELL_EXEC_REGEX: Final[re.Pattern] = re.compile(r"^\$\((.*)\)$")

    # [ASCENSION 6]: THE ENV EXPANSION PATTERN
    ENV_VAR_REGEX: Final[re.Pattern] = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)(?::-([^}]+))?\}")

    # [ASCENSION 7]: THE ARITHMETIC PATTERN (Simple heuristic)
    MATH_REGEX: Final[re.Pattern] = re.compile(r"^[\d\s+\-*/\(\).]+$")

    def __init__(self, parser):
        super().__init__(parser, "VariableScribe")
        # [ASCENSION 2]: THE IMMUTABLE REGISTRY
        self._constants: Set[str] = set()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Grand Symphony of Gnostic Transcription and Adjudication.
        """
        line_num = i + 1 + self.parser.line_offset
        raw_line = vessel.raw_scripture

        # We forge a temporary, humble item for heresy context.
        temp_name = raw_line.strip().split('=')[0].strip() if '=' in raw_line else "Variable"
        temp_item_for_context = ScaffoldItem(path=Path(temp_name), line_num=line_num, raw_scripture=raw_line,
                                             is_dir=False)

        try:
            # --- MOVEMENT I: THE DUAL-MODE PERCEPTION ---
            # Handles inline (`$$ x = y`) and block (`$$ x:\n ...`) definitions
            var_name, raw_value, type_hint, operator, is_const, end_index, full_scripture = \
                self._perceive_variable_scripture(lines, i)

            # --- MOVEMENT II: THE RITE OF PURIFICATION ---
            # 1. Strip comments
            clean_value_str = self._strip_trailing_comment(raw_value)

            # 2. Strip quotes (unless it's a block which is handled by consumer)
            if not "\n" in clean_value_str:
                clean_value_str = self._purify_value_string(clean_value_str)

            self.Logger.verbose(f"L{line_num:03d}: The Oracle of Gnosis transcribes '$$ {var_name}' ({operator}).")

            # --- MOVEMENT III: THE ALCHEMICAL TRANSMUTATION ---
            # This is the heart of the ascension. Shell, Env, Math, and Primitive thaw.
            final_value = self._transmute_gnosis(var_name, clean_value_str, temp_item_for_context)

            # --- MOVEMENT IV: THE MENTOR'S GAZE (STYLE & STATE) ---
            self._adjudicate_style(var_name, is_const, temp_item_for_context)
            self._adjudicate_immutability(var_name, is_const, operator)

            # --- MOVEMENT V: THE RITE OF GNOSTIC ADJUDICATION (TYPE CHECK) ---
            if type_hint:
                self._adjudicate_type_contract(var_name, final_value, type_hint, temp_item_for_context)

            # --- MOVEMENT VI: THE KINETIC OPERATION (ASSIGN / APPEND / MERGE) ---
            # [ASCENSION 3 & 4]: Apply += and |= logic
            final_value = self._apply_operator(var_name, final_value, operator, temp_item_for_context)

            # --- MOVEMENT VII: THE RITE OF CHRONICLING ---
            # 1. Update the Persistent Ledger (For final report)
            if not var_name.startswith('_'):
                self.parser.blueprint_vars[var_name] = final_value

            # =========================================================================
            # == [THE CURE]: IMMEDIATE CONTEXT SUTURE (ASCENSION 1)                  ==
            # =========================================================================
            # We MUST update the active `variables` map immediately.
            self.parser.variables[var_name] = final_value
            # =========================================================================

            # [ASCENSION 2]: Lock constants
            if is_const:
                self._constants.add(var_name)

            # 2. Forge the AST Node
            # We convert back to string for the content payload
            content_payload = self._serialize_for_ast(final_value)

            var_item = ScaffoldItem(
                path=Path(f"VARIABLE:{var_name}"), is_dir=False, content=content_payload,
                line_num=line_num, raw_scripture=full_scripture,
                original_indent=vessel.original_indent, line_type=GnosticLineType.VARIABLE,
                semantic_selector={
                    "type": "variable_def",
                    "var_name": var_name,
                    "is_const": is_const,
                    "operator": operator,
                    # [ASCENSION 27]: Security Redaction Flag
                    "is_secret": self._is_secret_key(var_name)
                }
            )
            self.parser.raw_items.append(var_item)

            # [ASCENSION 31]: Forensic Logging
            log_val = "[REDACTED]" if self._is_secret_key(var_name) else str(final_value)[:50]
            self.Logger.verbose(
                f"   -> State Mutation: {var_name} {operator} {log_val} (Type: {type(final_value).__name__})")

            return end_index

        except ArtisanHeresy as e:
            self.parser._proclaim_heresy(key=e.message, item=temp_item_for_context, details=e.details,
                                         severity=e.severity)
            return i + 1
        except Exception as e:
            self.parser._proclaim_heresy(
                key="META_HERESY_VARIABLE_SCRIBE_FRACTURED", item=temp_item_for_context,
                details=str(e), exception_obj=e
            )
            return i + 1

    # =========================================================================
    # == THE ALCHEMICAL ENGINE (TRANSMUTATION)                               ==
    # =========================================================================

    def _transmute_gnosis(self, var_name: str, value_str: str, item: ScaffoldItem) -> Any:
        """
        [ASCENSION 5, 6, 7, 8, 10]: The Central Transmutation Hub.
        Decides if the string is Shell, Math, Env, or Primitive.
        """
        # 1. [ASCENSION 8 & 9]: Interactive/Vault Proxy
        # If it's @ask or @vault, we store the directive string or resolve if possible.
        # Currently, we resolve templates via Alchemist, which handles variables.
        # But @vault might need runtime resolution. For now, we treat as string unless alchemist handles it.

        # 2. [ASCENSION 5]: SHELL EXECUTION ($(...))
        shell_match = self.SHELL_EXEC_REGEX.match(value_str)
        if shell_match:
            cmd = shell_match.group(1)
            return self._execute_shell_fragment(cmd)

        # 3. [ASCENSION 6]: ENV VARIABLE EXPANSION (${VAR} or ${VAR:-default})
        # Note: Jinja handles {{ env('VAR') }}, but this adds bash-style ${} syntax support.
        if "${" in value_str:
            value_str = self._expand_env_vars(value_str)

        # 4. [ASCENSION 7]: ARITHMETIC ENGINE
        # If it looks like pure math (digits and operators), evaluate it.
        # Safety: We check against a strict regex to prevent code execution.
        # We also check if it's NOT a version number (contains dots but maybe not spaces)
        if self.MATH_REGEX.match(value_str) and any(op in value_str for op in "+-*/") and not re.search(r'[a-zA-Z]',
                                                                                                        value_str):
            try:
                # Safe eval: only math
                return eval(value_str, {"__builtins__": None}, {})
            except:
                pass

        # 5. [ASCENSION 10]: PRIMITIVE ALCHEMY
        # Thaw YAML/JSON/Boolean/Int
        return self._transmute_primitive(value_str)

    def _transmute_primitive(self, value_str: str) -> Any:
        """
        [ASCENSION 10]: THE PRIMITIVE ALCHEMIST.
        Attempts to thaw strings into Python primitives using YAML safety.
        Recursive descent for lists/dicts.
        """
        # Fast path for template strings
        if "{{" in value_str:
            return value_str

        # [ASCENSION 25]: Boolean Unifier
        v_lower = value_str.lower()
        if v_lower in ('true', 'yes', 'on'): return True
        if v_lower in ('false', 'no', 'off'): return False
        if v_lower in ('null', 'none', 'void'): return None  # [ASCENSION 19]

        # Try YAML parsing for Integers, Floats, Lists, Dicts
        try:
            thawed = yaml.safe_load(value_str)

            # Recursive purification for containers
            if isinstance(thawed, dict):
                return self._recursive_purify(thawed)
            if isinstance(thawed, list):
                return [self._recursive_purify(x) for x in thawed]

            return thawed
        except Exception:
            return value_str

    def _recursive_purify(self, data: Any) -> Any:
        """Helper to ensure nested structures are also primitive-thawed."""
        if isinstance(data, dict):
            return {k: self._recursive_purify(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._recursive_purify(v) for v in data]
        if isinstance(data, str):
            # Check if the string inside the list/dict is actually a boolean/number
            # This handles cases like list = ["true", "8000"] -> [True, 8000]
            # BUT we must be careful not to over-eagerly convert things that should be strings.
            # For V1, we stick to YAML's typing for inside structures.
            return data
        return data

    def _execute_shell_fragment(self, cmd: str) -> str:
        """[ASCENSION 5]: Safe(ish) Shell Execution."""
        # [ASCENSION 32]: SUBSTRATE SHIELD
        if "rm " in cmd or "mkfs" in cmd:
            self.Logger.warn(f"Shell Gaze Averted: Dangerous command '{cmd}'. Returning void.")
            return ""

        try:
            # We run in shell mode to allow pipes, but capture output
            res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True)
            return res.stdout.strip()
        except subprocess.CalledProcessError:
            self.Logger.warn(f"Shell Gaze Failed: '{cmd}'. Returning void.")
            return ""

    def _expand_env_vars(self, value: str) -> str:
        """[ASCENSION 6]: Bash-style Env Expansion."""

        def replace(match):
            key = match.group(1)
            default = match.group(2)
            val = os.getenv(key)
            if val is not None:
                return val
            if default is not None:
                return default
            return ""  # Default to empty if not set and no default

        return self.ENV_VAR_REGEX.sub(replace, value)

    # =========================================================================
    # == THE ADJUDICATION RITES (VALIDATION)                                 ==
    # =========================================================================

    def _adjudicate_style(self, var_name: str, is_const: bool, item: ScaffoldItem):
        """[ASCENSION 22]: The Stylistic Mentor."""
        if is_const:
            if var_name != var_name.upper():
                self.parser._proclaim_heresy(
                    "STYLISTIC_HERESY_CONSTANT", item,
                    details=f"Constant '{var_name}' should be UPPER_CASE.",
                    severity=HeresySeverity.INFO
                )
        else:
            if var_name != to_snake_case(var_name) and not var_name.startswith('_'):
                self.parser._proclaim_heresy(
                    "STYLISTIC_HERESY_VARIABLE", item,
                    details=f"Variable '{var_name}' should be snake_case.",
                    severity=HeresySeverity.INFO
                )

        # [ASCENSION 14]: Shadow Guard
        if hasattr(dict, var_name) or hasattr(list, var_name) or var_name in ('id', 'type', 'format'):
            self.parser._proclaim_heresy(
                "SHADOW_HERESY", item,
                details=f"Variable '{var_name}' shadows a Python builtin. This may cause confusion.",
                severity=HeresySeverity.WARNING
            )

    def _adjudicate_immutability(self, var_name: str, is_const: bool, operator: str):
        """[ASCENSION 2 & 28]: The Immutable Lock."""
        if var_name in self._constants:
            # If it's already a constant, ANY modification is heresy
            raise ArtisanHeresy(
                f"IMMUTABILITY_HERESY: Cannot redefine Constant '{var_name}'.",
                severity=HeresySeverity.CRITICAL
            )

        if not is_const and var_name in self.parser.variables and operator == "=":
            # Re-definition of variable. Allowed, but logged.
            pass

    def _adjudicate_type_contract(self, var_name: str, value: Any, type_hint: str, item: ScaffoldItem):
        """[ASCENSION 4 & 13]: The Type-Contract Adjudicator."""
        if isinstance(value, str) and "{{" in value:
            self.Logger.verbose("   -> Deferred type check for dynamic value.")
            self.parser.variable_contracts[var_name] = type_hint
            return

        try:
            gnostic_type = GnosticTypeParser.parse(type_hint)
            gnostic_type.validate(value, f"$$ {var_name}", self.parser.contracts)
            self.Logger.success(f"      -> Contract verified. '{var_name}' is pure {type_hint}.")
        except ValueError as e:
            raise ArtisanHeresy(
                "CONTRACT_VIOLATION",
                details=f"Variable '{var_name}' ({value}) violates contract '{type_hint}': {e}",
                severity=HeresySeverity.CRITICAL
            )

    def _apply_operator(self, var_name: str, value: Any, operator: str, item: ScaffoldItem) -> Any:
        """[ASCENSION 3 & 4]: The Kinetic Merge."""
        if operator == "=":
            return value

        current = self.parser.variables.get(var_name)

        if current is None:
            raise ArtisanHeresy(
                f"OPERATOR_HERESY: Cannot use '{operator}' on undefined variable '{var_name}'.",
                severity=HeresySeverity.CRITICAL
            )

        if operator == "+=":
            # List Append
            if isinstance(current, list):
                new_list = list(current)
                if isinstance(value, list):
                    new_list.extend(value)
                else:
                    new_list.append(value)
                return new_list
            # String Concat
            elif isinstance(current, str) and isinstance(value, str):
                return current + value
            # Int Add
            elif isinstance(current, (int, float)) and isinstance(value, (int, float)):
                return current + value
            else:
                raise ArtisanHeresy(
                    f"TYPE_MISMATCH_HERESY: Cannot '+=' {type(value)} to {type(current)}.",
                    severity=HeresySeverity.CRITICAL
                )

        if operator == "|=":
            # Dict Merge
            if isinstance(current, dict) and isinstance(value, dict):
                new_dict = current.copy()
                new_dict.update(value)
                return new_dict
            else:
                raise ArtisanHeresy(
                    f"TYPE_MISMATCH_HERESY: Cannot '|=' (merge) {type(value)} to {type(current)}. Both must be dicts.",
                    severity=HeresySeverity.CRITICAL
                )

        return value

    # =========================================================================
    # == INTERNAL UTILITIES                                                  ==
    # =========================================================================

    def _perceive_variable_scripture(self, lines: List[str], i: int) -> Tuple[
        str, str, Optional[str], str, bool, int, str]:
        """
        Parses the variable definition line and potential block content.
        Returns: (name, value, type, operator, is_const, end_index, full_scripture)
        """
        line = lines[i]
        line_num = i + 1 + self.parser.line_offset

        # 1. Strip comments carefully
        clean_line = self._strip_trailing_comment(line).strip()

        match = self.VARIABLE_DEF_REGEX.match(clean_line)
        if not match:
            # Check for block syntax (ending in :)
            # regex expects =/+=, block syntax is `$$ name:`
            if clean_line.endswith(':'):
                return self._perceive_block_variable(lines, i, clean_line)
            raise ArtisanHeresy("MALFORMED_VARIABLE_HERESY: Invalid syntax.", line_num=line_num)

        prefix = match.group("prefix")
        name = match.group("name")
        type_hint = match.group("type")
        operator = match.group("operator")
        value = match.group("value")

        is_const = prefix == "const" or name == name.upper()  # Convention or Keyword

        return name, value, type_hint, operator, is_const, i + 1, line

    def _perceive_block_variable(self, lines: List[str], i: int, clean_line: str) -> Tuple[
        str, str, Optional[str], str, bool, int, str]:
        """Handles `$$ var:` indented blocks."""
        # e.g. `$$ config: dict =` is invalid for block. Block assumes `=` is implied or it's raw text.
        # Scaffold grammar: `$$ name:` starts a text/yaml block.

        # Strip prefix
        base = clean_line
        for p in ['$$', 'let', 'def', 'const']:
            if base.startswith(p):
                base = base[len(p):].strip()
                break

        name_part = base.rstrip(':')

        # Check for type hint in block header: `$$ config: dict:`
        type_hint = None
        if ':' in name_part:
            name, type_hint = [x.strip() for x in name_part.split(':', 1)]
        else:
            name = name_part

        is_const = name == name.upper()

        original_indent = self.parser._calculate_original_indent(lines[i])
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, original_indent)

        full_scripture = lines[i] + "\n" + "\n".join(content_lines)
        raw_value = dedent("\n".join(content_lines)).rstrip()

        return name, raw_value, type_hint, "=", is_const, end_index, full_scripture

    def _strip_trailing_comment(self, s: str) -> str:
        """[ASCENSION 21]: Removes comments while respecting quotes."""
        if '#' not in s: return s
        in_quote = False
        quote_char = None
        for idx, char in enumerate(s):
            if char in ('"', "'"):
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    in_quote = False
                    quote_char = None
            elif char == '#' and not in_quote:
                return s[:idx].strip()
        return s

    def _purify_value_string(self, raw_value: str) -> str:
        """[ASCENSION 20]: Quote Exorcist."""
        clean = raw_value.strip()
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or
                (clean.startswith("'") and clean.endswith("'"))
        ):
            return clean[1:-1]
        return clean

    def _is_secret_key(self, name: str) -> bool:
        """[ASCENSION 27]: Security Redaction."""
        n = name.upper()
        return "KEY" in n or "SECRET" in n or "PASS" in n or "TOKEN" in n or "AUTH" in n

    def _serialize_for_ast(self, value: Any) -> str:
        if isinstance(value, (dict, list, bool, int, float)):
            try:
                return json.dumps(value)
            except:
                return str(value)
        return str(value)