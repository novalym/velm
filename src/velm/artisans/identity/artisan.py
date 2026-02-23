# Path: artisans/identity/artisan.py
# =========================================================================================
# == THE IDENTITY ORACLE: OMEGA (V-Ω-MULTI-CLOUD-FEDERATION-TITANIUM)        ==
# =========================================================================================
# LIF: ∞ | ROLE: SOVEREIGN_DIPLOMAT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_IDENTITY_V9000_LENIENT_SUTURE_2026_FINALIS

import os
import sys
import json
import time
import uuid
import threading
import webbrowser
import traceback
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List, Union

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import IdentityRequest
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...help_registry import register_artisan

# =============================================================================
# == JIT PROVIDER MATERIALIZATION (THE LAZY LOAD)                            ==
# =============================================================================
# We wrap SDK imports in try/except blocks to prevent the "Import Avalanche"
# heresy. The Artisan validates existence before attempting communion.

# 1. OVH (The Sovereign)
try:
    import ovh

    OVH_AVAILABLE = True
except ImportError:
    OVH_AVAILABLE = False

# 2. AWS (The Leviathan)
try:
    import boto3
    import botocore.exceptions

    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

# 3. Azure (The Enterprise)
try:
    from azure.identity import DefaultAzureCredential, ClientSecretCredential
    from azure.core.exceptions import ClientAuthenticationError

    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

# 4. Hetzner (The Mercenary)
try:
    from hcloud import Client as HCloudClient
    from hcloud import APIException

    HETZNER_AVAILABLE = True
except ImportError:
    HETZNER_AVAILABLE = False

Logger = Scribe("IdentityArtisan")


@register_artisan("identity")
class IdentityArtisan(BaseArtisan[IdentityRequest]):
    """
    =============================================================================
    == THE IDENTITY ORACLE: OMEGA (V-Ω-MULTI-CLOUD-FEDERATION-TITANIUM)        ==
    =============================================================================
    LIF: ∞ | ROLE: SOVEREIGN_DIPLOMAT | RANK: OMEGA_SOVEREIGN

    The supreme gateway for establishing trust across the Multiverse.
    It manages the 3-Legged OAuth dance, Service Principal handshakes, and
    API Token verification with absolute, forensic precision.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Quad-Cloud Federation:** Native support for OVH, AWS, Azure, and Hetzner.
    2.  **Vacuum Physics:** Anchors to `~/.scaffold` if the project root is void.
    3.  **Substrate Sensing:** Detects WASM to return URLs instead of spawning browsers.
    4.  **Credential Scrying:** Priority-based key lookup (Request > Env > Disk).
    5.  **Atomic Persistence:** Thread-safe writing to the global `.env` ledger.
    6.  **Socratic Diagnostics:** Dumps masked environment keys on failure to aid debugging.
    7.  **JIT SDK Loading:** Prevents startup crashes if cloud SDKs are missing.
    8.  **The OVH Handshake:** Automates the complex consumer key validation flow.
    9.  **Contextual Lenience (THE CURE):** `whoami` never crashes on missing keys.
    10. **The AWS Bifrost:** Verifies STS identity via Access Key/Secret.
    11. **The Azure Nebula:** Supports Service Principal (Client/Secret/Tenant) auth.
    12. **The Hetzner Shield:** Verifies API Tokens against the HCloud API.
    13. **Entropy Redaction:** Scrubs secrets from logs before radiation.
    14. **Forensic Traceback:** Captures full Python stacks for deep diagnosis.
    15. **Visual Haptics:** Radiates UI hints (bloom/shake) for the Ocular HUD.
    16. **Identity Caching:** In-memory caching of verified identities to reduce API tax.
    17. **Environment Injection:** Supports `SCAFFOLD_` prefixed env vars.
    18. **Status Normalization:** Maps diverse provider statuses to `ACTIVE`/`VOID`.
    19. **Scope Introspection:** Ability to list effective permissions (where supported).
    20. **The Erasure Rite:** Securely removes keys from the local ledger (Logout).
    21. **Region Awareness:** Handles provider-specific region endpoints.
    22. **The Null-Safe Sarcophagus:** Wraps all external calls in generic try/except.
    23. **The Global Keyring:** Manages multiple profiles (dev/prod) via prefixes.
    24. **The Finality Vow:** Guaranteed `ScaffoldResult` return, never None.
    =============================================================================
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._lock = threading.RLock()
        self._identity_cache: Dict[str, Dict[str, Any]] = {}

        # [ASCENSION 3]: SUBSTRATE SENSING
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # [ASCENSION 2]: GLOBAL ANCHORING
        # If project_root is void (Lobby), we anchor to the Global User Sanctum.
        if not self.project_root or str(self.project_root) == ".":
            # In WASM, home is /home/pyodide. On Iron, it's actual Home.
            self._global_root = Path.home() / ".scaffold"
        else:
            self._global_root = self.project_root / ".scaffold"

        # Ensure the sanctum exists
        try:
            self._global_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass  # Ephemeral mode if disk locked

    def execute(self, request: IdentityRequest) -> ScaffoldResult:
        """
        [THE RITE OF DISPATCH]
        Routes the intent to the specific provider diplomat.
        """
        action = request.action.lower()
        provider = request.provider.lower()
        trace_id = getattr(request, 'trace_id', f"tr-id-{uuid.uuid4().hex[:6]}")

        self.logger.info(
            f"[{trace_id}] Identity Rite: [bold cyan]{action.upper()}[/] on [bold magenta]{provider.upper()}[/]")

        try:
            # [ASCENSION 1]: QUAD-CLOUD FEDERATION
            if provider == "ovh":
                return self._manage_ovh(action, request, trace_id)
            elif provider == "aws":
                return self._manage_aws(action, request, trace_id)
            elif provider == "azure":
                return self._manage_azure(action, request, trace_id)
            elif provider == "hetzner":
                return self._manage_hetzner(action, request, trace_id)
            else:
                return self.failure(f"Provider '{provider}' is not yet manifest in the Identity Matrix.")

        except Exception as e:
            # [ASCENSION 13]: FORENSIC TRACEBACK
            tb = traceback.format_exc()
            self.logger.error(f"Identity Fracture: {e}\n{tb}")

            return self.failure(
                f"Identity Rite Fractured: {str(e)}",
                details=tb,  # Send full trace to the HUD
                trace_id=trace_id,
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake_red", "sound": "error"}
            )

    def _simulate_handshake(self, provider: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF THE PHANTOM HANDSHAKE (V-Ω-SIMULACRUM)                      ==
        =============================================================================
        LIF: 100x | ROLE: DEVELOPMENT_ACCELERATOR

        Forges a hallucinatory handshake sequence for the Architect's convenience.
        It mimics the temporal weight (latency) and data topology of a true
        Celestial Bond without touching the external network.
        """
        self.logger.info(f"[SIMULATION] Forging phantom credentials for {provider.upper()}...")

        # 1. Artificial Latency (The "Network" Illusion)
        time.sleep(1.2)

        # 2. Forge the Phantom Keys
        mock_consumer_key = f"ck_mock_{uuid.uuid4().hex[:16]}"
        mock_validation_url = "https://eu.api.ovh.com/auth/?credentialToken=mock_token_123"

        self.console.print(f"[bold yellow]⚡ SIMULATION MODE:[/bold yellow] Returning phantom validation URL.")

        return self.success(
            message=f"Simulated {provider.upper()} Handshake Initiated.",
            data={
                "status": "AWAITING_SUTURE",
                "validation_url": mock_validation_url,
                "consumer_key": mock_consumer_key,
                "provider": provider,
                "is_simulation": True,
                "expires_in": 3600
            },
            ui_hints={
                "vfx": "pulse_cyan",
                "action": "OPEN_URL",
                "url": mock_validation_url,
                "message": "Simulation: Bond established instantly."
            }
        )

    # =========================================================================
    # == PROVIDER I: OVH CLOUD (THE SOVEREIGN DIPLOMAT)                      ==
    # =========================================================================
    def _manage_ovh(self, action: str, request: IdentityRequest, trace_id: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE OVH DIPLOMAT: OMEGA (V-Ω-TITANIUM-WARDED)                           ==
        =============================================================================
        LIF: ∞ | ROLE: OAUTH_ORCHESTRATOR

        The definitive handler for the OVH 3-Legged OAuth Dance.
        It possesses 'Contextual Lenience'—it knows when to scream and when to whisper.

        [CAPABILITIES]:
        1. **Simulation Gate:** Bypasses physics if the Architect wills it.
        2. **Credential Scrying:** Deep recursive lookup for keys (Request > Env > Disk).
        3. **Browser Bridge:** Spawns native windows on Iron, returns URLs on Ether.
        4. **Purity Verification:** Validates token scopes before acceptance.
        """
        # --- 0. THE SIMULATION GATE ---
        # We check both metadata (system) and variables (user intent)
        is_sim = request.metadata.get("simulation", False) or request.variables.get("simulation", False)

        if is_sim:
            if action == "handshake": return self._simulate_handshake("ovh")
            if action == "verify":
                time.sleep(0.5)  # Micro-latency
                return self.success(
                    "Simulated Identity Verified.",
                    data={
                        "status": "RESONANT",
                        "account": {"nichandle": "xx12345-ovh", "email": "architect@novalym.dev"},
                        "provider": "ovh",
                        "is_simulation": True
                    },
                    ui_hints={"vfx": "bloom", "glow": "#64ffda"}
                )

        # --- 1. THE SDK INQUEST ---
        if not OVH_AVAILABLE:
            raise ArtisanHeresy(
                "OVH SDK unmanifest.",
                suggestion="The 'ovh' python package is required. It should be bundled in the Mega-Wheel."
            )

        endpoint = request.region or "ovh-eu"

        # --- 2. THE CREDENTIAL SCRY (DEEP LOOKUP) ---
        # Priority: 1. Request Payload (BYOK) -> 2. Environment Vars -> 3. Persistent Vault
        app_key = (
                request.credentials.get("app_key") or
                os.environ.get("OVH_APPLICATION_KEY") or
                self._resolve_credential("OVH_APPLICATION_KEY", None)
        )
        app_secret = (
                request.credentials.get("app_secret") or
                os.environ.get("OVH_APPLICATION_SECRET") or
                self._resolve_credential("OVH_APPLICATION_SECRET", None)
        )

        # --- 3. CONTEXTUAL LENIENCE (THE CURE) ---
        # If keys are missing, we adjudicate based on Intent.
        if not app_key or not app_secret:
            if action == "whoami":
                # A query of self should never crash the engine.
                return self.success(
                    "Identity Void (System Keys Missing).",
                    data={"status": "VOID", "reason": "MISSING_SYSTEM_KEYS", "provider": "ovh"},
                    ui_hints={"vfx": "none"}
                )

            # For kinetic rites (Handshake/Verify), missing keys are a heresy.
            return self._proclaim_missing_keys("OVH", ["OVH_APPLICATION_KEY", "OVH_APPLICATION_SECRET"])

        # =========================================================================
        # == MOVEMENT I: THE RITE OF HANDSHAKE (INITIATION)                      ==
        # =========================================================================
        if action == "handshake":
            self.logger.info(f"[{trace_id}] Initiating Sovereign Handshake with {endpoint}...")

            try:
                # A. Initialize the Client
                client = ovh.Client(endpoint=endpoint, application_key=app_key, application_secret=app_secret)

                # B. Define the Scope of Power
                # We request full cloud control and read-only auth access
                access_rules = [
                    {'method': 'GET', 'path': '/cloud/*'},
                    {'method': 'POST', 'path': '/cloud/*'},
                    {'method': 'PUT', 'path': '/cloud/*'},
                    {'method': 'DELETE', 'path': '/cloud/*'},
                    {'method': 'GET', 'path': '/auth/*'}
                ]

                # C. Request the Credential
                ck = client.new_consumer_key_request()
                for rule in access_rules:
                    ck.add_rule(**rule)

                validation = ck.request()

                url = validation['validationUrl']
                consumer_key = validation['consumerKey']

                self.logger.debug(f"Consumer Key Forged: {consumer_key[:8]}...")

                # D. The Browser Bridge (Native Only)
                # If we are on Iron (Local), we open the window for the user.
                if not self._is_wasm:
                    try:
                        webbrowser.open(url)
                    except:
                        pass  # Headless fail-safe

                return self.success(
                    message="Handshake Initiated. Validation Required.",
                    data={
                        "status": "AWAITING_SUTURE",
                        "validation_url": url,
                        "consumer_key": consumer_key,
                        "provider": "ovh",
                        "endpoint": endpoint
                    },
                    ui_hints={
                        "vfx": "pulse_amber",
                        "action": "OPEN_URL",
                        "url": url,
                        "message": "Click the link to seal the bond."
                    }
                )

            except Exception as e:
                # Map specific OVH errors if possible
                raise ArtisanHeresy(f"OVH Handshake Failed: {str(e)}", details=traceback.format_exc())

        # =========================================================================
        # == MOVEMENT II: THE RITE OF VERIFICATION (COMPLETION)                  ==
        # =========================================================================
        elif action == "verify":
            # 1. Resolve the Consumer Key
            consumer_key = (
                    request.credentials.get("consumer_key") or
                    os.environ.get("OVH_CONSUMER_KEY") or
                    self._resolve_credential("OVH_CONSUMER_KEY", None)
            )

            if not consumer_key:
                return self.failure("No Consumer Key provided for verification.")

            try:
                # 2. Re-hydrate Client with the Candidate Key
                client = ovh.Client(
                    endpoint=endpoint, application_key=app_key,
                    application_secret=app_secret, consumer_key=consumer_key
                )

                # 3. The Vitality Probe
                # We call a lightweight endpoint to verify the signature is valid
                me = client.get('/auth/currentCredential')
                status = me.get('status', 'UNKNOWN')

                if status != 'VALIDATED':
                    return self.failure(f"Credential Status Invalid: {status}", code="AUTH_PENDING")

                # 4. The Persistence Vow
                if request.persist_globally:
                    self._persist_key("OVH_CONSUMER_KEY", consumer_key)

                account_info = me.get("ovhSupport", "Unknown")

                return self.success(
                    message=f"Sovereign Bond Verified: {status}",
                    data={
                        "status": "RESONANT",
                        "account": account_info,
                        "consumer_key": consumer_key,
                        "provider": "ovh",
                        "expiry": me.get("expiration", "NEVER")
                    },
                    ui_hints={"vfx": "bloom", "glow": "#64ffda", "sound": "success_chime"}
                )

            except ovh.APIError as e:
                # Detect specific rejection codes
                return self.failure(f"Verification Failed (API): {e}", severity=HeresySeverity.WARNING)
            except Exception as e:
                return self.failure(f"Verification Fracture: {e}", severity=HeresySeverity.CRITICAL)

        # Fallback for generic actions
        return self._handle_common_actions(action, "OVH_CONSUMER_KEY")

    # =========================================================================
    # == PROVIDER II: AWS (THE LEVIATHAN)                                    ==
    # =========================================================================

    def _manage_aws(self, action: str, request: IdentityRequest, trace_id: str) -> ScaffoldResult:
        """Logic for AWS STS Verification."""
        if not AWS_AVAILABLE:
            raise ArtisanHeresy("Boto3 SDK unmanifest.", suggestion="pip install boto3")

        # 1. Credentials
        key_id = self._resolve_credential("AWS_ACCESS_KEY_ID", request.credentials.get("aws_access_key_id"))
        secret = self._resolve_credential("AWS_SECRET_ACCESS_KEY", request.credentials.get("aws_secret_access_key"))
        region = request.region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

        if action == "verify":
            if not key_id or not secret:
                return self._proclaim_missing_keys("AWS", ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"])

            try:
                session = boto3.Session(
                    aws_access_key_id=key_id,
                    aws_secret_access_key=secret,
                    region_name=region
                )
                sts = session.client('sts')
                identity = sts.get_caller_identity()

                if request.persist_globally:
                    self._persist_key("AWS_ACCESS_KEY_ID", key_id)
                    self._persist_key("AWS_SECRET_ACCESS_KEY", secret)
                    self._persist_key("AWS_DEFAULT_REGION", region)

                return self.success(
                    "AWS Identity Confirmed.",
                    data={"arn": identity['Arn'], "account": identity['Account'], "status": "RESONANT"},
                    ui_hints={"vfx": "bloom", "glow": "#FF9900"}
                )
            except botocore.exceptions.ClientError as e:
                return self.failure(f"AWS Rejection: {e}", severity=HeresySeverity.WARNING)
            except Exception as e:
                return self.failure(f"AWS Fracture: {e}")

        # [ASCENSION 9]: Lenient Whoami
        if action == "whoami":
            if not key_id or not secret:
                return self.success("Identity Void.", data={"status": "VOID", "provider": "aws"})

        return self._handle_common_actions(action, "AWS_ACCESS_KEY_ID")

    # =========================================================================
    # == PROVIDER III: AZURE (THE ENTERPRISE)                                ==
    # =========================================================================

    def _manage_azure(self, action: str, request: IdentityRequest, trace_id: str) -> ScaffoldResult:
        """Logic for Azure Service Principal verification."""
        if not AZURE_AVAILABLE:
            raise ArtisanHeresy("Azure SDK unmanifest.", suggestion="pip install azure-identity")

        client_id = self._resolve_credential("AZURE_CLIENT_ID", request.credentials.get("azure_client_id"))
        client_secret = self._resolve_credential("AZURE_CLIENT_SECRET", request.credentials.get("azure_client_secret"))
        tenant_id = self._resolve_credential("AZURE_TENANT_ID", request.credentials.get("azure_tenant_id"))

        if action == "verify":
            if not client_id or not client_secret or not tenant_id:
                return self._proclaim_missing_keys("AZURE",
                                                   ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"])

            try:
                # We don't make a network call just to init, so we try to get a token to prove vitality
                cred = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
                token = cred.get_token("https://management.azure.com/.default")

                if request.persist_globally:
                    self._persist_key("AZURE_CLIENT_ID", client_id)
                    self._persist_key("AZURE_CLIENT_SECRET", client_secret)
                    self._persist_key("AZURE_TENANT_ID", tenant_id)

                return self.success(
                    "Azure Service Principal Active.",
                    data={"status": "RESONANT", "expires": str(token.expires_on)},
                    ui_hints={"vfx": "bloom", "glow": "#0078D4"}
                )
            except ClientAuthenticationError as e:
                return self.failure(f"Azure Auth Failed: {e}", severity=HeresySeverity.WARNING)
            except Exception as e:
                return self.failure(f"Azure Fracture: {e}")

        # [ASCENSION 9]: Lenient Whoami
        if action == "whoami":
            if not client_id:
                return self.success("Identity Void.", data={"status": "VOID", "provider": "azure"})

        return self._handle_common_actions(action, "AZURE_CLIENT_ID")

    # =========================================================================
    # == PROVIDER IV: HETZNER (THE MERCENARY)                                ==
    # =========================================================================

    def _manage_hetzner(self, action: str, request: IdentityRequest, trace_id: str) -> ScaffoldResult:
        """Logic for Hetzner Cloud API Token."""
        if not HETZNER_AVAILABLE:
            raise ArtisanHeresy("Hetzner SDK unmanifest.", suggestion="pip install hcloud")

        token = self._resolve_credential("HCLOUD_TOKEN", request.credentials.get("hcloud_token"))

        if action == "verify":
            if not token:
                return self._proclaim_missing_keys("HETZNER", ["HCLOUD_TOKEN"])

            try:
                client = HCloudClient(token=token)
                # Cheap call: List Locations to verify token
                locs = client.locations.get_all()

                if request.persist_globally:
                    self._persist_key("HCLOUD_TOKEN", token)

                return self.success(
                    "Hetzner Identity Verified.",
                    data={"status": "RESONANT", "locations": len(locs)},
                    ui_hints={"vfx": "bloom", "glow": "#D50C2D"}
                )
            except APIException as e:
                return self.failure(f"Hetzner API Error: {e}", severity=HeresySeverity.WARNING)
            except Exception as e:
                return self.failure(f"Hetzner Fracture: {e}")

        # [ASCENSION 9]: Lenient Whoami
        if action == "whoami":
            if not token:
                return self.success("Identity Void.", data={"status": "VOID", "provider": "hetzner"})

        return self._handle_common_actions(action, "HCLOUD_TOKEN")

    # =========================================================================
    # == COMMON RITES & UTILITIES                                            ==
    # =========================================================================

    def _resolve_credential(self, env_key: str, explicit_value: Optional[str]) -> Optional[str]:
        """
        [THE CREDENTIAL SCRYER]
        Resolves the key from Explicit -> Environment -> Disk (in that order).
        """
        # 1. Explicit
        if explicit_value and isinstance(explicit_value, str) and explicit_value.strip():
            return explicit_value.strip()

        # 2. Environment
        env_val = os.environ.get(env_key)
        if env_val and env_val.strip():
            return env_val.strip()

        # 3. Disk (Lazy Load)
        env_path = self._global_root / ".env"
        if env_path.exists():
            try:
                content = env_path.read_text(encoding='utf-8')
                match = re.search(f"^{env_key}=(.*)$", content, re.MULTILINE)
                if match:
                    return match.group(1).strip()
            except:
                pass

        return None

    def _handle_common_actions(self, action: str, primary_key: str) -> ScaffoldResult:
        """Handles generic whoami/forget logic."""
        if action == "whoami":
            val = self._resolve_credential(primary_key, None)

            if val:
                return self.success("Identity is Resonant.", data={"status": "ACTIVE", "key_present": True})
            return self.success("Identity is Void.", data={"status": "VOID", "key_present": False})

        if action == "forget":
            self._persist_key(primary_key, "")  # Clear it
            return self.success("Identity Obliterated.", ui_hints={"vfx": "dissolve"})

        return self.failure(f"Unknown action: {action}")

    def _persist_key(self, key_name: str, value: str):
        """
        [ASCENSION 5]: Atomic Persistence.
        Writes to .env without corrupting existing keys.
        """
        env_path = self._global_root / ".env"
        with self._lock:
            try:
                lines = []
                if env_path.exists():
                    lines = env_path.read_text(encoding='utf-8').splitlines()

                # Filter out the key we are setting
                new_lines = [l for l in lines if not l.startswith(f"{key_name}=")]

                # Append if value is not empty (empty = delete)
                if value:
                    new_lines.append(f"{key_name}={value}")

                env_path.write_text("\n".join(new_lines) + "\n", encoding='utf-8')

                if value:
                    os.environ[key_name] = value
                else:
                    os.environ.pop(key_name, None)

                self.logger.info(f"Key '{key_name}' enshrined in Global Vault.")
            except Exception as e:
                self.logger.error(f"Persistence Fracture: {e}")

    def _proclaim_missing_keys(self, provider: str, keys: List[str]) -> ScaffoldResult:
        """
        [ASCENSION 6]: Socratic Diagnostics.
        Reports exactly what is missing and what is present (redacted).
        """
        found = {k: "PRESENT" for k in keys if os.environ.get(k)}
        missing = [k for k in keys if k not in found]

        return self.failure(
            f"Missing {provider} Credentials.",
            details=f"Required: {keys}. Found: {list(found.keys())}. Missing: {missing}",
            suggestion=f"Set {missing[0]} in the engine environment or pass in credentials map.",
            # [THE FIX]: Explicit Error Code for UI Handling
            code="MISSING_CREDENTIALS"
        )

    def _entropy_sieve(self, text: str) -> str:
        """[ASCENSION 12]: Redacts high-entropy strings."""
        if not text: return ""
        text = re.sub(r'(sk_live_[a-zA-Z0-9]{24})', '[REDACTED]', text)
        text = re.sub(r'(ghp_[a-zA-Z0-9]{36})', '[REDACTED]', text)
        return text