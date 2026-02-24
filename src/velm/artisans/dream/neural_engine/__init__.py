# Path: artisans/dream/neural_engine/__init__.py
# ----------------------------------------------

"""
=================================================================================
== THE NEURAL ENGINE SANCTUM (V-Ω-PROPHETIC-CORE)                              ==
=================================================================================
@gnosis:title The Neural Engine
@gnosis:summary The Generative Heart of the Dream Artisan.
@gnosis:LIF INFINITY

This sanctum houses the **Neural Prophet**, a specialized AI conductor trained in
the Gnostic Grammar of `.scaffold` blueprints. It is not a generic chat bot.
It is an **Architectural Compiler** that transmutes natural language intent into
executable, deterministic infrastructure code.

### THE TRINITY OF THE ENGINE:
1.  **The Constitution (`constitution.py`):** The immutable System Prompt that
    teaches the AI the laws of Scaffold (Variables, File Syntax, Logic Gates).
    It is the "DNA" of the generated blueprints.

2.  **The Validator (`validator.py`):** The Inquisitor that audits every
    generated blueprint for structural heresies (Markdown leaks, missing sigils)
    *before* it is allowed to touch the Engine.

3.  **The Prophet (`prophet.py`):** The High Priest that orchestrates the
    communion with the Celestial Providers, handles the cost accounting, and
    executes the Self-Healing Loop if validation fails.

**Usage:**
    from .prophet import NeuralProphet
    prophet = NeuralProphet(engine)
    blueprint, cost = prophet.forge_blueprint("Create a react app", root)
=================================================================================
"""

from .prophet import NeuralProphet
from .validator import NeuralInquisitor
from .constitution import forge_system_prompt

__all__ = ["NeuralProphet", "NeuralInquisitor", "forge_system_prompt"]