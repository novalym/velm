import json
import re
from typing import Tuple, Optional

from .contracts import AIThoughtProcess, GnosticInquest, AIBlueprint
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("AI_Planner")


class GnosticPlanner:
    """
    =================================================================================
    == THE GNOSTIC PLANNER (V-Ω-RESILIENT-APOTHEOSIS)                              ==
    =================================================================================
    The strategic mind of the Gnostic Architect, now ascended with the **Gaze of
    Forgiveness**. It no longer trusts the AI's scripture blindly. It performs a
    surgical, brace-counting Gaze to extract the pure JSON soul from within any
    profane noise, rendering it immune to the chaotic whispers of lesser AI minds.
    =================================================================================
    """
    PLAN_PATTERN = re.compile(r'\[PLAN:\s*({)', re.DOTALL)

    def _extract_plan_json(self, text: str) -> Optional[str]:
        """
        [THE GAZE OF FORGIVENESS]
        Performs a brace-counting search to find the one true JSON object.
        """
        match = self.PLAN_PATTERN.search(text)
        if not match:
            return None

        start_index = match.start(1)  # The index of the opening '{'
        brace_count = 1
        for i in range(start_index + 1, len(text)):
            char = text[i]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1

            if brace_count == 0:
                # We found the matching brace. The JSON object is from start_index to i.
                return text[start_index: i + 1]

        return None  # Unmatched braces

    def divine_plan(self, raw_ai_response: str) -> Tuple[AIThoughtProcess, str]:
        """
        Performs a Gaze upon the AI's raw output to extract the plan.
        Returns the structured plan and the remaining content (the final output).
        """
        Logger.verbose("The Planner awakens its Gaze to perceive the AI's will...")

        plan_json_str = self._extract_plan_json(raw_ai_response)

        if plan_json_str:
            try:
                plan_data = json.loads(plan_json_str)
                plan = AIThoughtProcess.model_validate(plan_data)

                # The final output is everything *after* the extracted JSON.
                # Find the end index of our extracted JSON and slice from there.
                end_index = raw_ai_response.find(plan_json_str) + len(plan_json_str)
                # We need to find the closing bracket of the [PLAN: ...] block
                closing_bracket_index = raw_ai_response.find(']', end_index)
                if closing_bracket_index != -1:
                    end_index = closing_bracket_index + 1

                remaining_content = raw_ai_response[end_index:].strip()
                Logger.success("Perceived and purified a structured Gnostic Plan.")
                return plan, remaining_content
            except (json.JSONDecodeError, Exception) as e:
                raise ArtisanHeresy(f"AI spoke a profane plan, even after purification: {e}")

        # Fallback: No plan detected. Assume the entire output is the final answer.
        Logger.verbose("No Gnostic Plan perceived. Assuming a direct proclamation.")
        is_blueprint = "::" in raw_ai_response or "+=" in raw_ai_response or "$$" in raw_ai_response
        plan = AIThoughtProcess(
            reasoning="Direct response to user's plea.",
            inquests=[],
            final_output_type="blueprint" if is_blueprint else "markdown"
        )
        return plan, raw_ai_response