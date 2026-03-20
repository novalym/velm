# Path: core/cortex/archetype_indexer/extractor.py
# ------------------------------------------------

"""
=================================================================================
== THE SOUL EXTRACTOR: APOTHEOSIS (V-Ω-TOTALITY-VMAX-33-ASCENSIONS-FINALIS)    ==
=================================================================================
LIF: ∞^∞ | ROLE: GENOMIC_DECODER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_EXTRACTOR_VMAX_ETHEREAL_GAZE_2026_FINALIS

[THE MANIFESTO]
This is the supreme definitive authority for architectural DNA deconstruction.
It has been radically transfigured to achieve 'Spatiotemporal Omniscience'—it
righteously implements the **Ethereal Gaze**, mathematically annihilating the
"Virtual Path Schism" that previously shattered the biopsy of internal Engine matter.

### THE PANTHEON OF 33 LEGENDARY ASCENSIONS:
[... existing ascensions ...]
33. **[ASCENSION IV] The Iron Genomic Biopsy (THE MASTER CURE):** Bypasses the
    Python `re.MULTILINE` overhead by offloading the entire YAML Header extraction
    to the Rust Binary Core (`fast_genomic_extract`).
=================================================================================
"""

import os
import re
import yaml
import time
import hashlib
import gc
import sys
import threading
from pathlib import Path
from typing import Set, List, Optional, Dict, Any, Tuple, Final, Union

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import (
    ShardHeader, ShardMetabolism, ShardSubstrate, ShardSuture
)
from ....logger import Scribe

# [ASCENSION 33]: Binary Kernel Pivot
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("Indexer:GenomicDecoder")


class SoulExtractor:
    """
    =============================================================================
    == THE OMEGA GENOMIC DECODER (V-Ω-TOTALITY-VMAX-33-ASCENSIONS)             ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_DNA_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
    """

    # [ASCENSION 6]: Pydantic Decapitation
    __slots__ = ('_last_biopsy_tax', '_cache_hits', '_lock', '_l1_cache', '_trace_id')

    # =========================================================================
    # == THE SENSORY PHALANX (THE GRIMOIRE OF REGEX)                         ==
    # =========================================================================

    # [ASCENSION 1]: THE ETHEREAL GAZE PREFIXES
    # Virtual prefixes that represent Thought, not Matter.
    ETHEREAL_PREFIXES: Final[Tuple[str, ...]] = (
        "system:", "memory:", "virtual:", "BLOCK_HEADER:", "EDICT:", "LOGIC:", "VARIABLE:"
    )

    # [FACULTY 14]: THE SOVEREIGN HEADER GAZE (Fallback for Python)
    HEADER_BLOCK_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*#\s*={40,}\n'  # Top boundary
        r'(?P<dna_matter>.*?)'  # The Gnostic DNA (YAML)
        r'\n\s*#\s*={40,}',  # Bottom boundary
        re.MULTILINE | re.DOTALL
    )

    # [FACULTY 17]: LINGUISTIC PURITY SUTURE
    DNA_ATTR_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*#?\s*@(?P<key>[\w-]+):?\s+(?P<val>.*)$',
        re.MULTILINE
    )

    # [ASCENSION 9]: THE DANGLING QUANTIFIER CURE
    SGF_VAR_INFERENCE_PATTERN: Final[re.Pattern] = re.compile(
        r'\{\{\s*(?P<var>[a-zA-Z_]\w*)(?:\s*\|[^}]*)?\s*\}\}'
    )

    # [FACULTY 15]: THE DNA MARKER MATRIX
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

    HARDWARE_MARKERS: Final[List[str]] = ["cuda", "mps", "vulkan", "tensor", "gpu", "nvidia"]

    def __init__(self, trace_id: str = "tr-biopsy-void"):
        """[THE RITE OF INCEPTION]"""
        self._last_biopsy_tax = 0.0
        self._cache_hits = 0
        self._trace_id = trace_id
        self._lock = threading.RLock()
        self._l1_cache: Dict[str, Tuple[ShardHeader, str]] = {}

    def extract(self, path: Union[Path, str], rel_id: str, content: Optional[str] = None) -> Tuple[ShardHeader, str]:
        """
        =============================================================================
        == THE RITE OF THE GENOMIC BIOPSY: OMEGA (V-Ω-TOTALITY-VMAX-24-ASCENSIONS) ==
        =============================================================================
        LIF: ∞ | ROLE: ARCHITECTURAL_DNA_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_EXTRACT_VMAX_BICAMERAL_SUTURE_2026_FINALIS
        """
        _start_ns = time.perf_counter_ns()

        # [ASCENSION 2]: APOPHATIC PATH SUTURE
        path_str = str(path).replace('\\', '/')

        # [ASCENSION 3]: THE ETHEREAL GAZE
        # If the path is virtual or internal, we grant Absolute Amnesty from the Disk.
        if any(path_str.startswith(p) for p in self.ETHEREAL_PREFIXES) or "__init__" in path_str:
            soul = self._forge_stable_soul(rel_id, f"Ethereal Atom: manifest in Mind at {path_str}")
            return soul, rel_id

        try:
            # =========================================================================
            # == MOVEMENT I:[ASCENSION 1] - THE BICAMERAL CONTENT PASS (THE CURE)   ==
            # =========================================================================
            # If the Architect willed 'content' (from RAM), we bypass the Iron-Strike.
            if content is not None:
                # [ASCENSION 5 & 30]: Null-Byte & Type Suture
                raw_text = str(content).replace('\x00', '')
                raw_bytes = raw_text.encode('utf-8', errors='ignore')
            else:
                # Standard Physical Inception
                p = Path(path_str)
                if not p.exists():
                    # [ASCENSION 12]: SOCRATIC ERROR ENRICHMENT
                    raise FileNotFoundError(f"Coordinate Void: Physical iron unmanifest at {path_str}")

                # [ASCENSION 6]: BOM & Null-Byte Exorcism
                raw_bytes = p.read_bytes()
                if raw_bytes.startswith(b'\xef\xbb\xbf'):
                    raw_bytes = raw_bytes[3:]
                raw_text = raw_bytes.decode('utf-8', errors='ignore').replace('\x00', '')

            # [ASCENSION 7]: MERKLE INTEGRITY SEAL
            merkle_root = hashlib.sha256(raw_bytes).hexdigest()[:12].upper()

            # --- MOVEMENT II: [ASCENSION 8] - L1 RESONANCE PROBE ---
            cache_key = f"{rel_id}:{merkle_root}"
            with self._lock:
                if cache_key in self._l1_cache:
                    self._cache_hits += 1
                    return self._l1_cache[cache_key]

            # =========================================================================
            # == MOVEMENT III: [ASCENSION 33] - THE IRON GENOMIC BIOPSY (RUST CORE)  ==
            # =========================================================================
            # [THE MASTER CURE]: Use Rust's C-Speed Regex to pull the block.
            dna_matter = None
            header_end_idx = 0

            if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
                try:
                    rust_extracted = scaffold_core_rs.fast_genomic_extract(raw_text)
                    if "dna_matter" in rust_extracted:
                        dna_matter = rust_extracted["dna_matter"]
                        header_end_idx = int(rust_extracted["header_end_idx"])
                except Exception as e:
                    Logger.debug(f"Rust Biopsy fractured: {e}. Falling back to Python regex.")

            # Fallback to Python
            if dna_matter is None:
                header_match = self.HEADER_BLOCK_PATTERN.search(raw_text)
                if header_match:
                    dna_matter = header_match.group("dna_matter")
                    header_end_idx = header_match.end()

            # [ASCENSION 11]: IDENTITY LOCK
            clean_dna = {
                "id": rel_id,
                "version": "3.5.0-Ω",
                "merkle_root": merkle_root,
                "trace_id": self._trace_id
            }

            if dna_matter:
                self._scry_ocular_dna(dna_matter, clean_dna)
                # [ASCENSION 9]: BICAMERAL LEXICAL SIEVE (REGEX PASS)
                for match in self.DNA_ATTR_PATTERN.finditer(dna_matter):
                    key = match.group('key').replace('-', '_').lower()
                    val = match.group('val').strip()

                    # [ASCENSION 19]: SUMMARY SUTURE
                    if key in ('summary', 'description', 'desc'):
                        clean_dna['summary'] = self._strip_markdown(val)
                    elif key in ('vibe', 'tags', 'keywords'):
                        clean_dna['vibe'] = [v.strip() for v in val.strip('[]').split(',')]
                    elif key in ('id', 'name', 'slug'):
                        clean_dna['id'] = val.strip()
                    else:
                        clean_dna[key] = val

                # [ASCENSION 10]: STRICT YAML ALCHEMY (STRICT PASS)
                try:
                    yaml_lines = []
                    for line in dna_matter.splitlines():
                        l_clean = re.sub(r'^\s*#\s*', '', line).split(' #')[0].strip()
                        if l_clean and not l_clean.startswith('---'):
                            yaml_lines.append(l_clean)

                    raw_dna = yaml.safe_load("\n".join(yaml_lines)) or {}
                    # [ASCENSION 13]: LINGUISTIC PURITY SUTURE
                    for k, v in raw_dna.items():
                        if isinstance(k, str):
                            key = k.lstrip('@').replace('-', '_').lower()
                            if key not in clean_dna: clean_dna[key] = v
                except Exception:
                    pass

            # --- MOVEMENT IV: CONTRACT MATERIALIZATION ---
            if 'description' in clean_dna and 'summary' not in clean_dna:
                clean_dna['summary'] = clean_dna['description']

            clean_dna.setdefault("summary", f"Architectural shard: {rel_id}")
            clean_dna.setdefault("author", "Sovereign Architect")

            if "metabolism" not in clean_dna: clean_dna["metabolism"] = {}
            if "substrate" not in clean_dna: clean_dna["substrate"] = {}
            if "suture" not in clean_dna: clean_dna["suture"] = {}

            # [ASCENSION 4]: FORGE THE SOUL
            header = ShardHeader.model_validate(clean_dna)
            header.merkle_root = merkle_root

            # --- MOVEMENT V: [ASCENSION 14] - STRUCTURAL BIOPSY ---
            if "__" not in path_str:
                body_text = raw_text[header_end_idx:]
                self._scry_body_for_dna(body_text, header)

            # --- MOVEMENT VI: [ASCENSION 20] - CORPUS FUSION ---
            corpus = self._forge_weighted_corpus(header)
            result_tuple = (header, corpus)

            # [ASCENSION 16]: HYDRAULIC L1 CACHE ENTHRALLMENT
            with self._lock:
                if len(self._l1_cache) > 10000:
                    self._l1_cache.clear()
                    gc.collect(1)
                self._l1_cache[cache_key] = result_tuple

            # --- METABOLIC FINALITY ---
            self._last_biopsy_tax = (time.perf_counter_ns() - _start_ns) / 1_000_000

            # [ASCENSION 24]: THE FINALITY VOW
            return result_tuple

        except Exception as catastrophic_paradox:
            # [ASCENSION 4]: NONETYPE SARCOPHAGUS
            Logger.critical(f"L? Biopsy Fracture for {rel_id}: {catastrophic_paradox}")
            ghost = self._forge_stable_soul(rel_id, f"FRACTURED_SOUL: {str(catastrophic_paradox)}")
            return ghost, rel_id

    # =========================================================================
    # == INTERNAL FACULTIES (THE GENOMIC SENSORS)                            ==
    # =========================================================================

    def _scry_body_for_dna(self, body: str, header: ShardHeader):
        """
        =============================================================================
        == THE SECONDARY GAZE (V-Ω-HEURISTIC-TOMOGRAPHY)                           ==
        =============================================================================
        [ASCENSION 18 & 27]: The Socratic Role Diviner.
        Infers requirements, tiers, and roles from the physical code body using
        Multi-Vector Pattern Resonance.
        """
        if not body:
            return

        lines = body.splitlines()
        body_lower = body.lower()

        # --- MOVEMENT I: SGF VARIABLE INFERENCE ---
        # [ASCENSION 9]: Dangling Quantifier Suture
        # Scans for variables willed in templates but missing from Metabolism.
        for match in self.SGF_VAR_INFERENCE_PATTERN.finditer(body):
            var_name = match.group(1)
            # Ignore internal engine invariants (starting with '_')
            if var_name not in header.metabolism.env and not var_name.startswith('_'):
                if var_name not in header.requires:
                    header.requires.append(var_name)

        # --- MOVEMENT II: HARDWARE ACCELERATION SCRY ---
        # [ASCENSION 24]: If willed, we tag the shard as GPU-accelerated.
        if any(hw in body_lower for hw in self.HARDWARE_MARKERS):
            if "gpu-accelerated" not in header.vibe:
                header.vibe.append("gpu-accelerated")

        # --- MOVEMENT III: STRUCTURAL SIGNATURE SCAN ---
        # [FACULTY 15]: Determines Vibe/Tags based on file materialization.
        has_docker = False
        has_terraform = False
        has_fastapi = False
        has_react = False

        # [ASCENSION 21]: Polyglot Comment Sieve
        # We scry for file creation sigils (:: or <<)
        for line in lines:
            if file_match := re.search(r'^\s*([a-zA-Z0-9_\-\./]+)\s*(?:::|<<)', line):
                filename = Path(file_match.group(1)).name

                # Cross-reference with DNA Matrix
                for marker, tags in self.DNA_MARKERS.items():
                    if marker.lower() in filename.lower():
                        for tag in tags:
                            if tag not in header.vibe:
                                header.vibe.append(tag)

                # Set Heuristic Flags for Tier Divination
                if "Dockerfile" in filename or "docker-compose" in filename: has_docker = True
                if filename.endswith(".tf"): has_terraform = True
                if filename.endswith((".tsx", ".jsx")): has_react = True

            # [ASCENSION 28]: AST-Aware Dependency Extraction (Heuristic)
            if "from fastapi import" in line or "import fastapi" in line: has_fastapi = True

        # =========================================================================
        # == [ASCENSION 26]: HEURISTIC TIER DIVINATION                           ==
        # =========================================================================
        # If the Architect left the tier as 'mind' (default), we re-evaluate gravity.
        if header.tier == "mind":
            if has_docker or has_terraform:
                header.tier = "iron"  # Foundation Matter
            elif has_react:
                header.tier = "ocular"  # Sensory Matter
            elif has_fastapi:
                header.tier = "mind"  # Logical Matter

        # =========================================================================
        # == [ASCENSION 27]: THE SOCRATIC ROLE DIVINER                           ==
        # =========================================================================
        # Infers the surgical role for the StructureSentinel if unmanifest.
        if header.suture.role == "file":
            if "middleware" in body_lower:
                header.suture.role = "middleware-spine"
            elif "router" in body_lower or "routes" in body_lower:
                header.suture.role = "api-router"
            elif "provider" in body_lower or "repository" in body_lower:
                header.suture.role = "service-provider"

    def _scry_ocular_dna(self, dna_matter: str, clean_dna: Dict[str, Any]):
        """
        =============================================================================
        == THE RITE OF RETINAL SCRYING (V-Ω-TOTALITY-VMAX)                         ==
        =============================================================================
        [ASCENSION 29]: Surgically extracts UI control definitions from the header.
        """
        # [STRIKE]: Scry for the specific @ocular-ui YAML block
        if "@ocular-ui:" in dna_matter:
            try:
                # 1. Isolate the ocular block
                lines = dna_matter.splitlines()
                start_idx = -1
                for idx, line in enumerate(lines):
                    if "@ocular-ui:" in line:
                        start_idx = idx
                        break

                if start_idx != -1:
                    ocular_lines = []
                    # Consume indented lines
                    for line in lines[start_idx + 1:]:
                        if line.startswith('  ') or line.startswith('\t'):
                            ocular_lines.append(line)
                        elif not line.strip():
                            continue
                        else:
                            break

                    # 2. Transmute YAML to Gnosis
                    raw_ocular = yaml.safe_load("\n".join(ocular_lines))
                    if isinstance(raw_ocular, list):
                        # [THE FIX]: Support both function-string and dict-style YAML
                        processed_controls = []
                        for entry in raw_ocular:
                            if isinstance(entry, str):
                                # Handle: - toggle(key="strict", label="...")
                                match = re.match(r'(\w+)\((.*)\)', entry)
                                if match:
                                    ctrl_type, args_str = match.groups()
                                    # Atomic kwarg extraction
                                    ctrl_data = {"type": ctrl_type}
                                    for pair in re.findall(r'(\w+)="([^"]*)"', args_str):
                                        ctrl_data[pair[0]] = pair[1]
                                    processed_controls.append(ctrl_data)
                            else:
                                processed_controls.append(entry)

                        clean_dna['ocular_ui'] = processed_controls

            except Exception as e:
                Logger.debug(f"Retinal Scry deferred: {e}")

    def _forge_weighted_corpus(self, header: ShardHeader) -> str:
        """
        =============================================================================
        == THE RITE OF GRAVITY (WEIGHTED LEXICAL CORPUS)                           ==
        =============================================================================
        [ASCENSION 23]: Applies non-linear gravity to metadata for vector resonance.
        1. Identity (5x Gravity)
        2. Summary (3x Gravity)
        3. Vibes/Tags (4x Gravity)
        """
        parts = []

        # 1. Identity Resonance (Atomic slug)
        id_tokens = header.id.replace('/', ' ').replace('-', ' ').replace('_', ' ')
        parts.extend([id_tokens] * 5)

        # 2. Semantic Summary (Meaning)
        parts.extend([header.summary] * 3)

        # 3. Vibrationary Tags (Context)
        # Ensure vibes is a list
        vibe_list = header.vibe if isinstance(header.vibe, list) else []
        parts.extend(vibe_list * 4)

        # 4. Role & Capabilities (Will)
        if header.suture.role and header.suture.role != "file":
            parts.extend([header.suture.role.replace('-', ' ')] * 2)

        # [ASCENSION 32]: THE FINALITY VOW
        # Normalize for the BM25 Tensor
        return " ".join(parts).lower().strip()

    def _strip_markdown(self, text: str) -> str:
        """[ASCENSION 14]: Matter Purification. Cleans prose for the indexer."""
        # Banish headers, bold, italics, and links
        clean = re.sub(r'[*_`#]', '', text)
        clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean)
        return clean.strip()

    def _forge_stable_soul(self, rel_id: str, summary: str) -> ShardHeader:
        """
        =============================================================================
        == THE MASTER CURE: ETHEREAL SOUL GENERATOR                                ==
        =============================================================================
        [ASCENSION 1]: Forges an indestructible Ethereal Soul for internal shards.
        This annihilates the 'Shard unmanifest' heresy for system: paths.
        """
        return ShardHeader(
            id=rel_id,
            summary=summary,
            vibe=["engine", "structural", "stable", "ethereal"],
            tier="soul",
            author="God-Engine:Internal",
            merkle_root="0xETHEREAL"
        )

    def get_metabolic_stats(self) -> Dict[str, Any]:
        """Proclaims the sensory health of the decoder."""
        return {
            "last_tax_ms": round(self._last_biopsy_tax, 4),
            "cache_resonance": self._cache_hits,
            "trace_id": self._trace_id,
            "status": "RESONANT"
        }

    def __repr__(self) -> str:
        # [ASCENSION 32]: The Finality Vow
        return (
            f"<Ω_GENOMIC_DECODER "
            f"mode=ETHEREAL_GAZE_RUST_SUTURE "
            f"cache_depth={len(self._l1_cache)} "
            f"tax={self._last_biopsy_tax:.2f}ms "
            f"status=RESONANT>"
        )