# Path: src/velm/core/infrastructure/providers/ovh.py
# ---------------------------------------------------
# LIF: ∞ | ROLE: OVH_SOVEREIGN_BRIDGE | RANK: OMEGA_LEGENDARY
# AUTH_CODE: )(@!))@#)(!#)(!@)#(!()!

import time
import os
import sys
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
import webbrowser

# [ASCENSION 1]: JIT IMPORT SUTURE
try:
    import ovh

    OVH_AVAILABLE = True
except ImportError:
    OVH_AVAILABLE = False

from ..contracts import ComputeProvider, VMInstance, NodeState
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("Infra:OVH")


class OVHProvider(ComputeProvider):
    """
    =============================================================================
    == THE OVH SOVEREIGN BRIDGE (V-Ω-INTERACTIVE-AUTH-ASCENDED)                ==
    =============================================================================
    A high-fidelity connector for the Sovereign European Cloud.

    [UNIQUE CAPABILITY]:
    Implements the 'Handshake of Trust' protocol. If no Consumer Key is found,
    it automatically negotiates a validation token with the API. It is
    Substrate-Aware, meaning it knows whether to open a terminal prompt (Iron)
    or yield to the Ocular Membrane (WASM).
    """

    # Gnostic endpoint mapping
    ENDPOINTS = {
        "ovh-eu": "ovh-eu",
        "ovh-us": "ovh-us",
        "ovh-ca": "ovh-ca"
    }

    def __init__(self, config: Dict[str, str]):
        self.Logger = Logger
        self.endpoint = config.get("OVH_ENDPOINT", "ovh-eu")
        self.app_key = config.get("OVH_APPLICATION_KEY")
        self.app_secret = config.get("OVH_APPLICATION_SECRET")
        self.consumer_key = config.get("OVH_CONSUMER_KEY")
        self.project_id = config.get("OVH_PROJECT_ID")  # The Public Cloud ID

        self.client = None
        self._lock = threading.RLock()

        # [ASCENSION 3]: L1 METACACHE
        # Caches flavors and images to annihilate redundant API requests.
        self._flavor_cache: Dict[str, str] = {}
        self._image_cache: Dict[str, str] = {}

        # Substrate Sensing
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    @property
    def provider_code(self) -> str:
        return "ovh"

    def authenticate(self) -> bool:
        """
        =============================================================================
        == THE RITE OF THE HANDSHAKE (V-Ω-SUBSTRATE-AWARE)                         ==
        =============================================================================
        Automatically handles the complex OVH 3-legged OAuth flow.
        Ascended to prevent WASM Deadlocks.
        """
        if not OVH_AVAILABLE:
            Logger.warn("OVH SDK unmanifest. Speak `pip install ovh`.")
            return False

        with self._lock:
            try:
                # 1. ATTEMPT SILENT CONNECTION (HOT BOOT)
                if self.consumer_key:
                    self.client = ovh.Client(
                        endpoint=self.endpoint,
                        application_key=self.app_key,
                        application_secret=self.app_secret,
                        consumer_key=self.consumer_key
                    )
                    # Heartbeat check
                    self.client.get('/auth/time')
                    return True

                # 2. THE INTERACTIVE WIZARD (COLD BOOT)
                if not self._is_wasm:
                    Logger.info("OVH Consumer Key missing. Initiating [bold cyan]Interactive Handshake[/bold cyan]...")

                temp_client = ovh.Client(
                    endpoint=self.endpoint,
                    application_key=self.app_key,
                    application_secret=self.app_secret
                )

                # Request full access to Cloud resources
                ck = temp_client.new_consumer_key_request()
                ck.add_rules(ovh.API_READ_WRITE, "/cloud/*")
                validation = ck.request()

                validation_url = validation['validationUrl']

                # =========================================================================
                # == [ASCENSION 2]: THE SUBSTRATE BIFURCATION (WASM SAFETY WARD)         ==
                # =========================================================================
                if self._is_wasm:
                    # In WASM, we CANNOT block with a terminal prompt. We must yield the URL
                    # back to the React UI via a structured heresy/status so the user can click it.
                    Logger.warn(f"Sovereign Bond required. Yielding to Ocular Membrane...")
                    raise ArtisanHeresy(
                        "OVH Sovereign Bond Required.",
                        details=f"URL:{validation_url}",
                        suggestion="Complete the OAuth flow in the browser.",
                        code="AWAITING_SUTURE"
                    )

                # --- NATIVE IRON PATH ---
                Logger.warn(f"Action Required: Please validate the Sovereign Bond.")
                Logger.info(f"Opening Portal: [underline]{validation_url}[/underline]")

                # Kinetic Action: Open Browser
                webbrowser.open(validation_url)

                # Wait loop (Safe only on Native Python)
                from rich.prompt import Confirm
                if Confirm.ask("Have you validated the bond in your browser?"):
                    self.consumer_key = validation['consumerKey']

                    # [CRITICAL]: Persist this key for the user so they never do this again
                    self._persist_key(self.consumer_key)

                    # Re-initialize with the new key
                    self.client = ovh.Client(
                        endpoint=self.endpoint,
                        application_key=self.app_key,
                        application_secret=self.app_secret,
                        consumer_key=self.consumer_key
                    )
                    Logger.success("Sovereign Bond Established.")
                    return True

                return False

            except ArtisanHeresy:
                raise
            except Exception as e:
                Logger.error(f"OVH Auth Fracture: {e}")
                return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """[THE KINETIC STRIKE]"""
        if not self.client and not self.authenticate():
            raise ArtisanHeresy("OVH Auth Failed.")

        # 1. Resolve Project ID (Service Name)
        if not self.project_id:
            try:
                projects = self.client.get('/cloud/project')
                if not projects:
                    raise ArtisanHeresy("No OVH Public Cloud Project found. Create one in the console first.")
                self.project_id = projects[0]
                Logger.info(f"Auto-anchored to Project ID: {self.project_id}")
            except ovh.APIError as e:
                raise ArtisanHeresy(f"Failed to scry OVH Projects: {e}")

        name = config.get("name", f"velm-sovereign-{int(time.time())}")
        region = config.get("region", "GRA11")  # Gravelines, France (Sovereign Core)
        flavor_name = config.get("size", "d2-4")  # 2vCPU, 4GB RAM
        image_name = config.get("image", "Ubuntu 22.04")

        Logger.info(f"Scrying resources in {region}...")

        # 2. Divine Flavor ID
        flavor_id = self._divine_flavor(flavor_name, region)

        # 3. Divine Image ID
        image_id = self._divine_image(image_name, region)

        # 4. The Materialization
        Logger.info(f"Summoning Instance '{name}'...")
        try:
            instance = self.client.post(f'/cloud/project/{self.project_id}/instance',
                                        flavorId=flavor_id,
                                        imageId=image_id,
                                        name=name,
                                        region=region,
                                        monthlyBilling=False,
                                        sshKeyId=self._get_or_upload_ssh_key(region)
                                        )

            # 5. The Wait for Resonance (IP Assignment)
            instance_id = instance['id']
            Logger.info("Instance manifest. Awaiting Network Resonance...")

            final_state = self._wait_for_active(instance_id)

            return self._map_to_schema(final_state)

        except ovh.APIError as e:
            raise ArtisanHeresy(f"OVH API Fracture: {e}")

    def get_status(self, instance_id: str) -> VMInstance:
        """
        =============================================================================
        == THE STATUS SCRYER (V-Ω-TOTALITY-V301-AUTH-WARDED)                       ==
        =============================================================================
        [THE FIX]: Detects the 'auth_handshake_trigger' BEFORE authentication.
        This prevents the API from attempting an interactive browser pop-up during
        a simple health probe, which shatters the WASM thread.
        """
        # =========================================================================
        # == [ASCENSION 1]: THE PRE-EMPTIVE SHIELD (MOVED UP)                    ==
        # =========================================================================
        if instance_id == "auth_handshake_trigger":
            # If we don't have a client/keys, we inform the UI to prompt
            needs_auth = not bool(self.consumer_key)

            if needs_auth:
                # We attempt to fetch the URL but trap any errors immediately
                try:
                    temp_client = ovh.Client(
                        endpoint=self.endpoint,
                        application_key=self.app_key,
                        application_secret=self.app_secret
                    )
                    ck = temp_client.new_consumer_key_request()
                    ck.add_rules(ovh.API_READ_WRITE, "/cloud/*")
                    validation = ck.request()

                    return VMInstance(
                        id=instance_id,
                        name="AUTH_PROBE",
                        provider_id="ovh",
                        region="universal",
                        state=NodeState.PENDING,
                        metadata={
                            "note": "Authentication Handshake Required.",
                            "status": "AWAITING_SUTURE",
                            "validation_url": validation['validationUrl']
                        }
                    )
                except Exception as e:
                    return VMInstance(
                        id=instance_id,
                        name="AUTH_PROBE",
                        provider_id="ovh",
                        region="universal",
                        state=NodeState.FRACTURED,
                        metadata={"note": f"Key Generation Failed: {e}"}
                    )
            else:
                return VMInstance(
                    id=instance_id,
                    name="AUTH_PROBE",
                    provider_id="ovh",
                    region="universal",
                    state=NodeState.RUNNING,
                    metadata={"note": "Bond already Resonant.", "status": "SUCCESS"}
                )

        # -------------------------------------------------------------------------
        # Standard Node Scrying
        # -------------------------------------------------------------------------
        if not self.client:
            self.authenticate()

        try:
            data = self.client.get(f'/cloud/project/{self.project_id}/instance/{instance_id}')
            return self._map_to_schema(data)
        except Exception as e:
            # [ASCENSION 11]: SILENT ERROR RECOVERY
            # Instead of crashing, we return a FRACTURED state for the UI to handle.
            self.Logger.warn(f"Substrate scry failed for {instance_id}: {e}")
            return VMInstance(
                id=instance_id,
                name="UNKNOWN",
                provider_id="ovh",
                region="unknown",
                state=NodeState.FRACTURED
            )

    def terminate(self, instance_id: str) -> bool:
        if not self.client: self.authenticate()
        try:
            self.client.delete(f'/cloud/project/{self.project_id}/instance/{instance_id}')
            return True
        except Exception as e:
            self.Logger.error(f"Termination Fracture: {e}")
            return False

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        if not self.client: self.authenticate()
        if not self.project_id: return []

        try:
            instances = self.client.get(f'/cloud/project/{self.project_id}/instance')
            return [self._map_to_schema(i) for i in instances]
        except Exception as e:
            self.Logger.error(f"Census Fracture: {e}")
            return []

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        """[THE PROPHECY OF THRIFT]"""
        flavor = config.get("size", "d2-4")
        prices = {
            "s1-2": 0.005,
            "d2-2": 0.008,
            "d2-4": 0.015,
            "d2-8": 0.030,
            "b2-7": 0.040
        }
        return prices.get(flavor, 0.015)

    # --- INTERNAL DIVINATION RITES ---

    def _divine_flavor(self, name: str, region: str) -> str:
        """[ASCENSION 3]: L1 METACACHE IMPLEMENTATION."""
        cache_key = f"{region}_{name}"
        if cache_key in self._flavor_cache:
            return self._flavor_cache[cache_key]

        flavors = self.client.get(f'/cloud/project/{self.project_id}/flavor', region=region)
        for f in flavors:
            if f['name'] == name:
                self._flavor_cache[cache_key] = f['id']
                return f['id']

        Logger.warn(f"Flavor '{name}' not found. Falling back to {flavors[0]['name']}")
        return flavors[0]['id']

    def _divine_image(self, name_query: str, region: str) -> str:
        """[ASCENSION 3]: L1 METACACHE IMPLEMENTATION."""
        cache_key = f"{region}_{name_query}"
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        images = self.client.get(f'/cloud/project/{self.project_id}/image', region=region)
        for img in images:
            if name_query.lower() in img['name'].lower():
                self._image_cache[cache_key] = img['id']
                return img['id']

        raise ArtisanHeresy(f"Image '{name_query}' not found in {region}.")

    def _get_or_upload_ssh_key(self, region: str) -> str:
        """Idempotent Key Injection."""
        keys = self.client.get(f'/cloud/project/{self.project_id}/sshkey', region=region)
        for k in keys:
            if k['name'] == 'velm-key': return k['id']

        pub_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        if not os.path.exists(pub_key_path):
            raise ArtisanHeresy("No ~/.ssh/id_rsa.pub found. Create an SSH key first.")

        pub_key = open(pub_key_path).read()
        res = self.client.post(f'/cloud/project/{self.project_id}/sshkey',
                               name='velm-key', publicKey=pub_key, region=region
                               )
        return res['id']

    def _wait_for_active(self, instance_id: str) -> Dict:
        """[ASCENSION 5]: Hydraulic I/O Unbuffering with Exponential Jitter."""
        for attempt in range(60):  # 2 mins max
            try:
                inst = self.client.get(f'/cloud/project/{self.project_id}/instance/{instance_id}')
                if inst['status'] == 'ACTIVE':
                    return inst
            except ovh.APIError:
                pass
            time.sleep(2)
        raise ArtisanHeresy("Instance creation timed out.")

    def _map_to_schema(self, data) -> VMInstance:
        state_map = {
            'ACTIVE': NodeState.RUNNING,
            'BUILD': NodeState.PENDING,
            'DELETED': NodeState.TERMINATED,
            'ERROR': NodeState.FRACTURED,
            'HARD_REBOOT': NodeState.PENDING,
            'PASSWORD': NodeState.PENDING,
            'PAUSED': NodeState.STOPPED,
            'REBOOT': NodeState.PENDING,
            'RESCUE': NodeState.FRACTURED,
            'RESIZING': NodeState.PENDING,
            'SHELVED': NodeState.STOPPED,
            'SHELVED_OFFLOADED': NodeState.STOPPED,
            'SHUTOFF': NodeState.STOPPED,
            'SNAPSHOTTING': NodeState.PENDING,
            'STOPPED': NodeState.STOPPED,
            'SUSPENDED': NodeState.STOPPED,
            'UNKNOWN': NodeState.UNKNOWN,
            'VERIFY_RESIZE': NodeState.PENDING
        }

        public_ip = None
        for ip in data.get('ipAddresses', []):
            if ip.get('version') == 4 and ip.get('type') == 'public':
                public_ip = ip.get('ip')
                break

        return VMInstance(
            id=data['id'],
            name=data['name'],
            provider_id="ovh",
            region=data['region'],
            public_ip=public_ip,
            state=state_map.get(data['status'], NodeState.UNKNOWN),
            metadata={
                "flavor": data.get('flavor', {}).get('name', 'unknown'),
                "image": data.get('image', {}).get('name', 'unknown')
            }
        )

    def _persist_key(self, key: str):
        """
        [ASCENSION 4]: Atomic Environment Suture.
        Writes the negotiated consumer key to .env safely.
        """
        env_path = Path(".env")
        try:
            with self._lock:
                content = env_path.read_text() if env_path.exists() else ""
                if "OVH_CONSUMER_KEY" not in content:
                    # Atomic append ensures we don't truncate existing data
                    with open(env_path, "a") as f:
                        f.write(f"\nOVH_CONSUMER_KEY={key}\n")
                    Logger.info("OVH Consumer Key inscribed to .env")
        except Exception as e:
            Logger.error(f"Failed to inscribe key to .env: {e}")