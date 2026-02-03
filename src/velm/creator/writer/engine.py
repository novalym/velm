# Path: scaffold/creator/writer/engine.py
# ---------------------------------------

"""
=================================================================================
== THE GOD-ENGINE OF INSCRIPTION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)               ==
=================================================================================
LIF: 10,000,000,000,000 (THE FINAL BARRIER)

This is the sovereign artisan that transmutes Gnostic Intent into Physical Reality.
It acts as the **Unified Facade** for the writing subsystem, orchestrating a
pantheon of specialist artisans to ensure that every byte inscribed upon the
disk is pure, secure, verified, and atomic.

### THE PANTHEON OF 12 ASCENDED FACULTIES:

1.  **The Integrity Warden (@hash):** Checks the cryptographic fingerprint of the
    content *before* inscription. If it does not match the `@hash(...)` anchor provided
    in the blueprint, it raises a `IntegrityHeresy`, preventing tainted materialization.

2.  **The Binary Diviner (Base64):** Detects if the content is a Base64-encoded
    artifact (signaled by `is_binary` metadata). It performs the Rite of Transmutation,
    decoding the text string back into raw bytes for binary injection (images, zips).

3.  **The Permission Alchemist:** Transmutes semantic permission keys ('executable',
    'secret', 'readonly') into their octal truths ('755', '600', '444') before
    consecrating the file metadata.

4.  **The Alchemical Mixer:** Summons the `DivineAlchemist` to resolve all Jinja2
    variables (`{{ var }}`) within textual content before normalization.

5.  **The Atomic Hand:** Delegates the physical act of writing to the `AtomicScribe`,
    which uses a `write-temp-and-rename` strategy to ensure no file is ever left
    in a torn or partial state during a crash.

6.  **The Differential Oracle:** Before touching the disk, it computes the hash of
    the new soul and compares it to the existing reality. If they match, it
    proclaims `ALREADY_MANIFEST` and stays its hand (Idempotency).

7.  **The Dry-Run Prophet:** In simulation mode, it performs all calculations,
    transmutations, and diffs, but stops exactly one microsecond before the
    physical write, returning a perfect prophecy of what *would* have happened.

8.  **The Secret Sentinel:** Scans the final, transmuted content for hardcoded
    secrets (API keys, tokens) and raises a `SecurityHeresy` or warning if
    profane patterns are detected.

9.  **The Normalizer:** Enforces consistent Line Endings (LF vs CRLF) and
    Tab/Space discipline based on the file type (e.g., Makefiles get tabs).

10. **The Path Validator:** A final, paranoid check to ensure the target path
    does not contain illegal characters or traversal attempts (`../`) that
    slipped past the `IOController`.

11. **The Luminous Chronicle:** Returns a rich `GnosticWriteResult` object,
    containing the file's new hash, size, diff, and any security alerts,
    powering the high-fidelity UI reporting.

12. **The Unbreakable Ward:** All operations are wrapped in a master `try/except`
    block that transmutes raw OS errors into meaningful `ArtisanHeresy` exceptions
    without crashing the main loop.
=================================================================================
"""

import binascii
import base64
import hashlib
import os
import time
from pathlib import Path
from typing import Dict, Any, Union, Optional

from .validator import PathValidator
from .normalizer import ContentNormalizer
from .security import SecretSentinel
from .differential import DifferentialEngine
from .atomic import AtomicScribe
from .contracts import WriterResult
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("GnosticWriter")


class GnosticWriter:
    """
    The High Priest of Inscription.
    Orchestrates the transmutation of content into file.
    """

    def __init__(self, registers):
        self.regs = registers
        self.sanctum_root = Path(self.regs.sanctum.root)

        # Summon the Pantheon
        self.normalizer = ContentNormalizer(is_windows=(os.name == 'nt'))
        self.atomic = AtomicScribe(self.sanctum_root)
        self.differ = DifferentialEngine()

        # Gnostic Links
        from ...core.alchemist import get_alchemist
        self.alchemist = get_alchemist()

    def _resolve_target(self, logical_path: Path) -> Path:
        """
        Calculates the physical path, respecting transactions.
        If a transaction is active, redirects to the Staging Area.
        """
        if self.regs.transaction:
            return self.regs.transaction.get_staging_path(logical_path)
        return (self.sanctum_root / logical_path).resolve()

    def _resolve_permissions(self, perms_meta: Optional[str]) -> int:
        """
        [FACULTY 3] The Permission Alchemist.
        Transmutes named or string octals into integers.
        """
        if not perms_meta:
            return 0o644

        # The Grimoire of Named Permissions
        semantic_map = {
            "executable": 0o755,
            "bin": 0o755,
            "script": 0o755,
            "readonly": 0o444,
            "secret": 0o600,
            "private": 0o600,
            "public": 0o644
        }

        if perms_meta in semantic_map:
            return semantic_map[perms_meta]

        try:
            return int(perms_meta, 8)
        except ValueError:
            Logger.warn(f"Invalid permission '{perms_meta}'. Defaulting to 644.")
            return 0o644

    def write(
            self,
            logical_path: Path,
            content: Union[str, bytes],
            metadata: Dict[str, Any]
    ) -> GnosticWriteResult:
        """
        The Grand Rite of Inscription.

        Args:
            logical_path: Relative path within the project (e.g. src/main.py)
            content: The raw soul (text or bytes)
            metadata: Gnostic context (permissions, origin, expected_hash, is_binary)
        """
        start_time = time.time()

        # 1. THE WARD OF FORM (Validation)
        # This catches the "Parser Leak" (code as filename) before it hits the OS.
        PathValidator.adjudicate(logical_path)

        target_path = self._resolve_target(logical_path)

        # Check explicit binary flag from parser (via metadata) or type check
        is_binary_flag = metadata.get('is_binary', False)
        is_binary_content = isinstance(content, bytes)

        # 2. THE ALCHEMICAL TRANSMUTATION
        final_content_bytes = b""
        diff = None
        security_alerts = []

        try:
            # --- PATH A: BINARY ARTIFACTS ---
            if is_binary_content:
                # Content passed as bytes is already pure.
                final_content_bytes = content
            elif is_binary_flag:
                # [FACULTY 2] The Binary Diviner
                # The content is a string, but flagged as binary (e.g., base64 string).
                # We must transmute it.
                # First, resolve variables if it's a template string: "{{ var | base64 }}"
                transmuted_str = self.alchemist.transmute(content, self.regs.gnosis)
                try:
                    final_content_bytes = base64.b64decode(transmuted_str)
                except binascii.Error as e:
                    raise ArtisanHeresy(
                        f"Binary Transmutation Failed: '{logical_path}' content is not valid Base64.",
                        details=str(e),
                        severity=HeresySeverity.CRITICAL
                    )

            # --- PATH B: TEXTUAL SCRIPTURES ---
            else:
                # [FACULTY 4] The Alchemical Mixer
                # Transmute variables
                str_content = self.alchemist.transmute(str(content), self.regs.gnosis)

                # [FACULTY 9] The Normalizer
                # Harmonize EOL and indentation quirks
                str_content = self.normalizer.sanctify(logical_path, str_content)

                # [FACULTY 8] The Secret Sentinel
                # Scan for leaked API keys
                security_alerts = SecretSentinel.scan(str_content, logical_path.name)

                final_content_bytes = str_content.encode('utf-8')

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"Alchemical Paradox processing '{logical_path}': {e}") from e

        # 3. THE INTEGRITY WARDEN (Integrity Check)
        # [FACULTY 1]
        new_hash = self.differ.compute_hash(final_content_bytes)
        expected_hash = metadata.get('expected_hash')

        if expected_hash:
            # We support "algo:digest" format (e.g. sha256:abc...)
            algo, digest = "sha256", expected_hash
            if ":" in expected_hash:
                algo, digest = expected_hash.split(":", 1)

            # Currently we only support sha256 via compute_hash
            if algo != "sha256":
                Logger.warn(f"Integrity Warden only supports sha256. '{algo}' ignored for '{logical_path}'.")
            elif new_hash != digest:
                raise ArtisanHeresy(
                    f"Integrity Breach: The forged soul of '{logical_path}' does not match the Prophecy.",
                    details=f"Expected: {digest}\nActual:   {new_hash}",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify the template source or the @hash anchor in the blueprint."
                )
            else:
                Logger.verbose(f"Integrity Verified for '{logical_path}'.")

        # 4. THE DIFFERENTIAL GAZE
        action = InscriptionAction.CREATED

        # Check existing file on disk
        if target_path.exists() and target_path.is_file():
            try:
                old_bytes = target_path.read_bytes()
                old_hash = self.differ.compute_hash(old_bytes)

                # [FACULTY 6] Idempotency Check
                if old_hash == new_hash:
                    # Check if permissions drifted
                    current_mode = oct(target_path.stat().st_mode)[-3:]
                    target_mode_octal = oct(self._resolve_permissions(metadata.get('permissions')))[-3:]

                    if current_mode == target_mode_octal:
                        action = InscriptionAction.ALREADY_MANIFEST
                        if not self.regs.force:
                            return self._forge_result(
                                logical_path, True, action, 0, new_hash, None, security_alerts, start_time
                            )
                    else:
                        # Content same, perms diff -> Transfigure (chmod only)
                        action = InscriptionAction.TRANSFIGURED

                else:
                    action = InscriptionAction.TRANSFIGURED
                    # Generate Diff if text
                    if not is_binary_flag and not is_binary_content:
                        try:
                            old_str = old_bytes.decode('utf-8', errors='replace')
                            new_str = final_content_bytes.decode('utf-8', errors='replace')
                            diff = self.differ.compute_diff(old_str, new_str, logical_path.name)
                        except:
                            pass
            except Exception:
                pass

        # 5. THE SIMULATION WARD
        # [FACULTY 7]
        if self.regs.dry_run:
            dry_action = InscriptionAction.DRY_RUN_CREATED if action == InscriptionAction.CREATED else InscriptionAction.DRY_RUN_TRANSFIGURED
            Logger.info(f"[DRY-RUN] Write {logical_path} ({len(final_content_bytes)} bytes)")
            return self._forge_result(
                logical_path, True, dry_action, len(final_content_bytes), new_hash, diff, security_alerts, start_time
            )

        # 6. THE ATOMIC INSCRIPTION
        # [FACULTY 5]
        try:
            # Resolve permissions
            mode = self._resolve_permissions(metadata.get('permissions'))

            bytes_written = self.atomic.inscribe(target_path, final_content_bytes, mode)

            return self._forge_result(
                logical_path, True, action, bytes_written, new_hash, diff, security_alerts, start_time
            )

        except Exception as e:
            # [FACULTY 12] The Unbreakable Ward
            Logger.error(f"Write Paradox: {e}")
            return self._forge_result(
                logical_path, False, InscriptionAction.FAILED_IO, 0, None, None, [str(e)], start_time
            )

    def _forge_result(
            self,
            path: Path,
            success: bool,
            action: InscriptionAction,
            bytes_written: int,
            hash_sig: Optional[str],
            diff: Optional[str],
            alerts: list,
            start_time: float
    ) -> GnosticWriteResult:
        """
        [FACULTY 11] The Luminous Chronicle.
        Forges the standardized result object.
        """
        return GnosticWriteResult(
            success=success,
            path=path,
            action_taken=action,
            bytes_written=bytes_written,
            gnostic_fingerprint=hash_sig,
            diff=diff,
            security_notes=alerts,
            duration_ms=(time.time() - start_time) * 1000
        )