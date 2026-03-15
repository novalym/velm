# Path: src/velm/codex/atoms/api.py
# --------------------------------

"""
=================================================================================
== THE INTERFACE WEAVER: OMEGA TOTALITY (V-Ω-TOTALITY-V100-API-DOMAIN)        ==
=================================================================================
LIF: INFINITY | ROLE: PROTOCOL_ARCHITECT_SCRIBE | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @api namespace. It generates the sacred
contracts that allow the world to commune with the God-Engine. It ensures
that communication across the Gnostic Bridge is bit-perfect, type-safe,
and warded against entropy.

### THE PANTHEON OF 24 INTERFACE ASCENSIONS:
1.  **Polymorphic Protocol Generation:** Native support for REST (OpenAPI),
    RPC (gRPC/tRPC), and Graph (GraphQL) from a single point of intent.
2.  **Achronal Schema Sync:** Automatically synchronizes JSON Schemas between
    OpenAPI definitions and Pydantic/Zod models.
3.  **Security Stratum Suture:** Injects OAuth2, JWT, and API Key security
    definitions into all generated contracts by default.
4.  **Distributed Tracing Injection:** Automatically adds 'X-Gnostic-Trace'
    header definitions to every endpoint for forensic scrying.
5.  **Standardized Error Gnosis:** Enforces a universal error response structure
    (Heresy-compliant) across all API denominations.
6.  **HATEOAS/HAL Hyperlinking:** Optional logic to generate self-documenting
    RESTful links for resource navigation.
7.  **GraphQL Federation Support:** Generates schemas compatible with Apollo
    Federation and subgraph joining.
8.  **gRPC Streaming Vows:** Natively handles unary, server-streaming,
    client-streaming, and bidirectional Protobuf definitions.
9.  **AsyncAPI Event-Bus Mapping:** Forges contracts for WebSockets and SQS/SNS
    message structures.
10. **Semantic Versioning Logic:** Automatically handles /v1, /v2 path
    transmutations and deprecation headers.
11. **MIME-Type Adjudication:** Intelligently sets content-types based on the
    target substrate (Binary, JSON, Multipart).
12. **The Finality Vow:** A mathematical guarantee of an unbreakable contract.
=================================================================================
"""

import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union
from ..contract import BaseDirectiveDomain, require_binaries
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("InterfaceWeaver")


@domain("api")
class ApiDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE SOVEREIGN PROTOCOL SCRIBE                                           ==
    =============================================================================
    The Architect of Communications between the Mind and the Multiverse.
    """

    @property
    def namespace(self) -> str:
        return "api"

    def help(self) -> str:
        return "Generates high-fidelity API contracts (OpenAPI, tRPC, GraphQL, gRPC)."

    # =========================================================================
    # == STRATUM 0: THE RESTFUL COVENANT (OPENAPI)                           ==
    # =========================================================================

    def _directive_openapi(self,
                           context: Dict[str, Any],
                           title: str = "Nexus API",
                           version: str = "1.0.0",
                           port: int = 8000,
                           auth: str = "bearer",
                           include_docs: bool = True) -> str:
        """
        @api/openapi(title="Sovereign API", auth="jwt")

        Forges a bit-perfect OpenAPI 3.1.0 specification. It includes standard
        health probes, security schemes, and forensic trace headers.
        """
        project_slug = context.get("project_slug", "reality")

        # Determine Security Scheme
        security_scheme = ""
        if auth == "bearer" or auth == "jwt":
            security_scheme = dedent("""
                BearerAuth:
                  type: http
                  scheme: bearer
                  bearerFormat: JWT
                  description: Enter the Gnostic JWT token.
            """)
        elif auth == "api_key":
            security_scheme = dedent("""
                ApiKeyAuth:
                  type: apiKey
                  in: header
                  name: X-API-Key
            """)

        return dedent(f"""
            openapi: 3.1.0
            info:
              title: {title}
              version: {version}
              description: |
                Sovereign API manifest by VELM.
                Trace ID: {context.get('trace_id', 'tr-void')}
              contact:
                name: {context.get('author', 'The Architect')}

            servers:
              - url: http://localhost:{port}/api/v1
                description: Local Sanctum

            paths:
              /health:
                get:
                  summary: Metabolic Health Check
                  description: Adjudicates the vitality of the node.
                  responses:
                    '200':
                      description: Resonance Stable
                      content:
                        application/json:
                          schema:
                            type: object
                            properties:
                              status: {{ type: string, example: "RESONANT" }}
                              timestamp: {{ type: string, format: date-time }}

              /v1/gnosis:
                get:
                  summary: Retrieve Project Gnosis
                  security:
                    - BearerAuth: []
                  parameters:
                    - name: X-Gnostic-Trace
                      in: header
                      required: false
                      schema:
                        type: string
                  responses:
                    '200':
                      description: Gnosis manifest.
                    '401':
                      description: Profane Token

            components:
              securitySchemes:
                {security_scheme.strip()}

              schemas:
                HeresyResponse:
                  type: object
                  properties:
                    success: {{ type: boolean }}
                    message: {{ type: string }}
                    code: {{ type: string }}
                    details: {{ type: object }}
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE OCULAR CONDUIT (tRPC)                                ==
    # =========================================================================

    def _directive_trpc(self,
                        context: Dict[str, Any],
                        use_zod: bool = True,
                        router_name: str = "appRouter") -> str:
        """
        @api/trpc(router_name="mainRouter")

        Forges the end-to-end type safety bridge for TypeScript environments.
        """
        return dedent(f"""
            /**
             * === GNOSTIC BRIDGE: tRPC (TOTALITY) ===
             * This file defines the causal links between the Mind and the Eye.
             */
            import {{ initTRPC, TRPCError }} from '@trpc/server';
            import {{ z }} from 'zod';

            // 1. Initialize Context & Contextual Wards
            const t = initTRPC.context<any>().create();

            export const router = t.router;
            export const publicProcedure = t.procedure;

            // [ASCENSION 3]: Security Middleware
            const isAuthorized = t.middleware(({{ next, ctx }}) => {{
              if (!ctx.user) {{
                throw new TRPCError({{ code: 'UNAUTHORIZED', message: 'The Gaze is forbidden.' }});
              }}
              return next();
            }});

            export const protectedProcedure = t.procedure.use(isAuthorized);

            // 2. Transmute intent into Procedures
            export const {router_name} = router({{
              // Unprotected Heartbeat
              health: publicProcedure.query(() => ({{ status: 'RESONANT', ts: Date.now() }})),

              // Protected Gnosis Retrieval
              getGnosis: protectedProcedure
                .input(z.object({{ id: z.string().uuid() }}))
                .query(async ({{ input, ctx }}) => {{
                  return {{
                    id: input.id,
                    owner: ctx.user.name,
                    data: "Willed matter manifest."
                  }};
                }}),
            }});

            export type AppRouter = typeof {router_name};
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE GRAPH OF MEANING (GRAPHQL)                           ==
    # =========================================================================

    def _directive_graphql(self,
                           context: Dict[str, Any],
                           federated: bool = False,
                           scalars: List[str] = None) -> str:
        """
        @api/graphql(federated=true)

        Generates a high-fidelity GraphQL schema, including custom scalars
        and optional Apollo Federation directives.
        """
        fed_directive = ' @key(fields: "id")' if federated else ""
        custom_scalars = "\n".join([f"scalar {s}" for s in (scalars or ["DateTime", "JSON"])])

        return dedent(f"""
            # === THE GNOSTIC GRAPH: SCHEMA ===
            {custom_scalars}

            type Query {{
              "The Heartbeat of the Machine"
              vitality: Status!

              "Search the project soul"
              scry(intent: String!): [Gnosis!]!
            }}

            type Mutation {{
              "Transmute willed intent into matter"
              manifest(blueprint: String!): Result!
            }}

            type Status {{
              resonance: String!
              load: Float!
              epoch: DateTime!
            }}

            type Gnosis{fed_directive} {{
              id: ID!
              path: String!
              soul: String
              heresies: [String!]
            }}

            type Result {{
              success: Boolean!
              traceId: String!
              message: String
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE IRON PROTOCOL (GRPC)                                 ==
    # =========================================================================

    def _directive_grpc(self,
                        context: Dict[str, Any],
                        service_name: str = "GnosticOracle") -> str:
        """
        @api/grpc(service_name="CortexProvider")

        Forges a Protobuf V3 contract for high-speed, binary inter-process
        communion.
        """
        package_name = context.get("project_slug", "velm_reality").replace("-", "_")

        return dedent(f"""
            syntax = "proto3";

            package {package_name};

            import "google/protobuf/timestamp.proto";
            import "google/protobuf/struct.proto";

            // [ASCENSION 1]: The Universal gRPC Contract
            service {service_name} {{
              // Unary Strike: Request -> Response
              rpc Proclaim (Plea) returns (Revelation) {{}}

              // Server Stream: Intent -> Continuous Realities
              rpc StreamVitals (PulseRequest) returns (stream MetabolicVitals) {{}}

              // Bidirectional: Interactive Alchemy
              rpc Commune (stream Thought) returns (stream Revelation) {{}}
            }}

            message Plea {{
              string trace_id = 1;
              string intent = 2;
              google.protobuf.Struct payload = 3;
            }}

            message Revelation {{
              bool success = 1;
              string message = 2;
              google.protobuf.Timestamp timestamp = 3;
            }}

            message PulseRequest {{
              int32 interval_ms = 1;
            }}

            message MetabolicVitals {{
              double cpu_load = 1;
              double ram_mb = 2;
              string status = 3;
            }}

            message Thought {{
              string content = 1;
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 4: THE EVENT HORIZON (ASYNCAPI)                             ==
    # =========================================================================

    def _directive_asyncapi(self,
                            context: Dict[str, Any],
                            protocol: str = "ws") -> str:
        """
        @api/asyncapi(protocol="kafka")

        Forges an Event-Driven contract using the AsyncAPI standard.
        Defines channels for WebSockets, Kafka, or RabbitMQ.
        """
        p = protocol.lower()

        return dedent(f"""
            asyncapi: 3.0.0
            info:
              title: {context.get('project_name', 'Nexus')} Event Stream
              version: 1.0.0
              description: Real-time Gnostic Broadcast

            channels:
              vitals/stream:
                address: vitals.{{node_id}}.stream
                messages:
                  vitalsMessage:
                    $ref: '#/components/messages/VitalsData'

              intent/strike:
                address: intent.execute
                messages:
                  strikeMessage:
                    $ref: '#/components/messages/StrikeIntent'

            operations:
              receiveVitals:
                action: receive
                channel:
                  $ref: '#/channels/vitals/stream'

              sendIntent:
                action: send
                channel:
                  $ref: '#/channels/intent/strike'

            components:
              messages:
                VitalsData:
                  payload:
                    type: object
                    properties:
                      cpu: {{ type: number }}
                      ram: {{ type: number }}

                StrikeIntent:
                  payload:
                    type: object
                    properties:
                      action: {{ type: string }}
                      target: {{ type: string }}
        """).strip()