# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/engine.py
# ---------------------------------------------------------------------------------------------------------------------

import ast
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List

from ......utils import atomic_write
from .contracts import WiringStrategy, InjectionPlan
from .strategies import ALL_STRATEGIES
from .heuristics import EntrypointDiviner
from .surgeon import ASTSurgeon, DjangoSurgeon

if TYPE_CHECKING:
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class FrameworkFaculty:
    """
    [THE NERVOUS SYSTEM]
    Orchestrates framework detection and wiring via a pluggable neural network.
    """

    def __init__(self, logger: 'Scribe'):
        self.logger = logger
        self.strategies: List[WiringStrategy] = [cls(self) for cls in ALL_STRATEGIES]
        self.heuristics = EntrypointDiviner(self._read)

    def wire_components(self, file_path: Path, root: Path, tx: Optional["GnosticTransaction"]):
        content = self._read(file_path, root, tx)
        if not content: return

        for strategy in self.strategies:
            component_var = strategy.detect(content)
            if component_var:
                target_file = strategy.find_target(root, tx)

                # Prevent self-wiring
                if not target_file or target_file.resolve() == file_path.resolve():
                    continue

                target_content = self._read(target_file, root, tx)
                if not target_content: continue

                plan = strategy.forge_injection(file_path, component_var, target_content, root)

                if plan:
                    plan.target_file = target_file  # Bind the target
                    self._execute_wiring(plan, target_content, root, tx)
                    return

    def _execute_wiring(self, plan: InjectionPlan, content: str, root: Path, tx):
        try:
            tree = ast.parse(content)

            if plan.strategy_name == "Django":
                surgeon = DjangoSurgeon(plan.wiring_stmt)
            else:
                surgeon = ASTSurgeon(plan.import_stmt, plan.wiring_stmt, plan.anchor)

            new_tree = surgeon.visit(tree)
            ast.fix_missing_locations(new_tree)

            # Unparse (try astunparse for pre-3.9 compat if needed, else ast)
            try:
                import astunparse
                new_content = astunparse.unparse(new_tree)
            except ImportError:
                new_content = ast.unparse(new_tree)

            if new_content != content:
                self.logger.success(f"   -> Wiring {plan.strategy_name} Component into {plan.target_file.name}")
                self._write(plan.target_file, new_content, root, tx)

        except Exception as e:
            self.logger.warn(f"   -> Framework wiring failed for {plan.target_file.name}: {e}")

    def _read(self, path: Path, root: Path, tx) -> str:
        if tx:
            try:
                staged = tx.get_staging_path(path.relative_to(root))
                if staged.exists(): return staged.read_text('utf-8')
            except:
                pass
        if path.exists(): return path.read_text('utf-8')
        return ""

    def _write(self, path: Path, content: str, root: Path, tx):
        res = atomic_write(path, content, self.logger, root, transaction=tx, verbose=False)
        if tx and res.success:
            try:
                res.path = path.relative_to(root)
                tx.record(res)
            except:
                pass