# src/velm/artisans/project/persistence.py
# ----------------------------------------

import json
import os
import shutil
from pathlib import Path
from typing import Optional

from .contracts import RegistrySchema
from .constants import REGISTRY_FILENAME
from ...utils import atomic_write
from ...logger import Scribe

Logger = Scribe("ProjectPersistence")


class RegistryPersistence:
    """
    The Keeper of the Book of Names.
    Abstacts the physical storage of the projects.json ledger.
    """

    def __init__(self, root_override: Optional[Path] = None):
        self.root = root_override or self._divine_root()
        self.registry_path = self.root / REGISTRY_FILENAME
        self._ensure_sanctum()

    def _divine_root(self) -> Path:
        """Determines where the registry lives based on Substrate."""
        if os.environ.get("SCAFFOLD_ENV") == "WASM":
            return Path("/vault")
        return Path.home() / ".scaffold"

    def _ensure_sanctum(self):
        self.root.mkdir(parents=True, exist_ok=True)

    def load(self) -> RegistrySchema:
        """Resurrects the Registry from disk."""
        if not self.registry_path.exists():
            return RegistrySchema()

        try:
            content = self.registry_path.read_text(encoding='utf-8')
            data = json.loads(content)
            return RegistrySchema(**data)
        except Exception as e:
            Logger.error(f"Registry Corrupted: {e}. Returning Tabula Rasa.")
            # Backup corrupt file
            backup = self.registry_path.with_suffix(".bak")
            shutil.copy(self.registry_path, backup)
            return RegistrySchema()

    def save(self, registry: RegistrySchema):
        """Atomic Inscription of the Registry."""
        # Update timestamp on save? No, projects update their own timestamps.
        try:
            data = registry.model_dump(mode='json')
            # Using atomic write to prevent partial flush corruption
            atomic_write(self.registry_path, json.dumps(data, indent=2), Logger, self.root)
        except Exception as e:
            Logger.critical(f"Failed to persist Project Registry: {e}")
            raise e