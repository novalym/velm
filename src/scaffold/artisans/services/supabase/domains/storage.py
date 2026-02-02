import os
from typing import Any
from supabase import Client


class StorageKeeper:
    """
    [THE ASSET KEEPER]
    Manages the binary vaults (Buckets).
    """

    def __init__(self, client: Client):
        self.storage = client.storage

    def execute(self, request) -> Any:
        bucket = self.storage.from_(request.bucket)
        action = request.storage_action

        if action == "upload":
            if not request.file_source: raise ValueError("file_source path required")
            with open(request.file_source, 'rb') as f:
                return bucket.upload(request.path, f,
                                     file_options={"content-type": request.data.get("content_type", "auto")})

        elif action == "download":
            data = bucket.download(request.path)
            if request.file_source:  # Use file_source as dest for download
                with open(request.file_source, 'wb') as f:
                    f.write(data)
                return f"Downloaded to {request.file_source}"
            return data  # Return bytes if no dest

        elif action == "list":
            return bucket.list(request.path or None)

        elif action == "remove":
            return bucket.remove(request.path)

        elif action == "create_signed_url":
            expiry = request.data.get("expiry", 3600) if request.data else 3600
            return bucket.create_signed_url(request.path, expiry)

        raise ValueError(f"Unknown Storage Action: {action}")