# scaffold/semantic_injection/injector.py

"""
=================================================================================
== THE GOD-ENGINE OF SEMANTIC INJECTION (V-Ω-AST-RECURSIVE)                    ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000 (ABSOLUTE EXECUTION AUTHORITY)

This artisan is the **Grand Dispatcher**. It transcends simple string replacement.
It acts as a runtime interpreter for the Semantic Directive Language.

It uses Python's own `ast` module to parse arguments, ensuring full compatibility
with complex data structures (JSON-like objects, lists) and nested calls.
=================================================================================
"""
import ast
import inspect
import re
from typing import Any, Dict, Tuple, List, Optional, Callable

from .contract import SemanticHeresy
from .loader import SemanticRegistry
from ..core.alchemist import get_alchemist
from ..logger import Scribe

Logger = Scribe("SemanticInjector")


class SemanticInjector:
    """
    The Interpreter of the At-Sign (@).
    A recursive, type-safe, AST-powered execution engine.
    """

    # Regex to deconstruct "@namespace/name(args)" -> ("namespace", "name", "args")
    # This initial split is simple; complex parsing happens in _parse_args_via_ast
    DIRECTIVE_REGEX = re.compile(r'^@([\w-]+)/([\w-]+)(?:\((.*)\))?$')

    @classmethod
    def resolve(cls, directive_string: str, context: Dict[str, Any]) -> str:
        """
        THE RITE OF INJECTION (PUBLIC GATEWAY).

        Transmutes a directive string into content.
        Handles caching, recursion, and error boundaries.
        """
        directive_string = directive_string.strip()

        # 1. The Chronocache Check (Elevation 4)
        # We only cache if there are no dynamic variables in the string.
        # If {{}} exists, it's dynamic and must be re-evaluated.
        is_dynamic = "{{" in directive_string
        if not is_dynamic:
            cached = cls._check_cache(directive_string)
            if cached is not None:
                return cached

        # 2. The Gaze of Syntax
        match = cls.DIRECTIVE_REGEX.match(directive_string)
        if not match:
            # Fallback: It might be a simple string starting with @ that isn't a directive
            # We return it as is, or raise heresy if strict.
            # For now, we assume strictness for known @ patterns.
            if '/' in directive_string and '(' in directive_string:
                raise SemanticHeresy(f"Malformed Directive Syntax: '{directive_string}'")
            return directive_string

        namespace = match.group(1)
        name = match.group(2)
        raw_args_str = match.group(3) or ""

        # 3. The Summons of the Domain
        domain = SemanticRegistry.get_domain(namespace)
        if not domain:
            raise SemanticHeresy(
                f"Unknown Semantic Domain: '@{namespace}'. Has the plugin been registered?"
            )

        # 4. The Alchemical Context Injection (Elevation 5)
        # We resolve variables inside the argument string BEFORE parsing.
        # e.g. length={{ len }} -> length=32
        alchemist = get_alchemist()
        if is_dynamic:
            try:
                raw_args_str = alchemist.transmute(raw_args_str, context)
            except Exception as e:
                raise SemanticHeresy(f"Alchemical Paradox in arguments for @{namespace}/{name}: {e}")

        # 5. The AST Argument Parsing (Elevation 1)
        args, kwargs = cls._parse_args_via_ast(raw_args_str)

        # 6. The Recursive Resolution (Elevation 2)
        # If an arg is "@crypto/uuid", resolve it now.
        args = [cls._recursively_resolve(a, context) for a in args]
        kwargs = {k: cls._recursively_resolve(v, context) for k, v in kwargs.items()}

        # 7. The Type Marshall (Elevation 3)
        # Find the method to inspect its signature
        handler_name = f"_directive_{name}"
        handler_method = getattr(domain, handler_name, None)
        if not handler_method:
            raise SemanticHeresy(f"Domain '@{namespace}' does not know the rite of '{name}'.")

        bound_args = cls._bind_and_enforce_types(handler_method, context, args, kwargs)

        # 8. The Execution of Will
        try:
            result = handler_method(*bound_args.args, **bound_args.kwargs)

            # Ensure result is string
            final_result = str(result)

            # Cache if pure
            if not is_dynamic:
                cls._cache_result(directive_string, final_result)

            return final_result

        except Exception as e:
            Logger.error(f"Paradox in @{namespace}/{name}: {e}")
            raise SemanticHeresy(f"Directive Execution Failed: {e}") from e

    @classmethod
    def _recursively_resolve(cls, value: Any, context: Dict[str, Any]) -> Any:
        """
        [ELEVATION 2] THE RECURSIVE RESOLVER.
        If an argument is a string starting with '@' and looks like a directive,
        execute it.
        """
        if isinstance(value, str) and value.startswith('@') and '/' in value:
            # Simple heuristic to avoid infinite recursion loops or accidental text
            if cls.DIRECTIVE_REGEX.match(value):
                return cls.resolve(value, context)
        return value

    @staticmethod
    def _parse_args_via_ast(raw_args: str) -> Tuple[List[Any], Dict[str, Any]]:
        """
        [ELEVATION 1] THE AST WEAVER.
        Uses Python's AST to parse arguments safely and robustly.
        Handles: 1, "string", True, [1, 2], key="value"
        """
        if not raw_args.strip():
            return [], {}

        # We wrap the args in a dummy function call to use ast.parse
        # f("arg1", key="value")
        virtual_code = f"virtual_call({raw_args})"

        try:
            tree = ast.parse(virtual_code, mode='eval')

            # Verify structure
            if not isinstance(tree.body, ast.Call):
                raise ValueError("Invalid argument structure")

            call_node = tree.body

            args = []
            kwargs = {}

            # Parse Positional Args
            for node in call_node.args:
                args.append(ast.literal_eval(node))

            # Parse Keyword Args
            for keyword in call_node.keywords:
                kwargs[keyword.arg] = ast.literal_eval(keyword.value)

            return args, kwargs

        except Exception as e:
            raise SemanticHeresy(f"Syntax Heresy in Arguments: '{raw_args}'. Reason: {e}")

    @staticmethod
    def _bind_and_enforce_types(method: Callable, context: Dict, args: List, kwargs: Dict) -> inspect.BoundArguments:
        """
        [ELEVATION 3] THE TYPE MARSHALL (RE-FORGED).
        Introspects the handler signature and binds arguments.
        Intelligently injects 'context' as either the first positional arg or a kwarg
        to prevent 'multiple values' collisions.
        """
        sig = inspect.signature(method)
        params = list(sig.parameters.values())

        # Create copies to avoid mutating original lists/dicts from the caller
        binding_args = list(args)
        binding_kwargs = kwargs.copy()

        # GNOSTIC LOGIC: Context Injection
        # If the method defines 'context' as the first parameter, we MUST inject it positionally
        # to ensure subsequent user arguments (like '16') shift correctly to 'length'.
        if params and params[0].name == 'context':
            binding_args.insert(0, context)
        # Otherwise, if it asks for context by name (but not first), we use kwargs
        elif 'context' in sig.parameters and 'context' not in binding_kwargs:
            binding_kwargs['context'] = context

        try:
            bound = sig.bind(*binding_args, **binding_kwargs)
            bound.apply_defaults()

            return bound
        except TypeError as e:
            raise SemanticHeresy(f"Signature Mismatch: {e}")

    # --- CACHING LAYER (Simple Memory) ---
    _CACHE = {}

    @classmethod
    def _check_cache(cls, key: str) -> Optional[str]:
        return cls._CACHE.get(key)

    @classmethod
    def _cache_result(cls, key: str, value: str):
        cls._CACHE[key] = value