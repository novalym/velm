# // scaffold/parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe.py

import re
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple

import yaml

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import ScaffoldItem, GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
# --- THE DIVINE SUMMONS OF THE TYPE SYSTEM ---
from .....jurisprudence_core.gnostic_type_system import GnosticTypeParser
from .....utils import to_snake_case


class VariableScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF GNOSIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                        ==
    =================================================================================
    This divine artisan is a true, sentient Oracle whose Gaze perceives, validates,
    and chronicles all forms of Gnostic Will. It is the unbreakable conscience of
    the engine's variable system.
    """

    BARE_ASSIGNMENT_REGEX = re.compile(
        r"^\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*(?::\s*(?P<type>[^=]+))?\s*=\s*(?P<value>.*)$"
    )

    def __init__(self, parser):
        super().__init__(parser, "VariableScribe")

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
            var_name, raw_value, type_hint, end_index, full_scripture = self._perceive_variable_scripture(lines, i)

            # --- MOVEMENT II: THE RITE OF PURIFICATION ---
            clean_value = self._purify_value(raw_value)

            self.Logger.verbose(f"L{line_num:03d}: The Oracle of Gnosis transcribes '$$ {var_name}'.")

            # --- MOVEMENT III: THE MENTOR'S GAZE (STYLE & STATE) ---
            if var_name != to_snake_case(var_name):
                self.parser._proclaim_heresy(
                    "STYLISTIC_HERESY_VARIABLE", item=temp_item_for_context,
                    details=f"Variable '{var_name}' is not in snake_case. Suggestion: '{to_snake_case(var_name)}'",
                    severity=HeresySeverity.WARNING
                )

            if var_name in self.parser.blueprint_vars:
                self.Logger.warn(f"Gnostic Warning on L{line_num}: Variable '{var_name}' is being redefined.")

            # --- MOVEMENT IV: THE RITE OF GNOSTIC ADJUDICATION (THE LAW AWAKENED) ---
            if type_hint:
                self.Logger.verbose(
                    f"   -> Adjudicating '{var_name}' against Gnostic Type '[cyan]{type_hint}[/cyan]'...")

                # The Rite of Deferred Judgment: If the soul is a prophecy, we wait.
                if "{{" in clean_value:
                    self.Logger.verbose(
                        "      -> Value contains dynamic Gnosis ({{...}}). Adjudication deferred to runtime.")
                    self.parser.variable_contracts[var_name] = type_hint
                else:
                    self._adjudicate_static_value(var_name, clean_value, type_hint, temp_item_for_context)

            # --- MOVEMENT V: THE RITE OF CHRONICLING ---
            self.parser.blueprint_vars[var_name] = clean_value

            var_item = ScaffoldItem(
                path=Path(f"$$ {var_name}"), is_dir=False, content=clean_value,
                line_num=line_num, raw_scripture=full_scripture,
                original_indent=vessel.original_indent, line_type=GnosticLineType.VARIABLE
            )
            self.parser.raw_items.append(var_item)

            self.Logger.verbose(f"   -> Gnostic Transcription complete. Advancing timeline to line {end_index}.")
            return end_index

        except ArtisanHeresy as e:
            self.parser._proclaim_heresy(key=e.message, item=temp_item_for_context, details=e.details)
            return i + 1
        except Exception as e:
            self.parser._proclaim_heresy(
                key="META_HERESY_VARIABLE_SCRIBE_FRACTURED", item=temp_item_for_context,
                details=str(e), exception_obj=e
            )
            return i + 1

    def _purify_value(self, raw_value: str) -> str:
        """Strips quotes to reveal the pure soul of the value."""
        clean_value = raw_value.strip()
        if len(clean_value) >= 2 and (
                (clean_value.startswith('"') and clean_value.endswith('"')) or
                (clean_value.startswith("'") and clean_value.endswith("'"))
        ):
            return clean_value[1:-1]
        return clean_value

    def _adjudicate_static_value(self, var_name: str, value_str: str, type_hint: str, context_item: ScaffoldItem):
        """A pure artisan that judges a static value against a Gnostic Contract."""
        try:
            gnostic_type = GnosticTypeParser.parse(type_hint)

            try:
                # We use YAML to safely parse structured data like lists/dicts from the string
                parsed_soul = yaml.safe_load(value_str)
            except Exception:
                # If YAML fails (e.g., a string with special chars), use the raw string
                parsed_soul = value_str

            gnostic_type.validate(parsed_soul, f"$$ {var_name}", self.parser.contracts)
            self.Logger.success(f"      -> Gnostic Contract verified. '{var_name}' is pure.")
            self.parser.variable_contracts[var_name] = type_hint

        except ValueError as e:
            self.parser._proclaim_heresy(
                "SCHEMA_VIOLATION_HERESY", item=context_item,
                details=f"Variable '{var_name}' violates Type Contract '{type_hint}':\n{str(e)}",
                severity=HeresySeverity.CRITICAL
            )
        except Exception as e:
            self.parser._proclaim_heresy(
                "MALFORMED_DATA_HERESY", item=context_item,
                details=f"Paradox during type adjudication for '{var_name}': {e}",
                severity=HeresySeverity.CRITICAL
            )

    def _perceive_variable_scripture(self, lines: List[str], i: int) -> Tuple[str, str, Optional[str], int, str]:
        """The Gaze of the Gnostic Alchemist, perceiving a sigil-based scripture."""
        line = lines[i]
        line_num = i + 1 + self.parser.line_offset

        def _strip_comment(s: str) -> str:
            if '#' not in s: return s
            in_quote, quote_char = False, None
            for idx, char in enumerate(s):
                if char in ('"', "'"):
                    if not in_quote:
                        in_quote, quote_char = True, char
                    elif char == quote_char:
                        in_quote, quote_char = False, None
                elif char == '#' and not in_quote:
                    return s[:idx]
            return s

        clean_content_line = _strip_comment(line)
        full_raw_scripture = line
        raw_value_scripture = ""
        end_index = i + 1

        stripped_line = clean_content_line.strip()
        base_decl = stripped_line

        for prefix in ['$$', 'let ', 'def ', 'const ']:
            if base_decl.startswith(prefix):
                base_decl = base_decl[len(prefix):].strip()
                break

        if base_decl.endswith(':'):
            declaration_part = base_decl.rstrip(':').strip()
            if '=' in declaration_part:
                raise ArtisanHeresy("MALFORMED_VARIABLE_HERESY", line_num=line_num)

            original_indent = self.parser._calculate_original_indent(line)
            content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, original_indent)

            if content_lines:
                raw_value_scripture = dedent("\n".join(content_lines)).rstrip()
                full_raw_scripture = line + "\n" + "\n".join(content_lines)
            else:
                raw_value_scripture = ""
        else:
            match = re.match(r'^(?P<declaration>[^=]+)=\s*(?P<value>.*)$', base_decl)
            if not match:
                declaration_part = base_decl
                raw_value_scripture = ""
            else:
                declaration_part = match.group('declaration').strip()
                raw_value_scripture = match.group('value').strip()
            end_index = i + 1

        if ':' in declaration_part:
            var_name, type_hint = [p.strip() for p in declaration_part.split(':', 1)]
        else:
            var_name, type_hint = declaration_part.strip(), None

        if not var_name:
            raise ArtisanHeresy("MALFORMED_VARIABLE_HERESY: No variable name perceived.", line_num=line_num)

        return var_name, raw_value_scripture, type_hint, end_index, full_raw_scripture