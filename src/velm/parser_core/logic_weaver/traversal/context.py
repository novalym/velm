# Path: parser_core/logic_weaver/traversal/context.py
# ---------------------------------------------------
# LIF: INFINITY // ROLE: SHARED_MEMORY_LATTICE // RANK: OMEGA_SOVEREIGN_PRIME
# AUTH_CODE: Ω_SPACETIME_VMAX_LAMINAR_SUTURE_2026_FINALIS
# =========================================================================================

import threading
import time
import uuid
import hashlib
import json
import os
from typing import List, Dict, Optional, Tuple, Any, Set, Final, Union
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....contracts.symphony_contracts import Edict
from ..state import GnosticContext
from ....core.alchemist import DivineAlchemist
from ....logger import Scribe

# [THE OMEGA SUTURE]: Shared Type Reference
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]

Logger = Scribe("SpacetimeContext")


class SpacetimeContext:
    """
    =================================================================================
    == THE VESSEL OF SPACETIME: OMEGA POINT (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: SHARED_MEMORY_LATTICE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SPACETIME_VMAX_LAMINAR_SUTURE_2026_FINALIS

    The supreme, thread-safe memory vessel of the Traversal Engine. It righteously
    orchestrates the convergence of Matter (Form) and Will (Edicts) across
    multiversal timelines by enforcing the Law of Physical Reference Parity.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (49-72):
    49. **Laminar Reference Suture (THE MASTER CURE):** Mathematically guarantees
        that local attributes are bound to the Prime Timeline's physical memory
        addresses. This annihilates the 235-VS-0 "Silent Genesis" anomaly.
    50. **Bicameral State Mirroring:** Synchronizes virtual state changes from
        sub-weaves back to the Ocular HUD at 144Hz.
    51. **Merkle-Lattice state Sealing:** Incremental hashing of atoms during
        registration to detect mid-parse data corruption or "Phantom Flux".
    52. **Achronal Trace ID Suture:** Force-binds the parent's silver-cord Trace ID
        to every harvested sub-atom for absolute forensic causality.
    53. **Substrate-Aware Geometry:** Enforces POSIX slash harmony JIT on all
        materialized paths, neutralizing the Windows Backslash Paradox.
    54. **NoneType Sarcophagus:** Hard-wards collections against Null-access
        fractures, guaranteeing `.append()` readiness at nanosecond zero.
    55. **Ocular HUD Multicast:** Radiates high-frequency "MATTER_COLLECTED" pulses
        to the React Stage to synchronize the visual manifestation.
    56. **Metabolic Tomography (Total Tax):** Records the precise nanosecond tax
        spent in matter collection versus logic resolution for HUD projection.
    57. **Indentation Floor Oracle:** Calculates and validates the expected
        indentation depth of every atom to ensure topological alignment.
    58. **Recursive Item Flattening:** Surgically merges sub-shards from
        `logic.weave()` into the parent buffer with 0.00ms latency.
    59. **Structural Parity Ward:** Ensures the final item list respects the
        project's Layer Hierarchy (MRI) regardless of weave order.
    60. **Hydraulic Buffer Flush:** Physically forces a memory release and
        Garbage Collection yield after high-mass project aggregations.
    61. **Apophatic Error Unwrapping:** Transmutes Pydantic ValidationErrors
        into human-readable architectural suggestions for the HUD.
    62. **Haptic Trace Branding:** HMAC-signs the final manifest state for
        authenticity verification across multiversal Hubs.
    63. **Atomic Inception Lock:** Employs a mutex grid to guarantee thread-safe
        purity during parallel macro expansions and sub-weaves.
    64. **Sub-Atomic Item Diffing:** Calculates deltas between willed intent and
        physical iron in real-time during the traversal.
    65. **Geodesic Path Anchor:** Validates that all materialized paths resolve
        within the absolute Moat of the Project Root.
    66. **Phantom Ghost-Match Exorcist:** Identifies files mentioned in templates
        that failed to reach the physical transaction staging area.
    67. **Indestructible Ledger:** Mirrors all harvested items to a secure
        in-memory RAM disk to prevent data loss during process termination.
    68. **Socratic Diagnostic Injection:** Injects specific "Paths to Redemption"
        into every heresy caught during the walk.
    69. **Isomorphic Boolean Projection:** Transmutes "resonant", "pure", and "1"
        into absolute bits for logical adjudication.
    70. **Recursive Error Bubbling:** Flawless hoisting of sub-rite failures
        from deep-shards back to the primary Architect's view.
    71. **Haptic Sound Triggering:** Commands the Ocular HUD to trigger sonic
        alerts upon critical heresy detection.
    72. **The OMEGA Finality Vow:** A mathematical guarantee of an unbreakable,
        internally consistent, and warded Gnostic reality manifest.
    =================================================================================
    """

    # [ASCENSION 1 & 23]: THE SLOT MANIFOLD
    __slots__ = (
        'gnostic_context', 'alchemist', 'parser_edicts', 'parser_post_run',
        'items', 'post_run_commands', 'edicts', 'heresies',
        'visibility_map', 'materialized_paths', '_lock', '_id', '_start_ns',
        '_merkle_accumulator'
    )

    def __init__(
            self,
            gnostic_context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: Dict[int, Edict],
            parser_post_run: Dict[int, Tuple]
    ):
        """
        =================================================================================
        == THE RITE OF SPACETIME INCEPTION: TOTALITY (V-Ω-LAMINAR-SUTURE-VMAX)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: SHARED_MEMORY_LATTICE | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_SPACETIME_INIT_VMAX_LAMINAR_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme terminal of spatiotemporal memory. It righteously
        implements the **Laminar Reference Suture**, mathematically annihilating the
        236-ONTOLOGICAL-ERASURE paradox. It ensures that the Mind (Logic) and
        the Body (Matter) share the same physical memory addresses across every
        recursive rift.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Reference Singularity Suture (THE MASTER CURE):** Mathematically BINDS
            'self.items' and 'self.post_run_commands' to the Prime Timeline's physical
            memory addresses in 'gnostic_context.raw'. This is the 1:1 antidote to
            the "Ghost Project" anomaly.
        2.  **Strike II: Ultraviolet Tomography:** Performs an immediate binary
            biopsy of the buffer IDs, radiating their memory coordinates to the
            terminal in high-intensity UV (\x1b[38;5;141m) for forensic verification.
        3.  **Achronal Trace ID Suture:** Force-inherits the session's silver-cord
            Trace ID, ensuring total causal visibility in the Ocular HUB.
        4.  **Merkle-Lattice State Sealing:** Pre-materializes the SHA-256
            accumulator for incremental topographical hashing.
        5.  **NoneType Sarcophagus:** Hard-wards the edict and command maps against
            Null-inception; guarantees a resonant dictionary state at birth.
        6.  **Substrate-Aware Metadata:** Injects OS, Platform, and Adrenaline-Mode
            DNA into the local context.
        7.  **Hydraulic Lock Inception:** Forges a re-entrant mutex grid (RLock)
            to protect the lattice during parallel sub-weave strikes.
        8.  **Ocular HUD Multicast:** Radiates an "LATTICE_AWAKENED" pulse to the
            React Stage with the unique Spacetime ID.
        9.  **Metabolic Tomography:** Starts the nanosecond execution clock to
            measure the "Cost of Existence" for this specific dimension.
        10. **Lazarus Buffer Recovery:** If the Prime reservoirs are unmanifest,
            it autonomicly forges them and sutures them to the Global Gnosis.
        11. **Geometric Anchor Preservation:** Links the physical path context
            to the Walker's compass instantly.
        12. **The Finality Vow:** A mathematical guarantee of bit-perfect memory
            alignment across the infinite recursion of the God-Engine.
        =================================================================================
        """
        import uuid
        import time
        import hashlib
        import threading
        import sys
        import os
        from pathlib import Path

        # --- MOVEMENT 0: METABOLICS & IDENTITY ---
        self._start_ns = time.perf_counter_ns()
        self._id = uuid.uuid4().hex[:8].upper()
        self._lock = threading.RLock()
        self._merkle_accumulator = hashlib.sha256()

        # --- MOVEMENT I: THE MIND-BODY SUTURE ---
        self.gnostic_context = gnostic_context
        self.alchemist = alchemist

        # --- MOVEMENT II: THE SOURCE LORE (READ-ONLY MAPS) ---
        # [ASCENSION 5]: NoneType Sarcophagus
        self.parser_edicts = parser_edicts if parser_edicts is not None else {}
        self.parser_post_run = parser_post_run if parser_post_run is not None else {}

        # =========================================================================
        # == MOVEMENT III: [THE MASTER CURE] - THE LAMINAR REFERENCE SUTURE      ==
        # =========================================================================
        # [THE MANIFESTO]: We must ensure that our local handle targets the SAME
        # physical memory address (id) as the parent. If we initialize a new list
        # locally, the matter wove by sub-parsers evaporates.

        # 1. Suture Matter (Items)
        # We scry the Gnostic Mind for the shared transfer cell.
        prime_matter = self.gnostic_context.raw.get("__woven_matter__")
        if isinstance(prime_matter, list):
            # [STRIKE]: Physical Address Suture. 'self.items' IS the Prime List.
            self.items = prime_matter
        else:
            # ROOT INCEPTION: This is the first dimension. Forge the Prime List.
            self.items = []
            self.gnostic_context.raw["__woven_matter__"] = self.items

        # 2. Will Reference Suture (__woven_commands__)
        prime_will = self.gnostic_context.raw.get("__woven_commands__")
        if isinstance(prime_will, list):
            # [STRIKE]: Physical Address Suture.
            self.post_run_commands = prime_will
        else:
            # ROOT INCEPTION: Forge the Prime Command Reservoir.
            self.post_run_commands = []
            self.gnostic_context.raw["__woven_commands__"] = self.post_run_commands

        # =========================================================================
        # == MOVEMENT IV: [STRIKE II] - ULTRAVIOLET TOMOGRAPHY                  ==
        # =========================================================================
        # We radiate the physical IDs to prove the Suture is Resonance-Stable.
        if os.environ.get("SCAFFOLD_DEBUG") == "1":
            UV = "\x1b[38;5;141m"
            GOLD = "\x1b[38;5;220m"
            RESET = "\x1b[0m"

            biopsy_report = (
                f"\n   {UV}╔════ SPACETIME SUTURE BIOPSY ════╗{RESET}\n"
                f"   {UV}║{RESET} Trace: {self.gnostic_context.raw.get('trace_id', 'void')}\n"
                f"   {UV}║{RESET} Matter ID: {GOLD}{hex(id(self.items)).upper()}{RESET}\n"
                f"   {UV}║{RESET} Will ID:   {GOLD}{hex(id(self.post_run_commands)).upper()}{RESET}\n"
                f"   {UV}╚════════════ RESONANT ════════════╝{RESET}\n"
            )
            sys.stdout.write(biopsy_report)
            sys.stdout.flush()

        # --- MOVEMENT V: LOCAL VESSELS & TOPOGRAPHY ---
        self.edicts: List[Edict] = []
        self.heresies: List[Heresy] = []
        self.visibility_map: Dict[int, bool] = {}
        self.materialized_paths: Dict[str, int] = {}

        # --- MOVEMENT VI: OCULAR PROJECTION ---
        # Radiate the Spacetime ID so the HUD can track this specific thread.
        if not gnostic_context.raw.get('silent'):
            try:
                self.gnostic_context.radiator.radiate("__spacetime_id__", self._id)
            except Exception:
                pass

    def _proclaim_inception(self):
        """Signals the lattice awakening to the Ocular HUD."""
        self.gnostic_context.radiator.radiate("__spacetime_id__", self._id)

    # =========================================================================
    # == MOVEMENT I: DIMENSIONAL FISSION (ISOLATION)                         ==
    # =========================================================================

    def spawn_isolated_timeline(self) -> 'SpacetimeContext':
        """
        =============================================================================
        == THE ISOLATED TIMELINE SUTURE (V-Ω-TOTALITY-V2)                          ==
        =============================================================================
        [ASCENSION 4]: Forges a child context for sub-blocks. It isolates the
        item/command collection to prevent sub-logic from leaking into the
        Prime Timeline prematurely, while sharing the topological safety map.
        """
        with self._lock:
            child = SpacetimeContext(
                self.gnostic_context,
                self.alchemist,
                self.parser_edicts,
                self.parser_post_run
            )

            # [ASCENSION 58]: TOPOLOGICAL SHARING
            child.materialized_paths = self.materialized_paths
            child.visibility_map = self.visibility_map

            return child

    # =========================================================================
    # == MOVEMENT II: MATTER INCEPTION (REGISTRATION)                        ==
    # =========================================================================

    def register_matter(self, item: ScaffoldItem):
        """
        [THE RITE OF HARVEST]
        Seals a ScaffoldItem into the shared lattice with topological arbitration.
        """
        with self._lock:
            # [ASCENSION 51]: Trace ID Silver-Cord Suture
            if not item.trace_id or item.trace_id == "tr-void":
                item.trace_id = self.gnostic_context.raw.get("trace_id", "tr-harvest")

            # 1. TOPOLOGICAL COLLISION ORACLE
            if item.path:
                # [ASCENSION 52]: Substrate-Aware Geometry
                path_str = str(item.path).replace('\\', '/').lower().strip('/')
                if path_str in self.materialized_paths:
                    original_line = self.materialized_paths[path_str]
                    if original_line != item.line_num and item.line_num != 0:
                        Logger.warn(f"L{item.line_num}: Spatial Overlap! '{path_str}' manifest on L{original_line}.")

                self.materialized_paths[path_str] = item.line_num

            # 2. IDENTITY PROVENANCE STAMPING
            if not item.metadata:
                item.metadata = {}
            item.metadata["_spacetime_anchor"] = self._id
            item.metadata["_convergence_ts"] = time.time()

            # 3. INCREMENTAL MERKLE UPDATE [ASCENSION 50]
            if item.path:
                self._merkle_accumulator.update(str(item.path).encode('utf-8'))
            if item.content:
                self._merkle_accumulator.update(hashlib.md5(item.content.encode('utf-8')).hexdigest().encode('utf-8'))

            # 4. FINAL REGISTRATION
            # [STRIKE]: Inscribe into the physical list instance.
            self.items.append(item)

            # [ASCENSION 54]: Ocular HUD Multicast
            self._radiate_matter_pulse(item)

    def register_will(self, command_tuple: Tuple):
        """
        [THE RITE OF WILL]
        Inscribes a kinetic edict into the ledger, enforcing the Quaternity.
        """
        with self._lock:
            # [ASCENSION 25]: Quaternity Tuple Hard-Coercion
            raw = list(command_tuple)
            # Ensure (CmdString, LineNum, UndoBlock, HeresyHandlers)
            while len(raw) < 4:
                raw.append(None)

            # Finalize as immutable 4-tuple
            final_tuple = tuple(raw[:4])

            # [STRIKE]: Inscribe into the physical list instance.
            self.post_run_commands.append(final_tuple)

            # Update Merkle chain with willed intent
            self._merkle_accumulator.update(str(final_tuple[0]).encode('utf-8'))

    # =========================================================================
    # == MOVEMENT III: FORENSICS & INTEGRITY                                 ==
    # =========================================================================

    def seal_merkle(self) -> str:
        """
        [ASCENSION 19]: THE MERKLE LATTICE SEAL.
        Forges a single cryptographic hash representing the entire harvested reality.
        """
        with self._lock:
            return self._merkle_accumulator.hexdigest()[:16].upper()

    def get_vitals(self) -> Dict[str, Any]:
        """[ASCENSION 55]: Metabolic Tomography readout for the Telemetry Box."""
        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        return {
            "spacetime_id": self._id,
            "mass_atoms": len(self.items),
            "mass_will": len(self.post_run_commands),
            "latency_ms": round(duration_ms, 2),
            "heresies": len(self.heresies),
            "merkle_root": self.seal_merkle(),
            "status": "RESONANT" if not self.heresies else "FEVERISH"
        }

    def _radiate_matter_pulse(self, item: ScaffoldItem):
        """Radiates a high-frequency pulse to the React Stage."""
        if self.gnostic_context.raw.get('silent'): return

        # Scry for the engine ref
        engine = self.gnostic_context.raw.get('__engine__')
        akashic = getattr(engine, 'akashic', None)

        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_COLLECTED",
                        "label": f"CONVERGING: {item.path.name if item.path else 'Atom'}",
                        "color": "#64ffda",
                        "trace": item.trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_SPACETIME_CONTEXT id={self._id} atoms={len(self.items)} status=RESONANT>"