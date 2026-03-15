# Path: src/velm/codex/atoms/shield.py
# ------------------------------------

"""
=================================================================================
== THE ACTIVE DEFENSE (V-Ω-SHIELD-DOMAIN)                                      ==
=================================================================================
LIF: 500,000,000,000 | ROLE: RUNTIME_SECURITY_WARDEN | RANK: OMEGA_SOVEREIGN

This artisan implements the `@shield` namespace. It injects runtime security
controls (Rate Limiting, Sanitization, CSP Headers) directly into the application
layer logic.

Usage:
    middleware/limiter.py :: {{ shield.rate_limit(limit=100, window=60) }}
    utils/sanitize.ts     :: {{ shield.sanitize() }}
    config/headers.js     :: {{ shield.headers(mode="strict") }}
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("shield")
class ShieldDomain(BaseDirectiveDomain):
    """
    The Warden of the Runtime.
    """

    @property
    def namespace(self) -> str:
        return "shield"

    def help(self) -> str:
        return "Generates runtime security controls (Rate limits, Sanitization, Headers)."

    def _directive_rate_limit(self, context: Dict[str, Any], limit: int = 100, window: int = 60,
                              strategy: str = "token_bucket", *args, **kwargs) -> str:
        """
        shield.rate_limit(limit=100, window=60)
        Generates a memory-based rate limiter (Python/FastAPI friendly).
        """
        return dedent(f"""
            import time
            from collections import defaultdict
            from fastapi import HTTPException, Request

            # Strategy: {strategy}
            # Limit: {limit} requests per {window} seconds

            class RateLimiter:
                def __init__(self):
                    self.requests = defaultdict(list)
                    self.limit = {limit}
                    self.window = {window}

                async def check(self, request: Request):
                    client_ip = request.client.host if request.client else "unknown"
                    now = time.time()

                    # Clean old requests (The Rite of Purification)
                    self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.window]

                    if len(self.requests[client_ip]) >= self.limit:
                        raise HTTPException(status_code=429, detail="Shield Activated: Rate limit exceeded.")

                    self.requests[client_ip].append(now)

            limiter = RateLimiter()
        """).strip()

    def _directive_sanitize(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        shield.sanitize()
        Generates input sanitization utilities (XSS prevention) for TypeScript/JS.
        """
        return dedent("""
            import DOMPurify from 'dompurify';
            import { JSDOM } from 'jsdom';

            const window = new JSDOM('').window;
            const purify = DOMPurify(window);

            export function sanitizeInput(raw: string): string {
              return purify.sanitize(raw, {
                ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
                ALLOWED_ATTR: ['href']
              });
            }

            export function sanitizeObject(obj: any): any {
              if (typeof obj === 'string') return sanitizeInput(obj);
              if (typeof obj === 'object' && obj !== null) {
                Object.keys(obj).forEach(key => {
                  obj[key] = sanitizeObject(obj[key]);
                });
              }
              return obj;
            }
        """).strip()

    def _directive_headers(self, context: Dict[str, Any], mode: str = "strict", *args, **kwargs) -> str:
        """
        shield.headers(mode="strict")
        Generates OWASP-recommended security headers configuration (Express/Helmet style).
        """
        return dedent("""
            const helmet = require('helmet');

            // Gnostic Shield: OWASP Recommended Headers
            module.exports = helmet({
              contentSecurityPolicy: {
                directives: {
                  defaultSrc: ["'self'"],
                  scriptSrc: ["'self'", "'unsafe-inline'"], // Adjust for specific needs
                  styleSrc: ["'self'", "'unsafe-inline'"],
                  imgSrc: ["'self'", "data:", "https:"],
                },
              },
              referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
              frameguard: { action: 'deny' },
              hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
              noSniff: true,
              xssFilter: true,
            });
        """).strip()