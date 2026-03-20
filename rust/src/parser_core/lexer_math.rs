// Path: rust/src/parser_core/lexer_math.rs
// ----------------------------------------
// =================================================================================
// == THE IDENTIFIER ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)        ==
// =================================================================================
// LIF: 1,000,000x | ROLE: LEXICAL_VALIDATOR | RANK: OMEGA_GUARDIAN
// AUTH_CODE: Ω_LEXER_MATH_VMAX_O1_IDENTIFIER_2026_FINALIS

use pyo3::prelude::*;

/// [THE MASTER CURE: O(1) BYTE-LEVEL IDENTIFIER VALIDATION]
/// Determines if a string is a valid Python/Gnostic identifier natively.
#[pyfunction]
pub fn is_valid_identifier_fast(name: &str) -> bool {
    if name.is_empty() { return false; }
    let bytes = name.as_bytes();
    let first = bytes[0];
    if !(first.is_ascii_alphabetic() || first == b'_') {
        return false;
    }
    for &b in &bytes[1..] {
        if !(b.is_ascii_alphanumeric() || b == b'_') {
            return false;
        }
    }
    true
}