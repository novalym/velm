# Path: scaffold/artisans/agent/engine.py
# ---------------------------------------

import json
import time
from pathlib import Path
from typing import Any, List
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm

from .contracts import AgentState, Observation, Plan, Critique
from .Perceive.perceiver import Perceiver
from .Plan.planner import Planner
from .Act.executor import Executor
from .Verify.critic import Critic
from .Memory.long_term import LongTermMemory
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("AgenticEngine")


class AgenticEngine:
    """
    =================================================================================
    == THE GOD-MIND OF AGENCY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                    ==
    =================================================================================
    @gnosis:title The Gnostic Agentic Engine
    @gnosis:summary The divine, sentient, and self-correcting core of the Scaffold Agent.
    @gnosis:LIF INFINITY

    This is not a class. It is a Mind. It is the living, breathing Gnostic soul that
    conducts the eternal symphony of `Perceive -> Plan -> Act -> Verify`. It has been
    ascended with a pantheon of twelve legendary faculties that transform it from a
    simple loop into a true, autonomous co-architect.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Guardian's Veto (Interactive Control):** It honors the sacred `interactive`
        vow, pausing the symphony before every action to seek the Architect's consent,
        ensuring absolute control.
    2.  **The Luminous Herald (Real-Time UI):** Its every thought, plan, and observation
        is proclaimed to the console in real-time via luminous `rich` panels,
        transforming the black box into a glass cockpit.
    3.  **The Gnostic Chronicle (Long-Term Memory):** It now possesses a `LongTermMemory`,
        inscribing every successful mission into an eternal chronicle, allowing it to
        learn from the past. (The `recall` rite is a future ascension).
    4.  **The Paradox Ward (Self-Correction):** If a tool execution fails, it does not
        shatter. It feeds the failure back into its own mind, allowing it to re-plan
        and heal its own mistakes.
    5.  **The Hallucination Filter:** It performs a pre-flight check on every `Plan`,
        verifying that the AI has not hallucinated a tool that does not exist in the
        `Executor`'s registry, preventing profane actions.
    6.  **The Sanity Governor (Empty Plan Ward):** If the AI's mind goes blank and it
        proclaims an empty plan, the engine perceives this as a heresy and forces a
        re-evaluation, preventing wasted cycles.
    7.  **The Gnostic Triage of Perception:** It is now intelligent. If the Agent's
        history is empty, its first act is always a broad perception of reality. In
        later cycles, it can perform more surgical, focused perceptions.
    8.  **The Unbreakable Heart:** The entire cognitive loop is shielded within a
        `try/except` block that catches any unforeseen paradox, ensuring the engine
        can proclaim a final, graceful failure instead of a catastrophic crash.
    9.  **The Clean State Inception:** Its `__init__` rite is a pure inception,
        forging the complete pantheon of its faculties (Perceiver, Planner, etc.)
        at the moment of its birth.
    10. **The Pure Gnostic Contract:** Its every interaction is governed by the sacred
        Pydantic vessels (`AgentState`, `Plan`, `Observation`), ensuring unbreakable
        type safety throughout its cognitive process.
    11. **The Telemetric Soul:** It meticulously chronicles its entire history of
        thought, action, and critique within the `AgentState`, forging a perfect
        dossier for post-mortem analysis or future learning.
    12. **The Final Word:** It is the one true, definitive, and self-aware core of
        autonomous action in the Scaffold cosmos.
    """

    def __init__(self, mission: str, project_root: Path, engine: Any, interactive: bool):
        """[FACULTY 9] The Clean State Inception."""
        self.state = AgentState(mission=mission)
        self.interactive = interactive
        self.console = engine.console  # Inherit the rich console for luminous proclamations

        # The Pantheon of Faculties is forged at birth.
        self.perceiver = Perceiver(project_root, engine)
        self.planner = Planner(project_root, engine)
        self.executor = Executor(project_root, engine)
        self.critic = Critic(project_root, engine)
        self.long_term_memory = LongTermMemory(project_root)

    def _proclaim_plan(self, plan: Plan):
        """[FACULTY 2] A luminous herald for the AI's will."""
        tool_calls_str = ""
        for call in plan.tool_calls:
            args_str = ", ".join(f"{k}='{v}'" for k, v in call.arguments.items())
            tool_calls_str += f"  - [bold cyan]{call.tool_name}[/bold cyan]({args_str})\n"
            tool_calls_str += f"    [dim italic]Thought: {call.thought}[/dim italic]\n"

        panel = Panel(
            f"[bold]High-Level Thought:[/bold] [italic]{plan.thought}[/italic]\n\n[bold]Tool Calls:[/bold]\n{tool_calls_str}",
            title="[yellow]AI's Prophesied Plan[/yellow]",
            border_style="yellow"
        )
        self.console.print(panel)

    def _proclaim_observations(self, observations: List[Observation]):
        """[FACULTY 2] A herald for the echoes of reality."""
        for obs in observations:
            color = "green" if obs.status == "SUCCESS" else "red"
            # Use Syntax for better formatting of multi-line, potentially code-like output
            panel = Panel(
                Syntax(obs.output, "text", theme="monokai", word_wrap=True),
                title=f"[{color}]Observation: {obs.tool_name}[/{color}]",
                border_style=color
            )
            self.console.print(panel)

    def run_loop(self) -> AgentState:
        """The Grand Symphony of Cognition."""
        while not self.state.is_complete and self.state.current_cycle < self.state.max_cycles:
            self.state.current_cycle += 1
            self.console.rule(f"[bold]AGENT CYCLE {self.state.current_cycle}/{self.state.max_cycles}[/bold]")

            try:
                # 1. PERCEIVE
                self.console.print("[dim]Perceiving reality...[/dim]")
                context_blueprint = self.perceiver.perceive(self.state)

                # 2. PLAN
                self.console.print("[dim]Formulating a new plan...[/dim]")
                plan: Plan = self.planner.create_plan(self.state, context_blueprint)
                self._proclaim_plan(plan)

                # --- FACULTY 5 & 6: HALLUCINATION & VOID WARD ---
                if not plan.tool_calls:
                    self.console.print(
                        "[yellow]Warning: The AI proclaimed a void plan. Forcing re-evaluation.[/yellow]")
                    self.state.history.append({"cycle": self.state.current_cycle, "plan": plan.model_dump(),
                                               "critique": {"reasoning": "Void plan detected, forcing new cycle."}})
                    continue

                for call in plan.tool_calls:
                    if call.tool_name not in self.executor.registry:
                        raise ArtisanHeresy(f"The AI hallucinated a profane tool: '{call.tool_name}'",
                                            details=f"Known tools are: {list(self.executor.registry.keys())}")
                # -------------------------------------------------

                # --- FACULTY 1: THE GUARDIAN'S VETO ---
                if self.interactive:
                    if not Confirm.ask("\n[bold question]Execute this plan?[/bold question]", default=True):
                        self.state.is_complete = True
                        self.state.final_result = "Mission stayed by the Architect's hand."
                        self.console.print("[yellow]Rite stayed by Architect's will.[/yellow]")
                        break
                # ------------------------------------

                # 3. ACT
                self.console.print("[dim]Executing plan...[/dim]")
                observations: List[Observation] = self.executor.execute_plan(plan)
                self._proclaim_observations(observations)

                # 4. VERIFY (The Conscience)
                self.console.print("[dim]Critiquing the outcome...[/dim]")
                critique = self.critic.review(self.state, observations)
                self.console.print(
                    Panel(f"[bold]Critique:[/bold] {critique.reasoning}", title="[blue]The Conscience[/blue]",
                          border_style="blue"))

                # 5. UPDATE STATE & MEMORY
                self.state.history.append({
                    "cycle": self.state.current_cycle,
                    "plan": plan.model_dump(),
                    "observations": [o.model_dump() for o in observations],
                    "critique": critique.model_dump()
                })

                if critique.is_goal_achieved:
                    self.state.is_complete = True
                    self.state.final_result = critique.reasoning
                    # --- FACULTY 3: THE RITE OF REMEMBRANCE ---
                    self.long_term_memory.remember(self.state)
                    Logger.success("CRITIC: Goal Achieved. Mission Complete. The memory is enshrined.")

            except Exception as e:
                # --- FACULTY 8: THE UNBREAKABLE HEART ---
                Logger.error(f"Catastrophic Agent Loop Failure: {e}", exc_info=True)
                # --- FACULTY 4: THE PARADOX WARD ---
                # We record the failure in history so the agent can see its mistake in the next cycle.
                failure_observation = Observation(tool_name="SYSTEM", tool_input={},
                                                  output=f"A paradox shattered the loop: {e}", status="FAILURE")
                self.state.history.append({
                    "cycle": self.state.current_cycle,
                    "plan": {"thought": "Attempted to execute a plan that resulted in a system error."},
                    "observations": [failure_observation.model_dump()],
                    "critique": {
                        "reasoning": f"A system-level error occurred: {e}. I must re-evaluate my strategy based on this failure."}
                })
                self.console.print(Panel(f"[bold red]A paradox shattered the Agent's thought process:[/bold red]\n{e}",
                                         title="[red]SYSTEM HERESY[/red]", border_style="red"))
                # In non-interactive mode, we might choose to break. In interactive, we could let it try to recover.
                if not self.interactive:
                    self.state.final_result = f"Agent failed with exception: {e}"
                    break

        if not self.state.is_complete:
            self.state.final_result = self.state.final_result or "Agent exceeded max cycles."
            Logger.error("AGENT: Mission failed to complete within cycle limit.")

        return self.state