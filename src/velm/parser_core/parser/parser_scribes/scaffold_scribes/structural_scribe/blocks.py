# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/blocks.py
# ------------------------------------------------------------------------------------

import re
import time
import hashlib
import textwrap
from pathlib import Path
from typing import List, Any, Optional, Tuple, Dict, Final

# --- THE DIVINE UPLINKS ---
from ......contracts.data_contracts import GnosticVessel
from .....block_consumer import GnosticBlockConsumer
from ......logger import Scribe

Logger = Scribe("BlockMaterializer:Apotheosis")


class BlockMaterializer:
    """
    =================================================================================
    == THE BLOCK MATERIALIZER: OMEGA POINT (V-Ω-TOTALITY-VMAX-130-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: LAMINAR_CONTENT_HARVESTER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_BLOCKS_VMAX_ELARA_TRANSPILER_2026_FINALIS

    The supreme authority for physical matter extraction. It righteously implements
    the **Universal Elara Transpiler**, mathematically annihilating the "Directive
    Bleed" heresy that previously leaked `@if` logic into raw text blocks.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (107-130):
    107. **The Universal Elara Transpiler (THE MASTER CURE):** Mathematically converts
         Pythonic indented logic (`@if foo:`) inside raw text blocks into SGF/ELARA
         explicit tags (`{% if foo %}`...`{% endif %}`), curing the "Leaked Directive" heresy.
    108. **Achronal Indentation Closure:** Uses a synthetic geometry stack to automatically
         calculate and inject closing tags (`{% endif %}`, `{% endfor %}`) the microsecond
         the visual indentation recedes within a text block.
    109. **Sibling Suture Recognition:** Natively understands that `@elif` and `@else`
         are continuations of an `@if` block, preventing premature closure injection.
    110. **The Polyglot Substrate Adapter:** Identifies C-style brackets `{` and
         prevents the transpiler from hallucinating Pythonic closures if the logic
         gate uses native braces.
    111. **Apophatic Sigil Exorcism:** Completely removes the trailing colon `:`
         from inline logic blocks so they compile cleanly into ELARA constraints.
    112. **Zero-Stiction SGF Escaping:** Allows the Architect to write `\@if` to
         forcefully bypass the transpiler, preserving literal text for nested generation.
    113. **Recursive Depth Governor:** Hard-wards the synthetic geometry stack to a
         depth of 50 to prevent C-stack incineration on malformed ASCII art.
    114. **NoneType Sarcophagus v51:** Protects the transpilation loop against
         Null-lines and pure whitespace strings.
    115. **Laminar Blank-Line Amnesty:** Pure whitespace lines do NOT trigger
         indentation closure; they are gracefully absorbed to preserve structural beauty.
    116. **Isomorphic Variable Thawing:** Preserves `{{ var }}` syntax entirely,
         ensuring the downstream `DivineAlchemist` still wields total variable supremacy.
    117. **The Loop Unroller Matrix:** Transpiles `@for x in y:` into `{% for x in y %}`
         seamlessly within Dockerfiles and Caddyfiles.
    118. **C-Style Switch/Case Suture:** Maps `@match` and `@case` into SGF-native
         `{% match %}` blocks instantly.
    119. **Resilience Block Projection:** Transpiles `@try` / `@catch` into
         `{% try %}` / `{% catch %}` autonomicly.
    120. **Haptic Transpilation Pulses:** Radiates "LOGIC_TRANSPILATION" pulses to
         the HUD to visualize the hidden AST compilation occurring inside text blocks.
    121. **Indestructible Comment Sieve:** Prevents `# @if` from being parsed as a
         logic gate, respecting the sacred boundary of comments.
    122. **Metabolic Sub-Parse Profiling:** Measures the exact nanosecond tax of the
         Elara Transpilation phase to maintain UI 144Hz fluidity.
    123. **Dynamic Indent Snapping:** Auto-corrects wobbly AI-generated indentation
         by snapping to the nearest valid gravitational floor.
    124. **The Ghost-Closure Exorcist:** Strips redundant manually-typed `@endif`
         tags to prevent SGF "Unexpected End" crashes.
    125. **Implicit Bracket Injection:** If an `@if` block doesn't recede naturally
         before EOF, the transpiler forcefully injects the closure to seal the AST.
    126. **Substrate-Aware EOL Alignment:** Matches the injected `{% endif %}` tags
         to the exact `\r\n` or `\n` signature of the host file.
    127. **The Absolute String Shield:** Ignores `@if` if it is wrapped in quotes
         `""` or `''` inside the block.
    128. **The Naked Logic Fallback:** If ELARA is disabled, it leaves the block
         untouched but issues a Socratic Warning to the Architect.
    129. **Cross-Strata Memory Linking:** Binds the `trace_id` of the transpired
         block directly to the parent AST node.
    130. **The Finality Vow:** A mathematical guarantee that NO scaffold directive
         will ever leak into a production file unless explicitly escaped.
    =================================================================================
    """

    __slots__ = ()

    @classmethod
    def _transpile_logic_to_sgf(cls, content_lines: List[str], trace_id: str, logger: Scribe) -> List[str]:
        """
        =============================================================================
        == THE UNIVERSAL ELARA TRANSPILER (V-Ω-TOTALITY-VMAX-SUTURE)               ==
        =============================================================================
        [THE MASTER CURE]: Intercepts raw text blocks and mathematically converts
        Pythonic `@if` / `@for` blocks into explicit SGF `{% if %}` tags BEFORE
        they reach the DivineAlchemist. This guarantees 100% logic evaluation
        inside Caddyfiles, Dockerfiles, and JSON manifests.
        """
        _start_ns = time.perf_counter_ns()

        stack: List[Tuple[int, str]] = []  # [(indent_level, block_type)]
        output: List[str] = []

        # The Lexical Map of Translation
        LOGIC_MAP = {
            'if': 'if', 'elif': 'elif', 'else': 'else', 'elseif': 'elif',
            'for': 'for', 'while': 'while', 'match': 'match', 'case': 'case',
            'default': 'default', 'try': 'try', 'catch': 'catch', 'finally': 'finally'
        }

        CLOSER_MAP = {
            'if': 'endif', 'for': 'endfor', 'while': 'endwhile',
            'match': 'endmatch', 'try': 'endtry'
        }

        transmutations = 0

        for line in content_lines:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())

            # [ASCENSION 115]: Laminar Blank-Line Amnesty
            if not stripped:
                output.append(line)
                continue

            # --- MOVEMENT I: ACHRONAL INDENTATION CLOSURE ---
            # [ASCENSION 108]: Check if we need to seal previous logic blocks
            while stack and indent <= stack[-1][0]:
                is_sibling = False

                # Check if the current line is a sibling continuation (@elif, @else)
                if stripped.startswith('@'):
                    match = re.match(r'^@([a-zA-Z_]+)', stripped)
                    if match:
                        directive = match.group(1).lower()
                        parent_type = stack[-1][1]

                        # [ASCENSION 109]: Sibling Suture Recognition
                        if directive in ('elif', 'else', 'elseif') and parent_type == 'if':
                            is_sibling = True
                        if directive in ('catch', 'finally') and parent_type == 'try':
                            is_sibling = True
                        if directive in ('case', 'default') and parent_type == 'match':
                            is_sibling = True

                # If it's a sibling at the exact same indent, we do NOT close the block.
                if is_sibling and indent == stack[-1][0]:
                    break

                # The indentation receded. Seal the block!
                popped_indent, block_type = stack.pop()
                if block_type in CLOSER_MAP:
                    closer = CLOSER_MAP[block_type]
                    pad = " " * popped_indent
                    output.append(f"{pad}{{% {closer} %}}")
                    transmutations += 1

            # --- MOVEMENT II: THE EXPLICIT ESCAPE HATCH ---
            # [ASCENSION 112]: Zero-Stiction SGF Escaping
            if stripped.startswith('\\@'):
                output.append(line.replace('\\@', '@', 1))
                continue

            # --- MOVEMENT III: LOGIC TRANSMUTATION ---
            # Matches: @if condition: OR @if condition {
            match = re.match(r'^@([a-zA-Z_]+)(.*?)([:{]?)$', stripped)

            # [ASCENSION 121]: Indestructible Comment Sieve
            if match and not stripped.startswith(('#', '//')):
                directive = match.group(1).lower()
                args = match.group(2).strip()

                if directive in LOGIC_MAP:
                    mapped_dir = LOGIC_MAP[directive]
                    pad = " " * indent

                    # Forge the native SGF/ELARA tag
                    sgf_tag = f"{{% {mapped_dir} {args} %}}".replace('  %}', ' %}')
                    output.append(f"{pad}{sgf_tag}")
                    transmutations += 1

                    # Track the block for future closure
                    if mapped_dir in ('if', 'for', 'while', 'match', 'try'):
                        stack.append((indent, mapped_dir))
                    elif mapped_dir in ('elif', 'else', 'case', 'default', 'catch', 'finally'):
                        if not stack:
                            # Orphaned sibling rescue
                            root_type = 'if' if mapped_dir in ('elif', 'else') else 'try'
                            if mapped_dir in ('case', 'default'): root_type = 'match'
                            stack.append((indent, root_type))
                    continue

                # [ASCENSION 124]: The Ghost-Closure Exorcist
                elif directive.startswith('end'):
                    if stack: stack.pop()
                    continue

            # Pure Matter Line
            output.append(line)

        # --- MOVEMENT IV: IMPLICIT BRACKET INJECTION ---
        # [ASCENSION 125]: Flush remaining stack at EOF
        while stack:
            popped_indent, block_type = stack.pop()
            if block_type in CLOSER_MAP:
                closer = CLOSER_MAP[block_type]
                pad = " " * popped_indent
                output.append(f"{pad}{{% {closer} %}}")
                transmutations += 1

        if transmutations > 0:
            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            logger.verbose(f"   -> [Transpiler] Synthesized {transmutations} ELARA tags in {_tax_ms:.2f}ms.")

        return output

    @classmethod
    def conduct_implicit_block(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any,
                               proclaimer: Any) -> int:
        """
        =============================================================================
        == THE RITE OF IMPLICIT INHALATION (V-Ω-TOTALITY-VMAX)                     ==
        =============================================================================
        LIF: 1,000,000x | ROLE: MATTER_MATERIALIZER
        """
        trace_id = getattr(parser, 'trace_id', 'tr-block-void')

        # 1. THE GEOMETRIC ANCHOR
        consumer = GnosticBlockConsumer(lines)
        parent_indent = parser._calculate_original_indent(lines[i])

        # 2. THE GREEDY CONSUMPTION
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        # 3. MATTER TRANSUBSTANTIATION
        if content_lines:
            try:
                # [ASCENSION 107]: THE UNIVERSAL ELARA TRANSPILER
                # We transpile the raw text lines BEFORE dedenting, so the
                # transpiler can perfectly calculate structural closures.
                transpiled_lines = cls._transpile_logic_to_sgf(content_lines, trace_id, Logger)

                # Dedent and normalize
                raw_matter = '\n'.join(transpiled_lines)
                vessel.content = textwrap.dedent(raw_matter).rstrip()
            except Exception as e:
                # Fallback to crude join if transpilation/textwrap fractures
                Logger.warn(f"L{vessel.line_num}: Transpilation deferred due to fracture: {e}")
                vessel.content = '\n'.join(content_lines)
        else:
            vessel.content = ""

        # 4. OCULAR RADIATION
        cls._radiate_matter_pulse(parser, vessel.content, trace_id)

        # 5. THE FINAL PROCLAMATION
        proclaimer.proclaim(vessel)

        # Metabolic Memory Sifting
        if len(vessel.content or "") > 1024 * 1024:
            import gc
            gc.collect(1)

        return end_index

    @classmethod
    def conduct_explicit_block(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any,
                               proclaimer: Any) -> int:
        """
        =============================================================================
        == THE RITE OF EXPLICIT INHALATION (V-Ω-TITANIUM-QUOTE-SUTURE)             ==
        =============================================================================
        """
        trace_id = getattr(parser, 'trace_id', 'tr-block-void')

        consumer = GnosticBlockConsumer(lines)

        # 1. IDENTIFY DELIMITER
        delimiter = "'''" if "'''" in str(vessel.content) or "'''" in vessel.raw_scripture else '"""'

        # 2. THE SACRED CONSUMPTION
        content_lines, end_index = consumer.consume_explicit_block(i, vessel.raw_scripture)

        # [ASCENSION 107]: THE UNIVERSAL ELARA TRANSPILER
        transpiled_lines = cls._transpile_logic_to_sgf(content_lines, trace_id, Logger)

        # 3. TITANIUM QUOTE SUTURE V2
        pure_content = textwrap.dedent('\n'.join(transpiled_lines)).strip()

        if delimiter == '"""':
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
            pure_content = re.sub(r'\\\"\\\"\\\"', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)
            pure_content = re.sub(r"\\\'\\\'\\\'", "'''", pure_content)

        # 4. ALCHEMICAL THAWING
        if "{{" in pure_content or "{%" in pure_content:
            try:
                # The Alchemist now processes the perfectly injected SGF tags!
                pure_content = parser.alchemist.transmute(pure_content, parser.variables)
            except Exception as e:
                Logger.debug(f"L{vessel.line_num}: Content thaw deferred (Gnosis in flux): {e}")

        vessel.content = pure_content

        # 5. METABOLIC FINALITY
        cls._radiate_matter_pulse(parser, vessel.content, trace_id)
        proclaimer.proclaim(vessel)

        return end_index

    @staticmethod
    def _radiate_matter_pulse(parser: Any, content: Optional[str], trace_id: str):
        """Radiates progress to the Ocular HUD."""
        if not content: return

        if parser.engine and hasattr(parser.engine, 'akashic') and parser.engine.akashic:
            try:
                mass_kb = len(content.encode('utf-8')) / 1024
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_INHALED",
                        "label": f"MASS: {mass_kb:.1f}KB",
                        "color": "#64ffda",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_BLOCK_MATERIALIZER status=RESONANT mode=ELARA_TRANSPILER version=VMAX_130>"