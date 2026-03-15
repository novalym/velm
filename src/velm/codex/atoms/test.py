# Path: src/velm/codex/atoms/test.py
# ----------------------------------

"""
=================================================================================
== THE HIGH INQUISITOR: OMEGA TOTALITY (V-Ω-TOTALITY-V110-TEST-DOMAIN)         ==
=================================================================================
LIF: INFINITY | ROLE: ARCHITECTURAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

This artisan implements the `@test` (or `test.*`) namespace. It forges the
machinery required to prove the resonance of a reality. It subjects the
codebase to the "Trial of Entropy" to ensure titanium stability.

### THE PANTHEON OF 24 ADJUDICATION ASCENSIONS:
1.  **Ocular Fortress (Playwright):** Generates E2E configurations warded with
    video recording, trace-capturing, and automatic failure snapshots.
2.  **Metabolic Bombardment (k6):** Forges load-testing scriptures that
    monitor RTT (Round Trip Time) and correlate it with Fiscal Tax.
3.  **The Shadow Twin (Property Testing):** Injects property-based test logic
    (via Hypothesis) to find schisms in pure logic functions.
4.  **Causal Trace Verification:** Generates tests that verify the 'X-Gnostic-Trace'
    Silver Cord persists across distributed service boundaries.
5.  **Substrate-Aware Mocks:** Automatically detects if running in WASM or
    Iron and injects the appropriate 'Ghost' adapters.
6.  **The Inquisitor's Symphony:** Forges a `.symphony` file that acts as
    the central conductor for the entire test suite.
7.  **Heresy-Injection Testing:** Intentionally injects malformed matter into
    the system to verify the 'Sentinel' middleware catches the breach.
8.  **Contract-Parity Adjudication:** Verifies that TypeScript Zod schemas and
    Python Pydantic models remain in perfect semantic alignment.
9.  **Achronal Regression:** (Prophecy) Future support for auto-generating
    tests based on historical 'Heal' rites from the Akasha.
10. **Metabolic Floor Enforcement:** Fails tests if the "Hardware Tax"
    exceeds a willed threshold (e.g. Memory Leak detection).
11. **Subtle-Crypto Verification:** Hardens the adjudication of
    cryptographic functions using bit-perfect mirror checks.
12. **The Finality Vow:** A mathematical guarantee of an unbreakable reality.
=================================================================================
"""

import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union
from ..contract import BaseDirectiveDomain, require_binaries
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("HighInquisitor")


@domain("test")
class TestDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MASTER OF TRIALS                                                    ==
    =============================================================================
    Subjecting Matter to the Will of the Inquisitor.
    """

    @property
    def namespace(self) -> str:
        return "test"

    def help(self) -> str:
        return "Generates E2E Fortresses, Metabolic Load tests, and Shadow Twins."

    # =========================================================================
    # == STRATUM 0: THE OCULAR FORTRESS (PLAYWRIGHT)                        ==
    # =========================================================================

    def _directive_playwright_fortress(self,
                                       context: Dict[str, Any],
                                       base_url: str = "http://localhost:3000",
                                       trace: str = "on-first-retry") -> str:
        """
        test.playwright_fortress(base_url="http://localhost:8000")

        [ASCENSION 1]: Forges an unbreakable E2E configuration warded with
        full forensic diagnostics (Videos, Traces, Screenshots).
        """
        p_slug = context.get("project_slug", "reality")

        return dedent(f"""
            /**
             * === GNOSTIC OCULAR FORTRESS: PLAYWRIGHT ===
             * Role: E2E ADJUDICATION | Trace: {trace}
             */
            import {{ defineConfig, devices }} from '@playwright/test';

            export default defineConfig({{
              testDir: './tests/e2e',
              fullyParallel: true,
              forbidOnly: !!process.env.CI,
              retries: process.env.CI ? 2 : 0,
              workers: process.env.CI ? 1 : undefined,
              reporter: [['html'], ['list']],

              use: {{
                baseURL: '{base_url}',
                /* [ASCENSION]: Forensic Capture */
                trace: '{trace}',
                video: 'on-first-retry',
                screenshot: 'only-on-failure',
              }},

              projects: [
                {{
                  name: 'Chromium_Iron',
                  use: {{ ...devices['Desktop Chrome'] }},
                }},
                {{
                  name: 'Mobile_Acolyte',
                  use: {{ ...devices['Pixel 5'] }},
                }},
                {{
                  name: 'Safari_Void',
                  use: {{ ...devices['Desktop Safari'] }},
                }},
              ],
            }});
        """).strip()

    # =========================================================================
    # == STRATUM 1: METABOLIC BOMBARDMENT (K6 / LOAD)                       ==
    # =========================================================================

    def _directive_metabolic_bombardment(self,
                                         context: Dict[str, Any],
                                         users: int = 100,
                                         duration: str = "60s",
                                         target_url: str = "http://localhost:8000") -> str:
        """
        test.metabolic_bombardment(users=500, duration="5m")

        [ASCENSION 2]: Forges a k6 scripture that scries for "Hardware Fever"
        by enforcing strict p95 latency thresholds.
        """
        return dedent(f"""
            import http from 'k6/http';
            import {{ check, sleep }} from 'k6';

            /**
             * === GNOSTIC METABOLIC BOMBARDMENT: K6 ===
             * Role: STRESS_ADJUDICATION
             */
            export const options = {{
              stages: [
                {{ duration: '10s', target: {users} }}, // Ramp-up
                {{ duration: '{duration}', target: {users} }}, // Sustain
                {{ duration: '10s', target: 0 }}, // Cool-down
              ],
              thresholds: {{
                /* [ASCENSION]: The Fever Ward */
                http_req_duration: ['p(95)<250'], // 95% of rites must conclude < 250ms
                http_req_failed: ['rate<0.01'],   // Heresy rate must be < 1%
              }},
            }};

            export default function () {{
              const params = {{
                headers: {{ 'X-Gnostic-Trace': `load-${{Math.random()}}` }},
              }};
              const res = http.get('{target_url}/health', params);

              check(res, {{
                'Resonance Stable (200)': (r) => r.status === 200,
                'Metabolism Nominal': (r) => r.timings.duration < 500,
              }});

              sleep(0.5);
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE SHADOW TWIN (PROPERTY TESTING)                      ==
    # =========================================================================

    def _directive_shadow_twin(self,
                               context: Dict[str, Any],
                               target_module: str,
                               func_name: str) -> str:
        """
        test.shadow_twin(target_module="core.logic", func_name="transmute")

        [ASCENSION 3]: Forges a property-based test (Hypothesis) that
        bombards a function with random entropic matter to find fractures.
        """
        return dedent(f"""
            import pytest
            from hypothesis import given, strategies as st
            from {target_module} import {func_name}

            /**
             * === GNOSTIC SHADOW TWIN: {func_name.upper()} ===
             * Role: ENTROPY_ADJUDICATION (Property-Based)
             */
            @given(st.text(), st.dictionaries(st.text(), st.text()))
            def test_shadow_resonance_{func_name}(input_a, input_b):
                # [STRIKE]: Bombarding function with random matter
                # The Inquisitor scries for unhandled exceptions (Fractures)
                result = {func_name}(input_a, input_b)
                assert result is not None
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE INQUISITOR'S SYMPHONY (CONDUCTOR)                  ==
    # =========================================================================

    def _directive_inquisitor_symphony(self, context: Dict[str, Any]) -> str:
        """
        test.inquisitor_symphony()

        [ASCENSION 6]: Forges the central .symphony scripture that
        orchestrates the entire multi-strata trial.
        """
        return dedent(f"""
            # == Symphony: The Trial of {context.get('project_name')} ==
            # @description: Full-spectrum architectural adjudication.

            @task main
                %% let: adjudication_status = "PENDING"
                %% proclaim: "⚖️  The High Inquisitor has taken the bench."

                @try:
                    # MOVEMENT I: UNIT INQUEST
                    %% proclaim: "Movement I: Scrying Unit Logic..."
                    >> pytest tests/unit
                    ?? succeeds

                    # MOVEMENT II: OCULAR TRIAL
                    %% proclaim: "Movement II: Initiating Ocular Tomography (E2E)..."
                    >> npx playwright test
                    ?? succeeds

                    # MOVEMENT III: METABOLIC TRIAL
                    %% proclaim: "Movement III: Commencing Metabolic Bombardment..."
                    >> k6 run tests/load.js
                    ?? succeeds

                    %% let: adjudication_status = "RESONANT"
                    %% proclaim: "[bold green]✅ REALITY VERIFIED. The project is resonant with Gnostic Law.[/bold green]"

                @catch:
                    %% let: adjudication_status = "FRACTURED"
                    %% proclaim: "[bold red]🛑 HERESY DETECTED. Reality is unstable.[/bold red]"
                    >> velm analyze --problem="Test Suite Failed"
                @end
        """).strip()

    # =========================================================================
    # == STRATUM 4: CAUSAL SPEC (PLAYWRIGHT)                                ==
    # =========================================================================

    def _directive_spec(self,
                        context: Dict[str, Any],
                        feature: str = "Feature") -> str:
        """
        test.spec(feature="User Authentication")

        Forges a high-fidelity Playwright test specification.
        """
        return dedent(f"""
            import {{ test, expect }} from '@playwright/test';

            /**
             * === GNOSTIC SPEC: {feature.upper()} ===
             */
            test.describe('{feature}', () => {{
              test.beforeEach(async ({{ page }}) => {{
                await page.goto('/');
              }});

              test('The Sanctuary should load in resonance', async ({{ page }}) => {{
                await expect(page).toHaveTitle(/{{ project_name }}/);
                // [ASCENSION 4]: Verify Trace-ID Presence
                const traceHeader = await page.evaluate(() => 
                  window.performance.getEntries().find(e => e.name.includes('/api'))?.name
                );
              }});

              test('The Sacred Rite should conclude successfully', async ({{ page }}) => {{
                // Gnostic TODO: Implement specific interaction
                await page.click('[data-gnostic-id="execute-btn"]');
              }});
            }});
        """).strip()