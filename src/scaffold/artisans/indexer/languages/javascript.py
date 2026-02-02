import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind

class JavaScriptParser(BaseLanguageParser):
    RE_CLASS = re.compile(r'class\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_FUNC = re.compile(r'function\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_CONST_FUNC = re.compile(r'(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', re.MULTILINE)
    RE_INTERFACE = re.compile(r'interface\s+([a-zA-Z0-9_]+)', re.MULTILINE)

    def parse(self, content, path):
        return (
            self._extract(self.RE_CLASS, content, path, SymbolKind.CLASS) +
            self._extract(self.RE_FUNC, content, path, SymbolKind.FUNCTION) +
            self._extract(self.RE_CONST_FUNC, content, path, SymbolKind.FUNCTION) +
            self._extract(self.RE_INTERFACE, content, path, SymbolKind.INTERFACE)
        )