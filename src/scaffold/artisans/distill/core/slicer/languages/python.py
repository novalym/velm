# Path: scaffold/artisans/distill/core/slicer/languages/python.py
# ---------------------------------------------------------------

import ast
from typing import List, Set, Optional
from .base import LanguageAdapter
from ..contracts import SymbolNode


class PythonAdapter(LanguageAdapter):
    """
    The Serpent's Tongue. Uses `ast` (stdlib) for perfect Python understanding.
    """

    def parse(self, content: str) -> List[SymbolNode]:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        nodes = []
        self._visit(tree, nodes, None)
        return nodes

    def _visit(self, ast_node, nodes_list: List[SymbolNode], parent_name: Optional[str]):
        """Recursive AST walker."""
        for child in ast.iter_fields(ast_node):
            # child is (name, value)
            value = child[1]
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self._process_node(item, nodes_list, parent_name)
            elif isinstance(value, ast.AST):
                self._process_node(value, nodes_list, parent_name)

    def _process_node(self, node, nodes_list, parent_name):
        symbol = None

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            fqn = f"{parent_name}.{name}" if parent_name else name
            symbol = SymbolNode(
                name=name,  # Store simple name for matching
                type="function",
                start_line=node.lineno,
                end_line=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                start_byte=-1, end_byte=-1,  # AST doesn't give bytes easily, we use lines
                parent_name=parent_name,
                dependencies=self._extract_deps_from_ast(node)
            )
        elif isinstance(node, ast.ClassDef):
            name = node.name
            fqn = f"{parent_name}.{name}" if parent_name else name
            symbol = SymbolNode(
                name=name,
                type="class",
                start_line=node.lineno,
                end_line=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                start_byte=-1, end_byte=-1,
                parent_name=parent_name,
                dependencies=set()  # Class deps (base classes) handled separately ideally
            )

        if symbol:
            nodes_list.append(symbol)
            # Recurse with new parent
            # For class, the parent name becomes the class name
            new_parent = symbol.name
            self._visit(node, nodes_list, new_parent)
        else:
            # Recurse without changing parent
            self._visit(node, nodes_list, parent_name)

    def _extract_deps_from_ast(self, node: ast.AST) -> Set[str]:
        """Finds all Name nodes used in the function body."""
        deps = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.add(child.id)
            # Handle self.method() calls?
            # If child is Attribute (value=Name(id='self'), attr='method') -> 'method'
        return deps

    def extract_dependencies(self, content: str, node: SymbolNode) -> Set[str]:
        # Handled during parse for Python
        return node.dependencies