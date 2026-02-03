# Path: parser_core/lfg_builder/builders/codebase_python.py
# ----------------------------------------------------------

import ast
from pathlib import Path
from ..contracts import LogicFlowGraph, NodeShape


class PythonFlowBuilder:
    """
    Analyzes a Python file to visualize its Control Flow Graph (CFG) at a high level.
    """

    def build(self, file_path: Path) -> LogicFlowGraph:
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
        except Exception:
            return LogicFlowGraph(title=f"Error parsing {file_path.name}")

        graph = LogicFlowGraph(title=file_path.name)

        # We perform a recursive walk to build the graph
        self._walk(tree, graph, None)
        return graph

    def _walk(self, node: ast.AST, graph: LogicFlowGraph, parent_id: str = None):
        """Recursive AST walker that generates nodes."""

        current_id = None

        # 1. Functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            current_id = f"func_{node.lineno}"
            graph.add_node(current_id, f"def {node.name}()", NodeShape.SUBROUTINE)
            # Functions don't strictly connect to their container in flow,
            # but we can link them for structural visualization.

        # 2. Classes
        elif isinstance(node, ast.ClassDef):
            current_id = f"class_{node.lineno}"
            graph.add_node(current_id, f"class {node.name}", NodeShape.CYLINDER)
            # If we want to visualize method containment, we could use subgraphs.
            # For flow, classes are just containers.

        # 3. Control Flow (If)
        elif isinstance(node, ast.If):
            current_id = f"if_{node.lineno}"
            test_code = ast.unparse(node.test)
            graph.add_node(current_id, f"if {test_code}?", NodeShape.DIAMOND)
            if parent_id:
                graph.add_edge(parent_id, current_id)

            # Recurse Body (True branch)
            last_true_id = current_id
            for child in node.body:
                child_id = self._walk(child, graph, last_true_id)
                if child_id: last_true_id = child_id

            # Recurse Else (False branch)
            last_false_id = current_id
            for child in node.orelse:
                child_id = self._walk(child, graph, last_false_id)
                if child_id: last_false_id = child_id

            return current_id  # Return the split point? No, flow graphs are complex.
            # For V1 visualization, we just map structure, not full CFG execution paths.

        # 4. Loops
        elif isinstance(node, (ast.For, ast.While)):
            current_id = f"loop_{node.lineno}"
            label = "Loop"
            if isinstance(node, ast.For): label = f"For {ast.unparse(node.target)}"
            graph.add_node(current_id, label, NodeShape.PARALLELOGRAM)
            if parent_id: graph.add_edge(parent_id, current_id)

            last_loop_id = current_id
            for child in node.body:
                child_id = self._walk(child, graph, last_loop_id)
                if child_id: last_loop_id = child_id

        # 5. Calls (Significant Actions)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Name):
                current_id = f"call_{node.lineno}"
                graph.add_node(current_id, f"{call.func.id}()", NodeShape.RECTANGLE)
                if parent_id: graph.add_edge(parent_id, current_id)

        # Generic Recurse for things we didn't handle explicitly but contain logic
        else:
            for child in ast.iter_fields(node):
                if isinstance(child[1], list):
                    for item in child[1]:
                        if isinstance(item, ast.AST):
                            self._walk(item, graph, parent_id)
                elif isinstance(child[1], ast.AST):
                    self._walk(child[1], graph, parent_id)

        return current_id