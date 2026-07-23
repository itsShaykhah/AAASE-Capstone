import { Activity, FileText, Info, LayoutDashboard, Megaphone, PlusCircle } from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/new-campaign", label: "New Campaign", icon: PlusCircle, end: false },
  { to: "/results", label: "Campaign Results", icon: FileText, end: false },
  { to: "/observability", label: "Observability", icon: Activity, end: false },
  { to: "/about", label: "About", icon: Info, end: false },
] as const;

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r bg-card md:flex md:flex-col">
      <div className="flex h-16 items-center gap-2 border-b px-6">
        <Megaphone className="h-5 w-5 text-primary" />
        <span className="font-semibold tracking-tight">AI Marketing Team</span>
      </div>

      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t p-4 text-xs text-muted-foreground">
        LangGraph multi-agent campaign generator
      </div>
    </aside>
  );
}
