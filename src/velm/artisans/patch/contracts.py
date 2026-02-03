# Path: scaffold/artisans/patch/contracts.py
# ------------------------------------------


from enum import Enum
from typing import Optional

from pydantic import Field, field_validator

# --- THE DIVINE SUMMONS ---
from ...contracts.data_contracts import ScaffoldItem


class MutationOp(str, Enum):
    """
    The Sacred Glyphs of Transmutation.
    Each operator defines a specific mode of interaction with reality.
    """
    DEFINE = "::"  # The Rite of Creation (Overwrite/Create)
    APPEND = "+="  # The Rite of Addition (Text Append / Deep Merge)
    PREPEND = "^="  # The Rite of Introduction (Text Prepend)
    SUBTRACT = "-="  # The Rite of Excision (Regex Deletion)
    TRANSFIGURE = "~="  # The Rite of Alchemy (Regex Substitution)


class MutationEdict(ScaffoldItem):
    """
    =================================================================================
    == THE VESSEL OF MUTATION (V-Ω-STRUCTURAL-AWARENESS-HEALED)                    ==
    =================================================================================
    LIF: 1,000,000,000

    This vessel carries the Architect's will to change a specific scripture.
    It inherits the full Gnosis of a `ScaffoldItem` (path, content, line_num)
    but adds the specific mechanics of the mutation.

    ### ASCENDED FACULTIES:
    1.  **Structural Self-Awareness:** It knows if it targets a structured file
        (.json, .yaml) and automatically flags itself for a Deep Merge instead
        of a text append.
    2.  **Anchor Hashing:** Carries the `anchor_hash` metadata to verify the
        state of the target before operating.
    3.  **Operator Validation (The Fix):** The `mutation_op` field is now robust.
        It accepts the string values from the parser and validates them into the Enum.
        Crucially, it defaults to `DEFINE` if the input is None, healing the
        `ValidationError` heresy.
    """

    # We override the field to ensure it is validated as the Enum, but we allow
    # the input to be optional (defaulting to DEFINE).
    mutation_op: MutationOp = Field(
        default=MutationOp.DEFINE,
        description="The glyph representing the type of change."
    )

    anchor_hash: Optional[str] = Field(
        default=None,
        description="The required start-state hash (first 8 chars) for safety."
    )

    @field_validator('mutation_op', mode='before')
    @classmethod
    def validate_op(cls, v):
        """
        [THE RITE OF OPERATOR HEALING]
        Transmutes None or string values into the sacred Enum.
        """
        if v is None:
            return MutationOp.DEFINE
        if isinstance(v, MutationOp):
            return v
        try:
            return MutationOp(v)
        except ValueError:
            # If the value is profane, we default to DEFINE but warn?
            # Or we raise? Raising is safer.
            raise ValueError(f"Unknown mutation operator: {v}")

    # --- THE GAZE OF STRUCTURE ---
    @property
    def is_structural(self) -> bool:
        """
        Adjudicates if this edict requires a Structured Merge (JSON/YAML)
        rather than a textual append.
        """
        if not self.path:
            return False

        # The Grimoire of Structured Tongues
        STRUCTURAL_EXTENSIONS = {'.json', '.yaml', '.yml', '.toml'}

        is_structured_file = self.path.suffix.lower() in STRUCTURAL_EXTENSIONS
        is_additive_op = self.mutation_op == MutationOp.APPEND

        return is_structured_file and is_additive_op

    @property
    def is_regex_op(self) -> bool:
        """Determines if the content should be treated as a Regex pattern."""
        return self.mutation_op in (MutationOp.SUBTRACT, MutationOp.TRANSFIGURE)

    def describe(self) -> str:
        """Returns a human-readable prophecy of the edict."""
        if self.is_structural:
            return f"Deep Merge into '{self.path.name}'"

        descriptions = {
            MutationOp.DEFINE: f"Define '{self.path.name}'",
            MutationOp.APPEND: f"Append to '{self.path.name}'",
            MutationOp.PREPEND: f"Prepend to '{self.path.name}'",
            MutationOp.SUBTRACT: f"Excise pattern from '{self.path.name}'",
            MutationOp.TRANSFIGURE: f"Transfigure '{self.path.name}'",
        }
        return descriptions.get(self.mutation_op, "Unknown Rite")