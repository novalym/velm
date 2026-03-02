# Path: src/velm/core/lsp/base/types/primitives.py
# ------------------------------------------------

from __future__ import annotations
from enum import Enum
from typing import Union, List, Optional, Any, Dict, Literal
from pydantic import Field, model_validator, RootModel, ConfigDict
from .base import LspModel


# =================================================================================
# == I. THE IDENTIFIERS (ROOT TYPES)                                             ==
# =================================================================================

class URI(RootModel[str]):
    """
    [THE UNIFORM ANCHOR]
    A uniform resource identifier.[THE CURE]: __str__ ensures Pydantic V2 resolves the raw string soul,
    preventing the 'root=...' corruption heresy.
    """

    def __str__(self): return str(self.root)

    def __repr__(self): return f"'{self.root}'"


class DocumentUri(RootModel[str]):
    """The sacred string path to a scripture."""

    def __str__(self): return str(self.root)

    def __repr__(self): return f"'{self.root}'"


class ProgressToken(RootModel[Union[int, str]]):
    """A token used to report progress on a long-running rite."""

    def __str__(self): return str(self.root)

    def __repr__(self): return f"'{self.root}'"


class TraceValue(str, Enum):
    """The level of forensic detail requested."""
    Off = 'off'
    Messages = 'messages'
    Verbose = 'verbose'


# =================================================================================
# == II. THE GEOMETRY OF SPACETIME                                               ==
# =================================================================================

class Position(LspModel):
    """
    =============================================================================
    == THE ATOM OF LOCATION (V-Ω-FLUID-GEOMETRY-V200)                          ==
    =============================================================================
    LIF: 100,000x | ROLE: SPATIAL_COORDINATE | RANK: OMEGA_PRIMITIVE

    A zero-based point in 2D spacetime.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **The Thaw (THE CURE):** The `frozen=True` heresy has been annihilated.
        The God-Engine frequently expands blocks and ranges during dynamic AST
        reconstruction (e.g., SymbolEngine). This atom is now fluid, yet protected
        by Pydantic's mutation validation (`validate_assignment=True`).
    2.  **Isomorphic Comparison:** Overloaded `__eq__` and `__lt__` methods intelligently
        detect and compare against raw `dict` payloads sent by the Client, preventing
        'unsupported operand type' crashes when un-hydrated JSON touches the Engine.
    3.  **Hashable Fluidity:** Explicitly implements `__hash__` to guarantee the
        model can be stored in Sets and Dictionaries even while fully mutable.
    """
    model_config = ConfigDict(validate_assignment=True)

    line: int = Field(..., ge=0, description="Line position in a document (zero-based).")
    character: int = Field(..., ge=0, description="Character offset on a line (zero-based).")

    def __lt__(self, other: Union['Position', Dict[str, int]]) -> bool:
        o_line = other['line'] if isinstance(other, dict) else other.line
        o_char = other['character'] if isinstance(other, dict) else other.character
        if self.line < o_line: return True
        if self.line == o_line: return self.character < o_char
        return False

    def __le__(self, other: Union['Position', Dict[str, int]]) -> bool:
        return self < other or self == other

    def __gt__(self, other: Union['Position', Dict[str, int]]) -> bool:
        return not self <= other

    def __ge__(self, other: Union['Position', Dict[str, int]]) -> bool:
        return not self < other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict) and 'line' in other and 'character' in other:
            return self.line == other['line'] and self.character == other['character']
        if not isinstance(other, Position): return False
        return self.line == other.line and self.character == other.character

    def __hash__(self):
        # [ASCENSION]: Hashing remains perfectly intact despite fluidity.
        return hash((self.line, self.character))


class Range(LspModel):
    """
    =============================================================================
    == THE VESSEL OF EXTENT (V-Ω-FLUID-EXPANSION-V200)                         ==
    =============================================================================
    LIF: 100,000x | ROLE: SPATIAL_BOUNDARIES | RANK: OMEGA_PRIMITIVE

    A range expressed as (zero-based) start and end positions.
    Enforces the Law of Chronology: End must not precede Start.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Dynamic Boundary Expansion:** Unfrozen to allow hierarchical processors
        (like `SymbolEngine` and `FoldingRangeEngine`) to stretch the range as
        child nodes are discovered.
    2.  **Auto-Healing Chronology Ward:** When `validate_assignment=True` is active,
        mutating `start` and `end` sequentially creates a temporary invalid state
        if the new `start` eclipses the old `end`. The `validate_chronology` interceptor
        detects this race condition and automatically stretches the `end` coordinate
        to match, preventing a mid-assignment validation crash.
    """
    model_config = ConfigDict(validate_assignment=True)

    start: Position
    end: Position

    @model_validator(mode='after')
    def validate_chronology(self) -> 'Range':
        if self.end < self.start:
            # [ASCENSION 2: THE AUTO-HEALING WARD]
            # Pydantic triggers validation on *every* assignment.
            # If an artisan performs: `range.start = new_start`, and `new_start`
            # is past the current `range.end`, it will crash before they can update `range.end`.
            # We catch this temporal paradox and auto-heal the end vector to match the start,
            # ensuring the range collapses into a singularity rather than a fatal exception.
            self.end = Position(line=self.start.line, character=self.start.character)
        return self

    def contains(self, pos: Position) -> bool:
        """Adjudicates if a spatial coordinate falls within this geometric boundary."""
        return self.start <= pos <= self.end

    def __hash__(self):
        return hash((self.start, self.end))


class Location(LspModel):
    """
    [THE ANCHOR]
    Represents a location inside a resource, such as a line inside a text file.
    """
    uri: DocumentUri
    range: Range


class LocationLink(LspModel):
    """
    [THE BRIDGE]
    Represents a link between a source and a target location.
    Used for 'Go to Definition' to show the exact origin span.
    """
    model_config = ConfigDict(populate_by_name=True)

    origin_selection_range: Optional[Range] = Field(None, alias="originSelectionRange",
                                                    description="Span of the origin text.")
    target_uri: DocumentUri = Field(..., alias="targetUri", description="The target resource.")
    target_range: Range = Field(..., alias="targetRange", description="The full range of the target element.")
    target_selection_range: Range = Field(..., alias="targetSelectionRange",
                                          description="The range to highlight (e.g., function name).")


# =================================================================================
# == III. THE IDENTITY OF SCRIPTURE                                              ==
# =================================================================================

class TextDocumentIdentifier(LspModel):
    """
    [THE NAMING]
    Identifies a document using a URI.
    """
    uri: DocumentUri


class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """
    [THE CHRONICLE]
    Identifies a specific version of a document.
    """
    version: int = Field(..., description="The version number of this document.")


class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """
    [THE WEAK LINK]
    Identifies a document, optionally specifying a version.
    """
    version: Optional[int] = None


class TextDocumentItem(LspModel):
    """
    [THE FULL MANIFEST]
    The complete soul of a file transmitted during the 'didOpen' rite.
    """
    uri: DocumentUri
    language_id: str = Field(..., alias="languageId")
    version: int
    text: str


# =================================================================================
# == IV. THE RITES OF MUTATION                                                   ==
# =================================================================================

class TextEdit(LspModel):
    """
    [THE DELTA]
    A textual edit applicable to a text document.
    """
    range: Range
    new_text: str = Field(..., alias="newText")


class ChangeAnnotation(LspModel):
    """
    [THE FOOTNOTE]
    Metadata describing a document change (e.g., "Refactoring").
    """
    label: str
    needs_confirmation: Optional[bool] = Field(None, alias="needsConfirmation")
    description: Optional[str] = None


class AnnotatedTextEdit(TextEdit):
    """[THE SIGNED DELTA]
    A text edit with an additional change annotation.
    """
    annotation_id: str = Field(..., alias="annotationId")


class ResourceOperationKind(str, Enum):
    Create = 'create'
    Rename = 'rename'
    Delete = 'delete'


class FailureHandlingKind(str, Enum):
    Abort = 'abort'
    Transactional = 'transactional'
    TextOnlyTransactional = 'textOnlyTransactional'
    Undo = 'undo'


# =================================================================================
# == V. THE WILL & PROCLAMATION                                                  ==
# =================================================================================

class Command(LspModel):
    """
    [THE EDICT]
    A reference to a server-side command rite.
    """
    title: str = Field(..., description="Title of the command, like 'save'.")
    command: str = Field(..., description="The identifier of the actual command handler.")
    arguments: Optional[List[Any]] = Field(None,
                                           description="Arguments that the command handler should be invoked with.")


class MarkupKind(str, Enum):
    """The tongue of the description."""
    PlainText = "plaintext"
    Markdown = "markdown"


class MarkupContent(LspModel):
    """[THE SCROLL]
    A string interpreted based on its kind (Markdown or Plaintext).
    """
    kind: MarkupKind
    value: str


# =================================================================================
# == VI. THE PROTOCOL MECHANICS (MIXINS)                                         ==
# =================================================================================

class WorkDoneProgressParams(LspModel):
    """
    [THE LABOR TOKEN]
    Mixin for requests that support progress reporting.
    """
    work_done_token: Optional[ProgressToken] = Field(None, alias="workDoneToken")


class WorkDoneProgressOptions(LspModel):
    """[THE CAPABILITY OF LABOR]
    Options to signal support for progress reporting.
    """
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")


class PartialResultParams(LspModel):
    """
    [THE STREAMING TOKEN]
    Mixin for requests that support streaming partial results.
    """
    partial_result_token: Optional[ProgressToken] = Field(None, alias="partialResultToken")