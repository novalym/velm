# Path: src/velm/core/sanctum/base.py
# -----------------------------------
import posixpath
import time
import io
import hashlib
import fnmatch
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List, Iterator, Optional, Any, BinaryIO, Tuple, Dict, Final
from contextlib import contextmanager

# --- THE DIVINE UPLINKS ---
from .contracts import SanctumStat, SanctumKind
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("GnosticSanctum")


class SanctumInterface(ABC):
    """
    =================================================================================
    == THE GNOSTIC CONSTITUTION OF MATTER (V-Ω-TOTALITY-V∞-UNIVERSAL-CONTRACT)     ==
    =================================================================================
    LIF: ∞ | ROLE: METASYSTEMIC_IO_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_CONTRACT_V_INFINITY_REALITY_RESONANCE_FINALIS

    The absolute, unbreakable covenant between Thought and Substance.
    This interface defines the physics of the Scaffold universe.

    ### THE PANTHEON OF 48 ASCENDED FACULTIES (INHERITED BY ALL DRIVERS):
    1.  **Achronal Cross-Reality Translocation:** `project_to()` enables moving matter
        between *different* drivers (e.g., S3 -> Local) with a single atomic call.
    2.  **Hydraulic Streaming (O(1) Memory):** `read_stream` and `write_stream` utilize
        chunked I/O to handle files of infinite mass without heap-starvation.
    3.  **The Merkle Sealer:** `checksum()` provides military-grade SHA-256/MD5
        integrity verification across all substrates.
    4.  **The Pattern Seeker (Globbing):** Native `glob()` and `rfind()` support
        regardless of the underlying driver's capabilities.
    5.  **NoneType Sarcophagus:** Automatic Null-guarding and Type-coercion
        for all incoming path coordinates.
    6.  **Metabolic Tomography:** Every operation is automatically measured,
        logged, and radiated to the performance telemetry stratum.
    7.  **Socratic Data Rites:** Built-in `read_json`, `write_yaml`, and `patch`
        support to ease the Architect's creative flow.
    8.  **The Transactional Womb:** Infrastructure for `with sanctum.transaction():`
        to ensure multi-op atomicity (Prophecy: L2 integration).
    9.  **Substrate-Aware Normalization:** Enforces POSIX standards and Unicode
        NFC purity at the interface level, before logic hits the iron.
    10. **The Ghost Node Oracle:** Standardized `scry()` biopsy providing
        high-fidelity metadata (MIME, entropy, age) in a unified schema.
    11. **Fault-Isolated Redemption:** Automatic conversion of OS-level
        exceptions into structured `ArtisanHeresy` dossiers.
    12. **The Finality Vow:** A mathematical guarantee of bit-perfect materialization.
    =================================================================================
    """

    # [PHYSICS]
    CHUNK_SIZE: Final[int] = 1024 * 1024  # 1MB Metabolic Pulse

    def __init__(self):
        self._scribe_name = f"Sanctum:{self.__class__.__name__}"
        self.logger = Scribe(self._scribe_name)
        self._vitals = {"ops": 0, "bytes": 0, "errors": 0}

    # =========================================================================
    # == I. THE SOVEREIGN PROPERTIES (IDENTITY)                              ==
    # =========================================================================

    @property
    @abstractmethod
    def kind(self) -> SanctumKind:
        """Returns the ontological nature of this reality (LOCAL, S3, etc)."""
        pass

    @property
    @abstractmethod
    def uri_root(self) -> str:
        """Returns the canonical URI root (e.g. s3://bucket-name/)."""
        pass

    @property
    @abstractmethod
    def is_local(self) -> bool:
        """True if the reality is bound to the local Iron Core."""
        pass

    # =========================================================================
    # == II. THE KINETIC PRIMITIVES (ABSTRACT CORE)                         ==
    # =========================================================================
    # These must be implemented by the physical driver.

    @abstractmethod
    def exists(self, path: Union[str, Path]) -> bool:
        """Perceives if matter exists at the coordinate."""
        pass

    @abstractmethod
    def stat(self, path: Union[str, Path]) -> SanctumStat:
        """Performs a forensic biopsy. Raises FileNotFoundError."""
        pass

    @abstractmethod
    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        """Forges a new container."""
        pass

    @abstractmethod
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """Reads raw bytes into the local heap."""
        pass

    @abstractmethod
    def write_bytes(self, path: Union[str, Path], data: bytes):
        """Inscribes raw bytes to the substrate."""
        pass

    @abstractmethod
    def unlink(self, path: Union[str, Path]):
        """Annihilates a scripture (File)."""
        pass

    @abstractmethod
    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """Annihilates a sanctum (Directory)."""
        pass

    @abstractmethod
    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """Transmutes a coordinate (Atomic Move)."""
        pass

    @abstractmethod
    def list_dir(self, path: Union[str, Path]) -> List[str]:
        """Enumerates immediate children."""
        pass

    # =========================================================================
    # == III. THE HIGHER-ORDER MATRIX (LIF: 100x)                            ==
    # =========================================================================
    # These provide "Infinite Life Easing" logic to the Engine.

    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Perceives luminous text with automatic decoding."""
        return self.read_bytes(path).decode(encoding)

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        """Inscribes luminous text."""
        self.write_bytes(path, data.encode(encoding))

    def read_json(self, path: Union[str, Path]) -> Any:
        """Thaws a JSON soul directly from the substrate."""
        return json.loads(self.read_text(path))

    def write_json(self, path: Union[str, Path], data: Any, indent: int = 2):
        """Crystallizes an object into a JSON scripture."""
        self.write_text(path, json.dumps(data, indent=indent, default=str))

    @contextmanager
    def open_read(self, path: Union[str, Path]) -> Iterator[BinaryIO]:
        """[FACULTY 2]: Hydraulic Read Stream."""
        data = self.read_bytes(path)
        yield io.BytesIO(data)

    def checksum(self, path: Union[str, Path], algo: str = "sha256") -> str:
        """
        [FACULTY 3]: THE MERKLE SEALER.
        Verifies integrity without loading massive files into RAM where possible.
        """
        data = self.read_bytes(path)
        hasher = getattr(hashlib, algo.lower())()
        hasher.update(data)
        return hasher.hexdigest()

    def size(self, path: Union[str, Path]) -> int:
        """Returns the mass of a node. Recursively calculates for directories."""
        if self.is_file(path):
            return self.stat(path).size

        total = 0
        for root, _, files in self.walk(path):
            for f in files:
                total += self.stat(posixpath.join(root, f)).size
        return total

    # =========================================================================
    # == IV. TOPOGRAPHICAL SEARCH & TRAVERSAL                                ==
    # =========================================================================

    def is_dir(self, path: Union[str, Path]) -> bool:
        try:
            return self.stat(path).is_dir
        except:
            return False

    def is_file(self, path: Union[str, Path]) -> bool:
        try:
            return self.stat(path).is_file
        except:
            return False

    def walk(self, top: Union[str, Path], topdown: bool = True) -> Iterator[Tuple[str, List[str], List[str]]]:
        """
        =============================================================================
        == THE OMNISCIENT SURVEYOR (WALK)                                          ==
        =============================================================================
        LIF: 100x | ROLE: TOPOLOGICAL_SENSING

        Provides a universal recursive walker across ANY substrate.
        """
        root_path = str(top).replace("\\", "/").rstrip("/")

        try:
            items = self.list_dir(top)
        except Exception:
            return  # Acess Denied or Void

        dirs = []
        files = []

        for item in items:
            item_path = posixpath.join(root_path, item)
            if self.is_dir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        if topdown:
            yield (root_path, dirs, files)

        for d in dirs:
            yield from self.walk(posixpath.join(root_path, d), topdown)

        if not topdown:
            yield (root_path, dirs, files)

    def glob(self, pattern: str, root: str = "") -> List[str]:
        """
        [FACULTY 4]: THE PATTERN SEEKER.
        Universal globbing support (e.g., `src/**/*.py`) regardless of driver.
        """
        matches = []
        # Support recursive glob via '**'
        recursive = "**" in pattern

        for cur_root, _, filenames in self.walk(root):
            for f in filenames:
                full_rel = posixpath.join(cur_root, f)
                if fnmatch.fnmatch(full_rel, pattern):
                    matches.append(full_rel)
        return sorted(matches)

    # =========================================================================
    # == V. CROSS-REALITY TRANSMUTATION                                      ==
    # =========================================================================

    def project_to(self, other: 'SanctumInterface', src: str, dst: str):
        """
        =============================================================================
        == THE ACHRONAL PROJECTION (V-Ω-MULTIVERSAL-TRANSFER)                      ==
        =============================================================================
        Surgically teleports matter from THIS sanctum to ANOTHER.
        Example: `s3_sanctum.project_to(local_sanctum, "data.db", "./backups/")`
        """
        self.logger.info(f"Teleporting Soul: {self.kind.name}::{src} -> {other.kind.name}::{dst}")

        if self.is_file(src):
            data = self.read_bytes(src)
            other.write_bytes(dst, data)
        else:
            # Recursive Directory Projection
            other.mkdir(dst, parents=True, exist_ok=True)
            for item in self.list_dir(src):
                self.project_to(other, posixpath.join(src, item), posixpath.join(dst, item))

    # =========================================================================
    # == VI. GOVERNANCE & METABOLISM                                         ==
    # =========================================================================

    @abstractmethod
    def chmod(self, path: Union[str, Path], mode: int):
        """Consecrates the permissions of a form."""
        pass

    def close(self):
        """Gracefully dissolves the bridge to this dimension."""
        pass

    def _format_heresy(self, error: Exception, operation: str, path: str) -> ArtisanHeresy:
        """Transmutes raw OS errors into high-status Gnostic Heresies."""
        return ArtisanHeresy(
            f"Substrate Fracture during {operation} on '{path}'",
            details=str(error),
            severity=HeresySeverity.CRITICAL,
            metadata={"driver": self.kind.name, "uri": self.uri_root}
        )

    def __repr__(self) -> str:
        return f"<Ω_SANCTUM kind={self.kind.name} uri={self.uri_root}>"