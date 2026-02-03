# Path: artisans/analyze/rites/prophecy.py
# ----------------------------------------

from typing import Dict, Any
from pathlib import Path
from ....interfaces.requests import CompletionRequest, HoverRequest, DefinitionRequest
from ..reporting.diagnostics import DiagnosticForge


class RiteOfProphecy:
    """
    =============================================================================
    == THE RITE OF PROPHECY (V-Ω-LSP-DISPATCH)                                 ==
    =============================================================================
    Preserves the logic of `_rite_of_prophecy`.
    Recursively calls the Engine to summon sub-artisans.
    """

    @staticmethod
    def conduct(
            ctx: Dict[str, Any],
            engine: Any,
            session_id: str
    ) -> Dict[str, Any]:

        content = ctx['content']
        # Transmute offset to Position object
        pos = DiagnosticForge.offset_to_position(content, ctx['cursor_offset'])

        # Ensure URI for LSP compliance
        if isinstance(ctx['file_path'], str):
            file_uri = Path(ctx['file_path']).as_uri()
        else:
            file_uri = ctx['file_path'].as_uri()

        req_data = {
            "file_path": file_uri,
            "content": content,
            "position": pos,
            "project_root": ctx['project_root'],
            "session_id": session_id,
            "grammar": ctx['grammar']
        }

        results = {}

        # We assume the Engine has a ThreadPool (Cortex) we can utilize,
        # OR we dispatch synchronously. To preserve original parallelism logic:

        import concurrent.futures
        # Using a local executor to parallelize the sub-requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(engine.dispatch, CompletionRequest(**req_data)): "completion",
                executor.submit(engine.dispatch, HoverRequest(**req_data)): "hover",
                executor.submit(engine.dispatch, DefinitionRequest(**req_data)): "definition"
            }

            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    res = future.result(timeout=5)
                    if res and res.success:
                        if name == "completion":
                            results["completions"] = res.data or []
                        elif name == "hover":
                            results["hover"] = res.data
                        elif name == "definition":
                            results["definition"] = res.data
                except Exception:
                    # Silence is golden for optional prophecy
                    pass

        return results