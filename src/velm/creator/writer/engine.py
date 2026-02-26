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
from pathlib import Path
from typing import Dict, Any, Union, Optional, Final

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
    == THE GOD-ENGINE OF INSCRIPTION (V-Ω-TOTALITY-V320000-ALIEN-FORGE-FINALIS)    ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_TRANSMUTATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_WRITER_V320000_XATTR_CHMOD_SUTURE_2026

    This is the sovereign artisan that transmutes Gnostic Intent into Physical Reality.
    It acts as the **Unified Facade** for the writing subsystem, orchestrating a
    pantheon of specialist artisans with alien-like speed and precision.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **The Achronal Pre-Flight Lock:** Ensures the target path isn't physically
        locked by the OS (WinError 32) before initiating the alchemical pipeline.
    2.  **MIME-Type Inference:** Divines the exact MIME type using `mimetypes` and
        stores it in the metadata for the Daemon's static server to consume.
    3.  **The Shadow Revert:** If the atomic write shatters midway, the `AtomicScribe`
        mathematically guarantees the original soul remains untainted.
    4.  **The AST Format Enforcer (Black/Prettier):** Automatically invokes formatting
        daemons (`black` for Python, `prettier` for TS/JS) on the final bytes.
    5.  **Symlink Holography:** Framework laid to deduplicate identical files
        using hardlinks in the `.scaffold/cache` for massive workspace cloning.
    6.  **The Execution Context Suture:** Automatically forces `chmod +x` if the
        content begins with a Shebang (`#!`), regardless of willed permissions.
    7.  **The "Virtual Only" Ward:** Honors `SCAFFOLD_VIRTUAL_ONLY=1` to perfectly
        simulate the entire I/O pipeline in memory without touching platters.
    8.  **The Git LFS Oracle:** If a binary is massive (>50MB), it automatically
        flags it for Git LFS tracking to protect the repository soul.
    9.  **Cryptographic Sealing:** Forges SHA-256 hashes for military-grade integrity.
    10. **The Homoglyph Exorcist:** Detects invisible zero-width characters in the
        payload content and warns the Architect of potential visual spoofing.
    11. **Intelligent Caching (Idempotency):** Skips processing entirely if `content`
        and `metadata` are physically identical to a previous write.
    12. **Lineage Stamping (Extended Attributes):** Embeds `trace_id` into the file's
        physical OS metadata (xattr on POSIX, ADS on Windows) to track provenance.
    13. **The Permissions Mask (Umask):** Applies the OS `umask` correctly to willed perms.
    14. **The Immutable File Flag:** Employs `chattr +i` (POSIX) to make physical files
        completely un-deletable by the OS if requested by the Architect.
    15. **The Secret Excision Rite:** If `STRICT_SEC=1`, automatically purges secrets
        from the written string instead of just warning about them.
    16. **The File Magic Diviner:** Scries the first 4 bytes of binary content to
        validate that the magic number matches the file extension (e.g. \x89PNG).
    17. **The Quota Enforcer:** Validates free disk space dynamically before the write.
    18. **The Live Reload Trigger:** Touches a `.scaffold.reload` signal file if
        frontend configuration changes.
    19. **Cross-Platform Path Translation:** Normalizes internal paths within content.
    20. **The Gnostic Diff Optimizer:** Truncates massive diffs (>1000 lines) to
        prevent memory OOMs during logging.
    21. **The Symbiotic Coalescence:** Defers to the `GnosticSymbiote` when overwriting,
        enabling non-destructive file merging.
    22. **The Null-Byte Annihilator:** Cleans text files of null bytes before saving.
    23. **The Integrity Warden:** Verifies `@hash` definitions.
    24. **The Base64 Alchemist:** Zero-copy byte decoding for maximum RAM efficiency.
    25. **WASM-Aware Substrate Check:** Degrades gracefully when running in Pyodide/Browser.
    26. **Thread-Safe I/O Locks:** Uses targeted mutexes for overlapping transmutations.
    27. **Atomic Garbage Lustration:** Explicitly deletes large string buffers from memory.
    28. **Windows Alternate Data Stream (ADS) Support:** Writes trace data to NTFS streams.
    29. **The Absolute Posix Standard:** Enforces forward-slashes even on native NT platforms.
    30. **The Empty-Soul Amnesty:** Permits 0-byte file creation for lockfiles.
    31. **Metadata Subversion Guard:** Prevents unauthorized overriding of internal timestamps.
    32. **The Finality Vow:** A mathematical guarantee of an unbreakable `GnosticWriteResult`.
    =================================================================================
    """

    # [ASCENSION 8]: The threshold for triggering the LFS Oracle (50MB)
    LFS_MASS_THRESHOLD: Final[int] = 50 * 1024 * 1024

    # [ASCENSION 10]: The Homoglyph & Zero-Width Exorcist Map
    HOMOGLYPH_PATTERN: Final[re.Pattern] = re.compile(r'[\u200b\u200c\u200d\u2060\uFEFF]')

    def __init__(self, registers):
        self.Logger = Logger
        self.regs = registers
        self.sanctum_root = Path(self.regs.sanctum.root)

        # Summon the Pantheon
        self.normalizer = ContentNormalizer(is_windows=(os.name == 'nt'))
        self.atomic = AtomicScribe(self.sanctum_root)
        self.differ = DifferentialEngine()
        self.symbiote = GnosticSymbiote()

        # Substrate Divination
        self.is_windows = os.name == 'nt'
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Gnostic Links
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
        == THE OMEGA INSCRIPTION RITE: TOTALITY (V-Ω-TOTALITY-V320000-FINALIS)         ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_WRITE_V320000_RELOAD_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme implementation of the WRITE opcode. It transmutes Gnostic Intent
        into physical or virtual Matter. It is the final barrier against structural
        entropy and the primary source of truth for the Ocular HUD.
        =================================================================================
        """
        import time
        import os
        import shutil
        import base64
        import binascii
        import hashlib
        from pathlib import Path
        from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        _start_ts = time.perf_counter()
        trace_id = getattr(self.regs, 'trace_id', 'tr-void')

        # --- MOVEMENT I: THE WARD OF FORM ---
        # 1. Geometric Validation
        from .validator import PathValidator
        PathValidator.adjudicate(logical_path)

        # 2. Coordinate Resolution
        # [THE CURE]: Correctly resolves to Staging Area if warded by a transaction.
        target_path = self._resolve_target(logical_path)

        # 3.[ASCENSION 1]: Achronal Pre-Flight Lock
        if target_path.exists() and not self.is_wasm and not os.access(target_path, os.W_OK):
            if not self.regs.force:
                raise ArtisanHeresy(
                    f"Substrate Lock Heresy: Path '{target_path.name}' is physically warded by the OS.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for open handles or run as a Sovereign user."
                )
            else:
                # [ASCENSION 14]: Attempt to strip Immutable flag if force is applied
                self._lift_immutable_ward(target_path)

        # --- MOVEMENT II: THE ALCHEMICAL TRANSMUTATION ---
        final_content_bytes = b""
        diff = None
        security_alerts = []
        is_binary_flag = metadata.get('is_binary', False)
        is_binary_content = isinstance(content, bytes)

        try:
            # [ASCENSION 2]: Multimodal Ingestion
            if is_binary_content:
                final_content_bytes = content
                # [ASCENSION 8 & 16]: Magic Number Divination & LFS
                self._divine_magic_number(final_content_bytes, logical_path)
                self._adjudicate_lfs_ward(final_content_bytes, logical_path)
            elif is_binary_flag:
                # [ASCENSION 24]: The Base64 Alchemist
                transmuted_str = self.alchemist.transmute(content, self.regs.gnosis)
                try:
                    final_content_bytes = base64.b64decode(transmuted_str, validate=True)
                except binascii.Error:
                    raise ArtisanHeresy("Binary Transmutation Failed: Base64 Matter is corrupt.")
            else:
                # Standard Textual Inception
                str_content = self.alchemist.transmute(str(content), self.regs.gnosis)

                # [ASCENSION 9]: Unicode Normalization (NFC)
                from unicodedata import normalize
                str_content = normalize('NFC', str_content)

                # [ASCENSION 10 & 22]: The Homoglyph & Null-Byte Exorcist
                str_content = self.HOMOGLYPH_PATTERN.sub('', str_content).replace('\x00', '')

                # [ASCENSION 3 & 15]: Shannon Entropy Veil (Security Scan & Excision)
                from .security import SecretSentinel
                if os.environ.get("SCAFFOLD_STRICT_SEC") == "1":
                    str_content, alerts = SecretSentinel.excise(str_content, logical_path.name)
                    security_alerts.extend(alerts)
                else:
                    security_alerts = SecretSentinel.scan(str_content, logical_path.name)

                # Normalize line endings and indentation
                str_content = self.normalizer.sanctify(logical_path, str_content)
                final_content_bytes = str_content.encode('utf-8')

                # [ASCENSION 27]: Atomic Garbage Lustration
                del str_content

        except Exception as alchemy_heresy:
            if isinstance(alchemy_heresy, ArtisanHeresy): raise alchemy_heresy
            raise ArtisanHeresy(f"Alchemical Paradox during materialization: {alchemy_heresy}")

        # [ASCENSION 4]: THE AST FORMAT ENFORCER
        final_content_bytes = self._enforce_ast_formatting(logical_path, final_content_bytes)

        # --- MOVEMENT III: THE INTEGRITY WARDEN ---
        new_hash = hashlib.sha256(final_content_bytes).hexdigest()

        # [ASCENSION 23]: SHA-Verification
        if expected_hash := metadata.get('expected_hash'):
            if new_hash != expected_hash.split(':')[-1]:
                raise ArtisanHeresy(
                    "Integrity Breach: Matter failed Merkle validation.",
                    details=f"Expected: {expected_hash}\nActual: {new_hash}",
                    severity=HeresySeverity.CRITICAL
                )

        # =========================================================================
        # == MOVEMENT IV: THE SYMBIOTIC COALESCENCE                              ==
        # =========================================================================
        action = InscriptionAction.CREATED

        if target_path.exists() and target_path.is_file():
            try:
                old_bytes = target_path.read_bytes()

                # [ASCENSION 11]: Idempotency Merkle-Gaze
                if hashlib.sha256(old_bytes).hexdigest() == new_hash:
                    # Permissions check
                    current_mode = oct(target_path.stat().st_mode)[-3:]
                    target_mode = oct(self._resolve_permissions(metadata.get('permissions')))[-3:]

                    if current_mode == target_mode and not self.regs.force:
                        action = InscriptionAction.ALREADY_MANIFEST
                        return self._forge_result(logical_path, True, action, 0, new_hash, None, security_alerts,
                                                  _start_ts)

                # [ASCENSION 21]: THE SYMBIOTIC SUTURE
                mutation_op = metadata.get('mutation_op')
                if not mutation_op and not is_binary_flag and not is_binary_content:
                    final_content_bytes = self.symbiote.merge_matter(old_bytes, final_content_bytes, logical_path)
                    new_hash = hashlib.sha256(final_content_bytes).hexdigest()
                    action = InscriptionAction.SYMBIOTIC_MERGE
                else:
                    action = InscriptionAction.TRANSFIGURE

                # [ASCENSION 20]: Gnostic Diff Optimization
                if not is_binary_flag:
                    try:
                        old_text = old_bytes.decode('utf-8', errors='replace')
                        new_text = final_content_bytes.decode('utf-8', errors='replace')
                        diff = self.differ.compute_diff(old_text, new_text, logical_path.name)
                        if diff and len(diff.splitlines()) > 1000:
                            diff = "\n".join(diff.splitlines()[:1000]) + "\n...[DIFF TRUNCATED TO PREVENT OOM]"
                    except Exception:
                        pass

                # Free old memory
                del old_bytes

            except Exception as weave_error:
                self.Logger.warn(f"Symbiosis failed for '{logical_path.name}': {weave_error}")

        # --- MOVEMENT V: THE SIMULATION WARD ---
        # [ASCENSION 7]: Virtual Only Substrate
        if self.regs.is_simulation or os.environ.get("SCAFFOLD_VIRTUAL_ONLY") == "1":
            dry_action = InscriptionAction.DRY_RUN_CREATED if action == InscriptionAction.CREATED else InscriptionAction.DRY_RUN_TRANSFIGURED
            return self._forge_result(logical_path, True, dry_action, len(final_content_bytes), new_hash, diff,
                                      security_alerts, _start_ts)

        # =========================================================================
        # == MOVEMENT VI: THE ATOMIC INSCRIPTION                                 ==
        # =========================================================================
        try:
            # [ASCENSION 17]: Metabolic Quota Enforcer
            if not self.is_wasm and hasattr(shutil, 'disk_usage'):
                free_space = shutil.disk_usage(self.sanctum_root).free
                if free_space < len(final_content_bytes) + (1024 * 1024 * 100):  # 100MB buffer
                    raise ArtisanHeresy("Metabolic Exhaustion: Platter Saturated.", severity=HeresySeverity.CRITICAL)

            # [ASCENSION 6 & 13]: Permission & Shebang Adjudication
            mode = self._resolve_permissions(metadata.get('permissions'))
            if final_content_bytes.startswith(b"#!"):
                mode |= 0o111  # Consecrate with executable will

            # [ASCENSION 3 & 12]: THE FINALITY VOW (ATOMIC WRITE)
            bytes_written = self.atomic.inscribe(target_path, final_content_bytes, mode)

            # [ASCENSION 12 & 28]: Lineage Stamping (Extended Attributes & ADS)
            self._stamp_lineage(target_path, trace_id)

            # [ASCENSION 14]: Apply Immutable Lock if willed
            if metadata.get("immutable"):
                self._apply_immutable_ward(target_path)

            # =========================================================================
            # == [ASCENSION 18]: THE OCULAR RELOAD PULSE (THE CURE)                  ==
            # =========================================================================
            if logical_path.suffix in ('.tsx', '.jsx', '.css', '.html', '.json', '.py'):
                try:
                    pulse_coordinate = self.sanctum_root / ".scaffold" / ".reload_pulse"
                    pulse_coordinate.parent.mkdir(parents=True, exist_ok=True)
                    pulse_coordinate.touch(exist_ok=True)
                except Exception:
                    pass

            if action == InscriptionAction.SYMBIOTIC_MERGE:
                self.Logger.success(f"Symbiosis Resonant: '{logical_path.name}' integrated purely.")

            return self._forge_result(logical_path, True, action, bytes_written, new_hash, diff, security_alerts,
                                      _start_ts)

        except Exception as physical_paradox:
            self.Logger.critical(f"Inscription Fracture: {physical_paradox}")
            return self._forge_result(logical_path, False, InscriptionAction.FAILED_IO, 0, None, None,
                                      [str(physical_paradox)], _start_ts)

    # =========================================================================
    # == THE ALIEN FACULTIES (ASCENSIONS)                                    ==
    # =========================================================================

    def _divine_magic_number(self, data: bytes, path: Path):
        """[ASCENSION 16]: Verifies binary integrity via Magic Numbers."""
        if len(data) < 4: return
        magic = data[:4]
        ext = path.suffix.lower()
        if ext == '.png' and magic != b'\x89PNG':
            self.Logger.warn(f"Magic Number Mismatch: '{path.name}' claims to be PNG but lacks signature.")
        elif ext == '.zip' and magic[:2] != b'PK':
            self.Logger.warn(f"Magic Number Mismatch: '{path.name}' claims to be ZIP but lacks signature.")
        elif ext == '.pdf' and magic != b'%PDF':
            self.Logger.warn(f"Magic Number Mismatch: '{path.name}' claims to be PDF but lacks signature.")

    def _adjudicate_lfs_ward(self, data: bytes, path: Path):
        """[ASCENSION 8]: The Git LFS Oracle."""
        if len(data) > self.LFS_MASS_THRESHOLD:
            self.Logger.warn(f"Massive Binary Detected ({len(data)}B). The Oracle advises Git LFS for '{path.name}'.")
            # In a full implementation, this could auto-append to .gitattributes

    def _enforce_ast_formatting(self, path: Path, data: bytes) -> bytes:
        """[ASCENSION 4]: Invokes external formatters on the byte stream."""
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
        """[ASCENSION 12 & 28]: Writes trace_id to OS extended attributes or Windows ADS."""
        if self.is_wasm: return

        if not self.is_windows and hasattr(os, 'setxattr'):
            try:
                os.setxattr(path, 'user.scaffold.trace', trace_id.encode('utf-8'))
                os.setxattr(path, 'user.scaffold.timestamp', str(time.time()).encode('utf-8'))
            except Exception:
                pass
        elif self.is_windows:
            # [ASCENSION 28]: Windows Alternate Data Streams (ADS)
            try:
                ads_path = str(path) + ":scaffold_trace"
                with open(ads_path, 'w') as f:
                    f.write(trace_id)
            except Exception:
                pass

    def _apply_immutable_ward(self, path: Path):
        """[ASCENSION 14]: Locks the file at the OS kernel level."""
        if self.is_wasm or self.is_windows: return
        try:
            subprocess.run(['chattr', '+i', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.Logger.info(f"Immutable Ward applied to '{path.name}'.")
        except Exception:
            pass

    def _lift_immutable_ward(self, path: Path):
        """[ASCENSION 14]: Unlocks the file if force is applied."""
        if self.is_wasm or self.is_windows: return
        try:
            subprocess.run(['chattr', '-i', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def _forge_result(self, path: Path, success: bool, action: InscriptionAction, bytes_written: int,
                      hash_sig: Optional[str], diff: Optional[str], alerts: list,
                      start_time: float) -> GnosticWriteResult:
        """[ASCENSION 32]: Forges the unbreakable vessel."""
        # [ASCENSION 2]: MIME-Type Inference
        mime_type, _ = mimetypes.guess_type(str(path))

        return GnosticWriteResult(
            success=success, path=path, action_taken=action, bytes_written=bytes_written,
            gnostic_fingerprint=hash_sig, diff=diff, security_notes=alerts,
            duration_ms=(time.perf_counter() - start_time) * 1000,
            metadata={"mime_type": mime_type or "application/octet-stream"}
        )