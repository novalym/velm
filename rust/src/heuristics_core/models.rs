// Path: rust/src/heuristics_core/models.rs
// ----------------------------------------

use std::collections::HashSet;
use std::sync::Arc;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct SemVer(pub u32, pub u32, pub u32);

impl SemVer {
    pub fn parse(v: &str) -> Self {
        let clean = v.trim_start_matches(|c: char| !c.is_numeric());
        let mut parts = clean.split('.');
        let v1 = parts.next().unwrap_or("1").parse().unwrap_or(1);
        let v2 = parts.next().unwrap_or("0").parse().unwrap_or(0);
        let v3 = parts.next().unwrap_or("0").split(|c: char| !c.is_numeric()).next().unwrap_or("0").parse().unwrap_or(0);
        SemVer(v1, v2, v3)
    }
}

#[derive(Clone, Debug)]
pub struct OracleShard {
    pub id: String,
    pub norm_id: String,
    pub tier: String,
    pub tier_val: f64,
    pub provides: HashSet<String>,
    pub substrate: HashSet<String>,
    pub requires: Vec<String>,
    pub version: SemVer,
    pub semantic_vector: Option<Arc<Vec<f32>>>,
    
    // Kinetic & Topological Metadata
    pub resonance_score: f64,
    pub matter_density: usize,
    pub potential_unlocks: usize,       // Out-Degree in the DAG
    pub causal_gravity: f64,            // [ASCENSION]: Topological PageRank Score
    pub is_axiomatic: bool,             // The Bedrock Ward (Tests/CI/Security)
    pub is_heart: bool,                 // Sovereign Frameworks (FastAPI/NextJS)
}