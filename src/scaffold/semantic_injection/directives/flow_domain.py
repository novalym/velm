# scaffold/semantic_injection/directives/stack_domain.py

"""
=================================================================================
== THE BACKEND WEAVER (V-Ω-STACK-DOMAIN)                                       ==
=================================================================================
LIF: 100,000,000,000

This artisan implements the `@stack` namespace. It handles the heavy lifting of
backend configuration.

Usage:
    schema.prisma :: @stack/prisma(provider="postgresql")
    src/api.ts    :: @stack/fetch_client(base_url="/api/v1")
    server.js     :: @stack/express(port=3000)
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("stack")
class StackDomain(BaseDirectiveDomain):
    """
    The Glue of the Cosmos.
    """

    @property
    def namespace(self) -> str:
        return "stack"

    def help(self) -> str:
        return "Generates backend stack boilerplate (Prisma, API Clients, Servers)."

    def _directive_prisma(self, context: Dict[str, Any], provider: str = "sqlite", *args, **kwargs) -> str:
        """
        @stack/prisma(provider="postgresql")
        Generates a Prisma Schema with a sample User model.
        """
        url_env = "file:./dev.db" if provider == "sqlite" else "env(\"DATABASE_URL\")"

        return dedent(f"""
            // This is your Prisma schema file,
            // learn more about it in the docs: https://pris.ly/d/prisma-schema

            generator client {{
              provider = "prisma-client-js"
            }}

            datasource db {{
              provider = "{provider}"
              url      = "{url_env}"
            }}

            model User {{
              id        String   @id @default(cuid())
              email     String   @unique
              name      String?
              createdAt DateTime @default(now())
              updatedAt DateTime @updatedAt

              posts     Post[]
            }}

            model Post {{
              id        String   @id @default(cuid())
              title     String
              content   String?
              published Boolean  @default(false)
              authorId  String
              author    User     @relation(fields: [authorId], references: [id])
            }}
        """).strip()

    def _directive_fetch_client(self, context: Dict[str, Any], base_url: str = "/api", *args, **kwargs) -> str:
        """
        @stack/fetch_client(base_url="/api/v1")
        Generates a typed fetch wrapper for the frontend.
        """
        return dedent(f"""
            // Typed Fetch Wrapper
            const BASE_URL = "{base_url}";

            interface ApiError {{
                message: string;
                status: number;
            }}

            async function request<T>(endpoint: string, options: RequestInit = {{}}): Promise<T> {{
                const url = `${{BASE_URL}}${{endpoint}}`;
                const headers = {{
                    'Content-Type': 'application/json',
                    ...options.headers,
                }};

                const response = await fetch(url, {{ ...options, headers }});

                if (!response.ok) {{
                    const error: ApiError = {{
                        message: await response.text(),
                        status: response.status,
                    }};
                    throw error;
                }}

                try {{
                    return await response.json();
                }} catch (e) {{
                    return null as unknown as T;
                }}
            }}

            export const api = {{
                get: <T>(url: string) => request<T>(url),
                post: <T>(url: string, body: any) => request<T>(url, {{ method: 'POST', body: JSON.stringify(body) }}),
                put: <T>(url: string, body: any) => request<T>(url, {{ method: 'PUT', body: JSON.stringify(body) }}),
                del: <T>(url: string) => request<T>(url, {{ method: 'DELETE' }}),
            }};
        """).strip()

    def _directive_express(self, context: Dict[str, Any], port: int = 3000, *args, **kwargs) -> str:
        """
        @stack/express(port=3000)
        Generates a robust Express.js server entry point.
        """
        return dedent(f"""
            const express = require('express');
            const cors = require('cors');
            const helmet = require('helmet');
            const morgan = require('morgan');

            const app = express();
            const PORT = process.env.PORT || {port};

            // Middleware
            app.use(helmet());
            app.use(cors());
            app.use(morgan('dev'));
            app.use(express.json());

            // Health Check
            app.get('/health', (req, res) => {{
                res.status(200).json({{ status: 'ok', timestamp: new Date().toISOString() }});
            }});

            // Routes
            app.get('/', (req, res) => {{
                res.send('Hello from the Vibe Stack!');
            }});

            // Error Handling
            app.use((err, req, res, next) => {{
                console.error(err.stack);
                res.status(500).json({{ error: 'Something broke!' }});
            }});

            app.listen(PORT, () => {{
                console.log(`🚀 Server vibing on http://localhost:${{PORT}}`);
            }});
        """).strip()