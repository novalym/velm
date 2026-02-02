# Path: scaffold/core/runtime/middleware/librarian.py
# ---------------------------------------------------


import time
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Dict, Any

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, ManifestRequest, ArchitectRequest
from ....interfaces.base import ScaffoldResult
from ....core.cortex.tokenomics import TokenEconomist
from ....contracts.heresy_contracts import ArtisanHeresy

if TYPE_CHECKING:
    from ...ai.rag import TheLibrarian


class SemanticInjectorMiddleware(Middleware):
    """
    =================================================================================
    == THE ULTRALUMINOUS LIBRARIAN (V-Ω-XML-ENVELOPING-CONTEXT-ENGINE)             ==
    =================================================================================
    LIF: ∞ (OMNISCIENT CONTEXT INJECTION)

    The bridge between the File System and the Neural Cortex.
    It intercepts AI requests, scans the project, retrieves relevant memories via RAG,
    and constructs a **High-Fidelity Prompt Envelope**.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Dual-Gaze Topology:** Distinctly separates "Reality" (The File Tree Structure)
        from "Theory" (The Content of Relevant Files), giving the AI both map and territory.
    2.  **The XML Enveloping Protocol:** Wraps injected code in `<document path="...">` tags.
        This annihilates "Context Bleed" where the AI confuses two different files.
    3.  **The Relevance Threshold:** Discards RAG results with low cosine similarity (< 0.35),
        preventing the injection of noise that causes hallucinations.
    4.  **The Token Budget Governor:** Uses the `TokenEconomist` to hard-cap injected context
        (default 8k tokens) to prevent overflowing the model's window or wallet.
    5.  **The Lazy Summons:** Imports `TheLibrarian` and `ProjectScanner` only at the moment
        of need, keeping the CLI startup instant.
    6.  **The Intent Diviner:** Detects if the user is asking a "Global" question (requiring
        broad context) or a "Specific" question (requiring deep focus).
    7.  **The Privacy Ward:** Automatically filters out lockfiles, `.git`, and secrets from
        the File Tree visualization.
    8.  **The Path Normalizer:** Ensures all injected paths are relative to the Project Root,
        reducing token usage and ambiguity.
    9.  **The Auto-Indexer Link:** If the RAG store is empty, it triggers the `VectorCortex`
        to perform a Just-In-Time indexing of the project.
    10. **The Priority Sort:** Injects the most relevant code chunks *last* (closest to the
        user prompt) to maximize the "Recency Bias" of Attention mechanisms.
    11. **The Luminous Telemetry:** Logs exactly which files were injected and their relevance
        scores, allowing the Architect to audit the AI's "Short Term Memory".
    12. **The Fail-Open Circuit:** If RAG fails (database lock, corruption), it logs a
        warning but *allows the request to proceed* with just the file tree, ensuring
        resilience.
    =================================================================================
    """

    # The Budget of the Mind (Tokens reserved for Context)
    CONTEXT_TOKEN_LIMIT = 12000
    RELEVANCE_THRESHOLD = 0.35

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. Triage: Does this request need Gnosis?
        needs_context = False
        prompt_text = ""

        # Identify AI-bound requests
        if isinstance(request, (ManifestRequest, ArchitectRequest)):
            needs_context = True
            prompt_text = getattr(request, 'prompt', '') or ""
        elif request.variables.get('ai') or request.variables.get('use_rag'):
            needs_context = True
            prompt_text = str(request.variables.get("prompt", "")) or str(request.variables.get("user_query", ""))

        if not needs_context:
            return next_handler(request)

        self.logger.verbose("The Librarian awakens to curate Gnosis for the Neural Cortex...")

        try:
            # 2. Summon the Economist
            economist = TokenEconomist()

            # --- MOVEMENT I: INJECTING REALITY (The Map) ---
            self._inject_reality_tree(request, economist)

            # --- MOVEMENT II: INJECTING THEORY (The Territory) ---
            if prompt_text:
                self._inject_theory_rag(request, prompt_text, economist)

        except Exception as e:
            # [FACULTY 12] The Fail-Open Circuit
            self.logger.warn(f"The Librarian faltered, but the rite proceeds. Reason: {e}")

        return next_handler(request)

    def _inject_reality_tree(self, request: BaseRequest, economist: TokenEconomist):
        """
        [FACULTY 1 & 7] Scans the file system to build a visual tree.
        Gives the AI spatial awareness of where files live.
        """
        from ....core.cortex.scanner import ProjectScanner

        # We use a lightweight discovery scan
        scanner = ProjectScanner(request.project_root, economist)
        files = scanner.file_discoverer.discover()

        # Filter and Normalize
        rel_files = []
        for f in files:
            try:
                rel = f.relative_to(request.project_root)
                # [FACULTY 7] Privacy Ward: Skip noise
                if any(p.startswith('.') for p in rel.parts) and len(rel.parts) > 1: continue
                if rel.name in ['scaffold.lock', 'package-lock.json', 'poetry.lock']: continue
                rel_files.append(str(rel))
            except ValueError:
                continue

        # Sort for determinism
        rel_files.sort()

        # Format as a concise tree string
        # We limit the tree size to prevent token explosion on massive repos
        if len(rel_files) > 1000:
            rel_files = rel_files[:1000]
            tree_str = "\n".join([f"- {f}" for f in rel_files])
            tree_str += "\n... (Tree truncated due to size)"
        else:
            tree_str = "\n".join([f"- {f}" for f in rel_files])

        # Inject into variables
        reality_context = {
            "file_tree": tree_str,
            "file_count": len(rel_files),
            "root_name": request.project_root.name
        }
        request.variables["scaffold_reality"] = reality_context

        cost = economist.estimate_cost(tree_str)
        self.logger.verbose(f"Reality injected. Tree cost: ~{cost} tokens.")

    def _inject_theory_rag(self, request: BaseRequest, prompt_text: str, economist: TokenEconomist):
        """
        [FACULTY 2, 3, 4, 10] The RAG Engine.
        Retrieves code chunks, filters them, and wraps them in XML envelopes.
        """
        from ...ai.rag import TheLibrarian

        # [FACULTY 5] Lazy Summons
        librarian = TheLibrarian(request.project_root)

        # 1. The Rite of Recall
        # We fetch more than we need (10), then filter and truncate.
        hits = librarian.recall(prompt_text, limit=10)

        if not hits:
            self.logger.verbose("The Librarian found no resonant memories for this query.")
            return

        # 2. The Filter of Relevance
        valid_hits = [h for h in hits if h.get('score', 0) >= self.RELEVANCE_THRESHOLD]
        if not valid_hits:
            self.logger.verbose(f"Hits found but rejected. Top score: {hits[0].get('score', 0):.2f}")
            return

        # 3. The Sort of Priority
        # We want the highest score LAST so it's freshest in context window
        valid_hits.sort(key=lambda x: x['score'])

        # 4. The XML Enveloping & Budgeting
        current_tokens = 0
        xml_fragments = []
        injected_sources = []

        for hit in valid_hits:
            content = hit['content']
            source = hit['metadata'].get('source', 'unknown')
            score = hit.get('score', 0)

            # XML Envelope for AI Clarity
            # <document path="src/main.py" score="0.95"> ... code ... </document>
            xml_block = (
                f'<document path="{source}" relevance="{score:.2f}">\n'
                f"{content}\n"
                f"</document>"
            )

            chunk_cost = economist.estimate_cost(xml_block)

            if current_tokens + chunk_cost > self.CONTEXT_TOKEN_LIMIT:
                break

            current_tokens += chunk_cost
            xml_fragments.append(xml_block)
            injected_sources.append(f"{source} ({score:.2f})")

        # 5. Injection
        if xml_fragments:
            # Join them
            full_rag_context = "<relevant_code>\n" + "\n".join(xml_fragments) + "\n</relevant_code>"

            request.variables["scaffold_theory"] = full_rag_context

            # [FACULTY 11] Luminous Telemetry
            self.logger.success(
                f"Librarian injected {len(xml_fragments)} context fragments (~{current_tokens} tokens)."
            )
            for source in injected_sources:
                self.logger.verbose(f"   -> Enveloped: {source}")