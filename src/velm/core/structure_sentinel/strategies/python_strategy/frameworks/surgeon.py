import ast
from typing import Optional


class ASTSurgeon(ast.NodeTransformer):
    """
    [THE AST SCALPEL]
    Performs the physical insertion of nodes into the syntax tree.
    """

    def __init__(self, import_line: str, wiring_line: str, anchor_var: str):
        self.import_node = ast.parse(import_line).body[0]
        # wiring_line might be an Expr (call) or an Assign (list append)
        self.wiring_nodes = ast.parse(wiring_line).body
        self.anchor_var = anchor_var
        self.import_injected = False
        self.wiring_injected = False

    def visit_Module(self, node: ast.Module) -> ast.Module:
        # 1. Inject Import (After last import)
        last_import_index = -1
        for i, child in enumerate(node.body):
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                if isinstance(child, ast.ImportFrom) and child.module == "__future__":
                    continue
                last_import_index = i

        # Check if import already exists (simple check)
        # Real implementation would check module/names recursively
        node.body.insert(last_import_index + 1, self.import_node)
        self.import_injected = True

        # 2. Inject Wiring (Global Scope Fallback)
        # If we are in global scope, we look for the app assignment
        if not self.wiring_injected:
            anchor_idx = -1
            for i, child in enumerate(node.body):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == self.anchor_var:
                            anchor_idx = i
                            break

            if anchor_idx != -1:
                # Insert after app definition
                for n in reversed(self.wiring_nodes):
                    node.body.insert(anchor_idx + 1, n)
                self.wiring_injected = True

        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Handles Factory Pattern (def create_app(): ...)"""
        # Heuristic: If function returns the anchor var, inject before return
        returns_app = False
        return_idx = -1

        for i, child in enumerate(node.body):
            if isinstance(child, ast.Return) and child.value:
                if isinstance(child.value, ast.Name) and child.value.id == self.anchor_var:
                    returns_app = True
                    return_idx = i
                    break

        if returns_app:
            for n in reversed(self.wiring_nodes):
                node.body.insert(return_idx, n)
            self.wiring_injected = True

        return self.generic_visit(node)


class DjangoSurgeon(ast.NodeTransformer):
    """Specialized Surgeon for INSTALLED_APPS lists."""

    def __init__(self, app_config_path: str):
        self.app_config = app_config_path
        self.injected = False

    def visit_Assign(self, node: ast.Assign):
        # Look for INSTALLED_APPS = [...]
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'INSTALLED_APPS':
                if isinstance(node.value, ast.List):
                    # Check existence
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and elt.value == self.app_config:
                            return node

                    # Append
                    node.value.elts.append(ast.Constant(value=self.app_config))
                    self.injected = True
        return node