# scaffold/semantic_injection/directives/ui_knowledge/feedback.py

"""
=================================================================================
== THE PULSE OF THE INTERFACE (V-Ω-FEEDBACK)                                   ==
=================================================================================
This artisan provides visual feedback mechanisms.
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("skeleton")
def forge_skeleton(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Skeleton component for loading states.
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';

        export interface {name}Props extends React.HTMLAttributes<HTMLDivElement> {{}}

        function {name}({{ className, ...props }}: {name}Props) {{
          return (
            <div
              className={{cn("animate-pulse rounded-md bg-muted", className)}}
              {{...props}}
            />
          );
        }}

        export {{ {name} }};
    """).strip()

@ComponentRegistry.register("toast")
def forge_toast(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a simple, dependency-free Toast notification component.
    Note: A full Toast usually requires a Provider context, this is the visual Atom.
    """
    return dedent(f"""
        import React from 'react';
        import {{ X }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';
        import {{ cva, type VariantProps }} from 'class-variance-authority';

        const toastVariants = cva(
          "group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all",
          {{
            variants: {{
              variant: {{
                default: "border bg-background text-foreground",
                destructive:
                  "destructive group border-destructive bg-destructive text-destructive-foreground",
              }},
            }},
            defaultVariants: {{
              variant: "default",
            }},
          }}
        );

        export interface {name}Props
          extends React.HTMLAttributes<HTMLDivElement>,
            VariantProps<typeof toastVariants> {{
            title?: string;
            description?: string;
            onClose?: () => void;
        }}

        export function {name}({{ className, variant, title, description, onClose, ...props }}: {name}Props) {{
          return (
            <div className={{cn(toastVariants({{ variant }}), className)}} {{...props}}>
              <div className="grid gap-1">
                {{title && <div className="text-sm font-semibold">{{title}}</div>}}
                {{description && <div className="text-sm opacity-90">{{description}}</div>}}
              </div>
              {{onClose && (
                <button
                  onClick={{onClose}}
                  className="absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100"
                >
                  <X className="h-4 w-4" />
                </button>
              )}}
            </div>
          );
        }}
    """).strip()