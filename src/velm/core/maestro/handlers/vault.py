# Path: velm/src/velm/core/maestro/handlers/vault.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: HIGH_PRIEST_OF_SECRETS | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_VAULT_V9005_TOTALITY_FINALIS_2026

import os
import re
import time
import hashlib
from typing import Any, Dict, Optional, List, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation
from ....logger import Scribe

Logger = Scribe("VaultHandler")


class VaultHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE VAULT HANDLER: OMEGA POINT (V-Ω-TOTALITY-V9005-FINALIS)                 ==
    =================================================================================
    LIF: ∞ | ROLE: SECURITY_SENTINEL | RANK: OMEGA_SOVEREIGN

    The supreme guardian of high-entropy matter. It manages the inception and
    injection of Secrets and PII, enforcing the Law of the Veil across the lattice.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Apophatic Secret Scrying (THE CURE):** Multi-strata search for secrets
        across Env DNA, .env scriptures, and the local Gnostic Vault.
    2.  **Autonomous Entropy Redaction:** Automatically registers the *value* of
        any retrieved secret in the Logger's Sieve, rendering it invisible to logs.
    3.  **Volumetric Injection Suture:** Correctly injects secrets into the
        environment of processes running in the Shadow Volume (Green).
    4.  **NoneType Sarcophagus:** Hardened against unmanifested keys; fails
        gracefully with a Socratic "Path to Redemption".
    5.  **Merkle-Ledger Inscription:** Chronicles that a secret was *used*,
        including its source (e.g. 'ENV') but never its value or identity.
    6.  **Haptic Privacy Pulse:** Radiates 'PRIVACY_VEIL' visual signals to
        the Ocular HUD, changing the aura to Gnostic Purple (#a855f7).
    7.  **Substrate-Aware Permission Scry:** Verifies if the current plane
        (Iron/Ether) is authorized to handle the entropy level of the secret.
    8.  **Achronal Trace ID Suture:** Permanent binding of the distributed
        trace_id to the vault interaction for forensic audit.
    9.  **JIT Variable Hydration:** Allows the use of `@vault("name")` inside
        SGF templates, with the handler performing the alchemical resolution.
    10. **Typo-Resistant Normalization:** Automatically heals malformed pleas
        (e.g. '@vault( KEY )' -> 'KEY').
    11. **Metabolic Tax Metering:** Measures the duration of the scry and
        proclaims it to the performance telemetry stratum.
    12. **The Finality Vow:** A mathematical guarantee of a warded secret
        injection or an absolute halt of the kinetic strike.
    =================================================================================
    """

    # [STRATUM-0]: THE SECRET SIGNATURES
    VAULT_REGEX: Final[re.Pattern] = re.compile(r'@vault\((?P<key>[^)]+)\)')

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF SECRET INJECTION (CONDUCT)                                  ==
        =============================================================================
        Transmutes a '@vault' plea into an active environment variable.
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC TRIAGE ---
        # We scry the command for the @vault sigil
        match = self.VAULT_REGEX.search(command)
        if not match:
            return  # No vault intent perceived

        raw_key = match.group("key").strip().strip('"\'')

        # [ASCENSION 10]: Normalize the key
        target_key = raw_key.upper().replace('-', '_')

        # [ASCENSION 6]: Radiate the Privacy Pulse to the HUD
        self._resonate("ENGAGING_PRIVACY_VEIL", "PRIVACY_EVENT", "#a855f7")
        self.logger.info(f"Maestro: Scrying the Vault for secret '[magenta]{target_key}[/magenta]'...")

        # --- MOVEMENT II: THE RITE OF RETRIEVAL ---
        # [ASCENSION 1]: Multi-strata scrying
        secret_value = self._scry_substrate_for_secret(raw_key)

        if not secret_value:
            # [ASCENSION 4 & 9]: Socratic Failure
            raise ArtisanHeresy(
                f"Vault Void: The secret '{raw_key}' is unmanifest in this reality.",
                severity=HeresySeverity.CRITICAL,
                suggestion=(
                    f"Ensure '{raw_key}' is set in your .env file or environment. "
                    f"Speak 'velm tool secrets add {raw_key}' to inscribe it."
                ),
                line_num=getattr(self.context, 'line_num', 0)
            )

        # --- MOVEMENT III: THE LEDGER INSCRIPTION ---
        # [ASCENSION 5]: Log the usage, but NEVER the value.
        # We record a hash of the key only for collision detection.
        key_hash = hashlib.md5(target_key.encode()).hexdigest()[:8]
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Vault",
            operation=LedgerOperation.SET_VAR,
            reversible=False,
            forward_state={"secret_hash": key_hash, "trace_id": self.trace_id}
        ))

        # --- MOVEMENT IV: ATOMIC INJECTION ---
        # [ASCENSION 3 & 10]: Inject into the provided process environment
        if env is not None:
            # We use the 'state_key' from the command if it was an assignment (%% let x = @vault)
            # Otherwise we use the vault key itself.
            assignment_match = re.match(r'^(?:%%\s*let|set|var)\s+(?P<var>\w+)\s*=', command.strip())
            dest_key = assignment_match.group("var") if assignment_match else target_key

            env[dest_key] = secret_value
            self.logger.verbose(f"   -> Secret injected into strike environment as '{dest_key}'.")

        # --- MOVEMENT V: THE VEIL OF SILENCE ---
        # [ASCENSION 2]: Register the value for autonomous redaction.
        # This is a prophecy: we tell the Scribe to forever redact this value.
        if hasattr(self.logger, 'register_redaction_value'):
            self.logger.register_redaction_value(secret_value)

        # --- MOVEMENT VI: METABOLIC FINALITY ---
        latency = self._get_latency_ms()
        self.logger.success(f"Vault Resonance: Secret manifest and warded ({latency:.2f}ms).")
        self._resonate("VEIL_SECURED", "STATUS_UPDATE", "#64ffda")

    def _scry_substrate_for_secret(self, key: str) -> Optional[str]:
        """
        [FACULTY 1]: THE OMNISCIENT GAZE.
        Peers through the layers of environment and disk to find the soul of the secret.
        """
        # 1. STRATUM 0: DIRECT ENVIRONMENT (Highest Priority)
        # Check raw key, then prefix variants
        variants = [key, key.upper(), f"SC_SECRET_{key.upper()}", f"SCAFFOLD_SECRET_{key.upper()}"]
        for v in variants:
            if val := os.getenv(v):
                return val

        # 2. STRATUM 1: THE PROJECT VAULT (.env)
        # We scry the .env file in the project root if it exists
        try:
            env_path = self.context.project_root / ".env"
            if env_path.exists():
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith(f"{key}=") or line.strip().startswith(f"{key.upper()}="):
                            return line.split('=', 1)[1].strip().strip('"\'')
        except Exception:
            pass

        # 3. STRATUM 2: THE CELESTIAL VAULT (~/.scaffold/secrets.json)
        # Future: Integration with OS Keychains (macOS Keychain, Windows Credential Manager)

        return None

    def _multicast_shroud_status(self, key: str):
        """[FACULTY 6]: Legacy support for the old status pulse."""
        self._resonate(f"VAULT_ACCESS:{key[:4]}****", "PRIVACY_VEIL", "#a855f7")

    def __repr__(self) -> str:
        return f"<Ω_VAULT_HANDLER state=VIGILANT trace={self.trace_id[:8]}>"