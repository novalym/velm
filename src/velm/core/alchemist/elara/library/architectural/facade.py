# Path: core/alchemist/elara/library/architectural/facade.py
# ----------------------------------------------------------

from pathlib import Path
from typing import Any

from .iron.scryer import IronScryer
from .iron.forensics import IronForensics
from .topo.lattice import LatticeOracle
from .topo.vectors import VectorOracle
from .akasha.chronicle import GitChronicle
from .akasha.temporal import TemporalOracle
from .substrate.vitals import SystemVitals
from .substrate.network import NetworkOracle
from .substrate.security import SecurityOracle
from .polyglot.divination import LinguisticDiviner
from .polyglot.transmutation import RosettaTransmuter

class IronProxy:
    """
    =============================================================================
    == THE IRON PROXY (THE PHYSICAL REALM)                                     ==
    =============================================================================
    Delegates perception of physical matter, disk IO, and file forensics.
    """
    def __init__(self, root: Path):
        self.scryer = IronScryer(root)
        self.forensics = IronForensics(root)

    # Exposed Rites
    def read(self, path_str: str) -> Any: return self.scryer.read(path_str)
    def exists(self, path_str: str) -> bool: return self.scryer.exists(path_str)
    def mime(self, path_str: str) -> str: return self.scryer.mime(path_str)
    def checksum(self, path_str: str) -> str: return self.forensics.checksum(path_str)
    def complexity(self, path_str: str) -> dict: return self.forensics.complexity(path_str)
    def glob(self, pattern: str) -> list: return self.scryer.glob(pattern)

class TopoProxy:
    """
    =============================================================================
    == THE TOPO PROXY (THE CAUSAL WEB)                                         ==
    =============================================================================
    Delegates perception of the Abstract Syntax Tree, DAGs, and dependencies.
    """
    def __init__(self, engine_ref: Any):
        self.lattice = LatticeOracle(engine_ref)
        self.vectors = VectorOracle(engine_ref)

    def is_imported(self, symbol: str) -> bool: return self.lattice.is_imported(symbol)
    def dependents(self, path_str: str) -> list: return self.lattice.dependents(path_str)
    def is_circular(self) -> bool: return self.lattice.is_circular()
    def similarity(self, a: str, b: str) -> float: return self.vectors.similarity(a, b)

class AkashaProxy:
    """
    =============================================================================
    == THE AKASHA PROXY (THE TEMPORAL REALM)                                   ==
    =============================================================================
    Delegates perception of Git history, time, authors, and provenance.
    """
    def __init__(self, engine_ref: Any):
        self.chronicle = GitChronicle()
        self.temporal = TemporalOracle()

    @property
    def last_strike(self): return self.chronicle.last_strike
    @property
    def git_hash(self): return self.chronicle.git_hash
    def author_of(self, path: str): return self.chronicle.author_of(path)
    def age(self, path: str): return self.temporal.age(path)

class SubstrateProxy:
    """
    =============================================================================
    == THE SUBSTRATE PROXY (THE HARDWARE REALM)                                ==
    =============================================================================
    Delegates perception of CPU, RAM, OS, Networking, and Container state.
    """
    def __init__(self):
        self.vitals = SystemVitals()
        self.network = NetworkOracle()
        self.security = SecurityOracle()

    @property
    def has_gpu(self) -> bool: return self.vitals.has_gpu
    @property
    def is_container(self) -> bool: return self.security.is_container
    def can_run(self, binary: str) -> bool: return self.vitals.can_run(binary)
    def port_open(self, port: int) -> bool: return self.network.port_open(port)
    def find_free_port(self, start: int) -> int: return self.network.find_free_port(start)

class PolyglotProxy:
    """
    =============================================================================
    == THE POLYGLOT PROXY (THE LINGUISTIC REALM)                               ==
    =============================================================================
    Delegates code translation, syntax detection, and AST unparsing.
    """
    def __init__(self):
        self.diviner = LinguisticDiviner()
        self.transmuter = RosettaTransmuter()

    def detect(self, content: str) -> str: return self.diviner.detect(content)
    def format(self, code: str, lang: str) -> str: return self.transmuter.format(code, lang)
    def translate(self, code: str, lang: str) -> str: return self.transmuter.translate(code, lang)