# Path: scaffold/artisans/agent/artisan.py
# ----------------------------------------

import time
from types import SimpleNamespace
from typing import List, Optional, Set, Tuple
from .engine import AgenticEngine
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import AgentRequest
from ...help_registry import register_artisan
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...contracts.heresy_contracts import ArtisanHeresy


@register_artisan("agent")
class AgentArtisan(BaseArtisan[AgentRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF AGENCY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                   ==
    =================================================================================
    @gnosis:title The Gnostic Agent (`agent`)
    @gnosis:summary The divine conductor that awakens and governs the autonomous AI Agent.
    @gnosis:LIF 100,000,000,000,000,000,000

    This is the High Priest of Agency in its final, eternal form. It is the one true,
    sovereign gateway between the Architect's Will and the Agent's autonomous reality.
    It has been transfigured from a humble trigger into a sentient guardian and herald,
    its soul a pantheon of Gnostic faculties.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Anchor:** It performs a pre-flight Gaze to ensure it is being
        summoned within a valid Git sanctum, the only reality where the Agent can
        safely operate and reverse its own paradoxes.
    2.  **The Guardian's Veto Bridge:** It faithfully passes the Architect's vow of
        interactivity (`--interactive` or `--non-interactive`) to the `AgenticEngine`,
        enabling the crucial safety interlock.
    3.  **The Unbreakable Contract:** It speaks the pure, ascended `AgentRequest` vessel,
        its contract with the cosmos now whole and unbreakable.
    4.  **The Sovereign Soul:** Its purpose is pure orchestration. It contains no agentic
        logic itself; it delegates the entire symphony of thought to the `AgenticEngine`.
    5.  **The Luminous Herald of Apotheosis:** Upon a successful rite, it summons the
        one true `proclaim_apotheosis_dossier` to sing a triumphant, cinematic song of
        the Agent's Great Work, complete with rich telemetry.
    6.  **The Telemetric Heartbeat:** It meticulously chronicles the Agent's total
        runtime, the number of cognitive cycles, and the final state of its soul.
    7.  **The Artifact Hoarder:** It diligently gathers all files created or modified
        by the Agent into a pure list of `Artifact` vessels for the final proclamation,
        enabling perfect integration with the Gnostic UI.
    8.  **The Heresy Transmuter:** It wraps the entire agentic loop in an unbreakable
        ward, catching any catastrophic paradox and re-proclaiming it as a luminous
        `ArtisanHeresy` with full Gnostic context.
    9.  **The Luminous Voice:** Its every major action is proclaimed to the Gnostic
        Chronicle, from the moment of awakening to the final verdict.
    10. **The Dry-Run Prophecy (Future):** Its architecture is prepared for a future
        ascension where it can command the Agent to enter a "planning only" mode,
        prophesying its actions without touching the mortal realm.
    11. **The Cost Guard (Future):** It is the destined guardian of the treasury,
        prepared to receive a `--budget` vow to constrain the Agent's AI token usage.
    12. **The Final Word:** It is the one true, safe, and intelligent entry point to
        the entire Agentic Cosmos, the living heart of autonomous creation.
    """

    def execute(self, request: AgentRequest) -> ScaffoldResult:
        start_time = time.monotonic()
        self.console.rule(f"[bold magenta]Gnostic Agent Awakened. Mission: [cyan]{request.mission}[/cyan]")

        # --- MOVEMENT I: THE GNOSTIC ANCHOR (SAFETY INQUEST) ---
        if not (self.project_root / ".git").is_dir():
            raise ArtisanHeresy(
                "The Agent must be summoned within a Git sanctum.",
                suggestion="Please run `git init` to consecrate this reality before awakening the Agent."
            )

        try:
            # --- MOVEMENT II: THE DIVINE DELEGATION ---
            engine = AgenticEngine(
                mission=request.mission,
                project_root=self.project_root,
                engine=self.engine,
                interactive=request.interactive
            )

            # This blocks until the mission is complete, failed, or aborted.
            final_state = engine.run_loop()

            # --- MOVEMENT III: THE FINAL ADJUDICATION & PROCLAMATION ---
            duration = time.monotonic() - start_time
            if final_state.is_complete:
                # [FACULTY 7] The Artifact Hoarder
                # We perform a final gaze to determine what the agent has wrought.
                # This is a humble gaze; a future ascension would have the Agent self-report.
                artifacts = self._perceive_artifacts(start_time)

                # [FACULTY 5 & 6] The Luminous Herald of Apotheosis
                self._proclaim_success(request, final_state, duration, artifacts)

                return self.success(
                    final_state.final_result or "Mission accomplished.",
                    artifacts=artifacts,
                    data={"cycles": final_state.current_cycle, "duration": duration}
                )
            else:
                return self.failure(
                    final_state.final_result or "Mission failed to achieve its objective.",
                    data={"cycles": final_state.current_cycle, "duration": duration}
                )
        except Exception as e:
            # [FACULTY 8] The Heresy Transmuter
            if isinstance(e, ArtisanHeresy):
                raise e
            raise ArtisanHeresy("A catastrophic paradox shattered the Agent's reality.", child_heresy=e)

    def _perceive_artifacts(self, start_time: float) -> List[Artifact]:
        """A Gnostic Gaze to find scriptures touched by the Agent's hand."""
        artifacts = []
        try:
            # We use `git status` as the source of truth for what has changed.
            import subprocess
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=self.project_root, text=True
            ).strip()

            if not status_output:
                return []

            for line in status_output.splitlines():
                status, path_str = line[:2].strip(), line[3:]
                action = "modified"
                if status == "A" or status == "??":
                    action = "created"

                artifacts.append(Artifact(path=Path(path_str), type="file", action=action))

        except Exception:
            # Fallback to a simple mtime check if git fails
            for p in self.project_root.rglob("*"):
                if p.is_file() and p.stat().st_mtime > start_time:
                    artifacts.append(Artifact(path=p, type="file", action="modified"))

        return artifacts

    def _proclaim_success(self, request: AgentRequest, state: "AgentState", duration: float, artifacts: List[Artifact]):
        """[FACULTY 5] Summons the universal scribe."""

        # Forge ephemeral registers for the Dossier Scribe
        registers = SimpleNamespace(
            get_duration=lambda: duration,
            files_forged=len([a for a in artifacts if a.action == "created"]),
            sanctums_forged=0,  # The agent doesn't report this yet
            bytes_written=0,  # Not easily known without more Gnosis
            no_edicts=True,
        )

        gnosis_context = {
            "mission": request.mission,
            "cycles_taken": state.current_cycle,
            "final_thought": state.final_result
        }

        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis=gnosis_context,
            project_root=self.project_root,
            next_steps=[
                "Review the changes: [bold]git diff[/bold]",
                "Enshrine the work: [bold]scaffold save 'feat(agent): Accomplished mission'[/bold]"
            ],
            title="✨ Agentic Symphony Complete ✨",
            subtitle=f"The mission '[cyan]{request.mission[:50]}...[/cyan]' has been made manifest.",
            gnostic_constellation=artifacts
        )