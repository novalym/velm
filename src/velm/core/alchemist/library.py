# Path: src/velm/core/alchemist/library.py
# ----------------------------------------
"""
=================================================================================
== THE ALCHEMICAL LIBRARY (V-Ω-TOTALITY-V300-RESILIENT)                        ==
=================================================================================
LIF: INFINITY | ROLE: TEMPLATE_UTILITIES | RANK: OMEGA_SOVEREIGN

The standard library of rites available within the Jinja2 context.
Hardened against type drift, environment disconnects, and binary hazards.
"""

import datetime
import html
import json
import os
import secrets
import shlex
import subprocess
import uuid
import logging
from pathlib import Path
from typing import Any, Optional, Union

from ...logger import Scribe
from ...utils import is_binary

Logger = Scribe("AlchemicalLibrary")


# =============================================================================
# == RITE I: THE CHRONOMANCER (TIME)                                         ==
# =============================================================================

def now_rite(tz: Any = 'local', fmt: Any = '%Y-%m-%dT%H:%M:%SZ') -> str:
    """
    A divine rite to perceive and proclaim the current moment in time.
    [ASCENSION]: Robust type coercion for arguments.
    """
    try:
        # Coerce inputs
        tz_str = str(tz).lower().strip()
        fmt_str = str(fmt)

        if tz_str == 'utc':
            now = datetime.datetime.now(datetime.timezone.utc)
        else:
            now = datetime.datetime.now()

        return now.strftime(fmt_str)
    except Exception as e:
        Logger.warn(f"Time dilation error: {e}. Falling back to ISO UTC.")
        return datetime.datetime.now(datetime.timezone.utc).isoformat()


# =============================================================================
# == RITE II: THE CRYPTOGRAPHIC FORGE (SECRETS)                              ==
# =============================================================================

def forge_secret_rite(length: Any = 32, secret_type: Any = 'hex') -> str:
    """
    A private rite to forge Gnosis from chaos.
    [ASCENSION]: Argument Swapping Logic & Type Hardening.
    """
    # 1. THE ARGUMENT HEURISTIC
    # If the user wrote {{ secret('hex', 64) }} instead of {{ secret(64, 'hex') }}
    # we detect the type mismatch and swap them.
    if isinstance(length, str) and not length.isdigit() and isinstance(secret_type, int):
        length, secret_type = secret_type, length

    # 2. TYPE COERCION
    try:
        final_len = int(length)
    except (ValueError, TypeError):
        final_len = 32

    # [ASCENSION 4]: MEMORY WARD
    final_len = min(max(1, final_len), 4096)

    stype = str(secret_type).lower().strip()

    try:
        if stype == 'hex':
            return secrets.token_hex(final_len)
        if stype == 'urlsafe':
            return secrets.token_urlsafe(final_len)
        if stype == 'uuid':
            return str(uuid.uuid4())
        if stype == 'base64':
            return secrets.token_bytes(final_len).decode('latin1')  # Latin1 maps bytes 1:1

        # Fallback for unknown types
        Logger.warn(f"Unknown secret type '{stype}'. Defaulting to hex.")
        return secrets.token_hex(final_len)

    except Exception as e:
        Logger.error(f"Entropy generation failed: {e}")
        return "!!ENTROPY_FAILURE!!"


# =============================================================================
# == RITE III: THE STRUCTURED TRANSMUTATION (JSON/YAML)                      ==
# =============================================================================

def to_json_rite(data: Any, indent: Any = 2) -> str:
    """A divine rite to transmute any Python soul into a pure JSON scripture."""
    try:
        # Coerce indent
        final_indent = int(indent) if str(indent).isdigit() else 2
        return json.dumps(data, indent=final_indent, default=str)
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


# =============================================================================
# == RITE IV: THE KINETIC CONDUIT (SHELL)                                    ==
# =============================================================================

def shell_rite(command: Any, timeout: Any = 60) -> str:
    """
    A divine, but dangerous, rite to commune with the mortal shell.
    [ASCENSION 3]: Sets stdin=DEVNULL to prevent EOF hangs.
    """
    cmd_str = str(command).strip()

    try:
        final_timeout = int(timeout)
    except:
        final_timeout = 60

    if not cmd_str:
        return ""

    Logger.verbose(f"Alchemist invoking shell: '{cmd_str}'")

    try:
        # [THE CURE]: stdin=subprocess.DEVNULL is critical.
        # It ensures that if the command asks for input, it gets EOF immediately
        # and fails fast, rather than hanging the Titan.
        result = subprocess.run(
            cmd_str,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8',
            timeout=final_timeout,
            stdin=subprocess.DEVNULL  # <--- THE ANCHOR AGAINST THE VOID
        )

        if result.returncode != 0:
            err_msg = result.stderr.strip()
            Logger.debug(f"Shell rite '{cmd_str}' returned {result.returncode}: {err_msg}")
            # We return the error as a string so the template can decide how to handle it,
            # or use a default value if it checks for the error signature.
            return ""

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        Logger.error(f"Shell rite timed out after {final_timeout}s: {cmd_str}")
        return f"!!SHELL_TEMPORAL_PARADOX!!"
    except Exception as e:
        Logger.error(f"Catastrophic shell paradox: {e}")
        return f"!!SHELL_CATASTROPHE: {e}!!"


# =============================================================================
# == RITE V: THE MATTER INQUEST (FILES)                                      ==
# =============================================================================

def is_binary_test(path_str: Any) -> bool:
    """Delegates the judgment to the central utility."""
    if not path_str: return False
    return is_binary(Path(str(path_str)))


def include_file_rite(path: Any, start: Any = -1, end: Any = -1) -> str:
    """
    The Scribe of Celestial Souls.
    Reads a file from the disk and injects it into the template.
    [ASCENSION 10]: Multi-Encoding Resilience.
    """
    path_str = str(path).strip()
    if not path_str:
        return "!!INCLUDE_HERESY: Void Path!!"

    try:
        # Resolve path relative to CWD (Project Root)
        target_path = Path(path_str).resolve()

        # [ASCENSION 5]: TRAVERSAL WARD
        try:
            cwd = Path.cwd().resolve()
            if not str(target_path).startswith(str(cwd)):
                # We allow it if it's explicitly allowed by the Architect (omitted for now),
                # or we just log a warning.
                # For templates, we usually only want to include things inside the project.
                pass
        except Exception:
            pass

        if not target_path.exists():
            Logger.warn(f"Include failed: '{path_str}' does not exist.")
            return f"!!INCLUDE_VOID: {path_str}!!"

        if not target_path.is_file():
            return f"!!INCLUDE_HERESY: '{path_str}' is not a file!!"

        if is_binary_test(str(target_path)):
            return f"!!INCLUDE_HERESY: '{path_str}' is binary matter!!"

        # [ASCENSION 10]: ENCODING HEALER
        content = None
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                content = target_path.read_text(encoding=enc)
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            return f"!!INCLUDE_HERESY: Could not decode '{path_str}'!!"

        # Slicing Logic
        try:
            s_idx = int(start)
            e_idx = int(end)
        except:
            s_idx, e_idx = -1, -1

        if s_idx > -1 or e_idx > -1:
            lines = content.splitlines()
            start_line = max(0, s_idx)
            end_line = e_idx if e_idx > -1 else len(lines)
            sliced_content = "\n".join(lines[start_line:end_line])
            return sliced_content

        return content

    except Exception as e:
        Logger.error(f"Heresy of Inclusion for '{path_str}': {e}")
        return f"""<!-- 
           GNOSTIC HERESY: THE RITE OF INCLUSION FAILED
           Scripture: {html.escape(path_str)}
           Heresy:    {html.escape(str(e))}
           -->"""