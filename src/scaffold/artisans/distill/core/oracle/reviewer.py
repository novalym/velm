# === [scaffold/artisans/distill/core/oracle/reviewer.py] - SECTION 1 of 1: The Socratic Reviewer ===
import json
from pathlib import Path
from typing import List, Set, Dict, Any

from .contracts import OracleContext
from ..governance.contracts import RepresentationTier
from .....core.ai.engine import AIEngine
from .....logger import Scribe

Logger = Scribe("SocraticReviewer")


class SocraticReviewer:
    """
    =============================================================================
    == THE SOCRATIC REVIEWER (V-Ω-AGENTIC-CRITIC)                              ==
    =============================================================================
    LIF: 100,000,000,000,000

    A self-correcting agent that reviews the Distiller's proposed context.

    The Loop:
    1.  **Observe:** Look at the `governance_plan` (what we plan to include).
    2.  **Reflect:** Ask the AI: "Given intent X and files Y, what is missing?"
    3.  **Verify:** Check if the AI's suggestions actually exist in the Cortex.
    4.  **Refine:** Add valid suggestions to the Seed list for the next pass.
    """

    def __init__(self, root: Path):
        self.root = root
        self.ai = AIEngine.get_instance()

    def review(self, context: OracleContext) -> Set[str]:
        """
        Conducts the Socratic Review.
        Returns a set of NEW file paths (relative strings) to add to the seeds.
        """
        # 1. The Gaze of Prudence (Cost Check)
        if not context.profile.recursive_agent:
            return set()

        if not context.query_intent and not context.profile.feature:
            # If we don't know the intent, we can't critique the context.
            Logger.verbose("Socratic Loop skipped: No intent provided.")
            return set()

        intent = context.profile.feature or "Understand the codebase"

        # 2. Gather the Current Plan
        included_files = [
            str(p).replace('\\', '/')
            for p, tier in context.governance_plan.items()
            if tier != RepresentationTier.EXCLUDED.value
        ]

        if not included_files:
            Logger.warn("The Plan is empty. The Socratic Reviewer cannot critique a void.")
            return set()

        Logger.info(f"Initiating Socratic Review for intent: [cyan]'{intent}'[/cyan]")

        # 3. Forge the Meta-Prompt
        # We give the AI a summary of the current selection.
        prompt = f"""
        You are a Senior Software Architect performing a Code Context Review.

        **User Intent:** "{intent}"

        **Currently Selected Files:**
        {json.dumps(included_files, indent=2)}

        **Task:**
        Identify any CRITICAL missing files that are likely required to fulfill the user's intent but are missing from the list.
        - Look for missing imports, definitions, or configuration files implied by the selected files.
        - Only suggest files that likely exist in a standard project structure.
        - If the selection looks complete, return an empty list.

        **Output Format:**
        Return ONLY a JSON object with a single key "missing_files" containing a list of file paths.
        Example: {{ "missing_files": ["src/utils/auth_helper.py", "config.json"] }}
        """

        system_prompt = "You are a precise code analysis agent. Output valid JSON only."

        try:
            # 4. The Communion
            response = self.ai.ignite(prompt, system_prompt, model="smart", json_mode=True)

            # 5. The Interpretation
            data = json.loads(response)
            suggestions = data.get("missing_files", [])

            if not suggestions:
                Logger.success("The AI Architect approves the current context.")
                return set()

            # 6. The Verification (Grounding)
            # We must ensure the AI isn't hallucinating files.
            valid_additions = set()
            known_files = {str(g.path).replace('\\', '/') for g in context.memory.inventory}

            for sugg in suggestions:
                # Normalize AI suggestion
                sugg_clean = sugg.strip().lstrip('./').replace('\\', '/')

                # Check existence in Gnostic Memory
                if sugg_clean in known_files:
                    if sugg_clean not in included_files:
                        valid_additions.add(sugg_clean)
                else:
                    # Fuzzy match fallback? (Maybe later. For now, strict.)
                    Logger.verbose(f"   -> AI hallucinated/misnamed '{sugg_clean}'. Ignoring.")

            if valid_additions:
                Logger.warn(
                    f"Socratic Review suggests adding {len(valid_additions)} missing scripture(s): {', '.join(list(valid_additions)[:3])}...")
                return valid_additions

            return set()

        except Exception as e:
            Logger.warn(f"The Socratic Loop faltered: {e}")
            return set()