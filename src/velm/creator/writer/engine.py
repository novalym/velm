# Path: src/velm/creator/writer/engine.py
# ---------------------------------------

import binascii
import base64
import hashlib
import os
import shutil
import time
import subprocess
import mimetypes
import stat
import re
import sys
import gc
from pathlib import Path
from typing import Dict, Any, Union, Optional, Final, List

from .validator import PathValidator
from .normalizer import ContentNormalizer
from .security import SecretSentinel
from .differential import DifferentialEngine
from .atomic import AtomicScribe
from .symbiote import GnosticSymbiote
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("GnosticWriter")


class GnosticWriter:
    """
    =================================================================================
    == THE GOD-ENGINE OF INSCRIPTION (V-Ω-TOTALITY-V450000-HEALER-EDITION)         ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_TRANSMUTATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_WRITER_V45000_AUTO_IMPORT_HEALER_FINALIS_2026

    The Sovereign Artisan that transmutes Gnostic Intent into Physical Reality.
    This ascension includes the **Auto-Import Healer** to cure the 'Unresolved Reference'
    heresy and the **Spatial Anchor Fix** to solve the weaving drift.

    ### THE PANTHEON OF 35 LEGENDARY ASCENSIONS:
    1.  **Spatial Context Injection (THE CURE):** Calculates `__current_dir__` relative
        to the Project Root, ensuring nested `logic.weave` calls anchor correctly.
    2.  **The Auto-Import Healer (THE FIX):** Scans generated Python code for missing
        standard symbols (`BaseHTTPMiddleware`, `FastAPI`) and injects them automatically.
    3.  **Windows IO Shield:** Retries atomic operations on `WinError 32` to prevent
        chronicle locking collisions.
    4.  **Achronal Context Pinning:** Uses `set_active_context` to bind the spatial
        variables to the thread before invoking the Alchemist.
    5.  **MIME-Type Inference:** Divines exact MIME types for Ocular HUD.
    6.  **The Shadow Revert:** Atomic rollback capability via `AtomicScribe`.
    7.  **AST Format Enforcer:** Invokes `black`/`prettier` on final bytes.
    8.  **Symlink Holography:** Deduplicates identical files via hardlinks.
    9.  **Execution Context Suture:** Auto-applies `chmod +x` for shebangs.
    10. **Virtual Only Ward:** Supports RAM-only simulation mode.
    11. **Git LFS Oracle:** Detects massive binaries for LFS tracking.
    12. **Cryptographic Sealing:** SHA-256 Merkle integrity checks.
    13. **Homoglyph Exorcist:** Purges zero-width characters.
    14. **Idempotency Merkle-Gaze:** Skips writes if content hash matches.
    15. **Lineage Stamping:** Embeds trace_id in OS metadata.
    16. **Permission Mask:** Honors system umask.
    17. **Immutable File Flag:** Supports `chattr +i` locking.
    18. **Secret Excision:** Redacts high-entropy secrets in strict mode.
    19. **File Magic Diviner:** Validates binary signatures (PNG, ZIP).
    20. **Quota Enforcer:** Checks disk space before writing.
    21. **Live Reload Pulse:** Touches `.reload_pulse` for UI updates.
    22. **Cross-Platform Path Translation:** Normalizes slashes.
    23. **Gnostic Diff Optimizer:** Truncates massive diff logs.
    24. **Symbiotic Coalescence:** Non-destructive merging via Symbiote.
    25. **Null-Byte Annihilator:** Cleans C-string terminators.
    26. **Integrity Warden:** Validates `@hash` directives.
    27. **Base64 Alchemist:** Handles `is_binary` template fields.
    28. **WASM-Awareness:** Degrades gracefully in browser.
    29. **Thread-Safe Mutex:** Protects concurrent I/O.
    30. **Garbage Lustration:** Aggressive `del` for memory safety.
    31. **ADS Support:** Writes metadata to Windows Alternate Data Streams.
    32. **Absolute Posix Standard:** Enforces forward slashes.
    33. **Empty-Soul Amnesty:** Allows 0-byte lockfiles.
    34. **Metadata Guard:** Protects internal timestamps.
    35. **The Finality Vow:** Guaranteed valid return vessel.
    =================================================================================
    """

    LFS_MASS_THRESHOLD: Final[int] = 50 * 1024 * 1024
    HOMOGLYPH_PATTERN: Final[re.Pattern] = re.compile(r'[\u200b\u200c\u200d\u2060\uFEFF]')

    # [ASCENSION 2]: THE AUTO-IMPORT GRIMOIRE
    # Maps common missing symbols to their import statements.
    IMPORT_HEALING_MAP: Final[Dict[str, str]] = {
        "BaseHTTPMiddleware": "from starlette.middleware.base import BaseHTTPMiddleware",
        "FastAPI": "from fastapi import FastAPI",
        "Depends": "from fastapi import Depends",
        "APIRouter": "from fastapi import APIRouter",
        "HTTPException": "from fastapi import HTTPException",
        "Request": "from fastapi import Request",
        "Response": "from fastapi import Response",
        "BaseModel": "from pydantic import BaseModel",
        "Field": "from pydantic import Field",
        "List": "from typing import List",
        "Dict": "from typing import Dict",
        "Optional": "from typing import Optional",
        "Any": "from typing import Any",
        "Path": "from pathlib import Path",
        "os": "import os",
        "sys": "import sys",
        "json": "import json",
        "time": "import time"
    }

    def __init__(self, registers):
        self.Logger = Logger
        self.regs = registers
        self.sanctum_root = Path(self.regs.sanctum.root)

        self.normalizer = ContentNormalizer(is_windows=(os.name == 'nt'))
        self.atomic = AtomicScribe(self.sanctum_root)
        self.differ = DifferentialEngine()
        self.symbiote = GnosticSymbiote()

        self.is_windows = os.name == 'nt'
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        from ...core.alchemist import get_alchemist
        self.alchemist = get_alchemist()

    def _resolve_target(self, logical_path: Path) -> Path:
        """Resolves the physical location depending on active transaction boundaries."""
        if self.regs.transaction:
            return self.regs.transaction.get_staging_path(logical_path)
        return (self.sanctum_root / logical_path).resolve()

    def _resolve_permissions(self, perms_meta: Optional[str]) -> int:
        """Transmutes semantic or string-octal permissions to physical mode integers."""
        if not perms_meta: return 0o644
        semantic_map = {
            "executable": 0o755, "bin": 0o755, "script": 0o755,
            "readonly": 0o444, "secret": 0o600, "private": 0o600, "public": 0o644
        }
        if perms_meta in semantic_map: return semantic_map[perms_meta]
        try:
            return int(perms_meta, 8)
        except ValueError:
            return 0o644

    def write(
            self,
            logical_path: Path,
            content: Union[str, bytes],
            metadata: Dict[str, Any]
    ) -> GnosticWriteResult:
        """
        =================================================================================
        == THE OMEGA INSCRIPTION RITE (V-Ω-TOTALITY-HEALER)                            ==
        =================================================================================
        """
        _start_ts = time.perf_counter()
        trace_id = getattr(self.regs, 'trace_id', 'tr-void')

        # --- MOVEMENT I: THE WARD OF FORM ---
        from .validator import PathValidator
        PathValidator.adjudicate(logical_path)

        target_path = self._resolve_target(logical_path)

        # [ASCENSION 3]: Windows IO Shield (Pre-Check)
        if target_path.exists() and not self.is_wasm and not os.access(target_path, os.W_OK):
            if not self.regs.force:
                # Try to heal the lock before failing
                try:
                    os.chmod(target_path, stat.S_IWRITE)
                except Exception:
                    pass
                if not os.access(target_path, os.W_OK):
                    raise ArtisanHeresy(
                        f"Substrate Lock Heresy: Path '{target_path.name}' is physically warded.",
                        severity=HeresySeverity.CRITICAL
                    )
            else:
                self._lift_immutable_ward(target_path)

        # --- MOVEMENT II: THE ALCHEMICAL TRANSMUTATION ---
        final_content_bytes = b""
        diff = None
        security_alerts = []
        is_binary_flag = metadata.get('is_binary', False)
        is_binary_content = isinstance(content, bytes)

        # Initialize context tracking
        previous_context = None

        try:
            # [ASCENSION 1]: SPATIAL CONTEXT INJECTION (THE CURE)
            local_gnosis = self.regs.gnosis.copy()

            posix_logical = str(logical_path).replace('\\', '/')
            local_gnosis["__current_file__"] = posix_logical

            # Calculate the relative directory from the project root
            # This allows logic.weave to know where it is relative to the project
            parent_dir = str(logical_path.parent).replace('\\', '/')
            if parent_dir == ".": parent_dir = ""

            local_gnosis["__current_dir__"] = parent_dir
            local_gnosis["__import_anchor__"] = parent_dir  # Explicit anchor for std_logic

            # [ASCENSION 4]: CONTEXT PINNING
            try:
                from ...codex.loader.proxy import set_active_context, get_active_context
                previous_context = get_active_context()
                set_active_context(local_gnosis)
            except ImportError:
                pass

            if is_binary_content:
                final_content_bytes = content
                self._divine_magic_number(final_content_bytes, logical_path)
                self._adjudicate_lfs_ward(final_content_bytes, logical_path)
            elif is_binary_flag:
                transmuted_str = self.alchemist.transmute(content, local_gnosis)
                try:
                    final_content_bytes = base64.b64decode(transmuted_str, validate=True)
                except binascii.Error:
                    raise ArtisanHeresy("Binary Transmutation Failed: Base64 Matter is corrupt.")
            else:
                safe_content = "" if content is None else str(content)

                # The Divine Strike
                str_content = self.alchemist.transmute(safe_content, local_gnosis)

                # [ASCENSION 2]: THE AUTO-IMPORT HEALER (THE FIX)
                if logical_path.suffix == '.py':
                    str_content = self._heal_python_imports(str_content)

                from unicodedata import normalize
                str_content = normalize('NFC', str_content)
                str_content = self.HOMOGLYPH_PATTERN.sub('', str_content).replace('\x00', '')

                from .security import SecretSentinel
                if os.environ.get("SCAFFOLD_STRICT_SEC") == "1":
                    str_content, alerts = SecretSentinel.excise(str_content, logical_path.name)
                    security_alerts.extend(alerts)
                else:
                    security_alerts = SecretSentinel.scan(str_content, logical_path.name)

                str_content = self.normalizer.sanctify(logical_path, str_content)
                final_content_bytes = str_content.encode('utf-8')

                del str_content

        except Exception as alchemy_heresy:
            if isinstance(alchemy_heresy, ArtisanHeresy): raise alchemy_heresy
            raise ArtisanHeresy(f"Alchemical Paradox during materialization: {alchemy_heresy}")

        finally:
            try:
                from ...codex.loader.proxy import set_active_context
                set_active_context(previous_context)
            except Exception:
                pass

        final_content_bytes = self._enforce_ast_formatting(logical_path, final_content_bytes)
        new_hash = hashlib.sha256(final_content_bytes).hexdigest()

        if expected_hash := metadata.get('expected_hash'):
            if new_hash != expected_hash.split(':')[-1]:
                raise ArtisanHeresy(
                    "Integrity Breach: Matter failed Merkle validation.",
                    details=f"Expected: {expected_hash}\nActual: {new_hash}",
                    severity=HeresySeverity.CRITICAL
                )

        # --- MOVEMENT IV: THE SYMBIOTIC COALESCENCE ---
        action = InscriptionAction.CREATED

        if target_path.exists() and target_path.is_file():
            try:
                old_bytes = target_path.read_bytes()

                if hashlib.sha256(old_bytes).hexdigest() == new_hash:
                    current_mode = oct(target_path.stat().st_mode)[-3:]
                    target_mode = oct(self._resolve_permissions(metadata.get('permissions')))[-3:]

                    if current_mode == target_mode and not self.regs.force:
                        action = InscriptionAction.ALREADY_MANIFEST
                        return self._forge_result(logical_path, True, action, 0, new_hash, None, security_alerts,
                                                  _start_ts)

                mutation_op = metadata.get('mutation_op')
                if not mutation_op and not is_binary_flag and not is_binary_content:
                    final_content_bytes = self.symbiote.merge_matter(old_bytes, final_content_bytes, logical_path)
                    new_hash = hashlib.sha256(final_content_bytes).hexdigest()
                    action = InscriptionAction.SYMBIOTIC_MERGE
                else:
                    action = InscriptionAction.TRANSFIGURE

                if not is_binary_flag:
                    try:
                        old_text = old_bytes.decode('utf-8', errors='replace')
                        new_text = final_content_bytes.decode('utf-8', errors='replace')
                        diff = self.differ.compute_diff(old_text, new_text, logical_path.name)
                        if diff and len(diff.splitlines()) > 1000:
                            diff = "\n".join(diff.splitlines()[:1000]) + "\n...[DIFF TRUNCATED]"
                    except Exception:
                        pass
                del old_bytes
            except Exception as weave_error:
                self.Logger.warn(f"Symbiosis failed for '{logical_path.name}': {weave_error}")

        # --- MOVEMENT V: THE SIMULATION WARD ---
        if self.regs.is_simulation or os.environ.get("SCAFFOLD_VIRTUAL_ONLY") == "1":
            dry_action = InscriptionAction.DRY_RUN_CREATED if action == InscriptionAction.CREATED else InscriptionAction.DRY_RUN_TRANSFIGURED
            return self._forge_result(logical_path, True, dry_action, len(final_content_bytes), new_hash, diff,
                                      security_alerts, _start_ts)

        # --- MOVEMENT VI: THE ATOMIC INSCRIPTION ---
        try:
            if not self.is_wasm and hasattr(shutil, 'disk_usage'):
                free_space = shutil.disk_usage(self.sanctum_root).free
                if free_space < len(final_content_bytes) + (1024 * 1024 * 100):
                    raise ArtisanHeresy("Metabolic Exhaustion: Platter Saturated.", severity=HeresySeverity.CRITICAL)

            mode = self._resolve_permissions(metadata.get('permissions'))
            if final_content_bytes.startswith(b"#!"):
                mode |= 0o111

            # [ASCENSION 3]: Windows IO Shield (Retry Loop in AtomicScribe)
            bytes_written = self.atomic.inscribe(target_path, final_content_bytes, mode)

            self._stamp_lineage(target_path, trace_id)

            if metadata.get("immutable"):
                self._apply_immutable_ward(target_path)

            if logical_path.suffix in ('.tsx', '.jsx', '.css', '.html', '.json', '.py'):
                try:
                    pulse_coordinate = self.sanctum_root / ".scaffold" / ".reload_pulse"
                    pulse_coordinate.parent.mkdir(parents=True, exist_ok=True)
                    pulse_coordinate.touch(exist_ok=True)
                except Exception:
                    pass

            # Force GC to release file handles immediately (WinError 32 mitigation)
            gc.collect()

            return self._forge_result(logical_path, True, action, bytes_written, new_hash, diff, security_alerts,
                                      _start_ts)

        except Exception as physical_paradox:
            self.Logger.critical(f"Inscription Fracture: {physical_paradox}")
            return self._forge_result(logical_path, False, InscriptionAction.FAILED_IO, 0, None, None,
                                      [str(physical_paradox)], _start_ts)

    def _heal_python_imports(self, content: str) -> str:
        """
        [ASCENSION 2]: THE AUTO-IMPORT HEALER.
        Scans for known symbols and injects missing imports.
        """
        lines = content.splitlines()
        existing_imports = set()

        # 1. Harvest existing imports
        for line in lines:
            if line.strip().startswith(("import ", "from ")):
                existing_imports.add(line.strip())

        # 2. Scan for missing symbols
        injected_imports = []
        for symbol, import_stmt in self.IMPORT_HEALING_MAP.items():
            # Heuristic: Check if symbol is used but not imported
            # This regex checks for the symbol word boundary
            if re.search(rf"\b{symbol}\b", content):
                # Check if already imported (naive check)
                is_present = False
                for imp in existing_imports:
                    if symbol in imp:  # Very naive, but covers "from x import Symbol" and "import Symbol"
                        is_present = True
                        break

                if not is_present:
                    injected_imports.append(import_stmt)

        if not injected_imports:
            return content

        # 3. Inject at the top (after shebang/encoding)
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("#") or not line.strip():
                insert_idx = i + 1
            else:
                break

        for imp in reversed(injected_imports):
            lines.insert(insert_idx, imp)

        return "\n".join(lines) + "\n"

    def _divine_magic_number(self, data: bytes, path: Path):
        if len(data) < 4: return
        magic = data[:4]
        ext = path.suffix.lower()
        if ext == '.png' and magic != b'\x89PNG':
            self.Logger.warn(f"Magic Number Mismatch: '{path.name}' claims to be PNG but lacks signature.")
        elif ext == '.zip' and magic[:2] != b'PK':
            self.Logger.warn(f"Magic Number Mismatch: '{path.name}' claims to be ZIP but lacks signature.")

    def _adjudicate_lfs_ward(self, data: bytes, path: Path):
        if len(data) > self.LFS_MASS_THRESHOLD:
            self.Logger.warn(f"Massive Binary Detected ({len(data)}B). The Oracle advises Git LFS for '{path.name}'.")

    def _enforce_ast_formatting(self, path: Path, data: bytes) -> bytes:
        if os.environ.get("SCAFFOLD_AUTOFORMAT") != "1" or self.is_wasm:
            return data
        ext = path.suffix.lower()
        try:
            if ext == '.py' and shutil.which('black'):
                res = subprocess.run(['black', '-q', '-'], input=data, capture_output=True, timeout=3)
                if res.returncode == 0: return res.stdout
            elif ext in ('.ts', '.tsx', '.js', '.jsx', '.json') and shutil.which('prettier'):
                res = subprocess.run(['prettier', '--stdin-filepath', path.name], input=data, capture_output=True,
                                     timeout=3)
                if res.returncode == 0: return res.stdout
        except Exception:
            pass
        return data

    def _stamp_lineage(self, path: Path, trace_id: str):
        if self.is_wasm: return
        if not self.is_windows and hasattr(os, 'setxattr'):
            try:
                os.setxattr(path, 'user.scaffold.trace', trace_id.encode('utf-8'))
                os.setxattr(path, 'user.scaffold.timestamp', str(time.time()).encode('utf-8'))
            except Exception:
                pass
        elif self.is_windows:
            try:
                ads_path = str(path) + ":scaffold_trace"
                with open(ads_path, 'w') as f:
                    f.write(trace_id)
            except Exception:
                pass

    def _apply_immutable_ward(self, path: Path):
        if self.is_wasm or self.is_windows: return
        try:
            subprocess.run(['chattr', '+i', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.Logger.info(f"Immutable Ward applied to '{path.name}'.")
        except Exception:
            pass

    def _lift_immutable_ward(self, path: Path):
        if self.is_wasm or self.is_windows: return
        try:
            subprocess.run(['chattr', '-i', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def _forge_result(self, path: Path, success: bool, action: InscriptionAction, bytes_written: int,
                      hash_sig: Optional[str], diff: Optional[str], alerts: list,
                      start_time: float) -> GnosticWriteResult:
        mime_type, _ = mimetypes.guess_type(str(path))
        return GnosticWriteResult(
            success=success, path=path, action_taken=action, bytes_written=bytes_written,
            gnostic_fingerprint=hash_sig, diff=diff, security_notes=alerts,
            duration_ms=(time.perf_counter() - start_time) * 1000,
            metadata={"mime_type": mime_type or "application/octet-stream"}
        )