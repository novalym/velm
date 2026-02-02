import json
from typing import Any, Dict, List
from ....contracts.heresy_contracts import ArtisanHeresy

# Lazy import to prevent boot lag
try:
    from playwright.sync_api import sync_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class ChromeEngine:
    """[THE KINETIC BROWSER]"""

    def execute(self, request) -> Any:
        if not PLAYWRIGHT_AVAILABLE:
            raise ArtisanHeresy("Playwright not manifest. Run `pip install playwright && playwright install`.")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=request.headless)
            page = browser.new_page(viewport=request.viewport)

            try:
                page.goto(request.url, timeout=request.timeout * 1000)

                if request.wait_for:
                    page.wait_for_selector(request.wait_for)

                # --- RITE 1: SCREENSHOT ---
                if request.action == "screenshot":
                    path = "screenshot.png"  # Default, usually overridden by Artisan logic or returned bytes
                    data = page.screenshot(full_page=True)
                    return {"binary": data, "mime": "image/png"}

                # --- RITE 2: PDF RENDER ---
                elif request.action == "pdf":
                    data = page.pdf(format="A4")
                    return {"binary": data, "mime": "application/pdf"}

                # --- RITE 3: SCRAPE / EXTRACT ---
                elif request.action == "scrape":
                    if request.extract_fields:
                        result = {}
                        for key, selector in request.extract_fields.items():
                            # Auto-detect list vs single
                            elements = page.query_selector_all(selector)
                            if len(elements) > 1:
                                result[key] = [el.inner_text() for el in elements]
                            elif elements:
                                result[key] = elements[0].inner_text()
                            else:
                                result[key] = None
                        return result
                    else:
                        # Full text fallback
                        return {"content": page.content(), "text": page.inner_text("body")}

                # --- RITE 4: INTERACTION (Simple) ---
                elif request.action == "interact":
                    if request.input_value and request.selector:
                        page.fill(request.selector, request.input_value)
                    # This is limited; complex interaction usually requires custom scripting
                    return {"status": "Interacted", "url": page.url}

            finally:
                browser.close()