# Path: packages/novalym-logic/novalym_logic/artisans/services/communication/herald.py
# -------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: LINGUISTIC_ALCHEMIST | RANK: SOVEREIGN
# SYSTEM: NOVALYM_LOGIC | PROTOCOL: Ω_SEMANTIC_SYNTHESIS_V18
# =========================================================================================

from __future__ import annotations
import re
import logging
import html
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

# --- CORE SCAFFOLD UPLINKS ---
# We assume the engine's alchemist is passed or accessible
from scaffold.core.runtime.engine import ScaffoldEngine

Logger = logging.getLogger("Herald:Alchemist")


class TheHerald:
    """
    =============================================================================
    == THE LINGUISTIC HERALD (V-Ω-TOTALITY-V18-FINAL)                         ==
    =============================================================================
    LIF: ∞ | ROLE: SCRIPTURE_TRANSFIGURATOR | RANK: LEGENDARY

    The Master Artisan of form and voice. 
    Responsible for transmuting raw Gnosis into resonant communication matter.
    """

    def __init__(self, engine: ScaffoldEngine):
        self.engine = engine
        self.logger = Logger

    def compose(self, request: Any) -> Tuple[str, str]:
        """
        [THE RITE OF SEMANTIC SYNTHESIS]
        Transmutes a CommunicationRequest into (PlainText, HTML) matter.
        """
        # 1. INITIAL CONTEXT PREPARATION
        # We clone the context to avoid side-effect pollution in the request object.
        ctx = (request.context or {}).copy()
        trace_id = getattr(request, 'trace_id', '0xVOID')

        # 2. [ASCENSION 1 & 12]: THE IDENTITY PURIFIER
        # Annihilates the "- The" anomaly and ensures signature purity.
        ctx = self._purify_identity_matrix(ctx)

        # 3. [ASCENSION 3]: KINETIC LINK GRAFTING (UTM Injection)
        # We pre-process content strings if they are raw, or let the Alchemist handle templates.
        raw_content = request.content or ""
        if raw_content:
            raw_content = self._graft_kinetic_links(raw_content, trace_id)

        # 4. THE RITE OF RENDERING (THE ALCHEMIST'S HAND)
        try:
            if not request.template:
                # PATH A: RAW CONTENT MANIFESTATION
                plain_body = raw_content
                # [ASCENSION 4]: Isomorphic HTML Splicing
                html_body = self._transmute_to_html(raw_content, trace_id)
            else:
                # PATH B: TEMPLATE ALCHEMY (Jinja2)
                # We leverage the engine's alchemist for deep file/string rendering.
                if request.template.endswith((".html", ".j2", ".scaffold")):
                    plain_body = self.engine.alchemist.render_file(request.template, ctx)
                else:
                    plain_body = self.engine.alchemist.render_string(request.template, ctx)

                # For templates, we assume the template handles its own HTML/Text split
                # or we generate a standard wrapper.
                html_body = self._wrap_in_citadel_layout(plain_body, trace_id, ctx.get("tone", "Expert"))

            # 5. [ASCENSION 7]: UTF-8 NORMALIZATION
            return plain_body.strip(), html_body.strip()

        except Exception as e:
            # [ASCENSION 11]: SOCRATIC REDEMPTION
            self.logger.error(f"[{trace_id}] Alchemical Rendering Fracture: {e}")
            fallback = f"SYSTEM_NOTICE: {raw_content}"
            return fallback, f"<html><body>{fallback}</body></html>"

    def _purify_identity_matrix(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        """
        [FACULTY]: THE IDENTITY SURGEON
        Ensures 'owner' and 'biz' strings are human-grade and title-aware.
        """
        owner_raw = str(ctx.get("owner", "The Architect"))

        # [ASCENSION 1]: Title Preservation Logic
        # Handles "The Architect", "The Founder", etc.
        if owner_raw.lower().startswith("the "):
            ctx["owner"] = owner_raw  # Keep the full majestic title
        else:
            # Standard human name: extract first word
            # "John Smith" -> "John"
            ctx["owner"] = owner_raw.split()[0].strip()

        # [ASCENSION 10]: METABOLIC DEFAULTS
        ctx.setdefault("biz", "Novalym Systems")
        return ctx

    def _graft_kinetic_links(self, text: str, trace_id: str) -> str:
        """
        [FACULTY]: THE LINK GRAFTER
        Injects tracking and identity DNA into detected URLs.
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        def replace_url(match):
            original_url = match.group(0)
            try:
                parsed = urllib.parse.urlparse(original_url)
                params = urllib.parse.parse_qs(parsed.query)

                # Add Novalym DNA
                params['utm_source'] = ['novalym']
                params['utm_medium'] = ['kinetic_signal']
                params['trace_id'] = [trace_id]

                new_query = urllib.parse.urlencode(params, doseq=True)
                new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
                return new_url
            except Exception:
                return original_url

        return re.sub(url_pattern, replace_url, text)

    def _transmute_to_html(self, text: str, trace_id: str) -> str:
        """
        [FACULTY]: ISOMORPHIC TRANSFIGURATION
        Converts raw prose into email-safe HTML matter.
        """
        safe_text = html.escape(text)
        # Convert breaks to semantic tags
        html_content = safe_text.replace("\n", "<br />")
        return self._wrap_in_citadel_layout(html_content, trace_id)

    def _wrap_in_citadel_layout(self, inner_matter: str, trace_id: str, tone: str = "Expert") -> str:
        """
        [FACULTY]: THE CITADEL LAYOUT
        Wraps any communication in the high-status Novalym aesthetic.
        """
        # [ASCENSION 8]: Tonal Tints
        tint = "#64ffda" if tone == "Expert" else "#fbbf24"  # Teal vs Amber

        return f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; padding:20px; background-color:#020202; color:#ffffff; font-family:monospace;">
            <div style="max-width:600px; margin:0 auto; border:1px solid #1a1a1a; padding:40px; border-radius:8px;">
                <div style="color:{tint}; font-weight:bold; letter-spacing:2px; margin-bottom:20px;">NOVALYM_SYSTEMS_SIGNAL</div>
                <div style="line-height:1.6; color:#cccccc;">
                    {inner_matter}
                </div>
                <div style="margin-top:40px; padding-top:20px; border-top:1px solid #1a1a1a; font-size:10px; color:#444444;">
                    TRACE_ID: {trace_id} // SOVEREIGN_EMISSION_STABLE
                </div>
            </div>
            <!-- [ASCENSION 9]: FORENSIC TRACE COMMENT: {trace_id} -->
        </body>
        </html>
        """

# == SCRIPTURE SEALED: THE HERALD IS RESONANT ==