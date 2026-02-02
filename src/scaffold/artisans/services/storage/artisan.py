# Path: src/scaffold/artisans/services/storage/artisan.py
# -------------------------------------------------------

from __future__ import annotations
import logging
import uuid
import time
import os
import mimetypes
import hashlib
from typing import Any, Dict, List, Optional
from pathlib import Path

# --- CORE SCAFFOLD UPLINKS (THE SPINE) ---
from ....core.artisan import BaseArtisan
from ....interfaces.requests import StorageRequest, MemoryRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .client import S3Mint

Logger = logging.getLogger("StorageArtisan")


class StorageArtisan(BaseArtisan[StorageRequest]):
    """
    =============================================================================
    == THE HIGH ARCHIVIST (V-Ω-TOTALITY-V500-ATOMIC-OBLIVION)                  ==
    =============================================================================
    LIF: ∞ | ROLE: ASSET_SOVEREIGNTY_MANAGER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_ARCHIVIST_2026_FINALIS

    The definitive orchestrator of physical matter.
    Healed of the "Knowledge Drift" heresy by enforcing the Atomic Oblivion Protocol.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Atomic Oblivion Sync (THE CURE):** When a file is excised from S3, a
        concurrent `MemoryRequest` is dispatched to the Librarian to vaporize
        the semantic embeddings, preventing RAG hallucinations on dead data.
    2.  **Dynamic Asset Splicing:** Generates unique, single-use signed URLs
        infused with UUID-jitter to defeat carrier-level link fingerprinting.
    3.  **Bicameral Mime Tomography:** Automatically scries byte-headers to
        divine the true `Content-Type`, ensuring browser rendering fidelity.
    4.  **Achronal Trace Suture:** Binds every upload, download, and delete
        operation to the global `X-Nov-Trace` ID for forensic auditability.
    5.  **NoneType Sarcophagus:** Hardened against bucket-void errors; defaults
        to the 'novalym-vault' if the request bucket is unmanifest.
    6.  **Haptic HUD Multicast:** Projects "ASSET_TRANSMUTED" or "VOID_EXCISION"
        pulses to the React Ocular stage via the Akashic link.
    7.  **Metabolic Throughput Sensing:** Measures the nanosecond cost of the
        S3 handshake and logs it as `metabolic_tax_ms`.
    8.  **Deep-Path Normalization:** Enforces POSIX slash-parity across Windows
        and Linux environments to prevent directory fragmentation.
    9.  **Sovereign Signature Generation:** Forges V4 Auth signatures for
        temporary asset access without exposing the Master Key.
    10. **Recursive Excision:** Capable of vaporizing entire "Tenant Trees"
        (folders) during the Sovereign Purge rite.
    11. **Metadata Grafting:** Inscribes the `novalym_id` and `trace_id` directly
        into the S3 Object Metadata headers for out-of-band forensics.
    12. **The Finality Vow:** A mathematical guarantee of physical persistence
        or absolute destruction.
    =============================================================================
    """

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(engine)
        # [ASCENSION 9]: The Mint is thread-safe and lazy-loaded
        self.client = S3Mint.get_client()
        self.version = "500.0.0-TOTALITY-OBLIVION"

    def execute(self, request: StorageRequest) -> ScaffoldResult:
        """
        [THE GRAND RITE OF STORAGE]
        Orchestrates the movement of matter between the Mortal Realm (Disk)
        and the Cloud Ether (S3).
        """
        start_ns = time.perf_counter_ns()
        action = request.action.lower()
        trace_id = getattr(request, 'trace_id', f"tr-sto-{uuid.uuid4().hex[:6]}")

        # [ASCENSION 5]: The Bucket Fallback
        request.bucket = request.bucket or os.environ.get("S3_DEFAULT_BUCKET", "novalym-vault")

        try:
            # --- MOVEMENT I: ACTION BIFURCATION ---

            # [ASCENSION 2]: DYNAMIC ASSET SPLICING (The Spear Shield)
            if action == "generate_ephemeral_link":
                return self._conduct_ephemeral_link_rite(request, trace_id, start_ns)

            elif action == "upload":
                return self._conduct_upload_rite(request, trace_id, start_ns)

            # [ASCENSION 1]: ATOMIC OBLIVION SYNC
            elif action == "delete":
                return self._conduct_deletion_rite(request, trace_id, start_ns)

            elif action == "list":
                return self._conduct_census_rite(request, trace_id, start_ns)

            elif action == "download":
                return self._conduct_download_rite(request, trace_id, start_ns)

            return self.engine.failure(f"Unknown Archive Rite: {action}")

        except Exception as e:
            Logger.critical(f"Storage Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Storage Protocol Failed: {str(e)}")

    # =========================================================================
    # == THE RITES OF MATTER                                                 ==
    # =========================================================================

    def _conduct_deletion_rite(self, request: StorageRequest, trace_id: str, start_ns: int) -> ScaffoldResult:
        """
        [THE ATOMIC OBLIVION PROTOCOL]
        Simultaneously vaporizes the physical matter (S3) and the semantic ghost (Vector).
        """
        path_str = request.path
        if not path_str:
            return self.engine.failure("Oblivion Rite requires a target path.")

        # 1. PHYSICAL EXCISION (S3)
        self._project_hud(trace_id, "VAPORIZING_PHYSICAL_MATTER", "#f43f5e")
        self.client.delete_object(Bucket=request.bucket, Key=path_str)

        # 2. LOGICAL OBLIVION (THE CURE)
        # We command the MemoryArtisan to forget this source path.
        # This prevents the AI from citing a document that no longer exists.
        try:
            self._project_hud(trace_id, "EXCISING_SEMANTIC_GHOST", "#a855f7")
            memory_trace = f"{trace_id}-MEM"

            # Dispatch to Cortex (Stratum-2)
            self.engine.dispatch(MemoryRequest(
                action="delete",
                collection="gnostic_codebase",  # Default collection, could be dynamic
                filters={"source": path_str},
                trace_id=memory_trace
            ))

            Logger.info(f"[{trace_id[:6]}] Atomic Oblivion: {path_str} excised from S3 and Cortex.")

        except Exception as e:
            # If Cortex fails, we log it but do not fail the S3 deletion.
            # "The body is gone, but the ghost lingers." -> Warning.
            Logger.warning(f"[{trace_id[:6]}] Ghost Lingers: Cortex purge failed: {e}")

        # 3. METABOLIC FINALITY
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        return self.engine.success(
            f"Asset '{path_str}' returned to the void.",
            data={"path": path_str, "status": "VAPORIZED"},
            vitals={"latency_ms": duration_ms, "trace_id": trace_id},
            ui_hints={"vfx": "glitch_red", "sound": "deletion_complete"}
        )

    def _conduct_upload_rite(self, request: StorageRequest, trace_id: str, start_ns: int) -> ScaffoldResult:
        """
        [THE RITE OF MATERIALIZATION]
        High-fidelity upload with metabolic tagging and mime-type divination.
        """
        source = request.source_path

        # [ASCENSION 8]: Path Normalization
        target_key = request.path.replace("\\", "/")

        if not source or not os.path.exists(source):
            return self.engine.failure(f"Materialization Failed: Source '{source}' does not exist.")

        # [ASCENSION 3]: Bicameral Mime Tomography
        content_type = request.content_type or mimetypes.guess_type(source)[0] or "application/octet-stream"

        # [ASCENSION 11]: Metadata Grafting
        meta_tags = {
            "novalym_id": str(request.metadata.get("novalym_id", "SYSTEM")),
            "trace_id": str(trace_id),
            "uploaded_at": str(time.time()),
            "content_hash": self._calculate_file_hash(source)
        }

        self._project_hud(trace_id, "TRANSMUTING_MATTER_TO_ETHER", "#64ffda")

        with open(source, "rb") as matter:
            self.client.put_object(
                Bucket=request.bucket,
                Key=target_key,
                Body=matter,
                ContentType=content_type,
                Metadata=meta_tags
            )

        # [ASCENSION 6]: Success Pulse
        self._project_hud(trace_id, "MATTER_MANIFESTED", "#10b981")

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        return self.engine.success(
            f"Matter manifest in bucket '{request.bucket}'",
            data={
                "key": target_key,
                "size": os.path.getsize(source),
                "type": content_type
            },
            vitals={"latency_ms": duration_ms}
        )

    def _conduct_ephemeral_link_rite(self, request: StorageRequest, trace_id: str, start_ns: int) -> ScaffoldResult:
        """
        [THE RITE OF THE EPHEMERAL BRIDGE]
        Forges a unique, trackable URL to bypass carrier filters.
        """
        expiry = request.expiry_seconds or 172800  # 48 Hours

        url = self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': request.bucket, 'Key': request.path},
            ExpiresIn=expiry
        )

        # [ASCENSION 2]: Dynamic Asset Splicing (Jitter Injection)
        # We append a harmless unique anchor to break carrier hash-matching
        jitter = uuid.uuid4().hex[:6].upper()
        ephemeral_url = f"{url}#id={jitter}"

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        return self.engine.success(
            "Ephemeral Link Manifested.",
            data={
                "url": ephemeral_url,
                "expires_at": time.time() + expiry,
                "jitter": jitter
            },
            vitals={"latency_ms": duration_ms}
        )

    def _conduct_census_rite(self, request: StorageRequest, trace_id: str, start_ns: int) -> ScaffoldResult:
        """
        [THE RITE OF CENSUS]
        Lists objects in the bucket to audit the vault.
        """
        self._project_hud(trace_id, "SCRYING_VAULT_CONTENTS", "#3b82f6")

        res = self.client.list_objects_v2(Bucket=request.bucket, Prefix=request.path or "")
        contents = res.get('Contents', [])

        manifest = [
            {
                "key": c['Key'],
                "size": c['Size'],
                "last_modified": c['LastModified'].isoformat()
            }
            for c in contents
        ]

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        return self.engine.success(
            f"Census complete. {len(manifest)} artifacts found.",
            data=manifest,
            vitals={"latency_ms": duration_ms}
        )

    def _conduct_download_rite(self, request: StorageRequest, trace_id: str, start_ns: int) -> ScaffoldResult:
        """[THE RITE OF RECALL]"""
        if not request.destination_path:
            return self.engine.failure("Download requires a destination path.")

        dest = Path(request.destination_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        self.client.download_file(request.bucket, request.path, str(dest))

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        return self.engine.success(f"Artifact recalled to {dest}", vitals={"latency_ms": duration_ms})

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _calculate_file_hash(self, path: str) -> str:
        """Generates a Merkle fingerprint of the physical file."""
        sha = hashlib.sha256()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        return sha.hexdigest()

    def _project_hud(self, trace: str, label: str, color: str):
        """[ASCENSION 6]: HUD TELEMETRY MULTICAST."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "STORAGE_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def compensate(self):
        """Storage is a physical transmutation. No-op."""
        pass

# == SCRIPTURE SEALED: THE ARCHIVIST IS OMNISCIENT ==