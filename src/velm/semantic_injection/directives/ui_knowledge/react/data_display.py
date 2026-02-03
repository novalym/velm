# scaffold/semantic_injection/directives/ui_knowledge/data_display.py

"""
=================================================================================
== THE LEDGER OF TRUTH (V-Ω-DATA-DISPLAY)                                      ==
=================================================================================
This artisan provides the primitives for dense information display.
It generates a composable Table API compatible with TanStack Table.
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("table")
def forge_table(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a beautiful, responsive Table component suite.
    Includes: Table, Header, Body, Row, Head, Cell, Caption.
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';

        const {name} = React.forwardRef<
          HTMLTableElement,
          React.HTMLAttributes<HTMLTableElement>
        >(({{ className, ...props }}, ref) => (
          <div className="relative w-full overflow-auto">
            <table
              ref={{ref}}
              className={{cn("w-full caption-bottom text-sm", className)}}
              {{...props}}
            />
          </div>
        ));
        {name}.displayName = "{name}";

        const {name}Header = React.forwardRef<
          HTMLTableSectionElement,
          React.HTMLAttributes<HTMLTableSectionElement>
        >(({{ className, ...props }}, ref) => (
          <thead ref={{ref}} className={{cn("[&_tr]:border-b", className)}} {{...props}} />
        ));
        {name}Header.displayName = "{name}Header";

        const {name}Body = React.forwardRef<
          HTMLTableSectionElement,
          React.HTMLAttributes<HTMLTableSectionElement>
        >(({{ className, ...props }}, ref) => (
          <tbody
            ref={{ref}}
            className={{cn("[&_tr:last-child]:border-0", className)}}
            {{...props}}
          />
        ));
        {name}Body.displayName = "{name}Body";

        const {name}Footer = React.forwardRef<
          HTMLTableSectionElement,
          React.HTMLAttributes<HTMLTableSectionElement>
        >(({{ className, ...props }}, ref) => (
          <tfoot
            ref={{ref}}
            className={{cn(
              "border-t bg-muted/50 font-medium [&>tr]:last:border-b-0",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Footer.displayName = "{name}Footer";

        const {name}Row = React.forwardRef<
          HTMLTableRowElement,
          React.HTMLAttributes<HTMLTableRowElement>
        >(({{ className, ...props }}, ref) => (
          <tr
            ref={{ref}}
            className={{cn(
              "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Row.displayName = "{name}Row";

        const {name}Head = React.forwardRef<
          HTMLTableCellElement,
          React.ThHTMLAttributes<HTMLTableCellElement>
        >(({{ className, ...props }}, ref) => (
          <th
            ref={{ref}}
            className={{cn(
              "h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0",
              className
            )}}
            {{...props}}
          />
        ));
        {name}Head.displayName = "{name}Head";

        const {name}Cell = React.forwardRef<
          HTMLTableCellElement,
          React.TdHTMLAttributes<HTMLTableCellElement>
        >(({{ className, ...props }}, ref) => (
          <td
            ref={{ref}}
            className={{cn("p-4 align-middle [&:has([role=checkbox])]:pr-0", className)}}
            {{...props}}
          />
        ));
        {name}Cell.displayName = "{name}Cell";

        const {name}Caption = React.forwardRef<
          HTMLTableCaptionElement,
          React.HTMLAttributes<HTMLTableCaptionElement>
        >(({{ className, ...props }}, ref) => (
          <caption
            ref={{ref}}
            className={{cn("mt-4 text-sm text-muted-foreground", className)}}
            {{...props}}
          />
        ));
        {name}Caption.displayName = "{name}Caption";

        export {{
          {name},
          {name}Header,
          {name}Body,
          {name}Footer,
          {name}Head,
          {name}Row,
          {name}Cell,
          {name}Caption,
        }};
    """).strip()