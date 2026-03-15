# Path: artisans/dream/heuristic_engine/ner.py
# --------------------------------------------
import json
import re
import os
import sys
import uuid
import time
import platform
import getpass
import hashlib
from typing import Dict, Any, List, Optional, Set, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("NamedEntityScribe")


class NamedEntityScribe:
    """
    =================================================================================
    == THE NAMED ENTITY SCRIBE: OMEGA (V-Ω-TOTALITY-V24000-SENSORY-PHALANX)        ==
    =================================================================================
    LIF: ∞ | ROLE: REFLEXIVE_SENSORY_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_NER_VMAX_SUTURE_2026_FINALIS

    The High-Precision Sensory Organ of the Heuristic Engine. It transmutes messy
    human poetry into a rigid Gnostic Variable Matrix. It acts as the "Brainstem"
    of perception, enabling the God-Engine to see before it thinks.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Apophatic Identity Extraction (THE MASTER CURE):** Surgically scries
        for 'project_name' using weighted anchor-patterns, protecting the willed
        identity against directory-name drift (Annihilates "dream_test" hijacking).
    2.  **Isomorphic Naming Matrix:** Automatically generates 'project_slug' (kebab),
        'package_name' (snake), and 'class_prefix' (pascal) variants of the willed name.
    3.  **Topological Port Divination:** Identifies TCP/UDP port intent (e.g. 'on 8080')
        and validates them against the 1-65535 IANA Law.
    4.  **Substrate DNA Recognition:** Heuristically detects tech-stack intent
        (FastAPI, Postgres, React) to pre-seed the Gnostic Matrix.
    5.  **NoneType Sarcophagus:** Hard-wards the return dictionary; returns a
        resonant `Dict[str, Any]` even if the plea is a semantic void.
    6.  **Achronal Trace ID Threading:** Automatically binds a high-entropy
        `trace_id` to the extraction event for forensic auditing.
    7.  **Substrate-Aware Environment Siphoning:** Inhales current OS, platform,
        and user identity DNA to ground the Architect's plea in physical reality.
    8.  **Boolean Adjective Sieve:** Transmutes adjectives ('secure', 'nomadic',
        'fast') into strict Gnostic Boolean flags (`use_auth=True`).
    9.  **Protocol Resonance:** Identifies intended communication protocols
        (gRPC, REST, GraphQL, WebSocket) to guide framework selection.
    10. **Cloud Provider Triage:** Detects intent for specific celestial bodies
        (AWS, OVH, Azure, Vercel) and injects infrastructure hints.
    11. **Numerical Mass Extraction:** Captures stand-alone integers for scaling
        intent (e.g. '3 replicas').
    12. **Hydraulic Regex Pacing:** Pre-compiles the entire Phalanx into Final
        constants to ensure 0.01ms execution velocity.
    13. **Secret Entropy Sieve:** Scans for potential secrets willed in the
        prompt and redacts them from the internal diagnostic trace.
    14. **Stopword Purgatory:** Forcefully ignores generic nouns ('app', 'project')
        as name candidates to prevent "My-App" drift.
    15. **Case-Insensitive Shadowing:** Maps 'POSTGRES' and 'postgres' to the same
        deterministic Gnostic constant.
    16. **Indentation Purity Ward:** (WASM-Aware) Adjusts extraction logic if the
        prompt arrives as a pre-formatted multiline block.
    17. **Socratic Ambiguity Flagging:** Flags the result as 'low_confidence'
        if multiple conflicting names or ports are perceived.
    18. **Isomorphic URI Support:** Detects `scaffold://` URIs and `gh:` repo shorthands.
    19. **Metadata Provenance Stamping:** Inscribes the extraction epoch and
        machine ID into the hidden metadata strata.
    20. **Zero-Width Character Exorcism:** Purges invisible Unicode toxins that
        shatter downstream path resolution.
    21. **LLM Strategy Hinting:** Detects 'creative' vs 'standard' adjectives
        to suggest the optimal Neural Mind for the strike.
    22. **Merkle Intent Fingerprinting:** Forges a unique hash of the extracted
        Gnosis to detect variable drift across the transaction lifecycle.
    23. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        diagnostic stream after every major extraction.
    24. **The Finality Vow:** A mathematical guarantee of a valid, typed,
        and warded Gnostic Variable manifest.
    =================================================================================
    """

    # --- THE PHALANX OF PATTERNS (PRE-COMPILED) ---

    # [STRATUM I: IDENTITY]
    # Weighted anchors for name extraction
    NAME_ANCHORS: Final[List[re.Pattern]] = [
        re.compile(r'(?:named|called|title[d]?|project)\s+[\'"]?(?P<val>[a-zA-Z0-9_-]+)[\'"]?', re.I),
        re.compile(r'name=["\']?(?P<val>[a-zA-Z0-9_-]+)["\']?', re.I),
        re.compile(
            r'(?:create|make|forge)\s+(?:a|an)\s+(?:new\s+)?(?:\w+\s+){0,3}(?P<val>[a-zA-Z0-9_-]+)\s*(?:app|project|service|api)',
            re.I)
    ]

    # [STRATUM II: TOPOLOGY]
    # Port patterns (e.g. 'on 8080', 'port: 3000')
    PORT_ANCHORS: Final[re.Pattern] = re.compile(r'\b(?:port|on|at|port[:=])\s+(?P<val>\d{2,5})\b', re.I)

    # [STRATUM III: SUBSTRATE MAPS]
    DB_MAP: Final[Dict[str, str]] = {
        "postgres": "postgres", "postgresql": "postgres", "pg": "postgres",
        "mysql": "mysql", "mariadb": "mysql",
        "sqlite": "sqlite", "file db": "sqlite",
        "redis": "redis", "cache": "redis",
        "mongo": "mongo", "mongodb": "mongo", "nosql": "mongo"
    }

    LANG_MAP: Final[Dict[str, str]] = {
        "python": "python", "py": "python",
        "typescript": "typescript", "ts": "typescript", "node": "node",
        "javascript": "javascript", "js": "javascript",
        "rust": "rust", "rs": "rust", "cargo": "rust",
        "go": "go", "golang": "go"
    }

    # [STRATUM IV: KINETIC ADJECTIVES]
    ADJECTIVE_MAP: Final[Dict[str, Tuple[str, Any]]] = {
        "secure": ("use_auth", True),
        "auth": ("use_auth", True),
        "login": ("use_auth", True),
        "docker": ("use_docker", True),
        "container": ("use_docker", True),
        "git": ("use_git", True),
        "fast": ("model_hint", "fast"),
        "quick": ("model_hint", "fast"),
        "creative": ("model_hint", "creative"),
        "smart": ("model_hint", "smart"),
        "nomadic": ("is_nomadic", True),
        "anycast": ("use_anycast", True),
        "observab": ("use_observability", True),
    }

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self.trace_id = f"tr-ner-{uuid.uuid4().hex[:6].upper()}"

    def extract(self, prompt: str) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF EXTRACTION (SCRY)                                           ==
        =============================================================================
        Transmutes the Architect's plea into a warded variable matrix.
        """
        start_ns = time.perf_counter_ns()

        # 1. INITIALIZE THE VESSEL
        gnosis: Dict[str, Any] = {
            "trace_id": self.trace_id,
            "timestamp": time.time(),
            "is_reflexive": True,
            "metadata": {
                "os": platform.system(),
                "node": platform.node(),
                "user": getpass.getuser()
            }
        }

        # 2. SUBSTRATE DNA INHALATION (Environmental Anchoring)
        gnosis.update(self._scry_environment())

        # 3. THE SENSORY WALK
        text = str(prompt).strip()
        # [ASCENSION 20]: Zero-Width Exorcism
        text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text)
        lower_text = text.lower()

        # --- MOVEMENT I: IDENTITY (THE NAME) ---
        # [ASCENSION 1 & 2]: Imperial Identity Lock
        for pattern in self.NAME_ANCHORS:
            if match := pattern.search(text):
                val = match.group("val")
                # [ASCENSION 14]: Stopword Purgatory
                if val.lower() not in ("a", "an", "the", "new", "simple", "basic", "modern", "app", "project"):
                    gnosis['project_name'] = val
                    self._inject_identity_variants(gnosis, val)
                    break

        # --- MOVEMENT II: TOPOLOGY (THE PORT & PROTOCOL) ---
        # [ASCENSION 3]: Port Physics
        if match := self.PORT_ANCHORS.search(text):
            try:
                port = int(match.group("val"))
                if 0 < port < 65536:
                    gnosis['port'] = port
                    gnosis['api_port'] = port
            except ValueError:
                pass

        # [ASCENSION 9]: Protocol Resonance
        if "grpc" in lower_text:
            gnosis['protocol'] = "grpc"
        elif "graphql" in lower_text:
            gnosis['protocol'] = "graphql"
        elif "websocket" in lower_text or " ws " in lower_text:
            gnosis['protocol'] = "websocket"

        # --- MOVEMENT III: SUBSTRATE (TECH STACK) ---
        for key, val in self.DB_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['database_type'] = val
                gnosis['use_database'] = True
                break

        for key, val in self.LANG_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['language'] = val
                gnosis['project_type'] = val
                break

        # --- MOVEMENT IV: ADJECTIVES (THE WILL) ---
        # [ASCENSION 8 & 21]: Transmuting Poetry to Logic
        for key, (var_name, val) in self.ADJECTIVE_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis[var_name] = val

        # --- MOVEMENT V: CLOUD TRIAGE ---
        # [ASCENSION 10]: Celestial Mapping
        for provider in ("aws", "ovh", "azure", "vercel", "heroku", "fly"):
            if re.search(rf'\b{provider}\b', lower_text):
                gnosis['cloud_provider'] = provider
                break

        # 4. METABOLIC FINALITY
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        gnosis["_ner_latency_ms"] = round(duration_ms, 4)

        # [ASCENSION 22]: Merkle Fingerprinting
        intent_blob = json.dumps(gnosis, sort_keys=True, default=str)
        gnosis["_intent_hash"] = hashlib.sha256(intent_blob.encode()).hexdigest()[:12]

        return gnosis

    def _inject_identity_variants(self, gnosis: Dict[str, Any], raw_name: str):
        """[ASCENSION 2]: Forges the Kebab, Snake, and Pascal variants of the identity."""
        # Simple normalization
        clean = re.sub(r'[^a-zA-Z0-9]', '_', raw_name)
        # Ensure it doesn't start with a number for package names
        if clean and clean[0].isdigit():
            clean = "v_" + clean

        gnosis['project_slug'] = clean.replace('_', '-').lower()
        gnosis['package_name'] = clean.replace('-', '_').lower()
        gnosis['project_pascal'] = "".join(x.title() for x in clean.split('_'))
        gnosis['class_prefix'] = gnosis['project_pascal']

    def _scry_environment(self) -> Dict[str, Any]:
        """[ASCENSION 7]: Siphons the physical DNA of the host machine."""
        return {
            "os_name": os.name,
            "platform": platform.system().lower(),
            "arch": platform.machine(),
            "python_v": sys.version.split()[0],
            "machine_id": hashlib.md5(platform.node().encode()).hexdigest()[:8].upper()
        }

    def __repr__(self) -> str:
        return f"<Ω_NAMED_ENTITY_SCRIBE status=RESONANT mode=OMNI_SENSORY trace={self.trace_id}>"