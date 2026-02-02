# scaffold/semantic_injection/directives/neuron_knowledge/memory.py

"""
=================================================================================
== THE NEURAL MEMORY (V-Ω-RAG-ULTIMA)                                          ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000

This artisan generates production-grade Retrieval-Augmented Generation (RAG)
pipelines. It handles the full lifecycle of memory: Text Splitting, Embedding,
Vector Storage, and Intelligent Retrieval.

Usage:
    @neuron/rag(db="qdrant", embed="openai", strategy="mmr")
=================================================================================
"""
from contextlib import contextmanager
from typing import List, Dict, Set


# =============================================================================
# == THE GNOSTIC CODE BUILDER (STANDARD)                                     ==
# =============================================================================

class GnosticCodeBuilder:
    """
    A stateful engine for constructing indented code without string-mashing.
    """

    def __init__(self, indent_char: str = "    "):
        self.lines: List[str] = []
        self.level: int = 0
        self.indent_char: str = indent_char
        self.imports: Set[str] = set()
        self.from_imports: Dict[str, Set[str]] = {}
        self.metadata: List[str] = []

    def add_import(self, module: str):
        self.imports.add(module)

    def add_from_import(self, module: str, name: str):
        if module not in self.from_imports:
            self.from_imports[module] = set()
        self.from_imports[module].add(name)

    def add_metadata(self, key: str, value: str):
        self.metadata.append(f"# {key}: {value}")

    def add(self, line: str = ""):
        if not line:
            self.lines.append("")
        else:
            self.lines.append((self.indent_char * self.level) + line)

    @contextmanager
    def block(self, header: str):
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1
            self.add("")

    def render(self) -> str:
        output = []
        if self.metadata:
            output.extend(self.metadata)
            output.append("")

        if self.imports:
            output.extend([f"import {m}" for m in sorted(self.imports)])
        if self.from_imports:
            for mod in sorted(self.from_imports.keys()):
                names = ", ".join(sorted(self.from_imports[mod]))
                output.append(f"from {mod} import {names}")

        if self.imports or self.from_imports:
            output.append("")
            output.append("")

        output.extend(self.lines)
        return "\n".join(output).strip()


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_rag_pipeline(
        vector_db: str = "chroma",
        embedding: str = "openai",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        strategy: str = "similarity",  # similarity, mmr
        collection_name: str = "scaffold_memory"
) -> str:
    """
    Forges a complete RAG Pipeline Class.
    """
    cb = GnosticCodeBuilder()

    # --- 1. Configuration & Imports ---
    db_key = vector_db.lower()
    embed_key = embedding.lower()

    # Base Requirements
    reqs = ["langchain", "langchain-core", "langchain-text-splitters"]

    cb.add_import("os")
    cb.add_import("hashlib")
    cb.add_from_import("typing", "List")
    cb.add_from_import("typing", "Dict")
    cb.add_from_import("typing", "Any")
    cb.add_from_import("typing", "Optional")

    cb.add_from_import("langchain_core.documents", "Document")
    cb.add_from_import("langchain_text_splitters", "RecursiveCharacterTextSplitter")

    # --- 2. Embedding Strategy ---
    if embed_key == "openai":
        reqs.append("langchain-openai")
        cb.add_from_import("langchain_openai", "OpenAIEmbeddings")
        embed_class = "OpenAIEmbeddings"
        embed_init = 'model="text-embedding-3-small"'
    elif embed_key == "local" or embed_key == "huggingface":
        reqs.append("langchain-huggingface")
        reqs.append("sentence-transformers")
        cb.add_from_import("langchain_huggingface", "HuggingFaceEmbeddings")
        embed_class = "HuggingFaceEmbeddings"
        embed_init = 'model_name="all-MiniLM-L6-v2"'
    else:
        # Fallback
        reqs.append("langchain-openai")
        cb.add_from_import("langchain_openai", "OpenAIEmbeddings")
        embed_class = "OpenAIEmbeddings"
        embed_init = ""

    # --- 3. Vector DB Strategy ---
    if db_key == "chroma":
        reqs.append("langchain-chroma")
        cb.add_from_import("langchain_chroma", "Chroma")
        db_class = "Chroma"

    elif db_key == "pgvector":
        reqs.append("langchain-postgres")
        reqs.append("psycopg2-binary")
        cb.add_from_import("langchain_postgres", "PGVector")
        db_class = "PGVector"

    elif db_key == "qdrant":
        reqs.append("langchain-qdrant")
        reqs.append("qdrant-client")
        cb.add_from_import("langchain_qdrant", "QdrantVectorStore")
        cb.add_from_import("qdrant_client", "QdrantClient")
        db_class = "QdrantVectorStore"

    elif db_key == "pinecone":
        reqs.append("langchain-pinecone")
        reqs.append("pinecone-client")
        cb.add_from_import("langchain_pinecone", "PineconeVectorStore")
        db_class = "PineconeVectorStore"

    cb.add_metadata("requirements", ", ".join(reqs))

    # --- 4. The Class Definition ---
    with cb.block("class NeuralMemory:"):

        # __init__
        with cb.block("def __init__(self):"):
            cb.add('"""Initialize the Cortex: Embeddings, Splitter, and Vector Store."""')

            # A. Embeddings
            cb.add("# 1. Initialize Embeddings")
            cb.add(f"self.embeddings = {embed_class}({embed_init})")

            # B. Text Splitter
            cb.add("")
            cb.add("# 2. Initialize Text Splitter (The Maester)")
            cb.add(f"self.text_splitter = RecursiveCharacterTextSplitter(")
            cb.add(f"    chunk_size={chunk_size},")
            cb.add(f"    chunk_overlap={chunk_overlap}")
            cb.add(")")

            # C. Vector Store
            cb.add("")
            cb.add(f"# 3. Initialize Vector Store ({db_key.title()})")

            if db_key == "chroma":
                cb.add("self.vector_store = Chroma(")
                cb.add("    collection_name='scaffold_memory',")
                cb.add("    embedding_function=self.embeddings,")
                cb.add("    persist_directory='./chroma_db' # Local persistence")
                cb.add(")")

            elif db_key == "pgvector":
                cb.add("connection_string = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/db')")
                cb.add("self.vector_store = PGVector(")
                cb.add("    embeddings=self.embeddings,")
                cb.add(f"    collection_name='{collection_name}',")
                cb.add("    connection=connection_string")
                cb.add(")")

            elif db_key == "qdrant":
                cb.add("url = os.getenv('QDRANT_URL', 'http://localhost:6333')")
                cb.add("api_key = os.getenv('QDRANT_API_KEY')")
                cb.add("client = QdrantClient(url=url, api_key=api_key)")
                cb.add("self.vector_store = QdrantVectorStore(")
                cb.add("    client=client,")
                cb.add(f"    collection_name='{collection_name}',")
                cb.add("    embedding=self.embeddings")
                cb.add(")")

            elif db_key == "pinecone":
                cb.add("# Requires PINECONE_API_KEY env var")
                cb.add("self.vector_store = PineconeVectorStore(")
                cb.add(f"    index_name='{collection_name}',")
                cb.add("    embedding=self.embeddings")
                cb.add(")")

            # D. Retriever
            cb.add("")
            cb.add("# 4. Initialize Retriever")
            search_kwargs = "{'k': 4}"
            if strategy == "mmr":
                search_kwargs = "{'k': 4, 'fetch_k': 20}"

            cb.add(f"self.retriever = self.vector_store.as_retriever(")
            cb.add(f"    search_type='{strategy}',")
            cb.add(f"    search_kwargs={search_kwargs}")
            cb.add(")")

        # Helper: Idempotency Hash
        cb.add("")
        with cb.block("def _generate_hash(self, content: str) -> str:"):
            cb.add('"""Generates a deterministic hash for content idempotency."""')
            cb.add("return hashlib.sha256(content.encode('utf-8')).hexdigest()")

        # Method: Ingest
        cb.add("")
        with cb.block("async def ingest(self, text: str, metadata: Optional[Dict[str, Any]] = None):"):
            cb.add('"""Splits, hashes, and ingests text into the Vector Store."""')
            cb.add("meta = metadata or {}")

            # Split
            cb.add("# 1. Split Text")
            cb.add("docs = self.text_splitter.create_documents([text], metadatas=[meta])")

            # Hash & Tag
            cb.add("")
            cb.add("# 2. Tag with Idempotency Hash")
            with cb.block("for doc in docs:"):
                cb.add("doc_hash = self._generate_hash(doc.page_content)")
                cb.add("doc.metadata['source_hash'] = doc_hash")
                # Note: Real idempotency requires checking DB existence, complex for generic.
                # Adding hash to metadata allows downstream filtering.

            # Add
            cb.add("")
            cb.add("# 3. Index")
            cb.add("await self.vector_store.aadd_documents(docs)")
            cb.add("print(f'[Memory] Ingested {len(docs)} chunks.')")

        # Method: Retrieve
        cb.add("")
        with cb.block("async def retrieve(self, query: str, k: int = 4) -> List[Document]:"):
            cb.add('"""Retrieves relevant documents from the store."""')
            # Allow runtime override of k
            cb.add("# Temporarily override K if needed, or just use retriever default")
            cb.add("results = await self.retriever.ainvoke(query)")
            cb.add("return results[:k]")

        # Method: Clear (For testing/reset)
        cb.add("")
        with cb.block("async def clear(self):"):
            cb.add('"""Annihilates all memories (Danger)."""')
            cb.add("try:")
            if db_key == "chroma":
                cb.add("    self.vector_store.delete_collection()")
                cb.add("    print('[Memory] Chroma collection cleared.')")
            else:
                cb.add("    # Not all providers support simple clear via LangChain interface")
                cb.add("    print('[Memory] Clear not fully implemented for this provider.')")
            cb.add("except Exception as e:")
            cb.add("    print(f'[Memory] Failed to clear: {e}')")

    # --- 5. The Living Main (Integration Test) ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        cb.add("import asyncio")

        with cb.block("async def main():"):
            # Environment Check
            required_keys = ["OPENAI_API_KEY"]
            if db_key == "pinecone": required_keys.append("PINECONE_API_KEY")
            if db_key == "qdrant": required_keys.append("QDRANT_URL")

            for key in required_keys:
                cb.add(f"if not os.getenv('{key}'):")
                cb.add(f"    print('[Error] Missing {key}. Memory cannot awaken.')")
                # cb.add("    return") # Soft return for generated code readability

            cb.add("")
            cb.add("print('⚡ Awakening Neural Memory...')")
            cb.add("memory = NeuralMemory()")

            cb.add("")
            cb.add("print('📥 Ingesting Genesis Gnosis...')")
            cb.add("genesis_text = \"The Scaffold Engine is a tool for Symbiotic Creation. It unifies Form and Will.\"")
            cb.add("await memory.ingest(genesis_text, {'source': 'genesis.txt'})")

            cb.add("")
            cb.add("query = 'What is the purpose of Scaffold?'")
            cb.add("print(f'🔍 Dreaming of: {query}')")
            cb.add("results = await memory.retrieve(query)")

            cb.add("")
            with cb.block("for i, doc in enumerate(results):"):
                cb.add("print(f'   [{i+1}] {doc.page_content} (Source: {doc.metadata.get(\"source\")})')")

        cb.add("")
        cb.add("asyncio.run(main())")

    return cb.render()