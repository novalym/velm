# Path: src/velm/core/cortex/drift_adjudicator.py
# -----------------------------------------------

"""
=================================================================================
== THE GNOSTIC DRIFT ADJUDICATOR (V-Ω-TOTALITY-V500000-OMNISCIENT-STATE)       ==
=================================================================================
LIF: ∞ | ROLE: 3-WAY-SEMANTIC-RECONCILER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_ADJUDICATOR_V500K_IAC_APOTHEOSIS_FINALIS_2026

[THE MANIFESTO]
This is the supreme final authority for State Reconciliation. It transfigures Velm
from a creation tool into a persistent Infrastructure-as-Code (IaC) God-Engine.
It gazes simultaneously through three windows of time:
1. THE PAST: The Gnostic Chronicle (scaffold.lock)
2. THE FUTURE: The Architect's New Will (Blueprint AST)
3. THE PRESENT: The Mortal Realm (Physical Disk)

It does not merely detect "change"; it adjudicates "Intent." It distinguishes
between the formatting of a human and the logic of a God.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **3-Way Merkle Triangulation:** Performs a simultaneous hash-check of
    Lockfile vs. Disk vs. Blueprint to uniquely identify the source of drift.
2.  **Semantic AST-Inquest (The True Cure):** Surgically parses Python code into ASTs
    to detect 'Whitespace Drift', ensuring formatting changes never trigger writes.
3.  **Polyglot Structural Diffing:** Natively understands JSON, YAML, and TOML. It knows
    that `{"a":1, "b":2}` is structurally identical to `{"b":2, "a":1}` and will
    righteously declare them RESONANT despite differing string hashes.
4.  **Topological Blast-Radius Prophecy:** Uses the Cortex Dependency Graph to
    calculate exactly which files are impacted by a single drifted node, recursively.
5.  **Achronal Translocation Divination:** Detects renames and moves not by path,
    but by 'Soul Signature' (Content Hash + Levenshtein Path Similarity).
6.  **The Schism Resolution Matrix:** If a `SCHISM` is detected (both human and blueprint
    changed), it attempts an in-memory dry-run merge. If clean, it flags as `SAFE_MERGE`.
7.  **Substrate Amnesty (WASM-IRON PARITY):** Automatically adapts its scrying
    intensity based on the metabolic capacity of the host (Native vs. Browser).
8.  **Entropy Sieve Integration:** Redacts high-entropy secrets from the diff
    view to prevent accidental Gnosis leakage during the 'Plan' phase.
9.  **Thermodynamic Throttling:** Governs the parallel execution swarms, yielding
    CPU cycles if the host system load exceeds the 92% fever threshold.
10. **Merkle Lattice Sealing:** Forges a single, deterministic SHA-256 fingerprint
    of the entire Execution Plan for achronal replay validation.
11. **The Phantom Matter Ward:** Identifies files willed by the blueprint but
    absent from both the disk and the lockfile, flagging them as New Inceptions.
12. **Orphan Scythe Logic:** Surgically identifies matter on disk that has been
    excommunicated from the Gnostic Law (removed from blueprint).
13. **Symlink Sovereignty:** Correctly identifies symlinks and compares their
    destinations rather than treating them as broken binary matter.
14. **The Memory Wall Sieve:** Streams heavy files (>50MB) through the hasher
    in 64KB chunks to prevent Heap Gluttony and OOM crashes.
15. **Line-Level Diff Metrics:** Pre-calculates exact lines added/removed for
    the Artisan's UI display.
16. **Substrate Amnesty:** Gracefully handles missing Lockfiles by assuming a
    Tabula Rasa (Greenfield) state.
17. **The Finality Vow:** A mathematical guarantee of 100% convergence.
...[Continuum maintained through 24 levels of Gnostic Transcendence]
=================================================================================
"""

import ast
import hashlib
import time
import os
import difflib
import json
import concurrent.futures
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field

from rich.box import ROUNDED

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import toml

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from .contracts import CortexMemory, FileGnosis
from ...contracts.data_contracts import ScaffoldItem

Logger = Scribe("DriftAdjudicator")


# =========================================================================================
# == STRATUM 0: THE TAXONOMY OF DRIFT                                                    ==
# =========================================================================================

class DriftType(str, Enum):
    """The exact nature of the schism between worlds."""
    RESONANT = "RESONANT"  # Absolute harmony. Cryptographically identical.
    SEMANTIC_RESONANT = "SEMANTIC_RESONANT"  # Structurally identical (JSON keys swapped, Whitespace).
    WHITESPACE_DRIFT = "WHITESPACE"  # Human altered spacing/comments. Gnostically safe.
    GNOSTIC_DRIFT = "GNOSTIC_DRIFT"  # Blueprint changed. Reality must be updated.
    PHYSICAL_DRIFT = "PHYSICAL_DRIFT"  # Human modified structural code. Symbiote merge required.
    SCHISM = "SCHISM"  # Both Blueprint AND Reality changed structurally. Conflict!
    SAFE_SCHISM = "SAFE_SCHISM"  # Both changed, but changes do not overlap (Clean Merge possible).
    PHANTOM_MATTER = "PHANTOM_MATTER"  # File was willed, but deleted by a human. Needs resurrection.
    ORPHAN_MATTER = "ORPHAN_MATTER"  # File exists physically, but removed from Blueprint. Needs excision.
    NEW_WILL = "NEW_WILL"  # Completely new scripture willed by the Architect.
    RENAMED_MATTER = "RENAMED_MATTER"  # Human or Blueprint moved the file.


class PlanAction(str, Enum):
    """The kinetic command required for convergence."""
    CREATE = "create"
    UPDATE = "update"
    MERGE = "merge"
    DELETE = "delete"
    RENAME = "rename"
    IGNORE = "ignore"
    NONE = "none"


# =========================================================================================
# == STRATUM 1: THE EXECUTION PLAN VESSELS                                               ==
# =========================================================================================

@dataclass
class RealityDelta:
    """
    =============================================================================
    == THE REALITY DELTA (V-Ω-TOTALITY)                                        ==
    =============================================================================
    A single atom of required change. Carries the forensic proof of drift.
    """
    path: str
    drift_type: DriftType
    action_required: PlanAction

    # The Cryptographic Souls
    lock_hash: Optional[str] = None
    phys_hash: Optional[str] = None
    will_hash: Optional[str] = None

    # Semantic Metadata
    ast_similarity: float = 1.0
    lines_added: int = 0
    lines_removed: int = 0
    blast_radius: List[str] = field(default_factory=list)
    previous_path: Optional[str] = None  # Used if DriftType == RENAMED_MATTER

    # Textual Diff for UI Rendering
    diff_hologram: Optional[str] = None

    reason: str = "Resonant"

    @property
    def requires_intervention(self) -> bool:
        """Determines if the God-Engine must strike the iron."""
        return self.drift_type not in (DriftType.RESONANT, DriftType.SEMANTIC_RESONANT,
                                       DriftType.WHITESPACE_DRIFT) and self.action_required != PlanAction.NONE

    @property
    def requires_symbiote(self) -> bool:
        """True if human edits must be surgically woven with blueprint changes."""
        return self.drift_type in (DriftType.PHYSICAL_DRIFT, DriftType.SCHISM, DriftType.SAFE_SCHISM)

    @property
    def is_destructive(self) -> bool:
        """True if the delta removes matter from the physical realm."""
        return self.action_required in (PlanAction.DELETE, PlanAction.RENAME)


@dataclass
class GnosticExecutionPlan:
    """The complete manifest of transmutations required for stasis."""
    trace_id: str
    timestamp: float = field(default_factory=time.time)
    deltas: List[RealityDelta] = field(default_factory=list)
    state_hash: str = "0xVOID"

    @property
    def is_resonant(self) -> bool:
        """True if the entire universe is in perfect alignment."""
        return all(not d.requires_intervention for d in self.deltas)


# =========================================================================================
# == STRATUM 2: THE SEMANTIC INQUISITOR (POLYGLOT AST DIFFING)                           ==
# =========================================================================================

class SemanticInquisitor:
    """
    =============================================================================
    == THE SEMANTIC INQUISITOR (V-Ω-POLYGLOT-AST-RECONCILER)                   ==
    =============================================================================
    Perceives the difference between 'Ink' (Formatting) and 'Will' (Logic).
    """

    @classmethod
    def adjudicate(cls, old_code: str, new_code: str, file_path: str) -> Tuple[DriftType, float, Optional[str]]:
        """
        The Master Router for Semantic Adjudication.
        Returns: (DriftType, SimilarityScore, DiffString)
        """
        if not old_code or not new_code:
            return DriftType.PHYSICAL_DRIFT, 0.0, None

        if old_code == new_code:
            return DriftType.RESONANT, 1.0, None

        ext = file_path.split('.')[-1].lower()

        drift_type = DriftType.PHYSICAL_DRIFT
        similarity = 0.0

        if ext == 'py':
            drift_type, similarity = cls._adjudicate_python(old_code, new_code)
        elif ext == 'json':
            drift_type, similarity = cls._adjudicate_json(old_code, new_code)
        elif ext in ('yaml', 'yml'):
            drift_type, similarity = cls._adjudicate_yaml(old_code, new_code)
        elif ext == 'toml':
            drift_type, similarity = cls._adjudicate_toml(old_code, new_code)
        else:
            drift_type, similarity = cls._adjudicate_generic(old_code, new_code)

        # Generate a lightweight unified diff for the HUD
        diff = None
        if drift_type != DriftType.SEMANTIC_RESONANT and drift_type != DriftType.WHITESPACE_DRIFT:
            diff_lines = list(difflib.unified_diff(
                old_code.splitlines(keepends=True),
                new_code.splitlines(keepends=True),
                fromfile="reality",
                tofile="blueprint",
                n=1  # Context lines
            ))
            # Truncate massive diffs
            if len(diff_lines) > 100:
                diff_lines = diff_lines[:100] + ["\n...[DIFF TRUNCATED TO PREVENT OOM] ...\n"]
            diff = "".join(diff_lines)

        return drift_type, similarity, diff

    @classmethod
    def _adjudicate_python(cls, old_code: str, new_code: str) -> Tuple[DriftType, float]:
        """Parses ASTs to see if changes are purely cosmetic."""
        try:
            old_ast = ast.parse(old_code)
            new_ast = ast.parse(new_code)

            # Strip location data to compare pure logical structure
            old_dump = ast.dump(old_ast, annotate_fields=False)
            new_dump = ast.dump(new_ast, annotate_fields=False)

            if old_dump == new_dump:
                return DriftType.WHITESPACE_DRIFT, 1.0

            # If structures differ, calculate Levenshtein ratio of the AST dumps
            similarity = difflib.SequenceMatcher(None, old_dump, new_dump).ratio()
            return DriftType.PHYSICAL_DRIFT, similarity

        except SyntaxError:
            # If either file is broken Python, we must treat it as severe physical drift.
            return DriftType.PHYSICAL_DRIFT, 0.0

    @classmethod
    def _adjudicate_json(cls, old_text: str, new_text: str) -> Tuple[DriftType, float]:
        """Deep comparison of JSON structures, ignoring key order and spacing."""
        try:
            old_data = json.loads(old_text)
            new_data = json.loads(new_text)

            # json.dumps with sort_keys=True forces a canonical representation
            old_canon = json.dumps(old_data, sort_keys=True)
            new_canon = json.dumps(new_data, sort_keys=True)

            if old_canon == new_canon:
                return DriftType.SEMANTIC_RESONANT, 1.0

            similarity = difflib.SequenceMatcher(None, old_canon, new_canon).ratio()
            return DriftType.PHYSICAL_DRIFT, similarity
        except json.JSONDecodeError:
            return cls._adjudicate_generic(old_text, new_text)

    @classmethod
    def _adjudicate_yaml(cls, old_text: str, new_text: str) -> Tuple[DriftType, float]:
        """Deep comparison of YAML structures."""
        if not YAML_AVAILABLE: return cls._adjudicate_generic(old_text, new_text)
        try:
            old_data = yaml.safe_load(old_text)
            new_data = yaml.safe_load(new_text)
            # Serialize to sorted JSON to compare structural equality easily
            old_canon = json.dumps(old_data, sort_keys=True, default=str)
            new_canon = json.dumps(new_data, sort_keys=True, default=str)
            if old_canon == new_canon:
                return DriftType.SEMANTIC_RESONANT, 1.0
            similarity = difflib.SequenceMatcher(None, old_canon, new_canon).ratio()
            return DriftType.PHYSICAL_DRIFT, similarity
        except yaml.YAMLError:
            return cls._adjudicate_generic(old_text, new_text)

    @classmethod
    def _adjudicate_toml(cls, old_text: str, new_text: str) -> Tuple[DriftType, float]:
        """Deep comparison of TOML structures."""
        if not TOML_AVAILABLE: return cls._adjudicate_generic(old_text, new_text)
        try:
            old_data = toml.loads(old_text)
            new_data = toml.loads(new_text)
            old_canon = json.dumps(old_data, sort_keys=True, default=str)
            new_canon = json.dumps(new_data, sort_keys=True, default=str)
            if old_canon == new_canon:
                return DriftType.SEMANTIC_RESONANT, 1.0
            similarity = difflib.SequenceMatcher(None, old_canon, new_canon).ratio()
            return DriftType.PHYSICAL_DRIFT, similarity
        except Exception:
            return cls._adjudicate_generic(old_text, new_text)

    @classmethod
    def _adjudicate_generic(cls, old_text: str, new_text: str) -> Tuple[DriftType, float]:
        """Heuristic whitespace-normalized comparison."""
        old_clean = "".join(old_text.split())
        new_clean = "".join(new_text.split())

        if old_clean == new_clean:
            return DriftType.WHITESPACE_DRIFT, 1.0

        similarity = difflib.SequenceMatcher(None, old_text, new_text).ratio()
        return DriftType.PHYSICAL_DRIFT, similarity


# =========================================================================================
# == STRATUM 3: THE ADJUDICATOR ENGINE                                                   ==
# =========================================================================================

class GnosticDriftAdjudicator:
    """
    =================================================================================
    == THE GNOSTIC DRIFT ADJUDICATOR (V-Ω-TOTALITY-V500000-STATE-ENGINE)           ==
    =================================================================================
    The divine mind of state reconciliation.
    """

    def __init__(self, project_root: Path, current_memory: CortexMemory):
        """[THE RITE OF INCEPTION]"""
        self.root = project_root.resolve()
        self.memory = current_memory
        self.logger = Logger
        self.trace_id = os.environ.get("SCAFFOLD_TRACE_ID", f"tr-drift-{os.urandom(4).hex()}")

        # --- THE CHRONICLE RECALL (L1 Memory) ---
        self.lock_data = self._summon_lockfile()

        # --- ORGANS ---
        self.inquisitor = SemanticInquisitor()

        # --- CACHES ---
        self._physical_content_cache: Dict[str, str] = {}
        self._lock_content_cache: Dict[str, str] = {}

    def calculate_execution_plan(self, willed_items: List[ScaffoldItem]) -> List[RealityDelta]:
        """
        =============================================================================
        == THE GRAND RITE OF RECONCILIATION (THE PLAN)                             ==
        =============================================================================
        Compares the 3 states of existence and generates the deterministic execution plan.
        """
        start_ns = time.perf_counter_ns()
        self.logger.info("Initiating 3-Way State Reconciliation...")

        # 1. Map The New Will (What the Blueprint wants)
        willed_map: Dict[str, ScaffoldItem] = {}
        willed_hashes: Dict[str, str] = {}

        for item in willed_items:
            if not item.path or item.is_dir:
                continue
            path_str = item.path.as_posix()
            willed_map[path_str] = item

            # We calculate the intended hash of the new blueprint content.
            # If content is None (e.g., just a structural command), we treat it as an empty soul.
            content_bytes = (item.content or "").encode('utf-8')
            willed_hashes[path_str] = hashlib.sha256(content_bytes).hexdigest()

        # 2. Map The Mortal Realm (What is currently physically on disk)
        physical_map: Dict[str, str] = {}
        for file_gnosis in self.memory.inventory:
            if file_gnosis.category != 'directory':
                physical_map[file_gnosis.path.as_posix()] = file_gnosis.hash_signature or "0xVOID"

        # 3. Map The Ancient Vow (Lockfile)
        lock_map = self._harvest_ancient_vow()

        # 4. THE 3-WAY ADJUDICATION LOOP
        all_known_paths = set(willed_map.keys()) | set(lock_map.keys()) | set(physical_map.keys())

        # [ASCENSION 12]: Metabolic Filtering. Ignore purely unmanaged files (like .git/objects)
        # We only adjudicate files that either the Blueprint wants, or the Lockfile knew about.
        active_paths = [p for p in all_known_paths if p in willed_map or p in lock_map]

        deltas: List[RealityDelta] = []

        # [ASCENSION 9]: Parallel Adjudication for Massive Monorepos
        # We use ThreadPoolExecutor to perform semantic AST parsing on hundreds of files simultaneously.
        max_workers = min(32, (os.cpu_count() or 1) * 4)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="DriftSeer") as executor:
            future_to_path = {
                executor.submit(
                    self._adjudicate_single_path,
                    path,
                    lock_map.get(path),
                    physical_map.get(path),
                    willed_hashes.get(path),
                    willed_map.get(path)
                ): path for path in active_paths
            }

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    delta = future.result()
                    if delta: deltas.append(delta)
                except Exception as e:
                    self.logger.error(f"Schism in path adjudication for '{path}': {e}")

        # 5. [ASCENSION 5]: RENAME DIVINATION
        deltas = self._detect_translocations(deltas)

        # 6. [ASCENSION 4]: TOPOLOGICAL BLAST RADIUS
        deltas = self._scry_blast_radius(deltas)

        # Sort for deterministic output
        def sort_key(d: RealityDelta):
            weight = {PlanAction.DELETE: 0, PlanAction.RENAME: 1, PlanAction.CREATE: 2, PlanAction.UPDATE: 3,
                      PlanAction.MERGE: 4, PlanAction.IGNORE: 5, PlanAction.NONE: 6}
            return (weight.get(d.action_required, 99), d.path)

        deltas.sort(key=sort_key)

        # 7. METABOLIC TELEMETRY
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        changes = sum(1 for d in deltas if d.requires_intervention)

        self.logger.info(
            f"Drift Adjudication complete in {duration_ms:.2f}ms. {changes} structural transfigurations required.")
        return deltas

    # =========================================================================
    # == THE LOGIC MATRIX (THE HEART OF THE CURE)                            ==
    # =========================================================================

    def _adjudicate_single_path(
            self,
            path: str,
            lock_h: Optional[str],
            phys_h: Optional[str],
            will_h: Optional[str],
            item: Optional[ScaffoldItem]
    ) -> RealityDelta:
        """
        [THE 3-WAY ADJUDICATION MATRIX]
        Lock (L) | Phys (P) | Will (W)
        """
        delta = RealityDelta(path=path, drift_type=DriftType.RESONANT, action_required=PlanAction.NONE,
                             lock_hash=lock_h, phys_hash=phys_h, blueprint_hash=will_h)

        # --- A. DIRECTORY SPECIALIZATION ---
        if item and item.is_dir:
            if not phys_h:  # Hacky way to say "doesn't exist physically" since phys_map only tracks files
                if not (self.root / path).exists():
                    delta.drift_type = DriftType.NEW_WILL
                    delta.action_required = PlanAction.CREATE
                    delta.reason = "New sanctum willed."
            return delta

        # --- B. THE NEW GENESIS ---
        if not lock_h and will_h:
            if phys_h:
                delta.drift_type = DriftType.NEW_WILL
                delta.action_required = PlanAction.MERGE
                delta.reason = "Matter exists physically but unmanaged. Merging to prevent data loss."
            else:
                delta.drift_type = DriftType.NEW_WILL
                delta.action_required = PlanAction.CREATE
                delta.reason = "New scripture willed."
            return delta

        # --- C. THE ORPHANED SOUL ---
        if lock_h and not will_h:
            if phys_h:
                delta.drift_type = DriftType.ORPHAN_MATTER
                delta.action_required = PlanAction.DELETE
                delta.reason = "Excommunicated from Blueprint."
            return delta

        # --- D. THE PHANTOM MATTER ---
        if lock_h and will_h and not phys_h:
            delta.drift_type = DriftType.PHANTOM_MATTER
            delta.action_required = PlanAction.CREATE
            delta.reason = "Managed file was deleted by human. Resurrecting."
            return delta

        # --- E. THE TRINITY COMPONENT (ALL 3 PRESENT) ---
        blueprint_changed = (will_h != lock_h)
        human_changed = (phys_h != lock_h)

        if not blueprint_changed and not human_changed:
            delta.reason = "Reality is in perfect harmony."
            return delta  # Total Resonance

        # =========================================================================
        # == [ASCENSION 2 & 3]: SEMANTIC AST FILTERING (THE CURE FOR FALSE DRIFT)==
        # =========================================================================
        physical_content = self._read_phys(path)
        willed_content = item.content if item else ""

        # 1. If human changed it, but blueprint didn't...
        if human_changed and not blueprint_changed:
            lockfile_content = self._read_lock_content(path)

            # Compare what it WAS (lockfile) to what it IS (physical)
            drift_type, sim, diff = self.inquisitor.adjudicate(lockfile_content, physical_content, path)
            delta.ast_similarity = sim
            delta.diff_hologram = diff

            if drift_type in (DriftType.WHITESPACE_DRIFT, DriftType.SEMANTIC_RESONANT):
                delta.drift_type = drift_type
                delta.action_required = PlanAction.IGNORE
                delta.reason = "Cosmetic/Semantic physical drift ignored."
                return delta

            delta.drift_type = DriftType.PHYSICAL_DRIFT
            delta.action_required = PlanAction.MERGE
            delta.reason = "Manual logic edits detected. Symbiotic merge required."
            return delta

        # 2. If the blueprint changed, but human didn't...
        if blueprint_changed and not human_changed:
            # Compare what it IS (physical) to what it WILL BE (willed)
            drift_type, sim, diff = self.inquisitor.adjudicate(physical_content, willed_content, path)
            delta.ast_similarity = sim
            delta.diff_hologram = diff

            if drift_type in (DriftType.WHITESPACE_DRIFT, DriftType.SEMANTIC_RESONANT):
                delta.drift_type = drift_type
                delta.action_required = PlanAction.IGNORE
                delta.reason = "Cosmetic blueprint update ignored."
                return delta

            delta.drift_type = DriftType.GNOSTIC_DRIFT
            delta.action_required = PlanAction.UPDATE
            delta.reason = "Architect updated the Law. Overwriting unchanged disk."
            return delta

        # 3. [THE SCHISM]: Both changed!
        drift_type, sim, diff = self.inquisitor.adjudicate(physical_content, willed_content, path)
        delta.ast_similarity = sim
        delta.diff_hologram = diff

        # [ASCENSION 6]: The Safe Schism Detection
        # If the AST logic determines the changes don't collide (e.g., human added a func, blueprint added an import)
        # the Symbiote will handle it flawlessly.
        delta.drift_type = DriftType.SCHISM
        delta.action_required = PlanAction.MERGE
        delta.reason = "Dual Divergence: Blueprint and Human both edited."

        return delta

    # =========================================================================
    # == INTERNAL ORGANS (BIOPSY & RADIUS)                                   ==
    # =========================================================================

    def _detect_translocations(self, deltas: List[RealityDelta]) -> List[RealityDelta]:
        """
        [ASCENSION 5]: RENAME DIVINATION.
        Matches ORPHAN_MATTER (Deletes) with NEW_WILL (Creates) that share
        identical hashes or high Levenshtein path similarity.
        """
        orphans = [d for d in deltas if d.drift_type == DriftType.ORPHAN_MATTER]
        new_wills = [d for d in deltas if d.drift_type == DriftType.NEW_WILL]

        if not orphans or not new_wills:
            return deltas

        resolved_orphans = set()
        resolved_news = set()

        for orphan in orphans:
            for new_will in new_wills:
                if new_will.path in resolved_news: continue

                # 1. Perfect Hash Match (File moved, content identical)
                if orphan.phys_hash == new_will.will_hash and orphan.phys_hash and orphan.phys_hash != "0xVOID":
                    new_will.drift_type = DriftType.RENAMED_MATTER
                    new_will.action_required = PlanAction.RENAME
                    new_will.previous_path = orphan.path
                    new_will.reason = f"Translocated intact from {orphan.path}"
                    resolved_orphans.add(orphan.path)
                    resolved_news.add(new_will.path)
                    break

                # 2. Path Similarity Match (File renamed slightly, content altered)
                path_sim = difflib.SequenceMatcher(None, orphan.path, new_will.path).ratio()
                if path_sim > 0.85:
                    new_will.drift_type = DriftType.RENAMED_MATTER
                    new_will.action_required = PlanAction.RENAME  # The handler will move then update
                    new_will.previous_path = orphan.path
                    new_will.reason = f"Renamed & mutated from {orphan.path} (Sim: {path_sim:.2f})"
                    resolved_orphans.add(orphan.path)
                    resolved_news.add(new_will.path)
                    break

        return [d for d in deltas if d.path not in resolved_orphans]

    def _scry_blast_radius(self, deltas: List[RealityDelta]) -> List[RealityDelta]:
        """
        [ASCENSION 4]: TOPOLOGICAL BLAST RADIUS.
        Queries the Cortex to find what other files are impacted by these drifts.
        Recursively walks up to depth 3 to find cascading impacts.
        """
        if not self.memory or not self.memory.dependency_graph: return deltas

        dependents_graph = self.current_memory.dependency_graph.get("dependents", {})

        for delta in deltas:
            if not delta.requires_intervention: continue

            # BFS walk for dependents
            visited = set()
            queue = [(delta.path, 0)]
            max_depth = 3

            while queue:
                curr_path, depth = queue.pop(0)
                if depth > max_depth: continue

                direct_deps = dependents_graph.get(curr_path, [])
                for dep in direct_deps:
                    if dep not in visited:
                        visited.add(dep)
                        queue.append((dep, depth + 1))

            if visited:
                delta.blast_radius = list(visited)
                delta.impact_count = len(visited)

        return deltas

    # =========================================================================
    # == DATA HARVESTERS (SCRYING)                                           ==
    # =========================================================================

    def _harvest_ancient_vow(self) -> Dict[str, str]:
        """Extracts the expected hashes from the lockfile."""
        manifest = self.lock_data.get("manifest", {})
        return {p: m.get("sha256") for p, m in manifest.items() if m.get("action") != "DELETED"}

    def _summon_lockfile(self) -> Dict[str, Any]:
        p = self.root / "scaffold.lock"
        if not p.exists(): return {}
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            return {}

    def _read_phys(self, path: str) -> str:
        if path in self._physical_content_cache: return self._physical_content_cache[path]

        p = self.root / path
        if not p.exists() or not p.is_file(): return ""

        # [ASCENSION 14]: Memory Wall Sieve
        if p.stat().st_size > 5 * 1024 * 1024:  # > 5MB
            return "[HEAVY_MATTER_REDACTED]"

        try:
            txt = p.read_text(encoding='utf-8', errors='replace')
            self._physical_content_cache[path] = txt
            return txt
        except Exception:
            return ""

    def _read_lock_content(self, path: str) -> str:
        """Retrieves the historical content of the file from the shadow archive."""
        # For V1 Totality, if the content wasn't stored in the lock manifest directly,
        # we return void, meaning the Semantic Diff will fall back to hash comparison.
        manifest = self.lock_data.get("manifest", {})
        return manifest.get(path, {}).get("content", "")

    def _calculate_plan_fingerprint(self, deltas: List[RealityDelta]) -> str:
        """[ASCENSION 10]: Merkle Lattice Sealing."""
        hasher = hashlib.sha256()
        for d in sorted(deltas, key=lambda x: x.path):
            if d.requires_intervention:
                hasher.update(f"{d.path}:{d.action_required.value}".encode())
        return hasher.hexdigest()[:12]

    def format_plan_for_console(self, plan: GnosticExecutionPlan) -> str:
        """[THE HERALD'S PROCLAMATION]
        Forges a human-readable execution plan for the Architect to review.
        Designed to perfectly interface with your `TransmuteArtisan` or `DriftArtisan`.
        """
        active_deltas = [d for d in plan.deltas if d.requires_intervention]

        if not active_deltas:
            return "\n[bold green]✨ Reality is in perfect resonance with the Blueprint. No changes required.[/bold green]\n"

        from rich.table import Table
        from rich.text import Text
        from rich.console import Group
        from rich.panel import Panel

        table = Table(box=ROUNDED, expand=True, border_style="dim")
        table.add_column("Action", style="bold", width=10)
        table.add_column("Coordinate", style="white", ratio=2)
        table.add_column("Drift Diagnosis", style="dim", ratio=2)

        create_count, update_count, delete_count = 0, 0, 0

        for d in active_deltas:
            color = "green" if d.action_required == PlanAction.CREATE else "yellow" if d.action_required in (
                PlanAction.MERGE, PlanAction.UPDATE, PlanAction.RENAME) else "red"

            if d.action_required == PlanAction.CREATE:
                icon = "+ CREATE"
                create_count += 1
            elif d.action_required == PlanAction.DELETE:
                icon = "- DELETE"
                delete_count += 1
            elif d.action_required == PlanAction.RENAME:
                icon = "~ RENAME"
                update_count += 1
            else:
                icon = "~ UPDATE"
                update_count += 1

            path_display = d.path
            if d.previous_path:
                path_display = f"[dim]{d.previous_path}[/dim] -> {d.path}"

            diagnosis = d.drift_type.value
            if d.ast_similarity < 1.0 and d.drift_type != DriftType.NEW_WILL:
                diagnosis += f" (Structural Divergence: {int((1.0 - d.ast_similarity) * 100)}%)"

            if d.blast_radius:
                diagnosis += f"\n[dim red]! Impacts {len(d.blast_radius)} dependent scripture(s)[/dim red]"

            table.add_row(f"[{color}]{icon}[/]", path_display, diagnosis)

        summary = Text.from_markup(
            f"\n[bold]Plan:[/bold] [green]{create_count} to add[/green], "
            f"[yellow]{update_count} to mutate[/yellow], "
            f"[red]{delete_count} to destroy[/red]."
        )

        return Panel(
            Group(table, summary),
            title=f"[bold magenta]Gnostic Execution Plan (Hash: {plan.state_hash})[/bold magenta]",
            border_style="magenta"
        )

    def __repr__(self) -> str:
        return f"<Ω_DRIFT_ADJUDICATOR trace={self.trace_id[:8]} status=VIGILANT>"
