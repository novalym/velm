# // scaffold/artisans/translocate_core/resolvers/go/inquisitor.py
from typing import List
from tree_sitter import QueryCursor
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