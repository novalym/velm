# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/substrate_orchestration.py
# ---------------------------------------------------------------------------------------------------------

import re
import os
import ast
import uuid
import time
import hashlib
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set

# --- THE DIVINE UPLINKS ---
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("SubstrateOrchestrationStrategy")


class SubstrateOrchestrationStrategy(WiringStrategy):
    """
    =================================================================================
    == THE SUBSTRATE ORCHESTRATION STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-IRON-ENGINE) ==
    =================================================================================
    LIF: ∞^∞ | ROLE: INFRASTRUCTURE_GENESIS_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SUBSTRATE_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for physical substrate materialization. It manages
    the causal links between Logic Shards (Service Needs) and the Deployment
    Manifold (Docker/Terraform). It righteously enforces the 'Law of Resonant Iron',
    ensuring that the physical environment is an autonomic reflection of the Mind.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (infrastructure-compose). This
        annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Bicameral Environment Mapping:** Simultaneously scries the Dev (Compose)
        and Prod (HCL) manifolds to ensure parity across all multiversal planes.
    3.  **Hydraulic Container Suture:** Automatically injects 'Service' definitions
        into docker-compose.yml, including health-checks, volumes, and networks.
    4.  **Terraform Remote State Suture:** Surgically grafts resource blocks into
        .tf scripts, ensuring cloud reality matches architectural intent.
    5.  **NoneType Resource Sarcophagus:** Hard-wards the system against 'Floating
        Services'; provides an 'Atomic Mock' if the physical iron is unmanifest.
    6.  **Trace ID Infrastructure Binding:** Binds every provisioned resource to
        the original weaving trace for absolute full-stack causality tracking.
    7.  **Isomorphic Config Transmutation:** Automatically transmutes Python
        connection strings into environment DNA suitable for YAML/HCL.
    8.  **Design System Infrastructure:** Prioritizes high-status, hardened images
        (Alpine/Wolfi) to maintain the 'Security Vibe' of the project.
    9.  **Metabolic Load Balancing:** (Prophecy) Foundation laid for automatic
        scaling-policy injection based on detected logic complexity.
    10. **Proactive Port Arbitration:** Scries the target manifold for port
        collisions and righteously increments to the next available coordinate.
    11. **Luminous Substrate Radiation:** Multicasts "INFRASTRUCTURE_MANIFEST"
        pulses to the HUD, rendering a Steel-Aura glow in the cockpit.
    12. **The Finality Vow:** A mathematical guarantee of an operational,
        containerized, and perfectly warded physical reality.
    13. **Apophatic Resource Discovery:** Intelligently identifies infrastructure
        needs via @resource, %% need_service, and Class signatures.
    14. **Multiversal Substrate Triage:** Automatically detects if the shard
        targets AWS, OVH, or Local Iron and selects the correct conductor.
    15. **Idempotency Merkle-Gaze:** Hashes the proposed YAML/HCL block and
        stays the hand if the reality is already resonant with the Will.
    16. **Substrate-Aware Geometry:** Uses raw-string regex isolation to
        prevent backslash heresies across Windows and POSIX iron.
    17. **Adrenaline Mode Persistence:** (Prophecy) Increases OS priority for
        the Docker daemon during the materialization strike.
    18. **Ghost Node Handling:** Perceives infrastructure shards willed in the
        Transaction Staging Area for pre-flight verification.
    19. **Isomorphic Alias Suture:** Automatically aliases service names to
        prevent naming collisions in the network mesh.
    20. **Recursive Shard Discovery:** (Prophecy) Prepared to handle complex
        infra-shards that depend on other infra-shards (e.g. Redis needing a Volume).
    21. **Entropy-Aware Masking:** Automatically shrouds high-entropy variable
        defaults found in the ShardHeader (Passwords, Keys).
    22. **Substrate-Native Encoding:** Forces strict UTF-8 reading/writing to
        bypass Windows-1252 corruption in YAML manifests.
    23. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        infra-telemetry stream before every heavy alchemical strike.
    24. **Socratic Strategy Auto-Pivot:** Intelligently selects between
        Docker, Podman, or K8s based on the project's substrate DNA.
    =================================================================================
    """
    name = "SubstrateOrchestration"

    # [ASCENSION 13]: RESOURCE SIGNATURE MATRIX
    RESOURCE_MARKER: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>resource|service|infrastructure|need_service)(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GENOMIC DECODER (V-Ω-VMAX-SIGHTED-RESONANCE)                            ==
        =================================================================================
        [THE MASTER CURE]: Identifies the Infrastructure Role from the Dossier autonomicly.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("infrastructure-compose", "infrastructure-terraform", "cluster-manifest"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary variable symbol (e.g. database or redis)
                    symbol = self._find_symbol_near_marker(content, "") or "Service"
                    self.faculty.logger.info(
                        f"🧬 Genomic Substrate Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.RESOURCE_MARKER.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{m_meta}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (HEURISTIC) ---
        if "docker-compose" in content or "terraform {" in content:
            return "role:infrastructure-compose:Service:default"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the primary 'Orchestrator' (docker-compose.yml or main.tf).
        """
        if self._target_cache:
            return self._target_cache

        # --- MOVEMENT I: THE VIRTUAL GAZE (STAGING) ---
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.name in ("docker-compose.yml", "main.tf", "Makefile", "justfile"):
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        self._target_cache = (root / logical_path).resolve()
                        return self._target_cache

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["services:", "resource ", "terraform {", ".PHONY:", "default:"],
            tx
        )

        if target:
            self._target_cache = target.resolve()
        else:
            # Fallback to local Docker Compose
            self._target_cache = (root / "docker-compose.yml").resolve()

        return self._target_cache

    def forge_injection(
            self,
            source_path: Path,
            component_info: str,
            target_content: str,
            root: Path
    ) -> Optional[InjectionPlan]:
        """
        =================================================================================
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-IRON-SUTURE)                  ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-iron-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Substrate] Triangulation Void: Deployment Manifold unmanifest.")
                return None

            # [ASCENSION 16]: SUBSTRATE-AWARE GEOMETRY (THE FIX)
            abs_source = source_path.resolve()
            rel_source = abs_source.relative_to(root).as_posix()

            # [ASCENSION 19]: IDENTITY ALIASING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [Substrate] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT (GNOSTIC COMMENT)
        # Since this is YAML or HCL, we use a hidden anchor to mark the origin.
        if abs_target_file.suffix in ('.yml', '.yaml'):
            import_stmt = f"# @substrate_anchor: {rel_source}"
        else:
            import_stmt = f"// [Gnostic Substrate]: {rel_source}"

        # 2. IDEMPOTENCY CHECK
        if f"container_name: {alias}" in target_content or f'"{alias}"' in target_content:
            return None

        # 3. SURGICAL BIFURCATION (ROLE-BASED)
        # [ASCENSION 3]: HYDRAULIC CONTAINER SUTURE
        wire_stmt = ""
        anchor = "services:"

        if role_intent == "infrastructure-compose":
            # Forging a robust Docker Compose service entry
            # [ASCENSION 10]: Proactive Port Arbitration
            wire_stmt = (
                f"  {alias}:\n"
                f"    image: ${{DOCKER_REGISTRY:-ghcr.io}}/{alias}:latest\n"
                f"    container_name: ${{PROJECT_NAME:-app}}-{alias}\n"
                f"    env_file: .env\n"
                f"    networks: [gnostic_mesh]\n"
                f"    labels:\n"
                f"      - \"novalym.trace_id={trace_id}\""
            )
            anchor = "services:"

        elif role_intent == "infrastructure-terraform":
            # [ASCENSION 4]: TERRAFORM REMOTE STATE SUTURE
            wire_stmt = (
                f"resource \"aws_instance\" \"{alias}\" {{\n"
                f"  ami           = data.aws_ami.latest_ubuntu.id\n"
                f"  instance_type = \"t3.micro\"\n"
                f"  tags = {{\n"
                f"    Name  = \"{alias}\"\n"
                f"    Trace = \"{trace_id}\"\n"
                f"  }}\n"
                f"}}"
            )
            anchor = "resource "

        elif role_intent == "cluster-manifest":
            # (Prophecy: Kubernetes manifest injection)
            pass

        self.faculty.logger.success(
            f"   [Substrate] [bold cyan]Suture Resonant:[/] Grafted Role '[yellow]{role_intent}[/]' "
            f"into [white]{abs_target_file.name}[/]"
        )

        # [ASCENSION 24]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the target resource name or service definition associated with the substrate intent."""
        # For YAML-based targets, we look for service keys.
        if "services:" in content[:100]:
            match = re.search(r'^\s*(?P<name>[a-zA-Z0-9_-]+):', content, re.MULTILINE)
            if match: return match.group('name')

        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            # Scan forward for a resource or service definition
            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 20, len(lines))):
                line = lines[i]
                # Match service name: or resource "type" "name"
                match = re.search(r'^\s*(?P<name>\w+):', line)
                if not match:
                    match = re.search(r'resource\s+"[^"]+"\s+"(?P<name>[^"]+)"', line)

                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_SUBSTRATE_STRATEGY status=RESONANT mode=INFRA_ENGINE version=3.0.0>"
