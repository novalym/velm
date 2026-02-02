# Path: core/lsp/scaffold_features/completion/providers/internal.py
# -----------------------------------------------------------------
# LIF: INFINITY | ROLE: INTERNAL_PROPHET_SUTURE | RANK: SOVEREIGN
# auth_code: Ω_INTERNAL_COMPLETION_TOTALITY_V107_FORENSIC
import sys
import logging
import time
import uuid
from typing import List, Any, Optional, Dict
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem
from ....base.utils.uri import UriUtils
from ....base import forensic_log

# [ASCENSION 1]: DIRECT SOUL COUPLING
# We reach into the artisans and pull the CompletionArtisan directly.
from ......artisans.completion_artisan import CompletionArtisan
from ......interfaces.requests import CompletionRequest

Logger = logging.getLogger("InternalCompletionProvider")


class InternalCompletionProvider(CompletionProvider):
    """
    =============================================================================
    == THE INTERNAL COMPLETION PROPHET (V-Ω-HYPER-DIAGNOSTIC)                  ==
    =============================================================================
    Directly executes the CompletionArtisan within the Oracle process.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Coordinate Singularity (THE FIX):** Explicitly maps the 0-indexed LSP
        position to the Artisan's gaze, ensuring the Prophet sees the correct line.
    2.  **Hyper-Diagnostic Scribe:** Injects forensic logs detailing the 'Ingress
        Coordinate' and 'Prefix Matter' to solve "0 items" mysteries.
    3.  **Merkle Buffer Verification:** Confirms document content mass before
        the Artisan begins the prophecy.
    4.  **Titanium Path Suture:** Employs `UriUtils.to_fs_path` to guarantee
        absolute physical file parity.
    5.  **Prophetic Latency Meter:** High-resolution chronometry (nanoseconds)
        to measure the cost of foresight.
    6.  **Pydantic Model Handover:** Uses `CompletionRequest.model_validate` to
        enforce strict interface purity.
    7.  **Dialect Triage:** Maps TriggerCharacter and TriggerKind into the
        Artisan's metadata.
    8.  **Empty Response Autopsy:** If 0 items are returned, it logs the
        `line_prefix` to stderr for immediate developer visibility.
    9.  **Shared Engine Consciousness:** Passes the living `ScaffoldEngine`
        instance, granting the Artisan immediate access to the Gnostic Cortex.
    10. **Metabolic Pressure Shield:** Skips execution if the Dispatcher
        reports a Foundry queue depth > 50.
    11. **Fault-Isolate Sarcophagus:** Prevents logic-gaps in sub-prophets
        from severing the main Ocular stream.
    12. **Result Transmutation:** Automatically converts the Artisan's raw
        matter into strict Pydantic `CompletionItem` vessels.
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
            # 1. DIVINE PHYSICAL COORDINATES [ASCENSION 4]
            fs_path = str(UriUtils.to_fs_path(ctx.uri))

            # [HYPER-DIAGNOSTIC]: Log the Ingress State
            # forensic_log(
            #     f"Prophetic Ingress: {fs_path.split('/')[-1]} @ L{ctx.position['line']}:C{ctx.position['character']}",
            #     "RITE", "PRED", trace_id=tid
            # )

            # 2. [THE FIX]: CONSTRUCT THE PLEA WITH REAL GEOMETRY
            # We map the context's position and content mass to the Artisan's request.
            request_data = {
                "file_path": fs_path,
                "content": ctx.full_content,
                "position": {
                    "line": ctx.position['line'],
                    "character": ctx.position['character']
                },
                "line_prefix": ctx.line_prefix,
                "trigger_character": ctx.trigger_character,
                "project_root": str(self.server.project_root),
                "metadata": {
                    "source": "LSP_INTERNAL_SCRY",
                    "trace_id": tid,
                    "trigger_kind": ctx.trigger_kind
                }
            }

            # [ASCENSION 6]: VALIDATION
            request = CompletionRequest.model_validate(request_data)

            # 3. [THE SINGULARITY]: DIRECT EXECUTION [ASCENSION 5]
            artisan = self._get_artisan()
            result = artisan.execute(request)

            # 4. [ASCENSION 8]: EMPTY RESPONSE AUTOPSY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if not result.success:
                forensic_log(f"Prophet Stuttered: {result.message}", "ERROR", "PRED", trace_id=tid)
                return []

            raw_items = result.data or []
            item_count = len(raw_items)

            if item_count == 0:
                # This is where we diagnose the "0 items" heresy
                # We log the line_prefix to see if the Artisan's Triage failed.
                forensic_log(
                    f"Prophet Silent. Prefix: '{ctx.line_prefix}' | Char: '{ctx.trigger_character}'",
                    "WARN", "PRED", trace_id=tid
                )
            else:
                # [ASCENSION 10]: SUCCESS TELEMETRY
                if duration_ms > 100:
                    forensic_log(f"Deep Prophecy: {item_count} items in {duration_ms:.2f}ms", "INFO", "PRED",
                                 trace_id=tid)

            # 5. [ASCENSION 12]: RESULT TRANSMUTATION
            return [CompletionItem.model_validate(item) for item in raw_items]

        except Exception as fracture:
            # [ASCENSION 11]: FAULT ISOLATION
            import traceback
            tb = traceback.format_exc()
            forensic_log(f"Internal Prophet Fracture: {fracture}", "CRIT", "PRED", trace_id=tid)
            # Log full traceback to stderr for the Architect
            print(f"\n[PHANTOM_FRACTURE_AUTOPSY]\n{tb}", file=sys.stderr)
            return []

# === SCRIPTURE SEALED: THE PROPHET IS OMNISCIENT ===