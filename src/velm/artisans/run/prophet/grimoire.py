# Path: scaffold/artisans/run/prophet/grimoire.py
# -----------------------------------------------

"""
=================================================================================
== THE DECLARATIVE GRIMOIRE (V-Ω-ETERNAL-KNOWLEDGE)                            ==
=================================================================================
This is the living mind of the Prophet Pantheon. It is a declarative, extensible
scripture that contains all Gnostic fingerprints for divining the soul of any
scripture or sanctum. To teach the Prophet a new language or pattern, an artisan
must only inscribe its Gnosis here.
=================================================================================
"""
from typing import Dict, List, Any

# [FACULTY 7] The Bayesian Fingerprinter's Knowledge
LANGUAGE_FINGERPRINTS: Dict[str, Dict[str, float]] = {
    "python": {r"\b(def|class|import|from)\b": 1.0, r"__init__\.py": 2.0},
    "javascript": {r"\b(function|const|let|import|=>)\b": 1.0, r"require\(": 0.8},
    "ruby": {r"\b(def|class|require|module|end)\b": 1.0},
    "go": {r"\b(package|func|import|:=)\b": 1.0},
    "rust": {r"\b(fn|struct|impl|use|let mut)\b": 1.0},
    "shell": {r"\b(echo|export|if|then|fi)\b": 0.5},
}

# Knowledge for the Sanctum Seer
SANCTUM_FINGERPRINTS: List[Dict[str, str]] = [
    {"manifest": "package.json", "rite": "npm"},
    {"manifest": "pyproject.toml", "rite": "poetry"},
    {"manifest": "requirements.txt", "rite": "python_venv"},
    {"manifest": "Cargo.toml", "rite": "cargo"},
    {"manifest": "go.mod", "rite": "go_mod"},
    {"manifest": "Makefile", "rite": "make"},
    {"manifest": "docker-compose.yml", "rite": "docker_compose"},
]

# Knowledge for the Language Oracle
SACRED_NAME_MAP: Dict[str, str] = {
    'Dockerfile': 'docker_build',
    'Makefile': 'make',
    'Procfile': 'procfile',
}

# Knowledge for the Language Oracle & Rite Adjudicator
EXTENSION_MAP: Dict[str, str] = {
    '.patch.scaffold': 'patch',
    '.scaffold': 'form',
    '.symphony': 'symphony',
    '.arch': 'arch',
    '.py': 'python',
    '.js': 'node', '.mjs': 'node', '.cjs': 'node',
    '.ts': 'ts', '.tsx': 'react', # More specific
    '.jsx': 'react',
    '.go': 'go', '.rs': 'rust', '.rb': 'ruby',
    '.sh': 'sh', '.bash': 'sh', '.zsh': 'sh',
    '.html': 'html',
}

TEST_FILE_PATTERNS: List[str] = [
    'test_*.py', '*_test.py',
    '*.test.ts', '*.spec.ts',
    '*.test.js', '*.spec.js',
]