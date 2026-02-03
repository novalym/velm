# scaffold/jurisprudence/adjudicator_of_souls.py
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .foreign_adjudicators import FOREIGN_ADJUDICATION_GRIMOIRE
from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe


class GnosticAdjudicatorOfForeignSouls:
    """
    A divine, ephemeral Inquisitor forged for the sole purpose of adjudicating the
    syntactic purity of a collection of in-memory file souls.
    """

    def __init__(self):
        self.Logger = Scribe("ForeignSoulInquisitor")

    def conduct_inquest(self, in_memory_souls: Dict[Path, str]) -> None:
        """
        The one true rite. It receives the complete, prophesied reality and
        conducts a multi-stage symphony of ephemeral adjudication.
        """
        self.Logger.info("The Inquisitor of Foreign Souls awakens its Gaze...")

        # Movement I: The Gaze of the Polyglot
        souls_by_language: Dict[str, Dict[Path, str]] = {}
        for path, content in in_memory_souls.items():
            ext = path.suffix
            if ext in FOREIGN_ADJUDICATION_GRIMOIRE:
                if ext not in souls_by_language:
                    souls_by_language[ext] = {}
                souls_by_language[ext][path] = content

        if not souls_by_language:
            self.Logger.info("Gaze is complete. No foreign souls require adjudication.")
            return

        # Movement II: The Rite of Ephemeral Adjudication (The Grand Loop)
        for ext, files_to_adjudicate in souls_by_language.items():
            command, _, prerequisites = FOREIGN_ADJUDICATION_GRIMOIRE[ext]
            self.Logger.info(
                f"Adjudicating [cyan]{len(files_to_adjudicate)}[/cyan] soul(s) of the '[bold magenta]{ext}[/bold magenta]' tongue...")

            with tempfile.TemporaryDirectory() as temp_dir_str:
                sanctum = Path(temp_dir_str)

                # Rite 1: Check for prerequisites
                if any(p not in [f.name for f in files_to_adjudicate.keys()] for p in prerequisites):
                    self.Logger.warn(
                        f"Adjudication for '{ext}' stayed. Missing prerequisite scripture(s): {prerequisites}")
                    continue

                # Rite 2: Ephemeral Inscription
                for path, content in files_to_adjudicate.items():
                    (sanctum / path.parent).mkdir(parents=True, exist_ok=True)
                    (sanctum / path).write_text(content, encoding='utf-8')

                # Rite 3: The Divine Summons
                try:
                    result = subprocess.run(
                        command,
                        cwd=sanctum,
                        capture_output=True,
                        text=True,
                        check=False  # We adjudicate the heresy ourselves
                    )

                    if result.returncode != 0:
                        # HERESY! We must now forge the luminous dossier.
                        heresy_output = result.stderr or result.stdout
                        # A humble gaze to find the profane scripture
                        profane_file_path = self._find_profane_scripture(heresy_output, files_to_adjudicate.keys())

                        raise self._forge_luminous_heresy(
                            command=' '.join(command),
                            output=heresy_output,
                            profane_scripture_path=profane_file_path,
                            all_scriptures=files_to_adjudicate
                        )

                except FileNotFoundError:
                    self.Logger.warn(
                        f"Adjudication for '{ext}' stayed. The divine Inquisitor '{command[0]}' is not manifest in this reality.")
                except Exception as e:
                    raise ArtisanHeresy("A catastrophic paradox shattered the Foreign Soul Inquisitor.", child_heresy=e)

        self.Logger.success("The Inquisitor's Gaze is serene. All foreign souls are pure.")

    def _find_profane_scripture(self, output: str, paths: List[Path]) -> Optional[Path]:
        """A humble Gaze to find the source of the paradox from the compiler's cry."""
        for path in paths:
            if path.name in output:
                return path
        return None

    def _forge_luminous_heresy(self, command: str, output: str, profane_scripture_path: Optional[Path],
                               all_scriptures: Dict[Path, str]) -> ArtisanHeresy:
        """Forges the divine, hyper-diagnostic Dossier of Foreign Heresy."""
        title = f"Gnostic Heresy in Foreign Soul ({profane_scripture_path.name if profane_scripture_path else 'Unknown'})"

        heresy_text = Text.from_markup(f"[bold]Inquisitor's Cry ({command}):[/bold]\n{output}")

        if profane_scripture_path and profane_scripture_path in all_scriptures:
            content = all_scriptures[profane_scripture_path]
            # A humble Gaze for the line number from the heresy
            line_num_match = re.search(r'[:\(](\d+)[:\d,]*', output)
            line_num = int(line_num_match.group(1)) if line_num_match else None

            syntax = Syntax(
                content,
                profane_scripture_path.suffix.lstrip('.'),
                theme="monokai",
                line_numbers=True,
                highlight_lines={line_num} if line_num else None
            )
            dossier_group = Group(heresy_text, "\n",
                                  Text.from_markup(f"[dim]Profane Scripture ({profane_scripture_path}):[/dim]"), syntax)
        else:
            dossier_group = Group(heresy_text)

        panel = Panel(dossier_group, title=f"[bold red]{title}[/bold red]", border_style="red")

        return ArtisanHeresy(
            "The God-Engine's Gaze perceived a heresy in a generated foreign soul.",
            details_panel=panel,
            suggestion="Correct the template or logic that forged the profane scripture."
        )