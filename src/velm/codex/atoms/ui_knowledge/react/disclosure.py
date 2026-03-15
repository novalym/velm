# scaffold/semantic_injection/directives/ui_knowledge/disclosure.py

"""
=================================================================================
== THE CODEX OF DISCLOSURE (V-Ω-ACCORDION)                                     ==
=================================================================================
This artisan provides components for managing content density and revealing
information progressively.
Dependencies: @radix-ui/react-accordion, @radix-ui/react-collapsible
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("accordion")
def forge_accordion(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a vertically stacked set of interactive headings that reveal content.
    """
    return dedent(f"""
        import React from 'react';
        import * as AccordionPrimitive from '@radix-ui/react-accordion';
        import {{ ChevronDown }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';

        const {name} = AccordionPrimitive.Root;

        const {name}Item = React.forwardRef<
          React.ElementRef<typeof AccordionPrimitive.Item>,
          React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
        >(({{ className, ...props }}, ref) => (
          <AccordionPrimitive.Item
            ref={{ref}}
            className={{cn("border-b", className)}}
            {{...props}}
          />
        ));
        {name}Item.displayName = "AccordionItem";

        const {name}Trigger = React.forwardRef<
          React.ElementRef<typeof AccordionPrimitive.Trigger>,
          React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
        >(({{ className, children, ...props }}, ref) => (
          <AccordionPrimitive.Header className="flex">
            <AccordionPrimitive.Trigger
              ref={{ref}}
              className={{cn(
                "flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180",
                className
              )}}
              {{...props}}
            >
              {{children}}
              <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
            </AccordionPrimitive.Trigger>
          </AccordionPrimitive.Header>
        ));
        {name}Trigger.displayName = AccordionPrimitive.Trigger.displayName;

        const {name}Content = React.forwardRef<
          React.ElementRef<typeof AccordionPrimitive.Content>,
          React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
        >(({{ className, children, ...props }}, ref) => (
          <AccordionPrimitive.Content
            ref={{ref}}
            className="overflow-hidden text-sm transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
            {{...props}}
          >
            <div className={{cn("pb-4 pt-0", className)}}>{{children}}</div>
          </AccordionPrimitive.Content>
        ));
        {name}Content.displayName = AccordionPrimitive.Content.displayName;

        export {{ {name}, {name}Item, {name}Trigger, {name}Content }};
    """).strip()

@ComponentRegistry.register("collapsible")
def forge_collapsible(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a simple component for expanding/collapsing a panel.
    """
    return dedent(f"""
        import * as CollapsiblePrimitive from '@radix-ui/react-collapsible';

        const {name} = CollapsiblePrimitive.Root;
        const {name}Trigger = CollapsiblePrimitive.CollapsibleTrigger;
        const {name}Content = CollapsiblePrimitive.CollapsibleContent;

        export {{ {name}, {name}Trigger, {name}Content }};
    """).strip()