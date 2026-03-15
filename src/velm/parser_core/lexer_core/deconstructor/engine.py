# Path: src/velm/parser_core/lexer_core/deconstructor/engine.py
# -------------------------------------------------------------

import threading
import re
from typing import List, Dict, Any, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import GnosticVessel, GnosticLineType
from ....contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from ....contracts.symphony_contracts import EdictType
from ..contracts import Token, TokenType
from ....logger import Scribe

from .sentinel import CodeSentinel
from .state import DeconstructionState
from .handlers.form import FormHandler

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser

Logger = Scribe("DeconstructionScribe")


class DeconstructionScribe:
    """
    =================================================================================
    == THE GOD-ENGINE OF ATOMIC ASSEMBLY (V-Ω-TOTALITY-VMAX-ZERO-ALLOCATION)       ==
    =================================================================================
    LIF: ∞ | ROLE: TOKEN_TRANSMUTER | RANK: OMEGA_SOVEREIGN[THE MASTER CURE: ZERO-ALLOCATION VESSEL POOLING]
    Pydantic object creation is expensive. For a 100,000-line parse, we previously
    instantiated 100,000 GnosticVessels.

    Now, the Scribe uses a thread-local object pool. It borrows a vessel, resets
    its properties in C-time, populates it, and hands it back. This annihilates
    the Python GC (Garbage Collection) pause during deep architectural parsing.
    """

    # =========================================================================
    # == [ASCENSION 38]: THE O(1) JUMP TABLE                                 ==
    # =========================================================================
    # A mathematical map routing TokenTypes directly to their handler methods.
    # Completely replaces the O(N) if/elif chain.
    _JUMP_TABLE: Final[Dict[TokenType, str]] = {
        TokenType.SIGIL_SIMPLE: "_conduct_symphony_atomic",
        TokenType.SIGIL_VOW: "_conduct_vow",
        TokenType.SIGIL_TRAIT_DEF: "_conduct_trait_def",
        TokenType.SIGIL_TRAIT_USE: "_conduct_trait_use",
        TokenType.SIGIL_DIRECTIVE: "_conduct_directive"
    }

    # =========================================================================
    # == [ASCENSION 39]: THE THREAD-LOCAL VESSEL POOL                        ==
    # =========================================================================
    _vessel_pool = threading.local()

    # [ASCENSION 5]: THE RAW TRUTH FAILSAFE REGEX
    RAW_ASSIGNMENT_REGEX: Final[re.Pattern] = re.compile(r'(::|\+=|\^=|~=|<<|\*=)')

    __slots__ = ('raw_scripture', 'line_num', 'tokens', 'Logger', 'original_indent', 'variables', 'parser', 'vessel')

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

        # Acquire a Vessel from the Zero-Allocation Pool
        self.vessel = self._acquire_vessel()

    def _acquire_vessel(self) -> GnosticVessel:
        """[ASCENSION 40]: Fetches or resets a cached GnosticVessel."""
        if not hasattr(self._vessel_pool, 'vessel'):
            # The one-time instantiation per thread
            self._vessel_pool.vessel = GnosticVessel(
                raw_scripture=self.raw_scripture,
                line_num=self.line_num,
                original_indent=self.original_indent
            )
            return self._vessel_pool.vessel

        # O(1) attribute reset (Bypasses heavy Pydantic __init__ and validation tax)
        v = self._vessel_pool.vessel
        v.raw_scripture = self.raw_scripture
        v.line_num = self.line_num
        v.original_indent = self.original_indent

        # Reset fields to primordial state
        v.name = ""
        v.path = None
        v.content = None
        v.is_dir = False
        v.is_valid = True
        v.line_type = GnosticLineType.FORM
        v.mutation_op = None
        v.edict_type = None
        v.directive_type = None
        v.symlink_target = None
        v.is_symlink = False
        v.expected_hash = None
        v.semantic_selector = None
        v.seed_path = None
        v.permissions = None
        v.trait_name = None
        v.trait_path = None
        v.trait_args = None

        return v

    def inquire(self) -> GnosticVessel:
        """
        =========================================================================
        == THE GRAND RITE OF INQUIRY (ENTRY POINT)                             ==
        =========================================================================
        Analyzes the token stream and populates the GnosticVessel via O(1) jumps.
        """
        # 1. The Gaze of the Void
        if not self.tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        # 2. [ASCENSION 41]: The Code Sentinel (Fast-Fail)
        # We mathematically exclude valid Path assignments (::, +=) from rejection.
        if CodeSentinel.is_mental_matter(self.raw_scripture) and not self.RAW_ASSIGNMENT_REGEX.search(
                self.raw_scripture):
            self.Logger.verbose(f"L{self.line_num}: Code Sentinel detected mental matter. Suppressing physical form.")
            self.vessel.line_type = GnosticLineType.VOID
            return self.vessel

        first_token = self.tokens[0]

        # 3. [ASCENSION 42]: O(1) JUMP TABLE ROUTING
        # Eradicates the massive if/elif chain for symphonic, vow, trait, and directive signals.
        handler_method = self._JUMP_TABLE.get(first_token.type)

        if handler_method:
            # Dynamically invoke the internal handler
            getattr(self, handler_method)(first_token)
            return self.vessel

        # 4. [ASCENSION 43]: FALLBACK TO FORM HANDLER (PHYSICAL PATHS)
        try:
            # We initialize a fast-state cursor to pass to the Form Handler
            state = DeconstructionState(self.tokens, self.variables)
            FormHandler.handle(state, self.vessel)

            # [ASCENSION 5]: The Raw Truth Failsafe
            # If the FormHandler found no content, seed path, or mutation op,
            # but an assignment sigil exists, we default to block instantiation (""").
            if not self.vessel.content and not self.vessel.seed_path and not self.vessel.mutation_op:
                if self.RAW_ASSIGNMENT_REGEX.search(self.raw_scripture):
                    if '"' in self.raw_scripture or "'" in self.raw_scripture:
                        self.vessel.content = '"""'
                    elif '<<' in self.raw_scripture:
                        self.vessel.content = '"""'

        except Exception as e:
            self.vessel.is_valid = False
            self.Logger.error(
                f"[danger]Heresy META_HERESY_DECONSTRUCTION_FRACTURED on L{self.line_num}: Quantum Paradox during inquest: {e}[/danger]")

        return self.vessel

    # =========================================================================
    # == JUMP TABLE TARGETS                                                  ==
    # =========================================================================

    def _conduct_symphony_atomic(self, token: Token):
        """Translates >>, ??, and %% sigils into their respective Edict types."""
        sigil = token.value
        if sigil == ">>":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.ACTION
        elif sigil == "??":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.VOW
        elif sigil == "%%":
            self.vessel.line_type = GnosticLineType.VOW
            self.vessel.edict_type = EdictType.STATE

    def _conduct_vow(self, token: Token):
        """Processes assertion/vow logic."""
        self.vessel.line_type = GnosticLineType.VOW
        # Reconstruct content by skipping the first token (the sigil)
        # and joining the rest while filtering comments.
        vow_parts = [t.value for t in self.tokens[1:] if t.type != TokenType.COMMENT]
        self.vessel.content = " ".join(vow_parts).strip()

    def _conduct_trait_def(self, token: Token):
        """Processes %% trait definitions."""
        self.vessel.line_type = GnosticLineType.TRAIT_DEF

        # Verify length and type of next token
        if len(self.tokens) > 1 and self.tokens[1].type in (TokenType.IDENTIFIER, TokenType.WORD):
            self.vessel.trait_name = self.tokens[1].value

            # Verify assignment equals
            if len(self.tokens) > 2 and self.tokens[2].value == '=':
                if len(self.tokens) > 3:
                    self.vessel.trait_path = self.tokens[3].value.strip('"\'')
                else:
                    self.vessel.is_valid = False
                    self.Logger.error(
                        f"[danger]Heresy TRAIT_SYNTAX on L{self.line_num}: Expected path assignment for trait.[/danger]")
            else:
                if len(self.tokens) > 2:
                    self.vessel.trait_path = self.tokens[-1].value.strip('"\'')
        else:
            self.vessel.is_valid = False
            self.Logger.error(
                f"[danger]Heresy TRAIT_SYNTAX on L{self.line_num}: Expected trait name after '%% trait'.[/danger]")

    def _conduct_trait_use(self, token: Token):
        """Processes %% use injections."""
        self.vessel.line_type = GnosticLineType.TRAIT_USE
        if len(self.tokens) > 1:
            self.vessel.trait_name = self.tokens[1].value
            # Collect remaining arguments for the trait mixin
            args_parts = [t.value for t in self.tokens[2:] if t.type != TokenType.COMMENT]
            if args_parts:
                self.vessel.trait_args = " ".join(args_parts)
        else:
            self.vessel.is_valid = False
            self.Logger.error(
                f"[danger]Heresy TRAIT_SYNTAX on L{self.line_num}: Expected trait name after '%% use'.[/danger]")

    def _conduct_directive(self, token: Token):
        """Processes @directives mapping to Blocks or Tasks."""
        self.vessel.directive_type = token.value.lstrip('@')

        if self.raw_scripture.strip().endswith(':'):
            self.vessel.line_type = GnosticLineType.BLOCK_START
            self.vessel.edict_type = self._map_directive_to_edict_type(self.vessel.directive_type)
        else:
            self.vessel.edict_type = EdictType.DIRECTIVE

    def _map_directive_to_edict_type(self, directive: str) -> EdictType:
        """Determines the specific Enum type based on the directive keyword."""
        d = directive.lower()
        if d in ('if', 'elif', 'else'): return EdictType.CONDITIONAL
        if d == 'for': return EdictType.LOOP
        if d == 'try': return EdictType.RESILIENCE
        if d in ('task', 'macro'): return EdictType.DIRECTIVE
        if d == 'conduct': return EdictType.ACTION
        return EdictType.DIRECTIVE