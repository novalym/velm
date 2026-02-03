# Path: inquisitor/sanctum/diagnostics/python.py
# ----------------------------------------------

from typing import Dict, Any
from .python_symbolic_cortex import PythonSymbolicCortex
from ..engine import BaseInquisitor
from ....logger import Scribe

Logger = Scribe("PythonInquisitor")


class PythonInquisitor(BaseInquisitor):
    """
    =================================================================================
    == THE GNOSTIC INQUISITOR (V-Ω-CORTEX-POWERED)                                 ==
    =================================================================================
    LIF: 10,000,000,000,000

    The High Priest of Python Analysis. It delegates the surgical dissection of the
    AST to the `PythonSymbolicCortex`.
    """
    LANGUAGE_NAME = 'python'
    GRAMMAR_PACKAGE = 'tree_sitter_python'
    QUERIES = {}  # Handled internally by Cortex now

    def perform_inquisition(self, content: str) -> Dict[str, Any]:
        """
        The Rite of Parsing.
        """
        parser = self.get_parser()
        if not parser:
            return {"error": "Parser not initialized"}

        try:
            tree = parser.parse(bytes(content, "utf8"))

            # Summon the Cortex for this specific analysis
            cortex = PythonSymbolicCortex(parser.language)

            # The Cortex performs the deep gaze
            dossier = cortex.inquire(tree)

            return dossier

        except Exception as e:
            Logger.error(f"Inquisition failed: {e}")
            return {"error": str(e)}