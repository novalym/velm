import ast
from typing import Tuple, List, Any
from .base import BaseVowHandler


class PythonVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE SEMANTIC INQUISITOR (V-Ω-AST-ANALYSIS)                              ==
    =============================================================================
    Judges the soul of Python scriptures.
    """

    def _get_ast(self, path: str) -> Tuple[bool, Any, str]:
        """Internal rite to parse a python file safely."""
        target = self._resolve(path)
        if not target.is_file(): return False, None, f"'{path}' is void."
        try:
            content = target.read_text(encoding='utf-8')
            tree = ast.parse(content)
            return True, tree, "Parsed."
        except SyntaxError as e:
            return False, None, f"Syntax Heresy in '{path}': {e}"
        except Exception as e:
            return False, None, f"Unreadable: {e}"

    def _vow_python_valid(self, path: str) -> Tuple[bool, str]:
        """Asserts that a file contains valid Python syntax."""
        success, _, msg = self._get_ast(path)
        return success, msg

    def _vow_python_imports(self, path: str, module_name: str) -> Tuple[bool, str]:
        """Asserts that a script imports a specific module."""
        success, tree, msg = self._get_ast(path)
        if not success: return False, msg

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == module_name: return True, f"Imports '{module_name}'."
            elif isinstance(node, ast.ImportFrom):
                if node.module == module_name: return True, f"Imports from '{module_name}'."

        return False, f"Scripture does not import '{module_name}'."

    def _vow_python_defines_class(self, path: str, class_name: str) -> Tuple[bool, str]:
        """Asserts that a specific Class is defined."""
        success, tree, msg = self._get_ast(path)
        if not success: return False, msg

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return True, f"Class '{class_name}' is defined."
        return False, f"Class '{class_name}' not found."

    def _vow_python_defines_function(self, path: str, func_name: str) -> Tuple[bool, str]:
        """Asserts that a specific Function is defined."""
        success, tree, msg = self._get_ast(path)
        if not success: return False, msg

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                return True, f"Function '{func_name}' is defined."
        return False, f"Function '{func_name}' not found."

    def _vow_python_complexity_lt(self, path: str, limit: str) -> Tuple[bool, str]:
        """
        Asserts the Cyclomatic Complexity (heuristic) is below a threshold.
        Counts decision points: if, for, while, except, assert.
        """
        success, tree, msg = self._get_ast(path)
        if not success: return False, msg

        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.Assert)):
                complexity += 1

        limit_int = int(limit)
        return complexity < limit_int, f"Complexity {complexity} < {limit_int}."
