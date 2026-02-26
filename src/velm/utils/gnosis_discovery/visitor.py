import re
from typing import Set, Dict, Any, Optional
from jinja2 import nodes
from jinja2.visitor import NodeVisitor


class GnosticASTVisitor(NodeVisitor):
    """
    =============================================================================
    == THE MIND WALKER (V-Ω-AST-ANALYSIS-V700)                                 ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SYMBOLIC_TRACER
    """

    def __init__(self, local_scope_override: Set[str] = None):
        self.required_vars: Set[str] = set()
        self.local_scope: Set[str] = local_scope_override or set()
        self.inferred_types: Dict[str, str] = {}
        self.defaults: Dict[str, Any] = {}
        self.filters_used: Set[str] = set()
        self.complex_objects: Set[str] = set()

    def visit_Name(self, node: nodes.Name):
        """Perceives a variable usage or storage event."""
        if node.ctx == 'load' and node.name not in self.local_scope:
            if not node.name.startswith('_'):
                self.required_vars.add(node.name)
        elif node.ctx == 'store':
            self.local_scope.add(node.name)

    def visit_Filter(self, node: nodes.Filter):
        self.filters_used.add(node.name)
        type_map = {
            'int': 'number', 'float': 'number', 'sum': 'number',
            'list': 'list', 'join': 'list', 'first': 'list', 'last': 'list',
            'string': 'string', 'lower': 'string', 'upper': 'string'
        }
        if node.name in type_map:
            self._infer_type_from_node(node.node, type_map[node.name])

        if node.name == 'default' and node.args:
            try:
                default_val_node = node.args[0]
                if isinstance(default_val_node, nodes.Const):
                    target_var = self._get_root_var_name(node.node)
                    if target_var:
                        self.defaults[target_var] = default_val_node.value
            except Exception:
                pass
        self.generic_visit(node)

    def visit_For(self, node: nodes.For):
        self.visit(node.iter)
        loop_vars = set()
        if isinstance(node.target, nodes.Name):
            loop_vars.add(node.target.name)
        elif isinstance(node.target, (nodes.Tuple, nodes.List)):
            for child in node.target.items:
                if isinstance(child, nodes.Name):
                    loop_vars.add(child.name)
        self.local_scope.update(loop_vars)
        self.generic_visit(node)

    def visit_Assign(self, node: nodes.Assign):
        if isinstance(node.target, nodes.Name):
            self.local_scope.add(node.target.name)
        self.generic_visit(node)

    def visit_Getattr(self, node: nodes.Getattr):
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)

    def visit_Getitem(self, node: nodes.Getitem):
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)
        self.visit(node.arg)

    def _infer_type_from_node(self, node, type_name: str):
        name = self._get_root_var_name(node)
        if name and name not in self.local_scope:
            self.inferred_types[name] = type_name

    def _get_root_var_name(self, node) -> Optional[str]:
        if node is None: return None
        if isinstance(node, nodes.Name):
            return node.name
        elif isinstance(node, (nodes.Getattr, nodes.Getitem, nodes.Filter)):
            return self._get_root_var_name(getattr(node, 'node', None))
        return None