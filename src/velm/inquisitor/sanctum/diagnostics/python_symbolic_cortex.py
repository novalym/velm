# === [scaffold/inquisitor/sanctum/diagnostics/python_symbolic_cortex.py] - SECTION 1 of 1: The Ascended Python Cortex ===
import sys
from typing import Dict, Any, List, Tuple, Set, Optional

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # Attempting to speak with the native C-matter (Local/Titan Node).
    from tree_sitter import Tree, Node, QueryCursor, Language, Query

    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native library is unmanifest, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum's ignition.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]

        # [ASCENSION]: We extract the Diamond souls from the Proxy
        # These classes are telepathically linked to the JS WASM engine.
        Tree = _ts.Tree
        Node = _ts.Node
        QueryCursor = _ts.QueryCursor
        Language = _ts.Language

        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If the Mind is cold in all realms, we forge hollow vessels.
        # This prevents 'AttributeError' and 'TypeError' during registration.
        TREE_SITTER_AVAILABLE = False

        # [ASCENSION 5]: Hollow Type Generation (The Sarcophagus)
        # We create specific type identities rather than generic objects.
        Tree = type("HollowTree", (object,), {})
        Node = type("HollowNode", (object,), {})
        QueryCursor = type("HollowQueryCursor", (object,), {})
        Language = type("HollowLanguage", (object,), {})


class PythonSymbolicCortex:
    """
    =================================================================================
    == THE GOD-ENGINE OF PYTHONIC GNOSIS (V-Ω-BOUND-CURSOR-FIX)                    ==
    =================================================================================
    @gnosis:title The Symbolic Cortex (Python)
    @gnosis:summary The divine, sentient AST Surgeon. Updated for strict bindings where
                     QueryCursor is immutably bound to a specific Query.
    @gnosis:LIF INFINITY

    ### THE ASCENSIONS OF THE CURSOR:
    1.  **The Explicit Query Constructor:** Uses `Query(language, source)`.
    2.  **The Bound Cursor Protocol:** Since `QueryCursor` requires a `Query` at birth,
        we instantiate ephemeral cursors (`QueryCursor(self.q_defs)`) for each specific
        rite, rather than holding a single mutable cursor.
    3.  **The Correct Invocation:** Calls `cursor.captures(node)` on the bound cursor.
    """

    # --- THE ATOMIC QUERIES ---

    # 1. Definitions (The Skeleton)
    QUERY_DEFS = """
    (function_definition
      name: (identifier) @name
      parameters: (parameters) @args
      body: (block)? @body
    ) @function

    (class_definition
      name: (identifier) @name
      body: (block)? @body
    ) @class
    """

    # 2. Imports (The Bonds)
    QUERY_IMPORTS = """
    (import_statement
      name: (dotted_name) @import_path
    ) @import

    (import_from_statement
      module_name: (dotted_name)? @module
      name: (dotted_name) @name
    ) @import_from

    (import_from_statement
        module_name: (dotted_name)? @module
        (wildcard_import) @wildcard
    ) @import_wildcard

    (aliased_import
      name: (dotted_name) @original
      alias: (identifier) @alias
    ) @alias
    """

    # 3. References (The Nervous System)
    QUERY_REFS = """
    (identifier) @ref
    (attribute attribute: (identifier) @attr_ref)
    """

    # 4. Complexity (The Weight of Logic)
    QUERY_COMPLEXITY = """
    (if_statement) @branch
    (for_statement) @branch
    (while_statement) @branch
    (try_statement (except_clause)) @branch
    (boolean_operator) @branch
    """

    def __init__(self, language: Language):
        self.language = language

        # [THE FIX] The Rite of Explicit Compilation
        # We compile the maps (Queries) once.
        self.q_defs = Query(self.language, self.QUERY_DEFS)
        self.q_imports = Query(self.language, self.QUERY_IMPORTS)
        self.q_refs = Query(self.language, self.QUERY_REFS)
        self.q_complexity = Query(self.language, self.QUERY_COMPLEXITY)

    def inquire(self, tree: Tree) -> Dict[str, Any]:
        """
        [THE GRAND RITE OF INQUIRY]
        Orchestrates the surgical dissection of the AST.
        """
        root = tree.root_node

        # 1. Mine Structure (Classes & Functions)
        structure = self._mine_structure(root)

        # 2. Mine Imports (External Bonds)
        dependencies = self._mine_imports(root)

        # 3. Mine Causal Bonds (Who uses what?)
        for func in structure['functions']:
            func_node = func.pop('_node', None)
            if func_node:
                func['dependencies'] = self._mine_causal_bonds(func_node, func['name'], func['args_list'])

        for cls in structure['classes']:
            cls_node = cls.pop('_node', None)
            if cls_node:
                cls['dependencies'] = self._mine_causal_bonds(cls_node, cls['name'], [])

        # 4. Calculate Global Metrics
        metrics = {
            "complexity": 1 + len(structure['functions']) + len(structure['classes']),
            "function_count": len(structure['functions']),
            "class_count": len(structure['classes']),
            "line_count": len(root.text.splitlines())
        }

        return {
            "functions": structure['functions'],
            "classes": structure['classes'],
            "dependencies": dependencies,
            "metrics": metrics
        }

    def _mine_structure(self, root: Node) -> Dict[str, List[Dict]]:
        """[THE STRUCTURAL SURGEON] Extracts definitions."""
        functions = []
        classes = []

        # [THE FIX] Bind a fresh cursor to the DEFS query
        cursor = QueryCursor(self.q_defs)
        captures = self._normalize_captures(cursor.captures(root))

        for node, name in captures:
            if name == 'function':
                name_node = node.child_by_field_name('name')
                func_name = name_node.text.decode('utf-8') if name_node else "unknown"

                is_async = node.text.decode('utf-8').lstrip().startswith('async')
                decorators = self._extract_decorators(node)
                docstring = self._extract_docstring(node)
                complexity = self._calculate_complexity(node)
                args_list = self._extract_arg_names(node)

                functions.append({
                    "name": func_name,
                    "type": "method" if node.parent.type == 'class_definition' else "function",
                    "start_point": node.start_point,
                    "end_point": node.end_point,
                    "start_byte": node.start_byte,
                    "end_byte": node.end_byte,
                    "line_count": node.end_point[0] - node.start_point[0] + 1,
                    "docstring": docstring,
                    "decorators": decorators,
                    "cyclomatic_complexity": complexity,
                    "is_async": is_async,
                    "args_list": args_list,
                    "_node": node
                })

            elif name == 'class':
                name_node = node.child_by_field_name('name')
                cls_name = name_node.text.decode('utf-8') if name_node else "unknown"

                docstring = self._extract_docstring(node)
                decorators = self._extract_decorators(node)

                classes.append({
                    "name": cls_name,
                    "start_point": node.start_point,
                    "end_point": node.end_point,
                    "start_byte": node.start_byte,
                    "end_byte": node.end_byte,
                    "line_count": node.end_point[0] - node.start_point[0] + 1,
                    "docstring": docstring,
                    "decorators": decorators,
                    "_node": node
                })

        return {"functions": functions, "classes": classes}

    def _mine_imports(self, root: Node) -> Dict[str, Any]:
        """[THE IMPORT DISSECTOR]"""
        imports = []
        imported_symbols = set()

        # [THE FIX] Bind a fresh cursor to the IMPORTS query
        cursor = QueryCursor(self.q_imports)
        captures = self._normalize_captures(cursor.captures(root))

        for node, name in captures:
            text = node.text.decode('utf-8')
            line_num = node.start_point[0] + 1

            if name == 'import_path':
                imports.append({"path": text, "line_num": line_num})
                imported_symbols.add(text)

            elif name == 'name':
                parent = node.parent
                module_node = parent.child_by_field_name('module_name')
                module_name = module_node.text.decode('utf-8') if module_node else ""

                full_symbol = f"{module_name}.{text}" if module_name else text
                imports.append({"path": full_symbol, "line_num": line_num})
                imported_symbols.add(full_symbol)

            elif name == 'wildcard':
                parent = node.parent
                module_node = parent.child_by_field_name('module_name')
                module_name = module_node.text.decode('utf-8') if module_node else "unknown"
                imports.append({"path": f"{module_name}.*", "line_num": line_num})
                imported_symbols.add(module_name)

        return {
            "imports": imports,
            "imported_symbols": sorted(list(imported_symbols))
        }

    def _mine_causal_bonds(self, node: Node, self_name: str, local_args: List[str]) -> List[str]:
        """[THE CAUSAL MINER]"""
        refs = set()

        # [THE FIX] Bind a fresh cursor to the REFS query
        cursor = QueryCursor(self.q_refs)
        captures = self._normalize_captures(cursor.captures(node))

        IGNORED = {'self', 'cls', 'print', 'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple', 'None',
                   'True', 'False', 'super', 'isinstance', 'getattr', 'setattr', 'hasattr'}

        ignored_locals = set(local_args)
        ignored_locals.add(self_name)

        for ref_node, capture_name in captures:
            text = ref_node.text.decode('utf-8')

            if text in IGNORED: continue
            if text in ignored_locals: continue

            parent = ref_node.parent
            if parent.type == 'assignment' and ref_node == parent.child_by_field_name('left'):
                ignored_locals.add(text)
                continue
            if parent.type == 'parameter':
                ignored_locals.add(text)
                continue

            refs.add(text)

        return sorted(list(refs))

    def _calculate_complexity(self, node: Node) -> int:
        """[THE COMPLEXITY AUDITOR]"""
        # [THE FIX] Bind a fresh cursor to the COMPLEXITY query
        cursor = QueryCursor(self.q_complexity)
        captures = cursor.captures(node)

        if isinstance(captures, list):
            return 1 + len(captures)
        elif isinstance(captures, dict):
            return 1 + sum(len(v) for v in captures.values())
        return 1

    def _extract_docstring(self, node: Node) -> str:
        body = node.child_by_field_name('body')
        if not body: return ""
        for child in body.children:
            if child.type == 'expression_statement':
                grandchild = child.child(0)
                if grandchild and grandchild.type == 'string':
                    raw = grandchild.text.decode('utf-8')
                    if raw.startswith('"""') or raw.startswith("'''"):
                        return raw[3:-3].strip()
                    if raw.startswith('"') or raw.startswith("'"):
                        return raw[1:-1].strip()
            if child.type not in ('comment', 'text'):
                break
        return ""

    def _extract_decorators(self, node: Node) -> List[str]:
        decorators = []
        parent = node.parent
        if parent and parent.type == 'decorated_definition':
            for child in parent.children:
                if child.type == 'decorator':
                    decorators.append(child.text.decode('utf-8').strip())
        return decorators

    def _extract_arg_names(self, node: Node) -> List[str]:
        args = []
        params_node = node.child_by_field_name('parameters')
        if params_node:
            for child in params_node.children:
                if child.type in ('identifier', 'typed_parameter', 'default_parameter'):
                    name_node = child.child_by_field_name('name')
                    if name_node:
                        args.append(name_node.text.decode('utf-8'))
                    elif child.type == 'identifier':
                        args.append(child.text.decode('utf-8'))
        return args

    def _normalize_captures(self, captures: Any) -> List[Tuple[Node, str]]:
        """[THE COMPATIBILITY SHIM]"""
        results = []
        if isinstance(captures, dict):
            for name, nodes in captures.items():
                if not isinstance(nodes, list): nodes = [nodes]
                for n in nodes:
                    results.append((n, name))
        elif isinstance(captures, list):
            for item in captures:
                if isinstance(item, tuple) and len(item) == 2:
                    results.append(item)
                elif hasattr(item, 'node') and hasattr(item, 'name'):
                    results.append((item.node, item.name))
        return results