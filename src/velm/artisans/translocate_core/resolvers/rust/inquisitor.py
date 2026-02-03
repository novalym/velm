# // scaffold/artisans/translocate_core/resolvers/rust/inquisitor.py
# ------------------------------------------------------------------

from typing import List
from tree_sitter import QueryCursor
from .....inquisitor.sanctum.diagnostics.go import GoInquisitor  # Reuse base if needed, but Rust has its own
# We need to import the Rust Inquisitor from diagnostics if it exists, or use BaseInquisitor pattern
# Assuming a RustInquisitor class exists in diagnostics or we use BaseInquisitor logic here.
from .....inquisitor.core import is_grammar_available, LANGUAGES
from .....logger import Scribe
from .contracts import RustDetectedUse

Logger = Scribe("RustInquisitor")


class RustInquisitorEngine:
    # Query to capture the path part of a use declaration
    # use crate::foo::bar; -> crate::foo::bar
    QUERY = """
    (use_declaration
      argument: [
        (scoped_identifier) @path
        (identifier) @path
      ]
    )
    """

    @classmethod
    def scan(cls, content: str) -> List[RustDetectedUse]:
        # Direct loading logic for autonomy
        if not is_grammar_available("tree_sitter_rust", "rust"):
            Logger.warn("Rust Grammar missing.")
            return []

        parser = None
        # ... (Implementation similar to others: instantiate parser with rust language)
        # For brevity, assuming access to the language object:
        lang = LANGUAGES["rust"]
        from tree_sitter import Parser
        parser = Parser()
        parser.set_language(lang)

        tree = parser.parse(bytes(content, "utf8"))
        query = lang.query(cls.QUERY)
        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)

        results = []
        for node, name in captures:
            if name == "path":
                results.append(RustDetectedUse(
                    line_num=node.start_point[0] + 1,
                    path=node.text.decode('utf-8'),
                    start_byte=node.start_byte,
                    end_byte=node.end_byte
                ))
        return results