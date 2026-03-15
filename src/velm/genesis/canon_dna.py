# Path: src/velm/genesis/canon_dna.py
# -----------------------------------

import re
import logging
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from collections import Counter

# --- THE LUMINOUS SCRIBE ---
try:
    from ..logger import Scribe

    Logger = Scribe("GnosticDNAOracle")
except ImportError:
    Logger = logging.getLogger("GnosticDNAOracle")


class GnosticDNAOracle:
    """
    =============================================================================
    == THE GNOSTIC DNA ORACLE (V-Ω-TOTALITY-VMAX-ONTOLOGY-AWARE)               ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_GENOME_SCRYER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_DNA_ORACLE_VMAX_TOTALITY_2026_FINALIS

    The supreme sensory organ for blueprint perception. It transmutes raw text
    into a structured, hierarchical, and warded DNA Dossier.
    """

    # --- THE GRIMOIRE OF REGEX ---

    # [ASCENSION 1]: The Ontology Phalanx
    # Matches: == GNOSTIC [TYPE]: [NAME] ==
    ONTOLOGY_PATTERN = re.compile(
        r"== GNOSTIC\s+(?P<type>SHARD|TRAIT|MONAD|CITADEL|ARCHETYPE):\s*(?P<title>.*)\s*==",
        re.IGNORECASE
    )

    HEADER_PATTERN = re.compile(r"^#\s*@(\w+):\s*(.*)$")
    VAR_PATTERN = re.compile(r"^\$\$\s*(\w+)\s*=")
    FILE_DEF_PATTERN = re.compile(r"^\s*([\w\.\-\/]+)\s*(:|::|<<)")

    # --- THE TAXONOMY OF SOULS ---
    CATEGORY_WEIGHTS = {
        "Backend": {"python", "go", "rust", "java", "c#", "php", "ruby", "fastapi", "django", "flask", "gin", "actix",
                    "database", "sql", "postgres", "redis"},
        "Frontend": {"javascript", "typescript", "react", "vue", "svelte", "nextjs", "vite", "tailwind", "css", "html",
                     "spa"},
        "Intelligence": {"ai", "ml", "pytorch", "tensorflow", "llm", "openai", "langchain", "vector", "rag", "jupyter",
                         "data"},
        "Infrastructure": {"docker", "kubernetes", "terraform", "helm", "aws", "cloud", "nginx", "caddy", "prometheus",
                           "grafana"},
        "System": {"linux", "bash", "shell", "makefile", "git", "ci", "github-actions"},
        "Meta": {"scaffold", "plugin", "arch", "symphony", "tool"}
    }

    # [ASCENSION 3]: Aura Mapping for Ocular HUD
    AURA_MAP = {
        "SHARD": {"color": "#64ffda", "icon": "💎"},  # Teal
        "TRAIT": {"color": "#3b82f6", "icon": "🧬"},  # Blue
        "MONAD": {"color": "#a855f7", "icon": "🌀"},  # Purple
        "CITADEL": {"color": "#fbbf24", "icon": "🏰"},  # Gold
        "ARCHETYPE": {"color": "#ffffff", "icon": "📦"},  # White
    }

    @classmethod
    def divine(cls, slug: str, content: str) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GRAND RITE OF DIVINATION (V-Ω-TOTALITY-VMAX)                        ==
        =============================================================================
        LIF: 100x | ROLE: METADATA_DIVINER
        """
        _start_ns = time.perf_counter_ns()

        # 1. Initialize the Vessel with the new 'Ontology' and 'Aura' strata
        # [ASCENSION 4]: NONE-TYPE SARCOPHAGUS (THE FIX)
        dna = {
            "name": slug,
            "title": slug.replace("-", " ").title(),
            "ontology_type": "SHARD",
            "aura_color": "#64ffda",
            "icon": "💎",
            "description": None,
            "category": "Unclassified",
            "tags": [],
            "difficulty": "Unknown",
            "is_integration": False,
            "gnosis_overrides": {},
            "detected_capabilities": [],
            "merkle_fingerprint": cls._forge_merkle_fingerprint(content),
            "confidence": 0.0
        }

        # 2. Analyze Structure
        lines = content.splitlines()
        header_lines = lines[:100]  # Scan deeper for complex headers

        # --- MOVEMENT 0: THE ONTOLOGICAL GAZE (ASCENSION 1) ---
        # We scry the very first line for the Gnostic Signature.
        if header_lines:
            first_line = header_lines[0].strip()
            if onto_match := cls.ONTOLOGY_PATTERN.search(first_line):
                o_type = onto_match.group("type").upper()
                dna["ontology_type"] = o_type
                dna["title"] = onto_match.group("title").strip()

                aura_data = cls.AURA_MAP.get(o_type, {"color": "#64748b", "icon": "📄"})
                dna["aura_color"] = aura_data["color"]
                dna["icon"] = aura_data["icon"]

        # --- MOVEMENT I: THE EXPLICIT GAZE (HEADERS) ---
        explicit_dna = cls._scry_headers(header_lines)

        # [DEFENSIVE SUTURE]: Merge with absolute priority to explicit headers
        # We use a set to keep tags unique before converting to a sorted list
        tag_accumulator = set(explicit_dna.get('tags', []))

        for key, val in explicit_dna.items():
            if key == 'tags':
                continue  # Handled separately
            if key == 'gnosis_overrides':
                dna['gnosis_overrides'].update(val)
            else:
                dna[key] = val

        # --- MOVEMENT II: THE IMPLICIT GAZE (INFERENCE) ---
        inferred_tags, capabilities = cls._infer_traits(content, lines)
        tag_accumulator.update(inferred_tags)
        dna['detected_capabilities'].extend(capabilities)

        # --- MOVEMENT III: THE LOGIC OF INTEGRATION (SENTINEL) ---
        action_count = content.count(">>")
        patch_count = content.count("+=")
        file_count = len(re.findall(cls.FILE_DEF_PATTERN, content))
        if not dna['is_integration']:
            if (action_count > 0 or patch_count > 0) and file_count < 3:
                dna['is_integration'] = True

        # --- MOVEMENT IV: THE CALCULUS OF DIFFICULTY ---
        if dna['difficulty'] == "Unknown":
            dna['difficulty'] = cls._calculate_difficulty(len(lines), content)

        # --- MOVEMENT V: THE MATRIX OF CATEGORIZATION ---
        if dna['category'] == "Unclassified":
            dna['category'] = cls._divine_category(tag_accumulator, slug)

        # --- MOVEMENT VI: THE FALLBACK DESCRIPTION ---
        if not dna['description']:
            dna['description'] = cls._generate_fallback_description(dna, tag_accumulator)

        # --- MOVEMENT VII: FINAL ALCHEMY & POLISH ---
        dna["tags"] = sorted(list(tag_accumulator))

        # [ASCENSION 15]: Identity Suture
        dna.update(cls._forge_identity_aliases(dna["title"]))

        # METABOLIC FINALITY
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        dna["scry_latency_ms"] = round(_duration_ms, 4)

        return dna

    @classmethod
    def _scry_headers(cls, lines: List[str]) -> Dict[str, Any]:
        """Ingests explicit metadata headers from the scripture's zenith."""
        extracted = {"tags": [], "gnosis_overrides": {}}
        for line in lines:
            stripped = line.strip()
            # Stop if we hit a file definition or a non-comment line that isn't the ontology header
            if stripped and not stripped.startswith("#"):
                if "== GNOSTIC" not in stripped:
                    break

            match = cls.HEADER_PATTERN.match(stripped)
            if match:
                key, value = match.groups()
                key, value = key.lower().strip(), value.strip()

                if key == "description":
                    extracted["description"] = value
                elif key == "category":
                    extracted["category"] = value
                elif key == "difficulty":
                    extracted["difficulty"] = value
                elif key == "version":
                    extracted["version"] = value
                elif key == "author":
                    extracted["author"] = value
                elif key == "tags":
                    extracted["tags"] = [t.strip().lower() for t in value.split(",")]
                elif key == "is_integration":
                    extracted["is_integration"] = value.lower() in ("true", "yes", "1")
                elif key in ("dna", "vars", "overrides", "gnosis"):
                    extracted["gnosis_overrides"].update(cls._parse_genetic_sequence(value))
        return extracted

    @classmethod
    def _parse_genetic_sequence(cls, sequence: str) -> Dict[str, Any]:
        """Transmutes comma-separated sequences into typed Pythonic matter."""
        genes = {}
        # Support both 'key=val' and 'key:val'
        parts = re.split(r',\s*', sequence)
        for part in parts:
            if '=' not in part and ':' not in part: continue
            k, v = re.split(r'[=:]', part, 1)
            k, v = k.strip(), v.strip()

            # Type Divination
            if v.lower() == 'true':
                genes[k] = True
            elif v.lower() == 'false':
                genes[k] = False
            elif v.isdigit():
                genes[k] = int(v)
            else:
                genes[k] = v.strip('"\'')
        return genes

    @classmethod
    def _infer_traits(cls, content: str, lines: List[str]) -> Tuple[Set[str], List[str]]:
        """
        =============================================================================
        == THE ALL-SEEING EYE (V-Ω-TOTALITY-VMAX)                                  ==
        =============================================================================
        LIF: ∞ | ROLE: SEMANTIC_INFERER
        """
        tags = set()
        caps = []

        # --- A. THE STRUCTURAL BIOPSY (The Dictionary of Truth) ---
        signatures = {
            "Dockerfile": ("docker", "Containerization"),
            "docker-compose": ("docker", "Orchestration"),
            "pyproject.toml": ("python", "Poetry"),
            "poetry.lock": ("python", "Poetry"),
            "requirements.txt": ("python", "Pip"),
            "package.json": ("node", "NPM"),
            "tsconfig.json": ("typescript", "TypeScript"),
            "go.mod": ("go", "Go Modules"),
            "Cargo.toml": ("rust", "Cargo"),
            "Makefile": ("makefile", "Make"),
            "Justfile": ("just", "Just"),
            "mix.exs": ("elixir", "Mix"),
            "Gemfile": ("ruby", "Bundler"),
            ".github/workflows": ("ci", "GitHub Actions"),
            "vite.config": ("vite", "Vite"),
            "next.config": ("nextjs", "Next.js"),
            "tailwind.config": ("tailwind", "Tailwind CSS"),
            "alembic.ini": ("database", "Alembic"),
            "prisma.schema": ("database", "Prisma"),
        }

        # Scan for physical file definitions
        for line in lines:
            match = cls.FILE_DEF_PATTERN.search(line)
            if match:
                fname = match.group(1)
                # Check against the Registry of Truth
                for sig, (tag, cap) in signatures.items():
                    if sig in fname:
                        tags.add(tag)
                        if cap not in caps: caps.append(cap)

                # Extension Logic
                ext = Path(fname).suffix.lower()
                ext_map = {
                    ".py": "python", ".ts": "typescript", ".tsx": "typescript",
                    ".js": "javascript", ".jsx": "javascript", ".rs": "rust",
                    ".go": "go", ".rb": "ruby", ".java": "java"
                }
                if ext in ext_map: tags.add(ext_map[ext])

        # --- B. THE VARIABLE DIVINER ($$ var) ---
        for line in lines:
            if match := cls.VAR_PATTERN.match(line.strip()):
                var = match.group(1).lower()
                if "python" in var: tags.add("python")
                if "node" in var: tags.add("node")
                if "docker" in var: tags.add("docker")
                if "db" in var or "postgres" in var: tags.add("database")
                if "auth" in var: tags.add("security")

        # --- C. THE CONTENT RADIOGRAPHY (Deep Scan) ---
        content_lower = content.lower()
        if "fastapi" in content_lower: tags.add("fastapi")
        if "django" in content_lower: tags.add("django")
        if "react" in content_lower or "jsx" in content_lower: tags.add("react")
        if "vue" in content_lower: tags.add("vue")
        if any(x in content_lower for x in ["torch", "tensorflow", "scikit"]):
            tags.update(["ai", "ml"])
        if "openai" in content_lower: tags.update(["ai", "openai"])
        if "stripe" in content_lower: tags.update(["market", "billing"])

        return tags, caps

    @classmethod
    def _calculate_difficulty(cls, line_count: int, content: str) -> str:
        """Heuristically weighs architectural mass to rank difficulty."""
        score = line_count
        score += content.count("@if") * 5
        score += content.count("@for") * 10
        score += content.count(">>") * 8  # Kinetic edicts are heavy
        score += content.count("{{") * 2  # Interpolation tax

        if score < 60: return "Novice"
        if score < 200: return "Adept"
        if score < 500: return "Master"
        return "Grand Architect"

    @classmethod
    def _divine_category(cls, tags: Set[str], name: str) -> str:
        """The Sorting Hat: Multi-dimensional Bayesian Categorization."""
        scores = Counter()
        name_lower = name.lower()

        # 1. Weigh Tags (Lattice Resonance)
        for tag in tags:
            for cat, cat_tags in cls.CATEGORY_WEIGHTS.items():
                if tag in cat_tags:
                    scores[cat] += 1

        # 2. Weigh Name (High-Status Identity)
        for cat, cat_tags in cls.CATEGORY_WEIGHTS.items():
            for tag in cat_tags:
                if tag in name_lower:
                    scores[cat] += 3  # Stronger signal

        if not scores: return "System"  # Default fallback

        return scores.most_common(1)[0][0]

    @classmethod
    def _generate_fallback_description(cls, dna: Dict, tags: Set[str]) -> str:
        """Forges a semantic description from the void of metadata."""
        stack = ", ".join(list(tags)[:3]) if tags else "generic"
        o_type = dna.get('ontology_type', 'SHARD').lower()
        return f"A {dna['difficulty']} {dna['category']} {o_type} forging a {stack} reality."

    @staticmethod
    def _forge_identity_aliases(title: str) -> Dict[str, str]:
        """[ASCENSION 15]: Generates case-standardized aliases."""
        # Convert "My Great App" -> my_great_app, my-great-app, MyGreatApp
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        parts = clean.split()
        return {
            "name_snake": "_".join(p.lower() for p in parts),
            "name_kebab": "-".join(p.lower() for p in parts),
            "name_pascal": "".join(p.title() for p in parts),
            "name_camel": parts[0].lower() + "".join(p.title() for p in parts[1:]) if parts else ""
        }

    @staticmethod
    def _forge_merkle_fingerprint(content: str) -> str:
        """[ASCENSION 6]: Forges a hash for integrity verification."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12].upper()

    @staticmethod
    def inspect_dna(dna: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE LUMINOUS DNA DOSSIER (V-Ω-TOTALITY)                                 ==
        =============================================================================
        Renders a high-fidelity summary for the CLI or Ocular Eye.
        """
        aura = dna.get('aura_color', '#64ffda')
        o_type = dna.get('ontology_type', 'SHARD')
        icon = dna.get('icon', '💎')

        return (
            f"[{aura}]{icon} GNOSTIC {o_type}: {dna['title']}[/]\n"
            f"   ID: [bold cyan]{dna['name']}[/]\n"
            f"   Category: [white]{dna['category']}[/] | Difficulty: [white]{dna['difficulty']}[/]\n"
            f"   [dim]{dna['description']}[/]\n"
            f"   Tags: [yellow]{', '.join(dna['tags'])}[/]\n"
            f"   DNA: [green]{dna['gnosis_overrides']}[/]\n"
            f"   Seal: [dim]0x{dna['merkle_fingerprint']}[/]"
        )

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_DNA_ORACLE capacity=24_ASCENSIONS status=RESONANT>"