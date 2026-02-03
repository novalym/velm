# Path: scaffold/core/ai/rag/knowledge/scaffold_syntax.py
# -------------------------------------------------------

SCAFFOLD_SHARDS = [
    {
        "id": "scaffold_syntax_basics",
        "tags": ["scaffold", "syntax", "blueprint", "file_creation", "basics"],
        "content": "\n".join([
            "# Scaffold Blueprint Syntax: The Basics",
            "",
            "1. **File Creation (Inline):**",
            "   Use the `::` sigil to define content inline.",
            "   Syntax: `path/to/file.ext :: \"content\"`",
            "   Example:",
            "   `src/main.py :: \"print('Hello World')\"`",
            "",
            "2. **File Creation (Block):**",
            "   Use triple quotes for multi-line content.",
            "   Example:",
            "   ```scaffold",
            "   src/config.json :: \"\"\"",
            "   {",
            "     \"debug\": true",
            "   }",
            "   \"\"\"",
            "   ```",
            "",
            "3. **Directory Creation:**",
            "   End a path with `/` to explicitly create a directory.",
            "   Example: `src/utils/`",
            "",
            "4. **Variable Definition:**",
            "   Use `$$` to define Gnostic Variables.",
            "   Syntax: `$$ key = value`",
            "   Example: `$$ project_name = \"nexus-core\"`",
            "",
            "5. **Variable Usage:**",
            "   Use Jinja2 syntax to inject variables.",
            "   Example: `README.md :: \"# {{ project_name }}\"`"
        ])
    },
    {
        "id": "scaffold_syntax_advanced",
        "tags": ["scaffold", "syntax", "advanced", "seed", "permissions"],
        "content": "\n".join([
            "# Scaffold Blueprint Syntax: Advanced Rites",
            "",
            "1. **External Seeding (<<):**",
            "   Copy content from an existing file (template) instead of writing it inline.",
            "   Syntax: `target_path << source_path`",
            "   Example: `Dockerfile << templates/python.dockerfile`",
            "",
            "2. **Permissions (%%):**",
            "   Set file permissions using the `%%` sigil.",
            "   Syntax: `path :: \"content\" %% 755`",
            "   Example: `scripts/deploy.sh :: \"echo 'Deploying'\" %% 755`",
            "",
            "3. **Directives (@):**",
            "   Use `@` for meta-instructions.",
            "   - `@if {{ condition }}`: Conditional generation.",
            "   - `@include \"path\"`: Include another blueprint.",
            "",
            "   Example:",
            "   ```scaffold",
            "   @if {{ use_docker }}",
            "       Dockerfile :: \"FROM alpine\"",
            "   @endif",
            "   ```"
        ])
    }
]