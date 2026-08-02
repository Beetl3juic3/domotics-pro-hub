import { Link } from "@tanstack/react-router";
import { Cpu } from "lucide-react";

export function AppHeader() {
  return (
    <header className="border-b bg-card">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <Link to="/obras" className="flex items-center gap-2 font-semibold">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Cpu className="h-4 w-4" />
          </span>
          Smarthome SPNOS
        </Link>
        <span className="text-sm text-muted-foreground">Gestão de Obras</span>
      </div>
    </header>
  );
}