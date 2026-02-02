# Path: scaffold/core/ai/rag/knowledge/python_gnosis.py
# -----------------------------------------------------

PYTHON_SHARDS = [
    {
        "id": "arch_python_fastapi",
        "tags": ["python", "fastapi", "backend", "api", "architecture"],
        "content": "\n".join([
            "# FastAPI Clean Architecture Pattern",
            "",
            "To forge a scalable FastAPI application, adhere to this topography:",
            "",
            "1. **`src/api/routes/`**: ",
            "   Contains the Router definitions. ",
            "   - **Rule:** Minimal logic. Validate input, call Service, return Response.",
            "",
            "2. **`src/services/`**: ",
            "   Contains the Business Logic.",
            "   - **Rule:** Pure Python. No HTTP dependencies. Accepts Pydantic models or primitives.",
            "",
            "3. **`src/repositories/`**: ",
            "   Contains Data Access Logic (SQLAlchemy/Prisma).",
            "   - **Rule:** Only this layer touches the database.",
            "",
            "4. **`src/models/`**: ",
            "   Contains Pydantic Schemas (DTOs) and ORM Models.",
            "",
            "5. **`src/core/config.py`**: ",
            "   Uses `pydantic-settings` to manage environment variables."
        ])
    },
    {
        "id": "python_modern_standards",
        "tags": ["python", "standards", "typing", "pep8"],
        "content": "\n".join([
            "# Modern Python Standards (The Gnostic Way)",
            "",
            "1. **Typing:** ",
            "   Use `typing` or standard collections (Python 3.9+). ",
            "   Always use Type Hints.",
            "   Example: `def connect(url: str) -> bool:`",
            "",
            "2. **Imports:**",
            "   Use absolute imports for clarity.",
            "   `from src.core.config import settings`",
            "",
            "3. **Async:**",
            "   Prefer `async/await` for I/O bound operations (DB, Network).",
            "",
            "4. **Testing:**",
            "   Use `pytest`. Place tests in `tests/` mirroring the `src/` structure."
        ])
    }
]