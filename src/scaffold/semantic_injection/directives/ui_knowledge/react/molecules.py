from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("card")
def forge_card(name: str, props: List[Tuple[str, str]]) -> str:
    # A beautiful, modular Card composition
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';

        const {name} = React.forwardRef<
          HTMLDivElement,
          React.HTMLAttributes<HTMLDivElement>
        >(({{ className, ...props }}, ref) => (
          <div
            ref={{ref}}
            className={{cn(
              "rounded-lg border bg-card text-card-foreground shadow-sm",
              className
            )}}
            {{...props}}
          />
        ));
        {name}.displayName = "{name}";

        const {name}Header = React.forwardRef<
          HTMLDivElement,
          React.HTMLAttributes<HTMLDivElement>
        >(({{ className, ...props }}, ref) => (
          <div
            ref={{ref}}
            className={{cn("flex flex-col space-y-1.5 p-6", className)}}
            {{...props}}
          />
        ));
        {name}Header.displayName = "{name}Header";

        const {name}Title = React.forwardRef<
          HTMLParagraphElement,
          React.HTMLAttributes<HTMLHeadingElement>
        >(({{ className, ...props }}, ref) => (
          <h3
            ref={{ref}}
            className={{cn(
              "text-2xl font-semibold leading-none tracking-tight",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Title.displayName = "{name}Title";

        const {name}Content = React.forwardRef<
          HTMLDivElement,
          React.HTMLAttributes<HTMLDivElement>
        >(({{ className, ...props }}, ref) => (
          <div ref={{ref}} className={{cn("p-6 pt-0", className)}} {{...props}} />
        ));
        {name}Content.displayName = "{name}Content";

        const {name}Footer = React.forwardRef<
          HTMLDivElement,
          React.HTMLAttributes<HTMLDivElement>
        >(({{ className, ...props }}, ref) => (
          <div
            ref={{ref}}
            className={{cn("flex items-center p-6 pt-0", className)}}
            {{...props}}
          />
        ));
        {name}Footer.displayName = "{name}Footer";

        export {{ {name}, {name}Header, {name}Title, {name}Content, {name}Footer }};
    """).strip()

@ComponentRegistry.register("alert")
def forge_alert(name: str, props: List[Tuple[str, str]]) -> str:
    return dedent(f"""
        import React from 'react';
        import {{ cva, type VariantProps }} from 'class-variance-authority';
        import {{ cn }} from '@/lib/utils';
        import {{ AlertCircle, CheckCircle2 }} from 'lucide-react';

        const alertVariants = cva(
          "relative w-full rounded-lg border px-4 py-3 text-sm [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground",
          {{
            variants: {{
              variant: {{
                default: "bg-background text-foreground",
                destructive:
                  "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
                success: "border-green-500/50 text-green-600 dark:border-green-500 [&>svg]:text-green-600",
              }},
            }},
            defaultVariants: {{
              variant: "default",
            }},
          }}
        );

        const {name} = React.forwardRef<
          HTMLDivElement,
          React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
        >(({{ className, variant, children, ...props }}, ref) => (
          <div
            ref={{ref}}
            role="alert"
            className={{cn(alertVariants({{ variant }}), className)}}
            {{...props}}
          >
            {{variant === 'destructive' && <AlertCircle className="h-4 w-4" />}}
            {{variant === 'success' && <CheckCircle2 className="h-4 w-4" />}}
            {{children}}
          </div>
        ));
        {name}.displayName = "{name}";

        const {name}Title = React.forwardRef<
          HTMLParagraphElement,
          React.HTMLAttributes<HTMLHeadingElement>
        >(({{ className, ...props }}, ref) => (
          <h5
            ref={{ref}}
            className={{cn("mb-1 font-medium leading-none tracking-tight", className)}}
            {{...props}}
          />
        ));
        {name}Title.displayName = "{name}Title";

        const {name}Description = React.forwardRef<
          HTMLParagraphElement,
          React.HTMLAttributes<HTMLParagraphElement>
        >(({{ className, ...props }}, ref) => (
          <div
            ref={{ref}}
            className={{cn("text-sm [&_p]:leading-relaxed", className)}}
            {{...props}}
          />
        ));
        {name}Description.displayName = "{name}Description";

        export {{ {name}, {name}Title, {name}Description }};
    """).strip()