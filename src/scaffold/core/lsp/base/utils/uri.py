# Path: core/lsp/base/utils/uri.py
# --------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_URI_OMNI_SOLVENT_V9000_MATH_CERTAINTY
# SYSTEM: IRON_CORE | ROLE: PATH_PHYSICS_ENGINE
# =================================================================================

import os
import re
import sys
import urllib.parse
import unicodedata
import hashlib
from functools import lru_cache
from pathlib import Path, PureWindowsPath, PurePosixPath
from typing import Union, Any, Optional

# =================================================================================
# == I. THE GRIMOIRE OF PATTERNS (REGEX PHYSICS)                                 ==
# =================================================================================

# [ASCENSION 1]: GREEDY SCHEME ANNIHILATOR
# Matches file://, vscode-vfs://, etc., but also catches malformed double-schemes.
SCHEME_PATTERN = re.compile(r'^([a-zA-Z][a-zA-Z0-9+.-]+:/{1,4})+', re.IGNORECASE)

# [ASCENSION 2]: DRIVE LETTER SINGULARITY
# Captures Windows drives (c:, C:, /c:) with absolute precision.
WINDOWS_DRIVE_PATTERN = re.compile(r'^/?([a-zA-Z]):')

# [ASCENSION 3]: ARTIFACT EXORCIST
# Matches trailing garbage commonly left by Python's ast.literal_eval or f-strings.
# Quotes (' "), dots (.), whitespace, and null bytes.
ARTIFACT_TAIL_PATTERN = re.compile(r'[\'"\.\s\x00]+$')


class UriUtils:
    """
    =============================================================================
    == THE OMNI-SOLVENT (V-Ω-MATHEMATICAL-CERTAINTY-V9000)                     ==
    =============================================================================
    The final authority on location in the Gnostic Cosmos.

    [THE 12 LEGENDARY ASCENSIONS]:
    1.  **Quantum Decoding Loop:** Recursively unquotes URIs until they reach a stable state
        to handle double/triple encoded entities (%2520 -> %20 -> ' ').
    2.  **Fractal Collapse Algorithm:** Mathematically detects and collapses recursive
        path duplication (e.g. `Root/A/B/Root/A/B` -> `Root/A/B`).
    3.  **Artifact Annihilation:** Aggressively strips trailing parsing shrapnel (`'`, `"`, `.`).
    4.  **Drive Letter Normalization:** Forces all Windows drive letters to lowercase `c:`
        to ensure hash-map stability.
    5.  **Scheme Decapitation:** Removes all protocols (`file://`) to expose raw matter.
    6.  **Slash Unification:** Enforces POSIX forward-slashes `/` universally.
    7.  **Absolute Anchor Logic:** Distinguishes between "Relative" paths and "Malformed Absolute"
        paths to prevent incorrect CWD prepending.
    8.  **Home Expansion:** Resolves `~` to the user's home directory.
    9.  **Unicode Normalization (NFC):** Prevents MacOS decomposed character schisms.
    10. **Idempotency Guard:** `to_fs_path(Path object)` returns instantly.
    11. **Merkle Hashing:** Generates stable, collision-resistant keys for map lookups.
    12. **Root Topology Check:** `is_child_of` uses strict path math, not string prefixing.
    """

    @staticmethod
    def to_fs_path(uri: Union[str, Path, Any]) -> Path:
        """
        [THE RITE OF MATERIALIZATION]
        Transmutes any Gnostic representation into a Physical Path.
        """
        # 1. UNWRAP & TYPE CHECK
        if isinstance(uri, Path):
            return uri.resolve()

        raw_str = UriUtils._unwrap(uri)
        if not raw_str or raw_str == '.':
            return Path.cwd().resolve()

        # 2. THE ALCHEMICAL TRANSFORMATION
        clean_str = UriUtils._transform_uri_to_path_string(raw_str)

        # 3. [THE CURE]: RECURSIVE DUPLICATION COLLAPSE
        clean_str = UriUtils._fractal_collapse(clean_str)

        # 4. OS-LEVEL RESOLUTION
        p = Path(clean_str)
        try:
            # If it exists, resolve it to get the true casing/path
            if p.exists():
                return p.resolve()

            # If it looks absolute, trust it.
            if p.is_absolute():
                return p

            # Windows Check: If it starts with a drive letter, it IS absolute
            if os.name == 'nt' and WINDOWS_DRIVE_PATTERN.match(clean_str):
                return p

            # If strictly relative, anchor to CWD
            return p.resolve()

        except OSError:
            return p.absolute()

    @staticmethod
    def to_uri(path: Union[str, Path, Any]) -> str:
        """
        [THE RITE OF ASCENSION]
        Transmutes physical matter into a Celestial URI (file://...).
        """
        # If it's already a URI, clean it and return
        if isinstance(path, str) and path.startswith('file:'):
            return UriUtils.normalize_uri(path)

        path_obj = UriUtils.to_fs_path(path)
        try:
            return path_obj.as_uri()
        except ValueError:
            return f"file:///{path_obj.as_posix().lstrip('/')}"

    @staticmethod
    def normalize_uri(uri: Union[str, Any]) -> str:
        """
        [THE RITE OF CANONIZATION]
        Annihilates drive letter casing entropy.
        """
        path = UriUtils.to_fs_path(uri)
        try:
            # Path.as_uri() is the standard.
            clean_uri = path.as_uri()
        except ValueError:
            clean_uri = f"file:///{path.resolve().as_posix().lstrip('/')}"

        # [THE MANDATE]: UNIFIED CASING
        # file:///C:/... -> file:///c:/...
        # This ensures that both Python and Node/Monaco see the same ID.
        if os.name == 'nt' and clean_uri.startswith('file:///'):
            # Match drive letter and colon, lowercase the letter
            return re.sub(r'^file:///([A-Z])(:)', lambda m: f"file:///{m.group(1).lower()}{m.group(2)}", clean_uri)

        return clean_uri

    @staticmethod
    @lru_cache(maxsize=4096)
    def _transform_uri_to_path_string(uri_str: str) -> str:
        """
        [THE ALCHEMICAL CORE]
        Pure string manipulation. Caching ensures O(1) speed for repeated lookups.
        """
        # 1. [ASCENSION 6]: FRAGMENT CAUTERIZATION
        if '?' in uri_str or '#' in uri_str:
            uri_str = uri_str.split('?')[0].split('#')[0]

        # 2. [ASCENSION 3]: ARTIFACT EXORCISM
        uri_str = ARTIFACT_TAIL_PATTERN.sub('', uri_str)

        # 3. [ASCENSION 1]: QUANTUM DECODING LOOP
        last_str = ""
        clean = uri_str
        loop_guard = 0
        while clean != last_str and loop_guard < 5:
            last_str = clean
            clean = urllib.parse.unquote(clean)
            loop_guard += 1

        # 4. [ASCENSION 5]: SCHEME DECAPITATION
        clean = SCHEME_PATTERN.sub('', clean)

        # 5. [ASCENSION 9]: UNICODE NORMALIZATION
        clean = unicodedata.normalize('NFC', clean)

        # 6. [ASCENSION 8]: HOME EXPANSION
        if clean.startswith('~'):
            clean = os.path.expanduser(clean)

        # 7. [ASCENSION 6]: SLASH UNIFICATION
        clean = clean.replace('\\', '/')

        # 8. [ASCENSION 4]: WINDOWS DRIVE SURGERY
        if os.name == 'nt':
            # Handle /c:/path -> c:/path
            drive_match = WINDOWS_DRIVE_PATTERN.match(clean)
            if drive_match:
                drive_letter = drive_match.group(1).lower()  # FORCE LOWER
                remainder = clean[drive_match.end():]
                clean = f"{drive_letter}:{remainder}"

        return clean

    @staticmethod
    def _fractal_collapse(path_str: str) -> str:
        """
        [ASCENSION 2]: THE FRACTAL COLLAPSE ENGINE
        Detects if a path has duplicated itself and reduces it to the singularity.
        """
        if len(path_str) < 10: return path_str

        # 1. Detect Drive Letter Duplication (Windows)
        if os.name == 'nt':
            drive_matches = list(re.finditer(r'[a-zA-Z]:', path_str, re.IGNORECASE))
            if len(drive_matches) > 1:
                # We take the LAST occurrence, as it likely precedes the actual relative path.
                last_match = drive_matches[-1]
                return path_str[last_match.start():]

        # 2. Detect General Path Duplication
        parts = path_str.split('/')
        n = len(parts)
        if n < 4: return path_str

        max_window = n // 2
        for w in range(max_window, 1, -1):
            for i in range(n - 2 * w + 1):
                chunk_a = parts[i: i + w]
                chunk_b = parts[i + w: i + 2 * w]

                if chunk_a == chunk_b:
                    # Reconstruction: Prefix + One Chunk + Suffix
                    prefix = parts[:i]
                    suffix = parts[i + w:]  # Skip the second chunk
                    return '/'.join(prefix + chunk_a + suffix)

        return path_str

    @staticmethod
    def _unwrap(obj: Any) -> str:
        """[THE UNWRAPPER] Extracts the string soul."""
        if obj is None: return ""
        if isinstance(obj, str): return obj
        if hasattr(obj, 'root'): return str(obj.root)  # Pydantic RootModel
        if isinstance(obj, Path): return str(obj)
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return obj.decode('latin-1', errors='replace')
        if hasattr(obj, 'uri'): return UriUtils._unwrap(obj.uri)
        return str(obj)

    @staticmethod
    def is_child_of(child_uri: str, parent_uri: str) -> bool:
        """[ASCENSION 12]: TOPOLOGICAL CONTAINMENT"""
        try:
            parent = UriUtils.to_fs_path(parent_uri)
            child = UriUtils.to_fs_path(child_uri)
            child.relative_to(parent)
            return True
        except ValueError:
            return False

    @staticmethod
    def relative_to(child_uri: str, parent_uri: str) -> str:
        """[ASCENSION 7]: RELATIVE ALGEBRA"""
        try:
            parent = UriUtils.to_fs_path(parent_uri)
            child = UriUtils.to_fs_path(child_uri)
            return str(child.relative_to(parent)).replace('\\', '/')
        except ValueError:
            return UriUtils._unwrap(child_uri)

    @staticmethod
    def get_extension(uri: str) -> str:
        path = UriUtils.to_fs_path(uri)
        return path.suffix.lower()

    @staticmethod
    def forge_merkle_key(uri: str) -> str:
        """[ASCENSION 11]: DETERMINISTIC FINGERPRINTING"""
        canon = UriUtils.normalize_uri(uri)
        return hashlib.blake2b(canon.encode('utf-8'), digest_size=8).hexdigest()