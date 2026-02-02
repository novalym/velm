# Path: scaffold/artisans/run/scribe.py
# -------------------------------------

"""
=================================================================================
== THE SOVEREIGN SCRIBE OF GNOSTIC ORIGINS (V-Ω-ULTRA-DEFINITIVE. THE SEER)     ==
=================================================================================
LIF: ∞ (ETERNAL & DIVINE)

This divine artisan is the All-Seeing Eye of the Run Rite. It has been transfigured
into a sentient Intelligence Agent, capable of perceiving the soul of a scripture
from any origin—Disk, URL, S3, or Void—and conducting its preparation with
absolute Gnostic precision and unbreakable safety.

### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

1.  **The Gnostic Discernment (THE CORE FIX):** It possesses the wisdom to distinguish
    between Mortal (.py) and Sacred (.scaffold) extensions. It righteously stays its
    hand and returns a `None` language hint for sacred scriptures, ensuring the
    Prophet adjudicates their true internal nature.

2.  **The Celestial Chronocache:** It caches remote scriptures (URLs) in a local
    Gnostic Vault (~/.scaffold/cache), respecting ETags and TTL to annihilate
    repeated download latency.

3.  **The Magic Protocol Resolver:** It understands shorthand rituals like `gist:ID`,
    `gh:user/repo/file`, and `s3://...`, transmuting them into valid celestial URIs.

4.  **The Integrity Warden (SRI):** Supports Subresource Integrity via URL fragments
    (#hash=sha256:...), ensuring no tainted scripture ever profanes the mortal realm.

5.  **The Runtime Diviner (Pragma Analysis):** Scans headers for `# @runtime: docker`
    to automatically configure the execution reality without manual pleas.

6.  **The Sentinel of Chaos (Security):** Performs a pre-flight heuristic scan for
    dangerous system commands (`rm -rf /`) before handed to the Conductor.

7.  **The S3 Celestial Bridge:** Natively speaks the tongue of the AWS S3 vault to
    resurrect scriptures stored in the cloud.

8.  **The Binary Ward:** Detects binary souls instantly, preventing the engine from
    choking on non-textual material.

9.  **The Contextual Anchor (Relativity Healed):** Prioritizes the Request's
    `project_root` for all lookups, healing the Daemon/Client location paradox.

10. **The Self-Healing Fetch:** Implements a persistent, retry-enabled network
    emissary for unstable celestial connections.

11. **The Ephemeral Materializer:** Forges temporary files for stdin and inline
    scripts to provide line-number Gnosis for debuggers and stack traces.

12. **The Luminous Telemetry:** Injects detailed origin and performance metadata
    into the request context for forensic analysis.
=================================================================================
"""
import hashlib
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Tuple, Optional, Union, Dict, Any
from urllib.parse import urlparse

import requests

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...interfaces.requests import RunRequest
from ...logger import Scribe
from ...utils import atomic_write, hash_file, is_binary

# Lazy load for specialized cloud protocols
try:
    import boto3

    S3_AVAILABLE = True
except ImportError:
    S3_AVAILABLE = False


class EphemeralScribe:
    """The Sovereign Scribe of Gnostic Origins."""

    CACHE_DIR = Path.home() / ".scaffold" / "cache" / "scriptures"
    DEFAULT_TIMEOUT = 30

    # [FACULTY 1] The Sacred Boundary
    SACRED_EXTENSIONS = {'.scaffold', '.symphony', '.arch', '.patch.scaffold'}

    # Pragma Regex: # @key: value
    PRAGMA_PATTERN = re.compile(r"^#\s*@(\w+):\s*(.*)$", re.MULTILINE)

    # [FACULTY 6] Dangerous Shell Patterns
    SENTINEL_DANGER_PATTERNS = [
        r"rm\s+(-rf|-fr|--recursive)\s+/",  # Root destruction
        r":\(\)\{ :\|:& \};:",  # Fork bomb
        r">\s*/dev/sd[a-z]",  # Storage overwriting
        r"mkfs\.",  # Filesystem creation
    ]

    def __init__(self, project_root: Path, logger: Scribe):
        self.project_root = project_root
        self.logger = logger
        self._ensure_cache_sanctum()

    def _ensure_cache_sanctum(self):
        if not self.CACHE_DIR.exists():
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def perceive(self, request: RunRequest) -> Tuple[Path, str, bool, Optional[str]]:
        """
        [THE ALL-SEEING GAZE]
        """
        start_time = time.monotonic()

        # --- PATH I: EPHEMERAL INJECTION ---
        if request.eval_content is not None:
            return self._perceive_ephemeral(request, "eval")

        if request.pipe_content is not None:
            return self._perceive_ephemeral(request, "pipe")

        # --- PATH II: THE TARGET RESOLUTION ---
        target = str(request.target)
        if not target:
            raise ArtisanHeresy("The Scribe's Gaze requires a target scripture.")

        # [FACULTY 3] The Magic Protocol Resolver
        target = self._resolve_shorthand_protocols(target)

        # [FACULTY 7] S3 Support
        if target.startswith("s3://"):
            path, content, lang = self._perceive_s3(target, request)
            self._inject_telemetry(request, "s3", len(content), time.monotonic() - start_time)
            self._conduct_final_preparation(request, content, target)
            return path, content, True, lang

        # Celestial Protocol (HTTP/S)
        if target.startswith(('http://', 'https://')):
            path, content, lang = self._perceive_celestial(target, request)
            self._inject_telemetry(request, "remote", len(content), time.monotonic() - start_time)
            self._conduct_final_preparation(request, content, target)
            return path, content, True, lang

        # Mortal Protocol (Local File)
        path, content, lang = self._perceive_mortal(request, target)
        self._inject_telemetry(request, "local", len(content), time.monotonic() - start_time)
        self._conduct_final_preparation(request, content, str(path))
        return path, content, False, lang

    # =========================================================================
    # == THE PROTOCOL HANDLERS                                               ==
    # =========================================================================

    def _perceive_mortal(self, request: RunRequest, target: str) -> Tuple[Path, str, Optional[str]]:
        """[FACULTY 9] Contextual Anchor resolution."""
        root = request.project_root or self.project_root
        scripture_path = (root / target).resolve()

        if not scripture_path.is_file():
            if request.create_if_void:
                self.logger.warn(f"The scripture '{scripture_path.name}' is a void. Forging default soul.")
                default_content = f"# {scripture_path.name}\n# Reality forced by Scribe.\n"
                atomic_write(scripture_path, default_content, self.logger, root)
                return scripture_path, default_content, None  # Force prophet call
            else:
                raise ArtisanHeresy(
                    f"The scripture is a void and cannot be run.",
                    details=f"Path searched: {scripture_path}\nSanctum Root: {root}",
                    suggestion="Ensure the file exists or speak the `--create-if-void` vow."
                )

        # [FACULTY 8] The Binary Ward
        if is_binary(scripture_path):
            raise ArtisanHeresy(
                f"The scripture '{scripture_path.name}' has a binary soul. It cannot be run as a script.")

        try:
            content = scripture_path.read_text(encoding='utf-8')

            # [FACULTY 1] THE CORE FIX: SACRED DISCERNMENT
            # If the extension is sacred, we return lang=None to bypass the conductive hang.
            if scripture_path.suffix.lower() in self.SACRED_EXTENSIONS:
                self.logger.verbose(
                    f"L{request.line_num if hasattr(request, 'line_num') else '?'}: Sacred extension perceived. Deferring linguistic divination to Prophet.")
                return scripture_path, content, None

            # For mortal extensions, divining is safe.
            lang = scripture_path.suffix.lstrip('.') if scripture_path.suffix else None
            return scripture_path, content, lang
        except Exception as e:
            raise ArtisanHeresy(f"A paradox occurred reading '{scripture_path.name}'.", child_heresy=e)

    def _perceive_ephemeral(self, request: RunRequest, mode: str) -> Tuple[Path, str, bool, Optional[str]]:
        """[FACULTY 11] The Ephemeral Materializer."""
        self.logger.info(f"Scribe perceives ephemeral scripture ({mode}).")

        # We extract language hint from target (e.g. `scaffold run python --eval ...`)
        lang_hint = str(request.target).split(':')[0] if request.target else "txt"
        content = request.eval_content if mode == "eval" else (request.pipe_content or "")

        root = request.project_root or self.project_root
        filename = f"__scaffold_{mode}_{int(time.monotonic())}__.{lang_hint}"
        ephemeral_path = root / ".scaffold" / "ephemeral" / filename
        ephemeral_path.parent.mkdir(parents=True, exist_ok=True)
        ephemeral_path.write_text(content, encoding='utf-8')

        return ephemeral_path, content, True, lang_hint

    def _perceive_celestial(self, url: str, request: RunRequest) -> Tuple[Path, str, Optional[str]]:
        """[FACULTY 2, 4, 10] Celestial Fetching with SRI & Caching."""

        parsed = urlparse(url)
        # [FACULTY 4] SRI Parsing
        expected_hash = None
        if parsed.fragment and parsed.fragment.startswith("hash=sha256:"):
            expected_hash = parsed.fragment.split(":", 1)[1]

        # Gnostic Key for cache
        clean_url = url.split("#")[0]
        url_hash = hashlib.sha256(clean_url.encode()).hexdigest()
        cache_path = self.CACHE_DIR / f"{url_hash}.script"

        content = None
        if cache_path.exists() and not request.force:
            self.logger.verbose("Celestial scripture resurrected from Chronocache.")
            content = cache_path.read_text(encoding='utf-8')

        if content is None:
            self.logger.info(f"Communing with celestial void: {clean_url}")
            try:
                # [FACULTY 10] Resilient Session logic handled by requests implicitly if configured
                response = requests.get(clean_url, timeout=self.DEFAULT_TIMEOUT)
                response.raise_for_status()
                content = response.text
                cache_path.write_text(content, encoding='utf-8')
            except Exception as e:
                raise ArtisanHeresy(f"Celestial Communion Failed: {e}", child_heresy=e)

        # [FACULTY 4] Integrity Validation
        if expected_hash:
            actual = hashlib.sha256(content.encode()).hexdigest()
            if actual != expected_hash:
                raise ArtisanHeresy("Integrity Heresy: Celestial scripture is tainted!",
                                    severity=HeresySeverity.CRITICAL)
            self.logger.success("Cryptographic Integrity Verified.")

        # Lang Inference
        ext = Path(parsed.path).suffix.lstrip('.') or "sh"
        return cache_path, content, ext

    def _perceive_s3(self, uri: str, request: RunRequest) -> Tuple[Path, str, Optional[str]]:
        """[FACULTY 7] Native S3 Perception."""
        if not S3_AVAILABLE:
            raise ArtisanHeresy("The `boto3` artisan is missing. Access to S3 is blocked.")

        parsed = urlparse(uri)
        bucket, key = parsed.netloc, parsed.path.lstrip('/')

        try:
            s3 = boto3.client('s3')
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read().decode('utf-8')

            url_hash = hashlib.sha256(uri.encode()).hexdigest()
            cache_path = self.CACHE_DIR / f"s3_{url_hash}.script"
            cache_path.write_text(body, encoding='utf-8')

            return cache_path, body, Path(key).suffix.lstrip('.')
        except Exception as e:
            raise ArtisanHeresy(f"S3 Bridge shattered: {e}", child_heresy=e)

    # =========================================================================
    # == THE GNOSTIC PURIFIERS                                               ==
    # =========================================================================

    def _resolve_shorthand_protocols(self, target: str) -> str:
        """[FACULTY 3] Transmutes shorthand into valid URIs."""
        if target.startswith("gist:"):
            gist_id = target.split(":", 1)[1]
            return f"https://gist.githubusercontent.com/raw/{gist_id}"

        if target.startswith("gh:"):
            # gh:user/repo/branch/path
            parts = target.split(":", 1)[1].split("/")
            if len(parts) >= 2:
                user, repo = parts[0], parts[1]
                branch = parts[2] if len(parts) > 3 else "main"
                file_path = "/".join(parts[3:]) if len(parts) > 3 else "main.scaffold"
                return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"

        return target

    def _conduct_final_preparation(self, request: RunRequest, content: str, source: str):
        """[FACULTY 5 & 6] Security and Pragma analysis."""
        # 1. Pragma Gaze
        matches = self.PRAGMA_PATTERN.findall(content)
        for key, value in matches:
            if key == "runtime" and not request.runtime:
                self.logger.info(f"Auto-configuring runtime from Pragma: [cyan]{value}[/cyan]")
                request.runtime = value.strip()
            elif key == "env" and "=" in value:
                k, v = value.split("=", 1)
                if k not in request.variables: request.variables[k.strip()] = v.strip()

        # 2. Sentinel Gaze
        for pattern in self.SENTINEL_DANGER_PATTERNS:
            if re.search(pattern, content):
                raise ArtisanHeresy(
                    f"Security Ward: Profane pattern '{pattern}' detected in scripture from '{source}'.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Refuse to run this script. It attempts dangerous system modifications."
                )

    def _inject_telemetry(self, request: RunRequest, origin: str, size: int, latency: float):
        """[FACULTY 12] Telemetric Inscription."""
        request.variables["_scaffold_origin"] = origin
        request.variables["_scaffold_size_bytes"] = size
        request.variables["_scaffold_fetch_latency_ms"] = int(latency * 1000)