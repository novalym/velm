# Path: artisans/indexer/languages/factory.py
from typing import Optional, Dict
from pathlib import Path
from .base import BaseLanguageParser
from .python import PythonParser
from .javascript import JavaScriptParser
from .go import GoParser
from .rust import RustParser
from .java import JavaParser
from .ruby import RubyParser

class LanguageFactory:
    _REGISTRY: Dict[str, BaseLanguageParser] = {
        '.py': PythonParser(),
        '.js': JavaScriptParser(), '.jsx': JavaScriptParser(),
        '.ts': JavaScriptParser(), '.tsx': JavaScriptParser(),
        '.go': GoParser(),
        '.rs': RustParser(),
        '.java': JavaParser(),
        '.rb': RubyParser()
    }

    @staticmethod
    def get_parser(path: Path) -> Optional[BaseLanguageParser]:
        return LanguageFactory._REGISTRY.get(path.suffix.lower())