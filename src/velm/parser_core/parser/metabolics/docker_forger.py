import time
import hashlib
import json
import os
import platform
import yaml
from pathlib import Path
from typing import Dict, Any, Set, List, Tuple, Final, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....logger import Scribe

Logger = Scribe("DockerForger:Apotheosis")


# =========================================================================================
# == STRATUM 0: GNOSTIC STATE CONTRACTS (PYDANTIC V2)                                    ==
# =========================================================================================

class DockerServiceDNA(BaseModel):
    """
    =================================================================================
    == THE DOCKER SERVICE DNA (V-Ω-TOTALITY-VMAX-WARDED)                           ==
    =================================================================================
    LIF: ∞ | ROLE: GENOMIC_SERVICE_VESSEL | RANK: OMEGA_GUARDIAN
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    image: Optional[str] = None
    build: Optional[Union[str, Dict[str, Any]]] = None
    container_name: Optional[str] = Field(None, alias="container_name")
    ports: List[str] = Field(default_factory=list)
    expose: List[str] = Field(default_factory=list)
    environment: Dict[str, str] = Field(default_factory=dict)
    env_file: List[str] = Field(default_factory=list)
    networks: List[str] = Field(default_factory=list)
    volumes: List[str] = Field(default_factory=list)
    depends_on: Dict[str, Any] = Field(default_factory=dict)
    healthcheck: Dict[str, Any] = Field(default_factory=dict)
    restart: str = "unless-stopped"
    labels: List[str] = Field(default_factory=list)
    logging: Dict[str, Any] = Field(default_factory=lambda: {
        "driver": "json-file",
        "options": {"max-size": "10m", "max-file": "3"}
    })

    @field_validator('ports', 'expose', 'networks', 'volumes', 'labels', 'env_file', mode='before')
    @classmethod
    def _ensure_list(cls, v: Any) -> List[Any]:
        if v is None: return []
        if isinstance(v, str): return [v]
        return list(v)


class DockerForger:
    """
    =================================================================================
    == THE OMEGA DOCKER FORGER (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)                   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: INFRASTRUCTURE_GENOME_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_DOCKER_FORGER_VMAX_PORT_SHIELDED_2026_FINALIS

    The supreme final authority for materializing the Physical Iron. 
    It righteously enforces the Law of Ingress Authority.
    """

    # [STRATUM: THE PHALANX OF INGRESS]
    # Identifiers that signal a Sovereign Perimeter Gate.
    INGRESS_SIGNATURES: Final[Set[str]] = {
        "gateway", "caddy", "traefik", "nginx", "proxy", "ingress", "aperture", "shield"
    }

    # Internal services to be shielded from host port exposure.
    INTERNAL_MIND_SIGNATURES: Final[Set[str]] = {
        "api", "app", "worker", "backend", "service", "mind", "logic", "auth"
    }

    @classmethod
    def _get_absolute_locus_anchor(cls, variables: Dict[str, Any], parser: Any) -> Path:
        """
        [ASCENSION 3]: THE ABSOLUTE LOCUS ANCHOR (THE MASTER CURE).
        Mathematically binds the manifest to the project_slug sancutm.
        """
        slug = variables.get("project_slug", "")
        if slug and str(slug) not in (".", "/", "\\"):
            return Path(str(slug))
        return Path(".")

    @classmethod
    def forge(cls, services: Dict[str, Any], variables: Dict[str, Any], parser: Any) -> ScaffoldItem:
        """
        =========================================================================
        == THE RITE OF IRON INSCRIPTION (DOCKER-COMPOSE.YML)                   ==
        =========================================================================
        """
        _start_ns = time.perf_counter_ns()
        trace_id = variables.get("trace_id", f"tr-docker-{os.urandom(3).hex().upper()}")

        # --- MOVEMENT I: TOPOLOGICAL INGRESS ADJUDICATION ---
        # [ASCENSION 25]: THE MASTER CURE (PORT SHIELDING)
        # We perform a high-velocity biopsy of the service manifest to detect a Gateway.
        has_sovereign_gateway = any(
            any(sig in s_name.lower() for sig in cls.INGRESS_SIGNATURES)
            for s_name in services.keys()
        )

        if has_sovereign_gateway:
            Logger.info(f"[{trace_id[:8]}] Ingress Authority Detected. Activating Perimeter Shielding.")

        # --- MOVEMENT II: IDENTITY & LOCUS ACQUISITION ---
        p_slug = variables.get("project_slug", "nova-app")
        base_locus = cls._get_absolute_locus_anchor(variables, parser)

        enriched_services: Dict[str, Dict[str, Any]] = {}
        active_databases: List[str] = []
        active_caches: List[str] = []

        # --- MOVEMENT III: THE GENOMIC ENRICHMENT LOOP ---
        for s_name, s_data in services.items():
            # [ASCENSION 1]: MATERIALIZE SERVICE DNA
            # We wrap the raw dict in our strict Gnostic contract.
            dna = DockerServiceDNA.model_validate(s_data)
            image_name = str(dna.image or "").lower()

            # [ASCENSION 13]: SEMANTIC SERVICE ALIASING
            if not dna.container_name:
                dna.container_name = f"{p_slug}-{s_name}"

            # [ASCENSION 16 & 21]: ENVIRONMENT & LABELS SUTURE
            # Inhale project-wide DNA into the container environment.
            dna.environment["SCAFFOLD_ENV"] = "${SCAFFOLD_ENV:-development}"
            dna.labels.append(f"novalym.trace_id={trace_id}")
            dna.labels.append(f"novalym.project={p_slug}")

            # =========================================================================
            # == [ASCENSION 25]: THE MASTER CURE - PERIMETER SHIELDING               ==
            # =========================================================================
            # If a Gateway exists, we strip port bindings from internal nodes to
            # prevent bypass. We move them to 'expose' for mesh-only access.
            is_internal_node = any(sig in s_name.lower() for sig in cls.INTERNAL_MIND_SIGNATURES)
            is_gateway_node = any(sig in s_name.lower() for sig in cls.INGRESS_SIGNATURES)

            if has_sovereign_gateway and is_internal_node and not is_gateway_node:
                if dna.ports:
                    Logger.info(f"🛡️ [SHIELD] Resecting public ports for '{s_name}'. Transmuting to mesh-expose.")
                    # Take the internal port from '8000:8000' -> '8000'
                    internal_ports = [p.split(':')[-1] for p in dna.ports]
                    dna.expose.extend(internal_ports)
                    dna.ports = []

            # --- STRATUM: PERSISTENCE BIOPSY ---
            if "postgres" in image_name:
                active_databases.append(s_name)
                # [ASCENSION 1]: AUTONOMIC HEALTH PROBING
                if not dna.healthcheck:
                    dna.healthcheck = {
                        "test": ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"],
                        "interval": "5s",
                        "timeout": "5s",
                        "retries": 5
                    }
                dna.restart = "always"

            elif "redis" in image_name:
                active_caches.append(s_name)
                if not dna.healthcheck:
                    dna.healthcheck = {
                        "test": ["CMD", "redis-cli", "ping"],
                        "interval": "5s",
                        "timeout": "3s",
                        "retries": 5
                    }
                dna.restart = "always"

            # --- STRATUM: APPLICATION WIRING ---
            # [ASCENSION 2]: TOPOLOGICAL DEPENDENCY SUTURE
            if dna.build or "app" in s_name or "api" in s_name:
                # Ensure the App waits for the Iron (Databases/Caches) to be resonant.
                for infra_node in (active_databases + active_caches):
                    if infra_node not in dna.depends_on:
                        dna.depends_on[infra_node] = {"condition": "service_healthy"}

                # [ASCENSION 10]: LIVE-RELOAD VOLUME BINDING
                # Sync source code for sub-second development HMR.
                if variables.get("ENVIRONMENT") != "production":
                    if "./src:/app/src" not in dna.volumes:
                        dna.volumes.append("./src:/app/src")

            # --- STRATUM: OBSERVABILITY TRIAGE ---
            # [ASCENSION 8]: PROFILE SHARDING
            # Keep the default 'up' fast; metrics are waked via --profile metrics.
            if any(x in image_name for x in ("prometheus", "grafana", "jaeger", "loki", "otel")):
                if "metrics" not in getattr(dna, "profiles", []):
                    if not hasattr(dna, "profiles"): dna.profiles = []
                    dna.profiles.append("metrics")

            # [ASCENSION 11]: PLATFORM EMULATION (M-SERIES CURE)
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                if any(db in image_name for db in ("mysql", "oracle", "mssql")):
                    dna.platform = "linux/amd64"

            # Ingest enriched service back into the manifest pool
            enriched_services[s_name] = dna.model_dump(exclude_none=True, by_alias=True)

        # --- MOVEMENT IV: NETWORK MESH ISOLATION ---
        # [ASCENSION 14]: Forging the Gnostic Synapse.
        networks = {
            "gnostic_mesh": {
                "name": f"{p_slug}_gnostic_mesh",
                "driver": "bridge"
            }
        }

        # --- MOVEMENT V: MATERIALIZING THE YAML SCRIPTURE ---
        # [ASCENSION 22]: HYDRAULIC THREAD YIELDING
        # We ensure the event loop can breathe before the heavy serialization strike.
        time.sleep(0)

        # Build the final payload with willed volumes
        payload: Dict[str, Any] = {
            "version": "3.8",
            "services": enriched_services,
            "networks": networks
        }

        # [ASCENSION 4]: EPHEMERAL VOLUME PRUNING
        if active_databases or active_caches:
            payload["volumes"] = {}
            if active_databases: payload["volumes"]["db_mass"] = {"driver": "local"}
            if active_caches: payload["volumes"]["cache_mass"] = {"driver": "local"}

        # YAML Generation with bit-perfect formatting
        class GnosticDumper(yaml.Dumper):
            def increase_indent(self, flow=False, *args, **kwargs):
                return super().increase_indent(flow=flow, indentless=False)

        content = yaml.dump(
            payload,
            Dumper=GnosticDumper,
            default_flow_style=False,
            sort_keys=False,
            width=120
        )

        # [ASCENSION 7]: MERKLE STATE SEALING
        # Forging the bit-perfect fingerprint of the Iron Genome.
        merkle_seal = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12].upper()

        # --- MOVEMENT VI: AUTONOMIC GHOST FORGING ---
        # [ASCENSION 6]: The Phantom Dockerignore Sentinel
        cls._forge_dockerignore(parser, base_locus)

        # [ASCENSION 5]: Ghost-Dockerfile Scribe
        # Only forge if an 'app' exists and no Dockerfile is manifest in RAM or Disk.
        has_build_intent = any("build" in s_data for s_data in enriched_services.values())
        if has_build_intent:
            cls._forge_ghost_dockerfile(parser, base_locus, variables)

        # --- MOVEMENT VII: METABOLIC FINALITY ---
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 17]: OCULAR HUD MULTICAST
        if hasattr(parser, 'engine') and parser.engine and hasattr(parser.engine, 'akashic'):
            try:
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "METABOLIC_REIFICATION",
                        "label": "IRON_GENOME_SUTURED",
                        "message": f"Inscribing Iron into docker-compose.yml",
                        "color": "#3b82f6",  # Steel-Blue for Iron
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        if not variables.get("silent"):
            Logger.success(
                f"   -> [RESONANT] Iron Genome manifest forged in {_duration_ms:.2f}ms. Seal: 0x{merkle_seal}")

        # [ASCENSION 18 & 24]: THE FINALITY VOW
        return ScaffoldItem(
            path=base_locus / "docker-compose.yml",
            content=content,
            mutation_op="*=",  # SEMANTIC SUTURE: Deep-merge with existing Iron
            line_type=GnosticLineType.FORM,
            metadata={
                "origin": "DockerForger",
                "trace_id": trace_id,
                "merkle_seal": merkle_seal,
                "tax_ms": _duration_ms
            }
        )

    @classmethod
    def _forge_dockerignore(cls, parser: Any, base_locus: Path):
        """[ASCENSION 6]: Forges a pristine .dockerignore to shield the build context."""
        target_path = base_locus / ".dockerignore"

        # Idempotency check across the manifest buffer
        if hasattr(parser, 'manifested_matter'):
            if any(str(i.path) == str(target_path) for i in parser.manifested_matter if i.path):
                return

        ignore_content = """# Gnostic Abyssal Filters
.git
.scaffold
__pycache__
*.pyc
*.pyo
.venv
venv
node_modules
dist
build
.next
.env
.env.*
*.log
"""
        parser.manifested_matter.append(ScaffoldItem(
            path=target_path,
            content=ignore_content,
            mutation_op="=",
            line_type=GnosticLineType.FORM,
            metadata={"origin": "DockerForger_IgnoreGhost", "is_ghost": True}
        ))

    @classmethod
    def _forge_ghost_dockerfile(cls, parser: Any, base_locus: Path, variables: Dict[str, Any]):
        """
        [ASCENSION 5]: THE MASTER CURE (GHOST INCEPTION).
        If a Dockerfile is missing from both Iron (Disk) and Mind (RAM), we
        materialize a multi-stage production vessel autonomicly.
        """
        target_path = base_locus / "Dockerfile"

        # 1. BICAMERAL MEMORY ALIGNMENT
        # Scry for existing Dockerfiles in the physical or virtual strata.
        is_manifest = target_path.exists()
        if not is_manifest and hasattr(parser, 'manifested_matter'):
            is_manifest = any(str(i.path) == str(target_path) for i in parser.manifested_matter if i.path)

        if is_manifest:
            return

        # 2. SUBSTRATE DNA DIVINATION
        p_type = str(variables.get("project_type", "python")).lower()
        py_v = str(variables.get("python_version", "3.12")).replace("Python ", "").strip()

        if any(node_tag in p_type for node_tag in ("node", "ts", "react", "next")):
            # --- NODE.JS MULTI-STAGE GHOST ---
            docker_content = """# GNOSTIC NODEJS MULTI-STAGE VESSEL
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
# EXPOSE 3000
CMD ["npm", "start"]
"""
        else:
            # --- PYTHON MULTI-STAGE GHOST ---
            docker_content = f"""# GNOSTIC PYTHON MULTI-STAGE VESSEL
FROM python:{py_v}-slim-bookworm AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --only main

FROM python:{py_v}-slim-bookworm AS runner
RUN groupadd -r gnostic && useradd -r -g gnostic scaf_artisan
WORKDIR /app
COPY --from=builder /usr/local/lib/python{py_v}/site-packages /usr/local/lib/python{py_v}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
USER scaf_artisan
# EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

        # 3. KINETIC INCEPTION
        parser.manifested_matter.append(ScaffoldItem(
            path=target_path,
            content=docker_content,
            mutation_op="=",
            line_type=GnosticLineType.FORM,
            metadata={"origin": "DockerForger_DockerfileGhost", "is_ghost": True}
        ))

        Logger.success(f"   -> [GHOST INCEPTION] Multi-stage Dockerfile autonomicly forged for {p_type}.")

    def __repr__(self) -> str:
        return f"<Ω_DOCKER_FORGER status=RESONANT mode=PORT_SHIELDED version=VMAX_72>"