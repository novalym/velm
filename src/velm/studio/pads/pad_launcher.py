"""
=================================================================================
== THE SOVEREIGN CONDUCTOR OF PADS (V-Ω-ETERNAL-APOTHEOSIS++)                  ==
=================================================================================
LIF: ∞ (ETERNAL & DIVINE)

This is the divine, sentient, and eternal Nexus for all Gnostic Pads. It is a
hyper-intelligent God-Engine that does not just summon artisans, but first
adjudicates the very reality in which they must be born. It is a Gnostic
Guardian, a Wise Mentor, and an Unbreakable Conductor, all forged into a single,
luminous scripture. Its wisdom will serve our Great Work for all time.
=================================================================================
"""
import argparse
import traceback
from pathlib import Path
from typing import Dict, Any, Type, List

from textual.app import App

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("PadNexus")

# =================================================================================
# == I. THE SACRED GRIMOIRE OF PADS (THE SELF-AWARE SOUL)                        ==
# =================================================================================
# This is the Gnostic heart of the Nexus. To teach the Nexus a new Pad, one must
# simply inscribe its soul into this divine scripture.

# =================================================================================
# == I. THE SACRED GRIMOIRE OF PADS (THE SELF-AWARE SOUL)                        ==
# =================================================================================
PAD_GRIMOIRE: Dict[str, Dict[str, Any]] = {
    "beautify": {
        "description": "The Luminous Mirror. An interactive, real-time purifier for architectural scriptures.",
        "module_path": ".scaffold_pad", # Still points to our ascended BeautifyPad
        "class_name": "ScaffoldPad",
        "dependencies": ["textual", "pyperclip"],
    },
    # === THE DIVINE INSCRIPTION ===
    # The Gnosis of the new Pad is inscribed upon the Nexus's soul.
    "genesis": {
        "description": "The Altar of Genesis. A sentient gallery for forging new realities.",
        "module_path": ".genesis_pad",
        "class_name": "GenesisPad",
        "dependencies": ["textual"],
    },
    # === THE GRIMOIRE IS WHOLE ===
    "distill": {
        "description": "The Gnostic Workbench. An interactive sanctum for forging the perfect AI context.",
        "module_path": ".distill_pad.distill_pad_app",
        "class_name": "DistillPadApp",
        "dependencies": ["textual", "pyperclip", "requests"],
    },
    # --- THE GRIMOIRE IS NOW WHOLE ---
}

# =================================================================================
# == II. THE GOD-ENGINE OF GNOSTIC COMMUNION (THE NEXUS)                         ==
# =================================================================================

def handle_pad_launch(args: argparse.Namespace):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC COMMUNION (THE NEXUS'S ETERNAL FORM)              ==
    =================================================================================
    This is the divine artisan in its final, eternal form. It is now a true Gnostic
    Guardian and Mentor, forged with a pantheon of legendary faculties that make it
    unbreakable, intelligent, and infinitely extensible.

    ### The Pantheon of Gnostic Faculties:

    1.  **THE SENTINEL OF DEPENDENCIES:** Before it summons a soul, it performs a
        Gaze upon reality to ensure all of the Pad's divine allies (dependencies)
        are manifest. If they are not, it proclaims a luminous, helpful heresy,
        guiding the Architect to the path of righteousness (`pip install ...`).

    2.  **THE GNOSTIC INQUISITOR (The `--help` Gaze):** It is a wise Mentor. If it
        perceives the `--help` plea, it does not crudely summon the Pad. It forges and
        proclaims a beautiful, Gnostic Dossier describing all known Pads and their
        sacred purposes, transforming a simple query into an act of discovery.

    3.  **THE HYPER-DIAGNOSTIC WARD:** Its every rite is shielded. A catastrophic
        paradox during import or instantiation does not shatter the engine. It is
        perceived, chronicled, and proclaimed as a hyper-diagnostic Dossier, its
        full traceback made luminous for the Co-Architect's Gaze.

    4.  **THE JUST-IN-TIME ALCHEMIST (Dynamic Import):** Its Gaze upon the Grimoire
        is one of pure, dynamic alchemy. It forges the module path and summons the
        artisan's soul from the aether at the precise moment it is needed.
    =================================================================================
    """
    pad_to_summon = args.pad_name.lower()

    # --- FACULTY #2: THE GNOSTIC INQUISITOR (The `--help` Gaze) ---
    if pad_to_summon == 'help' or hasattr(args, 'help'):
        _proclaim_pad_dossier()
        return

    # --- THE GNOSTIC TRIAGE ---
    pad_gnosis = PAD_GRIMOIRE.get(pad_to_summon)
    if not pad_gnosis:
        raise ArtisanHeresy(
            f"The cosmos knows no Gnostic Pad named '{pad_to_summon}'.",
            suggestion=f"Speak `scaffold pad help` to see all known rites. Known rites are: {', '.join(PAD_GRIMOIRE.keys())}"
        )

    Logger.info(f"The Nexus prepares to summon the '{pad_to_summon}' Pad...")

    try:
        # --- FACULTY #1: THE SENTINEL OF DEPENDENCIES ---
        _adjudicate_dependencies(pad_gnosis.get("dependencies", []))

        # --- FACULTY #4: THE JUST-IN-TIME ALCHEMIST ---
        # The sacred rite of dynamic import.
        from importlib import import_module
        pad_module = import_module(pad_gnosis["module_path"], package=__package__)
        PadClass: Type[App] = getattr(pad_module, pad_gnosis["class_name"])

        # --- The Forging of the Gnostic Arguments ---
        # We perform a Gaze to see which Gnosis the Pad's soul requires.
        import inspect
        init_signature = inspect.signature(PadClass.__init__)
        pad_kwargs = {}

        if 'initial_file_path' in init_signature.parameters and hasattr(args, 'initial_path') and args.initial_path:
            initial_path = Path(args.initial_path).resolve()
            if initial_path.is_file():
                pad_kwargs['initial_file_path'] = initial_path
            else:
                Logger.warn(f"Initial path Gnosis '{args.initial_path}' is a void. The Pad will be born without it.")

        # --- The Divine Delegation ---
        Logger.verbose(f"Summoning the '{PadClass.__name__}' artisan with Gnosis: {pad_kwargs}")
        pad_instance = PadClass(**pad_kwargs)
        pad_instance.run()

    # --- FACULTY #3: THE HYPER-DIAGNOSTIC WARD ---
    except ImportError as e:
        raise ArtisanHeresy(
            "The Gnostic Pad requires its divine allies to be manifest.",
            suggestion=f"Speak the sacred plea: `pip install \"scaffold-cli[studio]\"` or `pip install {e.name}`",
            details=f"Missing artisan: {e.name}\n{traceback.format_exc()}"
        ) from e
    except Exception as e:
        raise ArtisanHeresy(
            f"A catastrophic paradox shattered the '{pad_to_summon}' Pad's reality during its genesis.",
            details=traceback.format_exc()
        ) from e


def _adjudicate_dependencies(dependencies: List[str]):
    """A pure Gnostic Sentinel that gazes upon reality for required allies."""
    import importlib.util
    missing_allies = []
    for dep in dependencies:
        if importlib.util.find_spec(dep) is None:
            missing_allies.append(dep)

    if missing_allies:
        raise ArtisanHeresy(
            "The chosen Pad requires divine allies that are not manifest in this reality.",
            suggestion=f"Speak the plea: `pip install {' '.join(f'\"{ally}\"' for ally in missing_allies)}`",
            details=f"Missing Allies: {', '.join(missing_allies)}"
        )
    Logger.verbose(f"Sentinel's Gaze is pure. All {len(dependencies)} required allies are manifest.")


def _proclaim_pad_dossier():
    """A luminous Scribe that proclaims the Gnosis of all known Pads."""
    from rich.table import Table
    from rich.panel import Panel
    from ...logger import get_console

    console = get_console()
    dossier_table = Table(
        title="[bold]The Grimoire of Gnostic Pads[/bold]",
        box=None,
        show_header=True,
        header_style="bold magenta"
    )
    dossier_table.add_column("Plea", style="cyan", no_wrap=True)
    dossier_table.add_column("Description", style="white")
    dossier_table.add_column("Dependencies", style="dim")

    for name, gnosis in PAD_GRIMOIRE.items():
        dossier_table.add_row(
            f"scaffold pad {name}",
            gnosis.get("description", "No Gnosis provided."),
            ", ".join(gnosis.get("dependencies", []))
        )

    console.print(Panel(
        dossier_table,
        title="[bold green]The Gnostic Nexus[/bold green]",
        subtitle="[dim]Your gateway to interactive architectural rites.[/dim]",
        border_style="green"
    ))