# // scaffold/artisans/translocate_core/resolvers/javascript/inquisitor.py
# ------------------------------------------------------------------------

from typing import List
from tree_sitter import Node, QueryCursor
from .....inquisitor.sanctum.diagnostics.javascript import JavaScriptInquisitor
from .....logger import Scribe
from .contracts import JSDetectedImport

Logger = Scribe("JSInquisitor")


class JSInquisitorEngine:
    """
    Perceives imports in ES6 (import) and CommonJS (require).
    """

    # Matches: import x from 'y'; export x from 'y'; require('y'); import('y')
    IMPORT_QUERY = """
    (import_statement source: (string) @src) @import
    (export_statement source: (string) @src) @export
    (call_expression
      function: (identifier) @func
      arguments: (arguments (string) @src)
      (#match? @func "^(require|import)$")
    ) @dynamic
    """

    @classmethod
    def scan_content(cls, content: str) -> List[JSDetectedImport]:
        parser = JavaScriptInquisitor.get_parser()
        if not parser: return []

        tree = parser.parse(bytes(content, "utf8"))
        query = parser.language.query(cls.IMPORT_QUERY)

        # Determine cursor/captures method (compatibility shim)
        captures = []
        if hasattr(query, 'captures'):
            captures = query.captures(tree.root_node)
        else:
            cursor = QueryCursor(query)
            captures = cursor.captures(tree.root_node)

        results = []

        # We need to extract the string node which is usually @src
        # captures is [(Node, 'name')]

        for node, capture_name in captures:
            if capture_name == 'src':
                # node.text is b"'./path'" or b'"./path"'
                raw_text = node.text.decode('utf-8')
                quote = raw_text[0]
                specifier = raw_text[1:-1]

                # Determine line
                line = node.start_point[0] + 1

                # Dynamic check
                is_dynamic = (node.parent.parent.type == 'call_expression')

                results.append(JSDetectedImport(
                    line_num=line,
                    quote_style=quote,
                    specifier=specifier,
                    start_byte=node.start_byte,
                    end_byte=node.end_byte,
                    is_dynamic=is_dynamic
                ))

        return results