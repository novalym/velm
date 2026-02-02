# Path: scaffold/artisans/translate/artisan.py
# --------------------------------------------

from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import TranslateRequest
from ...core.ai.engine import AIEngine
from ...help_registry import register_artisan
from ...inquisitor import get_treesitter_gnosis


@register_artisan("translate")
class TranslateArtisan(BaseArtisan[TranslateRequest]):
    """
    =============================================================================
    == THE ROSETTA STONE (V-Ω-ARCHITECTURAL-TRANSLATOR)                        ==
    =============================================================================
    Transmutes code between tongues while preserving the Gnostic Soul.
    Uses AST analysis to prime the AI with structural context.
    """

    def execute(self, request: TranslateRequest) -> ScaffoldResult:
        source_path = (self.project_root / request.source_path).resolve()
        if not source_path.exists():
            return self.failure("Source scripture not found.")

        self.logger.info(f"Translating {source_path.name} to {request.target_lang}...")

        # 1. Extract Gnosis (AST)
        content = source_path.read_text(encoding='utf-8')
        dossier = get_treesitter_gnosis(source_path, content)

        # Summarize Structure for the AI
        structure_summary = []
        if "functions" in dossier:
            structure_summary.append(f"Functions: {', '.join([f['name'] for f in dossier['functions']])}")
        if "classes" in dossier:
            structure_summary.append(f"Classes: {', '.join([c['name'] for c in dossier['classes']])}")

        context_str = "\n".join(structure_summary)

        # 2. The Prompt
        prompt = (
            f"Translate the following code from {request.source_lang} to {request.target_lang}.\n"
            f"Context: {context_str}\n"
            "Maintain the exact architectural pattern (Class/Function structure). "
            "Use idiomatic patterns for the target language (e.g. Structs/Impl for Rust, Classes for Python).\n\n"
            f"Code:\n```\n{content}\n```"
        )

        # 3. The Communion
        ai = AIEngine.get_instance()
        translated_code = ai.ignite(prompt, model="smart")

        # 4. The Proclamation
        self.console.print(Panel(
            Syntax(translated_code, request.target_lang, theme="monokai"),
            title=f"[bold green]Translation: {request.target_lang.upper()}[/bold green]"
        ))

        return self.success("Translation complete.", data={"content": translated_code})