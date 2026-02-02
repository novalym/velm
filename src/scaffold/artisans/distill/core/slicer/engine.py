# Path: artisans/distill/core/slicer/engine.py
# --------------------------------------------

from pathlib import Path
from typing import List, Optional, Any

from .contracts import SliceProfile
from .graph import SemanticGraph
from .languages.python import PythonAdapter
from .weavers.facade import SurgicalWeaverFacade
from .....logger import Scribe

Logger = Scribe("CausalSlicer")


class CausalSlicer:
    """
    =============================================================================
    == THE CAUSAL SLICER (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                       ==
    =============================================================================
    @gnosis:title The Causal Slicer
    @gnosis:summary The divine, sentient God-Engine of Surgical Code Extraction.
    """

    def __init__(self, root: Path, focus_symbols: List[str]):
        self.root = root
        self.profile = SliceProfile(focus_symbols=focus_symbols)
        self.weaver = SurgicalWeaverFacade()

    def slice(self, file_path: Path, content: str) -> str:
        """The Grand Rite of Slicing."""
        if not self.profile.focus_symbols:
            return content

        # 1. Adapter Selection
        adapter = self._get_adapter(file_path)
        if not adapter:
            return content

        try:
            # 2. Parse into Symbol Nodes
            nodes = adapter.parse(content)
            if not nodes:
                return content

                # 3. Build Graph
            graph = SemanticGraph()
            for n in nodes:
                # Basic parent linking is done by adapter usually, but we ensure it here if needed
                # (For V1 PythonAdapter, child processing is recursive, so relationships exist)
                graph.add_node(n)

            # 4. Calculate Relevance
            scores = graph.calculate_relevance(set(self.profile.focus_symbols))

            # 5. Weave the Final Scripture
            sliced_content = self.weaver.weave(
                file_path=file_path,
                content=content,
                scores=scores,
                graph_roots=graph.roots
            )

            # Logger.verbose(f"Sliced '{file_path.name}'.")
            return sliced_content

        except Exception as e:
            Logger.warn(f"Slicing paradox for {file_path.name}: {e}")
            return content

    def _get_adapter(self, path: Path):
        """THE POLYGLOT MIND"""
        if path.suffix == '.py':
            return PythonAdapter()
        return None

