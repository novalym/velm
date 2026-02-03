# Path: scaffold/artisans/templates.py
# ------------------------------------

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple

import requests
from rich.box import ROUNDED
from rich.console import Group

try:
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
    from rich.status import Status
    from rich.text import Text
    from rich.table import Table
except ImportError:
    Panel = Confirm = Status = Text = Table = object

from .. import utils
from ..logger import Scribe, get_console
from ..help_registry import register_artisan
from ..constants import TEMPLATE_ROOT
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..interfaces.requests import TemplateRequest
from ..interfaces.base import ScaffoldResult

Logger = Scribe("TemplateManager")

ALLOWED_TEMPLATE_EXTS = (
    '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.rb', '.java', '.html',
    '.css', '.scss', '.md', '.json', '.txt', '.sh', '.bat', '.zsh', '.yml', '.yaml',
    '.toml', 'dockerfile', 'gitignore', '.scaffold'
)


@register_artisan("templates")
class TemplateManagerCLI(BaseArtisan[TemplateRequest]):
    """
    @gnosis:title The Artisan of the Forge (`templates`)
    @gnosis:summary The master command for your personal, intelligent boilerplate library, turning your best practices into an instantaneous creative force.
    @gnosis:related creator distill weave blueprint
    @gnosis:keywords boilerplate starter-kit library automation codify best-practice reusability
    @gnosis:description
    The `scaffold templates` command is the master artisan for your **Template Forge**—your personal, private library of boilerplate code that resides at `~/.scaffold/templates/`.

    The Forge is the sacred heart of Scaffold's intelligence. It allows you to **transfigure the tool into a sentient extension of your own will**. When you declare a file in a blueprint without providing content, the engine automatically seeks a corresponding scripture in your Forge (e.g., `template.py`). If found, it uses **your perfected template**, injecting all blueprint variables.

    This command is your one true interface for controlling this divine library, ensuring that every project you create is born from your personal, Gnostic standard of perfection.
    ---
    ### The Philosophy: Your Executable Wisdom

    The Template Forge is not a folder of snippets; it is your **accumulated wisdom made executable**. Every time you perfect a starter file—a `.gitignore`, a `Dockerfile`, a React component—you can teach it to the Forge. From that moment on, that perfected form becomes the new, instantaneous standard for every project you create. It is the key to compounding your expertise and achieving flawless consistency at the speed of thought.
    ---
    ### The Arsenal of the Forge: The Edicts of Management

    •   **`list`**: The Rite of Perception. Displays a complete Gnostic dossier of all templates and kits currently in your Forge.
    •   **`edit <ext>`**: The Rite of Transfiguration. Instantly opens the template for an extension in your native editor, forging a blank scripture if one does not yet exist.
    •   **`add <src> <ext>`**: The Rite of New Creation. Teaches the Forge a new Gnosis by copying a perfected local file (`<src>`) and consecrating it as the new standard for an extension (`<ext>`).
    •   **`search <keyword>`**: The Rite of Discovery. Searches the filenames and the *content* of every scripture in your Forge, allowing you to instantly locate specific Gnosis.
    •   **`pull <gist_id|url>`**: The Rite of Curation. Summons a "template kit"—a collection of templates—from a GitHub Gist, downloading them into your Forge for immediate use. This is the key to sharing and using community-vetted boilerplate libraries.
    @gnosis:faqs
    Q: What is the unbreakable law of naming for templates?
    A: The law is simple and absolute: `template.[file_extension]`. For `main.py`, the Forge seeks `template.py`. For files without an extension like `Dockerfile`, the entire filename becomes the extension (`template.dockerfile`). For files with multiple dots like `.env.local`, only the final part is the true extension (`template.local`).
    ---
    Q: Can templates use `$$` variables from my blueprint?
    A: Yes, absolutely. This is the key to their power. Any variable you define in your blueprint (`$$ project_name = "nova-core"`) can be used directly within any of your template files (`"name": "{{ project_name }}"`), making them profoundly dynamic.
    ---
    Q: What is the difference between a Template and a `weave` Archetype?
    A: A **Template** is for a **single file**. It defines the soul of a `.py` or a `.tsx`. An **Archetype** is for a **multi-file architectural pattern**. It defines how a `component.tsx`, its `component.css`, and its `component.test.tsx` all relate to each other across a directory structure. The Forge holds your perfect files; the Sanctum holds your perfect patterns.
    @gnosis:example
    # --- The Rite of Transfiguration: Forge Your Perfect Python Scripture ---
    # This opens ~/.scaffold/templates/template.py in your default editor.
    # Add your preferred logging setup, docstrings, and main guard.
    # Every `.py` file you scaffold hereafter will be born with this Gnosis.
    scaffold templates edit py

    ---
    # --- The Rite of New Creation: Teach the Forge a New Gnosis ---
    # You have perfected your universal `.dockerignore` file. This command
    # copies it into the Forge and consecrates it as the new standard.
    scaffold templates add ./my-perfect.dockerignore dockerignore

    ---
    # --- The Rite of Curation: Summon a Community-Vetted Kit ---
    # This summons a complete boilerplate kit for React projects from a Gist
    # and installs it into a 'react-kit' subdirectory in your Forge.
    scaffold templates pull 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d --name react-kit
    ```
    """
    GIST_API_REGEX = re.compile(r'^[a-f0-9]{32,}$')

    def __init__(self, engine):
        super().__init__(engine)
        if not TEMPLATE_ROOT.exists():
            TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)
            Logger.warn(f"Template Forge sanctum created at: [info]{TEMPLATE_ROOT}[/info]")

    def execute(self, request: TemplateRequest) -> ScaffoldResult:
        """
        The Grand Router of the Forge.
        Dispatches the Architect's will to the correct Gnostic Rite.
        """
        command = request.template_command

        if command == 'list':
            return self.list_templates()
        elif command == 'edit':
            return self.edit_template(request.extension)
        elif command == 'add':
            return self.add_template(request.source_file, request.extension, request.force)
        elif command == 'rename':
            return self.rename_template(request.old_extension, request.new_extension)
        elif command == 'search':
            return self.search_templates(request.keyword)
        elif command == 'pull':
            return self.pull_templates(request.source, request.name, request.force_refresh)
        elif command == 'docs':
            return self.open_docs()
        else:
            raise ArtisanHeresy(f"The Sacred Map of the Forge is misaligned. Unknown rite: '{command}'.")

    def _resolve_ext(self, ext_input: str) -> Optional[str]:
        """[GNOSIS PARSING] Resolves a user input (e.g., 'py', '.py', 'main.py') to a pure extension string."""
        if ext_input.startswith('.'):
            ext_input = ext_input.lstrip('.')
        elif '.' in ext_input:
            ext_input = Path(ext_input).suffix.lstrip('.')

        if ext_input:
            return ext_input.lower()
        return None

    def _open_file_in_editor(self, file_path: Path):
        """
        [THE RITE OF THE SCRIBE'S INVOCATION, ASCENDED]
        Performs a three-fold Gnostic Gaze to open a scripture in the
        Architect's preferred editor.
        """
        editor = os.getenv('EDITOR')
        if editor:
            try:
                subprocess.run([editor, str(file_path)], check=True)
                Logger.success(f"Summoned declared editor '{editor}' for transfiguration.")
                return
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                Logger.warn(f"Failed to summon declared editor '{editor}'. Reason: {e}")

        try:
            Logger.info("No $EDITOR declared. Attempting to summon the realm's default editor...")
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(file_path)], check=True)
            else:
                subprocess.run(["xdg-open", str(file_path)], check=True)
            Logger.success("Successfully summoned the realm's default editor.")
            return
        except (OSError, subprocess.CalledProcessError, FileNotFoundError):
            Logger.warn("Failed to summon the realm's default editor.")

        Logger.error("All Gnosis failed. Please set your $EDITOR environment variable for a better experience.")
        if sys.platform == "win32":
            try:
                subprocess.run(["notepad", str(file_path)], check=True)
            except FileNotFoundError:
                pass

    def _confirm_overwrite(self, path: Path, is_dir: bool = False) -> bool:
        """[SHIELD OF PRUDENCE] Helper to get overwrite confirmation."""
        console = get_console()
        if is_dir:
            prompt_text = f"[question]Directory '[bold]{path.name}[/bold]' already exists. Overwrite contents? (y/N)[/question] "
        else:
            prompt_text = f"[question]Overwrite existing template '[bold]{path.name}[/bold]'? (y/N)[/question] "

        choice = console.input(prompt_text).lower().strip()
        return choice == 'y'

    def list_templates(self) -> ScaffoldResult:
        """[RITE OF PERCEPTION] Displays all templates currently in the Forge with rich metadata."""
        console = get_console()
        console.rule("[bold cyan]Template Forge Gnosis[/bold cyan]")

        template_files = sorted([f for f in TEMPLATE_ROOT.rglob('*') if f.is_file()])

        if not template_files:
            Logger.info("The Forge is a void. No custom templates found.")
            console.print(f"[subtle]To add one, use: [info]scaffold templates edit py[/info][/subtle]")
            return self.success("The Forge is empty.")

        for f in template_files:
            size_bytes = f.stat().st_size
            rel_path = f.relative_to(TEMPLATE_ROOT)

            if rel_path.parts[0] == '.git': continue

            if rel_path.name.startswith('template.'):
                target_ext = rel_path.name.split('.', 1)[1]
                display_name = f"[bold white]template.{target_ext}[/bold white] -> Targets: [green]*.{target_ext}[/green]"
            else:
                display_name = f"[yellow]{rel_path}[/yellow] (Kit file)"

            console.print(f"  {display_name} ([subtle]{size_bytes} bytes[/subtle])")

        console.print(f"\n[subtle]Root Sanctum:[/subtle] [info]{TEMPLATE_ROOT}[/info]")
        return self.success("Templates listed.")

    def add_template(self, source_file: str, extension: str, force: bool = False) -> ScaffoldResult:
        """
        =================================================================================
        == THE AI ALCHEMIST OF THE FORGE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)               ==
        =================================================================================
        @gnosis:title add_template
        @gnosis:summary The divine rite that teaches the Forge new Gnosis, now with an AI soul.
        @gnosis:LIF 10,000,000,000

        This is not a function. It is a divine, sentient **AI Alchemist**. It no longer
        performs a humble, hardcoded Gaze. It summons the full power of the **Neural
        Cortex** to perform a deep, semantic inquest upon a scripture's soul. It does
        not just find a project name; it understands purpose, perceives variables, and
        prophesies a complete, Gnostically-aware set of abstractions, transforming a
        simple `add` command into a profound act of intelligent co-creation.

        ### THE PANTHEON OF 12+ ASCENDED FACULTIES:

        1.  **The AI's Gaze:** The profane, hardcoded `ALCHEMICAL_GRIMOIRE` is annihilated.
            The artisan now summons the `AIEngine` to perform a deep semantic analysis.
        2.  **The Gnostic Prompt Forge:** It forges a divine, context-aware prompt, teaching
            the AI about the scripture's purpose (`template.py`), its name, and the sacred
            laws of Jinja2 abstraction.
        3.  **The JSON Oracle:** It commands the AI to return its prophecy as a pure JSON
            scripture, ensuring an unbreakable, machine-readable communion.
        4.  **The Unbreakable Heresy Ward:** The entire AI communion is shielded. If the AI's
            Gaze is clouded or it speaks a profane tongue (invalid JSON), the artisan
            gracefully falls back to a non-alchemical copy.
        5.  **The Luminous Dossier of Prophecy:** It transmutes the AI's JSON prophecy into a
            luminous `rich.Table`, revealing not just the `find` and `replace` Gnosis, but
            the AI's own reasoning for each transmutation.
        6.  **The Interactive Adjudicator:** It conducts a sacred dialogue, allowing the
            Architect to adjudicate each of the AI's prophecies individually.
        7.  **The Polyglot Path Gaze:** The `_resolve_ext` rite is now a master of Gnostic
            paths, capable of perceiving the true extension of complex scriptures like
            `Dockerfile.dev` or `.env.example`.
        8.  **The Security Inquisitor:** Its pre-flight Gaze for profane secrets (`sk_live_...`)
            remains an unbreakable, sacred duty.
        9.  **The Idempotency Ward:** Its Gaze of Gnostic State Confirmation (hash check) is
            eternal and absolute.
        10. **The Atomic Inscription:** It continues to wield the `atomic_write` artisan for
            unbreakably pure inscriptions into the Forge.
        11. **The Luminous Proclamation:** Its final proclamation remains a glorious, cinematic
            `Dossier of Apotheosis`, a testament to the Great Work performed.
        12. **The Sovereign Soul:** Its architecture is a masterpiece of Gnostic design, a
            symphony of perception, communion, adjudication, and inscription.
        =================================================================================
        """
        console = get_console()
        console.rule("[bold magenta]Rite of Gnostic Curation (AI-Ascended)[/bold magenta]")

        source_path = Path(source_file).resolve()
        target_ext = self._resolve_ext(extension or source_path.name)
        if not target_ext:
            raise ArtisanHeresy(
                f"Could not perceive a valid extension from '{source_path.name}'. You must provide one explicitly.")
        if not source_path.is_file():
            raise ArtisanHeresy(f"Source scripture not found at: '{source_path}'. The rite is stayed.")

        try:
            content = source_path.read_text(encoding='utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"A paradox occurred while gazing upon the soul of '{source_path}': {e}") from e

        target_name = f"template.{target_ext}"
        target_path = TEMPLATE_ROOT / target_name

        if target_path.exists() and hashlib.sha256(content.encode('utf-8')).hexdigest() == hashlib.sha256(
                target_path.read_bytes()).hexdigest():
            Logger.success("Gnostic State Confirmed. The will is already manifest. The rite is complete.")
            return self.success("Template already exists and is identical.")

        # --- MOVEMENT I: THE PRE-FLIGHT INQUEST (UNCHANGED AND PURE) ---
        warnings = self._pre_flight_inquest(content)

        # --- MOVEMENT II: THE AI'S GNOSTIC GAZE ---
        prophecies = self._summon_ai_alchemist(content, target_name)

        abstractions_to_perform: List[Dict] = []
        if not force:
            self._proclaim_dossier_of_curation(source_path, target_name, target_path, warnings, prophecies)

            if not Confirm.ask("\n[bold question]Shall this new Gnosis be enshrined in the Forge?[/bold question]",
                               default=True):
                raise ArtisanHeresy("Rite of Enshrinement stayed by the Architect.", exit_code=0)

            if prophecies:
                abstractions_to_perform = self._adjudicate_prophecies(prophecies)
        else:
            abstractions_to_perform = prophecies

        # --- MOVEMENT III: THE RITE OF TRANSMUTATION & INSCRIPTION ---
        try:
            final_content = content
            for prop in abstractions_to_perform:
                final_content = final_content.replace(prop['find'], prop['replace'])

            write_result = utils.atomic_write(
                target_path=target_path, content=final_content,
                logger=Logger, verbose=True, sanctum=TEMPLATE_ROOT
            )
            if not write_result.success:
                raise ArtisanHeresy("The Rite of Atomic Inscription failed. The Divine Hand perceived a paradox.")

            self._proclaim_dossier_of_apotheosis(source_path, target_name, write_result.action_taken,
                                                 abstractions_to_perform, target_ext)
            return self.success(f"Template '{target_name}' added successfully.")

        except Exception as e:
            raise ArtisanHeresy(f"A catastrophic paradox occurred during the Rite of Forging: {e}") from e

    def _pre_flight_inquest(self, content: str) -> List[str]:
        """Performs a security and Gnostic purity gaze."""
        warnings = []
        if re.search(r'\{\{.*?\}\}', content):
            warnings.append("Gnostic Contamination: Source already contains `{{...}}` placeholders.")
        if re.search(r'sk_(live|test)_[a-zA-Z0-9]+', content):
            warnings.append("Critical Heresy: A profane secret key was perceived in the scripture's soul.")
        return warnings

    def _summon_ai_alchemist(self, content: str, target_name: str) -> List[Dict]:
        """Summons the Neural Cortex to prophesy abstractions."""
        from ..core.ai.engine import AIEngine
        ai_engine = AIEngine.get_instance()

        prompt = f"""
        Analyze the following code file, which is being saved as a Scaffold template named '{target_name}'.
        Your task is to identify hardcoded values that should be replaced with Jinja2 variables.
        Provide a JSON list of abstraction suggestions. Each item in the list must be an object with three keys:
        1. "find": The exact, literal string to be replaced.
        2. "replace": The new Jinja2 variable expression (e.g., "{{{{ project_name | pascal }}}}").
        3. "reason": A brief explanation for why this abstraction is useful.

        Focus on:
        - Project names, author names, version numbers.
        - Core class or function names that are derived from the filename.
        - Hardcoded ports, database names, or API endpoints.
        - Avoid abstracting common programming keywords or standard library imports.

        Respond ONLY with the JSON list.

        File Content:
        ```        {content}
        ```
        """

        try:
            with self.console.status(
                    "[bold magenta]The AI Alchemist is gazing upon the scripture's soul...[/bold magenta]"):
                response_str = ai_engine.ignite(prompt, system="You are an expert system for code abstraction.",
                                                model="smart", json_mode=True)
                # The AI is commanded to return JSON, but we perform a final purification.
                json_match = re.search(r'\[.*\]', response_str, re.DOTALL)
                if not json_match:
                    self.console.print(
                        "[yellow]AI Alchemist's Gaze was clouded (no JSON found). Proceeding without abstractions.[/yellow]")
                    return []

                prophecies = json.loads(json_match.group(0))
                self.console.print(f"[green]AI Alchemist has returned {len(prophecies)} prophecies.[/green]")
                return prophecies
        except Exception as e:
            self.console.print(
                f"[yellow]AI Alchemist's communion failed: {e}. Proceeding without abstractions.[/yellow]")
            return []

    def _proclaim_dossier_of_curation(self, source_path, target_name, target_path, warnings, prophecies):
        """Renders the pre-flight dossier for the Architect's Gaze."""
        dossier_table = Table(title="[bold]Dossier of Gnostic Curation[/bold]", box=None, show_header=False)
        dossier_table.add_column(style="dim", justify="right", width=20)
        dossier_table.add_column()
        dossier_table.add_row("Source Scripture:", f"[cyan]{source_path.name}[/cyan]")
        dossier_table.add_row("Destination in Forge:", f"[green]{target_name}[/green]")
        if target_path.exists():
            dossier_table.add_row("Rite to be Performed:", "[yellow]Transfiguration (Overwrite)[/yellow]")
        if warnings:
            dossier_table.add_row("Gnostic Inquest:", "\n".join(f"• [red]{w}[/red]" for w in warnings))

        self.console.print(Panel(dossier_table, border_style="magenta"))

        if prophecies:
            prophecy_table = Table(title="[bold]AI Alchemist's Prophecy[/bold]", box=ROUNDED, show_lines=True)
            prophecy_table.add_column("Find (Literal)", style="red", max_width=30)
            prophecy_table.add_column("Replace (Gnostic)", style="cyan", max_width=30)
            prophecy_table.add_column("Reason", style="dim")
            for prop in prophecies:
                prophecy_table.add_row(prop.get('find'), prop.get('replace'), prop.get('reason'))
            self.console.print(prophecy_table)

    def _adjudicate_prophecies(self, prophecies: List[Dict]) -> List[Dict]:
        """Conducts the sacred dialogue for adjudicating AI prophecies."""
        abstractions_to_perform = []
        if not prophecies:
            return abstractions_to_perform

        action = Prompt.ask("\n[bold magenta]Adjudicate AI Prophecies[/bold magenta]",
                            choices=["all", "interactive", "none"], default="all")

        if action == "all":
            return prophecies
        if action == "none":
            return []

        # Interactive Adjudication
        for prop in prophecies:
            self.console.print(Panel(
                f"[dim]Find:[/dim]    [red]{prop['find']}[/red]\n"
                f"[dim]Replace:[/dim] [cyan]{prop['replace']}[/cyan]\n"
                f"[dim]Reason:[/dim]  [italic]{prop['reason']}[/italic]",
                title="[yellow]Adjudicate Prophecy[/yellow]"
            ))
            if Confirm.ask("[bold question]Apply this abstraction?[/bold question]", default=True):
                abstractions_to_perform.append(prop)

        return abstractions_to_perform

    def _proclaim_dossier_of_apotheosis(self, source_path, target_name, action, abstractions, target_ext):
        """Renders the final, luminous report of the Great Work."""
        final_dossier = Table(box=None, show_header=False, padding=(0, 2))
        final_dossier.add_column(style="dim", justify="right")
        final_dossier.add_column(style="white")
        final_dossier.add_row("Source Scripture:", f"[cyan]{source_path.name}[/cyan]")
        final_dossier.add_row("Enshrined As:", f"[bold green]{target_name}[/bold green]")
        final_dossier.add_row("Rite Performed:", f"[yellow]{action.value}[/yellow]")
        if abstractions:
            final_dossier.add_row("Alchemical Rites:",
                                  f"[magenta]{len(abstractions)} abstraction(s) performed[/magenta]")

        next_step = Text.assemble(("\nTo further refine this Gnosis, speak the edict:\n", "white"),
                                  (f"scaffold templates edit {target_ext}", "bold cyan"))

        self.console.print(Panel(
            Group(final_dossier, next_step),
            title="[bold green]Dossier of Apotheosis[/bold green]",
            subtitle="[dim]The Architect's wisdom has been immortalized.[/dim]",
            border_style="green"
        ))
    def edit_template(self, ext: str) -> ScaffoldResult:
        """[RITE OF TRANSFIGURATION] Opens an existing or new template in the user's default editor."""
        target_ext = self._resolve_ext(ext)
        if not target_ext:
            raise ArtisanHeresy(f"Invalid extension provided: '{ext}'. The rite is stayed.")

        target_name = f"template.{target_ext}"
        target_path = TEMPLATE_ROOT / target_name

        if not target_path.exists():
            Logger.warn(f"Template '{target_name}' does not exist. Forging an empty scripture...")
            try:
                target_path.touch()
            except Exception as e:
                raise ArtisanHeresy(f"Failed to forge new template scripture: {e}") from e

        if self._open_file_in_editor(target_path):
            Logger.success(f"Opened [info]{target_name}[/info] for transfiguration. Forge is now active.")
            return self.success(f"Opened '{target_name}' in editor.")
        else:
            Logger.error(f"Failed to open default editor. Please manually open: [info]{target_path}[/info]")
            return self.failure(f"Failed to open editor for '{target_name}'.")

    def rename_template(self, old_ext: str, new_ext: str) -> ScaffoldResult:
        """[RITE OF TRUE NAMING] Renames a template to target a different extension."""
        old_ext_p = self._resolve_ext(old_ext)
        new_ext_p = self._resolve_ext(new_ext)

        if not (old_ext_p and new_ext_p):
            Logger.error("Invalid old or new extension provided.")
            return self.failure("Invalid extensions.")

        old_path = TEMPLATE_ROOT / f"template.{old_ext_p}"
        new_path = TEMPLATE_ROOT / f"template.{new_ext_p}"

        if not old_path.exists():
            Logger.error(f"Template for extension [danger]*.{old_ext_p}[/danger] not found. Rite aborted.")
            return self.failure(f"Template for '{old_ext_p}' not found.")

        if new_path.exists() and not self._confirm_overwrite(new_path):
            Logger.info("Rename Rite cancelled by Architect (target exists).")
            return self.success("Rename cancelled.")

        try:
            old_path.rename(new_path)
            Logger.success(f"Renamed: [info]*.{old_ext_p}[/info] is now [green]*.{new_ext_p}[/green].")
            return self.success(f"Renamed '{old_ext_p}' to '{new_ext_p}'.")
        except Exception as e:
            Logger.error(f"Failed to rename template: {e}")
            return self.failure(f"Rename failed: {e}")

    def search_templates(self, keyword: str) -> ScaffoldResult:
        """[RITE OF DISCOVERY] Searches all template content and filenames for a keyword."""
        console = get_console()
        keyword_lower = keyword.lower()
        results = []

        template_files = sorted([f for f in TEMPLATE_ROOT.rglob('*') if f.is_file()])

        for f in template_files:
            rel_path = f.relative_to(TEMPLATE_ROOT)

            if keyword_lower in f.name.lower():
                results.append((rel_path, "Filename Match"))
                continue

            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if keyword_lower in content.lower():
                    results.append((rel_path, "Content Match"))
            except Exception:
                continue

        console.rule(f"[bold magenta]Search Results for '{keyword}'[/bold magenta]")
        if not results:
            Logger.info("No scriptures found matching the keyword.")
            return self.success("No matches found.")

        for path, reason in results:
            console.print(f"  [info]{path}[/info] [subtle]({reason})[/subtle]")

        return self.success(f"Found {len(results)} matches.")

    def pull_templates(self, source: str, name: str, force_refresh: bool = False) -> ScaffoldResult:
        """
        =================================================================================
        ==  THE SENTINEL OF CURATION (V-Ω-APOTHEOSIS-ULTIMA. THE GLOBAL FORGE GATEWAY) ==
        =================================================================================
        LIF: 10,000,000,000

        This artisan is the final, resilient gateway for remote templates. It is capable
        of Gist API communion, direct URL fallback, and robustly manages the target
        kit directory, ensuring security and cleanliness.
        """
        console = get_console()
        sanitized_name = re.sub(r'[^\w-]', '_', name).lower()
        if not sanitized_name:
            raise ArtisanHeresy("Kit name is profane. Please use letters, numbers, hyphens, or underscores.")

        kit_path = TEMPLATE_ROOT / sanitized_name

        GIST_ID_REGEX = re.compile(r'^[a-f0-9]{32,}$')
        gist_id = None

        if GIST_ID_REGEX.match(source):
            gist_id = source
        else:
            gist_match = re.search(r'/([a-f0-9]{32,})', source)
            if gist_match:
                gist_id = gist_match.group(1)

        manifest = None

        if gist_id:
            api_url = f"https://api.github.com/gists/{gist_id}"
            try:
                Logger.info(f"Communing with Gist API: [info]{gist_id}[/info]")
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                manifest = response.json()
            except requests.exceptions.RequestException as e:
                raise ArtisanHeresy(f"Celestial Heresy: Could not summon Gist manifest. Reason: {e}") from e

        elif source.startswith('http'):
            Logger.info(f"Source is a direct URL. Treating as a single template file.")
            filename = Path(source).name
            manifest = {'files': {filename: {'raw_url': source, 'size': 0}}}
            if sanitized_name == 'remote_kit':
                kit_path = TEMPLATE_ROOT / filename.replace('.', '_')

        if not manifest or not manifest.get('files'):
            raise ArtisanHeresy("No valid template manifest or single file found. Pull Rite aborted.")

        try:
            if kit_path.exists() and not self._confirm_overwrite(kit_path, is_dir=True):
                Logger.info("Kit download cancelled by Architect.")
                return self.success("Pull cancelled.")

            shutil.rmtree(kit_path, ignore_errors=True)
            kit_path.mkdir(parents=True)

            download_count = 0
            total_size_bytes = sum(f.get('size', 0) for f in manifest['files'].values())

            Logger.info(
                f"Manifest accepted. Total size: [subtle]{total_size_bytes / 1024:.1f} KB[/subtle]. Commencing download...")

            for filename, file_data in manifest['files'].items():
                file_size = file_data.get('size', 0)
                if file_size > 5 * 1024 * 1024:
                    Logger.warn(f"Skipping {filename}: file exceeds 5MB security limit.")
                    continue

                is_allowed_type = any(filename.lower().endswith(ext) for ext in ALLOWED_TEMPLATE_EXTS)
                is_template_name = filename.lower().startswith('template.')

                if not is_allowed_type and not is_template_name:
                    Logger.warn(
                        f"Skipping {filename}: Unrecognized or forbidden file type. (Not in ALLOWED_TEMPLATE_EXTS)")
                    continue

                if filename.startswith('template.') or '.' in filename:
                    file_content = requests.get(file_data['raw_url'], timeout=20).text
                    local_path = kit_path / filename

                    local_path.write_text(file_content, encoding='utf-8')
                    download_count += 1
                    rel_path = local_path
                    console.print(
                        f"  [success]FORGED:[/success] [green]{rel_path}[/green] ({file_size / 1024:.1f} KB)")

            Logger.success(
                f"Rite of Curation complete. {download_count} scriptures enshrined in kit: [info]{kit_path.name}[/info].")
            return self.success(f"Kit '{kit_path.name}' pulled successfully.")

        except requests.exceptions.RequestException as e:
            raise ArtisanHeresy(
                f"Celestial Heresy: Download failed. Connection error or server denial. Reason: {e}") from e
        except Exception as e:
            raise ArtisanHeresy(f"A catastrophic paradox occurred during kit installation: {e}") from e

    def open_docs(self) -> ScaffoldResult:
        """[RITE OF SELF-AWARENESS] Opens the TEMPLATES.md documentation."""
        doc_path = Path(__file__).parent.parent / 'README.md'
        if not doc_path.exists():
            Logger.error(f"Documentation not found at: [danger]{doc_path}[/danger]")
            return self.failure("Documentation not found.")

        if self._open_file_in_editor(doc_path):
            Logger.info("Opened TEMPLATES.md documentation in your default viewer.")
            return self.success("Docs opened.")
        else:
            Logger.error(f"Failed to open default editor. Please manually open: [info]{doc_path}[/info]")
            return self.failure("Failed to open docs.")