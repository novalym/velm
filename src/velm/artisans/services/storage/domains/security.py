# Path: scaffold/src/scaffold/artisans/services/storage/domains/security.py
from typing import Any


class KeyMaster:
    """
    [THE KEYMASTER]
    Generates ephemeral access tokens (Presigned URLs).
    """

    def __init__(self, client):
        self.s3 = client

    def execute(self, action: str, request: Any) -> Any:
        if action == "sign_url":
            # Determine if we are signing a GET (download) or PUT (upload)
            # Default to get_object
            method = request.data.get("method", "get_object")
            expiry = request.expiry_seconds or 3600

            params = {'Bucket': request.bucket, 'Key': request.path}

            # If signing an upload, we might need content-type
            if method == "put_object" and request.content_type:
                params['ContentType'] = request.content_type

            url = self.s3.generate_presigned_url(
                ClientMethod=method,
                Params=params,
                ExpiresIn=expiry
            )
            return {"url": url, "expiry": expiry, "method": method}

        raise ValueError(f"Unknown Security Action: {action}")