# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/transmuter.py
# --------------------------------------------------------------------------------------

import re
import os
import uuid
import time
import math
import base64
import hashlib
import yaml
import subprocess
from pathlib import Path
from typing import Any, Optional
from ......logger import Scribe
from ......contracts.heresy_contracts import ArtisanHeresy
from .regex_phalanx import VariableRegexPhalanx

Logger = Scribe("VariableScribe:Transmuter")


class GnosticTransmuter:
    """
    =============================================================================
    == THE GNOSTIC TRANSMUTER (V-Ω-POLYGLOT-ALCHEMY)                           ==
    =============================================================================
    LIF: 10,000x | ROLE: VALUE_MATERIALIZER

    Resolves Shell, Env, Math, Directives, and Auto-Types primitive YAML structures.
    """

    @classmethod
    def transmute(cls, value_str: str, base_dir: Path) -> Any:
        if not value_str: return ""

        # --- MOVEMENT I: THE CRYPTOGRAPHIC RITES ---
        if value_str.startswith('@secret('):
            return cls._handle_secret(value_str)

        if value_str.startswith('@b64(') and value_str.endswith(')'):
            return cls._handle_base64(value_str)

        if value_str.startswith('@hash(') and value_str.endswith(')'):
            return cls._handle_hash(value_str)

        # --- MOVEMENT II: THE SPATIAL RITES ---
        if value_str.startswith('@file('):
            return cls._handle_file(value_str, base_dir)

        # --- MOVEMENT III: THE TEMPORAL RITES ---
        if value_str == '@uuid': return str(uuid.uuid4())
        if value_str == '@now': return time.strftime("%Y-%m-%d %H:%M:%S")

        # --- MOVEMENT IV: THE SUBSTRATE RITES ---
        if value_str.startswith('$(') and value_str.endswith(')'):
            return cls._handle_shell(value_str[2:-1])

        if "${" in value_str:
            value_str = cls._handle_env_expansion(value_str)

        # --- MOVEMENT V: THE MATHEMATICAL RITES ---
        if VariableRegexPhalanx.MATH_CALC.match(value_str) and any(op in value_str for op in "+-*/%") and not re.search(
                r'[a-zA-Z]', value_str):
            try:
                return eval(value_str, {"__builtins__": None}, {"math": math, "abs": abs})
            except:
                pass

        # --- MOVEMENT VI: PRIMITIVE ALCHEMY ---
        return cls.transmute_primitive(value_str)

    @staticmethod
    def transmute_primitive(value_str: str, is_path_var: bool = False) -> Any:
        """
        [THE MASTER CURE]: Differentiates between Logical Void (None) and
        Physical Empty (""). Wards against NoneType Topography Collapse.
        """
        if isinstance(value_str, str) and ("{{" in value_str or "{%" in value_str):
            return value_str

        v_lower = str(value_str).lower().strip()

        # 1. THE TRINITY OF BOOLEAN TRUTH
        if v_lower in ('true', 'yes', 'on', 'resonant'): return True
        if v_lower in ('false', 'no', 'off', 'fractured'): return False

        # 2. THE NONETYPE SARCOPHAGUS
        if v_lower in ('null', 'none', 'void', ''):
            if is_path_var: return ""  # Path variables MUST remain strings
            return None

        # 3. COLLECTION INCEPTION
        try:
            thawed = yaml.safe_load(value_str)
            if isinstance(thawed, (dict, list)):
                return GnosticTransmuter._recursive_purify(thawed)
            return thawed
        except Exception:
            return value_str

    @staticmethod
    def _recursive_purify(data: Any) -> Any:
        if isinstance(data, dict): return {k: GnosticTransmuter._recursive_purify(v) for k, v in data.items()}
        if isinstance(data, list): return [GnosticTransmuter._recursive_purify(v) for v in data]
        return data

    @staticmethod
    def _handle_secret(value_str: str) -> str:
        match = re.match(r'@secret\((.*?)\)', value_str)
        if match:
            args_str = match.group(1).strip()
            args = [arg.strip().strip("'\"") for arg in args_str.split(',')] if args_str else []
            from ......utils import forge_gnostic_secret
            return forge_gnostic_secret(int(args[1]) if len(args) > 1 and args[1].isdigit() else 32,
                                        args[0] if args else 'hex')
        raise ArtisanHeresy(message=f"Malformed @secret directive: '{value_str}'")

    @staticmethod
    def _handle_base64(value_str: str) -> str:
        match = re.match(r'@b64\((.*?)\)', value_str)
        if match:
            inner = match.group(1).strip().strip("'\"")
            try:
                return base64.b64decode(inner).decode('utf-8')
            except Exception as e:
                raise ArtisanHeresy(message=f"Base64 Decoding Fracture: {e}")

    @staticmethod
    def _handle_hash(value_str: str) -> str:
        match = re.match(r'@hash\((.*?)\)', value_str)
        if match:
            args_str = match.group(1).strip()
            args = [arg.strip().strip("'\"") for arg in args_str.split(',')]
            algo = args[0] if len(args) > 0 else 'sha256'
            data = args[1] if len(args) > 1 else ''
            try:
                return hashlib.new(algo, data.encode('utf-8')).hexdigest()
            except ValueError:
                raise ArtisanHeresy(message=f"Unsupported hash algorithm: '{algo}'")

    @staticmethod
    def _handle_file(value_str: str, base_dir: Path) -> str:
        match = re.match(r'@file\((.*?)\)', value_str)
        if match:
            path_str = match.group(1).strip().strip('"\'')
            file_to_read = (base_dir / Path(path_str)).resolve()
            if not file_to_read.is_file(): raise ArtisanHeresy(message=f"Celestial soul not found at: '{file_to_read}'")
            try:
                return file_to_read.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                return file_to_read.read_text(encoding='latin-1', errors='replace')

    @staticmethod
    def _handle_shell(cmd: str) -> str:
        if "rm " in cmd or "mkfs" in cmd:
            Logger.warn(f"Shell Gaze Averted: Dangerous command '{cmd}'. Returning void.")
            return ""
        try:
            res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True)
            return res.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def _handle_env_expansion(value: str) -> str:
        def replace(match):
            key, default = match.group(1), match.group(2)
            val = os.getenv(key)
            if val is not None: return val
            if default is not None: return default
            return ""

        return VariableRegexPhalanx.ENV_VAR.sub(replace, value)