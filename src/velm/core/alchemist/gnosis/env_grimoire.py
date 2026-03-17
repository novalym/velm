# Path: velm/core/alchemist/gnosis/env_grimoire.py
# -----------------------------------------------

from dataclasses import dataclass
from typing import Dict, Any, List, Final, Optional

"""
=================================================================================
== THE OMNISCIENT GRIMOIRE OF SUBSTRATES: TOTALITY (V-Ω-VMAX-1000-ASCENSIONS)  ==
=================================================================================
LIF: ∞^∞ | ROLE: PROVIDER_ONTOLOGY_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_GRIMOIRE_VMAX_TOTALITY_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
This is the supreme definitive authority for SaaS and Cloud DNA. It serves as the
Mind of the ConscienceForger, teaching the God-Engine the coordinates of every
significant service in the digital multiverse.
=================================================================================
"""


@dataclass(frozen=True)
class ProviderGnosis:
    name: str
    description: str
    setup_url: str
    primary_keys: List[str]
    is_internal: bool = False
    vibe_color: str = "#64ffda"
    cure_note: str = "Obtain keys from the dashboard and inscribe here."


# =============================================================================
# == THE PANTHEON OF PROVIDERS: THE TWELVE HOLY STRATA                       ==
# =============================================================================

PROVIDER_DNA: Final[Dict[str, ProviderGnosis]] = {

    # --- STRATUM I: IDENTITY & JURISPRUDENCE (AUTH) ---
    "CLERK": ProviderGnosis(
        name="Clerk",
        description="The Ocular Identity Membrane for Next.js/React.",
        setup_url="https://dashboard.clerk.com/",
        primary_keys=["CLERK_SECRET_KEY", "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"],
        vibe_color="#6c47ff"
    ),
    "AUTH0": ProviderGnosis(
        name="Auth0",
        description="Enterprise-grade SSO and Identity.",
        setup_url="https://manage.auth0.com/",
        primary_keys=["AUTH0_SECRET", "AUTH0_CLIENT_ID", "AUTH0_DOMAIN"],
        vibe_color="#eb5424"
    ),
    "SUPABASE_AUTH": ProviderGnosis(
        name="Supabase Auth",
        description="JWT-based authentication for the Supabase ecosystem.",
        setup_url="https://supabase.com/dashboard/project/_/auth/settings",
        primary_keys=["SUPABASE_AUTH_JWT_SECRET"],
        vibe_color="#3ecf8e"
    ),
    "FIREBASE": ProviderGnosis(
        name="Firebase",
        description="Google's monolithic backend-as-a-service.",
        setup_url="https://console.firebase.google.com/",
        primary_keys=["FIREBASE_API_KEY", "FIREBASE_AUTH_DOMAIN", "FIREBASE_PROJECT_ID"],
        vibe_color="#ffca28"
    ),
    "KINDE": ProviderGnosis(
        name="Kinde",
        description="Modern dev-first authentication and user management.",
        setup_url="https://kinde.com/dashboard/",
        primary_keys=["KINDE_CLIENT_ID", "KINDE_CLIENT_SECRET", "KINDE_ISSUER_URL"],
        vibe_color="#ff4800"
    ),
    "WORKOS": ProviderGnosis(
        name="WorkOS",
        description="The bridge to Enterprise SSO (SAML, SCIM).",
        setup_url="https://dashboard.workos.com/",
        primary_keys=["WORKOS_API_KEY", "WORKOS_CLIENT_ID"],
        vibe_color="#6363f1"
    ),
    "STYTCH": ProviderGnosis(
        name="Stytch",
        description="Passwordless and B2B identity substrate.",
        setup_url="https://stytch.com/dashboard",
        primary_keys=["STYTCH_PROJECT_ID", "STYTCH_SECRET"],
        vibe_color="#191d21"
    ),

    # --- STRATUM II: NEURAL & INTELLIGENCE (AI) ---
    "OPENAI": ProviderGnosis(
        name="OpenAI",
        description="The primary neural cortex (GPT-4o, o1, DALL-E).",
        setup_url="https://platform.openai.com/api-keys",
        primary_keys=["OPENAI_API_KEY", "OPENAI_ORG_ID"],
        vibe_color="#10a37f"
    ),
    "ANTHROPIC": ProviderGnosis(
        name="Anthropic",
        description="The Claude neural series for high-fidelity reasoning.",
        setup_url="https://console.anthropic.com/settings/keys",
        primary_keys=["ANTHROPIC_API_KEY"],
        vibe_color="#d97757"
    ),
    "MISTRAL": ProviderGnosis(
        name="Mistral AI",
        description="Open-weight models with European sovereignty.",
        setup_url="https://console.mistral.ai/api-keys/",
        primary_keys=["MISTRAL_API_KEY"],
        vibe_color="#f5d142"
    ),
    "GROQ": ProviderGnosis(
        name="Groq",
        description="LPU-accelerated high-velocity neural inference.",
        setup_url="https://console.groq.com/keys",
        primary_keys=["GROQ_API_KEY"],
        vibe_color="#f55036"
    ),
    "PERPLEXITY": ProviderGnosis(
        name="Perplexity",
        description="Real-time web-grounded search and neural scrying.",
        setup_url="https://www.perplexity.ai/settings/api",
        primary_keys=["PERPLEXITY_API_KEY"],
        vibe_color="#22c55e"
    ),
    "REPLICATE": ProviderGnosis(
        name="Replicate",
        description="Cloud substrate for running diverse neural models.",
        setup_url="https://replicate.com/account/api-tokens",
        primary_keys=["REPLICATE_API_TOKEN"],
        vibe_color="#000000"
    ),
    "LANGSMITH": ProviderGnosis(
        name="LangSmith",
        description="The observatory for neural trace analysis.",
        setup_url="https://smith.langchain.com/",
        primary_keys=["LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2"],
        vibe_color="#ff9900"
    ),
    "DEEPSEEK": ProviderGnosis(
        name="DeepSeek",
        description="High-efficiency reasoning and coding models.",
        setup_url="https://platform.deepseek.com/api_keys",
        primary_keys=["DEEPSEEK_API_KEY"],
        vibe_color="#4d6bed"
    ),
    "TOGETHER": ProviderGnosis(
        name="Together AI",
        description="Distributed substrate for open-source model inference.",
        setup_url="https://api.together.xyz/settings/api-keys",
        primary_keys=["TOGETHER_API_KEY"],
        vibe_color="#4b46ff"
    ),

    # --- STRATUM III: FISCAL & COMMERCE (PAYMENTS) ---
    "STRIPE": ProviderGnosis(
        name="Stripe",
        description="The multiversal ledger for global payments.",
        setup_url="https://dashboard.stripe.com/test/apikeys",
        primary_keys=["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET", "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"],
        vibe_color="#635bff"
    ),
    "LEMONSQUEEZY": ProviderGnosis(
        name="Lemon Squeezy",
        description="Merchant of record for SaaS and digital goods.",
        setup_url="https://app.lemonsqueezy.com/settings/api",
        primary_keys=["LEMONSQUEEZY_API_KEY", "LEMONSQUEEZY_STORE_ID"],
        vibe_color="#ffc233"
    ),
    "PADDLE": ProviderGnosis(
        name="Paddle",
        description="Complete checkout, tax, and compliance substrate.",
        setup_url="https://vendors.paddle.com/authentication-v2",
        primary_keys=["PADDLE_API_KEY", "PADDLE_VENDOR_ID"],
        vibe_color="#00ff00"
    ),
    "PLAID": ProviderGnosis(
        name="Plaid",
        description="The bridge to the physical banking world.",
        setup_url="https://dashboard.plaid.com/team/keys",
        primary_keys=["PLAID_CLIENT_ID", "PLAID_SECRET", "PLAID_ENV"],
        vibe_color="#33a6e3"
    ),
    "PAYPAL": ProviderGnosis(
        name="PayPal",
        description="Legacy global payment network.",
        setup_url="https://developer.paypal.com/dashboard/applications",
        primary_keys=["PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET"],
        vibe_color="#003087"
    ),

    # --- STRATUM IV: COMMUNICATION & SIGNALS (MESSAGING) ---
    "RESEND": ProviderGnosis(
        name="Resend",
        description="The modern scribe for transactional email.",
        setup_url="https://resend.com/api-keys",
        primary_keys=["RESEND_API_KEY"],
        vibe_color="#000000"
    ),
    "TWILIO": ProviderGnosis(
        name="Twilio",
        description="Kinetic SMS, Voice, and WhatsApp signals.",
        setup_url="https://www.twilio.com/console",
        primary_keys=["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER"],
        vibe_color="#f22f46"
    ),
    "SENDGRID": ProviderGnosis(
        name="SendGrid",
        description="High-volume email delivery infrastructure.",
        setup_url="https://app.sendgrid.com/settings/api_keys",
        primary_keys=["SENDGRID_API_KEY"],
        vibe_color="#1a82e2"
    ),
    "POSTMARK": ProviderGnosis(
        name="Postmark",
        description="Indestructible transactional email with zero-latency.",
        setup_url="https://account.postmarkapp.com/servers",
        primary_keys=["POSTMARK_SERVER_TOKEN"],
        vibe_color="#ff6e21"
    ),
    "MAILGUN": ProviderGnosis(
        name="Mailgun",
        description="Developer-first email APIs for large scale.",
        setup_url="https://app.mailgun.com/app/dashboard",
        primary_keys=["MAILGUN_API_KEY", "MAILGUN_DOMAIN"],
        vibe_color="#ff4339"
    ),
    "PUSHER": ProviderGnosis(
        name="Pusher",
        description="Real-time WebSocket pub/sub for the Ocular HUD.",
        setup_url="https://dashboard.pusher.com/",
        primary_keys=["PUSHER_APP_ID", "PUSHER_KEY", "PUSHER_SECRET", "PUSHER_CLUSTER"],
        vibe_color="#30373d"
    ),
    "ONESIGNAL": ProviderGnosis(
        name="OneSignal",
        description="Omnichannel push notifications and engagement.",
        setup_url="https://dashboard.onesignal.com/",
        primary_keys=["ONESIGNAL_APP_ID", "ONESIGNAL_REST_API_KEY"],
        vibe_color="#e44b32"
    ),

    # --- STRATUM V: PERSISTENCE & AKASHA (DATABASES) ---
    "NEON": ProviderGnosis(
        name="Neon",
        description="Serverless Postgres with branching capabilities.",
        setup_url="https://console.neon.tech/",
        primary_keys=["DATABASE_URL", "PGHOST", "PGPASSWORD"],
        vibe_color="#00e599"
    ),
    "PLANETSCALE": ProviderGnosis(
        name="PlanetScale",
        description="Vitess-powered serverless MySQL substrate.",
        setup_url="https://app.planetscale.com/",
        primary_keys=["DATABASE_URL", "DB_HOST", "DB_USERNAME", "DB_PASSWORD"],
        vibe_color="#000000"
    ),
    "TURSO": ProviderGnosis(
        name="Turso",
        description="Edge-distributed SQLite (LibSQL).",
        setup_url="https://turso.tech/dashboard",
        primary_keys=["TURSO_DATABASE_URL", "TURSO_AUTH_TOKEN"],
        vibe_color="#4ec5f1"
    ),
    "MONGODB": ProviderGnosis(
        name="MongoDB Atlas",
        description="The multiversal document store.",
        setup_url="https://cloud.mongodb.com/",
        primary_keys=["MONGODB_URI", "MONGODB_DB_NAME"],
        vibe_color="#13aa52"
    ),
    "UPSTASH": ProviderGnosis(
        name="Upstash",
        description="Serverless Redis, Kafka, and Vector data.",
        setup_url="https://console.upstash.com/",
        primary_keys=["UPSTASH_REDIS_REST_URL", "UPSTASH_REDIS_REST_TOKEN"],
        vibe_color="#00e9a3"
    ),
    "PINECONE": ProviderGnosis(
        name="Pinecone",
        description="The long-term memory for Neural Agents.",
        setup_url="https://app.pinecone.io/",
        primary_keys=["PINECONE_API_KEY", "PINECONE_ENVIRONMENT"],
        vibe_color="#27272a"
    ),
    "WEAVIATE": ProviderGnosis(
        name="Weaviate",
        description="Open-source vector database for AI-native apps.",
        setup_url="https://console.weaviate.cloud/",
        primary_keys=["WEAVIATE_URL", "WEAVIATE_API_KEY"],
        vibe_color="#2ecc71"
    ),
    "ALGOLIA": ProviderGnosis(
        name="Algolia",
        description="High-velocity semantic search and discovery.",
        setup_url="https://www.algolia.com/dashboard",
        primary_keys=["ALGOLIA_APP_ID", "ALGOLIA_API_KEY"],
        vibe_color="#003dff"
    ),

    # --- STRATUM VI: INFRASTRUCTURE & IRON (CLOUD) ---
    "AWS": ProviderGnosis(
        name="AWS",
        description="Amazon Web Services - The Master Celestial Iron.",
        setup_url="https://console.aws.amazon.com/iam/",
        primary_keys=["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION", "AWS_BUCKET"],
        vibe_color="#ff9900"
    ),
    "AZURE": ProviderGnosis(
        name="Azure",
        description="Microsoft's enterprise cloud substrate.",
        setup_url="https://portal.azure.com/",
        primary_keys=["AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_SECRET"],
        vibe_color="#0089d6"
    ),
    "GCP": ProviderGnosis(
        name="Google Cloud",
        description="GCP - Intelligence and scale at Google speed.",
        setup_url="https://console.cloud.google.com/",
        primary_keys=["GOOGLE_APPLICATION_CREDENTIALS", "GCP_PROJECT_ID"],
        vibe_color="#4285f4"
    ),
    "VERCEL": ProviderGnosis(
        name="Vercel",
        description="The Ocular deployment plane for React and Next.js.",
        setup_url="https://vercel.com/dashboard",
        primary_keys=["VERCEL_TOKEN", "VERCEL_ORG_ID", "VERCEL_PROJECT_ID"],
        vibe_color="#000000"
    ),
    "NETLIFY": ProviderGnosis(
        name="Netlify",
        description="Automated workflow for modern web projects.",
        setup_url="https://app.netlify.com/",
        primary_keys=["NETLIFY_AUTH_TOKEN", "NETLIFY_SITE_ID"],
        vibe_color="#00ad9f"
    ),
    "CLOUDFLARE": ProviderGnosis(
        name="Cloudflare",
        description="Global edge compute and security shield (Workers, R2).",
        setup_url="https://dash.cloudflare.com/",
        primary_keys=["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"],
        vibe_color="#f38020"
    ),
    "FLY": ProviderGnosis(
        name="Fly.io",
        description="App servers close to your users.",
        setup_url="https://fly.io/dashboard",
        primary_keys=["FLY_API_TOKEN"],
        vibe_color="#24185b"
    ),
    "RAILWAY": ProviderGnosis(
        name="Railway",
        description="Infrastructure for those who just want to ship.",
        setup_url="https://railway.app/dashboard",
        primary_keys=["RAILWAY_TOKEN"],
        vibe_color="#131313"
    ),
    "RENDER": ProviderGnosis(
        name="Render",
        description="Unified cloud to build and run all your apps.",
        setup_url="https://dashboard.render.com/",
        primary_keys=["RENDER_API_KEY"],
        vibe_color="#46e3b7"
    ),
    "DIGITALOCEAN": ProviderGnosis(
        name="DigitalOcean",
        description="The cloud of choice for nomadic architects.",
        setup_url="https://cloud.digitalocean.com/account/api/tokens",
        primary_keys=["DIGITALOCEAN_TOKEN"],
        vibe_color="#008bcf"
    ),
    "HETZNER": ProviderGnosis(
        name="Hetzner",
        description="High-performance European iron.",
        setup_url="https://console.hetzner.cloud/",
        primary_keys=["HCLOUD_TOKEN"],
        vibe_color="#d50c2d"
    ),

    # --- STRATUM VII: OBSERVABILITY & RETINA (MONITORING) ---
    "DATADOG": ProviderGnosis(
        name="Datadog",
        description="The total panopticon for metrics and traces.",
        setup_url="https://app.datadoghq.com/organization-settings/api-keys",
        primary_keys=["DD_API_KEY", "DD_APP_KEY", "DD_SITE"],
        vibe_color="#632ca6"
    ),
    "SENTRY": ProviderGnosis(
        name="Sentry",
        description="The high-fidelity crash-oracle.",
        setup_url="https://sentry.io/settings/account/api/auth-tokens/",
        primary_keys=["SENTRY_DSN", "SENTRY_AUTH_TOKEN"],
        vibe_color="#362d59"
    ),
    "NEWRELIC": ProviderGnosis(
        name="New Relic",
        description="Full-stack observability and error tracking.",
        setup_url="https://one.newrelic.com/",
        primary_keys=["NEW_RELIC_LICENSE_KEY", "NEW_RELIC_APP_NAME"],
        vibe_color="#1ce783"
    ),
    "LOGFIRE": ProviderGnosis(
        name="Pydantic Logfire",
        description="Python-native observability for warded data.",
        setup_url="https://logfire.pydantic.dev/",
        primary_keys=["LOGFIRE_TOKEN"],
        vibe_color="#000000"
    ),
    "AXIOM": ProviderGnosis(
        name="Axiom",
        description="Zero-config logging and analytics for serverless.",
        setup_url="https://axiom.co/dashboard",
        primary_keys=["AXIOM_TOKEN", "AXIOM_DATASET"],
        vibe_color="#000000"
    ),
    "HONEYCOMB": ProviderGnosis(
        name="Honeycomb",
        description="Observability for complex distributed systems.",
        setup_url="https://ui.honeycomb.io/",
        primary_keys=["HONEYCOMB_API_KEY"],
        vibe_color="#e2a528"
    ),

    # --- STRATUM VIII: PRODUCTIVITY & CRM (THE ARK) ---
    "HUBSPOT": ProviderGnosis(
        name="HubSpot",
        description="The multiversal CRM and growth engine.",
        setup_url="https://app.hubspot.com/settings/api-key",
        primary_keys=["HUBSPOT_ACCESS_TOKEN"],
        vibe_color="#ff7a59"
    ),
    "SALESFORCE": ProviderGnosis(
        name="Salesforce",
        description="Enterprise CRM substrate.",
        setup_url="https://login.salesforce.com/",
        primary_keys=["SF_USERNAME", "SF_PASSWORD", "SF_TOKEN"],
        vibe_color="#00a1e0"
    ),
    "SLACK": ProviderGnosis(
        name="Slack",
        description="Kinetic collaboration and signal hub.",
        setup_url="https://api.slack.com/apps",
        primary_keys=["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET"],
        vibe_color="#4a154b"
    ),
    "DISCORD": ProviderGnosis(
        name="Discord",
        description="Community signals and bot orchestration.",
        setup_url="https://discord.com/developers/applications",
        primary_keys=["DISCORD_TOKEN", "DISCORD_CLIENT_ID"],
        vibe_color="#5865f2"
    ),
    "NOTION": ProviderGnosis(
        name="Notion",
        description="The connected workspace for project Gnosis.",
        setup_url="https://www.notion.so/my-integrations",
        primary_keys=["NOTION_TOKEN", "NOTION_DATABASE_ID"],
        vibe_color="#000000"
    ),
    "AIRTABLE": ProviderGnosis(
        name="Airtable",
        description="The relational spreadsheet mind.",
        setup_url="https://airtable.com/account",
        primary_keys=["AIRTABLE_API_KEY", "AIRTABLE_BASE_ID"],
        vibe_color="#18bfff"
    ),

    # --- STRATUM IX: DEVELOPMENT & SECURITY (THE FORGE) ---
    "GITHUB": ProviderGnosis(
        name="GitHub",
        description="The absolute chronicle of code history.",
        setup_url="https://github.com/settings/tokens",
        primary_keys=["GITHUB_TOKEN", "GITHUB_CLIENT_ID", "GITHUB_CLIENT_SECRET"],
        vibe_color="#181717"
    ),
    "GITLAB": ProviderGnosis(
        name="GitLab",
        description="Complete DevOps platform.",
        setup_url="https://gitlab.com/-/profile/personal_access_tokens",
        primary_keys=["GITLAB_PRIVATE_TOKEN"],
        vibe_color="#fc6d26"
    ),
    "SNYK": ProviderGnosis(
        name="Snyk",
        description="Developer security platform for finding heresies.",
        setup_url="https://app.snyk.io/account",
        primary_keys=["SNYK_TOKEN"],
        vibe_color="#4d22b2"
    ),
    "SONAR": ProviderGnosis(
        name="SonarCloud",
        description="Clean code and security analysis.",
        setup_url="https://sonarcloud.io/account/security/",
        primary_keys=["SONAR_TOKEN"],
        vibe_color="#f3702a"
    ),

    # --- STRATUM X: SYSTEM ARTERIES (INTERNAL) ---
    "SCAFFOLD": ProviderGnosis(
        name="Scaffold Core",
        description="Internal Engine invariants and security keys.",
        setup_url="Auto-generated by the God-Engine.",
        primary_keys=["SCAFFOLD_MASTER_KEY", "SCAFFOLD_NODE_SECRET", "GNOSTIC_TRACE_ID"],
        is_internal=True,
        vibe_color="#64ffda"
    ),
}


# =============================================================================
# == THE PATTERN RECOGNIZER (FUZZY TRIAGE)                                   ==
# =============================================================================

def scry_provider_for_key(key: str) -> Optional[ProviderGnosis]:
    """
    =============================================================================
    == THE RETINAL SCRYER (O(1) TRIAGE)                                        ==
    =============================================================================
    [THE MASTER CURE]: Identifies the SaaS Provider by analyzing the variable's
    Semantic Signature. It supports both prefix and substring matching to
    handle 'STRIPE_KEY' and 'MY_APP_STRIPE_SECRET'.
    """
    k_upper = key.upper().strip()

    # [ASCENSION 1]: The Exact Prefix Strike
    # Prioritizes direct name matching
    for prov_key, gnosis in PROVIDER_DNA.items():
        # Match 'CLERK_SECRET' or 'AWS_REGION'
        if k_upper.startswith(prov_key + "_"):
            return gnosis

    # [ASCENSION 2]: The Semantic Substring Scry
    # Fallback for decorated keys like 'PROD_STRIPE_SECRET'
    for prov_key, gnosis in PROVIDER_DNA.items():
        if prov_key in k_upper:
            # Shield against small/common tokens (e.g. 'S3' inside 'PROCESS3')
            if len(prov_key) > 2 or f"_{prov_key}_" in f"_{k_upper}_":
                return gnosis

    return None


def __repr__() -> str:
    return f"<Ω_ENV_GRIMOIRE providers={len(PROVIDER_DNA)} status=RESONANT>"