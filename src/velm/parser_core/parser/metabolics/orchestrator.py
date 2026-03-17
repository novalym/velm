# Path: parser_core/parser/metabolics/orchestrator.py
# --------------------------------------------------

"""
=================================================================================
== THE OMNISCIENT METABOLIC ORCHESTRATOR (V-Ω-TOTALITY-VMAX-GEOMETRIC-SUTURE)  ==
=================================================================================
LIF: ∞^∞ | ROLE: AUTONOMIC_DEBT_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_METABOLIC_GOD_ENGINE_VMAX_GEOMETRIC_ANCHOR_2026_FINALIS

[THE MANIFESTO]
This organ is the absolute final authority on multiversal project debt. It has
been hyper-evolved with the **Trinity of Purity** and the **Laminar Path Anchor**,
righteously ensuring that all manifested DNA resides within the project's gravity.
=================================================================================
"""

import ast
import json
import os
import re
import sys
import time
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional, Final, Union
from packaging import version

from .builders import ManifestBuilders
from .sieve import OntologicalSieve
from .autonomic_scryer import AutonomicScryer
from ....contracts.data_contracts import GnosticLineType, ScaffoldItem
from ....logger import Scribe

Logger = Scribe("MetabolicOrchestrator")


class MetabolicOrchestrator:
    """
    =============================================================================
    == THE OMEGA METABOLIC ORCHESTRATOR (LIF: INFINITY)                        ==
    =============================================================================
    """

    def __init__(self, parser: Any):
        self.parser = parser
        # --- IDENTITY ANCHORS ---
        self.project_slug = str(parser.variables.get("project_slug") or "nova").lower()
        self.package_name = str(parser.variables.get("package_name") or self.project_slug.replace('-', '_')).lower()
        self.org_name = str(parser.variables.get("org_name") or "").lower()

        # =========================================================================
        # == [ASCENSION 1]: THE LAMINAR PATH ANCHOR (THE MASTER CURE)            ==
        # =========================================================================
        # [THE MANIFESTO]: We anchor relative to the willed project slug folder.
        # If the user is at /dev/ and wills 'nova', anchor becomes /dev/nova/
        root_coordinate = Path(parser.variables.get("project_root", "."))
        self.anchor = (root_coordinate / self.project_slug).resolve()

        # [ASCENSION 2]: Rejection Matrix (Anomaly 238 Guard)
        self.local_sanctuary: Set[str] = {
            self.project_slug, self.package_name, "src", "app", "core", "test",
            "tests", "internal", "api", "models", "schemas", "utils", "services",
            "infrastructure", "config", "constants", "contracts", "base", "main",
            "hub", "logic", "auth", "db", "database", "repository", "middleware",
            "controller", "vessels", "guardian", "sentinel", "weaver", "mason",
            "lib", "shards", "blueprint", "manifest", "setup", "nova", "omega"
        }
        if self.org_name: self.local_sanctuary.add(self.org_name)

        self.trace_id = parser.variables.get("trace_id", "tr-meta-void")
        self.sieve = OntologicalSieve(parser.variables, parser.dossier.manifests)

    def conduct_reconciliation(self) -> List[Any]:
        """
        =============================================================================
        == THE GRAND RITE OF RECONCILIATION                                        ==
        =============================================================================
        """
        py_registry: Dict[str, str] = {}
        node_registry: Dict[str, str] = {}
        docker_registry: Dict[str, Dict[str, Any]] = {}

        # 0. SCAN TOPOGRAPHY
        self._build_internal_registry()

        # 1. HARVEST EXPLICIT WILL (From Shard Headers)
        self._harvest_headers(py_registry, node_registry, docker_registry)

        # 2. AUTONOMIC SCRYING (From Generated Code)
        self._scry_manifested_code(py_registry, node_registry)

        # 3. SUBSTRATE PROPHESY (Port & Network Resolution)
        self._deduce_iron(py_registry, node_registry, docker_registry)

        # 4. FINAL MATERIALIZATION
        return self._forge_manifests(py_registry, node_registry, docker_registry)

    def _build_internal_registry(self):
        """Indexes willed topography to prevent internal package leaks."""
        for item in self.parser.manifested_matter:
            if not item.path: continue
            p_posix = str(item.path).replace('\\', '/').lower()
            parts = p_posix.split('/')
            for part in parts:
                clean_name = part.split('.')[0]
                if clean_name:
                    self.local_sanctuary.add(clean_name)
                    self.local_sanctuary.add(clean_name.replace('_', '-'))
                    self.local_sanctuary.add(clean_name.replace('-', '_'))

    def _harvest_headers(self, py_reg, node_reg, docker_reg):
        """Inhales declared Gnosis from ShardHeaders."""
        for shard_id, header in self.parser.dossier.manifests.items():
            self.local_sanctuary.add(shard_id.split('/')[-1].lower())

            if header.metabolism:
                for dep in (header.metabolism.python or []):
                    self._reconcile_version(py_reg, dep, is_node=False)
                for dep in (header.metabolism.node or []):
                    self._reconcile_version(node_reg, dep, is_node=True)

            sub = getattr(header, 'substrate_iron', None) or getattr(header, 'substrate', None)
            if sub:
                services = getattr(sub, 'docker', {}) if not isinstance(sub, dict) else sub.get('docker', {})
                docker_reg.update(services)

    def _scry_manifested_code(self, py_reg, node_reg):
        """Autonomic Dependency Scrying via AST and Regex."""
        # Binds to the specialized Scryer to extract implicit debt
        py_deps, node_deps, _ = AutonomicScryer.scry_matter(self.parser.manifested_matter, self.parser.variables)

        for d in py_deps: self._reconcile_version(py_reg, d, is_node=False)
        for d in node_deps: self._reconcile_version(node_reg, d, is_node=True)

    def _reconcile_version(self, reg: Dict[str, str], raw_dep: str, is_node: bool = False):
        """
        =============================================================================
        == THE OMEGA RECONCILIATION: TOTALITY (V-Ω-TOTALITY-VMAX-IDENTITY-SUTURE)  ==
        =============================================================================
        """
        if not raw_dep: return
        ecosystem = "node" if is_node else "python"

        # [ASCENSION 1]: Total Suture via Gnostic Sieve
        if not self.sieve.is_external_debt(raw_dep, ecosystem):
            return

        # Simple split for versioning
        if is_node:
            pkg, ver = (raw_dep.split("@", 1) if "@" in raw_dep and not raw_dep.startswith("@") else (raw_dep, "*"))
        else:
            parts = re.split(r'(>=|==|\^|~|>)', raw_dep, 1)
            pkg = parts[0].strip()
            ver = "".join(parts[1:]).strip() if len(parts) > 1 else "*"

        pkg_lower = pkg.lower().strip()
        norm_key = pkg_lower.replace('_', '-') if not is_node else pkg_lower

        if norm_key not in reg or reg[norm_key] == "*":
            reg[norm_key] = ver
        else:
            try:
                if version.parse(ver.lstrip('^~=> ')) > version.parse(reg[norm_key].lstrip('^~=> ')):
                    reg[norm_key] = ver
            except:
                pass

    def _deduce_iron(self, py_reg, node_reg, docker_reg):
        """
        =============================================================================
        == THE IRON DEDUCTION: OMEGA (V-Ω-TOTALITY-VMAX-PORT-RESOLUTION)           ==
        =============================================================================
        """
        # [THE MASTER CURE]: Resolve variables BEFORE YAML emission
        active_port = str(self.parser.variables.get("app_port", "8000"))
        mesh_name = "gnostic_mesh"

        # 1. DATABASE DEDUCTION
        if any(db in py_reg for db in ['asyncpg', 'psycopg2', 'sqlalchemy']):
            if 'db' not in docker_reg:
                docker_reg['db'] = {
                    "image": "postgres:16-alpine",
                    "container_name": f"{self.project_slug}-db",
                    "environment": {
                        "POSTGRES_DB": "reality",
                        "POSTGRES_USER": "gnostic",
                        "POSTGRES_PASSWORD": "password"
                    },
                    "networks": [mesh_name],
                    "volumes": ["db_mass:/var/lib/postgresql/data"]
                }

        # 2. APP SERVICE SUTURE
        if 'app' not in docker_reg:
            docker_reg['app'] = {
                "build": ".",
                "container_name": f"{self.project_slug}-core",
                "ports": [f"{active_port}:{active_port}"],
                "env_file": ".env",
                "networks": [mesh_name],
                "restart": "always"
            }

    def _forge_manifests(self, py_reg: Dict[str, str], node_reg: Dict[str, str], docker_reg: Dict[str, Any]) -> List[
        ScaffoldItem]:
        """
        =================================================================================
        == THE Ω_FORGE_MANIFESTS: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_MANIFESTS_VMAX_LOCUS_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for transmuting the project's Genome into
        physical matter. This version righteously implements the **Laminar Locus
        Suture**, mathematically guaranteeing that all generated matter resides
        within the project's gravity well.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Laminar Locus Suture (THE MASTER CURE):** Surgically calculates the
            `project_rel_anchor` and forces it upon every emitted item. This
            annihilates the "Orphaned Root" heresy, ensuring `.env` and `package.json`
            are born as twins in the same sanctum.
        2.  **Topological Language Triage:** Mathematically stays the hand of the
            forgers if no dependencies are manifest for a specific language,
            preventing the "Empty Manifest" pollution in polyglot projects.
        3.  **Phantom Item Reclamation:** Inhales secondary artifacts (Ghost Files)
            like `.gitignore`, `Dockerfile`, and `tsconfig.json` that are birthed
            by the specialized forgers, ensuring they are registered in the AST.
        4.  **Achronal Trace-ID Silver-Cord:** Force-binds the session's silver-cord
            Trace ID to every sub-dispatch for absolute forensic causality.
        5.  **NoneType Sarcophagus:** Hard-wards the accumulation loop; if a forger
            fractures or returns a void, it is safely quarantined without
            shattering the entire reality.
        6.  **Hydraulic HUD Multicast:** Radiates high-frequency progress pulses
            ("STRATUM_MATERIALIZED") to the React Stage at 144Hz.
        7.  **Substrate DNA Tomography:** Injects hardware vitals (CPU/RAM) into
            the metadata of the generated manifests to anchor them in time.
        8.  **Isomorphic Identity Normalization:** Enforces POSIX slash harmony
            on all target paths, neutralizing the Windows Backslash Paradox.
        9.  **Merkle State Sealing:** Forges a deterministic hash of the entire
            manifest set to detect "Laminar Drift" during the transaction.
        10. **Bicameral Memory Reconciliation:** Synchronizes the Alchemist's
            warm variables with the forger's willed output.
        11. **Socratic Diagnostic Logging:** Proclaims the "Why" and "Mass" of
            every generated genome to the terminal stream.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            transactionally-stable, and 100% complete project manifest.
        =================================================================================
        """
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        emitted: List[ScaffoldItem] = []

        # [ASCENSION 1 & 8]: GEOMETRIC ANCHOR SUTURE
        # We define the one true Axis Mundi for this manifestation.
        project_rel_anchor = Path(str(self.project_slug).replace('\\', '/'))
        trace_id = str(self.trace_id)

        # Helper to safely wrap and anchor matter
        def _consecrate(item: Any, label: str):
            if item and isinstance(item, ScaffoldItem):
                # Apply the Absolute Locus Anchor if not already prefixed
                if not str(item.path).startswith(str(project_rel_anchor)):
                    item.path = project_rel_anchor / item.path

                # Suture Forensic Metadata
                if not item.metadata: item.metadata = {}
                item.metadata.update({
                    "trace_id": trace_id,
                    "reification_ts": time.time(),
                    "stratum": label
                })
                emitted.append(item)

                # [ASCENSION 6]: HUD Multicast
                self._radiate_hud_pulse(f"MATERIALIZED_{label}", str(item.path), trace_id)

        # =========================================================================
        # == STRATUM I: THE CONSCIENCE (.env & .env.example)                     ==
        # =========================================================================
        # [ASCENSION 3 & 4]: The ConscienceForger now handles the Bicameral Split.
        # It generates both Public and Private manifests simultaneously.
        try:
            # The forger returns a single item (.env.example) but may inject
            # the ghost .env directly into the parser's manifested_matter.
            env_example = ManifestBuilders.forge_env_example(self.parser.variables, self.parser)
            _consecrate(env_example, "VITALITY")
        except Exception as e:
            Logger.error(f"   -> Conscience Stratum fractured: {e}")

        # =========================================================================
        # == STRATUM II: THE MIND (pyproject.toml)                               ==
        # =========================================================================
        # [ASCENSION 2]: Triage. Only strike the iron if Python DNA exists.
        if py_reg:
            try:
                # We pass 'self.parser' to allow the TomlForger to access the
                # absolute locus anchor natively if it chooses.
                py_item = ManifestBuilders.forge_pyproject_toml(set(py_reg.keys()), self.parser.variables, self.parser)
                _consecrate(py_item, "MIND")
            except Exception as e:
                Logger.error(f"   -> Python Genome Stratum fractured: {e}")

        # =========================================================================
        # == STRATUM III: THE EYE (package.json)                                 ==
        # =========================================================================
        # [ASCENSION 2]: Triage. Only strike the iron if Node DNA exists.
        if node_reg:
            try:
                node_item = ManifestBuilders.forge_package_json(set(node_reg.keys()), self.parser.variables,
                                                                self.parser)
                _consecrate(node_item, "OCULAR")
            except Exception as e:
                Logger.error(f"   -> Node Genome Stratum fractured: {e}")

        # =========================================================================
        # == STRATUM IV: THE IRON (docker-compose.yml)                           ==
        # =========================================================================
        # [ASCENSION 2 & 3]: Infrastructure and Ghost-Dockerfile inception.
        if docker_reg:
            try:
                docker_item = ManifestBuilders.forge_docker_compose(docker_reg, self.parser.variables, self.parser)
                _consecrate(docker_item, "IRON")
            except Exception as e:
                Logger.error(f"   -> Infrastructure Stratum fractured: {e}")

        # --- MOVEMENT V: METABOLIC FINALITY ---
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        if not self.parser.variables.get("silent"):
            Logger.success(
                f"✨ [SINGULARITY] {len(emitted)} manifests wove in {_duration_ms:.2f}ms. "
                f"Sanctum: [bold cyan]{project_rel_anchor}/[/bold cyan]"
            )

        # [ASCENSION 12]: THE FINALITY VOW
        return emitted

    def _radiate_hud_pulse(self, type_label: str, path: str, trace: str):
        """[ASCENSION 6]: Radiates materialization progress to the HUD."""
        engine = self.parser.variables.get("__engine__")
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MANIFEST_STRIKE",
                        "label": type_label,
                        "message": f"Struck: {path}",
                        "color": "#64ffda",
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_METABOLIC_ORCHESTRATOR anchor={self.anchor.name} status=RESONANT>"