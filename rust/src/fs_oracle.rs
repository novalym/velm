// Path: rust/src/fs_oracle.rs
// ---------------------------
use pyo3::prelude::*;
use pyo3::exceptions::PyIOError;
use std::fs::File;
use std::path::Path;
use sha2::{Sha256, Digest};
use rayon::prelude::*;
use ignore::WalkBuilder;
use std::time::SystemTime;

use crate::utils::{is_binary_buffer, system_time_to_float};

#[pyclass]
#[derive(Clone)]
pub struct FileRecord {
    #[pyo3(get)] pub path: String,
    #[pyo3(get)] pub size: u64,
    #[pyo3(get)] pub is_binary: bool,
    #[pyo3(get)] pub mtime: f64,
}

#[pymethods]
impl FileRecord { 
    #[new] 
    pub fn new(path: String, size: u64, is_binary: bool, mtime: f64) -> Self { 
        FileRecord { path, size, is_binary, mtime } 
    } 
}

#[pyclass]
pub struct GrepMatch {
    #[pyo3(get)] pub path: String,
    #[pyo3(get)] pub line_number: usize,
    #[pyo3(get)] pub content: String,
}

#[pyfunction]
#[pyo3(signature = (root, hidden=false, threads=0))]
pub fn scan_directory_fast(py: Python, root: String, hidden: bool, threads: usize) -> PyResult<Vec<FileRecord>> {
    let final_threads = if threads == 0 { std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1) } else { threads };

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
                                    let mut buffer =[0; 1024];
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
pub fn hash_file(path: String) -> PyResult<String> {
    let mut file = File::open(path).map_err(|e| PyIOError::new_err(e.to_string()))?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher).map_err(|e| PyIOError::new_err(e.to_string()))?;
    Ok(hex::encode(hasher.finalize()))
}

#[pyfunction]
pub fn hash_directory(py: Python, root: String) -> PyResult<String> {
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
pub fn grep_fast(py: Python, paths: Vec<String>, pattern: String) -> PyResult<Vec<GrepMatch>> {
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

#[pyfunction]
pub fn read_text_file(path: String) -> PyResult<String> { 
    std::fs::read_to_string(path).map_err(|e| PyIOError::new_err(e.to_string())) 
}