# Path: src/velm/core/infrastructure/providers/ovh.py
# ---------------------------------------------------
# LIF: ∞ | ROLE: OVH_SOVEREIGN_BRIDGE | RANK: OMEGA_LEGENDARY

import time
import os
import logging
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
    == THE OVH SOVEREIGN BRIDGE (V-Ω-INTERACTIVE-AUTH)                         ==
    =============================================================================
    A high-fidelity connector for the Sovereign European Cloud.

    [UNIQUE CAPABILITY]:
    Implements the 'Handshake of Trust' protocol. If no Consumer Key is found,
    it automatically negotiates a validation token with the API, opens the
    browser for the user, and waits for confirmation.

    It turns OVH's complex auth flow into a single kinetic click.
    """

    # Gnostic endpoint mapping
    ENDPOINTS = {
        "ovh-eu": "ovh-eu",
        "ovh-us": "ovh-us",
        "ovh-ca": "ovh-ca"
    }

    def __init__(self, config: Dict[str, str]):
        self.endpoint = config.get("OVH_ENDPOINT", "ovh-eu")
        self.app_key = config.get("OVH_APPLICATION_KEY")
        self.app_secret = config.get("OVH_APPLICATION_SECRET")
        self.consumer_key = config.get("OVH_CONSUMER_KEY")
        self.project_id = config.get("OVH_PROJECT_ID")  # The Public Cloud ID

        self.client = None

    @property
    def provider_code(self) -> str:
        return "ovh"

    def authenticate(self) -> bool:
        """
        [THE RITE OF THE HANDSHAKE]
        Automatically handles the complex OVH 3-legged OAuth flow in the terminal.
        """
        if not OVH_AVAILABLE:
            Logger.warn("OVH SDK unmanifest. Speak `pip install ovh`.")
            return False

        try:
            # 1. ATTEMPT SILENT CONNECTION
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

            # 2. THE INTERACTIVE WIZARD (THE KILLER FEATURE)
            # If no consumer key, we forge one now.
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
            Logger.warn(f"Action Required: Please validate the Sovereign Bond.")
            Logger.info(f"Opening Portal: [underline]{validation_url}[/underline]")

            # Kinetic Action: Open Browser
            webbrowser.open(validation_url)

            # Wait loop
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

        except Exception as e:
            Logger.error(f"OVH Auth Fracture: {e}")
            return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """[THE KINETIC STRIKE]"""
        if not self.client and not self.authenticate():
            raise ArtisanHeresy("OVH Auth Failed.")

        # 1. Resolve Project ID (Service Name)
        # If not in env, grab the first active cloud project
        if not self.project_id:
            projects = self.client.get('/cloud/project')
            if not projects:
                raise ArtisanHeresy("No OVH Public Cloud Project found. Create one in the console first.")
            self.project_id = projects[0]
            Logger.info(f"Auto-anchored to Project ID: {self.project_id}")

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
        if not self.client: self.authenticate()
        try:
            data = self.client.get(f'/cloud/project/{self.project_id}/instance/{instance_id}')
            return self._map_to_schema(data)
        except Exception:
            return VMInstance(id=instance_id, name="UNKNOWN", provider_id="ovh", region="", state=NodeState.FRACTURED)

    def terminate(self, instance_id: str) -> bool:
        if not self.client: self.authenticate()
        try:
            self.client.delete(f'/cloud/project/{self.project_id}/instance/{instance_id}')
            return True
        except Exception:
            return False

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        if not self.client: self.authenticate()
        if not self.project_id: return []

        try:
            instances = self.client.get(f'/cloud/project/{self.project_id}/instance')
            # OVH doesn't support tag filtering in list, so we filter client-side
            # Note: OVH metadata support varies, implemented as name-filtering for now
            return [self._map_to_schema(i) for i in instances]
        except Exception:
            return []

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        """[THE PROPHECY OF THRIFT]"""
        # Heuristic Pricing for standard flavors
        # d2-4 is ~0.011 EUR/hour
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
        flavors = self.client.get(f'/cloud/project/{self.project_id}/flavor', region=region)
        for f in flavors:
            if f['name'] == name: return f['id']
        # Fallback to first available if not found
        Logger.warn(f"Flavor '{name}' not found. Falling back to {flavors[0]['name']}")
        return flavors[0]['id']

    def _divine_image(self, name_query: str, region: str) -> str:
        images = self.client.get(f'/cloud/project/{self.project_id}/image', region=region)
        for img in images:
            if name_query.lower() in img['name'].lower():
                return img['id']
        raise ArtisanHeresy(f"Image '{name_query}' not found in {region}.")

    def _get_or_upload_ssh_key(self, region: str) -> str:
        """Idempotent Key Injection."""
        # Check if 'velm-key' exists
        keys = self.client.get(f'/cloud/project/{self.project_id}/sshkey', region=region)
        for k in keys:
            if k['name'] == 'velm-key': return k['id']

        # Upload
        pub_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        if not os.path.exists(pub_key_path):
            # Generate one? For now, raise heresy.
            raise ArtisanHeresy("No ~/.ssh/id_rsa.pub found. Create an SSH key first.")

        pub_key = open(pub_key_path).read()
        res = self.client.post(f'/cloud/project/{self.project_id}/sshkey',
                               name='velm-key', publicKey=pub_key, region=region
                               )
        return res['id']

    def _wait_for_active(self, instance_id: str) -> Dict:
        """Polls until IP is assigned."""
        for _ in range(60):  # 2 mins max
            inst = self.client.get(f'/cloud/project/{self.project_id}/instance/{instance_id}')
            if inst['status'] == 'ACTIVE':
                return inst
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

        # Extract IP (IPv4 Public)
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
                "flavor": data['flavor']['name'],
                "image": data['image']['name']
            }
        )

    def _persist_key(self, key: str):
        """Writes the negotiated consumer key to .env for future use."""
        # [THE FIX]: We append to .env, ensuring we don't overwrite user data
        env_path = Path(".env")
        if env_path.exists():
            content = env_path.read_text()
            if "OVH_CONSUMER_KEY" not in content:
                with open(env_path, "a") as f:
                    f.write(f"\nOVH_CONSUMER_KEY={key}\n")
                Logger.info("OVH Consumer Key inscribed to .env")
        else:
            with open(env_path, "w") as f:
                f.write(f"OVH_CONSUMER_KEY={key}\n")