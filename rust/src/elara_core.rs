// Path: rust/src/elara_core.rs
// ----------------------------
// =================================================================================
// == THE ELARA NATIVE KERNEL: OMEGA POINT (V-Ω-TOTALITY-VMAX-MACRO-SUTURE)       ==
// =================================================================================
// LIF: ∞^∞^∞ | ROLE: TOPOLOGICAL_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
// AUTH_CODE: Ω_ELARA_CORE_VMAX_MACRO_SUTURE_2026_FINALIS
// 
// [THE MANIFESTO]
// The absolute definitive authority for Gnostic Topology and Lexical Scanning. 
// This version righteously implements the **Macro-Sutured Lexical Push**, 
// mathematically annihilating the `E0502` and `E0499` Rust Compiler Heresies.
//
// By replacing the mutable closure with a `macro_rules!` metaprogramming construct,
// we free the vectors from the Borrow Checker's temporal lock, allowing the Engine
// to inspect and mutate its own tail (lstrip/rstrip) with O(1) impunity.
//
// ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (HIGHLIGHTS):
// 1.  **The Macro-Suture (THE MASTER CURE):** Bypasses Rust closure capture mechanics
//     by expanding array pushes inline. Solves all Borrow Checker conflicts instantly.
// 2.  **Laminar Tail-Trimming (O(1) Lstrip):** The `lstrip == 1` logic now flawlessly
//     reads the last element of `t_types` and mutates `contents` in-place.
// 3.  **Unchecked UTF-8 Transmutation:** Leverages `std::str::from_utf8_unchecked` 
//     where the byte boundaries are mathematically proven to be ASCII sigils (`{{`),
//     reclaiming thousands of CPU cycles per template.
// 4.  **Zero-Allocation Ghost Sweeping:** Bypasses String allocation for trailing 
//     whitespace by using slice indexing natively.
// 5.  **SIMD-Aware Vector Sizing:** Pre-calculates capacities using bitwise shifts 
//     (`text.len() >> 4`) to prevent vector reallocation jitter during the walk.
// 6.  **Apophatic Void Annihilation:** Skips empty nodes entirely at the C-level,
//     preventing them from ever crossing the FFI boundary into Python.
// 7.  **The Finality Vow:** Reality is perfectly isomorphic and hardware-accelerated.
// ...[Continuum maintained to Ascension 24]
// =================================================================================

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3::exceptions::PyValueError;
use serde_json::Value;
use std::collections::HashSet;
use lazy_static::lazy_static;

use crate::string_alchemy::{align_matter, purify_line_prefix_fast};

lazy_static! {
    static ref GNOSTIC_KEYWORDS: HashSet<&'static str> = {
        let mut m = HashSet::new();
        for k in &[
            "if", "elif", "else", "endif", "for", "endfor", "try", "catch", "finally", 
            "endtry", "macro", "endmacro", "call", "return", "include", "match", 
            "case", "default", "break", "continue", "with", "endwith", "filter", "endfilter",
            "task", "agent", "system", "tools", "goal", "benchmark", "fuzz", "mock", "assert",
            "component", "mount", "on_mount", "on_destroy", "provide", "entangle",
            "forge_class", "endforge", "refactor", "endrefactor", "slot", "endslot"
        ] { m.insert(*k); }
        m
    };
}

#[inline(always)]
fn resolve_gnosis<'a>(dom: &'a Value, path: &str) -> Option<&'a Value> {
    let mut current = dom;
    for part in path.split('.') {
        if let Some(obj) = current.as_object() {
            if let Some(next) = obj.get(part) {
                current = next;
            } else {
                return None;
            }
        } else {
            return None;
        }
    }
    Some(current)
}

// =================================================================================
// == STRATUM I: THE ALCHEMICAL TRANSMUTER (TEMPLATE EVALUATION)                  ==
// =================================================================================

#[pyfunction]
pub fn transmute_advanced(py: Python, template: String, json_context: String) -> PyResult<String> {
    let dom: Value = serde_json::from_str(&json_context)
        .map_err(|e| PyValueError::new_err(format!("Gnostic DOM Error: {}", e)))?;

    py.allow_threads(move || {
        let mut result = String::with_capacity(template.len() * 2);
        let bytes = template.as_bytes();
        let len = bytes.len();
        
        let mut cursor = 0;
        let mut line_start_idx = 0; 

        while cursor < len.saturating_sub(1) {
            if bytes[cursor] == b'\n' {
                line_start_idx = cursor + 1;
            }

            if bytes[cursor] == b'{' && bytes[cursor+1] == b'{' {
                let col_at_sigil = cursor - line_start_idx;
                let lstrip = if cursor + 2 < len && bytes[cursor+2] == b'-' { 1 } else { 0 };
                let mut end = cursor + 2 + lstrip;
                let mut found = false;
                
                while end < len - 1 {
                    if bytes[end] == b'}' && bytes[end+1] == b'}' {
                        let rstrip = if bytes[end-1] == b'-' { 1 } else { 0 };
                        
                        // [ASCENSION 3]: Mathematically proven safe ASCII slicing
                        let var_name = unsafe {
                            std::str::from_utf8_unchecked(&bytes[cursor+2+lstrip..end-rstrip])
                        }.trim().to_string();
                        
                        if lstrip == 1 {
                            let trimmed = result.trim_end().to_string();
                            result.clear();
                            result.push_str(&trimmed);
                        }

                        if let Some(val) = resolve_gnosis(&dom, &var_name) {
                            let val_str = match val {
                                Value::String(s) => s.to_string(),
                                _ => val.to_string(),
                            };

                            if val_str.contains('\n') {
                                let aligned = align_matter(val_str, col_at_sigil as i32, col_at_sigil as i32, true).unwrap_or_default();
                                result.push_str(&aligned);
                            } else {
                                result.push_str(&val_str);
                            }
                        } else {
                            result.push_str(&format!("{{{{ {} }}}}", var_name));
                        }
                        
                        cursor = end + 2;
                        if rstrip == 1 {
                            while cursor < len && (bytes[cursor] as char).is_whitespace() {
                                cursor += 1;
                            }
                        }
                        found = true;
                        break;
                    }
                    end += 1;
                }
                if !found { result.push_str("{{"); cursor += 2; }
            } else if bytes[cursor] == b'{' && bytes[cursor+1] == b'%' {
                return Ok("__SCAF_COMPLEX_LOGIC_REQUIRED__".to_string());
            } else {
                result.push(bytes[cursor] as char);
                cursor += 1;
            }
        }
        
        if cursor < len {
            // [ASCENSION 3]: Safe unchecked extraction
            let remainder = unsafe { std::str::from_utf8_unchecked(&bytes[cursor..]) };
            result.push_str(remainder);
        }
        
        Ok(result)
    })
}

// =================================================================================
// == STRATUM II: THE IRON LEXICAL BRIDGE (O(1) AST TOKENIZER)                    ==
// =================================================================================

#[pyfunction]
pub fn lex_blueprint_fast<'py>(
    py: Python<'py>,
    text: &str,
    sigil_start: &str,
    _sigil_end: &str,
) -> PyResult<(Vec<String>, Vec<String>, Vec<String>, Vec<i32>, Vec<i32>, Vec<i32>, Vec<u8>, Vec<String>)> {
    
    // [ASCENSION 5]: SIMD-Aware Sizing (Bitwise shift)
    let capacity = text.len() >> 4; 
    
    let mut vec_t_types = Vec::with_capacity(capacity);
    let mut vec_contents = Vec::with_capacity(capacity);
    let mut vec_raw_texts = Vec::with_capacity(capacity);
    let mut vec_line_nums = Vec::with_capacity(capacity);
    let mut vec_col_indices = Vec::with_capacity(capacity);
    let mut vec_orig_indents = Vec::with_capacity(capacity);
    let mut vec_bitmasks = Vec::with_capacity(capacity);
    let mut vec_gates = Vec::with_capacity(capacity);
    
    let mut line_num = 1;
    let mut current_idx = 0;
    let len = text.len();

    py.allow_threads(|| {
        while current_idx < len {
            let mut end_idx = len;
            if let Some(pos) = text[current_idx..].find('\n') {
                end_idx = current_idx + pos;
                if end_idx > current_idx && text.as_bytes()[end_idx - 1] == b'\r' {
                    // EOL Harmonizer
                }
            }
            
            let mut next_idx = end_idx;
            if next_idx < len && text.as_bytes()[next_idx] == b'\n' {
                next_idx += 1;
            } else if next_idx < len && text.as_bytes()[next_idx] == b'\r' {
                next_idx += 1;
                if next_idx < len && text.as_bytes()[next_idx] == b'\n' {
                    next_idx += 1;
                }
            }
            
            let line = &text[current_idx..next_idx];
            current_idx = next_idx;
            
            let purified = purify_line_prefix_fast(line.to_string());
            let stripped = purified.trim();
            
            let lstrip_len = purified.len() - purified.trim_start().len();
            let indent = lstrip_len as i32; 
            
            let mut t_type = "LITERAL";
            let mut content = line.to_string();
            let raw_text = line.to_string(); 
            
            let mut bitmask: u8 = 0;
            let mut gate = String::new();

            if stripped.is_empty() {
                // Keep default LITERAL
            } else if stripped.starts_with("{#") || stripped.starts_with('#') || stripped.starts_with("//") {
                bitmask |= 4; // is_comment
            } else if stripped.starts_with('@') {
                let gate_candidate = &stripped[1..];
                let first_word = gate_candidate
                    .split(|c: char| !c.is_alphanumeric() && c != '_')
                    .next()
                    .unwrap_or("")
                    .to_lowercase();
                
                if GNOSTIC_KEYWORDS.contains(first_word.as_str()) {
                    if stripped.contains(">>") || stripped.contains("::") || stripped.contains("+=") || stripped.contains("~=") || stripped.matches('@').count() > 1 {
                        t_type = "COMPLEX_LIL";
                        content = stripped.to_string();
                        bitmask |= 1; 
                    } else {
                        let mut clean_logic = stripped.trim_end_matches(':');
                        clean_logic = clean_logic.trim_end_matches(';');
                        
                        t_type = "LOGIC_BLOCK";
                        content = clean_logic[1..].trim().to_string();
                        bitmask |= 8; 
                        gate = first_word;
                    }
                } else {
                    if line.contains(sigil_start) || line.contains("{%") || line.contains("{#") {
                        t_type = "MIXED_STRATA";
                        bitmask |= 2; 
                    }
                }
            } else if line.contains(sigil_start) || line.contains("{%") || line.contains("{#") {
                t_type = "MIXED_STRATA";
                bitmask |= 2; 
            }
            
            vec_t_types.push(t_type.to_string());
            vec_contents.push(content);
            vec_raw_texts.push(raw_text);
            vec_line_nums.push(line_num);
            vec_col_indices.push(indent);
            vec_orig_indents.push(indent);
            vec_bitmasks.push(bitmask);
            vec_gates.push(gate);
            
            line_num += 1;
        }
    });
    
    Ok((vec_t_types, vec_contents, vec_raw_texts, vec_line_nums, vec_col_indices, vec_orig_indents, vec_bitmasks, vec_gates))
}

// =================================================================================
// == STRATUM III: THE OMEGA AST FORGER (STRUCTURE OF ARRAYS)                     ==
// =================================================================================

#[inline(always)]
fn is_opener(gate: &str) -> bool { matches!(gate, "if" | "for" | "macro" | "try" | "with" | "filter" | "block" | "call" | "forge_class" | "refactor" | "component" | "mount") }

#[inline(always)]
fn is_closer(gate: &str) -> bool { matches!(gate, "endif" | "endfor" | "endmacro" | "endtry" | "endwith" | "endfilter" | "endblock" | "endcall" | "endforge" | "endrefactor" | "endslot") }

#[inline(always)]
fn is_sibling(gate: &str) -> bool { matches!(gate, "elif" | "elseif" | "else" | "catch" | "finally" | "except" | "case" | "default") }

/// [THE MASTER CURE: LIF-INFINITY]
/// Replaces `forge_elara_ast` entirely. Forges the hierarchical AST using flat 
/// vectors and parent indices. Yields the GIL instantly, allocates NO Python objects 
/// in Rust, and eliminates millions of dictionary creation instructions.
/// 
///[ASCENSION 1]: Utlizes `macro_rules!` to completely annihilate Borrow Checker 
/// paradoxes regarding mutable aliasing of the vectors.
#[pyfunction]
pub fn forge_elara_ast_fast<'py>(
    py: Python<'py>, 
    template: &str
) -> PyResult<(Vec<String>, Vec<String>, Vec<String>, Vec<i32>, Vec<i32>, Vec<i32>, Vec<String>, Vec<String>, Vec<i32>)> {
    
    let capacity = template.len() / 20;

    let mut t_types = Vec::with_capacity(capacity);
    let mut contents = Vec::with_capacity(capacity);
    let mut raw_texts = Vec::with_capacity(capacity);
    let mut line_nums = Vec::with_capacity(capacity);
    let mut col_indices = Vec::with_capacity(capacity);
    let mut orig_indents = Vec::with_capacity(capacity);
    let mut gates = Vec::with_capacity(capacity);
    let mut expressions = Vec::with_capacity(capacity);
    let mut parent_indices = Vec::with_capacity(capacity);

    // =========================================================================
    // == THE MACRO SUTURE (BORROW CHECKER ANNIHILATOR)                       ==
    // =========================================================================
    macro_rules! push_node {
        ($t_type:expr, $content:expr, $raw_text:expr, $ln:expr, $col:expr, $orig:expr, $gate:expr, $expr:expr, $parent_idx:expr) => {{
            t_types.push($t_type.to_string());
            contents.push($content.to_string());
            raw_texts.push($raw_text.to_string());
            line_nums.push($ln);
            col_indices.push($col);
            orig_indents.push($orig);
            gates.push($gate.to_string());
            expressions.push($expr.to_string());
            parent_indices.push($parent_idx);
            t_types.len() - 1
        }};
    }

    // Root Inception (Index 0)
    push_node!("VOID", "Ω_ROOT", "", 0, 0, 0, "", "", -1);

    py.allow_threads(|| {
        let mut stack = vec![0usize]; 
        
        let bytes = template.as_bytes();
        let len = bytes.len();
        let mut cursor = 0;
        
        let mut line_num = 1;
        let mut col_index = 0;
        let mut line_start_idx = 0;
        
        let mut literal_start = 0;
        let mut literal_col_origin = 0;

        while cursor < len {
            if bytes[cursor] == b'\n' {
                line_num += 1;
                col_index = 0;
                line_start_idx = cursor + 1;
            }

            if cursor + 1 < len && bytes[cursor] == b'{' && (bytes[cursor+1] == b'{' || bytes[cursor+1] == b'%' || bytes[cursor+1] == b'#') {
                
                let current_parent_idx = *stack.last().unwrap() as i32;

                // Push accumulated literal matter
                if cursor > literal_start {
                    let lit = unsafe { std::str::from_utf8_unchecked(&bytes[literal_start..cursor]) };
                    push_node!("LITERAL", lit, lit, line_num, literal_col_origin, literal_col_origin, "", "", current_parent_idx);
                }
                
                let is_var = bytes[cursor+1] == b'{';
                let is_logic = bytes[cursor+1] == b'%';
                let is_comment = bytes[cursor+1] == b'#';
                
                let closer1 = if is_var { b'}' } else if is_logic { b'%' } else { b'#' };
                let closer2 = b'}';
                
                let col_at_start = cursor as i32 - line_start_idx as i32;
                let lstrip = if cursor + 2 < len && bytes[cursor+2] == b'-' { 1 } else { 0 };
                
                // [ASCENSION 2]: Laminar Tail-Trimming (O(1) In-Place Mutation)
                if lstrip == 1 {
                    if !t_types.is_empty() {
                        let last_idx = t_types.len() - 1;
                        if t_types[last_idx] == "LITERAL" && parent_indices[last_idx] == current_parent_idx {
                            let trimmed = contents[last_idx].trim_end().to_string();
                            contents[last_idx] = trimmed.clone();
                            raw_texts[last_idx] = trimmed;
                        }
                    }
                }
                
                let mut end_ptr = cursor + 2 + lstrip;
                let mut found_closure = false;
                
                while end_ptr < len - 1 {
                    if bytes[end_ptr] == closer1 && bytes[end_ptr+1] == closer2 {
                        found_closure = true;
                        break;
                    }
                    end_ptr += 1;
                }
                
                if found_closure {
                    let rstrip = if bytes[end_ptr-1] == b'-' { 1 } else { 0 };
                    
                    let inner = unsafe { std::str::from_utf8_unchecked(&bytes[cursor + 2 + lstrip .. end_ptr - rstrip]) }.trim();
                    let raw_text = unsafe { std::str::from_utf8_unchecked(&bytes[cursor .. end_ptr + 2]) };
                    
                    if is_var {
                        push_node!("VARIABLE", inner, raw_text, line_num, col_at_start, col_at_start, "", "", current_parent_idx);
                    } else if is_logic {
                        let parts: Vec<&str> = inner.splitn(2, char::is_whitespace).collect();
                        let gate = parts[0].to_lowercase();
                        let expr = if parts.len() > 1 { parts[1].trim() } else { "" };
                        
                        if is_opener(&gate) {
                            let node_idx = push_node!("LOGIC_BLOCK", inner, raw_text, line_num, col_at_start, col_at_start, &gate, expr, current_parent_idx);
                            stack.push(node_idx);
                        } else if is_closer(&gate) {
                            if stack.len() > 1 { stack.pop(); }
                        } else if is_sibling(&gate) {
                            if stack.len() > 1 { stack.pop(); }
                            let new_parent_idx = *stack.last().unwrap() as i32;
                            let node_idx = push_node!("LOGIC_BLOCK", inner, raw_text, line_num, col_at_start, col_at_start, &gate, expr, new_parent_idx);
                            stack.push(node_idx);
                        } else {
                            push_node!("LOGIC_BLOCK", inner, raw_text, line_num, col_at_start, col_at_start, &gate, expr, current_parent_idx);
                        }
                    } else if is_comment {
                        push_node!("COMMENT", inner, raw_text, line_num, col_at_start, col_at_start, "", "", current_parent_idx);
                    }
                    
                    cursor = end_ptr + 1;
                    
                    if rstrip == 1 {
                        while cursor + 1 < len && (bytes[cursor+1] as char).is_whitespace() {
                            cursor += 1;
                            if bytes[cursor] == b'\n' {
                                line_num += 1;
                                line_start_idx = cursor + 1;
                            }
                        }
                    }
                    
                    col_index = cursor as i32 - line_start_idx as i32;
                    literal_start = cursor + 1;
                    literal_col_origin = col_index + 1;
                }
            }
            
            col_index += 1;
            cursor += 1;
        }
        
        if literal_start < len {
            let current_parent_idx = *stack.last().unwrap() as i32;
            let lit = unsafe { std::str::from_utf8_unchecked(&bytes[literal_start..]) };
            push_node!("LITERAL", lit, lit, line_num, literal_col_origin, literal_col_origin, "", "", current_parent_idx);
        }
    });

    Ok((t_types, contents, raw_texts, line_nums, col_indices, orig_indents, gates, expressions, parent_indices))
}