# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/javascript_strategy.py
# -------------------------------------------------------------------------------------------------------

from .node_strategy import NodeStructureStrategy

class JavaScriptStructureStrategy(NodeStructureStrategy):
    """
    The Guardian of the JavaScript Cosmos.
    Manages `index.js` barrels.
    """
    def __init__(self):
        super().__init__("JavaScript", "index.js")