# scaffold/core/assembler/weavers/base_weaver.py

"""
=================================================================================
== THE SACRED CONTRACT OF THE WEAVER (V-Ω-ABSTRACT-PRIME)                      ==
================================
LIF: 10,000,000,000

This scripture defines the pure, abstract soul of all Weavers. It is the
unbreakable Gnostic Contract that binds all surgical artisans to the will of the
Assembler Engine.

It makes no assumptions about implementation. It only defines the sacred vows
that all children must honor.
=================================================================================
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING, Optional, List

from ....contracts.data_contracts import ScaffoldItem
from ....logger import Scribe
from ....utils import atomic_write

if TYPE_CHECKING:
    from ..engine import AssemblerEngine
    from ...kernel import GnosticTransaction

class BaseWeaver(ABC):
    """The Abstract Soul of all Integration Artisans."""

    def __init__(self, root: Path, parent_assembler: 'AssemblerEngine'):
        self.root = root
        self.logger = Scribe(self.__class__.__name__)

    @property
    @abstractmethod
    def language(self) -> str:
        """
        [THE VOW OF IDENTITY]
        A Weaver must proclaim the language of its soul (e.g., 'react', 'python').
        This Gnosis allows the Assembler's Graph to summon the correct surgeon.
        """
        pass

    @abstractmethod
    def can_weave(self, item: ScaffoldItem) -> bool:
        """
        [THE VOW OF PERCEPTION]
        A Weaver must be able to gaze upon a newly forged scripture and know
        if it is a soul that it is destined to connect.
        """
        pass

    @abstractmethod
    def weave(
            self,
            item: ScaffoldItem,
            context: Dict[str, Any],
            target_file: Path,
            transaction: Optional["GnosticTransaction"] = None,  # <--- THE ASCENSION
            dry_run: bool = False  # <--- THE ASCENSION
    ) -> List[Path]:
        """
        [THE VOW OF ACTION, ASCENDED]
        The sacred rite of surgical connection. It receives the new scripture,
        the Gnostic context, and the one true target reality. It must perform
        its rite and proclaim a list of all scriptures it has modified.
        It now understands the Gaze of Prophecy (dry_run) and the Chronicle of
        History (transaction).
        """
        pass

    def _inject_import(
            self,
            file_path: Path,
            import_line: str,
            transaction: Optional["GnosticTransaction"] = None,  # <--- THE ASCENSION
            dry_run: bool = False  # <--- THE ASCENSION
    ) -> bool:
        """Idempotently injects an import, now with Gnostic awareness."""
        if not file_path.exists(): return False
        content = file_path.read_text(encoding='utf-8')

        if import_line.strip() in content:
            return False  # No change made

        lines = content.splitlines()
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ', 'require(', 'use ')):
                last_import_idx = i + 1

        lines.insert(last_import_idx, import_line)
        final_content = "\n".join(lines)

        if dry_run:
            self.logger.info(f"[DRY RUN] Would inject import into: {file_path.name}")
            return True  # Pretend a change was made for logging

        # The Rite of Atomic Inscription, now with Transactional Gnosis
        atomic_write(file_path, final_content, self.logger, self.root, transaction=transaction)
        return True

    def _inject_after_marker(
            self,
            file_path: Path,
            marker: str,
            code: str,
            transaction: Optional["GnosticTransaction"] = None,  # <--- THE ASCENSION
            dry_run: bool = False  # <--- THE ASCENSION
    ) -> bool:
        """Injects code after a marker, now with Gnostic awareness."""
        if not file_path.exists(): return False
        content = file_path.read_text(encoding='utf-8')

        if code.strip() in content:
            return False  # No change made

        if marker in content:
            new_content = content.replace(marker, f"{marker}\n{code}", 1)

            if dry_run:
                self.logger.info(f"[DRY RUN] Would inject code after marker in: {file_path.name}")
                return True

            atomic_write(file_path, new_content, self.logger, self.root, transaction=transaction)
            return True
        return False

