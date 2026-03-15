# Path: codex/core/std_logic.py
# -----------------------------


"""
=================================================================================
== THE OMEGA LOGIC WEAVER: TOTALITY (V-Ω-TOTALITY-VMAX-PART-1-OF-2)            ==
=================================================================================
LIF: ∞^∞ | ROLE: DYNAMIC_COMPOSITION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_LOGIC_VMAX_PART1_MEMORY_SUTURE_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for state mutation. This scripture governs the
physics of composition. It righteously implements the Isolated Memory Suture,
annihilating the "Secondary Semantic Leak" and "14-VS-0" paradoxes by guaranteeing
that matter forged in recursive sub-weaves is mathematically isolated during
creation and perfectly stitched upon return.

### THE PANTHEON OF 48 LEGENDARY ASCENSIONS:
1.  **The Weaver's Meta Suture (THE MASTER CURE):** Explicitly injects
    `metadata={"_is_nested_weave": True}` into the `WeaveRequest`. This mathematically
    annihilates the Impatient Weaver Paradox, guaranteeing that sub-shards never
    trigger physical I/O or shell execution until the Prime Timeline collapses.
2.  **Achronal Buffer Suture:** Safe memory reference handling.
3.  **Lazarus Engine Link:** Resurrects the Engine reference via global heap scavenging.[... Continuum maintained through 48 layers of Gnostic Oracle Mastery ...]
=================================================================================
"""

import ast
import binascii
import json
import base64
import hashlib
import time
import uuid
import re
import os
import sys
import gc
import inspect
import urllib.parse
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Set, Tuple, Callable, Final
from collections import defaultdict

from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import toml as tomllib
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

Logger = Scribe("LogicWeaver")


@domain("logic")
class LogicDomain(BaseDirectiveDomain):
    MAX_RECURSION_DEPTH: Final[int] = 100

    def __init__(self):
        super().__init__()
        self.Logger = Logger
        self._lock = threading.RLock()
        self._phantom_cache: Dict[str, Any] = {}

    @property
    def namespace(self) -> str:
        return "logic"

    def help(self) -> str:
        return "The God-Engine of data mutation, recursive weaving, and alchemical merging."

    def _directive_weave(
            self,
            context: Dict[str, Any],
            shard_name: str,
            variables: Optional[Dict[str, Any]] = None,
            target: Optional[str] = None
    ) -> str:
        """
        =================================================================================
        == THE OMEGA WEAVE: TOTALITY (V-Ω-TOTALITY-VMAX-LAMINAR-SUTURE-FINALIS)        ==
        =================================================================================
        """
        import time
        import uuid
        import base64
        import json
        from pathlib import Path
        from ...contracts.heresy_contracts import CodexExecutionHeresy

        _start_ns = time.perf_counter_ns()
        trace_id = context.get("__trace_id__") or context.get("trace_id") or f"tr-weave-{uuid.uuid4().hex[:6].upper()}"

        current_file_anchor = context.get("__current_file__")

        if current_file_anchor is None:
            payload = {"shard": shard_name, "vars": variables, "target": target, "trace": trace_id}
            b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
            phantom_id = uuid.uuid4().hex[:8].upper()
            return f"__phantom_weave_{phantom_id}__ :: \"{{{{ logic._execute_phantom('{b64_payload}') }}}}\""

        engine = self._scry_engine(context)
        if not engine:
            return f"/*[GNOSTIC_WEAVE_FRACTURED]: Engine_Void */"

        try:
            from ...interfaces.requests import WeaveRequest

            target_dir = target or context.get("__current_dir__") or "."
            target_dir_normalized = str(target_dir).replace('\\', '/').rstrip('/') or "."

            merged_gnosis = {
                k: v for k, v in context.items()
                if (not str(k).startswith("__") or k in ("__woven_matter__", "__woven_commands__"))
                   and k != "variables"
            }

            if variables:
                merged_gnosis.update(self._coerce_variables(variables))

            depth = context.get("__weave_depth__", 0)
            if depth > self.MAX_RECURSION_DEPTH: return f"/*[WEAVE_HALTED_MAX_DEPTH] */"
            merged_gnosis["__weave_depth__"] = depth + 1

            # =========================================================================
            # == [THE IMPATIENT WEAVER CURE]: EXPLICIT NESTED METADATA               ==
            # =========================================================================
            # We MUST explicitly pass `_is_nested_weave` inside the `metadata` dictionary
            # so the GnosticWeaver knows to stay the hand of physical I/O and Shell Exec.
            # This mathematically annihilates the `npm install` premature execution heresy.
            # =========================================================================
            request_metadata = {"_is_nested_weave": True}

            request = WeaveRequest(
                fragment_name=shard_name,
                target_directory=target_dir_normalized,
                variables=merged_gnosis,
                metadata=request_metadata, # <--- THE ABSOLUTE CURE
                trace_id=trace_id,
                silent=True,
                force=True,
                non_interactive=True,
                dry_run=context.get('dry_run', False),
                project_root=context.get("__project_root__")
            )

            result = engine.dispatch(request)

            if not result.success:
                raise CodexExecutionHeresy(f"Shard '{shard_name}' failed: {result.message}")

            atom_count = 0
            if result.data:
                sub_items = result.data.get("scaffold_items",[])
                sub_cmds = result.data.get("post_run_commands",[])
                atom_count = len(sub_items)

                # =====================================================================
                # == [THE MASTER CURE]: BICAMERAL COMMAND HOISTING                   ==
                # =====================================================================
                parent_matter = context.get("__woven_matter__")
                if parent_matter is not None:
                    existing_ids = {id(i) for i in parent_matter}
                    parent_matter.extend([i for i in sub_items if id(i) not in existing_ids])

                parent_commands = context.get("__woven_commands__")
                if parent_commands is not None:
                    existing_cmd_ids = {id(c) for c in parent_commands}
                    parent_commands.extend([c for c in sub_cmds if id(c) not in existing_cmd_ids])

            return f"#[GNOSTIC_WEAVE_RESONANT]: {shard_name}[{atom_count} atoms]"

        except Exception as catastrophic_paradox:
            return f"/* [WEAVE_FRACTURE]: {str(catastrophic_paradox)} */"

    def _directive__execute_phantom(self, context: Dict[str, Any], b64_payload: str) -> str:
        try:
            raw_json = base64.b64decode(b64_payload).decode('utf-8')
            payload = json.loads(raw_json)

            return self._directive_weave(
                context,
                shard_name=payload.get("shard"),
                variables=payload.get("vars"),
                target=payload.get("target")
            )
        except Exception as e:
            Logger.error(f"Phantom Annihilation Failed: {e}")
            return "#[PHANTOM_FRACTURE]"

    def _scry_engine(self, context: Dict[str, Any]) -> Any:
        if context.get("__engine__"): return context["__engine__"]
        alchemist = context.get("__alchemist__")
        if alchemist and getattr(alchemist, 'engine', None):
            return alchemist.engine
        if alchemist and hasattr(alchemist, 'env') and "__engine__" in alchemist.env.globals:
            return alchemist.env.globals["__engine__"]
        try:
            for obj in gc.get_objects():
                if hasattr(obj, '__class__') and obj.__class__.__name__ == 'VelmEngine':
                    context["__engine__"] = obj
                    return obj
        except Exception:
            pass
        return None

    def _directive_json_parse(self, context: Dict[str, Any], data: str) -> Any:
        if not data: return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}

    def _directive_json_dump(self, context: Dict[str, Any], data: Any, indent: int = 2) -> str:
        return json.dumps(data, indent=indent, default=str)

    def _directive_yaml_parse(self, context: Dict[str, Any], data: str) -> Any:
        if not data: return {}
        if not YAML_AVAILABLE: return self._directive_json_parse(context, data)
        try:
            return yaml.safe_load(data)
        except Exception:
            return {}

    def _directive_toml_parse(self, context: Dict[str, Any], data: str) -> Any:
        if not data or not TOML_AVAILABLE: return {}
        try:
            return tomllib.loads(data)
        except Exception:
            return {}

    def _directive_merge(self, context: Dict[str, Any], base: Union[Dict, List], overlay: Union[Dict, List]) -> Any:
        import copy
        def deep_merge(d1, d2):
            if isinstance(d1, dict) and isinstance(d2, dict):
                merged = copy.deepcopy(d1)
                for k, v in d2.items():
                    if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                        merged[k] = deep_merge(merged[k], v)
                    elif k in merged and isinstance(merged[k], list) and isinstance(v, list):
                        merged[k] = deep_merge(merged[k], v)
                    else:
                        merged[k] = copy.deepcopy(v)
                return merged
            elif isinstance(d1, list) and isinstance(d2, list):
                merged = copy.deepcopy(d1)
                for item in d2:
                    if isinstance(item, (dict, list)):
                        merged.append(copy.deepcopy(item))
                    elif item not in merged:
                        merged.append(item)
                return merged
            else:
                return copy.deepcopy(d2)

        return deep_merge(base, overlay)

    def _directive_extract_path(self, context: Dict[str, Any], data: Union[Dict, List], path: str,
                                default: Any = None) -> Any:
        keys = str(path).split('.')
        current = data
        try:
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                elif hasattr(current, k):
                    current = getattr(current, k)
                elif isinstance(current, list) and k.isdigit():
                    idx = int(k)
                    current = current[idx] if idx < len(current) else None
                else:
                    return default
            return current if current is not None else default
        except Exception:
            return default

    def _directive_pluck(self, context: Dict[str, Any], data_list: List[Dict[str, Any]], key: str) -> List[Any]:
        if not isinstance(data_list, list): return []
        return[
            item.get(key) if isinstance(item, dict) else getattr(item, key, None)
            for item in data_list
        ]

    def _directive_group_by(self, context: Dict[str, Any], data_list: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict]]:
        if not isinstance(data_list, list): return {}
        grouped = defaultdict(list)
        for item in data_list:
            val = item.get(key) if isinstance(item, dict) else getattr(item, key, "unknown")
            grouped[str(val)].append(item)
        return dict(grouped)

    def _directive_coalesce(self, context: Dict[str, Any], *args) -> Any:
        return next((a for a in args if a is not None and str(a).lower() not in ('none', 'null', 'void', '')), None)

    def _directive_ternary(self, context: Dict[str, Any], condition: Any, true_val: Any, false_val: Any) -> Any:
        is_true = False
        if isinstance(condition, bool):
            is_true = condition
        elif isinstance(condition, str):
            is_true = condition.lower() in ("true", "yes", "1", "on", "resonant")
        elif isinstance(condition, (int, float)):
            is_true = bool(condition)
        else:
            is_true = bool(condition)
        return true_val if is_true else false_val

    def _directive_type_cast(self, context: Dict[str, Any], value: Any, target_type: str) -> Any:
        t = str(target_type).lower().strip()
        try:
            if t in ('int', 'integer'): return int(value)
            if t in ('float', 'double'): return float(value)
            if t in ('bool', 'boolean'): return str(value).lower() in ('true', 'yes', '1', 'on')
            if t in ('str', 'string'): return str(value)
            if t in ('list', 'array', 'dict', 'object'): return json.loads(value) if isinstance(value, str) else value
        except Exception:
            pass
        return value

    def _directive_b64_encode(self, context: Dict[str, Any], data: Union[str, bytes], url_safe: bool = False) -> str:
        s = data.encode('utf-8') if isinstance(data, str) else data
        if url_safe:
            return base64.urlsafe_b64encode(s).decode('utf-8').rstrip('=')
        return base64.b64encode(s).decode('utf-8')

    def _directive_b64_decode(self, context: Dict[str, Any], data: str, url_safe: bool = False) -> str:
        try:
            padded = str(data)
            padding_needed = len(padded) % 4
            if padding_needed: padded += '=' * (4 - padding_needed)
            if url_safe:
                return base64.urlsafe_b64decode(padded.encode('utf-8')).decode('utf-8')
            return base64.b64decode(padded.encode('utf-8')).decode('utf-8')
        except binascii.Error:
            return "[DECODE_FRACTURE]"

    def _directive_hash(self, context: Dict[str, Any], data: Any, algo: str = "sha256") -> str:
        if isinstance(data, (dict, list)):
            m = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
        else:
            m = str(data).encode('utf-8')
        try:
            return hashlib.new(algo, m).hexdigest()
        except ValueError:
            return hashlib.sha256(m).hexdigest()

    def _directive_uuid(self, context: Dict[str, Any], namespace: Optional[str] = None, name: Optional[str] = None) -> str:
        if namespace and name:
            ns_uuid = uuid.UUID(namespace) if '-' in namespace else uuid.NAMESPACE_DNS
            return str(uuid.uuid5(ns_uuid, name))
        return str(uuid.uuid4())

    def _directive_type_of(self, context: Dict[str, Any], value: Any) -> str:
        return type(value).__name__

    def _directive_regex_extract(self, context: Dict[str, Any], text: str, pattern: str, group: int = 1, match_all: bool = False) -> Any:
        try:
            if match_all:
                return re.findall(pattern, str(text))
            match = re.search(pattern, str(text))
            if match: return match.group(group) if group < len(match.groups()) + 1 else match.group(0)
            return ""
        except Exception:
            return ""

    def _directive_regex_replace(self, context: Dict[str, Any], text: str, pattern: str, replacement: str) -> str:
        try:
            return re.sub(pattern, replacement, str(text))
        except Exception:
            return str(text)

    def _directive_strip(self, context: Dict[str, Any], text: str, chars: Optional[str] = None) -> str:
        return str(text).strip(chars)

    def _directive_lstrip(self, context: Dict[str, Any], text: str, chars: Optional[str] = None) -> str:
        return str(text).lstrip(chars)

    def _directive_rstrip(self, context: Dict[str, Any], text: str, chars: Optional[str] = None) -> str:
        return str(text).rstrip(chars)

    def _directive_url_encode(self, context: Dict[str, Any], text: str) -> str:
        return urllib.parse.quote(str(text))

    def _directive_upper(self, context: Dict[str, Any], text: str) -> str:
        return str(text).upper()

    def _directive_lower(self, context: Dict[str, Any], text: str) -> str:
        return str(text).lower()

    def _directive_title(self, context: Dict[str, Any], text: str) -> str:
        return str(text).title()

    def _directive_slice(self, context: Dict[str, Any], text: str, start: Optional[int] = None, end: Optional[int] = None) -> str:
        try:
            s = int(start) if start is not None else None
            e = int(end) if end is not None else None
            return str(text)[s:e]
        except Exception:
            return str(text)

    def _directive_chunk(self, context: Dict[str, Any], iterable: List[Any], chunk_size: int) -> List[List[Any]]:
        if not isinstance(iterable, list): return[iterable]
        size = int(chunk_size)
        if size <= 0: return[iterable]
        return [iterable[i:i + size] for i in range(0, len(iterable), size)]

    def _directive_unique(self, context: Dict[str, Any], iterable: List[Any]) -> List[Any]:
        if not isinstance(iterable, list): return iterable
        return list(dict.fromkeys(iterable))

    def _directive_flatten(self, context: Dict[str, Any], iterable: List[Any]) -> List[Any]:
        if not isinstance(iterable, list): return [iterable]
        flat_list =[]
        for i in iterable:
            if isinstance(i, list):
                flat_list.extend(self._directive_flatten(context, i))
            else:
                flat_list.append(i)
        return flat_list

    def _directive_map(self, context: Dict[str, Any], iterable: List[Any], attr: str) -> List[Any]:
        if not isinstance(iterable, list): return []
        return[item.get(attr) if isinstance(item, dict) else getattr(item, attr, None) for item in iterable]

    def _directive_filter_list(self, context: Dict[str, Any], iterable: List[Any], attr: str, value: Any) -> List[Any]:
        if not isinstance(iterable, list): return []
        return[item for item in iterable if
                (item.get(attr) if isinstance(item, dict) else getattr(item, attr, None)) == value]

    def _directive_dedup_by(self, context: Dict[str, Any], iterable: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        if not isinstance(iterable, list): return iterable
        seen = set()
        result =[]
        for item in iterable:
            if isinstance(item, dict) and key in item:
                val = item[key]
                if val not in seen:
                    seen.add(val)
                    result.append(item)
            else:
                result.append(item)
        return result

    def _directive_timestamp(self, context: Dict[str, Any], fmt: str = "epoch") -> Union[int, str]:
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        if fmt == "epoch": return int(now.timestamp())
        if fmt == "iso": return now.isoformat()
        try:
            return now.strftime(fmt)
        except Exception:
            return str(int(now.timestamp()))

    def _directive_env(self, context: Dict[str, Any], key: str, default: Any = "") -> Any:
        return os.environ.get(key, default)

    def _directive_path_join(self, context: Dict[str, Any], *args) -> str:
        return os.path.join(*[str(a) for a in args]).replace('\\', '/')

    def _directive_shell(self, context: Dict[str, Any], command: str, timeout: int = 10) -> str:
        if os.environ.get("SCAFFOLD_ENV") == "WASM": return ""
        if os.environ.get("SCAFFOLD_NO_SHELL") == "1": return ""
        try:
            res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            return res.stdout.strip()
        except Exception as e:
            Logger.debug(f"Shell execution failed: {e}")
            return ""

    def _directive_read_file(self, context: Dict[str, Any], path: str) -> str:
        try:
            target = Path(path)
            if not target.is_absolute():
                base = context.get("__current_dir__", ".")
                target = Path(base) / target
            if target.exists() and target.is_file():
                return target.read_text(encoding='utf-8', errors='ignore')
            return ""
        except Exception:
            return ""

    def _directive_math(self, context: Dict[str, Any], expression: str) -> Any:
        if not re.match(r"^[\d\s+\-*/\(\).]+$", str(expression)):
            return 0
        try:
            return ast.literal_eval(str(expression))
        except Exception:
            try:
                return eval(str(expression), {"__builtins__": None}, {})
            except Exception:
                return 0

    def _coerce_variables(self, vars_dict: Dict[str, Any]) -> Dict[str, Any]:
        new_vars = {}
        for k, v in vars_dict.items():
            if isinstance(v, str):
                v_low = v.lower().strip()
                if v_low in ("true", "yes", "on", "resonant"):
                    new_vars[k] = True
                elif v_low in ("false", "no", "off", "fractured"):
                    new_vars[k] = False
                elif v.isdigit():
                    new_vars[k] = int(v)
                elif v.replace('.', '', 1).isdigit() and v.count('.') < 2:
                    new_vars[k] = float(v)
                else:
                    new_vars[k] = v
            else:
                new_vars[k] = v
        return new_vars

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_WEAVER status=RESONANT mode=TOTALITY version=2026.VMAX_SUTURED>"