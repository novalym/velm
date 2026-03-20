// Path: rust/src/heuristics_core/affinity.rs
// ------------------------------------------

use std::collections::HashMap;
use lazy_static::lazy_static;

lazy_static! {
    /// [ASCENSION]: MULTI-DIMENSIONAL SYNAPTIC AFFINITY MATRIX
    /// Tech that "loves" each other. If Node A is willed, Node B gains massive gravity.
    /// Expanded to forcefully bind test frameworks to their respective substrates with
    /// overwhelming mathematical force (e.g. pytest is inextricably linked to fastapi).
    pub static ref AFFINITY_MATRIX: HashMap<&'static str, Vec<(&'static str, f64)>> = {
        let mut m = HashMap::new();
        // Python/FastAPI Ecosystem
        m.insert("fastapi", vec![
            ("pydantic", 3.0), ("sqlalchemy", 2.5), ("alembic", 2.0), 
            ("uvicorn", 2.0), ("pytest", 8.0), ("coverage", 5.0) // Bedrock Affinity
        ]);
        m.insert("python", vec![("pytest", 6.0), ("ruff", 4.0)]);
        
        // Node/React Ecosystem
        m.insert("nextjs", vec![
            ("tailwind", 2.5), ("clerk", 3.0), ("typescript", 2.0), 
            ("lucide", 1.5), ("zod", 2.5), ("jest", 7.0), ("cypress", 4.0)
        ]);
        m.insert("react", vec![("vite", 2.5), ("tailwind", 2.0), ("vitest", 6.0)]);
        
        // Data & Infra
        m.insert("postgres", vec![("prisma", 2.5), ("docker", 2.0), ("pgvector", 3.0), ("sql", 1.5)]);
        m.insert("auth", vec![("identity", 2.5), ("jwt", 2.0), ("citadel", 3.5)]);
        
        // Rust Ecosystem
        m.insert("rust", vec![("tokio", 2.5), ("serde", 2.5), ("cargo-test", 8.0)]);
        m
    };
}