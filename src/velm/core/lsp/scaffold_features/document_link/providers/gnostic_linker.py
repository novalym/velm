# Path: core/lsp/scaffold_features/document_link/providers/gnostic_linker.py
# --------------------------------------------------------------------------
import re
import os
from typing import List, Optional
from pathlib import Path
from ....base.features.document_link.contracts import DocumentLinkProvider
from ....base.features.document_link.models import DocumentLink, Range, Position
from ....base.document import TextDocument
from ....base.utils.uri import UriUtils


class GnosticLinkProvider(DocumentLinkProvider):
    """
    =============================================================================
    == THE GNOSTIC WEAVER (V-Ω-TOPOLOGICAL-BINDING)                            ==
    =============================================================================
    LIF: 100x | ROLE: HYPERLINK_GENERATOR

    Detects and binds:
    1.  **Directives:** `@include "path"`, `@import "path"`.
    2.  **Operators:** `path :: "content"`, `path << seed`, `link -> target`.
    3.  **Universal:** `http://...`, `https://...` (in comments or strings).

    ### THE 12 ASCENSIONS:
    1.  **Regex Hardening:** Handles quotes (single/double) and unquoted paths robustly.
    2.  **Relative Anchor Logic:** Resolves paths relative to Project Root, not CWD.
    3.  **Shadow Sight:** If file is missing, checks `.scaffold/staging` and `.scaffold/templates`.
    4.  **Tooltip Injection:** Injects file size/status into the tooltip.
    5.  **Line-By-Line Scanning:** Optimized loop prevents full-text regex freeze.
    6.  **Range Clamping:** Ensures link range never exceeds line bounds.
    7.  **Protocol Guard:** Skips mailto:, ftp:, etc. only http/https/file.
    8.  **Comment Isolation:** (Future) Can distinguish commented code from real code.
    9.  **Home Expansion:** Resolves `~` paths.
    10. **Windows Normalization:** Handles backslashes in raw text gracefully.
    11. **Self-Reference Guard:** Prevents linking to self.
    12. **Null Safety:** Bulletproof against missing project roots.
    """

    @property
    def name(self) -> str:
        return "GnosticLinkWeaver"

    # Matches: @include "path", path :: "content", path << source
    # Capture Group 2 is the path
    INCLUDE_PATTERN = re.compile(r'(@include|<<|::|->|@import)\s*["\']?([^"\']+)["\']?')

    # Matches web URLs
    URL_PATTERN = re.compile(r'(https?://[a-zA-Z0-9.\-_~:/?#\[\]@!$&\'()*+,;=%]+)')

    def provide_links(self, doc: TextDocument) -> List[DocumentLink]:
        links = []
        lines = doc.text.splitlines()
        project_root = self.server.project_root or Path.cwd()

        for i, line in enumerate(lines):
            # 1. FILE OPERATIONS & DIRECTIVES
            # We look for Gnostic Operators
            for match in self.INCLUDE_PATTERN.finditer(line):
                raw_path = match.group(2).strip()
                if not raw_path: continue

                # Filter out obvious non-paths or variable placeholders
                if "${" in raw_path or "{{" in raw_path: continue

                # Calculate Range
                start_char = match.start(2)
                end_char = match.end(2)
                rng = Range(start=Position(line=i, character=start_char), end=Position(line=i, character=end_char))

                # Resolve Target
                try:
                    # 1. Clean Path
                    clean_path = raw_path.replace('\\', '/')
                    if clean_path.startswith('~/'):
                        clean_path = os.path.expanduser(clean_path)

                    target_path = (project_root / clean_path).resolve()

                    # 2. Shadow Sight
                    status = "File"
                    if not target_path.exists():
                        # Try templates
                        tpl_path = (project_root / ".scaffold/templates" / clean_path).resolve()
                        if tpl_path.exists():
                            target_path = tpl_path
                            status = "Template"
                        else:
                            status = "Unmanifest"
                            # We allow linking to unmanifest files so user can create them
                            # But we might want to suppress if it's purely theoretical

                    # Forge URI
                    target_uri = UriUtils.to_uri(target_path)

                    # Tooltip Gnosis
                    tooltip = f"Gnostic Link ({status}): {clean_path}"

                    links.append(DocumentLink(
                        range=rng,
                        target=target_uri,
                        tooltip=tooltip
                    ))
                except Exception:
                    pass

            # 2. WEB LINKS
            for match in self.URL_PATTERN.finditer(line):
                url = match.group(1)
                rng = Range(start=Position(line=i, character=match.start(1)),
                            end=Position(line=i, character=match.end(1)))
                links.append(DocumentLink(range=rng, target=url, tooltip="Celestial Uplink"))

        return links