# Path: scaffold/src/scaffold/artisans/services/storage/domains/buckets.py
from typing import Any


class ContainerManager:
    """
    [THE ARCHITECT OF VOIDS]
    Manages the buckets themselves.
    """

    def __init__(self, client):
        self.s3 = client

    def execute(self, action: str, bucket: str) -> Any:
        if action == "create_bucket":
            self.s3.create_bucket(Bucket=bucket)
            return {"status": "created", "bucket": bucket}

        elif action == "delete_bucket":
            self.s3.delete_bucket(Bucket=bucket)
            return {"status": "deleted", "bucket": bucket}

        elif action == "list_buckets":
            response = self.s3.list_buckets()
            return [b['Name'] for b in response.get('Buckets', [])]

        raise ValueError(f"Unknown Bucket Action: {action}")