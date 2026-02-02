# Path: core/lsp/features/code_action/__init__.py
# -----------------------------------------------

"""
=================================================================================
== THE HALL OF REDEMPTION (V-Ω-CODE-ACTION-CORE-V12)                           ==
=================================================================================
The engine of restorative action and architectural evolution.
Orchestrates the discovery and execution of QuickFixes and Refactorings.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import CodeActionEngine
from .contracts import CodeActionProvider
from .models import CodeAction, CodeActionKind, CodeActionParams

__all__ = ["CodeActionEngine", "CodeActionProvider", "CodeAction", "CodeActionKind", "CodeActionParams"]