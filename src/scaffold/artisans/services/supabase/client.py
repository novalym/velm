# Path: scaffold/artisans/services/supabase/client.py
# --------------------------------------------------

from __future__ import annotations
import os
import time
import logging
import threading
from typing import Optional, Dict, Any, Final

# --- TWILIO / SUPABASE DRIVERS ---
try:
    from supabase import create_client, Client

    SUPABASE_SDK_READY = True
except ImportError:
    SUPABASE_SDK_READY = False
    Client = object

# --- CORE SCAFFOLD UPLINKS ---
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe


# =============================================================================
# == THE SOVEREIGN AKASHIC LINK (V-Ω-TOTALITY-V2026-TITANIUM-REFORGED)       ==
# =============================================================================
# LIF: ∞ | ROLE: DATA_ACCESS_AUTHORITY | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_SB_SECRET_TOTALITY_2026_FINALIS

class SupabaseConnection:
    """
    =============================================================================
    == THE SILVER CORD (V-Ω-TOTALITY-V2026-TITANIUM-REFORGED)                  ==
    =============================================================================
    The definitive, self-healing conductor for the Akashic Record.
    This version annihilates the legacy split-key model in favor of the 
    'sb_secret' protocol, ensuring absolute data sovereignty.
    """

    _instance: Optional[Client] = None
    _lock: Final[threading.RLock] = threading.RLock()
    _last_checked: float = 0.0
    _version: Final[str] = "2026.1.3-TOTALITY"

    @classmethod
    def get_client(cls) -> Client:
        """
        =============================================================================
        == THE RITE OF SUMMONS                                                     ==
        =============================================================================
        Materializes the Sovereign Client using the modern Secret Key protocol.
        Guarantees O(1) retrieval after the first successful handshake.
        """
        # 0. VITALITY CHECK
        if not SUPABASE_SDK_READY:
            raise ArtisanHeresy(
                "Supabase SDK not manifest in the environment.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Execute: `pip install supabase` to heal the environment."
            )

        # 1. ATOMIC SINGLETON MUTEX
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking to prevent race-condition inception
                if cls._instance is None:
                    cls._conduct_inception_rite()

        return cls._instance

    @classmethod
    def _conduct_inception_rite(cls):
        """
        [THE INTERNAL INCEPTION]
        Screams to the environment DNA to find the God-Keys.
        """
        logger = Scribe("Kernel::SupabaseClient")

        # 1. HARVEST DNA
        # We prioritize the new SUPABASE_SECRET protocol over legacy keys.
        url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
        secret = (
                os.environ.get("SUPABASE_SECRET") or
                os.environ.get("SB_SECRET") or
                os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        )

        # 2. NONE-TYPE SARCOPHAGUS
        if not url or not secret:
            raise ArtisanHeresy(
                "Akashic Credentials Missing: The Silver Cord cannot be forged.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Inject NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SECRET into the environment.",
                details=f"URL_STATUS: {'FOUND' if url else 'VOID'} | SECRET_STATUS: {'FOUND' if secret else 'VOID'}"
            )

        # 3. KINETIC MATERIALIZATION
        try:
            start_time = time.perf_counter()

            # [THE APOTHEOSIS]: Creating the connection with total authority
            # We explicitly strip whitespace to prevent copy-paste heresies
            cls._instance = create_client(url.strip(), secret.strip())

            latency = (time.perf_counter() - start_time) * 1000
            logger.success(f"Akashic Uplink Resonant. Latency: {latency:.2f}ms.")

            # 4. HAPTIC HUD MULTICAST (Prophetic)
            # If the engine is manifest, we notify the React Stage
            cls._broadcast_vitality(True)

        except Exception as e:
            cls._broadcast_vitality(False)
            raise ArtisanHeresy(
                f"Failed to forge Silver Cord to Supabase: {str(e)}",
                severity=HeresySeverity.CRITICAL,
                details=traceback.format_exc(),
                suggestion="Verify that the sb_secret_ matches your project settings and IP restrictions."
            )

    @classmethod
    def clear(cls):
        """
        [THE RITE OF DISSOLUTION]
        Returns the connection to the void. Mandatory for hot-swapping Strata.
        """
        with cls._lock:
            cls._instance = None
            Logger = Scribe("Kernel::SupabaseClient")
            Logger.info("Akashic Link Severed. Memory Purified.")

    @classmethod
    def _broadcast_vitality(cls, success: bool):
        """Projects vitality telemetry to the global state if available."""
        try:
            # We look for a global 'akashic' broadcaster (standard in Novalym Daemon)
            from ....api.state import GlobalState
            engine = GlobalState.get_engine()
            if engine and hasattr(engine, 'akashic') and engine.akashic:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "AKASHIC_UPLINK",
                        "status": "RESONANT" if success else "FRACTURED",
                        "color": "#64ffda" if success else "#ef4444",
                        "timestamp": time.time()
                    }
                })
        except:
            pass  # Pulse is non-essential for the core strike

    def __repr__(self) -> str:
        return f"<Ω_SUPABASE_CONNECTION version={self._version} status={'RESONANT' if self._instance else 'VOID'}>"

# == SCRIPTURE SEALED: THE SILVER CORD IS UNBREAKABLE ==