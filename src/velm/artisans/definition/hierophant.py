# Path: definition/artisan.py
# ---------------------------

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import DefinitionRequest
from ...help_registry import register_artisan


@register_artisan("definition")
class DefinitionArtisan(BaseArtisan[DefinitionRequest]):
    """
    =================================================================================
    == THE GNOSTIC NAVIGATOR (V-Ω-SAFE-DISPATCH)                                   ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE LINK)

    Resolves the origin of a symbol.
    - Blueprints (.scaffold): Resolves variables ($$) and file paths.
    - Code (.py, .ts): Resolves functions/classes via Ctags/Tree-sitter (Stub).
    """

    def execute(self, request: DefinitionRequest) -> ScaffoldResult:
        self.logger.info(f"Navigating to origin: {request.file_path} L{request.position['line']}")

        file_path = Path(request.file_path)
        ext = file_path.suffix.lower()

        # [THE FIX]: SAFE DISPATCH TABLE
        # We explicitly map extensions to handler methods.
        handlers = {
            '.scaffold': self._resolve_scaffold,
            '.arch': self._resolve_scaffold,
            '.symphony': self._resolve_scaffold,
            # Add other languages here as their handlers are forged
        }

        handler = handlers.get(ext)

        # [THE GUARD]: If no specialist exists, use the Fallback Gaze
        if not handler:
            self.logger.debug(f"No specialist for {ext}. Attempting generic symbol lookup.")
            return self._resolve_generic(request)

        # Execute the specialist
        try:
            return handler(request)
        except Exception as e:
            self.logger.error(f"Navigation Paradox: {e}")
            return self.failure(f"Definition lookup failed: {str(e)}")

    def _resolve_scaffold(self, request: DefinitionRequest) -> ScaffoldResult:
        """
        Resolves definitions within a Blueprint.
        1. Variables: {{ my_var }} -> $$ my_var = ...
        2. File Paths: src/main.py -> The actual file definition line.
        """
        content = request.content
        if not content:
            # Fallback to disk read if content not provided
            abs_path = (self.project_root / request.file_path).resolve()
            if abs_path.exists():
                content = abs_path.read_text(encoding='utf-8')
            else:
                return self.success("Void", data=None)

        lines = content.splitlines()
        line_idx = request.position['line']
        char_idx = request.position['character']

        if line_idx >= len(lines):
            return self.success("Void (OOB)", data=None)

        current_line = lines[line_idx]

        # --- STRATEGY A: VARIABLE LOOKUP ---
        # Check if cursor is on a variable usage {{ var }} or $var
        # Simple heuristic: grab the word under cursor
        word = self._get_word_at(current_line, char_idx)

        if word:
            # Search for definition: $$ word = ...
            # Regex for definition: ^\s*($$|let|def)\s+WORD\b
            pattern = re.compile(r'^\s*(\$\$|let|def|const)\s+' + re.escape(word) + r'\b')

            for i, line in enumerate(lines):
                if pattern.match(line):
                    return self._forge_location(request.file_path, i, 0, line)

        # --- STRATEGY B: FILE PATH LOOKUP ---
        # If the line looks like a file definition: "src/main.py ::"
        # We might want to jump to the actual file on disk if it exists?
        # Or if we are 'using' a path, jump to its definition in the tree.
        # (For V1, let's stick to variables as that is the primary use case)

        return self.success("No origin found in Blueprint.", data=None)

    def _resolve_generic(self, request: DefinitionRequest) -> ScaffoldResult:
        """
        Fallback for code files.
        In a full implementation, this would query the Cortex's Symbol Map.
        For now, it safely returns None instead of crashing.
        """
        # [FUTURE]: self.engine.cortex.lookup_symbol(word)
        return self.success("Generic lookup not yet implemented.", data=None)

    def _get_word_at(self, line: str, col: int) -> Optional[str]:
        """Extracts the identifier at the specific column."""
        if col >= len(line): return None

        # Scan back
        start = col
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] in '_-'):
            start -= 1

        # Scan forward
        end = col
        while end < len(line) and (line[end].isalnum() or line[end] in '_-'):
            end += 1

        return line[start:end]

    def _forge_location(self, uri: str, line: int, char: int, context_line: str) -> ScaffoldResult:
        """Constructs the LSP Location object."""
        return self.success(
            "Origin Found",
            data={
                "uri": f"file://{uri}" if not uri.startswith('file://') else uri,
                "range": {
                    "start": {"line": line, "character": char},
                    "end": {"line": line, "character": len(context_line)}
                }
            }
        )