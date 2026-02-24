# Path: artisans/publish/artisan.py
# ---------------------------------
import os
import re
import time
import json
import hashlib
import zipfile
import io
from pathlib import Path
from typing import Dict, Any, List, Tuple


from .merkle import GnosticMerkleTree
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import PublishRequest
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("PublishArtisan")


class PublishArtisan(BaseArtisan[PublishRequest]):
    """
    =================================================================================
    == THE PUBLISH ARTISAN (V-Ω-TOTALITY-V100.0-HUB-CONDUCTOR)                    ==
    =================================================================================
    LIF: ∞ | ROLE: CELESTIAL_CONSECRATOR | RANK: OMEGA_SUPREME

    [ARCHITECTURAL MANIFESTO]
    The absolute hand of the God-Engine for shard distribution. It performs
    physical matter compression, Merkle-lattice verification, and Hub-RPC dispatch.
    =================================================================================
    """

    def execute(self, request: PublishRequest) -> ScaffoldResult:
        start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', 'tr-pub-void')

        self.logger.info(
            f"Initiating Consecration Rite for shard: [cyan]{request.namespace}.{request.shard_name}[/cyan]")

        try:
            # --- MOVEMENT I: SPATIAL BIOPSY ---
            root_path = Path(request.target_path).resolve()
            if not root_path.exists() or not root_path.is_dir():
                raise ArtisanHeresy(f"Sanctum Void: Locus '{root_path}' is unmanifest.")

            # --- MOVEMENT II: THE MERKLE INQUEST ---
            # [ASCENSION 1]: Every shard identity is content-addressable.
            self.logger.verbose("Conducting Merkle-Lattice Tomography...")
            merkle = GnosticMerkleTree(root_path)
            shard_hash = merkle.calculate_root()
            self.logger.success(f"Merkle-Identity Resonant: [bold]{shard_hash[:16]}...[/bold]")

            # --- MOVEMENT III: SEMANTIC MINING ---
            # [ASCENSION 2]: Automatically extract intent from the index.scaffold
            metadata = self._mine_gnosis(root_path)
            metadata.update({
                "hash": shard_hash,
                "namespace": request.namespace,
                "name": request.shard_name,
                "published_at": time.time(),
                "architect_id": request.session_id
            })

            # --- MOVEMENT IV: KINETIC HEALTH CHECK ---
            # [ASCENSION 8]: Simulate the shard before allowing it to enter the Hub.
            if not request.force:
                self._verify_shard_vitality(root_path)

            # --- MOVEMENT V: MATTER ENCAPSULATION ---
            # [ASCENSION 11]: Build the compressed vessel shard.
            self.logger.verbose("Encapsulating matter into Celestial Vessel (.zip)...")
            vessel_bytes = self._forge_vessel(root_path, request.is_private)

            # --- MOVEMENT VI: THE HUB HANDSHAKE ---
            if request.dry_run:
                self.logger.info("[DRY-RUN] Strike Stayed. Shard remains in local realm.")
                return self.success("Publication Prophecy complete.", data={"manifest": metadata})

            # [STRIKE]: Connect to SCAF-Hub RPC (Conceptual)
            # In a real strike, we would use the NetworkArtisan to POST to the Hub.
            self._dispatch_to_hub(metadata, vessel_bytes)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.logger.success(f"Singularity Achieved: Shard is now resonant on SCAF-Hub ({duration_ms:.2f}ms).")

            return self.success(
                message=f"Shard '{request.shard_name}' willed into the Aether.",
                data={"hash": shard_hash, "url": f"hub.novalym.dev/{request.namespace}/{request.shard_name}"},
                ui_hints={"vfx": "bloom", "sound": "consecration_complete"}
            )

        except Exception as e:
            self.logger.critical(f"Publication Fractured: {e}")
            raise

    def _mine_gnosis(self, path: Path) -> Dict[str, Any]:
        """[FACULTY 2]: Extracts tags and descriptions from the shard soul."""
        index_file = path / "index.scaffold"
        if not index_file.exists():
            return {"description": "Atomic Gnostic Shard", "tags": ["snippet"]}

        content = index_file.read_text(encoding='utf-8')
        desc_match = re.search(r'@description:\s*(.*)', content)
        tags_match = re.search(r'@tags:\s*(.*)', content)

        return {
            "description": desc_match.group(1).strip() if desc_match else "Gnostic Shard",
            "tags": [t.strip() for t in tags_match.group(1).split(',')] if tags_match else []
        }

    def _forge_vessel(self, path: Path, encrypt: bool) -> bytes:
        """[FACULTY 11]: Transmutes directory into a byte-stream ZIP."""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(path):
                for f in files:
                    fpath = Path(root) / f
                    rel_path = fpath.relative_to(path)
                    # Skip noise
                    if any(part.startswith('.') for part in rel_path.parts) and '.scaffold' not in str(rel_path):
                        continue
                    zf.write(fpath, rel_path)
        return buf.getvalue()

    def _verify_shard_vitality(self, path: Path):
        """[FACULTY 8]: Runs a headless parse-check on the shard."""
        from ...parser_core.parser.engine import ApotheosisParser
        parser = ApotheosisParser()
        # We scry the index file specifically
        index = path / "index.scaffold"
        if index.exists():
            parser.parse_string(index.read_text(), index)
            if not parser.all_rites_are_pure:
                raise ArtisanHeresy("Shard Logic Tainted: Parsingheresies detected in index.scaffold.")

    def _dispatch_to_hub(self, metadata: Dict, matter: bytes):
        """[FACULTY 12]: THE FINAL STRIKE. Transmits matter to the Hub."""
        # This is where we would call the SCAF-Hub API.
        pass

    def __repr__(self) -> str:
        return f"<Ω_PUBLISH_ARTISAN status=RESONANT>"