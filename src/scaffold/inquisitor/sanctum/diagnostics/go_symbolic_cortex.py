# === [scaffold/inquisitor/sanctum/diagnostics/go_symbolic_cortex.py] - SECTION 1 of 1: Full File ===
from typing import Dict, Any, List
from tree_sitter import Tree, Node, QueryCursor, Language


class GoSymbolicCortex:
    """
    =================================================================================
    == THE GOPHER'S EYE (GO GNOSIS)                                                ==
    =================================================================================
    Parses Go structs, interfaces, and functions.
    Handles method receivers to link methods to structs.
    """

    QUERY_DEFS = """
    (function_declaration name: (identifier) @name) @function
    (method_declaration name: (field_identifier) @name) @method
    (type_declaration 
      (type_spec 
        name: (type_identifier) @name 
        type: [(struct_type) (interface_type)]
      )
    ) @class
    """

    QUERY_USAGES = """
    (identifier) @usage
    (type_identifier) @type_usage
    (field_identifier) @field_usage
    (package_identifier) @pkg_usage
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
            if name == "function":
                functions.append(self._mine_structure(node, "function"))
            elif name == "method":
                # Go methods are functions attached to structs
                functions.append(self._mine_structure(node, "method"))
            elif name == "class":
                classes.append(self._mine_structure(node, "struct"))

        return {"functions": functions, "classes": classes}

    def _mine_structure(self, node: Node, type_: str) -> Dict[str, Any]:
        name_node = node.child_by_field_name("name")
        name = name_node.text.decode('utf-8') if name_node else "anonymous"

        body_node = node.child_by_field_name("body")
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

        keywords = {'func', 'var', 'type', 'struct', 'interface', 'package', 'import', 'return', 'if', 'else', 'for',
                    'range', 'go', 'select', 'case', 'defer', 'map', 'chan', 'make', 'len', 'append', 'nil', 'true',
                    'false', 'error', 'int', 'string', 'bool', 'byte'}

        for cap_node, _ in captures:
            text = cap_node.text.decode('utf-8')
            if text not in keywords:
                usages.add(text)

        return {"local": [], "external": list(usages)}