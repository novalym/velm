# Path: scaffold/core/blueprint_scribe/content_renderer.py
# --------------------------------------------------------
import codecs
from pathlib import Path
from typing import Tuple, List, Optional

from ...contracts.data_contracts import ScaffoldItem
from ...utils import is_binary


class ContentRenderer:
    """
    =================================================================================
    == THE CONTENT ALCHEMIST (V-Ω-SOUL-INSCRIBER)                                  ==
    =================================================================================
    Handles the formatting of the 'Soul' of a file.

    [EVOLUTION 3, 4, 6, 7, 9]
    - Handles Binary Seeds (<<)
    - Handles Inline Content (::)
    - Handles Permissions (%%)
    - Handles Unicode Escaping
    """

    def render(self, item: ScaffoldItem, current_indent_level: int) -> Tuple[str, List[str]]:
        """
        Returns: (inline_suffix_string, list_of_block_lines)
        """
        parts = []
        block_lines = []

        # 1. [EVOLUTION 4] The Binary Ward & [EVOLUTION 7] Seed Resolver
        is_bin = self._check_binary(item)

        if is_bin:
            # Force Seed Syntax
            # We must use the resolved path as the seed source relative to the execution context
            seed_source = item.path.as_posix()
            parts.append(f"<< {seed_source}")

        # 2. Text Content
        elif item.content is not None:
            if '\n' in item.content:
                # Multi-line Block
                # Return the colon to signal block start in the suffix
                parts.append(":")
                # Indent the content
                indent = "    " * (current_indent_level + 1)
                for line in item.content.rstrip().splitlines():
                    block_lines.append(f"{indent}{line}")
            else:
                # [EVOLUTION 9] The Unicode Guardian
                # Inline Content
                escaped = codecs.encode(item.content, "unicode_escape").decode("utf-8").replace('"', '\\"')
                parts.append(f':: "{escaped}"')

        # 3. External Seed (Explicit)
        elif item.seed_path:
            seed_p = Path(item.seed_path) if isinstance(item.seed_path, str) else item.seed_path
            parts.append(f"<< {seed_p.as_posix()}")

        # 4. [EVOLUTION 6] The Permission Sentinel
        if item.permissions:
            parts.append(f"%% {item.permissions}")

        return " ".join(parts), block_lines

    def _check_binary(self, item: ScaffoldItem) -> bool:
        if hasattr(item.path, 'is_binary_gnosis'):
            return item.path.is_binary_gnosis
        if item.is_binary:
            return True
        if item.path and item.path.exists() and item.path.is_file():
            return is_binary(item.path)
        return False