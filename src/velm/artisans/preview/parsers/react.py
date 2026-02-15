# Path: scaffold/artisans/preview/parsers/react.py
# =================================================================================
# == THE JSX INQUISITOR (V-Ω-CRASH-PROOF-ULTIMA)                                 ==
# =================================================================================
# LIF: 10^42 | Deep AST Perception & Topology Extraction
#
# [HEALED]:
# 1. [SAFE QUERY PROTOCOL]: Removed specific logic nodes from SCM to prevent compilation errors.
#    Logic detection is now handled safely in Python via `_analyze_expression`.
# 2. [OMNISCIENT TRAVERSAL]: The fallback scanner now recursively enters functions and classes
#    to find the render root, ensuring no component is hidden.
# 3. [BROAD RETURN DETECTION]: Finds `return (...)` even in arrow functions without bodies.
# 4. [FRAGMENT NORMALIZATION]: Handles `<>...</>` explicitly.
import sys
import re
from typing import List, Dict, Any, Optional
from .base import BaseUIParser
from ..contracts import UIElement
from ....logger import Scribe

# --- THE DIVINE SUMMONS (CORE INTEGRATION) ---
try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # Attempting to speak with the native C-matter.
    from tree_sitter import Query, Node

    # Internal Artisan Suture
    try:
        from ....inquisitor.sanctum.diagnostics.react import ReactInquisitor
    except (ImportError, ValueError):
        # Handle cases where the relative path is fractured or the file is missing
        ReactInquisitor = None

    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # Native matter is unmanifest; we scry the Gnostic Registry for the Diamond Proxy.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        Query = _ts.Query
        Node = _ts.Node

        # Internal Artisan Suture within the Proxy Realm
        try:
            from ....inquisitor.sanctum.diagnostics.react import ReactInquisitor
        except (ImportError, ValueError):
            ReactInquisitor = None

        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # Reality is cold. We forge hollow vessels to preserve the script's existence.
        TREE_SITTER_AVAILABLE = False
        ReactInquisitor = None

        # Hollow types to ward against downstream TypeErrors
        Query = type("HollowQuery", (object,), {})
        Node = type("HollowNode", (object,), {})

Logger = Scribe("ReactTopologyParser")


class ReactParser(BaseUIParser):
    # [FALLBACK]: The Low Gaze
    JSX_REGEX_FALLBACK = re.compile(r'<(/)?([a-zA-Z0-9\.]+)([^>]*)?(/)?>')

    # [SCM]: THE SAFE HIGH GAZE QUERY
    # We only capture structural elements here. Logic is divined in Python.
    TOPOLOGY_QUERY_SCM = """
    (jsx_element
        open_tag: (jsx_opening_element name: (_) @tag_name)
    ) @element

    (jsx_self_closing_element
        name: (_) @tag_name
    ) @element

    (jsx_expression) @expression
    """

    def __init__(self):
        self._inquisitor = None
        self._language = None
        self._query = None

        if TREE_SITTER_AVAILABLE and ReactInquisitor:
            try:
                # [ASCENSION 1]: Reuse the System's Inquisitor
                self._inquisitor = ReactInquisitor()
                parser = self._inquisitor.get_parser()
                if parser:
                    self._language = parser.language
                    try:
                        self._query = self._language.query(self.TOPOLOGY_QUERY_SCM)
                    except Exception as qe:
                        Logger.warn(f"Topology Query Compilation Failed: {qe}. Falling back to manual traversal.")
            except Exception as e:
                Logger.warn(f"Failed to initialize Tree-Sitter Integration: {e}")

    def parse(self, content: str) -> List[UIElement]:
        """The Grand Rite of Parsing."""
        if self._inquisitor and self._language:
            try:
                return self._parse_with_treesitter(content)
            except Exception as e:
                Logger.warn(f"AST Gaze fractured: {e}. Reverting to Regex.")
                return self._parse_with_regex(content)
        return self._parse_with_regex(content)

    # =========================================================================
    # == STRATEGY A: THE TREE-SITTER ASCENSION                               ==
    # =========================================================================

    def _parse_with_treesitter(self, content: str) -> List[UIElement]:
        tree = self._inquisitor.parse(content)
        if not tree: raise ValueError("Parser returned Void Tree")

        # [STEP 1]: Find the UI Root
        ui_root_node = self._find_render_root(tree.root_node)

        if not ui_root_node:
            # [STEP 2]: Aggressive Fallback Scan
            return self._scan_for_any_jsx(tree.root_node, content.encode('utf-8'))

        # [STEP 3]: Transmute AST to Topology
        return self._transmute_node(ui_root_node, content.encode('utf-8'))

    def _find_render_root(self, root: Node) -> Optional[Node]:
        """Scans the AST for the most likely UI entry point."""
        try:
            # We look for return statements that return JSX
            find_return_q = self._language.query("""
                (return_statement (parenthesized_expression (jsx_element) @root))
                (return_statement (jsx_element) @root)
                (return_statement (jsx_fragment) @root)
                (return_statement (parenthesized_expression (jsx_fragment) @root))
            """)
            captures = find_return_q.captures(root)
            if captures:
                return captures[0][0]
        except Exception:
            pass
        return None

    def _scan_for_any_jsx(self, root: Node, source: bytes) -> List[UIElement]:
        """[THE OMNISCIENT TRAVERSAL]: Recursively searches everything."""
        to_visit = [root]

        while to_visit:
            node = to_visit.pop(0)

            if node.type in ('jsx_element', 'jsx_self_closing_element', 'jsx_fragment'):
                return self._transmute_node(node, source)

            # Unconditional traversal to find nested returns/exports
            if node.child_count > 0:
                to_visit.extend(node.children)

        return [UIElement(type='text', name='NO_RENDER_DETECTED')]

    def _transmute_node(self, node: Node, source_bytes: bytes, depth: int = 0) -> List[UIElement]:
        """Recursively converts a Tree-Sitter Node into UI Elements."""
        if depth > 50: return []

        node_type = node.type
        elements = []

        if node_type == 'jsx_element':
            opening = node.child_by_field_name('open_tag')
            name_node = opening.child_by_field_name('name') if opening else None

            tag_name = 'div'
            if name_node:
                tag_name = self._get_text(name_node, source_bytes)

            props = self._harvest_props(opening, source_bytes)
            children = []

            for child in node.children:
                if self._is_jsx_content_node(child):
                    children.extend(self._transmute_node(child, source_bytes, depth + 1))

            elements.append(UIElement(
                type=self._divine_type(tag_name),
                name=tag_name,
                props=props,
                children=children
            ))

        elif node_type == 'jsx_self_closing_element':
            name_node = node.child_by_field_name('name')
            tag_name = self._get_text(name_node, source_bytes) if name_node else 'div'
            props = self._harvest_props(node, source_bytes)

            elements.append(UIElement(
                type=self._divine_type(tag_name),
                name=tag_name,
                props=props,
                children=[]
            ))

        elif node_type == 'jsx_fragment':
            for child in node.children:
                if self._is_jsx_content_node(child):
                    elements.extend(self._transmute_node(child, source_bytes, depth + 1))

        elif node_type == 'jsx_text':
            text = self._get_text(node, source_bytes).strip()
            if text:
                elements.append(UIElement(type='text', name='text', props={'content': text[:30]}))

        elif node_type == 'jsx_expression':
            # [ASCENSION 4]: LOGIC ANALYSIS IN PYTHON
            # This avoids the Query Compilation Error by checking types manually.
            logic_el = self._analyze_expression(node, source_bytes)
            if logic_el:
                # If the expression contains logic, it might have nested JSX children
                # We attempt to find them in the expression's subtree
                logic_children = []
                # Simple DFS within the expression to find nested JSX
                stack = [node]
                while stack:
                    curr = stack.pop(0)
                    if curr.type in ('jsx_element', 'jsx_self_closing_element', 'jsx_fragment'):
                        logic_children.extend(self._transmute_node(curr, source_bytes, depth + 1))
                    elif curr.child_count > 0:
                        stack.extend(curr.children)

                logic_el.children = logic_children
                elements.append(logic_el)
            else:
                elements.append(UIElement(type='text', name='{Expr}', props={'code': 'dynamic'}))

        elif node_type == 'parenthesized_expression':
            for child in node.children:
                if child.type != '(' and child.type != ')':
                    elements.extend(self._transmute_node(child, source_bytes, depth))

        return elements

    def _analyze_expression(self, node: Node, source: bytes) -> Optional[UIElement]:
        """
        [THE LOGIC SEER]: Manually inspects the expression tree for logic patterns.
        Safe against grammar version mismatches.
        """
        expr_text = self._get_text(node, source)

        # 1. Map / Loop Detection
        if '.map' in expr_text:
            return UIElement(type='container', name='Loop', props={'logic': 'map', 'interactive': True})

        # 2. Conditional Detection (DFS for operators)
        # We look for 'binary_expression' with && or ||, or 'ternary_expression' / 'conditional_expression'
        stack = [node]
        while stack:
            curr = stack.pop(0)
            t = curr.type

            if t == 'binary_expression':
                # Check operator
                op = curr.child_by_field_name('operator')
                if op and self._get_text(op, source) in ['&&', '||', '??']:
                    return UIElement(type='container', name='Condition', props={'logic': 'if', 'interactive': True})

            if t in ('ternary_expression', 'conditional_expression'):
                return UIElement(type='container', name='Condition', props={'logic': 'ternary', 'interactive': True})

            # Don't dive too deep
            if curr.child_count > 0 and len(stack) < 20:
                stack.extend(curr.children)

        return None

    def _is_jsx_content_node(self, node: Node) -> bool:
        return node.type in (
            'jsx_element', 'jsx_self_closing_element', 'jsx_fragment',
            'jsx_expression', 'jsx_text', 'parenthesized_expression'
        )

    def _harvest_props(self, node: Node, source: bytes) -> Dict[str, Any]:
        props = {}
        if not node: return props

        for child in node.children:
            if child.type == 'jsx_attribute':
                prop_name_node = child.child_by_field_name('name')
                prop_value_node = child.child_by_field_name('value')

                if prop_name_node:
                    name = self._get_text(prop_name_node, source)

                    if not prop_value_node:
                        props[name] = True
                        continue

                    value_text = self._get_text(prop_value_node, source)

                    if name == 'className':
                        props['has_style'] = True
                        props['className'] = value_text.strip('"\'')

                    if name.startswith('on') and len(name) > 2 and name[2].isupper():
                        props['interactive'] = True
                        props['event'] = name

                    if name in ['src', 'href']:
                        props['has_source'] = True

        return props

    def _get_text(self, node: Node, source: bytes) -> str:
        if not node: return ""
        return source[node.start_byte:node.end_byte].decode('utf-8')

    # =========================================================================
    # == STRATEGY B: THE REGEX FALLBACK (LEGACY SAFEGUARD)                   ==
    # =========================================================================

    def _parse_with_regex(self, content: str) -> List[UIElement]:
        lines = content.split('\n')
        render_start = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('return (') or stripped.startswith('return <'):
                render_start = i
                break

        scan_text = content if render_start == -1 else "\n".join(lines[render_start:render_start + 150])
        return self._build_tree_regex(scan_text)

    def _build_tree_regex(self, text: str) -> List[UIElement]:
        root_elements = []
        stack: List[UIElement] = []

        for match in self.JSX_REGEX_FALLBACK.finditer(text):
            is_closing = bool(match.group(1))
            tag_name = match.group(2)
            attributes = match.group(3) or ""
            is_self_closing = bool(match.group(4))

            ui_type = self._divine_type(tag_name)

            if is_closing:
                if stack: stack.pop()
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
            return [UIElement(type='container', name='File', children=[])]

        return root_elements

    def _parse_props_regex(self, attr_str: str) -> dict:
        props = {}
        if 'className' in attr_str: props['has_style'] = True
        if 'onClick' in attr_str: props['interactive'] = True
        return props

    def _divine_type(self, tag: str) -> str:
        if not tag: return 'text'
        if tag[0].isupper(): return 'component'
        if tag in ['div', 'section', 'main', 'header', 'footer', 'nav', 'ul', 'li', 'form', 'article',
                   'aside']: return 'container'
        if tag in ['span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'strong', 'em', 'small']: return 'text'
        if tag in ['button', 'a', 'Link']: return 'button'
        if tag in ['input', 'textarea', 'select']: return 'input'
        if tag in ['img', 'svg', 'Image']: return 'image'
        return 'container'

