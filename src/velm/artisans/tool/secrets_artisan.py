# Path: scaffold/artisans/tool/secrets_artisan.py
# -----------------------------------------------

"""
=================================================================================
== THE Ω_SECRET_WARDEN: APOTHEOSIS (V-Ω-TOTALITY-VMAX-ENTROPY-FINALIS)         ==
=================================================================================
LIF: ∞^∞ | ROLE: ENTROPY_GOVERNOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SECRETS_VMAX_TOTALITY_2026_FINALIS_!#()$@()#()()

[THE MANIFESTO]
The era of the "Blank .env" is dead. This artisan is the absolute authority for
materializing project entropy. It righteously annihilates the "Manual Config"
heresy by conducting Autonomic Inception of internal secrets and providing
Gnostic Guidance for external providers.
=================================================================================
"""

import re
import secrets
import time
import hashlib
import unicodedata
from pathlib import Path
from typing import Dict, Any, List, Tuple, Final, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.requests import SecretsRequest
from ...interfaces.base import ScaffoldResult
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write
from rich.prompt import Confirm


class SecretsArtisan(BaseArtisan[SecretsRequest]):
    """
    =============================================================================
    == THE OMEGA SECRET WARDEN (V-Ω-TOTALITY-VMAX)                             ==
    =============================================================================
    LIF: ∞ | ROLE: ENTROPY_MATERIALIZER | RANK: OMEGA_SOVEREIGN
    """

    # [STRATUM: THE SAAS RETINA]
    # Maps key signatures to their celestial dashboards for the Architect.
    SAAS_ORACLE: Final[Dict[str, str]] = {
        "CLERK": "https://dashboard.clerk.com/",
        "STRIPE": "https://dashboard.stripe.com/test/apikeys",
        "AWS": "https://console.aws.amazon.com/iam/",
        "OPENAI": "https://platform.openai.com/api-keys",
        "SUPABASE": "https://supabase.com/dashboard/project/_/settings/api",
        "AUTH0": "https://manage.auth0.com/",
        "GITHUB": "https://github.com/settings/tokens",
        "RESEND": "https://resend.com/api-keys"
    }

    # [STRATUM: THE ENTROPY GRIMOIRE]
    # Regex to capture Keys and their (optional) existing values.
    SECRET_PATTERN: Final[re.Pattern] = re.compile(
        r"^(?P<key>[A-Z0-9_.-]+)\s*=\s*(?P<value>.*)$",
        re.MULTILINE
    )

    def execute(self, request: SecretsRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF DISPATCH (V-Ω-TOTALITY)                                     ==
        =============================================================================
        """
        trace_id = getattr(request, 'trace_id', 'tr-secrets-void')

        # Dispatch based on the willed action
        if request.action == "rotate":
            return self._conduct_rotation_rite(request, trace_id)
        elif request.action == "sync":
            return self._conduct_sync_rite(request, trace_id)

        return self.failure(f"Unmanifest Rite: The Keymaster does not know '{request.action}'.")

    def _conduct_sync_rite(self, request: SecretsRequest, trace_id: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF GENOMIC SYNC (V-Ω-TOTALITY-VMAX)                            ==
        =============================================================================
        LIF: 1,000x | ROLE: MATTER_CONVERGENCE
        [THE MASTER CURE]: Merges .env.example into .env, autonomicly materializing
        entropy for missing internal keys.
        """
        root = self.project_root
        target = request.target or ".env"
        example_path = root / f"{target}.example"
        env_path = root / target

        if not example_path.exists():
            return self.failure(f"Genetic Void: '{example_path.name}' is unmanifest. Cannot sync entropy.")

        self.logger.info(f"[{trace_id}] Initiating Genomic Sync: {example_path.name} -> {target}")

        # 1. READ THE LAW (Example) AND THE REALITY (Actual)
        example_content = example_path.read_text(encoding='utf-8')
        current_env = self._inhale_env(env_path) if env_path.exists() else {}

        # 2. THE CONVERGENCE LOOP
        new_lines = [
            f"# =============================================================================\n",
            f"# == GNOSTIC ENVIRONMENT MANIFEST | TRACE: {trace_id}\n",
            f"# == FORGED: {time.strftime('%Y-%m-%d %H:%M:%S')} | SEAL: 0x{self._forge_merkle_seal(example_content)}\n",
            f"# =============================================================================\n\n"
        ]

        waked_count = 0

        for line in example_content.splitlines():
            # Preserve Comments and Whitespace
            if not line.strip() or line.strip().startswith('#'):
                new_lines.append(line + "\n")
                continue

            match = self.SECRET_PATTERN.match(line)
            if not match:
                new_lines.append(line + "\n")
                continue

            key = match.group('key').strip()

            # THE ADJUDICATION
            if key in current_env and current_env[key]:
                # Reality is already resonant for this key. Preserve it.
                new_lines.append(f"{key}={current_env[key]}\n")
            else:
                # [THE MASTER CURE]: Direct Matter Inception
                # The key is missing or empty. We must manifest its soul.
                self.logger.verbose(f"   -> Waking internal entropy for '{key}'")

                # 1. Scry for SaaS guidance
                guidance = self._scry_saas_guidance(key)
                if guidance:
                    new_lines.append(f"# [GNOSTIC_CURE]: Obtain from {guidance}\n")

                # 2. Strike the Iron
                entropy = self._strike_entropy(key)
                new_lines.append(f"{key}={entropy}\n")
                waked_count += 1

        # 3. THE PHYSICAL STRIKE
        final_matter = "".join(new_lines)
        atomic_write(env_path, final_matter, self.logger, root)

        self._radiate_hud_pulse("ENV_SYNC_RESONANT", target, trace_id)

        return self.success(
            message=f"Genomic Sync Complete: {target} is now resonant with the Law.",
            data={"waked_keys": waked_count}
        )

    def _conduct_rotation_rite(self, request: SecretsRequest, trace_id: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF CHRONO-ROTATION (V-Ω-TOTALITY-VMAX)                         ==
        =============================================================================
        LIF: ∞ | ROLE: ENTROPY_RECYCLER
        [THE MASTER CURE]: Re-strikes all internal security keys with new entropy.
        """
        target = request.target or ".env"
        env_path = self.project_root / target

        if not env_path.exists():
            return self.failure(f"The scripture of secrets '{target}' is a void.")

        # --- MOVEMENT I: THE INQUEST ---
        content = env_path.read_text(encoding='utf-8')
        rotated_keys = []

        # [ASCENSION 1]: Gnostic Identity Suture
        # We only rotate keys that look like internal secrets, NOT third-party API keys
        # unless explicitly willed.
        def _replacer(match):
            key = match.group('key').strip()
            old_val = match.group('value').strip()

            # [THE CURE]: Logic for "Is this an internal re-strikable key?"
            is_internal = any(x in key.upper() for x in ("SECRET", "PASS", "SALT", "TOKEN", "KEY"))
            is_saas = any(saas in key.upper() for saas in self.SAAS_ORACLE)

            if is_internal and not is_saas:
                new_secret = self._strike_entropy(key)
                rotated_keys.append(key)
                return f"{key}={new_secret}"

            # Preserve existing if it's a SaaS key or non-secret matter
            return match.group(0)

        new_content, num_subs = self.SECRET_PATTERN.subn(_replacer, content)

        if not rotated_keys:
            return self.success("No internal Gnostic secrets found to rotate.")

        # --- MOVEMENT II: THE VOW OF WILL ---
        self.console.print(
            f"\n[bold yellow]The Keymaster will re-strike {len(rotated_keys)} internal secret(s) in {target}:[/]")
        for k in rotated_keys:
            self.console.print(f"  [cyan]Ω[/] {k}")

        if not request.force and not Confirm.ask("\n[bold red]This rite is IRREVERSIBLE. Shall we strike?[/]",
                                                 default=False):
            return self.success("The Rite of Rotation was stayed.")

        # --- MOVEMENT III: THE STRIKE ---
        atomic_write(env_path, new_content, self.logger, self.project_root)
        self._radiate_hud_pulse("ENTROPY_ROTATED", target, trace_id)

        return self.success(f"Success: {len(rotated_keys)} internal secrets have been waked with new entropy.")

    # =========================================================================
    # == INTERNAL FACULTIES (THE KERNEL)                                     ==
    # =========================================================================

    def _strike_entropy(self, key: str) -> str:
        """
        =============================================================================
        == THE ENTROPY KERNEL (V-Ω-TOTALITY)                                       ==
        =============================================================================
        [ASCENSION 3]: Forges high-entropy matter based on the key's semantic role.
        """
        k_upper = key.upper()

        # 1. The Password Alchemist (Human readable but complex)
        if "PASS" in k_upper:
            alphabet = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%^&*"
            return "".join(secrets.choice(alphabet) for _ in range(24))

        # 2. The Cryptographic Soul (High Density)
        if "KEY" in k_upper or "SECRET" in k_upper:
            return secrets.token_hex(64)  # 128-char hex soul

        # 3. The Token/Salt Shard
        return secrets.token_urlsafe(48)

    def _scry_saas_guidance(self, key: str) -> Optional[str]:
        """Perceives if a key belongs to a celestial provider."""
        k_upper = key.upper()
        for saas, url in self.SAAS_ORACLE.items():
            if saas in k_upper:
                return url
        return None

    def _inhale_env(self, path: Path) -> Dict[str, str]:
        """Inhales the environment into a Gnostic mapping."""
        env = {}
        try:
            content = path.read_text(encoding='utf-8')
            for match in self.SECRET_PATTERN.finditer(content):
                env[match.group('key').strip()] = match.group('value').strip()
        except Exception:
            pass
        return env

    def _forge_merkle_seal(self, content: str) -> str:
        """[ASCENSION 12]: Forges a 8-char seal of the Law."""
        return hashlib.md5(content.encode()).hexdigest()[:8].upper()

    def _radiate_hud_pulse(self, type_label: str, target: str, trace: str):
        """Radiates progress to the Ocular HUD."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SECRET_WARDEN_EVENT",
                        "label": type_label,
                        "message": f"Warded {target}",
                        "color": "#a855f7",
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_SECRET_WARDEN status=VIGILANT version=VMAX_2026>"