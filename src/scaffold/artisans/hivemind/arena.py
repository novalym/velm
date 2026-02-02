# Path: artisans/hivemind/arena.py
# --------------------------------

import time
import asyncio
from typing import List, Dict
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Group

from ...core.ai.engine import AIEngine
from ...core.ai.contracts import AIConfig
from ...logger import Scribe
from .contracts import PersonaProfile, Argument, Consensus
from .grimoire import PERSONA_ARCHETYPES

Logger = Scribe("HivemindArena")


class Arena:
    """
    =============================================================================
    == THE DEBATE HALL (V-Ω-MULTI-AGENT-ORCHESTRATOR)                          ==
    =============================================================================
    Orchestrates the conversation between multiple AI personas.
    Handles context switching and provider overrides dynamically.
    """

    def __init__(self, request_vars: Dict):
        self.ai = AIEngine.get_instance()
        self.transcript: List[Argument] = []
        self.overrides = request_vars

    def summon_council(self, names: List[str]) -> List[PersonaProfile]:
        """Materializes the requested personas from the Grimoire."""
        council = []
        for name in names:
            key = name.lower()
            if key in PERSONA_ARCHETYPES:
                profile = PERSONA_ARCHETYPES[key]
                # Apply User Overrides (e.g. swap model for specific persona)
                if self.overrides and key in self.overrides:
                    # In a full implementation, we'd deep copy and update fields
                    pass
                council.append(profile)
            else:
                # Dynamic Persona (Generic)
                council.append(PersonaProfile(
                    name=name.title(),
                    role="Guest Speaker",
                    system_prompt=f"You are a helpful assistant acting as {name}.",
                    color="white",
                    icon="👤"
                ))
        return council

    def conduct_debate(self, topic: str, council: List[PersonaProfile], rounds: int, blind: bool) -> List[Argument]:
        """The Main Loop of Discourse."""

        from rich.layout import Layout

        Logger.info(f"Topic of Debate: [bold]{topic[:50]}...[/bold]")

        # Initial Context
        shared_context = f"TOPIC: {topic}\n"

        for round_idx in range(1, rounds + 1):
            Logger.info(f"--- Round {round_idx} Begins ---")

            # In each round, every persona speaks
            for persona in council:
                # 1. Forge the Prompt
                if blind:
                    # They only see the topic, not others
                    prompt = f"{shared_context}\n\nProvide your analysis."
                else:
                    # They see the transcript so far
                    transcript_text = "\n".join([f"{a.speaker}: {a.content}" for a in self.transcript])
                    prompt = f"{shared_context}\n\n[TRANSCRIPT SO FAR]:\n{transcript_text}\n\n[INSTRUCTION]: Provide your input, responding to previous points if necessary."

                # 2. Invoke the Persona
                response_text = self._invoke_persona(persona, prompt)

                # 3. Record the Argument
                arg = Argument(
                    speaker=persona.name,
                    content=response_text,
                    round=round_idx,
                    timestamp=time.time()
                )
                self.transcript.append(arg)

                # 4. Proclaim Immediately
                self._proclaim_argument(persona, arg)

        return self.transcript

    def synthesize(self, council: List[PersonaProfile]) -> Consensus:
        """The Moderator's Final Word."""
        Logger.info("The Moderator is synthesizing the consensus...")

        transcript_text = "\n".join([f"{a.speaker}: {a.content}" for a in self.transcript])

        prompt = f"""
        You are the Moderator of a technical debate.
        Review the following transcript between: {', '.join([p.name for p in council])}.

        TRANSCRIPT:
        {transcript_text}

        TASK:
        1. Summarize the key points of agreement.
        2. Note the key points of contention.
        3. Provide a FINAL RESOLUTION / DECISION based on the strongest arguments.

        Output format: Markdown.
        """

        # Use the smartest available model for synthesis
        verdict = self.ai.ignite(prompt, model="smart")

        return Consensus(summary=verdict, resolution=verdict)

    def _invoke_persona(self, persona: PersonaProfile, prompt: str) -> str:
        """
        [THE POLYGLOT SWITCH]
        Dynamically reconfigures the AIEngine to match the Persona's preferred soul.
        """
        # 1. Capture current config
        original_config = self.ai.config.model_copy() if self.ai.config else AIConfig()

        try:
            # 2. Apply Persona Overrides
            temp_config = original_config.model_copy()
            if persona.provider:
                temp_config.provider = persona.provider
            if persona.model:
                temp_config.model = persona.model

            # Re-configure provider (This is efficient in V7, providers are cached)
            from ...core.ai.providers import get_provider
            provider_instance = get_provider(temp_config.provider)
            provider_instance.configure(temp_config)

            # 3. Ignite
            # We bypass the main engine's config lock by calling the provider directly
            # or by temporarily swapping the engine config.
            # Ideally, AIEngine.ignite should accept an override config.
            # For now, we hack the engine state (safe in single thread CLI)
            self.ai.active_provider = provider_instance
            self.ai.config = temp_config

            return self.ai.ignite(prompt, system=persona.system_prompt)

        finally:
            # 4. Restore Reality
            if self.ai.config:
                # Restore original provider
                provider_instance = get_provider(original_config.provider)
                provider_instance.configure(original_config)
                self.ai.active_provider = provider_instance
                self.ai.config = original_config

    def _proclaim_argument(self, persona: PersonaProfile, arg: Argument):
        """Renders the speech bubble."""
        from rich.console import Console
        console = Console()
        console.print(Panel(
            arg.content,
            title=f"{persona.icon} [bold {persona.color}]{persona.name}[/bold {persona.color}] [dim]({persona.role})[/dim]",
            border_style=persona.color,
            padding=(1, 2)
        ))