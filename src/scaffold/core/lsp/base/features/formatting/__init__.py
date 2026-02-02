# Path: core/lsp/features/formatting/__init__.py
# --------------------------------------------------

"""
=================================================================================
== THE HALL OF PURIFICATION (V-Ω-FORMATTING-CORE-V12)                          ==
=================================================================================
The engine of aesthetic structure.
Transmutes chaotic text into a state of geometric perfection.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import FormattingEngine
from .contracts import FormattingProvider
from .models import FormattingOptions, DocumentFormattingParams, TextEdit

__all__ = ["FormattingEngine", "FormattingProvider", "FormattingOptions", "DocumentFormattingParams", "TextEdit"]