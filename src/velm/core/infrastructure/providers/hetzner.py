# Path: src/velm/core/infrastructure/providers/hetzner.py
# -------------------------------------------------------
# LIF: ∞ | ROLE: HETZNER_MERCENARY | RANK: SOVEREIGN

import os
from typing import Dict, Any, List, Optional
from ..contracts import ComputeProvider, VMInstance, NodeState
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

# JIT Import
try:
    from hcloud import Client
    from hcloud.server_types.domain import ServerType
    from hcloud.images.domain import Image
    from hcloud.locations.domain import Location

    HCLOUD_AVAILABLE = True
except ImportError:
    HCLOUD_AVAILABLE = False

Logger = Scribe("Infra:Hetzner")


class HetznerProvider(ComputeProvider):
    """
    The Mercenary of Nuremburg.
    Provides brutally efficient bare-metal-adjacent VPS performance.
    """

    def __init__(self, token: str):
        self.token = token
        self.client = None

    @property
    def provider_code(self) -> str:
        return "hetzner"

    def authenticate(self) -> bool:
        if not HCLOUD_AVAILABLE:
            Logger.warn("HCloud SDK unmanifest. Speak `pip install hcloud`.")
            return False
        try:
            self.client = Client(token=self.token)
            # Ping
            self.client.locations.get_all()
            return True
        except Exception as e:
            Logger.error(f"Hetzner Auth Fracture: {e}")
            return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        if not self.client and not self.authenticate():
            raise ArtisanHeresy("Hetzner Authentication Failed.")

        name = config.get("name", "velm-node")
        server_type = config.get("size", "cx22")  # 2vCPU, 4GB RAM
        image = config.get("image", "ubuntu-22.04")
        location = config.get("region", "nbg1")  # Nuremberg

        Logger.info(f"Summoning Hetzner Droplet [{server_type}] in {location}...")

        try:
            # Resolve Objects
            st_obj = ServerType(name=server_type)
            img_obj = Image(name=image)
            loc_obj = Location(name=location)

            response = self.client.servers.create(
                name=name,
                server_type=st_obj,
                image=img_obj,
                location=loc_obj,
                labels={"ManagedBy": "VELM", "GnosticTier": config.get("tier", "standard")}
            )

            server = response.server
            Logger.success(f"Hetzner Node Manifest: {server.name} ({server.public_net.ipv4.ip})")

            return self._map_to_schema(server)

        except Exception as e:
            raise ArtisanHeresy(f"Hetzner Provisioning Fracture: {e}")

    def get_status(self, instance_id: str) -> VMInstance:
        if not self.client: self.authenticate()
        try:
            server = self.client.servers.get_by_id(int(instance_id))
            return self._map_to_schema(server)
        except Exception:
            return VMInstance(id=instance_id, name="UNKNOWN", provider_id="hetzner", region="",
                              state=NodeState.FRACTURED)

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        if not self.client: self.authenticate()

        # Hetzner filters by label selector string
        label_selector = "ManagedBy=VELM"
        if tag_filter:
            for k, v in tag_filter.items():
                label_selector += f",{k}={v}"

        try:
            servers = self.client.servers.get_all(label_selector=label_selector)
            return [self._map_to_schema(s) for s in servers]
        except Exception as e:
            Logger.error(f"Census Failed: {e}")
            return []

    def terminate(self, instance_id: str) -> bool:
        if not self.client: self.authenticate()
        try:
            self.client.servers.get_by_id(int(instance_id)).delete()
            return True
        except Exception:
            return False

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        # Heuristic Pricing (EUR -> USD approx)
        prices = {
            "cx22": 0.006,  # ~4 EUR/mo
            "cpx11": 0.007,
            "cpx21": 0.012,
            "cpx31": 0.024
        }
        return prices.get(config.get("size", "cx22"), 0.0)

    def _map_to_schema(self, server) -> VMInstance:
        state_map = {
            'running': NodeState.RUNNING,
            'initializing': NodeState.PENDING,
            'starting': NodeState.PENDING,
            'stopping': NodeState.RUNNING,
            'off': NodeState.STOPPED,
            'deleting': NodeState.TERMINATED
        }

        return VMInstance(
            id=str(server.id),
            name=server.name,
            provider_id="hetzner",
            region=server.datacenter.location.name,
            public_ip=server.public_net.ipv4.ip,
            state=state_map.get(server.status, NodeState.UNKNOWN),
            tags=server.labels,
            metadata={"cores": server.server_type.cores, "memory": server.server_type.memory}
        )