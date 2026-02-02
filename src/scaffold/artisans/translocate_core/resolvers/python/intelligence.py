# // scaffold/artisans/translocate_core/resolvers/python/intelligence.py
# ----------------------------------------------------------------------

import sys
from functools import lru_cache


class PythonIntelligence:
    """
    The Oracle of the Python Ecosystem.
    Distinguishes between Divine Law (Stdlib), Foreign Powers (3rd Party), and Local Reality.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_stdlib_modules() -> set[str]:
        """Returns the immutable set of standard library modules."""
        if sys.version_info >= (3, 10):
            return sys.stdlib_module_names

        # Fallback for older Pythons
        stdlib = set(sys.builtin_module_names)
        stdlib.update({
            'os', 'sys', 're', 'json', 'pathlib', 'typing', 'datetime',
            'time', 'math', 'shutil', 'subprocess', 'ast', 'logging'
        })
        return stdlib

    @classmethod
    def is_stdlib(cls, module_name: str) -> bool:
        """
        Adjudicates if a module belongs to the Standard Library.
        Handles submodules (e.g. 'os.path' -> 'os').
        """
        if not module_name: return False
        root = module_name.split('.')[0]
        return root in cls.get_stdlib_modules()

    @classmethod
    def is_known_third_party(cls, module_name: str) -> bool:
        """
        Prophecy: In the future, this will check the active venv.
        For now, it returns False to force local resolution attempts,
        which will fail gracefully if the file isn't found locally.
        """
        return False