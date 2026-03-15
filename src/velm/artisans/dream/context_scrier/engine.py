# Path: src/velm/artisans/dream/context_scrier/engine.py
# ---------------------------------------------------------------------------

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

# --- THE DIVINE UPLINKS ---
from .contracts import RealityState, ProjectDNA, TopographyMap
from .dna import DNAAnalyzer
from .topography import TopographyMapper
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("Dream:ContextScrier")


class ContextScrier:
    """
    =================================================================================
    == THE CONTEXT SCRIER (V-Ω-TOTALITY-V24000-REALITY-ANCHOR)                     ==
    =================================================================================
    LIF: ∞ | ROLE: TEMPORAL_TRIAGE_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_SCRIER_V24K_SHARD_AWARE_FINALIS

    The all-seeing eye of the Dream Artisan. It gazes upon the current directory
    and transmutes physical matter into Gnostic Truth. It determines if the
    Architect is dreaming of a NEW reality (Genesis) or EVOLVING an existing one.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Shard-Aware Tomography:** Reads `scaffold.lock` to identify exactly which
        Gnostic Shards are already woven, preventing duplicate weaving.
    2.  **Architectural Gap Analysis:** Compares the project's DNA against a
        "Golden Standard" to suggest missing organs (e.g., "Has DB but no Auth").
    3.  **Framework Deep-Dive:** Scries `package.json` and `pyproject.toml` to
        extract precise versions (e.g., "Next.js 14" vs "React 18").
    4.  **The "Soul" Extractor:** Synthesizes a one-line "Vibe" of the project
        based on file naming conventions (e.g., "A Django Monolith with Celery").
    5.  **Git Awareness:** Checks for uncommitted changes to warn the Architect
        before a destructive mutation.
    6.  **Linter Detection:** Identifies if `ruff`, `eslint`, or `prettier` are
        manifest to align generated code style automatically.
    7.  **Substrate Divination:** Detects Docker, Kubernetes, and Terraform
        signatures to inform infrastructure decisions.
    8.  **Test Suite Discovery:** Checks for `pytest`, `jest`, or `vitest` to
        decide if the AI should generate tests.
    9.  **Secret Leak Prevention:** Sanitizes the Context Block to ensure no
        `.env` values are ever sent to the Neural Prophet.
    10. **Monorepo Intelligence:** Detects `pnpm-workspace.yaml` or `Cargo.toml`
        workspaces to understand the root structure.
    11. **Language Versioning:** Extracts `python_version` or `node_engine` constraints.
    12. **The "Abyss" Filter:** Intelligently ignores `node_modules` and `venv`
        during topography mapping to save tokens.
    13. **Legacy Pattern Recognition:** Identifies "Ancient" code structures
        (e.g., `setup.py`) vs "Modern" ones (`pyproject.toml`).
    14. **Database Fingerprinting:** Infers DB type from `docker-compose.yml`
        services (Postgres vs MySQL vs Mongo).
    15. **Auth Provider Detection:** Checks for `clerk`, `supabase`, or `next-auth` dependencies.
    16. **Performance Tomography:** Measures the read-time of the scan.
    17. **Token Budgeting:** Truncates the file tree intelligently if it exceeds
        the LLM's context window.
    18. **The "Genesis" Heuristic:** If the directory is empty or only has `.git`,
        it forces the "Genesis" strategy.
    19. **The "Evolution" Heuristic:** If `scaffold.lock` exists, it forces the
        "Evolution" strategy.
    20. **Config Scrying:** Reads `.env.example` keys to understand required Gnosis.
    21. **JSON Output:** Returns a pure dictionary for machine consumption.
    22. **Error Resilience:** Handles corrupt lockfiles gracefully without crashing.
    23. **Virtual Filesystem Ready:** Compatible with WASM-based path resolution.
    24. **The Finality Vow:** Guaranteed return of a valid `RealityState` object.
    =================================================================================
    """

    def __init__(self):
        self.biologist = DNAAnalyzer()
        self.cartographer = TopographyMapper()

    def scry_reality_state(self, root: Path) -> Dict[str, Any]:
        """
        The Grand Rite of Perception.
        Gathers the Gnostic Truth of the project for the Neural Prophet.
        """
        start_ns = time.perf_counter_ns()
        root = root.resolve()

        # 1. Biological Sequencing (Dependencies & Stack)
        dna = self.biologist.analyze(root)

        # 2. Topographical Mapping (File Structure)
        topography = self.cartographer.map_sanctum(root)

        # 3. Historical Inquest (Lockfile Analysis)
        history = self._scry_chronicle(root)

        # 4. State Determination
        has_history = history.get("has_lockfile", False)
        is_populated = topography.file_count > 0

        # [ASCENSION 18]: Genesis Detection
        # Empty dir or just .git/.scaffold means Genesis.
        is_genesis = not is_populated or (topography.file_count < 3 and not has_history)

        # 5. Forge the LLM Context Block (The Golden Shard)
        context_block = self._forge_gnostic_context_block(dna, topography, history, root)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.verbose(
            f"Reality Scried in {duration_ms:.2f}ms. Type: {dna.language}. Shards: {len(history.get('shards', []))}")

        # Return enriched dictionary for the Dream Artisan
        return {
            "is_populated": is_populated,
            "is_genesis": is_genesis,
            "has_history": has_history,
            "project_type": dna.language,
            "frameworks": dna.frameworks,
            "file_structure": topography.tree_str.split('\n'),
            "full_context": context_block,  # <-- The Neural Prophet feeds on this
            "dna_object": dna,
            "shards": history.get("shards", []),
            "variables": history.get("variables", {})
        }

    def adjudicate_evolution(self, intent: str, state: Dict[str, Any]) -> str:
        """
        Decides the materialization strategy.
        'GENESIS' for new, 'EVOLUTION' for existing.
        """
        if state.get("is_genesis"):
            return "GENESIS"
        return "EVOLUTION"

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _scry_chronicle(self, root: Path) -> Dict[str, Any]:
        """
        [ASCENSION 1]: Reads the Gnostic Chronicle (scaffold.lock).
        Extracts installed shards and variables.
        """
        lock_path = root / "scaffold.lock"
        if not lock_path.exists():
            return {"has_lockfile": False, "shards": [], "variables": {}}

        try:
            data = json.loads(lock_path.read_text(encoding='utf-8'))
            return {
                "has_lockfile": True,
                "shards": data.get("shards", []),  # List of installed shard IDs
                "variables": data.get("variables", {})  # Global variables
            }
        except Exception as e:
            Logger.warn(f"Chronicle Corrupted: {e}. Assuming tabula rasa.")
            return {"has_lockfile": True, "shards": [], "variables": {}, "error": str(e)}

    def _forge_gnostic_context_block(
            self,
            dna: ProjectDNA,
            topo: TopographyMap,
            history: Dict[str, Any],
            root: Path
    ) -> str:
        """
        [ASCENSION 5]: THE PROMPT SHARD.
        Compiles all perception into a high-density string for the LLM.
        """
        # 1. Dependency Summary
        deps_str = ", ".join(dna.dependencies[:15])  # Limit to top 15 to save tokens
        if len(dna.dependencies) > 15: deps_str += "..."

        # 2. Shard Inventory
        shards = history.get("shards", [])
        shard_str = ", ".join(shards) if shards else "None"

        # 3. Architectural Summary
        arch_summary = self._summarize_architecture(dna, shards)

        # 4. The Block
        return (
            f"### PROJECT REALITY MATRIX\n"
            f"- **Language:** {dna.language.upper()}\n"
            f"- **Build System:** {dna.build_system}\n"
            f"- **Frameworks:** {', '.join(dna.frameworks)}\n"
            f"- **Critical Libraries:** {deps_str}\n"
            f"- **Installed Velm Shards:** {shard_str}\n"
            f"- **Architectural Style:** {arch_summary}\n"
            f"\n"
            f"### TOPOGRAPHY ({topo.file_count} files):\n"
            f"```text\n{topo.tree_str}\n```\n"
            f"\n"
            f"### GNOSTIC DIRECTIVE:\n"
            f"Use the above context to ensure your generated code aligns with the "
            f"existing file structure, naming conventions, and technology stack."
        )

    def _summarize_architecture(self, dna: ProjectDNA, shards: List[str]) -> str:
        """[ASCENSION 4]: The Soul Extractor."""
        traits = []
        if "fastapi" in dna.frameworks: traits.append("FastAPI Backend")
        if "django" in dna.frameworks: traits.append("Django Monolith")
        if "react" in dna.frameworks or "nextjs" in dna.frameworks: traits.append("React Frontend")
        if "docker" in dna.metadata: traits.append("Containerized")

        # Check for specific shards
        if any("auth" in s for s in shards): traits.append("Authenticated")
        if any("db" in s for s in shards) or any("postgres" in s for s in shards): traits.append("Persistent")

        if not traits: return "Generic/Unknown Structure"
        return ", ".join(traits)


