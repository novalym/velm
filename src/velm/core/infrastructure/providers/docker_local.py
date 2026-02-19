# Path: src/velm/core/infrastructure/providers/docker_local.py
# ------------------------------------------------------------
# LIF: ∞ | ROLE: LOCAL_REALITY_SIMULATOR | RANK: SOVEREIGN
import docker
import time
import socket
from typing import Dict, Any, List, Optional
from ..contracts import ComputeProvider, VMInstance, NodeState
from ....logger import Scribe

Logger = Scribe("Infra:Docker")


class DockerLocalProvider(ComputeProvider):
    """
    The Mirror of the Cloud.
    Runs local containers as if they were remote servers.
    Enables 'Air-Gapped' infrastructure orchestration.
    """

    def __init__(self):
        self.client = None

    @property
    def provider_code(self) -> str:
        return "docker"

    def authenticate(self) -> bool:
        try:
            self.client = docker.from_env()
            self.client.ping()
            Logger.success("Local Docker Socket Resonant.")
            return True
        except Exception as e:
            Logger.warn(f"Docker Daemon Unreachable: {e}")
            return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        if not self.client: self.authenticate()

        name = config.get("name", f"velm-local-{int(time.time())}")
        image = config.get("image", "ubuntu:latest")  # Default to a base OS
        ports = config.get("ports", {})  # e.g. {'80/tcp': 8080}

        # Keep container alive
        command = config.get("command", "tail -f /dev/null")

        try:
            Logger.info(f"Spinning Local Container '{name}'...")
            container = self.client.containers.run(
                image,
                command=command,
                detach=True,
                name=name,
                ports=ports,
                labels={"managed_by": "velm"}
            )

            # Reload to get network settings
            container.reload()

            return self._map_to_schema(container)
        except Exception as e:
            Logger.error(f"Local Provisioning Failed: {e}")
            raise e

    def get_status(self, instance_id: str) -> VMInstance:
        if not self.client: self.authenticate()
        try:
            container = self.client.containers.get(instance_id)
            return self._map_to_schema(container)
        except Exception:
            return VMInstance(
                id=instance_id, name="LOST", provider_id="docker",
                region="local", state=NodeState.TERMINATED, ip_address=None, private_ip=None
            )

    def terminate(self, instance_id: str) -> bool:
        if not self.client: self.authenticate()
        try:
            container = self.client.containers.get(instance_id)
            container.stop(timeout=1)
            container.remove()
            Logger.info(f"Container {instance_id} removed.")
            return True
        except Exception as e:
            Logger.error(f"Could not kill container: {e}")
            return False

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        if not self.client: self.authenticate()
        containers = self.client.containers.list(filters={"label": "managed_by=velm"})
        return [self._map_to_schema(c) for c in containers]

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        return 0.00  # The user provides the electricity

    def _map_to_schema(self, container) -> VMInstance:
        state_map = {
            'running': NodeState.RUNNING,
            'exited': NodeState.STOPPED,
            'paused': NodeState.STOPPED,
            'restarting': NodeState.PENDING
        }

        # Localhost is the public IP
        return VMInstance(
            id=container.id[:12],
            name=container.name,
            provider_id="docker",
            region="local",
            public_ip="127.0.0.1",
            private_ip="172.17.0.X",  # Placeholder for bridge IP
            state=state_map.get(container.status, NodeState.FRACTURED),
            metadata={"image": str(container.image)}
        )