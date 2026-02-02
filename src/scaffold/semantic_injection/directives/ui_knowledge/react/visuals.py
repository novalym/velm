# scaffold/semantic_injection/directives/ui_knowledge/visuals.py

"""
=================================================================================
== THE CODEX OF IDENTITY & STATUS (V-Ω-VISUALS)                                ==
=================================================================================
This artisan provides visual representations of users and system state.
Dependencies: @radix-ui/react-avatar, @radix-ui/react-progress
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("avatar")
def forge_avatar(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges an image element with a fallback for representing the user.
    """
    return dedent(f"""
        import React from 'react';
        import * as AvatarPrimitive from '@radix-ui/react-avatar';
        import {{ cn }} from '@/lib/utils';

        const {name} = React.forwardRef<
          React.ElementRef<typeof AvatarPrimitive.Root>,
          React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
        >(({{ className, ...props }}, ref) => (
          <AvatarPrimitive.Root
            ref={{ref}}
            className={{cn(
              "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full",
              className
            )}}
            {{...props}}
          />
        ));
        {name}.displayName = AvatarPrimitive.Root.displayName;

        const {name}Image = React.forwardRef<
          React.ElementRef<typeof AvatarPrimitive.Image>,
          React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
        >(({{ className, ...props }}, ref) => (
          <AvatarPrimitive.Image
            ref={{ref}}
            className={{cn("aspect-square h-full w-full", className)}}
            {{...props}}
          />
        ));
        {name}Image.displayName = AvatarPrimitive.Image.displayName;

        const {name}Fallback = React.forwardRef<
          React.ElementRef<typeof AvatarPrimitive.Fallback>,
          React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
        >(({{ className, ...props }}, ref) => (
          <AvatarPrimitive.Fallback
            ref={{ref}}
            className={{cn(
              "flex h-full w-full items-center justify-center rounded-full bg-muted",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Fallback.displayName = AvatarPrimitive.Fallback.displayName;

        export {{ {name}, {name}Image, {name}Fallback }};
    """).strip()

@ComponentRegistry.register("progress")
def forge_progress(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a progress bar indicator.
    """
    return dedent(f"""
        import React from 'react';
        import * as ProgressPrimitive from '@radix-ui/react-progress';
        import {{ cn }} from '@/lib/utils';

        const {name} = React.forwardRef<
          React.ElementRef<typeof ProgressPrimitive.Root>,
          React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>
        >(({{ className, value, ...props }}, ref) => (
          <ProgressPrimitive.Root
            ref={{ref}}
            className={{cn(
              "relative h-4 w-full overflow-hidden rounded-full bg-secondary",
              className
            )}}
            {{...props}}
          >
            <ProgressPrimitive.Indicator
              className="h-full w-full flex-1 bg-primary transition-all"
              style={{{{ transform: `translateX(-${{100 - (value || 0)}}%)` }}}}
            />
          </ProgressPrimitive.Root>
        ));
        {name}.displayName = ProgressPrimitive.Root.displayName;

        export {{ {name} }};
    """).strip()