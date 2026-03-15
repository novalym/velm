# Path: src/velm/parser_core/lexer_core/deconstructor/handlers/form.py
# --------------------------------------------------------------------

import re
import codecs
from pathlib import Path
from typing import Set, Final, Any

from ...contracts import Token, TokenType
from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from ..purifier import PathPurifier
from ..state import DeconstructionState


class FormHandler:
    """
    =============================================================================
    == THE FORM HANDLER (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE)                     ==
    =============================================================================
    LIF: ∞ | ROLE: PHYSICAL_GEOMETRY_PARSER | RANK: OMEGA_SOVEREIGN

    Processes physical file coordinates, structural sigils, and symlinks.
    It reads from the DeconstructionState cursor to extract paths and attributes
    with absolute safety and zero recursive limits.
    """

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

    BARRIERS: Final[Set[TokenType]] = CONTENT_SIGILS | BLOCK_SIGILS | {
        TokenType.SIGIL_PERMS, TokenType.COMMENT, TokenType.SIGIL_DIRECTIVE,
        TokenType.HASH_ANCHOR, TokenType.SIGIL_SYMLINK
    }

    @classmethod
    def handle(cls, state: DeconstructionState, vessel: GnosticVessel):
        """
        [ASCENSION 34]: The Central Form Loop.
        Iterates tokens using the high-speed state cursor until a barrier is hit.
        """
        vessel.line_type = GnosticLineType.FORM
        path_tokens = []

        # 1. CONSUME THE PATH (The Locus)
        while (token := state.current()):
            if token.type in cls.BARRIERS:
                break
            path_tokens.append(token.value)
            state.advance()

        if not path_tokens:
            vessel.line_type = GnosticLineType.VOID
            return

        raw_path = "".join(path_tokens)

        # 2. PURIFY THE PATH (The C-Matrix Sieve)
        purified_name, oracle_is_dir = PathPurifier.purify(raw_path)

        if purified_name:
            vessel.name = purified_name
            vessel.path = Path(purified_name)

            # [ASCENSION 35]: Strict trailing slash enforcement
            if oracle_is_dir or purified_name.endswith('/') or purified_name.endswith('\\'):
                vessel.is_dir = True
                if not purified_name.endswith('/'):
                    vessel.name += '/'
                    vessel.path = Path(vessel.name)
            else:
                vessel.is_dir = False
        else:
            # If purification left nothing, mark as void
            vessel.line_type = GnosticLineType.VOID
            return

        # 3. PROCESS OPERATORS AND METADATA
        cls._process_operators(state, vessel)

    @classmethod
    def _process_operators(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Surgically routes remaining tokens to their respective attribute parsers."""
        if state.current() and state.current().type == TokenType.SIGIL_SYMLINK:
            cls._handle_symlink(state, vessel)
            return

        if state.current() and state.current().type == TokenType.HASH_ANCHOR:
            cls._handle_hash_anchor(state, vessel)

        if state.current() and state.current().type == TokenType.SIGIL_DIRECTIVE:
            cls._handle_semantic_modifier(state, vessel)

        sigil = state.current()
        if sigil:
            if sigil.type in cls.CONTENT_SIGILS:
                cls._handle_content_sigil(state, vessel, sigil)
            elif sigil.type in cls.BLOCK_SIGILS:
                cls._handle_block_sigil(state, vessel, sigil)
            elif sigil.type == TokenType.SIGIL_PERMS:
                cls._handle_permissions(state, vessel)
            elif sigil.type == TokenType.COMMENT:
                state.advance()
                return
            else:
                state.advance()

        # Final check for permissions trailing behind content
        if state.current() and state.current().type == TokenType.SIGIL_PERMS:
            cls._handle_permissions(state, vessel)

    @classmethod
    def _handle_symlink(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Extracts the target of a symbolic link: path -> target."""
        vessel.is_symlink = True
        state.advance()
        target_parts = []
        while (token := state.current()):
            if token.type in (TokenType.COMMENT, TokenType.SIGIL_PERMS): break
            target_parts.append(token.value)
            state.advance()

        vessel.symlink_target = "".join(target_parts).strip()
        if state.current() and state.current().type == TokenType.SIGIL_PERMS:
            cls._handle_permissions(state, vessel)

    @classmethod
    def _handle_hash_anchor(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Extracts integrity markers: @hash(sha256:digest)"""
        token = state.current()
        match = re.search(r'@hash\((?P<algo>\w+):(?P<digest>[a-fA-F0-9]+)\)', token.value)
        if match:
            vessel.expected_hash = f"{match.group('algo')}:{match.group('digest')}"
        state.advance()

    @classmethod
    def _handle_semantic_modifier(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Extracts component selectors: @inside(key="val")"""
        token = state.current()
        modifier_name = token.value.lstrip('@')
        state.advance()

        if state.current() and state.current().type == TokenType.SIGIL_LPAREN:
            state.advance()
            selector = {}
            while (arg_tok := state.current()):
                if arg_tok.type == TokenType.SIGIL_RPAREN:
                    state.advance()
                    break
                if arg_tok.type == TokenType.KEY_VALUE_PAIR:
                    k, v = arg_tok.value.split('=', 1)
                    selector[k.strip()] = v.strip().strip('"\'')
                state.advance()

            if not vessel.semantic_selector:
                vessel.semantic_selector = {}
            vessel.semantic_selector['type'] = modifier_name
            vessel.semantic_selector.update(selector)

    @classmethod
    def _handle_content_sigil(cls, state: DeconstructionState, vessel: GnosticVessel,
                              sigil_token: getattr(Token, '__class__', Any)):
        """Handles inline content assignment: :: "content" or += "content" """
        state.advance()

        # Map the Sigil to the Mutation Operation
        if sigil_token.type == TokenType.SIGIL_APPEND:
            vessel.mutation_op = "+="
        elif sigil_token.type == TokenType.SIGIL_SUBTRACT:
            vessel.mutation_op = "-="
        elif sigil_token.type == TokenType.SIGIL_TRANSFIGURE:
            vessel.mutation_op = "~="
        elif sigil_token.type == TokenType.SIGIL_PREPEND:
            vessel.mutation_op = "^="
        elif sigil_token.type == TokenType.SIGIL_SEED:
            cls._extract_seed_path(state, vessel)
            return

        # Gather remaining tokens as the raw content string
        parts = []
        while (token := state.current()):
            if token.type in (TokenType.SIGIL_PERMS, TokenType.COMMENT): break
            parts.append(token.value)
            state.advance()

        raw = "".join(parts).strip()

        # [ASCENSION 36]: Alchemical Injection Check (Codex Resolution)
        if '@' in raw and '/' in raw:
            try:
                # Lazy import to prevent circularity
                from .....codex import resolve_codex_directive
                raw = re.sub(r'(@[\w-]+/[\w-]+(?:\([^)]*\))?)',
                             lambda m: resolve_codex_directive(m.group(1), state.variables), raw)
            except Exception:
                pass

        # Unescape quotes and unicode
        vessel.content = cls._transmute_raw_matter(raw)

    @classmethod
    def _handle_block_sigil(cls, state: DeconstructionState, vessel: GnosticVessel,
                            sigil_token: getattr(Token, '__class__', Any)):
        """Handles multiline block starters: :: \"\"\" """
        state.advance()

        # Map the Block Sigil to Mutation
        if sigil_token.type in (TokenType.SIGIL_APPEND_BLOCK_DQ, TokenType.SIGIL_APPEND_BLOCK_SQ):
            vessel.mutation_op = "+="
        elif sigil_token.type in (TokenType.SIGIL_TRANSFIGURE_BLOCK_DQ, TokenType.SIGIL_TRANSFIGURE_BLOCK_SQ):
            vessel.mutation_op = "~="
        elif sigil_token.type in (TokenType.SIGIL_PREPEND_BLOCK_DQ, TokenType.SIGIL_PREPEND_BLOCK_SQ):
            vessel.mutation_op = "^="

        # Identify Quote Type
        if '"""' in sigil_token.value:
            vessel.content = '"""'
        elif "'''" in sigil_token.value:
            vessel.content = "'''"

    @classmethod
    def _handle_permissions(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Handles POSIX or Named permissions: %% 755 or %% executable"""
        state.advance()
        token = state.current()
        if not token: return

        if re.match(r'^0?[0-7]{3,4}$', token.value) or token.value in ('executable', 'readonly', 'secret', 'public',
                                                                       'private'):
            vessel.permissions = token.value
            state.advance()

    @classmethod
    def _extract_seed_path(cls, state: DeconstructionState, vessel: GnosticVessel):
        """Extracts path for the << operator."""
        parts = []
        while (token := state.current()):
            if token.type in (TokenType.SIGIL_PERMS, TokenType.COMMENT): break
            parts.append(token.value)
            state.advance()

        if parts:
            vessel.seed_path = Path("".join(parts).strip())

    @classmethod
    def _transmute_raw_matter(cls, content: str) -> str:
        """
        [ASCENSION 37]: THE LITERAL ESCAPE SUTURE.
        Transmutes `\"hello\"` to `hello` while preserving Python escapes like `\n`.
        """
        if content in ('"""', "'''"): return content

        # Protect Jinja pipes from evaluation
        is_alchemical = bool(re.match(r'''^\s*(?:(['"]).*?\1|[^'"\s|]+)\s*\|\s*[a-zA-Z_]''', content))
        if is_alchemical: return f"{{{{ {content} }}}}"

        if len(content) >= 2:
            first, last = content[0], content[-1]
            if (first == '"' and last == '"') or (first == "'" and last == "'"):
                inner = content[1:-1]
                try:
                    # Native python unicode escape un-escaping
                    return codecs.decode(inner.encode('utf-8'), 'unicode_escape')
                except Exception:
                    return inner

        return content