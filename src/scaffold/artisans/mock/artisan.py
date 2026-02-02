# Path: scaffold/artisans/mock/artisan.py
# ---------------------------------------

import shutil
from pathlib import Path
from typing import List

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import MockRequest
from ...help_registry import register_artisan
from ...contracts.data_contracts import ScaffoldItem, InscriptionAction
from ...core.kernel.transaction import GnosticTransaction
from ...creator import create_structure


@register_artisan("mock")
class MockingbirdArtisan(BaseArtisan[MockRequest]):
    """
    =============================================================================
    == THE MOCKINGBIRD (V-Ω-TEST-FIXTURE-GENERATOR)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Generates a temporary, dummy file structure based on a simple spec string.
    Essential for creating reproduction cases or testing traversal logic.
    """

    def execute(self, request: MockRequest) -> ScaffoldResult:
        root = (self.project_root / (request.root or "mock_env")).resolve()

        # Safety: Don't mock in non-empty dir unless forced?
        # For mocks, we usually want to wipe and recreate.
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"The Mockingbird sings in [cyan]{root.name}[/cyan]...")

        # 1. Parse Spec
        # Format: "src/main.py,tests/,README.md"
        paths = [p.strip() for p in request.spec.split(',')]
        items: List[ScaffoldItem] = []

        for p in paths:
            is_dir = p.endswith('/')
            path_obj = Path(p)

            content = None
            if not is_dir:
                # Basic dummy content
                content = f"# Mock content for {path_obj.name}\n"

            items.append(ScaffoldItem(
                path=path_obj,
                is_dir=is_dir,
                content=content,
                line_num=0
            ))

        # 2. Materialize via QuantumCreator
        # We use a transaction to ensure atomicity even for mocks
        with GnosticTransaction(root, "Mockingbird Creation", use_lock=False) as tx:
            create_structure(
                scaffold_items=items,
                base_path=root,
                transaction=tx,
                silent=True  # Mocks should be quiet
            )

        # 3. Proclaim
        return self.success(
            f"Mock environment created at {root}.",
            artifacts=[Artifact(path=root, type="directory", action="created")]
        )