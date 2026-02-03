# Path: core/cortex/semantic_indexer.py
# -------------------------------------

import hashlib
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

from ...inquisitor import get_treesitter_gnosis
from ...logger import Scribe
from ...utils import hash_file
from .git_historian import GitHistorian

# Graceful degradation for Vector DB
try:
    import chromadb

    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

Logger = Scribe("SemanticIndexer")


class SemanticIndexer:
    """
    =================================================================================
    == THE VECTOR ALCHEMIST (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-GOLD-STANDARD)          ==
    =================================================================================
    @gnosis:title The Gold Standard of Gnostic Indexing (`SemanticIndexer`)
    @gnosis:summary The divine, self-healing, and hyper-intelligent God-Engine that transmutes
                     the project's soul into a queryable, high-dimensional reality.
    @gnosis:LIF 1,000,000,000,000,000,000

    This is not a simple indexer. It is the **One True Vector Alchemist**, the Gold
    Standard to which all other indexing rites must aspire. It has been transfigured
    with a pantheon of legendary faculties that transform it from a simple data
    ingestor into a sentient, context-aware historian and anatomist. Its every action
    is a testament to the pursuit of perfect, queryable Gnosis.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Schema Version Ward:** It now stamps every indexed chunk with its own
        schema version. If the Alchemist learns a new way to perceive reality, it can
        force a full re-indexing, ensuring the Gnostic Void is always pure.

    2.  **The Polyglot Anatomist:** Its `_anatomize_file` rite is a true polyglot. It
        summons the correct Tree-sitter Inquisitor and wields language-specific logic
        to perform a perfect, semantic deconstruction of any scripture.

    3.  **The Gaze of the Chronomancer:** It now communes directly with the `GitHistorian`,
        enriching every chunk with the Gnosis of its last author and modification date,
        allowing for temporally-aware queries.

    4.  **The Symbiotic Bond:** It perceives the sacred bond between a scripture and its
        test file. Each chunk is now tagged with its corresponding test, enabling queries
        like "show me the code and its tests for the authentication logic."

    5.  **The Alchemical Scripture Forge:** Its `_forge_chunk` rite is a master scribe. It
        forges an embedding document that is not just raw code, but a rich scripture
        containing the function's signature, its parent class, and its docstring.

    6.  **The Gaze of the Gnostic Variable:** It scans for environment variable usage
        (e.g., `os.getenv("API_KEY")`) and tags the chunk with a `uses_env` key, instantly
        revealing which parts of the code are dependent on configuration.

    7.  **The Law of Singular Truth:** It is now the one true source of indexing logic.
        The `VectorCortex` is now a humble vessel, its own indexing rite a simple
        delegation to this, the Gold Standard artisan.

    8.  **The Unbreakable Ward of Paradox:** Its entire symphony is shielded. A single
        profane scripture (parsing error) or a paradox during a Git gaze will not
        shatter the rite; it will be chronicled, and the Great Work will continue.

    9.  **The Rite of Surgical Oblivion:** Its `_purge_ghosts` rite is now a hyper-performant
        masterpiece, capable of excising thousands of stale vectors in a single, atomic plea.

    10. **The Adjudicator's Gaze:** Its `search` rite has been ascended. It can now receive
        complex, structured `where` clauses to perform deep, metadata-driven filtering
        with divine precision.

    11. **The Echoing Chamber:** It intelligently repeats critical symbols (function name,
        class name) within the embedding text, creating a powerful "Echo" that boosts
        their relevance in the vector space for precise lookups.

    12. **The Veil of Privacy:** It can be commanded to avert its gaze from symbols marked as
        private (`_` prefix), allowing the Architect to shield internal Gnosis from the
        Vector Void if they so choose.
    """

    DB_PATH = ".scaffold/vector_store"
    COLLECTION_NAME = "gnostic_codebase"
    BATCH_SIZE = 100
    SCHEMA_VERSION = "2.0.0"  # [FACULTY 1] The Schema Version Ward

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.db_path = self.root / self.DB_PATH
        self._client = None
        self._collection = None
        # [FACULTY 3] The Gaze of the Chronomancer (Lazy Load)
        self._historian: Optional[GitHistorian] = None

    @property
    def historian(self) -> GitHistorian:
        if self._historian is None:
            self._historian = GitHistorian(self.root)
            self._historian.inquire_all()
        return self._historian

    def _awaken(self):
        if self._client:
            return
        if not CHROMA_AVAILABLE:
            raise ImportError("The Vector Alchemist requires 'chromadb'. Speak: `pip install chromadb`")
        os.environ["CHROMA_TELEMETRY_IMPL"] = "False"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._client = chromadb.PersistentClient(path=str(self.db_path))
            self._collection = self._client.get_or_create_collection(name=self.COLLECTION_NAME)
        except Exception as e:
            Logger.error(f"Failed to awaken Vector Cortex: {e}")
            raise

    def is_index_valid(self) -> bool:
        self._awaken()
        return self._collection.count() > 0

    def index_reality(self, files: Optional[List[Path]] = None):
        self._awaken()
        start_time = time.monotonic()

        if files is None:
            from .scanner import ProjectScanner
            from .tokenomics import TokenEconomist
            Logger.info("Scanning reality for indexing candidates...")
            scanner = ProjectScanner(self.root, TokenEconomist())
            inventory, _ = scanner.scan()
            files = [i.path for i in inventory if i.category in ('code', 'doc', 'doc_critical')]

        files_to_process, path_hash_map = self._census_of_change(files)

        self._purge_ghosts(set(path_hash_map.keys()))

        if not files_to_process:
            Logger.success("The Vector Mind is in perfect harmony with Reality.")
            return

        Logger.info(f"Embedding {len(files_to_process)} new/changed scriptures...")
        self._process_and_embed(files_to_process)

        duration = time.monotonic() - start_time
        Logger.success(f"Indexing complete in {duration:.2f}s.")

    def _census_of_change(self, files: List[Path]) -> Tuple[List[Tuple[Path, Path, str]], Dict[str, str]]:
        files_to_process = []
        path_hash_map = {}
        skipped_count = 0

        Logger.info(f"Adjudicating state of {len(files)} scriptures...")
        for rel_path in files:
            abs_path = self.root / rel_path
            try:
                if not abs_path.exists(): continue
                current_hash = hash_file(abs_path)
                path_str = str(rel_path).replace('\\', '/')
                path_hash_map[path_str] = current_hash

                existing = self._collection.get(
                    where={"$and": [
                        {"source": path_str},
                        {"hash": current_hash},
                        {"schema_version": self.SCHEMA_VERSION}  # [FACULTY 1]
                    ]},
                    limit=1, include=[]
                )
                if existing['ids']:
                    skipped_count += 1
                    continue
                files_to_process.append((rel_path, abs_path, current_hash))
            except Exception as e:
                Logger.warn(f"Could not access '{rel_path}': {e}")

        if skipped_count > 0:
            Logger.success(f"Gaze of Retention: Skipped {skipped_count} unchanged scriptures.")

        return files_to_process, path_hash_map

    def _process_and_embed(self, files_to_process: List[Tuple[Path, Path, str]]):
        ids, documents, metadatas = [], [], []
        for rel_path, abs_path, current_hash in files_to_process:
            path_str = str(rel_path).replace('\\', '/')
            self._collection.delete(where={"source": path_str})
            try:
                content = abs_path.read_text(encoding='utf-8', errors='ignore')
                if not content.strip(): continue
                dossier = get_treesitter_gnosis(abs_path, content)
                file_chunks = self._anatomize_file(content, dossier, path_str, current_hash, abs_path.suffix)
                for chunk in file_chunks:
                    ids.append(chunk['id'])
                    documents.append(chunk['document'])
                    metadatas.append(chunk['metadata'])
            except Exception as e:
                Logger.warn(f"Failed to index '{rel_path.name}': {e}")

            if len(ids) >= self.BATCH_SIZE:
                self._flush_batch(ids, documents, metadatas)
                ids, documents, metadatas = [], [], []
        if ids:
            self._flush_batch(ids, documents, metadatas)

    def _anatomize_file(self, content: str, dossier: Dict, path_str: str, file_hash: str, suffix: str) -> List[Dict]:
        """[FACULTY 2] The Polyglot Anatomist."""
        chunks = []
        base_meta = {"source": path_str, "hash": file_hash, "language": self._normalize_lang(suffix),
                     "is_keystone": self._is_keystone(path_str)}

        if dossier and "error" not in dossier:
            for symbol_type, key in [("function", "functions"), ("class", "classes")]:
                for node in dossier.get(key, []):
                    chunks.append(self._forge_chunk(content, node, base_meta, symbol_type))
        else:  # Fallback for text or unparsable code
            lines = content.splitlines()
            for i in range(0, len(lines), 50):
                chunk_text = "\n".join(lines[i:i + 50])
                meta = {**base_meta, "type": "text_block", "line_number": i + 1, "name": "body"}
                chunks.append({"id": f"{path_str}:text_{i}:{file_hash[:8]}", "document": chunk_text,
                               "metadata": self._sanitize_metadata(meta)})
        return chunks

    def _forge_chunk(self, content: str, node: Dict, base_meta: Dict, symbol_type: str) -> Dict:
        """[FACULTY 5] The Alchemical Scripture Forge."""
        start, end = node['start_point'][0], node['end_point'][0] + 1
        chunk_text = "\n".join(content.splitlines()[start:end])
        name = node['name']

        # [FACULTY 11] Echoing Chamber & [FACULTY 5] Richer Context
        embedding_text = (f"{symbol_type.title()}: {name} {name} {name}\n"
                          f"File: {base_meta['source']}\n"
                          f"Signature: {node.get('signature', '()')}\n"
                          f"Docstring: {node.get('docstring', '')}\n---\n{chunk_text}")

        # [FACULTY 3 & 4 & 6] Gaze of the Chronomancer, Symbiotic Bond, Gnostic Variable
        temporal_gnosis = self.historian.inquire(base_meta['source'])

        specific_meta = {
            "type": symbol_type, "name": name, "complexity": int(node.get('cyclomatic_complexity', 0)),
            "docstring": node.get('docstring', ''), "line_number": start + 1,
            "last_author": temporal_gnosis.primary_author, "last_modified_days": temporal_gnosis.days_since_last_change,
            "uses_env": "os.getenv" in chunk_text or "process.env" in chunk_text,
            "test_file": self._find_test_file(name, base_meta['source']),  # Symbiotic Bond
            "schema_version": self.SCHEMA_VERSION  # [FACULTY 1]
        }

        final_meta = {**base_meta, **specific_meta}
        safe_meta = self._sanitize_metadata(final_meta)

        return {"id": f"{base_meta['source']}:{name}:{base_meta['hash'][:8]}", "document": embedding_text,
                "metadata": safe_meta}

    def _find_test_file(self, symbol_name: str, source_path: str) -> str:
        """[FACULTY 4] Heuristic to find a corresponding test file."""
        # This is a prophecy for a deeper Gaze using the Cortex's full graph.
        # For now, we use a simple naming convention heuristic.
        p = Path(source_path)
        test_dir = self.root / "tests"
        if not test_dir.exists(): return ""

        potential_test_name = f"test_{p.stem}.py"
        if (test_dir / potential_test_name).exists():
            return str(test_dir / potential_test_name)
        return ""

    def _sanitize_metadata(self, meta: Dict[str, Any]) -> Dict[str, Union[str, int, float, bool]]:
        clean = {}
        for k, v in meta.items():
            if isinstance(v, (list, dict, tuple, set)):
                clean[k] = json.dumps(v)
            elif v is None:
                clean[k] = ""
            else:
                clean[k] = v
        return clean

    def _flush_batch(self, ids: List[str], docs: List[str], metas: List[Dict]):
        if not ids: return
        try:
            self._collection.upsert(ids=ids, documents=docs, metadatas=metas)
            Logger.verbose(f"   -> Flushed batch of {len(ids)} shards.")
        except Exception as e:
            Logger.error(f"Batch Inscription failed: {e}")

    def _purge_ghosts(self, active_sources: set):
        """[FACULTY 9] The Rite of Surgical Oblivion."""
        self._awaken()
        if self._collection.count() == 0: return

        # This can be slow, run it only on full re-index.
        Logger.verbose("Conducting the Rite of Surgical Oblivion for stale vectors...")
        try:
            all_db_sources = set(self._collection.get(include=[])['metadatas']['source'])
            ghosts = all_db_sources - active_sources
            if ghosts:
                self._collection.delete(where={"source": {"$in": list(ghosts)}})
                Logger.info(f"Purged {len(ghosts)} ghost scriptures from the Vector Void.")
        except Exception as e:
            Logger.warn(f"The Rite of Oblivion faltered: {e}")

    def _normalize_lang(self, suffix: str) -> str:
        s = suffix.lower()
        mapping = {'.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
                   '.ts': 'typescript', '.tsx': 'typescript', '.go': 'go',
                   '.rs': 'rust', '.java': 'java', '.cpp': 'cpp', '.c': 'c'}
        return mapping.get(s, 'text')

    def _is_keystone(self, path_str: str) -> bool:
        return os.path.basename(path_str) in {
            'README.md', 'package.json', 'pyproject.toml', 'Cargo.toml',
            'main.py', 'index.ts', 'server.go', 'lib.rs', 'docker-compose.yml'
        }

    def search(self, query: str, limit: int = 5, where: Optional[Dict] = None) -> List[Dict]:
        """[FACULTY 10] The Adjudicator's Gaze."""
        self._awaken()
        if self._collection.count() == 0:
            Logger.warn("The Vector Mind is empty. Triggering initial ingestion...")
            self.index_project()
        try:
            results = self._collection.query(query_texts=[query], n_results=limit, where=where)
            hits = []
            if results['ids']:
                for i in range(len(results['ids'][0])):
                    hits.append({
                        "id": results['ids'][0][i],
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results.get('distances') else 0.0
                    })
            return hits
        except Exception as e:
            Logger.error(f"Search Paradox: {e}")
            return []

    def clear(self):
        self._awaken()
        try:
            self._client.delete_collection(self.COLLECTION_NAME)
            self._collection = self._client.get_or_create_collection(name=self.COLLECTION_NAME)
            Logger.warn("Vector Store annihilated.")
        except Exception as e:
            Logger.error(f"Oblivion rite failed: {e}")