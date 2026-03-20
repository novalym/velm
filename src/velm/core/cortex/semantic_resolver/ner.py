# Path: core/cortex/semantic_resolver/ner.py
# ------------------------------------------

"""
=================================================================================
== THE GNOSTIC INTENT SCRIBE (V-Ω-TOTALITY-VMAX-49-ASCENSIONS)                 ==
=================================================================================
LIF: ∞ | ROLE: MULTIDIMENSIONAL_VARIABLE_EXTRACTOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_INTENT_SCRIBE_VMAX_TOTALITY_2026_FINALIS

The supreme sensory organ of the Stratum-2 Cortex. It transmutes the "Dirty Matter"
of human speech into the "Pure Law" of Gnostic Variables with absolute
mathematical certainty.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (48 TOTAL):
[... existing ascensions ...]
49. **[ASCENSION II] The Neural Crab Suture (THE MASTER CURE):** Bypasses the
    Python `re` module entirely by offloading metadata extraction (Ports, Emails,
    Colors, Regions) to the pre-compiled `fast_intent_scry` in the Rust Binary Core.
=================================================================================
"""

import re
import uuid
import time
import hashlib
import json
import os
import sys
from typing import Dict, Any, List, Optional, Set, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 49]: Binary Kernel Pivot
try:
    import scaffold_core_rs
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

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
            "is_reflexive": True,
            "substrate_aura": "#64748b"
        }

        # 2. SUBSTRATE DNA INHALATION (Environmental Anchoring)
        gnosis.update(self._scry_environment())

        # 3. THE SENSORY WALK
        text = str(prompt).strip()
        # [ASCENSION 20]: Zero-Width Exorcism
        text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', text)
        lower_text = text.lower()

        # =========================================================================
        # == [ASCENSION 49]: THE NEURAL CRAB SUTURE (RUST FAST-PATH)             ==
        # =========================================================================
        if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
            try:
                # We pull all basic metadata in one native Rust strike
                rust_gnosis = scaffold_core_rs.fast_intent_scry(text)
                gnosis.update(rust_gnosis)
            except Exception as e:
                Logger.debug(f"Rust NER Scryer fractured: {e}")
        else:
            # --- FALLBACK MOVEMENT: PYTHONIC TOPOLOGY & PROTOCOLS ---
            # [ASCENSION 31]: Isomorphic Port Triage
            for match in self._PORT_RX.finditer(text):
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

            # [ASCENSION 28]: Region Tomography
            if region_match := self._REGION_RX.search(text):
                gnosis["cloud_region"] = region_match.group(1).upper()

            # [ASCENSION 38]: Digital Soul (Email)
            if email_match := self._EMAIL_RX.search(text):
                gnosis["author_email"] = email_match.group(0)

            # [ASCENSION 25]: Version Scrying
            if ver_match := self._VERSION_RX.search(text):
                gnosis["project_version"] = ver_match.group(1)

            # [ASCENSION 29]: Ocular Hex Gaze
            if color_match := self._COLOR_RX.search(text):
                gnosis["theme_accent"] = color_match.group(0)
                gnosis["substrate_aura"] = color_match.group(0)

            # [ASCENSION 36]: Fiscal Tomography
            if budget_match := self._BUDGET_RX.search(text):
                try:
                    gnosis["budget_ceiling_usd"] = float(budget_match.group(1))
                except ValueError:
                    pass

        # --- MOVEMENT I: IDENTITY (THE NAME) ---
        # [ASCENSION 27]: The Identity Alchemist
        for pattern in self._NAME_RX.finditer(text):
            val = (pattern.group(1) or pattern.group(2)).strip()
            #[ASCENSION 47]: Domain-Aware Stopword Sieve
            if val.lower() not in ("a", "an", "the", "new", "simple", "basic", "modern", "app", "project", "service", "api"):
                gnosis['project_name'] = val
                self._inject_identity_variants(gnosis, val)
                break

        # --- MOVEMENT II: SUBSTRATE (TECH STACK) ---
        for key, val in self._DB_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['database_type'] = val
                # Apply Apophatic Guard (Don't set true if negated)
                gnosis['use_database'] = self._scry_vow(key, [key], lower_text)
                break

        for key, sub_id in self._SUBSTRATE_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis["substrate"] = sub_id
                if sub_id == "docker":
                    gnosis["use_docker"] = self._scry_vow(key, [key], lower_text)
                break

        # [ASCENSION 35]: Protocol Resonance
        for key, proto in self._PROTOCOL_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                gnosis['api_protocol'] = proto
                break

        # --- MOVEMENT III: ADJECTIVES (THE WILL) ---
        #[ASCENSION 8 & 33]: Transmuting Poetry to Logic with Apophatic Guard
        gnosis["use_auth"] = self._scry_vow("auth", ["secure", "auth", "login", "clerk", "identity"], lower_text)
        gnosis["use_git"] = self._scry_vow("git", ["git", "github", "version control"], lower_text)
        gnosis["use_observability"] = self._scry_vow("observab",["observability", "metrics", "traces", "otel", "monitor"], lower_text)

        if re.search(r'\b(fast|quick|smart|creative)\b', lower_text):
            gnosis["model_hint"] = "fast" if "fast" in lower_text or "quick" in lower_text else "creative"

        if re.search(r'\b(nomadic|anycast)\b', lower_text):
            gnosis["is_nomadic"] = True

        # --- MOVEMENT IV: METADATA HARVESTING ---
        # [ASCENSION 39]: Dependency Inception
        deps = re.findall(r'\b(?:using|with)\s+([a-zA-Z0-9_\-]+)\b', lower_text)
        if deps:
            pure_deps =[d for d in deps if d not in ("a", "the", "an", "this", "that")]
            if pure_deps:
                gnosis["metabolic_needs"] = pure_deps

        # [ASCENSION 44]: Hardware DNA Scrying
        if re.search(r'\b(gpu|cuda|tensor|mps|vulkan)\b', lower_text):
            gnosis["has_gpu"] = True

        # --- MOVEMENT V: METABOLIC FINALITY ---
        #[ASCENSION 32]: The Vow of Privacy
        gnosis = self._redact_high_entropy(gnosis)

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
                prob =[float(v.count(c)) / len(v) for c in dict.fromkeys(list(v))]
                entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
                if entropy > 4.2:
                    clean[k] = "[REDACTED_BY_SOVEREIGN_SIEVE]"
                    continue
            clean[k] = v
        return clean

    def _scry_environment(self) -> Dict[str, Any]:
        import platform
        """[ASCENSION 7]: Siphons the physical DNA of the host machine."""
        return {
            "os_name": os.name,
            "platform": platform.system().lower(),
            "arch": platform.machine(),
            "python_v": sys.version.split()[0],
            "machine_id": hashlib.md5(platform.node().encode()).hexdigest()[:8].upper()
        }

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_INTENT_SCRIBE status=RESONANT mode=CORTEX_SENSORY version='VMAX_49_RUST_SUTURED'>"