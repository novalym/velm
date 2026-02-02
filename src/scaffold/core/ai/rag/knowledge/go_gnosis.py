# Path: scaffold/core/ai/rag/knowledge/go_gnosis.py
# -------------------------------------------------

GO_SHARDS = [
    {
        "id": "go_project_layout",
        "tags": ["go", "golang", "structure", "backend"],
        "content": "\n".join([
            "# Standard Go Project Layout",
            "",
            "1. **`cmd/`:**",
            "   Main applications. e.g., `cmd/server/main.go`.",
            "",
            "2. **`internal/`:**",
            "   Private application and library code. Cannot be imported by others.",
            "",
            "3. **`pkg/`:**",
            "   Library code that is ok to use by external applications (use sparingly).",
            "",
            "4. **`api/`:**",
            "   OpenAPI/Swagger specs, JSON schema files, protocol definition files.",
            "",
            "5. **Dependency Injection:**",
            "   Prefer explicit injection (passing structs) over global state or complex DI frameworks."
        ])
    }
]