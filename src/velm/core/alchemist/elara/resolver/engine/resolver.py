# Path: core/alchemist/elara/resolver/engine/resolver.py
# ------------------------------------------------------

import time
import hashlib
import threading
import os
import gc
from typing import List, Optional, Any, Dict, Final, Union

# --- THE NATIVE SGF UPLINKS ---
from ...contracts.atoms import GnosticToken, TokenType, ASTNode
from ...contracts.state import ForgeContext
from ..tree_forger import SyntaxTreeForger
from ..context import LexicalScope
from ..pipeline import FilterPipeline
from ..thaw import OuroborosBreaker
from ..evaluator import AmnestyGrantedHeresy, UndefinedGnosisHeresy
from ..inclusion import InclusionEmissary
from ..inheritance import InheritanceOracle

# --- ORGANS ---
from .spooler import LaminarStreamSpooler
from .gate_router import LogicGateRouter

from ......logger import Scribe
from ......contracts.heresy_contracts import HeresySeverity

Logger = Scribe("RecursiveResolver")

class RecursiveResolver:
    """
    =============================================================================
    == THE SOVEREIGN RESOLVER (L2) (V-Ω-TOTALITY-VMAX-169-ASCENDED)            ==
    =============================================================================
    LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN[ASCENSION 169]: The "Hydraulic Yield" (time.sleep(0)) has been surgically
    incinerated from the AST Walk loop. Thread yielding is now entirely governed
    by the LaminarStreamSpooler's disk I/O, guaranteeing that pure in-memory
    AST resolution runs at raw Python execution speed without OS interruptions.
    """

    MAX_DISPATCH_DEPTH: Final[int] = 100

    def __init__(self, engine_ref: Any):
        """[THE RITE OF INCEPTION]"""
        self.engine_ref = engine_ref
        self.inclusion = InclusionEmissary(engine_ref)
        self.inheritance = InheritanceOracle(engine_ref)
        self.gate_router = LogicGateRouter(self)

        self._node_count = 0
        self._start_ns = 0
        self._lock = threading.RLock()
        self._trace_depth = threading.local()

        self._ast_macro_vault: Dict[str, ASTNode] = {}
        self._macro_execution_cache: Dict[str, List[GnosticToken]] = {}

    def resolve(
            self,
            atoms: Union[List[GnosticToken], List[ASTNode]],
            ctx: ForgeContext
    ) -> List[GnosticToken]:
        """
        =================================================================================
        == THE OMEGA RESOLVE RITE: TOTALITY                                            ==
        =================================================================================
        """
        self._start_ns = time.perf_counter_ns()
        self._node_count = 0

        _engine = self.engine_ref
        _logger = getattr(_engine, 'logger', None)
        _is_verbose = getattr(_logger, 'is_verbose', False) if _logger else False

        is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        gc_was_enabled = gc.isenabled()
        if is_adrenaline:
            gc.disable()

        # --- MOVEMENT I: POLYMORPHIC INCEPTION ---
        if atoms and isinstance(atoms[0], ASTNode):
            ast_root = ASTNode(
                token=GnosticToken(type=TokenType.VOID, content="VIRTUAL_ROOT", ln=0, col=0, raw_text=""),
                children=atoms,
                metadata={"stratum": "ADOPTED_REALITY", "is_virtual": True}
            )
            if _is_verbose:
                Logger.verbose(f"   -> [INCEPTION] Adopted AST branch: {len(atoms)} nodes.")
        else:
            ast_root = SyntaxTreeForger.forge(atoms)

        # --- MOVEMENT II: CONTEXTUAL INCEPTION ---
        global_scope = LexicalScope(ctx)
        self._inject_semantic_filters(global_scope)

        # --- MOVEMENT III: TOPOLOGICAL MORPHOGENESIS ---
        try:
            ast_root = self.inheritance.resolve_hierarchy(ast_root, global_scope)
        except Exception as e:
            if _logger: _logger.error(f"Inheritance Fracture: {e}")
            if ctx.strict_mode: raise UndefinedGnosisHeresy(f"Topological Morphogenesis shattered: {e}")

        # --- MOVEMENT IV: THE DIMENSIONAL WALK ---
        resolved_tokens: List[GnosticToken] =[]
        spooler = LaminarStreamSpooler(ctx.trace_id)

        try:
            for child in ast_root.children:
                self._walk(child, global_scope, resolved_tokens, spooler)

            # --- MOVEMENT V: METABOLIC FINALITY ---
            final_tokens = spooler.unspool(resolved_tokens)

            if _is_verbose:
                _tax_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
                Logger.success(f"Resolution complete: {len(final_tokens)} atoms manifest in {_tax_ms:.2f}ms.")

            return final_tokens

        finally:
            if is_adrenaline and gc_was_enabled:
                gc.enable()
                if len(resolved_tokens) > 5000:
                    gc.collect(1)

    def _inject_semantic_filters(self, scope: LexicalScope):
        def find_shard(query: str):
            if not self.engine_ref or not hasattr(self.engine_ref, 'cortex'): return "VOID_SHARD"
            try:
                hits = self.engine_ref.cortex.semantic_resolver.resolve(query)
                return hits[0][0].id if hits and hits[0] else "VOID"
            except Exception:
                return "VOID_FRACTURE"
        scope.local_vars["find_shard"] = find_shard

    def _walk(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: LaminarStreamSpooler):
        """
        =============================================================================
        == THE RECURSIVE CONDUCTOR (WALK)                                          ==
        =============================================================================
        """
        self._node_count += 1

        #[ASCENSION 122]: LAMINAR STREAM SPOOLING
        if self._node_count % spooler.SPOOL_THRESHOLD == 0:
            output[:] = spooler.check_and_spool(self._node_count, output)

        # [THE CURE]: The `time.sleep(0)` Hydraulic Yield has been removed from this
        # path entirely. C-Speed iteration achieved.

        # RECURSION WARD
        if not hasattr(self._trace_depth, 'val'): self._trace_depth.val = 0
        if self._trace_depth.val > self.MAX_DISPATCH_DEPTH:
            Logger.critical(f"Ouroboros Overflow: Recursion limit reached in Resolver.")
            return

        # --- THE ONTOLOGICAL TRIAGE ---

        if node.token.type == TokenType.VOID:
            for child in node.children:
                self._walk(child, scope, output, spooler)
            return

        if node.token.type == TokenType.LITERAL:
            output.append(node.token)
            return

        if node.token.type == TokenType.COMMENT:
            return

        if node.token.type == TokenType.VARIABLE:
            self._conduct_variable_resolution(node, scope, output)
            return

        if node.token.type == TokenType.LOGIC_BLOCK:
            try:
                self._trace_depth.val += 1
                self.gate_router.dispatch(node, scope, output, spooler)
            finally:
                self._trace_depth.val -= 1
            return

    def _conduct_variable_resolution(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken]):
        """THE ALCHEMICAL RECEPTOR"""
        try:
            scope.set("__start_time_ns__", time.perf_counter_ns())
            raw_expr = node.token.content
            result = FilterPipeline.execute(raw_expr, scope)
            is_binary = isinstance(result, bytes)

            if is_binary:
                final_matter = result
                is_resolved_var = False
            else:
                final_matter = str(OuroborosBreaker.thaw(result, scope, self.engine_ref))
                is_resolved_var = True

            resolved_token = GnosticToken(
                type=TokenType.LITERAL,
                content=final_matter,
                raw_text=final_matter if not is_binary else b"<BINARY_SOUL>",
                line_num=node.token.line_num,
                column_index=node.token.column_index,
                is_binary=is_binary,
                metadata={**node.token.metadata, "is_resolved_variable": is_resolved_var}
            )

            if is_binary:
                object.__setattr__(resolved_token, 'binary_payload', final_matter)

            output.append(resolved_token)

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy):
            output.append(GnosticToken(
                type=TokenType.LITERAL,
                content=node.token.raw_text,
                raw_text=node.token.raw_text,
                line_num=node.token.line_num,
                column_index=node.token.column_index,
                metadata={**node.token.metadata, "is_resolved_variable": False}
            ))

        except Exception as catastrophic_heresy:
            error_msg = f"/*[LOGIC_FRACTURE]: {str(catastrophic_heresy)} */"
            Logger.error(f"L{node.token.line_num}: Alchemical fracture: {catastrophic_heresy}")
            output.append(GnosticToken(
                type=TokenType.LITERAL,
                content=error_msg,
                raw_text=error_msg,
                line_num=node.token.line_num,
                column_index=node.token.column_index
            ))

    def __repr__(self) -> str:
        return f"<Ω_RECURSIVE_RESOLVER atoms={self._node_count} status=RESONANT mode=VMAX_169_O1_SUTURE>"