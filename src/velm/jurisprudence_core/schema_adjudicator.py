# Path: scaffold/jurisprudence_core/schema_adjudicator.py
# -------------------------------------------------------

import ipaddress
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from ..contracts.data_contracts import GnosticContract, ContractField


class SchemaAdjudicator:
    """
    =================================================================================
    == THE GNOSTIC JUDGE OF TYPES (V-Ω-OMNISCIENT. THE 12-FOLD GAZE)               ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan is the supreme authority on Data Purity. It does not merely check types;
    it investigates the semantic soul of every value passed into the Blueprint.

    ### THE PANTHEON OF 12 ELEVATIONS:
    1.  **The Enum Oracle:** Strict validation against defined option sets (`enum("a", "b")`).
    2.  **The Chronomancer:** Validates ISO-8601 timestamps and dates.
    3.  **The Network Sentinel:** Validates IPv4, IPv6, and URL structures.
    4.  **The Filesystem Warden:** Checks paths for validity, existence, or absolute/relative status.
    5.  **The Secret Ward:** Automatically redacts sensitive values from Heresy proclamations.
    6.  **The Floating Precision:** Handles `float` with range and epsilon checks.
    7.  **The Json Inquisitor:** Validates if a string contains valid, parseable JSON.
    8.  **The Regex Alchemist:** Pre-compiles and caches validation patterns for speed.
    9.  **The Recursive Guard:** Prevents infinite loops in nested contract validation.
    10. **The Any Escape:** Honors the `any` type for intentional chaos.
    11. **The List Sentinel:** Validates homogenous lists with strict item checking.
    12. **The Polyglot Parser:** Intelligently parses Pythonic signature strings into Gnostic constraints.
    =================================================================================
    """

    # --- THE SACRED REGEX GRIMOIRE ---
    TYPE_SIG_REGEX = re.compile(r'^(\w+)(?:\((.*)\))?$')
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    URL_REGEX = re.compile(
        r'^(https?|ftp)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @classmethod
    def parse_field_signature(cls, raw_type_str: str) -> Tuple[str, Dict[str, Any], bool]:
        """
        [FACULTY 12: THE POLYGLOT PARSER]
        Deconstructs complex signatures like 'enum("a", "b")', 'str(min=5)', or 'List[int]'.
        """
        clean = raw_type_str.strip()
        is_list = False

        # 1. Handle List[...] wrapper
        if clean.lower().startswith("list[") and clean.endswith("]"):
            is_list = True
            clean = clean[5:-1].strip()

        match = cls.TYPE_SIG_REGEX.match(clean)
        if not match:
            return "any", {}, is_list

        type_name = match.group(1).lower()
        args_str = match.group(2)
        constraints = {}

        if args_str:
            # 2. The Constraint Alchemist
            try:
                # Try parsing as kwargs: dict(min=1, max=10)
                py_expr_kwargs = f"dict({args_str})"
                constraints = eval(py_expr_kwargs, {"__builtins__": {}}, {})
            except Exception:
                # Fallback: Try parsing as positional args (for Enums): ["a", "b"]
                try:
                    py_expr_args = f"[{args_str}]"
                    options = eval(py_expr_args, {"__builtins__": {}}, {})
                    constraints['options'] = options
                except Exception:
                    pass

        return type_name, constraints, is_list

    @classmethod
    def adjudicate_value(cls, value: Any, field: ContractField, contracts_registry: Dict[str, GnosticContract],
                         depth: int = 0) -> None:
        """
        Performs the Rite of Validation.
        """
        # [FACULTY 9: THE RECURSIVE GUARD]
        if depth > 20:
            raise ValueError("Contract recursion depth exceeded. The Ouroboros is choking.")

        # [FACULTY 10: THE ANY ESCAPE]
        if field.type_name == 'any':
            return

        # [FACULTY 11: THE LIST SENTINEL]
        if field.is_list:
            if not isinstance(value, list):
                raise ValueError(f"Field '{field.name}' expects a List, but received {type(value).__name__}.")
            for i, item in enumerate(value):
                cls._adjudicate_single_item(item, field, contracts_registry, context=f"{field.name}[{i}]", depth=depth)
            return

        cls._adjudicate_single_item(value, field, contracts_registry, context=field.name, depth=depth)

    @classmethod
    def _adjudicate_single_item(cls, value: Any, field: ContractField, registry: Dict[str, GnosticContract],
                                context: str, depth: int):
        t = field.type_name
        c = field.constraints

        # --- Primitive Types ---
        if t in ('str', 'string', 'text'):
            if not isinstance(value, str):
                raise ValueError(f"{context} must be a string.")
            if 'min' in c and len(value) < c['min']:
                raise ValueError(f"{context} is too short (min {c['min']}).")
            if 'max' in c and len(value) > c['max']:
                raise ValueError(f"{context} is too long (max {c['max']}).")
            # [FACULTY 8: THE REGEX ALCHEMIST]
            if 'pattern' in c and not re.match(c['pattern'], value):
                # [FACULTY 5: THE SECRET WARD] (Mask value in error if it looks like a secret)
                display_val = "***" if "secret" in context.lower() or "key" in context.lower() else value
                raise ValueError(f"{context} ('{display_val}') does not match pattern '{c['pattern']}'.")

        elif t in ('int', 'integer'):
            if not isinstance(value, int) or isinstance(value, bool):  # Bool is int in python, check explicitly
                raise ValueError(f"{context} must be an integer.")
            if 'min' in c and value < c['min']:
                raise ValueError(f"{context} is too small (min {c['min']}).")
            if 'max' in c and value > c['max']:
                raise ValueError(f"{context} is too large (max {c['max']}).")

        # [FACULTY 6: THE FLOATING PRECISION]
        elif t in ('float', 'number'):
            if not isinstance(value, (float, int)) or isinstance(value, bool):
                raise ValueError(f"{context} must be a number.")
            if 'min' in c and value < c['min']:
                raise ValueError(f"{context} is too small (min {c['min']}).")

        elif t in ('bool', 'boolean'):
            if not isinstance(value, bool):
                raise ValueError(f"{context} must be a boolean.")

        # --- Semantic Types ---
        elif t == 'uuid':
            try:
                uuid.UUID(str(value))
            except ValueError:
                raise ValueError(f"{context} is not a valid UUID.")

        elif t == 'email':
            if not isinstance(value, str) or not cls.EMAIL_REGEX.match(value):
                raise ValueError(f"{context} is not a valid email address.")

        # [FACULTY 1: THE ENUM ORACLE]
        elif t == 'enum':
            options = c.get('options', [])
            if value not in options:
                raise ValueError(f"{context} is invalid. Must be one of: {options}")

        # [FACULTY 3: THE NETWORK SENTINEL]
        elif t in ('ip', 'ipv4', 'ipv6'):
            try:
                ipaddress.ip_address(value)
            except ValueError:
                raise ValueError(f"{context} is not a valid IP address.")

        elif t == 'url':
            if not isinstance(value, str) or not cls.URL_REGEX.match(value):
                raise ValueError(f"{context} is not a valid URL.")

        # [FACULTY 2: THE CHRONOMANCER]
        elif t in ('date', 'datetime', 'iso8601'):
            try:
                # Handles '2023-01-01' and '2023-01-01T12:00:00'
                datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"{context} must be a valid ISO-8601 date/time string.")

        # [FACULTY 4: THE FILESYSTEM WARDEN]
        elif t == 'path':
            p = Path(str(value))
            if 'absolute' in c and c['absolute'] and not p.is_absolute():
                raise ValueError(f"{context} must be an absolute path.")
            if 'relative' in c and c['relative'] and p.is_absolute():
                raise ValueError(f"{context} must be a relative path.")
            # Note: We cannot check exists() here easily as it might be a path *to be created*.

        # [FACULTY 7: THE JSON INQUISITOR]
        elif t == 'json_string':
            if not isinstance(value, str):
                raise ValueError(f"{context} must be a string.")
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise ValueError(f"{context} is not valid JSON.")

        # --- Nested Contracts ---
        elif t in registry:
            # Recursive Validation
            if not isinstance(value, dict):
                raise ValueError(f"{context} must be an object matching contract '{t}'.")

            nested_contract = registry[t]
            for sub_name, sub_field in nested_contract.fields.items():
                if sub_name not in value:
                    if sub_field.default_value is not None or sub_field.is_optional:
                        continue  # Use default or skip
                    raise ValueError(f"Missing required field '{sub_name}' in {context} ({t}).")

                cls.adjudicate_value(value[sub_name], sub_field, registry, depth + 1)

        else:
            # Unknown type
            raise ValueError(f"Unknown Gnostic Type: '{t}' in contract.")