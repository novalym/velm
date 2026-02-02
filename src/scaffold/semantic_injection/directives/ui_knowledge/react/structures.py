# scaffold/semantic_injection/directives/ui_knowledge/structures.py

"""
=================================================================================
== THE FORGE OF STRUCTURES (ORGANISMS)                                         ==
=================================================================================
LIF: 50,000,000,000

This sanctum contains the generators for high-level UI organisms.
These are complex, often stateful components that compose Atoms and Molecules
into distinct sections of an interface.

Registry:
  - navbar: Responsive navigation with mobile menu.
  - sidebar: Dashboard navigation with collapsible states.
  - footer: Multi-column footer layout.
  - hero: High-impact landing page section.
  - auth-form: Production-ready login/signup form skeleton.
  - data-table: A foundation for dense data display.
=================================================================================
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("navbar")
def forge_navbar(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a responsive Navigation Bar with a mobile toggle state.
    """
    return dedent(f"""
        import React, {{ useState }} from 'react';
        import {{ Menu, X, Mountain }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';
        import {{ Button }} from '@/components/ui/button'; // Assumes Atom existence

        interface NavLink {{
          label: string;
          href: string;
          active?: boolean;
        }}

        export interface {name}Props extends React.HTMLAttributes<HTMLElement> {{
          logoText?: string;
          links?: NavLink[];
        }}

        export function {name}({{ 
          className, 
          logoText = "Acme Inc", 
          links = [
            {{ label: 'Home', href: '/' }},
            {{ label: 'Features', href: '/features' }},
            {{ label: 'Pricing', href: '/pricing' }},
            {{ label: 'About', href: '/about' }},
          ],
          ...props 
        }}: {name}Props) {{
          const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

          const toggleMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

          return (
            <nav className={{cn("border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60", className)}} {{...props}}>
              <div className="container mx-auto px-4 md:px-6">
                <div className="flex h-16 items-center justify-between">

                  {{/* Logo Area */}}
                  <div className="flex items-center gap-2">
                    <Mountain className="h-6 w-6" />
                    <span className="text-lg font-bold tracking-tight">{{logoText}}</span>
                  </div>

                  {{/* Desktop Navigation */}}
                  <div className="hidden md:flex gap-6">
                    {{links.map((link) => (
                      <a
                        key={{link.href}}
                        href={{link.href}}
                        className={{cn(
                          "text-sm font-medium transition-colors hover:text-primary",
                          link.active ? "text-primary" : "text-muted-foreground"
                        )}}
                      >
                        {{link.label}}
                      </a>
                    ))}}
                  </div>

                  {{/* Desktop Actions */}}
                  <div className="hidden md:flex items-center gap-4">
                    <Button variant="ghost" size="sm">Log in</Button>
                    <Button size="sm">Get Started</Button>
                  </div>

                  {{/* Mobile Menu Toggle */}}
                  <div className="md:hidden">
                    <Button variant="ghost" size="icon" onClick={{toggleMenu}} aria-label="Toggle menu">
                      {{isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}}
                    </Button>
                  </div>
                </div>
              </div>

              {{/* Mobile Menu Overlay */}}
              {{isMobileMenuOpen && (
                <div className="md:hidden border-t p-4 space-y-4 bg-background">
                  <div className="flex flex-col space-y-3">
                    {{links.map((link) => (
                      <a
                        key={{link.href}}
                        href={{link.href}}
                        className="text-sm font-medium text-muted-foreground hover:text-primary"
                        onClick={{() => setIsMobileMenuOpen(false)}}
                      >
                        {{link.label}}
                      </a>
                    ))}}
                  </div>
                  <div className="flex flex-col gap-2 pt-4 border-t">
                    <Button variant="outline" className="w-full justify-start">Log in</Button>
                    <Button className="w-full justify-start">Get Started</Button>
                  </div>
                </div>
              )}}
            </nav>
          );
        }}
    """).strip()


@ComponentRegistry.register("sidebar")
def forge_sidebar(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a vertical Sidebar layout often used in dashboards.
    """
    return dedent(f"""
        import React from 'react';
        import {{ LayoutDashboard, Settings, Users, BarChart3, LogOut }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';
        import {{ Button }} from '@/components/ui/button';

        interface SidebarItem {{
          icon: React.ElementType;
          label: string;
          href: string;
          active?: boolean;
        }}

        export interface {name}Props extends React.HTMLAttributes<HTMLElement> {{
          items?: SidebarItem[];
        }}

        export function {name}({{ className, items, ...props }}: {name}Props) {{
          const defaultItems: SidebarItem[] = [
            {{ icon: LayoutDashboard, label: "Dashboard", href: "/dashboard", active: true }},
            {{ icon: Users, label: "Team", href: "/team" }},
            {{ icon: BarChart3, label: "Analytics", href: "/analytics" }},
            {{ icon: Settings, label: "Settings", href: "/settings" }},
          ];

          const navItems = items || defaultItems;

          return (
            <div className={{cn("flex h-full w-64 flex-col border-r bg-card text-card-foreground", className)}} {{...props}}>
              <div className="p-6">
                <h2 className="text-2xl font-bold tracking-tight">Nexus</h2>
              </div>

              <div className="flex-1 overflow-auto py-2">
                <nav className="grid items-start px-4 text-sm font-medium">
                  {{navItems.map((item, index) => (
                    <a
                      key={{index}}
                      href={{item.href}}
                      className={{cn(
                        "flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary",
                        item.active 
                          ? "bg-secondary text-primary" 
                          : "text-muted-foreground hover:bg-secondary/50"
                      )}}
                    >
                      <item.icon className="h-4 w-4" />
                      {{item.label}}
                    </a>
                  ))}}
                </nav>
              </div>

              <div className="mt-auto p-4 border-t">
                <Button variant="ghost" className="w-full justify-start gap-2 text-muted-foreground">
                  <LogOut className="h-4 w-4" />
                  Sign Out
                </Button>
              </div>
            </div>
          );
        }}
    """).strip()


@ComponentRegistry.register("hero")
def forge_hero(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a high-impact Hero section.
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';
        import {{ Button }} from '@/components/ui/button';
        import {{ Badge }} from '@/components/ui/badge'; // Assumes Badge atom existence

        export interface {name}Props extends React.HTMLAttributes<HTMLElement> {{
          title?: string;
          subtitle?: string;
          badgeText?: string;
        }}

        export function {name}({{ 
          className, 
          title = "Build Faster with Gnosis", 
          subtitle = "The ultimate architectural engine for modern artisans. Manifest reality at the speed of thought.",
          badgeText = "v1.0 Released",
          ...props 
        }}: {name}Props) {{
          return (
            <section className={{cn("relative overflow-hidden py-20 md:py-32", className)}} {{...props}}>
              <div className="container relative z-10 mx-auto px-4 text-center">

                <div className="mb-6 animate-fade-in-up">
                  <Badge variant="secondary" className="px-4 py-1 text-sm">
                    {{badgeText}}
                  </Badge>
                </div>

                <h1 className="mb-6 text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
                  <span className="block bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                    {{title}}
                  </span>
                </h1>

                <p className="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground sm:text-xl">
                  {{subtitle}}
                </p>

                <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
                  <Button size="lg" className="min-w-[160px]">
                    Get Started
                  </Button>
                  <Button size="lg" variant="outline" className="min-w-[160px]">
                    Documentation
                  </Button>
                </div>
              </div>

              {{/* Background decoration */}}
              <div className="absolute top-1/2 left-1/2 -z-10 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 opacity-10 bg-gradient-to-tr from-primary to-purple-500 blur-[100px]" />
            </section>
          );
        }}
    """).strip()


@ComponentRegistry.register("auth-form")
def forge_auth_form(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Login/Signup form with loading states and validation structures.
    """
    return dedent(f"""
        import React, {{ useState }} from 'react';
        import {{ Loader2 }} from 'lucide-react';
        import {{ cn }} from '@/lib/utils';
        import {{ Button }} from '@/components/ui/button';
        import {{ Input }} from '@/components/ui/input';
        import {{ Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle }} from '@/components/ui/card';

        export interface {name}Props extends React.HTMLAttributes<HTMLDivElement> {{
          type?: 'login' | 'signup';
        }}

        export function {name}({{ className, type = 'login', ...props }}: {name}Props) {{
          const [isLoading, setIsLoading] = useState(false);

          const isLogin = type === 'login';

          async function onSubmit(event: React.FormEvent<HTMLFormElement>) {{
            event.preventDefault();
            setIsLoading(true);

            setTimeout(() => {{
              setIsLoading(false);
              // Gnostic TODO: Integrate auth provider here
            }}, 2000);
          }}

          return (
            <div className={{cn("flex justify-center items-center p-4", className)}} {{...props}}>
              <Card className="w-full max-w-sm">
                <CardHeader className="space-y-1">
                  <CardTitle className="text-2xl">
                    {{isLogin ? 'Welcome back' : 'Create an account'}}
                  </CardTitle>
                  <CardDescription>
                    Enter your email below to {{isLogin ? 'sign in to' : 'create'}} your account
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={{onSubmit}} className="space-y-4">
                    <div className="space-y-2">
                      <label htmlFor="email" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                        Email
                      </label>
                      <Input 
                        id="email" 
                        placeholder="m@example.com" 
                        required 
                        type="email" 
                        autoCapitalize="none" 
                        autoComplete="email" 
                        autoCorrect="off"
                        disabled={{isLoading}}
                      />
                    </div>
                    <div className="space-y-2">
                      <label htmlFor="password" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                        Password
                      </label>
                      <Input 
                        id="password" 
                        required 
                        type="password" 
                        disabled={{isLoading}}
                      />
                    </div>
                    <Button className="w-full" type="submit" disabled={{isLoading}}>
                      {{isLoading && (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      )}}
                      {{isLogin ? 'Sign In' : 'Create Account'}}
                    </Button>
                  </form>
                </CardContent>
                <CardFooter>
                  <div className="text-sm text-muted-foreground text-center w-full">
                    {{isLogin ? "Don't have an account? " : "Already have an account? "}}
                    <a href="#" className="underline underline-offset-4 hover:text-primary">
                      {{isLogin ? 'Sign Up' : 'Log In'}}
                    </a>
                  </div>
                </CardFooter>
              </Card>
            </div>
          );
        }}
    """).strip()


@ComponentRegistry.register("footer")
def forge_footer(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a professional Footer with columns.
    """
    return dedent(f"""
        import React from 'react';
        import {{ cn }} from '@/lib/utils';
        import {{ Mountain }} from 'lucide-react';

        export interface {name}Props extends React.HTMLAttributes<HTMLElement> {{}}

        export function {name}({{ className, ...props }}: {name}Props) {{
          return (
            <footer className={{cn("bg-background border-t py-12 md:py-16", className)}} {{...props}}>
              <div className="container mx-auto px-4 md:px-6">
                <div className="grid grid-cols-2 gap-8 md:grid-cols-4 lg:grid-cols-5">

                  <div className="col-span-2 lg:col-span-2">
                    <div className="flex items-center gap-2 mb-4">
                      <Mountain className="h-6 w-6" />
                      <span className="text-lg font-bold">Acme Inc</span>
                    </div>
                    <p className="text-sm text-muted-foreground max-w-xs">
                      Forging the future of digital realities with Gnostic intelligence and unbreakable code.
                    </p>
                  </div>

                  <div className="space-y-3">
                    <h4 className="text-sm font-medium">Product</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li><a href="#" className="hover:text-foreground transition-colors">Features</a></li>
                      <li><a href="#" className="hover:text-foreground transition-colors">Pricing</a></li>
                      <li><a href="#" className="hover:text-foreground transition-colors">Enterprise</a></li>
                    </ul>
                  </div>

                  <div className="space-y-3">
                    <h4 className="text-sm font-medium">Company</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li><a href="#" className="hover:text-foreground transition-colors">About</a></li>
                      <li><a href="#" className="hover:text-foreground transition-colors">Blog</a></li>
                      <li><a href="#" className="hover:text-foreground transition-colors">Careers</a></li>
                    </ul>
                  </div>

                  <div className="space-y-3">
                    <h4 className="text-sm font-medium">Legal</h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li><a href="#" className="hover:text-foreground transition-colors">Privacy</a></li>
                      <li><a href="#" className="hover:text-foreground transition-colors">Terms</a></li>
                    </ul>
                  </div>

                </div>

                <div className="mt-12 border-t pt-8 text-center text-sm text-muted-foreground">
                  © {{new Date().getFullYear()}} Acme Inc. All rights reserved.
                </div>
              </div>
            </footer>
          );
        }}
    """).strip()