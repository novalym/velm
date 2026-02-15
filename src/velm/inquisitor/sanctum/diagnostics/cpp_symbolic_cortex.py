# === [scaffold/inquisitor/sanctum/diagnostics/cpp_symbolic_cortex.py] - SECTION 1 of 1: Full File ===
import sys
from typing import Dict, Any, List

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # Attempting to speak with the native C-matter (Local/Titan Node).
    from tree_sitter import Tree, Node, QueryCursor, Language

    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native library is unmanifest, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum's ignition.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]

        # [ASCENSION]: We extract the Diamond souls from the Proxy
        # These classes are telepathically linked to the JS WASM engine.
        Tree = _ts.Tree
        Node = _ts.Node
        QueryCursor = _ts.QueryCursor
        Language = _ts.Language

        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If the Mind is cold in all realms, we forge hollow vessels.
        # This prevents 'AttributeError' and 'TypeError' during registration.
        TREE_SITTER_AVAILABLE = False

        # [ASCENSION 5]: Hollow Type Generation (The Sarcophagus)
        # We create specific type identities rather than generic objects.
        Tree = type("HollowTree", (object,), {})
        Node = type("HollowNode", (object,), {})
        QueryCursor = type("HollowQueryCursor", (object,), {})
        Language = type("HollowLanguage", (object,), {})


class CppSymbolicCortex:
    """
    =================================================================================
    == THE DEEP METAL (C++ GNOSIS)                                                 ==
    =================================================================================
    """

    QUERY_DEFS = """
    (function_definition
      declarator: (function_declarator declarator: (identifier) @name)
    ) @function

    (class_specifier name: (type_identifier) @name) @class
    (struct_specifier name: (type_identifier) @name) @class
    """

    QUERY_USAGES = """
    (identifier) @usage
    (type_identifier) @type_usage
    (field_identifier) @field_usage
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
            elif name == "class":
                classes.append(self._mine_structure(node, "class"))

        return {"functions": functions, "classes": classes}

    def _mine_structure(self, node: Node, type_: str) -> Dict[str, Any]:
        # C++ naming is complex (namespaces, pointers). We try simple extraction first.
        # Tree-sitter structure varies significantly.
        name = "unknown"
        if type_ == "function":
            decl = node.child_by_field_name("declarator")
            # Recursively find identifier
            while decl:
                if decl.type == 'identifier':
                    name = decl.text.decode('utf-8')
                    break
                decl = decl.child_by_field_name("declarator")
        else:
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

        keywords = {'int', 'char', 'float', 'double', 'void', 'bool', 'if', 'else', 'for', 'while', 'return', 'class',
                    'struct', 'public', 'private', 'protected', 'virtual', 'override', 'new', 'delete', 'nullptr',
                    'true', 'false', 'std', 'vector', 'string', 'cout', 'cin', 'endl'}

        for cap_node, _ in captures:
            text = cap_node.text.decode('utf-8')
            if text not in keywords:
                usages.add(text)

        return {"local": [], "external": list(usages)}