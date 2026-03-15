# Path: core/alchemist/elara/library/system_rites/ai_interaction.py
# -----------------------------------------------------------------

import os
import sys
import time
from typing import Any, Optional, List
from ..registry import register_rite
from ......logger import Scribe

Logger = Scribe("SystemRites:AI")

@register_rite("ai")
def generate_via_ai(value: Any, prompt: Optional[str] = None, model: str = "smart", **kwargs) -> str:
    """[ASCENSION 1]: Consults the Neural Cortex JIT to write code or content."""
    Logger.info(f"🧠 [SHADOW SUTURE] Consulting Neural Cortex...")
    actual_prompt = prompt if prompt else str(value)
    context_data = str(value) if prompt else ""

    try:
        from ......core.ai.engine import AIEngine
        from ......core.ai.contracts import NeuralPrompt
        import asyncio

        ai_engine = AIEngine.get_instance()
        system_instruction = "Output ONLY the raw content willed. No markdown fences. No chatter."
        full_query = f"Context:\n{context_data}\n\nTask: {actual_prompt}"

        try:
            loop = asyncio.get_running_loop()
            import nest_asyncio; nest_asyncio.apply()
            revelation = ai_engine.active_provider.commune(
                NeuralPrompt(user_query=full_query, system_instruction=system_instruction, model_hint=model)
            )
        except RuntimeError:
            revelation = asyncio.run(ai_engine.active_provider.commune(
                NeuralPrompt(user_query=full_query, system_instruction=system_instruction, model_hint=model)
            ))

        clean_content = revelation.content.strip()
        if clean_content.startswith("```"):
            clean_content = "\n".join(clean_content.splitlines()[1:-1])

        Logger.success(f"✨ [SHADOW SUTURE] Neural revelation manifest ({len(clean_content)} chars).")
        return clean_content
    except Exception as e:
        Logger.error(f"Neural Cortex Fracture: {e}")
        return f"/* AI_GENERATION_FAILED: {str(e)} */"

@register_rite("ask")
def socratic_prompt(value: Any, question: Optional[str] = None, default: Any = "", secret: bool = False, **kwargs) -> Any:
    """[ASCENSION 2]: Interactively requests missing Gnosis from the Architect."""
    from rich.prompt import Prompt
    if os.environ.get("SCAFFOLD_NON_INTERACTIVE") == "1":
        return default if default != "" else str(value)
    prompt_text = question if question else str(value)
    if secret:
        return Prompt.ask(f"[bold magenta]?[/] [cyan]{prompt_text}[/]", password=True, default=default)
    return Prompt.ask(f"[bold magenta]?[/] [cyan]{prompt_text}[/]", default=default)

@register_rite("choose")
def gnostic_choice(value: Any, options: List[Any], question: str = "Select a shard path", **kwargs) -> Any:
    """[ASCENSION 3]: Forces the Architect to select a single reality from a list."""
    from rich.prompt import IntPrompt
    from rich.console import Console
    if os.environ.get("SCAFFOLD_NON_INTERACTIVE") == "1": return options[0] if options else value
    console = Console()
    console.print(f"\n[bold yellow]⚖️  JURISPRUDENCE GATE: {question}[/]")
    for idx, opt in enumerate(options):
        console.print(f"  [bold cyan]{idx + 1}[/]. {opt}")
    choice_idx = IntPrompt.ask(f"\n[bold yellow]>>[/] Proclaim index", choices=[str(i + 1) for i in range(len(options))], show_choices=False)
    return options[choice_idx - 1]

@register_rite("confirm")
def confirmation_vow(value: Any, question: str = "Do you grant the Vow of Execution?", **kwargs) -> bool:
    """[ASCENSION 4]: Halts for explicit Architect authorization."""
    from rich.prompt import Confirm
    if os.environ.get("SCAFFOLD_NON_INTERACTIVE") == "1": return True
    return Confirm.ask(f"[bold red]⚠️  {question}[/]")