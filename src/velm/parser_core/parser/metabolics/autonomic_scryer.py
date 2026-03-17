# Path: parser_core/parser/metabolics/autonomic_scryer.py
# -------------------------------------------------------

"""
=================================================================================
== THE OMEGA AUTONOMIC SCRYER: TOTALITY (V-Ω-TOTALITY-VMAX-GENOMIC-FINALIS)    ==
=================================================================================
LIF: ∞^∞ | ROLE: IMPLICIT_DNA_EXTRACTOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_SCRYER_VMAX_DNA_DECODER_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
The supreme final authority for implicit dependency discovery. This version
righteously incinerates the "Dependency Mirage" by scrying the physical and
virtual reality manifest for hidden imports across all major languages.
=================================================================================
"""
import collections
import re
import time
import hashlib
import threading
from typing import List, Tuple, Set, Final, Dict, Any, Optional
from ....contracts.data_contracts import ScaffoldItem
from ....logger import Scribe

Logger = Scribe("AutonomicScryer")


class AutonomicScryer:
    """
    The High-Performance Implicit Dependency Oracle.
    Transmutes raw source code into a purified set of external requirements.
    """

    # [ASCENSION 4 & 5]: THE POLYGLOT GRAMMAR MATRIX (O(1) Vectorized)
    # Python: Standard and relative imports, warded against comments
    PY_RX: Final[re.Pattern] = re.compile(
        r'^\s*(?:from\s+(?!\.)(?P<from_mod>[a-zA-Z0-9_.]+)\s+import|import\s+(?P<imp_mod>[a-zA-Z0-9_.,\s]+))',
        re.MULTILINE
    )

    # Node/JS: ESM, CommonJS, and Scoped Packages
    NODE_RX: Final[re.Pattern] = re.compile(
        r'(?:from|import)\s+[\'"](?P<esm>[@a-zA-Z0-9_.-/]+)[\'"]|'
        r'require\s*\(\s*[\'"](?P<cjs>[@a-zA-Z0-9_.-/]+)[\'"]\s*\)|'
        r'import\s*\(\s*[\'"](?P<dyn>[@a-zA-Z0-9_.-/]+)[\'"]\s*\)',
        re.MULTILINE
    )

    # Rust: Cargo dependencies
    RUST_RX: Final[re.Pattern] = re.compile(r'^\s*use\s+(?P<mod>[a-zA-Z0-9_]+)::', re.MULTILINE)

    # Go: Module imports
    GO_RX: Final[re.Pattern] = re.compile(r'^\s*import\s+(?P<mod>[\'"][a-zA-Z0-9_./-]+[\'"])', re.MULTILINE)

    # [ASCENSION 2]: THE TYPE-CHECKING SANCTUARY WARD
    # Identifies code blocks that never execute at runtime
    PY_TYPE_CHECK_BLOCK: Final[re.Pattern] = re.compile(r'if\s+TYPE_CHECKING:.*?(?=\n\S|$)', re.DOTALL)
    NODE_TYPE_ONLY: Final[re.Pattern] = re.compile(r'import\s+type\s+.*?;', re.MULTILINE)

    # [ASCENSION 1]: THE DIFFERENTIAL MERKLE CACHE
    _SCRY_MEMO: Dict[str, Tuple[Set[str], Set[str]]] = {}
    _MEMO_LOCK = threading.RLock()

    @classmethod
    def scry_matter(cls, items: List[ScaffoldItem], variables: Dict[str, Any]) -> Tuple[
        Set[str], Set[str], Dict[str, Set[str]]]:
        """
        =============================================================================
        == THE RITE OF GENOMIC EXTRACTION (V-Ω-TOTALITY)                           ==
        =============================================================================
        LIF: 1,000,000x | ROLE: DNA_EXTRACTOR
        """
        start_ns = time.perf_counter_ns()

        python_total: Set[str] = set()
        node_total: Set[str] = set()
        others: Dict[str, Set[str]] = collections.defaultdict(set)

        trace_id = variables.get("trace_id", "tr-scry-void")

        for item in items:
            # --- PHASE 0: THE VOID & BINARY GUARD ---
            if not item.content or item.is_dir or item.is_binary:
                continue

            # [ASCENSION 1]: DIFFERENTIAL MERKLE CHECK
            # If the item has a hash and we've scried it before, reuse the Gnosis.
            item_hash = getattr(item, 'merkle_hash', hashlib.md5(item.content.encode()).hexdigest())

            with cls._MEMO_LOCK:
                if item_hash in cls._SCRY_MEMO:
                    p, n = cls._SCRY_MEMO[item_hash]
                    python_total.update(p)
                    node_total.update(n)
                    continue

            # --- PHASE 1: PURIFICATION ---
            # Remove comments and Type-Checking blocks to prevent phantom debt
            clean_content = item.content
            ext = item.path.suffix.lower() if item.path else ""

            if ext == '.py':
                clean_content = cls.PY_TYPE_CHECK_BLOCK.sub('', clean_content)
                # Remove single line comments for scrying purity
                clean_content = re.sub(r'#.*$', '', clean_content, flags=re.MULTILINE)
            elif ext in ('.ts', '.tsx', '.js', '.jsx'):
                clean_content = cls.NODE_TYPE_ONLY.sub('', clean_content)
                clean_content = re.sub(r'//.*$', '', clean_content, flags=re.MULTILINE)

            # --- PHASE 2: MULTIVERSAL INHALATION ---
            p_deps, n_deps = set(), set()

            # [MOVEMENT I]: PYTHON DNA
            if ext == '.py':
                for match in cls.PY_RX.finditer(clean_content):
                    from_mod, imp_mod = match.groups()
                    target = from_mod if from_mod else imp_mod
                    if target:
                        for sub_mod in target.split(','):
                            root = sub_mod.strip().split('.')[0]
                            if root and not root.startswith('.'): p_deps.add(root)

            # [MOVEMENT II]: NODE DNA
            elif ext in ('.js', '.ts', '.jsx', '.tsx'):
                for match in cls.NODE_RX.finditer(clean_content):
                    esm, cjs, dyn = match.group('esm'), match.group('cjs'), match.group('dyn')
                    target = esm or cjs or dyn
                    if target:
                        # [ASCENSION 11]: Scoped Package Normalizer
                        if target.startswith('@'):
                            parts = target.split('/')
                            if len(parts) >= 2: n_deps.add(f"{parts[0]}/{parts[1]}")
                        elif not target.startswith('.'):
                            n_deps.add(target.split('/')[0])

            # [MOVEMENT III: SYSTEM LANGUAGES]
            elif ext == '.rs':
                for m in cls.RUST_RX.finditer(clean_content): others['rust'].add(m.group('mod'))
            elif ext == '.go':
                for m in cls.GO_RX.finditer(clean_content): others['go'].add(m.group('mod').strip('"\''))

            # --- PHASE 3: CONSECRATION ---
            python_total.update(p_deps)
            node_total.update(n_deps)

            # Update Memo-Matrix
            with cls._MEMO_LOCK:
                if len(cls._SCRY_MEMO) > 5000: cls._SCRY_MEMO.clear()
                cls._SCRY_MEMO[item_hash] = (p_deps, n_deps)

            # [ASCENSION 9]: Hydraulic Yield
            if len(python_total) + len(node_total) % 100 == 0: time.sleep(0)

        # --- METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if duration_ms > 50.0:
            Logger.verbose(f"Deep-Tissue Scry complete in {duration_ms:.2f}ms. [Trace: {trace_id}]")

        return python_total, node_total, dict(others)

    def __repr__(self) -> str:
        return f"<Ω_AUTONOMIC_SCRYER status=RESONANT mode=GENOMIC_DECODER cache={len(self._SCRY_MEMO)}>"