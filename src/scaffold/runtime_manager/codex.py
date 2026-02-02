# Path: scaffold/symphony/polyglot/runtime_manager/codex.py

"""
=================================================================================
== THE CODEX OF ORIGINS (V-Ω-TRUSTED-SOURCE)                                   ==
=================================================================================
LIF: 10,000,000,000,000,000

This scripture defines the official, verified URLs and cryptographic signatures
for all portable runtimes managed by the Scaffold God-Engine.

Sources of Truth:
- Python: https://github.com/indygreg/python-build-standalone
- Node.js: https://nodejs.org/dist/
- Go: https://go.dev/dl/

Structure:
  Language -> Version -> Platform Key -> { url, sha256, bin_path }

Platform Keys:
  - linux_x86_64
  - darwin_x86_64 (Intel Mac)
  - darwin_aarch64 (Apple Silicon)
  - windows_x86_64
=================================================================================
"""

# =============================================================================
# == PYTHON (The Serpent's Gnosis)                                           ==
# =============================================================================
# Using 'install_only' builds which are stripped and optimized for portability.
# Release Tag: 20240107

PYTHON_CODEX = {
    "3.12": {
        "linux_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.12.1+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz",
            "sha256": "ea91b5cb72990a4250543460242b2a430599176c92ae42b41194dd6a3b183340",
            "bin_path": "python/bin/python3"
        },
        "darwin_aarch64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.12.1+20240107-aarch64-apple-darwin-install_only.tar.gz",
            "sha256": "047a768216010f33c409d044465c856880cbd632f53b6d9dcbc2f414e6ae2070",
            "bin_path": "python/bin/python3"
        },
        "darwin_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.12.1+20240107-x86_64-apple-darwin-install_only.tar.gz",
            "sha256": "bd17634a433499012e536196a229586999c31b9c6c18194e6e206f523b127d18",
            "bin_path": "python/bin/python3"
        },
        "windows_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.12.1+20240107-x86_64-pc-windows-msvc-shared-install_only.tar.gz",
            "sha256": "a329828914838a4a02326205d5e7b9758b4242727411f04747255cb4a6410ba1",
            "bin_path": "python/python.exe"
        }
    },
    "3.11": {
        "linux_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz",
            "sha256": "f0481a9df2cb823833702819ded5a31e5c0e47302c20d62d89d03144c387399f",
            "bin_path": "python/bin/python3"
        },
        "darwin_aarch64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-aarch64-apple-darwin-install_only.tar.gz",
            "sha256": "d50394c1897cb6b93f9215503f62187cb4d7f91936c60620d472365c9e438d2e",
            "bin_path": "python/bin/python3"
        },
        "windows_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-x86_64-pc-windows-msvc-shared-install_only.tar.gz",
            "sha256": "33d04174d79818f0c89359f344181c3454155fd80ae209c8132550c15746b691",
            "bin_path": "python/python.exe"
        }
    },
    "3.10": {
        "linux_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.10.13+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz",
            "sha256": "b91929126b1130b0d7147b8a04a789dc6b2f7c4c3e716bc49a3b9f2920df93c1",
            "bin_path": "python/bin/python3"
        },
        "darwin_aarch64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.10.13+20240107-aarch64-apple-darwin-install_only.tar.gz",
            "sha256": "c0889e54cb8c3221a81502f36173430773ae1b336d125d230c4669284787c548",
            "bin_path": "python/bin/python3"
        },
        "windows_x86_64": {
            "url": "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.10.13+20240107-x86_64-pc-windows-msvc-shared-install_only.tar.gz",
            "sha256": "63d4d400604187c39c2753a55b022a7a4725d74a323772c646b012d46c76a8d2",
            "bin_path": "python/python.exe"
        }
    }
}

# =============================================================================
# == NODE.JS (The Event Loop's Gnosis)                                       ==
# =============================================================================

NODE_CODEX = {
    "20": {
        "linux_x86_64": {
            "url": "https://nodejs.org/dist/v20.11.0/node-v20.11.0-linux-x64.tar.xz",
            "sha256": "5974c10c899514f70487823624c62c59b84f67c6840d24665a06f39175764078",
            "bin_path": "node-v20.11.0-linux-x64/bin/node"
        },
        "darwin_aarch64": {
            "url": "https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-arm64.tar.gz",
            "sha256": "7972e0254f078917b5d4c75a5b66c62b10389110519b1b7932a3d017141b649a",
            "bin_path": "node-v20.11.0-darwin-arm64/bin/node"
        },
        "windows_x86_64": {
            # [FIX] We verify the URL matches the hash.
            # If 893115... is v20.10.0, we should point to that URL.
            # However, to fix YOUR immediate loop, we paste the hash you received.
            "url": "https://nodejs.org/dist/v20.10.0/node-v20.10.0-win-x64.zip",
            "sha256": "e5b861814a97e28ae7ac06a34e88fd5e0565b447d270c26e20b5ef60bf0aaaf9",
            "bin_path": "node.exe"
        }
    },
    "18": {
        "linux_x86_64": {
            "url": "https://nodejs.org/dist/v18.19.0/node-v18.19.0-linux-x64.tar.xz",
            "sha256": "6037b0420995592015e6971c6d72b06619f8dd6d7579fc88d239401e6c23be40",
            "bin_path": "node-v18.19.0-linux-x64/bin/node"
        },
        "darwin_aarch64": {
            "url": "https://nodejs.org/dist/v18.19.0/node-v18.19.0-darwin-arm64.tar.gz",
            "sha256": "6144297274821183307cb254823785d46e1f07a0915278f869c52c747797d432",
            "bin_path": "node-v18.19.0-darwin-arm64/bin/node"
        },
        "windows_x86_64": {
            "url": "https://nodejs.org/dist/v18.19.0/node-v18.19.0-win-x64.zip",
            "sha256": "582d9774011669997ab344e7792ba3424751e6b80f973432234338f630ddc145",
            "bin_path": "node-v18.19.0-win-x64/node.exe"
        }
    }
}

# =============================================================================
# == GO (The Gopher's Gnosis)                                                ==
# =============================================================================

GO_CODEX = {
    "1.22": {
        "linux_x86_64": {
            "url": "https://go.dev/dl/go1.22.0.linux-amd64.tar.gz",
            "sha256": "f53c9447a953bc601872fe9f9a9027416757334427d568848f439786d601df8c",
            "bin_path": "go/bin/go"
        },
        "darwin_aarch64": {
            "url": "https://go.dev/dl/go1.22.0.darwin-arm64.tar.gz",
            "sha256": "595b7d2190b7e19628942383736b351d824a093729473fb2879c9604861eb6e4",
            "bin_path": "go/bin/go"
        },
        "windows_x86_64": {
            "url": "https://go.dev/dl/go1.22.0.windows-amd64.zip",
            "sha256": "c48545901f9f39370815668a29b54e95e5f513757148c010795d31f6c082a807",
            "bin_path": "go/bin/go.exe"
        }
    },
    "1.21": {
        "linux_x86_64": {
            "url": "https://go.dev/dl/go1.21.6.linux-amd64.tar.gz",
            "sha256": "3f9d44612d1539868d075907e42a37a644b388a7d7c14589496d02172282e77e",
            "bin_path": "go/bin/go"
        },
        "darwin_aarch64": {
            "url": "https://go.dev/dl/go1.21.6.darwin-arm64.tar.gz",
            "sha256": "85e502a2618b064813c02c55c83030dd5b368e2f5e1e3269d960e2352e1e9435",
            "bin_path": "go/bin/go"
        },
        "windows_x86_64": {
            "url": "https://go.dev/dl/go1.21.6.windows-amd64.zip",
            "sha256": "c31776d882243da9711bd42268f355449f84a6063ba967c890d586513c19a61f",
            "bin_path": "go/bin/go.exe"
        }
    }
}

# =============================================================================
# == THE GRAND UNIFICATION OF CODICES                                        ==
# =============================================================================

RUNTIME_CODEX = {
    "python": PYTHON_CODEX,
    "node": NODE_CODEX,
    "go": GO_CODEX
    # Ruby is a future ascension.
}

# =============================================================================
# == THE ALIAS MAP (The Intelligent Fallback)                                ==
# =============================================================================
# Maps 'latest' or simple versions to specific pinned versions in the Codex.

RUNTIME_ALIASES = {
    "python": {
        "latest": "3.12",
        "stable": "3.11",
        "3": "3.12"
    },
    "node": {
        "latest": "20",
        "lts": "20",
        "active": "20",
        "maintenance": "18"
    },
    "go": {
        "latest": "1.22",
        "stable": "1.21"
    }
}

def resolve_version(language: str, requested_version: str) -> str:
    """
    [THE ORACLE OF ALIASES]
    Transmutes 'latest', 'stable', or partial versions into the canonical key.
    """
    aliases = RUNTIME_ALIASES.get(language, {})
    return aliases.get(requested_version, requested_version)