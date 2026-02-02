# Path: scaffold/artisans/upgrade/merger.py
# -----------------------------------------
import ast
import json
import difflib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

try:
    import toml
    import yaml
except ImportError:
    toml = None
    yaml = None


class GnosticMerger:
    """
    =============================================================================
    == THE STRUCTURAL ALCHEMIST (V-Ω-AST-AWARE-MERGE)                          ==
    =============================================================================
    Merges 'Base' (Old Template), 'Current' (User Code), and 'New' (New Template).
    Prioritizes User Innovation while injecting Upstream Evolution.
    """

    def merge_text(self, current: str, new: str, base: str = "") -> str:
        """
        The Standard Rite: 3-Way Text Merge using difflib.
        """
        # Simple fallback to new if base is missing, or overwrite if forced.
        # A true 3-way merge is complex; here we use a heuristic:
        # If Current == Base, take New.
        # If Current != Base, keep Current (User modified).
        if not base:
            return new  # No history, overwrite (or prompt in UI)

        if current.strip() == base.strip():
            return new  # User hasn't touched it, safe to update

        if current.strip() == new.strip():
            return current  # Already up to date

        # Conflict! For V1, we return Current but mark it.
        # Future: Use `diff3` logic.
        return current

    def merge_structured(self, current_path: Path, new_content: str, ext: str) -> str:
        """
        The Deep Merge Rite for JSON/TOML/YAML.
        """
        if not current_path.exists(): return new_content

        current_content = current_path.read_text(encoding='utf-8')

        try:
            curr_data = self._load_data(current_content, ext)
            new_data = self._load_data(new_content, ext)

            # Deep Merge: New keys overwrite old keys ONLY if they are structural additions.
            # User values usually take precedence.
            merged_data = self._deep_merge_dict(curr_data, new_data)

            return self._dump_data(merged_data, ext)
        except Exception:
            return new_content  # Fallback

    def _deep_merge_dict(self, user: Dict, upstream: Dict) -> Dict:
        """
        Merges Upstream (New) into User (Current).
        Logic:
        1. If key in Upstream but not User -> Add it (New Feature).
        2. If key in User and Upstream -> Keep User (User Config).
        3. If key in User but not Upstream -> Keep User (User Customization).
        """
        result = user.copy()
        for k, v in upstream.items():
            if k not in result:
                result[k] = v
            elif isinstance(v, dict) and isinstance(result[k], dict):
                result[k] = self._deep_merge_dict(result[k], v)
            # Else keep user value
        return result

    def _load_data(self, content: str, ext: str) -> Any:
        if ext == '.json': return json.loads(content)
        if ext == '.toml' and toml: return toml.loads(content)
        if ext in ('.yaml', '.yml') and yaml: return yaml.safe_load(content)
        return {}

    def _dump_data(self, data: Any, ext: str) -> str:
        if ext == '.json': return json.dumps(data, indent=2)
        if ext == '.toml' and toml: return toml.dumps(data)
        if ext in ('.yaml', '.yml') and yaml: return yaml.dump(data)
        return ""

    def merge_python_ast(self, current_path: Path, new_content: str) -> str:
        """
        The Phoenix Rite for Python.
        Merges methods and classes via AST.
        """
        if not current_path.exists(): return new_content
        current_content = current_path.read_text(encoding='utf-8')

        try:
            curr_tree = ast.parse(current_content)
            new_tree = ast.parse(new_content)

            # We build a map of top-level nodes in Current
            curr_defs = {node.name: node for node in curr_tree.body if
                         isinstance(node, (ast.FunctionDef, ast.ClassDef))}

            # We inject NEW top-level nodes from New that are missing in Current
            # We DO NOT overwrite existing nodes (User Logic Protection)
            # UNLESS they are marked as @scaffold_managed (Future feature)

            final_body = curr_tree.body[:]

            for node in new_tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if node.name not in curr_defs:
                        # Append new functionality
                        final_body.append(node)
                    # If it exists, we could try to merge inside the class (Advanced)

            # Re-synthesize (This loses comments, a known AST limitation.
            # Ideally we use LibCST, but ast.unparse is stdlib).
            # To handle comments, we might append new code to the end of file instead.

            # Simple Append Strategy for V1 Safety:
            # Find what's missing and append it.
            missing_code = []
            for node in new_tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name not in curr_defs:
                    missing_code.append(ast.unparse(node))

            if missing_code:
                return current_content + "\n\n" + "\n\n".join(missing_code) + "\n"

            return current_content

        except Exception:
            return current_content  # Safe fallback

