# Path: scaffold/artisans/distill/core/oracle/forensics/grimoire.py
# -----------------------------------------------------------------

import re
from typing import Dict, Pattern

"""
=================================================================================
== THE GRIMOIRE OF CHAOS (V-Ω-POLYGLOT-PATTERNS)                               ==
=================================================================================
The immutable regex laws that define how different realities scream in pain.
"""

# Matches any string that looks like a file path (Windows or Unix)
# Must contain at least one slash and end in a word character.
GENERIC_PATH_REGEX = re.compile(r'(?:[a-zA-Z]:[\\/]|/|[.]{1,2}[\\/])[\w\-\s_./\\]+\.\w+')

# Language-Specific Stack Trace Patterns
STACK_PATTERNS: Dict[str, Pattern] = {
    # Python: File "src/main.py", line 10, in <module>
    "python": re.compile(r'File "(?P<path>[^"]+)", line (?P<line>\d+),'),

    # Node/JS: at Object.<anonymous> (/app/src/index.js:10:5)
    "node_nested": re.compile(r'[at] .*\((?P<path>/.+?):(?P<line>\d+):(?P<col>\d+)\)'),

    # Node/JS Simple: at /app/src/index.js:10:5
    "node_simple": re.compile(r'at\s+(?P<path>/.+?):(?P<line>\d+):(?P<col>\d+)'),

    # Go: /usr/local/go/src/runtime/panic.go:1038 +0x215
    "go": re.compile(r'\t(?P<path>/.+?):(?P<line>\d+)(?:\s+\+0x[0-9a-f]+)?$'),

    # Rust: --> src/main.rs:2:5
    "rust": re.compile(r'--> (?P<path>.+?):(?P<line>\d+):(?P<col>\d+)'),

    # Java: at com.example.App.main(App.java:10) - Weak path, strong line
    # We rely on generic path matching for Java usually, or specialized parsers later.
}

# Patterns that identify the "Head of the Hydra" (The actual error message)
ERROR_HEADERS = [
    r'^([A-Z]\w+Error: .*)$',  # Python (ValueError: ...)
    r'^(Error: .*)$',  # JS (Error: ...)
    r'^(panic: .*)$',  # Go
    r'^(error\[E\d+\]: .*)$',  # Rust
    r'(Exception: .*)$',  # Java/Generic
    r'(Fatal error: .*)$',  # PHP/Generic
    r'([A-Z][a-zA-Z]+Exception: .*)$'  # Generic Exception class names
]