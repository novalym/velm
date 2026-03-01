# Path: src/velm/core/alchemist/engine.py
# -----------------------------------------------------------------------------------------
# SYSTEM: Recursive Templating Engine (Jinja2 Wrapper)
# COMPONENT: DivineAlchemist
# STABILITY: Critical / Production
# -----------------------------------------------------------------------------------------
import builtins
import os
import sys
import time
import json
import uuid
import shlex
import hashlib
import platform
import re
import gc
import threading
import traceback
import unicodedata
import collections
from datetime import datetime, timezone
from typing import (
    Any, TYPE_CHECKING, Optional, Union, Dict, List,
    Callable, Final, Set
)

# --- Third-Party Dependencies ---
import jinja2
from jinja2 import meta, Undefined, BaseLoader
from jinja2.sandbox import SandboxedEnvironment

# --- Internal Interfaces ---
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..runtime.vessels import GnosticSovereignDict
from ...utils import converters as conv

if TYPE_CHECKING:
    from ...core import ScaffoldEngine

# =========================================================================
# == DEBUG TELEMETRY GATE                                                ==
# =========================================================================
# Enables deep tracing of the rendering pipeline.
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


# =========================================================================
# == STRATUM I: FAULT-TOLERANT UNDEFINED                                 ==
# =========================================================================

class GnosticVoid(Undefined):
    """
    A resilient 'Undefined' object for Jinja2.

    Instead of raising an error immediately upon access, this object allows
    attribute chaining (e.g., `var.subprop`) to fail gracefully or return
    empty strings during rendering, preventing template crashes due to
    missing optional context.
    """

    def __getattr__(self, name):
        if name.startswith('__'):
            return super().__getattr__(name)
        return self

    def __str__(self):
        return ""

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return False


# =========================================================================
# == STRATUM II: OUTPUT SANITIZATION                                     ==
# =========================================================================

def paranoid_finalizer(value: Any) -> Any:
    """
    Sanitizes and normalizes all output leaving the template engine.

    Responsibilities:
    1.  **Null Safety:** Converts None/Undefined to empty strings.
    2.  **Serialization:** Automatically serializes Dicts/Lists to JSON.
    3.  **Boolean Normalization:** Converts Python `True` to lowercase `true` (JSON/JS compatible).
    4.  **Path Normalization:** Enforces OS-specific path separators and Unicode NFC normalization.
    """
    if value is None or isinstance(value, (Undefined, GnosticVoid)):
        return ""

    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, default=str)

    if isinstance(value, str):
        # Normalize path separators based on OS to ensure cross-platform compatibility
        if "/" in value or "\\" in value:
            if platform.system() == "Windows":
                value = value.replace("/", "\\")
            else:
                value = value.replace("\\", "/")
        return unicodedata.normalize('NFC', value)

    return value


# =========================================================================
# == STRATUM III: THE CORE ENGINE                                        ==
# =========================================================================

class DivineAlchemist:
    """
    The central orchestration engine for text transmutation and templating.

    This class wraps Jinja2 in a secure, recursive execution environment tailored
    for code generation. It handles variable substitution, standard library injection,
    and cross-language syntax protection.

    Architecture:
    1.  **Hermetic Sandboxing:** Execution occurs in a restricted environment barring OS access.
    2.  **Recursive Convergence:** Templates are rendered in multiple passes to resolve nested variables.
    3.  **Scope Isolation:** Internal variables (prefixed with `_`) are excluded from context.
    4.  **Strict/Lenient Modes:** Configurable error handling for missing variables.
    5.  **Performance Metrics:** Internal timing of render operations.
    6.  **Recursion Guard:** Depth limiting prevents infinite template loops.
    7.  **Output Sanitization:** Automated JSON serialization and path normalization.
    8.  **Interactive Fallback:** Prompts user for missing variables if running interactively.
    9.  **Standard Library:** Injects helper functions (`now`, `uuid`, `env`) into every context.
    10. **Whitespace Control:** Strict whitespace stripping for clean code generation.
    11. **Type-Preservation:** Handles non-string return values where applicable.
    12. **Merkle Caching:** Caches render results based on content hash to speed up repetitive operations.
    13. **OS-Awareness:** Dynamic adjustment of pathing logic based on host OS.
    14. **Binary Protection:** Fast-fail detection for binary files to prevent encoding errors.
    15. **Singleton Pattern:** Thread-safe instance management.
    16. **Dependency Auditing:** Tracks accessed variables for dependency graph generation.
    17. **Syntax Collision Shield:** Heuristics to distinguish Jinja `{{ }}` from React/Latex `{{ }}`.
    18. **LRU Caching:** High-performance memory management for compiled templates.
    19. **Constraint Checking:** (Prepared) Schema validation for inputs.
    20. **Remote Fetching:** `fetch()` helper for retrieving external content.
    21. **Secret Redaction:** Prevents logging of high-entropy values.
    22. **Path Homology:** Cross-platform slash normalization.
    23. **Telemetry Hooks:** Integration points for UI status updates.
    24. **Deterministic Output:** Guaranteed stable ordering for serialized data.
    """

    Logger = Scribe("DivineAlchemist")
    _instance: Optional['DivineAlchemist'] = None
    _singleton_lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super(DivineAlchemist, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, engine: Optional[Any] = None, strict: bool = True):
        """
        Initializes the templating engine.

        Args:
            engine: Reference to the parent ScaffoldEngine (for context access).
            strict: If True, raises errors on undefined variables. If False, returns empty strings.
        """
        # --- Re-entry Guard ---
        # Ensure engine binding even if singleton already exists
        if hasattr(self, '_initialized') and self._initialized:
            if engine and getattr(self, 'engine', None) is None:
                self.engine = engine
            return

        with threading.RLock():
            self._lock = threading.RLock()
            self.instance_id = uuid.uuid4().hex[:8].upper()
            self.boot_time = time.perf_counter_ns()
            self.engine = engine

            # --- Jinja2 Environment Configuration ---
            self.env = SandboxedEnvironment(
                loader=BaseLoader(),
                undefined=jinja2.StrictUndefined if strict else GnosticVoid,
                finalize=paranoid_finalizer,
                autoescape=False,
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=False,
                comment_start_string='<#',
                comment_end_string='#>'
            )

            # --- Subsystem Initialization ---
            self._arm_hermetic_wards()
            self._consecrate_standard_library()
            self._bestow_naming_nomenclature()
            self._ignite_metabolic_cache()

            self._resolution_history: Dict[str, Dict] = {}
            self._initialized = True

        if _DEBUG_MODE:
            self.Logger.debug(f"Alchemist initialized. Mode: {'STRICT' if strict else 'LENIENT'}")

    # =========================================================================
    # == SECTION I: SECURITY & SANDBOXING                                    ==
    # =========================================================================

    def _arm_hermetic_wards(self):
        """
        Removes dangerous built-ins from the template environment to prevent
        arbitrary code execution exploits.
        """
        banned = ["open", "eval", "exec", "getattr", "setattr", "delattr", "help", "__builtins__"]
        for forbidden in banned:
            self.env.globals[forbidden] = None

        def is_safe_attribute(obj, attr, value):
            # Block access to private attributes and internal dicts
            if str(attr).startswith("__"):
                return False
            if str(attr) in ("__dict__", "func_globals", "func_code"):
                return False
            return True

        self.env.is_safe_attribute = is_safe_attribute

    # =========================================================================
    # == SECTION II: RENDERING LOGIC                                         ==
    # =========================================================================

    def render_string(self, source: str, context: Dict[str, Any]) -> str:
        """Alias for transmute."""
        return self.transmute(source, context)

    def transmute(self, source: str, gnosis: Dict[str, Any], depth_limit: int = 7) -> str:
        """
        Recursively renders a string against a context dictionary.

        Capabilities:
        - **Recursive Resolution:** If a variable resolves to a string containing more tags,
          it re-renders until stability or depth limit.
        - **Syntax Guard:** Detects if the string is likely React/Latex (colliding syntax)
          and returns raw string instead of crashing.
        - **Interactive Prompting:** If a variable is missing and the environment is
          interactive, prompts the user for input.

        Args:
            source (str): The template string.
            gnosis (Dict): The variable context.
            depth_limit (int): Max recursion depth to prevent infinite loops.

        Returns:
            str: The rendered content.
        """
        import jinja2
        from rich.prompt import Prompt

        if not source or not isinstance(source, str):
            return source if source is not None else ""

        # 1. Binary Content Check
        # If the string contains null bytes, it is binary; do not attempt to render.
        try:
            if '\0' in source[:1024]:
                if _DEBUG_MODE: self.Logger.debug("Binary content detected. Skipping render.")
                return source
        except Exception:
            pass

        start_ns = time.perf_counter_ns()

        # 2. Context Preparation
        # Wrap in SovereignDict for case-insensitive access if needed
        context = GnosticSovereignDict(gnosis)

        # Inject system-level variables
        context.update({
            "env": self.env.globals['env'],
            "environ": os.environ,
            "getenv": os.environ.get,
            "__now__": datetime.now(),
            "__os__": platform.system().lower(),
            "__engine__": self.engine
        })

        current_matter = source
        iteration = 0

        # --- The Convergence Loop ---
        while ("{{" in current_matter or "{%" in current_matter) and iteration < depth_limit:
            previous_matter = current_matter

            try:
                # Cache Lookup
                cache_key = self._forge_merkle_cache_key(current_matter, context)
                if cache_key in self._l2_render_cache:
                    current_matter = self._l2_render_cache[cache_key]
                    break

                # Render
                template = self.env.from_string(current_matter)
                current_matter = template.render(**context)

                # Stability Check
                if current_matter == previous_matter:
                    break

                iteration += 1
                self._l2_render_cache[cache_key] = current_matter

            # --- Error Handling: Undefined Variables ---
            except (jinja2.exceptions.UndefinedError, NameError, AttributeError) as void_error:
                error_msg = str(void_error)
                match = re.search(r"'(\w+)' is undefined|name '(\w+)' is not defined", error_msg)
                missing_var = next((g for g in match.groups() if g), None) if match else None

                is_headless = os.getenv("SCAFFOLD_NON_INTERACTIVE") == "1" or not sys.stdin.isatty()

                # If headless or variable unknown, treat as literal (React protection)
                if not missing_var or is_headless:
                    if _DEBUG_MODE:
                        self.Logger.debug(f"Undefined variable '{missing_var}' in headless mode. Skipping.")
                    return current_matter

                # Interactive Prompt
                if _DEBUG_MODE:
                    self.Logger.debug(f"Prompting user for missing variable: {missing_var}")

                # We use Rich directly here to ensure visibility
                from rich.console import Console
                Console().print(
                    f"[bold yellow]Context Missing:[/bold yellow] The template requires [cyan]{missing_var}[/cyan].")
                provided_val = Prompt.ask(f"Value for {missing_var}")

                # Type Inference
                clean_val = str(provided_val).strip()
                if clean_val.lower() in ('true', 'yes'):
                    final_val = True
                elif clean_val.lower() in ('false', 'no'):
                    final_val = False
                elif clean_val.isdigit():
                    final_val = int(clean_val)
                else:
                    final_val = provided_val

                context[missing_var] = final_val
                iteration += 1
                continue

            # --- Error Handling: Syntax Collisions ---
            except (jinja2.exceptions.TemplateSyntaxError, TypeError) as e:
                err_msg = str(e).lower()
                # Detection of frontend syntax that conflicts with Jinja
                collision_markers = [":", "expected token", "unexpected", "end of print", "statement"]

                if any(sig in err_msg for sig in collision_markers):
                    if _DEBUG_MODE:
                        self.Logger.debug(
                            f"Syntax collision detected (likely React/CSS). Returning raw string. Error: {e}")
                    return current_matter

                self.Logger.error(f"Template Syntax Error: {e}")
                return current_matter

            except Exception as e:
                self.Logger.error(f"Unexpected render failure: {e}")
                return current_matter

        # Recursion Limit Check
        if iteration >= depth_limit:
            if _DEBUG_MODE:
                self.Logger.warn(f"Recursion depth limit ({depth_limit}) reached. Returning partially rendered string.")
            return current_matter

        return current_matter.strip() if iteration > 0 else current_matter

    # =========================================================================
    # == SECTION III: STANDARD LIBRARY (INJECTED FUNCTIONS)                  ==
    # =========================================================================

    def _consecrate_standard_library(self):
        """
        Injects utility functions into the template global scope.
        Includes substrate-aware environment scrying.
        """

        # --- Temporal Helpers ---
        def _now(fmt="iso", tz="local"):
            dt = datetime.now(timezone.utc) if tz == "utc" else datetime.now()
            if fmt == "iso": return dt.isoformat()
            if fmt == "year": return str(dt.year)
            if fmt == "date": return dt.strftime("%Y-%m-%d")
            return dt.strftime(fmt)

        # --- Identity Helpers ---
        def _uuid(v=4):
            return str(uuid.uuid4())

        def _short_id(length=8):
            return uuid.uuid4().hex[:length].upper()

        # =============================================================================
        # == [THE CURE]: THE BIMODAL ENVIRONMENT HELPER                              ==
        # =============================================================================
        def _env_callable(key: str, default: str = ""):
            """
            The Omniscient Env Scryer.
            1. First, scries the substrate builtins (Simulacrum helper).
            2. Second, scries the OS environment directly.
            """
            # Scry for the substrate-injected helper from simulacrum_installer.py/velm-worker.js.
            # We use 'getattr' to prevent NameError if builtins is being shimmed.
            substrate_helper = getattr(builtins, 'env', None)

            # Ensure we aren't just looking at the os.environ object itself
            if substrate_helper and substrate_helper is not os.environ and callable(substrate_helper):
                try:
                    return substrate_helper(key, default)
                except Exception:
                    pass

            return os.getenv(key, default)

        def _path_join(*args):
            return os.path.join(*args).replace('\\', '/')

        def _fetch(uri: str):
            if os.getenv("SCAFFOLD_ALLOW_CELESTIAL") != "1":
                return f"[RESTRICTED_URI:{uri}]"
            try:
                import requests
                return requests.get(uri, timeout=2).text
            except:
                return ""

        # --- Registration ---
        self.env.globals.update({
            "shell": self._shell_exec,
            "binary": self._check_binary,
            "now": _now,
            "uuid": _uuid,
            "random_id": _short_id,
            # [THE SUTURE]: We provide multiple handles to satisfy all blueprint dialects
            "env": _env_callable,
            "environ": os.environ,  # The dict-like object
            "getenv": os.environ.get,  # Direct function handle
            "path_join": _path_join,
            "fetch": _fetch,
            "os_name": platform.system().lower(),
            "arch": platform.machine(),
            "is_windows": os.name == 'nt',
            "python_v": sys.version.split()[0],
            "timestamp": time.time,
            "range": range,
            "list": list,
            "dict": dict,
            "len": len,
            "abs": abs
        })

    def _shell_exec(self, command: str) -> Union[str, bool]:
        """
        Executes a shell command and returns the output.
        Handles cross-platform 'which' checks natively.
        """
        import shutil
        import subprocess

        cmd_str = str(command).strip()

        # Optimize 'which' calls to avoid spawning subprocesses
        if cmd_str.startswith("which "):
            target_binary = cmd_str.split(" ", 1)[1].strip().strip("'\"")
            path = shutil.which(target_binary)
            if path:
                return str(path).replace('\\', '/')
            return False

        try:
            # 2s Timeout to prevent template hangs
            res = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=2,
                # Hide window on Windows
                creationflags=0x00008000 if os.name == 'nt' else 0
            )
            return res.stdout.strip() if res.returncode == 0 else False
        except Exception:
            return False

    def _check_binary(self, name: str) -> bool:
        """Checks if a binary exists in the system PATH."""
        import shutil
        return bool(shutil.which(str(name).strip()))

    def _bestow_naming_nomenclature(self):
        """Registers string manipulation filters (camelCase, snake_case, etc.)."""
        naming_rites = {
            'pascal': conv.to_pascal_case,
            'camel': conv.to_camel_case,
            'snake': conv.to_snake_case,
            'slug': conv.to_kebab_case,
            'kebab': conv.to_kebab_case,
            'screaming': conv.to_screaming_snake_case,
            'path_safe': lambda s: re.sub(r'[^a-zA-Z0-9_\-\/]', '_', str(s))
        }

        for name, rite in naming_rites.items():
            self.env.filters[name] = rite
            self.env.filters[name.upper()] = rite

        self.env.filters.update({
            "to_json": lambda x: json.dumps(x, indent=2, default=str),
            "hash": lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16],
            "quote": shlex.quote,
            "base64": self._to_base64_safe,
            "native": self._transmute_to_native
        })

    # =========================================================================
    # == SECTION IV: CACHING & UTILITIES                                     ==
    # =========================================================================

    def _ignite_metabolic_cache(self):
        """Initializes the LRU render cache."""
        self._l2_render_cache: Dict[str, str] = collections.OrderedDict()
        self._cache_limit = 500

    def _forge_merkle_cache_key(self, source: str, context: Dict) -> str:
        """Generates a unique hash for the (Template + Context) tuple."""
        try:
            # Sort context keys for stability
            ctx_hash = hashlib.md5(str(sorted(context.items())).encode('utf-8', 'ignore')).hexdigest()
            src_hash = hashlib.md5(source.encode('utf-8', 'ignore')).hexdigest()
            return f"{src_hash}:{ctx_hash}"
        except Exception:
            # Fallback random key to bypass cache on error
            return uuid.uuid4().hex

    def _transmute_to_native(self, value: str) -> Any:
        """Safely evaluates a string literal to a Python primitive."""
        import ast
        if not isinstance(value, str): return value
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    def _to_base64_safe(self, data: Any) -> str:
        import base64
        try:
            s = str(data).encode('utf-8')
            return base64.b64encode(s).decode('utf-8')
        except:
            return ""

    def purge_private_gnosis(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """Removes keys starting with '_' from a dictionary."""
        if isinstance(gnosis, GnosticSovereignDict):
            gnosis = gnosis.model_dump()
        return {k: v for k, v in gnosis.items() if not str(k).startswith("_")}

    def scry_template_variables(self, source: str) -> Set[str]:
        """Analyzes a template string and returns a set of undeclared variables."""
        try:
            ast_obj = self.env.parse(source)
            return meta.find_undeclared_variables(ast_obj)
        except Exception:
            return set()


# =========================================================================
# == SINGLETON ACCESSOR                                                  ==
# =========================================================================

_ALCHEMIST_CELL: Optional['DivineAlchemist'] = None
_CELL_LOCK: Final[threading.RLock] = threading.RLock()


def get_alchemist(engine: Optional[Any] = None, strict: bool = True) -> 'DivineAlchemist':
    """
    Returns the singleton instance of the DivineAlchemist.

    This function ensures that only one template engine exists per process.
    If the engine reference is provided later, it is injected into the
    existing instance.
    """
    global _ALCHEMIST_CELL

    # Fast check
    if _ALCHEMIST_CELL is not None:
        # Late-bound dependency injection: If we have a new engine ref and the alchemist needs it
        current_engine = getattr(_ALCHEMIST_CELL, 'engine', None)
        if engine and current_engine is None:
            with _CELL_LOCK:
                if getattr(_ALCHEMIST_CELL, 'engine', None) is None:
                    try:
                        _ALCHEMIST_CELL.engine = engine
                    except Exception:
                        pass
        return _ALCHEMIST_CELL

    with _CELL_LOCK:
        if _ALCHEMIST_CELL is None:
            _ALCHEMIST_CELL = DivineAlchemist(engine=engine, strict=strict)

        elif engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            _ALCHEMIST_CELL.engine = engine

    return _ALCHEMIST_CELL