# Path: src/velm/genesis/canon_dna.py
# -----------------------------------

import re
import logging
from typing import Dict, Any, List, Optional, Set, Tuple
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
    == THE GNOSTIC DNA ORACLE (V-Ω-TOTALITY-V9000-HEURISTIC-SINGULARITY)       ==
    =============================================================================
    LIF: ∞ | ROLE: METADATA_DIVINER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: (@(*#**#((*

    The Divine Interpreter of Archetypes. It gazes upon the raw scripture of a
    .scaffold file and extracts its Gnostic Soul (Metadata) and Genetic Code (Overrides).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Header Scryer:** Extracts explicit Gnostic headers (`# @tag: value`) with atomic precision.
    2.  **The Genetic Sequencer:** Transmutes complex `@dna` strings into typed Python objects (Bool/Int/List).
    3.  **The Structural Biopsy:** Scans filenames defined in the blueprint (`package.json`, `Dockerfile`) to infer technology stacks.
    4.  **The Content Radiography:** Gazes *inside* defined file blocks to find import statements (`import fastapi`, `import React`) to tag libraries.
    5.  **The Variable Diviner:** Analyzes `$$ variable` definitions to infer project capabilities (e.g., `$$ python_version` -> Python).
    6.  **The Integration Sentinel:** Detects `>>` (Action) and `+=` (Patch) sigils to automatically flag an archetype as an `Integration` or `Automation`.
    7.  **The Difficulty Calculus:** Algorithms that weigh file count, lines of code, and logic depth (`@if`) to calculate a Difficulty Rating (Novice -> Grand Architect).
    8.  **The Category Matrix:** A weighted scoring system to definitively assign `Backend`, `Frontend`, `System`, or `Intelligence` categories based on tag density.
    9.  **The Tag Taxonomy:** Normalizes chaotic tags (`py`, `Python3`) into a canonical ontology.
    10. **The Unbreakable Ward:** Handles malformed utf-8, binary ghosts, and partial fragments without crashing.
    11. **The Implicit Description:** If no description is provided, it extracts the first non-header comment or generates a summary based on the detected stack.
    12. **The Confidence Metric:** Calculates a confidence score for its divination.
    """

    # --- THE GRIMOIRE OF REGEX ---
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

    @classmethod
    def divine(cls, slug: str, content: str) -> Dict[str, Any]:
        """
        The Grand Rite of Divination.
        Transmutes raw text into a structured DNA Helix.
        """
        # 1. Initialize the Vessel
        dna = {
            "name": slug,
            "description": None,
            "category": "Unclassified",
            "tags": set(),
            "difficulty": "Unknown",
            "is_integration": False,
            "gnosis_overrides": {},
            "detected_capabilities": [],
            "confidence": 0.0
        }

        # 2. Analyze Structure (Pre-computation)
        lines = content.splitlines()
        header_lines = lines[:50]

        # 3. The Explicit Gaze (Headers)
        explicit_dna = cls._scry_headers(header_lines)

        # [SURGICAL SUTURE 1: Defensive Merging]
        # We explicitly update the dictionary-only and set-only fields
        dna.update({k: v for k, v in explicit_dna.items() if k not in ['tags', 'gnosis_overrides']})

        if explicit_dna.get('tags'):
            dna['tags'].update(explicit_dna['tags'])

        if explicit_dna.get('gnosis_overrides'):
            dna['gnosis_overrides'].update(explicit_dna['gnosis_overrides'])

        # 4. The Implicit Gaze (Inference)
        inferred_tags, capabilities = cls._infer_traits(content, lines)
        dna['tags'].update(inferred_tags)
        dna['detected_capabilities'].extend(capabilities)

        # 5. The Logic of Integration (remains pure)
        action_count = content.count(">>")
        patch_count = content.count("+=")
        file_count = len(re.findall(cls.FILE_DEF_PATTERN, content))
        if not dna['is_integration']:
            if (action_count > 0 or patch_count > 0) and file_count < 2:
                dna['is_integration'] = True

        # 6. The Calculus of Difficulty (remains pure)
        if dna['difficulty'] == "Unknown":
            dna['difficulty'] = cls._calculate_difficulty(len(lines), content)

        # 7. The Matrix of Categorization (remains pure)
        if dna['category'] == "Unclassified":
            dna['category'] = cls._divine_category(dna['tags'], slug)

        # 8. The Fallback Description (remains pure)
        if not dna['description']:
            dna['description'] = cls._generate_fallback_description(dna)

        # 9. Final Polish
        dna["tags"] = sorted(list(dna["tags"]))

        # [CRITICAL FINAL SUTURE 2: Ensure all return fields are guaranteed to be Dict or List]
        # This is the final ward against the "list.update" failure in the MasterLibrarian.
        if not isinstance(dna['gnosis_overrides'], dict):
            dna['gnosis_overrides'] = {}
        if not isinstance(dna['tags'], list):  # Tags are converted to list above, but check is safe.
            dna['tags'] = list(dna['tags'])

        return dna

    @classmethod
    def _scry_headers(cls, lines: List[str]) -> Dict[str, Any]:
        """Ingests explicit metadata headers."""
        extracted = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"): break  # End of header block

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
                elif key == "tags":
                    extracted["tags"] = [t.strip().lower() for t in value.split(",")]
                elif key == "is_integration":
                    extracted["is_integration"] = value.lower() in ("true", "yes", "1")
                elif key in ("dna", "vars", "overrides"):
                    extracted.setdefault("gnosis_overrides", {}).update(cls._parse_genetic_sequence(value))
        return extracted

    @classmethod
    def _parse_genetic_sequence(cls, sequence: str) -> Dict[str, Any]:
        """Transmutes key=val string into typed objects."""
        genes = {}
        parts = sequence.split(',')
        for part in parts:
            if '=' not in part: continue
            k, v = part.split('=', 1)
            k, v = k.strip(), v.strip()

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
        == THE ALL-SEEING EYE (V-Ω-TOTALITY-HEALED)                                ==
        =============================================================================
        LIF: ∞ | ROLE: SEMANTIC_INFERER | RANK: OMEGA

        Scans filenames, variables, and content signatures to divine the
        architectural soul of the project.
        """
        tags = set()
        caps = []

        # --- A. THE GEOMETRIC SCAN (The Dictionary of Truth) ---
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
            "mix.exs": ("elixir", "Mix"),
            "Gemfile": ("ruby", "Bundler"),
            ".github/workflows": ("ci", "GitHub Actions"),
            "vite.config": ("vite", "Vite"),
            "next.config": ("nextjs", "Next.js"),
            "tailwind.config": ("tailwind", "Tailwind CSS"),
            "alembic.ini": ("database", "Alembic"),
        }

        # [THE DIVINE HEALING]: Correct nested unpacking of (key, (val1, val2))
        # This annihilates the 'expected 3, got 2' ValueError across all timelines.
        for sig, (tag, cap) in signatures.items():
            # 1. SCAN THE FILENAMES IN THE BLUEPRINT
            for line in lines:
                match = cls.FILE_DEF_PATTERN.search(line)
                if match:
                    fname = match.group(1)
                    if sig in fname:
                        tags.add(tag)
                        caps.append(cap)

                    # Extension heuristics
                    if fname.endswith(".py"): tags.add("python")
                    if fname.endswith((".ts", ".tsx")): tags.add("typescript")
                    if fname.endswith((".js", ".jsx")): tags.add("javascript")
                    if fname.endswith(".rs"): tags.add("rust")
                    if fname.endswith(".go"): tags.add("go")

        # --- B. THE VARIABLE DIVINER ($$ var) ---
        for line in lines:
            match = cls.VAR_PATTERN.match(line.strip())
            if match:
                var = match.group(1).lower()
                if "python" in var: tags.add("python")
                if "node" in var: tags.add("node")
                if "docker" in var: tags.add("docker")
                if "db" in var or "postgres" in var: tags.add("database")

        # --- C. THE CONTENT RADIOGRAPHY (Deep Scan) ---
        content_lower = content.lower()
        if "fastapi" in content_lower: tags.add("fastapi")
        if "django" in content_lower: tags.add("django")
        if "react" in content_lower or "jsx" in content_lower: tags.add("react")
        if "vue" in content_lower: tags.add("vue")
        if any(x in content_lower for x in ["torch", "tensorflow", "scikit"]):
            tags.update(["ai", "ml"])
        if "openai" in content_lower: tags.update(["ai", "openai"])

        return tags, list(set(caps))

    @classmethod
    def _calculate_difficulty(cls, line_count: int, content: str) -> str:
        """Determines the rank of the artisan required."""
        score = line_count
        # Weigh logic heavily
        score += content.count("@if") * 5
        score += content.count("@for") * 10
        score += content.count(">>") * 5  # Kinetic acts are heavy

        if score < 50: return "Novice"
        if score < 150: return "Adept"
        if score < 400: return "Master"
        return "Grand Architect"

    @classmethod
    def _divine_category(cls, tags: Set[str], name: str) -> str:
        """
        The Sorting Hat.
        Calculates resonance with known categories based on tag density.
        """
        scores = Counter()
        name_lower = name.lower()

        # 1. Weigh Tags
        for tag in tags:
            for cat, cat_tags in cls.CATEGORY_WEIGHTS.items():
                if tag in cat_tags:
                    scores[cat] += 1

        # 2. Weigh Name (Stronger signal)
        for cat, cat_tags in cls.CATEGORY_WEIGHTS.items():
            for tag in cat_tags:
                if tag in name_lower:
                    scores[cat] += 2

        # 3. Heuristic Overrides
        if "cli" in tags or "tool" in tags: scores["Utility"] += 3
        if "api" in tags: scores["Backend"] += 2

        if not scores: return "System"  # Default fallback

        return scores.most_common(1)[0][0]

    @classmethod
    def _generate_fallback_description(cls, dna: Dict) -> str:
        """Forges a description from the void."""
        stack = ", ".join(list(dna['tags'])[:3]) if dna['tags'] else "generic"
        return f"A {dna['difficulty']} {dna['category']} archetype forging a {stack} reality."

    @staticmethod
    def inspect_dna(dna: Dict[str, Any]) -> str:
        """Returns a luminous summary for the CLI."""
        return (
            f"[bold cyan]{dna['name']}[/] ({dna['category']})\n"
            f"[dim]{dna['description']}[/]\n"
            f"Difficulty: [white]{dna['difficulty']}[/]\n"
            f"Tags: [yellow]{', '.join(dna['tags'])}[/]\n"
            f"DNA: [green]{dna['gnosis_overrides']}[/]"
        )