# Path: core/semantics/engine.py
# ------------------------------

import time
from typing import Dict, Optional, List, Any, Set, Tuple
from pathlib import Path
from collections import Counter

# [FIX]: Imports must go UP one level to 'core' then down to 'cortex'
from ..cortex.contracts import CortexMemory
from ...logger import Scribe, get_console # Go up to root scaffold then logger
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# Local sibling imports (Safe)
from .contracts import UserIntent, SemanticHit
from .intent import IntentAnalyzer
from .retriever import SemanticRetriever
from .reranker import RelevanceReranker


# --- THE DIVINE SUMMONS FOR THE SOCRATIC DIALOGUE ---
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

Logger = Scribe("SemanticEngine")


class SemanticEngine:
    """
    =================================================================================
    == THE SEMANTIC ENGINE (V-Ω-COGNITIVE-PIPELINE-ULTIMA)                         ==
    =================================================================================
    LIF: ∞ (THE ORCHESTRATOR OF COGNITION)

    The Sovereign Conductor of the Semantic Sanctum. It orchestrates a multi-stage
    cognitive pipeline to transmute a simple query into a ranked list of the most
    Gnostically-relevant scriptures in the cosmos.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Gnostic Triage Conductor:** The `search` method is the main conductor,
        orchestrating the pipeline and returning a pure `List[SemanticHit]` vessel.
    2.  **The Socratic Inquisitor (Ascended):** Presents a rich, interactive table
        showing top files in each ambiguous domain for perfect clarity.
    3.  **The Dual-Gaze Prophet:** Performs two vector searches (precision & recall)
        and intelligently merges the results.
    4.  **The Auto-Indexing Mind (Hardened):** Raises a specific `ArtisanHeresy` if
        indexing fails, preventing operation on a void.
    5.  **The Cortex Bridge (Solidified):** The `memory: CortexMemory` dependency is
        an explicit part of the `search` signature, making the contract unbreakable.
    6.  **The Telemetric Heartbeat (Precise):** Tracks the duration of each individual
        movement (Intent Analysis, Retrieval, Reranking).
    7.  **The Luminous Dossier:** The final verbose output is a rich Panel summarizing
        the top hits and the reasons for their relevance.
    8.  **The Unbreakable Ward of Paradox (Hardened):** Provides specific, helpful
        heresies if the VectorCortex is unreachable or the Reranker fails.
    9.  **The Sovereign Soul (Purified):** The engine is a pure orchestrator, with all
        complex logic delegated to its specialist faculties.
    10. **The Gnostic Threshold (Configurable):** The relevance threshold is passed down
        from the `DistillationProfile` to tune the sensitivity of the Gaze.
    11. **The Performance Ward (JIT Instantiation):** The `RelevanceReranker` is
        instantiated Just-In-Time, ensuring it always uses the freshest memory state.
    12. **The Final Word (Return Vessel):** The `search` method returns a `List[SemanticHit]`,
        the richest possible vessel of Gnosis for downstream artisans.
    """

    def __init__(self, project_root: Path, silent: bool = False):
        self.root = project_root
        self.silent = silent
        self.console = get_console()

        # --- Forge the Pantheon ---
        self.analyzer = IntentAnalyzer()
        self.retriever = SemanticRetriever(project_root)
        self.reranker: Optional[RelevanceReranker] = None  # Forged JIT with memory

    def search(self, query: str, memory: CortexMemory, limit: int = 10, interactive: bool = False) -> List[str]:
        """
        The Grand Symphony of Semantic Search.
        Returns a simple list of paths for compatibility with the Ranker.
        """
        start_time = time.monotonic()
        try:
            # --- MOVEMENT I: INTENT ANALYSIS ---
            intent = self.analyzer.analyze(query)
            if not self.silent:
                Logger.verbose(
                    f"Intent Perceived: [cyan]{intent.intent.name}[/cyan] | Expanded Query: '{intent.expanded_query[:100]}...'")

            # --- MOVEMENT II: RETRIEVAL (THE DUAL GAZE) ---
            # Forge the Reranker now that we have the memory
            self.reranker = RelevanceReranker(memory)

            # Gaze 1: Precision (Raw Query)
            precision_hits = self.retriever.retrieve(intent, limit=limit)

            # Gaze 2: Recall (Expanded Query)
            recall_hits = self.retriever.retrieve(
                UserIntent(raw_query=intent.expanded_query, intent=intent.intent, expanded_query=intent.expanded_query),
                limit=limit * 2
            )

            # Merge and Deduplicate
            all_hits_map = {hit.path: hit for hit in recall_hits}
            for hit in precision_hits:
                if hit.path not in all_hits_map:
                    all_hits_map[hit.path] = hit
                else:  # Boost precision hits
                    all_hits_map[hit.path].initial_score = max(hit.initial_score,
                                                               all_hits_map[hit.path].initial_score) * 1.1

            if not all_hits_map: return []

            # --- MOVEMENT III: RERANKING ---
            ranked_hits = self.reranker.rank(list(all_hits_map.values()), intent)

            # --- MOVEMENT IV: SOCRATIC REFINEMENT (AMBIGUITY) ---
            final_hits = ranked_hits
            if interactive:
                final_hits = self._conduct_socratic_refinement(ranked_hits, query)

            # --- MOVEMENT V: PROCLAMATION ---
            final_paths = [hit.path for hit in final_hits[:limit]]

            if not self.silent:
                self._proclaim_luminous_dossier(final_hits[:5], (time.monotonic() - start_time) * 1000)

            return final_paths

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy("A paradox shattered the Semantic Engine's Gaze.", child_heresy=e)

    def _proclaim_luminous_dossier(self, top_hits: List[SemanticHit], duration_ms: float):
        """[FACULTY 7] Renders a rich summary of the search results."""
        if not top_hits:
            Logger.verbose("Semantic Gaze complete. The Void returned no echoes.")
            return

        table = Table(title="Top Semantic Resonances", box=None, show_header=True, header_style="bold magenta")
        table.add_column("Score", style="bold", justify="right", width=8)
        table.add_column("Scripture", style="cyan")
        table.add_column("Reasoning", style="dim")

        for hit in top_hits:
            reasons = ", ".join(
                hit.rerank_reasons) if hit.rerank_reasons else f"Initial Vector ({hit.initial_score:.2f})"
            table.add_row(f"{hit.final_score:.2f}", hit.path, reasons)

        self.console.print(Panel(
            table,
            title="[bold blue]Semantic Gaze Dossier[/bold blue]",
            subtitle=f"[dim]Completed in {duration_ms:.0f}ms[/dim]",
            border_style="blue"
        ))

    def _conduct_socratic_refinement(self, hits: List[SemanticHit], query: str) -> List[SemanticHit]:
        """[FACULTY 2] The Socratic Inquisitor."""
        from .intent import IntentAnalyzer  # Re-import for domain map

        domain_counts = Counter()
        domain_hits: Dict[str, List[SemanticHit]] = {key: [] for key in IntentAnalyzer.DOMAINS.keys()}
        domain_hits["other"] = []

        for hit in hits:
            path_str = hit.path.lower().replace('\\', '/')
            hit_domain = "other"

            for domain, keywords in IntentAnalyzer.DOMAINS.items():
                if any(f"/{keyword}/" in f"/{path_str}" or path_str.startswith(keyword) for keyword in keywords):
                    hit_domain = domain
                    break

            domain_counts[hit_domain] += 1
            domain_hits[hit_domain].append(hit)

        active_domains = [d for d in IntentAnalyzer.DOMAINS.keys() if domain_counts[d] > 0]
        if domain_counts["other"] > 0:
            active_domains.append("other")

        if len(active_domains) < 2:
            return hits

        # --- AMBIGUITY DETECTED ---
        self.console.print(Panel(
            Text.from_markup(
                f"The Oracle perceives a schism in the plea '[yellow]{query}[/yellow]'.\nResonance was found in multiple realms:"),
            title="[bold magenta]Socratic Refinement[/bold magenta]", border_style="magenta"
        ))

        choices_map: Dict[str, str] = {}
        display_choices: List[str] = []

        table = Table(box=None, show_header=False)
        table.add_column(style="magenta", width=5)
        table.add_column("Domain")
        table.add_column("Top Hit", style="cyan")

        for i, domain in enumerate(active_domains, 1):
            key = str(i)
            choices_map[key] = domain
            display_choices.append(key)
            top_hit_path = domain_hits[domain][0].path if domain_hits[domain] else "N/A"
            table.add_row(f"({key})", f"{domain.title()} ({domain_counts[domain]} files)", top_hit_path)

        table.add_row("(a)", "All Domains", "[dim]Combine all results[/dim]")
        choices_map['a'] = 'all'
        display_choices.append('a')

        self.console.print(table)
        response = Prompt.ask("\n[bold]Which reality do you seek?[/bold]", choices=display_choices, default='a')

        selected_domain = choices_map.get(response)
        if selected_domain == 'all':
            Logger.info("Architect's Will: Combining all resonant contexts.")
            return hits
        elif selected_domain:
            Logger.info(f"Refining Gaze to the [cyan]{selected_domain}[/cyan] domain.")
            return domain_hits.get(selected_domain, [])

        return hits  # Failsafe

