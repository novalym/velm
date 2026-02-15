import tempfile
import json
from pathlib import Path

from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.panel import Panel

# --- THE DIVINE SUMMONS OF THE PANTHEON & CONTRACTS ---
from .contracts import AIThoughtProcess
from .inquest import InquestConductor
from .planner import GnosticPlanner
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan
from ...core.ai.engine import AIEngine
# The one true, ascended Request vessel is summoned from its sacred home
from ...interfaces.requests import ArchitectRequest, DistillRequest, TransmuteRequest
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("GnosticArchitect")


@register_artisan("architect")
class ArchitectArtisan(BaseArtisan[ArchitectRequest]):
    """
    =================================================================================
    == THE GNOSTIC ARCHITECT (V-Ω-PANTHEON-MIND-APOTHEOSIS)                        ==
    =================================================================================
    @gnosis:title The Gnostic Architect (`architect`)
    @gnosis:summary The AI Co-Architect. A true sentient partner for architectural evolution.
    @gnosis:LIF 10,000,000

    This is the Gnostic Architect in its final, eternal form. It is a pure **Conductor**
    that orchestrates a **Pantheon of Specialist Faculties** to conduct a true,
    multi-step, conversational symphony with the AI, transforming natural language
    into pure, Gnostically-aware architectural change.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **The Pure Conductor:** This artisan is now a High Priest. It delegates all
        complex thought to its specialist faculties (`GnosticPlanner`, `InquestConductor`).
    2.  **The Conversational Symphony:** It no longer performs a single plea. It engages
        in a multi-step dialogue with the AI: Plan -> Inquest -> Proclamation.
    3.  **The Gnostic Planner:** It summons a dedicated `GnosticPlanner` to perceive the
        AI's explicit, structured `[PLAN:...]` block, separating intent from action.
    4.  **The Inquest Protocol:** It commands the `InquestConductor` to fulfill the AI's
        `[INQUEST:...]` pleas, granting the AI the power to query the project's soul.
    5.  **The Dual-Minded AI:** Its new `SYSTEM_PROMPT_V3` teaches the AI to be a true
        dual-purpose mind, capable of both **Inquiry** (answering questions) and
        **Evolution** (forging blueprints).
    6.  **The Gnostic Triage of Will:** It flawlessly adjudicates the AI's final intent,
        proclaiming Markdown answers directly or delegating blueprints to the Transmutator.
    7.  **The Contextual Anchor:** It continues to ground the AI's Gaze by providing a
        skeletal map of the current reality via the `distill` artisan.
    8.  **The Crystal Mind Conduit:** It detects the presence of the Gnostic Database
        (`gnosis.db`) and anoints the AI with the knowledge to query it.
    9.  **The Unbreakable Ward of Paradox:** Its entire symphony is shielded. A failure
        in the AI's Gaze or a paradox in an inquest does not shatter the engine.
    10. **The Pure Gnostic Contract:** It honors the one true `ArchitectRequest` from
        its sacred home in `interfaces/requests.py`.
    11. **The Sovereign Soul:** Its architecture is a masterpiece of Gnostic design,
        each faculty a sovereign, testable, and pure artisan.
    12. **The Final Word:** It is the one true Mission Control for AI-driven development,
        the living heart of the Symbiotic Creation & Manifestation mission.
    """

    SYSTEM_PROMPT_V3 = """
You are the Velm God-Engine, a master software architect. Your prime directive is to assist the user by answering questions or evolving their software project. You operate in a two-phase process: PLANNING and EXECUTION.

---
### PHASE 1: THE GNOSTIC PLAN

First, you MUST formulate a plan and proclaim it within a `[PLAN: ...]` block. This block MUST contain a valid JSON object with the following schema:
- `reasoning`: Your analysis of the user's request and the current project state.
- `inquests`: (Optional) An array of Gnostic Inquests to gather information *before* you can act. An inquest is a JSON object: `{"type": "sql", "query": "SELECT ...", "purpose": "..."}`.
- `final_output_type`: Your judgment of what the final output should be: `"blueprint"` or `"markdown"`.

---
### PHASE 2: THE FINAL PROCLAMATION

After the `[PLAN: ...]` block, you will proclaim your final output based on the `final_output_type`.

1.  **If `final_output_type` is `markdown`**: Answer the user's question in rich Markdown.
2.  **If `final_output_type` is `blueprint`**: Output the raw, complete `.scaffold` or `.patch.scaffold` blueprint. DO NOT wrap it in markdown code blocks.

---
### THE CRYSTAL MIND (IF AVAILABLE)

If the system prompt informs you that the Crystal Mind is awake, you can use `inquests` to query the project's dependency graph.
- **Schema:** `scriptures(path, ...)` and `bonds(source_path, target_path)`.
- **Use Case:** To answer "what is the impact of..." or to find all files that need to be changed for a refactor.

**EXAMPLE SYMPHONY (INQUIRY):**

User: "What is the impact of deleting `src/core/utils.py`?"

You:
[PLAN: {
  "reasoning": "The user wants to understand the impact of deleting a file. I must query the Crystal Mind's `bonds` table to find all scriptures that depend on `src/core/utils.py`.",
  "inquests": [{
    "type": "sql",
    "query": "SELECT source_path FROM bonds WHERE target_path LIKE '%src/core/utils.py'",
    "purpose": "To find all direct dependents of the target file."
  }],
  "final_output_type": "markdown"
}]
(System will respond with inquest results if any)
(You will then transmute the results into a beautiful Markdown answer)

**EXAMPLE SYMPHONY (EVOLUTION):**

User: "Add a health check endpoint to the API."

You:
[PLAN: {
  "reasoning": "The user wants to add a new feature. I will add a new route to the main router file and create a new service for the health logic.",
  "inquests": [],
  "final_output_type": "blueprint"
}]
# This plan creates a new health check service and wires it into the main router.
src/services/health_service.py :: "def check_health(): return {'status': 'ok'}"
src/api/router.py += "\\nfrom ..services.health_service import check_health\\n\\n@router.get('/health')\\ndef health_check():\\n    return check_health()"
"""

    def __init__(self, engine):
        super().__init__(engine)
        # The Pantheon is forged at the moment of birth
        self.planner = GnosticPlanner()
        self.inquest_conductor = InquestConductor(self.engine)

    def execute(self, request: ArchitectRequest) -> ScaffoldResult:
        self.console.rule("[bold magenta]The Gnostic Architect Awakens[/bold magenta]")

        # --- MOVEMENT I: PERCEPTION OF REALITY ---
        target_root = self.project_root
        self.logger.info("Distilling reality to skeletal essence...")
        distill_req = DistillRequest(
            source_path=str(target_root), strategy="structure", silent=True, non_interactive=True
        )
        distill_result = self.engine.dispatch(distill_req)
        if not distill_result.success:
            raise ArtisanHeresy("Failed to distill current reality.", details=distill_result.message)
        skeleton_content = distill_result.data.get("blueprint_content", "")

        # --- MOVEMENT II: FORGING OF THE AI's SOUL (SYSTEM PROMPT) ---
        final_system_prompt = self.SYSTEM_PROMPT_V3
        db_path = target_root / ".scaffold" / "gnosis.db"
        if db_path.exists():
            self.logger.info("Crystal Mind detected. The AI's Gaze is now omniscient.")

        # --- MOVEMENT III: THE CONVERSATIONAL SYMPHONY ---
        ai = AIEngine.get_instance()
        user_query = f"[CURRENT PROJECT SKELETON]\n{skeleton_content}\n\n[ARCHITECT'S INTENT]\n{request.prompt}"

        with self.console.status("[bold magenta]The AI Co-Architect is dreaming of the future...[/bold magenta]"):
            raw_ai_response = ai.ignite(
                user_query=user_query, system=final_system_prompt, model="smart", project_root=target_root
            )

        # --- MOVEMENT IV: THE GNOSTIC PLAN ---
        plan, final_proclamation = self.planner.divine_plan(raw_ai_response)

        # --- MOVEMENT V: THE GNOSTIC INQUEST ---
        if plan.inquests:
            inquest_results = self.inquest_conductor.conduct(plan.inquests)
            self.logger.info("Inquest complete. Re-awakening the AI with new Gnosis...")

            new_user_query = f"""
[PREVIOUS CONTEXT]
{user_query}

[PREVIOUS PLAN]
{plan.model_dump_json(indent=2)}

[GNOSTIC INQUEST RESULTS]
{json.dumps(inquest_results, indent=2)}

[YOUR TASK]
The inquest is complete. Now, using this new Gnosis, proclaim your final output as you originally planned (final_output_type: {plan.final_output_type}).
"""
            with self.console.status("[bold magenta]Synthesizing final proclamation from new Gnosis...[/bold magenta]"):
                final_proclamation = ai.ignite(
                    user_query=new_user_query, system=final_system_prompt, model="smart", project_root=target_root
                ).strip()

        # --- MOVEMENT VI: THE FINAL PROCLAMATION ---
        if plan.final_output_type == "markdown":
            self.console.print(Panel(
                Markdown(final_proclamation),
                title="[bold green]The Co-Architect's Gnosis[/bold green]",
                border_style="green"
            ))
            return self.success("The AI has proclaimed its Gnosis.")

        elif plan.final_output_type == "blueprint":
            return self._conduct_materialization_rite(final_proclamation, request)

        return self.failure("The AI's will was a void or its intent was unclear.")

    def _conduct_materialization_rite(self, blueprint_content: str, request: ArchitectRequest) -> ScaffoldResult:
        """The specialist artisan for materializing a blueprint forged by the AI."""
        target_root = self.project_root
        with tempfile.NamedTemporaryFile(mode='w+', suffix=".scaffold", delete=False,
                                         encoding='utf-8') as tmp_blueprint:
            tmp_blueprint.write(blueprint_content)
            blueprint_file = Path(tmp_blueprint.name)

        self.logger.info("The Prophecy has been inscribed. Initiating Simulation...")
        try:
            transmute_req = TransmuteRequest(
                blueprint_path=str(blueprint_file),
                project_root=target_root,
                preview=True, force=True, interactive=False
            )
            sim_result = self.engine.dispatch(transmute_req)
            if not sim_result.success:
                self.logger.warn("The Simulation revealed heresies.")

            if not request.interactive:
                confirm = True
            else:
                self.console.print()
                confirm = Confirm.ask(
                    "[bold green]Do you accept this Prophecy and wish to materialize it?[/bold green]")

            if confirm:
                self.console.rule("[bold red]Materializing Reality[/bold red]")
                real_req = TransmuteRequest(
                    blueprint_path=str(blueprint_file),
                    project_root=target_root,
                    preview=False, force=True, interactive=False
                )
                return self.engine.dispatch(real_req)
            else:
                return self.success("The Prophecy was rejected. Reality remains unchanged.")

        finally:
            if 'blueprint_file' in locals() and blueprint_file.exists():
                blueprint_file.unlink()