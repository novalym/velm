# Path: scaffold/artisans/tool/sbom_artisan.py
# --------------------------------------------

import json
from datetime import datetime, timezone
from pathlib import Path

from ...core.artisan import BaseArtisan
from ...interfaces.requests import SBOMRequest
from ...interfaces.base import ScaffoldResult
from ...utils import atomic_write
from ... import __version__




class SBOMArtisan(BaseArtisan[SBOMRequest]):
    """
    =============================================================================
    == THE SCRIBE OF ORIGINS (SOFTWARE BILL OF MATERIALS)                      ==
    =============================================================================
    Chronicles the Gnostic DNA of the project in SPDX format.
    """

    def execute(self, request: SBOMRequest) -> ScaffoldResult:
        self.logger.info("The Scribe of Origins awakens to chronicle the project's lineage...")

        lock_path = self.project_root / "scaffold.lock"
        if not lock_path.exists():
            return self.failure("The Gnostic Chronicle (scaffold.lock) is a void. Cannot generate SBOM.")

        lock_data = json.loads(lock_path.read_text())
        manifest = lock_data.get("manifest", {})

        # --- Forge the SPDX Document ---
        doc = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": self.project_root.name,
            "documentNamespace": f"http://spdx.org/spdxdocs/{self.project_root.name}-{lock_data['provenance']['rite_id']}",
            "creationInfo": {
                "created": datetime.now(timezone.utc).isoformat(),
                "creators": [f"Tool: scaffold-cli-{__version__}"]
            },
            "packages": [],
            "relationships": []
        }

        # Main package representing the project
        main_pkg = {
            "name": self.project_root.name,
            "SPDXID": "SPDXRef-Project",
            "versionInfo": lock_data['provenance'].get('git_commit', '0.1.0'),
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "supplier": f"Organization: {lock_data['provenance'].get('architect', 'Unknown')}"
        }
        doc['packages'].append(main_pkg)

        # Add packages for each blueprint origin
        origins = {meta.get("blueprint_origin") for meta in manifest.values() if meta.get("blueprint_origin")}
        for i, origin in enumerate(origins):
            pkg = {
                "name": Path(origin).name,
                "SPDXID": f"SPDXRef-Blueprint-{i}",
                "downloadLocation": "NOASSERTION" if 'remote' not in origin else origin,
                "filesAnalyzed": False,
                "supplier": "NOASSERTION"
            }
            doc['packages'].append(pkg)

            # Relate blueprint to main project
            doc['relationships'].append({
                "spdxElementId": "SPDXRef-Project",
                "relationshipType": "GENERATED_FROM",
                "relatedSpdxElementId": f"SPDXRef-Blueprint-{i}"
            })

        # --- Inscribe the Scripture ---
        output_path = self.project_root / request.output
        atomic_write(output_path, json.dumps(doc, indent=2), self.logger, self.project_root)

        return self.success(f"Software Bill of Materials inscribed at '{request.output}'.")