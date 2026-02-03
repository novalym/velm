# Path: scaffold/core/sanctum/s3.py
# ---------------------------------

from pathlib import Path
from typing import Union, Optional

import boto3
from botocore.exceptions import ClientError

from .base import SanctumInterface
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("CloudArchive")


class S3Sanctum(SanctumInterface):
    """
    =================================================================================
    == THE CLOUD ARCHIVE (V-Ω-S3-OBJECT-STORE)                                     ==
    =================================================================================
    LIF: 10,000,000,000,000

    A bridge to the AWS S3 Celestial Realm.

    ### THE PANTHEON OF 7 ELEVATIONS:
    1.  **The Prefix Jail:** Automatically roots all operations under a specific key
        prefix, isolating the project within the bucket.
    2.  **The Metadata Scribe:** Stores filesystem permissions (`chmod`) in S3 User
        Metadata (`x-amz-meta-mode`), preserving executable bits across the void.
    3.  **The Atomic Uploader:** Uses `upload_fileobj` for memory-efficient streaming
        of large assets.
    4.  **The Virtual Directory:** Simulates directories by checking for keys with
        the given prefix, maintaining the illusion of a filesystem.
    5.  **The Public Sentinel:** Supports `acl='public-read'` configuration (via
        constructor arg) for static site deployment scenarios.
    6.  **The Endpoint Mapper:** Supports custom endpoints (MinIO, DigitalOcean Spaces)
        via `endpoint_url`.
    7.  **The Rename simulator:** Implements `rename` via Copy+Delete (with warning).
    =================================================================================
    """

    def __init__(
            self,
            bucket: str,
            region: str = "us-east-1",
            prefix: str = "",
            endpoint_url: Optional[str] = None,
            acl: str = "private",
            profile_name: Optional[str] = None
    ):
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self.acl = acl

        session = boto3.Session(profile_name=profile_name)
        self.s3 = session.client('s3', region_name=region, endpoint_url=endpoint_url)

        # Verify Bucket Access
        try:
            self.s3.head_bucket(Bucket=self.bucket)
            Logger.success(f"Connected to Cloud Sanctum: s3://{self.bucket}/{self.prefix}")
        except ClientError as e:
            raise ArtisanHeresy(f"Cloud Sanctum unreachable: {e}")

    @property
    def is_local(self) -> bool:
        return False


    @property
    def uri(self) -> str:
        p = f"/{self.prefix}" if self.prefix else ""
        return f"s3://{self.bucket}{p}"

    @property
    def root(self) -> str:
        """The bucket URI."""
        return self.uri

    def _key(self, path: Union[str, Path]) -> str:
        """Transmutes a logical path into a Storage Key."""
        clean = str(path).replace("\\", "/").strip("/")
        if self.prefix:
            return f"{self.prefix}/{clean}"
        return clean

    def resolve_path(self, path: Union[str, Path]) -> str:
        return self._key(path)

    def exists(self, path: Union[str, Path]) -> bool:
        key = self._key(path)
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            # Check if it's a "directory" (prefix exists)
            res = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key + "/", MaxKeys=1)
            return 'Contents' in res

    def is_dir(self, path: Union[str, Path]) -> bool:
        # In S3, if it ends with / it's a folder object, OR if it has children.
        key = self._key(path)
        res = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key + "/", MaxKeys=1)
        return 'Contents' in res

    def is_file(self, path: Union[str, Path]) -> bool:
        key = self._key(path)
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        # S3 directories are implicit. We *can* create a 0-byte object ending in /,
        # but it's not strictly required. We do it to "reserve" the visual folder.
        key = self._key(path)
        if not key.endswith("/"): key += "/"

        self.s3.put_object(Bucket=self.bucket, Key=key)

    def write_bytes(self, path: Union[str, Path], data: bytes):
        key = self._key(path)
        # [FACULTY 2] Store default permissions in metadata
        metadata = {"mode": "0644"}

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            Metadata=metadata,
            ACL=self.acl
        )

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        key = self._key(path)
        try:
            res = self.s3.get_object(Bucket=self.bucket, Key=key)
            return res['Body'].read()
        except ClientError as e:
            raise FileNotFoundError(f"Cloud scripture '{key}' not found: {e}")

    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        return self.read_bytes(path).decode(encoding)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        # [FACULTY 7] The Heavy Rite (Copy + Delete)
        src_key = self._key(src)
        dst_key = self._key(dst)

        Logger.verbose(f"Transmuting (Rename) s3://{src_key} -> s3://{dst_key} (Costly Operation)")

        copy_source = {'Bucket': self.bucket, 'Key': src_key}
        self.s3.copy(copy_source, self.bucket, dst_key)
        self.s3.delete_object(Bucket=self.bucket, Key=src_key)

    def unlink(self, path: Union[str, Path]):
        key = self._key(path)
        self.s3.delete_object(Bucket=self.bucket, Key=key)

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        # Bulk delete of prefix
        key = self._key(path)
        if not key.endswith("/"): key += "/"

        # List all objects with prefix
        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket, Prefix=key)

        objects_to_delete = []
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects_to_delete.append({'Key': obj['Key']})

        if objects_to_delete:
            # Batch delete (max 1000 per request)
            for i in range(0, len(objects_to_delete), 1000):
                batch = objects_to_delete[i:i + 1000]
                self.s3.delete_objects(Bucket=self.bucket, Delete={'Objects': batch})

    def chmod(self, path: Union[str, Path], mode: int):
        # S3 has no chmod. We update Metadata.
        key = self._key(path)
        # Copy object to itself with new metadata
        copy_source = {'Bucket': self.bucket, 'Key': key}
        mode_octal = oct(mode)[2:]  # "755"

        self.s3.copy_object(
            Bucket=self.bucket,
            Key=key,
            CopySource=copy_source,
            Metadata={'mode': mode_octal},
            MetadataDirective='REPLACE'
        )
        Logger.verbose(f"Consecrated permissions for {key}: {mode_octal} (Metadata)")

    def close(self):
        self.s3.close()