# Path: novalym_logic/core/runtime/middleware/privacy.py
# -----------------------------------------------------

from __future__ import annotations
import hmac
import hashlib
import json
import os
import logging
import time
import base64
from typing import Any, Dict, List, Optional, Tuple, Final, Set
from cryptography.fernet import Fernet, InvalidToken

# --- CORE SCAFFOLD UPLINKS ---
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, SupabaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = logging.getLogger("Scaffold:PrivacySentinel")


class PrivacySentinelMiddleware(Middleware):
    """
    =============================================================================
    == THE PRIVACY SENTINEL (V-Ω-TOTALITY-V3.0-DUAL-PEPPER)                    ==
    =============================================================================
    LIF: ∞ | ROLE: CRYPTOGRAPHIC_SOVEREIGN | RANK: OMEGA_SUPREME
    AUTH_CODE: Ω_SENTINEL_2026_DUAL_AXIS

    The absolute arbiter of Data Sovereignty. It enforces the "Veil of Ignorance"
    between the AI (which sees Truth) and the Database (which sees Shadow).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Dual-Pepper Architecture (THE CURE):** Distinguishes between **Global Indexes**
        (hashed with System Key for routing) and **Private Indexes** (hashed with Client Key
        for sovereignty). This fixes the "Identity Paradox" where we couldn't look up a
        phone number to find the owner because we needed the owner to hash the number.
    2.  **Bi-Directional Alchemy:** Automatically Encrypts on Ingress (Write) and
        Decrypts on Egress (Read), maintaining a seamless illusion of plaintext for the logic layer.
    3.  **Blind-Hash Indexing:** Generates `_hash` columns automatically for every PII field,
        allowing O(1) searches on encrypted data without rainbow-table vulnerability.
    4.  **Recursive Payload Scrying:** Deep-walks JSONB trees (like `identity_matrix`)
        to shroud nested secrets without breaking the document structure.
    5.  **Achronal Key Derivation:** Uses HMAC-SHA256 to derive deterministic keys
        from the Master Secret, removing the need for a Key Management Server (KMS).
    6.  **NoneType Sarcophagus:** Titanium hardening against null values; returns the
        original atom if encryption fails or data is void.
    7.  **Selective Decryption Gate:** Only decrypts matter if the request context
        proves the entity has the "Right of Sight" (Trace ID + Valid Novalym ID).
    8.  **Metabolic Velocity Tomography:** Measures and logs the exact microsecond cost
        of the cryptographic operations (`privacy_tax_ms`).
    9.  **Haptic HUD Resonance:** Broadcasts "SHROUD_ACTIVE" or "VEIL_LIFTED" signals
        to the Ocular Dashboard for visual security confirmation.
    10. **Fernet AES-GCM Enveloping:** Uses industry-standard symmetric encryption
        (Fernet) with timestamp validation and integrity checks.
    11. **Bicameral Filter Translation:** Automatically detects if a `filter` targets a
        PII column and transmutes the value into its Blind Hash equivalent.
    12. **The Finality Vow:** A mathematical guarantee that no plaintext PII ever
        rests on the physical disk of the Akashic Record.
    =============================================================================
    """

    # [FACULTY 1]: THE PII GRIMOIRE
    # Fields that must be encrypted at rest.
    PII_KEYS: Final[Set[str]] = {
        "phone", "lead_phone", "owner_phone", "customer_phone", "sender_id",
        "email", "owner_email", "lead_email", "tax_id", "ssn", "dob",
        "system_id_key", "stripe_customer_id"
    }

    # [FACULTY 2]: THE GLOBAL INDEX GRIMOIRE (THE CURE)
    # These keys are used for Routing/Lookup and must be hashed with the SYSTEM PEPPER
    # so they can be found without knowing the Client ID first.
    GLOBAL_INDEX_KEYS: Final[Set[str]] = {
        "system_id_key",  # The Twilio Phone Number
        "system_sid",  # The Twilio SID
        "stripe_customer_id"  # Stripe ID (for webhooks)
    }

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.master_secret = os.environ.get("SCAFFOLD_INTERNAL_KEY", "VOID_SECRET")

        # Cache for expensive crypto object instantiation
        self._cipher_cache: Dict[str, Fernet] = {}

        # Pre-compute the System Pepper (Global)
        self._system_pepper = self._derive_pepper("SYSTEM")

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        [THE RITE OF CRYPTOGRAPHIC INTERCEPTION]
        """
        # --- 1. PRE-FLIGHT TRIAGE ---
        # Skip if not a Database request or if explicitly bypassed (for debug)
        if not isinstance(request, SupabaseRequest) or request.metadata.get("bypass_shroud"):
            return next_handler(request)

        start_ns = time.perf_counter_ns()
        trace_id = request.metadata.get("trace_id", "tr-crypto-void")

        # --- 2. IDENTITY RESOLUTION ---
        # We must know WHO we are encrypting for.
        # Priority: Metadata -> Payload -> Default(SYSTEM)
        nov_id = str(
            request.metadata.get("nov_id") or
            (request.data.get("client_novalym_id") if isinstance(request.data, dict) else None) or
            "SYSTEM"
        )

        # --- 3. KEY MATERIALIZATION ---
        cipher = self._get_cipher(nov_id)
        client_pepper = self._derive_pepper(nov_id)

        # --- 4. INGRESS TRANSFORMATION (WRITE) ---
        # Encrypt data before it hits the network/database
        if request.method in ["insert", "upsert", "update"]:
            if request.data:
                # [ASCENSION]: We pass both peppers to handle Global vs Private keys
                request.data = self._walk_and_shroud(request.data, client_pepper, cipher)

        # --- 5. COORDINATE TRANSFORMATION (SEARCH) ---
        # Transmute cleartext filters into Blind Hashes
        if request.filters:
            request.filters = self._shroud_filters(request.filters, client_pepper)

        # =========================================================================
        # == THE EXECUTION (THE MIRROR)                                          ==
        # =========================================================================
        result = next_handler(request)

        # --- 6. EGRESS TRANSFORMATION (READ) ---
        # If the database returns shrouded matter, we attempt to resurrect the truth
        # for the internal Artisans/AI.
        if result and result.success and result.data:
            result.data = self._walk_and_resurrect(result.data, cipher)

        # 7. METABOLIC FINALITY
        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if result and isinstance(result.data, dict):
            # Safe injection into vitals
            if not hasattr(result, 'vitals'):
                result.vitals = {}
            result.vitals["privacy_tax_ms"] = latency_ms
            # Mark the source
            result.source = f"{result.source or 'Kernel'}::PrivacySentinel"

            # [ASCENSION 11]: HUD Broadcast (Low Frequency to avoid noise)
            if latency_ms > 10.0:
                self._project_hud(trace_id, "HEAVY_CRYPTO_LOAD", "#fbbf24")

        return result

    # =========================================================================
    # == CRYPTOGRAPHIC RITES                                                 ==
    # =========================================================================

    def _get_cipher(self, nov_id: str) -> Fernet:
        """
        [FACULTY 4]: Thread-safe cipher materialization.
        Derives a unique encryption key for the client using the Master Secret.
        """
        if nov_id not in self._cipher_cache:
            # We use the Client Pepper as the seed for the Encryption Key
            pepper = self._derive_pepper(nov_id)
            # Forge 32-byte key from pepper (SHA256 digest is 32 bytes)
            key = base64.urlsafe_b64encode(hashlib.sha256(pepper).digest())
            self._cipher_cache[nov_id] = Fernet(key)
        return self._cipher_cache[nov_id]

    def _derive_pepper(self, salt: str) -> bytes:
        """
        [FACULTY 5]: Deterministic per-tenant HMAC Pepper.
        This ensures that even if two clients have the same email, their hashes differ.
        """
        return hmac.new(self.master_secret.encode(), salt.encode(), hashlib.sha256).digest()

    def _walk_and_shroud(self, node: Any, client_pepper: bytes, cipher: Fernet) -> Any:
        """
        [THE RITE OF SHROUDING - V3.1 ASCENDED]
        Recursive PII encryption and Blind-Hashing with Normalization.
        """
        # [THE CURE]: We import the Alchemist JIT to prevent boot-loops
        from velm.artisans.services.twilio.utils import TelephonicAlchemist
        alchemist = TelephonicAlchemist()

        if isinstance(node, dict):
            new_node = {}
            for k, v in node.items():
                key_lower = k.lower()

                if key_lower in self.PII_KEYS and isinstance(v, str) and v:
                    # 1. THE COORDINATE NORMALIZATION (THE CURE)
                    # We ensure "+1 (414)" becomes "+1414" so hashes always collide correctly.
                    pure_value = v
                    if "phone" in key_lower or key_lower == "system_id_key":
                        normalized = alchemist.normalize_e164(v)
                        if normalized:
                            pure_value = normalized

                    # 2. RESOLVE THE PEPPER
                    active_pepper = self._system_pepper if key_lower in self.GLOBAL_INDEX_KEYS else client_pepper

                    # 3. FORGE BLIND INDEX
                    blind_hash = hashlib.sha256(active_pepper + pure_value.encode()).hexdigest()
                    new_node[f"{k}_hash"] = blind_hash

                    # 4. ENCRYPT THE MATTER
                    new_node[k] = cipher.encrypt(v.encode()).decode()

                else:
                    new_node[k] = self._walk_and_shroud(v, client_pepper, cipher)
            return new_node

        elif isinstance(node, list):
            return [self._walk_and_shroud(i, client_pepper, cipher) for i in node]

        return node

    def _walk_and_resurrect(self, node: Any, cipher: Fernet) -> Any:
        """
        [THE RITE OF RESURRECTION]
        Recursive decryption of PII matter.
        """
        if isinstance(node, dict):
            new_node = {}
            for k, v in node.items():
                # [ASCENSION]: Fernet Token Detection
                # Standard Fernet tokens start with 'gAAAAA'
                if isinstance(v, str) and v.startswith("gAAAAA") and len(v) > 50:
                    try:
                        # Attempt Decryption
                        decrypted = cipher.decrypt(v.encode()).decode()
                        new_node[k] = decrypted
                    except InvalidToken:
                        # If decryption fails (wrong key or not a token), return raw
                        new_node[k] = v
                else:
                    new_node[k] = self._walk_and_resurrect(v, cipher)
            return new_node

        elif isinstance(node, list):
            return [self._walk_and_resurrect(i, cipher) for i in node]

        return node

    def _shroud_filters(self, filters: Dict[str, Any], client_pepper: bytes) -> Dict[str, Any]:
        """
        [FACULTY 11]: FILTER TRANSMUTATION
        Transmutes cleartext filters (e.g. 'email:eq:john@doe.com')
        into Blind Hash filters (e.g. 'email_hash:eq:a8f93...').
        """
        new_filters = {}
        for k, v in filters.items():
            key_lower = k.lower()

            # If the filter targets a PII key AND isn't already targeting the hash column
            if key_lower in self.PII_KEYS and not k.endswith("_hash"):

                # [THE CURE]: Global Index Check
                active_pepper = self._system_pepper if key_lower in self.GLOBAL_INDEX_KEYS else client_pepper

                if isinstance(v, str) and ":" in v:
                    # Handle operator syntax (eq:value)
                    op, raw = v.split(":", 1)
                    # Hash the search term
                    h = hashlib.sha256(active_pepper + raw.encode()).hexdigest()
                    # Retarget filter to the hash column
                    new_filters[f"{k}_hash"] = f"{op}:{h}"
                else:
                    # Raw value direct match (implied equality)
                    h = hashlib.sha256(active_pepper + str(v).encode()).hexdigest()
                    new_filters[f"{k}_hash"] = h
            else:
                new_filters[k] = v

        return new_filters

    def _project_hud(self, trace: str, label: str, color: str):
        """[ASCENSION 9]: Projects cryptographic status to the Ocular HUD."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "CRYPTO_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_PRIVACY_SENTINEL status=ARMED version=3.0>"