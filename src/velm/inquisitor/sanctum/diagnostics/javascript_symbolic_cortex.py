# === [scaffold/inquisitor/sanctum/diagnostics/javascript_symbolic_cortex.py] - SECTION 1 of 1: Full File ===
from typing import Dict, Any, List
from tree_sitter import Tree, Node, QueryCursor, Language


class JavaScriptSymbolicCortex:
    """
    =================================================================================
    == THE SCRIPT SEER (JS/JSX GNOSIS)                                             ==
    =================================================================================
    Handles function declarations, classes, and variable-bound arrow functions.
    """

    QUERY_DEFS = """
    (function_declaration name: (identifier) @name) @function
    (class_declaration name: (identifier) @name) @class
    (variable_declarator 
        name: (identifier) @name 
        value: [(arrow_function) (function_expression)]
    ) @var_func
    """

    QUERY_USAGES = """
    (identifier) @usage
    """

    def __init__(self, language: Language):
        self.language = language
        # [THE FIX] The Rite of Explicit Compilation
        # We compile the maps (Queries) once.
        self.q_defs = Query(self.language, self.QUERY_DEFS)
        self.q_imports = Query(self.language, self.QUERY_IMPORTS)
        self.q_refs = Query(self.language, self.QUERY_REFS)
        self.q_complexity = Query(self.language, self.QUERY_COMPLEXITY)

    def inquire(self, tree: Tree) -> Dict[str, Any]:
        root = tree.root_node
        functions = []
        classes = []

        cursor = QueryCursor(self.q_defs)
        captures = cursor.captures(root)

        for node, name in captures:
            if name in ["function", "var_func"]:
                functions.append(self._mine_structure(node, "function"))
            elif name == "class":
                classes.append(self._mine_structure(node, "class"))

        return {"functions": functions, "classes": classes}

    def _mine_structure(self, node: Node, type_: str) -> Dict[str, Any]:
        name_node = node.child_by_field_name("name")
        name = name_node.text.decode('utf-8') if name_node else "anonymous"

        body_node = node.child_by_field_name("body") or node.child_by_field_name("value")
        dependencies = self._mine_causal_bonds(body_node) if body_node else {"local": [], "external": []}

        return {
            "name": name,
            "type": type_,
            "start_point": node.start_point,
            "end_point": node.end_point,
            "line_count": node.end_point[0] - node.start_point[0] + 1,
            "dependencies": dependencies
        }

    def _mine_causal_bonds(self, node: Node) -> Dict[str, List[str]]:
        if not node: return {"local": [], "external": []}
        usages = set()
        cursor = QueryCursor(self.q_usages)
        captures = cursor.captures(node)

        keywords = {'function', 'class', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'import',
                    'from', 'export', 'default', 'try', 'catch', 'this', 'super', 'new', 'null', 'undefined', 'true',
                    'false', 'console', 'window', 'document'}

        for cap_node, _ in captures:
            text = cap_node.text.decode('utf-8')
            if text not in keywords:
                usages.add(text)

        return {"local": [], "external": list(usages)}