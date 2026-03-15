# Path: src/velm/codex/atoms/ui.py
# --------------------------------

"""
=================================================================================
== THE INTERFACE ARTISAN (V-Ω-HYBRID-OMNISCIENT-V500)                          ==
=================================================================================
LIF: 100,000,000,000,000 | ROLE: VISUAL_REALITY_ENGINE | RANK: OMEGA_SOVEREIGN

This artisan implements the `@ui` (or `ui.*`) namespace. It is the single source
of truth for all UI generation in the Scaffold Cosmos. It fuses Deterministic
Templates with Neural Creativity and Algorithmic Skeletons.

### THE PANTHEON OF 7 KINETIC RITES:
1.  **ui.component**: The Universal Component Factory (AI/Library/Skeleton).
2.  **ui.store**: The State Conduit (Zustand + Persistence).
3.  **ui.query**: The Data Fetcher (React Query/Fetch + Zod).
4.  **ui.mosaic**: The Micro-Frontend Shell (Module Federation).
5.  **ui.hook**: The Logic Encapsulator.
6.  **ui.tailwind**: The Style Configurator.
7.  **ui.utils**: The Class Merger (cn).

### THE GNOSTIC ASCENSIONS:
*   **Semantic Prop Triage:** `props="id:uuid, active:bool"` -> Typed TS Interface.
*   **Apophatic AI Fallback:** If AI fails, it gracefully degrades to a Skeleton.
*   **Safety Wards:** Injects `'use client'` automatically for interactive atoms.
=================================================================================
"""
import re
from textwrap import dedent
from typing import Dict, Any, List, Tuple, Optional

# --- THE DIVINE UPLINKS ---
# We invoke the Knowledge Registry to see if a deterministic form exists.
try:
    from .ui_knowledge import get_deterministic_component
except ImportError:
    # Fallback if knowledge base is unmanifest
    get_deterministic_component = lambda n, p: None

from ..contract import BaseDirectiveDomain
from ..injector import SemanticInjector
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("OcularArtisan")


@domain("ui")
class UiDomain(BaseDirectiveDomain):
    """
    The Forge of Pixels, Logic, and Neural Imagination.
    """

    @property
    def namespace(self) -> str:
        return "ui"

    def help(self) -> str:
        return "Generates React components, hooks, stores, and MFE shells."

    # =========================================================================
    # == STRATUM 0: THE COMPONENT FORGE (ui.component)                       ==
    # =========================================================================

    def _directive_component(self,
                             context: Dict[str, Any],
                             name: str,
                             props: str = "",
                             prompt: str = "",
                             ai: bool = False,
                             is_client: bool = True,
                             *args, **kwargs) -> str:
        """
        ui.component(name="Card", props="title:string, active:bool", ai=False)

        [THE MASTER BUILDER]
        Priority:
        1. AI Neural Path (if prompt/ai is set)
        2. Gnostic Component Codex (if name matches a known atom/molecule)
        3. Generic System Fallback (Algorithmic Skeleton)
        """
        # --- MOVEMENT I: THE PARSING OF PROPS ---
        prop_tuples, destructure_list = self._parse_props_logic(props)

        # Add implicit children/className if not explicitly forbidden
        if "children" not in destructure_list:
            prop_tuples.append(("children?", "React.ReactNode"))
            destructure_list.append("children")
        if "className" not in destructure_list:
            prop_tuples.append(("className?", "string"))
            destructure_list.append("className")

        # --- MOVEMENT II: THE NEURAL BRANCH (AI) ---
        if str(ai).lower() == 'true' or prompt:
            system_instruction = (
                f"Generate a React functional component named '{name}' using Tailwind CSS. "
                f"It must accept these props: {', '.join(destructure_list)}. "
                "Use 'lucide-react' for icons if appropriate. "
                "Ensure the code is production-ready TypeScript. "
                "Return ONLY the code (imports + interfaces + component), no markdown blocks."
            )
            user_instruction = prompt or f"A modern, accessible {name} component."

            try:
                # Recursive Injection: We call @ai/code via the Injector
                safe_prompt = user_instruction.replace('"', '\\"')
                directive = f'@ai/code(prompt="{safe_prompt}", lang="tsx", system="{system_instruction}")'

                # We use the Injector to bridge to the AI domain without circular imports
                generated_code = SemanticInjector.resolve(directive, context)

                # Gnostic Safety: If AI returns a heresy or void, we fall through.
                if "HERESY" not in generated_code and len(generated_code) > 50:
                    return generated_code
            except Exception as e:
                Logger.warn(f"Neural UI generation fractured: {e}. Falling back to Skeleton.")

        # --- MOVEMENT III: THE GNOSTIC CODEX BRANCH (LIBRARY) ---
        library_code = get_deterministic_component(name, prop_tuples)
        if library_code:
            return library_code

        # --- MOVEMENT IV: THE SYSTEM BRANCH (GENERIC FALLBACK) ---
        interface_name = f"{name}Props"

        # Forge Interface
        interface_lines = [f"export interface {interface_name} {{"]
        for p_name, p_type in prop_tuples:
            interface_lines.append(f"  {p_name}: {p_type};")
        interface_lines.append("}")
        interface_block = "\n".join(interface_lines)

        # Forge Destructuring
        props_str = f"{{ {', '.join(destructure_list)} }}"

        # Forge Imports
        imports = ["import React from 'react';"]
        if "cn" in context.get("utils", []) or True:  # Default assumption
            imports.append("import { cn } from '@/lib/utils';")

        header = "'use client';\n\n" if is_client else ""

        return dedent(f"""
            {header}{chr(10).join(imports)}

            {interface_block}

            export function {name}({props_str}: {interface_name}) {{
              return (
                <div className={{cn("relative overflow-hidden rounded-lg border bg-card text-card-foreground shadow-sm p-6", className)}}>
                  <div className="flex flex-col space-y-1.5">
                    {'{/* Generic Component Shell */}'}
                    <h3 className="text-lg font-semibold leading-none tracking-tight">{name}</h3>
                    <p className="text-sm text-muted-foreground">
                      Auto-generated scaffold for {name}.
                    </p>
                    <div className="mt-4">
                      {'{children}'}
                    </div>
                  </div>
                </div>
              );
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE SYNAPTIC STORE (ui.store)                            ==
    # =========================================================================

    def _directive_store(self,
                         context: Dict[str, Any],
                         name: str = "Auth",
                         state: str = "user:User|null, token:string|null",
                         persist: bool = True) -> str:
        """
        ui.store(name="Cart", state="items:CartItem[], total:number")

        [ASCENSION 4]: The State Conduit.
        Forges a fully typed Zustand store with optional persistence middleware.
        """
        store_name = f"use{name}Store"
        interface_name = f"{name}State"

        # Parse State
        state_props, _ = self._parse_props_logic(state)

        # 1. Forge Interface & Actions
        interface_lines = [f"interface {interface_name} {{"]
        initial_values = []
        actions = []

        for p_name, p_type in state_props:
            # Clean type for TS
            ts_type = p_type.replace('|', ' | ')

            interface_lines.append(f"  {p_name}: {ts_type};")
            interface_lines.append(f"  set{p_name[0].upper() + p_name[1:]}: (val: {ts_type}) => void;")

            # Determine initial value based on type
            init_val = "null"
            if "string" in ts_type:
                init_val = '""'
            elif "number" in ts_type:
                init_val = '0'
            elif "boolean" in ts_type:
                init_val = 'false'
            elif "[]" in ts_type or "Array" in ts_type:
                init_val = '[]'

            initial_values.append(f"{p_name}: {init_val},")
            actions.append(f"  set{p_name[0].upper() + p_name[1:]}: (val) => set({{ {p_name}: val }}),")

        interface_lines.append("}")
        interface_block = "\n".join(interface_lines)

        # 2. Persistence Logic
        middleware_import = "import { persist } from 'zustand/middleware';" if persist else ""
        store_wrapper_start = f"persist<{interface_name}>(" if persist else ""
        store_wrapper_end = f", {{ name: '{name.lower()}-storage' }})" if persist else ""

        return dedent(f"""
            import {{ create }} from 'zustand';
            {middleware_import}

            {interface_block}

            export const {store_name} = create<{interface_name}>()(
              {store_wrapper_start}(set) => ({{
                // Initial State
                {chr(10).join(initial_values)}

                // Actions
                {chr(10).join(actions)}
              }}){store_wrapper_end}
            );
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE DATA FETCHER (ui.query)                              ==
    # =========================================================================

    def _directive_query(self,
                         context: Dict[str, Any],
                         name: str = "User",
                         endpoint: str = "/api/user",
                         schema: str = "id:string, name:string") -> str:
        """
        ui.query(name="Products", endpoint="/api/products", schema="id:string, price:number")

        [ASCENSION 5]: The Data Hook.
        Forges a 'useQuery'-style hook using native fetch with Zod validation.
        """
        hook_name = f"use{name}Query"
        type_name = name

        # 1. Parse Schema for Zod
        props, _ = self._parse_props_logic(schema)
        zod_lines = []
        for p_name, p_type in props:
            z_type = "z.string()"
            if "number" in p_type:
                z_type = "z.number()"
            elif "boolean" in p_type:
                z_type = "z.boolean()"
            elif "[]" in p_type:
                z_type = "z.array(z.any())"

            zod_lines.append(f"  {p_name}: {z_type},")

        return dedent(f"""
            import {{ useState, useEffect, useCallback }} from 'react';
            import {{ z }} from 'zod';

            // [VALIDATION SCHEMA]
            export const {type_name}Schema = z.object({{
            {chr(10).join(zod_lines)}
            }});

            export type {type_name} = z.infer<typeof {type_name}Schema>;

            /**
             * === {hook_name} (V-Ω-DATA) ===
             * Fetches and validates {name} data from {endpoint}.
             */
            export function {hook_name}() {{
              const [data, setData] = useState<{type_name} | null>(null);
              const [loading, setLoading] = useState<boolean>(false);
              const [error, setError] = useState<string | null>(null);

              const fetchData = useCallback(async () => {{
                setLoading(true);
                try {{
                  const res = await fetch('{endpoint}');
                  if (!res.ok) throw new Error(`Network response was not ok: ${{res.status}}`);
                  const json = await res.json();

                  // Gnostic Validation
                  const parsed = {type_name}Schema.parse(json);
                  setData(parsed);
                  setError(null);
                }} catch (err) {{
                  console.error("Query Fracture:", err);
                  setError(err instanceof Error ? err.message : 'Unknown error');
                }} finally {{
                  setLoading(false);
                }}
              }}, []);

              useEffect(() => {{
                fetchData();
              }}, [fetchData]);

              return {{ data, loading, error, refetch: fetchData }};
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE MOSAIC SHELL (ui.mosaic)                             ==
    # =========================================================================

    def _directive_mosaic(self,
                          context: Dict[str, Any],
                          name: str = "shell",
                          remotes: List[str] = None,
                          port: int = 3000) -> str:
        """
        ui.mosaic(name="admin-hub", remotes=["dashboard", "settings"])

        [ASCENSION 3]: The MFE Mosaic Inception.
        Generates the complex Vite configuration for Module Federation.
        """
        remotes_list = remotes or ["sub-app"]
        remote_config_lines = []

        # Simple port assignment logic for dev convenience
        base_remote_port = 3001
        for i, r in enumerate(remotes_list):
            remote_config_lines.append(f"        {r}: 'http://localhost:{base_remote_port + i}/assets/remoteEntry.js',")

        return dedent(f"""
            /**
             * === GNOSTIC MOSAIC CONFIGURATION: {name.upper()} ===
             * Substrate: Vite + Module Federation
             */
            import {{ defineConfig }} from 'vite';
            import react from '@vitejs/plugin-react';
            import federation from '@originjs/vite-plugin-federation';

            export default defineConfig({{
              plugins: [
                react(),
                federation({{
                  name: '{name}',
                  remotes: {{
            {chr(10).join(remote_config_lines)}
                  }},
                  shared: ['react', 'react-dom', 'zustand', 'react-router-dom']
                }})
              ],
              server: {{
                port: {port},
                strictPort: true,
              }},
              build: {{
                modulePreload: false,
                target: 'esnext',
                minify: false,
                cssCodeSplit: false
              }}
            }});
        """).strip()

    # =========================================================================
    # == STRATUM 4: UTILITIES & HOOKS                                        ==
    # =========================================================================

    def _directive_hook(self, context: Dict[str, Any], name: str, logic: str = "", *args, **kwargs) -> str:
        """
        ui.hook(name="useLocalStorage", logic="storage")
        """
        if logic == "storage":
            return dedent(f"""
                import {{ useState, useEffect }} from 'react';

                export function {name}<T>(key: string, initialValue: T) {{
                  const [storedValue, setStoredValue] = useState<T>(() => {{
                    if (typeof window === 'undefined') return initialValue;
                    try {{
                      const item = window.localStorage.getItem(key);
                      return item ? JSON.parse(item) : initialValue;
                    }} catch (error) {{
                      return initialValue;
                    }}
                  }});

                  const setValue = (value: T | ((val: T) => T)) => {{
                    try {{
                      const valueToStore = value instanceof Function ? value(storedValue) : value;
                      setStoredValue(valueToStore);
                      if (typeof window !== 'undefined') {{
                        window.localStorage.setItem(key, JSON.stringify(valueToStore));
                      }}
                    }} catch (error) {{
                      console.warn(error);
                    }}
                  }};

                  return [storedValue, setValue] as const;
                }}
            """).strip()

        return dedent(f"""
            import {{ useState, useEffect, useCallback }} from 'react';

            export function {name}() {{
              const [value, setValue] = useState(null);
              useEffect(() => {{
                // Logic
              }}, []);
              return {{ value }};
            }}
        """).strip()

    def _directive_tailwind(self, context: Dict[str, Any], plugins: str = "", *args, **kwargs) -> str:
        """ui.tailwind(plugins="typography,forms")"""
        plugin_list = []
        if plugins:
            for p in plugins.split(','):
                clean_p = p.strip()
                if clean_p: plugin_list.append(f"require('@tailwindcss/{clean_p}')")

        if "require('tailwindcss-animate')" not in str(plugin_list):
            plugin_list.append("require('tailwindcss-animate')")

        return dedent(f"""
            /** @type {{import('tailwindcss').Config}} */
            module.exports = {{
              darkMode: ["class"],
              content: [
                './pages/**/*.{{ts,tsx}}',
                './components/**/*.{{ts,tsx}}',
                './app/**/*.{{ts,tsx}}',
                './src/**/*.{{ts,tsx}}',
              ],
              theme: {{
                container: {{ center: true, padding: "2rem", screens: {{ "2xl": "1400px" }} }},
                extend: {{
                  colors: {{
                    border: "hsl(var(--border))",
                    input: "hsl(var(--input))",
                    ring: "hsl(var(--ring))",
                    background: "hsl(var(--background))",
                    foreground: "hsl(var(--foreground))",
                    primary: {{ DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" }},
                    secondary: {{ DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" }},
                    destructive: {{ DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" }},
                    muted: {{ DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" }},
                    accent: {{ DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" }},
                  }},
                  borderRadius: {{ lg: "var(--radius)", md: "calc(var(--radius) - 2px)", sm: "calc(var(--radius) - 4px)" }},
                }},
              }},
              plugins: [{',\\n    '.join(plugin_list)}],
            }}
        """).strip()

    def _directive_utils(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """ui.utils()"""
        return dedent("""
            import { type ClassValue, clsx } from "clsx"
            import { twMerge } from "tailwind-merge"

            export function cn(...inputs: ClassValue[]) {
              return twMerge(clsx(inputs))
            }
        """).strip()

    # =========================================================================
    # == INTERNAL RITES                                                      ==
    # =========================================================================

    def _parse_props_logic(self, props_str: str) -> Tuple[List[Tuple[str, str]], List[str]]:
        """Splits 'name:type, active:bool' into tuples and names."""
        prop_tuples = []
        names = []

        if props_str:
            for p in props_str.split(','):
                if ':' in p:
                    k, v = p.split(':', 1)
                    prop_name = k.strip()
                    prop_type = v.strip()
                    if '|' in prop_type and "'" not in prop_type:
                        options = [f"'{o.strip()}'" for o in prop_type.split('|')]
                        prop_type = " | ".join(options)
                    prop_tuples.append((prop_name, prop_type))
                    names.append(prop_name)
                else:
                    clean = p.strip()
                    prop_tuples.append((clean, 'any'))
                    names.append(clean)

        return prop_tuples, names