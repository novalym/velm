# scaffold/artisans/dream.py
from ..core.artisan import BaseArtisan
from ..interfaces.requests import DreamRequest
from ..interfaces.base import ScaffoldResult
from ..core.ai.engine import AIEngine
from ..utils import atomic_write
from pathlib import Path





class DreamArtisan(BaseArtisan[DreamRequest]):
    """
    [THE ONEIROMANCER]
    Transmutes natural language intent into a Gnostic Blueprint.
    """

    def execute(self, request: DreamRequest) -> ScaffoldResult:
        ai = AIEngine.get_instance()

        system_prompt = """
        You are an expert Software Architect using the Scaffold framework.
        Generate a valid `.scaffold` file based on the user's description.
        Use `$$ variable = value` for configuration.
        Use `path/to/file :: "content"` for files.
        Use `%% post-run` for commands.
        Output ONLY the file content, no markdown blocks.
        """

        self.console.status("[bold magenta]Dreaming...[/bold magenta]")
        blueprint_content = ai.ignite(
            user_query=request.prompt,
            system=system_prompt,
            model="smart"
        )

        target = self.project_root / "dream.scaffold"
        atomic_write(target, blueprint_content, self.logger, self.project_root)

        return self.success(f"Dream materialized at {target.name}", artifacts=[])