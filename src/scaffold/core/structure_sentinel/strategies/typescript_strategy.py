# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/typescript_strategy.py
# -------------------------------------------------------------------------------------------------------

from .node_strategy import NodeStructureStrategy

class TypeScriptStructureStrategy(NodeStructureStrategy):
    """
    The Guardian of the TypeScript Cosmos.
    Manages `index.ts` barrels.
    """
    def __init__(self):
        super().__init__("TypeScript", "index.ts")