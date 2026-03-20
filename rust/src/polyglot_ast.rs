// Path: rust/src/polyglot_ast.rs
// ------------------------------
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use std::collections::HashMap;
use tree_sitter::{Parser, Query, QueryCursor};

#[pyfunction]
pub fn analyze_ast(py: Python, content: String, language: &str, query_str: &str) -> PyResult<Vec<HashMap<String, String>>> {
    py.allow_threads(move || {
        let mut parser = Parser::new();
        let ts_lang = match language.to_lowercase().as_str() {
            "python" => tree_sitter_python::language(),
            "javascript" | "js" => tree_sitter_javascript::language(),
            "jsx" => tree_sitter_javascript::language(), 
            "typescript" | "ts" => tree_sitter_typescript::language_typescript(),
            "tsx" => tree_sitter_typescript::language_tsx(), 
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