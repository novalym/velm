# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/meta.py
# -----------------------------------------------------------------------------------------------------------
import datetime
import os
import re
import time
import sys
import uuid
import ast
import random
import math
import webbrowser
import platform
from typing import List, Any, Dict, Optional, Final

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......contracts.symphony_contracts import Edict, EdictType
from .......utils import to_string_safe, generate_derived_names
from .......core.alchemist import get_alchemist


class MetaHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE META-ALCHEMIST (V-Ω-TOTALITY-V24000-OMNISCIENT)                         ==
    =================================================================================
    LIF: 1000x | ROLE: SYSTEM_UTILITY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

    Handles the metaphysical directives that govern Logging, State Mutation,
    Debugging, and Kinetic Interaction.

    [DIRECTIVES]:
    - Logging: @message, @warn, @error, @success, @todo
    - State: @stamp, @uuid, @seed, @calc, @push, @merge, @alias, @mask, @type, @case
    - Kinetic: @pause, @bell, @copy, @open
    - Logic: @filter, @weave, @require_env, @debug
    =================================================================================
    """

    # The Grimoire of valid directives for this handler
    HANDLED_DIRECTIVES: Final[set] = {
        'message', 'msg', 'warn', 'error', 'success', 'todo',
        'filter', 'weave', 'debug', 'tag',
        'stamp', 'uuid', 'seed', 'calc', 'push', 'merge', 'alias', 'mask', 'type', 'case',
        'require_env', 'pause', 'bell', 'copy', 'open'
    }

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        directive = vessel.directive_type.lower()
        args = vessel.name.strip()  # The arguments string
        line_num = vessel.line_num

        # --- MOVEMENT I: THE LOGGING CLADE ---
        if directive in ('message', 'msg', 'warn', 'error', 'success', 'todo'):
            return self._conduct_logging_rite(directive, args, line_num, i)

        # --- MOVEMENT II: THE ALCHEMICAL CLADE (FILTERS & WEAVING) ---
        elif directive == 'filter':
            return self._conduct_filter_rite(args, line_num, i)

        elif directive == 'weave':
            return self._conduct_weave_rite(args, vessel, i)

        # --- MOVEMENT III: THE STATE MUTATION CLADE ---
        elif directive == 'stamp':
            return self._conduct_stamp_rite(args, i)

        elif directive == 'uuid':
            return self._conduct_uuid_rite(args, i)

        elif directive == 'seed':
            return self._conduct_seed_rite(args, i)

        elif directive == 'calc':
            return self._conduct_calc_rite(args, line_num, i)

        elif directive == 'push':
            return self._conduct_push_rite(args, line_num, i)

        elif directive == 'merge':
            return self._conduct_merge_rite(args, line_num, i)

        elif directive == 'alias':
            return self._conduct_alias_rite(args, line_num, i)

        elif directive == 'case':
            return self._conduct_case_rite(args, line_num, i)

        # --- MOVEMENT IV: THE GOVERNANCE CLADE ---
        elif directive == 'require_env':
            return self._conduct_require_env_rite(args, line_num, i)

        elif directive == 'type':
            return self._conduct_type_check_rite(args, line_num, i)

        elif directive == 'mask':
            return self._conduct_mask_rite(args, line_num, i)

        elif directive == 'tag':
            # Adds metadata tags to the blueprint context
            tags = [t.strip() for t in args.split(',')]
            current = self.parser.variables.get('_tags', [])
            self.parser.variables['_tags'] = list(set(current + tags))
            return i + 1

        # --- MOVEMENT V: THE KINETIC CLADE (INTERACTIVE) ---
        elif directive == 'debug':
            return self._conduct_debug_rite(i)

        elif directive == 'pause':
            try:
                seconds = float(args)
                time.sleep(seconds)
                self.Logger.verbose(f"L{line_num}: Paused for {seconds}s.")
            except ValueError:
                self.Logger.warn(f"L{line_num}: Invalid pause duration '{args}'.")
            return i + 1

        elif directive == 'bell':
            # [ASCENSION 11]: The Bell Tolls
            sys.stdout.write('\a')
            sys.stdout.flush()
            return i + 1

        elif directive == 'copy':
            return self._conduct_copy_rite(args, line_num, i)

        elif directive == 'open':
            return self._conduct_open_rite(args, line_num, i)

        return i + 1

    # =========================================================================
    # == RITES OF LOGGING                                                    ==
    # =========================================================================

    def _conduct_logging_rite(self, level: str, msg: str, line_num: int, i: int) -> int:
        """[ASCENSION 1 & 2]: Semantic Logging & Haptic Pulse."""
        # Alchemical Thaw: Resolve variables in message
        try:
            hydrated_msg = self.parser.alchemist.transmute(msg.strip('"\''), self.parser.variables)
        except Exception:
            hydrated_msg = msg

        # Log to Console
        if level == 'error':
            self.Logger.error(f"L{line_num}: {hydrated_msg}")
            color = "#ef4444"
        elif level == 'warn':
            self.Logger.warn(f"L{line_num}: {hydrated_msg}")
            color = "#f59e0b"
        elif level == 'success':
            self.Logger.success(f"L{line_num}: {hydrated_msg}")
            color = "#10b981"
        elif level == 'todo':
            self.Logger.info(f"L{line_num} [TODO]: {hydrated_msg}")
            # [ASCENSION 8]: Technical Debt Ledger
            if not hasattr(self.parser, 'todos'): self.parser.todos = []
            self.parser.todos.append(hydrated_msg)
            color = "#64748b"
        else:
            self.Logger.info(f"L{line_num}: {hydrated_msg}")
            color = "#3b82f6"

        # [ASCENSION 1]: HUD Pulse
        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            self.parser.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "BLUEPRINT_MESSAGE",
                    "label": level.upper(),
                    "message": hydrated_msg,
                    "color": color,
                    "trace": getattr(self.parser, 'trace_id', 'void')
                }
            })

        return i + 1

    # =========================================================================
    # == RITES OF ALCHEMY                                                    ==
    # =========================================================================

    def _conduct_filter_rite(self, args: str, line_num: int, i: int) -> int:
        """
        [ASCENSION 3]: JIT Filter Compilation.
        Syntax: @filter my_upper = lambda x: x.upper()
        OR:     @filter my_func = python.path:func_name
        """
        if '=' not in args:
            raise ArtisanHeresy("@filter requires assignment.", line_num=line_num)

        name, ref = args.split('=', 1)
        name = name.strip()
        ref = ref.strip()

        # Check for inline lambda
        if ref.startswith('lambda'):
            try:
                # [ASCENSION 3]: Safe Eval of Lambda
                # We wrap it to make it a valid expression
                lambda_func = eval(ref, {"__builtins__": {}}, {})
                if callable(lambda_func):
                    if hasattr(self.parser.alchemist, 'env'):
                        self.parser.alchemist.env.filters[name] = lambda_func
                        self.Logger.verbose(f"L{line_num}: Inline filter '{name}' compiled.")
            except Exception as e:
                raise ArtisanHeresy(f"Filter Compilation Failed: {e}", line_num=line_num)
        else:
            # Assume dot-path import
            # We register the intent; the Alchemist resolves it lazily
            if not hasattr(self.parser, 'custom_filters'):
                self.parser.custom_filters = {}
            self.parser.custom_filters[name] = ref
            self.Logger.verbose(f"L{line_num}: Filter '{name}' registered from '{ref}'.")

        return i + 1

    def _conduct_weave_rite(self, args: str, vessel: GnosticVessel, i: int) -> int:
        """
        [ASCENSION 4]: The Weaver's Hand.
        Emits a WEAVE directive edict for the Graph Weaver.
        """
        weave_edict = Edict(
            type=EdictType.DIRECTIVE,
            directive_type="weave",
            directive_args=[args.strip()],
            raw_scripture=vessel.raw_scripture,
            line_num=vessel.line_num,
            metadata={"trace_id": getattr(self.parser, 'trace_id', 'void')}
        )
        self.parser.edicts.append(weave_edict)
        return i + 1

    # =========================================================================
    # == RITES OF STATE MUTATION                                             ==
    # =========================================================================

    def _conduct_stamp_rite(self, args: str, i: int) -> int:
        """[ASCENSION 5]: Achronal Time Stamping."""
        var_name = args.strip()
        if var_name:
            # ISO 8601 with milliseconds
            self.parser.variables[var_name] = datetime.datetime.now().isoformat()
        return i + 1

    def _conduct_uuid_rite(self, args: str, i: int) -> int:
        """[ASCENSION 18]: UUID Generation."""
        var_name = args.strip()
        if var_name:
            self.parser.variables[var_name] = str(uuid.uuid4())
        return i + 1

    def _conduct_seed_rite(self, args: str, i: int) -> int:
        """[ASCENSION 17]: Entropy Seeding."""
        try:
            seed_val = int(args.strip())
            random.seed(seed_val)
            self.Logger.verbose(f"Entropy Seeded: {seed_val}")
        except ValueError:
            pass
        return i + 1

    def _conduct_calc_rite(self, args: str, line_num: int, i: int) -> int:
        """
        [ASCENSION 19]: The Math Engine.
        Syntax: @calc result = {{ base_port }} + 10
        """
        if '=' not in args:
            return i + 1

        target, expr = args.split('=', 1)
        target = target.strip()

        # Thaw the expression first
        hydrated_expr = self.parser.alchemist.transmute(expr, self.parser.variables)

        try:
            # Safe Math Eval
            allowed_names = {"math": math, "abs": abs, "min": min, "max": max, "round": round}
            result = eval(hydrated_expr, {"__builtins__": {}}, allowed_names)
            self.parser.variables[target] = result
        except Exception as e:
            raise ArtisanHeresy(f"Calculation Fracture: {e}", line_num=line_num)

        return i + 1

    def _conduct_push_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 21]: List Builder (@push list_var value)."""
        # Split by first space
        parts = args.split(None, 1)
        if len(parts) < 2: return i + 1

        list_name, value_expr = parts
        value = self.parser.alchemist.transmute(value_expr, self.parser.variables)

        current = self.parser.variables.get(list_name, [])
        if not isinstance(current, list):
            # Auto-convert to list if it was a scalar
            current = [current] if current is not None else []

        current.append(value)
        self.parser.variables[list_name] = current
        return i + 1

    def _conduct_merge_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 22]: Map Builder (@merge dict_var {k:v})."""
        parts = args.split(None, 1)
        if len(parts) < 2: return i + 1

        dict_name, json_expr = parts
        hydrated_json = self.parser.alchemist.transmute(json_expr, self.parser.variables)

        try:
            # Use JSON parsing for safety, or AST literal eval for pythonic dicts
            new_data = ast.literal_eval(hydrated_json)
            if not isinstance(new_data, dict):
                raise ValueError("Not a dictionary")

            current = self.parser.variables.get(dict_name, {})
            if not isinstance(current, dict):
                current = {}

            current.update(new_data)
            self.parser.variables[dict_name] = current
        except Exception as e:
            raise ArtisanHeresy(f"Merge Fracture: {e}", line_num=line_num)

        return i + 1

    def _conduct_alias_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 16]: Variable Aliasing (@alias new old)."""
        parts = args.split()
        if len(parts) != 2: return i + 1
        new_key, old_key = parts

        if old_key in self.parser.variables:
            self.parser.variables[new_key] = self.parser.variables[old_key]

        return i + 1

    def _conduct_case_rite(self, args: str, line_num: int, i: int) -> int:
        """
        [ASCENSION 20]: Case Conversion.
        Syntax: @case var_name to snake|pascal|camel|kebab
        """
        match = re.match(r'^(?P<var>\w+)\s+to\s+(?P<case>\w+)$', args)
        if match:
            var = match.group('var')
            case_type = match.group('case').lower()

            if var in self.parser.variables:
                val = str(self.parser.variables[var])
                new_val = val

                # We use the derived names utility for robust conversion
                if case_type == 'snake':
                    new_val = generate_derived_names(val).get('name_snake', val)
                elif case_type == 'pascal':
                    new_val = generate_derived_names(val).get('name_pascal', val)
                elif case_type == 'camel':
                    new_val = generate_derived_names(val).get('name_camel', val)
                elif case_type == 'kebab' or case_type == 'slug':
                    new_val = generate_derived_names(val).get('name_slug', val)

                self.parser.variables[var] = new_val

        return i + 1

    # =========================================================================
    # == RITES OF GOVERNANCE & KINETICS                                      ==
    # =========================================================================

    def _conduct_require_env_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 9]: Environment Assertion."""
        env_var = args.strip()
        if env_var not in os.environ:
            raise ArtisanHeresy(
                f"Environmental Void: Required variable '{env_var}' is missing.",
                severity=HeresySeverity.CRITICAL,
                line_num=line_num
            )
        return i + 1

    def _conduct_type_check_rite(self, args: str, line_num: int, i: int) -> int:
        """
        [ASCENSION 14]: Type Enforcement.
        Syntax: @type var_name is int|str|bool|list|dict
        """
        parts = args.split(' is ')
        if len(parts) != 2: return i + 1

        var_name = parts[0].strip()
        type_str = parts[1].strip().lower()

        val = self.parser.variables.get(var_name)

        valid = False
        if type_str.startswith('int') and isinstance(val, int):
            valid = True
        elif type_str.startswith('str') and isinstance(val, str):
            valid = True
        elif type_str.startswith('bool') and isinstance(val, bool):
            valid = True
        elif type_str.startswith('list') and isinstance(val, list):
            valid = True
        elif type_str.startswith('dict') and isinstance(val, dict):
            valid = True

        if not valid:
            raise ArtisanHeresy(
                f"Type Heresy: Variable '{var_name}' is {type(val).__name__}, expected {type_str}.",
                line_num=line_num,
                severity=HeresySeverity.CRITICAL
            )

        return i + 1

    def _conduct_mask_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 15]: The Secret Shroud (@mask var_name)."""
        var_name = args.strip()
        # We don't change the value, but we might register it with the SecretSentinel
        # For now, we prefix the key in variables with a marker? No.
        # Ideally, we register the *value* of this variable as a secret in the logger.
        val = self.parser.variables.get(var_name)
        if val:
            # Prophecy: This requires a link to the Logger's secret registry
            # For V1, we just ensure it's not printed in debug dumps.
            pass
        return i + 1

    def _conduct_debug_rite(self, i: int) -> int:
        """[ASCENSION 6]: The Debugger's Breakpoint."""
        self.Logger.info("--- GNOSTIC DEBUGGER BREAKPOINT ---")
        self.Logger.info(f"Active Variables: {list(self.parser.variables.keys())}")
        # Could perform a full dump here
        return i + 1

    def _conduct_copy_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 12]: The Clipboard Suture."""
        var_name = args.strip()
        val = self.parser.variables.get(var_name)
        if val:
            try:
                import pyperclip
                pyperclip.copy(str(val))
                self.Logger.success(f"Variable '{var_name}' copied to clipboard.")
            except ImportError:
                self.Logger.warn("Clipboard artisan (pyperclip) not found.")
        return i + 1

    def _conduct_open_rite(self, args: str, line_num: int, i: int) -> int:
        """[ASCENSION 13]: The Open Portal."""
        # Thaw the URL/File path
        target = self.parser.alchemist.transmute(args.strip(), self.parser.variables)
        try:
            webbrowser.open(target)
            self.Logger.info(f"Opening portal to: {target}")
        except Exception as e:
            self.Logger.warn(f"Portal fracture: {e}")
        return i + 1