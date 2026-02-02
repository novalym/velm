# Path: scaffold/core/jurisprudence/vows/filesystem.py
# ----------------------------------------------------
import hashlib
import json
import os
import re
import stat
import time
from pathlib import Path
from typing import Tuple, Optional, Any, List

from .base import BaseVowHandler
from ....logger import Scribe

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

Logger = Scribe("FilesystemOracle")


class FilesystemVowHandlers(BaseVowHandler):
    """
    =================================================================================
    == THE ORACLE OF MATTER (V-Ω-OMNISCIENT-FS-GAZE-ASCENDED)                      ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    This artisan judges the physical reality of the Sanctum.
    """

    def _read_gnostic_content(self, path: Path) -> Optional[str]:
        """
        [THE DUAL GAZE]
        Reads content from the Virtual Buffer if applicable, otherwise from Disk.
        Returns None if reading fails (void).
        """
        # 1. Check Virtual Reality (Patch Buffer)
        if self.target_file_path and path.resolve() == self.target_file_path.resolve():
            if self.file_content_buffer is not None:
                return self.file_content_buffer

        # 2. Check Physical Reality (Disk)
        if path.exists() and path.is_file():
            try:
                return path.read_text(encoding='utf-8', errors='replace')
            except Exception:
                return None
        return None

    def _check_virtual_existence(self, path_str: str) -> bool:
        """
        [THE FACULTY OF VIRTUAL PERCEPTION]
        Checks if the file exists in the Architect's Plan (Virtual Manifest).
        """
        virtual_manifest: List[str] = getattr(
            self.context, 'generated_manifest', []
        ) or self.variables.get('generated_manifest', [])

        if not virtual_manifest:
            return False

        target_clean = path_str.replace('\\', '/').strip('/')

        if target_clean in virtual_manifest:
            return True

        for virtual_path in virtual_manifest:
            if virtual_path.endswith(target_clean):
                return True

        return False

    # =========================================================================
    # == I. THE GAZE OF ONTOLOGY (EXISTENCE & TYPE)                          ==
    # =========================================================================

    def _vow_path_exists(self, path: str) -> Tuple[bool, str]:
        """Asserts that a path (file or dir) manifests in reality or prophecy."""
        target = self._resolve(path)

        # Physical Check
        if target.exists():
            return True, f"Path '{path}' is physically manifest."

        # Virtual Check
        if self._check_virtual_existence(path):
            return True, f"Path '{path}' is virtually manifest (in the Plan)."

        return False, f"Path '{path}' is void in both Reality and Prophecy (Checked: {target})."

    def _vow_path_not_exists(self, path: str) -> Tuple[bool, str]:
        """Asserts that a path is void."""
        target = self._resolve(path)

        if target.exists():
            return False, f"Path '{path}' exists physically (Heresy). Location: {target}"

        if self._check_virtual_existence(path):
            return False, f"Path '{path}' exists virtually (Heresy)."

        return True, f"Path '{path}' is void."

    def _vow_file_exists(self, path: str) -> Tuple[bool, str]:
        """Asserts the entity is a scripture (File)."""
        target = self._resolve(path)

        if target.is_file():
            return True, f"Scripture '{path}' is physically manifest."

        if self._check_virtual_existence(path):
            return True, f"Scripture '{path}' is virtually manifest."

        return False, f"Scripture '{path}' is void. (Checked: {target})"

    # Alias for backward compatibility
    _vow_is_file = _vow_file_exists

    def _vow_dir_exists(self, path: str) -> Tuple[bool, str]:
        """Asserts the entity is a sanctum (Directory)."""
        target = self._resolve(path)
        # [THE DIAGNOSTIC FIX] Include resolved path in error message
        return (
            target.is_dir(),
            f"Sanctum '{path}' is manifest."
            if target.is_dir()
            else f"Sanctum '{path}' is missing or not a directory. (Searched: {target})"
        )

    # Alias for backward compatibility
    _vow_is_dir = _vow_dir_exists

    def _vow_is_symlink(self, path: str) -> Tuple[bool, str]:
        """Asserts the entity is a bridge (Symlink)."""
        target = self._resolve(path)
        return (
            target.is_symlink(),
            f"'{path}' is a symlink."
            if target.is_symlink()
            else f"'{path}' is solid matter."
        )

    def _vow_is_absolute_path(self, path: str) -> Tuple[bool, str]:
        """Asserts the path string provided is absolute."""
        p = Path(path)
        return (
            p.is_absolute(),
            f"'{path}' is absolute."
            if p.is_absolute()
            else f"'{path}' is relative."
        )

    # =========================================================================
    # == II. THE GAZE OF THE SOUL (TEXTUAL CONTENT)                          ==
    # =========================================================================

    def _vow_file_not_empty(self, path: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            if self._check_virtual_existence(path):
                return True, f"'{path}' is virtually manifest (assumed non-empty)."
            return False, f"'{path}' is void or unreadable."
        return len(content) > 0, f"'{path}' contains {len(content)} chars."

    def _vow_file_is_empty(self, path: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is unreadable."
        return len(content) == 0, f"'{path}' is empty."

    def _vow_file_contains(self, path: str, text: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        if text in content:
            return True, f"'{path}' contains the sacred phrase."
        return False, f"'{path}' lacks the phrase '{text}'."

    def _vow_file_not_contains(self, path: str, text: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        if text not in content:
            return True, f"'{path}' is pure of '{text}'."
        return False, f"'{path}' is tainted by '{text}'."

    def _vow_file_matches_regex(self, path: str, pattern: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        try:
            if re.search(pattern, content, re.MULTILINE):
                return True, f"'{path}' matches pattern '{pattern}'."
            return False, f"'{path}' does not match pattern '{pattern}'."
        except re.error as e:
            return False, f"Invalid Regex Heresy: {e}"

    def _vow_file_not_matches_regex(self, path: str, pattern: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        try:
            if not re.search(pattern, content, re.MULTILINE):
                return True, f"'{path}' is free of pattern '{pattern}'."
            return False, f"'{path}' is tainted by pattern '{pattern}'."
        except re.error as e:
            return False, f"Invalid Regex Heresy: {e}"

    def _vow_file_starts_with(self, path: str, text: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        return content.startswith(text), f"'{path}' starts with '{text}'."

    def _vow_file_ends_with(self, path: str, text: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, f"'{path}' is void."
        return content.strip().endswith(text), f"'{path}' ends with '{text}'."

    # =========================================================================
    # == III. THE GAZE OF STRUCTURE (JSON / YAML / TOML)                     ==
    # =========================================================================

    def _vow_is_valid_json(self, path: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, "Unreadable."
        try:
            json.loads(content)
            return True, f"'{path}' is valid JSON."
        except json.JSONDecodeError as e:
            return False, f"JSON Heresy in '{path}': {e}"

    def _vow_is_valid_yaml(self, path: str) -> Tuple[bool, str]:
        if not YAML_AVAILABLE:
            return False, "PyYAML artisan missing."
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, "Unreadable."
        try:
            yaml.safe_load(content)
            return True, f"'{path}' is valid YAML."
        except yaml.YAMLError as e:
            return False, f"YAML Heresy in '{path}': {e}"

    def _vow_is_valid_toml(self, path: str) -> Tuple[bool, str]:
        if not TOML_AVAILABLE:
            return False, "TOML artisan missing."
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, "Unreadable."
        try:
            toml.loads(content)
            return True, f"'{path}' is valid TOML."
        except Exception as e:
            return False, f"TOML Heresy in '{path}': {e}"

    def _vow_json_key_equals(self, path: str, key_path: str, expected_value: str) -> Tuple[bool, str]:
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, "Unreadable."
        try:
            data = json.loads(content)
            val = self._extract_nested_key(data, key_path)
            return str(val) == str(expected_value), f"JSON '{key_path}' == '{expected_value}'."
        except KeyError:
            return False, f"Key '{key_path}' not found in JSON."
        except Exception as e:
            return False, f"JSON Logic Paradox: {e}"

    def _vow_yaml_key_equals(self, path: str, key_path: str, expected_value: str) -> Tuple[bool, str]:
        if not YAML_AVAILABLE:
            return False, "PyYAML missing."
        content = self._read_gnostic_content(self._resolve(path))
        if content is None:
            return False, "Unreadable."
        try:
            data = yaml.safe_load(content)
            val = self._extract_nested_key(data, key_path)
            return str(val) == str(expected_value), f"YAML '{key_path}' == '{expected_value}'."
        except KeyError:
            return False, f"Key '{key_path}' not found in YAML."
        except Exception as e:
            return False, f"YAML Logic Paradox: {e}"

    def _extract_nested_key(self, data: Any, key_path: str) -> Any:
        current = data
        for part in key_path.split('.'):
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                current = current[int(part)]
            else:
                raise KeyError(f"Cannot traverse '{part}' in {type(current)}")
            if current is None:
                raise KeyError("Key is None")
        return current

    # =========================================================================
    # == IV. THE GAZE OF METADATA (PERMISSIONS & OWNERSHIP)                  ==
    # =========================================================================

    def _vow_permissions_are(self, path: str, octal: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.exists():
            return False, "Path missing."
        current = oct(target.stat().st_mode)[-3:]
        return current == octal, f"Permissions are {current}."

    def _vow_is_executable(self, path: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.exists():
            return False, "Path missing."
        return os.access(target, os.X_OK), f"'{path}' is executable."

    def _vow_is_writable(self, path: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        return os.access(target, os.W_OK), f"'{path}' is writable."

    def _vow_is_readable(self, path: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        return os.access(target, os.R_OK), f"'{path}' is readable."

    # =========================================================================
    # == V. THE GAZE OF PHYSICALITY (SIZE & CRYPTOGRAPHY)                    ==
    # =========================================================================

    def _vow_file_size_gt(self, path: str, size_kb: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_file():
            return False, "Not a file."
        try:
            limit = float(size_kb) * 1024
            actual = target.stat().st_size
            return actual > limit, f"Size {actual}B > {limit}B."
        except ValueError:
            return False, "Invalid size parameter."

    def _vow_file_size_lt(self, path: str, size_kb: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_file():
            return False, "Not a file."
        try:
            limit = float(size_kb) * 1024
            actual = target.stat().st_size
            return actual < limit, f"Size {actual}B < {limit}B."
        except ValueError:
            return False, "Invalid size parameter."

    def _vow_checksum_matches(self, path: str, algorithm: str, expected_hash: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_file():
            return False, f"'{path}' is not a file."

        try:
            algo = getattr(hashlib, algorithm.lower())
            hasher = algo()
            with open(target, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            actual_hash = hasher.hexdigest()

            if actual_hash == expected_hash:
                return True, f"{algorithm.upper()} Verified."
            return False, f"Hash Mismatch. Expected {expected_hash}, found {actual_hash}."
        except AttributeError:
            return False, f"Unknown hash algorithm: '{algorithm}'"
        except Exception as e:
            return False, f"Hashing paradox: {e}"

    # =========================================================================
    # == VI. THE GAZE OF THE CHRONOMANCER (TIME)                             ==
    # =========================================================================

    def _vow_is_newer_than(self, path_a: str, path_b: str) -> Tuple[bool, str]:
        t_a = self._resolve(path_a)
        t_b = self._resolve(path_b)
        if not t_a.exists():
            return False, f"'{path_a}' missing."
        if not t_b.exists():
            return False, f"'{path_b}' missing."

        return t_a.stat().st_mtime > t_b.stat().st_mtime, f"'{path_a}' is newer than '{path_b}'."

    def _vow_modified_within(self, path: str, seconds: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.exists():
            return False, "Path missing."
        try:
            limit = float(seconds)
            age = time.time() - target.stat().st_mtime
            return age <= limit, f"Modified {age:.1f}s ago (limit {limit}s)."
        except ValueError:
            return False, "Invalid duration."

    # =========================================================================
    # == VII. THE GAZE OF THE SANCTUM (DIRECTORY HIERARCHY)                  ==
    # =========================================================================

    def _vow_dir_is_empty(self, path: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_dir():
            return False, "Not a directory."
        is_empty = not any(target.iterdir())
        return is_empty, f"Sanctum '{path}' is empty." if is_empty else f"Sanctum '{path}' is occupied."

    def _vow_dir_not_empty(self, path: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_dir():
            return False, "Not a directory."
        has_items = any(target.iterdir())
        return has_items, f"Sanctum '{path}' is populated."

    def _vow_dir_contains_file(self, path: str, filename: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_dir():
            return False, "Not a directory."
        return (target / filename).exists(), f"Sanctum contains '{filename}'."

    def _vow_dir_contains_glob(self, path: str, pattern: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_dir():
            return False, "Not a directory."
        matches = list(target.glob(pattern))
        return bool(matches), f"Found {len(matches)} match(es) for '{pattern}' in '{path}'."

    def _vow_tree_contains_file(self, path: str, filename: str) -> Tuple[bool, str]:
        target = self._resolve(path)
        if not target.is_dir():
            return False, "Not a directory."

        try:
            next(target.rglob(filename))
            return True, f"Found '{filename}' deep within '{path}'."
        except StopIteration:
            return False, f"'{filename}' not found anywhere in '{path}' tree."