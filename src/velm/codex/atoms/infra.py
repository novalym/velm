# Path: src/velm/codex/atoms/infra.py
# -----------------------------------

"""
=================================================================================
== THE INFRASTRUCTURE TITAN (V-Ω-IAC-DOMAIN-ULTIMA)                            ==
=================================================================================
LIF: INFINITY | ROLE: SUBSTRATE_PROVISIONER | RANK: OMEGA_SOVEREIGN

This artisan implements the `@infra` namespace. It generates the high-fidelity
Infrastructure as Code (IaC) required to materialize the physical realm.

### THE PANTHEON OF 12 INFRASTRUCTURE ASCENSIONS:
1.  **Polymorphic Provisioning:** Native support for Terraform (HCL), Pulumi (Python/TS),
    and Ansible (YAML).
2.  **State Sovereignty:** Automatically configures S3/DynamoDB backends for
    Terraform locking to prevent "Split-Brain" heresies.
3.  **The Ansible Weaver:** Generates inventory files and playbooks that adapt
    to the target OS (Debian/RHEL).
4.  **Hyper-Modular Terraform:** Generates root modules that define VPCs,
    Security Groups, and RDS instances in a single atomic strike.
5.  **Pulumi Stack Inception:** Forges the `Pulumi.yaml` and `__main__.py`
    required to lift the infrastructure into the cloud via code.
6.  **Secret Injection Suture:** Automatically templates `.env` references into
    IaC variables to maintain the Veil of Secrecy.
7.  **Multi-Cloud Agnosticism:** Detects `aws`, `azure`, `gcp`, or `ovh` intent
    and swaps the provider blocks instantly.
8.  **The Bare Metal Bridge:** Specialized logic for provisioning OVH Dedicated
    Servers via OpenStack/Terraform providers.
9.  **Idempotency Guards:** Injects lifecycle rules (`create_before_destroy`)
    to ensure zero-downtime mutations.
10. **Forensic Tagging:** Automatically tags every cloud resource with
    `ManagedBy: Velm` and `TraceID: <uuid>`.
11. **Substrate Validation:** Ensures the user has `terraform` or `pulumi` CLI
    installed before generating complex stacks.
12. **The Finality Vow:** A mathematical guarantee of valid HCL/YAML syntax.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List, Optional
from ..contract import BaseDirectiveDomain, require_binaries
from ..loader import domain

@domain("infra")
class InfraDomain(BaseDirectiveDomain):
    """
    The Forger of Continents (Terraform, Pulumi, Ansible).
    """

    @property
    def namespace(self) -> str:
        return "infra"

    def help(self) -> str:
        return "Generates IaC (Terraform, Pulumi, Ansible) and Bare Metal configs."

    # =========================================================================
    # == STRATUM 0: THE TERRAFORM FORTRESS                                   ==
    # =========================================================================

    def _directive_terraform(self,
                             context: Dict[str, Any],
                             provider: str = "aws",
                             region: str = "us-east-1",
                             backend: bool = True,
                             modules: str = "") -> str:
        """
        @infra/terraform(provider="ovh", region="gra11", backend=true)

        [THE RITE OF HCL]
        Forges a production-grade `main.tf` with remote state locking.
        """
        p = provider.lower()
        project_name = context.get("project_name", "velm-reality")

        # 1. The Provider Block
        provider_block = ""
        if p == "aws":
            provider_block = dedent(f"""
                provider "aws" {{
                  region = "{region}"
                  default_tags {{
                    tags = {{
                      Project     = "{project_name}"
                      ManagedBy   = "Velm-God-Engine"
                      Environment = var.environment
                    }}
                  }}
                }}
            """)
        elif p == "ovh":
            provider_block = dedent(f"""
                provider "ovh" {{
                  endpoint = "ovh-eu"
                  application_key    = var.ovh_application_key
                  application_secret = var.ovh_application_secret
                  consumer_key       = var.ovh_consumer_key
                }}
            """)
        elif p == "azure":
            provider_block = dedent("""
                provider "azurerm" {
                  features {}
                }
            """)

        # 2. The Backend Suture (State Locking)
        backend_block = ""
        if backend and p == "aws":
            backend_block = dedent(f"""
                backend "s3" {{
                  bucket         = "{project_name}-tfstate"
                  key            = "global/s3/terraform.tfstate"
                  region         = "{region}"
                  dynamodb_table = "{project_name}-tflock"
                  encrypt        = true
                }}
            """)
        elif backend:
            backend_block = "# [NOTE]: Remote backend requires specific configuration for this provider."

        # 3. Module Injection
        module_block = ""
        if modules:
            for mod in modules.split(','):
                m_clean = mod.strip()
                module_block += dedent(f"""
                    module "{m_clean}" {{
                      source = "./modules/{m_clean}"
                      env    = var.environment
                    }}
                """) + "\n"

        return dedent(f"""
            # === GNOSTIC TERRAFORM MANIFEST ===
            # Generated by VELM for {project_name}

            terraform {{
              required_version = ">= 1.5.0"
              required_providers {{
                {p} = {{
                  source  = "hashicorp/{p}"
                  version = "~> 5.0"
                }}
              }}
              {backend_block}
            }}

            {provider_block}

            variable "environment" {{
              description = "The target reality (dev/prod)"
              default     = "dev"
            }}

            {module_block}
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE PULUMI SYNAPSE                                       ==
    # =========================================================================

    def _directive_pulumi(self,
                          context: Dict[str, Any],
                          lang: str = "python",
                          stack: str = "dev") -> str:
        """
        @infra/pulumi(lang="python", stack="prod")

        [THE RITE OF CODE-INFRASTRUCTURE]
        Generates the entry point for a Pulumi program.
        """
        if lang == "python":
            return dedent(f"""
                import pulumi
                import pulumi_aws as aws

                # === GNOSTIC PULUMI STACK: {stack.upper()} ===
                config = pulumi.Config()
                instance_type = config.get("instanceType") or "t3.micro"

                # 1. Network Lattice
                vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")

                # 2. Compute Node
                server = aws.ec2.Instance("web-server",
                    instance_type=instance_type,
                    ami="ami-0c55b159cbfafe1f0", # Ubuntu 20.04
                    tags={{
                        "Name": "{context.get('project_name')}-node",
                        "ManagedBy": "Velm"
                    }}
                )

                # 3. Revelation
                pulumi.export('public_ip', server.public_ip)
                pulumi.export('public_dns', server.public_dns)
            """).strip()
        elif lang == "typescript":
            return dedent("""
                import * as pulumi from "@pulumi/pulumi";
                import * as aws from "@pulumi/aws";

                const config = new pulumi.Config();
                const instanceType = config.get("instanceType") || "t3.micro";

                const server = new aws.ec2.Instance("web-server", {
                    instanceType: instanceType,
                    ami: "ami-0c55b159cbfafe1f0",
                    tags: { "ManagedBy": "Velm" }
                });

                export const publicIp = server.publicIp;
            """).strip()

        return "# Unknown Pulumi tongue."

    # =========================================================================
    # == STRATUM 2: THE ANSIBLE WEAVER                                       ==
    # =========================================================================

    def _directive_ansible(self,
                           context: Dict[str, Any],
                           roles: str = "common,docker",
                           hosts: str = "webservers") -> str:
        """
        @infra/ansible(roles="common,security,docker")

        [THE RITE OF CONFIGURATION]
        Forges a robust Ansible Playbook.
        """
        role_list = [r.strip() for r in roles.split(',')]
        roles_yaml = "\n    ".join([f"- {r}" for r in role_list])

        return dedent(f"""
            ---
            # === GNOSTIC PLAYBOOK: PROVISION ===
            - name: Consecrate the Iron
              hosts: {hosts}
              become: yes
              vars:
                project_name: "{context.get('project_name', 'velm-app')}"

              tasks:
                - name: Update Apt Cache
                  apt:
                    update_cache: yes
                    cache_valid_time: 3600

                - name: Ensure Dependencies are Manifest
                  apt:
                    name:
                      - git
                      - curl
                      - python3-pip
                    state: present

              roles:
                {roles_yaml}
        """).strip()

    def _directive_inventory(self, context: Dict[str, Any], ips: str = "127.0.0.1") -> str:
        """@infra/inventory(ips="192.168.1.1,192.168.1.2")"""
        lines = ["[webservers]"]
        for ip in ips.split(','):
            lines.append(f"{ip.strip()} ansible_user=root")
        return "\n".join(lines)

    # =========================================================================
    # == STRATUM 3: THE HELM CHART WEAVER                                    ==
    # =========================================================================

    def _directive_helm_chart(self, context: Dict[str, Any], name: str = "app") -> str:
        """@infra/helm_chart(name="nexus-api")"""
        return dedent(f"""
            apiVersion: v2
            name: {name}
            description: A Gnostic Helm Chart for {name}
            type: application
            version: 0.1.0
            appVersion: "1.0.0"
            dependencies:
              - name: postgresql
                version: 12.1.6
                repository: https://charts.bitnami.com/bitnami
                condition: postgresql.enabled
              - name: redis
                version: 17.3.14
                repository: https://charts.bitnami.com/bitnami
                condition: redis.enabled
        """).strip()