# Path: src/velm/core/infrastructure/providers/oracle.py
# ------------------------------------------------------
# LIF: ∞ | ROLE: ORACLE_CLOUD_CONDUCTOR | RANK: SOVEREIGN

import time
import base64
import gzip
import random
import logging
from typing import Dict, Any, Optional, List

# [ASCENSION 1]: JIT IMPORT SUTURE
try:
    import oci

    OCI_AVAILABLE = True
except ImportError:
    OCI_AVAILABLE = False

from ..contracts import ComputeProvider, VMInstance, NodeState
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("Infra:Oracle")


class OracleProvider(ComputeProvider):
    """
    =============================================================================
    == THE ORACLE CONDUCTOR (V-Ω-ARM-OPTIMIZED)                                ==
    =============================================================================
    The implementation of the ComputeProvider for Oracle Cloud Infrastructure (OCI).
    Specializes in acquiring Ampere A1 Flex instances via the 'Harmonic Pulse' siege strategy.
    """

    def __init__(self, config: Dict[str, str]):
        self.compartment_id = config.get("OCI_COMPARTMENT_ID")
        self.subnet_id = config.get("OCI_SUBNET_ID")
        self.image_id = config.get("OCI_IMAGE_ID")
        self.ssh_key = config.get("SSH_PUBLIC_KEY")
        self.user_id = config.get("OCI_USER_ID")
        self.fingerprint = config.get("OCI_FINGERPRINT")
        self.key_content = config.get("OCI_KEY_CONTENT")
        self.tenancy = config.get("OCI_TENANCY")
        self.region = config.get("OCI_REGION")

        self.client = None
        self.identity = None
        self.vnic_client = None

    @property
    def provider_code(self) -> str:
        """[CONTRACT FULFILLMENT]: The Mark of Identity."""
        return "oracle"

    def authenticate(self) -> bool:
        """[THE RITE OF KEYS]"""
        if not OCI_AVAILABLE:
            Logger.warn("OCI SDK unmanifest. Speak `pip install oci`.")
            return False

        try:
            config = {
                "user": self.user_id,
                "key_content": self.key_content,
                "fingerprint": self.fingerprint,
                "tenancy": self.tenancy,
                "region": self.region,
            }
            oci.config.validate_config(config)
            self.client = oci.core.ComputeClient(config)
            self.identity = oci.identity.IdentityClient(config)
            self.vnic_client = oci.core.VirtualNetworkClient(config)
            return True
        except Exception as e:
            Logger.error(f"Oracle Authentication Fracture: {e}")
            return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """[THE KINETIC STRIKE]: Materializes a VM via Round-Robin Siege."""
        if not self.client and not self.authenticate():
            raise ArtisanHeresy("Cannot provision: Authentication failed.")

        display_name = config.get("name", "VELM-TITAN-NODE")
        shape = config.get("shape", "VM.Standard.A1.Flex")
        ocpus = config.get("ocpus", 4)
        memory = config.get("memory_in_gbs", 24)

        # Cloud Init Compression
        user_data = config.get("user_data", "#!/bin/bash\necho 'Velm Init'")
        encoded_init = base64.b64encode(user_data.encode()).decode()

        # Scry Availability Domains
        ads = self.identity.list_availability_domains(self.compartment_id).data
        if not ads:
            raise ArtisanHeresy("No Availability Domains found in Compartment.")

        # The Siege Loop
        attempts = 0
        max_attempts = config.get("max_attempts", 5)  # Default to 5 for interactive, higher for daemon

        while attempts < max_attempts:
            target_ad = random.choice(ads)
            Logger.info(f"Striking Sector {target_ad.name} (Attempt {attempts + 1})...")

            try:
                launch_details = oci.core.models.LaunchInstanceDetails(
                    display_name=display_name,
                    compartment_id=self.compartment_id,
                    availability_domain=target_ad.name,
                    shape=shape,
                    shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=ocpus, memory_in_gbs=memory),
                    source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=self.image_id),
                    create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=self.subnet_id,
                                                                          assign_public_ip=True),
                    metadata={"ssh_authorized_keys": self.ssh_key, "user_data": encoded_init},
                    freeform_tags={"ManagedBy": "VELM", "GnosticTier": config.get("tier", "standard")}
                )

                response = self.client.launch_instance(launch_details)
                instance_data = response.data

                Logger.success(f"VICTORY: Instance {instance_data.id[-8:]} provisioned.")

                # Wait for IP? For now, return pending state.
                return self._map_to_schema(instance_data)

            except oci.exceptions.ServiceError as e:
                attempts += 1
                if e.status == 500:  # Internal Error
                    time.sleep(0.5)
                elif e.status == 429:  # Too Many Requests / Out of Host Capacity
                    Logger.warn("Capacity Shield detected. Retrying...")
                    time.sleep(2)
                else:
                    Logger.error(f"Oracle Error: {e.message}")
                    raise ArtisanHeresy(f"Provisioning Fracture: {e.message}")

        raise ArtisanHeresy("Siege failed. The Oracle refused to yield a compute node.")

    def get_status(self, instance_id: str) -> VMInstance:
        """[THE SCRYING RITE]"""
        if not self.client: self.authenticate()
        try:
            resp = self.client.get_instance(instance_id)
            return self._map_to_schema(resp.data)
        except Exception as e:
            Logger.warn(f"Status Scry Failed for {instance_id}: {e}")
            return VMInstance(
                id=instance_id, name="UNKNOWN", provider_id="oracle", region=self.region or "unknown",
                state=NodeState.FRACTURED
            )

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        """[THE CENSUS RITE]"""
        if not self.client: self.authenticate()
        try:
            # Oracle doesn't support server-side tag filtering well in list_instances, do client side
            resp = self.client.list_instances(self.compartment_id)
            all_instances = resp.data

            filtered = []
            for inst in all_instances:
                if inst.lifecycle_state == "TERMINATED": continue

                # Filter Logic
                if tag_filter:
                    tags = inst.freeform_tags or {}
                    match = True
                    for k, v in tag_filter.items():
                        if tags.get(k) != v:
                            match = False
                            break
                    if not match: continue

                filtered.append(self._map_to_schema(inst))

            return filtered
        except Exception as e:
            Logger.error(f"Census Failed: {e}")
            return []

    def terminate(self, instance_id: str) -> bool:
        """[THE RITE OF ANNIHILATION]"""
        if not self.client: self.authenticate()
        try:
            self.client.terminate_instance(instance_id)
            Logger.info(f"Oracle Instance {instance_id[-8:]} returning to void.")
            return True
        except Exception as e:
            Logger.error(f"Termination Failed: {e}")
            return False

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        """[THE PROPHECY OF ECONOMY]"""
        # Oracle A1 Flex pricing (Approximate)
        ocpus = config.get("ocpus", 4)
        mem = config.get("memory_in_gbs", 24)

        # Free tier allowance check could go here
        # Standard rate: $0.01 per OCPU hour, $0.0015 per GB hour
        cost = (ocpus * 0.01) + (mem * 0.0015)
        return round(cost, 4)

    def _map_to_schema(self, oci_inst) -> VMInstance:
        """Transmutes OCI object to Gnostic Schema."""
        state_map = {
            'MOVING': NodeState.PENDING,
            'PROVISIONING': NodeState.PENDING,
            'RUNNING': NodeState.RUNNING,
            'STARTING': NodeState.PENDING,
            'STOPPED': NodeState.STOPPED,
            'STOPPING': NodeState.RUNNING,
            'TERMINATED': NodeState.TERMINATED,
            'TERMINATING': NodeState.RUNNING
        }

        public_ip = None
        # Attempt to resolve IP if running (Requires extra API call usually, simplified here)
        # In a real high-throughput system, we'd cache this or fetch aggressively.

        return VMInstance(
            id=oci_inst.id,
            name=oci_inst.display_name,
            provider_id="oracle",
            region=oci_inst.region,
            state=state_map.get(oci_inst.lifecycle_state, NodeState.UNKNOWN),
            public_ip=public_ip,
            tags=oci_inst.freeform_tags or {},
            metadata={
                "shape": oci_inst.shape,
                "fault_domain": oci_inst.fault_domain
            }
        )