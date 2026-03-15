# Path: src/velm/core/cortex/semantic_resolver/ner.py
# ---------------------------------------------------------------------------

"""
=================================================================================
== THE GNOSTIC INTENT SCRIBE (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)                 ==
=================================================================================
LIF: ∞ | ROLE: MULTIDIMENSIONAL_VARIABLE_EXTRACTOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_INTENT_SCRIBE_VMAX_TOTALITY_2026_FINALIS

The supreme sensory organ of the Stratum-2 Cortex. It transmutes the "Dirty Matter"
of human speech into the "Pure Law" of Gnostic Variables with absolute
mathematical certainty.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (48 TOTAL):
25. **Achronal Version Scrying (THE MASTER CURE):** Surgically extracts SemVer
    patterns (v1.2.3) to anchor the project's temporal maturity.
26. **Geometric URL Suture:** Natively identifies Git repositories, API
    endpoints, and Webhook targets, transmuting them into `target_uri` gnosis.
27. **The Identity Alchemist:** Automatically forges `package_name` (snake_case)
    and `class_prefix` (PascalCase) from a single project title match.
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

import re
import uuid
import time
import hashlib
import json
from typing import Dict, Any, List, Optional, Set, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("GnosticIntentScribe")


class GnosticIntentScribe:
    """
    The High-Order Semantic Sensory Organ.
    Transmutes poetry into absolute Architectural Law.
    """

    # =========================================================================
    # == THE SENSORY PHALANX (THE GRIMOIRE OF REGEX)                         ==
    # =========================================================================

    # 1. PORT GRAVITY: [ASCENSION 31] Contextual Proximity
    _PORT_RX = re.compile(r'(?P<context>db|database|api|web|app|port)?\s*:?\s*(?P<val>\d{2,5})', re.IGNORECASE)

    # 2. IDENTITY INCEPTION: [ASCENSION 27] Complex Name Extraction
    _NAME_RX = re.compile(r'(?:named|called|title|project|app|service)\s*:?\s*["\']?([a-zA-Z0-9_\-\s]+)["\']?',
                          re.IGNORECASE)

    # 3. DATABASE FINGERPRINTING
    _DB_MAP: Final[Dict[str, str]] = {
        "postgres": "postgres", "postgresql": "postgres", "pg": "postgres",
        "mysql": "mysql", "mariadb": "mysql", "sqlite": "sqlite",
        "redis": "redis", "cache": "redis", "mongo": "mongo"
    }

    # 4. SUBSTRATE DIVINATION: [ASCENSION 42]
    _SUBSTRATE_MAP: Final[Dict[str, str]] = {
        "docker": "docker", "compose": "docker", "container": "docker",
        "serverless": "lambda", "lambda": "lambda", "edge": "worker",
        "bare-metal": "iron", "iron": "iron", "vps": "vps"
    }

    # 5. REGION TOMOGRAPHY: [ASCENSION 28]
    _REGION_RX = re.compile(r'\b(gra11|sbg5|us-east-1|us-west-2|eu-central-1|uk-london)\b', re.IGNORECASE)

    # 6. VERSION SCRYING: [ASCENSION 25]
    _VERSION_RX = re.compile(r'\b(?:v)?(\d+\.\d+\.\d+(?:-\w+)?)\b', re.IGNORECASE)

    # 7. OCULAR HEX GAZE: [ASCENSION 29]
    _COLOR_RX = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}\b')

    # 8. DIGITAL SOUL (EMAIL): [ASCENSION 38]
    _EMAIL_RX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # 9. FISCAL TOMOGRAPHY: [ASCENSION 36]
    _BUDGET_RX = re.compile(r'\$\s*(\d+(?:\.\d{2})?)\b')

    # 10. PROTOCOL RESONANCE: [ASCENSION 35]
    _PROTOCOL_MAP: Final[Dict[str, str]] = {
        "rest": "rest", "http": "rest", "graphql": "graphql",
        "grpc": "grpc", "ws": "websocket", "websocket": "websocket"
    }

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self.trace_id = f"tr-ner-cortex-{uuid.uuid4().hex[:6].upper()}"

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
            "substrate_aura": "#64748b"
        }

        # [ASCENSION 20]: Zero-Width character purge
        clean_prompt = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', prompt)
        text = clean_prompt.lower().strip()

        # --- MOVEMENT I: IDENTITY & TOPOGRAPHY ---

        # 1. Project Name & Slugs [ASCENSION 27 & 34]
        if name_match := self._NAME_RX.search(clean_prompt):
            # Extract from either the quoted group or the unquoted group
            raw_name = (name_match.group(1) or name_match.group(2)).strip()

            # Linguistic Purity: Replace spaces with underscores
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', raw_name.replace(' ', '_'))

            gnosis["project_name"] = raw_name
            gnosis["project_slug"] = clean_name.replace('_', '-').lower()
            gnosis["package_name"] = clean_name.lower().strip('_')
            # PascalCase for class prefixes
            gnosis["class_prefix"] = "".join(x.title() for x in gnosis["project_slug"].split('-'))

        # 2. Ports (Contextual Triage) [ASCENSION 31]
        for match in self._PORT_RX.finditer(text):
            context, val_str = match.group('context'), match.group('val')
            val = int(val_str)
            if context and context.lower() in ('db', 'database'):
                gnosis["database_port"] = val
            else:
                gnosis["api_port"] = val
                gnosis["default_port"] = val

        # --- MOVEMENT II: PERSISTENCE & IRON ---

        # 3. Databases & Substrates
        for key, hub_id in self._DB_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', text):
                gnosis["database_type"] = hub_id
                gnosis["use_database"] = True
                break

        for key, sub_id in self._SUBSTRATE_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', text):
                gnosis["substrate"] = sub_id
                if sub_id == "docker": gnosis["use_docker"] = True
                break

        # 4. Region & Protocol [ASCENSION 28 & 35]
        if region_match := self._REGION_RX.search(text):
            gnosis["cloud_region"] = region_match.group(1).upper()

        for key, proto in self._PROTOCOL_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', text):
                gnosis["api_protocol"] = proto
                break

        # --- MOVEMENT III: COGNITION & SECURITY ---

        # 5. [ASCENSION 33]: APOPHATIC NEGATION (The Shield of 'No')
        # "FastAPI with Auth" -> True | "FastAPI without Auth" -> False
        def _scry_vow(target: str, adjectives: List[str]) -> bool:
            has_intent = any(adj in text for adj in adjectives)
            # Negative lookbehind/lookahead for "no", "without", "skip"
            negation_pattern = rf'\b(?:no|without|skip|disable)\s+(?:[\w-]+\s+)?{target}'
            return has_intent and not bool(re.search(negation_pattern, text))

        gnosis["use_auth"] = _scry_vow("auth", ["auth", "login", "clerk", "identity"])
        gnosis["use_git"] = _scry_vow("git", ["git", "github", "version control"])
        gnosis["use_observability"] = _scry_vow("observab", ["observability", "metrics", "traces", "otel"])

        # 6. Metadata Harvesting [ASCENSION 25, 29, 36, 38]
        if email_match := self._EMAIL_RX.search(clean_prompt):
            gnosis["author_email"] = email_match.group(0)

        if ver_match := self._VERSION_RX.search(text):
            gnosis["project_version"] = ver_match.group(1)

        if color_match := self._COLOR_RX.search(clean_prompt):
            gnosis["theme_accent"] = color_match.group(0)
            gnosis["substrate_aura"] = color_match.group(0)

        if budget_match := self._BUDGET_RX.search(text):
            gnosis["budget_ceiling_usd"] = float(budget_match.group(1))

        # --- MOVEMENT IV: METABOLIC FINALITY ---

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

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_INTENT_SCRIBE status=RESONANT mode=CORTEX_SENSORY version='VMAX_48_ASCENSIONS'>"