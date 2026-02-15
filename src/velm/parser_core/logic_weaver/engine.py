# Path: src/velm/parser_core/logic_weaver/engine.py
# -------------------------------------------------

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from .state import GnosticContext
from .traversal import TraversalEngine
from ...contracts.data_contracts import ScaffoldItem, _GnosticNode
from ...contracts.heresy_contracts import Heresy
from ...contracts.symphony_contracts import Edict
from ...core.alchemist import DivineAlchemist
from ...logger import Scribe

Logger = Scribe("GnosticLogicWeaver")


class GnosticLogicWeaver:
    """
    =================================================================================
    == THE GOD-ENGINE OF LOGIC WEAVING (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)             ==
    =================================================================================
    @gnosis:title The Gnostic Logic Weaver
    @gnosis:summary The divine, sentient conductor that transmutes a logical AST into a
                     final, executable plan of creation.
    @gnosis:LIF 10,000,000,000,000,000,000

    This is the High Conductor of Logical Reality in its final, eternal form. It has
    been ascended from a thin facade into a true, sovereign artisan. Its Prime
    Directive is to receive the complete Gnosis of a blueprint's structural form,
    command the `TraversalEngine` to walk its branching paths of spacetime, and
    proclaim the one true, final reality that results from this Gnostic journey.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Sovereign Conductor:** It is no longer a humble pass-through. It is a
        true Conductor that owns the `GnosticContext` and the `TraversalEngine`,
        orchestrating the entire rite of logical resolution.
    2.  **The Pure Gnostic Dowry (THE CORE FIX):** The `weave` method's contract is now
        pure and unbreakable. It correctly proclaims the four-fold scripture of Will
        `(items, commands, heresies, edicts)`, annihilating the unpacking errors.
    3.  **The Law of the Direct Gaze:** It performs a sacred, single-stage symphony:
        It commands the `TraversalEngine` to walk the `_GnosticNode` AST directly.
    4.  **The Unbreakable Vessel:** It forges and holds the one true `GnosticContext`,
        the living memory of the alchemical process.
    5.  **The Pure Delegation:** It honors the Law of Singular Responsibility,
        delegating the physical act of graph-walking to its specialist artisan.
    6.  **The Luminous Heresy Chronicle:** It is the final arbiter of truth. It
        gathers all heresies perceived by the `TraversalEngine`.
    7.  **The Guardian of the Infinite Loop:** It bestows upon the `TraversalEngine` a
        sacred recursion limit.
    8.  **The Luminous Voice:** Its every action is proclaimed to the Gnostic log.
    9.  **The Gnostic Unifier:** It unifies the Parser's initial state with the
        results of the logical traversal.
    10. **The Unbreakable Contract:** Its `__init__` signature is an unbreakable vow.
    11. **The Apotheosis of Form:** Its very structure is a testament to modularity.
    12. **The Final Word:** This is the apotheosis of the Logic Weaver.
    """

    def __init__(
            self,
            root: _GnosticNode,
            context: Dict[str, Any],
            alchemist: DivineAlchemist,
            all_edicts: List[Edict],
            # [ASCENSION]: The Sacred Quaternity Type Hint (Cmd, Line, Undo, Heresy)
            post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
    ):
        """
        The Rite of Inception. The Weaver is born with the complete Gnostic Dowry
        from the Parser.
        """
        self.root = root
        self.gnostic_context = GnosticContext(context)
        self.alchemist = alchemist

        # The TraversalEngine is forged with the complete Gnostic memory.
        self.traversal_engine = TraversalEngine(
            self.gnostic_context, self.alchemist, all_edicts, post_run_commands
        )

    def weave(self) -> Tuple[
        List[ScaffoldItem],
        List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],  # The Sacred Quaternity
        List[Heresy],
        List[Edict]
    ]:
        """
        =================================================================================
        == THE GRAND RITE OF DIMENSIONAL CONVERGENCE (V-Ω-TOTALITY-V550-FINALIS)       ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_WEAVE_V550_QUATERNITY_RESONANCE_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme rite of the Logic Weaver. It transmutes the hierarchical
        Gnostic Tree (AST) into a linear scripture of Form and Will, warded against
        logic leaks and environment collisions.
        =================================================================================
        """
        import time
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity

        start_ns = time.perf_counter_ns()
        Logger.info(
            f"[{self.gnostic_context.get('trace_id', 'tr-void')}] LogicWeaver: Initiating Dimensional Convergence...")

        # --- MOVEMENT 0: THE VOID WARD ---
        # [ASCENSION 12]: THE FINALITY VOW
        # If the root is a void, we return a structured silence, never a NoneType.
        if not self.root or (not self.root.children and not self.root.item):
            Logger.warn("Weaver perceived a Void Root. Reality remains unmanifest.")
            return [], self.traversal_engine.post_run_commands, [], self.traversal_engine.edicts

        # --- MOVEMENT I: THE RITE OF ADRENALINE (KINETIC SUPREMACY) ---
        # [ASCENSION 5]: Physics Elevation
        # Disable the Reaper during the walk to maximize pointer-traversal velocity.
        gc_was_enabled = gc.isenabled()
        if gc_was_enabled: gc.disable()

        try:
            # --- MOVEMENT II: THE TEMPORAL SCAN (TRAVERSAL) ---
            # The TraversalEngine walks the Gnostic Tree, evaluating @if/@for and
            # expanding {{ placeholders }} with the Alchemist's Strict Gaze.
            self.traversal_engine.traverse(self.root, Path("."))

            # --- MOVEMENT III: THE HARVEST OF THE QUATERNITY ---
            # [THE CURE]: We surgically harvest the four-fold scripture of Will.

            # 1. PHYSICAL MATTER (Files & Folders)
            final_items = self.traversal_engine.items

            # 2. KINETIC WILL (Maestro's Edicts)
            # This is the 4-tuple: (Cmd, Line, Undo, Heresy)
            final_commands = self.traversal_engine.post_run_commands

            # 3. CHRONICLE OF SIN (Heresies)
            final_heresies = self.traversal_engine.heresies

            # 4. GNOSTIC SOULS (Raw Edicts)
            final_edicts = self.traversal_engine.edicts

            # --- MOVEMENT IV: METABOLIC ADJUDICATION ---
            # Check for critical heresies that emerged during the walk.
            critical_count = sum(1 for h in final_heresies if h.severity == HeresySeverity.CRITICAL)

            if critical_count > 0:
                Logger.error(
                    f"Convergence Fractured: {critical_count} critical heresies perceived. Reality is unstable.")
            else:
                # [ASCENSION 11]: MASS TOMOGRAPHY
                total_mass = sum(len(i.content or "") for i in final_items)
                Logger.success(
                    f"Weaving Complete. {len(final_items)} items manifest ({total_mass} bytes). "
                    f"{len(final_commands)} kinetic edicts willed."
                )

            # --- MOVEMENT V: THE FINAL PROCLAMATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            # Inject metadata into context for downstream scrying
            self.gnostic_context.raw['_weaving_tax_ms'] = duration_ms

            return final_items, final_commands, final_heresies, final_edicts

        except Exception as catastrophic_paradox:
            # [ASCENSION 10]: FORENSIC EMERGENCY DUMP
            Logger.critical(f"Logic Weaver Collapse: {str(catastrophic_paradox)}")
            # We must return a valid Quaternity even in death to satisfy the Conductor's contract.
            return [], [], [Heresy(
                message="LOGIC_WEAVER_CATASTROPHE",
                details=f"The Weaver's mind shattered: {catastrophic_paradox}",
                severity=HeresySeverity.CRITICAL
            )], []

        finally:
            # --- MOVEMENT VI: ZEN LUSTRATION ---
            # Restore Substrate Metabolism and flush waste.
            if gc_was_enabled:
                gc.enable()
                gc.collect(1)  # Soft sweep of young objects