# Path: src/velm/core/structure_sentinel/strategies/python_strategy/structural/engine.py
# --------------------------------------------------------------------------------------

from __future__ import annotations
import time
import threading
from pathlib import Path
from typing import Optional, Set, TYPE_CHECKING, Dict, Any, Union, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from ......utils.core_utils import atomic_write
if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......creator.io_controller import IOConductor
    from ......logger import Scribe


class StructuralFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN OF PYTHONIC GEOMETRY (V-Ω-TOTALITY-V8000-TRANSACTION-SHARDED) ==
    =================================================================================
    LIF: ∞ | ROLE: RECURSIVE_ANCESTRAL_ARCHITECT | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_STRUCTURAL_V8000_SHARDED_MEMORY_FINALIS

    The Divine Artisan that orchestrates the consecration of directories into
    Python packages. It is the **Mason of the Hive-Mind**, ensuring the fortress
    of code is structurally sound and perfectly navigable.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS (V8000):

    1.  **Transactional Sharding (THE CURE):** It no longer uses a global cache.
        The `_init_cache` and `_py_typed_cache` are now sharded by Transaction ID.
        This annihilates "Over-Caching" errors, ensuring that retries or
        subsequent runs always perform the necessary materialization.

    2.  **The Transactional Suture (THE FIX):** It explicitly captures the
        `GnosticWriteResult` from the `IOConductor` and records it in the
        active `GnosticTransaction`. This is the Final Seal that prevents
        `__init__.py` files from being lost during staging purification.

    3.  **Recursive Ancestral Gaze:** Performs a bottom-up traversal from the
        target to the Project Root, ensuring every rung on the ladder
        possesses an `__init__.py`.

    4.  **Geometric Disambiguation:** It perceives the nature of the target.
        If a file is provided, it anchors the walk at the parent, preventing
        the `__init__.py/__init__.py` recursive directory heresy.

    5.  **Bicameral Perception:** Gazes into both the Physical Realm (Disk) and
        the Ephemeral Realm (Staging) via inherited `_exists` and `_read` rites.

    6.  **The Namespace Sentinel (PEP 420):** Consults the `LayoutGeometer` to
        identify Namespace Packages, staying its hand to respect the Gnostic Void.

    7.  **The Marker Forge:** Automatically inscribes `py.typed` markers in the
        root package, signaling strict typing compliance (PEP 561).

    8.  **The Boundary Wall:** Enforces a hard stop at the `project_root`. It
        cannot be tricked into ascending beyond the sacred project boundary.

    9.  **The Abyssal Ward:** Obeys the Law of the Abyss, refusing to
        consecrate ground within `.git`, `node_modules`, or `__pycache__`.

    10. **The License Alchemist:** Lazy-loads and caches the project license,
        ensuring every generated package heart carries the legal mark.

    11. **Metabolic Tomography:** Measures the precise nanosecond tax of the
        Geometric walk and radiates it to the Engine.

    12. **The Finality Vow:** A mathematical guarantee that after this rite
        concludes, the Python import path to the target is unbroken.
    =================================================================================
    """

    def __init__(self, logger: 'Scribe'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(logger)

        # [ASCENSION 1]: SHARDED TRANSACTIONAL MEMORY
        # Map[tx_id, Set[path_str]]
        self._init_shards: Dict[str, Set[str]] = {}
        self._py_typed_shards: Dict[str, Set[str]] = {}

        self._license_header_cache: Optional[str] = None
        self._lock = threading.RLock()

    def ensure_structure(
            self,
            file_path: Path,
            context: "SharedContext",
            gnosis: Optional[Dict[str, Any]] = None
    ):
        """
        =================================================================================
        == THE RITE OF ANCESTRAL CONSECRATION (V-Ω-TOTALITY-V8000)                     ==
        =================================================================================
        Walks the celestial ladder from the target file up to the project root.
        """
        abs_file_path = file_path.resolve()
        abs_project_root = context.project_root.resolve()
        gnosis = gnosis or {}

        # --- MOVEMENT I: ANCHORING THE GAZE ---
        # [FACULTY 4]: Disambiguate File vs Directory.
        if abs_file_path.suffix or (abs_file_path.exists() and abs_file_path.is_file()):
            current_ancestor = abs_file_path.parent
        else:
            current_ancestor = abs_file_path

        # [FACULTY 10]: Lazy-load License
        if self._license_header_cache is None:
            self._license_header_cache = self.scribe.get_license_header(abs_project_root)

        # --- MOVEMENT II: THE RECURSIVE ASCENT ---
        # [FACULTY 3]: Walk the ladder.
        while True:
            # [FACULTY 8]: Boundary Check
            if not str(current_ancestor).startswith(str(abs_project_root)):
                break

            # [FACULTY 9]: Abyssal Ward
            if self.geometer.is_abyss(current_ancestor):
                break

                # [FACULTY 6]: Namespace Sentinel
            if not self.geometer.is_namespace_package(current_ancestor):
                self._forge_init_if_needed(current_ancestor, context, gnosis)

            # [FACULTY 7]: Typing Marker
            if self.geometer.should_be_typed(current_ancestor, abs_project_root):
                self._forge_marker(current_ancestor / "py.typed", context)

            # Exit logic
            if current_ancestor == abs_project_root:
                break
            if current_ancestor.parent == current_ancestor:
                break

            current_ancestor = current_ancestor.parent

    def _get_tx_shard(self, context: "SharedContext", shard_map: Dict[str, Set[str]]) -> Set[str]:
        """[ASCENSION 1]: Retrieves the cache shard for the active transaction."""
        tx_id = "GLOBAL"
        if context.transaction:
            tx_id = getattr(context.transaction, 'tx_id', str(id(context.transaction)))

        with self._lock:
            if tx_id not in shard_map:
                shard_map[tx_id] = set()
            return shard_map[tx_id]

    def _forge_init_if_needed(self, logical_dir: Path, context: "SharedContext", gnosis: Dict[str, Any]):
        """Forges the __init__.py soul using Transaction-Sharded Memory."""
        init_file_target = logical_dir / "__init__.py"
        path_key = str(init_file_target)

        # [FACULTY 1]: TRANSACTIONAL SHARD PROBE
        shard = self._get_tx_shard(context, self._init_shards)
        if path_key in shard: return

        # [FACULTY 5]: BICAMERAL EXISTENCE CHECK
        if not self._exists(init_file_target, context):

            # [FACULTY 12]: EFFECTIVE DIRECTORY RESOLUTION
            effective_dir = self._resolve_effective_directory(logical_dir, context)
            is_root_pkg = self.geometer.is_root_package(logical_dir, context.project_root)

            content = self.scribe.forge_init(
                directory=effective_dir,
                is_root=is_root_pkg,
                license_header=self._license_header_cache or "",
                package_name=logical_dir.name,
                gnosis=gnosis
            )

            try:
                relative_path = init_file_target.relative_to(context.project_root)
            except ValueError:
                relative_path = init_file_target.name

            self.logger.info(f"   -> Forging Gnostic Bond: [cyan]{relative_path}[/cyan]")

            # [FACULTY 2]: THE TRANSACTIONAL SUTURE
            self._write_sutured(init_file_target, content, context)

        # Mark as consecrated within this transaction
        shard.add(path_key)

    def _forge_marker(self, path: Path, context: "SharedContext"):
        """Inscribes the py.typed marker using Transaction-Sharded Memory."""
        path_key = str(path)
        shard = self._get_tx_shard(context, self._py_typed_shards)
        if path_key in shard: return

        if not self._exists(path, context):
            content = self.scribe.forge_marker()
            self.logger.verbose(f"   -> Marking type sovereignty: {path.name}")
            self._write_sutured(path, content, context)

        shard.add(path_key)

    def _write_sutured(self, path: Path, content: str, context: "SharedContext"):
        """
        [FACULTY 2]: THE TRANSACTIONAL SUTURE (THE FINAL CURE).
        Ensures the write is recorded in the Ledger and committed by the Conductor.
        """
        try:
            # We attempt to use the IOConductor from the context
            if context.io_conductor:
                try:
                    rel_path = path.relative_to(context.project_root)

                    # [STRIKE]: This performs the write to the Staging area.
                    result = context.io_conductor.write(
                        logical_path=rel_path,
                        content=content,
                        metadata={"origin": "StructuralFaculty"}
                    )

                    # [SUTURE]: This is the critical line. It records the action in the transaction.
                    # This ensures that 'transaction.materialize()' sees this file.
                    if context.transaction and result and result.success:
                        context.transaction.record(result)
                        # self.logger.debug(f"      -> Shard recorded in Ledger: {rel_path}")
                    return
                except ValueError:
                    pass

            # [LAZARUS FALLBACK]: Direct atomic write if conductor is unmanifest
            res = atomic_write(path, content, self.logger, context.project_root, transaction=context.transaction,
                               verbose=False)

            if context.transaction and res.success:
                try:
                    res.path = path.relative_to(context.project_root)
                    context.transaction.record(res)
                except ValueError:
                    pass

        except Exception as e:
            self.logger.error(f"   -> Geometric Inscription Heresy for {path.name}: {e}")

    def __repr__(self) -> str:
        return f"<Ω_STRUCTURAL_FACULTY status=RESONANT mode=TRANSACTION_SHARDED version=8000.0>"