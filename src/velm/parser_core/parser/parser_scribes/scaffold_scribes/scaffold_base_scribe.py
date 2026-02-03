# scaffold/parser_core/parser_scribes/scaffold_scribes/scaffold_base_scribe.py

from ..base_scribe import FormScribe


class ScaffoldBaseScribe(FormScribe):
    """
    The Ancestral Scribe for the Language of Form (.scaffold).
    All Scaffold artisans inherit from this lineage.

    This intermediate layer ensures that if the data contract for
    Scaffold parsing changes specifically, we can adapt here without
    affecting the Symphony scribes.
    """
    pass

