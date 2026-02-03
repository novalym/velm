import json
from typing import Any
from .base import BaseMutator, Logger
from ....contracts.heresy_contracts import ArtisanHeresy
from .textual import TextualMutator

# Lazy Loading for heavy dependencies
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import toml

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False


class StructuredMutator(BaseMutator):
    """
    =================================================================================
    == THE STRUCTURED ARCHITECT (V-Ω-DEEP-MERGE)                                   ==
    =================================================================================
    Master of JSON, YAML, and TOML.
    """

    @staticmethod
    def merge(original: str, fragment: str, ext: str) -> str:
        """[FACULTY 7] Deep merges structured data."""
        try:
            data = {}
            patch = {}

            if ext == '.json':
                # Pseudo-json5 support (strip comments)
                import re
                clean_orig = re.sub(r'//.*', '', original)
                clean_orig = re.sub(r'/\*.*?\*/', '', clean_orig, flags=re.DOTALL)
                data = json.loads(clean_orig) if clean_orig.strip() else {}
                patch = json.loads(fragment)

            elif ext in ('.yaml', '.yml'):
                if not YAML_AVAILABLE: raise ArtisanHeresy("PyYAML is required for YAML surgery.")
                data = yaml.safe_load(original) or {}
                patch = yaml.safe_load(fragment)

            elif ext == '.toml':
                if not TOML_AVAILABLE: raise ArtisanHeresy("toml is required for TOML surgery.")
                data = toml.loads(original)
                patch = toml.loads(fragment)

            else:
                # Fallback to textual append if unknown format
                return TextualMutator.append(original, fragment)

            merged = StructuredMutator._deep_merge(data, patch)

            if ext == '.json':
                return json.dumps(merged, indent=2) + "\n"
            elif ext in ('.yaml', '.yml'):
                return yaml.dump(merged, sort_keys=False)
            elif ext == '.toml':
                return toml.dumps(merged)

        except Exception as e:
            raise ArtisanHeresy(f"Structural Merge failed for {ext}: {e}")

        return original

    @staticmethod
    def _deep_merge(base: Any, update: Any) -> Any:
        """Recursive dictionary merge."""
        if isinstance(base, dict) and isinstance(update, dict):
            for k, v in update.items():
                if k in base:
                    base[k] = StructuredMutator._deep_merge(base[k], v)
                else:
                    base[k] = v
            return base
        elif isinstance(base, list) and isinstance(update, list):
            # Unique Append for primitives
            if all(isinstance(x, (str, int, float, bool)) for x in base + update):
                new_items = [item for item in update if item not in base]
                return base + new_items
            return base + update
        else:
            return update
