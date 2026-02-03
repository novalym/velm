# artisans/distill/core/assembler/content/artisans/formatter.py

import re
import math
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from .......core.cortex.contracts import FileGnosis


class Formatter:
    """
    =============================================================================
    == THE OMNISCIENT SCRIBE (V-Ω-HISTORY-MAKER-ULTIMA)                        ==
    =============================================================================
    LIF: ∞ (INFINITE GNOSIS)

    The God-Engine of Blueprint Formatting.
    It performs deep semantic analysis to produce a Luminous Scripture.
    """

    # [ELEVATION 2] The Celestial Iconography (V-Ω-EXPANDED-UNIVERSE)
    ICON_MAP = {
        # --- The Sacred Gnostic Scriptures ---
        'scaffold': '🏛️',  # The Temple: Structure, Form, Stability
        'symphony': '🎼',  # The Score: Orchestration, Will, Harmony
        'arch': '📐',  # The Plan: Pure Architecture
        'blueprint': '📜',  # The Scroll: Written Intent

        # --- The High Tongues (Systems & Backends) ---
        'python': '🐍', 'go': '🐹', 'rust': '🦀', 'ruby': '💎',
        'java': '☕', 'kotlin': '🇰', 'scala': '🔴', 'groovy': '🍸',
        'c': '🇨', 'cpp': '⚡', 'csharp': '#️⃣', 'fsharp': '🇫',
        'swift': '🐦', 'objective-c': '🍏', 'dart': '🎯',
        'elixir': '💧', 'erlang': '📞', 'haskell': 'λ', 'ocaml': '🐫',
        'nim': '👑', 'zig': '⚡', 'lua': '🌙', 'perl': '🐪',
        'r': '📉', 'julia': '🟣', 'fortran': '🦖', 'cobol': '🦕',

        # --- The Web Cosmos (Frontend) ---
        'javascript': '🟨', 'typescript': '🔷', 'react': '⚛️', 'jsx': '⚛️',
        'vue': '🟩', 'svelte': '🔥', 'angular': '🅰️', 'ember': '🐹',
        'html': '🌐', 'htm': '🌐', 'haml': '🔨', 'jade': '💎',
        'css': '🎨', 'scss': '🎀', 'sass': '🎀', 'less': '➖', 'stylus': '🖌️',
        'graphql': '◈', 'wasm': '🕸️',

        # --- The Data Plane (Config & Storage) ---
        'json': '📦', 'json5': '📦', 'jsonc': '📦',
        'yaml': '⚙️', 'yml': '⚙️', 'toml': '🔧', 'ini': '🔧', 'cfg': '🔧',
        'xml': '📰', 'plist': '🍎', 'csv': '📊', 'tsv': '📊',
        'sql': '🗄️', 'db': '💽', 'sqlite': '🪶', 'postgres': '🐘', 'mysql': '🐬',
        'redis': '🔺', 'mongo': '🍃',

        # --- The DevOps Realm (Infrastructure) ---
        'docker': '🐳', 'dockerfile': '🐳', 'compose': '🐙',
        'kubernetes': '☸️', 'helm': '⎈',
        'terraform': '🏗️', 'hcl': '🏗️', 'pulumi': '🔮', 'ansible': '📜',
        'vagrant': '📦', 'packer': '📦',
        'jenkins': '🤵', 'github': '🐙', 'gitlab': '🦊', 'azure': '☁️',
        'nginx': '🟩', 'apache': '🪶',

        # --- The Shell & Scripts ---
        'shell': '🐚', 'bash': '💲', 'sh': '💲', 'zsh': '٪', 'fish': '🐟',
        'powershell': '💻', 'ps1': '💻', 'bat': '🦇', 'cmd': '⌨️',
        'makefile': '🔨', 'cmake': '🛠️', 'gradle': '🐘', 'maven': '🪶',

        # --- The Textual & Documentation ---
        'markdown': '📝', 'md': '📝', 'mdx': '📝',
        'text': '📄', 'txt': '📄', 'rst': '📜', 'tex': '∫', 'latex': '∫',
        'pdf': '📕', 'log': '📋', 'lock': '🔒', 'gitignore': '🙈',

        # --- The Media & Assets ---
        'image': '🖼️', 'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'gif': '🎞️', 'svg': '✒️',
        'audio': '🔊', 'mp3': '🎵', 'wav': '🌊',
        'video': '🎬', 'mp4': '🎥', 'mov': '🎥',
        'font': '🔤', 'ttf': '🔤', 'woff': '🔤',

        # --- The Metaphysical States ---
        'binary': '💾', 'archive': '🗜️', 'zip': '🗜️', 'tar': '🗜️', 'gz': '🗜️',
        'secret': '🔑', 'key': '🗝️', 'cert': '🏵️',
        'symlink': '🔗', 'void': '⚫', 'unknown': '❓'
    }

    # [ELEVATION 6] The Heavyweights
    HEAVY_IMPORTS = {'pandas', 'numpy', 'tensorflow', 'torch', 'django', 'react-dom', 'aws-sdk', 'kubernetes'}

    def format_omitted_path(self, gnosis: FileGnosis) -> str:
        """Formats the entry for a file whose content is omitted."""
        path_str = self._normalize_path(gnosis.path)
        reason = "Low Relevance"
        if gnosis.category == 'binary': reason = "Binary Soul"
        if gnosis.category == 'lock': reason = "Lockfile"
        if gnosis.category == 'symlink': reason = "Symlink"

        meta = [
            f"Omitted: {reason}",
            f"Size: {self._human_size(gnosis.original_size)}",
            f"Score: {getattr(gnosis, 'centrality_score', 0.0):.2f}"
        ]
        return f"{path_str} # [{' | '.join(meta)}]"

    def format_blueprint_block(self, path: str, content: str, gnosis: FileGnosis) -> str:
        """
        The Atomic Formatter.
        Creates the final `path:` block with hoisted metadata and pure indented content.
        """
        # [ELEVATION 12] The Void Compressor (Inline small files)
        # We inline if small AND single line AND not empty
        if 0 < len(content) < 60 and '\n' not in content:
            safe_content = content.replace('"', '\\"')
            return f'{path} :: "{safe_content}" # [Inline Soul]\n'

        # [ELEVATION 9] Symlink Handling
        if gnosis.category == 'symlink':
            target = content.strip() if content else "???"
            return f"{path} -> {target} # [Symlink]\n"

        # [ELEVATION 8] The Binary Diviner
        if gnosis.category == 'binary':
            meta_str = self._forge_definition_meta(gnosis, content)
            return f"{path} << {path} # [Binary Soul | {meta_str}]\n"

        # --- 1. PREPARE HOISTED METADATA ---
        headers: List[Tuple[str, str]] = []

        # [ELEVATION 1] The Integrity Anchor
        if gnosis.hash_signature:
            headers.append(("@hash", f"sha256:{gnosis.hash_signature}"))

        # [ELEVATION 10] The Content Fingerprint (Visual ID)
        if content:
            content_fingerprint = hashlib.md5(content.encode()).hexdigest()[:4]
            headers.append(("@fingerprint", content_fingerprint))

        # [ELEVATION 1] The Semantic Archetype
        role = self._divine_role(path, content)
        if role:
            headers.append(("@role", role))

        # [ELEVATION 2] The Vitality Index
        vitality = self._calculate_vitality(gnosis)
        headers.append(("@vitality", vitality))

        # [ELEVATION 3] The Bus Factor Alarm
        if gnosis.author_count == 1 and gnosis.churn_score > 100:
            headers.append(("@risk", "Hero Dependency (High Churn, Single Author)"))

        # [ELEVATION 4] The Framework Diviner
        dialect = self._divine_dialect(gnosis, content)
        if dialect:
            headers.append(("@dialect", dialect))

        # [ELEVATION 7] The Security Auditor
        if "eval(" in content or "exec(" in content or "dangerouslySetInnerHTML" in content:
            headers.append(("@audit", "Unsafe Patterns Detected"))

        # [ELEVATION 5] The Tech Debt Triage
        todos = re.findall(r'TODO', content)
        fixmes = re.findall(r'FIXME', content)
        hacks = re.findall(r'HACK', content)
        if todos or fixmes or hacks:
            debt_str = []
            if fixmes: debt_str.append(f"{len(fixmes)} BROKEN")
            if hacks: debt_str.append(f"{len(hacks)} HACKS")
            if todos: debt_str.append(f"{len(todos)} TASKS")
            headers.append(("@debt", ", ".join(debt_str)))

        # [ELEVATION 6] The Import Weigher & Standard Imports
        if gnosis.imported_symbols:
            heavy = [i for i in gnosis.imported_symbols if any(h in i for h in self.HEAVY_IMPORTS)]
            if heavy:
                headers.append(("@weight", f"Heavy Dependencies: {', '.join(heavy[:3])}"))

            # Standard Imports (Truncated)
            deps = sorted(list(gnosis.imported_symbols))
            display_deps = [d.split('.')[-1] for d in deps]
            headers.append(("@imports", self._truncate_list(display_deps, 8)))

        # Metadata from Gnosis (Tags, Heresy)
        if gnosis.semantic_tags:
            heresy_tags = [t for t in gnosis.semantic_tags if "heresy" in t.lower()]
            if heresy_tags:
                headers.append(("[HERESY]", ", ".join(heresy_tags)))

        # [ELEVATION 9] The Luminous Alignment
        # Calculate max key length for alignment
        max_key_len = max([len(k) for k, v in headers]) if headers else 0

        hoisted_block = []
        for key, value in headers:
            # Format: # @key:      value
            padding = " " * (max_key_len - len(key))
            hoisted_block.append(f"# {key}:{padding} {value}")

        # --- 2. THE DEFINITION LINE (The Anchor) ---

        def_meta = self._forge_definition_meta(gnosis, content)
        header_comment = f" # [{def_meta}]" if def_meta else ""

        # [ELEVATION 6] The Skeleton Key (Void Handling)
        if not content.strip():
            return f"{path}: # [Void]\n"

        definition_line = f"{path}:{header_comment}"

        # --- 3. THE CONTENT BODY (Pure Indentation) ---

        # [ELEVATION 8] The Vertical Rhythm Enforcer
        # Normalize multiple newlines to max 2
        rhythmic_content = re.sub(r'\n{3,}', '\n\n', content.strip())

        # [ELEVATION 12] The Atomic Indenter
        indented_lines = []
        for line in rhythmic_content.splitlines():
            if line.strip():
                indented_lines.append(f"    {line}")
            else:
                indented_lines.append("")  # Preserve blank lines as-is (no trailing spaces)
        indented_content = "\n".join(indented_lines)

        # --- 4. ASSEMBLY ---
        # [ELEVATION 11] The Block Breather (Prepend newline)
        block = "\n" + "\n".join(hoisted_block + [definition_line, indented_content]) + "\n"
        return block

    def _forge_definition_meta(self, gnosis: FileGnosis, content: str) -> str:
        """Forges the lean metadata string for the definition line."""
        parts = []

        # Language & Icon
        lang = self._canonicalize_lang(gnosis.language, gnosis.path)
        icon = self._get_icon(lang, gnosis.path)

        # [ELEVATION 11] Scope detection
        scope = "Test" if "test" in gnosis.path.name.lower() or "spec" in gnosis.path.name.lower() else "Src"
        parts.append(f"{icon} {scope}/{lang}")

        if gnosis.original_size > 0:
            parts.append(self._human_size(gnosis.original_size))

        if gnosis.token_cost > 0:
            parts.append(f"{gnosis.token_cost} tk")

        if gnosis.ast_metrics:
            cc = gnosis.ast_metrics.get("cyclomatic_complexity", 0)
            if cc > 5:
                bar = self._visualize_complexity(cc)
                parts.append(f"C:{bar}({cc})")

        if gnosis.days_since_last_change is not None:
            parts.append(self._human_time(gnosis.days_since_last_change))

        return " | ".join(parts)

    def _divine_role(self, path: str, content: str) -> Optional[str]:
        """[ELEVATION 1] Infers architectural role."""
        p = path.lower()
        if "test" in p or "spec" in p: return "Adjudicator (Test)"
        if "controller" in p or "route" in p: return "Controller"
        if "model" in p or "schema" in p or "entity" in p: return "Model"
        if "view" in p or "component" in p or "ui" in p: return "View"
        if "service" in p: return "Service"
        if "util" in p or "helper" in p: return "Utility"
        if "config" in p or "setting" in p: return "Configuration"
        if "main" in p or "index" in p or "app" in p: return "Entrypoint"
        return None

    def _divine_dialect(self, gnosis: FileGnosis, content: str) -> Optional[str]:
        """[ELEVATION 4] Infers specific framework dialect."""
        c = content.lower()
        if gnosis.language == 'python':
            if "fastapi" in c: return "FastAPI"
            if "django" in c: return "Django"
            if "flask" in c: return "Flask"
        if gnosis.language in ('javascript', 'typescript', 'react'):
            if "next" in c: return "Next.js"
            if "vue" in c: return "Vue"
            if "react" in c: return "React"
        return None

    def _calculate_vitality(self, gnosis: FileGnosis) -> str:
        """Calculates the Vitality Index."""
        churn = gnosis.churn_score or 0
        cc = gnosis.ast_metrics.get("cyclomatic_complexity", 1) if gnosis.ast_metrics else 1
        age = max(1, gnosis.days_since_last_change or 1)

        # [THE FIX] The Untracked Gaze
        if gnosis.days_since_last_change == 9999:
            return "🌱 Fresh (Untracked)"

        score = (churn * cc) / age

        if score > 100: return "🔥 Volatile"
        if score > 50: return "⚡ Active"
        if age > 365: return "🗿 Ancient"
        return "🛡️ Stable"

    def _human_time(self, days: int) -> str:
        """Humanizes time deltas."""
        # [THE FIX] The Sentinel Check
        if days == 9999: return "Untracked"

        if days == 0: return "Today"
        if days == 1: return "Yesterday"
        if days < 7: return f"{days}d ago"
        if days < 30: return f"{days // 7}w ago"
        if days > 365: return f"{days // 365}y ago"
        return f"{days // 30}mo ago"

    def _canonicalize_lang(self, lang: str, path: Path) -> str:
        """[ELEVATION 10] Maps raw language keys to display names."""
        # Special check for React extensions
        if path.suffix in ('.tsx', '.jsx'):
            return "React"

        mapping = {
            'py': 'Python', 'ts': 'TypeScript', 'tsx': 'React', 'js': 'JavaScript', 'jsx': 'React',
            'rs': 'Rust', 'go': 'Go', 'rb': 'Ruby', 'md': 'Markdown', 'sh': 'Shell',
            'yml': 'YAML', 'yaml': 'YAML', 'json': 'JSON', 'toml': 'TOML'
        }
        return mapping.get(lang.lower(), lang.title()[:10])

    def _get_icon(self, lang: str, path: Path) -> str:
        """Retrieves the icon, checking specific filenames first."""
        name = path.name.lower()
        if 'dockerfile' in name: return self.ICON_MAP['dockerfile']
        if 'makefile' in name: return self.ICON_MAP['makefile']
        if 'jenkins' in name: return self.ICON_MAP['jenkins']
        if name.startswith('.env'): return self.ICON_MAP['secret']

        return self.ICON_MAP.get(lang.lower(), '📄')


    def _visualize_complexity(self, cc: int) -> str:
        score = min(5, math.ceil(cc / 5))
        return "▮" * score + "▯" * (5 - score)

    def _human_size(self, size_bytes: int) -> str:
        if size_bytes == 0: return "0B"
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 1)
        suffix = ("B", "KB", "MB", "GB", "TB")[i]
        return f"{s}{suffix}"

    def _truncate_list(self, items: List[str], limit: int) -> str:
        if len(items) <= limit:
            return ", ".join(items)
        return f"{', '.join(items[:limit])} (+{len(items) - limit})"

    def _normalize_path(self, path: Path) -> str:
        return str(path).replace('\\', '/')