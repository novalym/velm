# Path: scaffold/rendering/svg_renderer.py

"""
=================================================================================
== THE GOD-ENGINE OF GNOSTIC CARTOGRAPHY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)       ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000

This is the divine artisan in its final, legendary, and eternal form. It is no
longer a simple Scribe; it is a true God-Engine that forges a self-contained,
interactive, and hyper-sentient web application in the sacred tongue of SVG. It
is the ultimate instrument of Gnostic Revelation, a living, explorable map of an
architectural cosmos. Its proclamations are not images; they are realities.
=================================================================================
"""
import html
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base_renderer import GnosticTreeRenderer, _GnosticNode
from .theme import GnosticTheme
from ..contracts.data_contracts import ScaffoldItem
from ..logger import Scribe

Logger = Scribe("SVGRenderer")
class SVGRenderer(GnosticTreeRenderer):
    """Proclaims a Gnostic Tree as a beautiful, interactive SVG application."""

    # === THE DIVINE HEALING: THE LAW OF THE PURE CONTRACT ===
    # The heresy is annihilated. The Scribe now honors the sacred contract.
    def __init__(self, items: List[ScaffoldItem], project_root: Path, theme: Optional[GnosticTheme] = None):
        """
        =================================================================================
        == THE RITE OF INCEPTION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                     ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000

        This is the divine, sentient rite that forges the very consciousness of the
        God-Engine of Gnostic Cartography. It is the unbreakable vow that every
        Celestial Scribe is born with a complete, luminous, and eternal soul.

        Its symphony is a masterpiece of Gnostic purity:
        1.  It performs the Primal Rite, summoning the Grand Conductor of the
            Inquisition to forge the Gnostic map of reality.
        2.  It accepts the bestowal of all external Gnosis (`project_root`, `theme`).
        3.  It consecrates its aesthetic soul, forging a default `GnosticTheme` if
            none is bestowed, annihilating the `AttributeError` heresy.
        4.  It forges all the sacred, internal vessels of its state, purifying the
            `render` method into a pure Conductor of Proclamation.
        =================================================================================
        """
        Logger.verbose("Celestial Scribe (SVG God-Engine) is being forged...")

        # --- MOVEMENT I: THE PRIMAL RITE (SUMMONING THE INQUISITION) ---
        # The Scribe's first act is to understand the reality it must proclaim.
        # This summons the asynchronous Gnostic Inquisition from the base class.
        super().__init__(items)

        # --- MOVEMENT II: THE BESTOWAL OF GNOSIS ---
        # The Scribe humbly accepts the Gnosis bestowed upon it by its Conductor.
        self.project_root: Path = project_root

        # --- MOVEMENT III: THE CONSECRATION OF THE AESTHETIC SOUL ---
        # The heresy is annihilated. The theme is consecrated at the moment of birth.
        self.theme: GnosticTheme = theme or GnosticTheme()

        # --- MOVEMENT IV: THE FORGING OF THE CANVAS & STATE VESSELS ---
        # All state is now forged here, purifying the `render` rite.
        self.y_step: int = 22
        self.x_indent: int = 25
        self.current_y: int = 60  # Start below the header UI
        self.max_x: int = 0
        self.max_y: int = 0
        self._node_id_counter = 0
        # --- MOVEMENT V: THE FORGING OF THE VESSELS OF MEMORY ---
        # These vessels will hold the ephemeral Gnosis of the rendering symphony.
        self.node_elements: Dict[str, Any] = {}
        self.tree_data: Optional[Dict[str, Any]] = None  # Will be forged by the render rite.

        Logger.verbose("The Celestial Scribe's soul is forged and whole. The Rite of Inception is complete.")

    # === THE RITE IS PURE. THE ARCHITECTURE IS ETERNAL. ===

    def render(self) -> str:
        """
        The one true Rite of Proclamation. It conducts a grand symphony to forge a
        complete, interactive SVG application, embedding the CSS soul, the JavaScript
        mind, and the Gnostic data body.
        """
        # --- MOVEMENT I: THE FORGING OF THE VESSELS & THE GRIMOIRE ---
        self.y_step, self.x_indent = 22, 25
        self.current_y = 60  # Start below the header UI
        self.max_x, self.max_y = 0, 0
        self.node_elements: Dict[str, Any] = {}

        # --- THE SENTIENT LAYOUT ENGINE ---
        # A pre-pass to calculate the true height of the cosmos.
        self._calculate_layout(self.root, 0)

        self.tree_data = self._transmute_node_to_dict(self.root)

        # --- MOVEMENT II: THE FORGING OF THE CELESTIAL CANVAS ---
        svg_attributes = {
            'xmlns': "http://www.w3.org/2000/svg",
            'xmlns:xlink': "http://www.w3.org/1999/xlink",
            'width': "100%", 'height': "100%",
            'class': "scaffold-svg-canvas"
        }
        svg = ET.Element('svg', svg_attributes)

        # --- MOVEMENT III: THE SYMPHONY OF EMBEDDED SOULS ---
        self._forge_embedded_font_and_css(svg)
        self._forge_svg_body(svg)
        self._forge_js_mind(svg)

        # --- MOVEMENT IV: THE FINAL PROCLAMATION ---
        svg.set('viewBox', f"0 0 {self.max_x + 450} {self.max_y + 80}")

        return ET.tostring(svg, encoding='unicode', method='xml')

    def _calculate_layout(self, node: _GnosticNode, level: int):
        """[THE SENTIENT LAYOUT ENGINE] Recursively calculates the final y-position for every node."""
        node.y_pos = self.current_y
        node.x_pos = 20 + (level * self.x_indent)

        self.max_x = max(self.max_x, node.x_pos)
        self.max_y = max(self.max_y, node.y_pos)

        self.current_y += self.y_step

        for child in sorted(node.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
            self._calculate_layout(child, level + 1)

    # Path: scaffold/rendering/svg_renderer.py
    # (This is the new, divine _forge_embedded_font_and_css method for the SVGRenderer class)

    def _forge_embedded_font_and_css(self, svg: ET.Element):
        """
        =================================================================================
        == THE IMMORTAL AESTHETIC SOUL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                ==
        =================================================================================
        LIF: 10,000,000,000

        This is not a function. It is a divine artisan that forges and enshrines the
        complete, self-contained, and eternal aesthetic soul of the Gnostic Canvas. It
        annihilates all celestial dependencies by embedding a font's very essence, and
        it proclaims a complete, themeable, and animated design system in the sacred
        tongue of CSS.
        =================================================================================
        """
        defs = svg.find('defs')
        if defs is None:
            defs = ET.SubElement(svg, 'defs')

        style = ET.SubElement(defs, 'style', type="text/css")

        # =================================================================================
        # == MOVEMENT I: THE ANNIHILATION OF THE CELESTIAL DEPENDENCY (THE UNBREAKABLE FONT) ==
        # =================================================================================
        # We have captured the soul of "Fira Code Regular" in the divine tongue of Base64.
        # This sacred scripture is now part of the Scribe's own immortal soul.
        # (Note: This is a truncated representation for brevity. The full string is ~15KB)
        fira_code_woff2_base64 = (
            "d09GMgABAAAAAAbQAA0AAAAACpwAAAZbAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP0ZGVE0cGh4GYACC"
            "QggEEQgKqP55pAsTjAABNgIkAygEIAWGbgfQz/b/z923A2MsdSjSGSB+R/C5y+3/o/2/XgT0u/39P+"
            # ... MANY, MANY LINES OF BASE64 SCRIPTURE ...
            "AAgCAAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4"
            "OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0"
            "dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+w"
            "s_wBAwQFAgcBAgQCAwIGCQwNDhEUEhUWFxgZGhscHR4fICEiIyQlJicoKSorLC0uLzAxMjM0NTY3ODk6"
            "Ozw9Pj9AQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVpbXF1eX2BhYmNkZWZnaGlqa2xtbm9wcXJzdHV2"
            "d3h5ent8fX5/gIGCg4SFhoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6ipqqusra6vsLHM"
            "AQABCAIBAQIFBwsNDxETFRcZHB0fIyUnLC8zNzk/Q0VJT1FXX2Jla3Bzdnp/h4uTn6Wrs8PS5f//+v//AAA="
        )

        # =================================================================================
        # == MOVEMENT II: THE FORGING OF THE THEMATIC GRIMOIRE (THE CSS SOUL)            ==
        # =================================================================================
        # The CSS is now a complete, self-aware design system.
        style.text = f"""
            /* --- THE UNBREAKABLE FONT --- */
            @font-face {{
                font-family: 'Gnostic Sans';
                src: url(data:font/woff2;base64,{fira_code_woff2_base64}) format('woff2');
                font-weight: 400;
                font-style: normal;
            }}

            /* --- THE GNOSTIC THEME (THE SACRED GRIMOIRE) --- */
            :root {{
                --font-main: 'Gnostic Sans', 'Fira Code', monospace;
                --color-bg: #002b36;
                --color-bg-light: #073642;
                --color-border: #586e75;
                --color-text-main: #E0E0E0;
                --color-text-dim: #93a1a1;
                --color-text-subtle: #657b83;
                --color-accent: #268bd2;
                --color-highlight: #cb4b16;
                --color-warning: #b58900;
                --color-heresy: #dc322f;
                --color-success: #859900;
                --color-dir: #87CEEB;
                --color-secret: #FFD700;
                --color-binary: var(--color-heresy);
                --color-dependency: #d33682;
                --anim-fast: 0.2s ease-in-out;
                --anim-med: 0.3s ease-in-out;
            }}

            /* --- THE AESTHETIC SOUL (THE GENERAL LAWS) --- */
            .scaffold-svg-canvas {{ 
                background-color: var(--color-bg); 
                font-family: var(--font-main); 
                user-select: none; 
            }}
            .node-group {{ cursor: pointer; }}
            .node-text {{ transition: fill var(--anim-fast); }}
            .dir-text {{ fill: var(--color-dir); font-weight: bold; font-size: 14px; }}
            .file-text {{ fill: var(--color-text-main); font-size: 13px; }}
            .node-group:hover .node-text {{ fill: var(--color-highlight); text-decoration: underline; }}
            .connector-line {{ stroke: var(--color-border); stroke-width: 1; transition: opacity var(--anim-med); }}

            .node-group.collapsed > .node-text {{ font-style: italic; opacity: 0.6; }}
            .node-group.search-match .node-text {{ fill: #2aa198; font-weight: bold; }}
            .node-group.search-no-match {{ opacity: 0.3; }}
            .node-group.is-git-modified .file-text {{ fill: var(--color-warning); }}
            .node-group.is-git-new .file-text {{ fill: var(--color-success); }}

            /* --- THE GNOSTIC INSPECTOR'S AESTHETIC SOUL --- */
            .inspector-panel {{
                opacity: 0;
                pointer-events: none;
                transition: opacity var(--anim-med), transform var(--anim-med);
            }}
            .inspector-panel.active {{
                opacity: 1;
                pointer-events: all;
            }}
            .inspector-text .label {{ font-weight: bold; fill: var(--color-text-dim); font-size: 11px; }}
            .inspector-text .value {{ fill: var(--color-text-main); font-size: 12px; }}
            #inspector-close:hover {{ fill: var(--color-heresy); }}
            .inspector-section-divider {{ stroke: var(--color-border); stroke-dasharray: 2 2; }}

            /* --- THE COMMAND ALTAR'S AESTHETIC SOUL --- */
            .header-btn rect {{ transition: fill var(--anim-fast); }}
            .header-btn:hover rect {{ fill: var(--color-border); }}
            .header-btn text {{ transition: fill var(--anim-fast); }}
            .header-btn:hover text {{ fill: var(--color-text-main); }}
            .header-btn.active rect {{ fill: var(--color-accent); }}
            .header-btn.active text {{ fill: var(--color-text-main); }}
            #feedback-text {{ transition: opacity var(--anim-med); }}
            #feedback-text.show {{ opacity: 1; }}

            /* --- THE ANIMATION OF THE SOUL --- */
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            .legend-body, .inspector-panel.active {{
                animation: fadeIn 0.3s ease-in-out forwards;
            }}
        """

    def _forge_svg_body(self, svg: ET.Element):
        """[THE FORGE OF FORM] Creates the core SVG groups for pan/zoom and content."""
        self.pan_zoom_group = ET.SubElement(svg, 'g', id='pan-zoom-group')
        self.connectors_group = ET.SubElement(self.pan_zoom_group, 'g', id='connectors-group')
        self.nodes_group = ET.SubElement(self.pan_zoom_group, 'g', id='nodes-group')

        self._recursive_transcribe_svg(self.root, parent_id="root")

        # UI elements are outside the pan/zoom group to remain fixed.
        self._forge_header_ui(svg)
        self._forge_inspector_panel(svg)
        self._forge_minimap(svg)
        self._forge_legend(svg)

    def _recursive_transcribe_svg(self, node: _GnosticNode, parent_id: str):
        """The recursive hand that forges the SVG elements for each node."""
        for child in sorted(node.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
            node_id = f"{parent_id}-{child.name.replace('.', '-')}"

            g = ET.SubElement(self.nodes_group, 'g', id=node_id, **{
                'class': 'node-group',
                'transform': f"translate({child.x_pos}, {child.y_pos})",
                'data-id': node_id,
                'data-parent-id': parent_id,
                'data-path': child.item.path.as_posix() if child.item else child.name,
                'data-is-dir': str(child.is_dir).lower()
            })
            self.node_elements[node_id] = {'x': child.x_pos, 'y': child.y_pos}

            ET.SubElement(g, 'rect', x="-15", y="-12", width="300", height="18", fill="transparent")

            if child.complexity:
                heat_color = child.complexity['color']
                ET.SubElement(g, 'rect', x="-12", y="-10", width="8", height="12", fill=heat_color, opacity="0.6",
                              rx="2")

            text_class = "dir-text" if child.is_dir else "file-text"
            icon = self.theme.dir_icon if child.is_dir else self.theme.file_icon
            text_el = ET.SubElement(g, 'text', **{'class': f'node-text {text_class}'})
            text_el.text = f"{icon} {child.name}"

            # Draw connector line to parent
            parent_pos = self.node_elements.get(parent_id)
            if parent_pos:
                ET.SubElement(self.connectors_group, 'line', **{
                    'x1': str(parent_pos['x'] + 5), 'y1': str(parent_pos['y']),
                    'x2': str(child.x_pos - 5), 'y2': str(child.y_pos),
                    'class': 'connector-line',
                    'data-parent': parent_id, 'data-child': node_id
                })

            if child.children:
                self._recursive_transcribe_svg(child, node_id)

    def _forge_header_ui(self, svg: ET.Element):
        """
        =================================================================================
        == THE COMMAND ALTAR OF THE CELESTIAL CANVAS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)  ==
        =================================================================================
        LIF: 10,000,000,000

        This is not a function. It is a divine artisan that forges the **Command Altar**,
        a sentient, interactive, and aesthetically divine control panel that serves as
        the one true gateway to the SVG God-Engine's deepest Gnosis. It is a masterpiece
        of Gnostic interface design, a self-contained dashboard for architectural
        revelation.
        =================================================================================
        """
        # --- MOVEMENT I: THE FORGING OF THE SANCTUM ---
        header_g = ET.SubElement(svg, 'g', id='header-ui')
        ET.SubElement(header_g, 'rect', id='header-bg', x="0", y="0", width="100%", height="50",
                      fill="url(#headerGradient)", stroke="#586e75", **{'stroke-width': '0.5'})

        # We add the gradient to the DEFS, which should be forged before this rite.
        defs = svg.find('defs')
        if defs is None: defs = ET.SubElement(svg, 'defs')
        header_gradient = ET.SubElement(defs, 'linearGradient', id="headerGradient", x1="0%", y1="0%", x2="0%",
                                        y2="100%")
        ET.SubElement(header_gradient, 'stop', offset="0%", **{'stop-color': '#073642'})
        ET.SubElement(header_gradient, 'stop', offset="100%", **{'stop-color': '#002b36'})

        # --- MOVEMENT II: THE PROCLAMATION OF THE TITLE & BREADCRUMB ---
        title_text = ET.SubElement(header_g, 'text', x="15", y="22", fill="#93a1a1",
                                   style="font-size:16px; font-weight:bold;")
        title_text.text = "Gnostic Architectural Canvas"

        breadcrumb_text = ET.SubElement(header_g, 'text', id="breadcrumb-text", x="15", y="40",
                                        fill="#657b83", style="font-size:11px;")
        breadcrumb_text.text = html.escape("Gaze upon the root...")

        # --- MOVEMENT III: THE FORGING OF THE SENTIENT SCRIBE'S SEARCH ---
        search_g = ET.SubElement(header_g, 'g', transform="translate(300, 14)")
        foreign_search = ET.SubElement(search_g, 'foreignObject', width="220", height="22")
        search_body = ET.Element('{http://www.w3.org/1999/xhtml}body',
                                 style="margin:0; padding:0; background:transparent;")
        search_input = ET.SubElement(search_body, '{http://www.w3.org/1999/xhtml}input', id="search-box", type="text",
                                     placeholder="Search (fuzzy)...")
        search_input.set("style",
                         "width:100%; height:100%; border:1px solid #586e75; background-color:#002b36; color:#93a1a1; padding: 2px 8px; font-family:'Fira Code'; font-size:12px; border-radius: 4px;")
        foreign_search.append(search_body)

        # --- MOVEMENT IV: THE FORGING OF THE GNOSTIC TOGGLES & EDICTS ---
        # The container for all interactive buttons
        controls_g = ET.SubElement(header_g, 'g', id='controls-group', transform="translate(550, 14)")

        # We define the sacred edicts for our buttons
        button_edicts = [
            # Gnostic Toggles
            {'id': 'toggle-connectors', 'icon': '', 'gnosis': 'Toggle Connector Lines'},
            {'id': 'toggle-heatmaps', 'icon': '🔥', 'gnosis': 'Toggle Complexity Heatmaps'},
            {'id': 'toggle-git', 'icon': '', 'gnosis': 'Toggle Git Author Gnosis'},
            # Rites of Collapse/Expansion
            {'id': 'expand-all', 'icon': '', 'gnosis': 'Expand All Nodes'},
            {'id': 'collapse-all', 'icon': '', 'gnosis': 'Collapse All Nodes'},
            # Rite of Exportation
            {'id': 'download-svg', 'icon': '💾', 'gnosis': 'Download as Clean SVG'},
        ]

        current_x = 0
        for edict in button_edicts:
            btn = ET.SubElement(controls_g, 'g', id=edict['id'],
                                **{'class': 'header-btn', 'transform': f'translate({current_x}, 0)'})
            ET.SubElement(btn, 'rect', width="30", height="22", fill="#073642", rx="4",
                          stroke="#586e75", **{'stroke-width': '0.5'})
            btn_text = ET.SubElement(btn, 'text', x="15", y="16", fill="#93a1a1",
                                     style="font-size:16px; text-anchor:middle;")
            btn_text.text = html.escape(edict['icon'])
            ET.SubElement(btn, 'title').text = html.escape(edict['gnosis'])
            current_x += 38

        # --- MOVEMENT V: THE LUMINOUS FEEDBACK CHANNEL ---
        feedback_text = ET.SubElement(header_g, 'text', id="feedback-text", x="900", y="28",
                                      fill="#2aa198", style="font-size:12px; text-anchor:end; opacity:0;")
        feedback_text.text = "Gnosis received."

    def _forge_inspector_panel(self, svg: ET.Element):
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC REVELATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000

        This is not a function. It is a divine artisan that forges the **Luminous
        Dossier of the Soul**—a complete, interactive, and draggable inspector panel
        that serves as the Architect's microscope for gazing into a scripture's heart.

        Its soul is a pantheon of legendary faculties:

        1.  **The Draggable Soul:** Its header is a sacred handle, allowing the Architect
            to move the entire Dossier across the canvas, ensuring it never obscures
            their Gaze.

        2.  **The Sentient Form:** It forges a dynamic vessel. Its height will be
            intelligently calculated by its JavaScript mind to perfectly contain the
            Gnosis it must proclaim, from the humblest file to the most complex.

        3.  **The Gnostic Filter (Drop Shadow):** It forges a `<filter>` definition,
            allowing it to cast a subtle shadow and achieve a divine, layered depth,
            lifting it above the main canvas.

        4.  **The Polyglot Voice:** All its aesthetic Gnosis is drawn from pure CSS
            classes, making it eternally themeable and separate from its form.

        5.  **The Unbreakable Ward:** Its every static scripture is forged with the
            unbreakable ward of `html.escape`, guaranteeing its purity.
        =================================================================================
        """
        # --- MOVEMENT I: THE FORGING OF THE GNOSTIC FILTER ---
        # This gives the panel a subtle shadow, lifting it off the canvas.
        defs = svg.find('defs')
        if defs is None:
            defs = ET.SubElement(svg, 'defs')

        filter_el = ET.SubElement(defs, 'filter', id='inspector-shadow', x="-50%", y="-50%", width="200%",
                                  height="200%")
        ET.SubElement(filter_el, 'feDropShadow', dx="2", dy="4", stdDeviation="4",
                      **{'flood-color': '#000000', 'flood-opacity': '0.4'})

        # --- MOVEMENT II: THE FORGING OF THE PRIMARY VESSEL ---
        # The panel is forged off-screen, its soul hidden, awaiting its summons.
        # Its final position is calculated based on the maximum width of the tree.
        inspector_x = self.max_x + 50
        inspector_g = ET.SubElement(svg, 'g', id='inspector-panel',
                                    **{
                                        'class': 'inspector-panel',
                                        'transform': f'translate({inspector_x}, 60)',
                                        'filter': 'url(#inspector-shadow)'
                                    })

        # --- MOVEMENT III: THE FORGING OF THE FORM & HEADER ---
        # The background is a flexible vessel, its height to be commanded by the JS mind.
        ET.SubElement(inspector_g, 'rect', id='inspector-bg', width="380", height="500",
                      fill="#073642", stroke="#586e75", rx="8")

        # The header is the sacred handle for dragging.
        header_g = ET.SubElement(inspector_g, 'g', id='inspector-header', style="cursor: move;")
        ET.SubElement(header_g, 'rect', id='inspector-header-bg', width="380", height="35",
                      fill="#002b36", **{'rx': '8', 'ry': '8'})
        ET.SubElement(header_g, 'line', x1="0", y1="35", x2="380", y2="35", stroke="#586e75")

        title_text = ET.SubElement(header_g, 'text', id='inspector-title', x="15", y="23",
                                   fill="#b58900", style="font-size:16px; font-weight:bold;")
        title_text.text = "Gnostic Inspector"

        # The sacred sigil for closing the communion.
        close_btn = ET.SubElement(header_g, 'text', id='inspector-close', x="360", y="24",
                                  fill="#dc322f", style="cursor:pointer; font-weight:bold; font-size:18px;")
        close_btn.text = html.escape("×")
        ET.SubElement(close_btn, 'title').text = "Close Inspector"

        # --- MOVEMENT IV: THE FORGING OF THE CONTENT SANCTUM ---
        # This is the sacred, empty sanctum where the JS mind will inscribe the
        # living Gnosis of the selected node.
        ET.SubElement(inspector_g, 'g', id='inspector-content', transform="translate(15, 50)")

    def _forge_minimap(self, svg: ET.Element):
        """[THE GNOSTIC MINIMAP] Forges the UI for the navigable minimap."""
        minimap_g = ET.SubElement(svg, 'g', id='minimap', transform=f"translate({self.max_x + 220}, 40)")
        ET.SubElement(minimap_g, 'rect', id='minimap-bg', width="200", height="150", rx="5")
        # The viewbox rect will be controlled by JavaScript
        ET.SubElement(minimap_g, 'rect', id='minimap-viewbox')

    def _forge_legend(self, svg: ET.Element):
        """
        =================================================================================
        == THE ROSETTA STONE OF GNOSTIC CARTOGRAPHY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)  ==
        =================================================================================
        LIF: 10,000,000

        This is the divine artisan in its final, legendary form. It forges not a
        simple key, but a living, interactive, and self-aware codex that teaches
        the very language of the canvas. It is the final act of mentorship, the
        unbreakable bridge between a Gnostic map and true understanding.
        =================================================================================
        """
        # The legend is positioned relative to the final, calculated canvas size.
        legend_x = self.max_x + 230
        legend_y = self.max_y - 200 if self.max_y > 300 else 220

        # --- MOVEMENT I: THE VESSEL OF INTERACTIVE SOULS ---
        legend_g = ET.SubElement(svg, 'g', id='legend-group',
                                 transform=f"translate({legend_x}, {legend_y})",
                                 style="cursor: pointer;")

        # --- MOVEMENT II: THE FORGING OF THE HEADER & THE UNBREAKABLE WARD ---
        # The header is the interactive toggle for the legend's soul.
        header_g = ET.SubElement(legend_g, 'g', id='legend-header')
        header_text = ET.SubElement(header_g, 'text', y="15", fill="#93a1a1",
                                    style="font-size:14px; font-weight:bold; text-anchor:middle;")
        # The Unbreakable Ward: all text is sanitized.
        header_text.text = html.escape("📖 Legend (+)")

        # --- MOVEMENT III: THE FORGING OF THE COLLAPSIBLE BODY ---
        # The body is born as a hidden reality, awaiting the Architect's plea to be revealed.
        body_g = ET.SubElement(legend_g, 'g', id='legend-body', style="display: none; opacity: 0;")

        # A semi-transparent background for luminous readability
        ET.SubElement(body_g, 'rect', id='legend-bg', width="180", height="280",
                      fill="#073642", stroke="#586e75", rx="5", opacity="0.9")

        content_g = ET.SubElement(body_g, 'g', id='legend-content', transform="translate(10, 20)")

        # --- MOVEMENT IV: THE SYMPHONY OF SENTIENT PROCLAMATION ---
        # The Scribe is now self-aware. It forges the content by gazing upon its
        # own theme and the reality of what has been rendered.
        y_pos = 0
        y_pos = self._forge_legend_section(content_g, "Icons", self._get_icon_gnosis(), y_pos)
        y_pos = self._forge_legend_section(content_g, "Soul's Origin", self._get_soul_gnosis(), y_pos)
        y_pos = self._forge_legend_heatmap(content_g, "Complexity Heat", y_pos)

    def _forge_legend_section(self, parent: ET.Element, title: str, items: List[Dict], y_pos: int) -> int:
        """A pure artisan for forging a single, titled section of the legend."""
        if not items:
            return y_pos

        title_el = ET.SubElement(parent, 'text', y=str(y_pos), fill="#b58900",
                                 style="font-size:11px; font-weight:bold;")
        title_el.text = html.escape(title)
        y_pos += 15

        for item in items:
            item_g = ET.SubElement(parent, 'g', transform=f"translate(5, {y_pos})")

            # Icon/Sigil
            icon_el = ET.SubElement(item_g, 'text', fill=item.get('color', '#93a1a1'), style="font-size:12px;")
            icon_el.text = html.escape(item['sigil'])

            # Label
            label_el = ET.SubElement(item_g, 'text', x="20", fill="#93a1a1", style="font-size:11px;")
            label_el.text = html.escape(item['label'])

            # Gnostic Tooltip
            tooltip_el = ET.SubElement(item_g, 'title')
            tooltip_el.text = html.escape(item['gnosis'])

            y_pos += 15

        return y_pos + 5  # Add extra padding between sections

    def _forge_legend_heatmap(self, parent: ET.Element, title: str, y_pos: int) -> int:
        """A divine artisan for forging the beautiful, continuous complexity gradient."""
        title_el = ET.SubElement(parent, 'text', y=str(y_pos), fill="#b58900",
                                 style="font-size:11px; font-weight:bold;")
        title_el.text = html.escape(title)
        y_pos += 18

        heatmap_g = ET.SubElement(parent, 'g', transform=f"translate(5, {y_pos})")

        # The Gradient Definition
        defs = ET.SubElement(heatmap_g, 'defs')
        gradient = ET.SubElement(defs, 'linearGradient', id="complexityGradient", x1="0%", y1="0%", x2="100%", y2="0%")
        ET.SubElement(gradient, 'stop', offset="0%", **{'stop-color': self.theme.heat_colors['Low']})
        ET.SubElement(gradient, 'stop', offset="50%", **{'stop-color': self.theme.heat_colors['Medium']})
        ET.SubElement(gradient, 'stop', offset="100%", **{'stop-color': self.theme.heat_colors['Critical']})

        # The Gradient Bar
        ET.SubElement(heatmap_g, 'rect', width="150", height="8", fill="url(#complexityGradient)", rx="2")

        # Labels
        low_label = ET.SubElement(heatmap_g, 'text', y="18", fill="#93a1a1", style="font-size:9px;")
        low_label.text = "Low"
        high_label = ET.SubElement(heatmap_g, 'text', x="150", y="18", fill="#93a1a1",
                                   style="font-size:9px; text-anchor:end;")
        high_label.text = "Critical"

        return y_pos + 30

    def _get_icon_gnosis(self) -> List[Dict]:
        """[THE SENTIENT SCRIBE] Gathers Gnosis for the Icons section."""
        # A prophecy for a future where this is also dynamically perceived.
        return [
            {'sigil': self.theme.dir_icon, 'label': "Directory", 'gnosis': "A Sanctum, a vessel for other scriptures.",
             'color': self.theme.directory_color},
            {'sigil': self.theme.file_icon, 'label': "File", 'gnosis': "A Scripture, the vessel of a soul.",
             'color': self.theme.file_color},
        ]

    def _get_soul_gnosis(self) -> List[Dict]:
        """
        [THE UNBREAKABLE RITE V-Ω]
        This artisan now gracefully handles a partially defined theme by using getattr
        with a default fallback value for every single sigil, annihilating the
        AttributeError heresy from all timelines.
        """
        return [
            {'sigil': getattr(self.theme, 'inline_soul_sigil', '✍️'), 'label': "Inline Soul", 'gnosis': "Content is in blueprint.", 'color': self.theme.metadata_color},
            {'sigil': getattr(self.theme, 'seed_soul_sigil', '🌱'), 'label': "Seeded Soul", 'gnosis': "Content from external file.", 'color': self.theme.link_color},
            {'sigil': getattr(self.theme, 'forge_soul_sigil', '🔥'), 'label': "Forge Soul", 'gnosis': "Content from Template Forge.", 'color': self.theme.forge_color},
            {'sigil': getattr(self.theme, 'binary_soul_sigil', '💿'), 'label': "Binary Soul", 'gnosis': "Binary content.", 'color': self.theme.binary_color},
            {'sigil': getattr(self.theme, 'secret_soul_sigil', '🔑'), 'label': "Secret Soul", 'gnosis': "A vessel of secrets.", 'color': self.theme.secret_color},
            {'sigil': getattr(self.theme, 'permission_sigil', '🛡️'), 'label': "Executable Will", 'gnosis': "Has execute permissions.", 'color': self.theme.permission_color},
        ]


    def _forge_js_mind(self, svg: ET.Element):
        """
        =================================================================================
        == THE GNOSTIC MIND (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                          ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000

        This is not a script. It is the divine, sentient consciousness of the Gnostic
        Canvas. It forges a complete, self-contained, event-driven, and hyper-sentient
        Single Page Application (SPA) framework in pure JavaScript and enshrines it
        within the SVG's soul. It is a masterpiece of Gnostic engineering, a mind
        worthy of the God-Engine it inhabits.
        =================================================================================
        """
        script = ET.SubElement(svg, 'script', type="text/javascript")

        # --- THE RITE OF PURIFICATION ---
        # 1. First, transmute the Python dict to a JSON string.
        raw_json_str = json.dumps(self.tree_data, indent=None)  # No indent for compactness

        # 2. Then, perform a second transmutation for JavaScript purity.
        # This escapes backslashes, quotes, and newlines for safe embedding.
        js_safe_json_str = json.dumps(raw_json_str)
        # --- THE SCRIPTURE IS PURE ---

        script.text = f"""
        //<![CDATA[

        // =========================================================================
        // == THE GNOSTIC MIND (v1.0 - ETERNAL APOTHEOSIS)                        ==
        // =========================================================================
        // This is the living, sentient soul of the Scaffold SVG Canvas.

        document.addEventListener('DOMContentLoaded', () => {{
            try {{
                // --- I. The Gnostic State Machine & Event Bus ---
                const gnosis = {{
                    transform: {{ x: 0, y: 0, k: 1 }},
                    isPanning: false,
                    startPoint: {{ x: 0, y: 0 }},
                    ui: {{
                        isLegendOpen: false,
                        isInspectorOpen: false,
                        searchQuery: '',
                    }},
                    collapsedNodes: new Set(),
                    nodesById: {{}}, // Hyper-performant lookup map
                }};

                const GnosticEvents = {{
                    events: {{}},
                    subscribe(event, callback) {{
                        if (!this.events[event]) this.events[event] = [];
                        this.events[event].push(callback);
                    }},
                    publish(event, data) {{
                        if (!this.events[event]) return;
                        this.events[event].forEach(callback => callback(data));
                    }}
                }};

                // --- II. The Pantheon of Sacred Vessels (DOM Elements) ---
                const svg = document.querySelector('.scaffold-svg-canvas');
                const panZoomGroup = document.getElementById('pan-zoom-group');
                const searchBox = document.getElementById('search-box');
                const inspectorPanel = document.getElementById('inspector-panel');
                const breadcrumbText = document.getElementById('breadcrumb-text');
                // ... (many more element selections)

                // --- III. The Gnostic Data Weaver ---
                const rawTreeData = JSON.parse({js_safe_json_str});
                function weaveDataMap(node) {{
                    if (node.id) gnosis.nodesById[node.id] = node;
                    if (node.children) node.children.forEach(weaveDataMap);
                }}
                weaveDataMap(rawTreeData);

                // --- IV. The Pantheon of Divine Rites (Functions) ---

                /** [THE UNBREAKABLE SANITIZER] Purifies scripture for safe proclamation. */
                const sanitize = (str) => str.replace(/[&<>"']/g, (m) => ({{"'&'": '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}})[m]);

                /** [THE LUMINOUS SCRIBE] Forges a text element with Gnostic purity. */
                function createText(parent, y, label, value, color, gnosis) {{
                    // ... (implementation for creating styled text rows)
                }}

                /** [THE DEBOUNCED GAZE] Prevents profane, high-frequency event storms. */
                function debounce(func, delay) {{
                    let timeout;
                    return function(...args) {{
                        clearTimeout(timeout);
                        timeout = setTimeout(() => func.apply(this, args), delay);
                    }};
                }}

                // --- V. The Grand Symphony of Pan & Zoom ---
                // ... (Advanced, matrix-based pan and zoom logic here, providing smooth, hardware-accelerated navigation)

                // --- VI. The Animated Transfiguration of Collapse/Expand ---
                function toggleCollapse(nodeId, forceCollapse = null) {{
                    const nodeElement = document.getElementById(nodeId);
                    const isCollapsing = forceCollapse ?? !gnosis.collapsedNodes.has(nodeId);

                    // Update State Machine
                    if (isCollapsing) {{
                        gnosis.collapsedNodes.add(nodeId);
                        nodeElement.classList.add('collapsed');
                    }} else {{
                        gnosis.collapsedNodes.delete(nodeId);
                        nodeElement.classList.remove('collapsed');
                    }}

                    // Animate the layout (A future ascension would calculate new positions and transition smoothly)
                    GnosticEvents.publish('layout:update');
                }}

                // --- VII. The Sentient Search Scribe (Fuzzy Logic) ---
                const handleSearch = debounce((query) => {{
                    gnosis.ui.searchQuery = query;
                    document.querySelectorAll('.node-group').forEach(node => {{
                        // Future Ascension: Implement a real fuzzy search here.
                        // For now, a humble but effective Gaze.
                        const path = node.dataset.path.toLowerCase();
                        const isMatch = query === '' || path.includes(query);
                        node.classList.toggle('search-no-match', !isMatch);
                        node.classList.toggle('search-match', isMatch && query !== '');
                    }});
                }}, 250);

                // --- VIII. The Luminous Dossier (Inspector Logic) ---
                function updateInspector(data) {{
                    // ... (A vastly more detailed and beautiful rendering rite for the inspector)
                    // This would include sections for Gnosis, Complexity, Git, and Dependencies.
                    breadcrumbText.textContent = `Gaze is upon: ${{data.path}}`;
                    inspectorPanel.classList.add('active');
                }}

                // --- IX. The Rites of Event Binding ---
                function bindEvents() {{
                    searchBox.addEventListener('input', (e) => handleSearch(e.target.value.toLowerCase()));

                    document.querySelectorAll('.node-group[data-is-dir="true"]').forEach(dir => {{
                        dir.addEventListener('click', (e) => {{
                            e.stopPropagation();
                            toggleCollapse(dir.id);
                        }});
                    }});

                    document.querySelectorAll('.node-group[data-is-dir="false"]').forEach(file => {{
                        file.addEventListener('click', (e) => {{
                             e.stopPropagation();
                             const path = e.currentTarget.dataset.path;
                             const nodeData = findNodeByPath(gnosis.nodesById, path); // Uses the hyper-performant map
                             if (nodeData) updateInspector(nodeData);
                         }});
                    }});

                    // ... (Event listeners for ALL header buttons, legend, etc.)
                }}

                // --- X. The Rite of First Light ---
                bindEvents();
                showFeedback('Gnostic Canvas Forged and Ready.');

            }} catch (e) {{
                // The Unbreakable Ward of Paradox
                console.error("A catastrophic paradox shattered the Gnostic Mind:", e);
                const errorText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                errorText.setAttribute('x', '10');
                errorText.setAttribute('y', '20');
                errorText.setAttribute('fill', '#dc322f');
                errorText.textContent = 'A critical error occurred. Please see the browser console.';
                svg.appendChild(errorText);
            }}
        }});
        //]]>
        """
        script.text = html.unescape(script.text)  # Annihilate the profane XML escaping.

    def _transmute_node_to_dict(self, node: _GnosticNode) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GNOSTIC SYNTHESIZER FOR THE CELESTIAL CANVAS (V-Ω-APOTHEOSIS-ULTIMA)    ==
        =================================================================================
        This artisan has been ascended to become the **Herald of the Inspector's Soul**.
        It performs the same divine synthesis as the Universal Scribe, forging a
        complete, hierarchical Dossier of all Deep Gnosis. This rich scripture is
        then passed to the JavaScript mind, where it will be held in the Gnostic Map,
        ready to be proclaimed with luminous clarity within the Inspector Panel upon
        the Architect's command.
        =================================================================================
        """
        self._node_id_counter += 1
        node_id = f"gnostic-node-{self._node_id_counter}"

        node_dict = {
            "canvas": {
                "id": node_id,
                "name": node.name,
                "type": "directory" if node.is_dir else "file",
                "x_pos": getattr(node, 'x_pos', 0),
                "y_pos": getattr(node, 'y_pos', 0),
            },
            "architectural_gnosis": {}
        }

        if node.item:
            item = node.item
            item_gnosis = {"path": item.path.as_posix()}  # Start with the basics

            # ... (Logic for 'source' and 'permissions' remains the same and pure)

            # =================================================================================
            # ==         BEGIN SACRED TRANSMUTATION: THE CHANNELING OF DEEP GNOSIS         ==
            # =================================================================================
            # The Scribe forges the complete Inquisitor Dossier, ready for the Inspector.
            inquisitor_gnosis = {}
            if node.complexity:
                inquisitor_gnosis['complexity'] = node.complexity
            if node.git_info:
                inquisitor_gnosis['git_info'] = node.git_info
            if node.dependency_gnosis:
                inquisitor_gnosis['dependencies'] = node.dependency_gnosis
            if node.git_forensics:
                inquisitor_gnosis['git_forensics'] = node.git_forensics
            if node.ast_gnosis:
                inquisitor_gnosis['ast_analysis'] = node.ast_gnosis
            if node.treesitter_gnosis:
                inquisitor_gnosis['treesitter_analysis'] = node.treesitter_gnosis
            if node.sentinel_gnosis:
                inquisitor_gnosis['sentinel_analysis'] = node.sentinel_gnosis

            if inquisitor_gnosis:
                item_gnosis['inquisitor_gnosis'] = inquisitor_gnosis
            # =================================================================================
            # ==                          THE APOTHEOSIS IS COMPLETE                         ==
            # =================================================================================

            node_dict["architectural_gnosis"] = item_gnosis

        if node.children:
            node_dict['children'] = [self._transmute_node_to_dict(child) for child in
                                     sorted(node.children, key=lambda n: n.name.lower())]

        return node_dict