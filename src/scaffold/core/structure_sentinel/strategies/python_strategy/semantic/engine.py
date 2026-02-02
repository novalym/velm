# Path: scaffold/core/structure_sentinel/strategies/python_strategy/semantic/engine.py
# ------------------------------------------------------------------------------------

from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Dict, Any

from ..base_faculty import BaseFaculty
from ..contracts import SharedContext
from .harvester import SymbolHarvester
from .weaver import ImportWeaver
from .guardian import ApiGuardian
from ..structural.content import ContentScribe
from ..structural.layout import LayoutGeometer

if TYPE_CHECKING:
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class SemanticFaculty(BaseFaculty):
    """
    =============================================================================
    == THE SEMANTIC FACADE (V-Ω-GNOSTIC-INTEGRATOR-ULTIMA)                     ==
    =============================================================================
    LIF: 10,000,000,000,000

    The High Priest of Meaning.
    It orchestrates the Harvester (Perception), Weaver (Connection), and Guardian (Protection)
    to bind new scriptures into the Pythonic namespace.
    """

    def __init__(self, logger: 'Scribe'):
        super().__init__(logger)
        self.harvester = SymbolHarvester()
        self.weaver = ImportWeaver(logger)
        self.guardian = ApiGuardian(logger)

        self.content_scribe = ContentScribe()
        self.layout_geometer = LayoutGeometer()

    def register_symbols(self, file_path: Path, root: Path, tx: Optional["GnosticTransaction"]):
        """
        The Grand Rite of Semantic Registration.
        """
        # Forge the shared context for this operation
        context = SharedContext(project_root=root, transaction=tx, logger=self.logger)

        # 1. Read the Source Scripture
        content = self._read(file_path, context)
        if not content: return

        # 2. Harvest Public Symbols
        symbols = self.harvester.harvest(file_path, content)
        if not symbols: return

        # 3. Locate the Parent Package
        init_file = file_path.parent / "__init__.py"

        # 4. Perform the Injection
        self._inject(init_file, file_path.stem, symbols, context)

    def _inject(self, init_path: Path, module: str, symbols: List[str], context: SharedContext):
        """
        Surgically injects symbols into an __init__.py file.
        """
        # Read the target (from Staging or Disk)
        content = self._read(init_path, context) or ""
        original_content = content

        # [FACULTY 13] Extract Gnosis from Context
        # We try to extract the variable map from the transaction context if available
        gnosis = {}
        if context.transaction and hasattr(context.transaction, 'context'):
            gnosis = context.transaction.context

        # [FACULTY 17] THE CURE FOR THE VOICELESS SOUL
        # If the scripture is a void, consecrate it with a full header.
        if not content.strip():
            is_root = self.layout_geometer.is_root_package(init_path.parent, context.project_root)
            license_header = self.content_scribe.get_license_header(context.project_root)

            # [FACULTY 15] Resolve Effective Directory for Scanning
            # We need to look into the staging area to see other files (siblings) that might exist
            effective_dir = init_path.parent
            if context.transaction:
                try:
                    rel = init_path.parent.relative_to(context.project_root)
                    effective_dir = context.transaction.get_staging_path(rel)
                    if not effective_dir.exists():
                        effective_dir.mkdir(parents=True, exist_ok=True)
                except:
                    pass

            # [FACULTY 14] Forge with Logical Name
            content = self.content_scribe.forge_init(
                directory=effective_dir,  # Scan physical/staged files
                is_root=is_root,
                license_header=license_header,
                package_name=init_path.parent.name,  # Use logical name
                gnosis=gnosis  # Inject metadata
            )

            # Reset original content to force write
            original_content = ""

        # [FACULTY 16] THE FUTURE SIGHT
        content = self._ensure_future_import(content)

        # [FACULTY 19] THE WEAVER'S HAND
        content = self.weaver.weave(content, module, symbols)

        # [FACULTY 20] THE GUARDIAN'S SHIELD
        content = self.guardian.guard(content, symbols, context)

        # [FACULTY 22] IDEMPOTENCY WARD
        if content == original_content:
            return

        # [FACULTY 23] THE LUMINOUS VOICE
        self.logger.success(f"   -> Semantic Injection: {module} -> {init_path.name}")

        self._write(init_path, content, context)

    def _ensure_future_import(self, content: str) -> str:
        """
        Ensures 'from __future__ import annotations' is present and correctly placed.
        """
        if "from __future__ import annotations" in content:
            return content

        lines = content.splitlines()
        insert_idx = 0
        in_docstring = False
        docstring_quote = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                insert_idx = i + 1
                continue
            if stripped.startswith("#"):
                insert_idx = i + 1
                continue

            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    in_docstring = True
                    docstring_quote = stripped[:3]
                    if stripped.count(docstring_quote) >= 2 and len(stripped) > 3:
                        insert_idx = i + 1
                        break
                    continue

            if in_docstring:
                if docstring_quote in stripped:
                    in_docstring = False
                    insert_idx = i + 1
                    break
                continue

            # Found code or imports
            break

        # Insert
        lines.insert(insert_idx, "from __future__ import annotations")

        # Add a spacer if needed
        if insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, "")

        return "\n".join(lines)