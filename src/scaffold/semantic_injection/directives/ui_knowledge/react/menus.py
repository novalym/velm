# scaffold/semantic_injection/directives/ui_knowledge/menus.py

"""
=================================================================================
== THE CODEX OF ACTIONS (V-Ω-MENUS)                                            ==
=================================================================================
This artisan provides complex menu systems for high-density interaction.
Dependencies: @radix-ui/react-dropdown-menu, @radix-ui/react-menubar
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("dropdown-menu")
def forge_dropdown_menu(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Dropdown Menu suite (Root, Trigger, Content, Item, Label, Separator).
    """
    return dedent(f"""
        import React from 'react';
        import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
        import {{ Check, ChevronRight, Circle }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';

        const {name} = DropdownMenuPrimitive.Root;
        const {name}Trigger = DropdownMenuPrimitive.Trigger;
        const {name}Group = DropdownMenuPrimitive.Group;
        const {name}Portal = DropdownMenuPrimitive.Portal;
        const {name}Sub = DropdownMenuPrimitive.Sub;
        const {name}RadioGroup = DropdownMenuPrimitive.RadioGroup;

        const {name}Content = React.forwardRef<
          React.ElementRef<typeof DropdownMenuPrimitive.Content>,
          React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
        >(({{ className, sideOffset = 4, ...props }}, ref) => (
          <DropdownMenuPrimitive.Portal>
            <DropdownMenuPrimitive.Content
              ref={{ref}}
              sideOffset={{sideOffset}}
              className={{cn(
                "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
                className
              )}}
              {{...props}}
            />
          </DropdownMenuPrimitive.Portal>
        ));
        {name}Content.displayName = DropdownMenuPrimitive.Content.displayName;

        const {name}Item = React.forwardRef<
          React.ElementRef<typeof DropdownMenuPrimitive.Item>,
          React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item> & {{
            inset?: boolean;
          }}
        >(({{ className, inset, ...props }}, ref) => (
          <DropdownMenuPrimitive.Item
            ref={{ref}}
            className={{cn(
              "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
              inset && "pl-8",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Item.displayName = DropdownMenuPrimitive.Item.displayName;

        const {name}Label = React.forwardRef<
          React.ElementRef<typeof DropdownMenuPrimitive.Label>,
          React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Label> & {{
            inset?: boolean;
          }}
        >(({{ className, inset, ...props }}, ref) => (
          <DropdownMenuPrimitive.Label
            ref={{ref}}
            className={{cn(
              "px-2 py-1.5 text-sm font-semibold",
              inset && "pl-8",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Label.displayName = DropdownMenuPrimitive.Label.displayName;

        const {name}Separator = React.forwardRef<
          React.ElementRef<typeof DropdownMenuPrimitive.Separator>,
          React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Separator>
        >(({{ className, ...props }}, ref) => (
          <DropdownMenuPrimitive.Separator
            ref={{ref}}
            className={{cn("-mx-1 my-1 h-px bg-muted", className)}}
            {{...props}}
          />
        ));
        {name}Separator.displayName = DropdownMenuPrimitive.Separator.displayName;

        export {{
          {name},
          {name}Trigger,
          {name}Content,
          {name}Item,
          {name}Label,
          {name}Separator,
          {name}Group,
          {name}Portal,
          {name}Sub,
          {name}RadioGroup,
        }};
    """).strip()

@ComponentRegistry.register("menubar")
def forge_menubar(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a desktop-style Menubar.
    """
    return dedent(f"""
        import React from 'react';
        import * as MenubarPrimitive from '@radix-ui/react-menubar';
        import {{ Check, ChevronRight, Circle }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';

        const {name} = React.forwardRef<
          React.ElementRef<typeof MenubarPrimitive.Root>,
          React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Root>
        >(({{ className, ...props }}, ref) => (
          <MenubarPrimitive.Root
            ref={{ref}}
            className={{cn(
              "flex h-10 items-center space-x-1 rounded-md border bg-background p-1",
              className
            )}}
            {{...props}}
          />
        ));
        {name}.displayName = MenubarPrimitive.Root.displayName;

        const {name}Menu = MenubarPrimitive.Menu;
        const {name}Group = MenubarPrimitive.Group;
        const {name}Portal = MenubarPrimitive.Portal;
        const {name}Sub = MenubarPrimitive.Sub;
        const {name}RadioGroup = MenubarPrimitive.RadioGroup;

        const {name}Trigger = React.forwardRef<
          React.ElementRef<typeof MenubarPrimitive.Trigger>,
          React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Trigger>
        >(({{ className, ...props }}, ref) => (
          <MenubarPrimitive.Trigger
            ref={{ref}}
            className={{cn(
              "flex cursor-default select-none items-center rounded-sm px-3 py-1.5 text-sm font-medium outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Trigger.displayName = MenubarPrimitive.Trigger.displayName;

        const {name}Content = React.forwardRef<
          React.ElementRef<typeof MenubarPrimitive.Content>,
          React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Content>
        >(({{ className, align = "start", alignOffset = -4, sideOffset = 8, ...props }}, ref) => (
          <MenubarPrimitive.Portal>
            <MenubarPrimitive.Content
              ref={{ref}}
              align={{align}}
              alignOffset={{alignOffset}}
              sideOffset={{sideOffset}}
              className={{cn(
                "z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
                className
              )}}
              {{...props}}
            />
          </MenubarPrimitive.Portal>
        ));
        {name}Content.displayName = MenubarPrimitive.Content.displayName;

        const {name}Item = React.forwardRef<
          React.ElementRef<typeof MenubarPrimitive.Item>,
          React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Item> & {{
            inset?: boolean;
          }}
        >(({{ className, inset, ...props }}, ref) => (
          <MenubarPrimitive.Item
            ref={{ref}}
            className={{cn(
              "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
              inset && "pl-8",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Item.displayName = MenubarPrimitive.Item.displayName;

        const {name}Separator = React.forwardRef<
          React.ElementRef<typeof MenubarPrimitive.Separator>,
          React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Separator>
        >(({{ className, ...props }}, ref) => (
          <MenubarPrimitive.Separator
            ref={{ref}}
            className={{cn("-mx-1 my-1 h-px bg-muted", className)}}
            {{...props}}
          />
        ));
        {name}Separator.displayName = MenubarPrimitive.Separator.displayName;

        export {{
          {name},
          {name}Menu,
          {name}Trigger,
          {name}Content,
          {name}Item,
          {name}Separator,
          {name}Group,
          {name}Portal,
          {name}Sub,
          {name}RadioGroup,
        }};
    """).strip()