# Path: scaffold/parser_core/parser/parser_scribes/scaffold_scribes/contract_scribe.py
# ------------------------------------------------------------------------------------


import ast
import re
from pathlib import Path
from typing import List, TYPE_CHECKING, Dict, Any, Optional

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticContract, ContractField, ScaffoldItem, GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from .....jurisprudence_core.gnostic_type_system import GnosticTypeParser, OptionalType, AnyType

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class ContractScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF LAWS (V-Ω-LUMINOUS-VOICE-ULTIMA)                              ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    This divine artisan has achieved its final apotheosis. It now possesses the
    **Luminous Voice**, proclaiming its existence to the parser's timeline by forging
    a `CONTRACT_DEF` item. This annihilates the "Void AST" heresy caused by its
    previous silence.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "ContractScribe")
        self.HEADER_REGEX = re.compile(r"^\s*%%\s*contract\s+(?P<name>\w+)(?:\((?P<parent>\w+)\))?")
        self.FIELD_REGEX = re.compile(
            r"^\s*(?P<name>[\w\?]+)\s*:\s*(?P<type>[^=#]+)(?:\s*=\s*(?P<default>[^#]+))?(?:\s*#\s*(?P<doc>.*))?$"
        )

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Executes the Rite of Legislation.
        """
        line_num = vessel.line_num
        raw_line = vessel.raw_scripture

        match = self.HEADER_REGEX.match(raw_line)
        if not match:
            return i + 1

        contract_name = match.group("name")
        parent_name = match.group("parent")

        self.Logger.verbose(f"L{line_num}: Defining Gnostic Contract '[cyan]{contract_name}[/cyan]'")

        # --- THE MANUAL RITE OF CONSUMPTION ---
        content_lines = []
        current_idx = i + 1
        parent_indent = self.parser._calculate_original_indent(lines[i])

        while current_idx < len(lines):
            line = lines[current_idx]
            stripped = line.strip()

            if not stripped:
                break
            if stripped.startswith(('@', '$$', '%%')):
                self.Logger.verbose(
                    f"   -> Contract block terminated by Gnostic Barrier on L{current_idx + 1}: '{stripped}'")
                break

            current_indent = self.parser._calculate_original_indent(line)
            if current_indent <= parent_indent and not stripped.startswith('#'):
                self.Logger.verbose(f"   -> Contract block terminated by dedent on L{current_idx + 1}.")
                break

            content_lines.append(line)
            current_idx += 1

        end_index = current_idx
        self.Logger.verbose(f"   -> Consumed {len(content_lines)} lines. Returning control at index {end_index}.")

        if not content_lines:
            self.parser._proclaim_heresy("EMPTY_CONTRACT_HERESY", vessel,
                                         details=f"Contract '{contract_name}' has no clauses.",
                                         severity=HeresySeverity.WARNING)
            contract = GnosticContract(name=contract_name, fields={}, raw_scripture=raw_line, line_num=line_num)
        else:
            fields: Dict[str, ContractField] = {}
            if parent_name:
                if parent_name in self.parser.contracts:
                    fields = self.parser.contracts[parent_name].fields.copy()
                else:
                    self.parser._proclaim_heresy("ANCESTRAL_HERESY", vessel,
                                                 details=f"Parent contract '{parent_name}' is unknown.")

            for idx, line in enumerate(content_lines):
                current_line_num = line_num + 1 + idx
                clean_line = line.strip().rstrip(',').rstrip('{').rstrip('}')

                if not clean_line or clean_line.startswith(('#', '//')):
                    continue

                f_match = self.FIELD_REGEX.match(clean_line)
                if not f_match:
                    if ":" in clean_line:
                        err_item = ScaffoldItem(path=Path(f"Contract:{contract_name}"), line_num=current_line_num,
                                                is_dir=False, raw_scripture=line)
                        self.parser._proclaim_heresy("LEXICAL_HERESY_DECONSTRUCTION", err_item,
                                                     details=f"Could not parse contract field: '{clean_line}'",
                                                     severity=HeresySeverity.WARNING)
                    continue

                raw_name, raw_type_str, raw_default = f_match.group("name"), f_match.group(
                    "type").strip(), f_match.group("default")
                is_optional_sigil, f_name = (True, raw_name[:-1]) if raw_name.endswith('?') else (False, raw_name)

                try:
                    gnostic_type = GnosticTypeParser.parse(raw_type_str)
                    if is_optional_sigil and not isinstance(gnostic_type, OptionalType):
                        gnostic_type = OptionalType(gnostic_type)
                except ValueError as e:
                    err_item = ScaffoldItem(path=Path(f"Contract:{contract_name}:{f_name}"), line_num=current_line_num,
                                            is_dir=False, raw_scripture=line)
                    self.parser._proclaim_heresy("INVALID_TYPE_SIG_HERESY", err_item, details=str(e))
                    gnostic_type = AnyType()

                default_val = None
                if raw_default:
                    try:
                        default_val = ast.literal_eval(raw_default.strip())
                    except (ValueError, SyntaxError):
                        default_val = raw_default.strip()

                is_optional = is_optional_sigil or (default_val is not None) or isinstance(gnostic_type, OptionalType)

                if default_val is not None:
                    try:
                        gnostic_type.validate(default_val, f"Default for '{f_name}'", self.parser.contracts)
                    except ValueError:
                        pass

                from .....jurisprudence_core.gnostic_type_system import ListType
                fields[f_name] = ContractField(
                    name=f_name, type_name=raw_type_str, gnostic_type=gnostic_type,
                    default_value=default_val, is_optional=is_optional,
                    is_list=isinstance(gnostic_type, ListType),
                    constraints=gnostic_type.constraints
                )

            contract = GnosticContract(name=contract_name, fields=fields,
                                       raw_scripture="\n".join([raw_line] + content_lines), line_num=line_num)

        # --- THE FINAL PROCLAMATION RITES ---
        self.parser.contracts[contract_name] = contract

        # [THE LUMINOUS VOICE]
        # We proclaim a `ScaffoldItem` for this entire block. This is the Gnostic act
        # that inscribes its existence into the linear timeline for the AST Weaver.
        vessel.content = "\n".join(content_lines)
        self.parser._proclaim_final_item(vessel)

        self.Logger.success(f"Gnostic Contract '[cyan]{contract_name}[/cyan]' consecrated and proclaimed.")
        return end_index