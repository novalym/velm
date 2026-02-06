# Path: src/velm/genesis/genesis_profiles.py
# ------------------------------------------
# =========================================================================================
# == THE OMNISCIENT PROFILE ORACLE (V-Ω-TOTALITY-V120.0-UNBREAKABLE-FINALIS)             ==
# =========================================================================================
# LIF: INFINITY | ROLE: ARCHETYPAL_DNA_RECONSTRUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_PROFILES_V120_NAMESPACE_PURIFICATION_TOTALITY
# =========================================================================================

import importlib.resources as pkg_resources
import re
import os
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Final, Tuple
from types import MappingProxyType
from pydantic import BaseModel, Field, ConfigDict

from ..core.alchemist import get_alchemist
from ..logger import Scribe

Logger = Scribe("GenesisOracle")


# =========================================================================================
# == SECTION I: GNOSTIC DATA CONTRACTS                                                   ==
# =========================================================================================

class ArchetypeProfile(BaseModel):
    """
    [THE IMMUTABLE VESSEL]
    The sacred contract for every manifest reality's DNA.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str
    archetype_path: str
    description: str
    category: str
    difficulty: str = "Adept"
    source: str = "Velm_Canon"
    gnosis_overrides: Dict[str, Any] = Field(default_factory=dict)
    fingerprint: str
    timestamp: float
    mass_bytes: int = 0


# =========================================================================================
# == SECTION II: THE CANON DNA (THE IMMORTAL OVERRIDES)                                  ==
# =========================================================================================
# These are the hardcoded Gnostic Laws for specific high-order archetypes.
# They override scried metadata to ensure structural integrity and automation.
# =========================================================================================

CANON_DNA: Final[Dict[str, Dict[str, Any]]] = {
    "fastapi-service": {
        "category": "Backend",
        "gnosis_overrides": {
            "database_type": "postgres",
            "auth_method": "jwt",
            "use_docker": True,
            "use_poetry": True,
            "port": 8000
        }
    },
    "fastapi-sqlalchemy": {
        "category": "Backend",
        "gnosis_overrides": {"database_type": "postgres", "use_alembic": True, "use_poetry": True}
    },
    "ai-agent-swarm": {
        "category": "Intelligence",
        "gnosis_overrides": {"use_redis": True, "agent_count": 3, "use_docker": True}
    },
    "langchain-nexus": {
        "category": "Intelligence",
        "gnosis_overrides": {"use_vector_db": True, "provider": "openai", "use_poetry": True}
    },
    "fullstack-monorepo": {
        "category": "System",
        "gnosis_overrides": {"use_docker": True, "frontend_framework": "react", "use_poetry": True}
    },
    "react-vite": {
        "category": "Frontend",
        "gnosis_overrides": {"use_docker": True, "project_type": "node", "port": 3000}
    },
    "nextjs-fortress": {
        "category": "Frontend",
        "gnosis_overrides": {"project_type": "node", "use_tailwind": True, "port": 3000}
    },
    "poetry-basic": {
        "category": "Language",
        "gnosis_overrides": {"use_poetry": True}
    },
    "new-artisan": {
        "category": "Meta",
        "gnosis_overrides": {"is_scaffold_extension": True}
    },
    "generic": {
        "category": "General",
        "gnosis_overrides": {"project_type": "generic"}
    }
}


# =========================================================================================
# == SECTION III: THE HEURISTIC ENGINE (THE DIVINER)                                     ==
# =========================================================================================

def _divine_category(slug: str) -> str:
    """[ASCENSION 3]: Heuristic Industrial Categorization."""
    slug = slug.lower()
    if any(k in slug for k in ["fastapi", "express", "api", "service", "grpc", "graphene"]): return "Backend"
    if any(k in slug for k in ["react", "nextjs", "astro", "chrome", "vite", "frontend", "ui"]): return "Frontend"
    if any(k in slug for k in ["ai", "langchain", "agent", "nexus", "brain", "neural"]): return "Intelligence"
    if any(k in slug for k in ["cli", "tool", "script", "generic-script", "utility"]): return "Utility"
    if any(k in slug for k in ["rust", "go", "python", "node", "poetry", "kt", "zig", "java", "cpp"]): return "Language"
    if any(k in slug for k in ["monorepo", "citadel", "monad", "splane", "workspace"]): return "System"
    if any(
        k in slug for k in ["docker", "container", "synapse", "cloud", "infra", "deployment"]): return "Infrastructure"
    if any(k in slug for k in ["docs", "mkdocs", "grimoire", "wiki"]): return "Documentation"
    return "General"


def _perceive_metadata(content: str, slug: str) -> Dict[str, str]:
    """[ASCENSION 7]: Socratic Metadata Scrying from blueprint comments."""
    meta = {
        "description": "A new reality forged in the Gnostic Forge.",
        "category": _divine_category(slug),
        "difficulty": "Adept"
    }

    # Scrying for explicit @markers in the first 2KB of the file
    header = content[:2048]
    desc = re.search(r'#\s*@description:\s*(.*)', header, re.I)
    if desc: meta["description"] = desc.group(1).strip()

    cat = re.search(r'#\s*@category:\s*(.*)', header, re.I)
    if cat: meta["category"] = cat.group(1).strip()

    diff = re.search(r'#\s*@difficulty:\s*(.*)', header, re.I)
    if diff: meta["difficulty"] = diff.group(1).strip()

    return meta


# =========================================================================================
# == SECTION IV: THE DISCOVERY SYMPHONY (THE FIX)                                       ==
# =========================================================================================

def _forge_the_grimoire() -> Dict[str, Any]:
    """
    [THE RITE OF RECTIFIED DISCOVERY]
    Recursive, namespace-pure discovery of every archetype in the cosmos.
    """
    found_profiles: Dict[str, Any] = {}

    # [THE CURE]: THE PURE ANCHOR
    # We strictly define the internal package path.
    # We do NOT use relative pathing to avoid 'src' pollution.
    INTERNAL_PACKAGE_NAME = 'velm'
    ARCHETYPES_SUBPACKAGE = 'archetypes'

    try:
        # 1. Gaze into the Archetypes Universe
        # We anchor at the root of the package.
        root_resource = pkg_resources.files(INTERNAL_PACKAGE_NAME).joinpath(ARCHETYPES_SUBPACKAGE)

        # [ASCENSION 2]: Recursive Stratum Scrying
        # Finds every .scaffold file across all sub-packages (genesis, components, etc.)
        for entry in root_resource.rglob('*.scaffold'):
            slug = entry.name.replace('.scaffold', '')
            content = entry.read_text(encoding='utf-8')

            # --- [ASCENSION 1]: THE LOGICAL NAMESPACE SUTURE (THE FIX) ---
            # We must derive the dotted Python path from the Traversable's internal hierarchy.
            # We ignore the physical disk path and use the package-relative path.

            # entry.parts might be ('...', 'velm', 'archetypes', 'genesis', 'file.scaffold')
            # We MUST find the index of the root package 'velm' to anchor the namespace.
            try:
                # Find the start of the logical package
                # This kills the 'velm.src.velm' double-naming heresy.
                parts = entry.parts
                # We look for the LAST occurrence of 'velm' to handle edge cases
                # where the user's home folder contains the string 'velm'.
                indices = [idx for idx, part in enumerate(parts) if part == INTERNAL_PACKAGE_NAME]
                if not indices:
                    raise ValueError(f"Package root '{INTERNAL_PACKAGE_NAME}' not found in traversable parts.")

                start_idx = indices[-1]  # Take the most specific package root
                # Extract parts from 'velm' to the parent of the file.
                # Result: ['velm', 'archetypes', 'genesis']
                logical_parts = list(parts[start_idx:-1])
                logical_package_path = ".".join(logical_parts)

            except (ValueError, IndexError):
                # Fallback to a safe hardcoded path if scrying fails
                logical_package_path = f"{INTERNAL_PACKAGE_NAME}.{ARCHETYPES_SUBPACKAGE}.genesis"

            # 3. Perception & DNA Merging
            meta = _perceive_metadata(content, slug)
            dna = CANON_DNA.get(slug, {})

            # [ASCENSION 4]: Cryptographic Fingerprinting
            fingerprint = hashlib.md5(content.encode()).hexdigest()[:12]

            # 4. Materialization of the Contract
            profile = ArchetypeProfile(
                name=slug,
                archetype_path=f"{logical_package_path}:{entry.name}",
                description=dna.get("description") or meta["description"],
                category=dna.get("category") or meta["category"],
                difficulty=dna.get("difficulty") or meta["difficulty"],
                source="Velm_Canon",
                gnosis_overrides={
                    "use_git": True,
                    "use_vscode": True,
                    "author": "The Architect",
                    "secret": get_alchemist()._forge_secret_rite,
                    **dna.get("gnosis_overrides", {})
                },
                fingerprint=fingerprint,
                timestamp=time.time(),
                mass_bytes=len(content)
            )
            found_profiles[slug] = profile.model_dump()

    except Exception as e:
        # [ASCENSION 6]: NoneType Sarcophagus
        Logger.error(f"Namespace Discovery Paradox: {e}")

    # 5. Global Extension Phase (The User's local ~/.scaffold/archetypes)
    user_forge = Path.home() / ".scaffold" / "archetypes"
    if user_forge.is_dir():
        for f in user_forge.glob('**/*.scaffold'):
            if f.stem in found_profiles: continue  # System Sovereignty
            try:
                content = f.read_text(encoding='utf-8')
                meta = _perceive_metadata(content, f.stem)
                fingerprint = hashlib.md5(content.encode()).hexdigest()[:12]

                profile = ArchetypeProfile(
                    name=f.stem,
                    archetype_path=str(f),
                    description=meta["description"],
                    category="User_Extension",
                    difficulty="Architect",
                    source="Local_Forge",
                    gnosis_overrides={"author": "The Architect"},
                    fingerprint=fingerprint,
                    timestamp=f.stat().st_mtime,
                    mass_bytes=len(content)
                )
                found_profiles[f.stem] = profile.model_dump()
            except Exception:
                continue

    return dict(sorted(found_profiles.items()))


# =========================================================================================
# == SECTION V: THE PROCLAIMED API (LOCKED)                                             ==
# =========================================================================================

# [ASCENSION 8]: MappingProxy Immutability
# The Grimoire is now read-only to prevent runtime profanation.
PROFILES: Final[MappingProxyType] = MappingProxyType(_forge_the_grimoire())


def get_profile(name: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific profile with absolute error-warding."""
    return PROFILES.get(name)


def list_profiles(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lists all manifest profiles, optionally filtered by category."""
    all_p = list(PROFILES.values())
    if category:
        return [p for p in all_p if p['category'].lower() == category.lower()]
    return all_p


def get_categories() -> List[str]:
    """Returns the unique industrial categories manifest in the Canon."""
    return sorted(list(set(p['category'] for p in PROFILES.values())))


# [ASCENSION 11]: Semantic Resonance Search
def search_canon(query: str) -> List[Dict[str, Any]]:
    """Performs a fuzzy Gaze to find resonant archetypes."""
    query = query.lower()
    results = []
    for data in PROFILES.values():
        score = 0
        if query in data['name'].lower(): score += 10
        if query in data['description'].lower(): score += 5
        if query in data['category'].lower(): score += 3

        if score > 0:
            res = data.copy()
            res['relevance'] = score
            results.append(res)

    return sorted(results, key=lambda x: x['relevance'], reverse=True)


# The Default Anchor
DEFAULT_PROFILE_NAME: Final[str] = "fastapi-service" if "fastapi-service" in PROFILES else "generic"

Logger.success(f"Gnostic Grimoire forged. [bold cyan]{len(PROFILES)}[/bold cyan] archetypes manifest in the namespace.")

# == SCRIPTURE SEALED: THE CANON IS NOW UNBREAKABLE ==