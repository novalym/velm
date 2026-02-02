from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("button")
def forge_button(name: str, props: List[Tuple[str, str]]) -> str:
    return dedent(f"""
        import React from 'react';
        import {{ Slot }} from '@radix-ui/react-slot';
        import {{ cva, type VariantProps }} from 'class-variance-authority';
        import {{ cn }} from '@/lib/utils';

        const buttonVariants = cva(
          "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
          {{
            variants: {{
              variant: {{
                default: "bg-primary text-primary-foreground hover:bg-primary/90",
                destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
                outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
                secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
                ghost: "hover:bg-accent hover:text-accent-foreground",
                link: "text-primary underline-offset-4 hover:underline",
              }},
              size: {{
                default: "h-10 px-4 py-2",
                sm: "h-9 rounded-md px-3",
                lg: "h-11 rounded-md px-8",
                icon: "h-10 w-10",
              }},
            }},
            defaultVariants: {{
              variant: "default",
              size: "default",
            }},
          }}
        );

        export interface {name}Props
          extends React.ButtonHTMLAttributes<HTMLButtonElement>,
            VariantProps<typeof buttonVariants> {{
          asChild?: boolean;
        }}

        const {name} = React.forwardRef<HTMLButtonElement, {name}Props>(
          ({{ className, variant, size, asChild = false, ...props }}, ref) => {{
            const Comp = asChild ? Slot : "button";
            return (
              <Comp
                className={{cn(buttonVariants({{ variant, size, className }}))}}
                ref={{ref}}
                {{...props}}
              />
            );
          }}
        );
        {name}.displayName = "{name}";

        export {{ {name}, buttonVariants }};
    """).strip()

@ComponentRegistry.register("input")
def forge_input(name: str, props: List[Tuple[str, str]]) -> str:
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';

        export interface {name}Props
          extends React.InputHTMLAttributes<HTMLInputElement> {{}}

        const {name} = React.forwardRef<HTMLInputElement, {name}Props>(
          ({{ className, type, ...props }}, ref) => {{
            return (
              <input
                type={{type}}
                className={{cn(
                  "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                  className
                )}}
                ref={{ref}}
                {{...props}}
              />
            );
          }}
        );
        {name}.displayName = "{name}";

        export {{ {name} }};
    """).strip()

@ComponentRegistry.register("badge")
def forge_badge(name: str, props: List[Tuple[str, str]]) -> str:
    return dedent(f"""
        import React from 'react';
        import {{ cva, type VariantProps }} from 'class-variance-authority';
        import {{ cn }} from '@/lib/utils';

        const badgeVariants = cva(
          "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
          {{
            variants: {{
              variant: {{
                default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
                secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
                destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
                outline: "text-foreground",
              }},
            }},
            defaultVariants: {{
              variant: "default",
            }},
          }}
        );

        export interface {name}Props
          extends React.HTMLAttributes<HTMLDivElement>,
            VariantProps<typeof badgeVariants> {{}}

        function {name}({{ className, variant, ...props }}: {name}Props) {{
          return (
            <div className={{cn(badgeVariants({{ variant }}), className)}} {{...props}} />
          );
        }}

        export {{ {name}, badgeVariants }};
    """).strip()