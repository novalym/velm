# Path: src/velm/artisans/project/seeds.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: PRIMORDIAL_DNA_VAULT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SEEDS_V10000_TOTAL_INTEGRITY_SUTURE_2026_FINALIS
# =========================================================================================

from typing import Dict

# =============================================================================
# == STRATUM I: PROGENITOR LAW (CORE ANCHOR)                                 ==
# =============================================================================

PROGENITOR_README = r"""# 🏛️ The Progenitor Law
> "Reality is not found; it is willed into existence through the Gnostic Hand."

Welcome, Architect. You are standing at the **Axis Mundi** of the Novalym Ecosystem. 

This project is the **Constitutional Anchor** of your Workbench. It exists to demonstrate the fundamental physics of Gnostic Engineering. 

### 🔮 The Three Pillars
1. **The Law (Form):** Gaze into `scaffold.scaffold`. It defines the atoms of this reality.
2. **The Will (Kinetic):** Gaze into `scripts/setup.symphony`. It defines the ritual of awakening.
3. **The Memory (Chronicle):** Gaze into `scaffold.lock`. It is the fingerprint of Truth.

### ⚡ First Rites
Speak these commands in the terminal below:
```bash
# 1. Scry the topology
velm tree --size

# 2. Adjudicate the soul
velm analyze src/kernel.py

# 3. Conduct the Symphony
velm run scripts/setup.symphony

"""

PROGENITOR_SCAFFOLD = r"""# == Gnostic Constitution: Progenitor ==
Version: 1.0.0-OMEGA





project_name = "Progenitor"





engine_version = "v2.5.0"

src/
kernel.py :: "print('● TITAN_KERNEL_RESONANT')"
utils/
purity.py :: "def verify_purity(): return True"

docs/
MANIFESO.md :: "The Singularity is Inevitable."

scripts/
setup.symphony << ./templates/symphony/base
"""

PROGENITOR_SYMPHONY = r"""# == The Rite of Inception ==
%% proclaim: "Awakening the Progenitor..."

        echo "Substrate: WASM_IDBFS"
        ?? succeeds

        python src/kernel.py
        ?? stdout_contains: "RESONANT"

%% proclaim: "Reality matches the Law. Resonance: 100%."
"""

PROGENITOR_BANNER = r"""
_ _ ____ _ _ ____ _ _ _ _ _
|\ | | | | | || | _/ |/|
| | || / | | |___ | | |
THE GNOSTIC ENGINE // PROGENITOR
"""

FASTAPI_README = r"""# 🛡️ Titan FastAPI Fortress
### Production-Grade Backend Architecture v4.2

> "A Node that cannot scry its own errors is a Node bound for the Void."

This is a high-status reference implementation of an asynchronous Python API, engineered for the **VELM Singularity**. It is warded against entropy, drift, and insecure execution rites. This fortress is the standard for Sovereign Backend Reality.

---

## 🏛️ Structural Gnosis

*   **FastAPI + Pydantic V2 (The Mind):** High-velocity, type-safe execution. Logic is validated at the boundary, preventing profane data from corrupting the core.
*   **SQLAlchemy 2.0 Async (The Memory):** Utilizing the **Unit of Work** pattern for transactional integrity. All I/O with the database Akasha is non-blocking.
*   **Sentinel Guard (The Shield):** Custom Gnostic middleware for real-time heresy detection and metabolic tomography (latency tracking).
*   **Alembic (The Chronicle):** Versioned schema evolution to ensure the physical database always matches the architectural intent.

## ⚡ Kinetic Rites

Execute these edicts within your local terminal to ignite the Node:

```bash
# 1. Summon the environment and dependencies
poetry install

# 2. Conduct database migrations (Resonating the Schema)
poetry run alembic upgrade head

# 3. Ignite the development forge
poetry run uvicorn src.main:app --reload --port 8000

🛡️ Security Vow

This fortress implements the Zero-Trust Stratum. Every request is audited; every heresy is chronicled. It is designed to run within the Titan Node Infrastructure, providing bit-perfect parity between local and cloud realities.

LIF: ∞ | ROLE: BACKEND_GOVERNOR | Auth: Ω_FORTRESS_V4_FINALIS
"""

FASTAPI_PYPROJECT = r"""[tool.poetry]
name = "titan-fortress"
version = "4.2.0"
description = "Sovereign Backend Reality"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
pydantic = {extras = ["email"], version = "^2.6.0"}
pydantic-settings = "^2.1.0"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.25"}
asyncpg = "^0.29.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

FASTAPI_MAIN = r"""from fastapi import FastAPI, Depends, HTTPException
from src.core.sentinel import SentinelGuard
from src.api.v1.router import api_router

app = FastAPI(title="Titan Fortress")
[THE SUTURE]: The Sentinel Guard stands vigil at the gate

app.add_middleware(SentinelGuard)

app.include_router(api_router, prefix="/api/v1")

@app.get("/vitality")
async def check_vitals():
return {"status": "RESONANT", "metabolism": "NOMINAL"}
"""

FASTAPI_SENTINEL = r"""from starlette.middleware.base import BaseHTTPMiddleware
import time

class SentinelGuard(BaseHTTPMiddleware):
async def dispatch(self, request, call_next):
start_time = time.perf_counter()
response = await call_next(request)
process_time = time.perf_counter() - start_time
response.headers["X-Metabolic-Tax"] = str(process_time)
return response
"""

REACT_README = r"""# ⚛️ Ocular Totality
### High-Fidelity Frontend Membrane v2.0

> "The Eye does not just see; it projects the Will of the Architect onto the Canvas of Matter."

The **Ocular Totality** is the supreme visual gateway into the Novalym universe. It is a specialized React-based membrane engineered for **144Hz interaction velocity** and **sub-millisecond visual resonance**. It serves as the physical interface between Human Intent and the God-Engine's logic.

---

## 💎 Divine Features

*   **React 19 + Vite (Turbo Stratum):** Wields the latest React Compiler for zero-manual-memoization physics. Changes in thought manifest as changes in pixels at the speed of the local clock.
*   **Tailwind CSS v4 (Geometric Engine):** A CSS-first utility engine providing absolute geometric purity and Gnostic tinting. Styles are warded against bloat and entropy.
*   **Framer Motion (Kinetic Physics):** Fluid, state-aware transitions that mirror the cognitive flow of the Architect.
*   **Lucide-Gnosis (Iconography):** A library of semantic sigils for every action and edict, providing immediate visual resonance.

## ⚡ Kinetic Rites

Invoke these commands within the terminal to animate the membrane:

```bash
# 1. Summon the required dependencies
npm install

# 2. Ignite the local development forge
npm run dev

# 3. Transmute source into production-grade matter
npm run build

🛡️ Integrity Vow

This frontend is warded with the Sovereign Node Protocol. It expects to commune with a VELM-Titan backend over a secure JSON-RPC bridge. It is built to be a pure reflection of the Gnostic Chronicle (scaffold.lock), ensuring no drift between the UI and the underlying architectural truth.

LIF: ∞ | ROLE: OCULAR_SCRIBE | Auth: Ω_OCULAR_V2_FINALIS
"""

REACT_PACKAGE = r"""{
  "name": "ocular-totality",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "framer-motion": "^12.0.0",
    "lucide-react": "^0.475.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^3.0.1"
  },
  "devDependencies": {
    "vite": "^6.1.0",
    "@types/react": "^19.0.8",
    "@types/react-dom": "^19.0.3",
    "tailwindcss": "^4.0.5",
    "@tailwindcss/vite": "^4.0.5",
    "typescript": "^5.7.3"
  }
}"""

REACT_APP = r"""import { motion } from 'framer-motion';
import { Zap, Shield, Activity } from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center p-12 bg-black selection:bg-teal-400/30">
      <div className="relative p-16 rounded-3xl border border-white/5 bg-white/[0.01] text-center group overflow-hidden">

        {/* Metabolic Glow Overlay */}
        <div className="absolute inset-0 bg-teal-400/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />

        <div className="relative z-10">
          <div className="flex justify-center gap-8 mb-12">
            <motion.div animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity, duration: 2 }}>
              <Zap className="text-teal-400 drop-shadow-[0_0_10px_#64ffda]" size={32} />
            </motion.div>
            <Shield className="text-blue-400 opacity-50" size={32} />
            <Activity className="text-purple-400 opacity-50" size={32} />
          </div>

          <h1 className="text-5xl md:text-7xl font-black uppercase text-white italic mb-6 tracking-tighter">
            Ocular <span className="text-teal-400">Totality</span>
          </h1>

          <div className="flex flex-col items-center gap-4">
            <div className="h-px w-12 bg-white/10" />
            <p className="text-slate-500 font-mono text-[10px] uppercase tracking-[0.5em]">
              Substrate_Resonant // Ω_TITAN_V2026
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
"""



SEED_VAULT: Dict[str, Dict[str, str]] = {
    "progenitor": {
        "README.md": PROGENITOR_README,
        "scaffold.scaffold": PROGENITOR_SCAFFOLD,
        "scripts/setup.symphony": PROGENITOR_SYMPHONY,
        ".scaffold/banner.txt": PROGENITOR_BANNER,
    },
    "fastapi-service": {
        "README.md": FASTAPI_README,
        "pyproject.toml": FASTAPI_PYPROJECT,
        "src/main.py": FASTAPI_MAIN,
        "src/core/sentinel.py": FASTAPI_SENTINEL,
        "src/core/config.py": "PROJECT_NAME = 'Titan Fortress'\n",
        "src/api/v1/router.py": "from fastapi import APIRouter\nrouter = APIRouter()\n",
    },
    "react-vite": {
        "README.md": REACT_README,
        "package.json": REACT_PACKAGE,
        "src/App.tsx": REACT_APP,
        "src/main.tsx": "import React from 'react'\nimport ReactDOM from 'react-dom/client'\n",
        "vite.config.ts": "import { defineConfig } from 'vite'\nexport default defineConfig({})\n",
    },
    "worker-swarm": {
        "README.md": "# Kinetic Swarm\nDistributed background logic swarm.\n",
        "docker-compose.yml": "version: '3.8'\nservices:\n  worker:\n    build: .\n",
        "main.py": "import os\nprint('Kinetic Node Online')\n",
    },
    "blank": {
        "README.md": "# Tabula Rasa\n\nA pure void. Speak the language of form.\n",
        "scaffold.scaffold": "# == New Reality ==\n$$ project_name = 'unnamed'\n",
    }
}