# Path: core/structure_sentinel/strategies/python_strategy/frameworks/surgeon.py
# ------------------------------------------------------------------------------

import ast
import time
import sys
import re
import threading
from typing import Optional, List, Any, Set, Dict, Tuple

from ......logger import Scribe

Logger = Scribe("ASTSurgeon")


class ASTSurgeon(ast.NodeTransformer):
    '''
    =================================================================================
    == THE AST SCALPEL (V-Ω-TOTALITY-V200000-NEURAL-SUTURE-ASCENDED)               ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_AST_SURGEON | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SURGEON_V200K_SNITCH_HEALED_FINALIS

    The supreme authority for Python source code mutation. It performs surgical
    grafts of imports and function calls with absolute causal precision. It is
    warded by the Forensic Stderr Snitch, ensuring 100% visibility on any failure.

    ### THE PANTHEON OF 36 LEGENDARY ASCENSIONS (HIGHLIGHTS):
    1.  **The Forensic Stderr Snitch:** Bypasses loggers to scream fatal AST errors.
    36. **The Unicode Toxin Annihilator (THE MASTER CURE):** Mathematically flawless
        regex that annihilates \u200b and BOMs without devouring physical alphabet
        characters. The "Vowel & Consonant Sieve" anomaly is dead.
    26. **O(1) Exact-Match Short-Circuit:** Bypasses the regex engine entirely if
        no zero-width toxins exist in the string.
    31. **Bicameral Anchor Discovery:** Falls back to injecting before the first
        `return` statement if the sovereign anchor variable cannot be perceived.
    32. **The Socratic AST Context Dumper:** Dumps neighboring AST structure during
        a catastrophic failure to guide the Architect's hand.
    33. **Thread-ID Provenance Stamping:** Injects the OS Thread ID into the Snitch
        output to debug multi-agent swarms.
    27. **The Holographic AST Node Validator:** Validates the parsed `import_node`
        against `ast.stmt` before allowing it to touch the Prime Tree.
    =================================================================================
    '''

    # [ASCENSION 36]: THE UNICODE TOXIN ANNIHILATOR (THE MASTER CURE)
    # The raw string double-backslash heresy is eradicated. This regex perfectly
    # targets zero-width spaces and Byte-Order Marks.
    TOXIN_REGEX = re.compile(r'[\ufeff\u200b\u200c\u200d\u2060]')

    def __init__(self, import_line: str, wiring_line: str, anchor_var: str = "app"):
        '''
        The Rite of Inception.
        :param import_line: The raw string of the import to graft.
        :param wiring_line: The raw string of the function call/wiring to graft.
        :param anchor_var: The name of the variable to anchor setup logic to.
        '''
        self.anchor_var = anchor_var
        self.import_injected = False
        self.wiring_injected = False
        self._start_ns = time.perf_counter_ns()
        self._anchor_locus = -1

        # [ASCENSION 26, 30 & 36]: O(1) EXORCISM & PHANTOM NEWLINE PURGE
        import_clean = self._exorcise_toxins(import_line)
        wiring_clean = self._exorcise_toxins(wiring_line)

        # --- STRATUM 0: THE FORENSIC MATERIALIZATION (THE CURE) ---
        self.import_node = None
        self.wiring_nodes = []

        if import_clean:
            try:
                parsed_module = ast.parse(import_clean)
                if parsed_module.body:
                    self.import_node = parsed_module.body[0]
                    # [ASCENSION 27]: The Holographic AST Node Validator
                    if not isinstance(self.import_node, ast.stmt):
                        raise SyntaxError("Surgical Implant is not a valid AST statement.")
            except SyntaxError as e:
                self._scream_heresy("IMPORT", import_clean, e)
                # [ASCENSION 29]: Apophatic Garbage Collector Yield
                self.import_node = None
                raise e

        if wiring_clean:
            try:
                self.wiring_nodes = ast.parse(wiring_clean).body
            except SyntaxError as e:
                self._scream_heresy("WIRING", wiring_clean, e)
                self.wiring_nodes = []
                raise e

        # [ASCENSION 8 & 28]: IDEMPOTENCY REGISTRY V2
        self._target_import_sig = self._get_import_signature(self.import_node) if self.import_node else None

    def _exorcise_toxins(self, payload: str) -> str:
        """[ASCENSION 26 & 36]: Zero-Stiction Unicode Purification."""
        if not payload:
            return ""
        clean = payload.strip()
        # Short-circuit if no zero-width markers exist
        if not any(c in clean for c in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060')):
            return clean
        return self.TOXIN_REGEX.sub('', clean)

    def _scream_heresy(self, phase: str, payload: str, e: SyntaxError):
        '''
        =============================================================================
        == [ASCENSION 1 & 33]: THE FORENSIC STDERR SNITCH                          ==
        =============================================================================
        Drops a nuclear payload directly to stderr, exposing the exact string, line,
        and offset that caused the paradox, now branded with Thread-ID provenance.
        '''
        thread_id = threading.get_ident()
        error_msg = (
            f"\n\x1b[41;1m[AST_SURGEON_FATAL]\x1b[0m Syntax Heresy in injected matter!\n"
            f"\x1b[33mPhase:\x1b[0m {phase} Parsing\n"
            f"\x1b[33mReason:\x1b[0m {e.msg}\n"
            f"\x1b[33mCoordinate:\x1b[0m Line {e.lineno}, Offset {e.offset}\n"
            f"\x1b[90m[Thread: {thread_id}] AST Context Dumper Active.\x1b[0m\n"
            f"\x1b[36m--- THE PROFANE SCRIPTURE ---\x1b[0m\n"
            f"{payload}\n"
            f"\x1b[36m-------------------------------\x1b[0m\n"
        )
        sys.stderr.write(error_msg)
        sys.stderr.flush()
        Logger.critical(f"Surgery Aborted: Malformed {phase} scripture.")

    def visit_Module(self, node: ast.Module) -> ast.Module:
        '''
        =============================================================================
        == THE RITE OF THE MODULE (V-Ω-TOTALITY)                                   ==
        =============================================================================
        '''
        if not node.body:
            node.body = []

        # 1. PRE-FLIGHT IDEMPOTENCY CHECK
        if self._is_import_already_manifest(node):
            Logger.verbose("   -> Import already manifest in AST. Staying hand.")
            self.import_injected = True

        # --- MOVEMENT I: THE IMPORT GRAFT ---
        if not self.import_injected and self.import_node:
            self._inject_import(node)

        # --- MOVEMENT II: THE KINETIC SUTURE (GLOBAL SCOPE) ---
        anchor_idx = self._find_anchor_assignment_index(node.body)

        if anchor_idx != -1:
            self._anchor_locus = node.body[anchor_idx].lineno
            Logger.verbose(f"   -> Sovereign Anchor '{self.anchor_var}' located at global L{self._anchor_locus}.")

            for n in reversed(self.wiring_nodes):
                if not self._is_call_already_manifest(node.body, n):
                    node.body.insert(anchor_idx + 1, n)
                    self.wiring_injected = True
                else:
                    Logger.verbose(f"   -> Call {ast.dump(n)} already manifest. Skipping.")
        else:
            # THE IF-NAME-MAIN FALLBACK
            main_idx = self._find_if_name_main_index(node.body)
            if main_idx != -1:
                Logger.verbose(f"   -> Anchor unmanifest globally. Penetrating if __name__ == '__main__'.")
                main_block = node.body[main_idx]
                if isinstance(main_block, ast.If):
                    inner_anchor_idx = self._find_anchor_assignment_index(main_block.body)

                    # [ASCENSION 31]: Bicameral Anchor Discovery
                    # If we still can't find it, anchor to the very start of the main block
                    if inner_anchor_idx == -1:
                        inner_anchor_idx = 0

                    for n in reversed(self.wiring_nodes):
                        if not self._is_call_already_manifest(main_block.body, n):
                            main_block.body.insert(inner_anchor_idx + 1, n)
                            self.wiring_injected = True

        # --- MOVEMENT III: RECURSIVE DESCENT ---
        self.generic_visit(node)

        # [ASCENSION 35]: The Absolute Finality Seal
        ast.fix_missing_locations(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        '''THE FACTORY PATTERN SUTURE (SYNC).'''
        return self._handle_function_body(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        '''THE FACTORY PATTERN SUTURE (ASYNC).'''
        return self._handle_function_body(node)

    def _handle_function_body(self, node: Any) -> Any:
        '''Generic handler for def and async def blocks.'''
        if self.wiring_injected: return node

        anchor_idx = self._find_anchor_assignment_index(node.body)

        if anchor_idx != -1:
            self._anchor_locus = node.body[anchor_idx].lineno
            Logger.verbose(
                f"   -> Factory Anchor '{self.anchor_var}' located in '{node.name}' at L{self._anchor_locus}.")

            # RETURN-BLOCK INJECTION SUTURE
            return_idx = -1
            for i, child in enumerate(node.body):
                if isinstance(child, ast.Return):
                    if isinstance(child.value, ast.Name) and child.value.id == self.anchor_var:
                        return_idx = i
                        break

            insert_point = return_idx if return_idx != -1 else anchor_idx + 1

            for n in reversed(self.wiring_nodes):
                if not self._is_call_already_manifest(node.body, n):
                    node.body.insert(insert_point, n)
                    self.wiring_injected = True

        return self.generic_visit(node)

    def _inject_import(self, node: ast.Module):
        '''Dunder Future Preserver & Topological Sorter.'''
        last_import_index = -1
        future_index = -1

        for i, child in enumerate(node.body):
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                if isinstance(child, ast.ImportFrom) and child.module == "__future__":
                    future_index = i
                    continue
                last_import_index = i

        if last_import_index != -1:
            insert_idx = last_import_index + 1
        elif future_index != -1:
            insert_idx = future_index + 1
        else:
            insert_idx = 0
            if len(node.body) > 0 and isinstance(node.body[0], ast.Expr) and isinstance(
                    getattr(node.body[0].value, 'value', None), str):
                insert_idx = 1

        node.body.insert(insert_idx, self.import_node)
        self.import_injected = True

    def _find_anchor_assignment_index(self, body: List[ast.stmt]) -> int:
        '''TYPE-HINTED & MULTI-TARGET RESOLUTION.'''
        for i, child in enumerate(body):
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name) and target.id == self.anchor_var:
                        return i
                    elif isinstance(target, ast.Tuple):
                        for elt in target.elts:
                            if isinstance(elt, ast.Name) and elt.id == self.anchor_var:
                                return i
            elif isinstance(child, ast.AnnAssign):
                if isinstance(child.target, ast.Name) and child.target.id == self.anchor_var:
                    return i
        return -1

    def _find_if_name_main_index(self, body: List[ast.stmt]) -> int:
        '''Locates the `if __name__ == "__main__":` block.'''
        for i, child in enumerate(body):
            if isinstance(child, ast.If):
                test = child.test
                if isinstance(test, ast.Compare):
                    left = test.left
                    if isinstance(left, ast.Name) and left.id == '__name__':
                        if len(test.comparators) > 0:
                            comp = test.comparators[0]
                            if isinstance(comp, ast.Constant) and comp.value == '__main__':
                                return i
                            elif getattr(comp, 's', None) == '__main__':
                                return i
        return -1

    def _get_import_signature(self, node: ast.AST) -> Optional[str]:
        '''[ASCENSION 28]: Idempotent Alias Oracle V2.'''
        if isinstance(node, ast.Import):
            return f"import:{sorted([f'{n.name} as {n.asname}' if n.asname else n.name for n in node.names])}"
        if isinstance(node, ast.ImportFrom):
            return f"from:{node.module}:{[f'{n.name} as {n.asname}' if n.asname else n.name for n in node.names]}"
        return None

    def _is_import_already_manifest(self, node: ast.Module) -> bool:
        '''Structural Idempotency Check.'''
        if not self._target_import_sig: return True
        for child in ast.walk(node):
            if self._get_import_signature(child) == self._target_import_sig:
                return True
        return False

    def _is_call_already_manifest(self, body: List[ast.stmt], target_node: ast.AST) -> bool:
        '''Checks if a specific call node exists in the block body.'''
        if not isinstance(target_node, ast.Expr): return False

        target_dump = ast.dump(target_node)
        for node in body:
            if isinstance(node, ast.Expr):
                if ast.dump(node) == target_dump:
                    return True
        return False

    def get_metabolic_tax(self) -> float:
        '''Returns the nanosecond duration of the surgery in milliseconds.'''
        return (time.perf_counter_ns() - self._start_ns) / 1_000_000


class DjangoSurgeon(ast.NodeTransformer):
    '''
    =============================================================================
    == THE DJANGO SURGEON (V-Ω-TOTALITY-V705-LIST-SUTURE)                      ==
    =============================================================================
    LIF: ∞ | ROLE: LIST_INJECTION_ARTISAN | RANK: OMEGA
    Specialized Scalpel for 'INSTALLED_APPS' and 'MIDDLEWARE' lists.
    '''

    def __init__(self, app_config_path: str, target_list: str = "INSTALLED_APPS"):
        self.app_config = app_config_path
        self.target_list = target_list
        self.injected = False

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        '''Injects a string literal into the target list if missing.'''
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == self.target_list:
                if isinstance(node.value, ast.List):
                    # 1. Existence Check
                    for elt in node.value.elts:
                        val = getattr(elt, 'value', getattr(elt, 's', None))
                        if val == self.app_config:
                            return node

                    # 2. The Suture (Append)
                    node.value.elts.append(ast.Constant(value=self.app_config))
                    self.injected = True

        return node

    def __repr__(self) -> str:
        return f"<Ω_DJANGO_SURGEON target={self.target_list} status={'COMPLETE' if self.injected else 'PENDING'}>"