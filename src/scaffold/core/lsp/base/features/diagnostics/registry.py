# Path: core/lsp/base/features/diagnostics/registry.py
# ----------------------------------------------------

import logging
import time
import traceback
from typing import List, Any, Callable, Dict, Optional
from ...document import TextDocument
from ..linter.engine import LinterEngine
from ..linter.contracts import LinterRule  # [ASCENSION]: Import the Law Contract

Logger = logging.getLogger("SentinelRegistry")


class SentinelRegistry:
    """
    =============================================================================
    == THE SENTINEL REGISTRY (V-Ω-FAULT-TOLERANT-AGGREGATOR-HEALED)            ==
    =============================================================================
    The Commander of the Watch.
    It summons the Inquisitors (Local Linter, AI, Daemon, Plugins) and aggregates
    their findings into a single stream of raw evidence.

    [CAPABILITIES]:
    1. **Context Bridge:** Transforms the Document into a rich AnalysisContext via an injected factory.
    2. **Fault Isolation:** Wraps every source in a try/except block.
    3. **Dynamic Recruitment:** Allows registration of new diagnostic sources.
    4. **Law Propagation (THE FIX):** Proxies rules to the internal LinterEngine.
    """

    def __init__(self, server: Any):
        self.server = server

        # [SOURCE 1]: THE HIGH INQUISITOR (Static Linter)
        # Handles Syntax, Security, Style, and the Daemon Proxy Rule.
        self.linter = LinterEngine(server)

        # Dynamic Sources (e.g., AI Prophet, External Tools)
        # List of (Name, Callable[[TextDocument, Context], List[Findings]])
        self._external_sources: List[Any] = []

        # Context Factory: Optional hook to enrich the document before analysis
        self._context_factory: Optional[Callable[[TextDocument, Any], Any]] = None

    def register_rule(self, rule: LinterRule):
        """
        [THE PROXY RITE]
        Passes a Law down to the internal Static Inquisitor (LinterEngine).
        This fixes the 'AttributeError' in the bootstrap sequence.
        """
        self.linter.register(rule)

    def set_context_factory(self, factory: Callable[[TextDocument, Any], Any]):
        """
        [RITE OF ENRICHMENT]
        Registers a factory to transmute the raw TextDocument into a rich AnalysisContext.
        """
        self._context_factory = factory

    def register_source(self, name: str, source_func: Callable[[Any], List[Any]]):
        """
        [RITE OF RECRUITMENT]
        Adds a new diagnostic source to the registry.
        """
        self._external_sources.append((name, source_func))
        Logger.debug(f"Diagnostic Source Recruited: {name}")

    def poll_all(self, doc: TextDocument) -> List[Any]:
        """
        [THE GRAND INQUEST]
        Summons all registered inquisition sources.
        Returns a flat list of raw findings (dicts or objects).
        """
        all_findings = []

        # 1. Forge Context
        # If a factory is registered, use it. Otherwise, pass the raw doc.
        try:
            ctx = self._context_factory(doc, self.server) if self._context_factory else doc
        except Exception as e:
            Logger.error(f"Context Factory Fracture: {e}")
            return [{
                "message": f"Analysis Context Failed: {str(e)}",
                "severity": 2,
                "line": 0,
                "source": "SentinelRegistry",
                "code": "CTX_CRASH"
            }]

        # --- POLL 1: THE STATIC LINTER ---
        try:
            # The LinterEngine runs its suite of Rules against the Context
            linter_results = self.linter.conduct_inquest(ctx)
            if linter_results:
                all_findings.extend(linter_results)
        except Exception as e:
            Logger.error(f"Linter Source Fracture: {e}", exc_info=True)
            all_findings.append({
                "message": f"Static Analysis System Failure: {str(e)}",
                "severity": 2,  # Warning
                "line": 0,
                "source": "SentinelRegistry",
                "code": "LINTER_CRASH"
            })

        # --- POLL 2: EXTERNAL SOURCES ---
        for name, source_func in self._external_sources:
            t_source = time.perf_counter()
            try:
                results = source_func(ctx)  # Pass context (or doc if no factory)
                if results:
                    all_findings.extend(results)

                # Telemetry for slow sources
                dur = (time.perf_counter() - t_source) * 1000
                if dur > 100:
                    Logger.debug(f"Slow Source '{name}': {dur:.2f}ms")

            except Exception as e:
                Logger.error(f"Source '{name}' Fracture: {e}")
                # We do not report every plugin crash to the user to avoid noise.

        return all_findings