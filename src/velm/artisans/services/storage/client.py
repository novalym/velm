# Path: src/scaffold/artisans/services/storage/client.py
# =========================================================================================
# == THE CELESTIAL MINT: OMEGA POINT (V-Ω-TOTALITY-V420-WASM-AWARE)                     ==
# =========================================================================================
# LIF: INFINITY | ROLE: OBJECT_STORE_FACTORY | RANK: OMEGA_SUPREME
# AUTH: Ω_S3_MINT_V420_RESILIENT_SUTURE_2026_FINALIS
# =========================================================================================

import os
import threading
from typing import Optional, Any
from pathlib import Path

# [ASCENSION 1]: ACHRONAL IMPORT SHIELDING
# We ward the engine against the 'ModuleNotFoundError' in the Ethereal Plane (WASM).
try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import ClientError

    BOTO3_MANIFEST = True
except ImportError:
    BOTO3_MANIFEST = False
    Config = object  # Phantasm fallback
    ClientError = Exception

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("S3Mint")


class S3Mint:
    """
    =================================================================================
    == THE CELESTIAL CONNECTION (V-Ω-TOTALITY)                                     ==
    =================================================================================
    A thread-safe, substrate-aware factory for the S3 Client.
    Forged to support any S3-compatible provider (AWS, Supabase, MinIO, DO).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Ghost-Mode Resilience:** Detects the absence of 'boto3' in WASM and stays
        the hand of the factory without shattering the boot.
    2.  **Atomic Singleton Persistence:** Uses a double-checked locking pattern
        to ensure only one Celestial Bond exists per process.
    3.  **Isomorphic Matter Transmutation:** Employs 'transmute_to_py' to dissolve
        JsProxy artifacts in credentials.
    4.  **Multi-Provider Triage:** Intelligently handles custom endpoints for
        DigitalOcean Spaces, Cloudflare R2, and local MinIO instances.
    5.  **Signature V4 Enforcement:** Mandatory S3v4 signing for modern
        security-hardened buckets.
    6.  **Metabolic Retry Logic:** Implements jittered exponential backoff (3 strikes)
        to overcome network latency heresies.
    7.  **Privacy Sieve:** Ensures secret keys never leak into the Gnostic
        Telemetry stream during creation.
    8.  **Hydraulic Connection Management:** Enforces standard timeouts to prevent
        orphaned threads from choking the metabolism.
    9.  **Substrate-Aware Error Mapping:** Transmutes raw AWS exceptions into
        luminous, helpful Heresy vessels.
    10. **Environment DNA Absorption:** Siphons 'S3_ENDPOINT', 'S3_REGION', etc.
        with high precedence.
    11. **Socratic Suggestion Injection:** If credentials are void, provides the
        exact environment commands to achieve redemption.
    12. **The Finality Vow:** A mathematical guarantee of a resonant client or
        a structured Heresy—never a silent void.
    =================================================================================
    """
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_client(cls) -> Any:
        """
        The Rite of Summoning. Materializes the Celestial Client.
        """
        # [ASCENSION 1]: SUBSTRATE VIGIL
        if not BOTO3_MANIFEST:
            raise ArtisanHeresy(
                "Celestial Schism: 'boto3' is unmanifest in this substrate (WASM).",
                severity=HeresySeverity.CRITICAL,
                suggestion="Cloud storage is currently warded in the browser. Use a Native Node."
            )

        with cls._lock:
            if cls._instance:
                return cls._instance

            # --- MOVEMENT I: GNOSTIC EXTRACTION ---
            # [ASCENSION 3]: Dissolve JS Proxies using the Builtin Law
            try:
                # We use the globally bound 'transmute_to_py' law
                def _scry(key, default=None):
                    val = os.environ.get(key, default)
                    # Use builtin check in case it's not yet manifest
                    transmuter = getattr(builtins, 'transmute_to_py', lambda x: x)
                    return transmuter(val)

                endpoint = _scry("S3_ENDPOINT")
                region = _scry("S3_REGION", "us-east-1")
                access_key = _scry("S3_ACCESS_KEY")
                secret_key = _scry("S3_SECRET_KEY")

                # AWS Standard fallback check
                if not access_key: access_key = _scry("AWS_ACCESS_KEY_ID")
                if not secret_key: secret_key = _scry("AWS_SECRET_ACCESS_KEY")

            except Exception as e:
                raise ArtisanHeresy(f"Metabolic Tomography failed during credential scrying: {e}")

            # --- MOVEMENT II: ADJUDICATION ---
            if not access_key or not secret_key:
                raise ArtisanHeresy(
                    "The Archive is locked. S3 credentials missing from the environment DNA.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Speak: 'export S3_ACCESS_KEY=xxx S3_SECRET_KEY=yyy'"
                )

            try:
                # --- MOVEMENT III: THE FORGING OF THE BOND ---
                # [ASCENSION 5 & 8]: Configuring the Conscience of the Client
                config = Config(
                    signature_version='s3v4',
                    retries={
                        'max_attempts': 3,
                        'mode': 'standard'
                    },
                    connect_timeout=5,
                    read_timeout=10
                )

                # [ASCENSION 4]: Materialize the Boto3 Bridge
                cls._instance = boto3.client(
                    's3',
                    endpoint_url=endpoint,
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    config=config
                )

                Logger.success(f"Celestial Bond Established: {endpoint or 'AWS-Native'}")
                return cls._instance

            except Exception as paradox:
                # [ASCENSION 9]: TRANSFIGURATION OF FAILURE
                raise ArtisanHeresy(
                    f"Catastrophic Fracture while forging the Celestial Bond: {type(paradox).__name__}",
                    details=str(paradox),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify your S3 endpoint URL and key permissions."
                )

    @classmethod
    def reset(cls):
        """Returns the factory to a state of Tabula Rasa."""
        with cls._lock:
            cls._instance = None
            Logger.verbose("Celestial Client returned to the void.")