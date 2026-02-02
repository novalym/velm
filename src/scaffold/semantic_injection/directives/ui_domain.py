# scaffold/semantic_injection/directives/ui_domain.py

"""
=================================================================================
== THE INTERFACE ARTISAN (V-Ω-HYBRID-OMNISCIENT)                               ==
=================================================================================
LIF: 100,000,000,000,000,000,000,000,000

This artisan implements the `@ui` namespace. It is a hyper-intelligent
orchestrator that fuses Deterministic Knowledge with Neural Creativity.

It is the single source of truth for all UI generation in the Scaffold Cosmos.

Usage:
    # 1. The Codex Path (Deterministic, Best-Practice)
    Button.tsx :: @ui/component(name="Button", props="variant:enum")

    # 2. The Neural Path (AI-Generated)
    Dashboard.tsx :: @ui/component(name="Dashboard", prompt="Dark mode analytics with charts", ai=true)

    # 3. The System Path (Algorithmic Fallback)
    UnknownWidget.tsx :: @ui/component(name="UnknownWidget")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List, Tuple

# The Divine Summons of the Knowledge Registry
from .ui_knowledge import get_deterministic_component
from ..contract import BaseDirectiveDomain
from ..injector import SemanticInjector
from ..loader import domain


@domain("ui")
class UiDomain(BaseDirectiveDomain):
    """
    The Forge of Pixels, Logic, and Neural Imagination.
    """

    @property
    def namespace(self) -> str:
        return "ui"

    def help(self) -> str:
        return "Generates React components (Library, AI, or Generic), hooks, and configs."

    # =========================================================================
    # == THE RITE OF THE HYBRID COMPONENT                                    ==
    # =========================================================================

    def _directive_component(self, context: Dict[str, Any], name: str, props: str = "", prompt: str = "",
                             ai: bool = False, *args, **kwargs) -> str:
        """
        @ui/component(name="Card", props="title:string", prompt="...", ai=false)

        The Master Builder.
        Priority:
        1. AI Neural Path (if prompt/ai is set)
        2. Gnostic Component Codex (if name matches a known atom/molecule)
        3. Generic System Fallback
        """
        # --- MOVEMENT I: THE PARSING OF PROPS ---
        # We transmute the raw string "key:type, key:type" into a structured List[Tuple].
        prop_tuples: List[Tuple[str, str]] = []
        destructure_list: List[str] = []

        if props:
            for p in props.split(','):
                if ':' in p:
                    k, v = p.split(':', 1)
                    prop_name = k.strip()
                    prop_type = v.strip()

                    # Handle union types shorthand "status:active|inactive"
                    if '|' in prop_type and "'" not in prop_type and '"' not in prop_type:
                        options = [f"'{o.strip()}'" for o in prop_type.split('|')]
                        prop_type = " | ".join(options)

                    prop_tuples.append((prop_name, prop_type))
                    destructure_list.append(prop_name)
                else:
                    p_clean = p.strip()
                    prop_tuples.append((p_clean, 'any'))
                    destructure_list.append(p_clean)

        # Add implicit children/className if not explicitly forbidden (future flag)
        has_children = "children" in destructure_list
        if not has_children:
            prop_tuples.append(("children?", "React.ReactNode"))
            destructure_list.append("children")

        if "className" not in destructure_list:
            prop_tuples.append(("className?", "string"))
            destructure_list.append("className")

        # --- MOVEMENT II: THE NEURAL BRANCH (AI) ---
        # If the Architect demands creativity, we summon the Neural Cortex.
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
                # We escape quotes carefully to prevent syntax errors in the recursive call.
                safe_prompt = user_instruction.replace('"', '\\"')
                directive = f'@ai/code(prompt="{safe_prompt}", lang="tsx", system="{system_instruction}")'

                generated_code = SemanticInjector.resolve(directive, context)

                # Gnostic Safety: If AI returns a heresy or void, we fall through.
                if "HERESY" not in generated_code and len(generated_code) > 50:
                    return generated_code
            except Exception:
                pass  # Fallback to Deterministic

        # --- MOVEMENT III: THE GNOSTIC CODEX BRANCH (LIBRARY) ---
        # We consult the Registry. If the component is known (e.g. "Button", "Navbar"),
        # we return the handcrafted, perfected implementation.
        library_code = get_deterministic_component(name, prop_tuples)

        if library_code:
            return library_code

        # --- MOVEMENT IV: THE SYSTEM BRANCH (GENERIC FALLBACK) ---
        # The component is unknown, and no AI was requested. We forge a robust skeleton.

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
        if "cn" in context.get("utils", []) or True:  # Assume we want cn by default in this stack
            imports.append("import { cn } from '@/lib/utils';")

        # Heuristic: Is it a client component?
        is_client = any(k in name.lower() for k in ["modal", "input", "form", "dropdown", "sheet", "provider"])
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
    # == THE RITE OF LOGIC (HOOKS)                                           ==
    # =========================================================================

    def _directive_hook(self, context: Dict[str, Any], name: str, logic: str = "", *args, **kwargs) -> str:
        """
        @ui/hook(name="useLocalStorage", logic="storage")
        Generates custom React hooks.
        """
        if logic == "storage":
            return dedent(f"""
                import {{ useState, useEffect }} from 'react';

                export function {name}<T>(key: string, initialValue: T) {{
                  // State to store our value
                  // Pass initial state function to useState so logic is only executed once
                  const [storedValue, setStoredValue] = useState<T>(() => {{
                    if (typeof window === 'undefined') {{
                      return initialValue;
                    }}
                    try {{
                      const item = window.localStorage.getItem(key);
                      return item ? JSON.parse(item) : initialValue;
                    }} catch (error) {{
                      console.warn(`Error reading localStorage key "${{key}}":`, error);
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
                      console.warn(`Error setting localStorage key "${{key}}":`, error);
                    }}
                  }};

                  return [storedValue, setValue] as const;
                }}
            """).strip()

        # Generic Hook Fallback
        return dedent(f"""
            import {{ useState, useEffect, useCallback }} from 'react';

            export function {name}() {{
              const [value, setValue] = useState(null);

              const doWork = useCallback(() => {{
                // Implementation
              }}, []);

              useEffect(() => {{
                doWork();
              }}, [doWork]);

              return {{ value, doWork }};
            }}
        """).strip()

    # =========================================================================
    # == THE RITE OF FOUNDATION (CONFIGS & UTILS)                            ==
    # =========================================================================

    def _directive_tailwind(self, context: Dict[str, Any], plugins: str = "", *args, **kwargs) -> str:
        """
        @ui/tailwind(plugins="typography,forms,animate")
        Generates a robust tailwind.config.js tailored for Shadcn/UI.
        """
        plugin_list = []
        if plugins:
            for p in plugins.split(','):
                clean_p = p.strip()
                if clean_p:
                    plugin_list.append(f"require('@tailwindcss/{clean_p}')")

        # Always include animate for modern UIs
        if "require('tailwindcss-animate')" not in str(plugin_list):
            plugin_list.append("require('tailwindcss-animate')")

        plugins_str = ",\n    ".join(plugin_list)

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
                container: {{
                  center: true,
                  padding: "2rem",
                  screens: {{ "2xl": "1400px" }},
                }},
                extend: {{
                  colors: {{
                    border: "hsl(var(--border))",
                    input: "hsl(var(--input))",
                    ring: "hsl(var(--ring))",
                    background: "hsl(var(--background))",
                    foreground: "hsl(var(--foreground))",
                    primary: {{
                      DEFAULT: "hsl(var(--primary))",
                      foreground: "hsl(var(--primary-foreground))",
                    }},
                    secondary: {{
                      DEFAULT: "hsl(var(--secondary))",
                      foreground: "hsl(var(--secondary-foreground))",
                    }},
                    destructive: {{
                      DEFAULT: "hsl(var(--destructive))",
                      foreground: "hsl(var(--destructive-foreground))",
                    }},
                    muted: {{
                      DEFAULT: "hsl(var(--muted))",
                      foreground: "hsl(var(--muted-foreground))",
                    }},
                    accent: {{
                      DEFAULT: "hsl(var(--accent))",
                      foreground: "hsl(var(--accent-foreground))",
                    }},
                  }},
                  borderRadius: {{
                    lg: "var(--radius)",
                    md: "calc(var(--radius) - 2px)",
                    sm: "calc(var(--radius) - 4px)",
                  }},
                }},
              }},
              plugins: [
                {plugins_str}
              ],
            }}
        """).strip()

    def _directive_utils(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @ui/utils
        Generates the sacred `cn` utility for Tailwind class merging.
        """
        return dedent("""
            import { type ClassValue, clsx } from "clsx"
            import { twMerge } from "tailwind-merge"

            export function cn(...inputs: ClassValue[]) {
              return twMerge(clsx(inputs))
            }
        """).strip()