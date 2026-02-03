# Path: scaffold/core/ai/rag/knowledge/rust_gnosis.py
# ---------------------------------------------------

RUST_SHARDS = [
    {
        "id": "rust_project_structure",
        "tags": ["rust", "cargo", "structure", "backend"],
        "content": "\n".join([
            "# Rust Project Structure (The Iron Standard)",
            "",
            "1. **Binary vs Library:**",
            "   - `src/main.rs`: The entry point for an executable.",
            "   - `src/lib.rs`: The entry point for a library (or shared logic).",
            "",
            "2. **Modules:**",
            "   - Use `mod.rs` for directories or `filename.rs` for flat modules.",
            "   - Expose public API via `pub mod` in `lib.rs`.",
            "",
            "3. **Workspaces:**",
            "   - For multi-crate projects, use a root `Cargo.toml` with `[workspace]`.",
            "   - Place crates in `crates/` or `apps/`.",
            "",
            "4. **Error Handling:**",
            "   - Use `thiserror` for libraries.",
            "   - Use `anyhow` for applications/binaries."
        ])
    },
    {
        "id": "rust_wasm_gnosis",
        "tags": ["rust", "wasm", "webassembly", "frontend"],
        "content": "\n".join([
            "# Rust to WASM Transmutation",
            "",
            "1. **Dependencies:**",
            "   - `wasm-bindgen`: To bridge Rust and JS.",
            "   - `web-sys`: To access DOM APIs.",
            "",
            "2. **Configuration:**",
            "   - In `Cargo.toml`: `crate-type = [\"cdylib\"]`.",
            "",
            "3. **Build:**",
            "   - Use `wasm-pack build --target web`.",
            "",
            "4. **Optimization:**",
            "   - Enable LTO (Link Time Optimization) in release profile.",
            "   - Use `wasm-opt` to shrink binary size."
        ])
    }
]