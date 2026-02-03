# scaffold/semantic_injection/directives/test_domain.py

"""
=================================================================================
== THE HIGH INQUISITOR (V-Ω-TEST-DOMAIN)                                       ==
=================================================================================
LIF: 200,000,000,000

This artisan implements the `@test` namespace. It generates the machinery required
to prove the reality of your code.

Usage:
    playwright.config.ts :: @test/playwright(base_url="http://localhost:3000")
    tests/load.js        :: @test/k6(users=100, duration="30s")
    tests/e2e/login.spec.ts :: @test/spec(feature="Login Flow")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("test")
class TestDomain(BaseDirectiveDomain):
    """
    The Adjudicator of Stability.
    """

    @property
    def namespace(self) -> str:
        return "test"

    def help(self) -> str:
        return "Generates test configurations and scenarios (Playwright, k6)."

    def _directive_playwright(self, context: Dict[str, Any], base_url: str = "http://localhost:3000", *args, **kwargs) -> str:
        """
        @test/playwright
        Generates a robust Playwright configuration.
        """
        return dedent(f"""
            import {{ defineConfig, devices }} from '@playwright/test';

            export default defineConfig({{
              testDir: './tests/e2e',
              fullyParallel: true,
              forbidOnly: !!process.env.CI,
              retries: process.env.CI ? 2 : 0,
              workers: process.env.CI ? 1 : undefined,
              reporter: 'html',
              use: {{
                baseURL: '{base_url}',
                trace: 'on-first-retry',
              }},
              projects: [
                {{
                  name: 'chromium',
                  use: {{ ...devices['Desktop Chrome'] }},
                }},
                {{
                  name: 'mobile',
                  use: {{ ...devices['Pixel 5'] }},
                }},
              ],
            }});
        """).strip()

    def _directive_k6(self, context: Dict[str, Any], users: int = 50, duration: str = "30s", url: str = "http://localhost:3000", *args, **kwargs) -> str:
        """
        @test/k6(users=100, duration="1m")
        Generates a load testing script.
        """
        return dedent(f"""
            import http from 'k6/http';
            import {{ check, sleep }} from 'k6';

            export const options = {{
              vus: {users},
              duration: '{duration}',
              thresholds: {{
                http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
              }},
            }};

            export default function () {{
              const res = http.get('{url}');
              check(res, {{ 'status was 200': (r) => r.status == 200 }});
              sleep(1);
            }}
        """).strip()

    def _directive_spec(self, context: Dict[str, Any], feature: str = "Feature", *args, **kwargs) -> str:
        """
        @test/spec(feature="Authentication")
        Generates a Playwright test skeleton.
        """
        return dedent(f"""
            import {{ test, expect }} from '@playwright/test';

            test.describe('{feature}', () => {{
              test.beforeEach(async ({{ page }}) => {{
                await page.goto('/');
              }});

              test('should load the sanctuary correctly', async ({{ page }}) => {{
                await expect(page).toHaveTitle(/Scaffold/);
              }});

              test('should perform the sacred rite', async ({{ page }}) => {{
                // Gnostic TODO: Implement specific interaction
              }});
            }});
        """).strip()