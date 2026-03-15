# Path: utils/gnosis_discovery/visitor.py
# ---------------------------------------

"""
=================================================================================
== THE GNOSTIC AST VISITOR: TOTALITY (V-Ω-SGF-NATIVE-V3.1-ASCENDED)            ==
=================================================================================
LIF: ∞^∞ | ROLE: SYMBOLIC_REASONING_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_VISITOR_V3_1_FILTER_SUTURE_FINALIS_2026

[THE MANIFESTO]
Jinja is dead. This is the supreme Retinal Nerve of the Gnostic Inquisitor.
It performs deep-tissue biopsies on Python Abstract Syntax Trees to identify
the exact Gnosis required for reality manifestation.

It has been hyper-evolved to possess "Recursive Filter Suture" and
"Subscript Path Inception", annihilating the "Void Root" paradox.
=================================================================================
"""

import ast
import logging
from typing import Set, Dict, Any, Optional, List, Final

from ...logger import Scribe

Logger = Scribe("GnosticDiscovery")


class GnosticASTVisitor(ast.NodeVisitor):
    """
    =============================================================================
    == THE TOPOLOGICAL MIND-WALKER (V-Ω-SGF-TOTALITY-V3.1)                     ==
    =============================================================================
    LIF: 1,000,000 | ROLE: SYMBOLIC_TRACER | RANK: OMEGA

    Walks the Native Python AST of an SGF expression to identify Required Gnosis.
    Now perfectly aligned with the OmegaInquisitor's metabolic expectations.
    """

    # [ASCENSION 3]: THE RESERVED IDENTITY MOAT
    # These names are intrinsic to the God-Engine or Python's core and are
    # righteously ignored by the requirement inquisitor.
    RESERVED_MOAT: Final[Set[str]] = {
        # Python Primitives & Keywords
        'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple', 'bytes',
        'len', 'range', 'enumerate', 'zip', 'any', 'all', 'sum', 'max', 'min',
        'abs', 'round', 'pow', 'divmod', 'sorted', 'reversed', 'filter', 'map',
        'getattr', 'setattr', 'hasattr', 'isinstance', 'issubclass', 'type',
        'id', 'hash', 'repr', 'str', 'format', 'vars', 'dir', 'hex', 'bin', 'oct',
        'True', 'False', 'None', 'NotImplemented', 'Ellipsis', '__debug__',

        # SGF / Velm Native Rites & Proxies
        'logic', 'crypto', 'time', 'os', 'path', 'topo', 'akasha', 'iron', 'substrate',
        'now', 'uuid', 'uuid_v4', 'secret', 'shell', 'timestamp', 'random_id',
        'project_root', 'trace_id', 'session_id', 'vitals', 'loop', 'self', 'super',
        'default', 'd', 'defined', 'undefined', 'iterable', 'mapping', 'string',
        'file_exists', 'dir_exists', 'read_file', 'is_python', 'is_node', 'is_rust',

        # Common Loop/Temporary Identities [ASCENSION 14]
        'i', 'j', 'k', 'x', 'y', 'z', 'v', 'k', 'val', 'key', 'item', 'e', 'err'
    }

    def __init__(self, local_scope_override: Set[str] = None):
        """[THE RITE OF INCEPTION]"""
        # Variables that the Architect MUST provide
        self.required_vars: Set[str] = set()

        # [ASCENSION 1]: THE FILTER SUTURE (THE MASTER CURE)
        # We must track which alchemical filters are summoned to infer types.
        self.filters_used: Set[str] = set()

        # Variables defined within the logic (e.g., loop variables)
        self.local_scope: Set[str] = local_scope_override or set()

        # Forensic Metadata & Complexity Tomography
        self.inferred_types: Dict[str, str] = {}
        self.attributes_accessed: Dict[str, Set[str]] = {}
        self.functions_summoned: Set[str] = set()
        self.total_complexity: int = 0

    def discover(self, expression: str):
        """
        =============================================================================
        == THE RITE OF DISCOVERY                                                   ==
        =============================================================================
        Surgically parses the SGF expression and ignites the walk.
        """
        try:
            # Strip SGF braces if they survived the extractor
            clean_expr = expression.replace('{{', '').replace('}}', '').strip()
            if not clean_expr:
                return

            # [STRIKE]: Parse into native Python AST
            # mode='eval' is the fastest and safest for single expressions
            tree = ast.parse(clean_expr, mode='eval')
            self.visit(tree.body)

        except Exception as e:
            # [ASCENSION 11]: AMNESTY PROTOCOL
            # If the expression fractures (e.g. valid React JSX inside {{ }}),
            # we grant Amnesty. The Inquisitor will handle the regex fallback.
            Logger.debug(f"   -> Amnesty Granted: Expression '{expression[:30]}...' failed AST scry.")

    # =========================================================================
    # == THE ATOMS OF PERCEPTION (VISITORS)                                  ==
    # =========================================================================

    def visit_Name(self, node: ast.Name):
        """
        Perceives a variable usage event.
        Logic: If we LOAD a name, and it is NOT Local or Reserved, it is a Requirement.
        """
        self.total_complexity += 1

        if isinstance(node.ctx, ast.Load):
            name = node.id
            if name not in self.local_scope and name not in self.RESERVED_MOAT:
                # [ASCENSION 2]: Underscore Redaction (Dunder-Safe)
                if not name.startswith('__'):
                    self.required_vars.add(name)

        elif isinstance(node.ctx, ast.Store):
            # [ASCENSION 3]: Local Inscription.
            self.local_scope.add(node.id)

    def visit_Attribute(self, node: ast.Attribute):
        """
        Handles `user.profile.id` access.
        [ASCENSION 4]: ATTRIBUTE CLAIRVOYANCE.
        Identifies the root object as the requirement while chronicling the path.
        """
        self.total_complexity += 1

        root_name = self._get_root_name(node)
        if root_name:
            if root_name not in self.local_scope and root_name not in self.RESERVED_MOAT:
                self.required_vars.add(root_name)

            # [ASCENSION 12]: Structural Metadata Inception
            if root_name not in self.attributes_accessed:
                self.attributes_accessed[root_name] = set()
            self.attributes_accessed[root_name].add(node.attr)

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        """
        [ASCENSION 2]: SUBSCRIPT PATH INCEPTION.
        Handles `my_list[0]` or `my_dict['key']`.
        Identifies the container as the requirement.
        """
        self.total_complexity += 1

        root_name = self._get_root_name(node.value)
        if root_name:
            if root_name not in self.local_scope and root_name not in self.RESERVED_MOAT:
                self.required_vars.add(root_name)

        # We also visit the slice/index in case a variable is used there: my_dict[key_var]
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """
        [ASCENSION 5 & 18]: FUNCTION CALL DISTINCTION.
        Distinguishes between variables and functional artisans.
        """
        self.total_complexity += 2  # Higher weight for logic branches

        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            # [ASCENSION 1]: THE MASTER FIX
            # If the call is not a Python builtin, it is likely an SGF Filter or Rite.
            if func_name not in self.RESERVED_MOAT:
                self.filters_used.add(func_name)

            self.functions_summoned.add(func_name)

        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda):
        """
        [ASCENSION 4]: LAMBDA-FOLD TOMOGRAPHY.
        Surgically separates local lambda arguments from external dependencies.
        """
        self.total_complexity += 3

        # 1. Capture arguments and add to local scope
        original_scope = self.local_scope.copy()
        for arg in node.args.args:
            self.local_scope.add(arg.arg)

        # 2. Visit the body (expression)
        self.visit(node.body)

        # 3. Revert scope to prevent leakage
        self.local_scope = original_scope

    def visit_For(self, node: ast.For):
        """
        [ASCENSION 6]: LOOP SCOPING.
        Righteously identifies loop targets as local.
        """
        self.total_complexity += 5

        # 1. Scry the target (item in items)
        for target_node in ast.walk(node.target):
            if isinstance(target_node, ast.Name):
                self.local_scope.add(target_node.id)

        # 2. Scry the iterable (items)
        self.visit(node.iter)

        # 3. Walk the body with the newly waked local scope
        for child in node.body:
            self.visit(child)

    def visit_ListComp(self, node: ast.ListComp):
        """[ASCENSION 8]: BICAMERAL COMPREHENSION PHYSICS."""
        self._handle_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp):
        """[ASCENSION 8]: BICAMERAL COMPREHENSION PHYSICS."""
        self._handle_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp):
        """[ASCENSION 8]: BICAMERAL COMPREHENSION PHYSICS."""
        self._handle_comprehension(node)

    def _handle_comprehension(self, node: Any):
        """Unified logic for all comprehension types."""
        self.total_complexity += 4

        # Comprehension variables are strictly local to the thought
        original_scope = self.local_scope.copy()

        for gen in node.generators:
            for target_node in ast.walk(gen.target):
                if isinstance(target_node, ast.Name):
                    self.local_scope.add(target_node.id)
            self.visit(gen.iter)
            # Visit if-guards in generators
            for if_clause in gen.ifs:
                self.visit(if_clause)

        # Visit the element/key/value being yielded
        if isinstance(node, ast.DictComp):
            self.visit(node.key)
            self.visit(node.value)
        else:
            self.visit(node.elt)

        self.local_scope = original_scope

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _get_root_name(self, node: Optional[ast.AST]) -> Optional[str]:
        """
        [ASCENSION 7]: CAUSAL RECURSION.
        Deeply scries an attribute or subscript chain to find the ancestral root.
        `user.profile.id` -> `user`
        """
        if node is None: return None

        # [ASCENSION 5]: NoneType Sarcophagus
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return self._get_root_name(node.value)
        elif isinstance(node, ast.Subscript):
            return self._get_root_name(node.value)
        elif isinstance(node, ast.Call):
            # For calls like `get_user().id`, the root is the function call
            # which is handled by visit_Call. We continue recursing down the chain.
            return self._get_root_name(node.func)
        return None

    def generic_visit(self, node: ast.AST):
        """[ASCENSION 5]: NoneType Sarcophagus."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

    def __repr__(self) -> str:
        return (f"<Ω_GNOSTIC_VISITOR requirements={len(self.required_vars)} "
                f"filters={len(self.filters_used)} complexity={self.total_complexity} "
                f"status=RESONANT>")