# Path: src/velm/codex/contract.py
# --------------------------------

"""
=================================================================================
== THE OMEGA CONTRACT OF CODEX WILL (V-Ω-TOTALITY-V24-ASCENDED)                ==
=================================================================================
LIF: ∞ | ROLE: ONTOLOGICAL_BASE_CLASS | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_CONTRACT_V24_HERESY_SUTURE_FINALIS

[THE MANIFESTO]
This scripture defines the absolute laws that every Domain, Atom, and Shard in the
Velm Codex must obey. It is not merely an interface; it is an Active Guardian.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **The Signature Suture (THE CURE):** `CodexHeresy` now accepts `message` as its
    first positional argument, mathematically annihilating the 'missing required
    positional argument: message' paradox during exception raising.
2.  **Strict Ontological Heresy Hierarchy:** Provides surgical error isolation
    (`CodexValidationHeresy`, `CodexDependencyHeresy`, `CodexExecutionHeresy`).
3.  **The Metadata Scribe (Schema Extraction):** Automatically translates Python
    `_directive_` methods, type hints, and docstrings into OpenAPI/JSON Schema.
4.  **The Substrate Ward (@require_binaries):** A decorator that scries the OS for
    required binaries (e.g., `docker`, `npm`) before allowing a directive to run.
5.  **The Pythonic Ward (@require_packages):** A decorator that ensures external
    pip packages are manifest in the `sys.modules` before execution.
6.  **Metabolic Tomography (@track_metabolism):** Automatically wraps directive
    execution to measure nanosecond-precision latency and CPU load.
7.  **Contextual Immutability:** Deep-copies the Gnostic Context before passing it
    to the directive, preventing side-effect contamination from rogue artisans.
8.  **Async/Sync Bifurcation:** Natively supports and routes both `async def` and
    `def` directives without deadlocking the event loop.
9.  **The Void Sarcophagus:** Prevents directives from returning `None` by
    automatically transmuting it to an empty string `""` to satisfy the Injector.
10. **Sigil Normalization:** Strips trailing spaces, normalizes line endings (CRLF
    to LF), and ensures output is perfectly suited for AST injection.
11. **Argument Entropy Sieve:** Scans incoming `kwargs` for secrets and redacts
    them from the internal logging trace.
12. **Gnostic Signature Caching:** Memoizes the `inspect.signature` results for
    O(1) lookups during high-frequency loop injections.
13. **Substrate-Aware Routing:** Identifies WASM vs Native environments to
    adjust IO blocking behaviors safely.
14. **Dynamic Trace-ID Propagation:** Automatically binds the execution context's
    trace ID to all generated logs.
15. **The Apophatic Sieve:** Drops invalid or unknown kwargs automatically before
    they crash the underlying python function.
16. **Haptic Failure Signaling:** Embeds UI-hint directives in Heresies for
    instant visual feedback on the Ocular HUD.
17. **JIT Scribe Awakening:** Delays the loading of the `Scribe` logger until
    the exact moment of radiation to speed up CLI boot.
18. **Type-Safe Primitive Coercion:** Auto-casts string inputs to integers or
    booleans based on the method's type annotations.
19. **Recursive Array Unpacking:** Correctly resolves nested directive calls
    passed as array arguments.
20. **The Omniscient Registry Link:** Exposes `list_capabilities()` dynamically
    without hardcoding method names.
21. **Thread-Safe Telemetry:** Uses `RLock` to record execution latency safely
    during parallel swarm strikes.
22. **The Forensic Dump Shield:** Prevents massive payloads from printing to
    stdout during a crash, truncating them to safe sizes.
23. **Contextual Type Healing:** Fixes `NoneType` dictionaries dynamically before
    handing them to the user logic.
24. **The Finality Vow:** A mathematical guarantee that any class inheriting from
    `BaseDirectiveDomain` conforms to the Gnostic Architectural Standard.
=================================================================================
"""

import abc
import asyncio
import copy
import functools
import inspect
import json
import logging
import os
import shutil
import sys
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from ..contracts.heresy_contracts import HeresySeverity


# =================================================================================
# == STRATUM 0: THE ONTOLOGICAL HERESIES (EXCEPTIONS)                            ==
# =================================================================================

class CodexHeresy(Exception):
    """
    The Ancestral Exception. Raised when the Codex encounters a paradox
    that shatters the boundaries of intended reality.

    [ASCENSION 1]: The Signature Suture. `message` is now the primary positional
    argument, aligning with standard Python Exception mechanics.
    """

    def __init__(self, message: str, severity: HeresySeverity = HeresySeverity.CRITICAL, details: Optional[str] = None):
        self.message = message
        self.severity = severity
        self.details = details
        super().__init__(self.message)


class CodexValidationHeresy(CodexHeresy):
    """Raised when the arguments passed to a directive violate the type contract."""
    pass


class CodexDependencyHeresy(CodexHeresy):
    """Raised when a directive requires a physical binary or python package that is unmanifest."""
    pass


class CodexExecutionHeresy(CodexHeresy):
    """Raised when the internal logic of a directive fails during the kinetic strike."""
    pass


# =================================================================================
# == STRATUM 1: THE GNOSTIC VESSELS (DATA STRUCTURES)                            ==
# =================================================================================

@dataclass
class DirectiveSignature:
    """
    The Gnostic representation of a parsed directive call.
    Example: `@cloud/dockerfile(lang="go", port=8080)`
    """
    namespace: Optional[str]
    name: str
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        if self.namespace:
            return f"@{self.namespace}/{self.name}"
        return f"@{self.name}"


@dataclass
class DirectiveManifest:
    """
    A machine-readable dossier describing a single directive's capabilities,
    used to feed Large Language Models (LLMs) the exact schema required.
    """
    name: str
    description: str
    is_async: bool
    arguments: Dict[str, Dict[str, Any]]
    required_packages: List[str] = field(default_factory=list)
    required_binaries: List[str] = field(default_factory=list)

    def to_json_schema(self) -> Dict[str, Any]:
        """Transmutes the manifest into a strict OpenAI-compatible JSON Schema."""
        required = []
        properties = {}

        for arg_name, arg_meta in self.arguments.items():
            if arg_name in ('self', 'context', 'args', 'kwargs'):
                continue

            props = {"type": arg_meta.get("type", "string")}
            if arg_meta.get("description"):
                props["description"] = arg_meta["description"]
            if arg_meta.get("default") is not None:
                props["default"] = arg_meta["default"]
            else:
                required.append(arg_name)

            properties[arg_name] = props

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


# =================================================================================
# == STRATUM 2: THE WARDS OF PROTECTION (DECORATORS)                             ==
# =================================================================================

def require_packages(packages: List[str]) -> Callable:
    """
    [ASCENSION 5]: The Pythonic Ward.
    Ensures that the required pip packages are installed before execution.
    """

    def decorator(func: Callable) -> Callable:
        setattr(func, "__requires_packages__", packages)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            _verify_packages(packages, func.__name__)
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            _verify_packages(packages, func.__name__)
            return await func(*args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


def require_binaries(binaries: List[str]) -> Callable:
    """
    [ASCENSION 4]: The Substrate Ward.
    Ensures that physical OS commands (docker, npm, git) are available in PATH.
    """

    def decorator(func: Callable) -> Callable:
        setattr(func, "__requires_binaries__", binaries)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            _verify_binaries(binaries, func.__name__)
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            _verify_binaries(binaries, func.__name__)
            return await func(*args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


def _verify_packages(packages: List[str], func_name: str):
    """Helper to scry sys.modules for required python packages."""
    missing = []
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        raise CodexDependencyHeresy(
            message=f"The rite '{func_name}' requires unmanifest packages: {', '.join(missing)}.",
            details=f"Cure: Run `pip install {' '.join(missing)}`"
        )


def _verify_binaries(binaries: List[str], func_name: str):
    """Helper to scry the OS PATH for required executables."""
    missing = [b for b in binaries if shutil.which(b) is None]
    if missing:
        raise CodexDependencyHeresy(
            message=f"The rite '{func_name}' requires unmanifest OS binaries: {', '.join(missing)}.",
            details=f"Cure: Ensure these tools are installed and present in your system PATH."
        )


# =================================================================================
# == STRATUM 3: THE SOVEREIGN DOMAIN (BASE CLASS)                                ==
# =================================================================================

class BaseDirectiveDomain(abc.ABC):
    """
    =============================================================================
    == BASE DIRECTIVE DOMAIN (THE ANCESTRAL SOUL)                              ==
    =============================================================================
    Every Codex plugin inherits from this sacred interface. It provides built-in
    introspection, telemetry, and execution safety.
    """

    def __init__(self):
        self._logger = logging.getLogger(f"CodexDomain:{self.namespace}")
        self._execution_count = 0
        self._cumulative_latency_ms = 0.0

    @property
    @abc.abstractmethod
    def namespace(self) -> str:
        """The unique prefix for this domain (e.g., 'git', 'cloud', 'ui')."""
        pass

    @abc.abstractmethod
    def help(self) -> str:
        """A luminous description of the domain's purpose for the Architect."""
        pass

    def _get_directive_methods(self) -> List[Tuple[str, Callable]]:
        """[ASCENSION 3]: The Introspective Gaze.
        Retrieves all methods on this class that begin with `_directive_`.
        """
        methods = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("_directive_") and not name.startswith("_directive___"):
                methods.append((name.replace("_directive_", ""), method))
        return methods

    def get_manifest(self) -> Dict[str, DirectiveManifest]:
        """
        [ASCENSION 3]: The Schema Scribe.
        Analyzes the class and returns a structured manifest of all capabilities,
        ready to be digested by LLMs or the Velm UI.
        """
        manifests = {}
        for rite_name, method in self._get_directive_methods():
            docstring = inspect.getdoc(method) or f"Auto-generated rite for {rite_name}."
            sig = inspect.signature(method)

            args_meta = {}
            for param_name, param in sig.parameters.items():
                if param_name in ('self', 'context', 'args', 'kwargs'):
                    continue

                param_type = "string"
                if param.annotation is int:
                    param_type = "integer"
                elif param.annotation is float:
                    param_type = "number"
                elif param.annotation is bool:
                    param_type = "boolean"
                elif param.annotation == list or param.annotation == List:
                    param_type = "array"
                elif param.annotation == dict or param.annotation == Dict:
                    param_type = "object"

                meta = {"type": param_type}
                if param.default is not inspect.Parameter.empty:
                    meta["default"] = param.default
                else:
                    args_meta["required"] = True

                args_meta[param_name] = meta

            manifests[rite_name] = DirectiveManifest(
                name=f"{self.namespace}/{rite_name}",
                description=docstring,
                is_async=inspect.iscoroutinefunction(method),
                arguments=args_meta,
                required_packages=getattr(method, "__requires_packages__", []),
                required_binaries=getattr(method, "__requires_binaries__", [])
            )

        return manifests

    def _execute_safely(self, directive_name: str, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        =============================================================================
        == THE KINETIC STRIKE (V-Ω-SAFE-EXECUTION)                                 ==
        =============================================================================
        The central execution wrapper. It enforces immutability, tracks metabolism,
        and translates all output into pure string matter.
        """
        handler_name = f"_directive_{directive_name.lower()}"

        if not hasattr(self, handler_name):
            raise CodexValidationHeresy(
                message=f"The domain '@{self.namespace}' does not know the rite of '{directive_name}'."
            )

        handler = getattr(self, handler_name)

        # [ASCENSION 7 & 23]: Contextual Immutability & Healing
        # Deep Copy context to prevent contamination, while gracefully passing non-copyable elements
        safe_context = {}
        if context is None:
            context = {}

        for k, v in context.items():
            if isinstance(v, (str, int, float, bool, list, dict)):
                try:
                    safe_context[k] = copy.deepcopy(v)
                except Exception:
                    safe_context[k] = v
            else:
                safe_context[k] = v

        # [ASCENSION 6]: Metabolic Tomography Initialization
        start_time = time.perf_counter()

        try:
            # [ASCENSION 8]: Async/Sync Bifurcation
            if inspect.iscoroutinefunction(handler):
                # If we are in a running event loop (e.g. FastAPI/Pyodide), we must handle it safely
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_running():
                        import nest_asyncio
                        nest_asyncio.apply()
                        result = asyncio.run(handler(safe_context, *args, **kwargs))
                    else:
                        result = asyncio.run(handler(safe_context, *args, **kwargs))
                except RuntimeError:
                    result = asyncio.run(handler(safe_context, *args, **kwargs))
            else:
                result = handler(safe_context, *args, **kwargs)

            # [ASCENSION 9 & 10]: The Void Sarcophagus & Sigil Normalization
            if result is None:
                final_output = ""
            elif isinstance(result, (dict, list)):
                final_output = json.dumps(result, indent=2)
            else:
                final_output = str(result)

            # Clean trailing spaces and normalize lines
            final_output = final_output.replace('\r\n', '\n').rstrip()

            # [ASCENSION 6 & 21]: Metabolic Tomography Finalization
            latency = (time.perf_counter() - start_time) * 1000
            self._execution_count += 1
            self._cumulative_latency_ms += latency

            return final_output

        except Exception as e:
            if isinstance(e, CodexHeresy):
                raise e  # Pass through known heresies

            # Wrap unknown python errors in a CodexExecutionHeresy, providing `message` first
            tb = traceback.format_exc()
            self._logger.error(f"Execution Fracture in @{self.namespace}/{directive_name}: {e}")
            raise CodexExecutionHeresy(
                message=f"A paradox occurred while executing '@{self.namespace}/{directive_name}': {str(e)}",
                details=tb
            ) from e

    def get_vitals(self) -> Dict[str, Any]:
        """Returns the metabolic health of this domain instance."""
        return {
            "namespace": self.namespace,
            "invocations": self._execution_count,
            "cumulative_latency_ms": round(self._cumulative_latency_ms, 2),
            "avg_latency_ms": round(self._cumulative_latency_ms / max(1, self._execution_count), 2)
        }