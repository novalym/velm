# Path: scaffold/artisans/shadow_clone/catalog.py
# =================================================================================
# == THE SHADOW LEDGER (V-Ω-PERSISTENCE)                                        ==
# =================================================================================
import json
from pathlib import Path
from typing import List, Optional
from .contracts import ShadowEntity
from ...logger import Scribe

Logger = Scribe("ShadowCatalog")


class ShadowCatalog:
    """
    Manages the registry of active Shadow Clones.
    Ensures we never lose track of a spawned reality.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.registry_path = self.root / ".scaffold" / "shadows" / "registry.json"
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_registry()

    def _ensure_registry(self):
        if not self.registry_path.exists():
            self.registry_path.write_text("[]", encoding="utf-8")

    def register(self, entity: ShadowEntity):
        shadows = self.list_shadows()
        shadows.append(entity)
        self._save(shadows)
        Logger.verbose(f"Registered Shadow: {entity.id}")

    def deregister(self, shadow_id: str):
        shadows = self.list_shadows()
        shadows = [s for s in shadows if s.id != shadow_id]
        self._save(shadows)

    def get(self, shadow_id: str) -> Optional[ShadowEntity]:
        shadows = self.list_shadows()
        for s in shadows:
            if s.id == shadow_id:
                return s
        return None

    def list_shadows(self) -> List[ShadowEntity]:
        try:
            content = self.registry_path.read_text(encoding="utf-8")
            data = json.loads(content)
            return [ShadowEntity(**d) for d in data]
        except Exception:
            return []

    def _save(self, shadows: List[ShadowEntity]):
        data = [s.to_dict() for s in shadows]
        self.registry_path.write_text(json.dumps(data, indent=2), encoding="utf-8")