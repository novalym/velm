# Path: scaffold/artisans/aether/artisan.py
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import AetherRequest
from ...help_registry import register_artisan
from .analyzer import PatternAnalyzer
from .mesh import AetherMeshClient


@register_artisan("aether")
class AetherArtisan(BaseArtisan[AetherRequest]):
    """
    =============================================================================
    == THE NEURAL AETHER (V-Ω-FEDERATED-INTELLIGENCE)                          ==
    =============================================================================
    LIF: INFINITY

    The Sovereign of Collective Intelligence.
    1. ANALYZE: Extracts patterns from local code.
    2. BROADCAST: Shares patterns with the Global Lattice (anonymized).
    3. SYNC: Receives optimized architectural wisdom from the mesh.
    """

    def execute(self, request: AetherRequest) -> ScaffoldResult:
        analyzer = PatternAnalyzer(self.project_root)
        client = AetherMeshClient()

        if request.aether_command == "broadcast":
            self.logger.info("Extracting Gnostic DNA for broadcast...")
            dna = analyzer.extract_dna(privacy_level=request.privacy_level)
            self.logger.info("Communing with Mothership...")
            res = client.broadcast_pattern(dna, "MOCK_KEY")
            return self.success("Local wisdom has been shared with the Lattice.", data=res)

        elif request.aether_command == "sync":
            self.logger.info("Downloading wisdom from the Celestial Mesh...")
            wisdom = client.sync_wisdom()
            return self.success(f"Received {len(wisdom)} patterns.", data={"wisdom": wisdom})

        return self.failure("Unknown Aether rite.")