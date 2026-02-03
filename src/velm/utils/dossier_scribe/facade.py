# Path: scaffold/utils/dossier_scribe/facade.py
# ---------------------------------------------

from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.style import Style

# --- THE DIVINE SUMMONS OF THE SUB-SCRIBES ---
from .telemetry_grid import TelemetryScribe
from .prophecy_panel import ProphecyScribe as NextStepScribe
from .mentorship_scribe import MentorshipScribe
from .constellation import ConstellationScribe
from .security_scribe import SecurityScribe
from ...interfaces.base import Artifact
from ...logger import get_console, Scribe
from ...banners import get_project_sigil

Logger = Scribe("DossierFacade")


class AuditScribe:
    """
    =============================================================================
    == THE SILENT RECORDER (V-Ω-JSON-ARCHIVIST)                                ==
    =============================================================================
    Serializes the complete Gnostic Dossier to a persistent file (JSON).
    This ensures that the history of the rite is preserved even if the terminal
    fades.
    """

    def inscribe(self, path: Path, data: Dict[str, Any]):
        try:
            # Ensure the path exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Serialize with a default handler for non-JSON types (like Path)
            content = json.dumps(data, indent=2, default=str)
            path.write_text(content, encoding="utf-8")
            Logger.verbose(f"Audit log inscribed at: {path}")
        except Exception as e:
            Logger.warn(f"Audit Scribe faltered: {e}")


class DossierScribe:
    """
    =================================================================================
    == THE HIGH PRIEST OF THE FINAL PROCLAMATION (V-Ω-FACADE-ULTIMA-ROBUST)        ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE VOICE)

    The Orchestrator of the Visual Symphony. It gathers the fragmented Gnosis from
    all specialist Scribes and weaves them into a single, luminous tapestry of Truth.

    It is now **Future-Proof**. It accepts any Gnosis offered to it, discarding nothing,
    shattering never.
    """

    def __init__(
            self,
            *,
            # --- Core Data Sources ---
            telemetry_source: Any = None,
            registers: Any = None,  # [THE FIX] Alias for telemetry_source
            gnosis: Optional[Dict[str, Any]] = None,

            # --- Context ---
            project_root: Optional[Path] = None,
            session_id: Optional[str] = None,  # [FUTURE] For session tracking
            architect_name: Optional[str] = None,  # [FUTURE] For personalization

            # --- Narrative Control ---
            title: str = '✨ Rite Complete ✨',
            subtitle: str = "The Architect's will is manifest.",
            next_steps: Optional[List[str]] = None,

            # --- Visual Components ---
            gnostic_constellation: Optional[List[Artifact]] = None,
            mentorship_guidance: Optional[List[str]] = None,  # Alias
            mentors_guidance: Optional[List[str]] = None,  # Alias
            security_warnings: Optional[List[str]] = None,
            transmutation_plan: Optional[Dict] = None,

            # --- Metrics & Telemetry ---
            ai_telemetry: Optional[Dict[str, Any]] = None,
            environment_gnosis: Optional[Dict[str, Any]] = None,
            performance_metrics: Optional[Dict[str, float]] = None,

            # --- External Links ---
            git_repo_url: Optional[str] = None,
            audit_file_path: Optional[Path] = None,

            # --- Execution Details ---
            maestro_edicts: Optional[List[str]] = None,

            # --- Infrastructure ---
            console: Optional[Console] = None,
            visual_style: str = "default",  # [FUTURE] For theming
            tags: Optional[List[str]] = None,  # [FUTURE] For categorization

            # --- THE VOID SUMP (The Unbreakable Ward) ---
            **kwargs: Any
    ):
        """
        The Rite of Inception.
        """
        self.console = console or get_console()

        # [THE UNIFICATION OF ALIASES]
        self.telemetry_source = telemetry_source or registers
        self.mentors_guidance = mentors_guidance or mentorship_guidance

        self.gnosis = gnosis or {}
        self.project_root = project_root or Path.cwd()
        self.title = title
        self.subtitle = subtitle
        self.next_steps = next_steps

        self.gnostic_constellation = gnostic_constellation
        self.security_warnings = security_warnings
        self.transmutation_plan = transmutation_plan

        self.ai_telemetry = ai_telemetry
        self.environment_gnosis = environment_gnosis
        self.performance_metrics = performance_metrics

        self.git_repo_url = git_repo_url
        self.audit_file_path = audit_file_path
        self.maestro_edicts = maestro_edicts

        # [THE ABSORPTION OF THE UNKNOWN]
        if kwargs:
            Logger.verbose(f"DossierScribe absorbed unknown Gnosis: {list(kwargs.keys())}")
            self.extra_gnosis = kwargs
        else:
            self.extra_gnosis = {}

        # Summon the Sub-Scribes
        self.telemetry_scribe = TelemetryScribe(
            telemetry_source=self.telemetry_source,
            gnosis=self.gnosis,
            project_root=self.project_root,
            transmutation_plan=self.transmutation_plan,
            ai_telemetry=self.ai_telemetry,
            environment_gnosis=self.environment_gnosis,
            performance_metrics=self.performance_metrics
        )

        self.next_step_scribe = NextStepScribe(self.next_steps)

        self.constellation_scribe = ConstellationScribe(
            artifacts=self.gnostic_constellation,
            project_root=self.project_root,
            generate_arch_doc=False,  # We keep this lightweight for the summary
        )

        self.mentorship_scribe = MentorshipScribe(self.mentors_guidance)
        self.security_scribe = SecurityScribe(self.security_warnings)

        self.audit_scribe = AuditScribe()

    def render(self) -> RenderableType:
        """Composes the final visual layout."""
        layout_groups = []

        # 1. The Header (Sigil + Title)
        header = self._forge_header()
        layout_groups.append(header)

        # 2. The Telemetry Grid (The Pulse)
        telemetry_panel = self.telemetry_scribe.forge()
        if telemetry_panel:
            layout_groups.append(telemetry_panel)

        # 3. The Security Ward (Red Alert)
        security_panel = self.security_scribe.forge()
        if security_panel:
            layout_groups.append(security_panel)

        # 4. The Gnostic Constellation (File Tree / Changes)
        # Only render if we have artifacts or a plan
        if self.gnostic_constellation or (self.transmutation_plan and any(self.transmutation_plan.values())):
            # Note: ConstellationScribe.forge() prints to console directly currently.
            # Ideally it returns a renderable. For now, we call it in proclaim().
            pass

            # 5. The Prophecy (Next Steps)
        steps_panel = self.next_step_scribe.forge()
        if steps_panel:
            layout_groups.append(steps_panel)

        # 6. The Mentor's Voice (Quotes/Advice)
        mentor_panel = self.mentorship_scribe.forge()
        if mentor_panel:
            layout_groups.append(mentor_panel)

        return Group(*layout_groups)

    def _forge_header(self) -> Panel:
        """Forges the cinematic header."""
        # Try to get project-specific sigil, else fallback
        sigil = get_project_sigil()

        title_text = Text.assemble(
            (f"\n{self.title}\n", "bold white"),
            (f"{self.subtitle}", "dim italic white")
        )

        return Panel(
            Align.center(Group(sigil, title_text)),
            border_style="cyan",
            padding=(1, 2)
        )

    def proclaim(self):
        """
        The Grand Rite of Revelation.
        Renders the dossier to the console and archives it to disk.
        """
        # 1. Render the main visual stack
        visuals = self.render()
        self.console.print(visuals)

        # 2. Render the Constellation (Tree) separately if needed
        # (Because the current TreeScribe implementation prints directly)
        if self.gnostic_constellation:
            self.console.print()
            self.constellation_scribe.forge()
            self.console.print()

        # 3. The Rite of Archival (Audit Log)
        if self.audit_file_path:
            full_dossier = {
                "timestamp": time.time(),
                "title": self.title,
                "gnosis": self.gnosis,
                "environment": self.environment_gnosis,
                "telemetry": {
                    "ai": self.ai_telemetry,
                    "performance": self.performance_metrics
                },
                "artifacts": [str(a.path) for a in (self.gnostic_constellation or [])],
                "security_warnings": self.security_warnings,
                "edicts": self.maestro_edicts
            }
            self.audit_scribe.inscribe(self.audit_file_path, full_dossier)


def proclaim_apotheosis_dossier(**kwargs):
    """
    The one true, public gateway.
    Instantiates the DossierScribe with the provided Gnosis and executes the proclamation.

    This function acts as a firewall, catching any initialization heresies
    and logging them rather than crashing the engine at the finish line.
    """
    try:
        scribe = DossierScribe(**kwargs)
        scribe.proclaim()
    except Exception as e:
        Logger.error(f"The Dossier Scribe faltered at the moment of glory: {e}", exc_info=True)
        # We perform a humble fallback proclamation
        print(f"\n[!] Rite Complete (Dossier Error: {e})\n")