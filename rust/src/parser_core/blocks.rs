// Path: rust/src/parser_core/blocks.rs
// ------------------------------------
// =================================================================================
// == THE TOPOLOGICAL BLOCK CONSUMER: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASC)      ==
// =================================================================================
// LIF: ∞^∞^∞ | ROLE: MATTER_BOUNDARY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME
// AUTH_CODE: Ω_BLOCKS_VMAX_OWNED_MEMORY_SUTURE_2026_FINALIS

use pyo3::prelude::*;
use crate::parser_core::geometry::measure_visual_depth;
use crate::string_alchemy::purify_line_prefix_fast;

/// [THE MASTER CURE: INDENTATION CONSUMER]
/// Eliminates the Python loop for measuring line depths and aggregating structural blocks.
/// Now utilizes owned `Vec<String>` to satisfy FFI trait bounds and resolve E0277.
#[pyfunction]
pub fn consume_indented_block_fast(
    lines: Vec<String>, 
    start_idx: usize, 
    parent_indent: usize, 
    tab_width: usize
) -> PyResult<(Vec<String>, usize)> {
    
    // [ASCENSION 2]: Pre-allocation for metabolic haste
    let mut content_lines = Vec::with_capacity(512);
    let mut i = start_idx;
    let line_count = lines.len();
    
    // --- MOVEMENT I: THE SEARCH FOR THE BASELINE ---
    let mut block_baseline: i32 = -1;
    for peek_i in i..line_count {
        let line = &lines[peek_i];
        let stripped = line.trim();
        if !stripped.is_empty() && !stripped.starts_with('#') && !stripped.starts_with("//") {
            block_baseline = measure_visual_depth(line, tab_width) as i32;
            break;
        }
    }
    
    if block_baseline == -1 || block_baseline <= parent_indent as i32 {
        return Ok((Vec::new(), start_idx));
    }
    
    // --- MOVEMENT II: THE GREEDY CONSUMPTION ---
    while i < line_count {
        let line = &lines[i];
        let is_blank = line.trim().is_empty();
        
        if is_blank {
            content_lines.push(line.clone());
            i += 1;
            continue;
        }
        
        let current_indent = measure_visual_depth(line, tab_width);
        
        // [ASCENSION 14]: THE STRUCTURAL WALL SENTINEL
        if current_indent <= parent_indent {
            let stripped = line.trim_start();
            if stripped.starts_with('#') || stripped.starts_with("//") {
                // [ASCENSION 7]: Comment Amnesty
            } else {
                break; 
            }
        }
        
        content_lines.push(purify_line_prefix_fast(line.clone()));
        i += 1;
    }
    
    // --- MOVEMENT III: THE RITE OF THE TRAIL TRIMMER ---
    while let Some(last) = content_lines.last() {
        if last.trim().is_empty() {
            content_lines.pop();
        } else {
            break;
        }
    }
    
    Ok((content_lines, std::cmp::max(i, start_idx)))
}

/// [THE MASTER CURE: BRACKET CONSUMER]
/// Character-by-character bracket tracking executed entirely in Rust C-memory.
#[pyfunction]
pub fn consume_bracketed_block_fast(
    lines: Vec<String>, 
    start_idx: usize
) -> PyResult<(Vec<String>, usize)> {
    
    let mut bracket_depth = 0;
    let mut current_idx = start_idx;
    let mut block_lines = Vec::with_capacity(512);
    
    let mut in_string = false;
    let mut string_char = '\0';
    
    if current_idx >= lines.len() {
        return Ok((Vec::new(), start_idx));
    }

    let first_line = lines[current_idx].trim();
    let stripped = if first_line.starts_with('}') {
        first_line[1..].trim()
    } else {
        first_line
    };
    
    if stripped.contains('{') {
        bracket_depth += 1;
    } else if current_idx + 1 < lines.len() && lines[current_idx + 1].trim() == "{" {
        bracket_depth += 1;
        current_idx += 1; 
    } else {
        return Ok((Vec::new(), start_idx)); 
    }
    
    current_idx += 1; 
    
    while current_idx < lines.len() {
        let line = &lines[current_idx];
        let line_normalized = line.replace("\r\n", "\n");
        let chars: Vec<char> = line_normalized.chars().collect();
        
        let mut j = 0;
        let mut in_comment = false;
        
        while j < chars.len() {
            let c = chars[j];
            
            if !in_string && !in_comment {
                if c == '"' || c == '\'' || c == '`' {
                    in_string = true;
                    string_char = c;
                } else if c == '#' || (c == '/' && j + 1 < chars.len() && chars[j+1] == '/') {
                    in_comment = true;
                } else if c == '{' && j + 1 < chars.len() && (chars[j+1] == '{' || chars[j+1] == '%') {
                    j += 1; // [ASCENSION 16]: SGF Immunity Ward
                } else if c == '}' {
                    bracket_depth -= 1;
                } else if c == '{' {
                    bracket_depth += 1;
                }
            } else if in_string {
                if c == '\\' {
                    j += 1; 
                } else if c == string_char {
                    in_string = false;
                }
            }
            
            if bracket_depth == 0 {
                break;
            }
            j += 1;
        }
        
        if bracket_depth == 0 {
            break;
        }
        
        block_lines.push(line.to_string());
        current_idx += 1;
    }
    
    Ok((block_lines, current_idx + 1))
}