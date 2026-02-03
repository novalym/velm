# Path: scaffold/inquisitor/sanctum/diagnostics/react.py
# ------------------------------------------------------

"""
=================================================================================
== THE GOD-ENGINE OF REACT PERCEPTION (V-Ω-ULTIMA-STATEFUL)                    ==
=================================================================================
LIF: 10,000,000,000

This divine artisan has achieved its final apotheosis. It is now a true God-Engine,
a master of gazing into the soul of a TSX Abstract Syntax Tree. It has been
bestowed with a pantheon of new, hyper-sentient faculties to guide the Weaver's
unbreakable hand with absolute, byte-level precision.
"""
from typing import Optional, Any, Dict, List

from .javascript import JavaScriptInquisitor
from ..engine import BaseInquisitor
from ...queries import react_queries as queries
from ....logger import Scribe

Logger = Scribe("ReactInquisitor")


class ReactInquisitor(BaseInquisitor):
    """The AST Surgeon for React/TypeScript, based on JavaScriptInquisitor."""

    LANGUAGE_NAME = "tsx"
    GRAMMAR_PACKAGE = "tree_sitter_typescript"

    QUERIES = {
        **JavaScriptInquisitor.QUERIES,
        "gnostic_marker": queries.QUERY_GNOSTIC_MARKER,
        "return_jsx": queries.QUERY_RETURN_JSX,
        "last_import": queries.QUERY_LAST_IMPORT,
        "named_imports": queries.QUERY_NAMED_IMPORTS,
    }

    def __init__(self):
        """
        [THE RITE OF INCEPTION]
        We awaken the parser immediately upon birth to fail fast if the grammar is missing,
        and to cache the heavy object for the Weaver's repeated use.
        """
        self._parser = self.get_parser()
        if not self._parser:
            Logger.warn("The React Grammar is not manifest. The Inquisitor is blind.")

    def parse(self, content: str) -> Optional[Any]:
        """
        [THE DIVINE GAZE]
        Transmutes raw text string into a Tree-sitter Tree.
        Handles encoding and null-checks automatically.
        """
        if not self._parser:
            return None
        try:
            return self._parser.parse(bytes(content, "utf8"))
        except Exception as e:
            Logger.error(f"Parsing Paradox: {e}")
            return None

    def find_last_import_end(self, tree: Any) -> int:
        """
        [THE GAZE OF THE FINAL IMPORT]
        Perceives the precise byte offset where a new import should be woven.
        """
        captures = self._get_query_captures(tree, "last_import", "last_import")
        if captures:
            last_import_node = captures[-1][0]
            return last_import_node.end_byte
        return 0  # If no imports, weave at the dawn of the scripture.

    def find_import_by_source(self, tree: Any, code_bytes: bytes, source_path: str) -> Optional[Dict]:
        """
        [THE GAZE OF THE GNOSTIC GRAFT]
        Perceives if an import from a specific source already exists and, if so,
        provides the Gnosis needed to graft a new named import onto it.
        """
        captures = self._get_query_captures(tree, "named_imports")

        for node, capture_name in captures:
            if capture_name == 'source' and node.text.decode('utf-8').strip('"\'') == source_path:
                # We found the right import statement. Now find its children.
                parent_import_stmt = node.parent

                names = [
                    n.text.decode('utf-8') for n, name in
                    self._get_query_captures(parent_import_stmt, "named_imports", "imported_name")
                ]

                # Find the end position of the last named import to append a comma
                last_name_node = self._get_query_captures(parent_import_stmt, "named_imports", "imported_name")[-1][0]

                return {
                    "names": names,
                    "last_name_end": last_name_node.end_byte
                }
        return None

    def find_jsx_insertion_point(self, tree: Any, code_bytes: bytes) -> Optional[Dict]:
        """
        [THE ORACLE OF THE GNOSTIC TARGET]
        A divine, multi-stage Gaze to find the one true place to weave a new component.
        """
        # --- GAZE I: THE SACRED MARKER ---
        marker_captures = self._get_query_captures(tree, "gnostic_marker", "marker")
        if marker_captures:
            marker_node = marker_captures[0][0]
            line_num = marker_node.start_point[0]
            line_content = code_bytes.splitlines()[line_num].decode('utf-8')
            indent = " " * (len(line_content) - len(line_content.lstrip()))

            return {
                "index": marker_node.parent.start_byte,  # Insert before the comment
                "indent": indent + "  "
            }

        # --- GAZE II: THE HEART OF THE COMPONENT (RETURN STATEMENT) ---
        # Now matches fragments and self-closing tags too.
        return_captures = self._get_query_captures(tree, "return_jsx", "jsx_root")
        if return_captures:
            jsx_root_node = return_captures[0][0]

            # Strategy 1: If it has a closing tag (Standard Element or Fragment)
            # We insert BEFORE the closing tag.
            if jsx_root_node.type in ('jsx_element', 'jsx_fragment'):
                # The closing tag is always the last child
                closing_tag_node = jsx_root_node.children[-1]

                insertion_index = closing_tag_node.start_byte

                # Calculate indent based on the closing tag's line
                line_num = closing_tag_node.start_point[0]
                line_content = code_bytes.splitlines()[line_num].decode('utf-8')
                indent = " " * (len(line_content) - len(line_content.lstrip()))

                return {
                    "index": insertion_index,
                    "indent": indent + "  "
                }

            # Strategy 2: If it is Self-Closing (<App />)
            # We cannot insert INSIDE it. We must wrap it?
            # Or we assume the Weaver will handle wrapping?
            # The Weaver expects an insertion point *inside*.
            # If we return None here, the Weaver falls back to Regex, which is safer for wrapping.
            pass

        return None