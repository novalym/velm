# Path: scaffold/core/ai/rag/knowledge/devops_gnosis.py
# -----------------------------------------------------

DEVOPS_SHARDS = [
    {
        "id": "devops_docker_python",
        "tags": ["docker", "python", "devops", "container"],
        "content": "\n".join([
            "# Python Docker Best Practices (The Distroless Vow)",
            "",
            "1. **Multi-Stage Build:**",
            "   Use a `builder` stage to compile dependencies and a `runner` stage for the final image.",
            "",
            "2. **Base Image:**",
            "   Use `python:3.11-slim` for the builder.",
            "   Use `gcr.io/distroless/python3-debian12` for the runner (if possible) or `slim`.",
            "",
            "3. **Environment:**",
            "   Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`.",
            "",
            "4. **User:**",
            "   Never run as root. Create a `nonroot` user or use the one provided by Distroless.",
            "",
            "**Example:**",
            "```dockerfile",
            "FROM python:3.11-slim as builder",
            "WORKDIR /app",
            "COPY requirements.txt .",
            "RUN pip install --no-cache-dir -r requirements.txt",
            "",
            "FROM python:3.11-slim",
            "WORKDIR /app",
            "COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages",
            "COPY . .",
            "USER 1000",
            "CMD [\"python\", \"src/main.py\"]",
            "```"
        ])
    },
    {
        "id": "devops_ci_github",
        "tags": ["github", "actions", "ci", "cd"],
        "content": "\n".join([
            "# GitHub Actions Gnosis",
            "",
            "1. **Triggers:**",
            "   Use `on: [push, pull_request]` to guard the main branch.",
            "",
            "2. **Caching:**",
            "   Always cache dependencies (`actions/cache`) to speed up builds.",
            "   - Python: Cache `~/.cache/pip`",
            "   - Node: Cache `~/.npm`",
            "",
            "3. **Permissions:**",
            "   Set `permissions: contents: read` at the top level. Grant write only where needed.",
            "",
            "4. **Secrets:**",
            "   Never echo secrets. Use `${{ secrets.KEY }}`."
        ])
    }
]