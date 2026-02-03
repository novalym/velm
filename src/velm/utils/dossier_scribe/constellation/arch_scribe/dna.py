# Path: scaffold/utils/dossier_scribe/constellation/arch_scribe/dna.py
# --------------------------------------------------------------------

import subprocess
import re
import json
import time
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any, Tuple, Set, Optional

from .....utils import get_human_readable_size
from ..assets import GnosticAssets


class ProjectDNA:
    """
    =================================================================================
    == THE GENOME SEQUENCER (V-Ω-DEEP-ANALYSIS-ULTIMA)                             ==
    =================================================================================
    LIF: 100,000,000,000,000

    The Sentient Analyzer. It does not just count files; it reads the intent,
    history, and health of the project structure.
    """

    def __init__(self, root: Path, artifacts: List):
        self.root = root
        self.artifacts = artifacts

        # [1] The Census (File Scan)
        # We perform one heavy scan to power all analytics
        self.all_files = sorted(list(root.rglob("*")))
        self.files_only = [f for f in self.all_files if f.is_file() and not f.name.startswith('.')]
        self.dirs_only = [d for d in self.all_files if d.is_dir() and not d.name.startswith('.')]

        # --- Structural DNA ---
        self.file_count = len(self.files_only)
        self.dir_count = len(self.dirs_only)
        self.total_size = sum(f.stat().st_size for f in self.files_only)
        self.total_size_human = get_human_readable_size(self.total_size)

        # [9] The Size Categorizer
        self.project_scale = self._divine_scale()

        # --- Linguistic DNA ---
        self.extensions = Counter(f.suffix for f in self.files_only)
        self.primary_ext = self.extensions.most_common(1)[0][0] if self.extensions else ".txt"
        self.primary_language = self._map_ext_to_lang(self.primary_ext)
        self.language_emoji = GnosticAssets.ICON_MAP.get(self.primary_ext, "📄")

        # --- Framework & Dependency DNA ---
        self.frameworks = self._detect_frameworks()
        self.dependencies = self._harvest_dependencies()
        self.system_type = "Monolith" if self.dir_count > 10 else "Microservice" if self.file_count > 0 else "Seed"

        # --- [10] Git Identity ---
        self.git_branch = self._get_git_info("branch")
        self.git_commit = self._get_git_info("commit")

        # --- [4] Technical Debt ---
        self.debt_count = self._harvest_debt()

        # --- [3] Coverage Heuristic ---
        self.test_ratio = self._calculate_test_ratio()

        # --- [2] Vitality Gauge ---
        self.last_modified = self._get_latest_modification()

        # --- Navigation ---
        self.key_files = self._identify_key_files()
        self.top_level_dirs = sorted([d.name for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')])
        self.complexity_score = self.file_count / max(1, self.dir_count)

    # =========================================================================
    # == THE RITES OF PERCEPTION                                             ==
    # =========================================================================

    def _divine_scale(self) -> str:
        """[9] Classifies the project scale."""
        if self.file_count < 5: return "Nano"
        if self.file_count < 20: return "Micro"
        if self.file_count < 100: return "Standard"
        if self.file_count < 500: return "Macro"
        return "Monolithic"

    def _map_ext_to_lang(self, ext: str) -> str:
        """[6] Polyglot Mapping."""
        return {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.tsx': 'React/TS', '.jsx': 'React/JS',
            '.rs': 'Rust', '.go': 'Go', '.java': 'Java', '.cpp': 'C++', '.rb': 'Ruby', '.php': 'PHP',
            '.sh': 'Shell', '.css': 'CSS', '.html': 'HTML', '.sql': 'SQL', '.md': 'Markdown',
            '.json': 'JSON', '.toml': 'TOML', '.yaml': 'YAML', '.yml': 'YAML'
        }.get(ext, 'Generic')

    def _detect_frameworks(self) -> List[str]:
        """[5] The Framework Diviner."""
        frameworks = set()
        file_names = {f.name for f in self.all_files}

        # Signatures
        if 'manage.py' in file_names: frameworks.add("Django")
        if 'next.config.js' in file_names or 'next.config.ts' in file_names: frameworks.add("Next.js")
        if 'vite.config.ts' in file_names or 'vite.config.js' in file_names: frameworks.add("Vite")
        if 'tailwind.config.js' in file_names: frameworks.add("Tailwind CSS")
        if 'nest-cli.json' in file_names: frameworks.add("NestJS")
        if 'astro.config.mjs' in file_names: frameworks.add("Astro")
        if 'cargo.toml' in str(file_names).lower(): frameworks.add("Cargo")  # Loose match

        # Deep Scan (Manifests)
        # Check pyproject.toml content
        pyproj = self.root / "pyproject.toml"
        if pyproj.exists():
            try:
                txt = pyproj.read_text(encoding='utf-8')
                if "fastapi" in txt: frameworks.add("FastAPI")
                if "flask" in txt: frameworks.add("Flask")
                if "django" in txt: frameworks.add("Django")
                if "poetry" in txt: frameworks.add("Poetry")
            except:
                pass

        # Check package.json content
        pkg_json = self.root / "package.json"
        if pkg_json.exists():
            try:
                txt = pkg_json.read_text(encoding='utf-8')
                if '"react"' in txt: frameworks.add("React")
                if '"vue"' in txt: frameworks.add("Vue")
                if '"svelte"' in txt: frameworks.add("Svelte")
                if '"express"' in txt: frameworks.add("Express")
            except:
                pass

        return sorted(list(frameworks))

    def _harvest_dependencies(self) -> List[str]:
        """[7] The Dependency Spider."""
        deps = []

        # Python
        if (self.root / "requirements.txt").exists():
            deps.append("pip-requirements")
        if (self.root / "pyproject.toml").exists():
            deps.append("poetry/pep621")

        # Node
        if (self.root / "package.json").exists():
            deps.append("npm/yarn")

        # Rust
        if (self.root / "Cargo.toml").exists():
            deps.append("cargo")

        # Go
        if (self.root / "go.mod").exists():
            deps.append("go-modules")

        return deps

    def _harvest_debt(self) -> int:
        """[4] The Debt Collector."""
        count = 0
        # Only scan source files
        scan_exts = {'.py', '.ts', '.js', '.rs', '.go', '.java', '.cpp', '.md'}
        for f in self.files_only:
            if f.suffix in scan_exts and f.stat().st_size < 100 * 1024:  # Skip large files
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    count += len(re.findall(r'\b(TODO|FIXME|XXX|HACK)\b', content))
                except:
                    pass
        return count

    def _calculate_test_ratio(self) -> str:
        """[3] The Coverage Heuristic."""
        total_code = 0
        total_tests = 0

        for f in self.files_only:
            if f.suffix in {'.py', '.ts', '.js', '.rs', '.go'}:
                total_code += 1
                if 'test' in f.name.lower() or 'spec' in f.name.lower():
                    total_tests += 1

        if total_code == 0: return "N/A"
        ratio = (total_tests / total_code) * 100

        if ratio > 50: return f"High ({ratio:.0f}%)"
        if ratio > 20: return f"Moderate ({ratio:.0f}%)"
        if ratio > 0: return f"Low ({ratio:.0f}%)"
        return "None Detected"

    def _get_latest_modification(self) -> str:
        """[2] The Vitality Gauge."""
        if not self.files_only: return "N/A"
        try:
            latest_ts = max(f.stat().st_mtime for f in self.files_only)
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_ts))
        except:
            return "Unknown"

    def _identify_key_files(self) -> List[tuple]:
        """[8] The Entrypoint Scouter."""
        candidates = [
            ('pyproject.toml', 'Config', 'pyproject.toml'),
            ('package.json', 'Config', 'package.json'),
            ('Cargo.toml', 'Config', 'Cargo.toml'),
            ('go.mod', 'Config', 'go.mod'),
            ('Dockerfile', 'Infrastructure', 'Dockerfile'),
            ('docker-compose.yml', 'Infrastructure', 'docker-compose.yml'),
            ('main.py', 'Entrypoint', 'src/main.py'),
            ('app.py', 'Entrypoint', 'src/app.py'),
            ('index.ts', 'Entrypoint', 'src/index.ts'),
            ('index.js', 'Entrypoint', 'src/index.js'),
            ('lib.rs', 'Library Root', 'src/lib.rs'),
            ('main.rs', 'Binary Root', 'src/main.rs'),
            ('README.md', 'Documentation', 'README.md'),
            ('SECURITY.md', 'Security', 'SECURITY.md'),
            ('Makefile', 'Automation', 'Makefile'),
        ]
        found = []
        for name, kind, rel in candidates:
            if (self.root / rel).exists():
                found.append((name, kind, rel))
        return found

    def _get_git_info(self, mode: str) -> str:
        """[10] The Git Chronomancer."""
        try:
            if not (self.root / ".git").exists(): return "N/A"
            args = ['git', 'rev-parse', '--abbrev-ref', 'HEAD'] if mode == 'branch' else ['git', 'rev-parse', '--short',
                                                                                          'HEAD']
            return subprocess.check_output(args, cwd=self.root, text=True, stderr=subprocess.DEVNULL).strip()
        except:
            return "Unknown"

    def divine_directory_purpose(self, dirname: str) -> str:
        """[11] The Semantic Cartesian."""
        map = {
            'src': 'Source Code Root', 'app': 'Application Logic', 'tests': 'Test Suite',
            'docs': 'Documentation', 'scripts': 'Automation Scripts', 'tools': 'Developer Tools',
            'assets': 'Static Assets', 'config': 'Configuration Files',
            'migrations': 'Database Schema History', 'crates': 'Rust Workspace Members',
            'components': 'UI Components', 'pages': 'Route Definitions', 'utils': 'Shared Utilities',
            'lib': 'Library Code', 'bin': 'Executables', '.github': 'CI/CD Workflows',
            'pkg': 'Public Library Code (Go)', 'cmd': 'Application Entrypoints (Go)',
            'internal': 'Private Application Code (Go)'
        }
        return map.get(dirname, "Module / Domain Boundary")

    # =========================================================================
    # == THE RITE OF RECURSIVE REVELATION                                    ==
    # =========================================================================

    def generate_json_map(self) -> Dict:
        """
        [1] THE RECURSIVE SOUL MAPPER (THE FIX).
        Generates a deep, nested JSON representation of the directory structure.
        Crucial for AI context injection.
        """

        def _build_tree(dir_path: Path) -> Dict:
            tree = {
                "name": dir_path.name,
                "type": "directory",
                "children": []
            }
            try:
                # Sort for deterministic output
                for item in sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
                    # Ignore hidden files/dirs for the map
                    if item.name.startswith('.') and item.name != '.github':
                        continue
                    if item.name == '__pycache__': continue

                    if item.is_dir():
                        tree["children"].append(_build_tree(item))
                    else:
                        tree["children"].append({
                            "name": item.name,
                            "type": "file",
                            "size": item.stat().st_size
                        })
            except PermissionError:
                tree["error"] = "Access Denied"

            return tree

        return _build_tree(self.root)