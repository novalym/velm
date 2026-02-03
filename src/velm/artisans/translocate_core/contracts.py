"""
=================================================================================
== THE SACRED SCRIPTURE OF TRANSLOCATION CONTRACTS (V-Ω-ETERNAL)               ==
=================================================================================
This sanctum contains the pure, Gnostic vessels (dataclasses) that carry the
will and the Gnosis throughout the Translocation symphony. It is the unbreakable
contract between the Detective, the Conductor, and the Resolvers.
=================================================================================
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass
class TranslocationMap:
    """
    The one true, Gnostic representation of a refactoring plan. It is a sacred
    map chronicling the journey of scriptures from their old reality to the new.

    The keys are the original, absolute paths of files/directories.
    The values are the new, absolute paths.
    """
    moves: Dict[Path, Path]

# In a future ascension, we could add vessels for Healing Edicts, etc.
# @dataclass
# class HealingEdict:
#     file_to_heal: Path
#     line_num: int
#     original_import: str
#     new_import: str