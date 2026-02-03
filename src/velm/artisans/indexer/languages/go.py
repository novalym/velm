import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind

class GoParser(BaseLanguageParser):
    RE_FUNC = re.compile(r'^func\s+([a-zA-Z0-9_]+)\(', re.MULTILINE)
    RE_TYPE = re.compile(r'^type\s+([a-zA-Z0-9_]+)\s+(?:struct|interface)', re.MULTILINE)

    def parse(self, content, path):
        return (
            self._extract(self.RE_FUNC, content, path, SymbolKind.FUNCTION) +
            self._extract(self.RE_TYPE, content, path, SymbolKind.CLASS)
        )