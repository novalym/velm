# Path: src/velm/codex/atoms/stack.py
# -----------------------------------

"""
=================================================================================
== THE BACKEND WEAVER: OMEGA TOTALITY (V-Ω-TOTALITY-V100-STACK-DOMAIN)         ==
=================================================================================
LIF: INFINITY | ROLE: BACKEND_ARCHITECTURE_FORGE | RANK: OMEGA_SOVEREIGN

This artisan implements the `@stack` (or `stack.*`) namespace. It is the high-level
conductor responsible for weaving the internal logic of an application. It
bridges the gap between Data Modeling, API Design, and Business Logic.

Usage:
    # Forge a Python/FastAPI Fortress
    main.py        :: {{ stack.fastapi(auth=True, db="postgres") }}
    models.py      :: {{ stack.sqlalchemy(name="User", fields="id:uuid, email:str") }}

    # Forge a TypeScript/Node Sanctum
    schema.prisma  :: {{ stack.prisma(provider="postgresql") }}
    server.ts      :: {{ stack.express(port=3000, middleware=["auth", "logger"]) }}
=================================================================================
"""

import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, require_binaries
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("BackendWeaver")


@domain("stack")
class StackDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE SOVEREIGN BACKEND WEAVER                                            ==
    =============================================================================
    Materializes the Mind and Memory of the application.
    """

    @property
    def namespace(self) -> str:
        return "stack"

    def help(self) -> str:
        return "Generates Backend Fortresses (FastAPI, Express, Fiber) and Data Layers (SQLAlchemy, Prisma, GORM)."

    # =========================================================================
    # == STRATUM 0: THE DATA MEMORY (ORMS)                                   ==
    # =========================================================================

    def _directive_prisma(self,
                          context: Dict[str, Any],
                          provider: str = "postgresql",
                          models: List[str] = None) -> str:
        """
        stack.prisma(provider="postgresql", models=["User", "Post"])

        [ASCENSION 1]: Forges an extensive, production-ready Prisma schema.
        """
        p = provider.lower()
        url_val = 'env("DATABASE_URL")'
        if p == "sqlite": url_val = '"file:./dev.db"'

        return dedent(f"""
            // === GNOSTIC DATA SCHEMA: PRISMA ===
            // Forged via VELM God-Engine

            generator client {{
              provider = "prisma-client-js"
              previewFeatures = ["fullTextSearch", "metrics"]
            }}

            datasource db {{
              provider = "{p}"
              url      = {url_val}
            }}

            // --- STRATUM: IDENTITY ---
            model User {{
              id            String    @id @default(cuid())
              email         String    @unique
              name          String?
              role          Role      @default(USER)
              isActive      Boolean   @default(true)
              lastLogin     DateTime?
              createdAt     DateTime  @default(now())
              updatedAt     DateTime  @updatedAt

              // Relations
              posts         Post[]
              profile       Profile?

              @@index([email])
              @@map("users")
            }}

            model Profile {{
              id     Int     @id @default(autoincrement())
              bio    String?
              userId String  @unique
              user   User    @relation(fields: [userId], references: [id])
            }}

            // --- STRATUM: CONTENT ---
            model Post {{
              id        Int      @id @default(autoincrement())
              title     String
              content   String?
              published Boolean  @default(false)
              authorId  String
              author    User     @relation(fields: [authorId], references: [id])
              createdAt DateTime @default(now())
              updatedAt DateTime @updatedAt

              @@index([authorId])
              @@map("posts")
            }}

            enum Role {{
              USER
              ADMIN
              ARCHITECT
            }}
        """).strip()

    def _directive_sqlalchemy(self,
                              context: Dict[str, Any],
                              name: str = "Entity",
                              fields: str = "id:uuid, created_at:datetime") -> str:
        """
        stack.sqlalchemy(name="User", fields="id:uuid, email:str, is_active:bool")

        [ASCENSION 1]: Forges a modern SQLAlchemy 2.0 Async model.
        """
        parsed_fields = self._parse_fields_logic(fields)

        class_lines = [f"class {name}(Base, TimestampMixin):"]
        class_lines.append(f"    __tablename__ = \"{name.lower()}s\"")
        class_lines.append("")

        imports = {"from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey",
                   "from sqlalchemy.orm import relationship",
                   "from sqlalchemy.sql import func"}

        for fname, ftype in parsed_fields:
            if ftype == "uuid":
                imports.add("from sqlalchemy.dialects.postgresql import UUID")
                imports.add("import uuid")
                class_lines.append(f"    {fname} = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)")
            elif ftype == "str":
                class_lines.append(f"    {fname} = Column(String, index=True)")
            elif ftype == "int":
                class_lines.append(f"    {fname} = Column(Integer)")
            elif ftype == "bool":
                class_lines.append(f"    {fname} = Column(Boolean, default=True)")
            elif ftype == "datetime":
                class_lines.append(f"    {fname} = Column(DateTime(timezone=True), server_default=func.now())")

        return "\n".join(sorted(list(imports))) + "\n\n" + "\n".join(class_lines)

    # =========================================================================
    # == STRATUM 1: THE INTELLIGENCE GATEWAYS (SERVERS)                      ==
    # =========================================================================

    def _directive_fastapi(self,
                           context: Dict[str, Any],
                           title: str = "Nexus API",
                           auth: bool = True,
                           db: str = "postgres") -> str:
        """
        stack.fastapi(auth=True)

        [ASCENSION 3 & 5]: The Pythonic gold standard.
        Materializes a robust FastAPI entrypoint with a complete Lifespan and DI setup.
        """
        project_name = context.get("project_name", "VelmApp")

        return dedent(f"""
            # === GNOSTIC FORTRESS: FASTAPI (TOTALITY) ===
            import time
            from contextlib import asynccontextmanager
            from fastapi import FastAPI, Request, status
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.responses import JSONResponse
            from loguru import logger

            # [STRATUM: CONFIG]
            from .core.config import settings
            from .api.v1.router import api_router

            @asynccontextmanager
            async def lifespan(app: FastAPI):
                # --- MOVEMENT I: AWAKENING ---
                logger.info("🚀 {{}} Awakening...", settings.APP_NAME)
                # Initialize DB Pools / Redis here
                yield
                # --- MOVEMENT II: DISSOLUTION ---
                logger.info("🌑 {{}} Dissolving reality...", settings.APP_NAME)
                # Close connections gracefully

            app = FastAPI(
                title="{title}",
                version="1.0.0-Ω",
                lifespan=lifespan,
                docs_url="/docs" if settings.ENVIRONMENT == "development" else None
            )

            # [STRATUM: DEFENSE]
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"], # Tighten in .env
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            @app.middleware("http")
            async def metabolic_telemetry_middleware(request: Request, call_next):
                start_time = time.perf_counter()
                response = await call_next(request)
                process_time = (time.perf_counter() - start_time) * 1000
                response.headers["X-Metabolic-Tax-MS"] = f"{{process_time:.2f}}"
                return response

            # [STRATUM: DISPATCH]
            app.include_router(api_router, prefix="/api/v1")

            @app.get("/health", tags=["Vitality"])
            async def health_check():
                return {{"status": "RESONANT", "timestamp": time.time()}}

            @app.exception_handler(Exception)
            async def universal_heresy_handler(request: Request, exc: Exception):
                logger.error(f"UNHANDLED_PARADOX: {{exc}}")
                return JSONResponse(
                    status_code=500,
                    content={{"success": False, "error": "INTERNAL_FRACTURE", "message": str(exc)}}
                )
        """).strip()

    def _directive_express(self,
                           context: Dict[str, Any],
                           port: int = 3000,
                           middleware: List[str] = None) -> str:
        """
        stack.express(port=3000, middleware=["auth", "logger"])

        [ASCENSION 5]: Materializes a high-status ESM-First Express server.
        """
        m_list = middleware or ["helmet", "cors", "morgan"]

        return dedent(f"""
            /**
             * === GNOSTIC SANCTUM: EXPRESS.JS (TOTALITY) ===
             * Substrate: Node.js / TypeScript
             */
            import express from 'express';
            import helmet from 'helmet';
            import cors from 'cors';
            import morgan from 'morgan';
            import {{ createServer }} from 'http';
            import {{ config }} from './core/config.js';
            import {{ router }} from './routes/v1/index.js';
            import {{ errorHandler }} from './middleware/error.js';

            const app = express();
            const PORT = config.PORT || {port};

            // --- MOVEMENT I: THE SHIELD (MIDDLEWARE) ---
            app.use(helmet());
            app.use(cors());
            app.use(morgan('dev'));
            app.use(express.json({{ limit: '10kb' }}));
            app.use(express.urlencoded({{ extended: true }}));

            // --- MOVEMENT II: THE DISPATCH (ROUTES) ---
            app.get('/health', (req, res) => res.json({{ status: 'RESONANT', ts: Date.now() }}));
            app.use('/api/v1', router);

            // --- MOVEMENT III: THE REDEMPTION (ERROR HANDLING) ---
            app.use(errorHandler);

            const server = createServer(app);

            server.listen(PORT, () => {{
              console.log(`🚀 Citadel manifest at http://localhost:${{PORT}}`);
            }});

            // Graceful Shutdown
            process.on('SIGTERM', () => {{
              console.log('🌑 Signal perceived. Sealing the gates...');
              server.close(() => process.exit(0));
            }});
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE DATA VESSELS (DTO / SCHEMAS)                        ==
    # =========================================================================

    def _directive_dto(self,
                       context: Dict[str, Any],
                       name: str,
                       fields: str,
                       lang: str = "python") -> str:
        """
        stack.dto(name="UserCreate", fields="email:str, password:str")

        [ASCENSION 2]: Forges strict validation models.
        """
        parsed = self._parse_fields_logic(fields)

        if lang == "python":
            lines = [f"class {name}(BaseModel):"]
            for f_name, f_type in parsed:
                # Handle basic type mapping
                t_map = {"str": "str", "int": "int", "float": "float", "bool": "bool", "uuid": "UUID"}
                lines.append(f"    {f_name}: {t_map.get(f_type, 'Any')}")
            return "from pydantic import BaseModel\nfrom typing import Any\nfrom uuid import UUID\n\n" + "\n".join(
                lines)

        elif lang == "typescript":
            lines = [f"export const {name}Schema = z.object({{"]
            for f_name, f_type in parsed:
                t_map = {"str": "z.string()", "int": "z.number().int()", "float": "z.number()", "bool": "z.boolean()",
                         "uuid": "z.string().uuid()"}
                lines.append(f"  {f_name}: {t_map.get(f_type, 'z.any()')},")
            lines.append("});")
            lines.append(f"\nexport type {name} = z.infer<typeof {name}Schema>;")
            return "import { z } from 'zod';\n\n" + "\n".join(lines)

        return f"# Unknown DTO language: {lang}"

    # =========================================================================
    # == STRATUM 3: THE KINETIC CLIENTS (MIRRORS)                            ==
    # =========================================================================

    def _directive_fetch_client(self,
                                context: Dict[str, Any],
                                base_url: str = "/api/v1") -> str:
        """
        stack.fetch_client(base_url="/api/v1")

        [ASCENSION 9]: Forges a robust, interceptor-ready Fetch client.
        """
        return dedent(f"""
            /**
             * === GNOSTIC CLIENT: FETCH MIRROR ===
             * Centralized communication hub.
             */
            const BASE_URL = "{base_url}";

            interface RequestOptions extends RequestInit {{
              params?: Record<string, string>;
            }}

            export async function apiRequest<T>(endpoint: string, options: RequestOptions = {{}}): Promise<T> {{
              const url = new URL(`${{BASE_URL}}${{endpoint}}`, window.location.origin);

              if (options.params) {{
                Object.entries(options.params).forEach(([key, val]) => url.searchParams.append(key, val));
              }}

              const response = await fetch(url.toString(), {{
                ...options,
                headers: {{
                  'Content-Type': 'application/json',
                  'X-Gnostic-Trace': crypto.randomUUID(),
                  ...options.headers,
                }},
              }});

              if (!response.ok) {{
                const heresy = await response.json().catch(() => ({{ message: 'Unknown Paradox' }}));
                throw new Error(heresy.message || 'Network Fracture');
              }}

              return response.json();
            }}

            export const api = {{
              get: <T>(url: string, params?: any) => apiRequest<T>(url, {{ method: 'GET', params }}),
              post: <T>(url: string, body: any) => apiRequest<T>(url, {{ method: 'POST', body: JSON.stringify(body) }}),
              put: <T>(url: string, body: any) => apiRequest<T>(url, {{ method: 'PUT', body: JSON.stringify(body) }}),
              delete: <T>(url: string) => apiRequest<T>(url, {{ method: 'DELETE' }}),
            }};
        """).strip()

    # =========================================================================
    # == STRATUM 4: THE ARCHITECTURAL REPOSITORY                            ==
    # =========================================================================

    def _directive_repository(self,
                              context: Dict[str, Any],
                              name: str,
                              model: str) -> str:
        """
        stack.repository(name="User", model="User")

        [ASCENSION 7]: Implements the Repository pattern for data decoupling.
        """
        return dedent(f"""
            from typing import List, Optional
            from sqlalchemy.ext.asyncio import AsyncSession
            from sqlalchemy import select
            from ..models.{model.lower()} import {model}

            class {name}Repository:
                \"\"\"Encapsulates all persistence logic for {model}.\"\"\"

                def __init__(self, session: AsyncSession):
                    self.session = session

                async def get_by_id(self, id: str) -> Optional[{model}]:
                    result = await self.session.execute(select({model}).where({model}.id == id))
                    return result.scalar_one_or_none()

                async def list_all(self, limit: int = 100) -> List[{model}]:
                    result = await self.session.execute(select({model}).limit(limit))
                    return list(result.scalars().all())

                async def add(self, entity: {model}):
                    self.session.add(entity)
                    await self.session.flush()
                    return entity
        """).strip()

    # =========================================================================
    # == INTERNAL RITES                                                      ==
    # =========================================================================

    def _parse_fields_logic(self, fields_str: str) -> List[Tuple[str, str]]:
        """Parses "id:uuid, email:str" into structured tuples."""
        pairs = []
        for part in fields_str.split(','):
            if ':' in part:
                k, v = part.split(':', 1)
                pairs.append((k.strip(), v.strip().lower()))
            else:
                pairs.append((part.strip(), 'str'))
        return pairs