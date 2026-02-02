# Path: scaffold/src/scaffold/artisans/services/storage/domains/objects.py
import os
import mimetypes
from typing import Any, Dict
from botocore.exceptions import ClientError


class MatterHandler:
    """
    [THE KEEPER OF OBJECTS]
    Manages the physical transmission of files (Upload/Download/Delete).
    """

    def __init__(self, client):
        self.s3 = client

    def execute(self, action: str, request: Any) -> Any:
        bucket = request.bucket
        key = request.path

        if action == "upload":
            return self._upload(bucket, key, request.source_path, request.content_type, request.data)

        elif action == "download":
            return self._download(bucket, key, request.destination_path)

        elif action == "delete":
            self.s3.delete_object(Bucket=bucket, Key=key)
            return {"status": "deleted", "key": key}

        elif action == "copy":
            if not request.source_path: raise ValueError("Copy requires source_path (bucket/key)")
            copy_source = {'Bucket': bucket, 'Key': request.source_path}  # Assuming intra-bucket copy if bucket same
            # If source_path implies a different bucket, parsing is needed.
            # Simplified: source_path is the key in the SAME bucket.
            self.s3.copy_object(CopySource=copy_source, Bucket=bucket, Key=key)
            return {"status": "copied", "src": request.source_path, "dest": key}

        elif action == "list":
            # List objects in bucket with optional prefix (key)
            prefix = key if key else ""
            response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=request.limit or 1000)
            contents = response.get('Contents', [])
            return [
                {"key": obj['Key'], "size": obj['Size'], "last_modified": obj['LastModified'].isoformat()}
                for obj in contents
            ]

        raise ValueError(f"Unknown Object Action: {action}")

    def _upload(self, bucket: str, key: str, source: str, content_type: str, metadata: Dict) -> Dict:
        if not source or not os.path.exists(source):
            raise FileNotFoundError(f"Source matter not found: {source}")

        # Auto-divine ContentType if not provided
        if not content_type:
            content_type, _ = mimetypes.guess_type(source)
            if not content_type: content_type = "application/octet-stream"

        extra_args = {
            'ContentType': content_type,
            'Metadata': {k: str(v) for k, v in (metadata or {}).items()}
        }

        self.s3.upload_file(source, bucket, key, ExtraArgs=extra_args)
        return {"status": "uploaded", "bucket": bucket, "key": key, "type": content_type}

    def _download(self, bucket: str, key: str, dest: str) -> Dict:
        if not dest:
            # If no destination, we might want to return bytes,
            # but boto3.download_file writes to disk.
            # Use get_object for bytes. For now, require path.
            raise ValueError("Destination path required for download.")

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)

        self.s3.download_file(bucket, key, dest)
        return {"status": "downloaded", "local_path": dest}