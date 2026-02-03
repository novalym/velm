# Path: core/artisans/analyze/orchestrator.py
# --------------------------------------

import sys
import time
import uuid
from typing import Dict, Any, Set

from .processing.scaffold import ScaffoldProcessor
from .processing.foreign import ForeignProcessor
from .core.context import AnalysisContext
from ...core.sentinel_conduit import SentinelConduit
from ...logger import Scribe


class AnalysisOrchestrator:
    """
    =============================================================================
    == THE CONDUCTOR (V-Ω-ROUTING-LOGIC-ASCENDED)                              ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: LOGIC_DISPATCHER

    The central switchboard of the Analysis Artisan.
    It decides whether a scripture is Native (Scaffold/Symphony) or Foreign (Code),
    and dispatches it to the appropriate specialized processor.

    [ASCENSION LOG]:
    1.  **Forensic Routing Log:** Explicitly screams the chosen route to stderr.
    2.  **Chronometric Guard:** Measures exact processor execution latency.
    3.  **Sentinel Injection:** Injects the SentinelConduit for foreign tongues.
    4.  **Grammar Normalization:** Sanitizes input keys to prevent routing failures.
    5.  **Fault Tolerance:** Wraps processor execution in a global try/except.
    6.  **Result Standardization:** Guarantees a valid Dictionary return, never None.
    7.  **Trace ID Propagation:** Generates or propagates trace IDs.
    8.  **Telemetry Enrichment:** Adds orchestrator meta-data to results.
    9.  **Bimodal Dispatch:** Clear separation of Native vs Foreign logic.
    10. **The Void Fallback:** Graceful handling of unsupported grammars.
    11. **Foreign Grammar Whitelist:** Explicit knowledge of common tongues.
    12. **Visual Confirmation:** Logs result keys for integrity verification.
    """

    def __init__(self, engine):
        self.engine = engine
        self.logger = Scribe("AnalysisOrchestrator")
        # [ASCENSION 3]: SENTINEL INJECTION
        self.sentinel = SentinelConduit()
        self.scaffold_proc = ScaffoldProcessor(engine, self.logger)
        self.foreign_proc = ForeignProcessor(engine, self.logger)

    def conduct(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        """
        The Rite of Dispatch.
        """
        start_time = time.perf_counter()

        # [ASCENSION 4]: GRAMMAR NORMALIZATION
        raw_grammar = ctx.get('grammar', 'unknown')
        grammar = str(raw_grammar).lower().strip()
        ctx['grammar'] = grammar

        # [ASCENSION 7]: TRACE ID PROPAGATION
        trace_id = ctx.get('telemetry', {}).get('trace_id') or f"orch-{uuid.uuid4().hex[:6]}"

        # [ASCENSION 1]: FORENSIC ROUTING LOG
        # We use stderr to bypass Daemon log filters
        sys.stderr.write(f"[{trace_id}] [Orchestrator] 🎼 Conducting Analysis for: {ctx.get('file_path')}\n")
        sys.stderr.write(f"[{trace_id}] [Orchestrator]    Grammar: {grammar}\n")

        # [ASCENSION 3]: SENTINEL INJECTION
        ctx['sentinel_conduit'] = self.sentinel

        result = {}

        try:
            # [ASCENSION 9]: BIMODAL DISPATCH
            if grammar in ("scaffold", "symphony", "arch"):
                sys.stderr.write(f"[{trace_id}] [Orchestrator]    -> Route: NATIVE (ScaffoldProcessor)\n")
                result = self.scaffold_proc.process(ctx)

            elif self.sentinel.sentinel_path or grammar in self._get_foreign_grammars():
                sys.stderr.write(f"[{trace_id}] [Orchestrator]    -> Route: FOREIGN (Sentinel/ForeignProcessor)\n")
                result = self.foreign_proc.process(ctx)

            else:
                # [ASCENSION 10]: THE VOID FALLBACK
                sys.stderr.write(f"[{trace_id}] [Orchestrator]    -> Route: VOID (Unsupported Grammar)\n")
                result = {
                    "structure": [],
                    "ascii_tree": f"(Unsupported Grammar: {grammar})",
                    "diagnostics": [],
                    "metrics": {"status": "skipped", "reason": "unsupported_grammar"}
                }

        except Exception as e:
            # [ASCENSION 5]: FAULT TOLERANCE
            sys.stderr.write(f"[{trace_id}] [Orchestrator] 💥 Processor Fracture: {e}\n")
            import traceback
            traceback.print_exc(file=sys.stderr)

            result = {
                "structure": [],
                "ascii_tree": "(Processor Crashed)",
                "diagnostics": [{
                    "message": f"Analysis Processor Failed: {str(e)}",
                    "severity": 1,
                    "source": "AnalysisOrchestrator",
                    "code": "PROCESSOR_CRASH"
                }],
                "metrics": {"status": "error", "error": str(e)}
            }

        # [ASCENSION 2]: CHRONOMETRIC GUARD
        duration = (time.perf_counter() - start_time) * 1000

        # [ASCENSION 6 & 8]: RESULT STANDARDIZATION & ENRICHMENT
        if not isinstance(result, dict):
            sys.stderr.write(f"[{trace_id}] [Orchestrator] ⚠️ Invalid Result Type: {type(result)}. Forcing Dict.\n")
            result = {}

        result.setdefault('metrics', {})
        result['metrics']['orchestrator_ms'] = duration
        result['metrics']['trace_id'] = trace_id

        # [ASCENSION 12]: VISUAL CONFIRMATION
        keys_preview = list(result.keys())
        sys.stderr.write(f"[{trace_id}] [Orchestrator] 🏁 Concluded in {duration:.2f}ms. Output Keys: {keys_preview}\n")

        return result

    def _get_foreign_grammars(self) -> Set[str]:
        """
        [ASCENSION 11]: FOREIGN GRAMMAR WHITELIST
        Defines what the ForeignProcessor can attempt to handle even if Sentinel is questionable.
        """
        return {
            "python", "javascript", "typescript", "rust", "go",
            "json", "yaml", "toml", "dockerfile", "bash", "sh", "c", "cpp"
        }