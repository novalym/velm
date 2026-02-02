# Path: core/artisans/analyze/divination/grammar.py
# --------------------------------------------

import re
import sys
import os
from pathlib import Path
from typing import Optional

# [ASCENSION 11]: PRE-COMPILED PATTERNS
SHEBANG_PATTERN = re.compile(r'^#!.*(?:/bin/|/env\s+)(\w+)')
SCAFFOLD_SIGIL = re.compile(r'^\s*(\$\$|::|<<|@include|@if|%%)', re.MULTILINE)
SYMPHONY_SIGIL = re.compile(r'^\s*(\>\>|\?\?|!!)', re.MULTILINE)


class GrammarOracle:
    """
    =============================================================================
    == THE POLYGLOT ORACLE (V-Ω-LINGUISTIC-TRUTH-ILLUMINATED)                 ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: LANGUAGE_DIVINER

    Determines the tongue of a scripture using a multi-layered heuristic engine:
    1.  **Extension:** The most common identifier.
    2.  **Filename:** Specific files (Dockerfile).
    3.  **Shebang:** The first line execution directive.
    4.  **Sigils:** Gnostic markers for Scaffold/Symphony.
    5.  **Heuristics:** Keyword density analysis.
    """

    # [ASCENSION 4]: THE EXPANDED GRIMOIRE
    EXTENSION_MAP = {
        # Gnostic
        '.scaffold': 'scaffold',
        '.symphony': 'symphony',
        '.arch': 'arch',
        # Web
        '.js': 'javascript', '.jsx': 'javascript', '.mjs': 'javascript', '.cjs': 'javascript',
        '.ts': 'typescript', '.tsx': 'typescript',
        '.html': 'html', '.htm': 'html',
        '.css': 'css', '.scss': 'scss', '.less': 'less',
        '.json': 'json', '.jsonc': 'json',
        # Systems
        '.py': 'python', '.pyw': 'python',
        '.rs': 'rust',
        '.go': 'go',
        '.c': 'c', '.h': 'c',
        '.cpp': 'cpp', '.hpp': 'cpp', '.cc': 'cpp',
        '.java': 'java',
        '.cs': 'csharp',
        # Shell/Config
        '.sh': 'shell', '.bash': 'shell', '.zsh': 'shell',
        '.yaml': 'yaml', '.yml': 'yaml',
        '.toml': 'toml', '.ini': 'ini',
        '.md': 'markdown', '.txt': 'text',
        '.sql': 'sql',
        '.xml': 'xml',
        '.rb': 'ruby',
        '.php': 'php',
        '.lua': 'lua'
    }

    FILENAME_MAP = {
        'dockerfile': 'dockerfile',
        'makefile': 'makefile',
        'jenkinsfile': 'groovy',
        'vagrantfile': 'ruby',
        'gemfile': 'ruby',
        'rakefile': 'ruby',
        'cmakelists.txt': 'cmake',
        'nginx.conf': 'nginx'
    }

    @staticmethod
    def divine(file_path: str, content: Optional[str] = None, trace_id: str = "oracle") -> str:
        """
        The Rite of Divination.
        """
        # [ASCENSION 2]: NULL SAFETY
        if not file_path:
            return "unknown"

        # [ASCENSION 11]: PATH CANONIZATION
        path_obj = Path(file_path)
        filename = path_obj.name.lower()
        suffix = path_obj.suffix.lower()

        # [ASCENSION 1]: FORENSIC LOGGING START
        # sys.stderr.write(f"[{trace_id}] [GrammarOracle] Divining: {filename}\n")

        # 1. SPECIFIC FILENAME MATCH
        if filename in GrammarOracle.FILENAME_MAP:
            grammar = GrammarOracle.FILENAME_MAP[filename]
            # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> Match (Filename): {grammar}\n")
            return grammar

        # Special case for Dockerfile extensions (e.g., Dockerfile.dev)
        if 'dockerfile' in filename:
            return 'dockerfile'

        # 2. EXTENSION MATCH
        if suffix in GrammarOracle.EXTENSION_MAP:
            grammar = GrammarOracle.EXTENSION_MAP[suffix]
            # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> Match (Extension): {grammar}\n")
            return grammar

        # If content is missing, we can go no further.
        if not content:
            return "unknown"

        # [ASCENSION 12]: BINARY RESISTANCE (Safe Slicing)
        header = content[:1024]

        # 3. SHEBANG DIVINATION
        shebang_match = SHEBANG_PATTERN.match(header)
        if shebang_match:
            interpreter = shebang_match.group(1).lower()
            if 'python' in interpreter: return 'python'
            if 'node' in interpreter: return 'javascript'
            if 'bash' in interpreter or 'sh' in interpreter: return 'shell'
            if 'ruby' in interpreter: return 'ruby'
            if 'perl' in interpreter: return 'perl'
            # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> Match (Shebang): {interpreter}\n")

        # 4. GNOSTIC SIGIL SCAN
        # Check for Scaffold ($$)
        if SCAFFOLD_SIGIL.search(header):
            # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> Match (Sigil): scaffold\n")
            return "scaffold"

        # Check for Symphony (>>)
        if SYMPHONY_SIGIL.search(header):
            # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> Match (Sigil): symphony\n")
            return "symphony"

        # 5. [ASCENSION 7]: HEURISTIC FALLBACK
        # Simple keyword checks for extensionless files
        if "def " in header and "import " in header: return "python"
        if "function " in header and "var " in header: return "javascript"
        if "package " in header and "func " in header: return "go"
        if "fn " in header and "let " in header: return "rust"
        if "<html>" in header.lower(): return "html"

        # sys.stderr.write(f"[{trace_id}] [GrammarOracle]    -> No Match. Verdict: unknown\n")
        return "unknown"