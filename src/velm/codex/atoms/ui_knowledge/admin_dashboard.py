# scaffold/semantic_injection/directives/ui_knowledge/admin_dashboard.py

from textwrap import dedent
from typing import List, Tuple

from .registry import ComponentRegistry
from ....contracts.heresy_contracts import ArtisanHeresy
from ....utils.invocation import invoke_scaffold_command


@ComponentRegistry.register("admin-dashboard-kit")
def forge_admin_dashboard_kit(name: str, props: List[Tuple[str, str]]) -> str:
    """
    =================================================================================
    == THE GNOSTIC ADMIN CITADEL (V-Ω-KIT-CONDUCTOR)                               ==
    =================================================================================
    This is not a component; it is a Gnostic Kit Conductor. It proclaims a sacred,
    ephemeral blueprint scripture containing the complete, multi-file reality for a
    production-grade Admin Dashboard, and then summons the God-Engine to make it
    manifest in a single, atomic act of symbiotic creation.
    =================================================================================
    """
    # The Gnostic Blueprint is the artisan's one true soul.
    # It speaks the language of Form to forge a living, interconnected Organism.
    # We use raw strings (r"...") to prevent Python from misinterpreting backslashes.
    blueprint_scripture = dedent(r"""
# =================================================================
# == EPHEMERAL BLUEPRINT: GNOSTIC ADMIN DASHBOARD                ==
# =================================================================
# @description: A complete, responsive React/Tailwind Admin System.

$$ app_name = "nexus-dashboard"

# --- 1. THE CORE INFRASTRUCTURE (Providers & Routing) ---

src/providers/AuthProvider.tsx :: @ui/component(name="AuthProvider", prompt="A React Context provider for mock authentication state")
src/providers/ThemeProvider.tsx :: @ui/component(name="ThemeProvider", prompt="A React Context provider for light/dark theme toggling")

src/App.tsx :: '''
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@/providers/AuthProvider';
import { ThemeProvider } from '@/providers/ThemeProvider';
import DashboardLayout from '@/layouts/DashboardLayout';
import AuthGuard from '@/components/auth/AuthGuard';
import DashboardPage from '@/pages/DashboardPage';
import UsersPage from '@/pages/UsersPage';
import SettingsPage from '@/pages/SettingsPage';
import LoginPage from '@/pages/LoginPage';

export default function App() {
  return (
    <BrowserRouter>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={
              <AuthGuard>
                <DashboardLayout />
              </AuthGuard>
            }>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="users" element={<UsersPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}
'''

# --- 2. THE LAYOUT SYSTEM (The Citadel's Form) ---
# This single directive summons the entire multi-file layout system.
src/layouts/DashboardLayout.tsx :: @ui/component(name="dashboard-layout")

# --- 3. THE PAGES & WIDGETS ---

src/pages/DashboardPage.tsx :: @ui/component(name="DashboardPage")
src/pages/UsersPage.tsx :: @ui/component(name="UsersPage")
src/pages/SettingsPage.tsx :: @ui/component(name="SettingsPage", prompt="A settings page with a sidebar nav and form fields for profile and appearance.")
src/pages/LoginPage.tsx :: @ui/component(name="AuthForm")

src/components/dashboard/StatsCards.tsx :: @ui/component(name="StatsCards")
src/components/dashboard/RecentSales.tsx :: @ui/component(name="RecentSales")

# --- 4. AUTHENTICATION & UTILITIES ---

src/components/auth/AuthGuard.tsx :: @ui/component(name="AuthGuard")
src/hooks/useAuth.ts :: @ui/hook(name="useAuth", logic="auth-context")

# --- 5. THE FOUNDATIONAL ATOMS ---
# We ensure the core UI atoms are present for the other components to build upon.
# Note: The UI Domain is idempotent; these will only be created if they don't exist.
src/components/ui/button.tsx :: @ui/component(name="Button")
src/components/ui/card.tsx :: @ui/component(name="Card")
src/components/ui/input.tsx :: @ui/component(name="Input")
src/components/ui/badge.tsx :: @ui/component(name="Badge")
src/components/ui/table.tsx :: @ui/component(name="Table")
src/lib/utils.ts :: @ui/utils

    """)

    # --- The Rite of Gnostic Invocation ---
    # The artisan summons the God-Engine to make its own, internal will manifest.
    try:
        result = invoke_scaffold_command(
            command_args=["-"],
            stdin_content=blueprint_scripture,
            non_interactive=True,
            raw_mode=True # Ensures the output is pure and clean for return
        )

        if result.exit_code != 0:
            raise ArtisanHeresy("A paradox occurred while materializing the AdminDashboard kit.", details=result.output)

        # The Conductor's Vow: It proclaims the path to the main citadel file as a sacred comment.
        return "// Gnostic Admin Dashboard Kit materialized successfully. The main citadel is 'src/layouts/DashboardLayout.tsx'."

    except Exception as e:
        raise ArtisanHeresy("A catastrophic, unhandled paradox shattered the AdminDashboard Conductor.", child_heresy=e)