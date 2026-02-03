from pathlib import Path
from typing import Dict

from .....contracts.heresy_contracts import ArtisanHeresy
from .....inquisitor import get_treesitter_gnosis
from .....logger import Scribe
from .contracts import SemanticTarget
from .strategies import PythonInsertionStrategy, CStyleInsertionStrategy
import re

Logger = Scribe("SemanticRouter")


class SemanticRouter:
    """
    [FACULTY 2 & 6] The Semantic Router.
    Dispatches the insertion based on language.
    """

    PYTHONIC = {'.py', '.yaml', '.yml'}
    C_STYLE = {'.ts', '.tsx', '.js', '.jsx', '.go', '.rs', '.java', '.c', '.cpp', '.cs'}

    @staticmethod
    def dispatch(original: str, fragment: str, selector: Dict[str, str], file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        if suffix not in SemanticRouter.PYTHONIC and suffix not in SemanticRouter.C_STYLE:
            raise ArtisanHeresy(f"Semantic Insertion not supported for '{suffix}'.")

        # 1. Gnostic Inquest
        dossier = get_treesitter_gnosis(file_path, original)
        if "error" in dossier:
            raise ArtisanHeresy(f"Could not parse code: {dossier['error']}")

        # 2. Locate Target
        target = SemanticRouter._locate_target(dossier, selector, file_path.name)

        # 3. Idempotency Check
        if fragment.strip() in original:
            Logger.verbose("Semantic Insertion skipped: Gnosis already present.")
            return original

        lines = original.splitlines(keepends=True)
        mode = selector.get('type', 'inside')

        # 4. Dispatch Strategy
        if suffix in SemanticRouter.PYTHONIC:
            return PythonInsertionStrategy.insert(lines, target, fragment, mode)
        else:
            return CStyleInsertionStrategy.insert(lines, target, fragment, mode)

    @staticmethod
    def _locate_target(dossier: Dict, selector: Dict, filename: str) -> SemanticTarget:
        class_name = selector.get('class')
        func_name = selector.get('function')

        node = None
        node_type = "unknown"

        if class_name:
            classes = dossier.get('classes', [])
            node = next((c for c in classes if c['name'] == class_name), None)
            node_type = "class"
        elif func_name:
            funcs = dossier.get('functions', [])
            node = next((f for f in funcs if f['name'] == func_name), None)
            node_type = "function"

        if not node:
            raise ArtisanHeresy(f"Semantic target {node_type} not found in {filename}.")

        # Determine indentation
        # Tree-sitter gives start_point (row, col)
        start_row = node['start_point'][0]
        # We can't access lines here easily without passing content again,
        # but we can guess or require the Strategy to calculate it.
        # Actually, we pass 'lines' to the Strategy. We can just return the row index here.
        # Wait, we need base_indent for the strategy.
        # Let's return a SemanticTarget object that holds the indices.
        # The Strategy will read the line to get the indent string.

        # For 'base_indent', we need the content line.
        # We will let the Strategy calculate it from the line index to be precise.
        # We store an empty string here as placeholder or refactor.
        # REFACTOR: Let's pass just the indices.

        return SemanticTarget(
            name=node['name'],
            type=node_type,
            start_line=node['start_point'][0],
            end_line=node['end_point'][0],
            base_indent="",  # Strategy calculates this from lines[start_line]
            content_range=(node['start_byte'], node['end_byte'])
        )
