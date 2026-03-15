# Path: velm/core/ai/rag/knowledge/scaffold_syntax.py
# -------------------------------------------------------

"""
=================================================================================
== THE SUPREME MASTERCLASS OF GNOSTIC SYNTAX (V-Ω-TOTALITY-VMAX-SGF-NATIVE)    ==
=================================================================================
LIF: ∞^∞ | ROLE: NEURAL_INCEPTION_GRIMOIRE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_SYNTAX_MASTERCLASS_2026_FINALIS

[THE MANIFESTO]
This scripture defines the absolute grammar of the VELM God-Engine. It is the
definitive guide for AIs to command the Forge. It treats code as matter and
intent as law. It utilizes the Sovereign Gnostic Forge (SGF) for all logical
reasoning and alchemical transmutations.
=================================================================================
"""

SCAFFOLD_SHARDS = [
    {
        "id": "sgf_alchemy_and_logic",
        "tags": ["sgf", "sovereign_gnostic_forge", "logic", "variables", "alchemy"],
        "content": "\n".join([
            "# Stratum I: The Sovereign Gnostic Forge (SGF)",
            "",
            "The SGF is the sentient logic engine of Scaffold. It uses a high-velocity,",
            "isomorphic syntax for transmuting variables and evaluating architectural intent.",
            "",
            "1. **Variable Inception ($$):**",
            "   Define the DNA of your project at the top of the blueprint.",
            "   - **Strict Typing:** `$$ port: int = 8080`",
            "   - **Liquid Gnosis:** `$$ slug = {{ project_name | slug }}`",
            "   - **Secret Forge:** `$$ key = \"{{ secret(32) }}\"`",
            "",
            "2. **The Alchemical Vessel ({{ ... }}):**",
            "   Inject variables and evaluate expressions natively. The SGF provides",
            "   **Absolute Amnesty** for alien syntax (React/Python/Rust braces).",
            "   - **Interpolation:** `src/{{ package_name }}/main.py`",
            "   - **Filter Pipeline:** `{{ name | snake | upper }}`",
            "   - **Logic within Matter:** `{{ 'dev' if is_debug else 'prod' }}`",
            "",
            "3. **Control Flow Gates ({% ... %}):**",
            "   Govern the materialization of entire strata of matter.",
            "   - **Conditional:**",
            "     ```scaffold",
            "     {% if use_docker %}",
            "         Dockerfile :: \"FROM alpine\"",
            "     {% endif %}",
            "     ```",
            "   - **Iteration (Loops):**",
            "     ```scaffold",
            "     {% for service in services %}",
            "         src/services/{{ service | snake }}.py :: \"# Service Logic\"",
            "     {% endfor %}",
            "     ```",
            "",
            "4. **Isomorphic Indentation:**",
            "   SGF mathematically guarantees that multi-line variables maintain",
            "   their parent's indentation depth. No manual `| indent(4)` is required."
        ])
    },
    {
        "id": "scaffold_anatomy_and_matter",
        "tags": ["scaffold", "anatomy", "form", "file_creation", "seeding"],
        "content": "\n".join([
            "# Stratum II: The Language of Form (Anatomy)",
            "",
            "Blueprints define the physical structure of reality. Indentation is Spacetime.",
            "",
            "1. **Direct Inscription (::):**",
            "   Binds a string soul directly to a path coordinate.",
            "   - **Inline:** `README.md :: \"# My Project\"`",
            "   - **Block (Triple-Quotes):**",
            "     ```scaffold",
            "     src/main.py :: \"\"\"",
            "     import os",
            "     print(\"Reality Awakened\")",
            "     \"\"\"",
            "     ```",
            "",
            "2. **Topographical Anchoring:**",
            "   - **Directory:** End a path with `/` to forge a sanctum. `src/core/`.",
            "   - **Implicit Tree:** A path indented under a directory lives inside it.",
            "",
            "3. **Celestial Seeding (<<):**",
            "   Clones the soul of an external template or file shard.",
            "   - `Dockerfile << templates/fastapi.dockerfile`",
            "",
            "4. **Spatiotemporal Bridges (->):**",
            "   Forges a symbolic link on the physical substrate.",
            "   - `logs/current.log -> ./artifacts/latest.log`",
            "",
            "5. **Jurisprudential Wards (%%):**",
            "   - **Permissions:** `scripts/strike.sh :: \"...\" %% 755`",
            "   - **Named Modes:** `vault/secret.key :: \"...\" %% secret`"
        ])
    },
    {
        "id": "symphony_will_and_metabolism",
        "tags": ["symphony", "will", "automation", "edicts", "vows"],
        "content": "\n".join([
            "# Stratum III: The Language of Will (Metabolism)",
            "",
            "Symphonies (.symphony) define the kinetic metabolism of a project.",
            "",
            "1. **Action Edicts (>>):**",
            "   The Hand of the Maestro. Executes shell commands.",
            "   - `>> poetry install`",
            "   - **State Capture:** `>> git rev-parse HEAD as commit_sha`",
            "",
            "2. **Vow Edicts (??):**",
            "   The Conscience of the Maestro. Empirical assertions.",
            "   - `?? succeeds` (Assert last command exit 0)",
            "   - `?? file_exists: \"pyproject.toml\"`",
            "   - `?? port_open: 8080`",
            "",
            "3. **State Edicts (%%):**",
            "   The Mind of the Maestro. Transmutes internal reality.",
            "   - `%% let: mode = \"production\"`",
            "   - `%% sanctum: ./src` (Change Directory)",
            "   - `%% proclaim: \"Reality is RESONANT\"` (High-Status Log)",
            "",
            "4. **The Polyglot Wormhole (py: / js:):**",
            "   Execute high-order logic directly in Python or Node.js.",
            "   ```symphony",
            "   py:",
            "       import os",
            "       return len(os.listdir('.'))",
            "   as file_count",
            "   ```"
        ])
    },
    {
        "id": "advanced_metaphysics",
        "tags": ["macro", "task", "trait", "contract", "advanced"],
        "content": "\n".join([
            "# Stratum IV: Advanced Metaphysics",
            "",
            "1. **Gnostic Macros (@macro):**",
            "   Define reusable architectural patterns.",
            "   ```scaffold",
            "   @macro forge_service(name):",
            "       src/services/!{name}.py :: \"class !{name}Service: pass\"",
            "   @endmacro",
            "   ",
            "   @call forge_service(\"Auth\")",
            "   ```",
            "",
            "2. **Gnostic Contracts (%% contract):**",
            "   Define the immutable laws of data structures.",
            "   ```scaffold",
            "   %% contract User:",
            "       id: uuid",
            "       username: str(min=3)",
            "       email: email",
            "   ```",
            "",
            "3. **Resilience Wards (@try / @catch):**",
            "   Handle fractures in the timeline autonomicly.",
            "   ```symphony",
            "   @try",
            "       >> npm install",
            "   @catch",
            "       %% proclaim: \"Summoning failed. Retrying with lustration...\"",
            "       >> rm -rf node_modules && npm install",
            "   @end",
            "   ```",
            "",
            "4. **Achronal Lifecycle Blocks:**",
            "   - `%% post-run`: Kinetic edicts executed after the Form is manifest.",
            "   - `%% on-heresy`: The Phoenix Protocol. Redemption rites for failed strikes.",
            "   - `%% on-undo`: The Chronomancer's path for reversing a reality shift."
        ])
    },
    {
        "id": "the_architects_best_practices",
        "tags": ["best_practices", "sovereignty", "integrity", "philosophy"],
        "content": "\n".join([
            "# Stratum V: The Architect's Jurisprudence",
            "",
            "1. **Sovereignty:** Never hardcode project-specific names. Use `{{ project_slug }}`.",
            "2. **Integrity:** Every `>> Action` should be warded by a `?? Vow`.",
            "3. **Purity:** Keep secrets in the Vault. Summon them via `{{ env('KEY') }}`.",
            "4. **Geometry:** Use 4-space indentation for absolute topological resonance.",
            "5. **Causality:** Use `@include` to build a library of warded Gnostic Shards.",
            "6. **Amnesty:** Leverage the SGF's Absolute Amnesty to include raw code fragments in your blueprints.",
            "",
            "**Final Truth:** The blueprint is not a template; it is the source code of the Universe."
        ])
    }
]