# Path: scaffold/core/blueprint_scribe/scribe.py
# ----------------------------------------------
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from .metadata_scribe import MetadataScribe
from .tree_forger import TreeForger
from .canonical_serializer import CanonicalSerializer
from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.data_contracts import ScaffoldItem
from ...logger import Scribe

Logger = Scribe("BlueprintScribe")


class BlueprintScribe:
    """
    =================================================================================
    == THE BLUEPRINT SCRIBE (V-Ω-FACADE. THE GRAND ORCHESTRATOR)                   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The High Priest of the Scribe Sanctum. It coordinates the specialized artisans
    to transmute Gnostic Intent into a persistent `.scaffold` scripture.
    """

    def __init__(self, project_root: Path, *, alchemist: Optional[DivineAlchemist] = None):
        self.project_root = project_root
        self.alchemist = alchemist or get_alchemist()

        # The Sub-Artisans are summoned
        self.metadata_scribe = MetadataScribe(project_root, self.alchemist)
        self.tree_forger = TreeForger()
        self.serializer = CanonicalSerializer()

    def transcribe(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int]],
            gnosis: Dict[str, Any],
            rite_type: str = 'genesis'
    ) -> str:
        """
        The Grand Rite of Transcription.
        """
        Logger.verbose("The Blueprint Scribe begins the Rite of Transcription...")

        # 1. Segregate the Soul (Variables vs Form)
        # [EVOLUTION 5: The Variable Segregator]
        variable_items, form_items = self._segregate_items(items)

        # 2. Forge the Tree (Structure)
        # [EVOLUTION 12: The Gnostic Contract - Only Form enters the tree]
        root_node = self.tree_forger.forge(form_items)

        # 3. Generate the Core Scripture (The Body)
        # [EVOLUTION 1: The Stream of Consciousness]
        body_lines = list(self.serializer.serialize(root_node))

        # 4. Forge the Provenance (Header/Footer)
        # [EVOLUTION 7: The Metadata Historian]
        clean_commands = [cmd for cmd, _ in commands]
        header_lines = self.metadata_scribe.forge_header(gnosis)
        footer_lines = self.metadata_scribe.forge_footer(gnosis, clean_commands)

        # 5. The Final Assembly
        final_lines = header_lines

        # Append Variables
        if variable_items:
            final_lines.append("\n# --- I. The Altar of Gnostic Variables (The Soul of the Project) ---")
            for var_item in variable_items:
                # Clean up $$ prefix if present in path
                var_name = str(var_item.path).lstrip('$$ ').strip()
                final_lines.append(f"$$ {var_name} = {var_item.content}")
            final_lines.append("")

        # Append Body
        if body_lines:
            final_lines.append("# --- II. The Scripture of Form (The Body of the Project) ---")
            final_lines.extend(body_lines)
            final_lines.append("")

        # Append Maestro's Will
        if clean_commands:
            final_lines.append("\n# --- III. The Maestro's Will (Automation) ---")
            final_lines.append("%% post-run")
            for cmd in clean_commands:
                final_lines.append(f"    {cmd}")
            final_lines.append("")

        # Append Footer
        final_lines.extend(footer_lines)

        return "\n".join(final_lines)

    def _segregate_items(self, items: List[ScaffoldItem]) -> Tuple[List[ScaffoldItem], List[ScaffoldItem]]:
        """Separates Gnostic Variables from Physical Form."""
        from ...contracts.data_contracts import GnosticLineType

        vars_list = []
        form_list = []

        for item in items:
            if not item.path: continue

            # Explicit Check
            if str(item.path).startswith('$$') or item.line_type == GnosticLineType.VARIABLE:
                vars_list.append(item)
            elif item.line_type == GnosticLineType.FORM:
                form_list.append(item)
            # Implicitly drops LOGIC, COMMENT, POST_RUN from the file tree structure

        return vars_list, form_list