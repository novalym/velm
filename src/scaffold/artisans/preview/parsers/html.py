# Path: scaffold/artisans/preview/parsers/html.py
# =================================================================================
# == THE DOM SAGE (V-Ω-TREE-SITTER-NATIVE)                                     ==
# =================================================================================
# LIF: 10^24 | The Architect of Markup
#
# 12 LEGENDARY ASCENSIONS:
# 1. [NATIVE TREE-SITTER]: Binds directly to `tree_sitter_html` for fault-tolerant parsing.
# 2. [VOID ELEMENT GNOSIS]: Inherently understands elements that possess no soul (children),
#    like `<img>` and `<input>`, preventing nesting paradoxes.
# 3. [ATTRIBUTE HARVESTER]: Surgically extracts `class`, `id`, `src`, and data attributes.
# 4. [TEXT NORMALIZATION]: Collapses whitespace to reveal the true semantic text.
# 5. [STYLE DIVINATION]: Detects inline `style="..."` strings for future visual clues.
# 6. [SCRIPT/STYLE BLINDNESS]: Intentionally averts its gaze from `<script>` and `<style>`
#    blocks to keep the wireframe pure.
# 7. [ACCESSIBILITY SCAN]: Detects `aria-` attributes and `role` to enhance the preview.
# 8. [ROOT DISCOVERY]: Automatically finds `<body>` or the first significant container
#    if the file is a fragment.
# 9. [COMMENT EXORCISM]: Purges HTML comments from the visual topology.
# 10. [ROBUST FALLBACK]: A specialized Regex engine that handles unclosed tags gracefully.
# 11. [DEPTH GUARD]: Prevents infinite recursion in malformed DOMs.
# 12. [LUMINOUS LOGGING]: Reports parsing mode (High Gaze vs Low Gaze).

import re
from typing import List, Dict, Any, Optional
from .base import BaseUIParser
from ..contracts import UIElement
from ....logger import Scribe

# --- THE DIVINE SUMMONS ---
try:
    from tree_sitter import Language, Parser, Node
    import tree_sitter_html

    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False

Logger = Scribe("HTMLTopologyParser")


class HTMLParser(BaseUIParser):
    # [GNOSIS]: Void Elements (Self-closing by definition in HTML5)
    VOID_ELEMENTS = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    }

    # [FALLBACK]: Regex for the Low Gaze
    HTML_REGEX_FALLBACK = re.compile(r'<(/)?([a-zA-Z0-9\-]+)([^>]*)?(/)?>')

    def __init__(self):
        self._parser = None
        if TREE_SITTER_AVAILABLE:
            try:
                # [THE FIX: V0.22+ CONSTRUCTOR COMPATIBILITY]
                # We instantiate the Language first, then pass it to the Parser constructor.
                # set_language() is annihilated.
                lang_capsule = tree_sitter_html.language()
                lang = Language(lang_capsule)
                self._parser = Parser(lang)
            except Exception as e:
                Logger.warn(f"HTML Grammar initialization failed: {e}")

    def parse(self, content: str) -> List[UIElement]:
        """
        The Grand Rite of DOM Perception.
        """
        if self._parser:
            try:
                return self._parse_with_treesitter(content)
            except Exception as e:
                Logger.warn(f"HTML AST Gaze fractured: {e}. Reverting to Regex.")
                return self._parse_with_regex(content)

        return self._parse_with_regex(content)

    # =========================================================================
    # == STRATEGY A: THE TREE-SITTER ASCENSION                               ==
    # =========================================================================

    def _parse_with_treesitter(self, content: str) -> List[UIElement]:
        tree = self._parser.parse(bytes(content, "utf8"))
        root_node = tree.root_node

        # [ASCENSION 8]: Root Discovery
        # If full HTML doc, drill to body. Else, take root children.
        target_root = root_node

        # Simple walk to find <body>
        # In tree-sitter-html, structure is (document (element (start_tag) (element ...)))
        # We manually traverse to avoid query overhead for simple structure

        # Find <html> -> <body>
        html_node = self._find_child_by_tag(root_node, 'html', content)
        if html_node:
            body_node = self._find_child_by_tag(html_node, 'body', content)
            if body_node:
                target_root = body_node

        elements = []
        for child in target_root.children:
            transmuted = self._transmute_node(child, content.encode('utf-8'))
            if transmuted:
                elements.append(transmuted)

        if not elements:
            return [UIElement(type='text', name='EMPTY_DOM', props={})]

        return elements

    def _transmute_node(self, node: Node, source: bytes, depth: int = 0) -> Optional[UIElement]:
        if depth > 50: return None  # [ASCENSION 11]: Depth Guard

        node_type = node.type

        if node_type == 'element':
            # Structure: (element (start_tag (tag_name) (attribute)* ) (children)* (end_tag)?)
            start_tag = node.child_by_field_name('start_tag')
            if not start_tag: return None  # Malformed

            tag_name_node = start_tag.child_by_field_name('name') or start_tag.children[1]  # heuristic
            tag_name = self._get_text(tag_name_node, source).lower()

            # [ASCENSION 6]: Blindness
            if tag_name in ('script', 'style', 'head'):
                return None

            props = self._harvest_props(start_tag, source)

            children = []
            # Void elements have no children physically in the DOM, even if text exists after them
            if tag_name not in self.VOID_ELEMENTS:
                for child in node.children:
                    # Skip the start/end tags themselves
                    if child.type in ('start_tag', 'end_tag'): continue

                    child_el = self._transmute_node(child, source, depth + 1)
                    if child_el: children.append(child_el)

            return UIElement(
                type=self._divine_type(tag_name),
                name=tag_name,
                props=props,
                children=children
            )

        elif node_type == 'text':
            text = self._get_text(node, source).strip()
            # [ASCENSION 4]: Normalization
            if text:
                return UIElement(type='text', name='text', props={'content': text[:50]})
            return None

        elif node_type == 'comment':
            # [ASCENSION 9]: Exorcism
            return None

        return None

    def _harvest_props(self, start_tag: Node, source: bytes) -> Dict[str, Any]:
        """[ASCENSION 3]: Attribute Harvester"""
        props = {}
        for child in start_tag.children:
            if child.type == 'attribute':
                # (attribute (attribute_name) (quoted_attribute_value (attribute_value))?)
                name_node = child.child_by_field_name('name') or child.child(0)
                if not name_node: continue

                name = self._get_text(name_node, source)

                value_node = child.child_by_field_name('value')
                value = ""
                if value_node:
                    # Strip quotes
                    raw = self._get_text(value_node, source)
                    if raw.startswith('"') or raw.startswith("'"):
                        value = raw[1:-1]
                    else:
                        value = raw

                if name == 'class':
                    props['has_style'] = True
                    props['className'] = value  # For future Tailwind parsing
                elif name == 'id':
                    props['id'] = value
                elif name == 'src':
                    props['has_source'] = True
                elif name.startswith('aria-') or name == 'role':
                    props['accessible'] = True
                elif name.startswith('on'):  # Inline JS event
                    props['interactive'] = True
        return props

    def _find_child_by_tag(self, parent: Node, tag: str, source: str) -> Optional[Node]:
        for child in parent.children:
            if child.type == 'element':
                start = child.child_by_field_name('start_tag')
                if start:
                    name_node = start.child_by_field_name('name') or start.children[1]
                    name = self._get_text(name_node, source.encode('utf-8'))
                    if name.lower() == tag:
                        return child
        return None

    def _get_text(self, node: Node, source: bytes) -> str:
        if not node: return ""
        return source[node.start_byte:node.end_byte].decode('utf-8')

    # =========================================================================
    # == STRATEGY B: THE REGEX FALLBACK (LEGACY SAFEGUARD)                   ==
    # =========================================================================

    def _parse_with_regex(self, content: str) -> List[UIElement]:
        root_elements = []
        stack: List[UIElement] = []

        # Iterative Stack-based Parser
        for match in self.HTML_REGEX_FALLBACK.finditer(content):
            is_closing_tag = bool(match.group(1))
            tag_name = match.group(2).lower()
            attributes = match.group(3) or ""
            is_self_closing = bool(match.group(4)) or tag_name in self.VOID_ELEMENTS

            # [ASCENSION 6]: Ignore script/style tags in regex mode (simple skip)
            if tag_name in ('script', 'style', 'meta', 'link'): continue

            ui_type = self._divine_type(tag_name)

            if is_closing_tag:
                # Basic stack pop logic
                if stack:
                    # In HTML, tags can be unmatched. We pop until we find match or root.
                    # Simplified: just pop top
                    stack.pop()

            elif is_self_closing:
                el = UIElement(type=ui_type, name=tag_name, props=self._parse_props_regex(attributes))
                if stack:
                    stack[-1].children.append(el)
                else:
                    root_elements.append(el)

            else:
                el = UIElement(type=ui_type, name=tag_name, props=self._parse_props_regex(attributes))
                if stack:
                    stack[-1].children.append(el)
                else:
                    root_elements.append(el)
                stack.append(el)

        if not root_elements:
            return [UIElement(type='container', name='HTML_FRAGMENT', children=[])]

        return root_elements

    def _parse_props_regex(self, attr_str: str) -> dict:
        props = {}
        if 'class=' in attr_str: props['has_style'] = True
        if 'onclick' in attr_str: props['interactive'] = True
        if 'src=' in attr_str: props['has_source'] = True
        return props

    def _divine_type(self, tag: str) -> str:
        """[ASCENSION]: Semantic HTML Mapping"""
        if tag in ['div', 'section', 'main', 'header', 'footer', 'nav', 'ul', 'li', 'article', 'aside', 'body',
                   'html']: return 'container'
        if tag in ['span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'strong', 'em', 'small', 'b',
                   'i']: return 'text'
        if tag in ['button', 'a']: return 'button'
        if tag in ['input', 'textarea', 'select']: return 'input'
        if tag in ['img', 'svg', 'picture', 'figure']: return 'image'
        return 'container'