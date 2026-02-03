# Path: scaffold/core/ai/rag/knowledge/security_gnosis.py
# -------------------------------------------------------

SECURITY_SHARDS = [
    {
        "id": "security_secrets_management",
        "tags": ["security", "secrets", "env", "config"],
        "content": "\n".join([
            "# The Law of Secrets",
            "",
            "1. **Never Commit Secrets:**",
            "   API Keys, Passwords, and Tokens must NEVER be written into code or committed to Git.",
            "",
            "2. **Environment Variables:**",
            "   Use `.env` files for local development (add to `.gitignore`).",
            "   Use `os.getenv()` or `process.env` to access them.",
            "",
            "3. **Validation:**",
            "   Fail fast if a secret is missing.",
            "",
            "   *Python (Pydantic):*",
            "   ```python",
            "   class Settings(BaseSettings):",
            "       db_password: str # Will raise error if missing",
            "   ```"
        ])
    },
    {
        "id": "security_input_validation",
        "tags": ["security", "validation", "input"],
        "content": "\n".join([
            "# The Law of Input Validation",
            "",
            "1. **Trust No One:**",
            "   Treat all user input as hostile.",
            "",
            "2. **Type Safety:**",
            "   Use Pydantic (Python) or Zod (TypeScript) to enforce schemas at the edge.",
            "",
            "3. **Sanitization:**",
            "   Escape HTML output to prevent XSS.",
            "   Use parameterized queries to prevent SQL Injection."
        ])
    }
]