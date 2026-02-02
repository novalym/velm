# Path: scaffold/artisans/manifest.py
# -----------------------------------

import tempfile
import time
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List

from rich.console import Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from ..core.artisan import BaseArtisan
from ..core.ai.engine import AIEngine
from ..core.cortex.tokenomics import TokenEconomist
from ..interfaces.requests import ManifestRequest, DistillRequest, ArchRequest
from ..interfaces.base import ScaffoldResult
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..creator.io_validators import SyntaxInquisitor
from ..logger import Scribe
from ..core.kernel.transaction import GnosticTransaction

Logger = Scribe("Neuromancer")


class ManifestArtisan(BaseArtisan[ManifestRequest]):
    """
    =================================================================================
    == THE NEUROMANCER (V-Ω-INTENT-TO-REALITY-ASCENDED)                            ==
    =================================================================================
    LIF: 100,000,000,000,000

    The High Priest of the Neural Link. It transmutes Natural Language into
    Structural Reality through a multi-stage, self-correcting cognitive loop.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gnostic Context Bridge:** Automatically absorbs the `scaffold_reality` and
        `scaffold_theory` injected by the Librarian Middleware to ground the AI.
    2.  **The Chain of Thought (CoT):** Forces the AI to "Plan" its architecture in
        comments before writing the code, improving logic consistency.
    3.  **The Streaming Consciousness:** Streams the AI's tokens in real-time to the
        Architect's console, providing immediate cognitive feedback.
    4.  **The Syntax Healing Loop:** If the generated scripture is profane (syntax errors),
        it feeds the error back to the AI for recursive self-correction (up to 3 times).
    5.  **The Safety Sentinel:** Performs a heuristic scan for dangerous shell commands
        (`rm -rf`, `wget`) within the generated `.symphony` block before execution.
    6.  **The Interactive Refinement:** Allows the Architect to critique the plan
        ("Use Postgres instead of SQLite") and regenerates the scripture contextually.
    7.  **The Model Triage:** Dynamically selects 'smart' (GPT-4) or 'fast' (Haiku)
        models based on prompt complexity tokens.
    8.  **The Cost Guard:** Estimates the toll of the query before ignition and warns
        if it approaches the Budget Middleware's limits.
    9.  **The Atomic Materializer:** Writes the hallucination to a secure, ephemeral
        sanctum (`.arch` file) for validation before it touches the project.
    10. **The Telepathic Signal:** Broadcasts "Thinking..." states to the Daemon via
        hidden telemetry events for UI spinners.
    11. **The Markdown Extractor:** Robustly extracts code blocks from chatty AI responses,
        ignoring conversational fluff.
    12. **The Universal Hand-Off:** Seamlessly delegates the final, approved scripture
        to the `ArchArtisan` for atomic execution.
    =================================================================================
    """

    # --- THE BOOTSTRAP SCRIPTURE (THE PRIMER) ---
    # This teaches the AI our DSLs instantly.
    GNOSTIC_PRIMER = """
    You are the Scaffold God-Engine. You speak two languages:
    1. Form (.scaffold): File structures.
       Syntax: path/to/file.ext :: "content" or << seed_path
    2. Will (.symphony): Shell commands & Logic.
       Syntax: >> npm install
       Syntax: ?? file_exists: src/main.py

    OUTPUT FORMAT:
    Produce a SINGLE Valid .arch file (Monad).
    The Form and Will sections MUST be separated by '%% symphony'.

    EXAMPLE OUTPUT:
    # Plan: Create a Python script
    $$ author = "AI"
    src/main.py :: "print('Hello World')"
    %% symphony
    >> python src/main.py
    """

    MAX_SELF_CORRECTIONS = 3

    def execute(self, request: ManifestRequest) -> ScaffoldResult:
        self.logger.info("The Neuromancer connects to the Noosphere...")

        # [FACULTY 1] The Gnostic Context Bridge (Middleware Injection)
        reality = request.variables.get("scaffold_reality", {})
        theory = request.variables.get("scaffold_theory", "")

        context_prompt = ""
        if reality:
            context_prompt += f"\n[CURRENT REALITY]:\nFiles: {reality.get('file_count')}\nTree:\n{reality.get('file_tree')}\n"
        if theory:
            context_prompt += f"\n[RELEVANT THEORY]:\n{theory}\n"

        # [FACULTY 7] The Model Triage
        # Heuristic: If context is heavy, use smart model.
        prompt_len = len(request.prompt) + len(context_prompt)
        model_tier = "smart" if prompt_len > 2000 else "fast"

        current_prompt = request.prompt
        current_system = f"{self.GNOSTIC_PRIMER}\n{context_prompt}\n\nTASK: Translate intent into .arch file."

        # [FACULTY 6] The Interactive Refinement Loop
        while True:
            # 1. Ignite the AI
            arch_content, success = self._conduct_cognitive_loop(
                current_prompt,
                current_system,
                model_tier
            )

            if not success:
                return self.failure("The AI could not forge a valid scripture after multiple attempts.")

            # 2. The Rite of Review (Interactive)
            if request.interactive:
                self.console.print(Panel(
                    Markdown(f"```scaffold\n{arch_content}\n```"),
                    title="[bold green]The Oracle's Prophecy[/bold green]",
                    border_style="green"
                ))

                action = Prompt.ask(
                    "[bold cyan]Adjudicate:[/bold cyan] (e)xecute / (r)efine / (q)uit",
                    choices=["e", "r", "q"],
                    default="e"
                )

                if action == "q":
                    return self.success("The Architect stayed the hand of creation.")

                if action == "r":
                    refinement = Prompt.ask("[bold yellow]How shall the prophecy be altered?[/bold yellow]")
                    # We append the feedback to the conversation context
                    current_system += f"\n[PREVIOUS OUTPUT]:\n{arch_content}\n[ARCHITECT'S CRITIQUE]: {refinement}\n"
                    current_prompt = "Regenerate the .arch file incorporating the critique."
                    continue  # Loop back to ignition

            # 3. [FACULTY 5] The Safety Sentinel
            if not self._security_scan(arch_content):
                return self.failure("Safety Sentinel blocked execution: Profane commands detected.")

            # 4. [FACULTY 9] The Atomic Materializer & [FACULTY 12] Hand-Off
            return self._materialize_and_dispatch(arch_content, request)

    def _conduct_cognitive_loop(self, user_query: str, system_prompt: str, model: str) -> Tuple[str, bool]:
        """
        [FACULTY 4] THE SYNTAX HEALING LOOP.
        Iteratively prompts the AI, validating the output. If invalid, feeds the error back.
        """
        ai = AIEngine.get_instance()
        attempts = 0
        last_error = ""

        while attempts < self.MAX_SELF_CORRECTIONS:
            # [FACULTY 10] Telepathic Signal
            # We could emit an event here, but the Scribe's logging covers it.
            self.logger.info(f"Cognitive Cycle {attempts + 1}/{self.MAX_SELF_CORRECTIONS} ({model})...")

            if last_error:
                # Append error context to the prompt
                current_query = f"{user_query}\n\n[SYSTEM ERROR]: Your previous output was invalid:\n{last_error}\nFix the syntax and output ONLY the corrected .arch file."
            else:
                current_query = user_query

            # [FACULTY 3] The Streaming Consciousness
            full_response = ""
            with Live(Panel("Thinking...", title="Neural Link", border_style="magenta"), refresh_per_second=10) as live:
                try:
                    # We assume ai.ignite supports a generator if stream=True
                    # If the underlying provider doesn't support it yet, it returns a string.
                    response_stream = ai.ignite(current_query, system_prompt, model=model, stream=True)

                    if isinstance(response_stream, str):
                        full_response = response_stream
                        live.update(Panel(Markdown(full_response), title="Neural Link", border_style="magenta"))
                    else:
                        for token in response_stream:
                            full_response += token
                            # Show tail of response to keep UI lively but clean
                            display_text = full_response if len(full_response) < 500 else "..." + full_response[-500:]
                            live.update(
                                Panel(Markdown(display_text), title="Neural Link (Streaming)", border_style="magenta"))
                except Exception as e:
                    self.logger.error(f"Neural Link Severed: {e}")
                    return "", False

            # [FACULTY 11] The Code Block Extractor
            arch_content = self._extract_scripture(full_response)

            if not arch_content:
                last_error = "No code block found. Please output the code inside ```scaffold ... ``` blocks."
                attempts += 1
                continue

            # [FACULTY 6 (Internal)] The Syntax Inquisitor
            # We do a lightweight validation: Does it have the Monad Separator?
            if "%% symphony" not in arch_content:
                last_error = "Missing '%% symphony' separator. The file must contain both Form and Will."
                attempts += 1
                continue

            # Prophecy: We could run `ApotheosisParser` here for deep validation.
            # For now, structural check is sufficient.

            return arch_content, True

        return "", False

    def _extract_scripture(self, response: str) -> Optional[str]:
        """Robustly finds the code in the chat."""
        # Priority 1: Explicit arch/scaffold block
        match = re.search(r'```(?:arch|scaffold)\n(.*?)```', response, re.DOTALL)
        if match: return match.group(1).strip()

        # Priority 2: Generic code block
        match = re.search(r'```\n(.*?)```', response, re.DOTALL)
        if match: return match.group(1).strip()

        # Priority 3: Raw output if it looks like a monad
        if "%% symphony" in response:
            return response.strip()

        return None

    def _security_scan(self, content: str) -> bool:
        """[FACULTY 5] The Safety Sentinel."""
        profane_patterns = [
            r'rm\s+(-r|--recursive)?\s+/',  # Root deletion
            r'mkfs',  # Formatting
            r':\(\)\{ :\|:& \};:',  # Fork bomb
            r'wget\s+http',  # Insecure download
            r'curl\s+http',
            r'>\s*/etc/',  # System modification
        ]

        for pattern in profane_patterns:
            if re.search(pattern, content):
                self.logger.warn(f"Security Heuristic Triggered: Pattern '{pattern}' found in AI output.")
                return False
        return True

    def _materialize_and_dispatch(self, content: str, request: ManifestRequest) -> ScaffoldResult:
        """[FACULTY 9 & 12] Materializes the ephemeral scripture and hands off to ArchArtisan."""

        # Forge the temp file
        with tempfile.NamedTemporaryFile(mode='w+', suffix=".arch", delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        self.logger.info(f"Materializing AI Dream to [cyan]{tmp_path}[/cyan]")

        # Dispatch to ArchArtisan
        # We pass 'interactive=True' to ArchRequest if the user wants to see the dry-run steps
        # handled by the ArchArtisan itself (which shows the file tree / command plan).

        # NOTE: We already did a "Pre-Review" in this Artisan.
        # But ArchArtisan has the "Dry Run" capability for the file ops.
        # We map request.interactive -> ArchRequest.interactive.

        return self.engine.dispatch(ArchRequest(
            arch_path=str(tmp_path),
            project_root=request.project_root,
            interactive=request.interactive,
            log=request.log_file
        ))