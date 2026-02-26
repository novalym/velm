# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/python.py
# -------------------------------------------------------------------------------------------------------------
import json
import os
import re
import textwrap
import traceback
from typing import List
from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class PythonHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE NATIVE ALCHEMIST (V-Ω-JIT-PYTHON-BINDING-V1000)                         ==
    =================================================================================
    LIF: 1000x | ROLE: FUNCTION_AS_MATTER | RANK: OMEGA_SOVEREIGN

    Handles @py_func to dynamically compile and bind Python logic into the Gnostic Mind.
    This allows Blueprints to define complex logic (regex, math, API calls) that goes
    beyond Jinja's capabilities, without needing external plugins.

    [ASCENSION]: Uses a restricted execution namespace to prevent 'globals()' leakage.
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        directive = vessel.directive_type

        if directive == "py_func":
            return self._conduct_py_func(lines, i, vessel.raw_scripture)

        elif directive == "inject_vow":
            return self._conduct_inject_vow(lines, i, vessel.raw_scripture)

        return i + 1

    def _conduct_py_func(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        Compiles a python function block and registers it as a Global in the Alchemist.
        """
        # Signature: @py_func my_func(x, y):
        # We use a robust regex to capture the full signature including args
        match = re.match(r'^@py_func\s+(?P<sig>\w+\s*\(.*?\))\s*:?', raw_line.strip())
        if not match:
            raise ArtisanHeresy(
                "Malformed @py_func signature.",
                details="Expected syntax: @py_func name(args):",
                line_num=i + 1,
                severity=HeresySeverity.CRITICAL
            )

        sig = match.group('sig')
        # Extract just the function name for registration
        func_name = sig.split('(')[0].strip()

        # Consume the body until @endfunc
        block_lines, next_i = self._consume_block(lines, i + 1, "@endfunc")

        if not block_lines:
            self.Logger.warn(f"L{i + 1}: @py_func '{func_name}' is a void (empty body).")
            return next_i

        # Clean Indentation (Dedent)
        # The user writes the body indented, but exec() expects it relative to the def
        try:
            raw_python = textwrap.dedent("\n".join(block_lines))
            # Wrap in function definition and indent the body
            func_def = f"def {sig}:\n" + textwrap.indent(raw_python, "    ")
        except Exception as e:
            raise ArtisanHeresy(f"Python Indentation Heresy: {e}", line_num=i + 1)

        # JIT Compilation
        try:
            # We compile it in a restricted global namespace
            # We inject 'variables' so the function can read blueprint state
            local_namespace = {
                'variables': self.parser.variables,
                'log': self.Logger,
                're': re,  # Standard library access
                'os': os,  # Standard library access (use with caution)
                'json': json
            }

            # Execute the definition to create the function object
            exec(func_def, {}, local_namespace)

            # Retrieve the function object
            compiled_func = local_namespace.get(func_name)

            if not compiled_func:
                raise ArtisanHeresy(f"Compilation Ghost: Function '{func_name}' was not created.", line_num=i + 1)

            # Bind the function to the Alchemist's Jinja Environment
            # This makes it callable as {{ my_func(...) }} inside templates
            if hasattr(self.parser.alchemist, 'env'):
                self.parser.alchemist.env.globals[func_name] = compiled_func
                self.Logger.verbose(f"L{i + 1}: Native Python Rite '{func_name}' bound to Alchemist.")
            else:
                self.Logger.warn("Alchemist Environment unmanifest. Function compiled but not bound.")

        except Exception as e:
            tb = traceback.format_exc()
            raise ArtisanHeresy(
                f"Native Python Compilation Failed: {e}",
                details=f"Code:\n{func_def}\n\nTraceback:\n{tb}",
                line_num=i + 1,
                severity=HeresySeverity.CRITICAL
            )

        return next_i

    def _conduct_inject_vow(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        [ASCENSION 35]: DYNAMIC VOW INJECTION.
        Allows the blueprint to define custom ?? vows (assertions) written in Python.

        Syntax:
        @inject_vow my_custom_check(arg):
            return arg == 'expected'
        @endvow
        """
        # Signature parsing
        match = re.match(r'^@inject_vow\s+(?P<sig>\w+\s*\(.*?\))\s*:?', raw_line.strip())
        if not match:
            raise ArtisanHeresy("Malformed @inject_vow signature.", line_num=i + 1)

        sig = match.group('sig')
        vow_name = sig.split('(')[0].strip()

        block_lines, next_i = self._consume_block(lines, i + 1, "@endvow")

        # Compilation logic is identical to py_func, but destination is different
        try:
            raw_python = textwrap.dedent("\n".join(block_lines))
            func_def = f"def {sig}:\n" + textwrap.indent(raw_python, "    ")

            local_namespace = {}
            exec(func_def, {}, local_namespace)
            compiled_vow = local_namespace.get(vow_name)

            # We inject this into the Vow Registry (VOW_SIGNATURES)
            # This requires a dynamic patch to the running system or a special registry.
            # For V1 Totality, we attach it to the Parser instance for the PostRunScribe to find.
            if not hasattr(self.parser, 'custom_vows'):
                self.parser.custom_vows = {}

            self.parser.custom_vows[vow_name] = compiled_vow
            self.Logger.success(f"L{i + 1}: Custom Vow '{vow_name}' injected into the Conscience.")

        except Exception as e:
            raise ArtisanHeresy(f"Vow Injection Failed: {e}", line_num=i + 1)

        return next_i