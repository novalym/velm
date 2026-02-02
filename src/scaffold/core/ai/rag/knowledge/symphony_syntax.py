# Path: scaffold/core/ai/rag/knowledge/symphony_syntax.py
# -------------------------------------------------------

SYMPHONY_SHARDS = [
    {
        "id": "symphony_syntax_core",
        "tags": ["symphony", "syntax", "automation", "scripting", "commands"],
        "content": "\n".join([
            "# Symphony Syntax: The Language of Will",
            "",
            "Symphony files (`.symphony`) define executable workflows.",
            "",
            "1. **Action Edict (>>):**",
            "   Executes a shell command.",
            "   Syntax: `>> command`",
            "   Example: `>> npm install`",
            "",
            "2. **Vow Edict (??):**",
            "   Asserts a truth. If false, the Symphony halts.",
            "   Syntax: `?? predicate: args`",
            "   Example: `?? file_exists: package.json`",
            "   Example: `?? succeeds` (Checks if previous command exit code was 0)",
            "",
            "3. **State Edict (%%):**",
            "   Modifies the internal state of the Conductor.",
            "   Syntax: `%% key: value`",
            "   Example: `%% sanctum: ./src` (Changes CWD)",
            "   Example: `%% let: version = \"1.0.0\"`"
        ])
    },
    {
        "id": "symphony_syntax_structures",
        "tags": ["symphony", "syntax", "logic", "loops", "error_handling"],
        "content": "\n".join([
            "# Symphony Syntax: Structural Logic",
            "",
            "1. **Loops (@for):**",
            "   Iterate over a list.",
            "   ```symphony",
            "   @for service in {{ services }}",
            "       >> echo \"Deploying {{ service }}\"",
            "   @endfor",
            "   ```",
            "",
            "2. **Resilience (@try):**",
            "   Handle failures gracefully.",
            "   ```symphony",
            "   @try:",
            "       >> ./risky_script.sh",
            "   @catch:",
            "       >> echo \"Recovery mode engaged\"",
            "   @endtry",
            "   ```",
            "",
            "3. **Parallelism (&&:):**",
            "   Run commands concurrently.",
            "   ```symphony",
            "   &&:",
            "       >> npm run build:frontend",
            "       >> cargo build --release",
            "   @end",
            "   ```"
        ])
    }
]