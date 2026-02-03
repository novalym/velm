# Path: scaffold/artisans/distillation/oracle/consts.py
# -----------------------------------------------------

import re

DEFAULT_BUDGET = 800000
MAX_DEPTH = 2
SKELETON_COST_RATIO = 0.2

"""
=================================================================================
== THE GRIMOIRE OF PATTERNS                                                    ==
=================================================================================
Static knowledge used by the Forensic Inquisitor.
"""

# Matches paths like "src/core/main.py", "./lib/utils.js", "C:\Project\app.ts" within error logs
TRACEBACK_PATH_REGEX = re.compile(r'(?:[a-zA-Z]:[\\/]|/|[.]{1,2}[\\/])[\w\-\s_./\\]+\.\w+')

FORENSIC_PATTERNS = {
    # Python: File "src/main.py", line 10, in <module>
    "python": re.compile(r'File "(?P<path>[^"]+)", line (?P<line>\d+),'),
    # Node: at Object.<anonymous> (/app/src/index.js:10:5)
    "node": re.compile(r'[at] .*\((?P<path>/.+?):(?P<line>\d+):(?P<col>\d+)\)'),
    # Node (Alternative): at /app/src/index.js:10:5
    "node_simple": re.compile(r'at\s+(?P<path>/.+?):(?P<line>\d+):(?P<col>\d+)'),
    # Go: /usr/local/go/src/runtime/panic.go:1038 +0x215
    "go": re.compile(r'\t(?P<path>/.+?):(?P<line>\d+)(?:\s+\+0x[0-9a-f]+)?$'),
    # Rust: --> src/main.rs:2:5
    "rust": re.compile(r'--> (?P<path>.+?):(?P<line>\d+):(?P<col>\d+)'),
    # Generic Fallback: path/to/file.ext:10
    "generic": re.compile(r'(?P<path>(?:[a-zA-Z]:[\\/]|/|[.]{0,2}[\\/])[\w\-\s_./\\]+\.\w+):(?P<line>\d+)')
}

# Patterns for lines that contain the core error message (The Signal)
ERROR_MESSAGE_PATTERNS = [
    r'^([A-Z]\w+Error: .*)$',  # Python: ValueError: ...
    r'^(Error: .*)$',          # Node: Error: ...
    r'^(panic: .*)$',          # Go: panic: ...
    r'^(error\[E\d+\]: .*)$'   # Rust: error[E0425]: ...
]

# Directories that are considered noise in a stack trace
NOISE_DIRS = {
    'node_modules', 'site-packages', 'venv', '.venv', 'dist', 'build',
    'vendor', 'gems', 'anaconda', 'miniconda', 'usr/lib'
}