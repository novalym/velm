# Path: src/velm/core/infrastructure/factory.py
# ---------------------------------------------
# LIF: ∞ | ROLE: PROVIDER_MANUFACTORY | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_INFRA_FACTORY_V200_TOTALITY_2026_FINALIS

import os
import importlib
import threading
from typing import Dict, Type, Any, Optional, Final, List

from .contracts import ComputeProvider
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("InfraFactory")


class InfrastructureFactory:
    """
    =============================================================================
    == THE CLOUD FOUNDRY (V-Ω-TOTALITY-V200)                                   ==
    =============================================================================
    The supreme registry and materialization engine for Cloud Providers.
    It governs the transition from Gnostic Intent to Physical Connection.
    """

    # [STRATUM-0]: THE REGISTRY OF SOVEREIGNTY
    # Mapping of semantic slugs to their module and class coordinates.
    _GRIMOIRE: Final[Dict[str, Dict[str, str]]] = {
        "aws": {
            "module": ".providers.aws",
            "class": "AWSProvider",
            "sdk": "boto3",
            "alias": ["titan-west", "ec2"]
        },
        "oracle": {
            "module": ".providers.oracle",
            "class": "OracleProvider",
            "sdk": "oci",
            "alias": ["titan-east", "oci"]
        },
        "hetzner": {
            "module": ".providers.hetzner",
            "class": "HetznerProvider",
            "sdk": "hcloud",
            "alias": ["mercenary", "vps"]
        },
        "docker": {
            "module": ".providers.docker_local",
            "class": "DockerLocalProvider",
            "sdk": "docker",
            "alias": ["local", "simulacrum"]
        }
    }

    _INSTANCE_CACHE: Dict[str, ComputeProvider] = {}
    _LOCK = threading.RLock()

    @classmethod
    def summon(cls,
               provider_name: str,
               config: Optional[Dict[str, Any]] = None,
               use_cache: bool = True) -> ComputeProvider:
        """
        =============================================================================
        == THE RITE OF SUMMONING (V-Ω-JIT-MATERIALIZATION)                        ==
        =============================================================================
        LIF: 100x | ROLE: PROVIDER_INCEPTOR

        Materializes a concrete Cloud Provider. Resolves aliases, verifies SDKs,
        and injects environment DNA.
        """
        # 1. RESOLVE IDENTITY
        slug = cls._resolve_slug(provider_name)

        # 2. CACHE PROBE
        if use_cache and slug in cls._INSTANCE_CACHE:
            return cls._INSTANCE_CACHE[slug]

        with cls._LOCK:
            if use_cache and slug in cls._INSTANCE_CACHE:
                return cls._INSTANCE_CACHE[slug]

            # 3. LATE-BOUND MATERIALIZATION
            if slug not in cls._GRIMOIRE:
                raise ArtisanHeresy(
                    f"Unmanifest Provider: '{provider_name}' is unknown to the Foundry.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"Manifest providers: {', '.join(cls._GRIMOIRE.keys())}"
                )

            manifest = cls._GRIMOIRE[slug]

            # 4. SDK BIOPSY
            cls._verify_sdk_resonance(manifest)

            # 5. DYNAMIC IMPORT RITE
            try:
                module = importlib.import_module(manifest["module"], package=__package__)
                ProviderClass = getattr(module, manifest["class"])
            except (ImportError, AttributeError) as e:
                Logger.critical(f"Gnostic Schism: Failed to load {slug} driver: {e}")
                raise ArtisanHeresy(
                    f"Driver Fracture: The {slug} driver is corrupt or unmanifest.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

            # 6. CONFIGURATION FUSION (DNA GRAFTING)
            # We merge the provided config with the system environment.
            final_config = cls._terraform_config(config)

            # 7. APOTHEOSIS (INSTANTIATION)
            try:
                instance = ProviderClass(final_config)

                # Verify that the instance honors the current Constitution
                if not isinstance(instance, ComputeProvider):
                    raise TypeError(f"Artisan {manifest['class']} violates the ComputeProvider contract.")

                if use_cache:
                    cls._INSTANCE_CACHE[slug] = instance

                Logger.success(f"Provider [{slug.upper()}] manifest and resonant.")
                return instance

            except Exception as e:
                raise ArtisanHeresy(
                    f"Inception Fracture: Failed to birth {slug} provider.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL
                )

    @classmethod
    def _resolve_slug(cls, name: str) -> str:
        """Maps aliases back to the canonical provider code."""
        query = name.lower().strip()
        if query in cls._GRIMOIRE:
            return query

        for slug, meta in cls._GRIMOIRE.items():
            if query in meta.get("alias", []):
                return slug
        return query

    @classmethod
    def _verify_sdk_resonance(cls, manifest: Dict):
        """[THE CURE]: Checks for required Python SDKs before attempting import."""
        sdk_name = manifest.get("sdk")
        if not sdk_name: return

        if importlib.util.find_spec(sdk_name) is None:
            raise ArtisanHeresy(
                f"Metabolic Void: The {manifest['class']} requires the '{sdk_name}' shard.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Command the shell: [bold cyan]pip install {sdk_name}[/bold cyan]",
                code="MISSING_SDK"
            )

    @classmethod
    def _terraform_config(cls, user_config: Optional[Dict]) -> Dict[str, Any]:
        """[ASCENSION 2]: Inhales environment DNA and project metadata."""
        # 1. System DNA
        dna = dict(os.environ)

        # 2. User Intent (Overrides)
        if user_config:
            dna.update(user_config)

        return dna

    @classmethod
    def list_manifest_realms(cls) -> List[Dict[str, Any]]:
        """Proclaims the census of all supported cloud domains."""
        return [
            {
                "code": slug,
                "class": meta["class"],
                "aliases": meta["alias"],
                "status": "RESONANT" if importlib.util.find_spec(meta["sdk"]) else "LATENT"
            }
            for slug, meta in cls._GRIMOIRE.items()
        ]