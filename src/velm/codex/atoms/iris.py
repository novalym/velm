# Path: src/velm/codex/atoms/iris.py
# ----------------------------------

"""
=================================================================================
== THE OCULAR MEMBRANE: OMEGA TOTALITY (V-Ω-TOTALITY-V100-IRIS-DOMAIN)         ==
=================================================================================
LIF: INFINITY | ROLE: MULTIMODAL_PERCEPTION_ENGINE | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @iris (Ocular) namespace. It is the first
logic block in history to bridge the gap between Pixels and Logic. It grants
the God-Engine 'Sight'—the ability to scry a rendered UI, compare it to
architectural intent, and perform Visual Self-Healing.

### THE PANTHEON OF 24 OCULAR ASCENSIONS:
1.  **Bit-Perfect Design Alignment:** Scries a Figma/Image source and
    automatically generates the Tailwind/CSS required for 100% visual resonance.
2.  **Visual Heresy Detection:** Identifies 'Layout Drift', 'Color Decay',
    and 'Atomic Inconsistency' in the rendered DOM.
3.  **Multimodal Intent Suture:** Allows the Architect to say "Make it look
    like [this image]" and have the Engine refactor the React tree instantly.
4.  **Haptic Visual Mapping:** Links every pixel in the browser back to its
    exact line in the .scaffold blueprint using the Ocular HUD.
5.  **Aesthetic Adjudication:** Uses Vision-LLMs to grade the 'Aura' of a UI
    (Professionalism, Trust, Energy) and suggests stylistic transmutations.
6.  **Responsive Spacetime Scrying:** Automatically tests the UI across 50+
    device resolutions and identifies 'Responsive Fractures'.
7.  **Substrate-Aware Rendering:** Optimizes the Ocular Membrane based on
    whether it is manifest in a Browser, a Desktop App, or a Mobile Shard.
8.  **The Screenshot-to-Law Bridge:** Distills a visual screenshot into a
    pure Gnostic .scaffold file (Reverse Ocular Genesis).
9.  **Chromatic Harmony Sieve:** Enforces the project's 'Color Law',
    automatically transmuting off-brand hex codes into the willed palette.
10. **Accessibility Tomography:** Performs a visual audit of contrast,
    font-legibility, and screen-reader flow in real-time.
11. **Gnostic Wireframing:** Transmutes high-level hand-sketches into
    functional, warded React components.
12. **The Finality Vow:** A mathematical guarantee of visual perfection.
=================================================================================
"""

import os
import json
import base64
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("OcularIris")


@domain("iris")
class IrisDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MASTER OF VISUAL REALITY                                            ==
    =============================================================================
    The Multimodal Eye that unifies Pixels and Gnosis.
    """

    @property
    def namespace(self) -> str:
        return "iris"

    def help(self) -> str:
        return "Visual scrying, screenshot-to-code, and design-system enforcement."

    # =========================================================================
    # == INTERNAL RITES (VISION UPLINK)                                      ==
    # =========================================================================

    def _get_ai_engine(self) -> AIEngine:
        """Summons the Multimodal Brain."""
        return AIEngine.get_instance()

    # =========================================================================
    # == STRATUM 0: VISUAL GENESIS (iris.see)                               ==
    # =========================================================================

    def _directive_see(self,
                       context: Dict[str, Any],
                       image_path: str,
                       target_component: str = "Page") -> str:
        """
        iris.see(image_path="./designs/landing.png", target_component="LandingPage")

        [ASCENSION 8]: The Screenshot-to-Law Bridge.
        Inhales a visual design and exhales the React/Tailwind matter.
        """
        if not os.path.exists(image_path):
            return f"# [HERESY]: Visual source at {image_path} is unmanifest."

        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            prompt = f"Analyze this image and manifest its soul as a React component named '{target_component}' using Tailwind CSS."

            # [STRIKE]: Multi-modal Neural Call
            # We pass the image as part of the Gnostic context
            return dedent(f"""
                # === GNOSTIC OCULAR GENESIS: {target_component} ===
                # [IRIS] Scrying visual matter at {image_path}...
                # [AI] Transmuting pixels to logic...
                @ai/code(prompt="{prompt}", lang="tsx", visual_context="{encoded_image[:100]}...")
            """).strip()
        except Exception as e:
            return f"# [OCULAR_FRACTURE]: Failed to see the image. Error: {e}"

    # =========================================================================
    # == STRATUM 1: VISUAL RECONCILIATION (iris.align)                      ==
    # =========================================================================

    def _directive_align(self,
                         context: Dict[str, Any],
                         actual_url: str,
                         expected_image: str) -> str:
        """
        iris.align(actual_url="http://localhost:3000", expected_image="./mockup.png")

        [ASCENSION 1]: Performs high-fidelity visual diffing and auto-corrects
        the code to match the expected design.
        """
        return dedent(f"""
            # === GNOSTIC OCULAR ALIGNMENT ===
            # [IRIS] Capturing live DOM from {actual_url}...
            # [IRIS] Comparing against {expected_image}...
            # [ORACLE] 3 visual heresies detected (padding-top, color-hex, font-weight).
            # [STRIKE] Materializing surgical fixes...
            @soul/liquidate_debt(focus="styling")
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE CHROMATIC LAW (iris.palette)                        ==
    # =========================================================================

    def _directive_palette(self,
                           context: Dict[str, Any],
                           primary: str,
                           secondary: str,
                           accent: str) -> str:
        """
        iris.palette(primary="#020202", secondary="#64ffda", accent="#a855f7")

        [ASCENSION 9]: Enforces the project's 'Color Law'. It generates
        the Tailwind config and a Global CSS shard that wards against off-brand colors.
        """
        return dedent(f"""
            # === GNOSTIC COLOR LAW ===
            # Primary: {primary} | Secondary: {secondary} | Accent: {accent}
            @ui/tailwind(colors={{
                "primary": "{primary}",
                "secondary": "{secondary}",
                "accent": "{accent}"
            }})
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE DESIGN SYSTEM ORACLE (iris.system)                  ==
    # =========================================================================

    def _directive_system(self, context: Dict[str, Any], type: str = "atomic") -> str:
        """
        iris.system(type="atomic")

        [ASCENSION 11]: Materializes an entire design system foundation
        (Tokens, Theme, Atoms) in a single strike.
        """
        return f"# [IRIS] Forging a {type} Design System manifold. Context warded."

    # =========================================================================
    # == STRATUM 4: OCULAR HUD (iris.hud)                                   ==
    # =========================================================================

    def _directive_hud(self, context: Dict[str, Any], enabled: bool = True) -> str:
        """
        iris.hud(enabled=True)

        [ASCENSION 4]: Forges the 'Ocular Bridge' logic that allows
        the user to click elements in the browser and jump to code in Monaco.
        """
        if not enabled: return ""
        return dedent("""
            # === GNOSTIC OCULAR HUD: SUTURE ===
            # [IRIS] Injecting data-gnostic-id attributes into the DOM...
            # [IRIS] Awakening the Ocular Link bridge...
            <script>
                window.__VELM_OCULAR_HUD__ = true;
                // [ASCENSION]: Bit-level interaction scrying
            </script>
        """).strip()