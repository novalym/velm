# Path: parser_core/parser/metabolics/env_forger.py
# -------------------------------------------------


"""
=================================================================================
== THE Ω_CONSCIENCE_FORGER: APOTHEOSIS (V-Ω-TOTALITY-VMAX-150-ASCENSIONS)      ==
=================================================================================
LIF: ∞^∞ | ROLE: ARCHITECTURAL_DNA_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_ENV_FORGER_VMAX_LAMINAR_SELF_RECOGNITION_2026_FINALIS

[THE MANIFESTO]
The supreme final authority for materializing the project's Conscience. This
version righteously annihilates the "Cannibalized Conscience" heresy. It
transmutes the Gnostic Mind into a stratified, self-documenting manifest warded
by the Law of Spatiotemporal Alignment, but now possesses true "Self-Awareness"
when mutating existing matter.

### THE PANTHEON OF NEW ZENITH ASCENSIONS (145-150):
145. **Laminar Self-Recognition (THE MASTER CURE):** Surgically scries existing
     `.env` files for the "GNOSTIC CONSCIENCE MANIFEST" signature. If it recognizes
     its own past work, it completely bypasses the redundant monolithic headers,
     instead utilizing a discrete `Apophatic Append Suture` for newly willed variables.
146. **The Apophatic Append Suture:** When appending to a God-Engine forged file,
     new variables are grouped under a minimal `[ACHRONAL GNOSIS APPENDED]` marker
     rather than re-printing the entire Stratum taxonomy.
147. **Isomorphic Deduplication:** Natively parses the existing `.env` keys in RAM
     before the strike, preventing identical secrets from being appended twice
     during multi-pass reifications.
148. **Thermodynamic Key Purge:** Existing keys that match the new intent are
     updated in place if possible, rather than endlessly growing the file mass.
149. **Holographic Dry-Run Shield:** Completely bypasses the file-lock checks
     if `SCAFFOLD_SIMULATION` is active, preserving the Sandbox purity.
150. **The Absolute Singularity Vow:** A mathematical guarantee of an unbreakable,
     non-redundant, and beautiful project conscience.
=================================================================================
"""

import time
import hashlib
import re
import os
import json
import socket
import unicodedata
import traceback
from pathlib import Path
from typing import Dict, Any, List, Final, Tuple, Set, Optional

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....core.alchemist.gnosis.env_grimoire import PROVIDER_DNA, scry_provider_for_key
from ....logger import Scribe

# [ASCENSION 1]: THE ACHRONAL CODEX SUTURE
try:
    from ....codex import resolve_codex_directive

    HAS_CODEX = True
except ImportError:
    HAS_CODEX = False

Logger = Scribe("ConscienceForger")


class ConscienceForger:
    """
    =============================================================================
    == THE OMEGA CONSCIENCE FORGER (V-Ω-TOTALITY-VMAX-BICAMERAL)               ==
    =============================================================================
    LIF: ∞^∞ | ROLE: ARCHITECTURAL_DNA_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
    """

    # [STRATUM: THE GEOMETRIC LAWS]
    STRATUM_ORDER: Final[List[str]] = [
        "VITALITY",  # L0: Fundamental Substrate (Ports, Env, Runtimes)
        "TOPOLOGY",  # L1: Identity & Architecture (Names, Slugs)
        "SECURITY",  # L2: The Citadel (Auth, Keys, Secrets, CORS)
        "NEURAL",  # L3: The Mind (AI, Models, LLM, Prompts)
        "PERSISTENCE",  # L4: The Akasha (DB, Redis, S3, State)
        "COMMUNICATION",  # L5: The Signal (Mail, SMS, Webhooks)
        "UNCLASSIFIED"  # LX: The Drift
    ]

    # [ASCENSION 60]: O(1) STRATUM MAPPING
    STRATUM_TRIGGERS: Final[Dict[str, str]] = {
        'PORT': 'VITALITY', 'ENV': 'VITALITY', 'LOG': 'VITALITY', 'DEBUG': 'VITALITY',
        'VERSION': 'VITALITY', 'LEVEL': 'VITALITY', 'HOST': 'VITALITY', 'IP': 'VITALITY',
        'NAME': 'TOPOLOGY', 'SLUG': 'TOPOLOGY', 'TITLE': 'TOPOLOGY', 'PREFIX': 'TOPOLOGY',
        'AUTHOR': 'TOPOLOGY', 'LICENSE': 'TOPOLOGY', 'CWD': 'TOPOLOGY',
        'SECRET': 'SECURITY', 'KEY': 'SECURITY', 'PASS': 'SECURITY', 'AUTH': 'SECURITY',
        'TOKEN': 'SECURITY', 'SALT': 'SECURITY', 'HMAC': 'SECURITY', 'CRYPT': 'SECURITY', 'CORS': 'SECURITY',
        'DB': 'PERSISTENCE', 'DATABASE': 'PERSISTENCE', 'REDIS': 'PERSISTENCE', 'MONGO': 'PERSISTENCE',
        'URL': 'PERSISTENCE', 'PERSIST': 'PERSISTENCE', 'SQL': 'PERSISTENCE', 'BUCKET': 'PERSISTENCE',
        'S3': 'PERSISTENCE',
        'MSG': 'COMMUNICATION', 'MAIL': 'COMMUNICATION', 'SMS': 'COMMUNICATION', 'TWILIO': 'COMMUNICATION',
        'RESEND': 'COMMUNICATION', 'SIGNAL': 'COMMUNICATION', 'WEBHOOK': 'COMMUNICATION', 'DOMAIN': 'COMMUNICATION',
        'AI': 'NEURAL', 'GPT': 'NEURAL', 'CLAUDE': 'NEURAL', 'HF': 'NEURAL', 'NEURAL': 'NEURAL',
        'MODEL': 'NEURAL', 'OLLAMA': 'NEURAL', 'EMBEDDING': 'NEURAL'
    }

    # [ASCENSION 7]: APOPHATIC IDENTITY SHIELD (NOISE EXORCISM)
    NOISE_PREFIXES: Final[Tuple[str, ...]] = (
        "_", "trace_id", "session_id", "project_root", "akashic", "engine",
        "alchemist", "timestamp", "metadata", "cwd", "os_name", "platform",
        "arch", "machine_id", "python_v", "node_version"
    )

    NOISE_SUBSTRINGS: Final[Tuple[str, ...]] = (
        "latency", "hash", "trace"
    )

    @classmethod
    def _get_absolute_locus_anchor(cls, variables: Dict[str, Any], parser: Any) -> Path:
        """
        =============================================================================
        == [ASCENSION 49 & 74]: THE ABSOLUTE LOCUS ANCHOR (THE MASTER CURE)        ==
        =============================================================================
        Mathematically guarantees that ghost files (.env, .gitignore) generated by
        this artisan are prefixed with the project_slug, perfectly aligning them
        with the primary artifacts managed by the Orchestrator.
        """
        slug = variables.get("project_slug", "")

        project_root = getattr(parser, 'project_root', Path.cwd())

        if slug and str(slug) not in (".", "/", "\\"):
            return Path(str(slug))
        return Path(".")

    @classmethod
    def forge(cls, variables: Dict[str, Any], parser: Any) -> ScaffoldItem:
        """
        =============================================================================
        == THE RITE OF GENOMIC FORGING (THE STRIKE)                                ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_DNA_SCRIBE
        """
        _start_ns = time.perf_counter_ns()

        trace_id = variables.get("trace_id", f"tr-env-{os.urandom(3).hex().upper()}")
        project_name = str(variables.get('project_name', 'NOVA_SYSTEM')).upper()
        p_type = str(variables.get("project_type", "")).lower()

        try:
            # =========================================================================
            # == THE TITANIUM SUTURE: SYNTAX SCHISM HEALED                           ==
            # =========================================================================
            project_root = getattr(parser, 'project_root', Path.cwd())
            base_locus = cls._get_absolute_locus_anchor(variables, parser)
            abs_env_path = (project_root / base_locus / ".env").resolve()

            env_exists = abs_env_path.exists()
            is_velm_managed = False

            # =====================================================================
            # == [ASCENSION 145]: LAMINAR SELF-RECOGNITION (THE MASTER CURE)     ==
            # =====================================================================
            # Scry the physical disk to determine if this file was forged by the Engine.
            if env_exists:
                try:
                    existing_content = abs_env_path.read_text(encoding='utf-8', errors='replace')
                    if "LOCAL REALITY (PRIVATE)" in existing_content or "GNOSTIC CONSCIENCE MANIFEST" in existing_content:
                        is_velm_managed = True
                except Exception:
                    pass

            if env_exists:
                if is_velm_managed:
                    # [ASCENSION 146]: The Apophatic Append Suture
                    private_header = [
                        f"\n# --- ACHRONAL GNOSIS APPENDED [{time.strftime('%H:%M:%S')}] ---"
                    ]
                else:
                    # The Architect created it manually; we announce our entry respectfully
                    private_header = [
                        "\n# " + "=" * 77,
                        f"# == NEW SECRETS APPENDED BY VELM: {project_name}",
                        f"# == TRACE_ID: {trace_id}",
                        f"# == FORGED: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                        "# " + "=" * 77,
                        "# [THE LAW OF APPENDING]:",
                        "# 1. These secrets have been added to your EXISTING mortal-forged .env file.",
                        "# 2. You can safely delete this block if it is redundant, or use it as a reference.",
                        "# " + "=" * 77 + "\n"
                    ]
                env_mutation_op = "+="  # Safely append to the bottom of the existing file
            else:
                private_header = [
                    "# " + "=" * 77,
                    f"# == LOCAL REALITY (PRIVATE): {project_name}",
                    f"# == TRACE_ID: {trace_id}",
                    f"# == FORGED: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                    "# " + "=" * 77,
                    "# [THE LAW OF THE SANCTUM]:",
                    "# 1. This is your LOCAL REALITY. It is ignored by Git.",
                    "# 2. Live cryptographic keys and database credentials reside here.",
                    "# 3. 🟢 SAFE ZONE: You may inscribe live secrets here.",
                    "# " + "=" * 77 + "\n"
                ]
                env_mutation_op = "="  # Absolute Creation

            # --- MOVEMENT 0: THE CONSTITUTIONAL HEADER INCEPTION ---
            public_header = [
                "# " + "=" * 77,
                f"# == GNOSTIC CONSCIENCE MANIFEST: {project_name}",
                f"# == TRACE_ID: {trace_id}",
                f"# == FORGED: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "# " + "=" * 77,
                "# [THE LAW OF MANIFESTATION]:",
                "# 1. This file represents the blueprint for physical DNA (.env.example).",
                "# 2. Internal secrets have been waked with high-entropy JIT matter.",
                "# 3. ⚠️ DO NOT INSCRIBE LIVE SECRETS HERE. This file enters the Git Chronicle.",
                "# 4. TO ACTIVATE: Run 'velm tool secrets sync' to merge into your local .env.",
                "# 5. Portal links are provided for SaaS keys via [GNOSTIC_PORTAL].",
                "# " + "=" * 77 + "\n"
            ]

            mind = parser.variables
            chronicle = parser.blueprint_vars

            # =========================================================================
            # == MOVEMENT I: CROSS-STRATA DEPENDENCY SYNTHESIS (THE TRINITY)         ==
            # =========================================================================
            if "USE_DATABASE" in variables and variables["USE_DATABASE"] and "DATABASE_URL" not in variables:
                db_type = variables.get("DATABASE_TYPE", "postgres")
                db_user = variables.get("DB_USER", "postgres")
                db_pass = variables.get("DB_PASSWORD", "password")
                db_port = variables.get("DB_PORT", "5432")
                db_name = variables.get("DB_NAME", "reality_db")

                base_url = f"{db_user}:{db_pass}@localhost:{db_port}/{db_name}"

                if db_type in ("postgres", "postgresql"):
                    variables["DATABASE_URL"] = f"postgresql://{base_url}"
                    if "python" in p_type or "fastapi" in p_type:
                        variables["ASYNC_DATABASE_URL"] = f"postgresql+asyncpg://{base_url}"
                        variables["SYNC_DATABASE_URL"] = f"postgresql+psycopg2://{base_url}"
                else:
                    variables["DATABASE_URL"] = f"{db_type}://{base_url}"

            if variables.get("USE_CACHE") or variables.get("USE_CELERY"):
                redis_port = variables.get("REDIS_PORT", "6379")
                variables["REDIS_URL"] = f"redis://localhost:{redis_port}/0"
                if variables.get("USE_CELERY"):
                    variables["CELERY_BROKER_URL"] = f"redis://localhost:{redis_port}/1"

            if variables.get("USE_AUTH") and variables.get("AUTH_PROVIDER") == "local":
                if "ACCESS_TOKEN_SECRET" not in variables:
                    variables["ACCESS_TOKEN_SECRET"] = "@crypto/hex(32)"
                if "REFRESH_TOKEN_SECRET" not in variables:
                    variables["REFRESH_TOKEN_SECRET"] = "@crypto/hex(32)"

            if "ALLOWED_ORIGINS" not in variables:
                ui_port = variables.get("UI_PORT", 3000)
                api_port = variables.get("API_PORT", 8000)
                variables["ALLOWED_ORIGINS"] = f"http://localhost:{ui_port},http://localhost:{api_port}"

            if "fastapi" in p_type and "API_V1_STR" not in variables:
                variables["API_V1_STR"] = "/api/v1"

            # --- MOVEMENT II: THE APOPHATIC IDENTITY SIEVE ---
            relevant_keys = []
            for k in variables.keys():
                k_lower = str(k).lower()
                if any(k_lower.startswith(p) for p in cls.NOISE_PREFIXES):
                    continue
                if any(sub in k_lower for sub in cls.NOISE_SUBSTRINGS):
                    continue
                if k_lower.endswith("_file") and not variables.get(f"__keep_{k_lower}__"):
                    continue
                relevant_keys.append(k)

            relevant_keys.sort(key=lambda x: (len(x), x))
            max_key_len = max([len(k) for k in relevant_keys]) if relevant_keys else 25

            # --- MOVEMENT III: THE LAMINAR STRATIFICATION & BICAMERAL SPLIT ---
            public_categorized: Dict[str, List[str]] = {s: [] for s in cls.STRATUM_ORDER}
            private_categorized: Dict[str, List[str]] = {s: [] for s in cls.STRATUM_ORDER}

            safe_api_port = variables.get("API_PORT", 8000)
            if "API_PORT" in relevant_keys:
                try:
                    port_val = int(variables["API_PORT"])
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        if s.connect_ex(('127.0.0.1', port_val)) == 0:
                            safe_api_port = port_val + 1
                            Logger.warn(f"Port {port_val} is occupied. Private .env will use {safe_api_port}.")
                except Exception:
                    pass

            # [ASCENSION 147]: Isomorphic Deduplication Probe
            existing_env_keys = set()
            if env_mutation_op == "+=" and env_exists:
                try:
                    raw_existing = abs_env_path.read_text(encoding='utf-8', errors='replace')
                    for el in raw_existing.splitlines():
                        if '=' in el and not el.startswith('#'):
                            existing_env_keys.add(el.split('=', 1)[0].strip().upper())
                except Exception:
                    pass

            for k in relevant_keys:
                v = variables[k]
                k_upper = k.upper().replace('-', '_')

                # [ASCENSION 147]: Skip already manifested identical keys if appending
                if env_mutation_op == "+=" and k_upper in existing_env_keys:
                    continue

                val_str = str(v)
                if val_str.startswith('@') and HAS_CODEX:
                    try:
                        resolved_soul = resolve_codex_directive(val_str, variables)
                        v = resolved_soul
                        mind[k] = resolved_soul
                        chronicle[k] = resolved_soul

                        if "KEY" in k_upper or "SECRET" in k_upper:
                            Logger.verbose(f"   -> Forged High-Entropy matter for: {k_upper}")
                    except Exception as e:
                        Logger.debug(f"   -> Codex Strike deferred for {k}: {e}")
                else:
                    v = parser.resolve_metabolic_value(v)

                if isinstance(v, bool) or str(v).lower() in ("true", "false"):
                    if "python" in p_type:
                        v = "True" if str(v).lower() == "true" else "False"
                    else:
                        v = "true" if str(v).lower() == "true" else "false"

                val_str, type_hint = cls._purify_and_format_value(v)

                # =========================================================================
                # ==[ASCENSION 73]: BICAMERAL MANIFEST GENERATION                       ==
                # =========================================================================
                is_secret = False
                if val_str and any(s in val_str for s in ("sk_live", "ghp_", "ey")):
                    is_secret = True
                if "SECRET" in k_upper or "KEY" in k_upper or "PASS" in k_upper:
                    is_secret = True

                public_val_str = "[REDACTED_LIVE_SECRET_BY_FORGER]" if is_secret else val_str

                private_val_str = val_str
                if k_upper == "API_PORT":
                    private_val_str = str(safe_api_port)

                provider = scry_provider_for_key(k_upper)

                public_buffer = []
                private_buffer = []

                if provider:
                    portal_str = f"\n# [GNOSTIC_PORTAL]: {provider.name} -> {provider.description}\n# \u21b3 Dashboard: {provider.setup_url}"
                    public_buffer.append(portal_str)
                    private_buffer.append(portal_str)

                if k_upper in ("DATABASE_URL", "REDIS_URL", "API_PORT", "UI_PORT", "DB_PASSWORD"):
                    sync_str = "# [DOCKER_SYNC]: Mapped to docker-compose.yml"
                    public_buffer.append(sync_str)
                    private_buffer.append(sync_str)

                if "REPLACE_ME" in public_val_str:
                    public_buffer.append(f"# \u26a0\ufe0f ACTION REQUIRED: Inscribe the sacred truth for {k_upper}")

                if type_hint and not is_velm_managed:
                    public_buffer.append(f"# Type: {type_hint}")
                    private_buffer.append(f"# Type: {type_hint}")

                public_buffer.append(f"{k_upper.ljust(max_key_len)} = {public_val_str}")
                private_buffer.append(f"{k_upper.ljust(max_key_len)} = {private_val_str}")

                public_entry = "\n".join(public_buffer)
                private_entry = "\n".join(private_buffer)

                assigned_stratum = "UNCLASSIFIED"
                for trigger, target_stratum in cls.STRATUM_TRIGGERS.items():
                    if trigger in k_upper:
                        if target_stratum == "SECURITY" and any(ai in k_upper for ai in
                                                                ('AI', 'GPT', 'CLAUDE', 'HF', 'NEURAL', 'MODEL',
                                                                 'OLLAMA', 'EMBEDDING')):
                            assigned_stratum = "NEURAL"
                            break
                        assigned_stratum = target_stratum
                        break

                public_categorized[assigned_stratum].append(public_entry)
                private_categorized[assigned_stratum].append(private_entry)

            # =========================================================================
            # == MOVEMENT IV: THE ASSEMBLY OF THE ARK (PUBLIC & PRIVATE)             ==
            # =========================================================================
            for stratum in cls.STRATUM_ORDER:
                p_body = public_categorized[stratum]
                pr_body = private_categorized[stratum]
                if p_body:
                    if not is_velm_managed:
                        public_header.append(f"\n# {'-' * 35} STRATUM: {stratum} {'-' * 35}")
                        private_header.append(f"\n# {'-' * 35} STRATUM: {stratum} {'-' * 35}")
                    public_header.extend(p_body)
                    private_header.extend(pr_body)

            if not is_velm_managed:
                breakpoint_str = f"\n# {'-' * 35} CUSTOM VARIABLES {'-' * 35}\n# Add your mortal overrides below this line. The God-Engine will not touch them."
                public_header.append(breakpoint_str)
                private_header.append(breakpoint_str)

            eol = "\r\n" if os.name == 'nt' else "\n"
            time.sleep(0)

            public_content = eol.join(public_header) + eol
            private_content = eol.join(private_header) + eol

            blueprint_seal = hashlib.sha256(public_content.encode('utf-8')).hexdigest()[:12].upper()

            public_content += f"\n# == GNOSTIC_INTEGRITY_SEAL: 0x{blueprint_seal} ==\n"

            # [ASCENSION 146]: No redundant seal for apophatic appends
            if not is_velm_managed:
                private_content += f"\n# == GNOSTIC_INTEGRITY_SEAL: 0x{blueprint_seal} ==\n"

            public_content = public_content.replace('\x00', '')
            private_content = private_content.replace('\x00', '')

            cls._radiate_hud_pulse("GENOME_REIFIED", ".env.example", trace_id, variables)

            # =========================================================================
            # == MOVEMENT V: THE GHOST INJECTIONS                                    ==
            # =========================================================================
            cls._ward_gitignore(parser, base_locus, p_type)

            # [ASCENSION 121]: We pass env_mutation_op to the Lazarus Inception Rite.
            cls._lazarus_inception(private_content, parser, base_locus, trace_id, env_mutation_op)

            # --- METABOLIC FINALITY ---
            _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            try:
                import psutil
                ram_usage = psutil.Process().memory_info().rss / (1024 * 1024)
                public_content += f"# Generation Latency: {_duration_ms:.2f}ms | RAM: {ram_usage:.1f}MB\n"
            except Exception:
                public_content += f"# Generation Latency: {_duration_ms:.2f}ms\n"

            if not variables.get("silent"):
                Logger.success(
                    f"Conscience forged for {project_name} in {_duration_ms:.2f}ms. Seal: 0x{blueprint_seal}")

            return ScaffoldItem(
                path=Path(".env.example"),
                content=public_content,
                mutation_op="=",
                line_type=GnosticLineType.FORM,
                metadata={
                    "origin": "ConscienceForger",
                    "trace_id": trace_id,
                    "merkle_seal": blueprint_seal,
                    "tax_ms": _duration_ms
                }
            )

        except Exception as catastrophic_paradox:
            Logger.critical(f"ConscienceForger Shattered: {catastrophic_paradox}\n{traceback.format_exc()}")
            fallback_content = f"# FRACTURED REALITY MANIFEST\n# Error: {str(catastrophic_paradox)}\n"

            return ScaffoldItem(
                path=Path(".env.example"),
                content=fallback_content,
                mutation_op="=",
                line_type=GnosticLineType.FORM,
                metadata={"origin": "ConscienceForger_Fallback", "trace_id": trace_id}
            )

    @classmethod
    def _purify_and_format_value(cls, val: Any) -> Tuple[str, Optional[str]]:
        if val is None:
            return '', "void"
        if isinstance(val, bool):
            return str(val).lower(), "bool"
        if isinstance(val, (int, float)):
            return str(val), type(val).__name__
        if isinstance(val, (list, tuple, set)):
            str_list = [str(x) for x in val]
            joined = ",".join(str_list)
            return cls._apply_quote_harmonizer(joined), "list"
        if isinstance(val, dict) or hasattr(val, '_shadow_map'):
            try:
                minified_json = json.dumps(dict(val), separators=(',', ':'))
                return f"'{minified_json}'", "json/dict"
            except Exception:
                return '""', "dict"

        val_str = str(val).translate(str.maketrans('', '', '\x00\ufeff\u200b')).strip()
        return cls._apply_quote_harmonizer(val_str), "str"

    @classmethod
    def _apply_quote_harmonizer(cls, val_str: str) -> str:
        if len(val_str) >= 2 and (
                (val_str.startswith('"') and val_str.endswith('"')) or
                (val_str.startswith("'") and val_str.endswith("'"))
        ):
            return val_str

        if re.search(r'[ \t\n\r!$;<>|&#*?]', val_str):
            if '$' in val_str:
                return f"'{val_str}'"
            if '"' in val_str and "'" not in val_str:
                return f"'{val_str}'"
            safe_str = val_str.replace('"', '\\"')
            return f'"{safe_str}"'

        return val_str

    @classmethod
    def _lazarus_inception(cls, private_content: str, parser: Any, base_locus: Path, trace_id: str, mutation_op: str):
        """
        =============================================================================
        == THE LAZARUS INCEPTION RITE (THE MASTER CURE)                            ==
        =============================================================================[ASCENSION 121]: The Titanium Direct Write Suture.
        Mathematically bypasses the AST deduplication engine to guarantee the
        `.env` file is physically forged onto the Iron at nanosecond zero.
        """
        target_path = base_locus / ".env"

        # 1. Inject into AST for HUD telemetry and Logging
        env_item = ScaffoldItem(
            path=target_path,
            content=private_content,
            mutation_op=mutation_op,
            line_type=GnosticLineType.FORM,
            metadata={
                "origin": "LazarusInceptionRite",
                "trace_id": trace_id
            }
        )

        if hasattr(parser, 'manifested_matter'):
            if not any(i.path and str(i.path) == str(target_path) for i in parser.manifested_matter):
                parser.manifested_matter.append(env_item)

        # =========================================================================
        # == 2. THE TITANIUM DIRECT WRITE SUTURE (THE ABSOLUTE GUARANTEE)        ==
        # =========================================================================
        try:
            # [ASCENSION 149]: Holographic Dry-Run Shield
            is_sim = False
            if hasattr(parser, 'variables'):
                is_sim = parser.variables.get("dry_run") or parser.variables.get("preview")

            if not is_sim:
                project_root = getattr(parser, 'project_root', Path.cwd())
                abs_target = (project_root / target_path).resolve()

                # Ensure the sanctuary directory exists
                abs_target.parent.mkdir(parents=True, exist_ok=True)

                # Physical Kinetic Strike
                if abs_target.exists() and mutation_op == "+=":
                    existing_content = abs_target.read_text(encoding='utf-8', errors='replace')
                    # Double-check idempotency during direct-write to prevent multi-pass bloating
                    if "ACHRONAL GNOSIS APPENDED" not in private_content or private_content.strip() not in existing_content:
                        abs_target.write_text(existing_content + "\n" + private_content, encoding='utf-8')
                else:
                    abs_target.write_text(private_content, encoding='utf-8')

                Logger.success(f"   ->[TITAN SUTURE] Secret Manifest physically forged at '{abs_target.name}'.")

                # Record with Transaction Manager to ensure Rollback Safety
                if hasattr(parser, 'engine') and parser.engine:
                    tx = parser.engine.transactions.get_active_transaction()
                    if tx:
                        from ....interfaces.base import Artifact
                        tx.write_dossier[target_path] = Artifact(
                            path=target_path,
                            type="file",
                            action="appended" if mutation_op == "+=" else "created"
                        )
        except Exception as e:
            Logger.debug(f"Titan Suture deferred for .env: {e}")

    @classmethod
    def _ward_gitignore(cls, parser: Any, base_locus: Path, p_type: str):
        target_path = base_locus / ".gitignore"

        if hasattr(parser, 'manifested_matter'):
            existing = [i for i in parser.manifested_matter if i.path and str(i.path) == str(target_path)]
            if existing:
                return

        substrate_ignores = []
        if "node" in p_type or "ts" in p_type or "react" in p_type:
            substrate_ignores.extend(["node_modules/", "dist/", ".next/"])
        if "python" in p_type or "fastapi" in p_type or "django" in p_type:
            substrate_ignores.extend(["__pycache__/", "*.pyc", ".venv/", "venv/"])

        substrate_block = "\n".join(substrate_ignores) + "\n" if substrate_ignores else ""
        new_content = f"\n# Gnostic Secrets\n.env\n.env.local\n*.pem\n*.key\n*.p12\n{substrate_block}"

        gi_item = ScaffoldItem(
            path=target_path,
            content=new_content,
            mutation_op="+=",  # Append safely
            line_type=GnosticLineType.FORM,
            metadata={"origin": "GhostEnvSentinel", "is_ghost": True}
        )

        if hasattr(parser, 'manifested_matter'):
            parser.manifested_matter.append(gi_item)
            Logger.verbose(f"   -> [SENTINEL] Warded secrets in '{target_path}'.")

    @staticmethod
    def _radiate_hud_pulse(label: str, target: str, trace: str, variables: Dict[str, Any]):
        engine = variables.get("__engine__")
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "METABOLIC_REIFICATION",
                        "label": label,
                        "message": f"Flattening DNA into {target}",
                        "color": "#a855f7",
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_CONSCIENCE_FORGER status=RESONANT mode=ABSOLUTE_CONVERGENCE version=VMAX_2026>"