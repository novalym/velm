# Path: scaffold/parser_core/lexer_core/contracts.py
# --------------------------------------------------

from enum import Enum, auto
from pydantic import BaseModel, Field, ConfigDict


class TokenType(Enum):
    """
    =================================================================================
    == THE GNOSTIC SOUL OF THE ATOM (TokenType)                                    ==
    =================================================================================
    @gnosis:summary The complete enumeration of every recognized particle in the
                    Gnostic Grammar (V-Ω-EXPANDED).

    This Enum maps 1:1 with the Regex patterns defined in `scaffold.grammar`.
    It serves as the immutable alphabet of the God-Engine.
    """

    # -------------------------------------------------------------------------
    # I. THE ATOMS OF FORM (Core Values)
    # -------------------------------------------------------------------------
    UNKNOWN = auto()  # Profane matter, unrecognized by the Lexer
    PATH = auto()  # A filesystem path (The Locus)
    COMMENT = auto()  # A whisper to the Architect (Ignored by Engine)
    WORD = auto()  # Generic alphanumeric sequence
    QUOTED_STRING = auto()  # "Literal Truth"
    LITERAL = auto()  # Numbers or Booleans
    IDENTIFIER = auto()  # Variable names

    # -------------------------------------------------------------------------
    # II. THE ATOMS OF OPERATION (Separators & Keywords)
    # -------------------------------------------------------------------------
    OPERATOR_COLON = auto()  # :
    OPERATOR_COMMA = auto()  # ,
    OPERATOR_KEYWORD = auto()  # as, using, in

    # -------------------------------------------------------------------------
    # III. THE ATOMS OF MUTATION & DEFINITION (Scaffold Sigils)
    # -------------------------------------------------------------------------

    # -- The Trinity of Assignment --
    SIGIL_INLINE = auto()  # :: (Define content)
    SIGIL_SEED = auto()  # << (Seed from external)

    # -- The Sentinel of Links [NEW] --
    SIGIL_SYMLINK = auto()  # -> (Symlink Source -> Target)

    # -- The Operators of Transfiguration (Patching) --
    SIGIL_APPEND = auto()  # += (Append)
    SIGIL_SUBTRACT = auto()  # -= (Remove)
    SIGIL_TRANSFIGURE = auto()  # ~= (Regex Replace)
    SIGIL_PREPEND = auto()  # ^= (Prepend)

    # -- The Block Delimiters (Multi-line Souls) --
    SIGIL_MULTILINE_DQ = auto()  # :: """
    SIGIL_MULTILINE_SQ = auto()  # :: '''
    SIGIL_APPEND_BLOCK_DQ = auto()  # += """
    SIGIL_APPEND_BLOCK_SQ = auto()  # += '''
    SIGIL_TRANSFIGURE_BLOCK_DQ = auto()  # ~= """
    SIGIL_TRANSFIGURE_BLOCK_SQ = auto()  # ~= '''
    SIGIL_PREPEND_BLOCK_DQ = auto()  # ^= """
    SIGIL_PREPEND_BLOCK_SQ = auto()  # ^= '''

    SIGIL_INDENTED = auto()  # : (Implicit block start)

    # -- Metadata & Gnostic Vows --
    SIGIL_PERMS = auto()  # %% (Permissions)
    SIGIL_VAR_DEF = auto()  # $$ (Variable)
    SIGIL_VOW = auto()  # ?? (Assertion)

    # -- The Gnostic Traits (Mixins) [NEW] --
    SIGIL_TRAIT_DEF = auto()  # %% trait (Define Mixin)
    SIGIL_TRAIT_USE = auto()  # %% use (Apply Mixin)

    # -- The Integrity Anchor [NEW] --
    HASH_ANCHOR = auto()  # @hash(algo:digest)

    # -------------------------------------------------------------------------
    # IV. THE ATOMS OF WILL (Symphony Sigils)
    # -------------------------------------------------------------------------
    SIGIL_SIMPLE = auto()  # >>, ??, %% (Legacy grouping)
    SIGIL_HEREDOC = auto()  # << EOF
    SIGIL_DIRECTIVE = auto()  # @directive
    SIGIL_BLOCK_START = auto()  # block_name:
    SIGIL_PARALLEL = auto()  # &&
    SIGIL_BREAKPOINT = auto()  # !!

    # -------------------------------------------------------------------------
    # V. THE ATOMS OF LOGIC & STRUCTURE (Control Flow)
    # -------------------------------------------------------------------------
    SIGIL_IF = auto()
    SIGIL_ELIF = auto()
    SIGIL_ELSE = auto()
    SIGIL_ENDIF = auto()
    SIGIL_FOR = auto()
    SIGIL_ENDFOR = auto()

    # Resilience
    SIGIL_TRY = auto()
    SIGIL_CATCH = auto()
    SIGIL_FINALLY = auto()
    SIGIL_ENDTRY = auto()

    # Composition
    SIGIL_TASK_DEF = auto()
    SIGIL_TASK_END = auto()
    SIGIL_MACRO_DEF = auto()
    SIGIL_MACRO_END = auto()
    SIGIL_CALL = auto()
    SIGIL_IMPORT = auto()
    SIGIL_KILL = auto()  # @kill_port
    SIGIL_WEBHOOK = auto()  # @await_webhook
    SIGIL_HOARD = auto()  # %% hoard
    # -------------------------------------------------------------------------
    # VI. THE ATOMS OF VALUES (Complex Constructs)
    # -------------------------------------------------------------------------
    PERMISSIONS = auto()  # 755, executable, secret
    SEED_PATH = auto()  # Path after <<
    CONTENT = auto()  # Parsed content
    PLACEHOLDER = auto()  # {{ ... }}
    JINJA_CONSTRUCT = auto()  # {% ... %}

    # Semantic Arguments
    KEY_VALUE_PAIR = auto()  # key="val"
    SIGIL_LPAREN = auto()  # (
    SIGIL_RPAREN = auto()  # )


class Token(BaseModel):
    """
    =================================================================================
    == THE VESSEL OF THE ATOM (Token)                                              ==
    =================================================================================
    A pure, immutable vessel for a single atom of Gnostic grammar.
    It carries the Type (Soul) and the Value (Form) of the perceived text.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    type: TokenType = Field(..., description="The Gnostic classification of the atom.")
    value: str = Field(..., description="The raw textual content.")
    pos: int = Field(..., description="The character index where this atom begins.")