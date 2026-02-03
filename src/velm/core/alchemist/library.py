# Path: scaffold/core/alchemist/library.py
# ----------------------------------------

import datetime
import html
import json
import os
import secrets
import shlex
import subprocess
import uuid
from pathlib import Path
from typing import Any, Optional

from ...logger import Scribe
from ...utils import is_binary

Logger = Scribe("AlchemicalLibrary")

def now_rite(tz: str = 'local', fmt: str = '%Y-%m-%dT%H:%M:%SZ') -> str:
    """A divine rite to perceive and proclaim the current moment in time."""
    now = datetime.datetime.now(datetime.timezone.utc if tz.lower() == 'utc' else None)
    return now.strftime(fmt)


def forge_secret_rite(length: int = 32, secret_type: str = 'hex') -> str:
    """A private rite to forge Gnosis from chaos."""
    stype = secret_type.lower()
    if stype == 'hex':
        return secrets.token_hex(length)
    if stype == 'urlsafe':
        return secrets.token_urlsafe(length)
    if stype == 'uuid':
        return str(uuid.uuid4())
    if stype == 'base64':
        return secrets.token_bytes(length).decode('latin1')
    return f"!!UNKNOWN_SECRET_TYPE:{secret_type}!!"


def to_json_rite(data: Any, indent: Optional[int] = 2) -> str:
    """A divine rite to transmute any Python soul into a pure JSON scripture."""
    try:
        return json.dumps(data, indent=indent)
    except Exception as e:
        return f"!!JSON_TRANSMUTATION_HERESY: {e}!!"


def to_yaml_rite(data: Any) -> str:
    """A divine rite to transmute any Python soul into a pure YAML scripture."""
    try:
        import yaml
        return yaml.dump(data, default_flow_style=False)
    except ImportError:
        return "!!YAML_HERESY: The 'PyYAML' artisan is required. `pip install PyYAML`!!"
    except Exception as e:
        return f"!!YAML_TRANSMUTATION_HERESY: {e}!!"


def shell_rite(command: str, timeout: int = 60) -> str:
    """A divine, but dangerous, rite to commune with the mortal shell."""
    Logger.warn(f"A `shell()` rite was invoked for command: '{command}'.")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False, encoding='utf-8',
                                timeout=timeout)
        if result.returncode != 0:
            Logger.error(f"Shell rite failed (Code {result.returncode}): {result.stderr.strip()}")
            return f"!!SHELL_HERESY(code={result.returncode}): {result.stderr.strip()}!!"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"!!SHELL_TEMPORAL_PARADOX: The rite exceeded its {timeout}s timeout!!"
    except Exception as e:
        Logger.error(f"A catastrophic paradox occurred during a shell rite: {e}")
        return f"!!SHELL_CATASTROPHE: {e}!!"


def is_binary_test(path_str: str) -> bool:
    """Delegates the judgment to the central utility."""
    if not path_str: return False
    return is_binary(Path(path_str))


def include_file_rite(path: str, start: int = -1, end: int = -1) -> str:
    """The Scribe of Celestial Souls."""
    if not path:
        return "!!INCLUDE_HERESY: The path proclaimed was a void.!!"

    try:
        target_path = Path(path)
        if not target_path.is_file():
            raise FileNotFoundError(f"The scripture at '{path}' is a void or a directory.")

        if is_binary_test(str(target_path)):
            raise ValueError("The scripture's soul is profane (binary) and cannot be included.")

        try:
            content = target_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            Logger.warn(f"Gaze of Forgiveness: Reading '{path}' as latin-1.")
            content = target_path.read_text(encoding='latin-1')

        if start > -1 or end > -1:
            lines = content.splitlines()
            start_line = max(0, start)
            end_line = end if end > -1 else len(lines)
            sliced_content = "\n".join(lines[start_line:end_line])
            Logger.verbose(f"Gnostic Scalpel has extracted lines {start_line}-{end_line} from '{path}'.")
            return sliced_content

        return content

    except Exception as e:
        Logger.error(f"Heresy of Inclusion for file '{path}'. Reason: {e}")
        return f"""<!-- 
           GNOSTIC HERESY: THE RITE OF INCLUSION FAILED
           Scripture: {html.escape(str(path))}
           Heresy:    {html.escape(str(e))}
           -->"""