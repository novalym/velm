// Path: rust/src/heuristics_core/tensor_fusion.rs
// -----------------------------------------------

use std::collections::HashSet;

/// Calculates Jaccard Similarity for Pauli Exclusion.
#[inline(always)]
pub fn jaccard_similarity(set1: &HashSet<String>, set2: &HashSet<String>) -> f64 {
    let intersection = set1.intersection(set2).count() as f64;
    let union = set1.union(set2).count() as f64;
    if union == 0.0 { 0.0 } else { intersection / union }
}

///[ASCENSION]: SIMD-Aligned Cosine Similarity for Dense ONNX Vectors.
/// LLVM will autonomicly unroll this loop to use AVX2/AVX-512 registers.
#[inline(always)]
pub fn fast_cosine_similarity(v1: &[f32], v2: &[f32]) -> f64 {
    if v1.is_empty() || v1.len() != v2.len() { return 0.0; }
    
    let mut dot = 0.0_f32;
    let mut norm1 = 0.0_f32;
    let mut norm2 = 0.0_f32;

    for i in 0..v1.len() {
        dot += v1[i] * v2[i];
        norm1 += v1[i] * v1[i];
        norm2 += v2[i] * v2[i];
    }
    
    if norm1 == 0.0 || norm2 == 0.0 { return 0.0; }
    (dot / (norm1.sqrt() * norm2.sqrt())) as f64
}

/// [ASCENSION]: Sparse Keyword Tensor Interaction with Non-Linear Cohesion
#[inline(always)]
pub fn calculate_sparse_cohesion(query_tokens: &HashSet<String>, shard_tokens: &HashSet<String>) -> f64 {
    let intersection = query_tokens.intersection(shard_tokens).count() as f64;
    // Logarithmic dampening prevents keyword stuffing, but rewards hyper-specificity
    (intersection + 1.0).ln() * 1.5
}