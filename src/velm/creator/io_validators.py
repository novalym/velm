"""
=================================================================================
== THE SACRED SANCTUM OF THE SYNTAX INQUISITOR (V-Ω-JUDGE)                     ==
=================================================================================
This new, divine artisan is the Conscience of the I/O Trinity. It is a stateless
judge that adjudicates the structural purity of a scripture's soul *before* it is
made manifest, preventing the heresy of a broken configuration file from ever
profaning the mortal realm of the filesystem.
=================================================================================
"""
import ast
import json
from typing import Tuple, Optional

# Lazy-load heavy dependencies for hyper-performance
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


class SyntaxInquisitor:
    """
    The Guardian of Law. A stateless artisan that judges the purity of content.
    """

    @staticmethod
    def adjudicate(content: str, extension: str) -> Tuple[bool, Optional[str]]:
        """
        Performs a syntax check based on file extension.
        Returns (is_pure, error_message).
        """
        if not content.strip():
            return True, None # The void is pure.

        ext = extension.lower()

        if ext == '.json':
            return SyntaxInquisitor._check_json(content)
        elif ext in ('.yml', '.yaml'):
            return SyntaxInquisitor._check_yaml(content)
        elif ext == '.toml':
            return SyntaxInquisitor._check_toml(content)
        elif ext == '.py':
            return SyntaxInquisitor._check_python(content)

        return True, None # The Gaze is averted for unknown tongues.

    @staticmethod
    def _check_json(content: str) -> Tuple[bool, Optional[str]]:
        try:
            json.loads(content)
            return True, None
        except json.JSONDecodeError as e:
            return False, f"JSON Heresy: {e}"

    @staticmethod
    def _check_yaml(content: str) -> Tuple[bool, Optional[str]]:
        if not YAML_AVAILABLE:
            return True, "YAML Gaze averted: The 'PyYAML' artisan is not manifest."
        try:
            yaml.safe_load(content)
            return True, None
        except yaml.YAMLError as e:
            return False, f"YAML Heresy: {e}"

    @staticmethod
    def _check_toml(content: str) -> Tuple[bool, Optional[str]]:
        if not TOML_AVAILABLE:
            return True, "TOML Gaze averted: The 'toml' artisan is not manifest."
        try:
            toml.loads(content)
            return True, None
        except toml.TomlDecodeError as e:
            return False, f"TOML Heresy: {e}"

    @staticmethod
    def _check_python(content: str) -> Tuple[bool, Optional[str]]:
        try:
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, f"Python Syntax Heresy on line {e.lineno}: {e.msg}"