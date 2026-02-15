# === [scaffold/inquisitor/sanctum/diagnostics/rust_symbolic_cortex.py] - SECTION 1 of 1: Full File ===
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


class RustSymbolicCortex:
    """
    =================================================================================
    == THE IRON MIND (RUST GNOSIS)                                                 ==
    =================================================================================
    Perceives Structs, Enums, Traits, and Functions.
    Distinguishes between 'use' (imports) and 'call' (usages).
    """

    QUERY_DEFS = """
    (function_item name: (identifier) @name) @function
    (struct_item name: (type_identifier) @name) @class
    (enum_item name: (type_identifier) @name) @class
    (trait_item name: (type_identifier) @name) @class
    (impl_item 
      type: (type_identifier) @name 
      body: (declaration_list) @body
    ) @impl
    """

    # We capture all potential symbol usages
    QUERY_USAGES = """
    (type_identifier) @type_usage
    (identifier) @usage
    (scoped_identifier) @path_usage
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
            elif name == "impl":
                # Impl blocks define methods. We extract methods as functions
                # but mark them as methods in metadata if needed.
                # For graph purity, we dive into the body.
                body = node.child_by_field_name("body")
                if body:
                    # Recursive mining of the impl block
                    # In a full implementation, we'd attach these to the class.
                    # Here we flatten them into functions for dependency tracing.
                    sub_cursor = QueryCursor(self.q_defs)
                    sub_captures = sub_cursor.captures(body)
                    for sub_node, sub_name in sub_captures:
                        if sub_name == "function":
                            functions.append(self._mine_structure(sub_node, "method"))

        return {"functions": functions, "classes": classes}

    def _mine_structure(self, node: Node, type_: str) -> Dict[str, Any]:
        name_node = node.child_by_field_name("name")
        name = name_node.text.decode('utf-8') if name_node else "anonymous"

        # Body is usually the last child for functions
        body_node = node.child_by_field_name("body")

        # Heuristic for args to exclude from external deps
        params_node = node.child_by_field_name("parameters")
        local_args = self._extract_args(params_node)

        dependencies = self._mine_causal_bonds(body_node, local_args) if body_node else {"local": [], "external": []}

        return {
            "name": name,
            "type": type_,
            "start_point": node.start_point,
            "end_point": node.end_point,
            "line_count": node.end_point[0] - node.start_point[0] + 1,
            "dependencies": dependencies
        }

    def _extract_args(self, params_node: Node) -> List[str]:
        if not params_node: return []
        args = []
        # Rust args: (x: i32, y: Type)
        # We want 'x', 'y'.
        # Tree-sitter structure varies, simple identifier scan usually works.
        return []  # Simplified for V1

    def _mine_causal_bonds(self, node: Node, local_scope: List[str]) -> Dict[str, List[str]]:
        if not node: return {"local": [], "external": []}

        usages = set()
        cursor = QueryCursor(self.q_usages)
        captures = cursor.captures(node)

        keywords = {'fn', 'pub', 'use', 'mod', 'crate', 'self', 'super', 'let', 'mut', 'return', 'impl', 'struct',
                    'enum', 'match', 'if', 'else', 'for', 'while', 'loop'}

        for cap_node, _ in captures:
            text = cap_node.text.decode('utf-8')
            if text not in keywords and text not in local_scope:
                usages.add(text)

        return {"local": [], "external": list(usages)}