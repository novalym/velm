# Path: src/velm/codex/injector/engine.py
# ---------------------------------------

"""
=================================================================================
== THE CODEX INJECTOR ENGINE (V-Ω-AST-RECURSIVE-LEGENDARY)                     ==
=================================================================================
LIF: INFINITY | ROLE: DIRECTIVE_INTERPRETER | RANK: OMEGA_SOVEREIGN

This engine parses and executes string-based directives like:
`@cloud/dockerfile(lang="node")`
OR
`@Dockerfile(lang="node")` (Global Alias)

It is the bridge that allows text-based Blueprints to command the Python Kernel.
=================================================================================
"""
import ast
import re
import json
import asyncio
import inspect
from typing import Any, Dict, Tuple, List, Optional, Callable

from ..contract import CodexHeresy
from ..loader import CodexRegistry
from ...core.alchemist import get_alchemist
from ...logger import Scribe

Logger = Scribe("CodexInjector")


class CodexInjector:
    """
    The Supreme Interpreter of the At-Sign (@).
    """

    # Regex: @namespace/name(args) OR @name(args)
    DIRECTIVE_REGEX = re.compile(r'^@(?:([\w-]+)/)?([\w-]+)(?:\((.*)\))?$', re.DOTALL)

    MAX_RECURSION_DEPTH = 10
    _CACHE = {}

    @classmethod
    def resolve(cls, directive_string: str, context: Dict[str, Any], depth: int = 0) -> str:
        """
        [THE RITE OF INJECTION]
        Transmutes a directive string into pure matter (text).
        """
        if depth > cls.MAX_RECURSION_DEPTH:
            raise CodexHeresy("The Ouroboros Trap: Infinite recursion detected.")

        directive_string = directive_string.strip()

        # 1. Alchemical Pre-Pass (Resolve {{ vars }} inside the directive string itself)
        # This allows: @{{ provider }}/deploy(...)
        if "{{" in directive_string:
            alchemist = get_alchemist()
            try:
                directive_string = alchemist.transmute(directive_string, context)
            except:
                pass  # Fallback

        # 2. Syntax Gaze
        match = cls.DIRECTIVE_REGEX.match(directive_string)
        if not match:
            # Not a directive, return raw
            return directive_string

        namespace = match.group(1)  # Can be None (Global)
        name = match.group(2)
        raw_args_str = match.group(3) or ""

        # 3. Domain Resolution
        try:
            domain_handler, resolved_name = CodexRegistry.get_domain_and_rite(namespace, name)
        except Exception as e:
            raise CodexHeresy(f"Resolution Fracture: {e}")

        # 4. Argument Parsing (AST)
        raw_args, raw_kwargs = cls._parse_args_via_ast(raw_args_str)

        # 5. Recursive Resolution of Arguments
        # E.g. port=@math/ceil(10.5)
        resolved_args = [cls._recursively_resolve(a, context, depth + 1) for a in raw_args]
        resolved_kwargs = {k: cls._recursively_resolve(v, context, depth + 1) for k, v in raw_kwargs.items()}

        # 6. Execution
        handler_name = f"_directive_{resolved_name}"
        handler_method = getattr(domain_handler, handler_name)

        # Bind types (using the contract helper if available, or raw call)
        try:
            # We inject context if the method asks for it
            sig = inspect.signature(handler_method)
            if 'context' in sig.parameters:
                if 'context' not in resolved_kwargs:
                    # Place context as first arg if it's the first param, else kwarg
                    params = list(sig.parameters.values())
                    if params[0].name == 'context':
                        resolved_args.insert(0, context)
                    else:
                        resolved_kwargs['context'] = context

            if inspect.iscoroutinefunction(handler_method):
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_running():
                        import nest_asyncio;
                        nest_asyncio.apply()
                        result = asyncio.run(handler_method(*resolved_args, **resolved_kwargs))
                    else:
                        result = asyncio.run(handler_method(*resolved_args, **resolved_kwargs))
                except RuntimeError:
                    result = asyncio.run(handler_method(*resolved_args, **resolved_kwargs))
            else:
                result = handler_method(*resolved_args, **resolved_kwargs)

            # 7. Finality Vow
            if result is None: return ""
            if isinstance(result, (dict, list)): return json.dumps(result, indent=2)
            return str(result)

        except Exception as e:
            Logger.error(f"Paradox in @{name}: {e}")
            raise CodexHeresy(f"Codex Execution Failed: {e}") from e

    @classmethod
    def _recursively_resolve(cls, value: Any, context: Dict[str, Any], depth: int) -> Any:
        if isinstance(value, str) and value.startswith('@'):
            # Only recurse if it looks like a directive
            if cls.DIRECTIVE_REGEX.match(value):
                return cls.resolve(value, context, depth)
        return value

    @staticmethod
    def _parse_args_via_ast(raw_args: str) -> Tuple[List[Any], Dict[str, Any]]:
        if not raw_args.strip(): return [], {}
        virtual_code = f"virtual_call({raw_args})"
        try:
            tree = ast.parse(virtual_code, mode='eval')
            call_node = tree.body

            def safe_eval(node):
                if isinstance(node, ast.Call): raise ValueError("No function calls allowed")
                try:
                    return ast.literal_eval(node)
                except:
                    # Handle unquoted strings like: lang=python (treat python as string)
                    if isinstance(node, ast.Name): return node.id
                    return None

            args = [safe_eval(n) for n in call_node.args]
            kwargs = {kw.arg: safe_eval(kw.value) for kw in call_node.keywords}
            return args, kwargs
        except Exception as e:
            raise CodexHeresy(f"Syntax Heresy in Arguments: '{raw_args}'. Reason: {e}")


# EXPORT ALIAS for compatibility
SemanticInjector = CodexInjector