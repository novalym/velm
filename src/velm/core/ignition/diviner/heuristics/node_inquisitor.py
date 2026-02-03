# Path: scaffold/core/ignition/diviner/heuristics/node_inquisitor.py
# -----------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_NODE_INQUISITOR_V1

import json
from pathlib import Path
from typing import Tuple, List
from .base import BaseInquisitor
from ...contracts import IgnitionAura

class NodeInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE NODE INQUISITOR (V-Ω-JS-TOMOGRAPHY)                                 ==
    =============================================================================
    Performs deep manifest analysis for the Node.js ecosystem.
    """

    def analyze(self, root: Path) -> Tuple[IgnitionAura, float, List[str]]:
        manifest_path = root / "package.json"
        if not manifest_path.exists():
            return IgnitionAura.GENERIC, 0.0, []

        try:
            data = json.loads(self.read_manifest_safe(manifest_path))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            scripts = data.get("scripts", {})

            # [ASCENSION 3]: DEPENDENCY TREE INQUEST
            if "next" in deps:
                return IgnitionAura.NEXT, 0.99, ["Next.js found in dependencies."]
            if "nuxt" in deps:
                return IgnitionAura.NUXT, 0.99, ["Nuxt found in dependencies."]
            if "astro" in deps:
                return IgnitionAura.ASTRO, 0.99, ["Astro found in dependencies."]
            if "vite" in deps:
                # [ASCENSION 4]: DIALECT SCRYING
                flavor = "Generic"
                if "react" in deps: flavor = "React"
                if "vue" in deps: flavor = "Vue"
                if "svelte" in deps: return IgnitionAura.SVELTE, 0.99, ["Vite + Svelte detected."]
                return IgnitionAura.VITE, 0.98, [f"Vite ({flavor}) detected."]

            if "express" in deps:
                return IgnitionAura.GENERIC, 0.8, ["Express.js backend detected."]

            # [ASCENSION 7]: WORKSPACE AWARENESS
            if "workspaces" in data:
                return IgnitionAura.GENERIC, 0.9, ["Node.js Workspace root detected."]

            return IgnitionAura.GENERIC, 0.4, ["Standard package.json detected."]

        except Exception as e:
            return IgnitionAura.GENERIC, 0.1, [f"Node Inquest Fracted: {str(e)}"]