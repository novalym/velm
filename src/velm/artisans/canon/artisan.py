# Path: scaffold/artisans/canon/artisan.py
# ----------------------------------------
from pathlib import Path
import yaml
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import CanonRequest
from ...core.cortex.engine import GnosticCortex
from .law import LawEngine, CanonLaw




class CanonizeArtisan(BaseArtisan[CanonRequest]):
    """
    =============================================================================
    == THE CANONIZER (V-Ω-ARCHITECTURAL-GOVERNOR)                              ==
    =============================================================================
    Enforces dependency topology laws.
    """

    def execute(self, request: CanonRequest) -> ScaffoldResult:
        rules_path = self.project_root / request.rules_path
        if not rules_path.exists():
            return self.failure("No Gnostic Laws found. Create 'scaffold.rules.yaml'.")

        # 1. Load Laws
        data = yaml.safe_load(rules_path.read_text())
        laws = [CanonLaw(**d) for d in data.get("laws", [])]

        # 2. Perceive Reality
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()

        # 3. Adjudicate
        engine = LawEngine()
        heresies = []

        for file_gnosis in memory.inventory:
            if file_gnosis.category != 'code': continue

            imports = file_gnosis.ast_metrics.get("dependencies", {}).get("imports", [])
            path_str = str(file_gnosis.path.as_posix())

            violations = engine.adjudicate(path_str, imports, laws)
            heresies.extend(violations)

        if heresies:
            return self.failure(f"Architectural Heresies detected:\n" + "\n".join(heresies))

        return self.success("The Architecture is Pure.")