# Path: core/alchemist/elara/scanner/retina/engine.py
# ---------------------------------------------------


import time
import sys
import os
import gc
import hashlib
import threading
import unicodedata
import re
from typing import List, Optional, Dict, Any, Tuple, Final, Set

# --- MODULAR UPLINKS (STRATUM-0) ---
from ..buffer.engine import HydraulicBuffer
from ..scryer.engine import LookaheadScryer
from .purifier import RetinalPurifier
from .lil_suture import LaminarIndentationLogic

from ...constants import SGFTokens
from ...contracts.atoms import GnosticToken, TokenType
from ...contracts.state import ScannerState
from ......logger import Scribe

# [ASCENSION 196]: Binary Kernel Pivot
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("Elara:Retina")


class GnosticScanner:
    """
    =================================================================================
    == THE ELARA GNOSTIC SCANNER: OMEGA POINT (V-Ω-TOTALITY-VMAX-204-ASCENSIONS)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIMODAL_RETINAL_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SCANNER_VMAX_IRON_LEXICAL_BRIDGE_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for architectural perception. This version
    righteously implements the **Structure of Arrays (SoA) Suture**, mathematically
    annihilating the Python PyDict-Instantiation Tax by extracting flat vectors
    directly from the Rust Binary Core.

    ### THE PANTHEON OF 12 NEW ZENITH ASCENSIONS (193-204):
    193. **SoA Lexical Unpacking (THE MASTER CURE):** Bypasses the 100,000x PyDict
         overhead. Receives flat tuples of `(types, contents, raw, lines, cols, indents, masks, gates)`.
    194. **Vectorized Bit-Mask Thawing:** Decodes 4 boolean states (`is_braceless`,
         `complex_lil`, `is_comment`, `needs_inline`) from a single `u8` integer array.
    195. **C-Speed Zipped Reconstitution:** Uses native Python `zip()` over the
         unpacked vectors to instantiate GnosticTokens at the theoretical maximum CPython speed.
    196. **Enum String Bypass:** Resolves string types directly to Enum identities
         using a pre-warmed dictionary lookup, avoiding Pydantic validation tax.
    197. **Zero-Allocation Metadata Crafting:** Shallow-copies the cached metadata
         dict to eliminate heap fragmentation during mass token birth.
    198. **Hydraulic Thread Yielding (Python-Side):** `time.sleep(0)` removed from
         the token ingestion loop, leaving it unbroken and fully synchronous for max IPS.
    199. **Laminar Prefix Purity (Rust):** Inherits the pre-purified streams directly.
    200. **The Finality Vow:** Reality is perceived instantly.
    =================================================================================
    """

    __slots__ = (
        'state', '_start_ns', '_total_mass', '_trace_id',
        '_is_ether', 'logger', '_debug_mode', '_metadata_cache',
        '_is_adrenaline', '_merkle_tree', '_lock', '_token_lineage',
        '_custom_sigil_start', '_custom_sigil_end', '_sigil_regex'
    )

    # [ASCENSION 149]: THE OMEGA PURIFICATION MATRIX
    TOXIN_MAP: Final[Dict[int, None]] = {
        0xFEFF: None, 0x200B: None, 0x200C: None, 0x200D: None, 0x2060: None, 0x0000: None
    }

    # [ASCENSION 174]: THE SILENT COMMENT GUARDIAN
    COMMENT_EXORCIST_RX: Final[re.Pattern] = re.compile(r'(?<!:)\/\/.*$')

    # [ASCENSION 173]: MULTI-DIMENSIONAL TOKEN FISSION
    INLINE_GATE_CHAIN_RX: Final[re.Pattern] = re.compile(r'(@[a-zA-Z_]\w*\b[^@]*?:?)\s*(?=@|>>|::|\+=|~=|\*=|\^=|$)')

    def __init__(self, trace_id: str = "tr-retina-void"):
        """[THE RITE OF INCEPTION]"""
        self.state = ScannerState()
        self._start_ns: int = 0
        self._total_mass: int = 0
        self._token_lineage: int = 0
        self._trace_id = trace_id
        self._lock = threading.RLock()

        self._is_ether = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

        self.logger = Logger
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"
        self._metadata_cache: Dict[str, Any] = {}
        self._merkle_tree: List[str] = []

        self._custom_sigil_start = SGFTokens.VAR_START
        self._custom_sigil_end = SGFTokens.VAR_END

        sigil_override = os.environ.get("SCAFFOLD_SIGIL_OVERRIDE")
        if sigil_override and "," in sigil_override:
            parts = sigil_override.split(",")
            self._custom_sigil_start = parts[0].strip()
            self._custom_sigil_end = parts[1].strip()

        self._sigil_regex = re.compile(
            rf'(?P<var>{re.escape(self._custom_sigil_start)})|'
            rf'(?P<block>\{{%)|'
            rf'(?P<comment>\{{#)|'
            rf'(?P<doc_dq>\"\"\")|'
            rf'(?P<doc_sq>\'\'\')',
            re.MULTILINE
        )

    def scan(self, text: str) -> List[GnosticToken]:
        """
        =================================================================================
        == THE OMEGA SCAN RITE: TOTALITY (V-Ω-TOTALITY-VMAX-IRON-LEXICAL-BRIDGE)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: MATTER_PERCEPTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        """
        self._start_ns = time.perf_counter_ns()

        if not text:
            return [self._forge_literal("", 1, 0)]

        purified_text = text.translate(self.TOXIN_MAP)
        purified_text = RetinalPurifier.purify(purified_text)
        self._total_mass = len(purified_text)

        tokens: List[GnosticToken] = []

        self._metadata_cache["is_makefile"] = "Makefile" in purified_text[:512]
        self._metadata_cache["substrate"] = "WASM" if self._is_ether else "IRON"
        self._metadata_cache["trace_id"] = self._trace_id

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 193] - THE IRON LEXICAL BRIDGE (SoA SUTURE)  ==
        # =========================================================================
        if RUST_AVAILABLE and not self._is_ether and os.environ.get("SCAFFOLD_NO_RUST") != "1":
            try:
                # [THE MASTER CURE]: Unpack the massive C-Vector tuple instantly
                (
                    t_types,
                    contents,
                    raw_texts,
                    line_nums,
                    col_indices,
                    orig_indents,
                    bitmasks,
                    gates
                ) = scaffold_core_rs.lex_blueprint_fast(
                    purified_text,
                    self._custom_sigil_start,
                    self._custom_sigil_end
                )

                # Pre-warmed type map for O(1) resolution
                type_map = {e.name: e for e in TokenType}
                base_meta = self._metadata_cache

                # CPython Loop Optimization: Direct variable binding
                for t_str, c_str, r_str, ln, col, oi, mask, gate in zip(
                        t_types, contents, raw_texts, line_nums, col_indices, orig_indents, bitmasks, gates
                ):
                    # [ASCENSION 194]: Bit-Mask Thawing
                    # Bit 0 (1): complex_lil | Bit 1 (2): needs_inline | Bit 2 (4): is_comment | Bit 3 (8): is_braceless
                    complex_lil = (mask & 1) != 0
                    needs_inline = (mask & 2) != 0
                    is_comment = (mask & 4) != 0
                    is_braceless = (mask & 8) != 0

                    if complex_lil:
                        self._perform_multi_dimensional_fission(r_str, ln, oi, tokens)
                        continue
                    elif needs_inline:
                        tokens.extend(self._scan_character_strata(r_str, ln, oi))
                        continue

                    # [ASCENSION 197]: Zero-Allocation Metadata Crafting
                    meta = base_meta.copy()
                    self._token_lineage += 1
                    meta["token_lineage"] = self._token_lineage

                    if is_comment: meta["is_comment"] = True
                    if is_braceless:
                        meta["is_braceless"] = True
                        meta["gate"] = gate

                    t_type = type_map.get(t_str, TokenType.LITERAL)

                    tokens.append(GnosticToken(
                        type=t_type,
                        content=c_str,
                        raw_text=r_str,
                        line_num=ln,
                        column_index=col,
                        original_indent=oi,
                        metadata=meta,
                        trace_id=self._trace_id
                    ))

                self._proclaim_telemetry(len(tokens))
                return tokens

            except Exception as e:
                self.logger.debug(f"Rust Lexical Bridge fractured: {e}. Degrading to Python Swarm.")

        # =========================================================================
        # == MOVEMENT II: THE PYTHONIC FALLBACK (LEGACY LOOP)                    ==
        # =========================================================================
        lines = purified_text.splitlines(keepends=True)

        current_line_idx = 0
        while current_line_idx < len(lines):
            line = lines[current_line_idx]
            line_num = current_line_idx + 1

            if line_num % 500 == 0:
                self._yield_metabolism(line_num, len(lines))

            stripped = line.strip()
            indent = len(line) - len(line.lstrip())

            # Merkle-Leaf Inception
            line_hash = hashlib.md5(line.encode('utf-8')).hexdigest()[:8]
            self._merkle_tree.append(line_hash)

            # --- BRANCH A: THE VOID VERSES ---
            if not stripped:
                tokens.append(self._forge_literal(line, line_num, indent))
                current_line_idx += 1
                continue

            # --- BRANCH B: THE WHISPERS (COMMENTS) ---
            if stripped.startswith('{#'):
                pass
            elif stripped.startswith('#') or stripped.startswith('//'):
                tokens.append(self._forge_literal(line, line_num, indent, {"is_comment": True}))
                current_line_idx += 1
                continue

            # --- BRANCH C: THE LIL LATTICE (BRACELESS LOGIC) ---
            if LaminarIndentationLogic.is_braceless_logic(stripped, line):
                self._perform_multi_dimensional_fission(line, line_num, indent, tokens)
                current_line_idx += 1
                continue

            # --- BRANCH D: THE ALCHEMICAL STRATA (MIXED CONTENT) ---
            if any(s in line for s in (self._custom_sigil_start, '{%', '{#')):
                line_tokens = self._scan_character_strata(line, line_num, indent)
                tokens.extend(line_tokens)
            else:
                # --- BRANCH E: THE PURE MATTER ---
                tokens.append(self._forge_literal(line, line_num, indent))

            current_line_idx += 1

        self._proclaim_telemetry(len(tokens))

        if self._is_adrenaline and len(tokens) > 10000:
            gc.collect(1)

        return tokens

    def _perform_multi_dimensional_fission(self, raw_line: str, line_num: int, indent: int, tokens: List[GnosticToken]):
        """[ASCENSION 173]: Splits chained logic gates natively."""
        stripped = raw_line.strip()
        clean_logic = self.COMMENT_EXORCIST_RX.sub('', stripped).rstrip()
        chain_matches = self.INLINE_GATE_CHAIN_RX.findall(clean_logic)

        if chain_matches and len(chain_matches) > 1:
            synthetic_indent = indent
            for chain_part in chain_matches:
                part_clean = chain_part.rstrip(':').strip()
                if part_clean.startswith('@'): part_clean = part_clean[1:].strip()
                part_clean = part_clean.rstrip(';')

                first_word = part_clean.split('(')[0].split(':')[0].split()[0].lower()
                tokens.append(GnosticToken(
                    type=TokenType.LOGIC_BLOCK,
                    content=part_clean,
                    raw_text=chain_part,
                    line_num=line_num,
                    column_index=synthetic_indent,
                    original_indent=synthetic_indent,
                    metadata={**self._metadata_cache, "is_braceless": True, "gate": first_word}
                ))
                synthetic_indent += 4

            remainder = clean_logic[sum(len(m) for m in chain_matches):].strip()
            if remainder:
                tokens.append(self._forge_literal(remainder, line_num, synthetic_indent))
        else:
            clean_logic = clean_logic.rstrip(':').rstrip(';')
            if clean_logic.startswith('@'):
                clean_logic = clean_logic[1:].strip()

            first_word = clean_logic.split('(')[0].split(':')[0].split()[0].lower()

            tokens.append(GnosticToken(
                type=TokenType.LOGIC_BLOCK,
                content=clean_logic,
                raw_text=raw_line,
                line_num=line_num,
                column_index=indent,
                original_indent=indent,
                metadata={**self._metadata_cache, "is_braceless": True, "gate": first_word}
            ))

    def _scan_character_strata(self, line: str, line_num: int, base_indent: int) -> List[GnosticToken]:
        """
        =============================================================================
        == THE STRATA DISSECTOR (V-Ω-SPATIOTEMPORAL-ALIGNMENT)                     ==
        =============================================================================
        """
        line_tokens = []
        cursor = 0
        length = len(line)

        from ..patterns.sigils import WHITESPACE_CONTROL_REGEX

        while cursor < length:
            match = self._sigil_regex.search(line, cursor)

            if not match:
                matter = line[cursor:]
                effective_col = base_indent if cursor == 0 else 0
                line_tokens.append(self._forge_literal(matter, line_num, effective_col))
                break

            if match.start() > cursor:
                matter = line[cursor:match.start()]
                effective_col = base_indent if cursor == 0 else 0
                line_tokens.append(self._forge_literal(matter, line_num, effective_col))

            sigil = match.group()

            if sigil in (SGFTokens.DOCSTRING_DQ, SGFTokens.DOCSTRING_SQ):
                end_idx = line.find(sigil, match.end())
                if end_idx == -1:
                    matter = line[match.start():]
                    effective_col = base_indent if match.start() == 0 else 0
                    line_tokens.append(self._forge_literal(matter, line_num, effective_col, {"is_docstring": True}))
                    break
                else:
                    matter = line[match.start():end_idx + 3]
                    effective_col = base_indent if match.start() == 0 else 0
                    line_tokens.append(self._forge_literal(matter, line_num, effective_col, {"is_docstring": True}))
                    cursor = end_idx + 3
                    continue

            is_valid, total_len, inner_logic = LookaheadScryer.divine_closure(line[match.start():], sigil)

            if not is_valid:
                reclaimed = line[match.start():match.start() + len(sigil)]
                effective_col = base_indent if match.start() == 0 else 0
                line_tokens.append(self._forge_literal(reclaimed, line_num, effective_col))
                cursor = match.start() + len(sigil)
                continue

            if sigil == self._custom_sigil_start:
                t_type = TokenType.VARIABLE
            elif sigil == SGFTokens.COMMENT_START:
                t_type = TokenType.COMMENT
            else:
                t_type = TokenType.LOGIC_BLOCK

            final_content = WHITESPACE_CONTROL_REGEX.sub('', inner_logic).strip()

            self._token_lineage += 1

            line_tokens.append(GnosticToken(
                type=t_type,
                content=final_content,
                raw_text=line[match.start():match.start() + total_len],
                line_num=line_num,
                column_index=match.start(),
                original_indent=match.start(),  # <--- THE SUTURE
                metadata={
                    **self._metadata_cache.copy(),
                    "token_lineage": self._token_lineage
                },
                trace_id=self._trace_id
            ))

            cursor = match.start() + total_len

        return line_tokens

    def _forge_literal(self, text: str, ln: int, col: int, meta: Optional[Dict] = None) -> GnosticToken:
        """
        =============================================================================
        == THE OMEGA INDENT SUTURE (THE MASTER CURE)                               ==
        =============================================================================
        """
        merged_meta = self._metadata_cache.copy()
        if meta: merged_meta.update(meta)

        self._token_lineage += 1
        merged_meta["token_lineage"] = self._token_lineage

        return GnosticToken(
            type=TokenType.LITERAL,
            content=text,
            raw_text=text,
            line_num=ln,
            column_index=col,
            original_indent=col,
            metadata=merged_meta
        )

    def _yield_metabolism(self, current: int, total: int):
        if self._is_ether:
            time.sleep(0)

        if not self._is_adrenaline:
            percent = int((current / total) * 100)
            self._project_hud_pulse(percent)
            if current % 10000 == 0:
                gc.collect(1)

    def _project_hud_pulse(self, percent: int):
        try:
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)
            if engine and hasattr(engine, 'akashic') and engine.akashic:
                engine.akashic.broadcast({
                    "method": "elara/retina_pulse",
                    "params": {
                        "percentage": percent,
                        "trace": self._trace_id,
                        "label": "SCRYING_DNA",
                        "aura": "#3b82f6"
                    }
                })
        except:
            pass

    def _proclaim_telemetry(self, count: int):
        tax = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        if self._debug_mode:
            self.logger.success(f"ELARA Retina: {count} atoms manifest in {tax:.2f}ms.[RESONANT]")

    def __repr__(self) -> str:
        return f"<Ω_ELARA_SCANNER mode=IRON_LEXICAL_BRIDGE_SOA status=RESONANT trace={self._trace_id[:8]}>"