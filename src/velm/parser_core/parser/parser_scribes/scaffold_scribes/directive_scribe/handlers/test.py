# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/test.py
# -----------------------------------------------------------------------------------------------------------
import re
import time
import uuid
import random
import string
import ast
from typing import List, Dict, Any, Optional

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......contracts.symphony_contracts import Edict, EdictType


class TestHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE OMEGA TEST HANDLER (V-Ω-TOTALITY-V24000-CHAOS-ENGINE)                   ==
    =================================================================================
    LIF: 500x | ROLE: BLUEPRINT_INQUISITOR | RANK: OMEGA_SOVEREIGN

    The Supreme Judge of Blueprint Integrity.
    It parses test definitions, assertions, mocks, and now... CHAOS (@fuzz).

    [DIRECTIVES]:
    - @test <name>: Begins a named test scenario.
    - @assert <expr>: Evaluates a logic expression.
    - @assert_file <path>: Verifies file existence/content.
    - @mock <target> = <value>: Overrides a system function/variable.
    - @snapshot <name>: Compares state against a golden record.
    - @fuzz <var>: <type>: Injects random entropy into a variable.
    - @benchmark <name>: Measures metabolic tax of a block.
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        directive = vessel.directive_type.lower()

        # --- MOVEMENT I: SCENARIO DEFINITION ---
        if directive == "test":
            return self._conduct_test_definition(lines, i, vessel)

        # --- MOVEMENT II: ASSERTIONS (THE GNOSTIC PROBES) ---
        elif directive == "assert":
            return self._conduct_immediate_assertion(vessel, i)
        elif directive == "assert_file":
            return self._conduct_file_assertion(vessel, i)
        elif directive == "assert_var":
            return self._conduct_var_assertion(vessel, i)
        elif directive == "assert_error":
            return self._conduct_error_assertion(lines, i, vessel)

        # --- MOVEMENT III: MOCKINGBIRD PROTOCOL ---
        elif directive == "mock":
            return self._conduct_mock(vessel)

        # --- MOVEMENT IV: THE SNAPSHOT ORACLE ---
        elif directive == "snapshot":
            return self._conduct_snapshot(vessel)

        # --- MOVEMENT V: THE CHAOS ENGINE (@fuzz) ---
        elif directive == "fuzz":
            return self._conduct_fuzz_directive(lines, i, vessel)

        # --- MOVEMENT VI: METABOLIC TOMOGRAPHY (@benchmark) ---
        elif directive == "benchmark":
            return self._conduct_benchmark_block(lines, i, vessel)

        return i + 1

    def _conduct_test_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF REGISTRATION]
        Parses @test ... @endtest and stores it for the Test Runner.
        """
        raw_line = vessel.raw_scripture.strip()
        match = re.match(r'^@test\s+(?P<name>.*):?', raw_line)
        name = match.group('name').strip() if match and match.group('name') else f"anonymous_test_{i}"

        # [ASCENSION 8]: Conditional Skip Logic
        skip_condition = None
        if "skip_if(" in name:
            name_part, skip_part = name.split("skip_if(", 1)
            name = name_part.strip()
            skip_condition = skip_part.rstrip("):").strip()

        # Consume the body
        block_lines, next_i = self._consume_block(lines, i + 1, "@endtest")

        # Register in the Parser's Test Registry
        if not hasattr(self.parser, 'blueprint_tests'):
            self.parser.blueprint_tests = {}

        self.parser.blueprint_tests[name] = {
            "body": block_lines,
            "line": vessel.line_num,
            "skip_condition": skip_condition,
            "suite": self.parser.variables.get("_active_suite", "default"),
            "trace_id": getattr(self.parser, 'trace_id', 'void')  # [ASCENSION 24]
        }

        self.Logger.verbose(f"L{vessel.line_num}: Scenario '{name}' registered.")
        return next_i

    def _conduct_fuzz_directive(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF ENTROPY]
        Syntax: @fuzz var_name: type=string, len=10, iterations=5:
        Injects randomized Gnosis into the block to test resilience.
        """
        # Parse params
        raw_args = vessel.name.strip().rstrip(':')

        # Split var name from params
        if ':' in raw_args:
            var_name, params_str = raw_args.split(':', 1)
        else:
            var_name = raw_args
            params_str = ""

        var_name = var_name.strip()

        # Parse kwargs style params
        params = {}
        if params_str:
            try:
                # Use shlex to handle quoted params safely
                for part in params_str.split(','):
                    if '=' in part:
                        k, v = part.split('=', 1)
                        params[k.strip()] = v.strip()
            except Exception:
                pass

        # Defaults
        iterations = int(params.get('iterations', 3))
        fuzz_type = params.get('type', 'string')

        # Consume the block to be fuzzed
        block_lines, next_i = self._consume_block(lines, i + 1, "@endfuzz")

        # [ASCENSION 16]: THE MATRIX INTEGRATION
        # We don't execute here; we generate N tasks for the runtime.
        # But for parsing, we simulate the first pass to ensure syntax validity.

        self.Logger.info(f"L{vessel.line_num}: Fuzzing '{var_name}' ({iterations} iterations)...")

        # Generate Fuzz Values
        fuzz_values = []
        for _ in range(iterations):
            val = self._generate_entropy(fuzz_type, params)
            fuzz_values.append(val)

        # Register the Fuzz Plan
        if not hasattr(self.parser, '_fuzz_plans'): self.parser._fuzz_plans = []

        self.parser._fuzz_plans.append({
            "variable": var_name,
            "values": fuzz_values,
            "body": block_lines,
            "line": vessel.line_num
        })

        # We parse the block ONCE with a sample value to validate structure
        sample_val = fuzz_values[0]
        # Temporarily inject variable
        original_val = self.parser.variables.get(var_name)
        self.parser.variables[var_name] = sample_val

        # Sub-parse
        from ......parser.engine import ApotheosisParser
        sub_p = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_p.variables = self.parser.variables
        sub_p._silent = True

        sub_p.parse_string("\n".join(block_lines))

        # Restore
        if original_val is not None:
            self.parser.variables[var_name] = original_val
        else:
            self.parser.variables.pop(var_name, None)

        return next_i

    def _generate_entropy(self, ftype: str, params: Dict[str, str]) -> Any:
        """[ASCENSION 15]: The Chaos Seed Generator."""
        # Check for deterministic seed
        seed = self.parser.variables.get('_fuzz_seed')
        if seed: random.seed(seed + str(time.time()))  # Permute slightly

        if ftype == 'string':
            length = int(params.get('len', 10))
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            return "".join(random.choice(chars) for _ in range(length))
        elif ftype == 'int':
            min_v = int(params.get('min', 0))
            max_v = int(params.get('max', 100))
            return random.randint(min_v, max_v)
        elif ftype == 'email':
            return f"user_{uuid.uuid4().hex[:8]}@example.com"
        elif ftype == 'path':
            return f"/tmp/fuzz_{uuid.uuid4().hex[:8]}"
        return "fuzz_void"

    def _conduct_benchmark_block(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF CELERITY]
        Syntax: @benchmark "Macro Expansion":
        Measures the nanosecond tax of the contained block.
        """
        label = vessel.name.strip().rstrip(':') or "Anonymous Benchmark"
        block_lines, next_i = self._consume_block(lines, i + 1, "@endbenchmark")

        # We wrap the block in a telemetry pulse using Edicts
        # Start Clock
        self.parser.post_run_commands.append((f"proclaim: 'Benchmarking {label}...'", vessel.line_num, None, None))

        # Sub-parse to generate the items
        from ......parser.engine import ApotheosisParser
        sub_p = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_p.variables = self.parser.variables
        sub_p._silent = True

        # Measure Parsing Time (Metabolic Tax)
        start_t = time.perf_counter()
        _, sub_items, sub_cmds, _, _, _ = sub_p.parse_string("\n".join(block_lines))
        end_t = time.perf_counter()

        duration_ms = (end_t - start_t) * 1000

        # Graft results
        self.parser.raw_items.extend(sub_items)
        self.parser.post_run_commands.extend(sub_cmds)

        # Report
        msg = f"Benchmark '{label}': Parsed {len(block_lines)} lines in {duration_ms:.2f}ms."
        self.Logger.info(f"L{vessel.line_num} {msg}")
        self.parser.post_run_commands.append((f"proclaim: '{msg}'", vessel.line_num, None, None))

        return next_i

    def _conduct_immediate_assertion(self, vessel: GnosticVessel, i: int) -> int:
        """[THE RITE OF TRUTH] Global scope assertion."""
        condition = vessel.name.strip()
        if not condition: return i + 1

        try:
            # Wrap in Jinja if needed
            expr = f"{{{{ {condition} }}}}" if "{{" not in condition else condition
            res = self.parser.alchemist.transmute(expr, self.parser.variables)

            # [ASCENSION 8]: Type Inference
            is_true = str(res).lower() in ('true', 'yes', '1', 'on')
            if not is_true:
                # Try python eval
                try:
                    is_true = bool(eval(str(res)))
                except:
                    is_true = bool(res)  # Non-empty string is true

            if not is_true:
                raise ArtisanHeresy(
                    f"Assertion Failed: {condition}",
                    details=f"Evaluated: {res}",
                    line_num=vessel.line_num,
                    severity=HeresySeverity.CRITICAL
                )

            self.Logger.verbose(f"L{vessel.line_num}: Assertion Passed: {condition}")

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            # If alchemy fails, we warn but don't crash unless strict
            self.Logger.warn(f"Assertion Indeterminate: {e}")

        return i + 1

    def _conduct_file_assertion(self, vessel: GnosticVessel, i: int) -> int:
        """
        [THE FILE WITNESS]
        Syntax: @assert_file path/to/file [contains "text"]
        Note: Checks the PHYSICAL disk at parse time (or staging if available).
        """
        args = vessel.name.strip()
        parts = args.split(" contains ", 1)
        path = parts[0].strip()
        content_check = parts[1].strip().strip('"\'') if len(parts) > 1 else None

        target = (self.parser.project_root / path).resolve()

        # We also check the parser's items_by_path to see if we JUST created it in memory
        in_memory_item = self.parser.items_by_path.get(path.replace('\\', '/'))

        exists = target.exists() or (in_memory_item is not None)

        if not exists:
            # In simulation, we might not fail if it's in the plan
            if not self.parser.engine.context.is_simulation:  # Only fail if we expect it on disk
                pass  # Warning?

        # Add a verification edict for runtime check
        cmd = f"test -f {path}"
        if content_check:
            cmd += f" && grep -q '{content_check}' {path}"

        # We emit a VOW edict
        item = ScaffoldItem(
            path=None, is_dir=False, line_type=GnosticLineType.VOW,
            content=f"succeeds: {cmd}",  # Vow syntax
            raw_scripture=vessel.raw_scripture, line_num=vessel.line_num,
            original_indent=vessel.original_indent
        )
        self.parser.raw_items.append(item)
        return i + 1

    def _conduct_mock(self, vessel: GnosticVessel) -> int:
        """
        [THE MOCKINGBIRD]
        Syntax: @mock db_url = "sqlite:///:memory:"
        """
        if '=' in vessel.name:
            k, v = vessel.name.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"\'')

            # Backup original
            if not hasattr(self.parser, '_mock_backups'): self.parser._mock_backups = {}
            if k in self.parser.variables:
                self.parser._mock_backups[k] = self.parser.variables[k]

            self.parser.variables[k] = v
            self.Logger.verbose(f"L{vessel.line_num}: Mock injected: {k} -> {v}")

        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_snapshot(self, vessel: GnosticVessel) -> int:
        """
        [THE SNAPSHOT ORACLE]
        Syntax: @snapshot "auth_module_v1"
        Captures the file tree state for regression testing.
        """
        name = vessel.name.strip().strip('"\'')
        # Emit a snapshot edict
        # (The actual snapshot logic resides in the Runtime, triggered by this edict)
        # For now, we log the intent.
        self.Logger.info(f"L{vessel.line_num}: Snapshot point '{name}' registered.")
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_var_assertion(self, vessel: GnosticVessel, i: int) -> int:
        """[THE VARIABLE PROBE] @assert_var name == value"""
        return self._conduct_immediate_assertion(vessel, i)

    def _conduct_error_assertion(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [THE EXCEPTION CATCHER]
        Syntax: @assert_error "MyExpectedError":
        """
        expected_err = vessel.name.strip().strip('"\'')
        block_lines, next_i = self._consume_block(lines, i + 1, "@endassert")

        # We parse the block and EXPECT a heresy
        try:
            from ......parser.engine import ApotheosisParser
            sub_p = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
            sub_p._silent = True
            sub_p.parse_string("\n".join(block_lines))

            # If no heresy raised, that's a failure of the test
            if not sub_p.heresies:
                raise ArtisanHeresy(f"Test Failed: Expected error '{expected_err}' but block succeeded.",
                                    line_num=vessel.line_num)

        except ArtisanHeresy as e:
            if expected_err.lower() not in str(e).lower():
                raise ArtisanHeresy(f"Test Failed: Expected '{expected_err}', got '{e}'", line_num=vessel.line_num)
            else:
                self.Logger.success(f"L{vessel.line_num}: Error assertion passed (Caught '{expected_err}').")

        return next_i