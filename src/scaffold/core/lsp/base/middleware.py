# Path: core/lsp/base/middleware.py
# ---------------------------------
# LIF: INFINITY | ROLE: PIPELINE_ORCHESTRATOR | RANK: SOVEREIGN
# auth_code: Ω_MIDDLEWARE_TOTALITY_V26_SUTURED_SINGULARITY

import time
import logging
import traceback
from typing import Callable, Any, Dict, List, TypeVar, Union, Optional

# --- GNOSTIC CONTRACTS ---
# A Handler takes (Matter, Context) and returns a Revelation
Handler = Callable[[Any, Dict[str, Any]], Any]

# A Middleware takes (NextStep, Matter, Context) and returns a Revelation
Middleware = Callable[[Handler, Any, Dict[str, Any]], Any]


class MiddlewarePipeline:
    """
    =============================================================================
    == THE INTERCEPTOR NEXUS (V-Ω-TOTALITY-V26-SUTURED)                        ==
    =============================================================================
    LIF: INFINITY | ROLE: CROSS_CUTTING_ORCHESTRATOR | RANK: SOVEREIGN

    The aspect-oriented engine of the Gnostic Kernel. It wraps the execution
    of a Rite in layers of logic, ensuring absolute awareness across the
    entire causal chain.
    =============================================================================
    """

    def __init__(self):
        self._layers: List[Middleware] = []
        self.logger = logging.getLogger("MiddlewareNexus")

    def use(self, middleware: Middleware):
        """
        [RITE]: INJECT_ARMOR
        Adds a new layer to the exterior of the gnostic onion.
        """
        self._layers.append(middleware)
        self.logger.debug(f"Middleware Grafted. Nexus Depth: {len(self._layers)}")

    def run(self, final_handler: Handler, params: Any, context: Dict[str, Any]) -> Any:
        """
        [THE RITE OF EXECUTION]
        Sutures the layers and fires the intent through the neural stack.

        Args:
            final_handler: The core execution logic (Dispatcher Adapter).
            params: The primary Gnostic matter (Pydantic Model or Dict).
            context: The metadata context (TraceID, Server, Vitals).
        """

        # =========================================================================
        # == MOVEMENT I: THE SUTURED CORE ADAPTER (THE FIX)                      ==
        # =========================================================================
        # [ASCENSION 1]: Absolute Signature Parity.
        # This base case ensures that the context (c) is never discarded.
        def core_case(p: Any, c: Dict[str, Any]):
            return final_handler(p, c)

        # =========================================================================
        # == MOVEMENT II: ONION COMPILATION                                      ==
        # =========================================================================
        # We build the chain from the inside out (Tail-Recursion Style).
        # stack becomes: Layer1( Layer2( Layer3( core_case ) ) )

        chain = core_case

        for layer in reversed(self._layers):
            # We use a closure factory to bind the current layer to the next step
            def compile_layer(current_layer=layer, next_step=chain):
                # The compiled unit takes (Matter, Context) and passes them on
                return lambda p, c: current_layer(next_step, p, c)

            chain = compile_layer()

        # =========================================================================
        # == MOVEMENT III: IGNITION & TELEMETRY                                  ==
        # =========================================================================
        start_ns = time.perf_counter_ns()
        trace_id = context.get("trace_id", "0xVOID")

        try:
            # Entry into the first layer of the onion
            result = chain(params, context)

            # Performance Chronometry [ASCENSION 4]
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if duration_ms > 100:
                self.logger.warning(
                    f"[{trace_id}] Heavy Pipeline: {duration_ms:.2f}ms across {len(self._layers)} layers.")

            return result

        except Exception as fracture:
            # [ASCENSION 7]: EXCEPTION TRANSLOCATION
            # If the fracture wasn't caught by a middleware layer, we scribe it here
            # before it reaches the Dispatcher.
            if not isinstance(fracture, (ValueError, TypeError, AttributeError)):
                self.logger.error(f"[{trace_id}] Unhandled Pipeline Fracture: {fracture}")

            # Re-raise to let the Dispatcher's ErrorForge handle the protocol response
            raise fracture

    def clear(self):
        """[RITE]: TABULA_RASA"""
        self._layers = []
        self.logger.info("Middleware Nexus Purged.")

# === SCRIPTURE SEALED: THE NEXUS IS INVINCIBLE ===