# Path: core/lsp/base/types/primitives.py
# ---------------------------------------
from __future__ import annotations
from enum import Enum
from typing import Union, List, Optional, Any, Dict, Literal
from pydantic import Field, model_validator, RootModel, ConfigDict
from .base import LspModel


# =================================================================================
# == I. THE IDENTIFIERS (ROOT TYPES)                                             ==
# =================================================================================

class URI(RootModel[str]):
    """A uniform resource identifier."""
    pass


class DocumentUri(RootModel[str]):
    """The sacred string path to a scripture."""
    pass


class ProgressToken(RootModel[Union[int, str]]):
    """A token used to report progress on a long-running rite."""
    pass


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
    [THE ATOM OF LOCATION]
    A zero-based point in 2D spacetime.
    Includes dunder methods for geometric comparison.
    """
    model_config = ConfigDict(frozen=True)

    line: int = Field(..., ge=0, description="Line position in a document (zero-based).")
    character: int = Field(..., ge=0, description="Character offset on a line (zero-based).")

    def __lt__(self, other: 'Position') -> bool:
        if self.line < other.line: return True
        if self.line == other.line: return self.character < other.character
        return False

    def __le__(self, other: 'Position') -> bool:
        return self < other or self == other

    def __gt__(self, other: 'Position') -> bool:
        return not self <= other

    def __ge__(self, other: 'Position') -> bool:
        return not self < other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position): return False
        return self.line == other.line and self.character == other.character

    def __hash__(self):
        return hash((self.line, self.character))


class Range(LspModel):
    """
    [THE VESSEL OF EXTENT]
    A range expressed as (zero-based) start and end positions.
    Enforces the Law of Chronology: End must not precede Start.
    """
    model_config = ConfigDict(frozen=True)

    start: Position
    end: Position

    @model_validator(mode='after')
    def validate_chronology(self) -> 'Range':
        if self.end < self.start:
            # Auto-correction could be dangerous, so we raise a Heresy
            raise ValueError(f"Geometric Paradox: End {self.end} precedes start {self.start}.")
        return self

    def contains(self, pos: Position) -> bool:
        """Adjudicates if a position falls within this range."""
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
    """
    [THE SIGNED DELTA]
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
    """
    [THE SCROLL]
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
    """
    [THE CAPABILITY OF LABOR]
    Options to signal support for progress reporting.
    """
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")


class PartialResultParams(LspModel):
    """
    [THE STREAMING TOKEN]
    Mixin for requests that support streaming partial results.
    """
    partial_result_token: Optional[ProgressToken] = Field(None, alias="partialResultToken")