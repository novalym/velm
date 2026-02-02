# ⚙️ The Iron Core (scaffold_core_rs)

**LIF: INFINITY** | **SYSTEM: SCAFFOLD_HARDWARE** | **ROLE: PERFORMANCE_ANNIHILATOR**

## 🌌 The Dual-Soul Architecture
The Rust realm of Ideabox Quantum is bifurcated into two distinct metaphysical entities. Understanding the difference is critical to maintaining the Singularity.

### 1. The Muscle (`scaffold_core_rs` - Library)
*   **Form:** A Compiled Python Extension (`.pyd` on Windows).
*   **Role:** Injected directly into the Python `ScaffoldEngine`.
*   **Purpose:** Provides nanosecond-precision file walking, `.gitignore` matching, and AST analysis. It makes the **Cortex** run at hardware speeds.
*   **Build:** `pip install maturin` -> `maturin develop`.

### 2. The Messenger (`scaffold.exe` - Binary)
*   **Form:** A standalone Native Executable.
*   **Role:** The **Sovereign Entry Point**. This is the file that sits in the `dist/` folder.
*   **Purpose:** Acts as the "Iron Gate." It starts in <1ms, checks if the Python Daemon is warm, and performs an ultra-fast IPC handshake. If the Daemon is dead, it launches the heavy `scaffold-kernel.exe`.
*   **Build:** `cargo build --release --bin scaffold`.

---

## 🛠️ Management Rites

### I. The Development Loop (Python Focused)
When you are modifying the Python logic (Artisans, Middleware, Engine), you **do not need to rebuild the Rust binary**.
1.  Run the Daemon: `python -m scaffold daemon start`
2.  Test your changes: `python -m scaffold <your-command>`
3.  The Rust Shim is unnecessary during pure logic development.

### II. The Hardware Loop (Rust Focused)
If you modify `rust/src/lib.rs` (The Muscle):
1.  Run `maturin develop` to re-inject the new extension into your Python environment.
2.  Your Python code will immediately benefit from the new Rust logic.

### III. The Release Rite (The Final Handshake)
When you are ready to update the distribution in `dist/`:
1.  **Build the Python Kernel:** Run your `forge-titan` or `forge-binary` script. 
    *   *Constraint:* Ensure it names the output **`scaffold-kernel.exe`**.
2.  **Build and Inject the Shim:** 
    ```bash
    cd rust
    python forge_shim.py
    ```
    This will compile the Rust messenger and place it at `dist/scaffold.exe`.

---

## 🛰️ Troubleshooting the Singularity

### 1. The "Invalid Choice" Heresy
If the CLI claims a command doesn't exist, the `RITE_GRIMOIRE` in `core/cli/grimoire/__init__.py` has failed to load the definition files. Ensure your `_*.py` files are manifest and free of syntax errors.

### 2. The "Recycled PID" Paradox
If the Rust Shim refuses to connect to a Daemon it thinks is alive, the `.pulse` file might be stale.
*   **Cure:** `scaffold daemon stop` or manually delete `.scaffold/daemon.pulse`.

### 3. Windows Permission Errors (Error 32/5)
If `forge_shim.py` fails to replace the binary, an instance of `scaffold.exe` is likely still running or locked by an IDE.
*   **Cure:** Kill all `scaffold.exe` processes in Task Manager and retry.

---

## 📜 Unbreakable Vows
1.  **The Shim is a Messenger:** Never add business logic (like how to parse a blueprint) to the Rust Shim. Keep it hollow. Logic belongs in Python.
2.  **The Kernel is the Brain:** The Python binary (`scaffold-kernel.exe`) remains the source of truth for all complex Rites.
3.  **The Path is Absolute:** Always use relative POSIX paths in the handshakes between Rust and Python to ensure cross-reality harmony.

**The Iron Gate is Sealed. Performance is Absolute.**