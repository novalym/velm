# // scaffold/artisans/translocate_core/resolvers/cpp/inquisitor.py
# -----------------------------------------------------------------
import sys
from typing import List

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # We attempt to speak with the native C-extension.
    from tree_sitter import QueryCursor

    TREE_SITTER_AVAILABLE = True
except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native tongue is absent, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        QueryCursor = _ts.QueryCursor
        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If no soul is manifest in any realm, we forge hollow vessels.
        TREE_SITTER_AVAILABLE = False

        # We forge a 'Hollow' type to allow the CppInquisitorEngine
        # to be imported without crashing.
        QueryCursor = type("HollowQueryCursor", (object,), {})

from .....inquisitor.core import is_grammar_available, LANGUAGES
from .....logger import Scribe
from .contracts import CppDetectedInclude

Logger = Scribe("CppInquisitor")


class CppInquisitorEngine:
    QUERY = """
    (preproc_include
      path: [
        (string_literal) @local
        (system_lib_string) @system
      ]
    )
    """

    @classmethod
    def scan(cls, content: str) -> List[CppDetectedInclude]:
        """
        =============================================================================
        == THE GAZE OF THE HEALER (V-Ω-TOTALITY-V200.12-ISOMORPHIC)                ==
        =============================================================================
        LIF: 10x | ROLE: CXX_INCLUDE_INQUISITOR | RANK: OMEGA

        Perceives #include directives in C and C++ scriptures. Engineered to
        synchronize property access between C-Extensions and WASM Proxies.
        =============================================================================
        """
        # [ASCENSION 1]: Functional Availability Check
        # Wards the rite against execution if the Tree-sitter mind is cold.
        if not TREE_SITTER_AVAILABLE:
            Logger.warn("C++ Gaze deferred: Tree-sitter unmanifested in this stratum.")
            return []

        # --- MOVEMENT I: LINGUISTIC SHARD TRIAGE ---
        # We support both 'cpp' and 'c' grammars for total coverage.
        lang_name = "cpp"
        if not is_grammar_available("tree_sitter_cpp", "cpp"):
            if is_grammar_available("tree_sitter_c", "c"):
                lang_name = "c"
            else:
                Logger.warn("C/C++ Linguistic Shards missing. Adjudication impossible.")
                return []

        lang = LANGUAGES[lang_name]

        try:
            # [MOVEMENT II: THE SUMMONS]
            # The Diamond Meta-Path Suture guarantees this import resolves to the Proxy in WASM.
            from tree_sitter import Parser
            parser = Parser()
            parser.set_language(lang)

            # [MOVEMENT III: THE STRIKE]
            # Transmute content to bytes for the engine.
            # Our Diamond Proxy handles both 'str' and 'bytes' for maximum resilience.
            source_bytes = content.encode("utf-8") if isinstance(content, str) else content
            tree = parser.parse(source_bytes)

            # Compile the query via the Language Proxy
            query = lang.query(cls.QUERY)

            # [MOVEMENT IV: THE CAPTURE]
            # Our Proxy returns a List[Tuple[Node, str]] to mirror the modern C-API.
            captures = query.captures(tree.root_node)

            results = []
            for node, name in captures:
                # [ASCENSION 1]: Gnostic Byte Parity
                # node.text returns bytes in both strata.
                # We strip the first and last char to excise the quotes or <brackets>.
                raw_text = node.text.decode('utf-8', errors='replace')
                path_value = raw_text[1:-1]

                # [ASCENSION 2]: Classification Triage
                # Differentiates between local (#include "...") and system (#include <...>)
                kind = 'local' if name == 'local' else 'system'

                # [ASCENSION 3]: Achronal Point Parity
                # node.start_point returns (row, col) in both C and WASM strata.
                results.append(CppDetectedInclude(
                    line_num=node.start_point[0] + 1,
                    path=path_value,
                    kind=kind,
                    start_byte=node.start_byte,
                    end_byte=node.end_byte
                ))

            return results

        except Exception as fracture:
            # [ASCENSION 11]: Forensic Fracture Capture
            Logger.error(f"C++ Topography Inquest shattered: {str(fracture)}")
            return []