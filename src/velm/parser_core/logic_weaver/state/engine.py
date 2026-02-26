# Path: parser_core/logic_weaver/state/engine.py
# ----------------------------------------------

from pathlib import Path
from typing import Dict, Any, Optional, Generator
from ....logger import Scribe

from .memory import MemoryStratum
from .temporal import TemporalLoom
from .alchemy import TruthPurifier
from .topology import GeometricAnchor
from .forensics import HolographicTomographer
from .radiation import HUDMulticaster

Logger = Scribe("GnosticState")


class GnosticContext:
    """
    =================================================================================
    == THE GNOSTIC CONTEXT (V-Ω-TOTALITY-V15000-ORGAN-PATTERN)                     ==
    =================================================================================
    LIF: ∞ | ROLE: NEURAL_STACK_GOVERNOR | RANK: OMEGA_SUPREME
    AUTH_CODE: Ω_STATE_V15000_DIRECTORY_ASCENDED_FINALIS

    This is the Unified Facade. It behaves exactly like the ancient monolithic
    Context, providing 100% backward compatibility to the Logic Weaver, while
    internally delegating every action to its immortal, highly specialized Organs.
    =================================================================================
    """

    # [ASCENSION 2]: ZERO-OVERHEAD MEMORY FOOTPRINT
    __slots__ = (
        '_context', 'parent', 'id', 'name', 'depth', 'provenance', '_locks',
        'memory', 'temporal', 'alchemy', 'topology', 'forensics', 'radiator'
    )

    def __init__(
            self,
            raw_shared_context: Dict[str, Any],
            parent: Optional['GnosticContext'] = None,
            name: str = "root",
            depth: int = 0
    ):
        """The Rite of Inception. Sutures the Organs into the Body."""
        import uuid

        self._context = raw_shared_context if raw_shared_context is not None else {}
        self.parent = parent
        self.id = str(uuid.uuid4())[:8].upper()
        self.name = name
        self.depth = depth
        self.provenance: Dict[str, str] = {}
        self._locks: set = set()

        # --- ORCHESTRATION OF THE ORGANS ---
        self.memory = MemoryStratum(self)
        self.temporal = TemporalLoom(self)
        self.alchemy = TruthPurifier(self)
        self.topology = GeometricAnchor(self)
        self.forensics = HolographicTomographer(self)
        self.radiator = HUDMulticaster(self)

        # --- THE PRIMORDIAL AWAKENING ---
        self.topology.establish_root()
        self.topology.establish_manifest()
        self.alchemy.purify()

        if self.depth == 0:
            Logger.verbose(f"Multiversal Cortex Initialized. ID: {self.id}")

    # =========================================================================
    # == THE OMNISCIENT PROXY API (100% ISO-COMPATIBLE)                      ==
    # =========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        return self.memory.get(key, default)

    def set(self, key: str, value: Any, source: str = "internal", lock: bool = False):
        self.memory.set(key, value, source, lock)

    def __getitem__(self, key: str) -> Any:
        res = self.get(key)
        if res is None:
            raise KeyError(f"Variable '{key}' is unmanifest in the current lineage.")
        return res

    def mask(self, overrides: Dict[str, Any]) -> Generator['GnosticContext', None, None]:
        return self.temporal.mask(overrides)

    def spawn_child(self, name: str) -> 'GnosticContext':
        return self.temporal.spawn_child(name)

    def purify(self):
        self.alchemy.purify()

    def register_virtual_file(self, path: Path):
        self.topology.register_virtual_file(path)

    def scry(self, include_parents: bool = True) -> str:
        return self.forensics.scry(include_parents)

    @property
    def fingerprint(self) -> str:
        return self.forensics.fingerprint()

    @property
    def raw(self) -> Dict[str, Any]:
        """Returns the LIVE reference to the local Gnostic stratum."""
        return self._context

    @property
    def project_root(self) -> Path:
        """Absolute Gnostic Anchor."""
        return self._context.get('project_root', Path.cwd())

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_CONTEXT[{self.name}] id={self.id} depth={self.depth} hash={self.fingerprint[:8]}>"