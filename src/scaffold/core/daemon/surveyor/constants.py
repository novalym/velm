# Path: core/daemon/surveyor/constants.py
# ---------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_SURVEYOR_LAWS_V12

"""
The Immutable Laws of the Grand Survey.
Defines the boundaries of the Gaze and the signatures of Heresy.
"""

# The Abyss: Paths we never gaze into to preserve sanity.
IGNORE_PATTERNS = {
    '.git', '.svn', '.hg',
    'node_modules', 'bower_components', 'jspm_packages',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'venv', '.venv', 'env', '.env',
    'dist', 'build', 'out', 'target', 'bin', 'obj', 'lib',
    'coverage', '.idea', '.vscode', '.vs', '.gradle',
    '*.min.js', '*.map', '*.lock', '*.log', '*.sqlite', '*.db',
    '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico',
    '*.pyc', '*.class', '*.dll', '*.exe', '*.so', '*.dylib'
}

# The Grimoire: File extensions mapped to Sentinel designations.
EXTENSION_MAP = {
    # The Gnostic Tongues
    '.scaffold': 'SCAFFOLD',
    '.arch': 'SCAFFOLD',
    '.symphony': 'SYMPHONY',

    # The Mortal Tongues
    '.py': 'PYTHON',
    '.pyw': 'PYTHON',

    '.js': 'JAVASCRIPT',
    '.jsx': 'JAVASCRIPT',
    '.mjs': 'JAVASCRIPT',
    '.cjs': 'JAVASCRIPT',

    '.ts': 'TYPESCRIPT',  # Specialized TS Sentinel
    '.tsx': 'TYPESCRIPT',

    '.rs': 'RUST',

    '.go': 'GOLANG',

    '.java': 'JAVA',

    '.c': 'CPP',  # C/C++ share a sentinel for now
    '.cpp': 'CPP',
    '.h': 'CPP',
    '.hpp': 'CPP',

    # The Infrastructure
    'Dockerfile': 'INFRA',
    'docker-compose.yml': 'INFRA',
    'docker-compose.yaml': 'INFRA',
    '.env.example': 'CONFIG',
    'package.json': 'CONFIG',
    'Cargo.toml': 'CONFIG',
    'pyproject.toml': 'CONFIG',
    'pom.xml': 'CONFIG'
}

# Severity Levels (LSP Standard)
SEVERITY_ERROR = 1  # Critical failure / Security risk
SEVERITY_WARNING = 2  # Anti-pattern / Potential bug
SEVERITY_INFO = 3  # Stylistic drift / Complexity
SEVERITY_HINT = 4  # Debt marker / TODO

# Diagnostic Codes
CODE_SYNTAX = "SYNTAX_HERESY"
CODE_STYLE = "AESTHETIC_DRIFT"
CODE_SECURITY = "SECURITY_BREACH"
CODE_DEBT = "TECHNICAL_DEBT"
CODE_BEST_PRACTICE = "ANTI_PATTERN"
CODE_PERFORMANCE = "PERFORMANCE_DRAG"
CODE_TYPE_SAFETY = "TYPE_HERESY"

