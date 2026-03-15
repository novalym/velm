# Path: core/alchemist/elara/resolver/pipeline/engine.py
# ------------------------------------------------------

import time
import re
import logging
from typing import Any

from ..context import LexicalScope
from ..evaluator import GnosticASTEvaluator, UndefinedGnosisHeresy, AmnestyGrantedHeresy
from ......logger import Scribe

from .deconstructor import PipeDeconstructor
from .jit_alchemist import JitAlchemist
from .reactor import RiteReactor

Logger = Scribe("FilterPipeline")


class FilterPipeline:
    """
    =============================================================================
    == THE SUPREME ALCHEMICAL THRUWAY (L2) (V-Ω-TOTALITY-VMAX-ASCENDED)        ==
    =============================================================================
    LIF: 10,000,000x | ROLE: MATTER_TRANSMUTATION_CONDUCTOR | RANK: OMEGA

    The newly ascended Orchestrator. It delegates string parsing to the
    `PipeDeconstructor`, Python logic to the `JitAlchemist`, and filter execution
    to the `RiteReactor`.
    """

    @classmethod
    def execute(cls, raw_content: str, scope: LexicalScope) -> Any:
        """
        =========================================================================
        == THE RITE OF TRANSMUTATION (EXECUTE)                                 ==
        =========================================================================
        """
        _start_ns = time.perf_counter_ns()
        scope.set("__start_time_ns__", _start_ns)

        # 1. THE RECURSIVE PIPE SIEVE (DECONSTRUCT)
        pipeline_segments = PipeDeconstructor.deconstruct(raw_content)
        if not pipeline_segments:
            return None

        base_expression = pipeline_segments[0].strip()
        willed_filter_rites = pipeline_segments[1:]

        # 2. BASE EXPRESSION RESOLUTION
        if base_expression.startswith('py:'):
            value = JitAlchemist.execute(base_expression[3:], scope)
        else:
            # Scry for default filters downstream
            has_default = any(re.match(r'^_*(default|coalesce|d)_*\b', f.strip()) for f in willed_filter_rites)

            try:
                # [ASCENSION 101]: Resolve Codex Directives (@) within the base
                if base_expression.startswith('@'):
                    from ......codex import resolve_codex_directive
                    value = resolve_codex_directive(base_expression, scope.local_vars)
                else:
                    value = GnosticASTEvaluator.evaluate(base_expression, scope)

            except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as heresy:
                # [ASCENSION 98]: THE DEFAULT PARADOX SUTURE
                if has_default:
                    value = None
                else:
                    raise heresy
            except Exception as e:
                if has_default:
                    value = None
                else:
                    raise AmnestyGrantedHeresy(f"Base logic fracture: {e}")

        # =========================================================================
        # == 3. THE INDESTRUCTIBLE PIPELINE WARD (THE MASTER CURE)               ==
        # =========================================================================
        for idx, rite_scripture in enumerate(willed_filter_rites):
            rite_str = rite_scripture.strip()
            if not rite_str:
                continue

            # [ASCENSION 131]: Substrate-Aware Yielding
            if idx > 10: time.sleep(0)

            try:
                # Support for '| py' filter inline
                if rite_str == 'py':
                    value = JitAlchemist.execute(str(value), scope)
                else:
                    # [STRIKE]: Delegate to the Reactor
                    value = RiteReactor.strike(value, rite_str, scope)

            except (UndefinedGnosisHeresy, AmnestyGrantedHeresy, Exception) as pipeline_fracture:
                if 'has_default' in locals() and has_default:
                    Logger.verbose(f"Filter '{rite_str}' fractured ({pipeline_fracture}). Cascading Void.")
                    value = None
                else:
                    raise AmnestyGrantedHeresy(f"Pipeline Fracture in '{rite_str}': {pipeline_fracture}")

        # 4. METABOLIC FINALITY
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _duration_ms > 20.0:
            Logger.verbose(f"High-Mass Pipeline concluded in {_duration_ms:.2f}ms.")

        return value