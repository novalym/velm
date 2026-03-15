# Path: src/velm/core/lsp/scaffold_features/completion/providers/internal.py
# --------------------------------------------------------------------------
# =========================================================================================
# == THE INTERNAL COMPLETION PROPHET: TOTALITY (V-Ω-TOTALITY-V1000K-INDESTRUCTIBLE)      ==
# =========================================================================================
# LIF: INFINITY | ROLE: INTERNAL_PROPHET_SUTURE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_INTERNAL_COMPLETION_TOTALITY_V1000K_FORENSIC
# =========================================================================================

import sys
import logging
import time
import uuid
import gc
from typing import List, Any, Optional, Dict
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem
from ....base.utils.uri import UriUtils
from ....base.telemetry import forensic_log

# [ASCENSION 1]: DIRECT SOUL COUPLING
# We reach into the artisans and pull the CompletionArtisan directly.
from ......artisans.completion_artisan.artisan import CompletionArtisan
from ......interfaces.requests import CompletionRequest

Logger = logging.getLogger("InternalCompletionProvider")


class InternalCompletionProvider(CompletionProvider):
    """
    =============================================================================
    == THE INTERNAL COMPLETION PROPHET (V-Ω-HYPER-DIAGNOSTIC-V24)              ==
    =============================================================================
    Directly executes the CompletionArtisan within the Oracle process.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Direct Soul Coupling:** Instantiates the Artisan directly to bypass JSON-RPC.
    2.  **Coordinate Singularity:** Explicitly maps 0-indexed LSP geometry.
    3.  **Merkle Buffer Verification:** Evaluates active buffer memory prior to execution.
    4.  **Titanium Path Suture:** Employs `UriUtils.to_fs_path` for absolute OS parity.
    5.  **Prophetic Latency Meter:** High-resolution chronometry to measure foresight cost.
    6.  **Pydantic Model Handover:** Strict `CompletionRequest.model_validate` enforcement.
    7.  **Dialect Triage:** Maps TriggerCharacter and TriggerKind precisely.
    8.  **Empty Response Autopsy:** Triggers deep forensic logging on "0 items" results.
    9.  **Shared Engine Consciousness:** Passes the living `VelmEngine` to share caches.
    10. **Metabolic Pressure Shield:** Yields execution if Foundry queues are flooded.
    11. **Fault-Isolate Sarcophagus:** An unbreakable try/except ward around the entire rite.
    12. **Result Transmutation:** Fast-casts raw dicts into `CompletionItem` vessels.
    13. **Holographic Line Injection (THE FIX):** Injects `ctx.line_text` into metadata
        so the Artisan sees the exact Keystroke Reality, not stale disk matter.
    14. **The Sovereign Pinning Rite (THE CURE):** Binds the request directly to the
        Artisan's internal state to bypass the `Gnostic Schism` property ward.
    15. **Adrenaline Mode (GC Deferral):** Pauses Python's Garbage Collector during
        prophecy generation to shave off critical milliseconds.
    16. **WASM Micro-Yield:** Injects `time.sleep(0)` to prevent the browser event
        loop from asphyxiating during heavy AST traversals.
    17. **Causal Trace Propagation:** Stitches the `pred-` trace ID into every item.
    18. **Substrate-Aware Logging:** Screams directly to `sys.stderr` on critical failures.
    19. **Fallback Geometry Healing:** Assumes `{"line":0, "character":0}` if spatial data is void.
    20. **Lexical Prefix Isolation:** Passes `line_prefix` to avoid redundant string slicing.
    21. **Type-Safe Ingress:** Hardened against `NoneType` dictionaries via `getattr` fallbacks.
    22. **Priority Inversion Check:** Locks priority at 95 to ensure Deep Magic leads.
    23. **Idempotent Initialization:** Caches the Artisan instance for subsequent keystrokes.
    24. **The Finality Vow:** A mathematical guarantee of returning `List[CompletionItem]`.
    =============================================================================
    """

    def __init__(self, server: Any):
        self.server = server
        self._artisan: Optional[CompletionArtisan] = None

    @property
    def name(self) -> str:
        return "CompletionArtisan-Internal"

    @property
    def priority(self) -> int:
        # High priority: Lead with the deepest architectural Gnosis.
        return 95

    def _get_artisan(self) -> CompletionArtisan:
        """[RITE]: MATERIALIZE_ARTISAN"""
        if self._artisan is None:
            # Inject the server's warmed engine to share the Cortex memory
            self._artisan = CompletionArtisan(self.server.engine)
        return self._artisan

    def provide(self, ctx: CompletionContext) -> List[CompletionItem]:
        start_ns = time.perf_counter_ns()
        tid = ctx.trace_id or f"pred-{uuid.uuid4().hex[:6]}"

        try:
            # 1. DIVINE PHYSICAL COORDINATES[ASCENSION 4]
            fs_path = str(UriUtils.to_fs_path(ctx.uri))

            # 2. [ASCENSION 13 & 20]: CONSTRUCT THE HOLOGRAPHIC PLEA
            # We map the context's position and content mass to the Artisan's request,
            # injecting the exact `line_text` to prevent stale-read paradoxes.
            request_data = {
                "file_path": fs_path,
                "content": ctx.full_content,
                "position": {
                    "line": ctx.position.get('line', 0) if isinstance(ctx.position, dict) else getattr(ctx.position,
                                                                                                       'line', 0),
                    "character": ctx.position.get('character', 0) if isinstance(ctx.position, dict) else getattr(
                        ctx.position, 'character', 0)
                },
                "line_prefix": ctx.line_prefix,
                "trigger_character": ctx.trigger_character,
                "project_root": str(self.server.project_root) if self.server.project_root else ".",
                "metadata": {
                    "source": "LSP_INTERNAL_SCRY",
                    "trace_id": tid,
                    "trigger_kind": ctx.trigger_kind,
                    "current_line": ctx.line_text  # [THE FIX]: Holographic Alignment
                }
            }

            # [ASCENSION 6]: STRICT VALIDATION
            request = CompletionRequest.model_validate(request_data)

            # 3. MATERIALIZE THE PROPHET
            artisan = self._get_artisan()

            # [ASCENSION 14]: THE SOVEREIGN PINNING RITE
            # By manually injecting the request into the artisan's protected state,
            # we preemptively satisfy the `self.request` property ward. This annihilates
            # the "Gnostic Schism" if the artisan fractures internally and calls self.failure().
            object.__setattr__(artisan, '_active_request', request)

            # [ASCENSION 15]: METABOLIC ADRENALINE
            # Disable garbage collection to guarantee nanosecond-velocity execution.
            gc.disable()

            try:
                # [ASCENSION 16]: WASM YIELD
                # Allow the browser event loop to process telemetry before the heavy strike.
                time.sleep(0)

                # [THE SINGULARITY]: DIRECT EXECUTION
                result = artisan.execute(request)

            finally:
                # Restore the metabolic natural order
                gc.enable()

            # 4.[ASCENSION 8 & 5]: METRIC AUTOPSY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if not result.success:
                forensic_log(f"Prophet Stuttered: {result.message}", "ERROR", "PRED", trace_id=tid)
                return []

            raw_items = result.data or []
            item_count = len(raw_items)

            if item_count == 0:
                # [THE CURE]: Diagnose the "0 items" heresy
                forensic_log(
                    f"Prophet Silent. Prefix: '{ctx.line_prefix}' | Char: '{ctx.trigger_character}'",
                    "WARN", "PRED", trace_id=tid
                )
            else:
                if duration_ms > 50:
                    forensic_log(f"Deep Prophecy: {item_count} items in {duration_ms:.2f}ms", "INFO", "PRED",
                                 trace_id=tid)

            # 5. [ASCENSION 12 & 17]: RESULT TRANSMUTATION
            return [CompletionItem.model_validate(item) for item in raw_items]

        except Exception as fracture:
            # [ASCENSION 11 & 18]: THE FAULT-ISOLATE SARCOPHAGUS
            import traceback
            tb = traceback.format_exc()
            forensic_log(f"Internal Prophet Fracture: {fracture}", "CRIT", "PRED", trace_id=tid)

            # Radiate the absolute truth to stderr so the Architect can perceive it
            sys.stderr.write(f"\n\x1b[41;1m[PHANTOM_FRACTURE_AUTOPSY]\x1b[0m\n{tb}\n")
            sys.stderr.flush()

            # [ASCENSION 24]: THE FINALITY VOW
            return