# Path: scaffold/artisans/forge/artisan.py
# ----------------------------------------

from pathlib import Path
import textwrap

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ForgeArtisanRequest
from ...help_registry import register_artisan
from ...utils import to_pascal_case, atomic_write


@register_artisan("forge")
class ForgeArtisan(BaseArtisan[ForgeArtisanRequest]):
    """
    =============================================================================
    == THE ARTISAN'S ANVIL (V-Ω-META-GENERATOR)                                ==
    =============================================================================
    LIF: 10,000,000,000

    The tool that builds tools. It scaffolds the directory structure, the Python
    class, and the Request model for a new Artisan.
    """

    def execute(self, request: ForgeArtisanRequest) -> ScaffoldResult:
        name_snake = request.artisan_name.lower().replace("-", "_")
        name_pascal = to_pascal_case(name_snake)
        class_name = f"{name_pascal}Artisan"
        request_name = f"{name_pascal}Request"

        target_dir = self.project_root / "scaffold" / "artisans" / name_snake

        if target_dir.exists():
            return self.failure(f"Artisan '{name_snake}' already exists at {target_dir}.")

        self.logger.info(f"Forging new Artisan: [cyan]{class_name}[/cyan]...")

        # 1. Forge __init__.py
        init_content = f"""
# Path: scaffold/artisans/{name_snake}/__init__.py
from .artisan import {class_name}
__all__ = ["{class_name}"]
        """.strip()

        # 2. Forge artisan.py
        artisan_content = f"""
# Path: scaffold/artisans/{name_snake}/artisan.py
from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import {request_name}
from ...help_registry import register_artisan

@register_artisan("{name_snake.replace('_', '-')}")
class {class_name}(BaseArtisan[{request_name}]):
    \"\"\"
    {request.description}
    \"\"\"

    def execute(self, request: {request_name}) -> ScaffoldResult:
        self.logger.info(f"{{self.name}} has been summoned.")

        # TODO: Implement your logic here

        return self.success("The rite is complete.")
        """.strip()

        # 3. Forge the Request Model (Injection Instruction)
        request_instruction = f"""
# --- INSTRUCTION: Add this to scaffold/interfaces/requests.py ---

class {request_name}(BaseRequest):
    \"\"\"
    Request context for {class_name}.
    \"\"\"
    # Add your fields here
    example_field: str = "default"
        """.strip()

        # 4. Forge the Registration (Injection Instruction)
        reg_instruction = f"""
# --- INSTRUCTION: Add this to scaffold/core/cli/grimoire.py ---

"{name_snake.replace('_', '-')}": {{
    "help": "{request.description}",
    "description": "Details about what this artisan does.",
    "args": [],
    "flags": []
}},
        """.strip()

        # Write files
        target_dir.mkdir(parents=True, exist_ok=True)
        atomic_write(target_dir / "__init__.py", init_content, self.logger, self.project_root)
        atomic_write(target_dir / "artisan.py", artisan_content, self.logger, self.project_root)

        # Output instructions
        self.console.print(Panel(
            request_instruction,
            title="[bold yellow]Step 1: Update Requests[/bold yellow]",
            border_style="yellow"
        ))

        self.console.print(Panel(
            reg_instruction,
            title="[bold yellow]Step 2: Update Grimoire[/bold yellow]",
            border_style="yellow"
        ))

        return self.success(
            f"Artisan '{name_snake}' forged at {target_dir}.",
            artifacts=[
                Artifact(path=target_dir / "artisan.py", type="file", action="created"),
                Artifact(path=target_dir / "__init__.py", type="file", action="created")
            ]
        )