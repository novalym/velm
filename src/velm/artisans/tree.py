# Path: artisans/tree.py
# ----------------------

import fnmatch
import os
import subprocess
from pathlib import Path
from typing import List, Dict

from ..contracts.data_contracts import ScaffoldItem, GnosticLineType
# --- The Divine Summons ---
from ..core.artisan import BaseArtisan
from ..core.cortex.knowledge import KnowledgeBase
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import TreeRequest
from ..logger import Scribe
from ..rendering import render_gnostic_tree
from ..utils import atomic_write, get_ignore_spec, is_binary, launch_ephemeral_server

Logger = Scribe("GnosticSurveyor")


@register_artisan("tree")
class TreeArtisan(BaseArtisan[TreeRequest]):
    """
    =================================================================================
    == THE GNOSTIC SURVEYOR (V-Ω-ABYSSAL-WARD-ASCENDED)                            ==
    =================================================================================
    @gnosis:title The Gnostic Surveyor (`tree`)
    @gnosis:summary Visualizes a directory structure with deep metadata, Git status, and complexity metrics.
    @gnosis:description
    The `tree` command is the Rite of Pure Perception. Unlike the standard system `tree`,
    this artisan gazes into the **Gnostic Soul** of your project.

    ### THE PANTHEON OF ELEVATIONS:
    1.  **The Abyssal Ward:** Automatically prunes profane noise (`.venv`, `node_modules`, `__pycache__`)
        using the `KnowledgeBase`, keeping the tree luminous and focused.
    2.  **The Git Overlay:** Maps temporal state (Modified, New) onto the static structure.
    3.  **The Complexity Scout:** Heuristically calculates code density for heatmaps.
    4.  **The Polyglot Exporter:** Can transmute the view into JSON, SVG, or Text.
    """

    def execute(self, request: TreeRequest) -> ScaffoldResult:
        root = Path(request.target_path).resolve()
        if not root.exists() or not root.is_dir():
            return self.failure(f"The target '{root}' is not a valid sanctum.")

        self.console.rule(f"[bold cyan]Gnostic Survey: {root.name}[/bold cyan]")

        git_status_map = self._perceive_git_status(root)
        items = self._scan_reality(
            root=root,
            show_all=request.all,
            max_depth=request.depth,
            git_map=git_status_map
        )

        if not items:
            return self.success("The sanctum is empty or obscured by the Veil of Ignorance.")

        renderable = render_gnostic_tree(
            items,
            output_format=request.format,
            use_markup=True,
            project_root=root
        )

        # ★★★ THE EPHEMERAL SERVER RITE ★★★
        if request.serve:
            if request.format != 'svg':
                return self.failure("The Rite of Serving is only consecrated for the 'svg' format.")

            # The SVG renderer returns a string. We pass it to the server.
            launch_ephemeral_server(str(renderable), content_type='image/svg+xml')
            return self.success("Ephemeral server has returned to the void.")

        if request.output:
            return self._inscribe_output(renderable, request.output, request.format, root)
        else:
            return self._proclaim_terminal(renderable, request.format)

    def _perceive_git_status(self, root: Path) -> Dict[Path, str]:
        """[FACULTY 1] The Git Overlay."""
        status_map = {}
        # Only attempt if .git exists in root or ancestors
        if not any((p / ".git").exists() for p in [root, *root.parents]):
            return status_map

        try:
            # Run git status relative to the target root
            result = subprocess.run(
                ["git", "status", "--porcelain", "--ignored"],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=2.0
            )
            if result.returncode != 0: return status_map

            for line in result.stdout.splitlines():
                if len(line) < 4: continue
                code = line[:2]
                raw_path = line[3:].split(' -> ')[-1]
                path = (root / raw_path).resolve()

                if '?' in code:
                    status = '?'
                elif '!' in code:
                    status = 'I'
                elif 'M' in code:
                    status = 'M'
                elif 'A' in code:
                    status = 'A'
                elif 'D' in code:
                    status = 'D'
                else:
                    status = 'M'

                status_map[path] = status

        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        return status_map

    def _is_abyssal(self, name: str) -> bool:
        """
        [FACULTY 2] THE ABYSSAL WARD.
        Checks if a name belongs to the void (noise directories).
        """
        if name in KnowledgeBase.ABYSS_DIRECTORIES:
            return True
        if any(fnmatch.fnmatch(name, p) for p in KnowledgeBase.ABYSS_GLOBS):
            return True
        return False

    def _scan_reality(self, root: Path, show_all: bool, max_depth: int, git_map: Dict[Path, str]) -> List[ScaffoldItem]:
        """[THE DEEP REALITY SCANNER]"""
        items: List[ScaffoldItem] = []
        ignore_spec = get_ignore_spec(root) if not show_all else None

        # Stack: (current_path, depth)
        stack = [(root, 0)]

        with self.console.status("[bold green]Scanning Reality...[/bold green]") as status:
            processed_count = 0

            while stack:
                current_path, current_depth = stack.pop()

                if max_depth > -1 and current_depth > max_depth:
                    continue

                try:
                    # Sort for deterministic tree rendering
                    children = sorted(current_path.iterdir(), key=lambda p: p.name.lower())

                    for child in children:
                        rel_path = child.relative_to(root)
                        name = child.name

                        # 1. The Abyssal Ward (Force-Exclude Noise)
                        if not show_all and self._is_abyssal(name):
                            continue

                        # 2. The Gitignore Ward
                        if ignore_spec and ignore_spec.match_file(str(rel_path)):
                            if not show_all: continue

                        processed_count += 1
                        if processed_count % 200 == 0:
                            status.update(f"[bold green]Scanning Reality... ({processed_count} items)[/bold green]")

                        is_symlink = child.is_symlink()
                        is_dir = child.is_dir()

                        # Metadata
                        git_status = git_map.get(child.resolve(), None)
                        size = child.stat().st_size

                        # 3. The Binary Diviner
                        is_bin = False
                        if not is_dir and not is_symlink:
                            is_bin = is_binary(child)

                        # 4. The Complexity Scout
                        complexity_data = {}
                        if not is_dir and not is_bin and size < 100_000:
                            try:
                                with open(child, 'rb') as f:
                                    lines = sum(1 for _ in f)
                                complexity_data = {
                                    "lines": lines,
                                    "heat_level": "Low" if lines < 100 else "Medium" if lines < 300 else "High" if lines < 1000 else "Critical"
                                }
                            except:
                                pass

                        # 5. Forge the Item
                        # [VISUAL NOISE REDUCTION]
                        # We intentionally DO NOT set 'permissions' or 'content' here for the tree view.
                        # This prevents the TextRenderer from showing "Forge" or "777".
                        item = ScaffoldItem(
                            path=rel_path,
                            is_dir=is_dir,
                            content_hash=None,
                            last_modified=child.stat().st_mtime,
                            permissions=None,  # Hiding permissions to reduce noise
                            git_status=git_status,
                            is_binary=is_bin,
                            complexity=complexity_data,
                            line_type=GnosticLineType.FORM,
                            # We explicitly set content to None so it appears as "Structure Only"
                            content=None
                        )

                        items.append(item)

                        if is_dir and not is_symlink:
                            stack.append((child, current_depth + 1))

                except PermissionError:
                    Logger.warn(f"Permission denied: {current_path}")
                    continue

        return items

    def _inscribe_output(self, renderable, output_path: str, fmt: str, root: Path) -> ScaffoldResult:
        """[FACULTY 7] The Atomic Writer."""
        out_file = Path(output_path).resolve()
        content = ""

        if fmt in ['svg', 'json']:
            content = str(renderable)
        else:
            from rich.console import Console
            capture_console = Console(file=open(os.devnull, "w"), width=120, record=True)
            capture_console.print(renderable)
            content = capture_console.export_text()

        atomic_write(out_file, content, self.logger, root)
        return self.success(
            f"Gnostic Tree inscribed to [cyan]{out_file.name}[/cyan]",
            artifacts=[Artifact(path=out_file, type="file", action="created")]
        )

    def _proclaim_terminal(self, renderable, fmt: str) -> ScaffoldResult:
        if fmt == 'text':
            self.console.print(renderable)
        else:
            print(str(renderable))
        return self.success("Gaze complete.")