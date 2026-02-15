# // scaffold/artisans/translocate_core/resolvers/ruby/inquisitor.py
# ------------------------------------------------------------------
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

from .....inquisitor.sanctum.diagnostics.ruby import RubyInquisitor
from .....logger import Scribe
from .contracts import RubyDetectedRequire

Logger = Scribe("RubyInquisitor")


class RubyInquisitorEngine:
    """
    The Eye of Matz. Perceives 'require' and 'require_relative'.
    """

    # Matches: require 'foo' OR require_relative 'bar'
    QUERY = """
    (call
      method: (identifier) @method
      arguments: (argument_list (string) @path_node)
      (#match? @method "^(require|require_relative)$")
    )
    """

    @classmethod
    def scan(cls, content: str) -> List[RubyDetectedRequire]:
        parser = RubyInquisitor.get_parser()
        if not parser:
            Logger.warn("Ruby Grammar missing. The Gaze is blind.")
            return []

        tree = parser.parse(bytes(content, "utf8"))
        query = parser.language.query(cls.QUERY)

        # Polyglot binding shim
        captures = []
        if hasattr(query, 'captures'):
            captures = query.captures(tree.root_node)
        else:
            cursor = QueryCursor(query)
            captures = cursor.captures(tree.root_node)

        results = []

        # We need to pair @method and @path_node.
        # Tree-sitter returns a flat list of captures.
        # We group by parent node (the 'call' node).

        calls = {}

        for node, name in captures:
            parent_id = node.parent.parent.id  # grandparent is the 'call' node usually?
            # Structure: (call method: (identifier) arguments: (argument_list (string)))
            # Identifier parent is 'call'. String parent is 'argument_list', whose parent is 'call'.

            call_node = node.parent
            if name == 'path_node':
                call_node = node.parent.parent

            if call_node.id not in calls:
                calls[call_node.id] = {'method': None, 'path': None}

            if name == 'method':
                calls[call_node.id]['method'] = node.text.decode('utf-8')
            elif name == 'path_node':
                # node is the string literal including quotes
                raw_text = node.text.decode('utf-8')
                quote = raw_text[0]
                content_text = raw_text[1:-1]
                calls[call_node.id]['path'] = content_text
                calls[call_node.id]['quote'] = quote
                calls[call_node.id]['start'] = node.start_byte + 1  # Skip quote
                calls[call_node.id]['end'] = node.end_byte - 1  # Skip quote
                calls[call_node.id]['line'] = node.start_point[0] + 1

        for data in calls.values():
            if data['method'] and data['path']:
                kind = 'relative' if data['method'] == 'require_relative' else 'absolute'
                results.append(RubyDetectedRequire(
                    line_num=data['line'],
                    path=data['path'],
                    kind=kind,
                    start_byte=data['start'],
                    end_byte=data['end'],
                    quote_style=data['quote']
                ))

        return results