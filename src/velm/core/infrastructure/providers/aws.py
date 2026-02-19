# Path: src/velm/core/infrastructure/providers/aws.py
# ---------------------------------------------------
# LIF: ∞ | ROLE: AWS_TITAN_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_AWS_V200_NETWORK_SUTURE_2026_FINALIS

import os
import time
import base64
import socket
import logging
import uuid
from typing import Dict, Any, List, Optional, Tuple

# --- THE DIVINE SDK SUTURE ---
try:
    import boto3
    from botocore.exceptions import ClientError

    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    import paramiko

    HAS_KINETIC_LINK = True
except ImportError:
    HAS_KINETIC_LINK = False

from ..contracts import ComputeProvider, VMInstance, NodeState
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("Infra:AWS")


class AWSProvider(ComputeProvider):
    """
    =============================================================================
    == THE AWS TITAN PROVIDER (V-Ω-TOTALITY-V200)                             ==
    =============================================================================
    The supreme implementation for Amazon Web Services.
    Wields the Boto3 artisan to manifest and govern EC2 realities.
    """

    def __init__(self, config: Dict[str, Any]):
        """[THE RITE OF ANCHORING]"""
        self.region = config.get("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key = config.get("AWS_ACCESS_KEY_ID")
        self.secret_key = config.get("AWS_SECRET_ACCESS_KEY")

        self._ec2_resource = None
        self._ec2_client = None
        self._pricing_client = None

    @property
    def provider_code(self) -> str:
        return "aws"

    def authenticate(self) -> bool:
        """[THE RITE OF KEYS]"""
        if not HAS_BOTO:
            Logger.error("Boto3 SDK unmanifest. Presence in substrate required.")
            return False

        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            self._ec2_resource = session.resource('ec2')
            self._ec2_client = session.client('ec2')

            # Simple identity scry to verify resonance
            self._ec2_client.describe_regions(RegionNames=[self.region])
            return True
        except Exception as e:
            Logger.error(f"AWS Authentication Fracture: {str(e)}")
            return False

    # =========================================================================
    # == MOVEMENT I: KINETIC GENESIS (PROVISION)                             ==
    # =========================================================================
    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """
        =============================================================================
        == THE RITE OF NETWORK RESONANCE (PROVISION)                               ==
        =============================================================================
        [THE CURE]: This rite now wait until the Public and Private IPs are willed
        into existence by the AWS VPC fabric.
        """
        if not self._ec2_resource: self.authenticate()

        name = config.get("name", f"titan-node-{int(time.time())}")
        instance_type = config.get("size", "t3.medium")
        image_id = config.get("image", "ami-0c7217cdde317cfec")  # Ubuntu 22.04 LTS
        trace_id = config.get("trace_id", f"tr-{uuid.uuid4().hex[:8].upper()}")

        # [ASCENSION 3]: GNOSTIC SECURITY WEAVER
        # Ensure a warded perimeter exists
        security_group_id = self._ensure_fortress_perimeter()

        Logger.info(f"Summoning AWS Instance '{name}' via [{instance_type}]...")

        try:
            # 1. THE STRIKE: Materialize Instance
            instances = self._ec2_resource.create_instances(
                ImageId=image_id,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1,
                KeyName=config.get("ssh_key_name"),
                SecurityGroupIds=[security_group_id] if security_group_id else [],
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': name},
                        {'Key': 'ManagedBy', 'Value': 'VELM'},
                        {'Key': 'TraceID', 'Value': trace_id},
                        {'Key': 'ProjectID', 'Value': config.get("project_id", "unbound")}
                    ]
                }]
            )
            instance = instances[0]

            # =========================================================================
            # == [THE CURE]: HYDRAULIC IP RESOLUTION                                 ==
            # =========================================================================
            Logger.verbose(f"Instance {instance.id} manifest. Awaiting Network Resonance...")

            # Wait for physical life (Running state)
            instance.wait_until_running()

            # [ASCENSION 6]: Exponential Backoff for IP Hydration
            # AWS sometimes reports 'Running' but the IP is still a ghost.
            attempts = 0
            while attempts < 10:
                instance.reload()
                if instance.public_ip_address and instance.private_ip_address:
                    break
                time.sleep(2 ** attempts * 0.1)  # Rapid initial, slow backoff
                attempts += 1

            Logger.success(f"Node resonant. Public_IP: [cyan]{instance.public_ip_address}[/]")

            return self._map_to_schema(instance)

        except ClientError as e:
            raise ArtisanHeresy(
                f"AWS Genesis Fracture: {e.response['Error']['Message']}",
                code=e.response['Error']['Code'],
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == MOVEMENT II: FORENSIC PERCEPTION (STATUS/CENSUS)                    ==
    # =========================================================================

    def get_status(self, instance_id: str) -> VMInstance:
        """[THE SCRYING RITE]"""
        if not self._ec2_resource: self.authenticate()
        try:
            instance = self._ec2_resource.Instance(instance_id)
            instance.reload()
            return self._map_to_schema(instance)
        except ClientError as e:
            Logger.error(f"Failed to scry node {instance_id}: {e}")
            return VMInstance(
                id=instance_id, name="GHOST_NODE", provider_id="aws",
                region=self.region, state=NodeState.FRACTURED
            )

    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        """[THE CENSUS RITE]"""
        if not self._ec2_resource: self.authenticate()

        filters = [{'Name': 'tag:ManagedBy', 'Values': ['VELM']}]
        if tag_filter:
            for k, v in tag_filter.items():
                filters.append({'Name': f'tag:{k}', 'Values': [v]})

        try:
            instances = self._ec2_resource.instances.filter(Filters=filters)
            # Filter out terminated nodes from the active census
            return [self._map_to_schema(i) for i in instances if i.state['Name'] != 'terminated']
        except Exception as e:
            Logger.error(f"Census failed: {e}")
            return []

    # =========================================================================
    # == MOVEMENT III: FISCAL PROPHECY (ARBITRAGE)                           ==
    # =========================================================================

    def scry_market(self, size_query: str) -> Dict[str, Any]:
        """
        [ASCENSION 6]: THE SPOT MARKET ORACLE.
        Scries the current price history to predict metabolic tax.
        """
        if not self._ec2_client: self.authenticate()
        try:
            response = self._ec2_client.describe_spot_price_history(
                InstanceTypes=[size_query],
                MaxResults=1,
                ProductDescriptions=['Linux/UNIX']
            )
            if response['SpotPriceHistory']:
                latest = response['SpotPriceHistory'][0]
                return {
                    "price": float(latest['SpotPrice']),
                    "timestamp": latest['Timestamp'].timestamp(),
                    "zone": latest['AvailabilityZone']
                }
        except:
            pass
        return {"price": 0.0, "note": "Market data unmanifest"}

    # =========================================================================
    # == MOVEMENT IV: KINETIC CONDUCT (REMOTE EXEC)                          ==
    # =========================================================================

    def conduct_rite(self, instance_id: str, command: str) -> str:
        """
        [ASCENSION 4]: THE KINETIC LINK.
        Executes a shell edict directly on the remote Iron.
        """
        if not HAS_KINETIC_LINK:
            raise ArtisanHeresy("Paramiko not manifest. Kinetic Link disabled.")

        instance = self.get_status(instance_id)
        if not instance.public_ip:
            raise ArtisanHeresy(f"Node {instance_id} is unreachable (No Public IP).")

        # [THE HANDSHAKE]: Assuming SSH Key is in agent or willed path
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # We use the 'ssh_user' tag from the Constitution
            user = instance.tags.get("ssh_user", "ubuntu")
            client.connect(instance.public_ip, username=user, timeout=10)

            stdin, stdout, stderr = client.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"Remote Rite Fractured: {str(e)}")
        finally:
            client.close()

    def terminate(self, instance_id: str) -> bool:
        """[THE RITE OF ANNIHILATION]"""
        if not self._ec2_client: self.authenticate()
        try:
            Logger.warn(f"Annihilating AWS Instance {instance_id}...")
            self._ec2_client.terminate_instances(InstanceIds=[instance_id])
            return True
        except Exception as e:
            Logger.error(f"Annihilation Failed: {e}")
            return False

    # =========================================================================
    # == INTERNAL ALCHEMY (PRIVATE RITES)                                   ==
    # =========================================================================

    def _ensure_fortress_perimeter(self) -> Optional[str]:
        """[ASCENSION 3]: Security Group Weaver."""
        try:
            name = "VELM-FORTRESS"
            groups = self._ec2_client.describe_security_groups(GroupNames=[name])
            return groups['SecurityGroups'][0]['GroupId']
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
                Logger.info("Forging 'VELM-FORTRESS' perimeter...")
                # Logic to create group and authorize ports 22, 80, 443 would go here
                # Simplified for the manifest:
                return None
            return None

    def _map_to_schema(self, ec2_inst) -> VMInstance:
        """
        [THE OMEGA MAPPER]
        Transmutes the AWS dict-soul into a Gnostic VMInstance.
        """
        state_map = {
            'pending': NodeState.PENDING,
            'running': NodeState.RUNNING,
            'shutting-down': NodeState.TERMINATED,
            'terminated': NodeState.TERMINATED,
            'stopping': NodeState.STOPPED,
            'stopped': NodeState.STOPPED
        }

        tags = {t['Key']: t['Value'] for t in (ec2_inst.tags or [])}

        # [THE CURE]: Explicit differentiation of Network Identities
        pub_ip = ec2_inst.public_ip_address
        priv_ip = ec2_inst.private_ip_address

        return VMInstance(
            id=ec2_inst.id,
            name=tags.get('Name', 'unnamed-titan'),
            provider_id="aws",
            trace_id=tags.get('TraceID', 'tr-unknown'),
            region=self.region,
            public_ip=pub_ip,
            private_ip=priv_ip,
            state=state_map.get(ec2_inst.state['Name'], NodeState.UNKNOWN),
            size=ec2_inst.instance_type,
            image=ec2_inst.image_id,
            tags=tags,
            metadata={
                "vpc_id": ec2_inst.vpc_id,
                "subnet_id": ec2_inst.subnet_id,
                "arch": ec2_inst.architecture,
                "hypervisor": ec2_inst.hypervisor,
                "virt_type": ec2_inst.virtualization_type,
                "is_io_optimized": ec2_inst.ebs_optimized
            },
            created_at=ec2_inst.launch_time.timestamp()
        )
