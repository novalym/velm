// Path: rust/src/bin/scaffold.rs
// -----------------------------
// LIF: INFINITY | ROLE: ZERO_LATENCY_MESSENGER | AUTH: Ω_IRON_GATE_V1
// =================================================================================
// This binary acts as the sovereign entry point. It implements the "Fast Path"
// to the warm Daemon, achieving <10ms response times.
// =================================================================================

use std::env;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::process::{Command, Stdio};
use std::fs;
use std::path::{Path, PathBuf};
use serde::{Deserialize};

#[derive(Deserialize)]
struct PulseFile {
    pid: u32,
    port: u16,
    token: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. COLLECT INTENT (Args & Environment)
    let args: Vec<String> = env::args().skip(1).collect();
    let exe_path = env::current_exe()?;
    let exe_dir = exe_path.parent().unwrap();
    
    // 2. THE DAEMON PROBE
    // We attempt to find the Project Root to locate the Pulse file.
    if let Some(project_root) = find_root() {
        let pulse_path = project_root.join(".scaffold").join("daemon.pulse");
        
        if pulse_path.exists() {
            if let Ok(content) = fs::read_to_string(&pulse_path) {
                // Parse the Gnostic Pulse (JSON or Legacy)
                if let Some(conn) = parse_connection(&content) {
                    // --- MOVEMENT I: THE FAST PATH HANDSHAKE ---
                    // We attempt a TCP link with a 50ms timeout.
                    if let Ok(mut stream) = TcpStream::connect_timeout(
                        &format!("127.0.0.1:{}", conn.port).parse().unwrap(),
                        std::time::Duration::from_millis(50)
                    ) {
                        // Forge the JSON-RPC Plea
                        let method = args.get(0).map(|s| s.as_str()).unwrap_or("help");
                        let payload = serde_json::json!({
                            "jsonrpc": "2.0",
                            "method": method,
                            "params": { 
                                "args": args, 
                                "auth_token": conn.token,
                                "client_mode": "RUST_SHIM" 
                            },
                            "id": 1
                        });

                        if let Ok(bytes) = serde_json::to_vec(&payload) {
                            stream.write_all(&bytes)?;
                            // Send FIN to signal end of request
                            stream.shutdown(std::net::Shutdown::Write)?;
                            
                            // Relay the Daemon's Wisdom back to the user
                            let mut buffer = Vec::new();
                            if stream.read_to_end(&mut buffer).is_ok() {
                                std::io::stdout().write_all(&buffer)?;
                                return Ok(()); // 5ms Success
                            }
                        }
                    }
                }
            }
        }
    }

    // --- MOVEMENT II: THE KERNEL FALLBACK (THE 4s PATH) ---
    // If the Daemon is dead or the fast-path fails, we pay the "Python Tax".
    
    // Check for the "Frozen Soul" (scaffold-kernel.exe)
    let kernel_name = if cfg!(windows) { "scaffold-kernel.exe" } else { "scaffold-kernel" };
    let kernel_path = exe_dir.join(kernel_name);

    if kernel_path.exists() {
        // [ASCENSION]: Execute your existing PyInstaller/PyOxidizer binary
        let mut child = Command::new(kernel_path)
            .args(&args)
            .stdout(Stdio::inherit())
            .stderr(Stdio::inherit())
            .spawn()?;
        let status = child.wait()?;
        std::process::exit(status.code().unwrap_or(0));
    } else {
        // [DEVELOPMENT FALLBACK]: If no binary exists, run via Python Module
        let python_exe = if cfg!(windows) { "python.exe" } else { "python3" };
        let mut child = Command::new(python_exe)
            .arg("-m")
            .arg("scaffold")
            .args(&args)
            .stdout(Stdio::inherit())
            .stderr(Stdio::inherit())
            .spawn()?;
        let status = child.wait()?;
        std::process::exit(status.code().unwrap_or(0));
    }
}

fn parse_connection(content: &str) -> Option<PulseFile> {
    let content = content.trim();
    if content.starts_with('{') {
        serde_json::from_str::<PulseFile>(content).ok()
    } else {
        let parts: Vec<&str> = content.split(':').collect();
        if parts.len() >= 3 {
            Some(PulseFile {
                pid: parts[0].parse().unwrap_or(0),
                port: parts[1].parse().unwrap_or(5555),
                token: parts[2].to_string(),
            })
        } else { None }
    }
}

fn find_root() -> Option<PathBuf> {
    let mut curr = env::current_dir().ok()?;
    for _ in 0..12 {
        if curr.join(".scaffold").exists() { return Some(curr); }
        if let Some(parent) = curr.parent() { curr = parent.to_path_buf(); } 
        else { break; }
    }
    None
}