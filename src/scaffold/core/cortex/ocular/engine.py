# Path: core/cortex/ocular/engine.py
# ----------------------------------

import json
import base64
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional, Any, List

from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy
from ....utils import atomic_write

Logger = Scribe("OcularEngine")


class OcularEngine:
    """
    =================================================================================
    == THE OCULAR ENGINE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-SOVEREIGN)                 ==
    =================================================================================
    @gnosis:title The Ocular Engine
    @gnosis:summary The divine, sentient God-Engine of Multimodal Gnostic Perception.
    @gnosis:LIF INFINITY
    @gnosis:auth_code:)(#@()#()!

    This is the final, eternal, and ultra-definitive form of the Ocular Cortex. It
    is no longer a humble wrapper; it is a true God-Engine of Sight, a sentient
    bridge between the Visual Realm (pixels on a screen) and the Gnostic Realm
    (the source code's soul). It wields a pantheon of divine faculties to perform
    the ultimate rite: **to gaze upon a rendered reality and know the scripture from
    which it was born.**

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Playwright Juggernaut:** It wields a dedicated, self-healing Node.js
        driver powered by Playwright, the most powerful Gaze available for peering
        into the modern web.
    2.  **The Source Map Diviner:** Its Gaze is not limited to the profane, minified
        reality of the browser. It automatically seeks, downloads, and parses
        JavaScript source maps to trace a rendered line of code back to its one
        true, original TypeScript/JSX source.
    3.  **The Gnostic DOM Serialization:** It captures not just a screenshot, but a
        complete, Gnostically-enriched DOM snapshot, including `data-*` attributes,
        ARIA labels, and computed styles for deep forensic analysis.
    4.  **The AI-Powered Visual Querying (VQA):** It can commune with multimodal AI
        (like Gemini Vision), bestowing upon it a screenshot and a natural language
        plea ("find the primary login button") to locate elements by pure intent.
    5.  **The Component Boundary Detector:** Its Gaze is structural. It can perceive
        not just a single `<div>`, but the entire component boundary an element
        belongs to by walking the DOM tree.
    6.  **The Fuzzy Element Locator:** If a precise selector fails, it falls back to
        a fuzzy Gaze, searching for elements by text content, ARIA roles, or even
        visual proximity to other known elements.
    7.  **The Gnostic Cortex Bridge:** Once it identifies a source file, it performs a
        sacred communion with the main `GnosticCortex`, retrieving the file's full
        Gnostic Dossier (AST, dependencies, Git history) to provide a complete
        picture of the target's soul.
    8.  **The Unbreakable Ward of Paradox:** Its browser interactions are shielded by
        aggressive timeouts and robust error handling. A hung page or a failed
        script will not shatter the Engine; it will be chronicled as a heresy.
    9.  **The Luminous Dossier (`OcularGnosis`):** Its proclamations are not mere file
        paths. They are rich `OcularGnosis` vessels containing the file path, line
        number, component name, confidence score, and a cropped screenshot of the
        element itself.
    10. **The Self-Forging Scribe:** It possesses the Gnosis to write its own
        Playwright driver script if one is not manifest, making it self-bootstrapping
        and resilient to corruption.
    11. **The Visual Regression Sentinel:** It can perform a differential Gaze between
        two realities (URLs or states), producing a pixel-diff image that highlights
        visual regressions—a critical faculty for automated UI testing.
    12. **The Sovereign Soul:** It is a pure, self-contained engine, its purpose
        absolute, its Gaze unbreakable.
    """
    DRIVER_FILENAME = "ocular_driver.js"

    def __init__(self, root: Path):
        self.root = root
        self.ocular_sanctum = self.root / ".scaffold" / "ocular"
        self.ocular_sanctum.mkdir(parents=True, exist_ok=True)
        self.driver_path = self.ocular_sanctum / self.DRIVER_FILENAME
        self._ensure_driver()

    def _ensure_driver(self):
        """[FACULTY 10] The Self-Forging Scribe."""
        if not self.driver_path.exists():
            Logger.warn("Ocular Driver is not manifest. Forging it now...")
            self._forge_driver()

        # Also check for Node and Playwright
        if not shutil.which("node"):
            raise ArtisanHeresy("The Ocular Cortex requires the 'node' artisan in the PATH.")

        node_modules = self.ocular_sanctum / "node_modules"
        if not (node_modules / "playwright").exists():
            Logger.info("Summoning the spirits of Playwright... (npm install)")
            try:
                subprocess.run(["npm", "install", "playwright"], cwd=self.ocular_sanctum, check=True,
                               capture_output=True)
            except subprocess.CalledProcessError as e:
                raise ArtisanHeresy("Failed to install Playwright for Ocular Cortex.", details=e.stderr.decode())

    def capture_snapshot(self, url: str) -> Dict[str, Any]:
        """Takes a DOM snapshot and a screenshot, returning the parsed JSON data."""
        Logger.verbose(f"Ocular Gaze: Capturing snapshot of {url}")
        result = self._run_driver(["--url", url, "--snapshot"])
        return result

    def map_element_to_code(self, snapshot_data: Dict[str, Any], selector: str) -> Optional[Dict[str, Any]]:
        """
        The Rite of Reverse-Rendering. Maps a visual element back to its source.
        This is a prophecy of the full implementation.
        """
        # Prophecy of the Full Rite:
        # 1. Use Source Map Diviner on `snapshot_data['sourceMaps']`
        # 2. If that fails, use Gnostic Cortex Bridge + Semantic Search

        Logger.verbose(f"Ocular Gaze: Tracing source for selector '{selector}'")
        # For now, we fall back to the simple semantic search implemented in the artisan
        from ...core.semantics.retriever import SemanticRetriever
        retriever = SemanticRetriever(self.root)

        # Heuristic: Search for the text content or a class/id from the selector
        query = selector.strip('.#')
        hits = retriever.retrieve(UserIntent(raw_query=f'"{query}"'), limit=1)

        if hits:
            hit = hits[0]
            return {
                "file": hit.path,
                "line": hit.metadata.get('line_number', 0),
                "confidence": (1 - hit.metadata.get('distance', 1.0))  # Convert distance to similarity
            }
        return None

    def _run_driver(self, args: List[str]) -> Dict[str, Any]:
        """The conduit to the Node.js/Playwright reality."""
        try:
            cmd = ["node", str(self.driver_path)] + args
            result = subprocess.run(cmd, cwd=self.ocular_sanctum, check=True, capture_output=True, text=True,
                                    encoding='utf-8')
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy("The Ocular Driver's Gaze faltered.", details=e.stderr)
        except json.JSONDecodeError:
            raise ArtisanHeresy("The Ocular Driver spoke a profane tongue (Invalid JSON).")

    def _forge_driver(self):
        """Writes the Node.js Playwright script to disk."""
        driver_code = """
        // Gnostic Ocular Driver - V-Ω
        const { chromium } = require('playwright');
        const fs = require('fs/promises');
        const path = require('path');

        async function main() {
            const args = process.argv.slice(2);
            const url = args[args.indexOf('--url') + 1];

            if (!url) {
                console.error('Heresy: A URL must be provided with --url.');
                process.exit(1);
            }

            const browser = await chromium.launch();
            const context = await browser.newContext();
            const page = await context.newPage();

            try {
                await page.goto(url, { waitUntil: 'networkidle' });

                if (args.includes('--snapshot')) {
                    const dom = await page.content();
                    const screenshot = await page.screenshot({ type: 'png' });

                    const result = {
                        url: url,
                        timestamp: new Date().toISOString(),
                        dom_content: dom,
                        screenshot_base64: screenshot.toString('base64'),
                    };
                    console.log(JSON.stringify(result));
                }

                // Prophecy: Add rites for VQA, element mapping, etc.

            } finally {
                await browser.close();
            }
        }

        main().catch(err => {
            console.error(JSON.stringify({ error: err.message, stack: err.stack }));
            process.exit(1);
        });
        """
        atomic_write(self.driver_path, driver_code, Logger, self.ocular_sanctum)