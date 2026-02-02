import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind

class RubyParser(BaseLanguageParser):
    RE_CLASS = re.compile(r'^\s*class\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_DEF = re.compile(r'^\s*def\s+([a-zA-Z0-9_]+)', re.MULTILINE)

    def parse(self, content, path):
        return (
            self._extract(self.RE_CLASS, content, path, SymbolKind.CLASS) +
            self._extract(self.RE_DEF, content, path, SymbolKind.FUNCTION)
        )