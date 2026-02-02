# // scaffold/artisans/translocate_core/resolvers/java/inquisitor.py
# ------------------------------------------------------------------

from typing import List
from tree_sitter import QueryCursor
from .....inquisitor.core import is_grammar_available, LANGUAGES
from .....logger import Scribe
from .contracts import JavaDetectedImport

Logger = Scribe("JavaInquisitor")


class JavaInquisitorEngine:
    """
    The Eye of Gosling. Perceives imports in Java scriptures.
    """

    # Matches: import com.example.Foo; or import static com.example.Foo.bar;
    QUERY = """
    (import_declaration
        (scoped_identifier) @path
    ) @import
    """

    @classmethod
    def scan(cls, content: str) -> List[JavaDetectedImport]:
        if not is_grammar_available("tree_sitter_java", "java"):
            Logger.warn("Java Grammar missing. The Gaze is blind.")
            return []

        lang = LANGUAGES["java"]
        # Use the universal parser setup from the core if possible, but for autonomy:
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
                # Check for 'static' keyword in siblings/children if needed,
                # but for path resolution, we just need the text.
                raw_text = node.text.decode('utf-8')

                # Check if parent has 'static' modifier?
                # Tree-sitter structure: (import_declaration "import" "static"? (scoped_identifier))
                is_static = False
                parent = node.parent
                if "static" in parent.text.decode('utf-8'):
                    # Simple textual check on the statement node isn't perfect but works for detection
                    # Better: check children types.
                    pass

                results.append(JavaDetectedImport(
                    line_num=node.start_point[0] + 1,
                    package_path=raw_text,
                    is_static=is_static,
                    start_byte=node.start_byte,
                    end_byte=node.end_byte
                ))

        return results