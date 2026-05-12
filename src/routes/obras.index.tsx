import { createFileRoute, Link, Navigate, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Building2, ChevronRight, Loader2, Plus } from "lucide-react";
import { toast } from "sonner";

type Obra = { id: string; nome: string; updated_at: string };

export const Route = createFileRoute("/obras/")({
  component: ObrasList,
});

function ObrasList() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [obras, setObras] = useState<Obra[] | null>(null);
  const [novo, setNovo] = useState("");
  const [criando, setCriando] = useState(false);

  useEffect(() => {
    if (!user) return;
    supabase
      .from("obras")
      .select("id, nome, updated_at")
      .order("updated_at", { ascending: false })
      .then(({ data, error }) => {
        if (error) toast.error(error.message);
        else setObras((data ?? []) as Obra[]);
      });
  }, [user]);

  if (loading) return null;
  if (!user) return <Navigate to="/login" />;

  async function criarObra(e: React.FormEvent) {
    e.preventDefault();
    if (!novo.trim() || !user) return;
    setCriando(true);
    const { data, error } = await supabase
      .from("obras")
      .insert({ nome: novo.trim(), user_id: user.id })
      .select("id")
      .single();
    setCriando(false);
    if (error) return toast.error(error.message);
    setNovo("");
    navigate({ to: "/obras/$id", params: { id: data.id } });
  }

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      <main className="mx-auto max-w-5xl px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Obras</h1>
          <p className="text-muted-foreground">
            Cada obra (ex: Terramar) contém os seus apartamentos.
          </p>
        </div>

        <Card className="mb-8 p-4 shadow-sm">
          <form onSubmit={criarObra} className="flex flex-col gap-3 sm:flex-row">
            <Input
              placeholder="Nome da obra (ex: Terramar)"
              value={novo}
              onChange={(e) => setNovo(e.target.value)}
              maxLength={120}
            />
            <Button type="submit" disabled={criando || !novo.trim()}>
              {criando ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
              Nova obra
            </Button>
          </form>
        </Card>

        {obras === null ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : obras.length === 0 ? (
          <Card className="p-12 text-center text-muted-foreground">
            <Building2 className="mx-auto mb-3 h-10 w-10 opacity-40" />
            Sem obras ainda. Cria a primeira acima.
          </Card>
        ) : (
          <ul className="space-y-3">
            {obras.map((o) => (
              <li key={o.id}>
                <Link to="/obras/$id" params={{ id: o.id }} className="block">
                  <Card className="flex items-center justify-between p-4 transition hover:shadow-md">
                    <div className="flex items-center gap-3">
                      <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary">
                        <Building2 className="h-5 w-5 text-secondary-foreground" />
                      </span>
                      <div>
                        <div className="font-medium">{o.nome}</div>
                        <div className="text-xs text-muted-foreground">
                          Atualizado {new Date(o.updated_at).toLocaleDateString("pt-PT")}
                        </div>
                      </div>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </Card>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}