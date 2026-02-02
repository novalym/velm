# Path: scaffold/artisans/heal/healers/python_import_healer.py
# ------------------------------------------------------------

import ast
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

# --- The Divine Summons ---
from ..contracts import BaseHealer, HealingDiagnosis
from ....artisans.translocate_core.resolvers.python.surgeon import GnosticImportTransformer
from ....logger import Scribe

# --- JIT Summons for Standalone Healing ---
from ....inquisitor.python_inquisitor import PythonCodeInquisitor
from ....artisans.translocate_core.resolvers import PythonImportResolver

Logger = Scribe("PythonImportHealer")


class PythonImportHealer(BaseHealer):
    """
    =================================================================================
    == THE PYTHONIC PHYSICIAN (V-Ω-SELF-SUFFICIENT-ULTIMA)                         ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Healer of Import Paths.
    It acts as an adapter between the generic `HealArtisan` interface and the
    specialized `PythonImportResolver` engine.

    ### THE ASCENDED FACULTIES:
    1.  **The Adapter Pattern:** Maps `HealingEdict` (Translocation) to `HealingDiagnosis` (Repair).
    2.  **The JIT Context Forge:** If called without a resolver (e.g., standalone repair),
        it autonomously scans the project to build a symbol map, allowing it to heal
        broken imports even without a move operation.
    3.  **The AST Surgeon:** Wields the `GnosticImportTransformer` to perform precise,
        node-based surgery on the import statements.
    4.  **The Unbreakable Ward:** Wraps AST operations in safety blocks to prevent
        corrupting the file if syntax is already broken.
    """

    def __init__(self, project_root: Path, context: Dict[str, Any]):
        super().__init__(project_root, context)
        # We attempt to retrieve the resolver from the shared context (from Translocate/Conform).
        # If missing, we stay our hand until `diagnose` is called.
        self.resolver: Optional[PythonImportResolver] = context.get('python_resolver')

    @property
    def name(self) -> str:
        return "ImportAligner"

    @property
    def supported_extensions(self) -> List[str]:
        return ['.py']

    def _awaken_resolver(self):
        """
        [THE RITE OF SELF-RELIANCE]
        If the Healer was summoned without a map (standalone repair),
        it must forge one now.
        """
        if self.resolver:
            return

        Logger.info("Healer lacks a map. Initiating JIT Project Scan for symbols...")

        # 1. Summon the Inquisitor
        inquisitor = PythonCodeInquisitor(self.project_root)
        inquisitor.inquire_project()

        if not inquisitor.symbol_map:
            Logger.warn("The Inquisitor found no symbols. The Healer is blind.")
            return

        # 2. Forge the Resolver
        # For standalone repair, the translocation map is an identity map (no moves).
        identity_map = {}
        self.resolver = PythonImportResolver(self.project_root, inquisitor.symbol_map, identity_map)
        Logger.success(f"Healer equipped with {len(inquisitor.symbol_map)} symbols.")

    def diagnose(self, file_path: Path, content: str) -> List[HealingDiagnosis]:
        # 1. Ensure we have the tools
        self._awaken_resolver()
        if not self.resolver:
            return []

            # 2. Delegate to the Resolver's Logic
        # The resolver returns a list of serialized HealingEdicts (dicts)
        plan = self.resolver.diagnose_healing_needs(file_path)

        diagnoses = []
        for item in plan:
            # We assume 'item' is a dict representation of HealingEdict
            symbol = item.get('symbol_name', 'Unknown')
            old_mod = item.get('original_module', 'Unknown')
            new_mod = item.get('new_module_path', 'Unknown')

            diagnoses.append(HealingDiagnosis(
                file_path=file_path,
                healer_name=self.name,
                description=f"Import Mismatch: '{symbol}' is imported from '{old_mod}', but dwells in '{new_mod}'.",
                metadata={"plan_item": item},  # Carry the full edict for the cure
                severity="CRITICAL"
            ))
        return diagnoses

    def heal(self, file_path: Path, content: str, diagnoses: List[HealingDiagnosis]) -> Tuple[str, bool]:
        """
        The Rite of Surgery.
        Applies the collected diagnoses to the file content via AST transformation.
        """
        if not diagnoses:
            return content, False

        # Extract the specific plan items (HealingEdicts) from the generic diagnoses
        full_plan = [d.metadata["plan_item"] for d in diagnoses]

        # Import local contract for hydration
        from ....artisans.translocate_core.resolvers.python.contracts import HealingEdict

        try:
            # 1. Parse
            tree = ast.parse(content)

            # 2. Rehydrate Edicts
            edicts = [HealingEdict(**d) for d in full_plan]

            # 3. Transform
            transformer = GnosticImportTransformer(plan=edicts)
            new_tree = transformer.visit(tree)

            # 4. Fix Locations (Required for unparse)
            ast.fix_missing_locations(new_tree)

            # 5. Unparse (The Gnostic Formatter)
            # Note: ast.unparse (Python 3.9+) does not preserve comments or exact formatting.
            # This is a known trade-off for the purity of AST manipulation.
            # A future ascension could use LibCST for full fidelity.
            new_content = ast.unparse(new_tree)

            return new_content, True

        except SyntaxError:
            Logger.error(f"Syntax Heresy in '{file_path.name}'. Surgery aborted to prevent corruption.")
            return content, False
        except Exception as e:
            Logger.error(f"Surgical Paradox in '{file_path.name}': {e}", exc_info=True)
            return content, False

