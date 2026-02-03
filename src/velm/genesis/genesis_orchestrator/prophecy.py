# Path: genesis/genesis_orchestrator/prophecy.py
# ----------------------------------------------
from pathlib import Path
from typing import List, Tuple, Dict, Optional, TYPE_CHECKING

from rich.text import Text

from ..genesis_grimoires import GENESIS_GRIMOIRE
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from ...core.alchemist import get_alchemist
from ...logger import Scribe
from ...utils import is_git_installed, to_string_safe
import shutil

if TYPE_CHECKING:
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GenesisProphecy")


class ProphecyMixin:
    """
    =================================================================================
    == THE PROPHET OF THE GENESIS ENGINE (V-Ω-PROPHETIC-LAYER)                     ==
    =================================================================================
    Handles the translation of Gnosis into Structural Plans and Commands.
    """

    def _prophesy_commands(self: 'GenesisDialogueOrchestrator', gnosis: Dict) -> List[str]:
        """
        [THE ORACLE OF THE MAESTRO'S WILL]
        Generates post-run shell commands based on the gathered Gnosis.
        """
        Logger.verbose("Oracle of the Maestro's Will awakens...")
        commands = []
        project_slug = self.current_project_slug
        initial_commit_message = to_string_safe(
            gnosis.get('initial_commit_message', f"feat: Initial {gnosis.get('project_name')} project setup"))

        # Git Rites
        if gnosis.get('use_git'):
            if is_git_installed():
                commands.append("git init")
                commands.append("git add .")
                commands.append(f"git commit -m \"{initial_commit_message}\"")
            else:
                Logger.warn(
                    "Gaze of the Prudent Guardian: `git` artisan is a void. The Git-related Maestro's Edicts have been stayed.")

        # Toolchain Rites
        if gnosis.get('project_type') == 'python':
            if gnosis.get('use_poetry'):
                if shutil.which("poetry"):
                    commands.append("poetry install")
                else:
                    Logger.warn(
                        "Gaze of the Prudent Guardian: `poetry` artisan is a void. The 'poetry install' edict has been stayed.")
            else:
                if shutil.which("python"):
                    import platform
                    activate_script = "venv\\Scripts\\activate" if platform.system() == "Windows" else "source venv/bin/activate"
                    commands.append(f"python -m venv venv && {activate_script} && pip install -r requirements.txt")
                else:
                    Logger.warn(
                        "Gaze of the Prudent Guardian: `python` artisan is a void. The 'venv' and 'pip' edicts have been stayed.")

        elif gnosis.get('project_type') == 'node' and shutil.which("npm"):
            commands.append("npm install")

        if gnosis.get('use_docker') and shutil.which('docker'):
            commands.append(f"docker build -t {project_slug}:latest .")

        Logger.info(f"Maestro's Oracle has prophesied {len(commands)} pure and executable edict(s).")
        return commands

    def _prophesy_structure(self: 'GenesisDialogueOrchestrator', gnosis: Dict) -> Tuple[List[ScaffoldItem], List[Dict]]:
        """
        [THE HYPER-SENTIENT AI PROPHET]
        Translates the GENESIS_GRIMOIRE into a list of ScaffoldItems and a Review Dossier.

        *** GNOSTIC HEALING APPLIED ***
        The Alchemist is now summoned to transmute the path templates (e.g., `{{project_slug}}/src/`)
        into concrete reality paths BEFORE forging the ScaffoldItem. The Heresy of the Untransmuted Path is annihilated.
        """
        Logger.verbose("The Hyper-Sentient AI Prophet (V-Ω-LEGENDARY++) awakens...")
        items: List[ScaffoldItem] = []
        prophecies_for_review: List[Dict] = []

        alchemist = get_alchemist()

        # [THE FIX] Ensure 'project_slug' is explicitly in the context as 'slug'
        # The Grimoire uses {{slug}}, so we map it.
        alchemical_context = gnosis.copy()
        alchemical_context['slug'] = self.current_project_slug
        alchemical_context['project_slug'] = self.current_project_slug

        # [DIAGNOSTIC] Log the context used for transmutation
        Logger.verbose(f"Alchemical Context for Structure: slug='{alchemical_context.get('slug')}'")

        from ...artisans.template_engine import TemplateEngine
        template_engine = TemplateEngine()

        for prophecy in GENESIS_GRIMOIRE:
            try:
                if prophecy["adjudicator"](gnosis):
                    item_path_template = prophecy["path"]

                    # [THE DIVINE HEALING: RITE OF PATH TRANSMUTATION]
                    # We transmute the template path into a concrete path using the Alchemist.
                    final_path_str = alchemist.transmute(item_path_template, alchemical_context)

                    # [SAFETY CHECK] If transmutation failed, it might still contain braces
                    if "{{" in final_path_str:
                        Logger.warn(
                            f"Transmutation incomplete for '{item_path_template}'. Result: '{final_path_str}'. Attempting to proceed but IOController may reject.")

                    item_path = Path(final_path_str)
                    is_dir = prophecy.get("is_dir", final_path_str.endswith('/'))

                    content: Optional[str] = None
                    soul_origin: str = "From Template Forge"

                    content_rite = prophecy.get("content_rite")

                    if content_rite:
                        # Gaze 1: Alchemical Rite
                        content = content_rite(gnosis, self.current_project_slug)
                        soul_origin = "With Synthesized Content"
                    elif not is_dir:
                        # Gaze 2: Celestial Soul (Template Forge)
                        template_gnosis = template_engine.perform_gaze(item_path, alchemical_context)
                        if template_gnosis:
                            content = template_gnosis.content
                            soul_origin = f"From Forge ({template_gnosis.gaze_tier})"
                        else:
                            # If no template found, and no content rite, it is an Empty Scripture (Void)
                            soul_origin = "Void (Empty File)"

                    final_item = ScaffoldItem(
                        path=item_path,
                        is_dir=is_dir,
                        content=content.strip() if content else None
                    )
                    items.append(final_item)

                    # Review Dossier
                    review_info = prophecy.get("review", {})
                    prophecies_for_review.append({
                        "type": "Sanctum" if is_dir else "Scripture",
                        "path": str(item_path),
                        "description": Text(
                            review_info.get("description", "Auto-prophesied based on Architect's will.")),
                        "action": soul_origin,
                        "severity": review_info.get("severity", "info")
                    })

            except Exception as e:
                heresy = Heresy(
                    message=f"A paradox occurred while prophesying '{prophecy.get('key', 'unknown')}': {type(e).__name__}: {e}",
                    line_num=0,
                    line_content=f"Prophecy: {prophecy}",
                    severity=HeresySeverity.WARNING
                )
                self.adjudicated_heresies.append(heresy)
                Logger.warn(heresy.message)

        Logger.info(f"The AI Prophet has forged a Gnostic Plan of {len(items)} items.")
        return items, prophecies_for_review

    def _forge_gnostic_plan(self: 'GenesisDialogueOrchestrator') -> List[ScaffoldItem]:
        """
        [THE RITE OF TRANSLATION]
        Direct translation of Grimoire to Plan (used by Pad/API).
        """
        plan, _ = self._prophesy_structure(self.final_gnosis)
        return plan