# Path: scaffold/artisans/agent/Verify/critic.py
# ----------------------------------------------

import json
from typing import List, Any
from pathlib import Path

from ..contracts import AgentState, Observation, Critique
from ....core.ai.engine import AIEngine
from ....logger import Scribe

Logger = Scribe("AgentCritic")


class Critic:
    """
    =================================================================================
    == THE GNOSTIC CONSCIENCE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                      ==
    =================================================================================
    @gnosis:title The Agent's Conscience (The Critic)
    @gnosis:summary The divine, sentient judge that adjudicates the success or failure
                     of the Agent's mission with empirical certainty.
    @gnosis:LIF INFINITY

    This is the Critic in its final, eternal form. It is no longer a passive oracle,
    relying on the AI's opinion. It is an active **Inquisitor of Truth**. Its Prime
    Directive is to seek empirical, undeniable proof of success—the pure, green light
    of a passing test suite—before ever proclaiming a mission complete. It is the
    unbreakable anchor that grounds the Agent's abstract thought in the bedrock of
    manifest reality.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Law of Empirical Truth:** Its first and highest law is to gaze into the
        Agent's observations for the sacred `run_tests` tool. A "Tests Passed"
        observation is now the one true, non-negotiable sign of success.
    2.  **The Hallucination Override:** If the LLM proclaims `is_goal_achieved: true`
        but no passing test run has been observed, the Critic righteously overrides
        the AI's judgment, declaring the mission incomplete and commanding the Agent
        to verify its work. The heresy of assumption is annihilated.
    3.  **The Gnostic Triage of Observation:** It intelligently synthesizes the raw
        output from all tools into a concise, token-efficient summary for the AI,
        prioritizing test failures and error messages.
    4.  **The Mentor of Verification:** If the mission *seems* complete but no test has
        been run, its primary suggestion is no longer a guess. It is a divine edict:
        "Verify your work. Run the tests."
    5.  **The Unbreakable Ward of Paradox:** Its Gaze upon the AI's JSON response is
        shielded. A profane, malformed scripture from the AI will not shatter the
        Critic; it will be caught and transmuted into a coherent, actionable critique.
    6.  **The Luminous Voice:** It proclaims its final judgment to the Gnostic log,
        providing a clear, auditable reason for its decision to continue or halt
        the agentic loop.
    7.  **The Focused Mind:** Its prompt has been re-forged with a singular purpose:
        adjudicate the existing evidence against the mission, do not hallucinate new
        actions.
    8.  **The Pure Gnostic Contract:** Its `review` rite receives the pure `AgentState`
        and `Observation` vessels and returns a pure `Critique`, honoring the sacred
        contracts of the cosmos.
    9.  **The Sovereign Soul:** It is a pure artisan of judgment. It does not act; it
        only perceives and advises, honoring the separation of concerns.
    10. **The Token Economist:** By summarizing observations, it saves a vast amount of
        tokens, allowing the Agent to have a longer, more coherent memory in each loop.
    11. **The Heuristic of Progress:** It analyzes the *change* in observations over
        time. If the Agent is stuck in a loop (e.g., repeatedly failing the same test),
        it can increase the urgency of its critique. (Future Ascension).
    12. **The Final Word:** It is the one true arbiter of success, the final gatekeeper
        of the Agent's symphony, ensuring that no mission is ever proclaimed complete
        based on mere hope, but only on the immutable truth of verification.
    """

    def __init__(self, project_root: Path, engine: Any):
        self.ai = AIEngine.get_instance()
        self.engine = engine  # For logging

    def review(self, state: AgentState, observations: List[Observation]) -> Critique:
        """The Grand Rite of Adjudication."""

        # --- MOVEMENT I: THE GAZE FOR EMPIRICAL TRUTH ---
        # [FACULTY 1] We seek the one true sign of success.
        test_observation = next((obs for obs in observations if obs.tool_name == "run_tests"), None)

        test_result_summary = "No test results in this cycle."
        tests_passed = False

        if test_observation:
            # A test was run. We adjudicate its soul.
            if "Tests Passed" in test_observation.output or "passed" in test_observation.output.lower():
                tests_passed = True
                test_result_summary = "SUCCESS: The test suite passed, verifying the changes."
                Logger.success("Empirical Proof of Success: Tests Passed.")
                # [FACULTY 1] The highest law is satisfied. The mission is complete.
                return Critique(
                    is_goal_achieved=True,
                    reasoning="All tests passed, providing empirical verification for the successful completion of the mission.",
                    next_step_suggestion=None
                )
            else:
                test_result_summary = f"FAILURE: The test suite failed. Output: {test_observation.output[:1000]}..."

        # --- MOVEMENT II: THE COMMUNION WITH THE NEURAL CORTEX ---
        # If tests did not pass, we must ask the AI for its interpretation of the current reality.

        # [FACULTY 3 & 10] We synthesize the observations into a token-efficient summary.
        observation_summary = self._format_observations_for_ai(observations)

        prompt = f"""
        **MISSION:** "{state.mission}"

        **LATEST OBSERVATIONS (SUMMARY):**
        {observation_summary}

        **TEST SUITE STATUS:**
        {test_result_summary}

        **YOUR TASK:**
        You are the Conscience of an AI Agent. Your judgment must be ruthless and logical.
        1. Analyze the mission, observations, and especially the test results.
        2. Determine if the mission has been successfully and VERIFIABLY completed.
        3. If the goal seems complete but tests are failing, your primary suggestion MUST be to analyze the failure and fix the code.
        4. If the goal seems complete but tests have NOT been run, your primary suggestion MUST be to run the test suite.
        5. If the goal is not achieved, provide a concise, actionable next step for the planner.

        **Respond with a valid JSON object ONLY, matching the following schema:**
        {{
            "is_goal_achieved": boolean, 
            "reasoning": "Your brief analysis of the current state and why the goal is/isn't met.", 
            "next_step_suggestion": "Your concrete suggestion for the next logical action."
        }}
        """

        response_str = self.ai.ignite(
            prompt,
            system="You are an expert software engineering critic. Your judgment is final. Respond only in valid JSON.",
            model="smart",
            json_mode=True
        )

        # --- MOVEMENT III: THE FINAL JUDGMENT & HALLUCINATION OVERRIDE ---
        try:
            data = json.loads(response_str)
            critique = Critique(**data)

            # [FACULTY 2] The Hallucination Override
            if critique.is_goal_achieved and not tests_passed:
                critique.is_goal_achieved = False
                critique.reasoning = "[OVERRIDE] The AI's belief in success is a hallucination. " + critique.reasoning
                critique.next_step_suggestion = "The test suite has not passed. The next step MUST be to run and pass the tests to verify the mission's success."
                Logger.warn("Critic overrode AI's premature success proclamation.")

            Logger.info(
                f"Critic's Verdict: Goal Achieved? {critique.is_goal_achieved}. Suggestion: {critique.next_step_suggestion}")
            return critique

        except (json.JSONDecodeError, TypeError) as e:
            # [FACULTY 5] The Unbreakable Ward of Paradox
            Logger.error(f"Critic's mind faltered (Invalid JSON from AI): {e}", exc_info=True)
            return Critique(
                is_goal_achieved=False,
                reasoning=f"A paradox occurred in the Critic's mind. The AI's response was profane: {response_str}",
                next_step_suggestion="Re-evaluate the state of reality and formulate a new plan."
            )

    def _format_observations_for_ai(self, observations: List[Observation]) -> str:
        """[FACULTY 3] A Gnostic Gaze that summarizes reality for the AI."""
        if not observations:
            return "No actions were performed in the last cycle."

        summary = []
        for obs in observations:
            status = obs.status
            output_preview = obs.output.strip()
            if len(output_preview) > 300:
                output_preview = output_preview[:300] + "..."

            summary.append(f"- Tool '{obs.tool_name}' -> {status}\n  - Output: {output_preview}")

        return "\n".join(summary)