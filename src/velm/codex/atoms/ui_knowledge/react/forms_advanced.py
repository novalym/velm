# scaffold/semantic_injection/directives/ui_knowledge/forms_advanced.py

"""
=================================================================================
== THE GATES OF CHOICE (V-Ω-ADVANCED-FORMS)                                    ==
=================================================================================
This artisan provides complex form controls that are notoriously hard to style.
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("switch")
def forge_switch(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Toggle Switch using peer-checked Tailwind patterns.
    (A pure CSS implementation avoiding heavy Radix dependencies for simplicity,
    though Radix is recommended for full a11y).
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';

        export interface {name}Props extends React.InputHTMLAttributes<HTMLInputElement> {{
          label?: string;
        }}

        const {name} = React.forwardRef<HTMLInputElement, {name}Props>(
          ({{ className, label, ...props }}, ref) => (
            <div className="flex items-center space-x-2">
              <label className="relative inline-flex items-center cursor-pointer">
                <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    ref={{ref}}
                    {{...props}}
                />
                <div className={{cn(
                    "w-11 h-6 bg-input peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-background after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary",
                    className
                )}}></div>
                {{label && <span className="ml-3 text-sm font-medium text-foreground">{{label}}</span>}}
              </label>
            </div>
          )
        );
        {name}.displayName = "{name}";

        export {{ {name} }};
    """).strip()

@ComponentRegistry.register("select")
def forge_select(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a styled Native Select wrapper.
    (Simpler than a custom dropdown, but 100% accessible and mobile friendly).
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';
        import {{ ChevronDown }} from 'lucide-react';

        export interface {name}Props extends React.SelectHTMLAttributes<HTMLSelectElement> {{
          options?: {{ label: string; value: string }}[];
        }}

        const {name} = React.forwardRef<HTMLSelectElement, {name}Props>(
          ({{ className, options = [], children, ...props }}, ref) => (
            <div className="relative">
              <select
                className={{cn(
                  "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none",
                  className
                )}}
                ref={{ref}}
                {{...props}}
              >
                {{options.map((opt) => (
                  <option key={{opt.value}} value={{opt.value}}>
                    {{opt.label}}
                  </option>
                ))}}
                {{children}}
              </select>
              <ChevronDown className="absolute right-3 top-3 h-4 w-4 opacity-50 pointer-events-none" />
            </div>
          )
        );
        {name}.displayName = "{name}";

        export {{ {name} }};
    """).strip()