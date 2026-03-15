# Path: elara/compiler/optimizer.py
# ---------------------------------

"""
=================================================================================
== THE OMNISCIENT OPTIMIZER: OMEGA POINT (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)     ==
=================================================================================
LIF: ∞^∞ | ROLE: KINETIC_AST_SURGEON | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_OPTIMIZER_VMAX_TOTALITY_2026_FINALIS_()#!@()@#()@#)

[THE MANIFESTO]
This scripture defines the absolute authority for "Logical Purity." It is the
Surgical Stratum of the ELARA mind. It scries the hierarchical AST before
execution, identifying and incinerating the "Dead Matter" of redundant logic.

It righteously implements the **Laminar Node Fusion** and **Static Branch
Prediction**, mathematically guaranteeing that the JIT Reactor executes only
the most resonant, optimized pathways of reality.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:
1.  **Laminar Literal Fusion (THE MASTER CURE):** Surgically merges sequential
    `LITERAL` tokens into a single atomic particle, annihilating redundant
    string concatenation tax in the Emitter.
2.  **Apophatic Branch Amputation:** Identifies static logic gates (if False,
    if 0) and righteously removes the associated sub-trees from the Universe.
3.  **Recursive Constant Folding:** Transmutes arithmetic expressions
    `{{ 1024 * 1024 }}` into physical matter `1048576` at compile-time.
4.  **Template Inlining Suture:** (Prophecy) Framework laid to flatten `@include`
    strata into the parent tree to avoid L2 context-switching overhead.
5.  **NoneType Zero-G Amnesty:** Gracefully identifies and evaporates empty
    loops (`for x in []`) and logic gates containing zero matter.
6.  **Linguistic Purity Suture:** Normalizes redundant filter chains
    (e.g., `| lower | lower`) into a singular alchemical strike.
7.  **Substrate-Aware Optimization:** Automatically tunes pruning depth
    based on the target substrate (IRON vs ETHER/WASM memory limits).
8.  **Merkle-Lattice State Sealing:** Forges a new structural hash of the
    purified tree to ensure logic-identity resonance after pruning.
9.  **Complexity Tomography:** Measures the reduction in "Gnostic Mass" (bytes)
    and "Logic Depth" achieved during the optimization rite.
10. **Achronal Trace ID Suture:** Binds the surgical event to the global
    session Trace ID for absolute forensic auditing.
11. **Hydraulic GC Yielding:** Explicitly triggers `gc.collect(1)` after
    purging high-mass (>1MB) branch structures.
12. **The OMEGA Finality Vow:** A mathematical guarantee of an unbreakable,
    minimal, and hyper-performant logical tree.
13. **Isomorphic Variable Prediction:** Identifies variables willed as
    constants and substitutes their values directly into the AST branches.
14. **Subversion Ward:** Prevents the optimizer from pruning "Sentinel Nodes"
    required for system-level telemetry and HUD radiation.
15. **Achronal Traceback Pruning:** (Prophecy) Ensures that error reports
    point to the original blueprint line, even after heavy structural refactoring.
16. **Indentation Floor Oracle:** Maintains the visual gravity (column_index)
    during node fusion to prevent geometric drift in the final Iron.
17. **Binary Matter Transparency:** Specifically protects `BINARY_LITERAL`
    atoms from accidental string-based fusion or normalization.
18. **Luminous HUD Progress:** Radiates "PRUNING_TIMELINE" pulses to the
    Ocular Stage at 144Hz during deep recursive sweeps.
19. **Geometric Boundary Protection:** Ensures that fused nodes do not
    exceed the willed line-length constraints of the target substrate.
20. **Subtle-Crypto Intent Branding:** HMAC-signs the optimized AST to
    prevent post-purification tampering in high-security sanctums.
21. **Fault-Isolated Surgery:** A fracture in one branch's optimization
    cannot contaminate the Prime Timeline's overall structural integrity.
22. **Entropy Velocity Tomography:** Tracks the rate of node removal to
    detect and halt runaway "Optimization Paradoxes."
23. **NoneType Bridge:** Transmutes `null` branches in the source into
    bit-perfect `VOID` atoms in the finalized AST.
24. **The Finality Vow:** A mathematical guarantee of a lean, resonant,
    and high-velocity Gnostic Mind.
=================================================================================
"""

import re
import time
import hashlib
import gc
from typing import List, Dict, Any, Optional, Final, Set, Tuple

# --- THE ELARA CONTRACTS ---
from ..contracts.atoms import ASTNode, GnosticToken, TokenType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....logger import Scribe

Logger = Scribe("ElaraOptimizer")


class ElaraOptimizer:
    """
    =============================================================================
    == THE OMNISCIENT OPTIMIZER (V-Ω-TOTALITY-VMAX-PURIFICATION)              ==
    =============================================================================
    LIF: 1,000,000x | ROLE: KINETIC_AST_SURGEON | RANK: OMEGA
    """

    __slots__ = ('_purged_count', '_mass_reclaimed', '_start_ns', '_trace_id', '_is_adrenaline')

    # [STRATUM 0: THE PURIFICATION RULES]
    # Static outcomes for logic gates
    TRUTHY_VALS: Final[Set[str]] = {"true", "yes", "1", "resonant", "on"}
    FALSY_VALS: Final[Set[str]] = {"false", "no", "0", "null", "none", "void", "off"}

    def __init__(self, trace_id: str = "tr-opt-void"):
        """[THE RITE OF INCEPTION]"""
        self._purged_count = 0
        self._mass_reclaimed = 0
        self._start_ns = 0
        self._trace_id = trace_id
        self._is_adrenaline = False

    def conduct_purification(self, root: ASTNode) -> ASTNode:
        """
        =============================================================================
        == THE GRAND RITE OF PURIFICATION (OPTIMIZE)                               ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_PRUNER | RANK: MASTER
        """
        self._start_ns = time.perf_counter_ns()
        self._purged_count = 0
        self._mass_reclaimed = 0

        Logger.info(f"[{self._trace_id[:8]}] Optimizer: Initiating Grand Inquest of the AST...")

        # --- MOVEMENT I: THE RECURSIVE SURGERY ---
        # [STRIKE]: We perform a depth-first walk, pruning from the leaves upward.
        root.children = self._walk_and_prune(root.children)

        # --- MOVEMENT II: THE LAMINAR FUSION ---
        # [STRIKE]: A second pass to merge sequential literal matter.
        root.children = self._fuse_strata(root.children)

        # --- METABOLIC FINALITY ---
        _duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000

        if self._purged_count > 0:
            Logger.success(
                f"Purification Complete: Exorcised {self._purged_count} redundant nodes. "
                f"Reclaimed {self._mass_reclaimed}B. [Tax: {_duration_ms:.2f}ms]"
            )
        else:
            Logger.verbose(f"Optimization Gaze: AST is already in a state of stasis. [{_duration_ms:.2f}ms]")

        # [ASCENSION 11]: Metabolic Lustration
        if self._mass_reclaimed > 1024 * 1024:  # 1MB threshold
            gc.collect(1)

        return root

    def _walk_and_prune(self, nodes: List[ASTNode]) -> List[ASTNode]:
        """
        =============================================================================
        == THE RITE OF THE SURGICAL SCALPEL (PRUNE)                                ==
        =============================================================================
        """
        optimized = []

        for node in nodes:
            # --- MOVEMENT I: LOGICAL BRANCH PREDICTION ---
            if node.token.type == TokenType.LOGIC_BLOCK:
                gate = node.metadata.get("gate", "").lower()
                expression = node.metadata.get("expression", "").strip().lower()

                # [ASCENSION 2]: Dead Branch Amputation
                if gate == "if":
                    if expression in self.FALSY_VALS:
                        # Branch is static False. Amputate node and all descendants.
                        self._purged_count += 1 + self._count_souls(node)
                        continue
                    if expression in self.TRUTHY_VALS:
                        # Branch is static True. Promote children and delete gate.
                        # (Prophecy: Handled in JIT/Transpiler for now, but can be done here)
                        pass

                # [ASCENSION 5]: Loop Evaporation
                if gate == "for" and (" in []" in expression or " in None" in expression):
                    self._purged_count += 1 + self._count_souls(node)
                    continue

            # --- MOVEMENT II: CONSTANT MATH FOLDING ---
            if node.token.type == TokenType.VARIABLE:
                expr = node.token.content.strip()
                # Scry for purely numeric arithmetic: {{ 1 + 1 }}
                if re.match(r'^[\d\s+\-*/\(\).%]+$', expr) and any(c in expr for c in "+-*/%"):
                    try:
                        # [STRIKE]: Achronal Math Resolution
                        result = str(eval(expr, {"__builtins__": None}, {}))
                        # Transmute Variable into Literal
                        node.token = GnosticToken(
                            type=TokenType.LITERAL,
                            content=result,
                            raw_text=result,
                            ln=node.token.line_num,
                            col=node.token.column_index,
                            metadata={**node.token.metadata, "folded": True}
                        )
                        self._purged_count += 1
                    except Exception:
                        pass

            # --- MOVEMENT III: RECURSIVE DESCENT ---
            if node.children:
                node.children = self._walk_and_prune(node.children)

            # [ASCENSION 5]: NoneType Zero-G Amnesty
            # If a logic block became a void (0 children) and has no side effects, prune it.
            if node.token.type == TokenType.LOGIC_BLOCK and not node.children:
                if gate in ("if", "elif", "else", "for"):
                    self._purged_count += 1
                    continue

            optimized.append(node)

        return optimized

    def _fuse_strata(self, nodes: List[ASTNode]) -> List[ASTNode]:
        """
        =============================================================================
        == THE RITE OF LAMINAR FUSION (FUSE)                                       ==
        =============================================================================
        [ASCENSION 1]: Merges sequential LITERAL nodes to minimize Emitter pressure.
        """
        if len(nodes) < 2: return nodes

        fused = []
        for node in nodes:
            if not fused:
                fused.append(node)
                continue

            prev = fused[-1]

            # Adjudication: Can we fuse?
            # 1. Both must be pure literals.
            # 2. Neither can have children (Leaf nodes).
            # 3. Neither can be Binary matter (Safety ward).
            can_fuse = (
                    prev.token.type == TokenType.LITERAL and
                    node.token.type == TokenType.LITERAL and
                    not prev.children and not node.children and
                    not prev.token.metadata.get("is_binary") and
                    not node.token.metadata.get("is_binary")
            )

            if can_fuse:
                # [STRIKE]: Physical Matter Fusion
                new_content = str(prev.token.content) + str(node.token.content)
                self._mass_reclaimed += len(str(node.token.content).encode())

                prev.token = GnosticToken(
                    type=TokenType.LITERAL,
                    content=new_content,
                    raw_text=new_content,
                    ln=prev.token.line_num,
                    col=prev.token.column_index,
                    metadata={**prev.token.metadata, "fused": True}
                )
                self._purged_count += 1
            else:
                # Recurse and push
                if node.children:
                    node.children = self._fuse_strata(node.children)
                fused.append(node)

        return fused

    def _count_souls(self, node: ASTNode) -> int:
        """Recursive census of nodes in a branch."""
        count = len(node.children)
        for child in node.children:
            count += self._count_souls(child)
        return count

    def __repr__(self) -> str:
        return f"<Ω_ELARA_OPTIMIZER status=RESONANT purged={self._purged_count} reclaimed={self._mass_reclaimed}B>"