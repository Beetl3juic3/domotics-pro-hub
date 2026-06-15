import { createFileRoute, Link, Navigate, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Building2, ChevronRight, Loader2, Pencil, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { getNomes, formatModificado } from "@/lib/profiles";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

type Obra = { id: string; nome: string; modificado_em: string | null; modificado_por: string | null };

export const Route = createFileRoute("/obras/")({
  component: ObrasList,
});

function ObrasList() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [obras, setObras] = useState<Obra[] | null>(null);
  const [nomes, setNomes] = useState<Map<string, string>>(new Map());
  const [novo, setNovo] = useState("");
  const [criando, setCriando] = useState(false);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [editNome, setEditNome] = useState("");

  useEffect(() => {
    if (!user) return;
    supabase
      .from("obras")
      .select("id, nome, modificado_em, modificado_por")
      .order("modificado_em", { ascending: false })
      .then(async ({ data, error }) => {
        if (error) toast.error(error.message);
        else {
          const list = (data ?? []) as Obra[];
          setObras(list);
          setNomes(await getNomes(list.map((o) => o.modificado_por)));
        }
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

  async function apagarObra(id: string) {
    const prev = obras;
    setObras((arr) => (arr ?? []).filter((o) => o.id !== id));
    const { error } = await supabase.from("obras").delete().eq("id", id);
    if (error) {
      setObras(prev);
      toast.error(error.message);
    } else {
      toast.success("Obra apagada");
    }
  }

  async function guardarNome(id: string) {
    const nome = editNome.trim();
    if (!nome) return;
    const { error } = await supabase.from("obras").update({ nome }).eq("id", id);
    if (error) return toast.error(error.message);
    setObras((arr) => (arr ?? []).map((o) => (o.id === id ? { ...o, nome } : o)));
    setEditandoId(null);
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
                <Card className="flex items-center justify-between p-4 transition hover:shadow-md">
                  {editandoId === o.id ? (
                    <form
                      className="flex flex-1 items-center gap-2"
                      onSubmit={(e) => {
                        e.preventDefault();
                        guardarNome(o.id);
                      }}
                    >
                      <Input
                        autoFocus
                        value={editNome}
                        onChange={(e) => setEditNome(e.target.value)}
                        maxLength={120}
                      />
                      <Button type="submit" size="sm">Guardar</Button>
                      <Button type="button" size="sm" variant="ghost" onClick={() => setEditandoId(null)}>
                        Cancelar
                      </Button>
                    </form>
                  ) : (
                    <>
                      <Link to="/obras/$id" params={{ id: o.id }} className="flex flex-1 items-center gap-3">
                        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary">
                          <Building2 className="h-5 w-5 text-secondary-foreground" />
                        </span>
                        <div>
                          <div className="font-medium">{o.nome}</div>
                          <div className="text-xs text-muted-foreground">
                            Modificado por {formatModificado(o.modificado_por ? nomes.get(o.modificado_por) : undefined, o.modificado_em)}
                          </div>
                        </div>
                      </Link>
                      <div className="flex items-center gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => {
                            setEditandoId(o.id);
                            setEditNome(o.nome);
                          }}
                          aria-label="Renomear"
                        >
                          <Pencil className="h-4 w-4" />
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button variant="ghost" size="icon" aria-label="Apagar">
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>Apagar obra?</AlertDialogTitle>
                              <AlertDialogDescription>
                                Vai apagar “{o.nome}” e todos os apartamentos e tarefas associados. Esta ação não pode ser revertida.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>Cancelar</AlertDialogCancel>
                              <AlertDialogAction onClick={() => apagarObra(o.id)}>Apagar</AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      </div>
                    </>
                  )}
                </Card>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}