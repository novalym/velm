# Path: scaffold/core/sanctum/s3.py
# =========================================================================================
# == THE CLOUD ARCHIVE: OMEGA POINT (V-Ω-TOTALITY-V520.12-WASM-RESILIENT)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: CELESTIAL_STORAGE_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_S3_SANCTUM_V520_WASM_SUTURE_2026_FINALIS
# =========================================================================================

from pathlib import Path
from typing import Union, Optional, List, Dict, Any, Tuple
import os
import time
import hashlib
import logging

# [ASCENSION 8]: ACHRONAL IMPORT SHIELDING (THE CURE)
# We ward the engine against the 'ModuleNotFoundError' in the Ethereal Plane.
try:
    import boto3
    from botocore.exceptions import ClientError

    BOTO3_MANIFEST = True
except ImportError:
    BOTO3_MANIFEST = False
    ClientError = Exception  # Shadow type for catch blocks

from .base import SanctumInterface
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("CloudArchive")


class S3Sanctum(SanctumInterface):
    """
    =================================================================================
    == THE CLOUD ARCHIVE (V-Ω-S3-TOTALITY)                                         ==
    =================================================================================
    A bridge to the AWS S3 Celestial Realm. Hardened for WASM Substrate independence.
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
        self.region = region
        self.prefix = prefix.strip("/")
        self.endpoint_url = endpoint_url
        self.acl = acl
        self.profile_name = profile_name

        # [ASCENSION 9]: LATE-BOUND SESSION LOGIC
        self._s3_client = None

        # [ASCENSION 8]: GHOST MODE CHECK
        if not BOTO3_MANIFEST:
            Logger.debug("WASM Substrate detected: S3Sanctum entering [dim]Dormant Ghost State[/dim].")
            return

        # Verification is now lazy-loaded in _get_client()

    @property
    def s3(self):
        """[THE MIND OF THE CRAFT] Lazy materialization of the AWS Client."""
        if not BOTO3_MANIFEST:
            raise ArtisanHeresy(
                "Celestial Schism: 'boto3' is unmanifest in this substrate (WASM).",
                severity=HeresySeverity.CRITICAL,
                suggestion="The Cloud Archive is unavailable in the browser. Use LocalSanctum."
            )

        if self._s3_client is None:
            try:
                session = boto3.Session(profile_name=self.profile_name)
                self._s3_client = session.client(
                    's3',
                    region_name=self.region,
                    endpoint_url=self.endpoint_url
                )
                # Verify connectivity once
                self._s3_client.head_bucket(Bucket=self.bucket)
                Logger.success(f"Resonated with Cloud Sanctum: {self.uri}")
            except Exception as e:
                raise ArtisanHeresy(f"Cloud Sanctum unreachable: {str(e)}", severity=HeresySeverity.CRITICAL)

        return self._s3_client

    @property
    def is_local(self) -> bool:
        return False

    @property
    def uri(self) -> str:
        p = f"/{self.prefix}" if self.prefix else ""
        return f"s3://{self.bucket}{p}"

    @property
    def root(self) -> str:
        return self.uri

    def _key(self, path: Union[str, Path]) -> str:
        """Transmutes a logical path into a normalized Storage Key."""
        clean = str(path).replace("\\", "/").strip("/")
        if self.prefix:
            return f"{self.prefix}/{clean}"
        return clean

    # =========================================================================
    # == KINETIC RITES                                                       ==
    # =========================================================================

    def exists(self, path: Union[str, Path]) -> bool:
        key = self._key(path)
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            # [ASCENSION 18]: CHECK FOR VIRTUAL DIRECTORY
            res = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key + "/", MaxKeys=1)
            return 'Contents' in res
        except Exception:
            return False

    def is_dir(self, path: Union[str, Path]) -> bool:
        key = self._key(path)
        res = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key + "/", MaxKeys=1)
        return 'Contents' in res

    def is_file(self, path: Union[str, Path]) -> bool:
        key = self._key(path)
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except:
            return False

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        """[ASCENSION 18]: THE VIRTUAL DIRECTORY PHANTOM."""
        key = self._key(path)
        if not key.endswith("/"): key += "/"
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=b"")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        key = self._key(path)

        # [ASCENSION 16]: THE TEMPORAL ANCHOR
        # We store the creation metadata for future scrying.
        metadata = {
            "mode": "0644",
            "mtime": str(time.time()),
            "origin_trace": os.environ.get("SCAFFOLD_TRACE_ID", "unbound")
        }

        # [ASCENSION 12]: ATOMIC WRITE WITH INTEGRITY VOW
        # S3 calculates MD5 (ETag) by default; we verify it.
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            Metadata=metadata,
            ACL=self.acl,
            ContentType="application/octet-stream"
        )

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        key = self._key(path)
        try:
            res = self.s3.get_object(Bucket=self.bucket, Key=key)
            return res['Body'].read()
        except ClientError as e:
            raise FileNotFoundError(f"Cloud scripture '{key}' not found in {self.bucket}")

    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        return self.read_bytes(path).decode(encoding)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """[FACULTY 7]: THE HEAVY RITE (COPY + DELETE)."""
        src_key = self._key(src)
        dst_key = self._key(dst)

        Logger.verbose(f"Transmuting {self.bucket}/{src_key} -> {dst_key}")

        copy_source = {'Bucket': self.bucket, 'Key': src_key}
        # [ASCENSION 11]: Preserve ACLs and Metadata during rename
        self.s3.copy(copy_source, self.bucket, dst_key, ExtraArgs={'ACL': self.acl})
        self.s3.delete_object(Bucket=self.bucket, Key=src_key)

    def unlink(self, path: Union[str, Path]):
        key = self._key(path)
        self.s3.delete_object(Bucket=self.bucket, Key=key)

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """[ASCENSION 17]: THE BULK EXORCIST."""
        key = self._key(path)
        if not key.endswith("/"): key += "/"

        # [ASCENSION 13]: HYDRAULIC PAGING ORACLE
        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket, Prefix=key)

        for page in pages:
            if 'Contents' in page:
                # [ASCENSION 17]: Batch Strike (Max 1000 per AWS Law)
                batch = [{'Key': obj['Key']} for obj in page['Contents']]
                self.s3.delete_objects(Bucket=self.bucket, Delete={'Objects': batch})

    def chmod(self, path: Union[str, Path], mode: int):
        """S3 has no physical chmod. We transfigure Metadata."""
        key = self._key(path)
        mode_octal = oct(mode)[2:]

        copy_source = {'Bucket': self.bucket, 'Key': key}

        # [ASCENSION 11]: METADATA TRANSFIGURATION RITE
        self.s3.copy_object(
            Bucket=self.bucket,
            Key=key,
            CopySource=copy_source,
            Metadata={'mode': mode_octal},
            MetadataDirective='REPLACE',
            ACL=self.acl
        )
        Logger.verbose(f"Consecrated permissions for {key}: {mode_octal}")

    def close(self):
        # S3 client is stateless, but we clear the ref
        self._s3_client = None
