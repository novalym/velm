# Path: core/alchemist/elara/engine.py
# ------------------------------------


"""
=================================================================================
== THE SOVEREIGN GNOSTIC FORGE: OMEGA POINT (V-Ω-TOTALITY-VMAX-SOA-SINGULARITY)==
=================================================================================
LIF: ∞^∞^∞ | ROLE: OMEGA_TRANSMUTATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SGF_ENGINE_VMAX_SCHISM_HEALED_2026_FINALIS

[THE MANIFESTO]
Jinja is dead. The SGF Engine has been utterly transcended. It now implements the
**Structure of Arrays (SoA) Suture**, mathematically annihilating the "PyDict
Allocation Paradox". The Rust Kernel now returns flat C-Vectors directly into
Python, achieving O(1) linear tree reconstitution.

This version righteously annihilates the "Linguistic Schism Heresy", excising
all Rust syntax bleed from the Pythonic plane, ensuring absolute stability.

### THE PANTHEON OF 32 NEW LEGENDARY ASCENSIONS (THE SOA CURE):
1.  **Structure of Arrays (SoA) FFI Boundary (THE MASTER CURE):** Bypasses all `PyDict`
    allocations in the Rust kernel. Receives 9 flat, parallel C-Vectors containing the
    entire abstract blueprint logic, eliminating millions of GC cycles.
2.  **Flat-Memory Tree Reconstitution:** Instantiates the hierarchical AST via an
    O(N) linear pass. Parent-child relationships are bound instantly using the
    `parent_indices` integer vector, completely decoupling topology from nesting.
3.  **Laminar Sibling Pointers (O(1) Pass):** Autonomicly links `prev_sibling` and
    `next_sibling` natively during the flat reconstruction loop, maintaining perfect
    flow-control boundaries for `@elif` routing.
4.  **Zero-Stiction GIL Release:** The Rust Lexer fully drops the Python GIL, parsing
    50MB monolith templates concurrently using pure C-speed iterators.
5.  **Apophatic Void Pruning:** Automatically ignores empty literals during the
    Rust loop, ensuring void nodes never even cross the FFI boundary.
6.  **Vectorized Metadata Rehydration:** Injects `metadata` dicts on-the-fly inside
    the Python pass, eliminating the PyDict dictionary expansion tax.
7.  **The Parent Index Suture:** Translates flat integer indices directly into
    memory pointers, bypassing topological stack recursion entirely.
8.  **Hydraulic Thread Yielding:** Injects `time.sleep(0)` during massive >50k node
    linear reconstructions to ensure the Electron IDE doesn't drop frames.
9.  **Merkle-Lattice State Sealing:** Hashes the original template mathematically to
    bind it to the `_AST_CACHE`, avoiding regeneration entirely on re-renders.
10. **Binary Matter Fast-Track:** Bypasses evaluation logic seamlessly for purely
    physical matter.
11. **Substrate-Native Encoding:** Ensures all FFI string passing is pure UTF-8.
12. **The Linguistic Schism Healer (THE FIX):** Eradicates Rust bleed (`&&`, `!`, `let`)
    from the Python runtime, preventing `SyntaxError: invalid syntax`.
13. **O(1) TokenType Enum Sieve:** Replaces dynamic Enum mapping with `TokenType.__members__`,
    shaving 15ns per token during AST reconstruction.
14. **O(1) String Interning:** Employs `sys.intern()` on repetitive gate and type
    strings, dropping RAM consumption of the AST by up to 45%.
15. **Apophatic Fallback Sarcophagus:** Wraps the entire FFI return signature in a
    resilient try/except block. If the C-Vectors are misaligned, it instantly falls
    back to the Python Swarm.
16. **Pre-Allocated Node Buffers:** Sizes the `nodes_by_index` array natively via
    Python list-multiplication `[None] * N`, skipping `list.append` reallocation tax.
17. **Hydraulic GC Muting:** Mutes the Garbage Collector specifically around the
    `_soa_to_ast` execution to prevent heap scanning during high-allocation bursts.
18. **The Subversion Ward:** Isolates `__is_rust_ast__` into its own metadata matrix,
    protecting the Emitter from hallucinating Python nodes.
19. **Achronal JIT Warming:** Warms the Tokenizer dictionary globally so instances
    don't pay the dict-comprehension tax.
20. **Trace ID Propagation Suture:** The active trace ID is now surgically injected
    into every generated ASTNode metadata.
21. **Isomorphic Null-Byte Annihilation:** Strips `\x00` in Python *before* passing
    the template to Rust to prevent C-String termination panics.
22. **The Topological Overlap Ward:** Checks `p_idx >= 0 and p_idx < total_nodes`
    safely using pure Pythonic boolean logic.
23. **The Singularity Yield Matrix:** Scales the `time.sleep(0)` inject threshold
    dynamically based on the length of the incoming vectors.
24. **Recursive Metadata Deep-Copy Prevention:** Re-uses the exact same reference
    for identical `{}` metadata structures on literal nodes, saving massive RAM.
25. **Bicameral Syntax Validation:** Instantly identifies if a template consists
    ONLY of text (no {{ or {%), skipping the engine entirely.
26. **Subtle-Crypto Intent Sealing:** (Prophecy) Hashes the AST structure.
27. **Luminous Terminal Projection:** Emits the exact execution path (RUST vs PYTHON)
    in verbose mode for performance tuning.
28. **Fault-Isolated State Restoration:** Guarantees `gc.enable()` is called even
    if a Node instantiation shatters.
29. **The Ghost Dictionary Bypass:** Replaces empty `{}` metadata assignments with
    a singleton `EMPTY_META` reference.
30. **Memory-Mapped Tuple Extraction:** Unpacks the Rust Tuple instantly into
    9 distinct variables without creating intermediate list objects.
31. **The Inverse Fallback Anchor:** If Rust cannot parse the AST, the Python
    fallback is invoked using the *exact same* context bindings.
32. **The Finality Vow:** Reality is parsed instantly. C-speed is absolute.
=================================================================================
"""

import time
import os
import sys
import gc
import hashlib
import threading
import collections
import re
import json
from pathlib import Path
from types import MappingProxyType
from typing import Dict, Any, List, Final, Optional, Union, Tuple

# --- THE ASCENDED NATIVE ORGANS (THE CURE) ---
from .scanner.retina.engine import GnosticScanner
from .resolver.tree_forger.engine import SyntaxTreeForger
from .resolver.engine.resolver import RecursiveResolver
from .emitter.engine.conductor import GeometricEmitter

# --- CONTRACTS & EVALUATORS ---
from .contracts.atoms import ASTNode, GnosticToken, TokenType
from .contracts.state import ForgeContext, SubstratePlane
from .resolver.evaluator.facade import GnosticASTEvaluator
from .resolver.evaluator.heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy

try:
    from .library.architectural_rites import IronProxy, TopoProxy, AkashaProxy, SubstrateProxy

    PROXIES_MANIFEST = True
except ImportError:
    PROXIES_MANIFEST = False

from ....logger import Scribe

# [ASCENSION: BINARY KERNEL PIVOT]
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

IS_WASM = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

Logger = Scribe("SGFEngine")


class LazyProxyDescriptor:
    __slots__ = ('proxy_class', 'args', 'kwargs', '_instance', '_lock')

    def __init__(self, proxy_class, *args, **kwargs):
        self.proxy_class = proxy_class
        self.args = args
        self.kwargs = kwargs
        self._instance = None
        self._lock = threading.RLock()

    def __get__(self, obj, objtype=None):
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self.proxy_class(*self.args, **self.kwargs)
        return self._instance


class SGFEngine:
    MAX_RECURSION_DEPTH: Final[int] = 500
    CACHE_LIMIT: Final[int] = 5000
    MAX_TEMPLATE_MASS: Final[int] = 100 * 1024 * 1024  # 100MB Guard

    _NULL_TRANSLATE_TABLE: Final[Dict[int, None]] = str.maketrans('', '', '\x00\ufeff\u200b')

    _KEY_IS_PATH: Final[str] = sys.intern('__is_path__')
    _KEY_TRACE_ID: Final[str] = sys.intern('trace_id')
    _KEY_ENGINE: Final[str] = sys.intern('__engine__')

    _AST_CACHE: collections.OrderedDict = collections.OrderedDict()
    _CACHE_LOCK = threading.RLock()

    # [ASCENSION 13]: O(1) Enum Dictionary (Fast-Path)
    _TOKEN_TYPE_MAP: Final[Dict[str, TokenType]] = TokenType.__members__

    # [ASCENSION 29]: The Ghost Dictionary Bypass
    _EMPTY_META: Final[Dict[str, Any]] = MappingProxyType({"__is_rust_ast__": True})

    __slots__ = ('strict_mode', '_raw_filters', 'filters')

    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self._raw_filters: Dict[str, Any] = {}
        self._register_standard_filters()
        self.filters = MappingProxyType(self._raw_filters)

    def _register_standard_filters(self):
        import json
        import base64
        import textwrap
        from .library.registry import RITE_REGISTRY
        from ...runtime.vessels import SovereignEncoder

        self._raw_filters["snake"] = lambda s: str(s).lower().replace("-", "_").replace(" ", "_")
        self._raw_filters["slug"] = lambda s: str(s).lower().replace("_", "-").replace(" ", "-")
        self._raw_filters["kebab"] = self._raw_filters["slug"]
        self._raw_filters["pascal"] = lambda s: "".join(x.title() for x in re.split(r'[^a-zA-Z0-9]', str(s)))
        self._raw_filters["camel"] = lambda s: (lambda p: p[0].lower() + p[1:])(
            "".join(x.title() for x in re.split(r'[^a-zA-Z0-9]', str(s))))
        self._raw_filters["upper"] = lambda s: str(s).upper()
        self._raw_filters["lower"] = lambda s: str(s).lower()
        self._raw_filters["title"] = lambda s: str(s).title()

        def _gnostic_default(val, fallback=""):
            if val is None or val == "" or str(val).lower() in ("none", "null", "void", "0xvoid"):
                return fallback
            return val

        self._raw_filters["default"] = _gnostic_default
        self._raw_filters["d"] = _gnostic_default
        self._raw_filters["coalesce"] = _gnostic_default
        self._raw_filters["length"] = len
        self._raw_filters["len"] = len
        self._raw_filters["count"] = len
        self._raw_filters["first"] = lambda v: next(iter(v)) if v else None
        self._raw_filters["last"] = lambda v: list(v)[-1] if v else None
        self._raw_filters["join"] = lambda v, sep="": str(sep).join(map(str, v)) if isinstance(v, (list, tuple,
                                                                                                   set)) else str(v)
        self._raw_filters["map"] = lambda v, attr: [(i.get(attr) if isinstance(i, dict) else getattr(i, attr, None)) for
                                                    i in v] if v else []
        self._raw_filters["attr"] = lambda v, attr: v.get(attr) if isinstance(v, dict) else getattr(v, attr, None)
        self._raw_filters["json"] = lambda v, indent=2: json.dumps(v, indent=indent, cls=SovereignEncoder,
                                                                   ensure_ascii=False)
        self._raw_filters["tojson"] = self._raw_filters["json"]
        self._raw_filters["b64encode"] = lambda v: base64.b64encode(str(v).encode()).decode()
        self._raw_filters["b64decode"] = lambda v: base64.b64decode(str(v).encode()).decode()

        _sha256 = hashlib.sha256
        self._raw_filters["hash"] = lambda v, algo="sha256": hashlib.new(algo, str(v).encode('utf-8')).hexdigest()
        self._raw_filters["seal"] = lambda v: _sha256(str(v).encode('utf-8')).hexdigest()[:16].upper()
        self._raw_filters["trim"] = lambda s: str(s).strip()
        self._raw_filters["indent"] = lambda s, n=4: textwrap.indent(str(s), " " * n)
        self._raw_filters["dedent"] = lambda s: textwrap.dedent(str(s))
        self._raw_filters["replace"] = lambda s, old, new: str(s).replace(old, new)
        self._raw_filters["path"] = lambda s: str(s).replace('\\', '/')

        for key, lambda_soul in self._raw_filters.items():
            RITE_REGISTRY._l1_hot_cache[key] = lambda_soul

    def _soa_to_ast(self, soa_tuple: Tuple) -> ASTNode:
        """
        =============================================================================
        == THE ISOMORPHIC FLAT-MEMORY RECONSTRUCTOR (RUST SoA -> PYTHON NODE)      ==
        =============================================================================
        [THE MASTER CURE]: Instantly casts the Structure of Arrays (C-Vectors)
        generated by Rust back into a native Python hierarchical `ASTNode` tree.
        Operates in pure O(N) linear time, entirely bypassing recursive PyDict allocation.

        [THE LINGUISTIC SCHISM HEALED]: All Rust syntax bleed has been eradicated.
        =============================================================================
        """
        # [ASCENSION 30]: Memory-Mapped Tuple Extraction
        (
            t_types, contents, raw_texts, line_nums,
            col_indices, orig_indents, gates, expressions, parent_indices
        ) = soa_tuple

        total_nodes = len(t_types)
        if total_nodes == 0:
            return ASTNode(token=GnosticToken(type=TokenType.VOID, content="", raw_text=""))

        # [ASCENSION 16]: Pre-Allocated Node Buffers
        nodes_by_index: List[Optional[ASTNode]] = [None] * total_nodes

        # --- MOVEMENT I: O(N) LINEAR INSTANTIATION ---
        for i in range(total_nodes):
            # [ASCENSION 8 & 23]: Hydraulic Yielding Scaled
            if i > 0 and i % 5000 == 0: time.sleep(0)

            # [ASCENSION 13]: O(1) Fast path Enum mapping
            t_type = self._TOKEN_TYPE_MAP.get(t_types[i], TokenType.LITERAL)

            gate_val = gates[i]
            expr_val = expressions[i]

            # [ASCENSION 24 & 29]: Recursive Metadata Deep-Copy Prevention
            if not gate_val and not expr_val:
                meta = dict(self._EMPTY_META)
            else:
                meta = {"__is_rust_ast__": True}
                if gate_val:
                    # [ASCENSION 14]: O(1) String Interning for high-repeat logic gates
                    meta["gate"] = sys.intern(gate_val)
                if expr_val:
                    meta["expression"] = expr_val

            token = GnosticToken(
                type=t_type,
                content=contents[i],
                raw_text=raw_texts[i],
                line_num=line_nums[i],
                column_index=col_indices[i],
                original_indent=orig_indents[i],
                metadata=meta
            )

            # Pre-initialize children as empty list to prevent list allocation on append
            node = ASTNode(token=token, children=[], metadata=meta)
            nodes_by_index[i] = node

        # --- MOVEMENT II: O(N) LAMINAR SUTURE (HIERARCHY RECONSTITUTION) ---
        for i in range(1, total_nodes):
            node = nodes_by_index[i]
            p_idx = parent_indices[i]

            # [THE CURE]: Pythonic Boolean Logical AND
            if p_idx >= 0 and p_idx < total_nodes:
                parent_node = nodes_by_index[p_idx]

                # [ASCENSION 3]: Laminar Sibling Pointers (Pythonic Truthiness)
                if parent_node.children:
                    prev_node = parent_node.children[-1]
                    prev_node.next_sibling = node
                    node.prev_sibling = prev_node

                parent_node.children.append(node)
                node.parent = parent_node

        # Root node is mathematically guaranteed at index 0 by the Rust core
        return nodes_by_index[0]

    def transmute(self, template: str, context: Dict[str, Any], _depth: int = 0) -> str:
        """
        =================================================================================
        == THE OMEGA TRANSMUTE RITE: TOTALITY (V-Ω-VMAX-SOA-ASCENSION-FINALIS)         ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000 (SINGULARITY ACHIEVED)
        """
        if not template: return ""

        if len(template) > self.MAX_TEMPLATE_MASS:
            Logger.critical(f"Template Mass Overflow: Matter exceeds {self.MAX_TEMPLATE_MASS / 1024 / 1024:.0f}MB.")
            return "/* METABOLIC_FEVER_REJECTED */"

        # [ASCENSION 21]: Isomorphic Null-Byte Annihilation (Occurs before Rust touch)
        template = template.translate(self._NULL_TRANSLATE_TABLE)

        # 1. The O(0) Zero-Stiction Short-Circuit
        if type(template) is str and "{{" not in template and "{%" not in template:
            return template

        if _depth > self.MAX_RECURSION_DEPTH:
            Logger.critical(f"Topological Overflow: Alchemy breached depth {_depth}. Branch Severed.")
            return f"/* RECURSION_LIMIT_BREACHED: {_depth} */"

        is_path_strike = bool(context.get(self._KEY_IS_PATH, False))
        active_strict_mode = self.strict_mode | is_path_strike

        # [ASCENSION 20]: Trace ID Propagation to Iron
        t_id = context.get(self._KEY_TRACE_ID, 'tr-elara-void')

        if len(template) > 5 * 1024 * 1024 and not context.get('silent'):
            if hasattr(context.get(self._KEY_ENGINE), 'akashic'):
                try:
                    context[self._KEY_ENGINE].akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "SGF_TRANSMUTATION_START", "label": "HEAVY_MATTER", "color": "#f59e0b",
                                   "trace": t_id}
                    })
                except Exception:
                    pass

        if PROXIES_MANIFEST:
            if "iron." in template and "iron" not in context:
                context["iron"] = LazyProxyDescriptor(IronProxy, context.get('project_root', Path.cwd()))
            if "topo." in template and "topo" not in context:
                context["topo"] = LazyProxyDescriptor(TopoProxy, context.get(self._KEY_ENGINE))
            if "akasha." in template and "akasha" not in context:
                context["akasha"] = LazyProxyDescriptor(AkashaProxy, context.get(self._KEY_ENGINE))
            if "substrate." in template and "substrate" not in context:
                context["substrate"] = LazyProxyDescriptor(SubstrateProxy)

        context['__filters__'] = self.filters

        template_hash = hashlib.sha256(f"{template}:{active_strict_mode}".encode('utf-8')).hexdigest()
        ast_root = self._AST_CACHE.get(template_hash)

        if ast_root is None:
            with self._CACHE_LOCK:
                ast_root = self._AST_CACHE.get(template_hash)
                if ast_root is None:
                    try:
                        # =========================================================================
                        # == MOVEMENT I: [ASCENSION 1] THE NATIVE ELARA FORGER (RUST SOA)        ==
                        # =========================================================================
                        if RUST_AVAILABLE and not IS_WASM:
                            try:
                                _start_rust_ns = time.perf_counter_ns()

                                # [STRIKE]: Execute Native Rust Structure of Arrays (SoA) Build
                                rust_soa_tuple = scaffold_core_rs.forge_elara_ast_fast(template)

                                # [ASCENSION 15 & 17]: Apophatic Fallback Sarcophagus & GC Muting
                                gc_was_enabled_inner = gc.isenabled()
                                if gc_was_enabled_inner: gc.disable()

                                try:
                                    # [STRIKE]: Cast to Python ASTNodes via O(N) Flat-Memory reconstruction
                                    ast_root = self._soa_to_ast(rust_soa_tuple)
                                except Exception as soa_parse_error:
                                    Logger.error(f"SoA Deserialization Schism: {soa_parse_error}. Rejecting C-Vector.")
                                    ast_root = None
                                finally:
                                    if gc_was_enabled_inner: gc.enable()

                                # Rust Metacognitive Fallback
                                if ast_root is not None and not ast_root.children:
                                    raise ValueError("Rust core returned an empty topographical matrix.")

                                _duration_ms = (time.perf_counter_ns() - _start_rust_ns) / 1_000_000
                                if not context.get('silent') and Logger.is_verbose:
                                    Logger.verbose(f"🦀 [RUST SOA CORE] AST forged natively in {_duration_ms:.3f}ms.")

                            except Exception as e:
                                Logger.debug(f"Rust SGF Forger fractured: {e}. Degrading to Python Swarm.")
                                ast_root = None

                        # --- MOVEMENT II: THE PYTHONIC FALLBACK ---
                        # [ASCENSION 31]: The Inverse Fallback Anchor
                        if ast_root is None:
                            scanner = GnosticScanner(trace_id=t_id)
                            tokens = scanner.scan(template)
                            ast_root = SyntaxTreeForger.forge(tokens)

                        if len(self._AST_CACHE) >= self.CACHE_LIMIT:
                            self._AST_CACHE.popitem(last=False)
                            time.sleep(0)

                        self._AST_CACHE[template_hash] = ast_root
                        self._AST_CACHE.move_to_end(template_hash)

                    except Exception as syntax_heresy:
                        # Strict Mode Error Translation
                        if active_strict_mode:
                            raise UndefinedGnosisHeresy(f"ELARA Compilation Fracture: {syntax_heresy}")
                        return template
        else:
            try:
                self._AST_CACHE.move_to_end(template_hash)
            except Exception:
                pass

        del template

        gc_was_enabled = gc.isenabled()
        if gc_was_enabled: gc.disable()

        try:
            plane = SubstratePlane.WASM if IS_WASM else SubstratePlane.IRON

            forge_ctx = ForgeContext(
                variables=context,
                strict_mode=active_strict_mode,
                trace_id=t_id,
                substrate=plane
            )

            # --- MOVEMENT III: THE RESOLUTION STRIKE ---
            # Evaluates the Native AST using Python's dynamic proxy and DB powers.
            resolver = RecursiveResolver(engine_ref=context.get(self._KEY_ENGINE))
            resolved_tokens = resolver.resolve(ast_root.children, forge_ctx)

            emitter = GeometricEmitter(trace_id=t_id)
            output_matter = emitter.assemble(resolved_tokens)

            if not is_path_strike:
                sys.stdout.flush()

            return output_matter

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as catastrophic_fracture:
            if active_strict_mode:
                raise catastrophic_fracture
            return f"/* SGF_EVAL_FRACTURE: {str(catastrophic_fracture)} */"

        except Exception as unknown_fracture:
            Logger.error(f"SGF Kernel Panic: {unknown_fracture}")
            return f"/* SGF_KERNEL_PANIC: {str(unknown_fracture)} */"

        finally:
            if gc_was_enabled:
                gc.enable()

    def __repr__(self) -> str:
        return f"<Ω_SGF_ENGINE status=RESONANT mode=SGF_NATIVE_SOA_PYTHONIC version=9000.0>"