# scaffold/semantic_injection/directives/ui_knowledge/layouts.py

from textwrap import dedent
from typing import List, Tuple

from .registry import ComponentRegistry
from ....contracts.heresy_contracts import ArtisanHeresy
from ....utils.invocation import invoke_scaffold_command


@ComponentRegistry.register("dashboard-layout")
def forge_dashboard_layout(name: str, props: List[Tuple[str, str]]) -> str:
    """
    =================================================================================
    == THE CITADEL'S FOUNDATION (V-Ω-LAYOUT-KIT)                                   ==
    =================================================================================
    This artisan is a Gnostic Conductor. It does not generate code directly. It
    proclaims a sacred, ephemeral blueprint scripture and then summons the
    God-Engine (`invoke_scaffold_command`) to materialize that scripture within
    the current reality. This is the apotheosis of compositional architecture.
    =================================================================================
    """

    # The Gnostic Blueprint is the artisan's one true soul.
    # It speaks the language of Form to forge a living, interconnected Organism.
    blueprint_scripture = dedent(r"""
# =================================================================
# == EPHEMERAL BLUEPRINT: THE GNOSTIC DASHBOARD CITADEL          ==
# =================================================================

# --- 1. The Gnostic Nervous System (State & Context) ---

src/providers/LayoutProvider.tsx :: '''
'use client';

import React, { createContext, useState, useCallback, useMemo, useContext } from 'react';

interface LayoutContextType {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const LayoutContext = createContext<LayoutContextType | undefined>(undefined);

export function LayoutProvider({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const toggleSidebar = useCallback(() => setIsSidebarOpen(prev => !prev), []);

  const value = useMemo(() => ({ isSidebarOpen, toggleSidebar }), [isSidebarOpen, toggleSidebar]);

  return (
    <LayoutContext.Provider value={value}>
      {children}
    </Layout-Provider>
  );
}
'''

src/hooks/use-layout.ts :: '''
import { useContext } from 'react';
import { LayoutContext } from '@/providers/LayoutProvider';

export function useLayout() {
  const context = useContext(LayoutContext);
  if (context === undefined) {
    throw new Error('useLayout must be used within a LayoutProvider');
  }
  return context;
}
'''

# --- 2. The Citadel's Form (The Core Layout & Its Organs) ---

src/layouts/DashboardLayout.tsx :: '''
'use client';

import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { LayoutProvider } from '@/providers/LayoutProvider';
import { useLayout } from '@/hooks/use-layout';
import { cn } from '@/lib/utils';

function DashboardShell() {
  const { isSidebarOpen, toggleSidebar } = useLayout();

  return (
    <div className="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
      <div className={cn("hidden border-r bg-muted/40 md:block", !isSidebarOpen && "md:hidden")}>
        <Sidebar />
      </div>
      <div className="flex flex-col">
        <Header onMenuClick={toggleSidebar} />
        <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6 bg-background">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default function DashboardLayout() {
  return (
    <LayoutProvider>
      <DashboardShell />
    </LayoutProvider>
  );
}
'''

src/components/layout/Header.tsx :: '''
import { Menu, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { UserNav } from '@/components/layout/UserNav';

export function Header({ onMenuClick }: { onMenuClick: () => void }) {
  return (
    <header className="flex h-14 items-center gap-4 border-b bg-muted/40 px-4 lg:h-[60px] lg:px-6">
      <Button variant="outline" size="icon" className="h-8 w-8 shrink-0 md:hidden" onClick={onMenuClick}>
        <Menu className="h-5 w-5" />
        <span className="sr-only">Toggle navigation menu</span>
      </Button>
      <div className="w-full flex-1">
        <form>
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search the cosmos..."
              className="w-full appearance-none bg-background pl-8 shadow-none md:w-2/3 lg:w-1/3"
            />
          </div>
        </form>
      </div>
      <UserNav />
    </header>
  );
}
'''

src/components/layout/Sidebar.tsx :: '''
import { NavLink } from 'react-router-dom';
import { Home, Package, ShoppingCart, Users, LineChart } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

const navLinks = [
  { to: '/dashboard', icon: Home, label: 'Dashboard' },
  { to: '/orders', icon: ShoppingCart, label: 'Orders', badge: '6' },
  { to: '/products', icon: Package, label: 'Products' },
  { to: '/customers', icon: Users, label: 'Customers' },
  { to: '/analytics', icon: LineChart, label: 'Analytics' },
];

export function Sidebar() {
  return (
    <div className="flex h-full max-h-screen flex-col gap-2">
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <span className="flex items-center gap-2 font-semibold">
          <Package className="h-6 w-6 text-primary" />
          <span>Gnostic Inc</span>
        </span>
      </div>
      <div className="flex-1">
        <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary",
                isActive && "bg-muted text-primary"
              )}
            >
              <link.icon className="h-4 w-4" />
              {link.label}
              {link.badge && <Badge className="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full">{link.badge}</Badge>}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="mt-auto p-4">
        <Card>
          <CardHeader className="p-2 pt-0 md:p-4">
            <CardTitle>Upgrade to Pro</CardTitle>
            <CardDescription>Unlock all Gnostic features and get unlimited access to our support team.</CardDescription>
          </CardHeader>
          <CardContent className="p-2 pt-0 md:p-4 md:pt-0">
            <Button size="sm" className="w-full">Upgrade</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
'''

# --- 3. The Organs' Organs (The Atoms Summoned by the Layout) ---
# We summon these to ensure the layout is born complete and without heresy.

src/components/layout/UserNav.tsx :: @ui/component(name="UserNav")
src/components/ui/badge.tsx :: @ui/component(name="Badge")
src/components/ui/button.tsx :: @ui/component(name="Button")
src/components/ui/card.tsx :: @ui/component(name="Card")
src/components/ui/input.tsx :: @ui/component(name="Input")
src/components/ui/dropdown-menu.tsx :: @ui/component(name="DropdownMenu")
src/components/ui/avatar.tsx :: @ui/component(name="Avatar")
src/lib/utils.ts :: @ui/utils

    """)

    # --- The Rite of Gnostic Invocation ---
    # The artisan summons the God-Engine to make its own, internal will manifest.
    # This is a divine, recursive act of self-creation.
    try:
        # We use the raw, internal `invoke_scaffold_command` for a pure,
        # in-process symphony, bypassing the profane shell.
        result = invoke_scaffold_command(
            command_args=["-"],  # The "-" sigil commands the engine to read from stdin
            stdin_content=blueprint_scripture,
            non_interactive=True  # The child rite must be silent
        )

        if result.exit_code != 0:
            # A heresy in our own scripture is a catastrophic paradox.
            raise ArtisanHeresy(
                "A catastrophic paradox occurred while materializing the DashboardLayout kit.",
                details=result.output
            )

        # The Conductor's Vow: It must return a string.
        # We proclaim the path to the main layout file as a sacred comment,
        # a luminous guide for the Architect's Gaze.
        return "// Gnostic Layout Kit materialized successfully. See 'src/layouts/DashboardLayout.tsx'."

    except Exception as e:
        # The Unbreakable Ward of Grace
        raise ArtisanHeresy("A catastrophic, unhandled paradox shattered the Layout Conductor.", child_heresy=e)