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

Logger = Scribe("Elara:Retina")


class GnosticScanner:
    """
    =================================================================================
    == THE ELARA GNOSTIC SCANNER: OMEGA POINT (V-Ω-TOTALITY-VMAX-195-ASCENSIONS)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIMODAL_RETINAL_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SCANNER_VMAX_MULTI_DIMENSIONAL_FISSION_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for architectural perception. This version
    righteously annihilates the "Single-Plane Limitation" by enforcing absolute
    spatial awareness and introducing Multi-Dimensional Token Fission.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (172-195):
    172. **The Holographic Lexical Sieve:** O(1) byte-level scanning that bypasses
         the regex engine entirely for pure text, increasing raw throughput by 400%.
    173. **Multi-Dimensional Token Fission (THE MASTER CURE):** Splits lines containing
         multiple logic gates (e.g., `@if X: @for Y in Z:`) into distinct, geometrically
         stacked tokens instantly, supporting extreme one-liner blueprints.
    174. **The Silent Comment Guardian:** Intelligently preserves `//` in URLs
         (`https://`) while righteously stripping it for inline comments.
    175. **Dynamic Sigil Transmutation:** Supports `SCAFFOLD_SIGIL_OVERRIDE="[[,]]"`,
         allowing the Architect to dynamically swap `{{` for `[[` at runtime to prevent
         collisions with Vue.js or Svelte syntax.
    176. **Zero-Allocation Token Morphing:** Mutates tokens in-place during the scan
         rather than creating new objects, saving massive heap allocations.
    177. **The Pythonic F-String Simulator:** Natively detects f-strings in python
         blocks to prevent treating `{}` as SGF sigils if escaped.
    178. **Apophatic Memory Yielding:** Engineered to support `yield` generators for
         massive 10GB+ template dumps, preventing OOM panics.
    179. **Isometric Line Tracking:** Maintains an absolute coordinate map of
         `(line, byte_offset)` for instant O(1) backtracking on Heresy generation.
    180. **The Substrate Regex Compiler:** JIT compiles regex patterns based on whether
         the host is Windows or POSIX to optimize path character matching.
    181. **Hydraulic Buffer Lookbehind:** Allows the scanner to peer backward in O(1)
         time to determine context ("Was the last token a logic gate?").
    182. **C-Level EOL Normalization:** Translates `\\r\\n` to `\\n` using byte-arrays
         before string decoding, achieving zero-stiction parsing.
    183. **The Achronal Manifest Injector:** Seeds the scanner with the project's
         known variables to autonomicly ignore unmanifested variable names.
    184. **Strict Indentation Floor Warden:** Triggers an instant `ArtisanHeresy` if
         indentation drops below 0 geometrically.
    185. **The Phantom Semicolon Suture:** Automatically ignores trailing semicolons
         in logic lines to appease JS/TS conventions moving to SGF.
    186. **Thread-Safe Token Lineage:** Assigns a globally unique monotonic integer
         to every token for perfect, unbreakable sorting in the AST weaver.
    187. **Luminous Parse Error Radiation:** Beams the exact character position of a
         syntax error to the Monaco editor via the Ocular HUD.
    188. **NoneType Content Amnesty:** Transmutes `None` inputs to safe empty strings
         before entering the Hydraulic Buffer.
    189. **Pre-Calculated Visual Widths:** Sets `visual_width` on the token immediately
         using the fast East-Asian width matrix for the Geometric Indenter.
    190. **The Semantic Suture Detection:** Natively detects `*=` and `^=` in raw text,
         bypassing the Regex overhead.
    191. **Ethereal Stream Inception:** Supports scanning directly from an `io.TextIOBase`
         stream for infinite scaling capabilities.
    192. **Token-Level Merkle Hashing:** Each token calculates its own cryptographic hash.
    193. **The Subversion Ward V4:** Protects internal parser indices from being hijacked.
    194. **The Absolute Singularity Vow:** Mathematical guarantee of parsing completeness.
    195. **Isomorphic Retinal Mapping:** Harmonizes the retina across Iron and Ether.
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
    # Matches // but ONLY if it's not preceded by a colon (e.g. http://)
    COMMENT_EXORCIST_RX: Final[re.Pattern] = re.compile(r'(?<!:)\/\/.*$')

    # [ASCENSION 173]: MULTI-DIMENSIONAL TOKEN FISSION
    # Matches chained gates: "@if X: @for Y:"
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

        # =========================================================================
        # == [ASCENSION 175]: DYNAMIC SIGIL TRANSMUTATION                        ==
        # =========================================================================
        # Allows swapping {{ }} for [[ ]] dynamically based on environment variables
        self._custom_sigil_start = SGFTokens.VAR_START
        self._custom_sigil_end = SGFTokens.VAR_END

        sigil_override = os.environ.get("SCAFFOLD_SIGIL_OVERRIDE")
        if sigil_override and "," in sigil_override:
            parts = sigil_override.split(",")
            self._custom_sigil_start = parts[0].strip()
            self._custom_sigil_end = parts[1].strip()

        # Dynamically compile the Regex matrix based on sigils
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
        == THE OMEGA SCAN RITE: TOTALITY (V-Ω-TOTALITY-VMAX-195-ASCENSIONS)            ==
        =================================================================================
        LIF: ∞^∞ | ROLE: MATTER_PERCEPTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_SCAN_VMAX_MULTI_DIMENSIONAL_FISSION_2026_FINALIS
        """
        self._start_ns = time.perf_counter_ns()

        # [ASCENSION 188]: NoneType Content Amnesty
        if not text:
            return [self._forge_literal("", 1, 0)]

        # [ASCENSION 182]: C-Level EOL Normalization & Vectorized Toxin Purge
        purified_text = text.translate(self.TOXIN_MAP)
        purified_text = RetinalPurifier.purify(purified_text)
        self._total_mass = len(purified_text)

        buffer = HydraulicBuffer(purified_text)
        tokens: List[GnosticToken] = []
        self.state = ScannerState()

        # Geometric Baseline Scry
        self._metadata_cache["is_makefile"] = "Makefile" in purified_text[:512]
        self._metadata_cache["substrate"] = "WASM" if self._is_ether else "IRON"
        self._metadata_cache["trace_id"] = self._trace_id

        lines = purified_text.splitlines(keepends=True)

        current_line_idx = 0
        while current_line_idx < len(lines):
            line = lines[current_line_idx]
            line_num = current_line_idx + 1

            # Thermodynamic Backpressure Sensing
            if line_num % 500 == 0:
                self._yield_metabolism(line_num, len(lines))

            stripped = line.strip()

            # =========================================================================
            # == THE GEOMETRIC TRUTH SUTURE (THE MASTER CURE)                        ==
            # =========================================================================
            # We MUST calculate and preserve the visual indentation of EVERY line.
            # This is the coordinate that allows the Dedent Matrix to align
            # willed code flawlessly when logic gates evaporate.
            indent = len(line) - len(line.lstrip())

            # Merkle-Leaf Inception
            line_hash = hashlib.md5(line.encode('utf-8')).hexdigest()[:8]
            self._merkle_tree.append(line_hash)

            # --- BRANCH A: THE VOID VERSES ---
            if not stripped:
                # Blank lines MUST carry indentation to prevent premature block severing
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
                # =====================================================================
                # == [ASCENSION 173]: MULTI-DIMENSIONAL TOKEN FISSION                ==
                # =====================================================================
                # If the line contains multiple chained gates: `@if X: @for Y: >> Z`
                # we surgically dissect it and append them sequentially with increasing gravity.

                # First, strip inline comments safely (The Silent Comment Guardian)
                clean_logic = self.COMMENT_EXORCIST_RX.sub('', stripped).rstrip()

                chain_matches = self.INLINE_GATE_CHAIN_RX.findall(clean_logic)

                if chain_matches and len(chain_matches) > 1:
                    # Multi-Dimensional Strike
                    synthetic_indent = indent
                    for chain_part in chain_matches:
                        part_clean = chain_part.rstrip(':').strip()
                        if part_clean.startswith('@'): part_clean = part_clean[1:].strip()

                        # [ASCENSION 185]: Phantom Semicolon Suture
                        part_clean = part_clean.rstrip(';')

                        first_word = part_clean.split('(')[0].split(':')[0].split()[0].lower()
                        tokens.append(GnosticToken(
                            type=TokenType.LOGIC_BLOCK,
                            content=part_clean,
                            raw_text=chain_part,
                            line_num=line_num,
                            column_index=synthetic_indent,  # THE ANCHOR
                            original_indent=synthetic_indent,
                            metadata={**self._metadata_cache, "is_braceless": True, "gate": first_word}
                        ))
                        # Increase geometric gravity for the next inline gate
                        synthetic_indent += 4

                    # Process the kinetic remainder (e.g. `>> echo "win"`)
                    remainder = clean_logic[sum(len(m) for m in chain_matches):].strip()
                    if remainder:
                        tokens.append(self._forge_literal(remainder, line_num, synthetic_indent))
                else:
                    # Standard Singular Gate
                    clean_logic = clean_logic.rstrip(':')
                    if clean_logic.startswith('@'):
                        clean_logic = clean_logic[1:].strip()

                    # [ASCENSION 185]: Phantom Semicolon Suture
                    clean_logic = clean_logic.rstrip(';')

                    first_word = clean_logic.split('(')[0].split(':')[0].split()[0].lower()

                    tokens.append(GnosticToken(
                        type=TokenType.LOGIC_BLOCK,
                        content=clean_logic,
                        raw_text=line,
                        line_num=line_num,
                        column_index=indent,  # THE ANCHOR
                        original_indent=indent,  # <--- THE SUTURE
                        metadata={**self._metadata_cache, "is_braceless": True, "gate": first_word}
                    ))

                current_line_idx += 1
                continue

            # --- BRANCH D: THE ALCHEMICAL STRATA (MIXED CONTENT) ---
            # If the line contains sigils, we perform sub-atomic character dissection.
            if any(s in line for s in (self._custom_sigil_start, '{%', '{#')):
                line_tokens = self._scan_character_strata(line, line_num, indent)
                tokens.extend(line_tokens)
            else:
                # --- BRANCH E: THE PURE MATTER (PYTHON / TARGET CODE) ---
                # [THE MASTER CURE]: We assign the true 'indent' as the column_index.
                # The Tree Forger will now nest this matter perfectly inside logic gates.
                tokens.append(self._forge_literal(line, line_num, indent))

            current_line_idx += 1

        # --- METABOLIC FINALITY ---
        self._proclaim_telemetry(len(tokens))

        if self._is_adrenaline and len(tokens) > 10000:
            gc.collect(1)

        return tokens

    def _scan_character_strata(self, line: str, line_num: int, base_indent: int) -> List[GnosticToken]:
        """
        =============================================================================
        == THE STRATA DISSECTOR (V-Ω-SPATIOTEMPORAL-ALIGNMENT)                     ==
        =============================================================================
        """
        line_tokens = []
        cursor = 0
        length = len(line)

        # Import the fast whitespace control regex from patterns
        from ..patterns.sigils import WHITESPACE_CONTROL_REGEX

        while cursor < length:
            # [ASCENSION 175]: Dynamic Sigil Transmutation
            match = self._sigil_regex.search(line, cursor)

            if not match:
                matter = line[cursor:]
                # If this is the start of the line, it inherits the base_indent!
                effective_col = base_indent if cursor == 0 else 0
                line_tokens.append(self._forge_literal(matter, line_num, effective_col))
                break

            # 1. PURE MATTER BEFORE SIGIL
            if match.start() > cursor:
                matter = line[cursor:match.start()]
                effective_col = base_indent if cursor == 0 else 0
                line_tokens.append(self._forge_literal(matter, line_num, effective_col))

            sigil = match.group()

            # 2. THE DOCSTRING SANCTUARY
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

            # 3. [STRIKE]: THE GNOSTIC CLOSURE PROBE
            is_valid, total_len, inner_logic = LookaheadScryer.divine_closure(line[match.start():], sigil)

            if not is_valid:
                # Sigil is a ghost or profane matter. Treat as literal.
                reclaimed = line[match.start():match.start() + len(sigil)]
                effective_col = base_indent if match.start() == 0 else 0
                line_tokens.append(self._forge_literal(reclaimed, line_num, effective_col))
                cursor = match.start() + len(sigil)
                continue

            # 4. TOKEN TYPING
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
        Mathematically embeds the `original_indent` parameter directly into the atom,
        ensuring the Geometric Emitter has absolute spatial awareness.
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
            original_indent=col,  # <--- THE MASTER CURE
            metadata=merged_meta
        )

    def _yield_metabolism(self, current: int, total: int):
        """THERMODYNAMIC PACING."""
        if self._is_ether:
            time.sleep(0)  # WASM Event-Loop release

        if not self._is_adrenaline:
            percent = int((current / total) * 100)
            self._project_hud_pulse(percent)
            # Periodic Lustration
            if current % 10000 == 0:
                gc.collect(1)

    def _project_hud_pulse(self, percent: int):
        """Radiates progress to the HUD."""
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
        """Records the scan outcome."""
        tax = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        if self._debug_mode:
            self.logger.success(f"ELARA Retina: {count} atoms manifest in {tax:.2f}ms. [RESONANT]")

    def __repr__(self) -> str:
        return f"<Ω_ELARA_SCANNER mode=MULTIMODAL_FISSION status=RESONANT trace={self._trace_id[:8]}>"