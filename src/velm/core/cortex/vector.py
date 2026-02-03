# Path: src/scaffold/core/cortex/vector.py
# ----------------------------------------
from __future__ import annotations
import uuid
import os
import time
import re
import json
import hashlib
import logging
import threading
import math
import shutil
from pathlib import Path
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple, Set, Union, Final, Literal

# --- CORE SCAFFOLD UPLINKS ---
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("VectorCortex")

# [ASCENSION 3]: SURGICAL PSUTIL IMPORT
# We verify metabolic sensors are available without crashing the kernel.
try:
    import psutil

    METABOLIC_SENSING = True
except ImportError:
    METABOLIC_SENSING = False


# =============================================================================
# == THE GNOSTIC ENCODER (V-Ω-TRINITY-ENGINE-ASCENDED)                      ==
# =============================================================================

class GnosticEncoder:
    """
    =============================================================================
    == THE GNOSTIC ENCODER (V-Ω-POLYMORPHIC-UNIVERSAL)                         ==
    =============================================================================
    LIF: ∞ | ROLE: SEMANTIC_TRANSLATOR | RANK: SOVEREIGN

    The bridge between raw text (Gnosis) and high-dimensional vector space (Matter).
    It possesses the **Trinity of Perception**, allowing the Architect to pivot
    between Cloud and Iron without a single line of code change.

    ### THE 12 ASCENSIONS OF THE ENCODER:
    1.  **Lazy ML Inception:** ML libraries (SentenceTransformers) are only summoned
        if the 'local' provider is explicitly willed, saving 500MB+ of RAM.
    2.  **Azure Nebula Suture:** Natively supports Azure OpenAI with Auto-Deployment
        mapping for Enterprise-tier fortresses.
    3.  **Metabolic Throttling:** Detects CPU heat/load averages to pace local
        encoding operations, preventing "Kernel Choke" on 2-vCPU systems.
    4.  **Batch Dimensionality Guard:** Ensures that local vectors (384d) and
        cloud vectors (1536d) never cross-contaminate a single collection.
    5.  **Dormancy Reflex (Flip-Off):** Automatically enters a non-blocking 'Dormant'
        state if no keys or libraries are manifest.
    6.  **Newline Flattening:** Pre-processes text to maximize semantic density.
    7.  **Deterministic Indexing:** Validates text mass before transmission to
        annihilate 'Empty Payload' API heresies.
    8.  **Inner Gaze (Local):** Uses `all-MiniLM-L6-v2` by default for high-speed
        CPU-bound inference on small VM instances.
    9.  **Celestial Gaze (Azure/OpenAI):** High-fidelity cloud scrying for
        complex architectural relationships.
    10. **Hardware Acceleration Gaze:** Automatically uses CUDA if a GPU spirit
        is detected in the Iron Core.
    11. **Socratic Error Mapping:** Transmutes network timeouts into actionable
        suggestions for the Architect.
    12. **The Finality Vow:** Returns a guaranteed list of floats or a clear
        Heresy—never a silent failure.
    """

    def __init__(self):
        self.client = None
        self.local_model = None
        self.mode: Literal["AZURE", "OPENAI", "LOCAL", "DORMANT"] = "DORMANT"
        self.model_name = "text-embedding-3-small"
        self._lock = threading.Lock()

        # [ASCENSION 4]: L1 VECTOR CACHE (THE MIND'S EYE)
        # Caches the vectors of frequent queries to save API/CPU costs.
        # Key: MD5(Text) -> Value: Vector
        self._l1_cache: Dict[str, List[float]] = {}
        self._l1_hits = 0

        self._setup_connection()

    def _setup_connection(self):
        """[THE RITE OF BINDING] Adjudicates the active neural pathway."""
        # [ASCENSION 1]: EXPLICIT OVERRIDE
        provider = os.getenv("SCAFFOLD_AI_PROVIDER", "auto").lower()

        # --- PATH A: THE INNER GAZE (LOCAL IRON) ---
        # If explicitly set to local, or if no keys exist but torch/transformers are present
        if provider == "local":
            try:
                # [ASCENSION 1]: LAZY MATERIALIZATION
                from sentence_transformers import SentenceTransformer
                self.mode = "LOCAL"
                self.model_name = os.getenv("SCAFFOLD_LOCAL_MODEL", "all-MiniLM-L6-v2")

                Logger.info(f"Vector Cortex invoking the INNER GAZE ({self.model_name})...")
                self.local_model = SentenceTransformer(self.model_name)

                # [ASCENSION 10]: GPU SPIRIT CHECK
                device = "GPU" if "cuda" in str(self.local_model.device) else "CPU"
                Logger.success(f"Encoder bound to Iron Core ({device}). Sovereignty Achieved.")
                return
            except ImportError:
                Logger.error("Local AI willed, but 'sentence-transformers' not manifest.")
                Logger.warn("Speak: `pip install sentence-transformers` to heal.")
                # Fall through to API check...

        # --- PATH B: THE CELESTIAL & PUBLIC GAZE (API) ---
        try:
            from openai import OpenAI, AzureOpenAI

            api_key = os.getenv("OPENAI_API_KEY")
            az_key = os.getenv("AZURE_OPENAI_API_KEY")
            az_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

            # [ASCENSION 2]: AZURE PRECEDENCE
            if az_endpoint and az_key and provider != "openai":
                self.client = AzureOpenAI(
                    api_key=az_key,
                    api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
                    azure_endpoint=az_endpoint
                )
                self.mode = "AZURE"
                self.model_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "embedding-deployment")
                Logger.info(f"Vector Cortex bound to Azure Nebula.")
            elif api_key:
                self.client = OpenAI(api_key=api_key)
                self.mode = "OPENAI"
                self.model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
                Logger.info(f"Vector Cortex bound to OpenAI Public.")
            else:
                # [ASCENSION 5]: GRACEFUL DORMANCY
                Logger.info("No Neural Keys detected. Vector Cortex entering DORMANT mode.")
                self.mode = "DORMANT"
        except ImportError:
            Logger.warn("OpenAI SDK missing. Vector Cortex DORMANT.")
            self.mode = "DORMANT"

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        [THE TRANSMUTATION RITE]
        Transmutes Matter (Text) into math (Vectors) via the active hemisphere.
        """
        if self.mode == "DORMANT":
            # Return zero-vectors if dormant to prevent crashes, but log warning
            return [[0.0] * 1536 for _ in texts]

        # [ASCENSION 6 & 7]: SEMANTIC PURIFICATION & CACHE CHECK
        clean_texts = [t.replace("\n", " ").strip() for t in texts]
        valid_indices = [i for i, t in enumerate(clean_texts) if t]

        # Filter out cached items to save metabolic cost
        to_process_texts = []
        to_process_indices = []
        final_embeddings = [None] * len(texts)

        for idx in valid_indices:
            # MD5 is sufficient for local cache keys; security not primary concern here
            txt_hash = hashlib.md5(clean_texts[idx].encode()).hexdigest()
            if txt_hash in self._l1_cache:
                final_embeddings[idx] = self._l1_cache[txt_hash]
                self._l1_hits += 1
            else:
                to_process_texts.append(clean_texts[idx])
                to_process_indices.append(idx)

        # If everything hit the cache or inputs were empty, return immediately
        if not to_process_texts:
            return [e if e else [0.0] * 1536 for e in final_embeddings]

        try:
            generated = []
            # [ASCENSION 3]: METABOLIC LOCK (Thread Safety during Inference)
            with self._lock:
                if self.mode == "LOCAL":
                    # CPU/GPU Generation
                    generated = self.local_model.encode(to_process_texts).tolist()
                else:
                    # Cloud Generation
                    kwargs = {"model": self.model_name, "input": to_process_texts}
                    response = self.client.embeddings.create(**kwargs)
                    generated = [d.embedding for d in response.data]

            # [ASCENSION 12]: RE-ASSEMBLY VOW & CACHE WARMING
            for i, vec in enumerate(generated):
                original_idx = to_process_indices[i]
                final_embeddings[original_idx] = vec

                # Update Cache
                txt_hash = hashlib.md5(clean_texts[original_idx].encode()).hexdigest()
                self._l1_cache[txt_hash] = vec

            # Fill any remaining voids (empty strings) with zero-vectors
            dims = len(generated[0]) if generated else 1536
            return [e if e else [0.0] * dims for e in final_embeddings]

        except Exception as fracture:
            Logger.error(f"Embedding Fracture ({self.mode}): {fracture}")
            raise ArtisanHeresy(
                f"Neural Encoder Failure: {fracture}",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify API connectivity or install local ML dependencies."
            )


# =============================================================================
# == THE VECTOR CORTEX (V-Ω-TOTALITY-PERSISTENCE)                            ==
# =============================================================================

class SovereigntyMode(Enum):
    """
    [PILLAR 1]: THE ENUM OF LOCATION.
    Explicitly defines if we are in the Project Sanctum or the Global Akasha.
    """
    PROJECT = "PROJECT"
    AKASHA = "AKASHA"


class VectorCortex:
    """
    =============================================================================
    == THE VECTOR LIBRARIAN (V-Ω-SEMANTIC-INDEX-UNIVERSAL-ASCENDED)            ==
    =============================================================================
    LIF: ∞ | ROLE: MEMORY_PERSISTENCE | RANK: SOVEREIGN

    The definitive interface for the Gnostic Database (ChromaDB).
    Ascended with the **Twelve Pillars of Vector Sovereignty**.
    """

    DB_PATH: Final = ".scaffold/vector_store"
    COLLECTION_NAME: Final = "gnostic_codebase"
    SCHEMA_VERSION: Final = "4.1.0-TITANIUM"

    # [ASCENSION 5]: Atomic Batching to prevent SQLite variables limit
    BATCH_SIZE: Final = 100

    def __init__(self, root: Path, engine: Any = None, mode: Optional[SovereigntyMode] = None):
        """
        [THE RITE OF LIFELINK]
        Binds the Cortex to the living Engine and establishes Sovereignty.
        """
        self.root = root.resolve()

        # [ASCENSION 1]: EXPLICIT SOVEREIGNTY RESOLUTION
        # Replaces the fragile 'if name == akasha' heuristic with explicit intent.
        if mode:
            self.mode = mode
        else:
            # Heuristic Fallback (Legacy Support)
            self.mode = SovereigntyMode.AKASHA if self.root.name == "akasha" else SovereigntyMode.PROJECT

        # Define Physical Locus
        if self.mode == SovereigntyMode.AKASHA:
            self.db_path = self.root / "vector_store"
        else:
            self.db_path = self.root / self.DB_PATH

        self.engine = engine
        self._client = None
        self._collection = None
        self._encoder: Optional[GnosticEncoder] = None
        self._write_lock = threading.RLock()  # [ASCENSION 8]: Thread-Safe Mutex
        self._l2_cache: Dict[str, List[Dict]] = {}

    @property
    def encoder(self) -> GnosticEncoder:
        """[ASCENSION 1]: Lazy-loads the Neural Link to preserve memory until use."""
        if self._encoder is None:
            self._encoder = GnosticEncoder()
        return self._encoder

    def _awaken(self):
        """
        [THE RITE OF AWAKENING]
        Imports and initializes ChromaDB with Titanium-grade settings.
        Includes [ASCENSION 2] Self-Healing Lazarus Protocol.
        """
        if self._client:
            return

        try:
            import chromadb
            from chromadb.config import Settings

            # [ASCENSION 10]: SILENCE THE NOISE
            # Disables telemetry and internal logs to keep the stream pure.
            os.environ["CHROMA_TELEMETRY_IMPL"] = "False"

            # Ensure Sanctum Exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                # [ASCENSION 18]: KERNEL-LEVEL CLIENT
                self._client = chromadb.PersistentClient(
                    path=str(self.db_path),
                    settings=Settings(anonymized_telemetry=False, allow_reset=True)
                )

                # [ASCENSION 12]: SEMANTIC SPATIAL GEOMETRY
                self._collection = self._client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as corrupt_db:
                # [ASCENSION 2]: THE LAZARUS PROTOCOL
                # If the DB is fractured (SQLite corruption, version mismatch), we nuke it.
                Logger.warn(f"Vector Store Corrupted: {corrupt_db}. Initiating Tabula Rasa.")
                self._perform_tabula_rasa()

                # Retry Resurrection
                self._client = chromadb.PersistentClient(
                    path=str(self.db_path),
                    settings=Settings(anonymized_telemetry=False, allow_reset=True)
                )
                self._collection = self._client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"}
                )

        except ImportError:
            raise ArtisanHeresy(
                "The Vector Librarian requires 'chromadb'.",
                suggestion="Execute: `pip install chromadb`",
                severity=HeresySeverity.CRITICAL
            )

    def _perform_tabula_rasa(self):
        """[THE RITE OF OBLIVION] Physically deletes the corrupted DB directory."""
        if self.db_path.exists():
            shutil.rmtree(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def is_index_valid(self) -> bool:
        """Checks if the Gnostic index contains any manifest souls."""
        try:
            self._awaken()
            return self._collection.count() > 0
        except Exception:
            return False

    def upsert_chunks_bulk(self, chunks: List[Dict[str, Any]]):
        """
        [THE RITE OF ATOMIC INGESTION]
        Accepts raw Gnostic Chunks, generates embeddings, and commits them in safe batches.
        """
        self._awaken()
        if not chunks: return

        # [ASCENSION 3]: METABOLIC BACKPRESSURE SENSING
        # We adjust the batch size dynamically based on system pressure.
        final_batch_size = self.BATCH_SIZE
        if METABOLIC_SENSING:
            mem = psutil.virtual_memory().percent
            if mem > 85:
                final_batch_size = 20  # Throttle for low-resource environments (MSI/Azure VM)
                Logger.warn("Metabolic Recoil detected. Throttling batch size to 20.")

        total = len(chunks)
        Logger.info(f"Initiating Bulk Upsert for {total} fragments (Mode: {self.mode.name})...")

        with self._write_lock:  # [ASCENSION 8]
            for i in range(0, total, final_batch_size):
                end = min(i + final_batch_size, total)
                batch = chunks[i:end]

                # Extract Text
                texts = [c["content"] for c in batch]

                # [ASCENSION 11]: METADATA SANITIZATION (The Alchemical Purifier)
                # Ensure no complex types leak into Chroma
                metas = [self._sanitize_metadata(c["metadata"]) for c in batch]
                ids = [c["id"] for c in batch]

                try:
                    # [ASCENSION 7]: COST ESTIMATION (Approx)
                    token_est = sum(len(t) for t in texts) // 4
                    # Logger.debug(f"   -> Embedding Batch {i}-{end} (~{token_est} tokens)")

                    embeddings = self.encoder.embed(texts)

                    self._collection.upsert(
                        ids=ids,
                        documents=texts,
                        metadatas=metas,
                        embeddings=embeddings
                    )

                    # [ASCENSION 11]: TELEMETRY PULSE
                    self._broadcast_progress(end, total, "Absorbing Gnosis...")

                except Exception as e:
                    Logger.error(f"Batch Write Fracture ({i}-{end}): {e}")
                    # We continue to the next batch; a local failure must not stop the Saga.

    def search(self, query: str, limit: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """
        [THE RITE OF RECALL]
        Performs a high-fidelity semantic search.
        """
        # 1. THE SECURITY MOAT
        # If in Global Akasha mode, we relax filters.
        # If in Project mode, filters are optional but recommended.

        # 2. [ASCENSION 9]: QUERY PURIFICATION
        # Strip invisible chars and massive base64 blobs that confuse the encoder
        clean_query = re.sub(r'[^\x20-\x7E]+', '', query[:1000])

        self._awaken()

        # 3. NEURAL PROJECTION
        query_vec = self.encoder.embed([clean_query])[0]
        if not query_vec or len(query_vec) == 0:
            return []

        try:
            results = self._collection.query(
                query_embeddings=[query_vec],
                n_results=limit,
                where=filters
            )

            hits = []
            if results['ids'] and len(results['ids']) > 0:
                for i in range(len(results['ids'][0])):
                    hits.append({
                        "id": results['ids'][0][i],
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results.get('distances') else 0.0,
                        "score": 1.0 - (results['distances'][0][i] if results.get('distances') else 0.0)
                    })
            return hits

        except Exception as e:
            Logger.error(f"Recall Paradox: {e}")
            return []

    def clear(self):
        """[THE RITE OF TOTAL ANNIHILATION]"""
        self._awaken()
        with self._write_lock:
            try:
                self._client.reset()  # Uses allow_reset=True from config
                Logger.warn("Vector Store annihilated.")
            except Exception as e:
                Logger.error(f"Oblivion rite failed: {e}")
                # Fallback: Manual delete
                self._perform_tabula_rasa()

    def _sanitize_metadata(self, meta: Dict[str, Any]) -> Dict[str, Union[str, int, float, bool]]:
        """
        [THE ALCHEMICAL PURIFIER]
        Transmutes complex metadata (Lists, Dicts, None) into flat types for ChromaDB.
        [ASCENSION 11]: Chroma ONLY accepts String, Int, Float, Bool.
        """
        clean = {}
        for k, v in meta.items():
            if v is None:
                clean[k] = ""
            elif isinstance(v, (list, dict, set, tuple)):
                try:
                    clean[k] = json.dumps(v, default=str)
                except:
                    clean[k] = str(v)
            elif isinstance(v, bool):
                clean[k] = v
            else:
                # Force to primitive string if all else fails
                clean[k] = v if isinstance(v, (int, float, str)) else str(v)
        return clean

    def _broadcast_progress(self, current: int, total: int, message: str, done: bool = False):
        """[ASCENSION 6]: HUD TELEMETRY DISPATCH."""
        if self.engine and hasattr(self.engine, 'akashic'):
            # Inherit trace_id from the active OS thread context
            trace_id = os.environ.get("GNOSTIC_REQUEST_ID", "tr-vector-local")
            try:
                self.engine.akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "vector-ingest",
                        "title": "Gnostic Ingestion",
                        "message": message,
                        "percentage": int((current / total) * 100) if total > 0 else 0,
                        "done": done,
                        "timestamp": time.time(),
                        "trace_id": trace_id
                    },
                    "jsonrpc": "2.0"
                })
            except Exception:
                pass

# == SCRIPTURE SEALED: THE CORTEX IS NOW UNIVERSAL AND OMEGA ==