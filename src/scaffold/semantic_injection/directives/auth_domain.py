# scaffold/semantic_injection/directives/auth_domain.py

"""
=================================================================================
== THE GATEKEEPER (V-Ω-AUTH-DOMAIN)                                            ==
=================================================================================
LIF: 200,000,000,000

This artisan implements the `@auth` namespace. It handles the most critical and
error-prone part of any application: Security.

Usage:
    middleware.ts       :: @auth/jwt(secret="env(JWT_SECRET)")
    auth/[...nextauth].ts :: @auth/nextauth(providers="google,github")
    permissions.py      :: @auth/rbac(roles="admin,editor,viewer")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("auth")
class AuthDomain(BaseDirectiveDomain):
    """
    The Sentinel of Identity.
    """

    @property
    def namespace(self) -> str:
        return "auth"

    def help(self) -> str:
        return "Generates authentication boilerplate (JWT, NextAuth, RBAC)."

    def _directive_jwt(self, context: Dict[str, Any], secret: str = "env('JWT_SECRET')", lang: str = "typescript",
                       *args, **kwargs) -> str:
        """
        @auth/jwt(secret="process.env.JWT_SECRET")
        Generates a stateless JWT verification middleware.
        """
        if lang == "typescript":
            return dedent(f"""
                import {{ NextRequest, NextResponse }} from 'next/server';
                import {{ jwtVerify }} from 'jose';

                const SECRET = new TextEncoder().encode({secret});

                export async function middleware(req: NextRequest) {{
                  const token = req.headers.get('Authorization')?.split(' ')[1];

                  if (!token) {{
                    return NextResponse.json({{ error: 'Missing Sentinel Token' }}, {{ status: 401 }});
                  }}

                  try {{
                    const {{ payload }} = await jwtVerify(token, SECRET);
                    // Gnostic Context Injection
                    const requestHeaders = new Headers(req.headers);
                    requestHeaders.set('x-user-id', payload.sub as string);

                    return NextResponse.next({{
                      request: {{ headers: requestHeaders }},
                    }});
                  }} catch (err) {{
                    return NextResponse.json({{ error: 'Profane Token' }}, {{ status: 403 }});
                  }}
                }}

                export const config = {{
                  matcher: '/api/:path*',
                }};
            """).strip()

        elif lang == "python":
            return dedent(f"""
                from fastapi import Request, HTTPException, Depends
                from fastapi.security import HTTPBearer
                import jwt
                import os

                SECRET = os.getenv("JWT_SECRET", "dev_secret")
                security = HTTPBearer()

                async def verify_token(credentials: HTTPBearer = Depends(security)):
                    token = credentials.credentials
                    try:
                        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
                        return payload
                    except jwt.ExpiredSignatureError:
                        raise HTTPException(status_code=401, detail="Token has returned to the void (Expired)")
                    except jwt.InvalidTokenError:
                        raise HTTPException(status_code=403, detail="Profane Token")
            """).strip()

        return "# Language not supported for JWT gatekeeping."

    def _directive_nextauth(self, context: Dict[str, Any], providers: str = "github,google", *args, **kwargs) -> str:
        """
        @auth/nextauth(providers="github,google")
        Generates a NextAuth.js configuration.
        """
        prov_list = [p.strip().lower() for p in providers.split(',')]
        imports = []
        provider_configs = []

        if "github" in prov_list:
            imports.append("import GithubProvider from 'next-auth/providers/github';")
            provider_configs.append(dedent("""
                GithubProvider({
                  clientId: process.env.GITHUB_ID!,
                  clientSecret: process.env.GITHUB_SECRET!,
                })
            """).strip())

        if "google" in prov_list:
            imports.append("import GoogleProvider from 'next-auth/providers/google';")
            provider_configs.append(dedent("""
                GoogleProvider({
                  clientId: process.env.GOOGLE_ID!,
                  clientSecret: process.env.GOOGLE_SECRET!,
                })
            """).strip())

        return dedent(f"""
            import NextAuth from 'next-auth';
            {chr(10).join(imports)}

            export const authOptions = {{
              providers: [
                {', '.join(provider_configs)}
              ],
              callbacks: {{
                async session({{ session, token, user }}) {{
                  return session;
                }},
              }},
              pages: {{
                signIn: '/auth/signin',
              }},
            }};

            export default NextAuth(authOptions);
        """).strip()

    def _directive_rbac(self, context: Dict[str, Any], roles: str = "admin,user", *args, **kwargs) -> str:
        """
        @auth/rbac(roles="admin,editor,viewer")
        Generates a role-based access control map.
        """
        role_list = [r.strip().upper() for r in roles.split(',')]

        return dedent(f"""
            export enum Role {{
              {', '.join([f'{r} = "{r}"' for r in role_list])}
            }}

            export const PERMISSIONS = {{
              [Role.ADMIN]: ['*'],
              [Role.USER]: ['read:own', 'write:own'],
              // Add specific granular rites here
            }} as const;

            export function hasPermission(userRole: Role, action: string): boolean {{
              const permissions = PERMISSIONS[userRole];
              if (permissions.includes('*')) return true;
              return permissions.includes(action);
            }}
        """).strip()