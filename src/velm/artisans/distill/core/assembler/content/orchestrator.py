# Path: artisans/distill/core/assembler/content/orchestrator.py
# -------------------------------------------------------------

"""
=================================================================================
== THE WEAVING ORCHESTRATOR (V-Ω-SURGICAL-AWARE)                               ==
=================================================================================
The true mind of the ContentWeaver. It executes a pure, functional pipeline,
commanding the specialist artisans to transmute a raw soul into a luminous
blueprint entry. It is now the final hand that wields the CausalSlicer.
"""
from .contracts import WeavingContext
from .artisans import (
    SoulReader,
    Sanitizer,
    Summarizer,
    Transformer,
    Annotator,
    Formatter
)
from ......core.cortex.contracts import FileGnosis
from ......logger import Scribe

Logger = Scribe("WeavingOrchestrator")


class WeavingOrchestrator:
    """Orchestrates the pipeline of content transformation artisans."""

    def __init__(self):
        # The Pantheon is forged at birth.
        self.reader = SoulReader()
        self.sanitizer = Sanitizer()
        self.summarizer = Summarizer()
        self.transformer = Transformer()
        self.annotator = Annotator()
        self.formatter = Formatter()

    def weave(self, ctx: WeavingContext) -> str:
        """The Grand Symphony of Weaving, conducted as a pure pipeline."""
        gnosis = ctx.gnosis
        path_str = str(gnosis.path).replace('\\', '/')

        # --- Movement I: The Gaze of Omission ---
        if gnosis.representation_method == 'path_only':
            return self.formatter.format_omitted_path(gnosis)

        # --- Movement II: The Reading of the Soul ---
        content = self.reader.read(ctx.project_root / gnosis.path)
        if content is None:
            return f"{path_str} # [Error: Scripture unreadable or binary]"

        if len(content) > 2000 and len(content.splitlines()) < 5:
            return f"{path_str} # [Omitted: Minified/Obfuscated Soul detected]"

        final_content = ""
        rep_method = gnosis.representation_method

        # --- Movement III: The Gnostic Triage of Representation ---
        if gnosis.category == 'lock' or rep_method == 'summary':
            final_content = self.summarizer.summarize_lockfile(gnosis.name, content)
        elif rep_method == 'stub':
            final_content = ctx.skeletonizer.stub(content, gnosis.path)
        elif rep_method == 'summary':
            final_content = self.summarizer.summarize_code(gnosis.name, content)
        elif rep_method == 'skeleton':
            final_content = ctx.skeletonizer.consecrate(content, gnosis.path, ctx.active_symbols)
        elif rep_method == 'full':
            # This is the full pipeline for 'full' representation.
            pipeline_content = content
            pipeline_content = self.sanitizer.clean(pipeline_content, ctx.profile)
            pipeline_content = self.transformer.truncate_large_file(pipeline_content, gnosis)

            # [THE FIX] THE SURGICAL HAND
            # The Orchestrator, not the Weaver, wields the scalpel.
            if ctx.slicer:
                Logger.verbose(f"Surgical Gaze is upon '{gnosis.path.name}'...")
                sliced = ctx.slicer.slice(gnosis.path, pipeline_content)
                if sliced != pipeline_content:
                    Logger.success(f"   -> Surgically sliced '{gnosis.path.name}'.")
                    pipeline_content = sliced
                else:
                     Logger.verbose(f"   -> No surgical changes needed for '{gnosis.path.name}'.")

            pipeline_content = self.annotator.inject_all(pipeline_content, ctx)

            if ctx.profile.strategy == 'aggressive':
                pipeline_content = self.transformer.distill_docstrings(pipeline_content)

            final_content = self.transformer.compress_whitespace(pipeline_content)

        # --- Movement IV: The Final Adjudication & Formatting ---
        if not final_content.strip():
            return f"{path_str} # [Empty or Redacted]"

        return self.formatter.format_blueprint_block(path_str, final_content, gnosis)