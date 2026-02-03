# Path: artisans/hivemind/artisan.py
# ----------------------------------

from pathlib import Path
from rich.markdown import Markdown
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import DebateRequest
from ...help_registry import register_artisan
from ...utils import atomic_write
from .arena import Arena


@register_artisan("debate")
class HivemindArtisan(BaseArtisan[DebateRequest]):
    """
    =================================================================================
    == THE HIVEMIND (V-Ω-MULTI-AGENT-CONSENSUS)                                    ==
    =================================================================================
    LIF: INFINITY

    Spins up a council of AI personas to argue about code, architecture, or philosophy.
    Uses 'blind' mode for model benchmarking and 'open' mode for refinement.
    """

    def execute(self, request: DebateRequest) -> ScaffoldResult:
        arena = Arena(request.variables)

        # 1. Summon the Council
        council = arena.summon_council(request.personas)
        names = ", ".join([f"{p.icon} {p.name}" for p in council])
        self.console.print(f"[bold]The Council has assembled:[/bold] {names}")

        # 2. Conduct the Debate
        transcript = arena.conduct_debate(
            topic=request.topic,
            council=council,
            rounds=request.rounds,
            blind=request.blind
        )

        final_output = ""

        # 3. The Synthesis
        if request.synthesize:
            consensus = arena.synthesize(council)
            self.console.print("\n")
            self.console.rule("[bold magenta]The Final Consensus[/bold magenta]")
            self.console.print(Markdown(consensus.resolution))
            final_output = consensus.resolution

        # 4. Inscribe the Record
        # We save the full transcript as a Gnostic artifact
        transcript_log = "\n\n".join([f"### {a.speaker} (Round {a.round})\n{a.content}" for a in transcript])
        if final_output:
            transcript_log += f"\n\n## CONSENSUS\n{final_output}"

        log_path = self.project_root / ".scaffold" / "debates" / f"debate_{int(transcript[0].timestamp)}.md"
        atomic_write(log_path, transcript_log, self.logger, self.project_root)

        return self.success(
            "The Council has spoken.",
            artifacts=[Artifact(path=log_path, type="file", action="created")]
        )