# Path: core/cortex/knowledge.py
# ------------------------------


import fnmatch
from pathlib import Path

from ...utils import is_binary_extension


class KnowledgeBase:
    """
    The Librarian of File Types (V-Ω-EXPANDED-HIERARCHICAL).
    Categorizes files and defines the boundaries of the Abyss.
    """

    ABYSS_DIRECTORIES = {
        '.git', '.svn', '.hg', '.idea', '.vscode', '.history',
        '__pycache__', 'venv', '.venv', 'env', '.env', 'site-packages',
        'dist', 'build', 'develop-eggs', 'eggs', 'parts', 'sdist', 'var', 'wheels',
        'pip-wheel-metadata', 'share', 'lib', 'libs', 'scripts', 'include',
        '.pytest_cache', '.mypy_cache', '.tox', '.nox', '.coverage', 'htmlcov',
        'node_modules', '.npm', '.yarn', '.pnpm-store', 'bower_components',
        'jspm_packages', '.next', '.nuxt', '.cache', '.parcel-cache',
        'target', 'bin', 'obj', 'out', 'output', 'cmake-build-debug', 'debug', 'release',
        'x64', 'x86', 'vendor', 'third_party',
        '.scaffold'
    }

    ABYSS_GLOBS = {
        '*.egg-info', '*.egg', '.*_cache', '.*_store', '*_venv', '*_env'
    }

    LOCKFILE_PATTERNS = {
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lockb',
        'poetry.lock', 'Pipfile.lock', 'pdm.lock', 'Gemfile.lock',
        'go.sum', 'Cargo.lock', 'composer.lock', 'mix.lock',
        'requirements.txt'
    }

    # General docs
    DOC_PATTERNS = {
        '*.md', '*.txt', '*.rst', 'LICENSE*', 'NOTICE', 'AUTHORS', 'OWNERS', 'CHANGELOG*'
    }

    # [THE FIX] Critical Root Documentation
    # Only these specific filenames at the PROJECT ROOT are critical.
    CRITICAL_DOCS = {
        'README.md', 'ARCHITECTURE.md', 'CONTRIBUTING.md', 'CONTEXT.md'
    }

    NOISE_PATTERNS = {
        '*.min.js', '*.min.css', '*.map', '*.svg', '*.ico', '*.png', '*.jpg',
        '*.jpeg', '*.gif', '*.pyc', '*.whl', '*.pdf', '*.csv', '*.tsv', '*.sql',
        '.DS_Store', 'Thumbs.db', '*.log', '*.lock', '*.sqlite', '*.db',
        'gnosis.db', 'gnosis.db-shm', 'gnosis.db-wal'
    }

    CONFIG_PATTERNS = {
        'package.json', 'pyproject.toml', 'go.mod', 'Cargo.toml',
        'tsconfig.json', '.eslintrc*', 'Dockerfile', 'docker-compose*',
        'Makefile', 'Rakefile', 'vite.config.*', 'next.config.*',
        '.gitignore', '.editorconfig', '.env.example',
        'config.py', 'settings.py', 'constants.py', 'setup.py', 'conftest.py'
    }

    @classmethod
    def categorize(cls, path: Path) -> str:
        """Adjudicates the nature of a file."""
        name = path.name

        if is_binary_extension(path):
            return 'binary'

        if name in cls.LOCKFILE_PATTERNS:
            return 'lock'

        if any(fnmatch.fnmatch(name, p) for p in cls.NOISE_PATTERNS):
            return 'noise'

        if any(fnmatch.fnmatch(name, p) for p in cls.CONFIG_PATTERNS):
            return 'config'

        # [THE FIX] Precise Documentation Hierarchy
        # 1. Critical Root Docs
        # We assume the path passed here is relative to project root or is just a filename if unknown
        if name in cls.CRITICAL_DOCS:
            # Ideally we check depth, but name check is strong enough for categorization
            return 'doc_critical'

        # 2. General Docs
        if any(fnmatch.fnmatch(name, p) for p in cls.DOC_PATTERNS) or path.suffix == '.rst':
            return 'doc'

        return 'code'

