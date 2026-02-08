# Path: src/velm/core/infrastructure/providers/oracle.py
# ------------------------------------------------------
import time
import oci
import base64
import gzip
import random
import logging
from typing import Dict, Any, Optional

from ..contracts import ComputeProvider, VMInstance
from ....contracts.heresy_contracts import ArtisanHeresy

Logger = logging.getLogger("Infra:Oracle")


class OracleProvider(ComputeProvider):
    """
    The Oracle implementation of the Compute Provider.
    Encapsulates the 'Chronos Engine' logic for aggressive/smart provisioning.
    """

    def __init__(self, config: Dict[str, str]):
        self.compartment_id = config.get("OCI_COMPARTMENT_ID")
        self.subnet_id = config.get("OCI_SUBNET_ID")
        self.image_id = config.get("OCI_IMAGE_ID")
        self.ssh_key = config.get("SSH_PUBLIC_KEY")
        self.user_id = config.get("OCI_USER_ID")
        self.fingerprint = config.get("OCI_FINGERPRINT")
        self.key_content = config.get("OCI_KEY_CONTENT")  # PEM string
        self.tenancy = config.get("OCI_TENANCY")
        self.region = config.get("OCI_REGION")

        self.client = None
        self.identity = None

    def authenticate(self) -> bool:
        try:
            # Construct config dict programmatically to avoid file dependency
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
            return True
        except Exception as e:
            Logger.error(f"Oracle Authentication Fracture: {e}")
            return False

    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """
        Executes the 'Harmonic Pulse' logic to acquire a VM.
        """
        if not self.client:
            if not self.authenticate():
                raise ArtisanHeresy("Cannot provision: Authentication failed.")

        display_name = config.get("name", "VELM-TITAN-NODE")
        shape = config.get("shape", "VM.Standard.A1.Flex")
        ocpus = config.get("ocpus", 4)
        memory = config.get("memory_in_gbs", 24)

        # Prepare Cloud Init
        user_data = config.get("user_data", "")
        encoded_init = base64.b64encode(gzip.compress(user_data.encode())).decode()

        # Availability Domain Strategy (Round Robin logic from void_catcher)
        ads = self.identity.list_availability_domains(self.compartment_id).data
        if not ads:
            raise ArtisanHeresy("No Availability Domains found in Compartment.")

        # The Siege Loop
        attempts = 0
        max_attempts = config.get("max_attempts", 1000)  # Controlled persistence

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
                    metadata={"ssh_authorized_keys": self.ssh_key, "user_data": encoded_init}
                )

                response = self.client.launch_instance(launch_details)
                instance_data = response.data

                Logger.success(f"VICTORY: Instance {instance_data.id} provisioned.")

                return VMInstance(
                    id=instance_data.id,
                    provider_id="oracle",
                    ip_address="PENDING",  # Requires secondary lookup
                    state=instance_data.lifecycle_state,
                    metadata={"ad": target_ad.name}
                )

            except oci.exceptions.ServiceError as e:
                attempts += 1
                if e.status == 500:
                    Logger.debug("Void response (500). Retrying immediately.")
                    time.sleep(0.5)  # Harmonic Jitter
                elif e.status == 429:
                    Logger.warn("Shield detected (429). Engaging Backoff.")
                    time.sleep(random.uniform(15, 45))  # Logic from void_catcher
                else:
                    Logger.error(f"Oracle Error: {e.status} - {e.message}")
                    time.sleep(5)

            except Exception as e:
                Logger.error(f"Unknown Fracture: {e}")
                time.sleep(1)

        raise ArtisanHeresy("Siege failed. The Void refused to yield a compute node.")

    def get_status(self, instance_id: str) -> VMInstance:
        if not self.client: self.authenticate()
        try:
            resp = self.client.get_instance(instance_id)
            inst = resp.data

            # Scry IP if running
            ip = None
            if inst.lifecycle_state == "RUNNING":
                # Logic to fetch VNIC and IP would go here (simplified for brevity)
                vnic_attachments = self.client.list_vnic_attachments(self.compartment_id, instance_id=instance_id).data
                if vnic_attachments:
                    # This would need the VirtualNetworkClient
                    pass

            return VMInstance(
                id=inst.id,
                provider_id="oracle",
                ip_address=ip,
                state=inst.lifecycle_state
            )
        except Exception as e:
            Logger.error(f"Status Scry Failed: {e}")
            return VMInstance(id=instance_id, provider_id="oracle", state="UNKNOWN")

    def terminate(self, instance_id: str) -> bool:
        if not self.client: self.authenticate()
        try:
            self.client.terminate_instance(instance_id)
            return True
        except Exception as e:
            Logger.error(f"Termination Failed: {e}")
            return False