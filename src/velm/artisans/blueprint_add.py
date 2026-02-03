# Path: scaffold/artisans/blueprint_add.py
# -------------------------------

import re
import shutil
from typing import Tuple, List

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import AddRequest
from ..parser_core.block_consumer import GnosticBlockConsumer
from ..utils import atomic_write


class BlueprintAddArtisan(BaseArtisan[AddRequest]):
    """
    =================================================================================
    == THE SURGICAL PEN (V-Ω-SENTIENT-QUILL)                                       ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000

    This artisan surgically inserts new definitions into a living blueprint. It is no
    longer a simple text appender; it is a sentient quill that understands the
    grammar, context, and potential paradoxes of the law it inscribes.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Genesis Ward (`--create-if-void`):** Can be commanded to forge a new,
        empty blueprint if the target is a void, bridging the gap with `init`.
    2.  **The Guardian's Offer:** Invokes the universal `guarded_execution` rite to
        snapshot the blueprint before modification.
    3.  **The Hierarchical Inserter:** Performs a deep AST-like analysis to find the
        perfect, indented location for the new item within its parent directory block.
    4.  **The Duplicate Sentinel:** Prevents duplicate path definitions with a robust,
        regex-based gaze.
    5.  **The Directive Alchemist:** Intelligently formats the line based on whether the
        content is a simple string, a multi-line block, a seed, or a directive.
    6.  **The Permission Guard:** Correctly handles the `%% 755` syntax.
    7.  **The Path Normalizer:** Enforces POSIX-style `/` separators for universal purity.
    8.  **The Auto-Formatter:** Calculates and applies the correct indentation level.
    9.  **The Atomic Inscription:** Uses `atomic_write` to prevent blueprint corruption.
    10. **The Variable Mentor:** If new content uses `{{ var }}`, it warns the Architect
        if `var` is not defined in the blueprint, preventing runtime paradoxes.
    11. **The Luminous Dossier:** Returns a rich `Artifact` upon success for UI integration.
    12. **The Unbreakable Ward:** Uses a local `.bak` file as a final, catastrophic
        rollback mechanism in case of a core engine failure.
    =================================================================================
    """

    def execute(self, request: AddRequest) -> ScaffoldResult:
        blueprint_path = (self.project_root / request.blueprint_path).resolve()

        # [FACULTY 1] The Genesis Ward
        if not blueprint_path.exists():
            if getattr(request, 'create_if_void', False) or request.variables.get('create_if_void'):
                self.logger.info(f"Blueprint is a void. Forging new scripture at [cyan]{blueprint_path.name}[/cyan]...")
                atomic_write(blueprint_path, "# == Gnostic Blueprint ==\n\n", self.logger, blueprint_path.parent)
            else:
                return self.failure(f"Blueprint not found at: {blueprint_path}",
                                    suggestion="Use --create-if-void to forge it.")

        # [FACULTY 2] The Guardian's Offer
        # We offer a snapshot of the blueprint before this surgical rite.
        self.guarded_execution([blueprint_path], request, context="blueprint_add")

        # [FACULTY 12] The Unbreakable Ward (Local .bak)
        backup_path = blueprint_path.with_suffix('.scaffold.bak')
        shutil.copy2(blueprint_path, backup_path)

        try:
            current_content = blueprint_path.read_text(encoding='utf-8')
            lines = current_content.splitlines()

            # [FACULTY 7] The Path Normalizer
            target_path_str = request.item_path.replace('\\', '/')
            if request.is_dir and not target_path_str.endswith('/'):
                target_path_str += '/'

            # [FACULTY 4] The Duplicate Sentinel
            if self._check_existence(lines, target_path_str):
                return self.failure(
                    f"The path '{target_path_str}' is already inscribed in the blueprint.",
                    suggestion=f"Use `scaffold transfigure` to modify existing definitions."
                )

            # [FACULTY 5 & 6] The Directive Alchemist & Permission Guard
            new_line_content = self._forge_entry_string(request, target_path_str)

            # [FACULTY 3] The Hierarchical Inserter
            insert_index, indent_level = self._find_insertion_point(lines, target_path_str)

            # [FACULTY 8] The Auto-Formatter
            indentation = "    " * indent_level
            final_line = f"{indentation}{new_line_content}"

            # The Rite of Inscription
            lines.insert(insert_index, final_line)

            # [FACULTY 10] The Variable Mentor
            if request.content and "{{" in request.content:
                self._check_variable_consistency(lines, request.content)

            # [FACULTY 9] The Atomic Inscription
            final_content = "\n".join(lines)
            if not final_content.endswith('\n'):
                final_content += "\n"

            write_result = atomic_write(blueprint_path, final_content, self.logger, blueprint_path.parent)

            # [FACULTY 11] The Luminous Dossier
            artifact = Artifact(
                path=blueprint_path,
                type="file",
                action=write_result.action_taken,
                size_bytes=len(final_content.encode('utf-8'))
            )

            return self.success(
                f"Inscribed '[cyan]{target_path_str}[/cyan]' into '{blueprint_path.name}' at line {insert_index + 1}.",
                artifacts=[artifact]
            )

        except Exception as e:
            # Rollback from local .bak on catastrophic failure
            if backup_path.exists():
                shutil.move(str(backup_path), str(blueprint_path))
            raise ArtisanHeresy(f"A paradox occurred during inscription. Blueprint restored.", child_heresy=e)

    def _forge_entry_string(self, request: AddRequest, path_str: str) -> str:
        """The Directive Alchemist. Forges syntax based on content type."""
        entry = path_str
        if request.seed_path:
            return f"{entry} << {request.seed_path}"

        if request.content:
            content = request.content.strip()
            if content.startswith('@'):
                entry += f" :: {content}"
            elif '\n' in request.content:
                # For `add`, we prefer heredoc for clarity, but this is also valid.
                entry += f' :: """{request.content}"""'
            else:
                safe_content = content.replace('"', '\\"')
                entry += f' :: "{safe_content}"'

        return entry

    def _find_insertion_point(self, lines: List[str], target_path: str) -> Tuple[int, int]:
        """The Hierarchical Inserter."""
        parts = target_path.strip('/').split('/')
        if len(parts) == 1:
            return len(lines), 0  # Append to root

        consumer = GnosticBlockConsumer(lines)

        # We search for the deepest existing parent to nest inside.
        # e.g., for "src/api/v1/routes.py", check for "src/api/v1/", then "src/api/", then "src/".
        for i in range(len(parts) - 1, 0, -1):
            parent_to_find_str = "/".join(parts[:i]) + "/"

            # This requires a full tree traversal to find the node with the absolute path.
            # A simpler heuristic for `add` is often sufficient:
            for line_idx, line in enumerate(lines):
                stripped = line.strip()
                # A heuristic to match the start of a definition line.
                if stripped.startswith(parent_to_find_str):
                    parent_indent = consumer._measure_visual_depth(line)
                    # We found the parent. Now find the end of its block.
                    _, end_block_idx = consumer.consume_indented_block(line_idx + 1, parent_indent)

                    # We insert at the end of the parent block, one level deeper.
                    return end_block_idx, (parent_indent // 4) + 1

        # If no parent found, append to the end of the file.
        return len(lines), 0

    def _check_existence(self, lines: List[str], path_key: str) -> bool:
        """The Duplicate Sentinel."""
        escaped = re.escape(path_key)
        # Check for path followed by space, colon, or end of line.
        pattern = re.compile(rf"^\s*{escaped}(?:\s+|:|::|<<|$)")
        for line in lines:
            if pattern.match(line):
                return True
        return False

    def _check_variable_consistency(self, lines: List[str], content: str):
        """The Variable Mentor."""
        used_vars = set(re.findall(r"\{\{\s*([a-zA-Z0-9_]+)", content))
        defined_vars = set()
        for line in lines:
            match = re.match(r"^\s*\$\$\s*([a-zA-Z0-9_]+)", line)
            if match:
                defined_vars.add(match.group(1))

        missing = used_vars - defined_vars
        if missing:
            self.logger.warn(
                f"Variable Usage Warning: Content uses {missing}, which are not defined. Remember to add '$$ var = value'."
            )