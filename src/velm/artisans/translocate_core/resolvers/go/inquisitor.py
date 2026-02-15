# // scaffold/artisans/translocate_core/resolvers/go/inquisitor.py
import sys
from typing import List
try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # We attempt to speak with the native C-extension.
    from tree_sitter import QueryCursor

    TREE_SITTER_AVAILABLE = True
except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native tongue is absent, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        QueryCursor = _ts.QueryCursor
        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If no soul is manifest in any realm, we forge hollow vessels.
        TREE_SITTER_AVAILABLE = False

        # We forge a 'Hollow' type to allow the CppInquisitorEngine
        # to be imported without crashing.
        QueryCursor = type("HollowQueryCursor", (object,), {})

from .....inquisitor.sanctum.diagnostics.go import GoInquisitor
from .contracts import GoDetectedImport


class GoInquisitorEngine:
    QUERY = """
    (import_spec path: (interpreted_string_literal) @path) @import
    """

    @staticmethod
    def scan(content: str) -> List[GoDetectedImport]:
        parser = GoInquisitor.get_parser()
        if not parser: return []

        tree = parser.parse(bytes(content, "utf8"))
        query = parser.language.query(GoInquisitorEngine.QUERY)
        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)

        results = []
        for node, name in captures:
            if name == "path":
                # Node text includes quotes: "example.com/foo"
                raw = node.text.decode("utf-8")
                path = raw.strip('"')
                results.append(GoDetectedImport(
                    line_num=node.start_point[0] + 1,
                    import_path=path,
                    alias=None,  # Tree-sitter query can be expanded for aliases
                    start_byte=node.start_byte,
                    end_byte=node.end_byte
                ))
        return results