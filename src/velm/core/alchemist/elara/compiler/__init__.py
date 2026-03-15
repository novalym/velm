# Path: elara/compiler/__init__.py
# --------------------------------

"""
=================================================================================
== THE ELARA COMPILER STRATUM (STRATUM-0: THE KERNEL)                          ==
=================================================================================
@gnosis:title The Elara Compiler
@gnosis:summary The supreme authority for transmuting Gnostic ASTs into
                 executable Python bytecode or binary artifacts.
@gnosis:LIF INFINITY

This sanctum houses the artisans of Transmutation. It provides the faculties
required to take a high-level ELARA blueprint and optimize, compile, and
serialize it for 0ms execution.
=================================================================================
"""
from .bytecode import ElaraBytecodeCompiler
from .optimizer import ElaraOptimizer
from .transpiler import ElaraTranspiler
from .jit import ElaraJITEngine

__all__ = [
    "ElaraBytecodeCompiler",
    "ElaraOptimizer",
    "ElaraTranspiler",
    "ElaraJITEngine"
]

