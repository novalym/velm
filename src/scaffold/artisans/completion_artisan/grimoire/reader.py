# Path: scaffold/artisans/completion_artisan/grimoire/reader.py
# -------------------------------------------------------------

import json
import re
import time
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional

# --- CORE UPLINKS ---
from ....logger import Scribe

Logger = Scribe("SnippetOracle")


class SnippetOracle:
    """
    =============================================================================
    == THE SNIPPET ORACLE (V-Ω-SELF-HEALING-SINGULARITY)                       ==
    =============================================================================
    LIF: INFINITY | ROLE: KNOWLEDGE_KEEPER

    A resilient engine that ingests raw .jsonc files.
    If the Gnosis is missing, it summons the 'generate_snippets.py' script
    to forge reality from nothingness.
    """

    def __init__(self):
        # Cache Structure: { language_id: (timestamp, items_list) }
        self._cache: Dict[str, tuple[float, List[Dict]]] = {}

        # Determine the physical location of the Grimoire
        self._base_dir = Path(__file__).parent
        self._snippet_dir = self._base_dir / "snippets"

        # Ensure the sanctum exists
        if not self._snippet_dir.exists():
            try:
                self._snippet_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass  # Read-only filesystem handling

    def _purify_jsonc(self, raw_content: str) -> str:
        """
        [THE PURIFICATION RITE]
        Strips C-style comments (// and /* */) while preserving strings.
        This allows us to read human-annotated JSON without 'json5' dependencies.
        """
        pattern = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'

        def replacer(match):
            s = match.group(0)
            if s.startswith('/'): return ""  # It's a comment
            return s  # It's a string

        return re.sub(pattern, replacer, raw_content, flags=re.DOTALL | re.MULTILINE)

    def _summon_forge(self):
        """
        [THE RITE OF GENESIS]
        Attempts to locate and execute 'generate_snippets.py' to restore lost knowledge.
        """
        try:
            # We look for the script relative to the package root
            # Assuming scaffold/artisans/completion_artisan/grimoire/reader.py
            # We need to go up 4 levels to find scripts/

            # Heuristic 1: Development Environment
            repo_root = self._base_dir.parents[3]
            script_path = repo_root / "scripts" / "generate_snippets.py"

            if script_path.exists():
                Logger.info("Snippet Scripture missing. Summoning the Forge...")

                # Dynamic Import and Execution
                spec = importlib.util.spec_from_file_location("snippet_forge", script_path)
                if spec and spec.loader:
                    forge_module = importlib.util.module_from_spec(spec)
                    sys.modules["snippet_forge"] = forge_module
                    spec.loader.exec_module(forge_module)

                    # Invoke the Forge Class
                    if hasattr(forge_module, "SnippetForge"):
                        forge = forge_module.SnippetForge(output_override=self._snippet_dir)
                        forge.forge_all()
                        Logger.success("Gnosis Restored via Auto-Genesis.")
                        return True

            return False
        except Exception as e:
            Logger.warn(f"Auto-Genesis Failed: {e}")
            return False

    def load(self, language: str) -> List[Dict]:
        """
        [THE RITE OF RECALL]
        Loads, parses, and caches snippets for the given tongue.
        """
        target_file = self._snippet_dir / f"{language}.jsonc"

        # 1. CHECK EXISTENCE & AUTO-HEAL
        if not target_file.exists():
            # Attempt to regenerate
            success = self._summon_forge()
            if not success and not target_file.exists():
                return []  # The Void is absolute.

        # 2. CHECK CACHE VITALITY
        try:
            current_mtime = target_file.stat().st_mtime
            if language in self._cache:
                cached_ts, cached_items = self._cache[language]
                if cached_ts == current_mtime:
                    return cached_items
        except OSError:
            pass  # File lock race condition check

        # 3. INGESTION
        try:
            raw_content = target_file.read_text(encoding='utf-8')
            clean_json = self._purify_jsonc(raw_content)
            data = json.loads(clean_json)

            items = []
            for name, snippet in data.items():
                # Normalize Prefix
                prefixes = snippet.get("prefix")
                if isinstance(prefixes, str): prefixes = [prefixes]

                # Normalize Body
                body_raw = snippet.get("body", "")
                body = body_raw if isinstance(body_raw, str) else "\n".join(body_raw)

                # Construct Completion Items
                for prefix in prefixes:
                    items.append({
                        "label": prefix,
                        "kind": 15,  # CompletionItemKind.Snippet
                        "detail": f"✨ [{language.upper()}] {name}",
                        "documentation": {
                            "kind": "markdown",
                            "value": snippet.get("description", "Gnostic Snippet")
                        },
                        "insertText": body,
                        "insertTextFormat": 2,  # Snippet Format
                        "sortText": f"00-{prefix}"  # Priority Sort
                    })

            # Update Cache
            self._cache[language] = (current_mtime, items)
            return items

        except json.JSONDecodeError as e:
            Logger.error(f"Grimoire Corruption in {language}.jsonc: {e}")
            return []
        except Exception as e:
            Logger.error(f"Oracle Blinded: {e}")
            return []


# Singleton Instance
ORACLE = SnippetOracle()