# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/testing/analyzer.py
# --------------------------------------------------------------------------------------------------------------------

import ast
from pathlib import Path
from typing import List, Optional
from .contracts import TestableUnit, ArgumentGnosis, TestFileBlueprint
from ......logger import Scribe

Logger = Scribe("TestAnatomist")

class SourceCodeAnatomist:
    """
    =============================================================================
    == THE SOURCE CODE ANATOMIST (V-Ω-AST-INTROSPECTOR)                        ==
    =============================================================================
    Performs deep surgery on Python source code to extract testable metadata.
    """

    def analyze(self, source_path: Path, content: str, root: Path) -> Optional[TestFileBlueprint]:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            Logger.warn(f"Syntax Heresy in '{source_path.name}'. Test generation will be basic.")
            return None

        units: List[TestableUnit] = []
        has_classes = False

        # 1. Harvest Top-Level Functions
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if self._is_private(node.name): continue
                units.append(self._analyze_function(node))

            # 2. Harvest Classes
            elif isinstance(node, ast.ClassDef):
                if self._is_private(node.name): continue
                has_classes = True
                # Analyze methods
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if self._is_private(item.name) and item.name != "__init__": continue
                        unit = self._analyze_function(item)
                        unit.is_method = True
                        unit.parent_class = node.name
                        units.append(unit)

        # 3. Determine Import Path
        module_path = self._resolve_module_path(source_path, root)

        return TestFileBlueprint(
            source_module=module_path,
            units=units,
            has_classes=has_classes
        )

    def _analyze_function(self, node: ast.FunctionDef) -> TestableUnit:
        args = []
        for arg in node.args.args:
            if arg.arg == 'self': continue
            type_hint = self._get_annotation(arg.annotation)
            args.append(ArgumentGnosis(name=arg.arg, type_hint=type_hint))

        return TestableUnit(
            name=node.name,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            args=args,
            return_type=self._get_annotation(node.returns),
            docstring=ast.get_docstring(node),
            complexity=len(list(ast.walk(node))) # Heuristic complexity
        )

    def _get_annotation(self, node) -> Optional[str]:
        if node is None: return None
        try:
            return ast.unparse(node)
        except:
            return None

    def _is_private(self, name: str) -> bool:
        return name.startswith('_') and name != '__init__'

    def _resolve_module_path(self, path: Path, root: Path) -> str:
        try:
            # Enforce POSIX logic for dot-notation
            rel = path.relative_to(root).with_suffix('').as_posix()
            return rel.replace('/', '.')
        except ValueError:
            return path.stem