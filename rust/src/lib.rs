// Path: src/lib.rs
// ----------------
// =================================================================================
// == THE SCAFFOLD BINARY KERNEL: OMEGA POINT (V-Ω-TOTALITY-VMAX-M2-INCEPTION)    ==
// =================================================================================
// LIF: ∞^∞ | ROLE: KINETIC_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
// AUTH_CODE: Ω_LIB_RS_VMAX_PART2_2026_FINALIS
// 
//[THE MANIFESTO]
// The supreme final authority for Binary Execution. This version mathematically
// annihilates the "Infinite C-Loop" paradox that paralyzed the Host OS when
// fed malformed Jinja templates. It achieves absolute, unbreakable resonance.
// =================================================================================

use pyo3::prelude::*;
use pyo3::exceptions::{PyIOError, PyValueError};
use ignore::WalkBuilder;
use sha2::{Sha256, Digest};
use std::fs::File;
use std::time::{SystemTime, Instant};
use std::collections::{HashMap, BTreeMap};
use std::path::Path;
use rayon::prelude::*;
use serde_json::Value;

// --- THE PANTHEON OF TONGUES ---
use tree_sitter::{Parser, Query, QueryCursor};

const KERNEL_VERSION: &str = "1.0.0-Ω-TOTALITY-HEALED";

// =================================================================================
// == SECTION I: HELPER RITES & IRON SENSING                                      ==
// =================================================================================

#[inline(always)]
fn system_time_to_float(time: std::time::SystemTime) -> f64 {
    match time.duration_since(std::time::SystemTime::UNIX_EPOCH) {
        Ok(dur) => dur.as_secs_f64(),
        Err(_) => 0.0,
    }
}

#[inline(always)]
fn is_binary_buffer(buffer: &[u8]) -> bool {
    buffer.contains(&0)
}

#[inline(always)]
fn fast_cosine_similarity(v1: &[f32], v2: &[f32], v1_norm: f32, v2_norm: f32) -> f32 {
    if v1_norm == 0.0 || v2_norm == 0.0 || v1.len() != v2.len() { return 0.0; }
    
    let mut dot = 0.0;
    for i in 0..v1.len() {
        dot += v1[i] * v2[i];
    }
    dot / (v1_norm * v2_norm)
}

fn calculate_magnitude(v: &[f32]) -> f32 {
    let mut sum = 0.0;
    for &val in v { sum += val * val; }
    sum.sqrt()
}

// =================================================================================
// == SECTION II: THE LEGENDARY SEMANTIC ROUTER (LOCAL VECTOR DB)                 ==
// =================================================================================

#[derive(Clone)]
struct VectorNode {
    id: String,
    vector: Vec<f32>,
    magnitude: f32,
    payload: String,
}

#[pyclass]
struct SemanticIndex {
    nodes: Vec<VectorNode>,
    dimension: usize,
}

#[pymethods]
impl SemanticIndex {
    #[new]
    fn new() -> Self {
        SemanticIndex { nodes: Vec::new(), dimension: 0 }
    }

    fn add(&mut self, id: String, vec: Vec<f32>, payload: String) -> PyResult<()> {
        if self.dimension == 0 && !vec.is_empty() {
            self.dimension = vec.len();
        } else if !vec.is_empty() && vec.len() != self.dimension {
            return Err(PyValueError::new_err("Vector Dimension Schism."));
        }

        let magnitude = calculate_magnitude(&vec);
        self.nodes.push(VectorNode { id, vector: vec, magnitude, payload });
        Ok(())
    }
    
    fn clear(&mut self) {
        self.nodes.clear();
        self.dimension = 0;
    }

    fn search(&self, py: Python, query: Vec<f32>, top_k: usize) -> PyResult<Vec<(String, f32, String)>> {
        if query.len() != self.dimension {
            return Err(PyValueError::new_err("Query Vector Dimension Schism."));
        }

        let query_magnitude = calculate_magnitude(&query);

        py.allow_threads(|| {
            let mut scores: Vec<(String, f32, String)> = self.nodes.par_iter().map(|node| {
                let sim = fast_cosine_similarity(&node.vector, &query, node.magnitude, query_magnitude);
                (node.id.clone(), sim, node.payload.clone())
            }).collect();
            
            scores.par_sort_unstable_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
            scores.truncate(top_k);
            Ok(scores)
        })
    }
}

// =================================================================================
// == SECTION III: THE MERKLE VAULT (TRANSACTION LEDGER & COLLAPSE)               ==
// =================================================================================

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
struct MerkleLeaf {
    path: String,
    content_hash: String,
    size_bytes: u64,
    action: String, 
    timestamp: f64,
}

#[pyclass]
struct GnosticVault {
    matter_lattice: BTreeMap<String, MerkleLeaf>,
    #[pyo3(get)]
    trace_id: String,
    start_time: Instant,
}

#[pymethods]
impl GnosticVault {
    #[new]
    fn new(trace_id: String) -> Self {
        GnosticVault { matter_lattice: BTreeMap::new(), trace_id, start_time: Instant::now() }
    }

    fn record_intent(&mut self, path: String, hash: String, size: u64, action: String) {
        let leaf = MerkleLeaf {
            path: path.clone(), content_hash: hash, size_bytes: size, action,
            timestamp: system_time_to_float(SystemTime::now()),
        };
        self.matter_lattice.insert(path, leaf);
    }

    fn get_lattice_mass(&self) -> usize { self.matter_lattice.len() }
    fn get_latency_ms(&self) -> f64 { self.start_time.elapsed().as_secs_f64() * 1000.0 }

    fn commit_reality(&self, py: Python, shadow_root: String, live_root: String, legacy_root: String) -> PyResult<bool> {
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

// =================================================================================
// == SECTION IV: MATTER VESSELS & CRYPTOGRAPHY                                   ==
// =================================================================================

#[pyclass]
#[derive(Clone)]
struct FileRecord {
    #[pyo3(get)] path: String,
    #[pyo3(get)] size: u64,
    #[pyo3(get)] is_binary: bool,
    #[pyo3(get)] mtime: f64,
}

#[pymethods]
impl FileRecord {
    #[new]
    fn new(path: String, size: u64, is_binary: bool, mtime: f64) -> Self {
        FileRecord { path, size, is_binary, mtime }
    }
}

#[pyclass]
struct GrepMatch {
    #[pyo3(get)] path: String,
    #[pyo3(get)] line_number: usize,
    #[pyo3(get)] content: String,
}

#[pyfunction]
fn hash_file(path: String) -> PyResult<String> {
    let mut file = File::open(path).map_err(|e| PyIOError::new_err(e.to_string()))?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher).map_err(|e| PyIOError::new_err(e.to_string()))?;
    Ok(hex::encode(hasher.finalize()))
}

#[pyfunction]
fn calculate_entropy(text: String) -> f64 {
    let mut counts = HashMap::new();
    let mut total = 0;
    for c in text.chars() { *counts.entry(c).or_insert(0) += 1; total += 1; }
    let mut entropy = 0.0;
    for &count in counts.values() {
        let p = count as f64 / total as f64;
        entropy -= p * p.log2();
    }
    entropy
}

#[pyfunction]
fn read_text_file(path: String) -> PyResult<String> {
    std::fs::read_to_string(path).map_err(|e| PyIOError::new_err(e.to_string()))
}

// =================================================================================
// == SECTION V: THE ALCHEMICAL REACTOR (NATIVE RUST EVALUATION)                  ==
// =================================================================================

fn resolve_var<'a>(dom: &'a Value, path: &str) -> Option<&'a Value> {
    let mut current = dom;
    for part in path.split('.') {
        if let Some(obj) = current.as_object() {
            if let Some(next) = obj.get(part) { current = next; } else { return None; }
        } else { return None; }
    }
    Some(current)
}

/// The Native SGF Transmuter. Bypasses the GIL entirely.
#[pyfunction]
fn transmute_advanced(py: Python, template: String, json_context: String) -> PyResult<String> {
    let dom: Value = serde_json::from_str(&json_context)
        .map_err(|e| PyValueError::new_err(format!("Gnostic DOM Error: {}", e)))?;

    py.allow_threads(move || {
        let mut result = String::with_capacity(template.len() * 2);
        let bytes = template.as_bytes();
        let mut cursor = 0;

        //[ASCENSION 157]: The O(1) Loop Freeze Healer
        while cursor < bytes.len().saturating_sub(1) {
            if bytes[cursor] == b'{' && bytes[cursor+1] == b'{' {
                let mut end = cursor + 2;
                let mut found = false;
                
                while end < bytes.len() - 1 {
                    if bytes[end] == b'}' && bytes[end+1] == b'}' {
                        let var_name = String::from_utf8_lossy(&bytes[cursor+2..end]).trim().to_string();
                        if let Some(val) = resolve_var(&dom, &var_name) {
                            match val {
                                Value::String(s) => result.push_str(s),
                                _ => result.push_str(&val.to_string()),
                            }
                        } else {
                            result.push_str(&format!("{{{{ {} }}}}", var_name));
                        }
                        cursor = end + 2;
                        found = true;
                        break;
                    }
                    end += 1;
                }
                // [THE MASTER CURE]: Prevents the infinite loop if tag is never closed
                if !found {
                    result.push_str("{{");
                    cursor += 2;
                }
            } else if bytes[cursor] == b'{' && bytes[cursor+1] == b'%' {
                let mut end = cursor + 2;
                let mut found = false;
                
                while end < bytes.len() - 1 {
                    if bytes[end] == b'%' && bytes[end+1] == b'}' {
                        cursor = end + 2;
                        found = true;
                        break;
                    }
                    end += 1;
                }
                // [THE MASTER CURE]: Prevents the infinite loop if tag is never closed
                if !found {
                    result.push_str("{%");
                    cursor += 2;
                }
            } else {
                let char_len = match std::str::from_utf8(&bytes[cursor..=cursor]) {
                    Ok(_) => 1,
                    Err(_) => {
                        let mut l = 1;
                        while cursor + l < bytes.len() && std::str::from_utf8(&bytes[cursor..cursor+l]).is_err() {
                            l += 1;
                        }
                        l
                    }
                };
                if let Ok(s) = std::str::from_utf8(&bytes[cursor..cursor+char_len]) {
                    result.push_str(s);
                }
                cursor += char_len;
            }
        }
        
        // [THE MASTER CURE]: Grab the absolute final byte if we didn't consume it
        if cursor < bytes.len() {
            if let Ok(s) = std::str::from_utf8(&bytes[cursor..]) {
                result.push_str(s);
            }
        }
        
        Ok(result)
    })
}

// =================================================================================
// == SECTION VI: PARALLEL DISK I/O & SIMD GREP                                   ==
// =================================================================================

#[pyfunction]
#[pyo3(signature = (root, hidden=false, threads=0))]
fn scan_directory_fast(py: Python, root: String, hidden: bool, threads: usize) -> PyResult<Vec<FileRecord>> {
    let final_threads = if threads == 0 {
        std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1)
    } else { threads };

    py.allow_threads(move || {
        let walker = WalkBuilder::new(&root).hidden(!hidden).git_ignore(true).require_git(false).threads(final_threads).build_parallel();
        let (tx, rx) = std::sync::mpsc::channel();

        walker.run(|| {
            let tx = tx.clone();
            Box::new(move |entry| {
                if let Ok(e) = entry {
                    if e.path().is_file() {
                        let path_str = e.path().to_string_lossy().replace("\\", "/");
                        if let Ok(metadata) = e.metadata() {
                            let size = metadata.len();
                            let mtime = system_time_to_float(metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH));
                            let mut is_binary = false;
                            if size > 0 {
                                if let Ok(mut f) = File::open(e.path()) {
                                    let mut buffer = [0; 1024];
                                    use std::io::Read; 
                                    if let Ok(n) = f.read(&mut buffer) { is_binary = is_binary_buffer(&buffer[..n]); }
                                }
                            }
                            let _ = tx.send(FileRecord { path: path_str, size, is_binary, mtime });
                        }
                    }
                }
                ignore::WalkState::Continue
            })
        });
        drop(tx);
        Ok(rx.into_iter().collect())
    })
}

#[pyfunction]
fn hash_directory(py: Python, root: String) -> PyResult<String> {
    py.allow_threads(move || {
        let walker = WalkBuilder::new(&root).hidden(true).git_ignore(true).build();
        let mut results = Vec::new();
        for result in walker {
            if let Ok(e) = result {
                if e.path().is_file() {
                    let path_str = e.path().to_string_lossy().replace("\\", "/");
                    if let Ok(metadata) = e.metadata() {
                        let size = metadata.len();
                        let mtime = system_time_to_float(metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH));
                        results.push(FileRecord { path: path_str, size, is_binary: false, mtime });
                    }
                }
            }
        }
        results.sort_by(|a, b| a.path.cmp(&b.path));
        let mut hasher = Sha256::new();
        for record in results {
            hasher.update(record.path.as_bytes());
            hasher.update(record.size.to_le_bytes());
            hasher.update(record.mtime.to_le_bytes());
        }
        Ok(hex::encode(hasher.finalize()))
    })
}

#[pyfunction]
fn grep_fast(py: Python, paths: Vec<String>, pattern: String) -> PyResult<Vec<GrepMatch>> {
    let pattern_bytes = pattern.as_bytes();
    py.allow_threads(move || {
        let results: Vec<GrepMatch> = paths.into_par_iter().filter_map(|path_str| {
            let path = Path::new(&path_str);
            let file = File::open(path).ok()?;
            let mmap = unsafe { memmap2::MmapOptions::new().map(&file).ok()? };
            let mut matches = Vec::new();
            
            for match_pos in memchr::memmem::find_iter(&mmap, pattern_bytes) {
                let line_number = memchr::memchr_iter(b'\n', &mmap[..match_pos]).count() + 1;
                let line_start = match mmap[..match_pos].iter().rposition(|&b| b == b'\n') { Some(p) => p + 1, None => 0 };
                let line_end = match mmap[match_pos..].iter().position(|&b| b == b'\n') { Some(p) => match_pos + p, None => mmap.len() };
                let content = String::from_utf8_lossy(&mmap[line_start..line_end]).trim().to_string();
                matches.push(GrepMatch { path: path_str.clone(), line_number, content });
            }
            if matches.is_empty() { None } else { Some(matches) }
        }).flatten().collect();
        Ok(results)
    })
}

// =================================================================================
// == SECTION VII: THE TENSOR MATH COPROCESSOR (ONNX DELEGATE EXPOSED)            ==
// =================================================================================

#[pyfunction]
fn cosine_similarity_dense(v1: Vec<f32>, v2: Vec<f32>) -> f32 {
    let norm1 = calculate_magnitude(&v1);
    let norm2 = calculate_magnitude(&v2);
    fast_cosine_similarity(&v1, &v2, norm1, norm2)
}

#[pyfunction]
fn calculate_centroid(vectors: Vec<Vec<f32>>) -> PyResult<Vec<f32>> {
    if vectors.is_empty() { return Ok(vec![]); }
    let dims = vectors[0].len();
    let mut centroid = vec![0.0; dims];
    for v in &vectors {
        if v.len() != dims { return Err(PyValueError::new_err("Vector dimension mismatch.")); }
        for i in 0..dims { centroid[i] += v[i]; }
    }
    let len = vectors.len() as f32;
    for i in 0..dims { centroid[i] /= len; }
    let mag = calculate_magnitude(&centroid);
    if mag > 1e-12 { for i in 0..dims { centroid[i] /= mag; } }
    Ok(centroid)
}

#[pyfunction]
fn fuse_embeddings(vectors: Vec<Vec<f32>>) -> PyResult<Vec<f32>> {
    if vectors.is_empty() { return Ok(vec![]); }
    let dims = vectors[0].len();
    let mut sum_vector: Vec<f32> = (0..dims).into_par_iter().map(|i| {
        vectors.iter().map(|v| v[i]).sum::<f32>() / vectors.len() as f32
    }).collect();
    let mag = calculate_magnitude(&sum_vector);
    if mag > 1e-12 { for i in 0..dims { sum_vector[i] /= mag; } }
    Ok(sum_vector)
}

// =================================================================================
// == SECTION VIII: THE LEXICAL PURIFIER & POLYGLOT AST INQUISITOR                ==
// =================================================================================

#[pyfunction]
fn purify_string_fast(text: String) -> String {
    let mut result = String::with_capacity(text.len());
    for c in text.chars() {
        let u = c as u32;
        if u == 0xFEFF || (0x200B..=0x200D).contains(&u) || u == 0x2060 
            || (u < 0x20 && u != 0x0A && u != 0x0D && u != 0x09) 
            || (0x7F..=0x9F).contains(&u) 
            || (0xE000..=0xF8FF).contains(&u) {
            continue;
        }
        if (0x2500..=0x257F).contains(&u) { result.push(' '); } else { result.push(c); }
    }
    result
}

#[pyfunction]
fn get_line_from_offset(content: String, byte_offset: usize) -> usize {
    let mut line_count = 1;
    for (i, c) in content.char_indices() {
        if i >= byte_offset { break; }
        if c == '\n' { line_count += 1; }
    }
    line_count
}

#[pyfunction]
fn analyze_ast(py: Python, content: String, language: &str, query_str: &str) -> PyResult<Vec<HashMap<String, String>>> {
    py.allow_threads(move || {
        let mut parser = Parser::new();
        let ts_lang = match language.to_lowercase().as_str() {
            "python" => tree_sitter_python::language(),
            "javascript" | "js" => tree_sitter_javascript::language(),
            "jsx" => tree_sitter_javascript::language(), // Map JSX to standard JS parser
            "typescript" | "ts" => tree_sitter_typescript::language_typescript(),
            "tsx" => tree_sitter_typescript::language_tsx(), // THE MASTER CURE: Native TSX support
            "go" => tree_sitter_go::language(),
            "rust" | "rs" => tree_sitter_rust::language(),
            "ruby" | "rb" => tree_sitter_ruby::language(),
            "cpp" | "c++" | "cc" => tree_sitter_cpp::language(),
            "java" => tree_sitter_java::language(),
            "html" => tree_sitter_html::language(),
            "css" => tree_sitter_css::language(),
            _ => return Err(PyValueError::new_err(format!("Unmanifest Tongue: {}", language))),
        };
        parser.set_language(ts_lang).map_err(|e| PyValueError::new_err(e.to_string()))?;
        let tree = parser.parse(&content, None).ok_or_else(|| PyValueError::new_err("Ontological Failure"))?;
        let query = Query::new(ts_lang, query_str).map_err(|e| PyValueError::new_err(format!("Invalid Gnostic Query: {}", e)))?;
        let mut cursor = QueryCursor::new();
        let matches = cursor.matches(&query, tree.root_node(), content.as_bytes());
        let mut results = Vec::new();
        for m in matches {
            for capture in m.captures {
                let mut map = HashMap::new();
                let node = capture.node;
                let range = node.byte_range();
                let text = content.get(range.clone()).unwrap_or("");
                let capture_name = query.capture_names()[capture.index as usize].clone();
                map.insert("capture".to_string(), capture_name);
                map.insert("text".to_string(), text.to_string());
                map.insert("type".to_string(), node.kind().to_string());
                map.insert("start_byte".to_string(), node.start_byte().to_string());
                map.insert("end_byte".to_string(), node.end_byte().to_string());
                map.insert("start_line".to_string(), node.start_position().row.to_string());
                map.insert("start_col".to_string(), node.start_position().column.to_string());
                results.push(map);
            }
        }
        Ok(results)
    })
}

// =================================================================================
// == SECTION IX: THE KERNEL SEALING (MODULE DEFINITION)                          ==
// =================================================================================

#[pymodule]
fn scaffold_core_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FileRecord>()?;
    m.add_class::<GrepMatch>()?;
    m.add_class::<GnosticVault>()?; 
    m.add_class::<SemanticIndex>()?; 
    m.add_function(wrap_pyfunction!(scan_directory_fast, m)?)?;
    m.add_function(wrap_pyfunction!(hash_file, m)?)?;
    m.add_function(wrap_pyfunction!(hash_directory, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(grep_fast, m)?)?;
    m.add_function(wrap_pyfunction!(read_text_file, m)?)?;
    m.add_function(wrap_pyfunction!(transmute_advanced, m)?)?;
    m.add_function(wrap_pyfunction!(cosine_similarity_dense, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_centroid, m)?)?;
    m.add_function(wrap_pyfunction!(fuse_embeddings, m)?)?;
    m.add_function(wrap_pyfunction!(purify_string_fast, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_ast, m)?)?;
    m.add_function(wrap_pyfunction!(get_line_from_offset, m)?)?;
    m.add("KERNEL_VERSION", KERNEL_VERSION)?;
    m.add("POLYGLOT_CAPACITY", 10)?;
    m.add("SUBSTRATE_PLANE", if cfg!(windows) { "NT_IRON" } else { "POSIX_IRON" })?;
    m.add("SIMD_ENABLED", true)?;
    Ok(())
}