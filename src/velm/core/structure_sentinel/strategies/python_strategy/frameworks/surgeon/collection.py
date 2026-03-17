# ---------------------------------------------------------------------------------
# FILE: collection.py
# ---------------------------------------------------------------------------------
import ast
from typing import Any, Optional
from .......logger import Scribe

Logger = Scribe("GnosticCollectionSurgeon")

class GnosticCollectionSurgeon(ast.NodeTransformer):
    """
    =============================================================================
    == THE GNOSTIC COLLECTION SURGEON (LIF: INFINITY)                          ==
    =============================================================================
    LIF: ∞^∞ | ROLE: NESTED_DATA_MUTATOR | RANK: OMEGA_SURGEON

    This specialized artisan surgically penetrates Lists, Tuples, Sets, and
    Dictionaries willed as globals or class attributes (e.g. MIDDLEWARE).
    It righteously enforces the Law of the Unique Atom.
    """

    def __init__(self, target_val: Any, target_name: str, key: Optional[str] = None):
        self.target_val = target_val
        self.target_name = target_name
        self.dict_key = key
        self.injected = False

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == self.target_name:
                if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                    for elt in node.value.elts:
                        val = getattr(elt, 'value', getattr(elt, 's', None))
                        if val == self.target_val:
                            return node
                    node.value.elts.append(ast.Constant(value=self.target_val))
                    self.injected = True
                    return node

                if isinstance(node.value, ast.Dict) and self.dict_key is not None:
                    for k, v in zip(node.value.keys, node.value.values):
                        if k and getattr(k, 'value', getattr(k, 's', None)) == self.dict_key:
                            v.value = self.target_val
                            self.injected = True
                            return node

                    node.value.keys.append(ast.Constant(value=self.dict_key))
                    node.value.values.append(ast.Constant(value=self.target_val))
                    self.injected = True
                    return node
        return node

    def __repr__(self) -> str:
        return f"<Ω_COLLECTION_SURGEON target={self.target_name} status={'COMPLETE' if self.injected else 'PENDING'}>"