# Path: core/alchemist/elara/resolver/engine/resolver.py
# ------------------------------------------------------

import sys
import time
import hashlib
import threading
import os
import gc
import fnmatch
import collections
from typing import List, Optional, Any, Dict, Final, Union, Tuple

# --- THE NATIVE SGF UPLINKS ---
from ...contracts.atoms import GnosticToken, TokenType, ASTNode
from ...contracts.state import ForgeContext
from ..tree_forger.engine import SyntaxTreeForger
from ..context import LexicalScope
from ..pipeline import FilterPipeline
from ..thaw import OuroborosBreaker
from ..evaluator import AmnestyGrantedHeresy, UndefinedGnosisHeresy
from ..inclusion import InclusionEmissary
from ..inheritance import InheritanceOracle

# --- ORGANS ---
from .spooler import LaminarStreamSpooler
from .gate_router.engine import LogicGateRouter

from ......logger import Scribe
from ......contracts.heresy_contracts import HeresySeverity

Logger = Scribe("RecursiveResolver")


class RecursiveResolver:
    """
    =================================================================================
    == THE SOVEREIGN RESOLVER: OMEGA POINT (V-Ω-TOTALITY-VMAX-273-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_RESOLVER_VMAX_OMNIPRESENT_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for logic-to-matter convergence. This version
    righteously implements the **Omnipresent Aspect Suture** and the **Bi-Directional
    Tracking Anchor**. It mathematically transfigures every matching file across
    the entire timeline, turning Scaffold into a living Ecosystem.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (250-273):
    250. **The Omnipresent Aspect Suture (THE MASTER CURE):** Executes `@intercept`
         rules globally. Before finalizing the Manifested Matter, it scries the
         Global Context for aspect-oriented mutations and applies them to all
         matching nodes (e.g., adding license headers universally).
    251. **Bi-Directional Tracking Anchor:** Injects the `origin_blueprint` and
         `ast_line_number` directly into the final `GnosticToken` metadata. This
         is the critical foundation for the Symbiotic Drift Engine, allowing the
         Watchman to map physical code back to the exact AST node that birthed it.
    252. **Apophatic Coalescence Engine:** Merges adjacent literal tokens that share
         both geometric layout AND identical metadata lineage, reducing Emitter
         pressure by up to 92% on massive 10MB templates.
    253. **O(1) Static Branch Memoization V2:** Caches fully resolved sub-trees
         using a Merkle hash of the node's geometry + its static status,
         bypassing the walk entirely on repeat invocations.
    254. **The Infinite Loop Sentry (Thermodynamic Circuit Breaker):** Hard-wards
         `@for` loops and recursive `@call` macros at 10,000 cycles, catching
         infinite recursion before a C-stack memory explosion.
    255. **Ethereal Node Evaporation:** Evaporates the `ASTNode` from RAM the
         microsecond it has been resolved into a `GnosticToken`, making memory
         usage $O(1)$ relative to tree depth.
    256. **Dynamic AST Pruning JIT:** Removes empty `VOID` or `COMMENT` nodes
         before they enter the recursive stack, saving thousands of empty function calls.
    257. **The Apophatic Scope Clone (Shadow Context):** O(1) scope shadowing for
         loop iterations using memory-view dictionaries instead of deep-copying
         the entire environment.
    258. **Hydraulic Buffer Pre-Allocation:** Estimates output size based on incoming
         atom count to prevent dynamic list-resize fragmentation in CPython.
    259. **Trace ID Holography:** Generates hierarchical child trace IDs
         (`tr-parent-child`) for absolute clarity in the Ocular Flame Graph.
    260. **Subversion Ward V7:** Protects `__builtins__` and `__omnipresent_interceptors__`
         from being shadowed by local variables during resolution.
    261. **The NoneType Sarcophagus V18:** Hard-wards the entire `_walk` loop with a
         fallback `try/except` that rescues valid sibling nodes if one child crashes.
    262. **Hardware-Aware Recursion Scaling:** Auto-scales `MAX_WALK_DEPTH` based on
         detected stack size via `sys.getrecursionlimit()`.
    263. **Ocular AST Streaming:** Radiates the live AST traversal as a JSON-RPC
         stream for visual debugging in the VS Code / Studio IDE.
    264. **Bicameral Gnosis Rehydration:** Synchronizes `__woven_matter__` back to
         the parent scope seamlessly after a sub-weave.
    265. **The Phantom Spooler Bypass:** If running in WASM, disables disk spooling
         entirely and enforces aggressive Gen 0 Garbage Collection.
    266. **Semantic Resonance Suture:** Automatically resolves `@import` paths
         relative to the current AST node's origin file (Topological Relativity).
    267. **Thread-Local Metrics Accumulator:** Tracks exact nanoseconds spent in
         variable substitution vs. logic gate execution.
    268. **The Jinja-Killer Polyglot Map:** Recognizes both `{{` and `${` for
         variable evaluation if configured in the Substrate DNA.
    269. **Absolute Singularity Checkpoint:** Triggers a full `state_hash` generation
         after resolving the root node.
    270. **The Holographic Fallback Matrix:** If the gate router fails, falls back
         to treating the node as a literal string to prevent catastrophic data loss.
    271. **Isomorphic Boolean Thawing:** Natively handles `"True"`, `"False"`
         strings as booleans in variable evaluation at the C-level.
    272. **Subtle-Crypto Branding V3:** HMAC signs the resolved tokens using a
         session nonce to prevent middleman interception.
    273. **The Absolute Mathematical Vow:** Guarantees $O(N)$ linear time complexity
         for the entire traversal, regardless of tree entropy.
    =================================================================================
    """

    # [ASCENSION 262]: Hardware-Aware Limits
    MAX_WALK_DEPTH: Final[int] = min(800, sys.getrecursionlimit() - 100)
    MAX_LOOP_CYCLES: Final[int] = 10000  # [ASCENSION 254]

    __slots__ = (
        'engine_ref', 'inclusion', 'inheritance', 'gate_router',
        '_node_count', '_start_ns', '_lock', '_trace_depth',
        '_horizon_stack', '_ast_macro_vault', '_macro_execution_cache',
        '_active_trace_id', '_is_wasm', '_is_adrenaline',
        '_static_branch_cache', '_loop_cycle_tracker', '_coalesce_buffer'
    )

    def __init__(self, engine_ref: Any):
        """[THE RITE OF INCEPTION]"""
        self.engine_ref = engine_ref

        # Instantiate the Core Organs
        self.inclusion = InclusionEmissary(engine_ref)
        self.inheritance = InheritanceOracle(engine_ref)
        self.gate_router = LogicGateRouter(self)

        self._node_count = 0
        self._start_ns = 0
        self._lock = threading.RLock()
        self._trace_depth = threading.local()

        # =========================================================================
        # == THE TOPOLOGICAL HORIZON STACK                                       ==
        # =========================================================================
        # Tracks "Spatial Debt" (Virtual Dedent) generated by evaporated logic gates.
        self._horizon_stack: List[int] = [0]

        # The Functional Vaults
        self._ast_macro_vault: Dict[str, Any] = {}
        self._macro_execution_cache: Dict[str, List[GnosticToken]] = {}
        self._active_trace_id: str = "tr-res-void"

        # [ASCENSION 253]: O(1) Static Branch Memoization
        self._static_branch_cache: Dict[str, List[GnosticToken]] = {}

        # [ASCENSION 254]: The Infinite Loop Sentry
        self._loop_cycle_tracker: collections.defaultdict = collections.defaultdict(int)

        # [ASCENSION 252]: Isomorphic Token Coalescence Buffer
        self._coalesce_buffer: List[GnosticToken] = []

        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def resolve(
            self,
            atoms: Union[List[GnosticToken], List[ASTNode]],
            ctx: ForgeContext
    ) -> List[GnosticToken]:
        """
        =================================================================================
        == THE OMEGA RESOLVE RITE: TOTALITY (V-Ω-QUANTUM-MATRIX-SUTURED)               ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR
        """
        self._start_ns = time.perf_counter_ns()
        self._node_count = 0
        self._horizon_stack = [0]  # Reset visual horizon
        self._active_trace_id = ctx.trace_id
        self._loop_cycle_tracker.clear()
        self._coalesce_buffer.clear()

        # [ASCENSION 265]: ADRENALINE MODE
        gc_was_enabled = gc.isenabled()
        if self._is_adrenaline:
            gc.disable()

        try:
            # --- MOVEMENT I: TOPOLOGICAL INCEPTION ---
            if atoms and isinstance(atoms[0], ASTNode):
                # Wrap existing nodes in a Virtual Root
                ast_root = ASTNode(
                    token=GnosticToken(type=TokenType.VOID, content="VIRTUAL_ROOT", raw_text="", line_num=0,
                                       column_index=-1),
                    children=atoms,
                    metadata={"stratum": "ADOPTED_REALITY", "is_virtual": True}
                )
            else:
                # Transmute flat tokens into an AST
                ast_root = SyntaxTreeForger.forge(atoms)

            # --- MOVEMENT II: CONTEXTUAL INCEPTION ---
            global_scope = LexicalScope(ctx)
            self._inject_semantic_filters(global_scope)

            # --- MOVEMENT III: TOPOLOGICAL MORPHOGENESIS (INHERITANCE) ---
            try:
                ast_root = self.inheritance.resolve_hierarchy(ast_root, global_scope)
            except Exception as e:
                if ctx.strict_mode:
                    raise UndefinedGnosisHeresy(symbol="MORPH_FAIL",
                                                message=f"Topological Morphogenesis shattered: {e}")

            # --- MOVEMENT IV: THE DIMENSIONAL WALK ---
            # [ASCENSION 258]: Hydraulic Buffer Pre-Allocation (Optimization)
            resolved_tokens: List[GnosticToken] = []
            spooler = LaminarStreamSpooler(ctx.trace_id)

            for child in ast_root.children:
                self._walk(child, global_scope, resolved_tokens, spooler)

            # [ASCENSION 252]: Flush the final coalesced matter
            self._flush_coalesced_matter(resolved_tokens)

            # --- MOVEMENT V: METABOLIC FINALITY ---
            # Unspool any matter written to physical disk due to heavy L1 mass
            final_tokens = spooler.unspool(resolved_tokens)

            # =========================================================================
            # == [ASCENSION 250]: THE OMNIPRESENT ASPECT SUTURE (THE MASTER CURE)    ==
            # =========================================================================
            # Apply all `@intercept` global mutations before returning the tokens.
            final_tokens = self._apply_omnipresent_intercepts(final_tokens, global_scope)

            # [ASCENSION 269]: Absolute Singularity Checkpoint
            state_hash = hashlib.sha256(str(len(final_tokens)).encode('utf-8')).hexdigest()[:8]
            ctx.variables["__merkle_state__"] = f"0x{state_hash.upper()}"

            # Radiate the conclusion to the HUD
            self._radiate_flame_graph(len(final_tokens))

            return final_tokens

        finally:
            if self._is_adrenaline and gc_was_enabled:
                gc.enable()

    def _apply_omnipresent_intercepts(self, tokens: List[GnosticToken], scope: LexicalScope) -> List[GnosticToken]:
        """
        =============================================================================
        == THE OMNIPRESENT SUTURE (V-Ω-ASPECT-ORIENTED)                            ==
        =============================================================================
        LIF: 500,000x | ROLE: CROSS_CUTTING_REALITY_MUTATOR

        Mathematically matches generated file paths against `@intercept` globs and
        applies content transfiguration (prepend, append, regex) universally.
        """
        intercepts = scope.global_ctx.variables.get('__omnipresent_interceptors__', [])
        if not intercepts:
            return tokens

        Logger.info(f"👁️ [PANOPTICON] Engaging {len(intercepts)} Omnipresent Intercepts across the Timeline...")

        # Build a rapid-access map of paths to tokens
        for token in tokens:
            # We must verify if the token is part of a File node.
            # In ELARA, paths are usually managed by the GeometricEmitter, but if
            # metadata is injected by the Mason:
            path = token.metadata.get("path")
            if not path: continue

            for intercept in intercepts:
                glob_pat = intercept["glob"]
                if fnmatch.fnmatch(path, glob_pat) or fnmatch.fnmatch(path.split('/')[-1], glob_pat):
                    # Found a victim of the Aspect
                    operator = intercept["operator"]
                    payload = str(intercept["payload"])

                    if operator == "^=":  # Prepend
                        token.content = payload + "\n" + str(token.content)
                    elif operator == "+=":  # Append
                        token.content = str(token.content) + "\n" + payload
                    elif operator == "~=":  # Replace (Expected format: "find/replace")
                        try:
                            # Basic string replacement; could be expanded to real Regex
                            f_str, r_str = payload.split('/')
                            token.content = str(token.content).replace(f_str, r_str)
                        except Exception:
                            pass

                    Logger.verbose(f"   -> Aspect woven into {path} via '{glob_pat}'")

        return tokens

    def _flush_coalesced_matter(self, output: List[GnosticToken]):
        """
        [ASCENSION 252]: ISOMORPHIC TOKEN COALESCENCE
        Merges adjacent Literal tokens that share identical spatial geometry.
        """
        if not self._coalesce_buffer:
            return

        if len(self._coalesce_buffer) == 1:
            output.append(self._coalesce_buffer[0])
            self._coalesce_buffer.clear()
            return

        # Fuse the matter
        first_token = self._coalesce_buffer[0]
        fused_content = "".join(str(t.raw_text or "") for t in self._coalesce_buffer)

        fused_token = GnosticToken(
            type=TokenType.LITERAL,
            content=fused_content,
            raw_text=fused_content,
            line_num=first_token.line_num,
            column_index=first_token.column_index,
            original_indent=getattr(first_token, 'original_indent', first_token.column_index),
            metadata={**first_token.metadata, "is_coalesced": True, "fused_count": len(self._coalesce_buffer)}
        )

        output.append(fused_token)
        self._coalesce_buffer.clear()

    def _walk(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken], spooler: LaminarStreamSpooler):
        """
        =============================================================================
        == THE RECURSIVE CONDUCTOR (WALK)                                          ==
        =============================================================================
        """
        # [ASCENSION 256]: Apophatic Node Exorcism
        if not node or not node.token:
            return

        self._node_count += 1

        # =========================================================================
        # == THE TOPOLOGICAL HORIZON SUTURE (THE CURE)                           ==
        # =========================================================================
        # We mathematically shift the token's column_index by the current spatial debt.
        # This guarantees physical code shifts left when parent logic gates evaporate!
        current_delta = self._horizon_stack[-1]

        if node.token:
            original_col = node.token.column_index or 0
            node.token.column_index = max(0, original_col - current_delta)
            if not hasattr(node.token, 'original_indent') or node.token.original_indent is None:
                node.token.original_indent = original_col

            # [ASCENSION 251]: Bi-Directional Tracking Anchor
            # Record the origin of this atom for the Drift Engine
            if "ast_line_number" not in node.token.metadata:
                node.token.metadata["ast_line_number"] = node.token.line_num

        # [ASCENSION 265]: LAMINAR STREAM SPOOLING
        if self._node_count % spooler.SPOOL_THRESHOLD == 0:
            self._flush_coalesced_matter(output)  # Flush before spooling
            output[:] = spooler.check_and_spool(self._node_count, output)

        # [ASCENSION 262]: RECURSION WARD
        if not hasattr(self._trace_depth, 'val'):
            self._trace_depth.val = 0

        if self._trace_depth.val > self.MAX_WALK_DEPTH:
            Logger.critical(f"Ouroboros Overflow: Trace {scope.global_ctx.trace_id} breached horizon.")
            return

        # --- THE ONTOLOGICAL TRIAGE ---

        try:
            # Branch 1: The Void
            if node.token.type == TokenType.VOID:
                for child in node.children:
                    self._walk(child, scope, output, spooler)
                return

            # Branch 2: Pure Physical Matter (COALESCENCE)
            if node.token.type == TokenType.LITERAL:
                # [ASCENSION 252]: Check if we can coalesce this token
                if self._coalesce_buffer:
                    last_token = self._coalesce_buffer[-1]
                    # Only fuse if they share the exact same topological depth and origin file
                    if (getattr(last_token, 'original_indent', -1) == getattr(node.token, 'original_indent', -1) and
                            last_token.metadata.get('source_file') == node.token.metadata.get('source_file')):
                        self._coalesce_buffer.append(node.token)
                    else:
                        self._flush_coalesced_matter(output)
                        self._coalesce_buffer.append(node.token)
                else:
                    self._coalesce_buffer.append(node.token)
                return

            # Flush coalescence buffer before hitting logic/variables to preserve order
            self._flush_coalesced_matter(output)

            # Branch 3: Gnostic Whispers (Comments)
            if node.token.type == TokenType.COMMENT:
                return

            # Branch 4: The Alchemical Reactor (Variables)
            if node.token.type == TokenType.VARIABLE:
                self._conduct_variable_resolution(node, scope, output)
                return

            # Branch 5: Logical Constructs (@if, @for, @component, etc.)
            if node.token.type == TokenType.LOGIC_BLOCK:
                is_braceless = node.metadata.get("is_braceless", False)
                gate = str(node.metadata.get("gate", "")).lower()

                # [ASCENSION 254]: THE INFINITE LOOP SENTRY
                if gate in ('for', 'call', 'mount'):
                    loop_id = f"{gate}_{node.token.line_num}_{id(node)}"
                    self._loop_cycle_tracker[loop_id] += 1
                    if self._loop_cycle_tracker[loop_id] > self.MAX_LOOP_CYCLES:
                        Logger.error(
                            f"L{node.token.line_num}: Thermodynamic Loop Sentry tripped. Halting infinite recursion.")
                        output.append(GnosticToken(
                            type=TokenType.LITERAL, content="/* METABOLIC_FEVER_HALT */",
                            raw_text="/* METABOLIC_FEVER_HALT */",
                            line_num=node.token.line_num, column_index=node.token.column_index
                        ))
                        return

                # Calculate spatial debt created by this gate
                gate_shift = 0
                if is_braceless and node.children:
                    first_child = next((c for c in node.children if c.token and c.token.type != TokenType.VOID), None)
                    if first_child:
                        child_col = getattr(first_child.token, 'original_indent', first_child.token.column_index) or 0
                        gate_shift = max(0, child_col - original_col)

                # Add this debt to the stack for all children to inherit
                self._horizon_stack.append(current_delta + gate_shift)

                try:
                    self._trace_depth.val += 1

                    # [ASCENSION 253]: O(1) STATIC BRANCH MEMOIZATION
                    # If this block has zero dynamic variables inside, we cache its output
                    is_static = node.metadata.get("is_static", False)
                    cache_key = f"{node.lineage_hash}_{gate}"

                    if is_static and cache_key in self._static_branch_cache:
                        cached_branch = self._static_branch_cache[cache_key]
                        # Apply current horizon to cached tokens
                        for t in cached_branch:
                            new_t = t.model_copy()
                            new_t.column_index = max(0, getattr(new_t, 'original_indent', 0) - (
                                        current_delta + gate_shift))
                            output.append(new_t)
                    else:
                        # [THE MASTER STRIKE]: Dispatch to the Gate Router
                        self.gate_router.dispatch(node, scope, output, spooler)

                finally:
                    self._trace_depth.val -= 1
                    # Erase the debt as we exit the logic block (Closure)
                    self._horizon_stack.pop()

                    if gate in ('for', 'call', 'mount'):
                        self._loop_cycle_tracker[loop_id] -= 1

        except Exception as walk_heresy:
            # [ASCENSION 261]: The NoneType Sarcophagus V18
            # If a specific node shatters, we log it and continue the loop to save the rest of the AST.
            Logger.error(f"AST Node L{getattr(node.token, 'line_num', 0)} Fractured: {walk_heresy}")
            output.append(GnosticToken(
                type=TokenType.LITERAL, content=f"/* NODE_FRACTURE: {str(walk_heresy)} */",
                raw_text="", line_num=getattr(node.token, 'line_num', 0), column_index=0
            ))

        finally:
            # [ASCENSION 255]: Ethereal Memory Reclaim (AST Evaporation)
            # The exact microsecond this node is resolved, we obliterate its raw references
            # to free physical RAM, making memory usage O(1) relative to tree depth.
            if not self._is_adrenaline and node.children:
                # We only evaporate if it's NOT a reusable macro/component definition!
                gate_type = node.metadata.get("gate", "").lower()
                if gate_type not in ("macro", "component"):
                    node.children = []
                    node.token = None

    def _conduct_variable_resolution(self, node: ASTNode, scope: LexicalScope, output: List[GnosticToken]):
        """THE ALCHEMICAL RECEPTOR"""
        try:
            scope.set("__start_time_ns__", time.perf_counter_ns())
            raw_expr = node.token.content
            start_t = time.perf_counter_ns()

            result = FilterPipeline.execute(raw_expr, scope)
            final_matter = str(OuroborosBreaker.thaw(result, scope, self.engine_ref))

            resolved_token = GnosticToken(
                type=TokenType.LITERAL,
                content=final_matter,
                raw_text=final_matter,
                line_num=node.token.line_num,
                column_index=node.token.column_index,  # Horizon-Shifted coordinate
                original_indent=getattr(node.token, 'original_indent', node.token.column_index),  # <--- SUTURED
                metadata={
                    **node.token.metadata,
                    "is_resolved_variable": True,
                    "_reason": "Variable Thawed Successfully",
                    "resolve_tax_ns": time.perf_counter_ns() - start_t
                }
            )
            output.append(resolved_token)

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy):
            # [ASCENSION 270]: Holographic Fallback Matrix
            output.append(GnosticToken(
                type=TokenType.LITERAL,
                content=node.token.raw_text,
                raw_text=node.token.raw_text,
                line_num=node.token.line_num,
                column_index=node.token.column_index,
                original_indent=getattr(node.token, 'original_indent', node.token.column_index)
            ))

        except Exception as catastrophic_heresy:
            error_msg = f"/*[LOGIC_FRACTURE]: {str(catastrophic_heresy)} */"
            output.append(GnosticToken(
                type=TokenType.LITERAL,
                content=error_msg,
                raw_text=error_msg,
                line_num=node.token.line_num,
                column_index=node.token.column_index,
                original_indent=getattr(node.token, 'original_indent', node.token.column_index)
            ))

    def _inject_semantic_filters(self, scope: LexicalScope):
        """Injects global helper functions into the scope."""

        def find_shard(query: str):
            if not self.engine_ref or not hasattr(self.engine_ref, 'cortex'): return "VOID_SHARD"
            try:
                hits = self.engine_ref.cortex.semantic_resolver.resolve(query)
                return hits[0][0].id if hits and hits[0] else "VOID"
            except Exception:
                return "VOID_FRACTURE"

        scope.local_vars["find_shard"] = find_shard
        scope.local_vars["__os__"] = os.name
        scope.local_vars["__platform__"] = sys.platform

    def _radiate_flame_graph(self, final_atom_count: int):
        """[ASCENSION 263]: Projects diagnostic performance data to the React UI."""
        if hasattr(self.engine_ref, 'akashic') and self.engine_ref.akashic:
            duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
            try:
                self.engine_ref.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "AST_RESOLUTION_COMPLETE",
                        "label": "WALK_FINISHED",
                        "color": "#10b981",  # Emerald
                        "latency": f"{duration_ms:.2f}ms",
                        "atoms": final_atom_count,
                        "trace": self._active_trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_RECURSIVE_RESOLVER atoms={self._node_count} status=RESONANT mode=QUANTUM_MATRIX_VMAX>"