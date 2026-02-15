# Path: scaffold/artisans/translocate_core/resolvers/python/inquisitor.py
# -----------------------------------------------------------------------
from typing import List, Tuple, Dict, Any
try:
    # --- MOVEMENT I: NATIVE COMMUNION ---
    from tree_sitter import Node, QueryCursor
except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION ---
    # If in the WASM Stratum, the 'tree_sitter' module is provided by the Simulacrum.
    import sys
    if "tree_sitter" in sys.modules:
        ts_proxy = sys.modules["tree_sitter"]
        Node = ts_proxy.Node
        QueryCursor = ts_proxy.QueryCursor
    else:
        # Final Fallback: The Gaze is Blind
        class Node: pass
        class QueryCursor: pass

from .....inquisitor.sanctum.diagnostics.python import PythonInquisitor
from .....logger import Scribe
from .contracts import DetectedImport

Logger = Scribe("PythonInquisitor")


class PythonInquisitorEngine:
    """
    The Gnostic Eye. It parses raw text into Structured Import Data.
    """

    IMPORT_QUERY = """
    (import_statement
        name: (dotted_name) @full_import
    ) @import_node

    (import_from_statement
        (relative_import)? @dots
        module_name: (_)? @module
        name: [
            (dotted_name) @name
            (aliased_import
                name: (dotted_name) @name
                alias: (identifier) @alias
            )
        ]
    ) @import_node

    (import_from_statement
        (wildcard_import) @wildcard
    ) @import_node
    """

    @classmethod
    def scan_content(cls, content: str) -> List[DetectedImport]:
        parser = PythonInquisitor.get_parser()
        if not parser:
            return []

        try:
            tree = parser.parse(bytes(content, "utf8"))
            language = parser.language
            query = language.query(cls.IMPORT_QUERY)

            raw_captures = None
            if hasattr(query, 'captures'):
                try:
                    raw_captures = query.captures(tree.root_node)
                except TypeError:
                    raw_captures = query.captures(tree.root_node, start_point=(0, 0), end_point=(100000, 0))
            else:
                cursor = QueryCursor(query)
                raw_captures = cursor.captures(tree.root_node)

            normalized_captures: List[Tuple[Node, str]] = []
            if isinstance(raw_captures, dict):
                for name, nodes in raw_captures.items():
                    if not isinstance(nodes, list): nodes = [nodes]
                    for node in nodes:
                        normalized_captures.append((node, name))
            elif isinstance(raw_captures, list):
                for item in raw_captures:
                    if isinstance(item, (tuple, list)) and len(item) >= 2:
                        normalized_captures.append((item[0], item[1]))
            else:
                return []

            grouped: Dict[int, Dict[str, Any]] = {}

            for node, name in normalized_captures:
                if not hasattr(node, 'type'): continue

                parent = node
                while parent.type not in ('import_statement', 'import_from_statement'):
                    parent = parent.parent
                    if not parent: break
                if not parent: continue

                stmt_id = parent.id
                if stmt_id not in grouped:
                    grouped[stmt_id] = {
                        "line": parent.start_point[0] + 1,
                        "names": [],
                        "module": None,
                        "level": 0,
                        "wildcard": False
                    }

                if name == "module":
                    grouped[stmt_id]["module"] = node.text.decode('utf-8')
                elif name == "dots":
                    dots_bytes = node.text
                    dots_text = dots_bytes.decode('utf-8')

                    # [THE FIX] Count only LEADING dots.
                    # This prevents counting dots in the module part if captured greedily.
                    level = len(dots_text) - len(dots_text.lstrip('.'))

                    if level > 0:
                        # Logger.info(f"[INQ] L{grouped[stmt_id]['line']} Dots: '{dots_text}' -> Level {level}")
                        pass

                    grouped[stmt_id]["level"] = level
                elif name == "wildcard":
                    grouped[stmt_id]["wildcard"] = True
                elif name == "name":
                    grouped[stmt_id]["names"].append(node.text.decode('utf-8'))
                elif name == "full_import":
                    grouped[stmt_id]["names"].append(node.text.decode('utf-8'))

            results = []
            for g in grouped.values():
                names_list = g["names"]
                if not names_list and g["wildcard"]:
                    names_list = ["*"]

                for name_str in names_list:
                    results.append(DetectedImport(
                        line_num=g["line"],
                        module=g["module"],
                        name=name_str,
                        alias=None,
                        level=g["level"],
                        is_wildcard=g["wildcard"]
                    ))

            return results

        except Exception as e:
            Logger.error(f"Parsing Paradox in PythonInquisitor: {e}")
            return []