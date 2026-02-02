# Path: scaffold/artisans/harvest.py
# ----------------------------------

import re
import subprocess
import time
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydantic import BaseModel, Field
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import TodoRequest
from ..core.cortex.scanner import ProjectScanner
from ..core.cortex.tokenomics import TokenEconomist
from ..help_registry import register_artisan


# --- Gnostic Data Vessel ---
class TodoItem(BaseModel):
    path: Path
    line_num: int
    type: str
    message: str
    raw_line: str
    author: Optional[str] = None
    timestamp: Optional[int] = None
    age_days: Optional[int] = None
    hash: Optional[str] = Field(None, repr=False)


class TodoHarvester:
    """
    =============================================================================
    == THE PURE HARVESTER (V-Ω-LOGIC-ENGINE)                                   ==
    =============================================================================
    The pure logic engine. It scans files and returns a structured list of debt.
    It contains no CLI logic, no rendering, no Git. It is the Gnostic Heart.
    """
    DEBT_REGEX = re.compile(r'\b(TODO|FIXME|XXX|HACK|NOTE|BUG)\b[:\s(]*([^)\n]*)', re.IGNORECASE)

    def __init__(self, root: Path):
        self.root = root.resolve()

    def harvest(self) -> List[TodoItem]:
        scanner = ProjectScanner(self.root, TokenEconomist())
        inventory, _ = scanner.scan()
        code_files = [self.root / i.path for i in inventory if i.category in ('code', 'doc', 'doc_critical')]

        debt_items = []
        for path in code_files:
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    match = self.DEBT_REGEX.search(line)
                    if match:
                        debt_items.append(TodoItem(
                            path=path,
                            line_num=i + 1,
                            type=match.group(1).upper(),
                            message=match.group(2).strip() or line.strip(),
                            raw_line=line.strip()
                        ))
            except Exception:
                continue
        return debt_items


@register_artisan("todos")
class TodoArtisan(BaseArtisan[TodoRequest]):
    """
    =============================================================================
    == THE DEBT COLLECTOR (V-Ω-TEMPORAL-AWARENESS)                             ==
    =============================================================================
    LIF: 10,000,000,000

    Scans the codebase for technical debt markers.
    Uses 'git blame' to assign ownership and age to every TODO.
    """

    def execute(self, request: TodoRequest) -> ScaffoldResult:
        self.logger.info("The Debt Collector begins the harvest...")

        root = (self.project_root / request.path).resolve()

        # 1. Summon the pure Harvester
        harvester = TodoHarvester(root)
        debt_items = harvester.harvest()

        # 2. Enrich with Git Gnosis (Blame)
        if request.blame and (self.project_root / ".git").exists():
            with self.console.status("[bold magenta]Assigning Gnostic Provenance via Git...[/bold magenta]"):
                debt_items = self._enrich_with_git_blame(debt_items)

        # 3. Filter by Author
        if request.author:
            debt_items = [d for d in debt_items if d.author and request.author.lower() in d.author.lower()]

        # 4. Proclaim
        if request.format == "json":
            serializable = [item.model_dump(mode='json') for item in debt_items]
            return self.success("Debt harvested.", data=serializable)

        self._render_table(debt_items)
        return self.success(f"Harvested {len(debt_items)} debt items.")

    def _enrich_with_git_blame(self, items: List[TodoItem]) -> List[TodoItem]:
        """Performs a parallelized git blame lookup."""
        items_by_file = defaultdict(list)
        for item in items:
            items_by_file[item.path].append(item)

        enriched_items = []
        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self._blame_file, path): path for path in items_by_file.keys()}

            for future in as_completed(future_to_file):
                path = future_to_file[future]
                try:
                    blame_data = future.result()
                    for item in items_by_file[path]:
                        if item.line_num in blame_data:
                            item.author = blame_data[item.line_num].get('author')
                            item.timestamp = blame_data[item.line_num].get('timestamp')
                            item.age_days = blame_data[item.line_num].get('age_days')
                        enriched_items.append(item)
                except Exception:
                    # If blame fails for one file, add original items
                    enriched_items.extend(items_by_file[path])
        return enriched_items

    def _blame_file(self, file_path: Path) -> Dict[int, Dict]:
        """Runs git blame on a single file and parses the porcelain output."""
        try:
            res = subprocess.run(
                ["git", "blame", "--line-porcelain", str(file_path)],
                cwd=self.project_root, capture_output=True, text=True, errors='ignore'
            )
            if res.returncode == 0:
                return self._parse_git_blame(res.stdout)
        except Exception:
            pass
        return {}

    def _parse_git_blame(self, porcelain_output: str) -> Dict[int, Dict]:
        result = {}
        lines = porcelain_output.splitlines()
        i = 0
        while i < len(lines):
            try:
                final_line_num = int(lines[i].split()[2])
                meta = {}
                i += 1
                while i < len(lines) and not lines[i].startswith('\t'):
                    if lines[i].startswith('author '):
                        meta['author'] = lines[i][7:]
                    elif lines[i].startswith('author-time '):
                        ts = int(lines[i][12:])
                        meta['timestamp'] = ts
                        meta['age_days'] = (time.time() - ts) // 86400
                    i += 1
                i += 1  # Skip content line
                result[final_line_num] = meta
            except (IndexError, ValueError):
                i += 1  # Skip malformed line
        return result

    def _render_table(self, items: List[TodoItem]):
        if not items:
            self.console.print(Panel("[green]The Sanctum is pure. No debt detected.[/green]", border_style="green"))
            return

        table = Table(title=f"Debt Dossier ({len(items)} items)", border_style="red")
        table.add_column("Type", width=6)
        table.add_column("Age", justify="right")
        table.add_column("Author", style="cyan")
        table.add_column("Message")
        table.add_column("Location", style="dim")

        sorted_items = sorted(items, key=lambda x: x.timestamp or 0)

        for item in sorted_items:
            age = f"{int(item.age_days)}d" if item.age_days is not None else "?"
            author = item.author or 'Unknown'

            type_style = "bold red" if item.type in ("FIXME", "BUG") else "yellow"
            age_style = "red" if (item.age_days or 0) > 90 else "green"

            loc = f"{item.path.name}:{item.line_num}"

            table.add_row(
                f"[{type_style}]{item.type}[/]",
                f"[{age_style}]{age}[/]",
                author,
                item.message,
                loc
            )

        self.console.print(table)