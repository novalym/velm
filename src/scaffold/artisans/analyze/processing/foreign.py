# Path: artisans/analyze/processing/foreign.py
# --------------------------------------------

import time
from typing import Dict, Any

from .base import BaseProcessor
from ..reporting.diagnostics import DiagnosticForge


class ForeignProcessor(BaseProcessor):
    """
    =============================================================================
    == THE SENTINEL BRIDGE (V-Ω-FOREIGN-TONGUES)                               ==
    =============================================================================
    Delegates analysis of non-scaffold files (Python, JS, Rust) to the Sentinel.
    """

    def process(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        # Unwrap Context
        content = ctx['content']
        file_path = ctx['file_path']
        grammar = ctx['grammar']
        telemetry = ctx['telemetry']

        # 1. Sentinel Adjudication
        start = time.monotonic()
        # Access sentinel via the artisan instance (passed via engine or parent)
        # We assume the orchestrator set this up
        sentinel_conduit = ctx['sentinel_conduit']

        heresies = []
        try:
            # file_path proxy for language detection in sentinel
            heresies = sentinel_conduit.adjudicate(Path(grammar), content)
        except Exception as e:
            self.logger.error(f"Sentinel Fracture: {e}")

        telemetry['sentinel_ms'] = (time.monotonic() - start) * 1000

        # 2. Format
        diagnostics = []
        for h in heresies:
            diagnostics.append({
                "message": h.message,
                "severity": 1 if h.severity.name == "CRITICAL" else 2,
                "internal_line": max(0, h.line_num - 1),
                "source": f"Sentinel:{grammar}",
                "details": h.details,
                "suggestion": h.suggestion,
                "code": "FOREIGN"
            })

        # 3. Internal Prophecy (Completion/Hover for foreign files if supported)
        # (This logic is identical to scaffold processor prophecy, omitted for brevity but should be included if desired)

        return {
            "structure": [],
            "ascii_tree": f"(Sentinel Analysis: {grammar})",
            "completions": [],
            "hover": None,
            "definition": None,
            "diagnostics": DiagnosticForge.format_diagnostics(diagnostics, content),
            "symbols": [],
            "content": content,
            "metrics": telemetry
        }