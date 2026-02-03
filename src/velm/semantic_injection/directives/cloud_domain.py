# scaffold/semantic_injection/directives/cloud_domain.py

"""
=================================================================================
== THE ARCHITECT OF THE SKY (V-Ω-CLOUD-DOMAIN)                                 ==
=================================================================================
LIF: 50,000,000,000

This artisan implements the `@cloud` namespace. It automates the toil of
infrastructure configuration, forging best-practice Dockerfiles and CI pipelines.

Usage:
    Dockerfile :: @cloud/dockerfile(stack="python", version="3.11", port=8000)
    docker-compose.yml :: @cloud/compose(services=["postgres", "redis"])
    .github/workflows/ci.yml :: @cloud/ci(type="python-test")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("cloud")
class CloudDomain(BaseDirectiveDomain):
    """
    The God-Engine of Infrastructure as Code.
    """

    @property
    def namespace(self) -> str:
        return "cloud"

    def help(self) -> str:
        return "Generates Infrastructure (Dockerfiles, Compose, CI/CD)."

    # =========================================================================
    # == THE RITE OF CONTAINERIZATION                                        ==
    # =========================================================================

    def _directive_dockerfile(self, context: Dict[str, Any], stack: str = "python", version: str = "latest",
                              port: int = 8000, cmd: str = "") -> str:
        """
        @cloud/dockerfile(stack="python", version="3.11", port=8000)
        Forges a production-ready, multi-stage Dockerfile.
        """
        stack = stack.lower()

        if stack == "python":
            start_cmd = cmd or '["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]'
            return dedent(f"""
                # --- Stage 1: Builder ---
                FROM python:{version}-slim as builder

                WORKDIR /app
                ENV PYTHONDONTWRITEBYTECODE 1
                ENV PYTHONUNBUFFERED 1

                RUN apt-get update && apt-get install -y --no-install-recommends gcc

                COPY requirements.txt .
                RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

                # --- Stage 2: Final ---
                FROM python:{version}-slim

                WORKDIR /app

                COPY --from=builder /app/wheels /wheels
                COPY --from=builder /app/requirements.txt .

                RUN pip install --no-cache /wheels/*

                COPY src/ ./src/

                EXPOSE {port}

                CMD {start_cmd}
            """).strip()

        elif stack == "node":
            start_cmd = cmd or '["npm", "start"]'
            return dedent(f"""
                # --- Stage 1: Builder ---
                FROM node:{version}-alpine AS builder
                WORKDIR /app
                COPY package*.json ./
                RUN npm ci
                COPY . .
                RUN npm run build

                # --- Stage 2: Runner ---
                FROM node:{version}-alpine
                WORKDIR /app
                COPY --from=builder /app/dist ./dist
                COPY --from=builder /app/node_modules ./node_modules
                COPY package*.json ./

                EXPOSE {port}
                CMD {start_cmd}
            """).strip()

        elif stack == "go":
            return dedent(f"""
                # --- Stage 1: Builder ---
                FROM golang:{version}-alpine AS builder
                WORKDIR /app
                COPY go.mod go.sum ./
                RUN go mod download
                COPY . .
                RUN go build -o /main ./cmd/server

                # --- Stage 2: Runner ---
                FROM alpine:latest
                WORKDIR /root/
                COPY --from=builder /main .

                EXPOSE {port}
                CMD ["./main"]
            """).strip()

        return f"# Unknown stack '{stack}'. Please forge manually."

    def _directive_compose(self, context: Dict[str, Any], services: List[str] = None) -> str:
        """
        @cloud/compose(services=["postgres", "redis"])
        Forges a docker-compose.yml with selected backing services.
        """
        if services is None: services = []

        header = dedent("""
            version: '3.8'

            services:
              app:
                build: .
                ports:
                  - "${PORT:-8000}:8000"
                env_file:
                  - .env
        """).strip()

        extras = []

        if "postgres" in services:
            extras.append(dedent("""
              db:
                image: postgres:15-alpine
                volumes:
                  - postgres_data:/var/lib/postgresql/data
                environment:
                  POSTGRES_USER: ${DB_USER:-user}
                  POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
                  POSTGRES_DB: ${DB_NAME:-app_db}
                ports:
                  - "5432:5432"
            """).strip())

        if "redis" in services:
            extras.append(dedent("""
              redis:
                image: redis:7-alpine
                ports:
                  - "6379:6379"
            """).strip())

        volumes_block = "\nvolumes:\n  postgres_data:" if "postgres" in services else ""

        body = "\n  ".join(extras)
        return f"{header}\n  {body}{volumes_block}"

    # =========================================================================
    # == THE RITE OF CONTINUOUS INTEGRATION                                  ==
    # =========================================================================

    def _directive_ci(self, context: Dict[str, Any], provider: str = "github", type: str = "python-test") -> str:
        """
        @cloud/ci(type="python-test")
        Forges a CI/CD pipeline configuration.
        """
        if provider == "github":
            if type == "python-test":
                return dedent("""
                    name: Python CI

                    on: [push, pull_request]

                    jobs:
                      test:
                        runs-on: ubuntu-latest
                        steps:
                          - uses: actions/checkout@v3
                          - name: Set up Python
                            uses: actions/setup-python@v4
                            with:
                              python-version: '3.11'
                          - name: Install dependencies
                            run: |
                              python -m pip install --upgrade pip
                              pip install -r requirements.txt
                          - name: Test with pytest
                            run: |
                              pip install pytest
                              pytest
                """).strip()

            if type == "node-test":
                return dedent("""
                    name: Node CI

                    on: [push, pull_request]

                    jobs:
                      build:
                        runs-on: ubuntu-latest
                        steps:
                          - uses: actions/checkout@v3
                          - name: Use Node.js
                            uses: actions/setup-node@v3
                            with:
                              node-version: '20.x'
                          - run: npm ci
                          - run: npm run build --if-present
                          - run: npm test
                """).strip()

        return f"# CI Configuration for {provider}/{type} not yet in the Grimoire."