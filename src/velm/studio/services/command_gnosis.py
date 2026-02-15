"""
=================================================================================
== THE SCRIPTURE OF THE GNOSTIC ADJUDICATOR (THE ORACLE'S MIND)                ==
=================================================================================
This scripture contains the living soul of the GnosticAdjudicator, the central
artisan that performs a deep, Gnostic Introspection on the scaffold CLI's soul.
It understands the intent and requirements of every command, serving as the
mind for the CommandAltar Oracle.
=================================================================================
"""
from typing import List, Dict, Any

class GnosticAdjudicator:
    """
    Performs a deep, introspective Gaze upon the Velm God-Engine's own soul
    (the argparse CLI) to dynamically forge a Grimoire of Rites and their Gnostic
    requirements.
    """

    def __init__(self):
        """
        At the moment of its birth, the Adjudicator programmatically imports the
        one true source of Gnosis, `build_parser`, and forges a living, in-memory
        instance of the CLI's soul.
        """
        from ...core.cli.core_cli import build_parser
        self.parser = build_parser()

    def forge_grimoire(self) -> List[Dict[str, Any]]:
        """
        Performs the Gnostic Gaze and forges the complete Grimoire of all known
        rites, including the Gnosis of their required positional arguments.
        """
        import argparse
        grimoire: List[Dict[str, Any]] = []

        subparsers_action = next((action for action in self.parser._actions if isinstance(action, argparse._SubParsersAction)), None)

        # ★★★ THE RITE OF GNOSTIC UNIFICATION ★★★
        # The Oracle is taught to recognize the entire family of rites that
        # commune with a blueprint scripture's soul.
        BLUEPRINT_CONSUMING_RITES = {'distill', 'genesis', 'beautify', 'symphony'}
        # ★★★ THE GNOSIS IS NOW HOLISTIC ★★★

        if subparsers_action:
            for name, sub_parser in subparsers_action.choices.items():
                if name in ('__daemon-start', 'studio'):
                    continue

                rite_name = getattr(sub_parser, 'help', f"The Rite of {name.capitalize()}")
                description = getattr(sub_parser, 'description', None) or getattr(sub_parser, 'help', None) or "No Gnosis available for this rite."

                command_data = {
                    "command": name,
                    "rite_name": rite_name,
                    "description": description,
                    "argument_gnosis": None
                }

                positional_arg = next((action for action in sub_parser._actions if not action.option_strings), None)

                if positional_arg:
                    dest = positional_arg.dest
                    gnosis = {
                        "type": 'directory' if 'dir' in dest.lower() else 'file',
                        "extension": None,
                        "placeholder": f"<{dest}>"
                    }

                    # The Gaze is now upon the unified scripture of knowledge.
                    if name in BLUEPRINT_CONSUMING_RITES:
                        gnosis['extension'] = '.scaffold' if name != 'symphony' else '.symphony'

                    command_data["argument_gnosis"] = gnosis

                grimoire.append(command_data)

        return sorted(grimoire, key=lambda x: x['rite_name'])