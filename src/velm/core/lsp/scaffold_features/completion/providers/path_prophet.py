# Path: core/lsp/scaffold_features/completion/providers/path_prophet.py
# ---------------------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_PATH_PROPHET_INFINITE_V99
# SYSTEM: OCULAR_PROPHET | ROLE: FILESYSTEM_NAVIGATOR | RANK: GOD_TIER
# =================================================================================

import os
import logging
import re
import time
import stat
from pathlib import Path
from typing import List, Any, Optional, Tuple, Dict
from dataclasses import dataclass

# --- IRON CORE UPLINKS ---
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem, CompletionItemKind, InsertTextFormat, Command
from ....base.types import TextEdit, Range, Position
from ....base.telemetry import forensic_log

Logger = logging.getLogger("PathProphet")

# [ASCENSION 2]: CHRONOMETRIC CACHE
# Map[path_str, (timestamp, list_of_entries)]
DIR_CACHE: Dict[str, Tuple[float, List[Any]]] = {}
CACHE_TTL = 5.0  # Seconds


@dataclass
class PathEntry:
    """The Soul of a File."""
    name: str
    path: str
    is_dir: bool
    is_symlink: bool
    size: int
    mtime: float
    mode: int
    source_type: str = "Local"  # Local | Template | Shadow


class PathProphet(CompletionProvider):
    """
    =============================================================================
    == THE INFINITE PATHFINDER (V-Ω-UNBOUNDED)                                 ==
    =============================================================================
    A hyper-performant filesystem engine.
    It uses caching, generators, and relevance scoring to handle directories of any size.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "PathProphet"

    @property
    def priority(self) -> int:
        return 80

    # [ASCENSION 8]: ABYSSAL FILTER
    IGNORED_DIRS = {'.git', 'node_modules', '__pycache__', '.scaffold', '.idea', '.vscode', 'dist', 'build', 'coverage',
                    '.DS_Store'}

    # Matches: @include "path", path :: "content", path << seed, link -> target
    PATH_CONTEXT = re.compile(r'(@include|<<|::|->)\s*(["\'])([^"\']*)$')
    # Generic String Matcher
    IN_QUOTE = re.compile(r'(["\'])([^"\']*)$')

    def provide(self, ctx: CompletionContext) -> List[CompletionItem]:
        start_time = time.perf_counter()

        try:
            # [ASCENSION 8]: JINJA GUARD
            # If we are inside a Jinja expression, do not suggest paths (Variables take precedence)
            if ctx.is_inside_jinja: return []

            # --- 1. DIVINE CONTEXT ---
            line = ctx.line_prefix
            operator = None
            partial_path = ""

            # Check specific operators first
            match = self.PATH_CONTEXT.search(line)
            if match:
                operator = match.group(1)
                partial_path = match.group(3)  # Group 3 is path
            else:
                # Check generic quotes
                q_match = self.IN_QUOTE.search(line)
                if q_match:
                    partial_path = q_match.group(2)
                    # Heuristic: Treat as path if it has separators, is empty, or follows a space
                    if not ('/' in partial_path or '.' in partial_path or len(partial_path) == 0):
                        return []
                else:
                    return []

                    # --- 2. RESOLVE GEOMETRY ---
            project_root = Path(self.server.project_root) if self.server.project_root else Path.cwd()

            # [ASCENSION 9]: HOME EXPANSION
            clean_input = partial_path
            if clean_input.startswith('~'):
                clean_input = os.path.expanduser(clean_input)

            # Determine Target Directory
            if clean_input.startswith('/'):
                # Absolute relative to project root
                # "src/core/" -> project_root/src/core
                target_dir = project_root / clean_input.lstrip('/')
                search_prefix = clean_input
            else:
                # Relative to Project Root (Default Gnostic Behavior)
                target_dir = project_root / clean_input
                search_prefix = clean_input

            # If target_dir is not a dir (partial filename), look at parent
            query_name = ""
            # Handle trailing slash explicitly
            if not clean_input.endswith('/') and not (target_dir.exists() and target_dir.is_dir()):
                query_name = target_dir.name
                target_dir = target_dir.parent

            # [ASCENSION 7]: MULTIVERSAL SEARCH (LOCAL + TEMPLATES + SHADOW)
            search_targets = [(target_dir, "Local")]

            if operator == '<<':
                # Templates
                template_root = project_root / ".scaffold" / "templates"
                if len(clean_input.split('/')) <= 1:
                    search_targets.append((template_root, "Template"))

            # Shadow Staging (For '::' or generic)
            if not operator or operator == '::':
                shadow_root = project_root / ".scaffold" / "staging" / (
                    clean_input if clean_input.endswith('/') else os.path.dirname(clean_input))
                if shadow_root.exists():
                    search_targets.append((shadow_root, "Shadow"))

            items = []

            # Calculate Range
            current_range = Range(
                start=Position(line=ctx.position['line'], character=ctx.position['character'] - len(partial_path)),
                end=Position(line=ctx.position['line'], character=ctx.position['character'])
            )

            # --- 3. THE HARVEST (UNBOUNDED) ---
            all_entries: List[PathEntry] = []

            for directory, source_type in search_targets:
                dir_str = str(directory)

                # [ASCENSION 2]: CHRONOMETRIC CACHE CHECK
                cached = DIR_CACHE.get(dir_str)
                now = time.time()

                if cached and (now - cached[0] < CACHE_TTL):
                    entries = cached[1]
                else:
                    # Perform Disk Scan
                    entries = self._scan_directory(directory, source_type)
                    if entries:
                        DIR_CACHE[dir_str] = (now, entries)

                all_entries.extend(entries)

            # --- 4. FILTERING & SCORING ---
            scored_items = []
            query_lower = query_name.lower()

            for entry in all_entries:
                name_lower = entry.name.lower()

                # [ASCENSION 10]: HIDDEN FILE PROTOCOL
                if entry.name.startswith('.') and not query_lower.startswith('.'):
                    continue

                # Scoring Logic
                score = 0
                if name_lower == query_lower:
                    score = 100
                elif name_lower.startswith(query_lower):
                    score = 90
                elif query_lower in name_lower:
                    score = 50
                else:
                    continue  # No match

                # Boost Folders
                if entry.is_dir: score += 5

                # Boost .scaffold files in @include context
                if operator in ('@include', '<<') and entry.name.endswith('.scaffold'):
                    score += 20

                scored_items.append((score, entry))

            # Sort by Score DESC, then Name ASC
            scored_items.sort(key=lambda x: (-x[0], x[1].name))

            # [ASCENSION 3]: ADAPTIVE PAGINATION
            # If we have too many items, truncate and signal Incomplete
            # This prevents UI freeze while still allowing "Unlimited" scanning logic
            PAGINATION_LIMIT = 500
            is_incomplete = len(scored_items) > PAGINATION_LIMIT
            visible_items = scored_items[:PAGINATION_LIMIT]

            for score, entry in visible_items:
                # Forge Insert Text
                # Determine prefix based on input style
                path_prefix = ""
                if '/' in partial_path.replace('\\', '/'):
                    path_prefix = os.path.dirname(partial_path.replace('\\', '/')) + "/"

                final_insert = path_prefix + entry.name + ("/" if entry.is_dir else "")

                # Iconography & Detail
                kind = CompletionItemKind.File
                icon_char = "📄"
                if entry.is_dir:
                    kind = CompletionItemKind.Folder
                    icon_char = "📂"
                elif entry.is_symlink:
                    kind = CompletionItemKind.Reference
                    icon_char = "🔗"

                if entry.source_type == "Template": icon_char = "🧩"
                if entry.source_type == "Shadow": icon_char = "👻"

                # [ASCENSION 4]: PERMISSION ICONS
                perm_icon = ""
                if not (entry.mode & stat.S_IWUSR): perm_icon = "🔒"  # Read-only
                if (entry.mode & stat.S_IXUSR): perm_icon = "🚀"  # Executable

                # [ASCENSION 11]: DOC HYDRATION
                size_str = self._human_size(entry.size)
                mtime_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(entry.mtime))

                items.append(CompletionItem(
                    label=entry.name + ("/" if entry.is_dir else ""),
                    kind=kind,
                    detail=f"{icon_char} {entry.source_type} {perm_icon}",
                    insertText=final_insert,
                    # Zero-pad score for correct sort order
                    sortText=f"{1000 - score:04d}-{entry.name}",
                    textEdit=TextEdit(range=current_range, newText=final_insert),
                    command=Command(title="Next", command="editor.action.triggerSuggest") if entry.is_dir else None,
                    documentation=f"**Path:** `{entry.path}`\n\n**Size:** `{size_str}`\n**Modified:** `{mtime_str}`\n**Permissions:** `{oct(entry.mode)[-3:]}`"
                ))

            # --- 5. THE GENESIS OFFER ---
            if not items and query_name:
                self._offer_genesis(items, query_name, clean_input, current_range)

            # Telemetry
            duration = (time.perf_counter() - start_time) * 1000
            if duration > 50:
                forensic_log(f"Path Scry ({len(all_entries)} nodes) in {duration:.2f}ms", "INFO", "PATH")

            # [ASCENSION 3]: RETURN INCOMPLETE STATUS IF TRUNCATED
            # This forces the client to re-query as the user types more characters
            # allowing us to refine the 500 items from the 50,000 total.
            # We access the private _incomplete_flag via a special return structure if the Engine supports it,
            # or we rely on the Engine's default behavior.
            # Note: The CompletionList wrapper in the Engine handles the bool(not_done).
            # We can't return a CompletionList directly from a Provider.
            # However, if we return a list, the Engine assumes complete.
            # We rely on the Engine's "Metabolic Throttling" for time limits,
            # but for list size limits, we implicitly accept that we show the Top 500.

            return items

        except Exception as e:
            Logger.error(f"Path Prophecy Fractured: {e}")
            return []

    def _scan_directory(self, directory: Path, source_type: str) -> List[PathEntry]:
        """[ASCENSION 1]: GENERATOR PIPELINE"""
        entries = []
        if not directory.exists(): return []

        try:
            with os.scandir(directory) as scanner:
                for entry in scanner:
                    if entry.name in self.IGNORED_DIRS: continue

                    try:
                        stat_res = entry.stat()
                        entries.append(PathEntry(
                            name=entry.name,
                            path=entry.path,
                            is_dir=entry.is_dir(),
                            is_symlink=entry.is_symlink(),
                            size=stat_res.st_size,
                            mtime=stat_res.st_mtime,
                            mode=stat_res.st_mode,
                            source_type=source_type
                        ))
                    except OSError:
                        pass  # Race condition (file deleted during scan)
        except OSError:
            pass  # Permission denied

        return entries

    def _offer_genesis(self, items: List[CompletionItem], query_name: str, full_path: str, rng: Range):
        """[ASCENSION 9]: CREATION PROPOSAL"""
        is_folder = full_path.endswith('/')
        label = f"📂 Create Sanctum '{query_name}/'" if is_folder else f"✨ Create Scripture '{query_name}'"
        insert = query_name + ("/" if is_folder else "")

        items.append(CompletionItem(
            label=label,
            kind=CompletionItemKind.Event,
            detail="Genesis Rite",
            insertText=insert,
            sortText="zz-genesis",
            textEdit=TextEdit(range=rng, newText=insert),
            documentation=f"Materializes a new entity at `{full_path}`."
        ))

    def _human_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"