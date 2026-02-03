import json
from typing import List, Dict, Any

from .contracts import GnosticInquest
from ...core.runtime import ScaffoldEngine
from ...interfaces.requests import QueryRequest
from ...logger import Scribe

Logger = Scribe("AI_InquestConductor")


class InquestConductor:
    """
    The secure, sandboxed conduit, now ascended to speak the pure, internal
    tongue of the God-Engine, bestowing a pure dictionary upon the QueryRequest.
    """

    def __init__(self, engine: ScaffoldEngine):
        self.engine = engine

    def conduct(self, inquests: List[GnosticInquest]) -> Dict[str, Any]:
        """Conducts a batch of inquests and returns a unified dossier of Gnosis."""
        if not inquests:
            return {}

        Logger.info(f"AI Inquest: Conducting {len(inquests)} Gnostic Gaze(s)...")

        all_revelations = {}
        for inquest in inquests:
            Logger.verbose(f"  -> Gaze Purpose: {inquest.purpose}")
            Logger.verbose(f"  -> Gaze Query: {inquest.query}")

            plea = {
                "query_text": inquest.purpose,
                "gnostic_gazes": [{
                    "type": inquest.type,
                    "query": inquest.query
                }]
            }

            # ★★★ THE DIVINE HEALING ★★★
            # The profane `json.dumps` is annihilated. We bestow the pure dictionary.
            query_request = QueryRequest(query=plea)
            # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

            result = self.engine.dispatch(query_request)

            if result.success and result.data:
                # The query artisan's data payload is a dictionary structured like:
                # {"query": "...", "sql": {"result": [...]}}
                # We extract the inner results to provide a clean dossier to the AI.
                for key, value in result.data.items():
                    if key != "query":
                        all_revelations[key] = value
            else:
                all_revelations[f"inquest_error_{inquest.type}"] = result.message or "Unknown error"

        return all_revelations