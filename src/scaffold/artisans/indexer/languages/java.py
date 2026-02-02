import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind

class JavaParser(BaseLanguageParser):
    RE_CLASS = re.compile(r'\bclass\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_INTERFACE = re.compile(r'\binterface\s+([a-zA-Z0-9_]+)', re.MULTILINE)

    def parse(self, content, path):
        return (
            self._extract(self.RE_CLASS, content, path, SymbolKind.CLASS) +
            self._extract(self.RE_INTERFACE, content, path, SymbolKind.INTERFACE)
        )