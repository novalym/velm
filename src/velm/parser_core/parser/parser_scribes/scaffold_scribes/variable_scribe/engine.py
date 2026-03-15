# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/engine.py
# ----------------------------------------------------------------------------------

import time
import traceback
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple, Any, Dict, Set

from ..scaffold_base_scribe import ScaffoldBaseScribe
from ......contracts.data_contracts import ScaffoldItem, GnosticVessel, GnosticLineType
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils import generate_derived_names

# --- THE SOVEREIGN ORGANS ---
from .regex_phalanx import VariableRegexPhalanx
from .jit_thawer import JitVariableThawer
from .transmuter import GnosticTransmuter
from .adjudicator import VariableAdjudicator
from .operator_merge import KineticOperator


class VariableScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF GNOSIS (V-Ω-TOTALITY-VMAX-FISSION-ASCENDED)                   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: STATE_INSCRIPTION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_VAR_SCRIBE_VMAX_FISSION_2026_FINALIS

    This divine artisan has been shattered into highly specialized organs. It
    orchestrates the Perception, Thawing, Transmutation, Adjudication, and
    Inscription of variable definitions.
    =================================================================================
    """

    def __init__(self, parser):
        super().__init__(parser, "VariableScribe")
        self._constants: Set[str] = set()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """The Grand Orchestration Rite."""
        _start_ns = time.perf_counter_ns()
        line_num = i + 1 + self.parser.line_offset
        raw_line = vessel.raw_scripture
        trace_id = self.parser.variables.get('trace_id', 'tr-conduct-void')

        forensic_context = ScaffoldItem(
            path=Path(f"VARIABLE:{vessel.name or 'unknown'}"),
            line_num=line_num,
            raw_scripture=raw_line,
            line_type=GnosticLineType.VARIABLE
        )

        try:
            # --- MOVEMENT I: PERCEPTION ---
            var_name, raw_value, type_hint, operator, is_const, end_index = \
                self._perceive_variable_scripture(lines, i, vessel)

            var_name = var_name.replace('-', '_').strip()
            clean_value_str = self._strip_trailing_comment(raw_value)
            if "\n" not in clean_value_str:
                clean_value_str = self._purify_value_string(clean_value_str)

            # --- MOVEMENT II: JIT THAWING (THE MASTER CURE) ---
            # Resolves ELARA templates *before* parsing math/primitives to prevent
            # Topological Collapse (Identity Overwrite).
            clean_value_str = JitVariableThawer.thaw(
                var_name, clean_value_str, self.parser.alchemist, self.parser.variables
            )

            # --- MOVEMENT III: ALCHEMICAL TRANSMUTATION ---
            base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
            final_value = GnosticTransmuter.transmute(clean_value_str, base_dir)

            # --- MOVEMENT IV: ADJUDICATION & STYLING ---
            VariableAdjudicator.check_immutability(var_name, self._constants, line_num)

            # Topological Valence Anchor
            is_path_like = any(sfx in var_name.lower() for sfx in ('_slug', '_name', 'path', 'dir', 'prefix'))

            if type_hint:
                final_value = VariableAdjudicator.enforce_type_contract(
                    var_name, final_value, type_hint, self.parser.contracts, line_num
                )
            else:
                if isinstance(final_value, str):
                    final_value = GnosticTransmuter.transmute_primitive(final_value, is_path_var=is_path_like)

            # --- MOVEMENT V: KINETIC OPERATION ---
            final_value = KineticOperator.apply(var_name, self.parser.variables.get(var_name), final_value, operator,
                                                line_num)

            # --- MOVEMENT VI: INSCRIPTION (THE MIND-BODY SUTURE) ---
            self.parser.variables[var_name] = final_value
            if not var_name.startswith('_'):
                self.parser.blueprint_vars[var_name] = final_value

            # Identity Suture Sychronization
            if var_name == "project_name":
                val_str = str(final_value)
                if "{{" not in val_str and "{%" not in val_str:
                    derived = generate_derived_names(val_str)
                    self.parser.variables.update(derived)
                    self.parser.blueprint_vars.update({k: v for k, v in derived.items() if not k.startswith('_')})

            if is_const:
                self._constants.add(var_name)

            if hasattr(self.parser, 'dossier'):
                self.parser.dossier.mind_atoms[var_name] = final_value

            # --- MOVEMENT VII: TELEMETRY & FINALITY ---
            self._radiate_telemetry(var_name, final_value, operator, trace_id, _start_ns, line_num)

            self.parser._evolve_state_hash(f"var_{var_name}")
            if line_num % 100 == 0: time.sleep(0)

            return end_index

        except ArtisanHeresy as ah:
            self.parser._proclaim_heresy(key=ah.message, item=forensic_context, details=ah.details,
                                         severity=ah.severity)
            return i + 1
        except Exception as catastrophic_paradox:
            tb = traceback.format_exc()
            self.parser._proclaim_heresy(
                key="VARIABLE_SCRIBE_FRACTURE", item=forensic_context,
                details=f"Deconstruction Loop shattered during inscription: {str(catastrophic_paradox)}\n{tb}",
                severity=HeresySeverity.CRITICAL
            )
            return i + 1

    def _perceive_variable_scripture(self, lines: List[str], i: int, vessel: GnosticVessel) -> Tuple[
        str, str, Optional[str], str, bool, int]:
        clean_line = vessel.raw_scripture.strip()

        # Check for Block Syntax First (Ending in :)
        if clean_line.endswith(':'):
            if not any(clean_line.startswith(k) for k in ['if', 'for', 'try', 'macro', 'task']):
                return self._perceive_block_variable(lines, i, clean_line)

        # Check for Inline Syntax (Regex)
        match = VariableRegexPhalanx.INLINE_DEF.match(clean_line)
        if not match:
            raise ArtisanHeresy("MALFORMED_VARIABLE_HERESY: Invalid syntax.", line_num=i + 1)

        prefix, name, type_hint, operator, value = match.group("prefix"), match.group("name"), match.group(
            "type"), match.group("operator"), match.group("value")
        is_const = name == name.upper() if not prefix else prefix == "const" or name == name.upper()

        return name, value, type_hint, operator, is_const, i + 1

    def _perceive_block_variable(self, lines: List[str], i: int, clean_line: str) -> Tuple[
        str, str, Optional[str], str, bool, int]:
        base = clean_line
        for p in ['$$', 'let', 'def', 'const']:
            if base.startswith(p):
                base = base[len(p):].strip()
                break

        name_part = base.rstrip(':')
        type_hint = None
        if ':' in name_part:
            name, type_hint = [x.strip() for x in name_part.split(':', 1)]
        else:
            name = name_part

        is_const = name == name.upper()
        original_indent = self.parser._calculate_original_indent(lines[i])
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, original_indent)
        raw_value = dedent("\n".join(content_lines)).rstrip()

        return name, raw_value, type_hint, "=", is_const, end_index

    def _strip_trailing_comment(self, s: str) -> str:
        if '#' not in s: return s
        in_quote, quote_char = False, None
        for idx, char in enumerate(s):
            if char in ('"', "'"):
                if not in_quote:
                    in_quote, quote_char = True, char
                elif char == quote_char:
                    in_quote, quote_char = False, None
            elif char == '#' and not in_quote:
                return s[:idx].strip()
        return s

    def _purify_value_string(self, raw_value: str) -> str:
        clean = raw_value.strip()
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'"))):
            return clean[1:-1]
        return clean

    def _is_secret_key(self, name: str) -> bool:
        n = name.upper()
        return "KEY" in n or "SECRET" in n or "PASS" in n or "TOKEN" in n or "AUTH" in n

    def _radiate_telemetry(self, var_name: str, final_value: Any, operator: str, trace_id: str, _start_ns: int,
                           line_num: int):
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        is_secret = self._is_secret_key(var_name)
        log_val = "[REDACTED]" if is_secret else str(final_value)[:50]

        self.Logger.verbose(
            f"L{line_num:03d}: Mind Transmuted ({duration_ms:.2f}ms) -> {var_name} {operator} {log_val}")

        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/gnosis_shift",
                    "params": {
                        "key": var_name,
                        "value": "[REDACTED]" if is_secret else str(final_value),
                        "trace_id": trace_id,
                        "aura": "#64ffda" if not is_secret else "#a855f7"
                    }
                })
            except Exception:
                pass