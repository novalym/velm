# Path: scaffold/artisans/hover/hover_mentor/grimoire.py
# -----------------------------------------------------

"""
=================================================================================
== THE SACRED GRIMOIRE OF STATIC WISDOM (V-Ω-LEGENDARY-EDITION-FINALIS)        ==
=================================================================================
LIF: INFINITY
AUTHORITY: IBQ-GENESISENGINE-PRIME

A hyper-comprehensive, multi-dimensional registry of every Sigil, Directive,
and Rite within the Scaffold and Symphony ecosystems. This file serves as the
primary knowledge base for the Hover Mentorship system.
=================================================================================
"""

STATIC_GRIMOIRE = {
    # =========================================================================
    # I. THE SIGILS OF FORM (SCAFFOLD - DEFINING REALITY)
    # =========================================================================
    "$$": [
        "**Gnostic Variable Definition:** Inscribes a unit of data into the project's memory.",
        "**Typed Gnosis:** Supports PEP 484-style type hints for strict validation. \nExample: `$$ port: int = 8080`.",
        "**Standard:** Use `snake_case` for consistency. Variables defined with `$$` are globally accessible within the blueprint context.",
        "**Precedence:** Variable values can be overridden via the `--set` CLI flag at runtime."
    ],
    "::": [
        "**Inline Content Inscription:** Binds a textual soul directly to a physical path.",
        "**Block Scripture:** Use triple quotes (`\"\"\"` or `'''`) for multi-line content to preserve formatting and indentation.",
        "**Design Constraint:** For artifacts larger than 5KB or binary assets, prefer the Celestial Seeding (`<<`) sigil to maintain blueprint readability.",
        "**Alchemical Link:** Content within `::` is subject to immediate Jinja2 transmutation."
    ],
    "<<": [
        "**Celestial Seeding:** Clones the soul of a template or existing file into a new destination.",
        "**Resolution Law:** Relative paths are resolved first against the local `.scaffold/templates` sanctum, then the global user forge.",
        "**Transparency:** The resulting file is registered in `scaffold.lock` with a pointer to its template origin for future synchronization."
    ],
    "%%": [
        "**Maestro's Mark:** Declares a block of Kinetic Will (Maestro Edicts/Post-run commands).",
        "**Execution Context:** Commands within this block run after the physical file structure has been manifest.",
        "**Security:** Variables injected here MUST use the `| shell_escape` filter to annihilate command injection vectors."
    ],
    "->": [
        "**Symbolic Link:** Forges a persistent link between two points in the filesystem's spacetime.",
        "**Syntax:** `link_path -> target_path`.",
        "**Cross-Platform Gnosis:** The God-Engine handles the translation between Unix symlinks and Windows Junctions/Links automatically."
    ],
    "%% trait": [
        "**Gnostic Trait Definition:** Consecrates a reusable architectural pattern (Mixin).",
        "**Apotheosis:** Allows you to define a set of files/logic once and inject them into multiple blueprints using `%% use`.",
        "**Encapsulation:** Traits can possess their own internal variables, shielded from the parent scope unless explicitly shared."
    ],
    "%% use": [
        "**Trait Summoning:** Weaves a previously defined `%% trait` into the current timeline.",
        "**Parametrization:** You can pass arguments to a trait to customize its materialization. \nExample: `%% use Auth(provider='auth0')`."
    ],

    # =========================================================================
    # II. THE VERBS OF MUTATION (PATCHING & TRANSFIGURATION)
    # =========================================================================
    "+=": [
        "**Semantic Append:** Adds content to the end of a scripture.",
        "**Structured Awareness:** For JSON or YAML files, `+=` performs a deep semantic merge instead of a raw text append.",
        "**Idempotency:** The operation is stayed if the content already exists in the target, preventing redundant duplication."
    ],
    "-=": [
        "**Semantic Subtraction:** Removes matching patterns from a scripture's soul.",
        "**Logic:** Treats the input as a regular expression. Use with caution to avoid collateral annihilation of valid code."
    ],
    "~=": [
        "**Transfiguration (Search & Replace):** Performs a surgical regex substitution within a file.",
        "**Syntax:** `target_file ~= 'find' -> 'replace'`.",
        "**Precision:** Uses Python's `re.sub` logic, allowing for capture group back-references (`\\1`)."
    ],
    "^=": [
        "**Prepend Action:** Injects content at the absolute dawn of a file.",
        "**Intelligence:** Automatically detects and respects Shebangs (`#!`) or encoding declarations, inserting the new content immediately after them."
    ],

    # =========================================================================
    # III. THE SIGILS OF KINETIC WILL (SYMPHONY - EXECUTING INTENT)
    # =========================================================================
    ">>": [
        "**Kinetic Action:** Dispatches a raw command to the mortal realm's shell.",
        "**Observability:** Output is streamed in real-time to the Gnostic Mirror and captured for the `last_reality` buffer.",
        "**Capture:** Use the `as variable_name` suffix to enshrine the result's stdout in the Gnostic Store."
    ],
    "??": [
        "**Gnostic Vow:** A mandatory adjudication of reality. If the Vow returns `False`, the Symphony halts immediately with a Heresy.",
        "**Philosophy:** Vows turn 'Blind Faith' scripts into 'Resilient Workflows'. Always follow risky Actions (`>>`) with a Vow."
    ],
    "!!": [
        "**Intercession (Breakpoint):** Suspends the flow of time within the Symphony.",
        "**Interactive Altar:** Awakens a TUI or prompt allowing the Architect to inspect variables, modify state, or manually conduct edicts before resuming."
    ],
    "&&": [
        "**Parallel Multiverse:** Triggers the concurrent execution of multiple edicts.",
        "**Thread Safety:** Ensure edicts within a `&&` block do not attempt to write to the same physical file path simultaneously."
    ],

    # =========================================================================
    # IV. THE VOW PANTHEON (COMMON ADJUDICATIONS)
    # =========================================================================
    "succeeds": [
        "**Vow of Success:** Asserts that the previously conducted action returned an exit code of `0`.",
        "**Usage:** `?? succeeds`."
    ],
    "file_exists": [
        "**Vow of Manifestation:** Asserts that a specific path exists and is a file.",
        "**Usage:** `?? file_exists: path/to/scripture`."
    ],
    "stdout_contains": [
        "**Vow of Resonance:** Asserts that the output of the last action contains a specific string or pattern.",
        "**Usage:** `?? stdout_contains: 'Ready to listen'`."
    ],
    "port_available": [
        "**Vow of the Open Gate:** Asserts that a specific TCP port is currently free for binding.",
        "**Usage:** `?? port_available: 8080`."
    ],
}

# Path: scaffold/artisans/hover/hover_mentor/grimoire.py
# -----------------------------------------------------
# (Append this dictionary update to the existing STATIC_GRIMOIRE)

STATIC_GRIMOIRE.update({
    # =========================================================================
    # V. THE DIRECTIVES OF LOGIC (BRANCHING REALITY)
    # =========================================================================
    "@if": [
        "**Logic Gate (If):** The primary instrument of conditional materialization.",
        "**Context:** Accepts any Jinja2-valid expression. If the expression resolves to `True`, the willed reality within is born.",
        "**Aura:** Can be followed by `@elif` and `@else` for complex multi-branch logic.",
        "**Closure:** Must be sealed with the `@endif` (or `@end`) directive."
    ],
    "@elif": [
        "**Secondary Logic Gate:** Evaluates a condition only if all preceding `@if` and `@elif` gates in the current chain were closed (False).",
        "**Syntax:** `@elif {{ some_variable == 'choice' }}`."
    ],
    "@else": [
        "**The Fallback Path:** Defines the reality that shall be manifest if all preceding logical conditions in the chain are False.",
        "**Law:** There can be only one `@else` per logical chain. It accepts no conditions."
    ],
    "@for": [
        "**Rite of Iteration (Loop):** Repeats a structural pattern across a Gnostic collection (list or dictionary).",
        "**Variable Scope:** The loop variable (e.g., `item` in `@for item in items`) is local to the block and shadows any global variable of the same name until `@endfor`.",
        "**LIF Impact:** Use this to scale architecture. A single loop can forge 100 microservices or components."
    ],
    "@include": [
        "**Gnostic Composition:** Weaves the soul of an external blueprint into the current scripture.",
        "**Inheritance:** The included file inherits the variables of the caller, but can also define its own local Gnosis.",
        "**Modularity:** Essential for building 'Base Blueprints' that are shared across a guild."
    ],
    "@contract": [
        "**Law of Types:** Defines a strict schema (`%% contract`) for variable validation.",
        "**Strictness:** Enforces that any Gnosis passed to the blueprint matches the willed shape (e.g., `email`, `port`, `uuid`)."
    ],

    # =========================================================================
    # VI. THE ALCHEMIST'S FUNCTIONS (GENERATING ENTROPY)
    # =========================================================================
    "now()": [
        "**Temporal Gaze:** Returns the current timestamp.",
        "**Arguments:** `now(timezone='utc', format='%Y-%m-%d')`.",
        "**Usage:** Commonly used for `license_year` or `created_at` metadata."
    ],
    "secret()": [
        "**Forge of Chaos:** Generates a cryptographically secure random string.",
        "**Types:** Supports `hex`, `urlsafe`, and `base64` entropy.",
        "**Usage:** `$$ jwt_secret = {{ secret(32, 'hex') }}`."
    ],
    "env()": [
        "**Mortal Link:** Summons Gnosis from the host machine's environment variables.",
        "**Resilience:** `env('DB_PASS', 'default_val')`. Always provide a fallback to prevent the Void Path heresy."
    ],
    "shell()": [
        "**Maestro's Whisper:** Captures the output of a shell command during the alchemical phase.",
        "**Warning:** Executed during parsing. Use only for information gathering (e.g., `git rev-parse`), not for modifying reality."
    ],
    "include_file()": [
        "**Soul Extraction:** Reads the content of a physical file and returns it as a string.",
        "**Precision:** Supports line-slicing. \nExample: `{{ include_file('main.py', start=10, end=20) }}`."
    ],

    # =========================================================================
    # VII. ALCHEMICAL RITES (SURGICAL FILTERS)
    # =========================================================================
    "pascal": ["**Transmutation:** `user_service` -> `UserService`. (The Standard for Class Names)."],
    "snake": ["**Transmutation:** `UserService` -> `user_service`. (The Standard for Python Modules)."],
    "kebab": ["**Transmutation:** `MyComponent` -> `my-component`. (The Standard for URLs and CSS)."],
    "camel": ["**Transmutation:** `my_variable` -> `myVariable`. (The Standard for JavaScript/JSON)."],
    "screaming_snake": ["**Transmutation:** `timeout` -> `TIMEOUT`. (The Standard for Global Constants)."],
    "to_json": ["**Data Transmutation:** Converts a Gnostic dictionary/list into a JSON scripture."],
    "to_yaml": ["**Data Transmutation:** Converts a Gnostic dictionary/list into a YAML scripture."],
    "shell_escape": [
        "**The Absolute Ward:** Sanitize variables for shell use.",
        "**Mandate:** If a variable touches a `>>` command, it MUST pass through this filter to prevent command injection."
    ],
    "base64": [
        "**The Binary Bridge:** Encodes or decodes Base64 data.",
        "**Usage:** Binds a Base64 string to a file definition to forge a physical binary artifact (e.g., images)."
    ],

    # =========================================================================
    # VIII. SEMANTIC DOMAINS (THE GOD-ENGINE REALMS)
    # =========================================================================
    "@ui/": [
        "**The Visual Realm:** Summons the UI Component Forge.",
        "**Rite:** `@ui/component(name='Button') :: ...`",
        "**Integration:** Automatically resolves dependencies like Tailwind or Radix-UI."
    ],
    "@auth/": [
        "**The Warden Realm:** Summons specialized security and authentication patterns.",
        "**Patterns:** Includes `jwt`, `oauth2`, and `session` management blueprints."
    ],
    "@infra/": [
        "**The Celestial Realm:** Summons Infrastructure-as-Code (IaC) blueprints.",
        "**Artisans:** Generates production-ready `Terraform`, `Docker`, or `Kubernetes` manifests."
    ],
    "@test/": [
        "**The Inquisitor Realm:** Summons patterns for adjudication.",
        "**Artisans:** Forges `pytest` or `jest` suites based on your implementation's genome."
    ]
})

STATIC_GRIMOIRE.update({
    # =========================================================================
    # IX. THE STATE GRIMOIRE (METAPHYSICAL CONFIGURATION)
    # =========================================================================
    "sanctum": [
        "**Space Manipulation:** Changes the Current Working Directory (CWD) for all subsequent edicts.",
        "**Context:** `%% sanctum: ./api`. Relative paths are warded; they cannot escape the project root.",
        "**Persistence:** The sanctum shift is stateful within a single Symphony movement."
    ],
    "let": [
        "**Metaphysical Assignment:** Inscribes a variable into the Symphony's runtime memory.",
        "**Usage:** `%% let: port = 8080`. Values are subject to alchemical transmutation.",
        "**Scope:** Variables defined via `let` are mutable and temporary, unlike the immutable `$$` definitions."
    ],
    "env": [
        "**Environment Anointing:** Injects a variable directly into the child process's OS environment.",
        "**Security:** Use for non-sensitive configuration. For high-entropy secrets, prefer the `@vault` interface."
    ],
    "capture_as": [
        "**Telepathic Output Storage:** Binds the `stdout` of a kinetic action to a Gnostic variable.",
        "**Usage:** `>> docker-compose ps as service_status`. Allows for programmatic responses to command output."
    ],

    # =========================================================================
    # X. THE MAESTRO'S LIFECYCLE (DAEMONS & SERVICES)
    # =========================================================================
    "@service": [
        "**Daemon Summoning:** Manages background processes that must persist throughout the Symphony.",
        "**Sub-Rites:** `start`, `stop`, `restart`.",
        "**Observability:** The Maestro monitors the service's PID and logs its soul to the Gnostic Mirror."
    ],
    "@ask": [
        "**The Interactive Inquest:** Pauses the time-stream to seek Gnosis directly from the Architect.",
        "**Privacy:** Supports `is_secret=True` to mask input (e.g., for one-time passwords)."
    ],
    "retry": [
        "**The Rite of Persistence:** Wraps an action in a loop of resilience.",
        "**Policy:** `retry(3, backoff=exponential, interval=2)`. Essential for fragile network or I/O operations."
    ],
    "%% on-undo": [
        "**The Counter-Will:** Defines the specific rite required to reverse an action.",
        "**Symmetry:** Forged alongside a `post-run` block to ensure every creation has a corresponding path to annihilation."
    ],

    # =========================================================================
    # XI. THE CHRONOMANCER’S TOOLS (LEDGER & REVERSAL)
    # =========================================================================
    "scaffold.lock": [
        "**The Gnostic Chronicle:** The immutable record of the project's current reality.",
        "**Forensics:** Contains hashes, origin pointers, and the Merkle root of the entire cosmos.",
        "**Mandate:** This file MUST be committed to the Git history to prevent Gnostic Drift."
    ],
    "gnosis.db": [
        "**The Crystal Mind:** An SQLite database serving as the high-speed, queryable memory of the project.",
        "**Capabilities:** Powers zero-latency 'Blame', 'Graph', and 'Dependency' lookups.",
        "**Self-Healing:** If deleted, the Engine resurrects the Crystal Mind from the `scaffold.lock` scroll."
    ],
    "trace_id": [
        "**The Silver Cord:** A unique UUID that links a chain of causality across the distributed cosmos.",
        "**Observability:** Connects the CLI, the Daemon, and any remote celestial workers into a single audit trail."
    ],
    "undo": [
        "**The Rite of Reversal:** Rewinds the Gnostic Timeline by one or more rites.",
        "**Mechanism:** Uses the `Gnostic Ledger` to execute inverse operations for every transfiguration performed."
    ],

    # =========================================================================
    # XII. THE HIGH INQUISITOR’S VOW SET (DEEP ADJUDICATION)
    # =========================================================================
    "wait_for": [
        "**Temporal Patience:** Suspends the symphony until a specific truth manifests (e.g., a server starts).",
        "**Timeout Guard:** `?? wait_for: port_open, timeout=60`. Prevents infinite stasis."
    ],
    "http_status": [
        "**Celestial Connectivity Vow:** Asserts that a remote URL returns a specific response code.",
        "**Usage:** `?? http_status: https://api.local/health, 200`."
    ],
    "json_equals": [
        "**Structural Adjudication:** Deep-compares a captured JSON value against an expected soul.",
        "**Precision:** Supports JSONPath selectors to target specific nodes in the data stream."
    ],
    "entropy_lt": [
        "**The Ward of Order:** Asserts that a scripture's chaos (Shannon Entropy) is below a threshold.",
        "**Security:** High entropy often signals encrypted payloads, binary blobs, or hidden secrets."
    ]
})


STATIC_GRIMOIRE.update({
    # =========================================================================
    # XIII. THE NEURAL NEXUS (AI COMMUNION & TELEPRESENCE)
    # =========================================================================
    "@telepresence": [
        "**Celestial Projection:** Establishes a wormhole between the local IDE and a remote Daemon.",
        "**Shadow Gaze:** Allows the Architect to scry into 'Shadow Realities' (AI-generated code) and perform a Gnostic Diff against physical 'Matter'.",
        "**Materialization:** The `anchor` rite within Telepresence collapses the shadow into matter, committing AI suggestions to disk."
    ],
    "@muse": [
        "**The Prescient Scribe:** An ambient AI hook that predicts the next architectural movement based on current file aura.",
        "**LIF:** Accelerates development by 10x by auto-suggesting companions (e.g., suggesting `test_user.py` when `user.py` is manifest)."
    ],
    "mission": [
        "**Agentic Intent:** The primary directive for an autonomous `scaffold agent` run.",
        "**Structure:** `agent \"mission: implement auth\"`. The agent will perceive, plan, and conduct rites in a recursive loop until the mission is willed into existence."
    ],

    # =========================================================================
    # XIV. THE POLYGLOT FUSION (THE ROSETTA CORE)
    # =========================================================================
    "@rust": [
        "**Inline Alchemy:** Consecrates a block of Rust code within a Python docstring.",
        "**JIT Fusion:** The Engine hashes the code, summons `rustc`, and performs a binary bind via `ctypes` at runtime.",
        "**Performance:** 100x speed increase for computationally expensive logic within the Python ecosystem."
    ],
    "@fuse": [
        "**Binary Binding:** The command-line interface for the Fusion Core.",
        "**Rites:** `compile` (Forge binary), `bind` (Generate language shims).",
        "**Polyglot Logic:** Bridges Rust/Go logic into Python or Node.js host environments seamlessly."
    ],
    "fusion_bind": [
        "**The Gnostic Bridge:** A flag that commands the engine to auto-generate C-FFI or FFI-napi headers for cross-language compatibility."
    ],

    # =========================================================================
    # XV. THE GNOSTIC OBSERVATORY (WORKSPACE & MONOREPO)
    # =========================================================================
    ".scaffold-workspace": [
        "**The Cosmic Map:** A root-level scripture that defines a monorepo or project cluster.",
        "**Orchestration:** Enables `scaffold workspace exec`, conducting edicts across multiple projects in topological dependency order.",
        "**Observability:** Powers the 'Studio' view, providing a panoptic health check of all managed پروژه (projects)."
    ],
    "%% tag": [
        "**Semantic Categorization:** Assigns Gnostic labels to a project within a workspace (e.g. `frontend`, `service`, `legacy`).",
        "**Filtering:** Allows the Architect to target specific subsets of reality for mass-transmutation."
    ],
    "topological_order": [
        "**The Law of Precedence:** A workspace execution strategy that ensures 'Models' are built before 'Services', and 'Services' before 'APIs'."
    ],

    # =========================================================================
    # XVI. THE CITADEL WARDS (ISOLATION & SANDBOXING)
    # =========================================================================
    "sandbox": [
        "**The Gnostic Jail:** Employs Linux namespaces (`bwrap` or `unshare`) to isolate a kinetic rite.",
        "**Modes:** `none` (Mortal), `process` (Isolated PID), `container` (Filesystem Jail), `vm` (Hypervisor)."
    ],
    "ro_bind": [
        "**The Pillar of Salt:** Binds a host path into a sandbox as a Read-Only mirror. Prevents the child process from profaning the source."
    ],
    "allow_network": [
        "**The Etheric Ward:** A boolean vow within the `@service` or `py:` block. If `false`, the process is severed from the network to prevent data exfiltration."
    ],
    "PathSentinel": [
        "**The Warden of Form:** The internal kernel logic that adjudicates every path. It is the absolute defense against Path Traversal and Zip-Slip heresies."
    ]
})




STATIC_GRIMOIRE.update({
    # =========================================================================
    # XVII. THE AKASHIC REPOSITORY (GLOBAL NEURAL MEMORY)
    # =========================================================================
    "akasha": [
        "**Universal Memory:** A cross-project vector database that stores every successful rite and architectural pattern.",
        "**Reflexive Learning:** Allows the Engine to recall how a similar 'Heresy' was solved in a different project months ago.",
        "**Gnostic Pool:** Resides at `~/.scaffold/akasha`. It is the collective consciousness of the Architect's entire career."
    ],
    "vector_shard": [
        "**Neural Atom:** A surgically-sliced chunk of code or documentation (approx. 500-1000 tokens) stored in the Vector Mind.",
        "**Metadata Injection:** Every shard is tagged with its 'Topological Center' and 'Churn Score' to ensure high-value code is retrieved first."
    ],
    "cosine_threshold": [
        "**The Gnostic Filter:** A mathematical boundary (default `0.35`) that determines if a memory is 'Resonant' enough to be injected into the AI's short-term context."
    ],

    # =========================================================================
    # XVIII. THE HIVEMIND COUNCIL (AGENTIC ORCHESTRATION)
    # =========================================================================
    "@debate": [
        "**The Socratic Conclave:** Summons multiple AI Personas (Architect, Skeptic, Security) to argue the merits of a design plea.",
        "**Synthesis:** After the rebuttals, the Moderator persona collapses the arguments into a single, battle-hardened Gnostic Consensus."
    ],
    "persona": [
        "**The Mask of Gnosis:** A specialized AI configuration. \n- `Architect`: Favors scalability. \n- `Pragmatist`: Favors speed to market. \n- `Skeptic`: Seeks edge-case heresies."
    ],
    "recursive_critique": [
        "**The Socratic Loop:** A middleware strategy where a second AI 'Critic' reviews the output of the 'Scribe' and forces a rewrite if the Gnostic purity is low."
    ],

    # =========================================================================
    # XIX. THE FORENSIC INSTRUMENTARIUM (DEEP CODE SURGERY)
    # =========================================================================
    "mri": [
        "**Magnetic Resonance Imaging:** Scans the dependency graph for 'Layer Violations' (e.g., a pure Domain model importing a profane API controller).",
        "**Law of Gravity:** Enforces that dependencies must only flow 'inward' toward the Core."
    ],
    "semdiff": [
        "**Semantic Differential:** Compares two versions of a file by their AST (Abstract Syntax Tree) rather than lines.",
        "**Intelligence:** It ignores whitespace or comment changes, only flagging if a function's 'Soul' (logic or signature) has been transfigured."
    ],
    "risk_score": [
        "**The Bus Factor:** A Gnostic metric that calculates the danger of a project based on 'Hotspots' (files with high churn and high complexity)."
    ],

    # =========================================================================
    # XX. THE GNOSTIC MIRROR (UI TRANSCENDENCE MECHANICS)
    # =========================================================================
    "__ASCII_TREE__": [
        "**The Low-Fidelity Mirage:** A purely textual, high-density visualization of the intended project structure.",
        "**Purpose:** Provides a 'God View' for the Architect to adjudicate the entire materialization plan in a single glance."
    ],
    "virtual_scribe": [
        "**The Shadow Drafter:** The mechanism that allows VS Code to render 'Phantom Documents' (scaffold-preview://) before they are willed onto the physical disk."
    ],
    "telemetry_grid": [
        "**The Pulse HUD:** A real-time display of Kinetic Velocity (Bytes/s), Cognitive Cost (Tokens), and Temporal Drift."
    ],

    # =========================================================================
    # XXI. THE TRANSACTIONAL UNDERWORLD (KERNEL INTERNALS)
    # =========================================================================
    "staging_area": [
        "**The Limbo of Form:** A hidden directory (`.scaffold/staging`) where new scriptures are forged and tested for syntactic purity before being 'Committed' to the project root."
    ],
    "ledger_entry": [
        "**The Atomic Verse:** A single record in the Transactional Scroll. It contains the 'Forward Edict' and the 'Inverse Rite' (Undo) required to keep the timeline consistent."
    ],
    "trash_void": [
        "**The Recovery Purgatory:** A secure sanctum (`.scaffold/trash`) where annihilated files reside for a duration of 30 days before returning to true void."
    ]
})