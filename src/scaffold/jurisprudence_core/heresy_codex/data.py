# Path: jurisprudence_core/heresy_codex/data.py
# ---------------------------------------------

"""
=================================================================================
== THE ILLUSION OF PRECISION (DATA & TEMPORAL HERESIES)                        ==
=================================================================================
These laws govern the correctness of data representation. They prevent the
heresies of lost currency, drifting time, and type confusion.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

DATA_LAWS: Dict[str, GnosticLaw] = {

    "FLOATING_POINT_CURRENCY_HERESY": GnosticLaw(
        key="FLOATING_POINT_CURRENCY_HERESY",
        validator=NULL_VALIDATOR,
        title="The Illusion of Wealth",
        message="Floating point numbers used for currency calculations.",
        elucidation="Floats cannot represent decimal fractions precisely. In the realm of finance, a lost fraction of a cent is a grave heresy.",
        severity="CRITICAL",
        suggestion="Use the `Decimal` type or represent values as integers (cents)."
    ),

    "NAIVE_DATETIME_HERESY": GnosticLaw(
        key="NAIVE_DATETIME_HERESY",
        validator=NULL_VALIDATOR,
        title="The Illusion of Local Time",
        message="A 'naive' datetime object (no timezone) was created.",
        elucidation="Naive datetimes lead to the 'Temporal Schism' where different systems interpret the same moment differently. Absolute time requires a timezone.",
        severity="WARNING",
        suggestion="Use `timezone.utc` to make the datetime 'aware'."
    ),
}