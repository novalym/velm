// Path: rust/src/transaction.rs
// -----------------------------
use pyo3::prelude::*;
use pyo3::exceptions::PyIOError;
use std::collections::BTreeMap;
use std::path::Path;
use std::time::{Instant, SystemTime};
use crate::utils::system_time_to_float;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct MerkleLeaf {
    pub path: String,
    pub content_hash: String,
    pub size_bytes: u64,
    pub action: String, 
    pub timestamp: f64,
}

#[pyclass]
pub struct GnosticVault {
    matter_lattice: BTreeMap<String, MerkleLeaf>,
    #[pyo3(get)] pub trace_id: String,
    start_time: Instant,
}

#[pymethods]
impl GnosticVault {
    #[new]
    pub fn new(trace_id: String) -> Self { 
        GnosticVault { matter_lattice: BTreeMap::new(), trace_id, start_time: Instant::now() } 
    }

    pub fn record_intent(&mut self, path: String, hash: String, size: u64, action: String) {
        let leaf = MerkleLeaf { 
            path: path.clone(), 
            content_hash: hash, 
            size_bytes: size, 
            action, 
            timestamp: system_time_to_float(SystemTime::now()) 
        };
        self.matter_lattice.insert(path, leaf);
    }

    pub fn get_lattice_mass(&self) -> usize { self.matter_lattice.len() }
    
    pub fn get_latency_ms(&self) -> f64 { self.start_time.elapsed().as_secs_f64() * 1000.0 }

    pub fn commit_reality(&self, py: Python, shadow_root: String, live_root: String, legacy_root: String) -> PyResult<bool> {
        py.allow_threads(move || {
            let s_path = Path::new(&shadow_root); 
            let l_path = Path::new(&live_root); 
            let old_path = Path::new(&legacy_root);
            
            if l_path.exists() { let _ = std::fs::rename(l_path, old_path); }
            if s_path.exists() { 
                std::fs::rename(s_path, l_path).map_err(|e| PyIOError::new_err(format!("Collapse Fracture: {}", e)))?; 
            }
            Ok(true)
        })
    }
}