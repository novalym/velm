# scaffold/semantic_injection/directives/ui_knowledge/overlays.py

"""
=================================================================================
== THE PORTALS OF FOCUS (V-Ω-OVERLAYS)                                         ==
=================================================================================
This artisan generates complex overlay structures.
It leverages @radix-ui/react-dialog for accessible, robust interaction.
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("dialog")
def forge_dialog(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Dialog (Modal) component suite (Root, Trigger, Content, Header, Footer).
    """
    return dedent(f"""
        import React from 'react';
        import * as DialogPrimitive from '@radix-ui/react-dialog';
        import {{ X }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';

        const {name} = DialogPrimitive.Root;
        const {name}Trigger = DialogPrimitive.Trigger;

        const {name}Portal = ({{ className, ...props }}: DialogPrimitive.DialogPortalProps) => (
          <DialogPrimitive.Portal className={{cn(className)}} {{...props}} />
        );
        {name}Portal.displayName = DialogPrimitive.Portal.displayName;

        const {name}Overlay = React.forwardRef<
          React.ElementRef<typeof DialogPrimitive.Overlay>,
          React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
        >(({{ className, ...props }}, ref) => (
          <DialogPrimitive.Overlay
            ref={{ref}}
            className={{cn(
              "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Overlay.displayName = DialogPrimitive.Overlay.displayName;

        const {name}Content = React.forwardRef<
          React.ElementRef<typeof DialogPrimitive.Content>,
          React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
        >(({{ className, children, ...props }}, ref) => (
          <{name}Portal>
            <{name}Overlay />
            <DialogPrimitive.Content
              ref={{ref}}
              className={{cn(
                "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
                className
              )}}
              {{...props}}
            >
              {{children}}
              <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
                <X className="h-4 w-4" />
                <span className="sr-only">Close</span>
              </DialogPrimitive.Close>
            </DialogPrimitive.Content>
          </{name}Portal>
        ));
        {name}Content.displayName = DialogPrimitive.Content.displayName;

        const {name}Header = ({{
          className,
          ...props
        }}: React.HTMLAttributes<HTMLDivElement>) => (
          <div
            className={{cn(
              "flex flex-col space-y-1.5 text-center sm:text-left",
              className
            )}}
            {{...props}}
          />
        );
        {name}Header.displayName = "DialogHeader";

        const {name}Title = React.forwardRef<
          React.ElementRef<typeof DialogPrimitive.Title>,
          React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
        >(({{ className, ...props }}, ref) => (
          <DialogPrimitive.Title
            ref={{ref}}
            className={{cn("text-lg font-semibold leading-none tracking-tight", className)}}
            {{...props}}
          />
        ));
        {name}Title.displayName = DialogPrimitive.Title.displayName;

        export {{
          {name},
          {name}Trigger,
          {name}Content,
          {name}Header,
          {name}Title,
        }};
    """).strip()