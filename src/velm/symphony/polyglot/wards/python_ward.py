# Path: scaffold/symphony/polyglot/wards/python_ward.py

def get_harness(sanctum_abs_path: str) -> str:
    """Returns the Gnostic Ward Harness for the Python runtime."""
    return f'''
# --- BEGIN SCAFFOLD GNOSTIC WARD (PYTHON) ---
import os, pathlib, builtins, shutil
__sc_sanctum_path__ = pathlib.Path(r"{sanctum_abs_path}")
print(f"--- Gnostic Filesystem Ward Engaged (Sanctum: {{__sc_sanctum_path__}}) ---", flush=True)

__sc_profane_open__ = builtins.open
__sc_profane_Path__ = pathlib.Path

def __sc_path_adjudicator__(path_obj_or_str, rite_name="Unknown"):
    try:
        # We must resolve relative to the current CWD of the script
        abs_path = __sc_profane_Path__(os.path.abspath(str(path_obj_or_str))).resolve()
        if not str(abs_path).startswith(str(__sc_sanctum_path__)):
            raise PermissionError(f"[Gnostic Ward Heresy] The '{{rite_name}}' rite's attempt to access '{{abs_path}}' outside the sacred sanctum was struck down.")
    except Exception as e:
        raise PermissionError(f"[Gnostic Ward Heresy] A paradox occurred while adjudicating the path for '{{rite_name}}': {{e}}")

def __sc_gnostic_open__(file, *args, **kwargs):
    __sc_path_adjudicator__(file, "open")
    return __sc_profane_open__(file, *args, **kwargs)

class GnosticPath(__sc_profane_Path__):
    def __new__(cls, *args, **kwargs):
        if args:
            __sc_path_adjudicator__(args[0], "Path()")
        return super().__new__(cls, *args, **kwargs)

builtins.open = __sc_gnostic_open__
pathlib.Path = GnosticPath
# --- END SCAFFOLD GNOSTIC WARD ---
'''

