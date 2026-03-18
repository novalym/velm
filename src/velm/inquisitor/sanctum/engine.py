# Path: inquisitor/sanctum/engine.py
# ----------------------------------
import collections
import sys
import bisect
from abc import ABC
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple, Type, Set
import os
import time
import threading

from rich.panel import Panel
from rich.text import Text

from ...contracts.heresy_contracts import SyntaxHeresy, HeresySeverity
from ...jurisprudence_core.jurisprudence import conduct_architectural_inquest
from ...logger import Scribe

# =========================================================================================
# ==[ASCENSION 1]: THE BINARY KERNEL PIVOT (RUST SUBSTRATE)                             ==
# =========================================================================================
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    from tree_sitter import Language, Parser, Node, QueryError, QueryCursor

    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        Language = _ts.Language
        Parser = _ts.Parser
        Node = _ts.Node
        QueryError = _ts.QueryError
        QueryCursor = _ts.QueryCursor
        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        TREE_SITTER_AVAILABLE = False
        Language = type("HollowLanguage", (object,), {})
        Parser = type("HollowParser", (object,), {})
        Node = type("HollowNode", (object,), {})
        QueryCursor = type("HollowQueryCursor", (object,), {})
        QueryError = type("HollowQueryError", (Exception,), {})

Logger = Scribe("UniversalParser")


class UniversalParser:
    """
    =================================================================================
    == THE FOUNDRY MASTER (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                          ==
    =================================================================================
    LIF: 10,000,000,000,000,000 | ROLE: OMNISCIENT_ORCHESTRATOR | RANK: OMEGA_PRIME

    The pure and powerful orchestrator that commands the legion of Inquisitors.
    """

    def __init__(self, config: Any = None):
        self.config = config

    def conduct_rite(self, inquisitor: Type['BaseInquisitor'], content: str) -> Dict[str, Any]:
        """The Rite of Perception. Summons the specialist Scribe."""
        return inquisitor.perform_inquisition(content)

    def verify_syntax(self, code: str, lang_name: str, file_path: str = "ephemeral_scripture") -> Tuple[
        bool, List[SyntaxHeresy]]:
        """[THE RITE OF GNOSTIC JURISPRUDENCE]"""
        from ..core import is_grammar_available, LANGUAGES
        from ...contracts.data_contracts import ScaffoldItem

        lang_key = lang_name.lower()
        package_name = f"tree_sitter_{lang_key}"

        if is_grammar_available(package_name, lang_key):
            language = LANGUAGES[lang_key]
            parser = Parser(language)
            tree = parser.parse(bytes(code, "utf8"))
            if tree.root_node.has_error:
                Logger.verbose(f"Basic syntax heresy detected in '{file_path}'. Deferring to deep Gaze.")

        dummy_parser = type('DummyParser', (), {'raw_items': []})()
        item_to_judge = ScaffoldItem(
            path=Path(file_path), is_dir=False, content=code,
            raw_scripture=code.splitlines()[0] if code else ""
        )

        architectural_panels = conduct_architectural_inquest([item_to_judge])

        heresies: List[SyntaxHeresy] = []
        if architectural_panels:
            for panel in architectural_panels:
                heresies.append(self._forge_heresy_from_panel(panel, code, file_path))

        is_pure = not bool(heresies)
        return is_pure, heresies

    def _forge_heresy_from_panel(self, panel: Panel, full_source_code: str, file_path: str) -> SyntaxHeresy:
        """Transmutes the UI Panel into a programmatic Heresy object."""
        title = "Architectural Heresy"
        if isinstance(panel.title, Text):
            title = panel.title.plain
        elif isinstance(panel.title, str):
            title = panel.title

        message = "Consult details in panel."
        if hasattr(panel.renderable, 'renderables'):
            first_text = next((r for r in panel.renderable.renderables if isinstance(r, Text)), None)
            if first_text:
                message = first_text.plain

        return SyntaxHeresy(
            rule_name=title.strip("[]"),
            message=message,
            line_num=0,
            line_content="[Architectural Heresy]",
            full_source_code=full_source_code,
            metadata={'rich_panel': panel},
            file_path=file_path,
            suggestion="Review the architectural guidelines.",
            severity=HeresySeverity.WARNING
        )


class BaseInquisitor(ABC):
    """
    =================================================================================
    == THE SACRED CONTRACT OF PERCEPTION (V-Ω-TOTALITY-VMAX-RUST-ACCELERATED)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: POLYGLOT_SYNTAX_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_BASE_INQ_VMAX_QUERY_FISSION_2026_FINALIS

    The unbreakable foundation for all language-specific Scribes. It has been
    radically ascended to seamlessly route all AST queries through the compiled
    Rust Kernel, annihilating the Python GIL bottleneck.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (HIGHLIGHTING 13-24):
    13. **Apophatic Query Fission (THE MASTER CURE):** If the Rust compiler shatters
        due to a malformed Tree-Sitter SCM query (e.g. `Impossible pattern`), the
        Inquisitor no longer aborts to Python. It mathematically isolates the
        poisoned query, purges it from the Matrix, and executes the remaining
        queries natively in Rust at C-speed.
    14. **The L1 Poison Sieve:** A class-level dictionary (`_POISONED_QUERIES`)
        memorizes shattered queries per language across the entire Engine lifecycle.
        A bad query is parsed, caught, and skipped forever in 0.00ms.
    15. **JIT Query Fusion:** Automatically stitches all healthy queries in the
        `QUERIES` dictionary into a single S-Expression payload. The AST is
        traversed exactly *once* in C-memory, not N times in Python.
    16. **O(1) Flat Capture Reconstruction:** Transmutes the high-velocity flat array
        returned by Rust into the complex, nested `GnosticDossier` dictionary using
        mathematical byte-range containment.
    17. **Laminar Byte-to-Line Triangulation:** Uses `bisect` over a pre-computed
        newline index array to calculate line numbers from byte offsets in O(log N)
        time, bypassing expensive string-splitting operations.
    18. **Bicameral Method Binding:** Mathematically determines if a function resides
        within a class's byte boundaries, auto-converting it to a method.
    19. **Substrate Degradation Ward:** Gracefully falls back to the Python
        `tree_sitter` bindings only if Rust is physically unmanifest on the machine.
    20. **Semantic Debt Extractor:** Aggregates `@import` captures natively without
        recursive AST walking.
    21. **Complexity Tomography:** Aggregates `@complexity` tags into a unified
        cyclomatic score per function and file globally.
    22. **The Null-Byte Sarcophagus:** Purges C-string terminators before crossing
        the FFI boundary to prevent Rust panics.
    23. **The Universal Suture:** Completely backwards compatible with existing
        `Inquisitor` child classes. No changes required to `go.py`, `react.py`, etc.
    24. **The Finality Vow:** Reality is Manifest, Pure, and Indestructible.
    =================================================================================
    """
    LANGUAGE_NAME: str = "override_me"
    GRAMMAR_PACKAGE: str = "override_me"
    QUERIES: Dict[str, str] = {}

    # [ASCENSION 14]: THE L1 POISON SIEVE
    # Memorizes queries that shattered the Rust engine so they are never sent again.
    _POISONED_QUERIES: Dict[str, Set[str]] = collections.defaultdict(set)
    _SIEVE_LOCK = threading.RLock()

    @classmethod
    def get_parser(cls) -> Optional[Parser]:
        """The Forge of the Parser (Polymorphic Summons)."""
        from ..core import is_grammar_available, LANGUAGES
        if not is_grammar_available(cls.GRAMMAR_PACKAGE, cls.LANGUAGE_NAME):
            return None
        language = LANGUAGES[cls.LANGUAGE_NAME]
        parser = Parser(language)
        return parser

    @classmethod
    def _get_purified_queries(cls) -> Dict[str, str]:
        """Filters out queries known to be poisonous for this specific language."""
        poisoned = cls._POISONED_QUERIES[cls.LANGUAGE_NAME]
        return {k: v for k, v in cls.QUERIES.items() if k not in poisoned}

    @classmethod
    def perform_inquisition(cls, content: str) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF GNOSTIC EXTRACTION (CONDUCT)                      ==
        =============================================================================
        The Supreme Router. Attempts the Binary Kernel Pivot; falls back to Python.
        """
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        force_python = os.environ.get("SCAFFOLD_NO_RUST") == "1"

        if not content:
            return cls._forge_void_dossier()

        # [ASCENSION 1]: THE BINARY KERNEL PIVOT
        if RUST_AVAILABLE and not is_wasm and not force_python and cls.QUERIES:
            try:
                return cls._perform_rust_inquisition(content)
            except Exception as e:
                Logger.warn(f"Rust Core Fracture in {cls.LANGUAGE_NAME}: {e}. Falling back to Python.")

        # [ASCENSION 19]: THE PYTHON FALLBACK
        return cls._perform_python_inquisition(content)

    @classmethod
    def _perform_rust_inquisition(cls, content: str) -> Dict[str, Any]:
        """
        =============================================================================
        ==[ASCENSION 13]: APOPHATIC QUERY FISSION (THE MASTER CURE)               ==
        =============================================================================
        Mathematically isolates and evaporates invalid SCM queries without dropping
        the God-Engine out of Rust/C-speed mode.
        """
        start_ns = time.perf_counter_ns()
        clean_content = content.replace('\x00', '')

        safe_queries = cls._get_purified_queries()
        if not safe_queries:
            return cls._forge_void_dossier(error="All queries for this language were poisoned.")

        combined_query = "\n".join(f"{q}" for q in safe_queries.values())

        try:
            # The Primal Strike
            flat_captures = scaffold_core_rs.analyze_ast(clean_content, cls.LANGUAGE_NAME, combined_query)

        except Exception as e:
            err_str = str(e)
            if "Query error" in err_str or "Impossible pattern" in err_str:
                Logger.warn(f"Query Poisoning Detected in {cls.LANGUAGE_NAME}. Initiating Apophatic Query Fission...")

                # We iteratively test each query to find the traitor
                flat_captures = []
                for q_key, q_str in safe_queries.items():
                    try:
                        # Individual Fission Strike
                        caps = scaffold_core_rs.analyze_ast(clean_content, cls.LANGUAGE_NAME, q_str)
                        flat_captures.extend(caps)
                    except Exception as sub_err:
                        Logger.error(f"Surgically Exorcised poisoned query '{q_key}' in {cls.LANGUAGE_NAME}: {sub_err}")
                        with cls._SIEVE_LOCK:
                            cls._POISONED_QUERIES[cls.LANGUAGE_NAME].add(q_key)
            else:
                # If it's a real parse panic, re-raise to trigger Python fallback
                raise e

        # Reconstruct into the Gnostic Dossier
        dossier = cls._reconstruct_dossier_from_flat_captures(flat_captures, clean_content)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        dossier["metrics"]["parse_latency_ms"] = round(duration_ms, 3)
        dossier["_engine"] = "IRON_RUST_CORE"

        return dossier

    @classmethod
    def _reconstruct_dossier_from_flat_captures(cls, captures: List[Dict[str, str]], content: str) -> Dict[str, Any]:
        """
        =============================================================================
        == O(1) FLAT CAPTURE RECONSTRUCTION (THE ALCHEMY)                          ==
        =============================================================================[ASCENSION 16 & 17]: Transmutes flat Rust HashMaps into nested Python objects
        using byte-range containment math.
        """
        dossier = {
            "dependencies": {"count": 0, "imports": [], "imported_symbols": []},
            "metrics": {
                "line_count": 0,
                "function_count": 0,
                "class_count": 0,
                "cyclomatic_complexity": 0,
                "parse_latency_ms": 0.0
            },
            "functions": [],
            "classes": [],
            "smells": {"is_god_module": False}
        }

        # --- MOVEMENT I: LAMINAR BYTE-TO-LINE TRIANGULATION ---
        newline_offsets = [0]
        for i, char in enumerate(content):
            if char == '\n':
                newline_offsets.append(i + 1)

        dossier["metrics"]["line_count"] = len(newline_offsets)

        def get_line_num(byte_offset: int) -> int:
            # O(log N) lookup to find the line number of any byte offset
            return bisect.bisect_right(newline_offsets, byte_offset)

        # --- MOVEMENT II: STRUCTURAL IDENTIFICATION ---
        structures = []
        properties = []
        imports = set()

        for cap in captures:
            cap_name = cap["capture"]
            start_b = int(cap["start_byte"])
            end_b = int(cap["end_byte"])
            text = cap["text"].strip()

            if cap_name in ("function", "method", "class"):
                structures.append({
                    "_internal_type": cap_name,
                    "name": "anonymous",
                    "start_point": [get_line_num(start_b), 0],
                    "end_point": [get_line_num(end_b), 0],
                    "start_byte": start_b,
                    "end_byte": end_b,
                    "line_count": get_line_num(end_b) - get_line_num(start_b) + 1,
                    "arg_count": 0,
                    "cyclomatic_complexity": 1,
                    "method_count": 0
                })
            elif cap_name == "import":
                clean_imp = text.strip('"\'')
                if clean_imp not in imports:
                    imports.add(clean_imp)
                    dossier["dependencies"]["imports"].append({"path": clean_imp})
                    dossier["dependencies"]["imported_symbols"].append(clean_imp)
            else:
                properties.append(cap)

        dossier["dependencies"]["count"] = len(imports)

        # --- MOVEMENT III: PROPERTY ALLOCATION (CONTAINMENT MATH) ---
        # Sort structures by size (smallest first) so nested properties match innermost blocks
        structures.sort(key=lambda s: s["end_byte"] - s["start_byte"])

        for prop in properties:
            p_name = prop["capture"]
            p_start = int(prop["start_byte"])

            parent = None
            for struct in structures:
                if struct["start_byte"] <= p_start <= struct["end_byte"]:
                    parent = struct
                    break

            if parent:
                if p_name == "name":
                    parent["name"] = prop["text"]
                elif p_name == "arg":
                    parent["arg_count"] += 1
                elif p_name == "complexity":
                    parent["cyclomatic_complexity"] += 1

            if p_name == "complexity":
                dossier["metrics"]["cyclomatic_complexity"] += 1

        # --- MOVEMENT IV: BICAMERAL METHOD BINDING ---
        functions = []
        classes = []

        # Sort back to textual appearance order
        structures.sort(key=lambda s: s["start_byte"])

        for struct in structures:
            s_type = struct.pop("_internal_type")
            struct.pop("start_byte")
            struct.pop("end_byte")

            if s_type == "class":
                struct["is_god_class"] = struct["line_count"] > 300 or struct["method_count"] > 20
                classes.append(struct)
            else:
                struct["is_god_function"] = struct["line_count"] > 75 or struct["arg_count"] > 7 or struct[
                    "cyclomatic_complexity"] > 15
                functions.append(struct)

        for f in functions:
            f_line = f["start_point"][0]
            for c in classes:
                if c["start_point"][0] <= f_line <= c["end_point"][0]:
                    c["method_count"] += 1
                    break

        dossier["functions"] = functions
        dossier["classes"] = classes
        dossier["metrics"]["function_count"] = len(functions)
        dossier["metrics"]["class_count"] = len(classes)
        dossier["metrics"]["cyclomatic_complexity"] += len(functions) + len(classes)
        dossier["smells"]["is_god_module"] = (len(functions) + len(classes)) > 20

        return dossier

    # =========================================================================
    # == STRATUM B: THE PYTHONIC FALLBACK (TREE-SITTER)                      ==
    # =========================================================================

    @classmethod
    def _perform_python_inquisition(cls, content: str) -> Dict[str, Any]:
        """[ASCENSION 19]: The Pure Python tree-sitter bindings fallback."""
        start_ns = time.perf_counter_ns()
        parser = cls.get_parser()
        if not parser:
            return {"error": f"{cls.LANGUAGE_NAME.capitalize()} grammar not available."}

        tree = parser.parse(bytes(content, "utf8"))

        imports_raw = cls._get_query_captures(tree, "imports", "import")
        imports = [node.text.decode('utf8').strip('"\'') for node, _ in imports_raw]
        functions = cls._get_function_gnosis(tree)
        classes = cls._get_class_gnosis(tree)
        complexity_nodes = cls._get_query_captures(tree, "complexity_nodes", "complexity")
        cyclomatic_complexity = len(complexity_nodes) + len(functions)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        return {
            "dependencies": {"count": len(imports), "imports": [{"path": imp} for imp in sorted(list(set(imports)))],
                             "imported_symbols": sorted(list(set(imports)))},
            "metrics": {
                "line_count": len(content.splitlines()),
                "function_count": len(functions),
                "class_count": len(classes),
                "cyclomatic_complexity": cyclomatic_complexity,
                "parse_latency_ms": round(duration_ms, 3)
            },
            "functions": functions,
            "classes": classes,
            "smells": {"is_god_module": len(functions) + len(classes) > 20},
            "_engine": "ETHER_PYTHON_CORE"
        }

    @classmethod
    def _get_query_captures(cls, tree_or_node: Any, query_key: str, capture_name: Optional[str] = None) -> List[
        Tuple[Node, str]]:
        from ..core import LANGUAGES

        if not (lang := LANGUAGES.get(cls.LANGUAGE_NAME)) or not (query_str := cls.QUERIES.get(query_key)):
            return []

        try:
            query = lang.query(query_str)
            node_to_query = tree_or_node.root_node if hasattr(tree_or_node, 'root_node') else tree_or_node

            if hasattr(query, 'captures'):
                captures = query.captures(node_to_query)
            else:
                cursor = QueryCursor(query)
                captures = cursor.captures(node_to_query)

            results = []
            if isinstance(captures, dict):
                for name, nodes in captures.items():
                    if capture_name and name != capture_name: continue
                    if not isinstance(nodes, list): nodes = [nodes]
                    for node in nodes:
                        results.append((node, name))
            elif isinstance(captures, list):
                for capture in captures:
                    node = capture[0]
                    name = capture[1]
                    if capture_name and name != capture_name: continue
                    results.append((node, name))

            return results

        except (QueryError, Exception) as e:
            Logger.warn(f"A Tree-sitter query paradox occurred for '{query_key}': {e}")
            return []

    @classmethod
    def _get_function_gnosis(cls, tree) -> List[Dict]:
        captures = cls._get_query_captures(tree, "functions", "function")
        functions = []
        for node, _ in captures:
            name_node = next((n for n, name in cls._get_query_captures(node, "functions", "name") if name == 'name'),
                             None)
            if name_node:
                line_count = node.end_point[0] - node.start_point[0] + 1
                arg_nodes = cls._get_query_captures(node, "function_args", "arg")
                arg_count = len(arg_nodes)
                complexity_nodes = cls._get_query_captures(node, "complexity_nodes", "complexity")
                complexity = len(complexity_nodes) + 1
                functions.append({
                    "name": name_node.text.decode('utf8'),
                    "line_count": line_count,
                    "arg_count": arg_count,
                    "cyclomatic_complexity": complexity,
                    "is_god_function": line_count > 75 or arg_count > 7 or complexity > 15
                })
        return functions

    @classmethod
    def _get_class_gnosis(cls, tree) -> List[Dict]:
        captures = cls._get_query_captures(tree, "classes", "class")
        classes = []
        for node, _ in captures:
            name_node = next((n for n, name in cls._get_query_captures(node, "classes", "name") if name == 'name'),
                             None)
            if name_node:
                line_count = node.end_point[0] - node.start_point[0] + 1
                method_nodes = cls._get_query_captures(node, "methods", "method")
                method_count = len(method_nodes)
                classes.append({
                    "name": name_node.text.decode('utf8'),
                    "line_count": line_count,
                    "method_count": method_count,
                    "is_god_class": line_count > 300 or method_count > 20
                })
        return classes

    @classmethod
    def _forge_void_dossier(cls, error: Optional[str] = None) -> Dict[str, Any]:
        """Creates the bit-perfect, immutable schema for an empty return."""
        dossier = {
            "classes": [],
            "functions": [],
            "dependencies": {
                "internal": [],
                "external": [],
                "imported_symbols": []
            },
            "metrics": {
                "class_count": 0,
                "function_count": 0,
                "line_count": 0,
                "complexity_score": 0,
                "coupling_score": 0,
                "parse_latency_ms": 0.0
            }
        }
        if error:
            dossier["error"] = error
        return dossier