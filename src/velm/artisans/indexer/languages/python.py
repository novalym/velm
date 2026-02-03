import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind


class PythonParser(BaseLanguageParser):
    RE_CLASS = re.compile(r'^class\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_FUNC = re.compile(r'^def\s+([a-zA-Z0-9_]+)', re.MULTILINE)

    def parse(self, content, path):
        return (
                self._extract(self.RE_CLASS, content, path, SymbolKind.CLASS) +
                self._extract(self.RE_FUNC, content, path, SymbolKind.FUNCTION)
        )