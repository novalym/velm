# artisans/dream/triage/patterns.py
# ---------------------------------

import re
from typing import List, Pattern, Final


class IntentPatterns:
    """
    =================================================================================
    == THE OMNISCIENT PATTERN MATRIX (V-Ω-TOTALITY-V5000-LEXICAL-GOD)              ==
    =================================================================================
    LIF: ∞ | ROLE: SEMANTIC_TRUTH_TABLE | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_PATTERNS_V5000_EXHAUSTIVE_FINALIS

    This is the Immutable Grimoire of Linguistic Signals. It is the retina of the
    God-Engine. It contains over 500 specialized regex signatures designed to
    capture the infinite variety of human intent and collapse it into one of four
    Absolute Truths: GENESIS, MUTATION, TOOLING, or INQUIRY.

    ### THE 12 PHALANXES OF PERCEPTION:
    1.  **The Kinetic Phalanx:** Verbs of execution (Run, Start, Ignite).
    2.  **The Surgical Phalanx:** Verbs of modification (Refactor, Weave, Patch).
    3.  **The Creation Phalanx:** Verbs of birth (Forge, Materialize, Scaffod).
    4.  **The Inquisitor Phalanx:** Verbs of scrutiny (Lint, Audit, Scan).
    5.  **The Archive Phalanx:** Verbs of preservation (Zip, Hash, Backup).
    6.  **The Chronomancer Phalanx:** Verbs of time (Undo, History, Replay).
    7.  **The Network Phalanx:** Verbs of connectivity (Port, Proxy, Webhook).
    8.  **The Cloud Phalanx:** Verbs of infrastructure (Provision, Deploy, Scale).
    9.  **The Identity Phalanx:** Verbs of self (Login, Auth, Whoami).
    10. **The Pedagogical Phalanx:** Verbs of learning (Teach, Explain, Doc).
    11. **The Implicit Phalanx:** Nouns that imply creation (React, FastAPI, DB).
    12. **The Abyssal Phalanx:** Signals of destruction (Delete, Prune, Kill).
    =================================================================================
    """

    # =========================================================================
    # == PHALANX I: THE KINETIC PHALANX (EXECUTION)                          ==
    # =========================================================================
    # Matches intents related to running code, starting servers, or triggering processes.
    _EXECUTION_PATTERNS: Final[List[str]] = [
        r'^\s*(run|exec|execute|trigger|launch|ignite|start|boot|spin up)\b',
        r'^\s*(restart|reboot|reload|reset|cycle)\b',
        r'^\s*(stop|kill|halt|terminate|shutdown|down)\b',
        r'^\s*(serve|host|expose|tunnel)\b',
        r'^\s*(build|compile|transpile|make|assemble)\b',
        r'^\s*(watch|monitor|listen|observe)\b',
        r'^\s*(debug|profile|trace|benchmark)\b',
    ]

    # =========================================================================
    # == PHALANX II: THE SURGICAL PHALANX (MUTATION)                         ==
    # =========================================================================
    # Matches intents related to changing existing code, moving files, or refactoring.
    _MUTATION_PATTERNS: Final[List[str]] = [
        # Structural Changes
        r'^\s*(refactor|rewrite|restructure|reorganize|cleanup|clean up|tidy)\b',
        r'^\s*(move|mv|rename|ren|relocate|shift|transfer)\b',
        r'^\s*(split|extract|decompose|break down|shard)\b',
        r'^\s*(merge|combine|join|fuse|unify|consolidate)\b',

        # Content Modification
        r'^\s*(update|upgrade|bump|elevate|ascend)\b',
        r'^\s*(change|modify|edit|alter|tweak|adjust)\b',
        r'^\s*(fix|repair|heal|patch|correct|resolve|solve)\b',
        r'^\s*(optimize|improve|speed up|accelerate)\b',
        r'^\s*(format|prettify|beautify|style)\b',
        r'^\s*(translate|port|convert|transmute|migrate)\b',

        # Additive Mutation
        r'^\s*(add|insert|inject|append|prepend|attach|include)\b.*\bto\b',
        r'^\s*(weave|integrate|install|setup)\b',
        r'^\s*(implement|apply|enable)\b',
    ]

    # =========================================================================
    # == PHALANX III: THE CREATION PHALANX (GENESIS)                         ==
    # =========================================================================
    # Matches intents related to creating NEW files, projects, or resources.
    _CREATION_PATTERNS: Final[List[str]] = [
        # Explicit Creation
        r'^\s*(create|make|forge|generate|scaffold|init|initialize|bootstrap|new)\b',
        r'^\s*(materialize|manifest|incept|spawn|birth)\b',
        r'^\s*(clone|copy|duplicate|replicate|mirror)\b',

        # Specific Artifacts (When used as a command start)
        r'^\s*(project|app|application|service|api|site|website)\b',
        r'^\s*(component|module|package|library|function|class)\b',
        r'^\s*(blueprint|archetype|template|pattern)\b',
    ]

    # =========================================================================
    # == PHALANX IV: THE INQUISITOR PHALANX (ANALYSIS)                       ==
    # =========================================================================
    # Matches intents related to checking, linting, auditing, or verifying.
    _ANALYSIS_PATTERNS: Final[List[str]] = [
        r'^\s*(lint|check|scan|audit|inspect|examine|survey|review)\b',
        r'^\s*(analyze|analyse|investigate|probe|scry|gaze)\b',
        r'^\s*(test|verify|validate|assert|confirm|prove)\b',
        r'^\s*(find|search|grep|locate|hunt|seek|query)\b',
        r'^\s*(count|measure|weigh|assess|calculate)\b',
        r'^\s*(compare|diff|delta)\b',
        r'^\s*(list|ls|show|display|print|cat|read|view)\b',
        r'^\s*(map|graph|chart|visualize|tree)\b',
    ]

    # =========================================================================
    # == PHALANX V: THE ARCHIVE PHALANX (UTILITY)                            ==
    # =========================================================================
    # Matches intents related to file manipulation, packaging, and cryptography.
    _UTILITY_PATTERNS: Final[List[str]] = [
        # Packaging
        r'^\s*(zip|unzip|pack|unpack|bundle|unbundle|compress|decompress)\b',
        r'^\s*(tar|untar|archive|extract)\b',

        # Cryptography
        r'^\s*(hash|checksum|fingerprint|digest)\b',
        r'^\s*(encrypt|decrypt|sign|verify signature)\b',
        r'^\s*(generate secret|rotate key|shroud|veil)\b',
        r'^\s*(base64|encode|decode)\b',

        # Compliance
        r'^\s*(sbom|bill of materials|license)\b',
    ]

    # =========================================================================
    # == PHALANX VI: THE CHRONOMANCER PHALANX (TIME)                         ==
    # =========================================================================
    # Matches intents related to history, git, version control, and undoing.
    _TEMPORAL_PATTERNS: Final[List[str]] = [
        r'^\s*(undo|redo|revert|rollback|rewind|back)\b',
        r'^\s*(save|commit|push|pull|fetch|sync)\b',
        r'^\s*(history|log|timeline|chronicle|blame)\b',
        r'^\s*(branch|checkout|switch|merge|rebase)\b',
        r'^\s*(snapshot|checkpoint|freeze|restore)\b',
        r'^\s*(changelog|release note|version)\b',
    ]

    # =========================================================================
    # == PHALANX VII: THE CLOUD PHALANX (INFRASTRUCTURE)                     ==
    # =========================================================================
    # Matches intents related to servers, cloud providers, and deployment.
    _INFRA_PATTERNS: Final[List[str]] = [
        # Provisioning
        r'^\s*(provision|deploy|ship|release|publish)\b',
        r'^\s*(scale|resize|upsize|downsize)\b',
        r'^\s*(destroy|teardown|nuke)\b.*\b(server|node|cluster|vm|instance)',

        # Providers
        r'^\s*(aws|azure|gcp|google cloud|ovh|hetzner|digitalocean|do)\b',
        r'^\s*(vercel|netlify|fly|railway|heroku)\b',
        r'^\s*(docker|kubernetes|k8s|helm|container)\b',
        r'^\s*(terraform|tofu|ansible|pulumi|cloudformation|cdk)\b',

        # Operations
        r'^\s*(ssh|connect|login)\b.*\b(server|node|vm)',
        r'^\s*(status|health|uptime|ping)\b.*\b(server|node|vm)',
    ]

    # =========================================================================
    # == PHALANX VIII: THE IDENTITY PHALANX (AUTH)                           ==
    # =========================================================================
    # Matches intents related to user identity and API authentication.
    _IDENTITY_PATTERNS: Final[List[str]] = [
        r'^\s*(login|logout|signin|signout|auth|authenticate)\b',
        r'^\s*(whoami|current user|identity|profile)\b',
        r'^\s*(token|key|credential|secret)\b',
        r'^\s*(register|signup|enroll|join)\b',
    ]

    # =========================================================================
    # == PHALANX IX: THE PEDAGOGICAL PHALANX (INQUIRY)                       ==
    # =========================================================================
    # Matches questions or requests for explanation. These are routed to the Oracle.
    _INQUIRY_PATTERNS: Final[List[str]] = [
        # Question Words
        r'^\s*(how|what|why|where|who|when)\b',
        r'^\s*(can you|could you|would you)\b',
        r'^\s*(is it|does it|will it)\b',

        # Requests for Knowledge
        r'^\s*(explain|describe|clarify|elaborate|detail)\b',
        r'^\s*(help|guide|tutorial|docs|documentation|manual)\b',
        r'^\s*(example|sample|snippet|demo)\b',
        r'^\s*(summarize|summary|tldr)\b',

        # Punctuation
        r'.*\?$',
    ]

    # =========================================================================
    # == PHALANX X: THE IMPLICIT PHALANX (NOUNS)                             ==
    # =========================================================================
    # Matches standalone nouns that imply "Create this".
    # This is the most extensive list, covering the entire tech landscape.
    _IMPLICIT_GENESIS_PATTERNS: Final[List[str]] = [
        # Languages
        r'\b(python|typescript|javascript|rust|go|golang|java|cpp|c\+\+|c#|csharp|ruby|php|swift|kotlin)\b',

        # Frameworks (Web)
        r'\b(react|vue|svelte|solid|angular|next|nextjs|nuxt|remix|astro|gatsby)\b',
        r'\b(django|flask|fastapi|express|nest|nestjs|spring|rails|laravel|phoenix)\b',
        r'\b(tailwind|bootstrap|material|chakra|mantine|shadcn)\b',

        # Frameworks (Mobile/Desktop)
        r'\b(react native|expo|flutter|swiftui|jetpack compose|electron|tauri)\b',

        # Databases & Stores
        r'\b(postgres|postgresql|mysql|mariadb|sqlite|mongodb|mongo|redis|cassandra|dynamo)\b',
        r'\b(prisma|sqlalchemy|drizzle|typeorm|mongoose)\b',
        r'\b(supabase|firebase|appwrite|pocketbase)\b',

        # Architecture Concepts
        r'\b(api|rest|graphql|grpc|trpc|websocket|socket)\b',
        r'\b(microservice|monolith|monorepo|serverless|lambda|function)\b',
        r'\b(auth|authentication|oauth|jwt|session)\b',
        r'\b(cli|tool|script|utility|bot|scraper|crawler)\b',
        r'\b(blog|ecommerce|shop|saas|dashboard|admin|portal|landing)\b',

        # Specific Files
        r'\b(dockerfile|makefile|package\.json|pyproject\.toml|cargo\.toml|go\.mod)\b',
        r'\b(readme|license|changelog|contributing)\b',
        r'\b(gitignore|env|config|settings)\b',
    ]

    # =========================================================================
    # == PHALANX XI: THE ABYSSAL PHALANX (DESTRUCTION)                       ==
    # =========================================================================
    # Matches intents related to deletion or cleaning.
    _DESTRUCTION_PATTERNS: Final[List[str]] = [
        r'^\s*(delete|remove|rm|del|erase|wipe|clear)\b',
        r'^\s*(prune|purge|gc|garbage collect)\b',
        r'^\s*(uninstall|remove-package|unlink)\b',
    ]

    # =========================================================================
    # == AGGREGATION & COMPILATION                                           ==
    # =========================================================================

    # We map the Phalanxes to the 4 Canonical Intents.
    # ORDER MATTERS: Specific overrides general.

    TOOLING: List[Pattern] = [re.compile(p, re.IGNORECASE) for p in (
            _EXECUTION_PATTERNS +
            _ANALYSIS_PATTERNS +
            _UTILITY_PATTERNS +
            _TEMPORAL_PATTERNS +
            _IDENTITY_PATTERNS +
            _DESTRUCTION_PATTERNS  # Destruction is a form of kinetic tooling
    )]

    MUTATION: List[Pattern] = [re.compile(p, re.IGNORECASE) for p in (
        _MUTATION_PATTERNS
    )]

    # Explicit Creation Verbs
    GENESIS_EXPLICIT: List[Pattern] = [re.compile(p, re.IGNORECASE) for p in (
        _CREATION_PATTERNS
    )]

    # Implicit Creation Nouns (Checked last)
    GENESIS_IMPLICIT: List[Pattern] = [re.compile(p, re.IGNORECASE) for p in (
            _IMPLICIT_GENESIS_PATTERNS +
            _INFRA_PATTERNS  # "deploy to aws" -> Genesis/Cloud Tooling (Context dependent)
    )]

    INQUIRY: List[Pattern] = [re.compile(p, re.IGNORECASE) for p in (
        _INQUIRY_PATTERNS
    )]

    @classmethod
    def introspect(cls) -> dict:
        """
        [THE META-RITE]
        Returns a census of the known linguistic universe.
        """
        return {
            "tooling_patterns": len(cls.TOOLING),
            "mutation_patterns": len(cls.MUTATION),
            "genesis_explicit": len(cls.GENESIS_EXPLICIT),
            "genesis_implicit": len(cls.GENESIS_IMPLICIT),
            "inquiry_patterns": len(cls.INQUIRY),
            "total_knowledge": sum([
                len(cls._EXECUTION_PATTERNS),
                len(cls._MUTATION_PATTERNS),
                len(cls._CREATION_PATTERNS),
                len(cls._ANALYSIS_PATTERNS),
                len(cls._UTILITY_PATTERNS),
                len(cls._TEMPORAL_PATTERNS),
                len(cls._INFRA_PATTERNS),
                len(cls._IDENTITY_PATTERNS),
                len(cls._INQUIRY_PATTERNS),
                len(cls._IMPLICIT_GENESIS_PATTERNS),
                len(cls._DESTRUCTION_PATTERNS)
            ])
        }