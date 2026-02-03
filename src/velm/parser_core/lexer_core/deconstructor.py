# Path: scaffold/parser_core/lexer_core/deconstructor.py
# ------------------------------------------------------

import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Set, TYPE_CHECKING

from .contracts import Token, TokenType
from ...contracts.data_contracts import GnosticVessel, GnosticLineType
from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from ...contracts.symphony_contracts import EdictType  # <--- ASCENSION: Import EdictType
from ...logger import Scribe

if TYPE_CHECKING:
    from ..parser import ApotheosisParser

Logger = Scribe("DeconstructionScribe")


class DeconstructionScribe:
    """
    =================================================================================
    == THE GOD-ENGINE OF ATOMIC ASSEMBLY (V-Ω-SEMANTIC-AWARE-ULTIMA-FIXED)         ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan takes the raw atoms (Tokens) and weaves them into a coherent
    GnosticVessel. It understands:
    1.  **The Trinity of Assignment:** Definition (::), Seeding (<<), and Mutation (+=, -=, ~=).
    2.  **The Semantic Context:** Directives like `@inside(...)`.
    3.  **The Gnostic Vow:** Assertions like `?? file_exists`.
    4.  **The Permissions:** Mode bits (%% 755) and Named (%% executable).
    5.  **The Sentinel of Links:** Symbolic links via `->`.
    6.  **The Hash Anchor:** Integrity verification via `@hash(...)`.
    7.  **The Symphonic Triad (THE FIX):** Actions (>>), Vows (??), and State (%%) via SIGIL_SIMPLE.
    """

    CONTENT_SIGILS: Set[TokenType] = {
        TokenType.SIGIL_INLINE,
        TokenType.SIGIL_APPEND,
        TokenType.SIGIL_SUBTRACT,
        TokenType.SIGIL_TRANSFIGURE,
        TokenType.SIGIL_PREPEND,
        TokenType.SIGIL_SEED,
        TokenType.SIGIL_SYMLINK
    }

    BLOCK_SIGILS: Set[TokenType] = {
        TokenType.SIGIL_MULTILINE_DQ,
        TokenType.SIGIL_MULTILINE_SQ,
        TokenType.SIGIL_INDENTED,
        TokenType.SIGIL_APPEND_BLOCK_DQ,
        TokenType.SIGIL_APPEND_BLOCK_SQ,
        TokenType.SIGIL_TRANSFIGURE_BLOCK_DQ,
        TokenType.SIGIL_TRANSFIGURE_BLOCK_SQ,
        TokenType.SIGIL_PREPEND_BLOCK_DQ,
        TokenType.SIGIL_PREPEND_BLOCK_SQ
    }

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
        self.raw_scripture = raw_scripture
        self.line_num = line_num
        self.tokens = tokens
        self.Logger = logger
        self.original_indent = original_indent
        self.variables = variables
        self.parser = parser
        self._cursor = 0
        self.vessel = GnosticVessel(
            raw_scripture=self.raw_scripture,
            line_num=self.line_num,
            original_indent=self.original_indent
        )

    def inquire(self) -> GnosticVessel:
        """The Grand Rite of Deconstruction."""
        if not self.tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        first_token = self.tokens[0]

        # [FIX] THE SYMPHONIC TRIAD (SIGIL_SIMPLE)
        # We must explicitly handle >>, ??, and %% when they appear as SIGIL_SIMPLE
        if first_token.type == TokenType.SIGIL_SIMPLE:
            self._conduct_symphony_atomic_inquest()
            return self.vessel

        # [FACULTY 1] THE VOW CHECK (Legacy / Scaffold Vows)
        if first_token.type == TokenType.SIGIL_VOW:
            self._conduct_vow_inquest()
            return self.vessel

        # [FACULTY 2] THE TRAIT CHECK
        if first_token.type == TokenType.SIGIL_TRAIT_DEF:
            self._conduct_trait_def_inquest()
            return self.vessel
        if first_token.type == TokenType.SIGIL_TRAIT_USE:
            self._conduct_trait_use_inquest()
            return self.vessel

        # [FACULTY 3] THE DIRECTIVE CHECK (@directive)
        # This handles @task, @macro, @import, etc.
        if first_token.type == TokenType.SIGIL_DIRECTIVE:
            self.vessel.directive_type = first_token.value.lstrip('@')
            # If it ends with a colon (e.g., @task deploy:), it's a block start
            if self.raw_scripture.strip().endswith(':'):
                self.vessel.line_type = GnosticLineType.BLOCK_START
                self.vessel.edict_type = self._map_directive_to_edict_type(self.vessel.directive_type)
            else:
                self.vessel.edict_type = EdictType.DIRECTIVE
            return self.vessel

        try:
            self._conduct_gnostic_inquest()
        except Exception as e:
            self._proclaim_heresy("META_HERESY_DECONSTRUCTION_FRACTURED", f"Quantum Paradox: {e}")

        return self.vessel

    def _conduct_symphony_atomic_inquest(self):
        """
        [THE ASCENSION] Parses >>, ??, %% for Symphony mode.
        """
        sigil = self.tokens[0].value

        # We set the high-level Line Type (used by Parser Triage)
        # And the specific Edict Type (used by Symphony Scribes)

        if sigil == ">>":
            self.vessel.line_type = GnosticLineType.VOW  # Mapped to Atomic Scribe in Parser
            self.vessel.edict_type = EdictType.ACTION
        elif sigil == "??":
            self.vessel.line_type = GnosticLineType.VOW  # Mapped to Atomic Scribe in Parser
            self.vessel.edict_type = EdictType.VOW
        elif sigil == "%%":
            self.vessel.line_type = GnosticLineType.VOW  # Mapped to Atomic Scribe in Parser
            self.vessel.edict_type = EdictType.STATE

        # The content is the rest of the line, which the Scribe will parse further
        # We don't need to strip it here, the AtomicScribe uses raw_scripture

    def _map_directive_to_edict_type(self, directive: str) -> EdictType:
        """Maps @directives to EdictTypes."""
        if directive in ('if', 'elif', 'else'): return EdictType.CONDITIONAL
        if directive == 'for': return EdictType.LOOP
        if directive == 'try': return EdictType.RESILIENCE
        if directive == 'task': return EdictType.DIRECTIVE  # Treated as directive but block start
        if directive == 'macro': return EdictType.DIRECTIVE
        if directive == 'conduct': return EdictType.ACTION  # Or Directive? Usually single line.
        return EdictType.DIRECTIVE

    def _current(self) -> Optional[Token]:
        if self._cursor < len(self.tokens):
            return self.tokens[self._cursor]
        return None

    def _advance(self) -> None:
        self._cursor += 1

    def _conduct_vow_inquest(self):
        """Parses a Vow line: `?? contains 'foo'`"""
        self.vessel.line_type = GnosticLineType.VOW
        self._advance()  # Consume ??
        vow_parts = []
        while (token := self._current()):
            if token.type == TokenType.COMMENT: break
            vow_parts.append(token.value)
            self._advance()
        self.vessel.content = " ".join(vow_parts).strip()

    def _conduct_trait_def_inquest(self):
        """
        Parses: %% trait Auth = "./traits/auth.scaffold"
        """
        self.vessel.line_type = GnosticLineType.TRAIT_DEF
        self._advance()  # Consume %% trait

        if not self._current() or self._current().type not in (TokenType.IDENTIFIER, TokenType.WORD):
            self._proclaim_heresy("TRAIT_SYNTAX", "Expected trait name after '%% trait'.")
            return

        self.vessel.trait_name = self._current().value
        self._advance()

        curr = self._current()
        if curr and curr.value == '=':
            self._advance()

        if not self._current():
            self._proclaim_heresy("TRAIT_SYNTAX", "Expected path assignment for trait.")
            return

        path_token = self._current()
        path_val = path_token.value.strip('"\'')
        self.vessel.trait_path = path_val
        self._advance()

    def _conduct_trait_use_inquest(self):
        """
        Parses: %% use Auth
        """
        self.vessel.line_type = GnosticLineType.TRAIT_USE
        self._advance()  # Consume %% use

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

    def _conduct_gnostic_inquest(self):
        """
        Parses a standard line: `path -> target @hash(...) += content %% perms # comment`
        """
        self.vessel.line_type = GnosticLineType.FORM

        # 1. CONSUME THE PATH
        path_tokens = []
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
            # Check for directive-only line (@if) handled earlier?
            # Or if it was just whitespace handled by void check?
            self.vessel.line_type = GnosticLineType.VOID
            return

        raw_path = "".join(path_tokens)
        purified = self._purify_path_name(raw_path)

        if purified:
            self.vessel.name = purified
            self.vessel.path = Path(self.vessel.name)
            self.vessel.is_dir = purified.endswith('/') or purified.endswith('\\')

        # 2. CHECK FOR SYMLINK (->)
        if self._current() and self._current().type == TokenType.SIGIL_SYMLINK:
            self._handle_symlink()
            return

        # 3. CHECK FOR HASH ANCHOR (@hash)
        if self._current() and self._current().type == TokenType.HASH_ANCHOR:
            self._handle_hash_anchor()

        # 4. THE SEMANTIC MODIFIER GAZE (@inside)
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
                self._advance()
                return
            else:
                self._advance()

        # 6. FINAL PERMISSIONS CHECK (Post-Content)
        if self._current() and self._current().type == TokenType.SIGIL_PERMS:
            self._handle_permissions()

    def _handle_symlink(self):
        self.vessel.is_symlink = True
        self._advance()  # Consume ->

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
        raw = token.value
        match = re.search(r'@hash\((?P<algo>\w+):(?P<digest>[a-fA-F0-9]+)\)', raw)
        if match:
            self.vessel.expected_hash = f"{match.group('algo')}:{match.group('digest')}"
        else:
            self._proclaim_heresy("MALFORMED_HASH", f"Invalid hash anchor format: {raw}")
        self._advance()

    def _handle_semantic_modifier(self):
        token = self._current()
        modifier_name = token.value.lstrip('@')
        self._advance()

        if self._current() and self._current().type == TokenType.SIGIL_LPAREN:
            self._advance()  # Eat (
            selector = {}
            while (arg_tok := self._current()):
                if arg_tok.type == TokenType.SIGIL_RPAREN:
                    self._advance()  # Eat )
                    break
                if arg_tok.type == TokenType.KEY_VALUE_PAIR:
                    raw_kv = arg_tok.value
                    if '=' in raw_kv:
                        k, v = raw_kv.split('=', 1)
                        selector[k.strip()] = v.strip().strip('"\'')
                self._advance()

            if not self.vessel.semantic_selector:
                self.vessel.semantic_selector = {}
            self.vessel.semantic_selector['type'] = modifier_name
            self.vessel.semantic_selector.update(selector)

    def _handle_content_sigil(self, sigil_token: Token):
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
        self.vessel.content = self._purify_content_string(processed)

    def _handle_block_sigil(self, sigil_token: Token):
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
        self._advance()  # Eat %%
        token = self._current()
        if token and (re.match(r'^[0-7]{3}$', token.value) or token.value in ('executable', 'readonly', 'secret')):
            self.vessel.permissions = token.value
            self._advance()
        elif token and token.type == TokenType.PERMISSIONS:
            self.vessel.permissions = token.value
            self._advance()
        else:
            self._proclaim_heresy("PROFANE_WILL_HERESY", "Expected 3-digit octal or named permission.")

    def _extract_seed_path(self):
        parts = []
        while (token := self._current()):
            if token.type in (TokenType.SIGIL_PERMS, TokenType.COMMENT): break
            parts.append(token.value)
            self._advance()
        if not parts:
            self._proclaim_heresy("VOID_SOUL_HERESY_SEED", "Seed path required.")
            return
        self.vessel.seed_path = Path("".join(parts).strip())

    def _purify_path_name(self, raw: str) -> str:
        clean = raw.replace('\ufeff', '').replace('\u200b', '')
        clean = re.sub(r'^[\u2500-\u257f\|\+\\`\s\t-]+', '', clean).strip()
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'"))):
            clean = clean[1:-1]
        return clean.strip() if clean not in ('.', './', '.\\', '') else ""

    def _purify_content_string(self, content: str) -> str:
        if content in ('"""', "'''"): return content
        is_alchemical = bool(re.match(r'''^\s*(?:(['"]).*?\1|[^'"\s|]+)\s*\|\s*[a-zA-Z_]''', content))
        if is_alchemical: return f"{{{{ {content} }}}}"
        if len(content) >= 2 and ((content.startswith('"') and content.endswith('"')) or (
                content.startswith("'") and content.endswith("'"))):
            return content[1:-1]
        return content

    def _perform_semantic_injection(self, content: str, token: Token) -> str:
        if '@' not in content or '/' not in content: return content
        from ...semantic_injection import resolve_semantic_directive
        def _transmute(match):
            try:
                return resolve_semantic_directive(match.group(1), self.variables)
            except Exception:
                return match.group(1)

        try:
            return re.sub(r'(@[\w-]+/[\w-]+(?:\([^)]*\))?)', _transmute, content)
        except Exception:
            return content

    def _proclaim_heresy(self, key: str, details: str, token: Optional[Token] = None):
        self.vessel.is_valid = False
        loc = f" near '{token.value}'" if token else ""
        self.Logger.error(f"[danger]Heresy {key} on L{self.line_num}{loc}: {details}[/danger]")