import { Moon, Sun } from "lucide-react";
import { NavLink } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/context/ThemeContext";
import { useApiHealth } from "@/hooks/useApiHealth";

export function TopBar() {
  const isOnline = useApiHealth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="flex h-16 items-center justify-between border-b bg-card/50 px-4 backdrop-blur md:px-8">
      <div className="flex items-center gap-2 md:hidden">
        <span className="font-semibold">AI Marketing Team</span>
      </div>

      <div className="ml-auto flex items-center gap-3">
        <Badge variant={isOnline ? "success" : isOnline === null ? "outline" : "destructive"}>
          <span className="mr-1.5 inline-block h-1.5 w-1.5 rounded-full bg-current" />
          {isOnline === null ? "Checking API..." : isOnline ? "API Online" : "API Unreachable"}
        </Badge>

        <Button asChild size="sm">
          <NavLink to="/new-campaign">New Campaign</NavLink>
        </Button>

        <Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
      </div>
    </header>
  );
}
