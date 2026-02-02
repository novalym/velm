"""
    =================================================================================
    == THE POLYGLOT SURGEONS (V-Ω-PRECISION-INSTRUMENTS)                           ==
    =================================================================================
    LIF: 10,000,000,000,000

    This sanctum houses the strategies for physical code insertion.
    They rely on the Gnosis provided by the `SemanticTarget` (location, type) to
    perform byte-perfect surgery on the source lines.

    ### THE PANTHEON OF STRATEGIES:
    1.  **The Pythonic Adept:** Masters the invisible structure of whitespace. It knows
        that to exist inside a Python block is to share its indentation level.
    2.  **The Brace Mason:** Masters the visible structure of enclosures. It hunts for
        the closing sigil (`}`) to nest content safely within C-Style blocks.
    """

import re
from textwrap import dedent, indent
from typing import List

from .contracts import SemanticTarget
from .....logger import Scribe

Logger = Scribe("SemanticStrategies")


class BaseStrategy:
    """The Ancestral Soul of Insertion logic."""

    @staticmethod
    def _prepare_fragment(fragment: str, target_indent: str) -> str:
        """
        [THE RITE OF NORMALIZATION]
        Dedents the raw fragment to remove accidental nesting, then re-indents it
        to match the target reality.
        """
        # 1. Strip leading/trailing empty lines to avoid gaps
        clean_frag = fragment.strip('\n')
        # 2. Dedent to base (remove common whitespace)
        dedented = dedent(clean_frag)
        # 3. Re-indent to target level
        indented = indent(dedented, target_indent)
        return indented


class PythonInsertionStrategy(BaseStrategy):
    """
    =============================================================================
    == THE PYTHONIC ADEPT (V-Ω-INDENTATION-MASTER)                             ==
    =============================================================================
    Handles insertion for Python, YAML, and other whitespace-sensitive tongues.
    """

    @staticmethod
    def insert(lines: List[str], target: SemanticTarget, fragment: str, mode: str) -> str:
        # 1. Calculate Base Indentation from the Definition Line
        # We look at the start_line (e.g., "class User:")
        start_line_content = lines[target.start_line]
        match = re.match(r"^(\s*)", start_line_content)
        base_indent = match.group(0) if match else ""

        insert_idx = 0
        block_content = ""

        # --- STRATEGY: INSERT INSIDE ---
        if mode == 'inside':
            # In Python, "Inside" means appending to the end of the block
            # with a deeper indentation level.

            # Standard Python indent is 4 spaces.
            # Future Ascension: Detect file's indentation style dynamically.
            target_indent = base_indent + "    "

            # The `end_line` from Tree-sitter usually points to the last line of code in the block.
            # We insert AFTER this line.
            insert_idx = target.end_line + 1

            # Forge the block
            processed_fragment = BaseStrategy._prepare_fragment(fragment, target_indent)
            block_content = f"\n{processed_fragment}\n"

        # --- STRATEGY: INSERT AFTER ---
        elif mode == 'after':
            # "After" means appending after the block, returning to the base indentation (or parent's).
            target_indent = base_indent

            # We insert AFTER the last line of the current block.
            insert_idx = target.end_line + 1

            processed_fragment = BaseStrategy._prepare_fragment(fragment, target_indent)
            # Double newline for PEP-8ish separation between top-level entities
            block_content = f"\n\n{processed_fragment}\n"

        else:
            Logger.warn(f"Unknown insertion mode '{mode}'. Surgery stayed.")
            return "".join(lines)

        # --- THE SURGICAL IMPLANTATION ---
        # We verify bounds to be safe against empty files or EOF edge cases
        if insert_idx > len(lines):
            insert_idx = len(lines)

        new_lines = lines[:insert_idx] + [block_content] + lines[insert_idx:]
        return "".join(new_lines)


class CStyleInsertionStrategy(BaseStrategy):
    """
    =============================================================================
    == THE BRACE MASON (V-Ω-BOUNDARY-MASTER)                                   ==
    =============================================================================
    Handles insertion for JS, TS, Go, Rust, Java, C, C++, C#.
    It relies on finding the sacred Closing Brace `}`.
    """

    @staticmethod
    def insert(lines: List[str], target: SemanticTarget, fragment: str, mode: str) -> str:
        # 1. Calculate Base Indentation
        start_line_content = lines[target.start_line]
        match = re.match(r"^(\s*)", start_line_content)
        base_indent = match.group(0) if match else ""

        insert_idx = 0
        block_content = ""

        # --- STRATEGY: INSERT INSIDE ---
        if mode == 'inside':
            # We must find the closing brace of the block.
            # Tree-sitter's `end_line` typically includes the closing brace.
            # We scan backwards from the end_line to find the line containing `}`.

            brace_line_idx = target.end_line
            found_brace = False

            # Safety valve: Don't scan up past the start line
            curr = brace_line_idx
            while curr >= target.start_line:
                # We look for a line that essentially ends the block.
                # Simple heuristic: contains '}'
                if '}' in lines[curr]:
                    brace_line_idx = curr
                    found_brace = True
                    break
                curr -= 1

            if not found_brace:
                # Fallback: If tree-sitter says it ends here, but we can't find '}',
                # we append to the end_line anyway, hoping it's valid (e.g. implicit blocks).
                Logger.warn(f"Closing brace not found for '{target.name}'. Appending blindly at end of range.")
                brace_line_idx = target.end_line

            # We insert BEFORE the closing brace line to be "inside".
            insert_idx = brace_line_idx

            # Standard C-Style indent (often 2 or 4 spaces).
            # We default to 2 spaces (common for JS/TS/Go/Rust in modern tooling).
            # Prophecy: Detect from file content.
            target_indent = base_indent + "  "

            processed_fragment = BaseStrategy._prepare_fragment(fragment, target_indent)
            block_content = f"\n{processed_fragment}\n"

        # --- STRATEGY: INSERT AFTER ---
        elif mode == 'after':
            # We insert AFTER the closing brace line.
            insert_idx = target.end_line + 1
            target_indent = base_indent

            processed_fragment = BaseStrategy._prepare_fragment(fragment, target_indent)
            block_content = f"\n\n{processed_fragment}\n"

        else:
            Logger.warn(f"Unknown insertion mode '{mode}'. Surgery stayed.")
            return "".join(lines)

        # --- THE SURGICAL IMPLANTATION ---
        if insert_idx > len(lines):
            insert_idx = len(lines)

        new_lines = lines[:insert_idx] + [block_content] + lines[insert_idx:]
        return "".join(new_lines)


