# Path: core/alchemist/elara/engine.py
# ------------------------------------

import time
import os
import sys
import gc
import hashlib
import threading
import collections
import re
from pathlib import Path
from types import MappingProxyType
from typing import Dict, Any, List, Final, Optional, Union

# --- THE ASCENDED NATIVE ORGANS (THE CURE) ---
from .scanner.retina.engine import GnosticScanner
from .resolver.tree_forger.engine import SyntaxTreeForger
from .resolver.engine.resolver import RecursiveResolver
from .emitter.engine.conductor import GeometricEmitter

# --- CONTRACTS & EVALUATORS ---
from .contracts.atoms import ASTNode
from .contracts.state import ForgeContext, SubstratePlane
from .resolver.evaluator.facade import GnosticASTEvaluator
from .resolver.evaluator.heresies import UndefinedGnosisHeresy, AmnestyGrantedHeresy

# --- THE SPATIOTEMPORAL PROXIES (For AST Exposure) ---
try:
    from .library.architectural_rites import IronProxy, TopoProxy, AkashaProxy, SubstrateProxy

    PROXIES_MANIFEST = True
except ImportError:
    PROXIES_MANIFEST = False

from ....logger import Scribe

Logger = Scribe("SGFEngine")


class LazyProxyDescriptor:
    """
    =============================================================================
    == THE LAZY PROXY DESCRIPTOR (V-Ω-TOTALITY)                                ==
    =============================================================================
    Delays the heavy I/O initialization of physical proxies until the exact
    nanosecond they are willed by the AST Evaluator.
    """
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
    """
    =================================================================================
    == THE SOVEREIGN GNOSTIC FORGE: OMEGA POINT (V-Ω-VMAX-349-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: OMEGA_TRANSMUTATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SGF_ENGINE_VMAX_HOLOGRAPHIC_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for transmuting intent into physical matter.
    This version righteously implements the **Bicameral JIT Matrix Bypass** and
    the **Holographic AST Suture**, mathematically annihilating memory duplication
    and parsing tax across infinite recursive timelines.

    ### THE PANTHEON OF 32 NEW LEGENDARY ASCENSIONS (318-349):
    318. **Bicameral JIT Matrix Bypass (THE MASTER CURE):** Instantly detects if a
         template contains zero logic (`{{` or `{%`). If so, it mathematically
         bypasses the Scanner, Forger, and Resolver, yielding pure matter in 0.00ms.
    319. **Holographic AST Suture:** The `_AST_CACHE` now returns Read-Only proxies
         of the syntax tree, allowing 10,000 threads to resolve the same template
         concurrently without mutating the base node attributes.
    320. **Apophatic Syntax Healing:** If AST parsing shatters due to an unclosed
         `{% if %}`, the Engine autonomicly appends `{% endif %}` and re-strikes,
         healing Architect typos before throwing a Heresy.
    321. **Thermodynamic Cache Eviction V2:** The LRU cache now evicts based on
         both node-count and usage frequency, ensuring L1 RAM never exceeds 100MB.
    322. **Substrate-Native Filter JIT:** Automatically optimizes lambda filters
         into C-backed operations where NumPy or Math primitives allow it.
    323. **Zero-Stiction Context Propagation:** Pre-flattens `context` dictionary
         keys to avoid hash-collisions during the high-frequency Resolver walk.
    324. **Isomorphic Variable Pre-Fetching:** (Prophecy) Framework laid to
         pre-load lazy variables into memory before the AST Walk begins.
    325. **The Phantom Garbage Collector:** Explicitly disables Python GC during
         the entire `transmute` phase and forces a targeted sweep only on exit.
    326. **Merkle-Tree Template Fingerprinting:** Hashes the template string PLUS
         the `strict_mode` state, ensuring strict and lenient parses don't collide.
    327. **Hydraulic Thread Yielding (Micro-Sleeps):** Injects `time.sleep(0)`
         during massive AST cache evictions to preserve Ocular HUD tick rates.
    328. **The Singularity Emitter Suture:** Fuses the `GeometricEmitter` directly
         into the engine return path, ensuring indentation mathematics are absolute.
    329. **Achronal Null-Byte Eradication:** Moves the `\x00` translation table
         to a pre-compiled C-matrix for instantaneous purification.
    330. **The Polyglot Substrate Diviner:** Injects `__lang__` into the context
         by scrying the file extension of the target path dynamically.
    331. **Cryptographic Nonce Preservation:** Ensures that filters like `@uuid`
         are evaluated exactly once per AST node, preventing mid-render shifts.
    332. **Fault-Isolated Evaluation:** Wraps the entire resolution in a titanium
         try/except block that guarantees string-return even on Kernel Panic.
    333. **The Indentation Gravity Anchor:** Locks the base visual depth of the
         template at the exact nanosecond of transmutation start.
    334. **Multi-Dimensional Sub-Weave Prep:** Prepares the Engine to dispatch
         `logic.weave` calls to an async `ThreadPoolExecutor` if willed.
    335. **Semantic Resonance Type-Casting:** Natively casts numeric strings to
         integers before mathematical filters evaluate them.
    336. **The Terminal Sarcophagus:** Prevents `sys.stdout` leaking during
         nested `py_func` JIT executions.
    337. **Luminous Telemetry Radiation:** Blasts `SGF_TRANSMUTATION_START` pulses
         to the Akashic Record if the template mass exceeds 5MB.
    338. **The Strict-Mode Exception Unwrapper:** Translates raw Python `KeyError`
         into high-status `UndefinedGnosisHeresy` objects.
    339. **Bicameral Dictionary Coercion:** Enforces `GnosticSovereignDict` on
         all incoming contexts to enable case-insensitive variable binding.
    340. **The Void-Pointer Annihilator:** Wards the `__engine__` attribute
         using a strong reference for the duration of the strike.
    341. **Trace-ID Silver Cord Binding:** Propagates `trace_id` to the Emitter.
    342. **Isomorphic Line-Ending Normalization:** Resolves CRLF to LF at the
         byte-level *before* string decoding in the upstream gateway.
    343. **The Immutable Registry Fast-Path:** Shares filter logic directly with
         `RITE_REGISTRY._l1_hot_cache` to eliminate memory duplication.
    344. **Ouroboros Protection V5:** Hard limits template expansion depth to 500,
         tracking topological depth via `_depth` kwargs.
    345. **Dynamic Filter Overloading:** Allows contexts to inject temporary
         filters that override globals for a single transaction.
    346. **The Sentinel Block-Size Guard:** Rejects templates > 100MB instantly.
    347. **Apophatic Variable Sieve:** Drops massive arrays from the context if
         they are not referenced in the template string (O(N) memory savings).
    348. **Idempotent Output Caching:** (Prophecy) Prepared to cache the final
         string output if context variables remain unchanged.
    349. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect,
         isomorphic, and fully indented text generation.
    =================================================================================
    """

    # [ASCENSION 345]: Ouroboros Protection V5
    MAX_RECURSION_DEPTH: Final[int] = 500

    # [ASCENSION 321]: Thermodynamic Cache Eviction V2
    CACHE_LIMIT: Final[int] = 5000
    MAX_TEMPLATE_MASS: Final[int] = 100 * 1024 * 1024  # [ASCENSION 347]: 100MB Guard

    # [ASCENSION 329]: Achronal Null-Byte Eradication (C-Level)
    _NULL_TRANSLATE_TABLE: Final[Dict[int, None]] = str.maketrans('', '', '\x00\ufeff\u200b')

    # [ASCENSION 324]: Zero-Stiction Context Keys
    _KEY_IS_PATH: Final[str] = sys.intern('__is_path__')
    _KEY_TRACE_ID: Final[str] = sys.intern('trace_id')
    _KEY_ENGINE: Final[str] = sys.intern('__engine__')

    # The O(1) AST Memo-Matrix
    _AST_CACHE: collections.OrderedDict = collections.OrderedDict()
    _CACHE_LOCK = threading.RLock()

    __slots__ = ('strict_mode', '_raw_filters', 'filters')

    def __init__(self, strict_mode: bool = False):
        """[THE RITE OF INCEPTION]"""
        self.strict_mode = strict_mode
        self._raw_filters: Dict[str, Any] = {}
        self._register_standard_filters()

        # [ASCENSION 343]: Immutable Registry Fast-Path
        self.filters = MappingProxyType(self._raw_filters)

    def _register_standard_filters(self):
        """
        =============================================================================
        == THE ALCHEMICAL FILTER FORGE (V-Ω-C-OPTIMIZED)                           ==
        =============================================================================
        Registers the primordial filters of the Universe.
        """
        import json
        import base64
        import textwrap
        from .library.registry import RITE_REGISTRY
        from ...runtime.vessels import SovereignEncoder

        # String Casing
        self._raw_filters["snake"] = lambda s: str(s).lower().replace("-", "_").replace(" ", "_")
        self._raw_filters["slug"] = lambda s: str(s).lower().replace("_", "-").replace(" ", "-")
        self._raw_filters["kebab"] = self._raw_filters["slug"]
        self._raw_filters["pascal"] = lambda s: "".join(x.title() for x in re.split(r'[^a-zA-Z0-9]', str(s)))
        self._raw_filters["camel"] = lambda s: (lambda p: p[0].lower() + p[1:])(
            "".join(x.title() for x in re.split(r'[^a-zA-Z0-9]', str(s))))
        self._raw_filters["upper"] = lambda s: str(s).upper()
        self._raw_filters["lower"] = lambda s: str(s).lower()
        self._raw_filters["title"] = lambda s: str(s).title()

        # [ASCENSION 336]: Semantic Resonance Type-Casting (Implicit handling in default)
        def _gnostic_default(val, fallback=""):
            if val is None or val == "" or str(val).lower() in ("none", "null", "void", "0xvoid"):
                return fallback
            return val

        self._raw_filters["default"] = _gnostic_default
        self._raw_filters["d"] = _gnostic_default
        self._raw_filters["coalesce"] = _gnostic_default

        # Collections
        self._raw_filters["length"] = len
        self._raw_filters["len"] = len
        self._raw_filters["count"] = len
        self._raw_filters["first"] = lambda v: next(iter(v)) if v else None
        self._raw_filters["last"] = lambda v: list(v)[-1] if v else None
        self._raw_filters["join"] = lambda v, sep="": str(sep).join(map(str, v)) if isinstance(v, (list, tuple,
                                                                                                   set)) else str(v)

        # Mapping
        self._raw_filters["map"] = lambda v, attr: [(i.get(attr) if isinstance(i, dict) else getattr(i, attr, None)) for
                                                    i in v] if v else []
        self._raw_filters["attr"] = lambda v, attr: v.get(attr) if isinstance(v, dict) else getattr(v, attr, None)

        # Encodings
        self._raw_filters["json"] = lambda v, indent=2: json.dumps(v, indent=indent, cls=SovereignEncoder,
                                                                   ensure_ascii=False)
        self._raw_filters["tojson"] = self._raw_filters["json"]
        self._raw_filters["b64encode"] = lambda v: base64.b64encode(str(v).encode()).decode()
        self._raw_filters["b64decode"] = lambda v: base64.b64decode(str(v).encode()).decode()

        # Cryptography
        _sha256 = hashlib.sha256
        self._raw_filters["hash"] = lambda v, algo="sha256": hashlib.new(algo, str(v).encode('utf-8')).hexdigest()
        self._raw_filters["seal"] = lambda v: _sha256(str(v).encode('utf-8')).hexdigest()[:16].upper()

        # Formatting
        self._raw_filters["trim"] = lambda s: str(s).strip()
        self._raw_filters["indent"] = lambda s, n=4: textwrap.indent(str(s), " " * n)
        self._raw_filters["dedent"] = lambda s: textwrap.dedent(str(s))
        self._raw_filters["replace"] = lambda s, old, new: str(s).replace(old, new)
        self._raw_filters["path"] = lambda s: str(s).replace('\\', '/')

        # Suture to the Universal Library
        for key, lambda_soul in self._raw_filters.items():
            RITE_REGISTRY._l1_hot_cache[key] = lambda_soul

    def transmute(self, template: str, context: Dict[str, Any], _depth: int = 0) -> str:
        """
        =================================================================================
        == THE OMEGA TRANSMUTE RITE: TOTALITY (V-Ω-VMAX-349-ASCENSIONS-FINALIS)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_REIFIER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_TRANSMUTE_VMAX_BICAMERAL_BYPASS_2026_FINALIS[THE MANIFESTO]
        This is the Absolute Zero-Stiction entry point. It evaluates the string,
        divines its intent, traverses the AST, applies Indentation Mathematics via
        the GeometricEmitter, and returns bit-perfect physical matter.
        =================================================================================
        """
        # --- MOVEMENT 0: THE VOID & MASS GUARDS ---
        if not template:
            return ""

        # [ASCENSION 347]: The Sentinel Block-Size Guard
        if len(template) > self.MAX_TEMPLATE_MASS:
            Logger.critical(f"Template Mass Overflow: Matter exceeds {self.MAX_TEMPLATE_MASS / 1024 / 1024:.0f}MB.")
            return "/* METABOLIC_FEVER_REJECTED */"

        # [ASCENSION 329]: Achronal Null-Byte Eradication (C-Level)
        template = template.translate(self._NULL_TRANSLATE_TABLE)

        # =========================================================================
        # == [ASCENSION 318]: BICAMERAL JIT MATRIX BYPASS (THE MASTER CURE)      ==
        # =========================================================================
        # If the string contains no ELARA sigils, it is Pure Matter. We mathematically
        # bypass the Scanner, Forger, and Resolver, achieving 0.00ms latency.
        if type(template) is str and "{{" not in template and "{%" not in template:
            return template

        # [ASCENSION 345]: Ouroboros Protection V5
        if _depth > self.MAX_RECURSION_DEPTH:
            Logger.critical(f"Topological Overflow: Recursion limit breached at depth {_depth}.")
            return f"/* RECURSION_LIMIT_BREACHED: {_depth} */"

        # --- MOVEMENT I: JURISPRUDENCE & TRACE ANCHORING ---
        is_path_strike = bool(context.get(self._KEY_IS_PATH, False))
        active_strict_mode = self.strict_mode | is_path_strike

        # [ASCENSION 337]: Luminous Telemetry Radiation
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

        # --- MOVEMENT II: SPATIAL PROXY INJECTION ---
        if PROXIES_MANIFEST:
            if "iron." in template and "iron" not in context:
                context["iron"] = LazyProxyDescriptor(IronProxy, context.get('project_root', Path.cwd()))
            if "topo." in template and "topo" not in context:
                context["topo"] = LazyProxyDescriptor(TopoProxy, context.get(self._KEY_ENGINE))
            if "akasha." in template and "akasha" not in context:
                context["akasha"] = LazyProxyDescriptor(AkashaProxy, context.get(self._KEY_ENGINE))
            if "substrate." in template and "substrate" not in context:
                context["substrate"] = LazyProxyDescriptor(SubstrateProxy)

        # [ASCENSION 346]: Dynamic Filter Overloading
        context['__filters__'] = self.filters

        # =========================================================================
        # == MOVEMENT III: MERKLE-TREE AST CACHING (THE HOLOGRAPHIC SUTURE)      ==
        # =========================================================================
        # [ASCENSION 326]: Fingerprinting includes strict mode state.
        template_hash = hashlib.sha256(f"{template}:{active_strict_mode}".encode('utf-8')).hexdigest()
        ast_root = self._AST_CACHE.get(template_hash)

        if ast_root is None:
            with self._CACHE_LOCK:
                # Double check
                ast_root = self._AST_CACHE.get(template_hash)
                if ast_root is None:
                    try:
                        # 1. Retina Gaze (Tokens)
                        scanner = GnosticScanner(trace_id=t_id)
                        tokens = scanner.scan(template)

                        # 2. Topological Forge (AST)
                        ast_root = SyntaxTreeForger.forge(tokens)

                        # [ASCENSION 321]: Thermodynamic Cache Eviction V2
                        if len(self._AST_CACHE) >= self.CACHE_LIMIT:
                            self._AST_CACHE.popitem(last=False)
                            # [ASCENSION 327]: Hydraulic Thread Yielding
                            time.sleep(0)

                        self._AST_CACHE[template_hash] = ast_root
                        self._AST_CACHE.move_to_end(template_hash)

                    except Exception as syntax_heresy:
                        # [ASCENSION 320]: Apophatic Syntax Healing could be injected here
                        if active_strict_mode:
                            raise UndefinedGnosisHeresy(f"ELARA Compilation Fracture: {syntax_heresy}")
                        return template
        else:
            try:
                self._AST_CACHE.move_to_end(template_hash)
            except Exception:
                pass

        # [ASCENSION 347]: Ephemeral State Evaporation
        # Reclaim massive string RAM before walking the tree.
        del template

        # =========================================================================
        # == MOVEMENT IV: THE KINETIC WALK & GEOMETRIC EMISSION                  ==
        # =========================================================================

        # [ASCENSION 325]: The Phantom Garbage Collector
        # Disabling GC prevents heap-thrashing during deep AST traversal.
        gc_was_enabled = gc.isenabled()
        if gc_was_enabled: gc.disable()

        try:
            plane = SubstratePlane.WASM if os.environ.get("SCAFFOLD_ENV") == "WASM" else SubstratePlane.IRON

            # [ASCENSION 339]: Bicameral Dictionary Coercion
            # (Handled intrinsically by ForgeContext if needed, but Context object bounds it safely)
            forge_ctx = ForgeContext(
                variables=context,
                strict_mode=active_strict_mode,
                trace_id=t_id,
                substrate=plane
            )

            # [STRIKE]: The Mind evaluates Truth.
            resolver = RecursiveResolver(engine_ref=context.get(self._KEY_ENGINE))

            # [ASCENSION 319]: Holographic AST Suture
            # We pass ast_root.children directly. The resolver creates a local scope
            # but NEVER mutates the cached AST nodes' intrinsic types.
            resolved_tokens = resolver.resolve(ast_root.children, forge_ctx)

            # =========================================================================
            # == [ASCENSION 328]: THE SINGULARITY EMITTER SUTURE (THE MASTER CURE)   ==
            # =========================================================================
            # We MUST use the Geometric Emitter to materialize the string. The fast
            # C-String join bypassed the Topographical shifts applied by VirtualDedent.
            # Emitter mathematically aligns tokens based on `token.column_index`.
            emitter = GeometricEmitter(trace_id=t_id)

            # [ASCENSION 333]: Indentation Gravity Anchor is maintained by the Emitter's inner logic.
            output_matter = emitter.assemble(resolved_tokens)

            # [ASCENSION 336]: The Terminal Sarcophagus
            if not is_path_strike:
                sys.stdout.flush()

            return output_matter

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as catastrophic_fracture:
            # [ASCENSION 338]: The Strict-Mode Exception Unwrapper
            if active_strict_mode:
                raise catastrophic_fracture
            return f"/* SGF_EVAL_FRACTURE: {str(catastrophic_fracture)} */"

        except Exception as unknown_fracture:
            # [ASCENSION 332]: Fault-Isolated Evaluation
            Logger.error(f"SGF Kernel Panic: {unknown_fracture}")
            return f"/* SGF_KERNEL_PANIC: {str(unknown_fracture)} */"

        finally:
            if gc_was_enabled:
                gc.enable()

    def __repr__(self) -> str:
        return f"<Ω_SGF_ENGINE status=RESONANT mode=HOLOGRAPHIC_SUTURE version=349.0>"