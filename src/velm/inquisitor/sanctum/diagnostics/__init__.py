# Path: scaffold/inquisitor/sanctum/diagnostics/__init__.py
"""The sacred gateway to the Pantheon of Inquisitors."""
from .go import GoInquisitor
from .javascript import JavaScriptInquisitor
from .python import PythonInquisitor
from .react import ReactInquisitor
from .ruby import RubyInquisitor

__all__ = ["PythonInquisitor", "JavaScriptInquisitor", "GoInquisitor", "RubyInquisitor", "ReactInquisitor"]