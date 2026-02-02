# Path: artisans/tutorial/artisan.py
# ----------------------------------

from pathlib import Path
from rich.panel import Panel
from rich.markdown import Markdown

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import TeachRequest
from ...help_registry import register_artisan
from ...utils import atomic_write

from .engine import ThePedagogue
from .quest_giver import QuestGiver


@register_artisan("teach")
class TutorialArtisan(BaseArtisan[TeachRequest]):
    """
    =================================================================================
    == THE TUTORIAL FORGE (V-Ω-GAMIFIED-ONBOARDING)                                ==
    =================================================================================
    LIF: 10,000,000,000

    Transmutes the codebase into an interactive RPG (Role Playing Git).
    Creates a 'student' branch with broken code and tests, guiding the user to fix it.
    """

    def execute(self, request: TeachRequest) -> ScaffoldResult:
        if request.teach_command == "generate":
            return self._conduct_generation_rite(request)
        elif request.teach_command == "start":
            return self._conduct_start_rite(request)
        elif request.teach_command == "verify":
            return self._conduct_verify_rite(request)

        return self.failure("Unknown pedagogical rite.")

    def _conduct_generation_rite(self, request: TeachRequest) -> ScaffoldResult:
        self.logger.info("The Pedagogue analyzes the architectural narrative...")

        pedagogue = ThePedagogue(self.project_root)

        # 1. Analyze (Find optimal tutorial candidates)
        curriculum = pedagogue.design_curriculum(
            topic=request.topic,
            difficulty=request.difficulty
        )

        # 2. Inscribe
        output_path = self.project_root / request.output_dir / "curriculum.json"
        import json
        atomic_write(output_path, json.dumps(curriculum, indent=2), self.logger, self.project_root)

        return self.success(
            f"Curriculum forged with {len(curriculum['quests'])} quests.",
            artifacts=[Artifact(path=output_path, type="file", action="created")]
        )

    def _conduct_start_rite(self, request: TeachRequest) -> ScaffoldResult:
        """Initializes the interactive session."""
        qg = QuestGiver(self.project_root, request.output_dir)

        # 1. Load Curriculum
        quest = qg.load_next_quest()
        if not quest:
            return self.success("You have mastered all knowledge in this sanctum!")

        # 2. Break Reality (Apply the broken state)
        qg.apply_quest_state(quest)

        # 3. Proclaim the Quest
        self.console.print(Panel(
            Markdown(f"# Quest: {quest['title']}\n\n{quest['description']}\n\n**Objective:** {quest['objective']}"),
            title="[bold yellow]New Quest Accepted[/bold yellow]",
            border_style="yellow"
        ))

        return self.success(f"Quest '{quest['title']}' active.")

    def _conduct_verify_rite(self, request: TeachRequest) -> ScaffoldResult:
        """Checks if the student has fixed the code."""
        qg = QuestGiver(self.project_root, request.output_dir)

        if qg.verify_quest():
            self.console.print("[bold green]✨ QUEST COMPLETE! ✨[/bold green]")
            self.console.print("You have restored Gnostic Harmony to this module.")
            qg.advance_progress()
            return self.success("Quest complete.")
        else:
            return self.failure("The tests still fail. Gnosis is incomplete. Try again.")