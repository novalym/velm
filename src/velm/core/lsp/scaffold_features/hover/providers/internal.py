# Path: core/lsp/scaffold_features/hover/providers/internal.py
# ------------------------------------------------------------
# LIF: INFINITY | ROLE: INTERNAL_GNOSTIC_SCRYER | RANK: SOVEREIGN
# auth_code: Ω_INTERNAL_ARTISAN_ACCESS_V100_TITANIUM

import logging
import time
import uuid
from typing import Optional, Any, Dict, Union
from pathlib import Path

# --- CORE UPLINKS ---
from ....base.features.hover.contracts import HoverProvider, HoverContext
from ....base.utils.uri import UriUtils
from ....base.telemetry import forensic_log
from ....base.state import ServerState

# [ASCENSION 1]: DIRECT SOUL COUPLING
# We reach into the artisans and pull the soul directly into the LSP process.
# This bypasses the serialization overhead of JSON-RPC for internal calls.
from ......artisans.hover.hierophant import HoverArtisan
from ......interfaces.requests import HoverRequest

Logger = logging.getLogger("InternalHoverProvider")


class InternalHoverProvider(HoverProvider):
    """
    =============================================================================
    == THE INTERNAL ARTISAN PROVIDER (V-Ω-ZERO-LATENCY-SINGULARITY)            ==
    =============================================================================
    Directly executes the HoverArtisan within the Oracle process.
    Annihilates the IPC gap and serves as the Single Source of Truth for Hovers.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Direct Memory Coupling:** Bypasses TCP/Socket layers. 0ms transport overhead.
    2.  **Shared Engine Soul:** Pass the LSP's living `ScaffoldEngine` instance
        directly to the Artisan, ensuring perfect state synchronization.
    3.  **Atomic Request Synthesis:** Uses `HoverRequest.model_validate` to forge
        the plea with strict Pydantic V2 validation.
    4.  **Titanium Path Suture:** Uses `UriUtils.to_fs_path` to guarantee the
        Artisan gazes at the correct physical coordinate.
    5.  **Context Preservation:** Carries the full `HoverContext` (including
        unsaved "dirty" content) into the Artisan's Gaze.
    6.  **ScaffoldResult Extraction:** Surgically extracts the Markdown payload
        from the `ScaffoldResult` vessel.
    7.  **Fault Sarcophagus:** Wraps the local execution in a try/catch block
        to prevent logic-gaps from crashing the Inquisitor.
    8.  **Lazy Initialization:** Instantiates the Artisan only once and preserves
        its state for subsequent gaze requests.
    9.  **Verbosity Passthrough:** Inherits the Architect's requested gnosis-depth.
    10. **Telemetry Mirroring:** Logs internal execution time for performance audit.
    11. **Type-Safe Ingress:** Strictly adheres to the `BaseArtisan` contract.
    12. **Metabolic Guard:** Checks Server State before execution to prevent
        zombie logic during shutdown.
    """

    def __init__(self, server: Any):
        self.server = server
        self._artisan: Optional[HoverArtisan] = None
        # [ASCENSION 12]: Identity Marker
        self._instance_id = f"prov-{uuid.uuid4().hex[:6]}"

    @property
    def name(self) -> str:
        return "HoverArtisan-Internal"

    @property
    def priority(self) -> int:
        # High priority: We want the Artisan's deep Gnosis to lead the revelation.
        return 95

    def _get_artisan(self) -> HoverArtisan:
        """
        [RITE]: MATERIALIZE_ARTISAN
        Lazy-loads the Artisan to ensure the Engine is fully warm before first use.
        """
        if self._artisan is None:
            # We pass the server's already-warmed engine to the artisan
            self._artisan = HoverArtisan(self.server.engine)
        return self._artisan

    def provide(self, ctx: HoverContext) -> Optional[str]:
        """
        [THE RITE OF INTERNAL SCRYING]
        """
        start_ns = time.perf_counter_ns()
        trace_id = ctx.trace_id or f"hov-{uuid.uuid4().hex[:6]}"

        # [ASCENSION 12]: METABOLIC GUARD
        # Do not speak if the server is dying.
        if getattr(self.server, 'state', None) == ServerState.VOID:
            return None

        try:
            # 1. DIVINE PHYSICAL COORDINATES
            # Convert URI to absolute OS path
            fs_path = str(UriUtils.to_fs_path(ctx.uri))

            # [ASCENSION 4]: ROOT RESOLUTION
            # Ensure we have a valid project root anchor
            project_root = str(self.server.project_root) if self.server.project_root else "."

            # 2. FORGE THE PLEA
            # [ASCENSION 3]: Transmute context into a strict Artisan Plea
            request_data = {
                "file_path": fs_path,
                "content": ctx.full_content,
                "position": {
                    "line": ctx.position['line'],
                    "character": ctx.position['character']
                },
                "project_root": project_root,
                "metadata": {
                    "source": "LSP_INTERNAL_SCRY",
                    "trace_id": trace_id,
                    "token": ctx.word,
                    "provider_id": self._instance_id
                }
            }

            request = HoverRequest.model_validate(request_data)

            # 3. [THE SINGULARITY]: DIRECT EXECUTION
            # No sockets. No JSON-RPC overhead. Just pure Python logic.
            artisan = self._get_artisan()
            result = artisan.execute(request)

            # 4. TELEMETRY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            # Only log slow hovers (>50ms) to avoid log spam
            if duration_ms > 50:
                forensic_log(
                    f"Hover Scry: {ctx.word} in {duration_ms:.2f}ms",
                    "INFO", "INTERNAL_HOVER", trace_id=trace_id
                )

            # 5. REVELATION EXTRACTION
            if result.success and result.data:
                return self._extract_payload(result.data, result.message)

            return None

        except Exception as fracture:
            # [ASCENSION 7]: FAULT ISOLATION
            # We log the error but return None so the Editor doesn't crash
            forensic_log(f"Internal Artisan Fracture: {fracture}", "ERROR", "HOVER", exc=fracture, trace_id=trace_id)
            return None

    def _extract_payload(self, data: Union[Dict, Any], message: str) -> Optional[str]:
        """
        [THE PURIFIER]
        Extracts the markdown content from the Artisan's result.
        Prioritizes structured data over the raw message.
        """
        if isinstance(data, dict):
            # [ASCENSION 6]: PRIORITY FIELD EXTRACTION
            # The HoverArtisan puts the markdown in 'contents'
            if 'contents' in data and data['contents']:
                return str(data['contents'])

            # Fallback to legacy fields if present
            if 'markdown' in data:
                return str(data['markdown'])

        # Fallback to the message if it looks like content (and isn't just "Success")
        if message and "Success" not in message and len(message) > 20:
            return message

        return None