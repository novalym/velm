# // scaffold/artisans/translocate_core/resolvers/cpp/inquisitor.py
# -----------------------------------------------------------------

from typing import List
from tree_sitter import QueryCursor
from .....inquisitor.core import is_grammar_available, LANGUAGES
from .....logger import Scribe
from .contracts import CppDetectedInclude

Logger = Scribe("CppInquisitor")


class CppInquisitorEngine:
    QUERY = """
    (preproc_include
      path: [
        (string_literal) @local
        (system_lib_string) @system
      ]
    )
    """

    @classmethod
    def scan(cls, content: str) -> List[CppDetectedInclude]:
        # Support both 'cpp' and 'c' grammars
        lang_name = "cpp"
        if not is_grammar_available("tree_sitter_cpp", "cpp"):
            if is_grammar_available("tree_sitter_c", "c"):
                lang_name = "c"
            else:
                Logger.warn("C/C++ Grammar missing.")
                return []

        lang = LANGUAGES[lang_name]
        from tree_sitter import Parser
        parser = Parser()
        parser.set_language(lang)

        tree = parser.parse(bytes(content, "utf8"))
        query = lang.query(cls.QUERY)
        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)

        results = []
        for node, name in captures:
            raw_text = node.text.decode('utf-8')
            path = raw_text[1:-1]  # Strip quotes or brackets
            kind = 'local' if name == 'local' else 'system'

            results.append(CppDetectedInclude(
                line_num=node.start_point[0] + 1,
                path=path,
                kind=kind,
                start_byte=node.start_byte,
                end_byte=node.end_byte
            ))

        return results