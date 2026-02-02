# Path: core/cortex/engine/perception.py
# --------------------------------------

import hashlib
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

from ..contracts import CortexMemory
from ..graph_builder import GraphBuilder
from ..scanner import ProjectScanner
from ..tokenomics import TokenEconomist
from ..git_historian import GitHistorian
from ..file_interrogator import FileInterrogator
from ....logger import Scribe
import os

Logger = Scribe("PerceptionEngine")


class PerceptionEngine:
    """
    =================================================================================
    == THE PERCEPTION ENGINE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-PURE)                  ==
    =================================================================================
    @gnosis:title The Perception Engine
    @gnosis:summary The divine, stateless, and pure artisan that forges the Gnostic Memory.
    @gnosis:LIF INFINITY
    @gnosis:auth_code:)#@()#(!

    The Eyes and Ears of the Cortex. It is a pure, functional God-Engine. It receives
    Gnosis of a past reality, performs a deep scan of the present, and proclaims a
    new, perfected scripture of memory. It holds no state. Its every rite is a pure
    transmutation.
    """

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.economist = TokenEconomist()
        self.git_historian = GitHistorian(self.root)
        self.ignore_patterns: List[str] = []
        self.include_patterns: List[str] = []
        # The Interrogator's cache is bound to the lifecycle of this engine instance.
        self._interrogator_cache: Dict[str, Any] = {}

    def configure_filters(self, ignore: List[str] = None, include: List[str] = None):
        """[FACULTY 5] Bestows the Gaze of Aversion upon the engine."""
        if ignore: self.ignore_patterns.extend(ignore)
        if include: self.include_patterns.extend(include)

    def perceive(self) -> CortexMemory:
        """The Grand Rite of Perception. Forges a new memory from the void."""
        scanner = ProjectScanner(
            root=self.root, economist=self.economist,
            ignore_patterns=self.ignore_patterns, include_patterns=self.include_patterns
        )

        self.git_historian.inquire_all()
        # The scanner returns its new cache, which we adopt.
        inventory, project_gnosis = scanner.scan()
        self._interrogator_cache = scanner.new_cache

        if not inventory:
            Logger.warn("The Gaze found only a void. No analyzable scriptures manifest.")
            return CortexMemory(inventory=[], project_gnosis={}, dependency_graph={}, timestamp=time.time(), gnostic_hash="")

        Logger.verbose("Summoning the Gnostic Cartographer to map the cosmos...")
        graph_builder = GraphBuilder(self.root, inventory, project_gnosis)
        graph_data = graph_builder.build()

        return CortexMemory(
            inventory=inventory,
            project_gnosis=project_gnosis,
            dependency_graph=graph_data,
            co_change_graph=self.git_historian.co_change_graph,
            symbol_multimap=graph_builder.symbol_multimap,
            timestamp=time.time(),
            gnostic_hash=hashlib.sha256(str(time.time()).encode()).hexdigest()
        )

    def ingest_file(self, path: Path, memory: CortexMemory) -> CortexMemory:
        """
        [THE LAW OF GNOSTIC DOWRY - THE CORE FIX]
        Receives the current memory, ingests the new Gnosis, and returns a NEW,
        perfected memory object. The heresy of the implicit state is annihilated.
        """
        try:
            rel_path_str = os.path.relpath(path, self.root).replace('\\', '/')
        except ValueError:
            return memory # File is outside project, no change

        interrogator = FileInterrogator(
            root=self.root, economist=self.economist, git_historian=self.git_historian,
            cache=self._interrogator_cache, new_cache=self._interrogator_cache # Use same dict for read/write
        )
        gnosis, ast_dossier = interrogator.interrogate(path)

        if not gnosis:
            return self.forget_file(path, memory) # If interrogation fails, it's a deletion

        # --- THE RITE OF IMMUTABLE ASCENSION ---
        new_inventory = [i for i in memory.inventory if i.path.as_posix() != rel_path_str]
        new_inventory.append(gnosis)

        new_project_gnosis = memory.project_gnosis.copy()
        if ast_dossier:
            new_project_gnosis[rel_path_str] = ast_dossier
        elif rel_path_str in new_project_gnosis:
            del new_project_gnosis[rel_path_str]

        graph_builder = GraphBuilder(self.root, new_inventory, new_project_gnosis)
        new_dependency_graph = graph_builder.build()

        new_memory = CortexMemory(
            inventory=new_inventory, project_gnosis=new_project_gnosis,
            dependency_graph=new_dependency_graph, timestamp=time.time(),
            gnostic_hash=memory.gnostic_hash, # Stale, but preserved
            co_change_graph=memory.co_change_graph,
            symbol_multimap=graph_builder.symbol_multimap
        )
        return new_memory

    def forget_file(self, path: Path, memory: CortexMemory) -> CortexMemory:
        """
        [THE LAW OF GNOSTIC DOWRY - THE CORE FIX]
        Receives the current memory, removes the forgotten soul, and returns a
        NEW, perfected memory object.
        """
        try:
            rel_path_str = os.path.relpath(path, self.root).replace('\\', '/')
        except ValueError:
            return memory # File outside project

        if not any(i.path.as_posix() == rel_path_str for i in memory.inventory):
            return memory # File was never known

        # --- THE RITE OF IMMUTABLE ASCENSION ---
        new_inventory = [i for i in memory.inventory if i.path.as_posix() != rel_path_str]

        new_project_gnosis = memory.project_gnosis.copy()
        if rel_path_str in new_project_gnosis:
            del new_project_gnosis[rel_path_str]

        graph_builder = GraphBuilder(self.root, new_inventory, new_project_gnosis)
        new_dependency_graph = graph_builder.build()

        new_memory = CortexMemory(
            inventory=new_inventory, project_gnosis=new_project_gnosis,
            dependency_graph=new_dependency_graph, timestamp=time.time(),
            gnostic_hash=memory.gnostic_hash,
            co_change_graph=memory.co_change_graph,
            symbol_multimap=graph_builder.symbol_multimap
        )
        return new_memory