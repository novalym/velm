# Path: scaffold/artisans/distill/core/oracle/tracer/probes/python_probe.py
# -------------------------------------------------------------------------

import sys
import json
import tempfile
import subprocess
import os
from pathlib import Path
from typing import Dict

from .base import BaseProbe
from ..contracts import RuntimeState, TracePoint, VariableGnosis
from ......logger import Scribe

Logger = Scribe("PythonSeance")


class PythonSeance(BaseProbe):
    """
    =============================================================================
    == THE PYTHON SEANCE (V-Ω-SYS-SETTRACE-HARNESS)                            ==
    =============================================================================
    Wraps the target Python script in a Gnostic Harness that injects `sys.settrace`.
    It captures local variables at the moment of exceptions or key breakpoints.
    """

    HARNESS_TEMPLATE = """
import sys
import json
import traceback
import os
import inspect

# --- THE GNOSTIC TRACER ---
trace_data = []
PROJECT_ROOT = r"{project_root}"

def serializer(obj):
    try:
        return str(obj)
    except:
        return "<Unrepresentable>"

def trace_handler(frame, event, arg):
    # Only trace exceptions or explicit breakpoints for now to save noise
    if event != 'exception':
        return trace_handler

    exc_type, exc_value, exc_tb = arg

    # Filter: Only capture frames within the project root
    filename = frame.f_code.co_filename
    if PROJECT_ROOT not in os.path.abspath(filename):
        return trace_handler

    # Clean path
    rel_path = os.path.relpath(filename, PROJECT_ROOT).replace(os.sep, '/')

    # Capture Locals
    local_vars = {{}}
    for k, v in frame.f_locals.items():
        if k.startswith('__'): continue
        if inspect.ismodule(v) or inspect.isfunction(v) or inspect.isclass(v): continue

        # [FACULTY 5] Deep Freeze (Simple Stringification for V1)
        val_str = serializer(v)
        if len(val_str) > 200: val_str = val_str[:197] + "..."
        local_vars[k] = val_str

    trace_data.append({{
        "path": rel_path,
        "line": frame.f_lineno,
        "func": frame.f_code.co_name,
        "vars": local_vars,
        "error": f"{{exc_type.__name__}}: {{exc_value}}"
    }})
    return trace_handler

sys.settrace(trace_handler)

# --- EXECUTE TARGET ---
try:
    # We must adjust sys.argv so the script thinks it was called directly
    sys.argv = {target_argv}

    # Read and exec the target script
    target_path = r"{target_script}"
    with open(target_path, 'r') as f:
        code = compile(f.read(), target_path, 'exec')
        exec(code, {{'__name__': '__main__', '__file__': target_path}})

except Exception:
    # We catch the exception to dump the trace, but we let the trace_handler record it first
    pass
finally:
    # --- DUMP GNOSIS ---
    with open(r"{output_file}", 'w', encoding='utf-8') as f:
        json.dump(trace_data, f, indent=2)
"""

    def conduct(self, command: str) -> RuntimeState:
        # 1. Parse Command
        # Assumes: python path/to/script.py [args]
        parts = command.split()
        if len(parts) < 2:
            return RuntimeState()

        script_path = (self.root / parts[1]).resolve()
        script_args = parts[1:]  # script + args

        if not script_path.exists():
            Logger.warn(f"Target script void: {script_path}")
            return RuntimeState()

        # 2. Forge the Harness
        # We create a temporary python file that acts as the wrapper
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py', encoding='utf-8') as harness:
            output_file = Path(harness.name).with_suffix('.json')

            # Escape paths for Windows/Unix compatibility in the generated code
            root_str = str(self.root).replace('\\', '/')
            script_str = str(script_path).replace('\\', '/')
            output_str = str(output_file).replace('\\', '/')

            harness_code = self.HARNESS_TEMPLATE.format(
                project_root=root_str,
                target_argv=json.dumps(script_args),
                target_script=script_str,
                output_file=output_str
            )
            harness.write(harness_code)
            harness_path = Path(harness.name)

        # 3. Execute the Harness
        try:
            # We run the harness with the same python interpreter running Scaffold
            subprocess.run([sys.executable, str(harness_path)], cwd=self.root, capture_output=True)

            # 4. Harvest the Gnosis
            if output_file.exists():
                reader = SnapshotReader(self.root)  # Reuse snapshot logic
                return reader.load(output_file)

        except Exception as e:
            Logger.error(f"Séance failed: {e}")

        finally:
            # Cleanup
            if harness_path.exists(): os.unlink(harness_path)
            if output_file.exists(): os.unlink(output_file)

        return RuntimeState()