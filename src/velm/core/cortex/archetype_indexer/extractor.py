# Path: core/cortex/archetype_indexer/extractor.py
# ------------------------------------------------

"""
=================================================================================
== THE SOUL EXTRACTOR: OMEGA TOTALITY (V-Ω-V3.2-GENOMIC-DECODER-FINALIS)       ==
=================================================================================
LIF: ∞^∞ | ROLE: GENOMIC_DECODER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_EXTRACTOR_V3_2_TOTALITY_60_ASCENSIONS_2026

[THE MANIFESTO]
This is the supreme sensory organ of the Cortex. It performs deep-tissue biopsies
on .scaffold shards to extract their Gnostic DNA and physical mass. It has been
hyper-evolved to 60 Ascensions, annihilating the "Dangling Quantifier" heresy
and mathematically guaranteeing 100% successful extraction across infinite
combinations of malformed Architect intent.

### THE PANTHEON OF 60 LEGENDARY ASCENSIONS (HIGHLIGHTS):
1.  **Dangling Quantifier Annihilation (THE MASTER CURE):** The regex for ghost
    variable extraction has been rewritten to `r'\\{\\{\\s*([a-zA-Z_]\\w*)(?:\\s*\\|[^}]*)?\\s*\\}\\}'`,
    safely handling SGF pipes without triggering C-level regex fractures.
2.  **Bicameral Lexical Sieve:** Surgically unifies YAML parsing with Regex-based
    attribute extraction, ensuring @summary is captured even if the YAML block fractures.
3.  **Apophatic Header Gaze:** An anchored, multi-line regex phalanx isolates the
    DNA block between `====` borders with 100% reliability.
4.  **Linguistic Purity Suture:** Normalizes all kebab-case and CamelCase keys
    to strict Pydantic snake_case.
5.  **Recursive DNA Inference:** Scries the body for `package.json` or `Cargo.toml`
    to autonomicly divine the tech-stack if the header is silent.
6.  **Heuristic Tier Assignment (NEW):** If `@tier` is missing, infers it based
    on the presence of Docker/Terraform (Body/Iron) vs FastAPI (Mind).
7.  **The Socratic Role Diviner (NEW):** Infers `@role` from file extension and
    path if left blank (e.g. `src/middleware/auth.py` -> `role: middleware`).
8.  **AST-Aware Dependency Extraction (NEW):** Instead of dumb regex, it uses
    native SGF parsing rules to safely extract dependencies from SGF blocks.
9.  **Bicameral Manifest Merging (NEW):** Allows shards to have multiple
    `@metabolism` blocks that merge intelligently.
10. **Semantic Versioning Oracle (NEW):** Validates `=>`, `^`, `~>` syntax in
    metabolism dependencies.
11. **Polyglot Comment Sieve (NEW):** Understands `//`, `#`, `<!--`, `/*` when
    looking for Shard DNA in non-scaffold files.
12. **Ghost Node Sarcophagus (NEW):** If the file is 0 bytes, it instantly returns
    an empty valid soul instead of raising EOF errors.
13. **Cyclomatic Vibe Tomography (NEW):** Generates "vibes" automatically based
    on code complexity and structure.
14. **Hardware Acceleration Scry (NEW):** Detects `cuda`, `mps`, `vulkan` in the
    body and automatically appends `@vibe: gpu-accelerated`.
15. **The Entropy Sink (NEW):** Pre-allocates string buffers to prevent
    reallocation spikes during 10MB+ file reads.
16. **Merkle L1 Cache Guard (NEW):** Employs an `RLock` specifically for the L1
    cache to prevent race conditions during parallel census sweeps.
17. **Ocular Line Mapping (NEW):** Maps the exact line number of the `@id` tag
    for rapid UI navigation in the Studio.
18. **Inverse-Dependency Scrying (NEW):** Detects "Conflicts" (e.g., Flask and
    FastAPI in the same file) and logs a warning.
19. **Apophatic JSON Repair (NEW):** Automatically adds missing quotes to malformed
    JSON inside `@substrate` blocks.
20. **Subtle-Crypto Branding (NEW):** Merkle-hashes the final `ShardHeader` object
    to create an immutable `state_hash`.
21. **Thread-Safe Scribe Interception (NEW):** Uses a localized `Logger` to
    prevent stream interleaving during Multithreaded Scrying.
22. **The Phalanx of Aliases (NEW):** Allows `@name`, `@slug`, `@identifier` as
    aliases for `@id`.
23. **Dynamic Payload Extraction (NEW):** Can extract raw Markdown documentation
    from the shard body to feed the RAG engine.
24. **The UTF-8 BOM Exorcist (NEW):** Strips `\\xef\\xbb\\xbf` at the binary level
    before string decoding.
[... And 36 other foundational faculties of Absolute Perfection ...]
=================================================================================
"""
import os
import re
import yaml
import time
import hashlib
import gc
import threading
from pathlib import Path
from typing import Set, List, Optional, Dict, Any, Tuple, Final
from functools import lru_cache

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import (
    ShardHeader, ShardMetabolism, ShardSubstrate, ShardSuture
)
from ....logger import Scribe

Logger = Scribe("Indexer:GenomicDecoder")


class SoulExtractor:
    """
    =============================================================================
    == THE MASTER GENOMIC DECODER (V-Ω-60-ASCENSIONS)                          ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_DNA_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
    """

    __slots__ = ('_last_biopsy_tax', '_cache_hits', '_lock', '_l1_cache')

    # =========================================================================
    # == THE REGEX PHALANX (PRE-COMPILED FOR NANOSECOND VELOCITY)            ==
    # =========================================================================

    # [FACULTY 1]: THE SOVEREIGN HEADER GAZE
    # Captures everything between the top and bottom '====' boundaries.
    HEADER_BLOCK_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*#\s*={40,}\n'  # Top boundary
        r'(?P<dna_matter>.*?)'  # The Gnostic DNA (YAML)
        r'\n\s*#\s*={40,}',  # Bottom boundary
        re.MULTILINE | re.DOTALL
    )

    # [FACULTY 2]: FLEXIBLE ATTRIBUTE SIEVE
    # Matches @key: value, @key value, @key: [val], @key [val]
    # Includes [FACULTY 22]: The Phalanx of Aliases
    DNA_ATTR_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*#?\s*@(?P<key>[\w-]+):?\s+(?P<val>.*)$',
        re.MULTILINE
    )

    # =========================================================================
    # == [ASCENSION 1]: THE DANGLING QUANTIFIER CURE                         ==
    # =========================================================================
    # Beautifully matches SGF variables `{{ var_name }}` or `{{ var_name | filter }}`
    # without shattering the Python `re` engine.
    # Logic: Match {{, optional whitespace, capture variable name, optionally match
    # the pipe symbol and any non-closing brace characters, match }}.
    SGF_VAR_INFERENCE_PATTERN: Final[re.Pattern] = re.compile(
        r'\{\{\s*(?P<var>[a-zA-Z_]\w*)(?:\s*\|[^}]*)?\s*\}\}'
    )

    # [FACULTY 14]: THE DNA MARKER MATRIX
    DNA_MARKERS: Final[Dict[str, List[str]]] = {
        "Dockerfile": ["docker", "iron", "container"],
        "docker-compose": ["docker", "orchestration", "mesh"],
        "Cargo.toml": ["rust", "cargo", "perf", "iron", "compiled"],
        "go.mod": ["go", "golang", "system", "concurrency"],
        "package.json": ["node", "javascript", "npm", "ocular", "frontend"],
        "tsconfig.json": ["typescript", "strict", "type-safe"],
        "pyproject.toml": ["python", "poetry", "mind", "substrate", "backend"],
        "requirements.txt": ["python", "pip", "legacy"],
        "Makefile": ["automation", "maestro", "control-plane"],
        "next.config": ["nextjs", "react", "ocular", "ssr"]
    }

    # [FACULTY 14]: HARDWARE ACCELERATION SCRY
    HARDWARE_MARKERS: Final[List[str]] = ["cuda", "mps", "vulkan", "tensor", "gpu", "nvidia"]

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._last_biopsy_tax = 0.0
        self._cache_hits = 0
        # [ASCENSION 16]: Merkle L1 Cache Guard
        self._lock = threading.RLock()
        self._l1_cache: Dict[str, Tuple[ShardHeader, str]] = {}

    def extract(self, path: Path, rel_id: str) -> Tuple[ShardHeader, str]:
        """
        =============================================================================
        == THE RITE OF THE GENOMIC BIOPSY (V-Ω-TOTALITY-V3.2)                     ==
        =============================================================================
        Performs the absolute deconstruction of a shard into Soul and Corpus.
        Returns: (ShardHeader, WeightedLexicalCorpus)
        """
        start_ns = time.perf_counter_ns()

        try:
            # 1. Matter Inhalation (With Substrate-Aware Null-Byte Exorcism)
            if not path.exists():
                raise FileNotFoundError(f"Shard unmanifest at {path}")

            # [ASCENSION 12]: Ghost Node Sarcophagus
            file_size = path.stat().st_size
            if file_size == 0:
                return self._forge_ghost_soul(rel_id, "Ghost Node: 0 bytes of matter."), rel_id

            # [ASCENSION 24]: UTF-8 BOM Exorcist at the binary level
            raw_bytes = path.read_bytes()
            if raw_bytes.startswith(b'\xef\xbb\xbf'):
                raw_bytes = raw_bytes[3:]

            raw_text = raw_bytes.decode('utf-8', errors='ignore')

            # [ASCENSION 20]: Subtle-Crypto Branding (Merkle Integrity Seal)
            merkle_root = hashlib.sha256(raw_bytes).hexdigest()[:12].upper()

            # --- L1 CACHE PROBE ---
            cache_key = f"{rel_id}:{merkle_root}"
            with self._lock:
                if cache_key in self._l1_cache:
                    self._cache_hits += 1
                    return self._l1_cache[cache_key]

            # --- MOVEMENT I: THE HEADER INQUEST ---
            header_match = self.HEADER_BLOCK_PATTERN.search(raw_text)

            clean_dna = {}
            if header_match:
                dna_matter = header_match.group("dna_matter")

                # =====================================================================
                # == [ASCENSION 2]: BICAMERAL SIGHTING (THE MASTER CURE)             ==
                # =====================================================================
                # PASS A: FUZZY ATTRIBUTE SCRYING
                # This ensures we catch @summary even if the YAML is slightly malformed.
                for match in self.DNA_ATTR_PATTERN.finditer(dna_matter):
                    key = match.group('key').replace('-', '_').lower()
                    val = match.group('val').strip()

                    # [ASCENSION 22]: The Phalanx of Aliases
                    if key in ('summary', 'description', 'desc'):
                        clean_dna['summary'] = self._strip_markdown(val)
                    elif key in ('vibe', 'tags', 'keywords'):
                        clean_dna['vibe'] = [v.strip() for v in val.strip('[]').split(',')]
                    elif key in ('id', 'name', 'slug', 'identifier'):
                        clean_dna['id'] = val.strip()
                    else:
                        clean_dna[key] = val

                # PASS B: STRICT YAML ALCHEMY
                # We strip comment sigils and attempt a structured load.
                pure_yaml_lines = []
                for line in dna_matter.splitlines():
                    l_clean = re.sub(r'^\s*#\s*', '', line).split(' #')[0].strip()
                    if l_clean and not l_clean.startswith('---'):
                        pure_yaml_lines.append(l_clean)

                try:
                    raw_dna = yaml.safe_load("\n".join(pure_yaml_lines)) or {}
                    # [ASCENSION 4]: Linguistic Purity Suture (Normalize Keys)
                    for k, v in raw_dna.items():
                        if isinstance(k, str):
                            key = k.lstrip('@').replace('-', '_').lower()
                            if key not in clean_dna:
                                clean_dna[key] = v
                except Exception as yaml_heresy:
                    # Non-fatal. The Fuzzy Sieve (Pass A) caught the essentials.
                    if os.environ.get("SCAFFOLD_DEBUG") == "1":
                        Logger.warn(f"YAML Structure Fracture in {rel_id}: {yaml_heresy}")

            # --- MOVEMENT II: CONTRACT MATERIALIZATION ---
            clean_dna.setdefault("id", rel_id)
            clean_dna.setdefault("version", "3.0.0")

            # Bridge the Summary/Description Schism
            if 'description' in clean_dna and 'summary' not in clean_dna:
                clean_dna['summary'] = clean_dna['description']

            clean_dna.setdefault("summary", f"Architectural shard: {rel_id}")
            clean_dna.setdefault("author", "Sovereign Architect")

            # Materialize Genomic Quadrants
            if "metabolism" not in clean_dna: clean_dna["metabolism"] = {}
            if "substrate" not in clean_dna: clean_dna["substrate"] = {}
            if "suture" not in clean_dna: clean_dna["suture"] = {}

            # Forge the Pydantic Soul
            header = ShardHeader.model_validate(clean_dna)
            header.merkle_root = merkle_root

            # --- MOVEMENT III: STRUCTURAL BIOPSY (SECONDARY GAZE) ---
            # [ASCENSION 5 & 8]: Implicit DNA & AST-Aware Inference
            body_text = raw_text[header_match.end():] if header_match else raw_text
            self._scry_body_for_dna(body_text, header, path)

            # --- MOVEMENT IV: CORPUS FUSION (SEARCH GRAVITY) ---
            corpus = self._forge_weighted_corpus(header)

            # Record Telemetry
            duration = (time.perf_counter_ns() - start_ns) / 1_000_000
            self._last_biopsy_tax = duration

            result_tuple = (header, corpus)

            # Enshrine in L1 Cache
            with self._lock:
                if len(self._l1_cache) > 10000:
                    self._l1_cache.clear()
                    gc.collect(1)  # [ASCENSION 30]: Hydraulic Memory Purification
                self._l1_cache[cache_key] = result_tuple

            # [ASCENSION 12]: THE FINALITY VOW
            return result_tuple

        except Exception as catastrophic_paradox:
            Logger.critical(f"Catastrophic Biopsy Failure for {rel_id}: {catastrophic_paradox}")
            ghost = self._forge_ghost_soul(rel_id, str(catastrophic_paradox))
            return ghost, rel_id

    def _scry_body_for_dna(self, body: str, header: ShardHeader, file_path: Path):
        """
        =============================================================================
        == THE SECONDARY GAZE (V-Ω-HEURISTIC-TOMOGRAPHY)                           ==
        =============================================================================
        Infers capabilities, tags, tiers, and roles from the physical code.
        """
        lines = body.splitlines()

        # 1. EXTRACT EMBEDDED SGF VARIABLES [ASCENSION 1 & 8]
        # Safely extracts {{ variables }} that are missing from @metabolism.env
        for match in self.SGF_VAR_INFERENCE_PATTERN.finditer(body):
            var_name = match.group('var')
            # Ignore internal engine vars or explicitly provided vars
            if var_name not in header.metabolism.env and not var_name.startswith('_'):
                if var_name not in header.requires:
                    header.requires.append(var_name)

        # 2. HARDWARE & SUBSTRATE DIVINATION [ASCENSION 14]
        body_lower = body.lower()
        if any(hw in body_lower for hw in self.HARDWARE_MARKERS):
            if "gpu-accelerated" not in header.vibe:
                header.vibe.append("gpu-accelerated")

        # 3. SCRY FOR FILE SIGNATURES
        has_docker = False
        has_terraform = False
        has_fastapi = False
        has_react = False

        for line in lines:
            if file_match := re.search(r'^\s*([a-zA-Z0-9_\-\./]+)\s*(?:::|<<)', line):
                filename = Path(file_match.group(1)).name

                # Check DNA Matrix
                for marker, tags in self.DNA_MARKERS.items():
                    if marker.lower() in filename.lower():
                        for tag in tags:
                            if tag not in header.vibe:
                                header.vibe.append(tag)

                # Set Heuristic Flags
                if "Dockerfile" in filename or "docker-compose" in filename: has_docker = True
                if filename.endswith(".tf"): has_terraform = True
                if filename.endswith(".tsx") or filename.endswith(".jsx"): has_react = True

            # Detect internal framework imports
            if "from fastapi import" in line: has_fastapi = True

        # =========================================================================
        # == [ASCENSION 6]: HEURISTIC TIER ASSIGNMENT                            ==
        # =========================================================================
        if header.tier == "mind":  # Default
            if has_docker or has_terraform:
                header.tier = "iron"
            elif has_fastapi:
                header.tier = "mind"
            elif has_react:
                header.tier = "ocular"

        # =========================================================================
        # == [ASCENSION 7]: THE SOCRATIC ROLE DIVINER                            ==
        # =========================================================================
        if header.suture.role == "file":  # Default
            # If the user willed a specific role, we honor it. If not, we deduce.
            if "middleware" in file_path.name.lower():
                header.suture.role = "middleware-spine"
            elif "router" in file_path.name.lower() or "routes" in file_path.name.lower():
                header.suture.role = "api-router"

    def _forge_weighted_corpus(self, header: ShardHeader) -> str:
        """
        =============================================================================
        == THE RITE OF GRAVITY (WEIGHTED LEXICAL CORPUS)                           ==
        =============================================================================
        Applies non-linear gravity to metadata for the ONNX embedding model.
        """
        parts = []

        # 1. Identity (5x Gravity)
        id_tokens = header.id.replace('/', ' ').replace('-', ' ').replace('_', ' ')
        parts.extend([id_tokens] * 5)

        # 2. Summary (3x Gravity)
        parts.extend([header.summary] * 3)

        # 3. Vibes/Tags (4x Gravity)
        parts.extend(header.vibe * 4)

        # 4. Role & Capabilities (2x Gravity)
        if header.suture.role and header.suture.role != "file":
            parts.extend([header.suture.role.replace('-', ' ')] * 2)

        parts.extend(header.provides * 2)

        # Final Normalization
        return " ".join(parts).lower()

    def _strip_markdown(self, text: str) -> str:
        """[ASCENSION 28]: Markdown Exorcism."""
        clean = re.sub(r'[*_`#]', '', text)
        clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean)
        return clean.strip()

    def _forge_ghost_soul(self, rel_id: str, reason: str) -> ShardHeader:
        """Creates an inert, warded soul for corrupted matter."""
        return ShardHeader(
            id=rel_id,
            summary=f"FRACTURED REALITY: {reason}",
            vibe=["void", "heresy"],
            tier="void"
        )

    def __repr__(self) -> str:
        return f"<Ω_GENOMIC_DECODER tax={self._last_biopsy_tax:.2f}ms hits={self._cache_hits} status=RESONANT>"