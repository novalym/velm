# Path: core/lsp/base/types/base.py
# ---------------------------------

from pydantic import BaseModel, ConfigDict


class LspModel(BaseModel):
    """
    =================================================================================
    == THE ANCESTRAL SOUL (V-Ω-ROOT-ENTITY)                                        ==
    =================================================================================
    The Root Spirit of the Gnostic Protocol.

    Every artifact, plea, and revelation within the Language Server inherits from
    this vessel. It defines the Immutable Laws of Serialization and Validation.

    [THE FIVE LAWS]:
    1.  **Law of Translation:** Automatically accepts `camelCase` JSON and binds it
        to `snake_case` attributes (`populate_by_name=True`).
    2.  **Law of Absorption:** Absorb unknown fields without fracture. If a Client
        sends new metadata, we keep it (`extra='allow'`).
    3.  **Law of Purity:** Validates data even upon mutation (`validate_assignment=True`).
    4.  **Law of Values:** Serializes Enums to their raw primitives (`use_enum_values=True`).
    5.  **Law of Matter:** Allows arbitrary types to coexist within the schema
        (`arbitrary_types_allowed=True`).
    """

    model_config = ConfigDict(
        # Allow initialization by field name (snake_case) or alias (camelCase)
        populate_by_name=True,

        # Permit custom types that Pydantic might not natively validate perfectly
        arbitrary_types_allowed=True,

        # Resilience against future protocol extensions or client-specific telemetry
        extra='allow',

        # Ensure purity is maintained if logic alters the state
        validate_assignment=True,

        # Serialize Enum members to their values (e.g. DiagnosticSeverity.Error -> 1)
        use_enum_values=True,

        # Performance: Don't strip whitespace from code content strings
        str_strip_whitespace=False
    )

    def __repr__(self) -> str:
        """
        [THE GNOSTIC GAZE]
        Returns a high-fidelity string representation for forensic logs.
        """
        # We use model_dump_json for a clean, deterministic representation
        return f"<{self.__class__.__name__}> {self.model_dump_json(exclude_none=True)}"