import { createFileRoute, Link, Navigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ArrowLeft, ChevronRight, DoorOpen, Loader2, Pencil, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { estadoBadgeClass, estadoLabel, type Estado } from "@/lib/obra-utils";
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
import { useNavigate } from "@tanstack/react-router";

type Obra = { id: string; nome: string };
type Apartamento = { id: string; nome: string; estado: Estado; modificado_em: string | null; modificado_por: string | null };

export const Route = createFileRoute("/obras/$id/")({
  component: ObraDetail,
});

function ObraDetail() {
  const { id } = Route.useParams();
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [obra, setObra] = useState<Obra | null>(null);
  const [apartamentos, setApartamentos] = useState<Apartamento[] | null>(null);
  const [nomes, setNomes] = useState<Map<string, string>>(new Map());
  const [novo, setNovo] = useState("");
  const [criando, setCriando] = useState(false);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const [editNome, setEditNome] = useState("");

  useEffect(() => {
    if (!user) return;
    (async () => {
      const [{ data: o, error: e1 }, { data: a, error: e2 }] = await Promise.all([
        supabase.from("obras").select("id, nome").eq("id", id).maybeSingle(),
        supabase
          .from("apartamentos")
          .select("id, nome, estado, modificado_em, modificado_por")
          .eq("obra_id", id)
          .order("created_at"),
      ]);
      if (e1) toast.error(e1.message);
      if (e2) toast.error(e2.message);
      setObra((o as Obra) ?? null);
      const list = (a ?? []) as Apartamento[];
      setApartamentos(list);
      setNomes(await getNomes(list.map((x) => x.modificado_por)));
    })();
  }, [id, user]);

  if (loading) return null;
  if (!user) return <Navigate to="/login" />;

  async function criarApartamento(e: React.FormEvent) {
    e.preventDefault();
    if (!novo.trim()) return;
    setCriando(true);
    const { data, error } = await supabase
      .from("apartamentos")
      .insert({ obra_id: id, nome: novo.trim() })
      .select("id, nome, estado, modificado_em, modificado_por")
      .single();
    setCriando(false);
    if (error) return toast.error(error.message);
    const novoApt = data as Apartamento;
    setApartamentos((arr) => [...(arr ?? []), novoApt]);
    setNomes(await getNomes([novoApt.modificado_por, ...(apartamentos ?? []).map((x) => x.modificado_por)]));
    setNovo("");
  }

  async function apagarApartamento(aptId: string) {
    const prev = apartamentos;
    setApartamentos((arr) => (arr ?? []).filter((a) => a.id !== aptId));
    const { error } = await supabase.from("apartamentos").delete().eq("id", aptId);
    if (error) {
      setApartamentos(prev);
      toast.error(error.message);
    } else {
      toast.success("Apartamento apagado");
    }
  }

  async function guardarNomeApt(aptId: string) {
    const nome = editNome.trim();
    if (!nome) return;
    const { error } = await supabase.from("apartamentos").update({ nome }).eq("id", aptId);
    if (error) return toast.error(error.message);
    setApartamentos((arr) => (arr ?? []).map((a) => (a.id === aptId ? { ...a, nome } : a)));
    setEditandoId(null);
  }

  async function apagarObra() {
    const { error } = await supabase.from("obras").delete().eq("id", id);
    if (error) return toast.error(error.message);
    toast.success("Obra apagada");
    navigate({ to: "/obras" });
  }

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      <main className="mx-auto max-w-3xl px-4 py-8">
        <Link
          to="/obras"
          className="mb-4 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" /> Todas as obras
        </Link>

        {obra === null && apartamentos === null ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : !obra ? (
          <Card className="p-8 text-center text-muted-foreground">Obra não encontrada.</Card>
        ) : (
          <>
            <div className="mb-6 flex items-start justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">{obra.nome}</h1>
                <p className="text-sm text-muted-foreground">
                  {(apartamentos ?? []).length} apartamento(s)
                </p>
              </div>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="outline" size="sm">
                    <Trash2 className="mr-2 h-4 w-4" /> Apagar obra
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Apagar obra?</AlertDialogTitle>
                    <AlertDialogDescription>
                      Vai apagar “{obra.nome}” e todos os apartamentos e tarefas. Esta ação não pode ser revertida.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction onClick={apagarObra}>Apagar</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>

            <Card className="mb-6 p-4">
              <form onSubmit={criarApartamento} className="flex flex-col gap-3 sm:flex-row">
                <Input
                  placeholder="Nome do apartamento (ex: Bloco A · 3ºD)"
                  value={novo}
                  onChange={(e) => setNovo(e.target.value)}
                  maxLength={120}
                />
                <Button type="submit" disabled={criando || !novo.trim()}>
                  {criando ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
                  Novo apartamento
                </Button>
              </form>
            </Card>

            {(apartamentos ?? []).length === 0 ? (
              <Card className="p-10 text-center text-muted-foreground">
                <DoorOpen className="mx-auto mb-3 h-10 w-10 opacity-40" />
                Adiciona o primeiro apartamento desta obra.
              </Card>
            ) : (
              <ul className="space-y-3">
                {(apartamentos ?? []).map((a) => (
                  <li key={a.id}>
                    <Card className="flex items-center justify-between p-4 transition hover:shadow-md">
                      {editandoId === a.id ? (
                        <form
                          className="flex flex-1 items-center gap-2"
                          onSubmit={(e) => {
                            e.preventDefault();
                            guardarNomeApt(a.id);
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
                          <Link
                            to="/obras/$id/apartamentos/$aptId"
                            params={{ id, aptId: a.id }}
                            className="flex flex-1 items-center gap-3"
                          >
                            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary">
                              <DoorOpen className="h-5 w-5 text-secondary-foreground" />
                            </span>
                            <div>
                              <div className="font-medium">{a.nome}</div>
                              {a.modificado_em && (
                                <div className="text-xs text-muted-foreground">
                                  {formatModificado(a.modificado_por ? nomes.get(a.modificado_por) : undefined, a.modificado_em)}
                                </div>
                              )}
                            </div>
                          </Link>
                          <div className="flex items-center gap-2">
                            <span className={`rounded-full px-3 py-1 text-xs font-medium ${estadoBadgeClass(a.estado)}`}>
                              {estadoLabel(a.estado)}
                            </span>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => {
                                setEditandoId(a.id);
                                setEditNome(a.nome);
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
                                  <AlertDialogTitle>Apagar apartamento?</AlertDialogTitle>
                                  <AlertDialogDescription>
                                    Vai apagar “{a.nome}” e todas as tarefas. Esta ação não pode ser revertida.
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel>Cancelar</AlertDialogCancel>
                                  <AlertDialogAction onClick={() => apagarApartamento(a.id)}>Apagar</AlertDialogAction>
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
          </>
        )}
      </main>
    </div>
  );
}