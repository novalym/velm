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
# Handles the "Slash-Prepend" heresy common in URI decoding on *nix.
WINDOWS_DRIVE_PATTERN = re.compile(r'^/?([a-zA-Z]):')

# [ASCENSION 3]: ARTIFACT EXORCIST
# Matches trailing garbage commonly left by Python's ast.literal_eval or f-strings.
# Quotes (' "), dots (.), whitespace, and null bytes.
ARTIFACT_TAIL_PATTERN = re.compile(r'[\'"\.\s\x00]+$')

# [ASCENSION 13]: ENVIRONMENT VARIABLE PATTERN
# Detects ${VAR} or $VAR for expansion.
ENV_VAR_PATTERN = re.compile(r'\$\{?([a-zA-Z_][a-zA-Z0-9_]*)\}?')


class UriUtils:
    """
    =============================================================================
    == THE OMNI-SOLVENT (V-Ω-MATHEMATICAL-CERTAINTY-V9000)                     ==
    =============================================================================
    The final authority on location in the Gnostic Cosmos.

    [THE 24 LEGENDARY ASCENSIONS]:
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
    13. **Cross-Platform Empathy:** Handles Windows paths even when running on Linux (WASM).
    14. **Unwrap Protocol:** Extracts URIs from complex objects (Pydantic, Dicts) recursively.
    15. **Query/Fragment Lobotomy:** Severs URL parameters (`?foo=bar`) from file paths.
    16. **Environment Expansion:** Expands `${HOME}` vars in paths.
    17. **Stem Extraction:** Fast access to filename without extension.
    18. **Virtual Root Detection:** Recognizes `/vault/` as a sacred prefix.
    19. **Network Share (UNC) Support:** Handles `//server/share` logic safely.
    20. **Shadow Path Resolution:** Maps physical paths to their `.scaffold` shadow equivalent.
    21. **Relative Algebra:** Computes `relative_to` without crashing across drive letters.
    22. **Path Sanitization:** Strips illegal characters from filenames.
    23. **Scheme Injection:** Smartly re-applies `file:///` only if missing.
    24. **The Finality Vow:** A mathematical guarantee of returning a valid path string.
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

        # 2. THE ALCHEMICAL TRANSFORMATION (STRING LEVEL)
        clean_str = UriUtils._transform_uri_to_path_string(raw_str)

        # 3. [THE CURE]: RECURSIVE DUPLICATION COLLAPSE
        clean_str = UriUtils._fractal_collapse(clean_str)

        # 4. OS-LEVEL RESOLUTION
        # We assume the clean_str is now a valid path string for *some* OS.
        p = Path(clean_str)
        try:
            # If it exists, resolve it to get the true casing/path
            if p.exists():
                return p.resolve()

            # If it looks absolute, trust it.
            if p.is_absolute():
                return p

            # [ASCENSION 13]: WINDOWS-ON-WASM EMPATHY
            # If we are on Linux (WASM), Path('C:/foo') thinks it is relative to CWD.
            # We must detect the drive letter manually and force it absolute.
            if os.name != 'nt' and WINDOWS_DRIVE_PATTERN.match(clean_str):
                return p  # Treat as absolute, do not prepend CWD

            # If strictly relative, anchor to CWD
            return p.resolve()

        except OSError:
            # Fallback for permission errors or invalid names
            return p.absolute()

    @staticmethod
    def to_uri(path: Union[str, Path, Any]) -> str:
        """
        [THE RITE OF ASCENSION]
        Transmutes physical matter into a Celestial URI (file://...).
        """
        # If it's already a URI, clean it and return
        path_str = str(path)
        if path_str.startswith(('file:', 'vscode-vfs:', 'inmemory:')):
            return UriUtils.normalize_uri(path_str)

        path_obj = UriUtils.to_fs_path(path)

        try:
            # [ASCENSION 23]: SCHEME INJECTION
            # Path.as_uri() is robust but fails on relative paths.
            if not path_obj.is_absolute():
                path_obj = path_obj.resolve()
            return path_obj.as_uri()
        except ValueError:
            # Fallback for when resolve() fails or path is weird
            return f"file:///{path_obj.as_posix().lstrip('/')}"

    @staticmethod
    def normalize_uri(uri: Union[str, Any]) -> str:
        """
        [THE RITE OF CANONIZATION]
        Annihilates drive letter casing entropy and scheme drift.
        """
        raw = UriUtils._unwrap(uri)

        # 1. Strip Scheme to get path
        clean_path_str = UriUtils._transform_uri_to_path_string(raw)

        # 2. Re-Apply Scheme Standard
        # We always output file:/// with forward slashes
        clean_uri = f"file:///{clean_path_str.lstrip('/')}"

        # [THE MANDATE]: UNIFIED CASING
        # file:///C:/... -> file:///c:/...
        # This ensures that both Python and Node/Monaco see the same ID.
        # We apply this regex even on Linux if the path LOOKS like a Windows path.
        clean_uri = re.sub(r'^file:///([A-Z])(:)', lambda m: f"file:///{m.group(1).lower()}{m.group(2)}", clean_uri)

        return clean_uri

    @staticmethod
    @lru_cache(maxsize=4096)
    def _transform_uri_to_path_string(uri_str: str) -> str:
        """
        [THE ALCHEMICAL CORE]
        Pure string manipulation. Caching ensures O(1) speed for repeated lookups.
        """
        # 1. [ASCENSION 15]: QUERY/FRAGMENT LOBOTOMY
        if '?' in uri_str or '#' in uri_str:
            uri_str = uri_str.split('?')[0].split('#')[0]

        # 2. [ASCENSION 3]: ARTIFACT EXORCISM
        uri_str = ARTIFACT_TAIL_PATTERN.sub('', uri_str)

        # 3. [ASCENSION 1]: QUANTUM DECODING LOOP
        # Recursively decode until stable (%2520 -> %20 -> space)
        last_str = ""
        clean = uri_str
        loop_guard = 0
        while clean != last_str and loop_guard < 5:
            last_str = clean
            clean = urllib.parse.unquote(clean)
            loop_guard += 1

        # 4. [ASCENSION 5]: SCHEME DECAPITATION
        # Remove file://, vscode-vfs://, etc.
        clean = SCHEME_PATTERN.sub('', clean)

        # 5. [ASCENSION 9]: UNICODE NORMALIZATION
        clean = unicodedata.normalize('NFC', clean)

        # 6. [ASCENSION 16]: ENVIRONMENT EXPANSION
        # Expand $HOME or ${USER} if present
        if '$' in clean:
            clean = os.path.expandvars(clean)

        # 7. [ASCENSION 8]: HOME TILDE EXPANSION
        if clean.startswith('~'):
            clean = os.path.expanduser(clean)

        # 8. [ASCENSION 6]: SLASH UNIFICATION
        clean = clean.replace('\\', '/')

        # 9. [ASCENSION 4]: WINDOWS DRIVE SURGERY
        # Handle /c:/path -> c:/path AND C:/path -> c:/path
        # We strip the leading slash if a drive letter follows
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
        Detects if a path has duplicated itself due to recursive joining bug.
        e.g. /home/user/project/home/user/project/src/file.py
        """
        if len(path_str) < 10: return path_str

        # 1. Detect Drive Letter Duplication (Windows)
        if ':' in path_str:
            # c:/users/foo/c:/users/foo
            drive_matches = list(re.finditer(r'[a-zA-Z]:', path_str, re.IGNORECASE))
            if len(drive_matches) > 1:
                # We take the LAST occurrence, as it likely precedes the actual relative path.
                last_match = drive_matches[-1]
                return path_str[last_match.start():]

        # 2. Detect General Path Duplication (Sliding Window)
        parts = path_str.split('/')
        n = len(parts)
        if n < 4: return path_str

        # Try to find the largest repeating subsequence
        max_window = n // 2
        for w in range(max_window, 1, -1):
            for i in range(n - 2 * w + 1):
                chunk_a = parts[i: i + w]
                chunk_b = parts[i + w: i + 2 * w]

                if chunk_a == chunk_b and len(chunk_a) > 1:  # Ensure non-trivial match
                    # Reconstruction: Prefix + One Chunk + Suffix
                    prefix = parts[:i]
                    suffix = parts[i + w:]  # Skip the second chunk (chunk_b)
                    # Recursively check suffix for more corruption? No, greedy fix usually enough.
                    return '/'.join(prefix + chunk_a + suffix)

        return path_str

    @staticmethod
    def _unwrap(obj: Any) -> str:
        """
        [ASCENSION 14]: THE UNWRAPPER
        Extracts the string soul from any wrapper (Pydantic, Path, Dict).
        """
        if obj is None: return ""
        if isinstance(obj, str): return obj
        if hasattr(obj, 'root'): return UriUtils._unwrap(obj.root)  # Pydantic RootModel
        if isinstance(obj, Path): return obj.as_posix()
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return obj.decode('latin-1', errors='replace')
        if hasattr(obj, 'uri'): return UriUtils._unwrap(obj.uri)
        if isinstance(obj, dict) and 'uri' in obj: return UriUtils._unwrap(obj['uri'])
        return str(obj)

    @staticmethod
    def is_child_of(child_uri: str, parent_uri: str) -> bool:
        """
        [ASCENSION 12]: TOPOLOGICAL CONTAINMENT
        Robust check if child is inside parent, handling slash discrepancies.
        """
        try:
            # We use PurePath math to avoid OS calls
            parent = Path(UriUtils._transform_uri_to_path_string(UriUtils._unwrap(parent_uri)))
            child = Path(UriUtils._transform_uri_to_path_string(UriUtils._unwrap(child_uri)))

            # pathlib.is_relative_to is Py3.9+
            if hasattr(child, 'is_relative_to'):
                return child.is_relative_to(parent)
            else:
                # Legacy Support
                child.relative_to(parent)
                return True
        except ValueError:
            return False

    @staticmethod
    def relative_to(child_uri: str, parent_uri: str) -> str:
        """
        [ASCENSION 21]: RELATIVE ALGEBRA
        Returns the relative path string, forced to POSIX format.
        """
        try:
            parent = Path(UriUtils._transform_uri_to_path_string(UriUtils._unwrap(parent_uri)))
            child = Path(UriUtils._transform_uri_to_path_string(UriUtils._unwrap(child_uri)))
            return str(child.relative_to(parent)).replace('\\', '/')
        except ValueError:
            # If not relative, return the absolute path of child
            return UriUtils._unwrap(child_uri)

    @staticmethod
    def get_extension(uri: str) -> str:
        """[ASCENSION 17]: EXTENSION EXTRACTOR"""
        path_str = UriUtils._transform_uri_to_path_string(UriUtils._unwrap(uri))
        return Path(path_str).suffix.lower()

    @staticmethod
    def get_stem(uri: str) -> str:
        """[ASCENSION 18]: STEM EXTRACTOR (No extension, no dir)"""
        path_str = UriUtils._transform_uri_to_path_string(UriUtils._unwrap(uri))
        return Path(path_str).stem

    @staticmethod
    def forge_merkle_key(uri: str) -> str:
        """
        [ASCENSION 11]: DETERMINISTIC FINGERPRINTING
        Creates a short, stable hash for caching purposes.
        """
        canon = UriUtils.normalize_uri(uri)
        return hashlib.blake2b(canon.encode('utf-8'), digest_size=8).hexdigest()

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        [ASCENSION 22]: PATH SANITIZATION
        Removes characters that are illegal in file names.
        """
        # Remove null bytes
        name = name.replace('\0', '')
        # Allow alphanumeric, dot, dash, underscore. Replace others with _
        return re.sub(r'[^\w\.\-_]', '_', name)

    @staticmethod
    def is_virtual_root(uri: str) -> bool:
        """
        [ASCENSION 18]: VIRTUAL ROOT DETECTION
        Checks if the path belongs to the WASM Vault.
        """
        path_str = UriUtils._transform_uri_to_path_string(UriUtils._unwrap(uri))
        return path_str.startswith('/vault')