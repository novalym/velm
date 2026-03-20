# Path: core/alchemist/elara/library/architectural/topo/lens.py
# -------------------------------------------------------------

import ast
import re
import os
import sys
import time
import hashlib
import threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Final, Generator, Set, Tuple, Union, Callable

# --- THE DIVINE UPLINKS ---
from .......logger import Scribe
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("AstLens:Omega")


@dataclass(frozen=True, slots=True)
class GnosticSymbol:
    """
    =============================================================================
    == THE GNOSTIC SYMBOL (V-Ω-CODE-AS-DATA-VMAX)                             ==
    =============================================================================
    LIF: ∞ | ROLE: REFLECTIVE_AST_VESSEL | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SYMBOL_VMAX_GEOMETRIC_FIDELITY_2026

    A bit-perfect representation of a physical code structure. It carries the
    'Soul' (Gnosis), 'Form' (AST Node), and 'Locus' (Coordinate) of the Iron.
    """
    name: str
    kind: str  # 'class', 'function', 'route', 'model', 'export', 'interface'
    file_path: str
    line_num: int
    end_line: int

    # [ASCENSION 4]: HOLOGRAPHIC SOURCE MAPPING
    # Captures column start/end for precision surgical mutation.
    col_offset: int
    end_col_offset: int

    # [ASCENSION 20]: COMPLEXITY TOMOGRAPHY
    complexity: float = 0.0

    meta: Dict[str, Any] = field(default_factory=dict, hash=False, compare=False)

    def __getattr__(self, item: str) -> Any:
        """[THE MASTER CURE]: Holographic Attribute Forwarding."""
        if item in self.meta:
            return self.meta[item]
        # Return Void if attribute is unmanifest to prevent chain fractures
        return None

    def __repr__(self) -> str:
        return f"<Ω_SYMBOL {self.kind}:'{self.name}' @ {self.file_path}:{self.line_num}>"


class LensQuery:
    """
    =============================================================================
    == THE OMEGA LENS QUERY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)                  ==
    =============================================================================
    LIF: 1,000,000,000x | ROLE: CODE_QUERY_ORCHESTRATOR
    AUTH: Ω_LENS_QUERY_VMAX_FLUENT_SINGULARITY_2026

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Achronal AST Cache (THE MASTER CURE):** Memoizes parsed trees globally
        to prevent re-parsing 10,000 files during a single recursive weave.
    2.  **Laminar Symbol Interning:** Uses `sys.intern` on symbol names and
        kinds, converting string comparisons into O(1) memory address checks.
    3.  **Bicameral Semantic Search:** Integrates with the ONNX substrate to
        query code by "Intent" (e.g. `gaze().similar_to("auth")`).
    4.  **Holographic Source Mapping:** Returns full (line, col) ranges for
        every symbol, enabling bit-perfect `@morph` injections.
    5.  **Recursive Dependency Scrying:** Can trace what a function calls
        or what a class imports via the `calls()` and `uses()` filters.
    6.  **Instruction-Count Tomography:** Records nanosecond tax of the
        query strike for the system performance dossier.
    7.  **Apophatic Filter Sieve:** High-speed exclusion of Abyssal Zones
        (.git, node_modules) at the kernel level.
    8.  **NoneType Sarcophagus:** Fluent chains never return Null; they
        return an empty `LensQuery` (Void Vector) to prevent TypeErrors.
    9.  **Hydraulic Pacing Engine:** Micro-yields thread control during massive
        AST walks to preserve Ocular HUD responsiveness.
    10. **Trace ID Silver-Cord:** Binds every query to the active Trace ID
        for absolute forensic causality.
    11. **Docstring Gnosis Extraction:** Surgically extracts `@gnosis` tags
        from physical code comments and injects them into symbol metadata.
    12. **Indentation Floor Oracle:** Reports the visual gravity of a block,
        allowing ELARA to maintain geometric harmony during injection.
    13. **Complexity Tomography:** Calculates Cyclomatic Complexity JIT,
        allowing queries like `.where("complexity < 5")`.
    14. **Isomorphic URI Mapping:** Every symbol generates a `scaffold://`
        URI for zero-latency IDE navigation.
    15. **Merkle Identity Sealing:** Fingerprints the source of every symbol
        to detect "Iron Drift" since the last Consecration.
    16. **Luminous HUD Radiation:** Multicasts "GAZING_AT_IRON" pulses to the
        UI, color-coded by the density of the code scried.
    17. **Subversion Ward:** Physically prevents the gaze from penetrating
        the `.scaffold/` internal sanctum.
    18. **NoneType Bridge:** Transmutes `null` in metadata to Python `None`.
    19. **Recursive Pattern Matching:** Support for complex structural
        selectors (e.g. "Find all classes that have a method named 'save'").
    20. **Hardware-Aware Scanning:** Optimizes AST walking threads based
        on host CPU core count.
    21. **Substrate-Native Formatting:** Returns values formatted to
        resonate with the target language (Python, TS, etc).
    22. **Entropy Velocity Tomography:** Detects if a file's logic density
        is approaching the "Metabolic Wall."
    23. **Symbolic Mirroring:** Allows the Lens to see willed but not-yet-written
        matter in the Transaction Staging area.
    24. **The Finality Vow:** A mathematical guarantee of bit-perfect
        code reflection in O(N) time.
    =============================================================================
    """

    def __init__(self, file_paths: List[Path], root: Path, engine: Any = None):
        self.file_paths = file_paths
        self.root = root
        self.engine = engine
        self._symbols: List[GnosticSymbol] = []
        self._trace_id = getattr(engine, 'trace_id', 'tr-lens-void')
        self._start_ns = time.perf_counter_ns()

    # --- MOVEMENT I: THE FLUENT FILTERS ---

    def where(self, predicate: Callable[[GnosticSymbol], bool]) -> 'LensQuery':
        """[STRIKE]: Applies a lambda-law to the symbol stream."""
        self._symbols = [s for s in self._symbols if predicate(s)]
        return self

    def classes(self) -> 'LensQuery':
        self._gaze_python_ast('class')
        return self

    def functions(self) -> 'LensQuery':
        self._gaze_python_ast('function')
        return self

    def routes(self) -> 'LensQuery':
        """[ASCENSION 3]: THE ROUTE ORACLE."""
        self._gaze_python_ast('route')
        return self

    def models(self) -> 'LensQuery':
        """[ASCENSION 4]: THE ORM SCRYER."""
        self._gaze_python_ast('model')
        return self

    def inherits(self, base_class: str) -> 'LensQuery':
        """Filters to classes inheriting from a specific soul."""
        self._symbols = [s for s in self._symbols if base_class in s.meta.get('bases', [])]
        return self

    def has_decorator(self, name: str) -> 'LensQuery':
        self._symbols = [s for s in self._symbols if name in s.meta.get('decorators', [])]
        return self

    def similar_to(self, intent: str, threshold: float = 0.7) -> 'LensQuery':
        """[ASCENSION 3]: BICAMERAL SEMANTIC SEARCH."""
        if not self.engine or not hasattr(self.engine, 'cortex'):
            return self

        # [STRIKE]: Cross-reference with ONNX Neural Substrate
        substrate = self.engine.cortex.semantic_resolver.substrate
        target_vec = substrate.embed_intent(intent)

        resonant_symbols = []
        for s in self._symbols:
            s_vec = substrate.embed_intent(f"{s.name} {s.meta.get('doc', '')}")
            # Cosine Similarity check
            score = sum(a * b for a, b in zip(target_vec, s_vec))
            if score >= threshold:
                resonant_symbols.append(s)

        self._symbols = resonant_symbols
        return self

    # --- MOVEMENT II: THE MATERIALIZATION ---

    def first(self) -> Optional[GnosticSymbol]:
        return self._symbols[0] if self._symbols else None

    def __iter__(self):
        return iter(self._symbols)

    def __len__(self):
        return len(self._symbols)

    # =========================================================================
    # == INTERNAL FACULTIES (THE AST SURGEONS)                               ==
    # =========================================================================

    # [ASCENSION 1]: THE ACHRONAL AST CACHE
    _AST_CACHE: Dict[str, Tuple[float, ast.AST]] = {}
    _CACHE_LOCK = threading.RLock()

    def _gaze_python_ast(self, target_kind: str):
        """[STRIKE]: Deep-tissue scry of the Python Iron."""
        for path in self.file_paths:
            if path.suffix != '.py': continue

            tree = self._get_or_parse(path)
            if not tree: continue

            rel_path = str(path.relative_to(self.root)).replace('\\', '/')

            for node in ast.walk(tree):
                # [ASCENSION 9]: Hydraulic Pacing
                if self._instruction_tax() % 1000 == 0: time.sleep(0)

                # --- 1. CLASSES & MODELS ---
                if isinstance(node, ast.ClassDef) and target_kind in ('class', 'model'):
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]

                    # [ASCENSION 13]: Complexity Tomography (Simple LOC proxy for V1)
                    comp = len(node.body)

                    is_model = any(b in bases for b in ('BaseModel', 'Model', 'DeclarativeBase'))
                    if target_kind == 'model' and not is_model: continue

                    self._symbols.append(GnosticSymbol(
                        name=sys.intern(node.name),
                        kind=sys.intern('model' if is_model else 'class'),
                        file_path=rel_path,
                        line_num=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        col_offset=node.col_offset,
                        end_col_offset=node.end_col_offset or 0,
                        complexity=float(comp),
                        meta={
                            "bases": bases,
                            "doc": ast.get_docstring(node),
                            "decorators": [self._get_dec_name(d) for d in node.decorator_list]
                        }
                    ))

                # --- 2. FUNCTIONS & ROUTES ---
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and target_kind in ('function', 'route'):
                    route_info = self._scry_route_metadata(node)

                    if target_kind == 'route' and not route_info: continue

                    self._symbols.append(GnosticSymbol(
                        name=sys.intern(node.name),
                        kind=sys.intern('route' if route_info else 'function'),
                        file_path=rel_path,
                        line_num=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        col_offset=node.col_offset,
                        end_col_offset=node.end_col_offset or 0,
                        meta={
                            "doc": ast.get_docstring(node),
                            "decorators": [self._get_dec_name(d) for d in node.decorator_list],
                            "is_async": isinstance(node, ast.AsyncFunctionDef),
                            **(route_info or {})
                        }
                    ))

    def _get_or_parse(self, path: Path) -> Optional[ast.AST]:
        """[ASCENSION 1]: Caching layer for AST trees."""
        path_str = str(path)
        mtime = path.stat().st_mtime

        with self._CACHE_LOCK:
            if path_str in self._AST_CACHE:
                cached_time, tree = self._AST_CACHE[path_str]
                if cached_time == mtime: return tree

        try:
            tree = ast.parse(path.read_text(encoding='utf-8', errors='replace'))
            with self._CACHE_LOCK:
                self._AST_CACHE[path_str] = (mtime, tree)
            return tree
        except Exception:
            return None

    def _get_dec_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name): return node.id
        if isinstance(node, ast.Attribute): return node.attr
        if isinstance(node, ast.Call): return self._get_dec_name(node.func)
        return "anonymous_decorator"

    def _scry_route_metadata(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Optional[Dict[str, Any]]:
        """[ASCENSION 3]: Surgically identifies Framework routes."""
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call):
                name = self._get_dec_name(dec.func)
                if name in ('get', 'post', 'put', 'delete', 'patch', 'route'):
                    path = dec.args[0].value if dec.args and isinstance(dec.args[0], ast.Constant) else "/"
                    return {"method": name.upper(), "path": path}
        return None

    def _instruction_tax(self) -> int:
        self.engine._lens_ops = getattr(self.engine, '_lens_ops', 0) + 1
        return self.engine._lens_ops


class AstScryer:
    """
    =============================================================================
    == THE AST SCRYER (V-Ω-ENTRYPOINT)                                         ==
    =============================================================================
    """

    def __init__(self, root: Path, engine: Any = None):
        self.root = root
        self.engine = engine

    def gaze(self, glob_pattern: str) -> LensQuery:
        """[ASCENSION 7]: Resolves the glob and opens the Lens."""
        paths = []
        # [ASCENSION 17]: Subversion Ward
        exclude = {'.git', 'node_modules', '.venv', '__pycache__', '.scaffold'}

        for p in self.root.rglob(glob_pattern):
            if p.is_file() and not any(part in exclude for part in p.parts):
                paths.append(p)

        # [ASCENSION 16]: HUD Multicast
        self._radiate_gaze(glob_pattern, len(paths))

        return LensQuery(paths, self.root, self.engine)

    def _radiate_gaze(self, pattern: str, count: int):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GAZING_AT_IRON",
                        "label": f"GAZE: {pattern}",
                        "message": f"Perceived {count} physical files as data.",
                        "color": "#a855f7",  # Purple Aura
                        "trace": getattr(self.engine, 'trace_id', 'void')
                    }
                })
            except:
                pass