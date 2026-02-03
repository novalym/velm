# // scaffold/artisans/translocate_core/resolvers/java/contracts.py
# -----------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class JavaDetectedImport:
    """
    A raw import statement perceived by the Java Inquisitor.
    """
    line_num: int
    package_path: str  # e.g. "com.example.utils.Helper"
    is_static: bool  # import static ...
    start_byte: int  # Start offset of the package string
    end_byte: int  # End offset of the package string


@dataclass
class JavaHealingEdict:
    """
    An instruction to transfigure a Java import.
    """
    line_num: int
    original_path: str
    new_path: str
    start_byte: int
    end_byte: int

