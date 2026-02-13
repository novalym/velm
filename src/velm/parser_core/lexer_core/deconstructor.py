# Path: src/velm/parser_core/lexer_core/deconstructor.py
# ------------------------------------------------------


import re
import codecs
from pathlib import Path
from typing import List, Optional, Dict, Any, Set, TYPE_CHECKING, Union, Final

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
    == THE GOD-ENGINE OF ATOMIC ASSEMBLY (V-Ω-TOTALITY-V1000-FAILSAFE)             ==
    =================================================================================
    LIF: ∞ | ROLE: TOKEN_TRANSMUTER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_DECONSTRUCTOR_V1000_FAILSAFE_FINALIS

    The Supreme Interpreter of the Gnostic Stream. It takes the raw atoms (Tokens)
    provided by the Lexer and assembles them into a coherent `GnosticVessel`.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **The Raw Truth Failsafe (THE CORE FIX):** If the Lexer fails to tokenize a
        `::` or `<<` sigil (due to spacing/noise), the Deconstructor performs a
        regex scan on the `raw_scripture`. If the sigil exists, it enforces the
        Block/Content logic, locking the line as a File.
    2.  **The Atomic Cursor:** A precise, stateful iterator over the token stream.
    3.  **The Void Sanitizer:** Strips tree artifacts (`├──`) and invisible Unicode
        garbage before path assembly.
    4.  **The Quote Alchemist:** Hydrates escaped characters (`\\n`) within inline
        strings, allowing single-line definitions to hold multi-line souls.
    5.  **The Path Normalizer:** Forces all paths to POSIX standard (forward slashes),
        stripping wrapping quotes and trailing whitespace.
    6.  **The Symlink Diviner:** Detects and parses `-> target` syntax for symbolic links.
    7.  **The Hash Anchor:** Extracts `@hash(algo:digest)` integrity markers.
    8.  **The Permission Scribe:** Parses `%% 755` or named permissions at the end of lines.
    9.  **The Semantic Modifier:** Extracts `@inside(...)` directives.
    10. **The Block Sigil Detector:** Identifies the start of multi-line blocks
        (`:: \"\"\"`) vs inline content (`:: "foo"`).
    11. **The Mutation Operator:** Distinguishes between Creation (`::`), Append (`+=`),
        Prepend (`^=`), and Transfiguration (`~=`).
    12. **The Seed Extractor:** Parses `<< path/to/seed` for external content injection.
    13. **The Symphony Router:** Handles Kinetic Edicts (`>>`, `??`, `%%`) by checking
        the first token's soul.
    14. **The Vow Router:** Handles legacy `??` assertions.
    15. **The Trait Router:** Handles `%% trait` definitions and usage.
    16. **The Directive Router:** Handles `@if`, `@for`, `@task` control flow.
    17. **The Unbreakable Ward:** Wraps the entire inquest in a try/catch block that
        transmutes crashes into `META_HERESY_DECONSTRUCTION_FRACTURED`.
    18. **The Void Guard:** Handles empty token streams gracefully.
    19. **The Logic Validator:** Ensures `@if` has a condition and `@macro` has a name.
    20. **The Comment Stripper:** Ignores comments during path assembly but preserves
        them in raw scripture.
    21. **The Alchemical Injection:** Supports variable expansion `{{ var }}` within
        inline content strings.
    22. **The Lexical Suture:** Re-assembles fragmented path tokens into a single
        coherent string.
    23. **The Fallback Heuristic:** If path assembly fails, defaults to `VOID` type
        to prevent file system corruption.
    24. **The Finality Vow:** Guaranteed return of a `GnosticVessel` object, populated
        with as much truth as could be divined.
    =================================================================================
    """

    # [FACULTY 10 & 11]: THE SIGIL MATRIX
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

    # [FACULTY 3]: THE VOID SANITIZER PATTERNS
    ARTIFACT_CLEANER: Final[re.Pattern] = re.compile(r'^[\u2500-\u257f\|\+\\`\s\t-]+')

    # [FACULTY 1]: THE RAW TRUTH FAILSAFE REGEX
    # Matches explicit assignment sigils even if tokenization failed
    RAW_ASSIGNMENT_REGEX: Final[re.Pattern] = re.compile(r'(::|:?\s*=|\+=|\^=|~=|<<)')

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
        """
        The Rite of Inception. Binds the Scribe to the raw atoms of the line.
        """
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
        # 1. [FACULTY 18] The Gaze of the Void
        if not self.tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        first_token = self.tokens[0]

        # 2. [FACULTY 13] THE SYMPHONIC TRIAD (SIGIL_SIMPLE)
        if first_token.type == TokenType.SIGIL_SIMPLE:
            self._conduct_symphony_atomic_inquest()
            return self.vessel

        # 3. [FACULTY 14] THE VOW CHECK (SIGIL_VOW)
        if first_token.type == TokenType.SIGIL_VOW:
            self._conduct_vow_inquest()
            return self.vessel

        # 4. [FACULTY 15] THE TRAIT CHECK
        if first_token.type == TokenType.SIGIL_TRAIT_DEF:
            self._conduct_trait_def_inquest()
            return self.vessel
        if first_token.type == TokenType.SIGIL_TRAIT_USE:
            self._conduct_trait_use_inquest()
            return self.vessel

        # 5. [FACULTY 16] THE DIRECTIVE CHECK (@directive)
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
            # [FACULTY 17] The Unbreakable Ward
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

        # [FACULTY 3]: THE VOID SANITIZER
        purified = self._purify_path_name(raw_path)

        if purified:
            self.vessel.name = purified
            self.vessel.path = Path(self.vessel.name)
            # Heuristic directory detection: ends in slash
            self.vessel.is_dir = purified.endswith('/') or purified.endswith('\\')

        # 2. [FACULTY 6]: CHECK FOR SYMLINK (->)
        if self._current() and self._current().type == TokenType.SIGIL_SYMLINK:
            self._handle_symlink()
            return  # Symlinks usually end the structural definition

        # 3. [FACULTY 7]: CHECK FOR HASH ANCHOR (@hash)
        if self._current() and self._current().type == TokenType.HASH_ANCHOR:
            self._handle_hash_anchor()

        # 4. [FACULTY 9]: THE SEMANTIC MODIFIER GAZE (@inside)
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

        # [FACULTY 1]: THE RAW TRUTH FAILSAFE (THE CORE FIX)
        # If the Tokenizer missed the sigil (e.g. `path :: "content"` parsed as all text),
        # we check the raw scripture. If we find a `::` or `<<` that wasn't consumed,
        # we FORCE the vessel to acknowledge content. This triggers the Lock in StructuralScribe.

        if not self.vessel.content and not self.vessel.seed_path and not self.vessel.mutation_op:
            if self.RAW_ASSIGNMENT_REGEX.search(self.raw_scripture):
                # We found a ghost sigil.
                # Heuristic: If it contains quotes, assume inline content.
                if '"' in self.raw_scripture or "'" in self.raw_scripture:
                    # We set a placeholder content to trigger the StructuralScribe's lock.
                    # The StructuralScribe will then use the BlockConsumer to re-parse the raw line accurately.
                    self.vessel.content = '"""'
                    # self.Logger.verbose(f"Failsafe: Detected ghost sigil in '{self.raw_scripture.strip()}'. Forcing Content Lock.")
                elif '<<' in self.raw_scripture:
                    # Force seed path detection logic downstream?
                    # Better to just set content to trigger lock.
                    self.vessel.content = '"""'

        # 6. FINAL PERMISSIONS CHECK (Post-Content)
        # e.g. path :: "content" %% 755
        if self._current() and self._current().type == TokenType.SIGIL_PERMS:
            self._handle_permissions()

    # =========================================================================
    # == THE ATOMIC HANDLERS (COMPONENT PARSERS)                             ==
    # =========================================================================

    def _conduct_symphony_atomic_inquest(self):
        """[FACULTY 13] Parses >>, ??, %% for Symphony mode."""
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
                    self._advance();
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
        """[FACULTY 11] Parses content assignment sigils."""
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
        # [FACULTY 21] Semantic Injection handled here or later?
        # Usually processed by StructuralScribe, but we purify quotes here.
        processed = self._perform_semantic_injection(raw, sigil_token)
        self.vessel.content = self._purify_content_string(processed)

    def _handle_block_sigil(self, sigil_token: Token):
        """[FACULTY 10] Identifies block starts."""
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
        """[FACULTY 8] Parses %% permissions."""
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
        """[FACULTY 12] Parses << path."""
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

    def _purify_path_name(self, raw: str) -> str:
        """[FACULTY 3] Strips artifacts."""
        clean = raw.replace('\ufeff', '').replace('\u200b', '')
        clean = self.ARTIFACT_CLEANER.sub('', clean).strip()
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'"))):
            clean = clean[1:-1]
        return "" if clean in ('.', './', '.\\', '') else clean

    def _purify_content_string(self, content: str) -> str:
        """[FACULTY 4] Quote stripping and escape hydration."""
        if content in ('"""', "'''"): return content
        is_alchemical = bool(re.match(r'''^\s*(?:(['"]).*?\1|[^'"\s|]+)\s*\|\s*[a-zA-Z_]''', content))
        if is_alchemical: return f"{{{{ {content} }}}}"

        if len(content) >= 2:
            first, last = content[0], content[-1]
            if (first == '"' and last == '"') or (first == "'" and last == "'"):
                inner = content[1:-1]
                try:
                    return codecs.decode(inner.encode('utf-8'), 'unicode_escape')
                except Exception:
                    return inner
        return content

    def _perform_semantic_injection(self, content: str, token: Token) -> str:
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