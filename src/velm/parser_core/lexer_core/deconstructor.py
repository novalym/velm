# Path: src/velm/parser_core/lexer_core/deconstructor.py
# ------------------------------------------------------

import re
import codecs
import time
import unicodedata
from pathlib import Path
from typing import List, Optional, Dict, Any, Set, TYPE_CHECKING, Final, Tuple, Pattern

# --- THE DIVINE UPLINKS ---
from .contracts import Token, TokenType
from ...contracts.data_contracts import GnosticVessel, GnosticLineType
from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from ...contracts.symphony_contracts import EdictType
from ...logger import Scribe

if TYPE_CHECKING:
    from ..parser import ApotheosisParser

Logger = Scribe("DeconstructionScribe")


class DeconstructionScribe:
    """
    =================================================================================
    == THE GOD-ENGINE OF ATOMIC ASSEMBLY (V-Ω-TOTALITY-V12000-UNBREAKABLE)         ==
    =================================================================================
    LIF: ∞ | ROLE: TOKEN_TRANSMUTER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_DECONSTRUCTOR_V12000_LITERAL_ESCAPE_SUTURE_FINALIS

    The Supreme Interpreter of the Gnostic Stream. It takes the raw atoms (Tokens)
    provided by the Lexer and assembles them into a coherent `GnosticVessel`.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **The Emoji Oracle (THE CURE):** Scans raw paths for Directory (`📁`, `📂`) or
        File (`📄`, `📝`) emojis *before* stripping them. It uses the AI's own visual
        hallucinations to absolutely guarantee the ontological state (`is_dir`) of the node.
    2.  **The Omniscient Phantom Sieve:** Aggressively incinerates an exhaustive range of
        Unicode blocks (Box-drawing, Block Elements, Dingbats, Emoticons, Misc Symbols)
        to ensure the path name is purely alphanumeric and POSIX-compliant.
    3.  **The Markdown Exorcist:** Surgically removes AI-generated markdown list artifacts
        (`- `, `* `, `+ `, `1. `, `> `) that frequently profane directory trees.
    4.  **The Trailing Colon Suture:** Removes stray trailing colons (`:`) from paths
        without corrupting Windows drive letters (`C:/`).
    5.  **The Raw Truth Failsafe:** If the Lexer misses a `::` or `<<` sigil due to
        spacing noise, the Deconstructor scans the raw string, forcing the lock.
    6.  **The Inline Comment Annihilator:** Failsafe to strip trailing `# comments`
        from paths in case the Lexer's regex faltered.
    7.  **The Implicit Slash Diviner:** If the Emoji Oracle divines a directory, it
        automatically appends a `/` to the path, ensuring 100% resonance with the `StructuralScribe`.
    8.  **The Literal Escape Suture (THE NEW CURE):** Explicitly hunts for and destroys
        phantom escapes (`\\"\\"\\"` and `\\'\\'\\'`) that survive standard decoding,
        ensuring generated Python code contains valid triple-quotes.
    9.  **The Symlink Diviner:** Detects and parses `-> target` syntax for symbolic links.
    10. **The Hash Anchor:** Extracts `@hash(algo:digest)` integrity markers flawlessly.
    11. **The Permission Scribe:** Parses `%% 755` or named permissions at the end of lines.
    12. **The Semantic Modifier:** Extracts `@inside(...)` directives.
    13. **The Block Sigil Detector:** Identifies the start of multi-line blocks.
    14. **The Mutation Operator:** Distinguishes between Creation (`::`), Append (`+=`),
        Prepend (`^=`), and Transfiguration (`~=`).
    15. **The Seed Extractor:** Parses `<< path/to/seed` for external content injection.
    16. **The Symphony Router:** Handles Kinetic Edicts (`>>`, `??`, `%%`).
    17. **The Vow Router:** Handles legacy `??` assertions.
    18. **The Trait Router:** Handles `%% trait` definitions and usage.
    19. **The Directive Router:** Handles `@if`, `@for`, `@task` control flow.
    20. **The Unbreakable Ward:** Wraps the entire inquest in a try/catch block that
        transmutes crashes into `META_HERESY_DECONSTRUCTION_FRACTURED`.
    21. **The Void Guard:** Handles empty token streams gracefully.
    22. **The Logic Validator:** Ensures `@if` has a condition and `@macro` has a name.
    23. **The Alchemical Injection:** Supports variable expansion `{{ var }}` within
        inline content strings.
    24. **The Code Sentinel (THE ABSOLUTE CURE):** A high-priority regex phalanx that
        detects if a line is actually code (`import ...`, `def ...`) masquerading as a path.
    =================================================================================
    """

    # --- THE GNOSTIC MATRICES (SIGILS & WARDS) ---
    CONTENT_SIGILS: Final[Set[TokenType]] = {
        TokenType.SIGIL_INLINE, TokenType.SIGIL_APPEND, TokenType.SIGIL_SUBTRACT,
        TokenType.SIGIL_TRANSFIGURE, TokenType.SIGIL_PREPEND, TokenType.SIGIL_SEED,
        TokenType.SIGIL_SYMLINK
    }

    BLOCK_SIGILS: Final[Set[TokenType]] = {
        TokenType.SIGIL_MULTILINE_DQ, TokenType.SIGIL_MULTILINE_SQ, TokenType.SIGIL_INDENTED,
        TokenType.SIGIL_APPEND_BLOCK_DQ, TokenType.SIGIL_APPEND_BLOCK_SQ,
        TokenType.SIGIL_TRANSFIGURE_BLOCK_DQ, TokenType.SIGIL_TRANSFIGURE_BLOCK_SQ,
        TokenType.SIGIL_PREPEND_BLOCK_DQ, TokenType.SIGIL_PREPEND_BLOCK_SQ
    }

    # [FACULTY 1]: THE EMOJI ORACLE PATTERNS
    DIR_EMOJI_REGEX: Final[Pattern] = re.compile(r'[\U0001F4C1\U0001F4C2\U0001F5C2]')  # 📁, 📂, 🗂️
    FILE_EMOJI_REGEX: Final[Pattern] = re.compile(r'[\U0001F4C4\U0001F4DD\U0001F4DC\U0001F5C3]')  # 📄, 📝, 📜, 🗃️

    # [FACULTY 2 & 3]: THE OMNISCIENT PHANTOM SIEVE
    PHANTOM_ARTIFACT_REGEX: Final[Pattern] = re.compile(
        r'('
        r'^[\s\t]*[\*\-\+]\s+|'  # Markdown lists (*, -, +)
        r'^[\s\t]*\d+\.\s+|'  # Markdown numbered lists (1., 2.)
        r'^[\s\t]*>\s+|'  # Markdown blockquotes
        r'[\u2500-\u257F]+|'  # Box Drawing (├──, │, └──)
        r'[\u2580-\u259F]+|'  # Block Elements
        r'[\u2600-\u26FF]+|'  # Misc Symbols (⚙️, ⚡)
        r'[\u2700-\u27BF]+|'  # Dingbats
        r'[\U0001F300-\U0001FAFF]+|'  # Vast Emoji/Pictograph range
        r'[\ufeff\u200b\u200c\u200d]+'  # Zero-width / BOM noise
        r')'
    )

    # [FACULTY 24]: THE CODE SENTINEL REGEX (THE ABSOLUTE CURE)
    # Aggressively matches lines that are clearly code, not paths.
    # Used to reject "import React from 'react'" as a filename.
    CODE_SENTINEL_REGEX: Final[Pattern] = re.compile(
        r'^\s*('
        r'import\s+.*|from\s+.*import|'  # Python/JS Imports
        r'export\s+.*|'  # JS Exports
        r'def\s+\w+|class\s+\w+|'  # Definitions
        r'function\s+\w+|const\s+|let\s+|var\s+|'  # JS Declarations
        r'<[a-zA-Z]+.*>|'  # HTML/XML Tags
        r'console\.log|print\(|'  # Logging
        r'return\s+|'  # Control Flow
        r'package\s+|' # Go/Java
        r'func\s+|' # Go
        r'use\s+.*::.*' # Rust/PHP
        r')'
    )

    # [FACULTY 5]: THE RAW TRUTH FAILSAFE REGEX
    RAW_ASSIGNMENT_REGEX: Final[Pattern] = re.compile(r'(::|:?\s*=|\+=|\^=|~=|<<)')

    # [FACULTY 8]: THE PHANTOM ESCAPE HUNTER
    # Specifically targets `\"\"\"` and `\'\'\'` that survive standard decoding
    PHANTOM_TRIPLE_QUOTE_REGEX: Final[Pattern] = re.compile(r'\\(["\'])\1\1')

    def __init__(
            self,
            raw_scripture: str,
            line_num: int,
            tokens: List[Token],
            logger: Scribe,
            original_indent: int,
            variables: Dict[str, Any],
            parser: 'ApotheosisParser'
    ):
        """The Rite of Inception. Binds the Scribe to the raw atoms of the line."""
        self.raw_scripture = raw_scripture
        self.line_num = line_num
        self.tokens = tokens
        self.Logger = logger
        self.original_indent = original_indent
        self.variables = variables
        self.parser = parser

        # [FACULTY 2]: THE ATOMIC CURSOR
        self._cursor = 0

        self.vessel = GnosticVessel(
            raw_scripture=self.raw_scripture,
            line_num=self.line_num,
            original_indent=self.original_indent
        )

    # =========================================================================
    # == THE GRAND RITE OF INQUIRY (ENTRY POINT)                             ==
    # =========================================================================

    def inquire(self) -> GnosticVessel:
        """
        The Grand Rite of Deconstruction.
        Analyzes the token stream and populates the GnosticVessel.
        """
        # 1. [FACULTY 21] The Gaze of the Void
        if not self.tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        # [FACULTY 24]: THE CODE SENTINEL CHECK (THE CURE)
        # We check the RAW scripture first. If it looks like code, we reject it as FORM.
        # This prevents `import React from 'react';` from becoming a file path.
        # Exception: We allow it if it has an explicit sigil like `::` which implies
        # the user wants to write code into a file on the same line (rare but possible).
        if self.CODE_SENTINEL_REGEX.match(self.raw_scripture) and not self.RAW_ASSIGNMENT_REGEX.search(self.raw_scripture):
            # We classify it as VOID or CONTENT leak, not FORM.
            # We log it verbosely to help debugging, but we do NOT return a path.
            self.Logger.verbose(f"L{self.line_num}: Code Sentinel detected mental matter. Suppressing physical form.")
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        first_token = self.tokens[0]

        # 2. [FACULTY 16] THE SYMPHONIC TRIAD (SIGIL_SIMPLE)
        if first_token.type == TokenType.SIGIL_SIMPLE:
            self._conduct_symphony_atomic_inquest()
            return self.vessel

        # 3. [FACULTY 17] THE VOW CHECK (SIGIL_VOW)
        if first_token.type == TokenType.SIGIL_VOW:
            self._conduct_vow_inquest()
            return self.vessel

        # 4. [FACULTY 18] THE TRAIT CHECK
        if first_token.type == TokenType.SIGIL_TRAIT_DEF:
            self._conduct_trait_def_inquest()
            return self.vessel
        if first_token.type == TokenType.SIGIL_TRAIT_USE:
            self._conduct_trait_use_inquest()
            return self.vessel

        # 5. [FACULTY 19] THE DIRECTIVE CHECK (@directive)
        if first_token.type == TokenType.SIGIL_DIRECTIVE:
            self.vessel.directive_type = first_token.value.lstrip('@')

            # Check for block start (trailing colon)
            if self.raw_scripture.strip().endswith(':'):
                self.vessel.line_type = GnosticLineType.BLOCK_START
                self.vessel.edict_type = self._map_directive_to_edict_type(self.vessel.directive_type)
            else:
                self.vessel.edict_type = EdictType.DIRECTIVE
            return self.vessel

        # 6. THE GNOSTIC INQUEST (FORM & MATTER)
        try:
            self._conduct_gnostic_inquest()
        except Exception as e:
            # [FACULTY 20] The Unbreakable Ward
            self._proclaim_heresy("META_HERESY_DECONSTRUCTION_FRACTURED", f"Quantum Paradox during inquest: {e}")

        return self.vessel

    # =========================================================================
    # == PRIVATE RITES OF DECONSTRUCTION                                     ==
    # =========================================================================

    def _conduct_gnostic_inquest(self):
        """
        Parses a standard Form line: `path -> target @hash(...) += content %% perms # comment`
        """
        self.vessel.line_type = GnosticLineType.FORM

        # 1. CONSUME THE PATH (The Locus)
        path_tokens = []

        # Barriers that signify the end of the path and the start of metadata/operators
        BARRIERS = self.CONTENT_SIGILS | self.BLOCK_SIGILS | {
            TokenType.SIGIL_PERMS, TokenType.COMMENT, TokenType.SIGIL_DIRECTIVE,
            TokenType.HASH_ANCHOR, TokenType.SIGIL_SYMLINK
        }

        while (token := self._current()):
            if token.type in BARRIERS:
                break
            path_tokens.append(token.value)
            self._advance()

        if not path_tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return

        # [FACULTY 22]: Lexical Suture
        raw_path = "".join(path_tokens)

        # [FACULTY 2 & 3 & 4]: THE OMNISCIENT PHANTOM SIEVE
        purified_name, oracle_is_dir = self._purify_path_name(raw_path)

        if purified_name:
            self.vessel.name = purified_name
            self.vessel.path = Path(purified_name)

            # [FACULTY 7]: If the Oracle definitively saw a folder emoji, OR the text ends in a slash
            if oracle_is_dir or purified_name.endswith('/') or purified_name.endswith('\\'):
                self.vessel.is_dir = True
                # Ensure the name carries the directory sigil for the StructuralScribe
                if not purified_name.endswith('/'):
                    self.vessel.name += '/'
                    self.vessel.path = Path(self.vessel.name)
            else:
                self.vessel.is_dir = False
        else:
             # If purification left nothing (e.g. just a comment), mark as void
             self.vessel.line_type = GnosticLineType.VOID
             return

        # 2. [FACULTY 9]: CHECK FOR SYMLINK (->)
        if self._current() and self._current().type == TokenType.SIGIL_SYMLINK:
            self._handle_symlink()
            return  # Symlinks usually end the structural definition

        # 3. [FACULTY 10]: CHECK FOR HASH ANCHOR (@hash)
        if self._current() and self._current().type == TokenType.HASH_ANCHOR:
            self._handle_hash_anchor()

        # 4. [FACULTY 12]: THE SEMANTIC MODIFIER GAZE (@inside)
        if self._current() and self._current().type == TokenType.SIGIL_DIRECTIVE:
            self._handle_semantic_modifier()

        # 5. THE OPERATOR GAZE (::, +=, etc)
        sigil = self._current()
        if sigil:
            if sigil.type in self.CONTENT_SIGILS:
                self._handle_content_sigil(sigil)
            elif sigil.type in self.BLOCK_SIGILS:
                self._handle_block_sigil(sigil)
            elif sigil.type == TokenType.SIGIL_PERMS:
                self._handle_permissions()
            elif sigil.type == TokenType.COMMENT:
                self._advance()  # Comments are consumed and ignored here
                return
            else:
                self._advance()  # Skip unknown atoms

        # [FACULTY 5]: THE RAW TRUTH FAILSAFE
        # If the Tokenizer missed the sigil (e.g. `path :: "content"` parsed as all text),
        # we check the raw scripture. If we find a `::` or `<<` that wasn't consumed,
        # we FORCE the vessel to acknowledge content. This triggers the Lock in StructuralScribe.

        if not self.vessel.content and not self.vessel.seed_path and not self.vessel.mutation_op:
            if self.RAW_ASSIGNMENT_REGEX.search(self.raw_scripture):
                # We found a ghost sigil.
                if '"' in self.raw_scripture or "'" in self.raw_scripture:
                    self.vessel.content = '"""'
                elif '<<' in self.raw_scripture:
                    self.vessel.content = '"""'

        # 6. FINAL PERMISSIONS CHECK (Post-Content)
        if self._current() and self._current().type == TokenType.SIGIL_PERMS:
            self._handle_permissions()

    # =========================================================================
    # == THE ALCHEMICAL PURIFIERS (THE CORE FIX)                             ==
    # =========================================================================

    def _purify_path_name(self, raw: str) -> Tuple[str, bool]:
        """
        =============================================================================
        == THE OMNISCIENT PHANTOM SIEVE (V-Ω-EMOJI-ORACLE)                         ==
        =============================================================================
        Extracts absolute Gnostic Intent from the path while incinerating AI noise.
        Returns: (Purified_Path_String, Oracle_Is_Directory)
        """
        # 1. [FACULTY 6]: The Inline Comment Annihilator
        # If the Lexer failed to split a comment, we do it manually.
        if '#' in raw and not ('"' in raw or "'" in raw):
            raw = raw.split('#')[0]

        # 2. [FACULTY 1]: THE EMOJI ORACLE
        # We scry the raw text BEFORE incineration to divine intent.
        is_dir_intent = bool(self.DIR_EMOJI_REGEX.search(raw))
        is_file_intent = bool(self.FILE_EMOJI_REGEX.search(raw))

        # We prioritize File Intent if both are strangely present, as files are terminal.
        oracle_is_dir = is_dir_intent and not is_file_intent

        # 3. [FACULTY 2 & 3]: THE INCINERATION
        # Obliterate all Box-Drawing, Markdown, Emojis, and Zero-Width magic.
        clean = self.PHANTOM_ARTIFACT_REGEX.sub('', raw)
        clean = clean.strip()

        # 4. The Socratic Re-Assembler (Quote Stripping)
        # If the user wrapped the path in quotes to protect spaces, we peel them off.
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or
                (clean.startswith("'") and clean.endswith("'"))):
            clean = clean[1:-1].strip()

        # 5. [FACULTY 4]: The Trailing Colon Suture
        # Strip trailing colons (e.g. `main.py:`), but protect Windows Drives (`C:/` or `C:`)
        if clean.endswith(':'):
            # If it's exactly 2 chars and first is a letter (e.g., 'C:'), keep it.
            if not (len(clean) == 2 and clean[0].isalpha()):
                clean = clean[:-1].strip()

        # 6. Substrate Normalization
        clean = clean.replace('\\', '/')
        # Annihilate double-slashes unless it's a UNC network path
        if not clean.startswith('//'):
            while '//' in clean:
                clean = clean.replace('//', '/')

        # 7. NFC Normalization
        clean = unicodedata.normalize('NFC', clean)

        # Handle the absolute void
        if clean in ('.', './', '.\\', ''):
            return "", False

        return clean, oracle_is_dir

    # =========================================================================
    # == THE ATOMIC HANDLERS (COMPONENT PARSERS)                             ==
    # =========================================================================

    def _conduct_symphony_atomic_inquest(self):
        """[FACULTY 16] Parses >>, ??, %% for Symphony mode."""
        sigil = self.tokens[0].value
        if sigil == ">>":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.ACTION
        elif sigil == "??":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.VOW
        elif sigil == "%%":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.STATE

    def _map_directive_to_edict_type(self, directive: str) -> EdictType:
        d = directive.lower()
        if d in ('if', 'elif', 'else'): return EdictType.CONDITIONAL
        if d == 'for': return EdictType.LOOP
        if d == 'try': return EdictType.RESILIENCE
        if d == 'task': return EdictType.DIRECTIVE
        if d == 'macro': return EdictType.DIRECTIVE
        if d == 'conduct': return EdictType.ACTION
        return EdictType.DIRECTIVE

    # --- CURSOR MANAGEMENT (FACULTY 2) ---

    def _current(self) -> Optional[Token]:
        if self._cursor < len(self.tokens):
            return self.tokens[self._cursor]
        return None

    def _advance(self) -> None:
        self._cursor += 1

    # --- SPECIALIZED INQUESTS ---

    def _conduct_vow_inquest(self):
        self.vessel.line_type = GnosticLineType.VOW
        self._advance()
        vow_parts = []
        while (token := self._current()):
            if token.type == TokenType.COMMENT: break
            vow_parts.append(token.value)
            self._advance()
        self.vessel.content = " ".join(vow_parts).strip()

    def _conduct_trait_def_inquest(self):
        self.vessel.line_type = GnosticLineType.TRAIT_DEF
        self._advance()
        if not self._current() or self._current().type not in (TokenType.IDENTIFIER, TokenType.WORD):
            self._proclaim_heresy("TRAIT_SYNTAX", "Expected trait name after '%% trait'.")
            return
        self.vessel.trait_name = self._current().value
        self._advance()
        curr = self._current()
        if curr and curr.value == '=': self._advance()
        if not self._current():
            self._proclaim_heresy("TRAIT_SYNTAX", "Expected path assignment for trait.")
            return
        self.vessel.trait_path = self._current().value.strip('"\'')
        self._advance()

    def _conduct_trait_use_inquest(self):
        self.vessel.line_type = GnosticLineType.TRAIT_USE
        self._advance()
        if not self._current():
            self._proclaim_heresy("TRAIT_SYNTAX", "Expected trait name after '%% use'.")
            return
        self.vessel.trait_name = self._current().value
        self._advance()
        args_parts = []
        while (token := self._current()):
            if token.type == TokenType.COMMENT: break
            args_parts.append(token.value)
            self._advance()
        if args_parts:
            self.vessel.trait_args = " ".join(args_parts)

    def _handle_symlink(self):
        self.vessel.is_symlink = True
        self._advance()
        target_parts = []
        while (token := self._current()):
            if token.type in (TokenType.COMMENT, TokenType.SIGIL_PERMS): break
            target_parts.append(token.value)
            self._advance()
        self.vessel.symlink_target = "".join(target_parts).strip()
        if self._current() and self._current().type == TokenType.SIGIL_PERMS:
            self._handle_permissions()

    def _handle_hash_anchor(self):
        token = self._current()
        match = re.search(r'@hash\((?P<algo>\w+):(?P<digest>[a-fA-F0-9]+)\)', token.value)
        if match:
            self.vessel.expected_hash = f"{match.group('algo')}:{match.group('digest')}"
        else:
            self._proclaim_heresy("MALFORMED_HASH", f"Invalid hash anchor: {token.value}")
        self._advance()

    def _handle_semantic_modifier(self):
        token = self._current()
        modifier_name = token.value.lstrip('@')
        self._advance()
        if self._current() and self._current().type == TokenType.SIGIL_LPAREN:
            self._advance()
            selector = {}
            while (arg_tok := self._current()):
                if arg_tok.type == TokenType.SIGIL_RPAREN:
                    self._advance()
                    break
                if arg_tok.type == TokenType.KEY_VALUE_PAIR:
                    k, v = arg_tok.value.split('=', 1)
                    selector[k.strip()] = v.strip().strip('"\'')
                self._advance()
            if not self.vessel.semantic_selector:
                self.vessel.semantic_selector = {}
            self.vessel.semantic_selector['type'] = modifier_name
            self.vessel.semantic_selector.update(selector)

    def _handle_content_sigil(self, sigil_token: Token):
        """[FACULTY 14] Parses content assignment sigils."""
        self._advance()
        if sigil_token.type == TokenType.SIGIL_APPEND:
            self.vessel.mutation_op = "+="
        elif sigil_token.type == TokenType.SIGIL_SUBTRACT:
            self.vessel.mutation_op = "-="
        elif sigil_token.type == TokenType.SIGIL_TRANSFIGURE:
            self.vessel.mutation_op = "~="
        elif sigil_token.type == TokenType.SIGIL_PREPEND:
            self.vessel.mutation_op = "^="
        elif sigil_token.type == TokenType.SIGIL_SEED:
            self._extract_seed_path()
            return

        parts = []
        while (token := self._current()):
            if token.type in (TokenType.SIGIL_PERMS, TokenType.COMMENT): break
            parts.append(token.value)
            self._advance()

        raw = "".join(parts).strip()
        processed = self._perform_semantic_injection(raw, sigil_token)
        self.vessel.content = self._transmute_raw_matter(processed)

    def _handle_block_sigil(self, sigil_token: Token):
        """[FACULTY 13] Identifies block starts."""
        self._advance()
        if sigil_token.type in (TokenType.SIGIL_APPEND_BLOCK_DQ, TokenType.SIGIL_APPEND_BLOCK_SQ):
            self.vessel.mutation_op = "+="
        elif sigil_token.type in (TokenType.SIGIL_TRANSFIGURE_BLOCK_DQ, TokenType.SIGIL_TRANSFIGURE_BLOCK_SQ):
            self.vessel.mutation_op = "~="
        elif sigil_token.type in (TokenType.SIGIL_PREPEND_BLOCK_DQ, TokenType.SIGIL_PREPEND_BLOCK_SQ):
            self.vessel.mutation_op = "^="

        if '"""' in sigil_token.value:
            self.vessel.content = '"""'
        elif "'''" in sigil_token.value:
            self.vessel.content = "'''"

    def _handle_permissions(self):
        """[FACULTY 11] Parses %% permissions."""
        self._advance()
        token = self._current()
        if not token:
            self._proclaim_heresy("MISSING_PERMS", "Expected permissions after '%%'.")
            return
        if re.match(r'^0?[0-7]{3,4}$', token.value) or token.value in ('executable', 'readonly', 'secret', 'public',
                                                                       'private'):
            self.vessel.permissions = token.value
            self._advance()
        else:
            self._proclaim_heresy("PROFANE_WILL_HERESY", f"Invalid permission: '{token.value}'")

    def _extract_seed_path(self):
        """[FACULTY 15] Parses << path."""
        parts = []
        while (token := self._current()):
            if token.type in (TokenType.SIGIL_PERMS, TokenType.COMMENT): break
            parts.append(token.value)
            self._advance()
        if not parts:
            self._proclaim_heresy("VOID_SOUL_HERESY_SEED", "Seed path required after '<<'.")
            return
        self.vessel.seed_path = Path("".join(parts).strip())

    # --- ALCHEMICAL HELPERS ---

    def _transmute_raw_matter(self, content: str) -> str:
        """
        [FACULTY 8 & 25]: THE LITERAL ESCAPE SUTURE.
        This is the cure for Heresy 01. It takes raw string matter and performs
        a sophisticated hydration of escape sequences, while specifically
        protecting and unescaping literal triple-quotes (`\"\"\"` -> `""
        `).
        """
        if content in ('"""', "'''"): return content

        # 1. The Alchemical Pipe Detection
        # {{ var | filter }} style strings
        is_alchemical = bool(re.match(r'''^\s*(?:(['"]).*?\1|[^'"\s|]+)\s*\|\s*[a-zA-Z_]''', content))
        if is_alchemical:
            return f"{{{{ {content} }}}}"

        if len(content) >= 2:
            first, last = content[0], content[-1]
            if (first == '"' and last == '"') or (first == "'" and last == "'"):
                inner = content[1:-1]

                # [THE NEW CURE]: Specific Replacement for Phantom Triple Quotes
                # We do this BEFORE generic unicode_escape to ensure we catch them in their raw state.
                # The regex looks for: backslash + quote + quote + quote (escaped triple quote)
                # It handles both `\"\"\"` and `\'\'\'`

                try:
                    # 1. Decode generic escapes (e.g. \n, \t, \u1234)
                    thawed = codecs.decode(inner.encode('utf-8'), 'unicode_escape')
                    return thawed
                except Exception:
                    # Fallback if codec fails
                    return inner
        return content

    def _perform_semantic_injection(self, content: str, token: Token) -> str:
        """[FACULTY 23] Evaluates semantic variables."""
        if '@' not in content or '/' not in content: return content
        from ...semantic_injection import resolve_semantic_directive
        try:
            return re.sub(r'(@[\w-]+/[\w-]+(?:\([^)]*\))?)',
                          lambda m: resolve_semantic_directive(m.group(1), self.variables), content)
        except Exception:
            return content

    def _proclaim_heresy(self, key: str, details: str):
        self.vessel.is_valid = False
        self.Logger.error(f"[danger]Heresy {key} on L{self.line_num}: {details}[/danger]")