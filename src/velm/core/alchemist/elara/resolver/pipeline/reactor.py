# Path: core/alchemist/elara/resolver/pipeline/reactor.py
# -------------------------------------------------------

import re
import inspect
from typing import Any, Set, Final

from ..context import LexicalScope
from ..evaluator import GnosticASTEvaluator, UndefinedGnosisHeresy, AmnestyGrantedHeresy, GnosticVoid
from ...library.registry import RITE_REGISTRY
from ......logger import Scribe

from .argument_thawer import ArgumentThawer

Logger = Scribe("RiteReactor")

class RiteReactor:
    """
    =============================================================================
    == THE KINETIC FILTER REACTOR (V-Ω-TOTALITY)                               ==
    =============================================================================
    LIF: ∞^∞ | ROLE: RITE_ADJUDICATOR | RANK: OMEGA_SOVEREIGN[ASCENSION 149]: The execution switchboard. Evaluates a single filter rite.
    """

    ARITHMETIC_OPERATORS: Final[Set[str]] = {'+', '-', '*', '/', '%', '//', '**'}

    @classmethod
    def strike(cls, value: Any, rite_str: str, scope: LexicalScope) -> Any:
        """
        =============================================================================
        == THE KINETIC FILTER REACTOR: OMEGA (V-Ω-TOTALITY-VMAX-SENSORY-SUTURE)    ==
        =============================================================================
        LIF: ∞ | ROLE: RITE_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

        [THE MASTER CURE]: Implements Bicameral Sensory Scrying. It righteously
        prioritizes the Alchemist's waked filters (| default, | snake) before
        querying the static registry, annihilating the 'Unmanifest Rite' heresy.
        """
        # --- MOVEMENT 0: ARITHMETIC SHORTHAND ---
        if rite_str and rite_str[0] in cls.ARITHMETIC_OPERATORS:
            try:
                math_expr = f"{value} {rite_str}"
                return GnosticASTEvaluator.evaluate(math_expr, scope)
            except Exception:
                return value

        # --- MOVEMENT I: THE HALLUCINATION SHEARS ---
        clean_rite = rite_str.strip().strip('_')
        match = re.match(r'^([a-zA-Z0-9_.\-]+)(?:\((.*)\))?$', clean_rite)
        if not match:
            return f"{{{{ {rite_str} }}}}"

        name, args_body = match.groups()
        rite_name = name.lower()
        is_mercy = rite_name in ('default', 'coalesce', 'd')

        # =========================================================================
        # == MOVEMENT II: [THE MASTER CURE] - BICAMERAL SENSORY SCRY             ==
        # =========================================================================
        # 1. Scry the Lexical Mind-State (__filters__ injected by Alchemist)
        # 2. Scry the Registry's Hot-Path Cache

        filter_func = None
        # Retrieve the Alchemist's local filter bank from the scope
        alchemist_filters = scope.get('__filters__', {})
        filter_func = alchemist_filters.get(rite_name)

        if not filter_func:
            # Consult the Registry's O(1) Hot Cache (Jinja-Killers reside here)
            filter_func = RITE_REGISTRY.get(rite_name)

        # 3. Consult the Static Metadata Ledger (For complex, non-lambda rites)
        rite_metadata = RITE_REGISTRY.get_rite_metadata(rite_name)

        # --- MOVEMENT III: ADJUDICATION ---
        if not filter_func and not rite_metadata:
            if scope.global_ctx.strict_mode:
                # [THE FIX]: Only raise if truly unmanifest in every stratum
                raise UndefinedGnosisHeresy(f"Unmanifest alchemical rite: '{rite_name}'")
            return value

        # --- MOVEMENT IV: ARGUMENT THAWING ---
        # [ASCENSION 146]: Transmute raw strings into Python souls
        args, kwargs = ArgumentThawer.thaw(args_body, rite_name, scope, is_mercy)

        # --- MOVEMENT V: THE KINETIC STRIKE ---
        try:
            # If we have a static metadata record, perform a warded strike
            if rite_metadata:
                sig = rite_metadata.signature
                if 'start_time_ns' in sig.parameters:
                    kwargs['start_time_ns'] = scope.get("__start_time_ns__")

                # Execute via the warded metadata handler
                return rite_metadata.handler(value, *args, **kwargs)

            # [PATH B]: Execute the dynamic lambda-soul (The Jinja Killer path)
            return filter_func(value, *args, **kwargs)

        except Exception as strike_fracture:
            # [ASCENSION 120]: Fault-Isolated Redemption
            if is_mercy:
                return value  # The default filter is a Savior; it never fractures.

            raise AmnestyGrantedHeresy(f"Alchemical Strike Fractured in '{rite_name}': {strike_fracture}")