# path: scaffold/core/kernel/sentinel_gardener.py

import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..cortex.engine import GnosticCortex

from ...logger import Scribe
from ...utils import atomic_write

Logger = Scribe("KG_Gardener")


class SentinelGardener:
    """
    The tireless artisan that keeps the written Chronicle (documentation)
    in sync with the living Soul (code).
    """
    ANCHOR_REGEX = re.compile(r"<!--\s*GNOSTIC_ANCHOR:\s*([\w\.]+)\s*-->")
    END_ANCHOR = "<!-- END_GNOSTIC_ANCHOR -->"

    def __init__(self, project_root: Path, cortex: "GnosticCortex"):
        self.root = project_root
        self.cortex = cortex
        # Prophecy: This would be configurable
        self.chronicle_files = list(self.root.glob("**/*.md"))

    def on_file_modified(self, modified_path: Path):
        """The entry point for the Sentinel's plea."""
        self.logger.verbose(f"Gardener perceived flux in '{modified_path.name}'. Gazing for impact...")

        # 1. Gaze of Impact: Does this change affect any anchored docs?
        # We need to find which symbol lives in the modified file. We ask the Cortex.
        # This is a reverse lookup.

        # A full implementation requires iterating through the Cortex symbol map.
        # For this ascension, we'll demonstrate the core update logic.

        # 2. Gaze of the Chronicle: We scan all known doc files for anchors.
        for doc_file in self.chronicle_files:
            self._heal_chronicle(doc_file)

    def _heal_chronicle(self, doc_path: Path):
        """Performs the surgical update on a single documentation file."""
        try:
            content = doc_path.read_text(encoding='utf-8')
            new_content = content
            made_changes = False

            # Use a non-greedy regex to find all anchor blocks
            # (anchor_start)(content_to_replace)(anchor_end)
            pattern = re.compile(f"({self.ANCHOR_REGEX.pattern})(.*?)({re.escape(self.END_ANCHOR)})", re.DOTALL)

            # We must use a function for re.sub to regenerate content for each match
            def _regenerate_anchor(match: re.Match) -> str:
                start_tag = match.group(1)
                # Extract the symbol FQN from the start_tag
                symbol_fqn = self.ANCHOR_REGEX.search(start_tag).group(1)

                # Ask the Cortex for the Gnosis of this symbol
                new_doc_content = self._forge_doc_for_symbol(symbol_fqn)

                # Return the full, healed block
                return f"{start_tag}\n{new_doc_content}\n{self.END_ANCHOR}"

            new_content, num_subs = pattern.subn(_regenerate_anchor, content)

            if num_subs > 0:
                self.logger.success(
                    f"Living Chronicle '{doc_path.name}' has been healed ({num_subs} anchor(s) updated).")
                atomic_write(doc_path, new_content, Logger, self.root)

        except Exception as e:
            self.logger.error(f"Gardener's hand faltered while tending '{doc_path.name}': {e}")

    def _forge_doc_for_symbol(self, symbol_fqn: str) -> str:
        """Queries the Cortex and renders markdown for a symbol."""
        # This requires the Cortex to have the full AST Gnosis, which it does.

        # 1. Find the file containing the symbol
        if not self.cortex._memory or not self.cortex._memory.symbol_map:
            return f"`[Gnosis Unavailable: Cortex is cold for {symbol_fqn}]`"

        file_path = self.cortex._memory.symbol_map.get(symbol_fqn)
        if not file_path:
            return f"`[Heresy: Symbol '{symbol_fqn}' not found in Gnostic Graph]`"

        rel_path_str = file_path.relative_to(self.root).as_posix()
        file_gnosis = self.cortex._memory.project_gnosis.get(rel_path_str, {})

        # 2. Find the specific symbol's data (function or class)
        symbol_name = symbol_fqn.split('.')[-1]
        target_node = None
        for fn in file_gnosis.get("functions", []):
            if fn.get("name") == symbol_name:
                target_node = fn
                break

        if not target_node:
            return f"`[Gnosis Obscured: Could not find details for {symbol_name}]`"

        # 3. Forge the Markdown
        # A real implementation would be a rich template.
        docstring = target_node.get('docstring', 'No docstring provided.').strip()
        signature = f"def {symbol_name}(...):"  # Heuristic

        md = f"**`{symbol_fqn}`**\n\n"
        md += f"```python\n{signature}\n```\n\n"
        md += f"> {docstring}\n"

        return md