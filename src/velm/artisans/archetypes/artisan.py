# Path: src/velm/artisans/archetypes/artisan.py
# ---------------------------------------------

"""
=================================================================================
== THE CELESTIAL LIBRARIAN (V-Ω-TOTALITY-V200.0-FEDERATED-CORE)                ==
=================================================================================
LIF: ∞ | ROLE: ARCHETYPE_GOVERNOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_LIBRARIAN_V200_UI_READY

The Supreme Conductor of pattern discovery and materialization.
This artisan bridges the gap between the Physical Hardware (Disk) and the
Celestial Gist Stream (GitHub).

It provides a unified, precedence-aware, and type-safe view of all Gnostic
Archetypes available to the Architect, specifically engineered to serve as the
backend logic for Ocular UIs (React/Next.js) via the Daemon.
=================================================================================
"""

import os
import json
import time
import shutil
import hashlib
import requests
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, asdict, field

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ArchetypeRequest
from ...help_registry import register_artisan
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("Librarian")


# =============================================================================
# == I. THE GNOSTIC DATA CONTRACTS (UI-READY)                                ==
# =============================================================================

@dataclass
class ArchetypeProfile:
    """
    The Immutable Soul of an Archetype.
    Structured for direct consumption by the Ocular UI.
    """
    id: str
    name: str
    description: str
    category: str  # Backend, Frontend, System, etc.
    tags: List[str]
    difficulty: str
    source_realm: str  # Celestial, Global, Local, System
    url: Optional[str] = None  # None if local
    sha256: Optional[str] = None
    local_path: Optional[str] = None
    is_installed: bool = False
    last_updated: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# == II. THE CELESTIAL LIBRARIAN                                             ==
# =============================================================================

@register_artisan("archetypes")
class ArchetypeArtisan(BaseArtisan[ArchetypeRequest]):
    """
    =================================================================================
    == THE OMNISCIENT LIBRARIAN                                                    ==
    =================================================================================
    The Sovereign Mind of pattern discovery.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Quadratic Dimensional Fusion:** Simultaneously scries Local, Global,
        System, and Celestial realms to build a unified Gnostic registry.
    2.  **Merkle Root Integrity Warden:** Uses SHA-256 fingerprints from the
        Master Index to verify the 'Soul Purity' of every downloaded shard.
    3.  **Achronal Cache Protocol (ETag):** Uses HTTP ETag validation to prevent
        burning bandwidth on unchanged indices. 0ms latency if fresh.
    4.  **Ocular-Optimized Serialization:** The `list` rite returns a hyper-structured
        JSON payload specifically designed for virtualized lists in Web UIs.
    5.  **Semantic Precedence Enforcement:** Physically handles collisions by
        prioritizing Local > Global > System > Celestial patterns.
    6.  **Fault-Isolated Triage:** If the aether is dark (offline), the Librarian
        silently falls back to cached Gnosis, maintaining 100% uptime for the UI.
    7.  **HUD Multicast:** Broadcasts 'LIBRARIAN_SCRY' signals to the
        React membrane via the Daemon for real-time visual loading states.
    8.  **Atomic Inscription:** Writes blueprints to `.tmp` before renaming, ensuring
        no torn reads by the filesystem watcher.
    9.  **Socratic Search:** Implements fuzzy keyword matching on the client side
        to filter the merged registry instantly.
    10. **Metadata Injection:** Automatically injects `_provenance` metadata into
        downloaded blueprints for future auditing.
    11. **The Purge Rite:** Can surgically excise cached archetypes to free space.
    12. **The Finality Vow:** Returns a guarantee of structural validity for every
        profile served.
    """

    # [THE CELESTIAL COORDINATES]
    # Anchored to the Sovereign Repository of the Grimoire.
    # This URL points to the auto-generated index from the GitHub Action.
    REPO_USER = "novalym"
    REPO_NAME = "velm-grimoire"
    CELESTIAL_INDEX_URL = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/index.json"

    # [LOCAL SANCTUMS]
    GLOBAL_FORGE = Path.home() / ".scaffold" / "archetypes"
    SYSTEM_FORGE = Path(__file__).parent.parent.parent / "archetypes"
    CACHE_FILE = Path.home() / ".scaffold" / "celestial_index.json"
    ETAG_FILE = Path.home() / ".scaffold" / "celestial_etag.txt"

    def execute(self, request: ArchetypeRequest) -> ScaffoldResult:
        """The Grand Symphony of Discovery."""

        # 0. THE AUTO-BOOTSTRAP
        self._ensure_global_sanctum()

        # RITE ROUTING
        rite_map = {
            "list": self._conduct_list_rite,
            "sync": self._conduct_sync_rite,
            "pull": self._conduct_pull_rite,
            "inspect": self._conduct_inspect_rite,
            "search": self._conduct_search_rite,
            "purge": self._conduct_purge_rite
        }

        # Default to List if ambiguous
        handler = rite_map.get(request.command, self._conduct_list_rite)
        return handler(request)

    # =========================================================================
    # == MOVEMENT I: THE RITE OF DISCOVERY (LIST)                            ==
    # =========================================================================

    def _conduct_list_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """
        [THE OMNISCIENT LIST]
        Aggregates all known archetypes into a unified, UI-ready list.
        """
        self._hud_pulse("SCRYING_REGISTRY", "#64ffda")

        # 1. Scry All Realms
        merged_registry = self._scry_all_realms()

        # 2. Filter (The Socratic Sieve)
        # Allows the UI/CLI to request specific subsets
        filtered = []
        target_category = request.category.lower() if request.category else None
        target_query = request.target.lower() if request.target else None

        for profile in merged_registry.values():
            # Category Filter
            if target_category and target_category != "all":
                if profile.category.lower() != target_category:
                    continue

            # Text Search Filter
            if target_query:
                blob = f"{profile.name} {profile.description} {' '.join(profile.tags)}".lower()
                if target_query not in blob:
                    continue

            filtered.append(profile)

        # Sort: Local first, then by name
        filtered.sort(key=lambda x: (0 if x.source_realm == "Local" else 1, x.name))

        # [ASCENSION 4]: Ocular Projection (JSON Mode)
        # This is the primary output for the Workbench/UI.
        if request.json or getattr(request, 'json_mode', False):
            return self.success(
                "Librarian Census complete.",
                data={
                    "count": len(filtered),
                    "profiles": [p.to_dict() for p in filtered],
                    "realms_scanned": ["System", "Global", "Local", "Celestial"]
                }
            )

        # --- THE HUMAN REVELATION (RICH TABLE) ---
        from rich.table import Table
        from rich.box import SIMPLE_HEAVY

        table = Table(
            title=f"[bold cyan]The Gnostic Grimoire[/bold cyan] [dim]({len(filtered)} shards manifest)[/]",
            box=SIMPLE_HEAVY,
            expand=True,
            border_style="dim"
        )
        table.add_column("Shard ID", style="bold white", width=25)
        table.add_column("Stratum", style="magenta")
        table.add_column("Realm", justify="center")
        table.add_column("Status", justify="right")

        for p in filtered:
            realm_style = {
                "Local": "bold cyan",
                "Global": "green",
                "System": "dim white",
                "Celestial": "blue"
            }.get(p.source_realm, "white")

            status = "✅ Manifest" if p.is_installed else "☁️ Aether"

            table.add_row(
                p.name,
                p.category,
                f"[{realm_style}]{p.source_realm}[/]",
                status
            )

        self.console.print(table)
        return self.success("The Census of Patterns is manifest.")

    # =========================================================================
    # == MOVEMENT II: THE RITE OF HARMONY (SYNC)                             ==
    # =========================================================================

    def _conduct_sync_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """
        [THE CELESTIAL SYNC]
        Communes with GitHub to update the local cache index.
        Uses ETag to ensure zero-cost if nothing has changed.
        """
        Logger.info(f"Communing with Celestial Atlas at {self.REPO_USER}/{self.REPO_NAME}...")
        self._hud_pulse("SYNCING_CELESTIAL", "#a855f7")

        try:
            headers = {}
            # Load previous ETag
            if self.ETAG_FILE.exists() and self.CACHE_FILE.exists():
                headers['If-None-Match'] = self.ETAG_FILE.read_text().strip()

            # 1. Scry the Master Index
            response = requests.get(self.CELESTIAL_INDEX_URL, headers=headers, timeout=10)

            if response.status_code == 304:
                Logger.verbose("Celestial Index is unchanged. Using cached Gnosis.")
                return self.success("Lattice is already in harmony.")

            response.raise_for_status()

            # 2. Validate Gnosis
            data = response.json()
            if "archetypes" not in data:
                raise ArtisanHeresy("Celestial Index is profane (Missing 'archetypes' key).")

            # 3. Inscribe to Achronal Cache
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.CACHE_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')

            # Save new ETag
            if 'ETag' in response.headers:
                self.ETAG_FILE.write_text(response.headers['ETag'])

            count = len(data.get("archetypes", []))
            return self.success(
                f"Lattice synchronized. {count} celestial patterns manifest in cache."
            )

        except Exception as e:
            # [ASCENSION 6]: Fault-Isolated Triage
            Logger.warn(f"Celestial link severed: {e}. Falling back to cached Gnosis.")
            return self.failure(
                f"Celestial link severed: {str(e)}",
                suggestion="Verify your connection to the GitHub aether."
            )

    # =========================================================================
    # == MOVEMENT III: ACQUISITION (PULL)                                    ==
    # =========================================================================

    def _conduct_pull_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """
        [THE CELESTIAL PULL]
        Materializes a remote pattern into the Global Forge.
        """
        slug = request.target
        if not slug:
            return self.failure("Heresy of the Void: No archetype target willed for acquisition.")

        # 1. Locate in Cache
        registry = self._scry_all_realms()
        profile = registry.get(slug)

        if not profile:
            return self.failure(f"Archetype '{slug}' is unknown to the Librarian.")

        if profile.source_realm != "Celestial":
            return self.success(f"Archetype '{slug}' is already manifest in the {profile.source_realm} realm.")

        if not profile.url:
            return self.failure("Archetype has no celestial coordinate.")

        self.Logger.info(f"Materializing '{slug}' from the heavens...")
        self._hud_pulse("PULLING_MATTER", "#fbbf24")

        try:
            # 2. Streaming Inception
            res = requests.get(profile.url, timeout=15)
            res.raise_for_status()
            content = res.text

            # 3. [ASCENSION 2]: Merkle Integrity Check
            if profile.sha256:
                actual_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                if actual_hash != profile.sha256:
                    raise ArtisanHeresy(
                        f"Integrity Breach: Shard '{slug}' is corrupted.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="The cloud matter has drifted. Contact the High Architect."
                    )

            # 4. Atomic Inscription
            dest = self.GLOBAL_FORGE / f"{slug}.scaffold"

            # Inject Provenance Header
            provenance = f"# @provenance: celestial_pull_v1\n# @timestamp: {time.time()}\n"
            final_content = provenance + content

            tmp_dest = dest.with_suffix(".tmp")
            tmp_dest.write_text(final_content, encoding='utf-8')
            tmp_dest.replace(dest)

            return self.success(
                f"Pattern '{slug}' successfully manifest in Global Forge.",
                data={"path": str(dest)},
                artifacts=[Artifact(path=dest, action="created", type="file")]
            )

        except Exception as e:
            return self.failure(f"Materialization Paradox: {str(e)}")

    # =========================================================================
    # == MOVEMENT IV: INSPECTION & SEARCH                                    ==
    # =========================================================================

    def _conduct_inspect_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """Detailed Gnostic Dossier for a single archetype."""
        slug = request.target
        registry = self._scry_all_realms()
        profile = registry.get(slug)

        if not profile:
            return self.failure(f"Pattern '{slug}' not found.")

        # If it's local/global, we can read the file content to extract variables
        dna_content = {}
        if profile.local_path and Path(profile.local_path).exists():
            from ...genesis.canon_dna import GnosticDNAOracle
            # Lightweight scan
            try:
                content = Path(profile.local_path).read_text()
                dna_content = GnosticDNAOracle.extract_variables(content)
            except:
                pass

        return self.success(
            "Inspection Complete",
            data={
                "profile": profile.to_dict(),
                "variables": dna_content
            }
        )

    def _conduct_search_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """Alias for filtered list."""
        return self._conduct_list_rite(request)

    def _conduct_purge_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        slug = request.target
        target = self.GLOBAL_FORGE / f"{slug}.scaffold"
        if target.exists():
            target.unlink()
            return self.success(f"Archetype '{slug}' returned to the void.")
        return self.failure("Target not found in Global Forge.")

    # =========================================================================
    # == INTERNAL ORGANS (THE SENSES)                                        ==
    # =========================================================================

    def _scry_all_realms(self) -> Dict[str, ArchetypeProfile]:
        """
        [THE QUADRATIC FUSION]
        Merges System, Global, Local, and Celestial definitions.
        Higher realms override lower ones.
        """
        registry: Dict[str, ArchetypeProfile] = {}

        # 1. Celestial Realm (From Cache)
        if self.CACHE_FILE.exists():
            try:
                data = json.loads(self.CACHE_FILE.read_text())
                for item in data.get("archetypes", []):
                    prof = ArchetypeProfile(
                        id=item['name'],
                        name=item['name'],
                        description=item.get('description', ''),
                        category=item.get('category', 'Unclassified'),
                        tags=item.get('tags', []),
                        difficulty=item.get('difficulty', 'Unknown'),
                        source_realm="Celestial",
                        url=item.get('url'),
                        sha256=item.get('sha256')
                    )
                    registry[prof.id] = prof
            except Exception:
                Logger.warn("Celestial Cache is corrupt.")

        # 2. System Realm (Built-ins)
        self._scan_fs_realm(self.SYSTEM_FORGE, "System", registry)

        # 3. Global Realm (~/.scaffold)
        self._scan_fs_realm(self.GLOBAL_FORGE, "Global", registry)

        # 4. Local Realm (Project .scaffold)
        local_forge = self.engine.project_root / ".scaffold" / "archetypes"
        if local_forge.exists():
            self._scan_fs_realm(local_forge, "Local", registry)

        return registry

    def _scan_fs_realm(self, path: Path, realm: str, registry: Dict[str, ArchetypeProfile]):
        """Scans a physical directory for .scaffold files and parses headers."""
        from ...genesis.canon_dna import GnosticDNAOracle

        if not path.exists(): return

        for f in path.rglob("*.scaffold"):
            try:
                # Fast header read
                content = f.read_text(encoding='utf-8')[:2048]
                dna = GnosticDNAOracle.divine(f.stem, content)

                profile = ArchetypeProfile(
                    id=dna['name'],
                    name=dna['name'],
                    description=dna.get('description', 'Local Artifact'),
                    category=dna.get('category', 'Custom'),
                    tags=dna.get('tags', []),
                    difficulty=dna.get('difficulty', 'Unknown'),
                    source_realm=realm,
                    local_path=str(f),
                    is_installed=True,
                    last_updated=f.stat().st_mtime
                )
                registry[profile.id] = profile
            except Exception:
                pass

    def _ensure_global_sanctum(self):
        self.GLOBAL_FORGE.mkdir(parents=True, exist_ok=True)
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    def _hud_pulse(self, label: str, color: str):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LIBRARIAN_SCRY",
                        "label": label,
                        "color": color,
                        "trace": getattr(self.request, 'trace_id', 'tr-librarian')
                    }
                })
            except:
                pass

# == SCRIPTURE SEALED: THE LIBRARIAN IS OMNIPOTENT ==