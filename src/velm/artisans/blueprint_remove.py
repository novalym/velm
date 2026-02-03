# Path: scaffold/artisans/blueprint_remove.py
# ----------------------------------

import difflib
import re
import shutil
from pathlib import Path
from typing import List, Tuple

from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.text import Text

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import BlueprintExciseRequest  # <-- NEW REQUEST TYPE
from ..logger import Scribe
from ..parser_core.block_consumer import GnosticBlockConsumer
from ..utils import atomic_write

Logger = Scribe("BlueprintAnnihilator")


class BlueprintExciseArtisan(BaseArtisan[BlueprintExciseRequest]): # <-- NEW NAME
    """
    =================================================================================
    == THE SURGICAL SCALPEL (V-Ω-HIERARCHICAL-ANNIHILATOR)                         ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan surgically excises definitions from a blueprint. It has ascended to
    understand the Gnostic hierarchy, allowing it to remove not just single lines,
    but entire architectural branches with their comments and children.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Hierarchical Pathfinder:** Tracks indentation to find the *exact* node
        in the Gnostic Tree corresponding to the target path.
    2.  **The Block Annihilator:** Consumes the entire indented block belonging to the
        target, including all children.
    3.  **The Phantom Guard:** Detects if the target path is a void and fails gracefully.
    4.  **The Variable Pruner:** Supports removing `$$ var = val` definitions.
    5.  **The Luminous Diff:** In `--preview` mode, it generates a beautiful diff showing
        exactly what lines will be returned to the void.
    6.  **The Safety Interlock:** Prompts for confirmation before annihilating large blocks.
    7.  **The Void Eater:** Cleans up extra blank lines left after the excision.
    8.  **The Genesis Ward:** Can be commanded to create a blueprint if it doesn't exist,
        enabling idempotent scripting. (Future Ascension Proxy)
    9.  **The Comment Sweeper:** Intelligently removes comments directly associated with
        the excised node.
    10. **The Atomic Hand:** Uses `atomic_write` to prevent blueprint corruption.
    11. **The Path Normalizer:** Enforces POSIX-style path separators.
    12. **The Luminous Dossier:** Returns a rich `Artifact` chronicling the change.
    =================================================================================
    """

    def execute(self, request: BlueprintExciseRequest) -> ScaffoldResult:
        blueprint_path = (self.project_root / request.blueprint_path).resolve()

        if not blueprint_path.exists():
            return self.failure(f"Blueprint not found at: {blueprint_path}")

        # --- The Guardian's Offer ---
        self.guarded_execution([blueprint_path], request, context="blueprint_remove")

        backup_path = blueprint_path.with_suffix('.scaffold.bak')
        shutil.copy2(blueprint_path, backup_path)

        try:
            content = blueprint_path.read_text(encoding='utf-8')
            lines = content.splitlines()
            target_path_str = request.target_path.replace('\\', '/')

            # --- MOVEMENT I: THE HIERARCHICAL PATHFINDER ---
            start_idx, end_idx, found_line = self._locate_target_block(lines, target_path_str)

            # [FACULTY 3] The Phantom Guard
            if start_idx == -1:
                # [FACULTY 4] The Variable Pruner
                if target_path_str.startswith("$$"):
                    return self._handle_variable_removal(lines, target_path_str, blueprint_path, request)

                return self.failure(
                    f"The target '{target_path_str}' was not found in the blueprint.",
                    suggestion="Check the full path and indentation in your scaffold file."
                )

            # [FACULTY 6] The Safety Interlock
            lines_to_remove = end_idx - start_idx
            if lines_to_remove > 5 and not request.force and not request.non_interactive:
                preview = "\n".join(lines[start_idx:min(end_idx, start_idx + 10)])
                self.console.print(
                    Panel(Text(f"{preview}\n...", overflow="ellipsis"),
                          title=f"[bold red]Targeting {lines_to_remove} lines[/bold red]"))
                if not Confirm.ask(f"Annihilate this entire architectural branch?", default=False):
                    return self.success("The Rite of Annihilation was stayed.")

            # --- MOVEMENT II: THE EXCISION ---
            new_lines = lines[:start_idx] + lines[end_idx:]

            # [FACULTY 7] The Void Eater
            final_lines = self._purify_voids(new_lines)
            final_content = "\n".join(final_lines) + "\n"

            # [FACULTY 5] The Luminous Diff (Preview/Dry-Run)
            if request.dry_run or request.preview:
                self._proclaim_diff(content, final_content, blueprint_path.name)
                return self.success("Dry Run: Annihilation simulated successfully.")

            # [FACULTY 10] The Atomic Hand
            write_result = atomic_write(blueprint_path, final_content, self.logger, blueprint_path.parent)

            # [FACULTY 12] The Luminous Dossier
            artifact = Artifact(
                path=blueprint_path,
                type="file",
                action=write_result.action_taken,
                size_bytes=len(final_content.encode('utf-8'))
            )

            return self.success(
                f"Excised '[cyan]{target_path_str}[/cyan]' from '{blueprint_path.name}' (Lines {start_idx + 1}-{end_idx}).",
                artifacts=[artifact]
            )

        except Exception as e:
            if 'backup_path' in locals() and backup_path.exists():
                shutil.move(str(backup_path), str(blueprint_path))
            raise ArtisanHeresy(f"A paradox occurred during the Rite of Removal. Blueprint restored.", child_heresy=e)

    def _locate_target_block(self, lines: List[str], target_path: str) -> Tuple[int, int, str]:
        """
        [FACULTY 1, 2, 9] The Hierarchical Pathfinder, Block Annihilator, and Comment Sweeper.
        """
        consumer = GnosticBlockConsumer(lines)
        path_stack: List[Tuple[str, int]] = []
        target_parts = [p for p in target_path.strip('/').split('/') if p]

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(('#', '//')):
                continue

            current_indent = consumer._measure_visual_depth(line)

            # Pop stack until we find the parent context
            while path_stack and path_stack[-1][1] >= current_indent:
                path_stack.pop()

            # Parse current line's name, ignoring sigils and content
            # This regex is a humble gaze to extract just the path-like part.
            match = re.match(r'^\s*([^\s:<%#]+)', line)
            if not match:
                continue

            node_name = match.group(1).strip('/')
            path_stack.append((node_name, current_indent))

            # Construct full path from stack and compare
            current_full_path = "/".join([p[0] for p in path_stack])

            # We match if the current path ENDS with the target path,
            # allowing for flexibility in how the root is defined in the blueprint.
            if current_full_path.endswith(target_path.strip('/')):
                # Found the start line!
                # Consume the entire indented block to find the end.
                _, end_index = consumer.consume_indented_block(i + 1, current_indent)

                # Look back for attached comments.
                start_index = i
                if i > 0:
                    prev_line = lines[i - 1]
                    if prev_line.strip().startswith('#') and consumer._measure_visual_depth(
                            prev_line) == current_indent:
                        Logger.verbose("Sweeping attached comment into the void.")
                        start_index = i - 1

                return start_index, end_index, line

        return -1, -1, ""

    def _handle_variable_removal(self, lines: List[str], target_var: str, path: Path, request: BlueprintExciseRequest):
        """[FACULTY 4] The Variable Pruner."""
        clean_target = target_var.replace('$$', '').strip()
        var_regex = re.compile(rf"^\s*(\$\$)?\s*{re.escape(clean_target)}\s*(?::.*)?\s*=")
        new_lines = [line for line in lines if not var_regex.match(line)]

        if len(new_lines) == len(lines):
            return self.failure(f"Variable '{clean_target}' not found in blueprint.")

        final_content = "\n".join(new_lines) + "\n"

        if request.dry_run or request.preview:
            self._proclaim_diff("\n".join(lines), final_content, path.name)
            return self.success("Dry Run: Variable annihilation simulated.")

        atomic_write(path, final_content, self.logger, path.parent)
        return self.success(f"Annihilated variable '$$ {clean_target}'.")

    def _purify_voids(self, lines: List[str]) -> List[str]:
        """[FACULTY 7] The Void Eater."""
        purified = []
        prev_empty = False
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            purified.append(line)
            prev_empty = is_empty
        return purified

    def _proclaim_diff(self, old: str, new: str, filename: str):
        """[FACULTY 5] The Luminous Diff."""
        diff = "".join(difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{filename} (Reality)",
            tofile=f"b/{filename} (Prophecy)"
        ))
        self.console.print(Panel(
            Syntax(diff, "diff", theme="monokai", line_numbers=True),
            title="[bold red]Prophecy of Annihilation[/bold red]",
            border_style="red"
        ))