# Path: scaffold/semantic_injection/directives/infra_knowledge/registry.py
# ------------------------------------------------------------------------

"""
=================================================================================
== THE INFRASTRUCTURE REGISTRY (V-Ω-CLOUDFORGER)                               ==
=================================================================================
LIF: 50,000,000,000

The Grimoire of Celestial Architecture. This artisan knows how to transmute
high-level intent ("I need a bucket") into the low-level scriptures of
Terraform (HCL) and Pulumi (Python).
"""
from typing import List, Tuple, Dict, Callable

from ...loader import SemanticRegistry


class InfraRegistry:
    """
    The Forger of Cloud Reality.
    """

    _library: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        """A decorator to enshrine a new infrastructure pattern."""

        def decorator(func: Callable):
            cls._library[name] = func
            return func

        return decorator

    @classmethod
    def get_generator(cls, name: str) -> Callable:
        return cls._library.get(name)

    @staticmethod
    def _parse_props(props: List[Tuple[str, str]]) -> Dict[str, str]:
        """Transmutes tuple props into a dictionary."""
        return {k: v for k, v in props}


# =============================================================================
# == TERRAFORM (THE HASHICORP TONGUE)                                        ==
# =============================================================================

@InfraRegistry.register("terraform-s3")
def forge_tf_s3(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Generates a secure AWS S3 Bucket in HCL.
    Usage: @infra/terraform-s3(name="assets", props="versioning:true")
    """
    config = InfraRegistry._parse_props(props)
    versioning = config.get("versioning", "false")
    acl = config.get("acl", "private")

    return f"""
resource "aws_s3_bucket" "{name}" {{
  bucket = "{name}-${{var.environment}}"

  tags = {{
    Name        = "{name}"
    Environment = var.environment
    ManagedBy   = "Scaffold"
  }}
}}

resource "aws_s3_bucket_ownership_controls" "{name}" {{
  bucket = aws_s3_bucket.{name}.id
  rule {{
    object_ownership = "BucketOwnerPreferred"
  }}
}}

resource "aws_s3_bucket_acl" "{name}" {{
  depends_on = [aws_s3_bucket_ownership_controls.{name}]
  bucket = aws_s3_bucket.{name}.id
  acl    = "{acl}"
}}

resource "aws_s3_bucket_versioning" "{name}" {{
  bucket = aws_s3_bucket.{name}.id
  versioning_configuration {{
    status = "{'Enabled' if versioning == 'true' else 'Disabled'}"
  }}
}}
"""


@InfraRegistry.register("terraform-ec2")
def forge_tf_ec2(name: str, props: List[Tuple[str, str]]) -> str:
    """Generates an EC2 instance."""
    config = InfraRegistry._parse_props(props)
    size = config.get("size", "t3.micro")
    ami = config.get("ami", "${var.ami_id}")

    return f"""
resource "aws_instance" "{name}" {{
  ami           = "{ami}"
  instance_type = "{size}"

  tags = {{
    Name = "{name}"
  }}
}}
"""


@InfraRegistry.register("terraform-lambda")
def forge_tf_lambda(name: str, props: List[Tuple[str, str]]) -> str:
    """Generates a basic Lambda function setup."""
    return f"""
resource "aws_lambda_function" "{name}" {{
  filename      = "lambda_function_payload.zip"
  function_name = "{name}"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.test"
  runtime       = "python3.11"

  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  environment {{
    variables = {{
      foo = "bar"
    }}
  }}
}}
"""


# =============================================================================
# == PULUMI (THE PYTHONIC CLOUD)                                             ==
# =============================================================================

@InfraRegistry.register("pulumi-s3")
def forge_pulumi_s3(name: str, props: List[Tuple[str, str]]) -> str:
    """Generates a Pulumi S3 Bucket definition in Python."""
    config = InfraRegistry._parse_props(props)
    versioning = config.get("versioning", "False")

    return f"""
import pulumi
import pulumi_aws as aws

# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('{name}',
    versioning=aws.s3.BucketVersioningArgs(
        enabled={versioning.title()},
    ),
    tags={{
        "ManagedBy": "Scaffold",
        "Name": "{name}"
    }}
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
"""


@InfraRegistry.register("pulumi-fargate")
def forge_pulumi_fargate(name: str, props: List[Tuple[str, str]]) -> str:
    """Generates a high-level Fargate service."""
    return f"""
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

cluster = aws.ecs.Cluster("{name}-cluster")

lb = awsx.lb.ApplicationLoadBalancer("{name}-lb")

service = awsx.ecs.FargateService("{name}-service",
    cluster=cluster.arn,
    assign_public_ip=True,
    task_definition_args=awsx.ecs.FargateServiceTaskDefinitionArgs(
        containers={{
            "{name}": awsx.ecs.TaskDefinitionContainerDefinitionArgs(
                image="nginx:latest",
                cpu=512,
                memory=128,
                port_mappings=[awsx.ecs.TaskDefinitionPortMappingArgs(
                    container_port=80,
                    target_group=lb.default_target_group,
                )],
            ),
        }},
    ),
)

pulumi.export("url", lb.load_balancer.dns_name)
"""


# Register the domain handler in the central SemanticRegistry
class InfraDomainHandler:
    """The Handler for the @infra domain."""

    def __getattr__(self, name: str):
        # Magic router: @infra/terraform-s3 -> finds "terraform-s3" in registry
        generator = InfraRegistry.get_generator(name)
        if generator:
            return generator
        raise AttributeError(f"The Infra Registry contains no knowledge of '{name}'.")


# Bind the handler to the domain
SemanticRegistry.register_domain("infra", InfraDomainHandler())