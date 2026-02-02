// ---------------------
// Path: rust/src/lib.rs
// ---------------------
use pyo3::prelude::*;
use pyo3::exceptions::{PyIOError, PyValueError};
use ignore::WalkBuilder;
use sha2::{Sha256, Digest};
use std::fs::{self, File};
use std::io::Read;
use memmap2::MmapOptions;
use std::time::SystemTime;
use std::thread;
use std::collections::HashMap;
    
// The Divine Summons of the Syntax Trees
// Ensure your Cargo.toml has tree-sitter dependencies!
use tree_sitter::{Parser, Query, QueryCursor};
    
// =================================================================================
// == THE GNOSTIC VESSELS (STRUCTS)                                               ==
// =================================================================================
    
#[pyclass]
struct FileRecord {
    #[pyo3(get)]
    path: String,
    #[pyo3(get)]
    size: u64,
    #[pyo3(get)]
    is_binary: bool,
    #[pyo3(get)]
    mtime: f64,
}
    
#[pymethods]
impl FileRecord {
    #[new]
    fn new(path: String, size: u64, is_binary: bool, mtime: f64) -> Self {
        FileRecord { path, size, is_binary, mtime }
    }
        
    fn __repr__(&self) -> String {
        format!("<FileRecord path='{}' size={} binary={}>", self.path, self.size, self.is_binary)
    }
}
    
// =================================================================================
// == THE IRON ARTISANS (FUNCTIONS)                                               ==
// =================================================================================
    
fn is_binary_buffer(buffer: &[u8]) -> bool {
    // A heuristic: if we find a null byte in the first 8KB, it's likely binary.
    buffer.iter().take(8192).any(|&b| b == 0)
}
    
fn system_time_to_float(t: SystemTime) -> f64 {
    match t.duration_since(SystemTime::UNIX_EPOCH) {
        Ok(d) => d.as_secs_f64(),
        Err(_) => 0.0,
    }
}
    
#[pyfunction]
fn hash_file(path: String) -> PyResult<String> {
    let file = File::open(&path).map_err(|e| PyIOError::new_err(e.to_string()))?;
    let metadata = file.metadata().map_err(|e| PyIOError::new_err(e.to_string()))?;
    let len = metadata.len();
    let mut hasher = Sha256::new();
    
    if len > 0 {
        // Safety: Mmap is safe for reading unless the file is truncated externally.
        let mmap = unsafe { MmapOptions::new().map(&file).map_err(|e| PyIOError::new_err(e.to_string()))? };
        hasher.update(&mmap);
    }
    
    let result = hasher.finalize();
    Ok(hex::encode(result))
}
    
#[pyfunction]
fn calculate_entropy(data: &[u8]) -> f64 {
    if data.is_empty() { return 0.0; }
    let mut counts = [0usize; 256];
    for &byte in data { counts[byte as usize] += 1; }
    let len = data.len() as f64;
    let mut entropy = 0.0;
    for &count in counts.iter() {
        if count > 0 {
            let p = count as f64 / len;
            entropy -= p * p.log2();
        }
    }
    entropy
}
    
/// [THE FIX] Renamed to scan_directory to match Python expectation
#[pyfunction]
#[pyo3(signature = (root, hidden=false))]
fn scan_directory(py: Python, root: String, hidden: bool) -> PyResult<Vec<FileRecord>> {
    // We release the GIL to allow Python to breathe while we work.
    py.allow_threads(move || {
        let mut results = Vec::new();
        // Auto-detect thread count for maximum parallelism
        let threads = thread::available_parallelism().map(|n| n.get()).unwrap_or(1);
    
        let walker = WalkBuilder::new(&root)
            .hidden(!hidden) 
            .git_ignore(true) 
            .threads(threads) 
            .build();
    
        for result in walker {
            match result {
                Ok(entry) => {
                    if !entry.path().is_file() { continue; }
                    let path = entry.path();
                    let path_str = path.to_string_lossy().replace("\\", "/");
    
                    if let Ok(metadata) = entry.metadata() {
                        let size = metadata.len();
                        let mtime = system_time_to_float(metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH));
                            
                        // The Binary Gaze: Check the first few bytes
                        let mut is_binary = false;
                        if size > 0 {
                                if let Ok(mut f) = File::open(path) {
                                    let mut buffer = [0; 1024];
                                    if let Ok(n) = f.read(&mut buffer) {
                                        is_binary = is_binary_buffer(&buffer[..n]);
                                    }
                                }
                        }
                        results.push(FileRecord { path: path_str, size, is_binary, mtime });
                    }
                }
                Err(_) => continue,
            }
        }
        Ok(results)
    })
}
    
#[pyfunction]
fn read_text_file(path: String) -> PyResult<String> {
    let content = fs::read(&path).map_err(|e| PyIOError::new_err(e.to_string()))?;
    match String::from_utf8(content.clone()) {
        Ok(s) => Ok(s),
        Err(_) => {
            // Fallback decode for legacy windows files
            let (res, _, _) = encoding_rs::WINDOWS_1252.decode(&content);
            Ok(res.into_owned())
        }
    }
}
    
/// [THE PROPHESIED INQUISITOR]
#[pyfunction]
fn analyze_ast(py: Python, content: String, language: &str, query_str: &str) -> PyResult<Vec<HashMap<String, String>>> {
    py.allow_threads(move || {
        let mut parser = Parser::new();
            
        // Map string to Tree-sitter language function
        let lang = match language {
            "python" => tree_sitter_python::language(),
            "javascript" => tree_sitter_javascript::language(),
            "typescript" | "tsx" => tree_sitter_typescript::language_tsx(),
            "go" => tree_sitter_go::language(),
            "rust" => tree_sitter_rust::language(),
            _ => return Err(PyValueError::new_err(format!("Unknown tongue: {}", language))),
        };
            
        parser.set_language(lang).map_err(|e| PyValueError::new_err(e.to_string()))?;
            
        let tree = parser.parse(&content, None).ok_or_else(|| PyValueError::new_err("Failed to parse content"))?;
        let query = Query::new(lang, query_str).map_err(|e| PyValueError::new_err(format!("Invalid query: {}", e)))?;
        let mut cursor = QueryCursor::new();
        let matches = cursor.matches(&query, tree.root_node(), content.as_bytes());
            
        let mut results = Vec::new();
        for m in matches {
            for capture in m.captures {
                let mut map = HashMap::new();
                let node = capture.node;
                let range = node.byte_range();
                let text = &content[range];
                let capture_name = query.capture_names()[capture.index as usize].clone();
                    
                map.insert("capture".to_string(), capture_name);
                map.insert("text".to_string(), text.to_string());
                map.insert("type".to_string(), node.kind().to_string());
                map.insert("start_byte".to_string(), node.start_byte().to_string());
                map.insert("end_byte".to_string(), node.end_byte().to_string());
                results.push(map);
            }
        }
        Ok(results)
    })
}
    
#[pymodule]
fn scaffold_core_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FileRecord>()?;
    m.add_function(wrap_pyfunction!(scan_directory, m)?)?;
    m.add_function(wrap_pyfunction!(hash_file, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(read_text_file, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_ast, m)?)?;
    Ok(())
}