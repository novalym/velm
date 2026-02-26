# Path: parser_core/parser/ast_weaver/contracts/spatial.py
# --------------------------------------------------------

from enum import Enum, auto


class SpatialRelationship(Enum):
    """
    =============================================================================
    == THE SPATIAL MATRIX (V-Ω-RELATIONAL-TOPOLOGY)                            ==
    =============================================================================
    Defines the absolute ontological relationship between two nodes in the
    Gnostic Abstract Syntax Tree based purely on their indentation coordinates.
    """
    PARENT = auto()  # The active node is shallower; it envelopes the new node.
    CHILD = auto()  # The active node is deeper; the new node envelopes it.
    SIBLING = auto()  # The nodes exist on the exact same topological plane.
    VOID = auto()  # The relationship is unmanifest or paradoxical.

    @classmethod
    def divine(cls, active_indent: int, incoming_indent: int) -> 'SpatialRelationship':
        """
        [ASCENSION 5]: The Sibling Matrix Logic.
        Calculates the relationship in O(1) time.
        """
        if incoming_indent > active_indent:
            return cls.CHILD
        elif incoming_indent == active_indent:
            return cls.SIBLING
        elif incoming_indent < active_indent:
            return cls.PARENT

        return cls.VOID