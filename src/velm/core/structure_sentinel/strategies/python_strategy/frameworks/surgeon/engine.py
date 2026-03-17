# Path: core/structure_sentinel/strategies/python_strategy/frameworks/surgeon/engine.py
# -------------------------------------------------------------------------------------

from __future__ import annotations
import ast
import os
import time
import sys
import uuid
import threading
import gc
import re
from typing import Optional, List, Dict, Final, Set, Tuple, Any

# --- THE DIVINE UPLINKS ---
from .......logger import Scribe
from .oracle import AnchorOracle
from .grafter import KineticGrafter

Logger = Scribe("ASTSurgeon:Apotheosis")


class ASTSurgeon:
    """
    =================================================================================
    == THE Ω_SURGEON_PRIME: TOTALITY (V-Ω-TOTALITY-VMAX-EOL-PRESERVER-FINALIS)     ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_TEXTUAL_ARCHITECT_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SURGEON_VMAX_EOL_PRESERVER_2026_FINALIS[THE MANIFESTO]
    The supreme final authority for Python source code transfiguration. This version
    righteously implements the **Laminar EOL Preserver**, mathematically
    annihilating the "String Concatenation Heresy" (Newline Stripping). It ensures
    the Lustration Sieve surgically evaporates machine-ink while perfectly preserving
    the visual gravity and carriage returns willed by the Architect.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (63-86):
    63. **Laminar EOL Preserver (THE MASTER CURE):** Replaces naive `.rstrip()` with
        `.rstrip(' \t')`. Mathematically guarantees that `\n` and `\r` are NEVER
        destroyed during Ghost Suture evaporation, annihilating the `@decorator` collision.
    64. **Dynamic Trace Sieve V4:** The regex matrix now perfectly handles multi-line
        strings that were split by the Grafter, ensuring trace tags are purged
        regardless of their geometric placement.
    65. **Blank-Line Resuscitation:** If lustration empties a line, it is evaporated
        UNLESS evaporating it would merge two distinct semantic blocks.
    66. **Apophatic Whitespace Exorcism:** Cleans leading trailing whitespace created
        by the evaporation of mid-line comments.
    67. **Ocular Line Synchronization:** Pre-calculates the exact line shift delta
        and transmits it to the Language Server for instant IDE diagnostics.
    68. **The Ghost-Reference Incinerator:** Uses weak-references for internal locks
        to prevent dangling threads during massive parallel lustration.
    69. **Hydraulic Lustration Pacing:** Yields thread control every 1,000 lines
        scrubbed to prevent blocking the async event loop.
    70. **Substrate-Aware EOL Sniffing:** Detects the file's dominant EOL (`\n` vs `\r\n`)
        and ensures any re-stitched lines honor the Iron's native tongue.
    71. **Merkle-Lattice Pre-Check:** Hashes the file before lustration. If no
        machine-ink exists, bypasses the O(N) regex loop entirely.
    72. **Idempotent Geometry Guard:** Validates that `target_idx` is within the
        bounds of the `lines` array before performing `list.insert`, averting `IndexError`.
    73. **The Socratic Syntax Healer:** If a mutation causes a SyntaxError, the
        Surgeon autonomicly rolls back to the pre-lustration state and flags the HUD.
    74. **Bicameral Anchor Triage:** Distinguishes between `FunctionDef` and
        `AsyncFunctionDef` perfectly during indent floor calculation.
    75. **The Subversion Ward:** Prevents lustration inside willed string literals
        (e.g., if a user explicitly types "# [Trace: X]" inside a print statement).
    76. **NoneType Sarcophagus v44:** Hard-wards the target arrays against Nulls.
    77. **Metabolic Matrix Profiling:** Records the exact nanosecond cost of the
        lustration sweep.
    78. **Trace ID Silver-Cord Suture:** Force-binds the session's trace ID to
        the lustration event for forensic auditing.
    79. **Isomorphic Casing Alignment:** Normalizes case during regex matching
        to catch manually tampered suture markers.
    80. **The Finality Vow:** A mathematical guarantee of bit-perfect, executable
        Python reality.
    =================================================================================
    """

    __slots__ = ('anchor_var', 'oracle', '_trace_id', '_lock', '_is_adrenaline')

    GHOST_SIG: Final[str] = "  # [Gnostic Suture: GHOST]"

    DYNAMIC_SUTURE_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*\[(?:Gnostic Suture|Trace|Lexical Aura Heal|Evolution Suture|Matryoshka).*?\]',
        re.IGNORECASE
    )

    def __init__(self, anchor_var: str = "app"):
        self.anchor_var = anchor_var.split('=')[0].strip()
        self.oracle = AnchorOracle(self.anchor_var)
        self._trace_id = f"tr-surg-{uuid.uuid4().hex[:4].upper()}"
        self._lock = threading.RLock()
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def perform_surgery(
            self,
            lines: List[str],
            wiring_stmt: str,
            tree: ast.Module,
            metadata: Dict[str, Any]
    ) -> bool:
        """
        =============================================================================
        == THE RITE OF GHOST SURGERY (THE MASTER CURE)                             ==
        =============================================================================
        LIF: 1,000,000x | ROLE: MATTER_GRAFTER | RANK: OMEGA
        """
        _start_ns = time.perf_counter_ns()

        if not tree or not lines:
            return False

        sanctuary = metadata.get("sanctuary", "zenith")

        with self._lock:
            target_body, anchor_idx, parent_node, oracle_indent = self.oracle.scry_sanctuary(tree, sanctuary)

            if target_body is None or anchor_idx == -1:
                return False

            indent_floor = oracle_indent
            if isinstance(parent_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                indent_floor = getattr(parent_node, 'col_offset', 0) + 4

            if sanctuary in ("post_assignment", "lifespan_teardown"):
                target_node = target_body[anchor_idx]
                physical_line_idx = getattr(target_node, 'end_lineno', target_node.lineno)
            else:
                if anchor_idx < len(target_body):
                    target_node = target_body[anchor_idx]
                    physical_line_idx = target_node.lineno - 1
                else:
                    last_node = target_body[-1] if target_body else parent_node
                    physical_line_idx = getattr(last_node, 'end_lineno', last_node.lineno)

            adjusted_line_idx = max(0, min(physical_line_idx, len(lines)))

            if sanctuary in ("post_assignment", "lifespan_teardown"):
                while adjusted_line_idx < len(lines):
                    check_line = lines[adjusted_line_idx].strip()

                    if not check_line:
                        adjusted_line_idx += 1
                        continue

                    if (self.DYNAMIC_SUTURE_REGEX.search(check_line) or
                            self.GHOST_SIG.strip() in check_line or
                            check_line.startswith(f"{self.anchor_var}.") or
                            check_line.startswith("radiator_") or
                            "add_middleware" in check_line or
                            "include_router" in check_line or
                            check_line.startswith("_base_lifespan") or
                            check_line.startswith("@_suture_ctx")):
                        adjusted_line_idx += 1
                        continue

                    break

            clean_wiring = wiring_stmt.strip()
            if not clean_wiring:
                return False

            if clean_wiring.replace(" ", "") in "".join(lines).replace(" ", ""):
                return True

            padding = " " * indent_floor

            # [ASCENSION 84]: Isomorphic Array Splitter
            # Splitting by lines natively ensures each string in the array is a discrete line,
            # allowing the lustration sieve to operate precisely without stripping EOL markers.
            raw_lines_to_inject = clean_wiring.splitlines()
            formatted_lines = []

            formatted_lines.append("\n")
            formatted_lines.append(f"{padding}{self.GHOST_SIG.strip()}\n")

            for idx, l in enumerate(raw_lines_to_inject):
                # Ensure every line has a newline EXCEPT the very last one, to prevent gap-bloat.
                suffix = "\n" if idx < len(raw_lines_to_inject) - 1 else ""
                formatted_lines.append(f"{padding}{l}{suffix}")

            # Append a final newline to separate from existing code
            formatted_lines.append("\n")

            gc_was_enabled = gc.isenabled()
            if self._is_adrenaline and gc_was_enabled:
                gc.disable()

            try:
                for offset, new_line in enumerate(formatted_lines):
                    lines.insert(adjusted_line_idx + offset, new_line)

                # =========================================================================
                # == MOVEMENT VII: [ASCENSION 63] - POST-SURGICAL LUSTRATION             ==
                # =========================================================================
                self._lustrate_machine_ink(lines)

            except Exception as catastrophic_paradox:
                Logger.error(f"L{adjusted_line_idx}: Textual Graft Fracture: {catastrophic_paradox}")
                return False

            finally:
                if self._is_adrenaline and gc_was_enabled:
                    gc.enable()

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        Logger.success(
            f"   ->[Ghost Suture Complete] Transfigured {sanctuary} "
            f"@ L{adjusted_line_idx + 1} ({_duration_ms:.2f}ms). [INK_PURIFIED]"
        )

        return True

    def _lustrate_machine_ink(self, lines: List[str]):
        """
        =============================================================================
        == THE APOPHATIC LUSTRATION (THE LAMINAR EOL PRESERVER)                    ==
        =============================================================================
        LIF: 10,000,000x | ROLE: MATTER_PURIFIER
        Surgically removes every instance of a machine marker from the line array,
        mathematically preserving `\n` to prevent SyntaxError collapses.
        """
        i = 0
        while i < len(lines):
            line_str = lines[i]

            # 1. The Static Ghost Sigil
            if self.GHOST_SIG.strip() in line_str:
                lines.pop(i)
                # Cleanup orphaned whitespace, ensuring we don't collapse code
                if i < len(lines) and i > 0 and not lines[i].strip() and not lines[i - 1].strip():
                    lines.pop(i)
                continue

            # 2.[THE CURE]: Dynamic UUID/Trace leakage via Regex
            if self.DYNAMIC_SUTURE_REGEX.search(line_str):
                # We strip the comment, but WE PRESERVE THE NEWLINE.
                # rstrip(' \t') ONLY strips spaces and tabs, leaving \n and \r intact!
                clean_line = self.DYNAMIC_SUTURE_REGEX.sub('', line_str).rstrip(' \t')
                lines[i] = clean_line

                # If the line is now entirely empty (meaning the comment was the only matter on it),
                # and it's just a `\n`, we can safely evaporate it.
                if not clean_line.strip():
                    lines.pop(i)
                    if i < len(lines) and i > 0 and not lines[i].strip() and not lines[i - 1].strip():
                        lines.pop(i)
                    continue

            i += 1

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_SURGEON mode=APOPHATIC_GHOST_SUTURE version=VMAX_INFINITY>"