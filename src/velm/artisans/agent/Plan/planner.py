# artisans/agent/Plan/planner.py
import json
from pathlib import Path
from typing import Any
from ..contracts import AgentState, Plan
from .prompt_forge import PromptForge
from ....core.ai.engine import AIEngine
from ....contracts.heresy_contracts import ArtisanHeresy


class Planner:
    """
    The Strategic Mind.
    Consults the Neural Cortex to formulate a plan based on the mission and perception.
    """

    def __init__(self, project_root: Path, engine: Any):
        self.root = project_root
        self.engine = engine
        self.forge = PromptForge()
        self.ai = AIEngine.get_instance()
        # We need to discover tools to teach them to the AI
        # Circular import avoidance: we import tools in execute or init
        from ..Act.executor import Executor
        self.tools = Executor(project_root, engine).registry.values()

    def create_plan(self, state: AgentState, context_blueprint: str) -> Plan:
        """
        Ignites the AI to forge a Plan, with a self-healing retry loop.
        """
        system_prompt = self.forge.forge_system_prompt(list(self.tools))
        user_prompt = self.forge.forge_user_prompt(state, context_blueprint)

        max_retries = 2
        for attempt in range(max_retries):
            response = self.ai.ignite(
                user_query=user_prompt,
                system=system_prompt,
                model="smart",
                json_mode=True
            )

            try:
                # The AI might wrap JSON in markdown blocks, we clean it
                clean_response = response.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response.lstrip("```json").strip()
                if clean_response.endswith("```"):
                    clean_response = clean_response.rstrip("```").strip()

                plan_data = json.loads(clean_response)
                return Plan(**plan_data)
            except (json.JSONDecodeError, ValueError) as e:
                self.engine.logger.warn(f"AI produced profane JSON (Attempt {attempt + 1}/{max_retries}). Heresy: {e}")
                # The Rite of Self-Healing: We tell the AI what it did wrong.
                user_prompt += f"\n\n[CRITIQUE]\nYour previous response was not valid JSON. Heresy: {e}. Please correct your output and respond with ONLY the valid JSON Plan object, without any surrounding text or markdown."
                if attempt == max_retries - 1:
                    raise ArtisanHeresy(f"The AI spoke in tongues after {max_retries} attempts (Invalid JSON Plan): {e}", details=response)

        # This line should not be reachable, but as a failsafe:
        raise ArtisanHeresy("The Planner's mind has faltered. Could not forge a valid plan.")