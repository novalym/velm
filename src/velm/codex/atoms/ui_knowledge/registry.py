import re
from typing import Callable, Dict, List, Tuple

# Type definition for a Component Generator
# Accepts: (name: str, props: List[Tuple[name, type]]) -> str (Source Code)
ComponentGenerator = Callable[[str, List[Tuple[str, str]]], str]

class ComponentRegistry:
    _library: Dict[str, ComponentGenerator] = {}

    @classmethod
    def register(cls, key: str):
        """Decorator to enshrine a component in the library."""
        def decorator(func: ComponentGenerator):
            cls._library[key.lower()] = func
            return func
        return decorator

    @classmethod
    def get_generator(cls, name: str) -> ComponentGenerator:
        """Retrieves the generator, or None if the name is unknown."""
        # Attempt 1: Exact/Lower match
        if name.lower() in cls._library:
            return cls._library[name.lower()]

        # Attempt 2: PascalCase to kebab-case (e.g. DropdownMenu -> dropdown-menu)
        kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
        if kebab in cls._library:
            return cls._library[kebab]

        return None

    @classmethod
    def list_keys(cls) -> List[str]:
        return sorted(list(cls._library.keys()))