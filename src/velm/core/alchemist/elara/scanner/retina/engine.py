# Path: core/alchemist/elara/scanner/retina/engine.py
# ---------------------------------------------------

import time
import sys
import os
import gc
from typing import List, Optional, Dict, Any

# --- MODULAR UPLINKS ---
from ..buffer.engine import HydraulicBuffer
from ..scryer.engine import LookaheadScryer
from .purifier import RetinalPurifier
from .lil_suture import LaminarIndentationLogic
from ..patterns.sigils import SIGIL_OR_DOCSTRING_REGEX, WHITESPACE_CONTROL_REGEX

from ...constants import SGFTokens
from ...contracts.atoms import GnosticToken, TokenType
from ...contracts.state import ScannerState
from ......logger import Scribe

Logger = Scribe("Elara:Retina")


class GnosticScanner:
    """
    =================================================================================
    == THE ELARA GNOSTIC SCANNER: OMEGA POINT (V-Ω-TOTALITY-VMAX-144-ASCENSIONS)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIMODAL_RETINAL_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    """

    __slots__ = (
        'state', '_start_ns', '_total_mass', '_trace_id',
        '_is_ether', 'logger', '_debug_mode', '_metadata_cache',
        '_is_adrenaline'
    )

    def __init__(self, trace_id: str = "tr-elara-retina-void"):
        self.state = ScannerState()
        self._start_ns: int = 0
        self._total_mass: int = 0
        self._trace_id = trace_id

        self._is_ether = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

        self.logger = Logger
        self._debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"
        self._metadata_cache: Dict[str, Any] = {}

    def scan(self, text: str) -> List[GnosticToken]:
        """Transmutes raw scripture into a stream of warded Gnostic Atoms."""
        self._start_ns = time.perf_counter_ns()
        if not text:
            return [self._forge_void_token()]

        # [MODULAR SUTURE]: Purify Text
        text = RetinalPurifier.purify(text)
        self._total_mass = len(text)

        buffer = HydraulicBuffer(text)
        tokens: List[GnosticToken] = []
        self.state = ScannerState()

        self._metadata_cache["is_makefile"] = "Makefile" in text[:512]
        self._metadata_cache["substrate"] = "WASM" if self._is_ether else "IRON"

        lines = text.splitlines(keepends=True)

        current_line_idx = 0
        while current_line_idx < len(lines):
            line = lines[current_line_idx]
            line_num = current_line_idx + 1

            if line_num % 1000 == 0:
                self._yield_metabolism(line_num, len(lines))

            stripped = line.strip()

            if not stripped:
                tokens.append(self._forge_literal(line, line_num, 0))
                current_line_idx += 1
                continue

            if stripped.startswith('{#') or stripped.startswith('{%') or stripped.startswith('{{'):
                pass
            elif stripped.startswith('#') or stripped.startswith('//'):
                tokens.append(self._forge_literal(line, line_num, 0, {"is_comment": True}))
                current_line_idx += 1
                continue

            indent = len(line) - len(line.lstrip())

            # [MODULAR SUTURE]: Laminar Indentation Logic
            if LaminarIndentationLogic.is_braceless_logic(stripped, line):
                clean_logic = stripped.rstrip(':')

                # [ASCENSION 145]: UNIVERSAL AT-SIGIL ALIASING
                # Automatically strip the leading @ so the Gate Router processes it perfectly.
                if clean_logic.startswith('@'):
                    clean_logic = clean_logic[1:].strip()

                first_word = clean_logic.split('(')[0].split(':')[0].split()[0].lower()

                tokens.append(GnosticToken(
                    type=TokenType.LOGIC_BLOCK,
                    content=clean_logic,
                    raw_text=line,
                    line_num=line_num,
                    column_index=indent,
                    metadata={**self._metadata_cache, "is_braceless": True, "gate": first_word}
                ))
                current_line_idx += 1
                continue

            if any(s in line for s in ('{{', '{%', '{#')):
                line_tokens = self._scan_character_strata(line, line_num, indent)
                tokens.extend(line_tokens)
            else:
                tokens.append(self._forge_literal(line, line_num, 0))

            current_line_idx += 1

        self._proclaim_telemetry(len(tokens))
        return tokens

    def _scan_character_strata(self, line: str, line_num: int, base_indent: int) -> List[GnosticToken]:
        line_tokens = []
        cursor = 0
        length = len(line)

        while cursor < length:
            match = SIGIL_OR_DOCSTRING_REGEX.search(line, cursor)

            if not match:
                matter = line[cursor:]
                line_tokens.append(self._forge_literal(matter, line_num, cursor))
                break

            if match.start() > cursor:
                matter = line[cursor:match.start()]
                line_tokens.append(self._forge_literal(matter, line_num, cursor))

            sigil = match.group()

            if sigil in (SGFTokens.DOCSTRING_DQ, SGFTokens.DOCSTRING_SQ):
                end_idx = line.find(sigil, match.end())
                if end_idx == -1:
                    matter = line[match.start():]
                    line_tokens.append(self._forge_literal(matter, line_num, match.start(), {"is_docstring": True}))
                    break
                else:
                    matter = line[match.start():end_idx + 3]
                    line_tokens.append(self._forge_literal(matter, line_num, match.start(), {"is_docstring": True}))
                    cursor = end_idx + 3
                    continue

            # [MODULAR SUTURE]: Divine Closure
            is_valid, total_len, inner_logic = LookaheadScryer.divine_closure(line[match.start():], sigil)

            if not is_valid:
                reclaimed = line[match.start():match.start() + len(sigil)]
                line_tokens.append(self._forge_literal(reclaimed, line_num, match.start()))
                cursor = match.start() + len(sigil)
                continue

            if sigil == SGFTokens.VAR_START:
                t_type = TokenType.VARIABLE
            elif sigil == SGFTokens.COMMENT_START:
                t_type = TokenType.COMMENT
            else:
                t_type = TokenType.LOGIC_BLOCK

            final_content = WHITESPACE_CONTROL_REGEX.sub('', inner_logic).strip()

            line_tokens.append(GnosticToken(
                type=t_type,
                content=final_content,
                raw_text=line[match.start():match.start() + total_len],
                line_num=line_num,
                column_index=match.start(),
                metadata=self._metadata_cache.copy(),
                trace_id=self._trace_id
            ))

            cursor = match.start() + total_len

        return line_tokens

    def _forge_literal(self, text: str, ln: int, col: int, meta: Optional[Dict] = None) -> GnosticToken:
        merged_meta = self._metadata_cache.copy()
        if meta: merged_meta.update(meta)
        return GnosticToken(type=TokenType.LITERAL, content=text, raw_text=text, line_num=ln, column_index=col,
                            metadata=merged_meta)

    def _forge_void_token(self) -> GnosticToken:
        return GnosticToken(type=TokenType.VOID, content="", raw_text="", line_num=1, column_index=0)

    def _yield_metabolism(self, current: int, total: int):
        if self._is_ether: time.sleep(0)
        if not self._is_adrenaline:
            percent = int((current / total) * 100)
            self._project_hud_pulse(percent)
            if current % 10000 == 0: gc.collect(1)

    def _project_hud_pulse(self, percent: int):
        try:
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)
            if engine and hasattr(engine, 'akashic') and engine.akashic:
                engine.akashic.broadcast({
                    "method": "elara/retina_pulse",
                    "params": {"percentage": percent, "trace": self._trace_id, "label": "SCRYING_DNA"}
                })
        except:
            pass

    def _proclaim_telemetry(self, count: int):
        tax = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        if self._debug_mode:
            self.logger.success(f"ELARA Retina: {count} atoms manifest in {tax:.2f}ms. [RESONANT]")

    def __repr__(self) -> str:
        return f"<Ω_ELARA_SCANNER mode=MULTIMODAL_LIL_SUTURE status=RESONANT trace={self._trace_id}>"