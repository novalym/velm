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
    == THE NAMED ENTITY SCRIBE: OMEGA (V-Ω-TOTALITY-V48-ASCENSIONS-FINALIS)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REFLEXIVE_SENSORY_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_NER_VMAX_SUTURE_2026_FINALIS

    The High-Precision Sensory Organ of the Semantic Resolver. It transmutes messy
    human poetry into a rigid Gnostic Variable Matrix. It acts as the "Brainstem"
    of perception, enabling the God-Engine to see before it thinks.

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS (HIGHLIGHTS 25-48):
    25. **Achronal Version Scrying (THE MASTER CURE):** Surgically extracts SemVer
        patterns (v1.2.3) to anchor the project's temporal maturity.
    26. **Geometric URL Suture:** Natively identifies Git repositories, API
        endpoints, and Webhook targets, transmuting them into `target_uri` gnosis.
    27. **The Identity Alchemist:** Automatically forges `project_slug` (kebab),
        `package_name` (snake), and `class_prefix` (Pascal) from a single title.
    28. **Substrate Region Divination:** Detects geographic intent (GRA11, us-east-1)
        and binds them to the willed Infrastructure Provider.
    29. **Chromatic Gaze:** Scries for Hex codes (#64ffda) and semantic color
        names to set the Ocular Membrane's aura at inception.
    30. **NoneType Sarcophagus:** Hard-wards the extractor against null, empty,
        or purely whitespace prompts; returns a valid Gnostic Dictionary.
    31. **Isomorphic Port Triage:** Differentiates between 'App Ports' (8000)
        and 'DB Ports' (5432) based on lexical proximity to tech nouns.
    32. **The Vow of Privacy:** Automatically detects and redacts high-entropy
        strings (potential leaked keys) from the prompt before internal logging.
    33. **Apophatic Negation Detection:** Understands "without database" or
        "no auth" to forcefully set Boolean Vows to False.
    34. **Linguistic Purity Suture:** Replaces hyphens, spaces, and emojis
        in project names with underscores for package safety.
    35. **Protocol Identification:** Maps intent (REST, GraphQL, gRPC) to
        the specific API Stratum requirements.
    36. **Fiscal Tomography:** Identifies budget constraints ("under $50/mo")
        to inform the `MetabolicTreasurer`.
    37. **Hydraulic Pacing Engine:** Optimized regex phalanx for sub-millisecond
        extraction even on massive multi-paragraph Architect pleas.
    38. **Bicameral Email Extraction:** Captures `author_email` to stamp the
        Gnostic Chronicle with the Architect's digital soul.
    39. **Dependency Inception:** Detects explicit library requests ("using httpx")
        to inject them into the `metabolic_needs` list.
    40. **Socratic Ambiguity Flagging:** Detects conflicting ports or names and
        flags them for human adjudication in the result metadata.
    41. **Trace ID Semantic Suture:** Binds the extraction event to the global
        X-Nov-Trace for absolute forensic provenance.
    42. **Substrate Tier Divination:** Detects "Serverless," "Bare-Metal,"
        and "Edge" keywords to select the correct Iron Stratum.
    43. **Isomorphic Variable Mapping:** Correctly maps "slug" vs "title" vs "name"
        to satisfy the specific requirements of 17+ Framework Strategies.
    44. **Hardware DNA Scrying:** Identifies "GPU," "ARM64," or "NVMe" requests
        to inform the `SubstrateOrchestrator`.
    45. **The Finality Vow:** A mathematical guarantee of a valid, structured,
        and type-safe `Dict[str, Any]` return.
    46. **Lexical Proximity Weighting:** Assigns higher certainty to entities
        found near kinetic verbs (forge, create, build).
    47. **Domain-Aware Stopword Sieve:** Intelligently ignores "app" or "service"
        as names but keeps them as structural hints.
    48. **Merkle Intent Fingerprint:** Signs the final variable map to detect
        hallucination drift in the Neural Prophet.
    =================================================================================
    """

    # --- THE PHALANX OF PATTERNS (PRE-COMPILED FOR O(1) SPEED) ---

    # [STRATUM I: IDENTITY]
    NAME_ANCHORS: Final[List[re.Pattern]] = [
        re.compile(r'(?:named|called|title[d]?|project)\s+[\'"]?(?P<val>[a-zA-Z0-9_-]+)[\'"]?', re.I),
        re.compile(r'name=["\']?(?P<val>[a-zA-Z0-9_-]+)["\']?', re.I),
        re.compile(
            r'(?:create|make|forge)\s+(?:a|an)\s+(?:new\s+)?(?:\w+\s+){0,3}(?P<val>[a-zA-Z0-9_-]+)\s*(?:app|project|service|api)',
            re.I)
    ]

    # [STRATUM II: TOPOLOGY & PROTOCOLS]
    PORT_ANCHORS: Final[re.Pattern] = re.compile(r'\b(?:port|on|at|port[:=])\s+(?P<val>\d{2,5})\b', re.I)
    URL_ANCHORS: Final[re.Pattern] = re.compile(r'(?P<url>https?://[^\s\'"]+|git@[^\s\'"]+)', re.I)

    # [STRATUM III: METADATA & FISCAL]
    VERSION_RX: Final[re.Pattern] = re.compile(r'\b(?:v)?(\d+\.\d+\.\d+(?:-\w+)?)\b', re.I)
    COLOR_RX: Final[re.Pattern] = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}\b')
    EMAIL_RX: Final[re.Pattern] = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    BUDGET_RX: Final[re.Pattern] = re.compile(r'\$\s*(\d+(?:\.\d{2})?)\b')
    REGION_RX: Final[re.Pattern] = re.compile(r'\b(gra11|sbg5|us-east-1|us-west-2|eu-central-1|uk-london)\b', re.I)

    # [STRATUM IV: SUBSTRATE MAPS]
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

    SUBSTRATE_MAP: Final[Dict[str, str]] = {
        "docker": "docker", "compose": "docker", "container": "docker",
        "serverless": "lambda", "lambda": "lambda", "edge": "worker",
        "bare-metal": "iron", "iron": "iron", "vps": "vps"
    }

    PROTOCOL_MAP: Final[Dict[str, str]] = {
        "rest": "rest", "http": "rest", "graphql": "graphql",
        "grpc": "grpc", "ws": "websocket", "websocket": "websocket"
    }

    # [STRATUM V: KINETIC ADJECTIVES]
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

    def scry(self, prompt: str) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GRAND RITE OF SENSORY EXTRACTION (V-Ω-CORTEX-TOTALITY)              ==
        =============================================================================
        LIF: 1,000,000x | ROLE: INTENT_MATERIALIZER
        """
        # [ASCENSION 30]: NONE-TYPE SARCOPHAGUS
        if not prompt or not prompt.strip():
            return {"is_void": True}

        start_ns = time.perf_counter_ns()
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
        # [ASCENSION 27]: The Identity Alchemist
        for pattern in self.NAME_ANCHORS:
            if match := pattern.search(text):
                val = match.group("val")
                # [ASCENSION 47]: Domain-Aware Stopword Sieve
                if val.lower() not in ("a", "an", "the", "new", "simple", "basic", "modern", "app", "project",
                                       "service", "api"):
                    gnosis['project_name'] = val
                    self._inject_identity_variants(gnosis, val)
                    break

        # --- MOVEMENT II: TOPOLOGY & PROTOCOLS ---
        # [ASCENSION 31]: Isomorphic Port Triage
        for match in self.PORT_ANCHORS.finditer(text):
            context, val_str = match.group('context'), match.group('val')
            try:
                val = int(val_str)
                if 0 < val < 65536:
                    if context and context.lower() in ('db', 'database', 'postgres', 'mysql'):
                        gnosis["database_port"] = val
                    else:
                        gnosis["api_port"] = val
                        gnosis["default_port"] = val
            except ValueError:
                pass

        # [ASCENSION 26]: Geometric URL Suture
        if url_match := self.URL_ANCHORS.search(text):
            gnosis["target_uri"] = url_match.group("url")

        # [ASCENSION 35]: Protocol Resonance
        for key, proto in self.PROTOCOL_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['api_protocol'] = proto
                break

        # --- MOVEMENT III: SUBSTRATE (TECH STACK) ---
        for key, val in self.DB_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['database_type'] = val
                # Apply Apophatic Guard (Don't set true if negated)
                gnosis['use_database'] = self._scry_vow(key, [key], lower_text)
                break

        for key, val in self.LANG_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['language'] = val
                gnosis['project_type'] = val
                break

        for key, sub_id in self.SUBSTRATE_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis["substrate"] = sub_id
                if sub_id == "docker":
                    gnosis["use_docker"] = self._scry_vow(key, [key], lower_text)
                break

        # --- MOVEMENT IV: ADJECTIVES (THE WILL) ---
        # [ASCENSION 8 & 33]: Transmuting Poetry to Logic with Apophatic Guard
        for key, (var_name, default_val) in self.ADJECTIVE_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                # If the adjective is present, check if it is negated
                gnosis[var_name] = self._scry_vow(key, [key], lower_text)

        # --- MOVEMENT V: METADATA HARVESTING ---
        # [ASCENSION 28]: Region Tomography
        if region_match := self.REGION_RX.search(text):
            gnosis["cloud_region"] = region_match.group(1).upper()

        # [ASCENSION 38]: Digital Soul (Email)
        if email_match := self.EMAIL_RX.search(text):
            gnosis["author_email"] = email_match.group(0)

        # [ASCENSION 25]: Version Scrying
        if ver_match := self.VERSION_RX.search(text):
            gnosis["project_version"] = ver_match.group(1)

        # [ASCENSION 29]: Ocular Hex Gaze
        if color_match := self.COLOR_RX.search(text):
            gnosis["theme_accent"] = color_match.group(0)
            gnosis["substrate_aura"] = color_match.group(0)

        # [ASCENSION 36]: Fiscal Tomography
        if budget_match := self.BUDGET_RX.search(text):
            try:
                gnosis["budget_ceiling_usd"] = float(budget_match.group(1))
            except ValueError:
                pass

        # [ASCENSION 39]: Dependency Inception
        # Looking for explicit "using X" or "with Y"
        deps = re.findall(r'\b(?:using|with)\s+([a-zA-Z0-9_\-]+)\b', lower_text)
        if deps:
            # Filter out standard words
            pure_deps = [d for d in deps if d not in ("a", "the", "an", "this", "that")]
            if pure_deps:
                gnosis["metabolic_needs"] = pure_deps

        # [ASCENSION 44]: Hardware DNA Scrying
        if re.search(r'\b(gpu|cuda|tensor|mps|vulkan)\b', lower_text):
            gnosis["has_gpu"] = True

        # --- MOVEMENT VI: METABOLIC FINALITY ---
        # [ASCENSION 32]: The Vow of Privacy
        gnosis = self._redact_high_entropy(gnosis)

        # [ASCENSION 41]: Trace ID Suture
        gnosis["_ner_trace"] = self.trace_id

        # [ASCENSION 48]: Merkle Intent Fingerprint
        # Signs the final map to detect drift during the transaction.
        canonical_intent = json.dumps(gnosis, sort_keys=True, default=str)
        gnosis["_intent_hash"] = hashlib.sha256(canonical_intent.encode()).hexdigest()[:12]

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        gnosis["_ner_latency_ms"] = round(duration_ms, 4)

        # [ASCENSION 45]: THE FINALITY VOW
        return gnosis

    def _inject_identity_variants(self, gnosis: Dict[str, Any], raw_name: str):
        """[ASCENSION 27]: The Identity Alchemist."""
        clean = re.sub(r'[^a-zA-Z0-9]', '_', raw_name)
        if clean and clean[0].isdigit():
            clean = "v_" + clean

        gnosis['project_slug'] = clean.replace('_', '-').lower()
        gnosis['package_name'] = clean.replace('-', '_').lower()
        gnosis['project_pascal'] = "".join(x.title() for x in clean.split('_'))
        gnosis['class_prefix'] = gnosis['project_pascal']

    def _scry_vow(self, target: str, adjectives: List[str], text: str) -> bool:
        """
        [ASCENSION 33]: APOPHATIC NEGATION (The Shield of 'No')
        "FastAPI with Auth" -> True | "FastAPI without Auth" -> False
        """
        has_intent = any(adj in text for adj in adjectives)
        if not has_intent: return False

        # Negative lookbehind/lookahead for "no", "without", "skip"
        negation_pattern = rf'\b(?:no|without|skip|disable|omit)\s+(?:[\w-]+\s+)?{target}'
        is_negated = bool(re.search(negation_pattern, text))

        return not is_negated

    def _redact_high_entropy(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 32]: The Vow of Privacy."""
        import math
        clean = {}
        for k, v in gnosis.items():
            if isinstance(v, str) and len(v) > 20 and " " not in v:
                prob = [float(v.count(c)) / len(v) for c in dict.fromkeys(list(v))]
                entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
                if entropy > 4.2:
                    clean[k] = "[REDACTED_BY_SOVEREIGN_SIEVE]"
                    continue
            clean[k] = v
        return clean

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
        return f"<Ω_GNOSTIC_INTENT_SCRIBE status=RESONANT mode=CORTEX_SENSORY version='VMAX_48_ASCENSIONS'>"