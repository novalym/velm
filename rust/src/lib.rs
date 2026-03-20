// Path: rust/src/lib.rs
// --------------------
// =================================================================================
// == THE SCAFFOLD BINARY KERNEL: OMEGA POINT (V-Ω-TOTALITY-VMAX-MODULAR-IRON)    ==
// =================================================================================
// LIF: ∞^∞ | ROLE: KINETIC_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
// AUTH_CODE: Ω_LIB_RS_VMAX_PARSER_CORE_SINGULARITY_2026_FINALIS

use pyo3::prelude::*;

// --- THE ARCHITECTURAL SUB-DOMAINS ---
pub mod utils;           
pub mod string_alchemy;  
pub mod vector_mind;     
pub mod fs_oracle;       
pub mod transaction;     
pub mod elara_core;      
pub mod polyglot_ast;    
pub mod emitter_core;    
pub mod heuristics_core;

// [ASCENSION]: The Monolithic parser_core.rs is dead. Welcome the Parser Core Pantheon.
pub mod parser_core; 

const KERNEL_VERSION: &str = "8.0.0-Ω-TOTALITY-VMAX-SINGULARITY";

#[pymodule]
fn scaffold_core_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    
    // STRATUM 0: KERNEL
    m.add_class::<transaction::GnosticVault>()?; 
    m.add_function(wrap_pyfunction!(elara_core::forge_elara_ast_fast, m)?)?;
    m.add_function(wrap_pyfunction!(elara_core::transmute_advanced, m)?)?;
    m.add_function(wrap_pyfunction!(elara_core::lex_blueprint_fast, m)?)?;
    m.add_function(wrap_pyfunction!(emitter_core::assemble_reality_fast, m)?)?;

    // [ASCENSION]: THE PARSER CORE PANTHEON (LIF-INFINITY)
    m.add_function(wrap_pyfunction!(parser_core::blocks::consume_bracketed_block_fast, m)?)?;
    m.add_function(wrap_pyfunction!(parser_core::blocks::consume_indented_block_fast, m)?)?;
    m.add_function(wrap_pyfunction!(parser_core::anti_matter::is_anti_matter_fast, m)?)?;
    m.add_function(wrap_pyfunction!(parser_core::geometry::calculate_visual_width_fast, m)?)?;
    m.add_function(wrap_pyfunction!(parser_core::shlex_core::shlex_split_fast, m)?)?;
    m.add_function(wrap_pyfunction!(parser_core::lexer_math::is_valid_identifier_fast, m)?)?;

    // STRATUM 1: FILESYSTEM
    m.add_class::<fs_oracle::FileRecord>()?;
    m.add_class::<fs_oracle::GrepMatch>()?;
    m.add_function(wrap_pyfunction!(fs_oracle::scan_directory_fast, m)?)?;
    m.add_function(wrap_pyfunction!(fs_oracle::hash_file, m)?)?;
    m.add_function(wrap_pyfunction!(fs_oracle::hash_directory, m)?)?;
    m.add_function(wrap_pyfunction!(fs_oracle::grep_fast, m)?)?;
    m.add_function(wrap_pyfunction!(fs_oracle::read_text_file, m)?)?;

    // STRATUM 2: TENSOR MIND
    m.add_class::<vector_mind::SemanticIndex>()?; 
    m.add_function(wrap_pyfunction!(vector_mind::cosine_similarity_dense, m)?)?;
    m.add_function(wrap_pyfunction!(vector_mind::calculate_centroid, m)?)?;
    m.add_function(wrap_pyfunction!(vector_mind::fuse_embeddings, m)?)?;
    m.add_function(wrap_pyfunction!(polyglot_ast::analyze_ast, m)?)?;
    m.add_function(wrap_pyfunction!(vector_mind::jaccard_similarity_fast, m)?)?;
    m.add_function(wrap_pyfunction!(vector_mind::cosine_similarity_sparse_fast, m)?)?;
    m.add_function(wrap_pyfunction!(vector_mind::forge_sparse_fast, m)?)?;
    // STRATUM 3: THE QUANTUM ADJUDICATOR
    m.add_class::<heuristics_core::adjudicator::QuantumAdjudicator>()?;

    // STRATUM 4: UTILITIES
    m.add_function(wrap_pyfunction!(string_alchemy::pipe_deconstruct, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::exorcise_ghost_lines, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::align_matter, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::purify_string_fast, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::purify_line_prefix_fast, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::fast_intent_scry, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::fast_genomic_extract, m)?)?;
    m.add_function(wrap_pyfunction!(string_alchemy::get_line_from_offset, m)?)?;

    m.add_function(wrap_pyfunction!(utils::fast_daemon_probe, m)?)?;
    m.add_function(wrap_pyfunction!(utils::fast_locus_anchor_scry, m)?)?;
    m.add_function(wrap_pyfunction!(utils::calculate_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(utils::current_time_iso8601, m)?)?;
    m.add_function(wrap_pyfunction!(utils::levenshtein_distance, m)?)?;
    m.add_function(wrap_pyfunction!(utils::fast_uuid4, m)?)?;
    m.add_function(wrap_pyfunction!(utils::is_valid_uuid, m)?)?;
    m.add_function(wrap_pyfunction!(utils::fast_b64_encode, m)?)?;
    m.add_function(wrap_pyfunction!(utils::fast_b64_decode, m)?)?;
    m.add_function(wrap_pyfunction!(utils::fast_url_encode, m)?)?;
    m.add_function(wrap_pyfunction!(utils::detect_magic_mime, m)?)?;

    m.add("KERNEL_VERSION", KERNEL_VERSION)?;

    Ok(())
}