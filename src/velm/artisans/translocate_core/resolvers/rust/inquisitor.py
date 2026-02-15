# // scaffold/artisans/translocate_core/resolvers/rust/inquisitor.py
# ------------------------------------------------------------------
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
from .....inquisitor.sanctum.diagnostics.go import GoInquisitor  # Reuse base if needed, but Rust has its own
# We need to import the Rust Inquisitor from diagnostics if it exists, or use BaseInquisitor pattern
# Assuming a RustInquisitor class exists in diagnostics or we use BaseInquisitor logic here.
from .....inquisitor.core import is_grammar_available, LANGUAGES
from .....logger import Scribe
from .contracts import RustDetectedUse

Logger = Scribe("RustInquisitor")


class RustInquisitorEngine:
    # Query to capture the path part of a use declaration
    # use crate::foo::bar; -> crate::foo::bar
    QUERY = """
    (use_declaration
      argument: [
        (scoped_identifier) @path
        (identifier) @path
      ]
    )
    """

    @classmethod
    def scan(cls, content: str) -> List[RustDetectedUse]:
        """
        =============================================================================
        == THE GAZE OF THE HEALER: RUST (V-Ω-TOTALITY-V200.12-ISOMORPHIC)          ==
        =============================================================================
        LIF: 10x | ROLE: RUST_USE_INQUISITOR | RANK: OMEGA

        Perceives 'use' declarations within Rust scriptures. Engineered to
        synchronize property access between C-Extensions and WASM Proxies.
        =============================================================================
        """
        # [ASCENSION 1]: Functional Availability Check
        # Prevents execution if the Tree-sitter mind is cold or unmanifested.
        if not TREE_SITTER_AVAILABLE:
            Logger.warn("Rust Gaze deferred: Tree-sitter unmanifested in this stratum.")
            return []

        # [ASCENSION 8]: Linguistic Shard Verification
        # Checks the registry for the compiled Rust grammar shard.
        if not is_grammar_available("tree_sitter_rust", "rust"):
            Logger.warn("Rust Linguistic Shard missing. Adjudication impossible.")
            return []

        lang = LANGUAGES["rust"]

        try:
            # [MOVEMENT I: THE SUMMONS]
            # The Diamond Meta-Path Suture ensures 'tree_sitter' points to the Proxy in WASM.
            from tree_sitter import Parser
            parser = Parser()
            parser.set_language(lang)

            # [MOVEMENT II: THE STRIKE]
            # Transmute content to bytes for the engine.
            # The Diamond Proxy accepts both 'str' and 'bytes' for maximum resilience.
            source_bytes = content.encode("utf-8") if isinstance(content, str) else content
            tree = parser.parse(source_bytes)

            # Compile the query via the Language Proxy
            query = lang.query(cls.QUERY)

            # [MOVEMENT III: THE CAPTURE]
            # Our Proxy returns a List[Tuple[Node, str]] to mirror the modern C-API.
            captures = query.captures(tree.root_node)

            results = []
            for node, name in captures:
                # We filter for the 'path' capture group defined in our S-expression QUERY.
                if name == "path":
                    # [ASCENSION 1]: Achronal Point Parity
                    # node.start_point returns (row, col) in both C and WASM strata.
                    line_num = node.start_point[0] + 1

                    # [ASCENSION 2]: Gnostic Byte Parity
                    # node.text returns bytes. We decode to provide a clean string path.
                    path_text = node.text.decode('utf-8', errors='replace')

                    # [ASCENSION 3]: Geometric Offsets
                    # start_byte/end_byte are mapped in the Diamond Proxy __slots__.
                    results.append(RustDetectedUse(
                        line_num=line_num,
                        path=path_text,
                        start_byte=node.start_byte,
                        end_byte=node.end_byte
                    ))

            return results

        except Exception as fracture:
            # [ASCENSION 11]: Forensic Fracture Capture
            Logger.error(f"Rust Topography Inquest shattered: {str(fracture)}")
            return []