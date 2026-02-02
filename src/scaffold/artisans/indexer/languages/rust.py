import re
from .base import BaseLanguageParser
from ....core.cortex.contracts import SymbolKind

class RustParser(BaseLanguageParser):
    RE_FN = re.compile(r'\bfn\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_STRUCT = re.compile(r'\bstruct\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    RE_TRAIT = re.compile(r'\btrait\s+([a-zA-Z0-9_]+)', re.MULTILINE)

    def parse(self, content, path):
        return (
            self._extract(self.RE_FN, content, path, SymbolKind.FUNCTION) +
            self._extract(self.RE_STRUCT, content, path, SymbolKind.CLASS) +
            self._extract(self.RE_TRAIT, content, path, SymbolKind.INTERFACE)
        )