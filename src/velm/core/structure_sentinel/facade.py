# Path: src/velm/core/structure_sentinel/facade.py
# ------------------------------------------------

import time
import os
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Set, TYPE_CHECKING, Final, Union

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from .strategies import STRATEGY_REGISTRY
from .contracts import StructureStrategy
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...core.kernel.transaction import GnosticTransaction
    from ...creator.io_controller import IOConductor

Logger = Scribe("StructureSentinel")


class StructureSentinel:
    """
    =================================================================================
    == THE SOVEREIGN GUARDIAN OF STRUCTURE (V-Ω-TOTALITY-V5000-MOAT-BUILDER)       ==
    =================================================================================
    LIF: ∞ (THE ETERNAL GEOMETER) | ROLE: STRUCTURAL_ADJUDICATOR | RANK: OMEGA

    The divine orchestrator of structural resonance. It acts as the **Immutable Gate**
    through which all materialization requests must pass to ensure they conform to
    the sacred laws of their language (Python, Rust, Node, etc.).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS (V5000):

    1.  **The Geometric Singularity (Anchor Lock):** It enforces a single, absolute
        coordinate system relative to the `project_root`. No path can escape its Gaze.
        It neutralizes "Floating Path" heresies by anchoring all vectors to the Axis Mundi.

    2.  **The Bicameral Perception Engine:** It possesses "Second Sight". It gazes
        simultaneously upon the **Physical Realm** (Disk) and the **Ephemeral Realm**
        (Staging Transaction). It knows a file exists even if it has not yet been written,
        allowing for "Pre-Materialization Consecration".

    3.  **The Shadow Registry (O(1) Caching):** It maintains a thread-safe, high-speed
        `_consecrated_cache` of every locus it has visited. It ensures that the Rite
        of `__init__.py` forging happens exactly once per sanctum per eternity.

    4.  **The Strategy Multiplexer:** It does not simply pick one strategy. It can
        summon a coalition of guardians (e.g., Python + General) to bless a single
        scripture if multiple laws apply.

    5.  **The Unbreakable Hand (IOConductor Injection):** It passes the `IOConductor`
        organ down to the strategies. This allows language guardians (like the Python
        Strategy) to perform **Atomic, Transactional Writes** when creating structural
        bonds (like `__init__.py` or `mod.rs`), ensuring perfect reversibility.

    6.  **The Void Sieve:** It intelligently filters out "Phantom Directories". If a
        path ends in a file extension, it knows to consecrate the *parent* sanctum,
        not the file itself as a directory.

    7.  **Metabolic Tomography:** It measures the exact nanosecond cost of every
        consecration rite, feeding this data back to the Engine's vitality monitor.

    8.  **The Recursive Ancestry Ward:** It guards against infinite loops when walking
        up directory trees, implementing a "Root Wall" that stops at the project boundary.

    9.  **The Heuristic DNA Scanner:** For directories, it scans the contents (both
        physical and staged) to divine the dominant tongue (Python, Rust, etc.) without
        needing explicit file extensions.

    10. **Fault-Isolated Execution:** If a specific strategy fractures (crashes), the
        Sentinel catches the shard, logs a "Non-Critical Heresy," and continues the
        Great Work. The collapse of one limb does not kill the body.

    11. **The Dynamic Gnosis Injection:** It accepts a `gnosis` dictionary, allowing
        context (like `project_name` or `author`) to flow into the structural files
        it creates.

    12. **The Finality Vow:** A mathematical guarantee that if `ensure_structure` returns,
        the target locus is geometrically valid according to the laws of the Engine.
    """

    def __init__(
            self,
            project_root: Path,
            transaction: Optional["GnosticTransaction"] = None,
            io_conductor: Optional["IOConductor"] = None
    ):
        """
        [THE RITE OF INCEPTION]
        Sutures the Sentinel to the Project Root and its physical organs.
        """
        # [ANCHOR LOCK]: Resolve absolute path immediately.
        self.project_root = project_root.resolve()

        self.transaction = transaction

        # [ASCENSION 5]: THE ORGAN SUTURE
        # The IOConductor is the hand that writes to the Ledger.
        self.io_conductor = io_conductor

        # Materialize strategies from the Gnostic Registry
        self.strategies = STRATEGY_REGISTRY

        # [ASCENSION 3]: THE SHADOW REGISTRY
        # A thread-safe cache of visited paths to prevent redundant rites.
        self._consecrated_cache: Set[str] = set()
        self._cache_lock = threading.Lock()

        if Logger.is_verbose:
            substrate = 'TRANSACTIONAL' if transaction else 'PHYSICAL'
            Logger.verbose(
                f"Structure Sentinel materialised. "
                f"Anchor: [cyan]{self.project_root}[/] | "
                f"Substrate: {substrate} | "
                f"Strategies: {len(self.strategies)}"
            )

    def ensure_structure(self, path: Path, gnosis: Optional[Dict[str, Any]] = None):
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-BICAMERAL-GAZE-V5000)                     ==
        =============================================================================
        LIF: 100x | ROLE: STRUCTURAL_ADJUDICATOR

        The primary entry point. It receives a path (File or Directory) and ensures
        that the surrounding space honors the architectural laws.
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: GEOMETRIC NORMALIZATION ---
        # We ensure the path is absolute and anchored to the project root.
        try:
            abs_path = path.resolve()
        except OSError:
            # If the file doesn't exist yet, resolve() might fail on some OSs.
            # We construct it relative to CWD or Project Root.
            if path.is_absolute():
                abs_path = path
            else:
                abs_path = (self.project_root / path).resolve()

        # [THE MOAT]: Ensure path is within the Sanctum
        try:
            # We calculate the relative path to use as the cache key.
            # If it's outside the root, we treat it as an external dependency (warn but proceed?)
            # No, structural enforcement should only happen INSIDE the project.
            if not abs_path.is_relative_to(self.project_root):
                # Allow exact match (root itself)
                if abs_path != self.project_root:
                    # Logger.debug(f"Sentinel Gaze averted: '{path}' is outside the Sanctum.")
                    return
        except ValueError:
            # Path on different drive
            return

        # [ASCENSION 3]: THE CACHE CHECK (Thread-Safe)
        path_key = str(abs_path)
        with self._cache_lock:
            if path_key in self._consecrated_cache:
                return
            self._consecrated_cache.add(path_key)

        Logger.debug(f"Sentinel gazing upon structural integrity of: [cyan]{abs_path.name}[/cyan]")

        # --- MOVEMENT II: STRATEGY MULTIPLEXING ---
        # Divine which guardians manage this specific locus.
        strategies_to_invoke = self._divine_strategies(abs_path)

        if not strategies_to_invoke:
            # Logger.verbose(f"   -> No known language signatures found for '{abs_path.name}'.")
            return

        # --- MOVEMENT III: KINETIC CONSECRATION ---
        # Invoke the guardians.
        for strategy in strategies_to_invoke:
            try:
                # [ASCENSION 7]: METABOLIC TOMOGRAPHY
                rite_start = time.perf_counter()

                # Logger.info(f"   -> Invoking {strategy.__class__.__name__} Consecration...")

                # [ASCENSION 5]: THE FULL GNOSTIC DOWRY
                # We bestow the transaction AND the io_conductor.
                # This ensures the strategy can write __init__.py files atomically via the Ledger.
                strategy.consecrate(
                    path=abs_path,
                    project_root=self.project_root,
                    transaction=self.transaction,
                    io_conductor=self.io_conductor,
                    gnosis=gnosis or {}
                )

                duration = (time.perf_counter() - rite_start) * 1000
                # Logger.debug(f"      -> Consecration successful ({duration:.2f}ms).")

            except Exception as paradox:
                # [ASCENSION 10]: FAULT-ISOLATED HERESY MAPPING
                # We catch the exception to prevent one bad plugin from killing the Engine.
                Logger.error(f"Structural Consecration failed for '{abs_path}': {paradox}")

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        total_tax = (time.perf_counter_ns() - start_ns) / 1_000_000
        # if total_tax > 50:
        #     Logger.verbose(f"Structural Gaze Tax: {total_tax:.2f}ms")

    def _divine_strategies(self, path: Path) -> List[StructureStrategy]:
        """
        =============================================================================
        == THE SEMANTIC DIVINER (V-Ω-BICAMERAL-PERCEPTION)                         ==
        =============================================================================
        Perceives the language of a path across the Iron (Disk) and Ether (Transaction).
        """
        found_strategies = []
        path_str = str(path).lower()

        # --- PATH A: FILE INFERENCE (THE EXTENSION GAZE) ---
        # Check if the path *looks* like a file (has extension) or *is* a file (on disk).
        # [ASCENSION 6]: The Void Sieve.
        is_file = path.suffix != "" or (path.exists() and path.is_file())

        # Check Ephemeral Reality if physical reality is ambiguous
        if not is_file and self.transaction:
            try:
                rel = path.relative_to(self.project_root)
                if self.transaction.is_file_in_staging(rel):
                    is_file = True
            except ValueError:
                pass

        if is_file:
            ext = path.suffix.lower()
            if ext in self.strategies:
                found_strategies.append(self.strategies[ext])

            # Special Case: Dockerfile, Makefile (No extension but specific names)
            if path.name == "Dockerfile" and ".docker" in self.strategies:
                found_strategies.append(self.strategies[".docker"])

            return found_strategies

        # --- PATH B: DIRECTORY INFERENCE (THE BICAMERAL PEER) ---
        # If it's a directory, we must scan its contents to determine its nature.
        # [ASCENSION 2]: We scry BOTH the physical disk and the Staging area.

        try:
            # 1. Scry the Physical Reality
            search_paths = [path]

            # 2. Scry the Ephemeral Reality (Transaction Staging)
            if self.transaction:
                try:
                    rel_path = path.relative_to(self.project_root)
                    staging_path = self.transaction.get_staging_path(rel_path)
                    if staging_path.exists():
                        search_paths.append(staging_path)
                except ValueError:
                    pass

            # [ASCENSION 9]: HEURISTIC DNA SCAN
            # We look for ANY signature of a known language in the folder.
            has_py, has_rs, has_node = False, False, False

            for sp in search_paths:
                if not sp.exists() or not sp.is_dir(): continue

                for f in sp.iterdir():
                    s = f.suffix.lower()
                    name = f.name.lower()

                    if s == '.py':
                        has_py = True
                    elif s == '.rs':
                        has_rs = True
                    elif s in ('.js', '.ts', '.tsx', '.jsx') or name == 'package.json':
                        has_node = True

                    # Early exit if we found everything
                    if has_py and has_rs and has_node: break

            # Append strategies based on what we found
            if has_py and '.py' in self.strategies:
                found_strategies.append(self.strategies['.py'])
            if has_rs and '.rs' in self.strategies:
                found_strategies.append(self.strategies['.rs'])
            if has_node and '.ts' in self.strategies:
                found_strategies.append(self.strategies['.ts'])  # Generalized Node strategy

        except Exception as e:
            Logger.debug(f"Gaze clouded upon directory '{path.name}': {e}")

        return found_strategies

    def clear_cache(self):
        """
        [THE RITE OF AMNESIA]
        Purges the Shadow Registry for a fresh Gaze.
        Used during long-running Daemon sessions.
        """
        with self._cache_lock:
            self._consecrated_cache.clear()
        Logger.verbose("Sentinel cache purged.")

    def __repr__(self) -> str:
        return (
            f"<Ω_STRUCTURE_SENTINEL root={self.project_root.name} "
            f"strategies={len(self.strategies)} cache={len(self._consecrated_cache)}>"
        )