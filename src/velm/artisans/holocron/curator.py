import json
from typing import List, Set
from ...core.ai.engine import AIEngine
from ...logger import Scribe
from .contracts import HolocronCandidate

Logger = Scribe("HolocronCurator")


class AICurator:
    """
    =============================================================================
    == THE GNOSTIC CURATOR (V-Ω-AI-FILTER)                                     ==
    =============================================================================
    Uses the Architect's preferred AI (Local/Cloud) to judge the relevance of
    candidates proposed by the Graph.
    """

    def __init__(self):
        self.ai = AIEngine.get_instance()

    def curate(self, intent: str, candidates: List[HolocronCandidate]) -> List[str]:
        """
        Asks the AI: "Here are 50 files related to the graph. The user wants to
        fix 'Login Bug'. Which ones actully matter?"
        """
        Logger.info(f"Summoning AI ({self.ai.config.model}) to curate {len(candidates)} candidates...")

        # We construct a metadata manifest (Token efficient)
        manifest = [
            {"path": c.path, "reason": c.reason, "summary": c.summary}
            for c in candidates
        ]

        prompt = f"""
        I am building a context for a developer to solve a problem.

        PROBLEM: "{intent}"

        CANDIDATE FILES (Traced via Dependency Graph):
        {json.dumps(manifest, indent=2)}

        TASK:
        Select ONLY the files that are strictly necessary to understand and solve the problem. 
        Exclude boilerplate, generic utils, or unrelated logic.

        OUTPUT:
        A JSON object with a single key "selected_paths" containing the list of file paths.
        """

        system = "You are a Senior Architect optimizing context windows. Be ruthless."

        try:
            response = self.ai.ignite(prompt, system, json_mode=True, model="smart")
            data = json.loads(response)
            selected = data.get("selected_paths", [])

            Logger.success(f"AI Curator selected {len(selected)}/{len(candidates)} high-value scriptures.")
            return selected
        except Exception as e:
            Logger.warn(f"AI Curation faltered ({e}). Falling back to Graph Truth.")
            return [c.path for c in candidates]  # Fail open

