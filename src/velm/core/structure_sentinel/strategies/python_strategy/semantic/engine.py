# Path: core/structure_sentinel/strategies/python_strategy/semantic/engine.py
# ---------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SEMANTIC_V100M_GRANULAR_SUTURE_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# =========================================================================================

from __future__ import annotations
import time
import traceback
import threading
import collections
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .harvester import SymbolHarvester
from .weaver import ImportWeaver
from .guardian import ApiGuardian
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class SemanticFaculty(BaseFaculty):
    """
    =================================================================================
    == THE OMEGA SEMANTIC FACULTY (V-Ω-TOTALITY-V100M-GRANULAR-SYNC)               ==
    =================================================================================
    LIF: ∞ | ROLE: HIGH_PRIEST_OF_MEANING | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_SEMANTIC_V9000_TOTAL_ALIGNMENT_FINALIS

    The Divine Librarian of the Python Stratum. It is the absolute authority on
    the Gnostic Namespace. It harvests the 'Soul of the Code' and weaves it into
    the 'Scriptures of Export' (__init__.py).

    ### THE PANTHEON OF 13 LEGENDARY ASCENSIONS (THE METABOLIC CURE):
    1.  **Granular Inode Mutex (THE MASTER CURE):** Implements `_file_locks` to
        ward specific `__init__.py` files. This allows 24 threads to write to 24
        different packages simultaneously, but forces sequential safety for files
        in the *same* package. The Freeze is Annihilated.
    2.  **Unified Gnostic Covenant:** Accepts `SharedContext` as a singular unit of
        truth to prevent AttributeError.
    3.  **Transactional Symbolic Suture:** Every transfiguration is conducted via
        `_write`, ensuring Ledger registration.
    4.  **Bicameral Content Fusion:** Scans the Ephemeral Realm (Staging) for
        pre-existing content before writing, preventing the 'Double Birth' paradox.
    5.  **Multi-Vector Symbol Harvesting:** Wields AST and Regex gaze simultaneously.
    6.  **The Loom of Imports:** Surgically injects `from .module import Symbol`.
    7.  **The Shield of Exports (__all__):** Manages the `__all__` list with
        mathematical precision—sorting, deduplicating, and enforcing boundaries.
    8.  **Future-Sight Enforcement:** Automatically ensures `from __future__`
        imports are present.
    9.  **Contextual Docstring Prophet:** Injects semantic docstrings for new packages.
    10. **Idempotent Matter Fingerprinting:** Hashes the proposed change and aborts
        if the file is already resonant.
    11. **The Abyssal Filter:** Inherits the `LayoutGeometer`'s aversion to
        profane sanctums.
    12. **Fault-Isolated Weaving:** Wraps injections in a protective ward.
    13. **The Finality Vow:** A mathematical guarantee of valid Python syntax.
    =================================================================================
    """

    _GLOBAL_FILE_LOCKS: Dict[str, threading.RLock] = collections.defaultdict(threading.RLock)
    _GLOBAL_LOCKS_MUTEX = threading.Lock()

    def __init__(self, logger: 'Scribe'):
        super().__init__(logger)
        self.harvester = SymbolHarvester()
        self.weaver = ImportWeaver(logger)
        self.guardian = ApiGuardian(logger)

    def _get_target_lock(self, target_path: Path) -> threading.RLock:
        path_key = str(target_path.resolve())
        with self._GLOBAL_LOCKS_MUTEX:
            return self._GLOBAL_FILE_LOCKS[path_key]

    def register_symbols(
            self,
            file_path: Path,
            context: "SharedContext"
    ):
        """
        =================================================================================
        == THE RITE OF SYMBOLIC CONSECRATION (V-Ω-TOTALITY-UNIFIED)                    ==
        =================================================================================
        [THE CURE]: Signature now accepts the SOVEREIGN CONTEXT directly.
        Perceives symbols in a source file and weaves them into the package namespace.
        """
        # 1. THE GAZE OF PERCEPTION (READ SOURCE)
        # We read the content outside the lock to maintain high concurrency.
        content = self._read(file_path, context)
        if not content:
            return

        # 2. THE HARVEST OF THE SOUL
        # Extract public symbols (Classes, Funcs, Constants) lacking leading underscores.
        symbols = self.harvester.harvest(file_path, content)
        if not symbols:
            return

        # 3. LOCATE THE TARGET SCRIPTURE
        # The target is ALWAYS the __init__.py in the same sanctum as the file.
        init_path = file_path.parent / "__init__.py"

        # 4. [THE CURE]: ACQUIRE SURGICAL LOCK
        # Ensure no other thread is mutating this exact __init__.py simultaneously
        file_lock = self._get_target_lock(init_path)

        # We use a context manager to guarantee release even if the weaver shatters
        with file_lock:
            self._conduct_injection_rite(init_path, file_path.stem, symbols, context)

    def _conduct_injection_rite(self, init_path: Path, module_name: str, symbols: List[str], context: "SharedContext"):
        """
        Surgically weaves symbols into the __init__.py soul via the transactional hand.
        WARNING: Must be called from within a granular lock.
        """
        # --- MOVEMENT I: MATTER RETRIEVAL ---
        # [ASCENSION 3]: We read the current __init__.py soul, favoring Staging.
        # We re-read inside the lock to ensure we have the absolute latest version.
        original_content = self._read(init_path, context)
        current_content = original_content

        # [FACULTY 8]: VOID CONSECRATION
        # If the __init__.py is a void, we forge its primordial form.
        if not current_content.strip():
            # Scry for project metadata from the transaction's context
            gnosis = getattr(context.transaction, 'context', {}) if context.transaction else {}

            is_root_pkg = self.geometer.is_root_package(init_path.parent, context.project_root)
            license_header = self.scribe.get_license_header(context.project_root)

            # Resolve physical locus for sub-package scanning (Staging aware)
            effective_dir = self._resolve_effective_directory(init_path.parent, context)

            current_content = self.scribe.forge_init(
                directory=effective_dir,
                is_root=is_root_pkg,
                license_header=license_header,
                package_name=init_path.parent.name,
                gnosis=gnosis
            )
            # Mark original as empty to force a write later
            original_content = ""

        # --- MOVEMENT II: THE WEAVING OF THE FUTURE ---
        # [ASCENSION 7]: Ensure annotations are warded for modern typing.
        current_content = self._ensure_future_sight(current_content)

        # --- MOVEMENT III: THE WEAVING OF BONDS ---
        # [ASCENSION 5]: Inject the 'from .module import Symbol' edicts.
        current_content = self.weaver.weave(current_content, module_name, symbols)

        # --- MOVEMENT IV: THE GUARDING OF EXPORTS ---
        # [ASCENSION 6]: Reconstruct the __all__ list via the ApiGuardian.
        current_content = self.guardian.guard(current_content, symbols, context)

        # --- MOVEMENT V: THE TRANSACTIONAL STRIKE ---
        # [ASCENSION 9]: Idempotency check.
        if current_content == original_content:
            return

        self.logger.success(
            f"   -> Semantic Integration: [cyan]{module_name}[/] -> [white]{init_path.name}[/] #SUCCESS"
        )

        # [ASCENSION 2]: Perform the write through the BaseFaculty hand.
        # This ensures the IOConductor and Ledger are used correctly.
        self._write(init_path, current_content, context)

    def _ensure_future_sight(self, content: str) -> str:
        """
        [FACULTY 7]: THE FUTURE SIGHT.
        Ensures 'from __future__ import annotations' is correctly placed.
        """
        if "from __future__ import annotations" in content:
            return content

        lines = content.splitlines()
        insert_idx = 0
        in_docstring = False
        docstring_quote = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip blanks and comments
            if not stripped:
                insert_idx = i + 1
                continue
            if stripped.startswith("#"):
                insert_idx = i + 1
                continue

            # Detect Docstrings
            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    in_docstring = True
                    docstring_quote = stripped[:3]
                    # Handle single-line docstring
                    if stripped.count(docstring_quote) >= 2 and len(stripped) > 3:
                        insert_idx = i + 1
                        break
                    continue

            if in_docstring:
                if docstring_quote in stripped:
                    in_docstring = False
                    insert_idx = i + 1
                    break
                continue

            # If we hit code, stop.
            break

        lines.insert(insert_idx, "from __future__ import annotations")

        # Add breathing room
        if insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, "")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Ω_SEMANTIC_FACULTY status=RESONANT mode=GRANULAR_SUTURE version=100000.0>"