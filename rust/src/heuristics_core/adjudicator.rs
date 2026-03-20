// Path: rust/src/heuristics_core/adjudicator.rs
// ---------------------------------------------

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use rayon::prelude::*;
use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use crate::heuristics_core::models::{OracleShard, SemVer};
use crate::heuristics_core::axioms::{
    AXIOMATIC_PREFIXES, SOVEREIGN_HEARTS, CHIMERA_EXCLUSION_RINGS, 
    TIER_GRAVITY, UNIVERSAL_MATTER, normalize_gnosis
};
use crate::heuristics_core::affinity::AFFINITY_MATRIX;
use crate::heuristics_core::tensor_fusion::{jaccard_similarity, fast_cosine_similarity, calculate_sparse_cohesion};

#[pyclass]
pub struct QuantumAdjudicator {
    shards: HashMap<String, OracleShard>,
    capability_map: HashMap<String, Vec<String>>,
}

#[pymethods]
impl QuantumAdjudicator {
    #[new]
    pub fn new() -> Self {
        QuantumAdjudicator { shards: HashMap::new(), capability_map: HashMap::new() }
    }

    ///[THE RITE OF INGESTION]: Hydrates the C-Memory DAG and calculates Topological Gravity.
    pub fn ingest_grimoire(&mut self, shard_data: &Bound<'_, PyList>) -> PyResult<()> {
        self.shards.clear();
        self.capability_map.clear();

        for item in shard_data.iter() {
            let dict = match item.downcast::<PyDict>() { Ok(d) => d, Err(_) => continue };
            
            let id: String = match dict.get_item("id") { Ok(Some(v)) => v.extract()?, _ => continue };
            let tier: String = match dict.get_item("tier") { Ok(Some(v)) => v.extract().unwrap_or_else(|_| "mind".into()), _ => "mind".into() };
            let provides_list: Vec<String> = match dict.get_item("provides") { Ok(Some(v)) => v.extract()?, _ => vec![] };
            let substrate_list: Vec<String> = match dict.get_item("substrate") { Ok(Some(v)) => v.extract()?, _ => vec![] };
            let requires_list: Vec<String> = match dict.get_item("requires") { Ok(Some(v)) => v.extract()?, _ => vec![] };
            let version_str: String = match dict.get_item("version") { Ok(Some(v)) => v.extract()?, _ => "1.0.0".into() };
            let resonance_score: f64 = match dict.get_item("resonance_score") { Ok(Some(v)) => v.extract()?, _ => 0.0 };
            
            let semantic_vector: Option<Arc<Vec<f32>>> = match dict.get_item("semantic_vector") {
                Ok(Some(v)) => v.extract::<Vec<f32>>().ok().map(Arc::new),
                _ => None,
            };

            let norm_id = normalize_gnosis(&id);
            // [ASCENSION]: Axiomatic Bedrock detection - Prevents tests from evaporating!
            let is_axiomatic = AXIOMATIC_PREFIXES.iter().any(|p| id.starts_with(p));
            let is_heart = SOVEREIGN_HEARTS.contains(norm_id.as_str());

            let shard = OracleShard {
                id: id.clone(),
                norm_id: norm_id.clone(),
                tier: tier.clone(),
                tier_val: *TIER_GRAVITY.get(&tier.to_lowercase()).unwrap_or(&10.0),
                provides: provides_list.iter().map(|p| normalize_gnosis(p)).collect(),
                substrate: substrate_list.iter().map(|s| normalize_gnosis(s)).collect(),
                requires: requires_list.iter().map(|r| normalize_gnosis(r)).collect(),
                version: SemVer::parse(&version_str),
                semantic_vector,
                resonance_score,
                matter_density: provides_list.len() + 1,
                potential_unlocks: 0,
                causal_gravity: 0.0, // Calculated post-ingestion
                is_axiomatic,
                is_heart,
            };

            self.shards.insert(id.clone(), shard);
            let mut all_caps = provides_list;
            all_caps.push(id.clone());
            for cap in all_caps {
                let norm_cap = normalize_gnosis(&cap);
                self.capability_map.entry(norm_cap).or_default().push(id.clone());
            }
        }

        // =========================================================================
        // == [ASCENSION]: TOPOLOGICAL PAGERANK (CAUSAL GRAVITY)                  ==
        // =========================================================================
        // We mathematically measure how "important" a shard is by how many other
        // shards rely on its existence. A shard that unlocks 10 others gains massive
        // gravitational pull in the election matrix.
        let mut potentials = Vec::new();
        for (sid, s) in &self.shards {
            let mut unlock_count = 0;
            let mut gravity = 0.0;

            for other in self.shards.values() {
                if other.id != *sid && other.requires.iter().any(|r| s.provides.contains(r)) {
                    unlock_count += 1;
                    // A shard gains gravity based on the tier of the shard it unlocks
                    gravity += other.tier_val * 0.5; 
                }
            }
            potentials.push((sid.clone(), unlock_count, gravity));
        }

        for (sid, count, gravity) in potentials {
            if let Some(s) = self.shards.get_mut(&sid) { 
                s.potential_unlocks = count; 
                s.causal_gravity = gravity;
            }
        }

        Ok(())
    }

    /// [THE OMEGA ELECTION RITE]
    /// Fuses Dense Embeddings, Sparse TF-IDF, Topological PageRank, and Axiomatic Immunity.
    #[pyo3(signature = (requirement, active_substrates, banned_capabilities, project_centroid=None, willed_shards=Vec::new(), query_dense=None, query_sparse_tokens=Vec::new()))]
    pub fn elect_best_provider(
        &self,
        requirement: &str,
        active_substrates: Vec<String>,
        banned_capabilities: Vec<String>,
        project_centroid: Option<Vec<f32>>,
        willed_shards: Vec<String>,
        query_dense: Option<Vec<f32>>,
        query_sparse_tokens: Vec<String>,
    ) -> Option<String> {
        let norm_req = normalize_gnosis(requirement);
        let candidates = match self.capability_map.get(&norm_req) {
            Some(c) => c,
            None => return None,
        };

        let norm_bans: HashSet<String> = banned_capabilities.iter().map(|s| normalize_gnosis(s)).collect();
        let norm_active_subs: HashSet<String> = active_substrates.iter().map(|s| normalize_gnosis(s)).collect();
        let active_ids: HashSet<String> = willed_shards.iter().map(|s| normalize_gnosis(s)).collect();
        let sparse_query_set: HashSet<String> = query_sparse_tokens.iter().map(|s| normalize_gnosis(s)).collect();

        // 1. ADJUDICATE LANGUAGE BIAS & ACTIVE HEARTS
        let mut lang_dist: HashMap<String, usize> = HashMap::new();
        let mut active_heart = None;

        for sid in &willed_shards {
            if let Some(s) = self.shards.get(sid) {
                for sub in &s.substrate { if sub != "agnostic" { *lang_dist.entry(sub.clone()).or_default() += 1; } }
                if s.is_heart && s.tier == "mind" { active_heart = Some(s.norm_id.clone()); }
            }
        }
        let dominant_lang = lang_dist.iter().max_by_key(|e| e.1).map(|(k, _)| k.clone());

        // 2. PARALLEL DIMENSIONAL ADJUDICATION (RAYON SIMD)
        let winner = candidates.par_iter().filter_map(|cid| {
            let shard = &self.shards[cid];

            // =========================================================================
            // == [ASCENSION]: THE CHIMERA EXCLUSION RINGS                            ==
            // =========================================================================
            // If the active project possesses a Heart (e.g. FastAPI), we mathematically 
            // forbid the election of any shard that belongs to an antagonistic ring 
            // (e.g. Express, Django).
            if let Some(ref heart) = active_heart {
                if let Some(antagonists) = CHIMERA_EXCLUSION_RINGS.get(heart.as_str()) {
                    if antagonists.contains(shard.norm_id.as_str()) { return None; }
                }
            }

            // =========================================================================
            // == [THE MASTER CURE]: AXIOMATIC BEDROCK PRESERVATION                   ==
            // =========================================================================
            // Tests and CI are granted Absolute Amnesty from the Standard Bans.
            // They are evaluated purely on their Substrate Resonance (Do they fit the language?)
            if !shard.is_axiomatic {
                // Standard Pauli Exclusion
                if shard.is_heart && active_heart.is_some() && shard.tier == "mind" { return None; }
                if norm_bans.contains(&shard.norm_id) || !shard.provides.is_disjoint(&norm_bans) { return None; }
            }

            // --- THE CALCULUS OF MAGNITUDE ---
            
            // A. SUBSTRATE DNA RESONANCE
            let mut sub_score = 0.0;
            if shard.substrate.contains("agnostic") || norm_active_subs.is_empty() || !shard.substrate.is_disjoint(&norm_active_subs) {
                sub_score = 6000.0; // Hard substrate match is mandatory for life
            } else if !shard.substrate.is_disjoint(&*UNIVERSAL_MATTER) {
                sub_score = 3000.0;
            } else if shard.is_axiomatic {
                // If it's a Test shard but matches NO active substrates, it must be vaporized.
                // You cannot weave PyTest into a pure NextJS project.
                return None; 
            }
            
            if let Some(ref dom) = dominant_lang {
                if !shard.substrate.contains(dom) && !shard.substrate.contains("agnostic") { sub_score -= 3000.0; }
            }

            // B. SYNAPTIC SYNERGY (The Love Matrix)
            let mut synergy_boost = 1.0;
            for aid in &active_ids {
                if let Some(links) = AFFINITY_MATRIX.get(aid.as_str()) {
                    for (friend, weight) in links {
                        // If the project has FastAPI, and this shard is PyTest, Weight is Massive.
                        if *friend == shard.norm_id.as_str() { synergy_boost += weight; }
                    }
                }
            }

            // C. BICAMERAL NEURAL FUSION (ONNX + JACCARD)
            let mut neural_score = 0.0;
            if let (Some(q_vec), Some(s_vec)) = (&query_dense, &shard.semantic_vector) {
                neural_score += fast_cosine_similarity(q_vec, s_vec) as f64 * 80.0;
            }
            if let (Some(cent), Some(s_vec)) = (&project_centroid, &shard.semantic_vector) {
                // Cohesion with the existing graph
                neural_score += fast_cosine_similarity(cent, s_vec) as f64 * 30.0;
            }
            
            let sparse_score = calculate_sparse_cohesion(&sparse_query_set, &shard.provides) * 40.0;

            // D. TOPOLOGICAL PAGERANK
            let prophecy_boost = shard.causal_gravity * 15.0;

            // E. AXIOMATIC Z-AXIS GRAVITY
            // We force testing and CI to the top of the stack if they passed the Substrate check.
            let axiom_offset = if shard.is_axiomatic { 100_000.0 } else { 0.0 };
            
            // --- FINAL FUSION ---
            let magnitude = 
                (sub_score * synergy_boost) +
                axiom_offset + 
                (shard.tier_val * 250.0) +
                (shard.resonance_score * 100.0) +
                neural_score +
                sparse_score +
                prophecy_boost +
                (shard.matter_density as f64 * 15.0) +
                (250.0 - shard.requires.len() as f64); // Penalize extreme neediness

            Some((magnitude, &shard.version, cid))
        }).max_by(|a, b| {
            let res = a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal);
            if res != std::cmp::Ordering::Equal { return res; }
            // Break ties with Semantic Versioning (newer is better)
            a.1.cmp(&b.1)
        });

        winner.map(|(_, _, cid)| cid.clone())
    }
}