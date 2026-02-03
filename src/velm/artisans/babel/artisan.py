# Path: artisans/babel/artisan.py
# -------------------------------

from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import BabelRequest
from ...help_registry import register_artisan
from ...core.ai.engine import AIEngine
from ...utils import atomic_write
from ...contracts.heresy_contracts import ArtisanHeresy


@register_artisan("port")
class BabelArtisan(BaseArtisan[BabelRequest]):
    """
    =================================================================================
    == THE BABEL ENGINE (V-Ω-SEMANTIC-TRANSPILER)                                  ==
    =================================================================================
    LIF: 10,000,000,000

    Transmutes code from one language to another, preserving architectural intent.
    Optionally invokes Fusion to bind the new code back to the old.
    """

    def execute(self, request: BabelRequest) -> ScaffoldResult:
        source = (self.project_root / request.source).resolve()
        if not source.exists():
            raise ArtisanHeresy(f"Source void: {source}")

        self.logger.info(
            f"Initiating Transmutation: [cyan]{source.name}[/cyan] -> [magenta]{request.target_lang.upper()}[/magenta]")

        # 1. Read Soul
        content = source.read_text(encoding='utf-8')

        # 2. The Alchemical Translation
        ai = AIEngine.get_instance()
        prompt = f"""
        Translate the following code to {request.target_lang}.

        SOURCE CODE ({source.name}):
        ```
        {content}
        ```

        REQUIREMENTS:
        1. Use idiomatic {request.target_lang} patterns.
        2. Preserve all comments and logic.
        3. If porting to Rust, make it compatible with PyO3 if requested.

        Output ONLY the code.
        """

        with self.console.status("[bold magenta]Transmuting logic...[/bold magenta]"):
            new_code = ai.ignite(prompt, model="smart")
            # Strip markdown blocks
            new_code = new_code.replace("```rust", "").replace("```python", "").replace("```", "").strip()

        # 3. Inscribe
        ext_map = {"rust": "rs", "python": "py", "go": "go", "typescript": "ts"}
        new_ext = ext_map.get(request.target_lang, "txt")
        new_path = source.with_suffix(f".{new_ext}")

        atomic_write(new_path, new_code, self.logger, self.project_root)

        self.console.print(Panel(
            Syntax(new_code, request.target_lang, theme="monokai"),
            title=f"[green]Transmutation Complete: {new_path.name}[/green]"
        ))

        # 4. Fusion Binding (Optional)
        if request.fusion_bind and request.target_lang == "rust" and source.suffix == ".py":
            from ...interfaces.requests import FusionRequest
            from ..fusion.artisan import FusionArtisan

            self.logger.info("Invoking Fusion Core to bind the new organ...")
            fusion_req = FusionRequest(
                fusion_command="compile",
                source=str(new_path.relative_to(self.project_root)),
                target_lang="python",
                output_dir=str(source.parent.relative_to(self.project_root))
            )
            # We delegate to the Fusion Artisan
            return FusionArtisan(self.engine).execute(fusion_req)

        return self.success(
            f"Ported to {new_path.name}",
            artifacts=[Artifact(path=new_path, type="file", action="created")]
        )