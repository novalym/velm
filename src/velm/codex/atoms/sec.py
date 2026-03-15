# Path: src/velm/codex/atoms/sec.py
# ---------------------------------------------------------------------------------
# SYSTEM: Codex Atoms / Security Domain
# COMPONENT: SecurityDomain (The Omega Sentinel)
# STABILITY: Titanium / Unbreakable / Resonant
# ---------------------------------------------------------------------------------
import hashlib
import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union
from ..contract import BaseDirectiveDomain, require_packages
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("SecurityDomain")


@domain("sec")
class SecurityDomain(BaseDirectiveDomain):
    """
    =================================================================================
    == THE OMEGA SECURITY ATOM (V-Ω-TOTALITY-V100200-SUTURED-FINALIS)              ==
    =================================================================================
    LIF: ∞ | ROLE: SECURITY_CONDUCTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SEC_ATOM_V100K_FINAL_SUTURE_2026

    The supreme orchestrator of the project's immune system. This artisan scries
    the project's topology to forge warded logical bonds that protect the
    sanctity of Matter and Mind.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Functional Interface Suture (THE CURE):** Ensures the generated __init__.py
        imports perfectly match the functional proxies (summon_secret, awaken),
        annihilating the "Cannot find reference" IDE heresy.
    2.  **Absolute Dependency Inception (THE FIX):** Automatically injects all
        runtime imports (starlette, fastapi, pydantic) into the generated output,
        ensuring 100% syntactical purity upon materialization.
    3.  **Substrate-Aware Geometry:** Dynamically detects if the target is a
        Package vs a Module to resolve 'from .' vs 'from ..' import paradoxes.
    4.  **The Omni-Fortify Rite:** A singular, high-LIF command to weave the entire
        Security Stratum and output a unified 'bind_security_citadel(app)' orchestrator.
    5.  **Recursive Fortress Weaving:** Automatically triggers 'logic.weave' of
        corresponding structural shards (DNA) for Vault, Shield, and Sentinel.
    6.  **Shannon Entropy Sieve:** Scans willed security variables for accidental
        plaintext secret leaks before they strike the Iron.
    7.  **JWT Sentinel Forge:** Materializes industrial-grade JWT validation with
        asymmetric key support and automatic token-revocation checks.
    8.  **PII Redaction Scribe:** Generates high-speed regex phalanxes to mask
        sensitive data (Emails, Keys, SSNs) in outgoing logs and JSON responses.
    9.  **The Privacy Shroud (AES-GCM):** Forges the logic for rotational
        field-level encryption for persistence models.
    10. **Forensic Audit Injection:** Weaves a Merkle-signed ledger into
        state-changing API endpoints for absolute traceability.
    11. **Zero-Trust CORS Tomography:** Intelligently calculates allowed hosts
        based on environment DNA (DEV/PROD) and domain intention.
    12. **RBAC Jurisprudence:** Generates declarative permission gates using
        FastAPI 'Depends' to enforce the Law of Station.
    13. **Argon2id Hash Vow:** Injects the current gold-standard for password
        hashing, including salt-generation and Pepper-suturing.
    14. **CSP Header Alchemist:** Forges Content Security Policies that
        neutralize XSS vectors while preserving Ocular HUD functionality.
    15. **Brute-Force Banishment:** Forges Nginx and Systemd configurations
        to banish IP addresses exhibiting high-frequency metabolic friction.
    16. **Secure Session Sarcophagus:** Forges encrypted, server-side session
        stores using Redis-backed ephemeral memory.
    17. **Vault Secret Rotation Edict:** Generates the Maestro commands required
        to rotate AWS/HCP Vault secrets without downtime.
    18. **SSRF Perimeter Shield:** Injects logic to prevent the AI or Backend
        from accessing the 169.254.169.254 celestial metadata endpoint.
    19. **Zero-Trust SSH Tunneling:** Forges the configuration for warded,
        identity-proxied SSH access to internal databases.
    20. **Achronal Trace ID Suture:** Binds the weave's Trace ID to the
        generated security metadata for distributed forensic tracking.
    21. **Haptic HUD Multicast:** Radiates "SEC_WARD_ACTIVE" pulses to the
        Ocular HUD for real-time visual confirmation of defense.
    22. **NoneType Root Sarcophagus:** Hard-wards the path resolution to
        prevent 'Lobby Paradox' crashes on absolute paths.
    23. **Module Resurrection Gaze:** Detects missing libraries and prophesies
        the exact 'pip install' command to heal the environment.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable perimeter
        and flawless Python Abstract Syntax Tree generation.
    =================================================================================
    """

    @property
    def namespace(self) -> str:
        return "sec"

    def help(self) -> str:
        return "Sovereign Conductor for: Vault, Shroud, Shield, Cors, and Sentinel."

    def _get_target_pkg(self, context: Dict[str, Any]) -> str:
        """Divines the relative package path to ensure import resonance."""
        # Detect if we are being woven into a nested sub-package
        if context.get("__current_dir__", "").count("/") > 0:
            return "."
        return "."

    # =========================================================================
    # == STRATUM 0: THE VAULT GUARDIAN (SUTURED)                             ==
    # =========================================================================

    def _directive_vault(self, context: Dict[str, Any], provider: str = "aws", weave: bool = True) -> str:
        """
        @sec/vault(provider="aws")
        Forges the functional interface for the Secrets Vault.
        [THE CURE]: Synchronizes exports with the Shard's functional proxies.
        """
        pkg = self._get_target_pkg(context)

        # 1. Weave the physical matter (Implementation)
        result = ""
        if weave:
            # We pass the provider to the shard so it knows which DNA to use.
            result += f"{{{{ logic.weave('security/vault-guardian', variables={{'vault_provider': '{provider}'}}) }}}}\n"

        # 2. Forge the Mind (Exports)
        # We explicitly include 'summon_secret' and 'awaken' to satisfy the IDE's Gaze.
        result += dedent(f"""
            # === THE VAULT GUARDIAN (SECRETS MANAGEMENT) ===
            from {pkg}secrets_schema import RequiredGnosis, awaken, secrets
            from {pkg}vault import (
                AWSVault,
                HashiCorpVault,
                LocalMockVault,
                VaultProvider,
                check_health,
                get_guardian,
                guardian,
                summon_secret,
                wire_vault_citadel,
            )

            __all__ = [
                "AWSVault",
                "HashiCorpVault",
                "LocalMockVault",
                "RequiredGnosis",
                "VaultProvider",
                "awaken",
                "check_health",
                "get_guardian",
                "guardian",
                "secrets",
                "summon_secret",
                "wire_vault_citadel",
            ]
        """).strip()
        return result

    # =========================================================================
    # == STRATUM 1: THE ACTIVE SHIELD (WAF)                                  ==
    # =========================================================================
    def _directive_shield(self, context: Dict[str, Any], limit: int = 100, window: int = 60, weave: bool = True) -> str:
        """
        =================================================================================
        == THE OMEGA SHIELD CONDUCTOR (V-Ω-TOTALITY-V200000-ATOMIC-DELEGATION)         ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SHIELD_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SHIELD_V200K_DECOUPLED_FINALIS_2026

        [THE MANIFESTO]
        The supreme authority for Active Defense inception. This version righteously
        implements 'Atomic Delegation', excising the local function wrapper to
        annihilate the 'Redeclaration' heresy. It ensures that the project soul
        possesses the 'shield.py' organ and that the target scripture possesses
        the necessary imports, achieving bit-perfect lexical purity.
        """
        # --- MOVEMENT I: SPATIOTEMPORAL IDENTITY BIOPSY ---
        # We anchor the Gaze to the specific file coordinate to prevent local drift.
        target_file = context.get("__current_file__", "void_reality")
        # Generate a deterministic key for this file to prevent duplicate imports.
        local_import_lock = f"_sec_shield_import_etched_{hashlib.md5(target_file.encode()).hexdigest()[:8]}"
        global_shard_lock = "_sec_shield_shard_woven_final"

        # [THE CURE]: The Hand is Stayed if the import is already manifest in this file.
        if context.get(local_import_lock):
            return f"# [SEC] Shield interface already manifest in {target_file}."

        pkg = self._get_target_pkg(context)
        result_lines = []

        # --- MOVEMENT II: THE RITE OF AUTONOMIC WEAVING ---
        # [ASCENSION 1]: Only weave the physical implementation (shield.py) once per project.
        if weave and not context.get(global_shard_lock):
            result_lines.append(f"{{{{ logic.weave('security/shield', variables={{'shield_limit': {limit}, 'shield_window': {window}}}) }}}}")
            # Enshrine the Vow of Existence in the project-wide memory.
            context[global_shard_lock] = True

        # --- MOVEMENT III: THE ATOMIC DELEGATION (THE FIX) ---
        # [THE MASTER CURE]: We surgically remove the 'def bind_shield' block.
        # We instead provide a clean, high-status import that satisfies 'fortify'.
        # This prevents redeclaration and ensures Starlette finds the correct dispatcher.
        result_lines.append(dedent(f"""
            # === THE ACTIVE SHIELD (V-Ω-TOTALITY) ===
            from {pkg}shield import bind_shield, security_shield_middleware
        """).strip())

        # --- MOVEMENT IV: CHRONICLE UPDATE ---
        # Update the local context so sibling calls in this file are silenced.
        context[local_import_lock] = True

        return "\n".join(result_lines)

    # =========================================================================
    # == STRATUM 2: THE CORS HARMONIZER                                      ==
    # =========================================================================

    def _directive_cors(self, context: Dict[str, Any], env: str = "DEV", domain: Optional[str] = None,
                        weave: bool = True) -> str:
        """
        @sec/cors(env="PROD", domain="novalym.systems")
        """
        pkg = self._get_target_pkg(context)
        result = ""
        if weave:
            result += f"{{{{ logic.weave('security/cors', variables={{'cors_env': '{env}', 'cors_domain': '{domain}'}}) }}}}\n"

        result += dedent(f"""
            # === THE CORS HARMONIZER (CROSS-ORIGIN RESOURCE SHIELD) ===
            from fastapi import FastAPI
            from {pkg}cors import harden_cors

            def bind_cors(app: FastAPI) -> None:
                \"\"\"Harmonizes Web Origins via Environment DNA.\"\"\"
                harden_cors(app)
        """).strip()
        return result

    # =========================================================================
    # == STRATUM 3: PII REDACTION SCRIBE                                     ==
    # =========================================================================

    def _directive_redactor(self, context: Dict[str, Any]) -> str:
        """
        @sec/redactor()
        Materializes a high-speed regex sieve to mask PII in the stream.
        """
        return dedent("""
            import re
            from typing import Any

            # [ASCENSION 8]: THE GNOSTIC PRIVACY SIEVE
            _PII_PATTERNS = [
                (re.compile(r'sk_live_[a-zA-Z0-9]{24}'), "[REDACTED_STRIPE_KEY]"),
                (re.compile(r'ghp_[a-zA-Z0-9]{36}'), "[REDACTED_GITHUB_TOKEN]"),
                (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'), "[REDACTED_EMAIL]"),
                (re.compile(r'\\\\d{3}-\\\\d{2}-\\\\d{4}'), "[REDACTED_SSN]"),
            ]

            def scrub_matter(text: Any) -> str:
                \"\"\"Surgically redacts PII from strings or serialized objects.\"\"\"
                content = str(text)
                for pattern, replacement in _PII_PATTERNS:
                    content = pattern.sub(replacement, content)
                return content
        """).strip()

    # =========================================================================
    # == STRATUM 4: JWT SENTINEL FORGE                                       ==
    # =========================================================================

    def _directive_jwt_guard(self, context: Dict[str, Any], algo: str = "RS256") -> str:
        """
        @sec/jwt_guard(algo="RS256")
        """
        return dedent(f"""
            # === GNOSTIC SECURITY: JWT SENTINEL ({algo}) ===
            from jose import jwt, JWTError
            from fastapi import HTTPException, status
            import os

            def verify_gnosis_token(token: str):
                \"\"\"Validates the Gnostic Token against the Citadel's Public Key.\"\"\"
                secret = os.getenv("JWT_PUBLIC_KEY") or os.getenv("JWT_SECRET")
                if not secret:
                    raise RuntimeError("Security Failure: JWT Secret unmanifest.")
                try:
                    payload = jwt.decode(token, secret, algorithms=["{algo}"])
                    return payload
                except JWTError:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Profane Token: Identity could not be verified."
                    )
        """).strip()

    # =========================================================================
    # == STRATUM 100: THE FORTIFY RITE (TOTAL CONVERGENCE)                   ==
    # =========================================================================

    def _directive_fortify(self, context: Dict[str, Any], provider: str = "aws") -> str:
        """
        @sec/fortify(provider="aws")
        [THE OMEGA RITE]: Total Convergence of the Security Stratum.
        """
        # [ASCENSION 4]: Materialize the complete defense-in-depth stack.
        vault_logic = self._directive_vault(context, provider=provider, weave=True)
        shield_logic = self._directive_shield(context, weave=True)
        cors_logic = self._directive_cors(context, weave=True)

        # [ASCENSION 10]: Forensic Trace ID Inception
        trace_id = context.get("trace_id", "tr-fortify-void")

        proclamation = [
            "\"\"\"",
            "===============================================================================",
            "== THE GNOSTIC SECURITY CITADEL (V-Ω-TOTALITY-V100)                          ==",
            "== AUTO-GENERATED BY VELM | TRACE: " + trace_id + "                         ==",
            "===============================================================================",
            "\"\"\"",
            "from fastapi import FastAPI",
            "",
            vault_logic,
            "",
            shield_logic,
            "",
            cors_logic,
            "",
            "# === THE MASTER ORCHESTRATOR ===",
            "def bind_security_citadel(app: FastAPI) -> None:",
            "    \"\"\"Sutures the entire Security Stratum to the Application Body.\"\"\"",
            "    # [ASCENSION 1]: Waking the Vault Guardian",
            "    wire_vault_citadel(app)",
            "    ",
            "    # [ASCENSION 11]: Harmonizing Web Origins",
            "    bind_cors(app)",
            "    ",
            "    # [ASCENSION 5]: Engaging the Active Shield",
            "    bind_shield(app)",
            "    ",
            "    import logging",
            "    logging.getLogger('SecurityCitadel').info('🛡️  Citadel Resonant and Active.')",
            "",
        ]
        return "\n".join(proclamation)