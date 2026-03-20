// Path: rust/src/heuristics_core/axioms.rs
// ----------------------------------------

use std::collections::{HashMap, HashSet};
use lazy_static::lazy_static;

lazy_static! {
    /// Sovereign Hearts: Only ONE of these may exist in the 'Mind' tier to prevent Chimeras.
    pub static ref SOVEREIGN_HEARTS: HashSet<&'static str> = {
        let mut s = HashSet::new();
        s.insert("fastapi"); s.insert("express"); s.insert("django"); s.insert("flask");
        s.insert("nextjs"); s.insert("nuxt"); s.insert("astro"); s.insert("remix");
        s
    };

    /// Chimera Exclusion Rings: If Key exists, Values are mathematically forbidden.
    pub static ref CHIMERA_EXCLUSION_RINGS: HashMap<&'static str, HashSet<&'static str>> = {
        let mut m = HashMap::new();
        m.insert("fastapi", vec!["express", "django", "flask"].into_iter().collect());
        m.insert("nextjs", vec!["nuxt", "astro", "vue"].into_iter().collect());
        m.insert("postgres", vec!["mysql", "mariadb", "sqlite"].into_iter().collect());
        m
    };

    pub static ref TIER_GRAVITY: HashMap<String, f64> = vec![
        ("soul".to_string(), 35.0), 
        ("mind".to_string(), 20.0),
        ("body".to_string(), 10.0),
        ("iron".to_string(), 5.0),
        ("void".to_string(), 0.0)
    ].into_iter().collect();

    pub static ref UNIVERSAL_MATTER: HashSet<String> = vec![
        "docker", "kubernetes", "system", "bash", "shell", "terraform", "cloud", "iron", "agnostic"
    ].into_iter().map(|s| s.to_string()).collect();

    /// [THE MASTER CURE]: AXIOMATIC SOVEREIGN IMMUNITY
    /// Shards residing in these dimensions are the Immune System of the project.
    /// They bypass prompt-relevance pruning entirely and are evaluated on the Z-Axis.
    pub static ref AXIOMATIC_PREFIXES: Vec<&'static str> = vec![
        "tests/", "test-utils/", "scripts/security/", "security/audit/", "ci/", ".github/", ".scaffold/"
    ];
}

#[inline(always)]
pub fn normalize_gnosis(text: &str) -> String {
    let mut lower = text.to_lowercase();
    let prefixes = ["capability:", "logic:", "urn:", "shard:", "vow:", "trait:", "contract:"];
    for p in prefixes {
        if lower.starts_with(p) { lower = lower[p.len()..].to_string(); break; }
    }
    if let Some(idx) = lower.rfind('/') { lower = lower[idx + 1..].to_string(); }
    lower.chars().filter(|c| c.is_alphanumeric() || *c == '-').collect()
}