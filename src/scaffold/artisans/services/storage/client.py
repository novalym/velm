# Path: scaffold/src/scaffold/artisans/services/storage/client.py
import os
import boto3
from threading import Lock
from botocore.config import Config
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class S3Mint:
    """
    [THE CELESTIAL CONNECTION]
    A thread-safe factory for the S3 Client.
    Supports any S3-compatible provider (AWS, Supabase, MinIO, DO).
    """
    _instance = None
    _lock = Lock()

    @classmethod
    def get_client(cls):
        with cls._lock:
            if cls._instance:
                return cls._instance

            # 1. Divine Credentials
            endpoint = os.environ.get("S3_ENDPOINT")  # e.g. https://nyc3.digitaloceanspaces.com
            region = os.environ.get("S3_REGION", "us-east-1")
            access_key = os.environ.get("S3_ACCESS_KEY")
            secret_key = os.environ.get("S3_SECRET_KEY")

            if not access_key or not secret_key:
                raise ArtisanHeresy(
                    "The Archive is locked. S3 credentials missing.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Inject S3_ACCESS_KEY and S3_SECRET_KEY into the environment."
                )

            try:
                # 2. Forge Configuration
                # We use signature_version='s3v4' which is required by most modern providers
                config = Config(
                    signature_version='s3v4',
                    retries={'max_attempts': 3, 'mode': 'standard'}
                )

                # 3. Establish the Bond
                cls._instance = boto3.client(
                    's3',
                    endpoint_url=endpoint,
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    config=config
                )
                return cls._instance
            except Exception as e:
                raise ArtisanHeresy(f"Failed to forge connection to the Archive: {e}")