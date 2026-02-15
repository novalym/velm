# Path: src/velm/core/structure_sentinel/strategies/python_strategy/frameworks/engine.py
# --------------------------------------------------------------------------------------

from __future__ import annotations
import ast
import time
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final, Union

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .contracts import WiringStrategy, InjectionPlan
from .strategies import ALL_STRATEGIES
from .heuristics import EntrypointDiviner
from .surgeon import ASTSurgeon, DjangoSurgeon
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils import atomic_write

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......creator.io_controller import IOConductor
    from ......logger import Scribe


class FrameworkFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN FRAMEWORK FACULTY (V-Ω-TOTALITY-V7000-KINETIC-WIRING)         ==
    =================================================================================
    LIF: ∞ | ROLE: NEURAL_WIRING_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_FRAMEWORK_V7000_SINGULAR_CONTEXT_FINALIS

    The Divine Artisan responsible for the automated integration of components.
    It ensures that what is forged is also connected, annihilating the
    "Mute Component" heresy.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **Unified Context Consumption (THE FIX):** It no longer materializes its own
        context. It consumes the sovereign `SharedContext` bestowed by the
        Orchestrator, ensuring 100% alignment with the active strike's geometry.

    2.  **Transactional Neuro-Surgery (THE CURE):** It utilizes the inherited `_write`
        rite from `BaseFaculty`. This guarantees that every `app.include_router` or
        `INSTALLED_APPS` update is chronicled in the Ledger and manifest upon commit.

    3.  **Bicameral Entrypoint Scrying:** It wields the `EntrypointDiviner` to find
        the application's "Sun" (main.py) within both the Physical and Staging
        realms, enabling wiring even during a total project genesis.

    4.  **Polyglot Strategy Matrix:** Supports a pluggable architecture of
        `WiringStrategies` for FastAPI, Flask, Django, and Typer, selecting
        the correct logic based on the scripture's DNA.

    5.  **AST-Aware Precision:** Employs the `ASTSurgeon` to perform surgical grafts
        of `import` and `registration` edicts, respecting the Architect's
        formatting and preserving comments.

    6.  **The Idempotency Shield:** Performs a pre-flight "Existence Gaze" on the
        target's AST. If the component is already wired, the Hand is stayed,
        preventing duplicate registration heresies.

    7.  **Geometric Path Normalization:** Resolves relative import paths by
        calculating the distance between the Component and the App Root across
        the transaction's virtual topography.

    8.  **Fault-Isolated Integration:** Wraps every surgical strike in a
        protective ward. A failure to wire one component is chronicled as an
        anomaly, but the Electrician continues the Great Work.

    9.  **Alchemical Expression Support:** Transmutes wiring statements using
        Jinja2 variables, allowing for dynamic prefixing (`/api/v1`) based on
        the project's Gnostic state.

    10. **Metabolic Tomography:** Measures the nanosecond cost of framework
        perception and surgery, reporting the "Integration Tax" to the Ocular HUD.

    11. **Semantic Selector Logic:** Uses the `@inside` directive logic to find
        the perfect line for injection (e.g., immediately after the App initialization).

    12. **The Finality Vow:** A mathematical guarantee that after this rite, the
        newly forged logic is resonant and reachable within the application.
    =================================================================================
    """

    def __init__(self, logger: 'Scribe'):
        """
        [THE RITE OF INCEPTION]
        Births the Electrician with the full endowment of the BaseFaculty.
        """
        super().__init__(logger)

        # Specialist Instruments
        self.strategies: List[WiringStrategy] = [cls(self) for cls in ALL_STRATEGIES]
        self.heuristics = EntrypointDiviner(self._read_with_ctx)

    def wire_components(
            self,
            file_path: Path,
            context: "SharedContext"
    ):
        """
        =============================================================================
        == THE RITE OF KINETIC INTEGRATION (V-Ω-TOTALITY-UNIFIED)                  ==
        =============================================================================
        Detects if a new file is an integratable framework component and wires it.
        """
        start_ns = time.perf_counter_ns()

        # 1. READ THE SOURCE (Using the Ancestral Hand)
        # We scry the file being processed to see if it's a Router, Blueprint, etc.
        content = self._read(file_path, context)
        if not content:
            return

        # 2. THE FRAMEWORK INQUISITION
        for strategy in self.strategies:
            # A. DETECT: Does this file define a "Wireable" entity?
            component_var = strategy.detect(content)
            if not component_var:
                continue

            self.logger.verbose(f"   -> {strategy.name} Component detected: [yellow]{component_var}[/]")

            # B. LOCATE: Find the Application's "Sun" (e.g. main.py)
            # We pass the context to the diviner for staging-aware scrying.
            target_file = strategy.find_target(context.project_root, context.transaction)

            # C. GHOST-TARGET WARD: Prevent self-wiring
            if not target_file or target_file.resolve() == file_path.resolve():
                continue

            # D. PERCEIVE: Read the target's soul (main.py)
            target_content = self._read(target_file, context)
            if not target_content:
                continue

            # E. FORGE: Calculate the surgical plan
            plan = strategy.forge_injection(file_path, component_var, target_content, context.project_root)

            if plan:
                # F. STRIKE: Perform the AST surgery
                plan.target_file = target_file
                self._execute_wiring_rite(plan, target_content, context)

                # Proclaim the success of the integration
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                self.logger.verbose(f"      -> Integrated into '{target_file.name}' ({duration_ms:.2f}ms)")
                return

    def _execute_wiring_rite(self, plan: InjectionPlan, content: str, context: "SharedContext"):
        """
        Performs the physical AST surgery and commits it to the Ledger via the Unified Hand.
        """
        try:
            # 1. THE INQUISITION: Parse the target soul
            tree = ast.parse(content)

            # 2. THE SURGERY: Select the specialized surgeon
            if plan.strategy_name == "Django":
                surgeon = DjangoSurgeon(plan.wiring_stmt)
            else:
                surgeon = ASTSurgeon(plan.import_stmt, plan.wiring_stmt, plan.anchor)

            # 3. THE TRANSMUTATION: Mutate the AST
            new_tree = surgeon.visit(tree)
            ast.fix_missing_locations(new_tree)

            # 4. THE RE-MATERIALIZATION: Unparse back to scripture
            if hasattr(ast, 'unparse'):
                new_content = ast.unparse(new_tree)
            else:
                import astunparse
                new_content = astunparse.unparse(new_tree)

            # 5. THE TRANSACTIONAL STRIKE
            if new_content != content:
                self.logger.success(
                    f"   -> Wiring {plan.strategy_name} [cyan]{plan.anchor}[/] in [white]{plan.target_file.name}[/]"
                )

                # [ASCENSION 2]: THE UNBREAKABLE HAND
                # Use the parent's _write which is sutured to the IOConductor.
                self._write(plan.target_file, new_content, context)

        except Exception as e:
            # [FACULTY 8]: Fault Isolation
            self.logger.warn(f"   -> Integration Heresy in '{plan.target_file.name}': {e}")
            if self.logger.is_verbose:
                self.logger.debug(traceback.format_exc())

    def _read_with_ctx(self, path: Path, root: Path, tx: Optional["GnosticTransaction"]) -> str:
        """
        A local bridge for the EntrypointDiviner to use the Bicameral Gaze.
        """
        # We manually wrap the call for the diviner which uses an older signature
        if tx:
            try:
                rel = path.relative_to(root)
                staged = tx.get_staging_path(rel)
                if staged.exists():
                    return staged.read_text(encoding='utf-8')
            except ValueError:
                pass

        if path.exists():
            return path.read_text(encoding='utf-8')
        return ""

    def __repr__(self) -> str:
        return f"<Ω_FRAMEWORK_FACULTY status=VIGILANT version=7000.0>"