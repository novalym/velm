# scaffold/semantic_injection/directives/api_domain.py

"""
=================================================================================
== THE INTERFACE WEAVER (V-Ω-API-DOMAIN)                                       ==
=================================================================================
LIF: 200,000,000,000

This artisan implements the `@api` namespace. It generates the contracts that
allow the world to commune with your application.

Usage:
    openapi.yaml    :: @api/openapi(title="Nexus API", version="1.0.0")
    src/trpc.ts     :: @api/trpc
    schema.graphql  :: @api/graphql
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("api")
class ApiDomain(BaseDirectiveDomain):
    """
    The Scribe of Protocols.
    """

    @property
    def namespace(self) -> str:
        return "api"

    def help(self) -> str:
        return "Generates API schemas and router boilerplate (OpenAPI, tRPC, GraphQL)."

    def _directive_openapi(self, context: Dict[str, Any], title: str = "API", version: str = "1.0.0", *args, **kwargs) -> str:
        """
        @api/openapi
        Generates a base OpenAPI 3.0 Spec.
        """
        return dedent(f"""
            openapi: 3.0.3
            info:
              title: {title}
              version: {version}
              description: Auto-generated Gnostic Schema
            servers:
              - url: http://localhost:3000/api/v1
                description: Local Sanctum
            paths:
              /health:
                get:
                  summary: The Heartbeat Rite
                  responses:
                    '200':
                      description: The system is alive
            components:
              securitySchemes:
                BearerAuth:
                  type: http
                  scheme: bearer
        """).strip()

    def _directive_trpc(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @api/trpc
        Generates a tRPC backend setup (router + procedure).
        """
        return dedent("""
            import { initTRPC } from '@trpc/server';
            import { z } from 'zod';

            const t = initTRPC.create();

            export const router = t.router;
            export const publicProcedure = t.procedure;

            export const appRouter = router({
              hello: publicProcedure
                .input(z.object({ text: z.string().nullish() }).nullish())
                .query(({ input }) => {
                  return {
                    greeting: `Hello ${input?.text ?? 'world'} from the Gnostic Router`,
                  };
                }),
            });

            export type AppRouter = typeof appRouter;
        """).strip()

    def _directive_graphql(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @api/graphql
        Generates a basic GraphQL schema.
        """
        return dedent("""
            type Query {
              hello: String
              users: [User!]!
            }

            type User {
              id: ID!
              name: String!
              email: String!
              createdAt: String!
            }

            type Mutation {
              createUser(name: String!, email: String!): User!
            }
        """).strip()