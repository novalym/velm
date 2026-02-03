# Path: scaffold/artisans/graph/layout.py
# ---------------------------------------
import json
from pathlib import Path
from typing import Dict, List


class LayoutManager:
    """The Archivist of Space. Manages node coordinates."""

    LAYOUT_FILE = ".scaffold/genesis.layout.json"

    def __init__(self, root: Path):
        self.path = root / self.LAYOUT_FILE

    def load(self) -> Dict[str, Dict[str, float]]:
        if not self.path.exists(): return {}
        try:
            return json.loads(self.path.read_text(encoding='utf-8'))
        except:
            return {}

    def save(self, nodes: List[Dict]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # We only save X and Y to minimize noise
        data = {n['id']: {"x": n['x'], "y": n['y']} for n in nodes}
        self.path.write_text(json.dumps(data, indent=2), encoding='utf-8')