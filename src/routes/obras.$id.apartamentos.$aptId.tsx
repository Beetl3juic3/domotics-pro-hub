import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, Loader2, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { ESTADOS, type Estado } from "@/lib/obra-utils";
import { getNomes, formatModificado } from "@/lib/profiles";

type Apt = { id: string; nome: string; estado: Estado; obra_id: string; modificado_em: string | null; modificado_por: string | null };
type Item = { id: string; descricao: string; concluido: boolean; ordem: number; modificado_em: string | null; modificado_por: string | null };

export const Route = createFileRoute("/obras/$id/apartamentos/$aptId")({
  head: () => ({
    meta: [
      { title: "Checklist do apartamento · Smarthome SPNOS" },
      { name: "description", content: "Estado do apartamento e checklist de tarefas de instalação de domótica." },
      { property: "og:title", content: "Checklist do apartamento · Smarthome SPNOS" },
      { property: "og:description", content: "Estado do apartamento e checklist de tarefas de instalação de domótica." },
    ],
  }),
  component: ApartamentoDetail,
});

function ApartamentoDetail() {
  const { id, aptId } = Route.useParams();
  const [apt, setApt] = useState<Apt | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [nomes, setNomes] = useState<Map<string, string>>(new Map());
  const [novo, setNovo] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    (async () => {
      const [{ data: a, error: e1 }, { data: it, error: e2 }] = await Promise.all([
        supabase.from("apartamentos").select("id, nome, estado, obra_id, modificado_em, modificado_por").eq("id", aptId).maybeSingle(),
        supabase
          .from("checklist_items")
          .select("id, descricao, concluido, ordem, modificado_em, modificado_por")
          .eq("apartamento_id", aptId)
          .order("ordem"),
      ]);
      if (e1) toast.error(e1.message);
      if (e2) toast.error(e2.message);
      const aptData = (a as Apt) ?? null;
      const itemsData = (it ?? []) as Item[];
      setApt(aptData);
      setItems(itemsData);
      setNomes(await getNomes([aptData?.modificado_por, ...itemsData.map((i) => i.modificado_por)]));
      setCarregando(false);
    })();
  }, [aptId]);

  async function alterarEstado(estado: Estado) {
    if (!apt) return;
    setApt({ ...apt, estado });
    const { data, error } = await supabase
      .from("apartamentos")
      .update({ estado })
      .eq("id", apt.id)
      .select("modificado_em, modificado_por")
      .single();
    if (error) return toast.error(error.message);
    if (data) {
      setApt((p) => (p ? { ...p, modificado_em: data.modificado_em, modificado_por: data.modificado_por } : p));
      setNomes(await getNomes([data.modificado_por]));
    }
  }

  async function adicionarItem(e: React.FormEvent) {
    e.preventDefault();
    if (!novo.trim()) return;
    const ordem = items.length;
    const { data, error } = await supabase
      .from("checklist_items")
      .insert({ apartamento_id: aptId, descricao: novo.trim(), ordem })
      .select("id, descricao, concluido, ordem, modificado_em, modificado_por")
      .single();
    if (error) return toast.error(error.message);
    const it = data as Item;
    setItems([...items, it]);
    setNomes(await getNomes([it.modificado_por]));
    setNovo("");
  }

  async function toggleItem(item: Item) {
    const concluido = !item.concluido;
    setItems((arr) => arr.map((i) => (i.id === item.id ? { ...i, concluido } : i)));
    const { data, error } = await supabase
      .from("checklist_items")
      .update({ concluido })
      .eq("id", item.id)
      .select("modificado_em, modificado_por")
      .single();
    if (error) return toast.error(error.message);
    if (data) {
      setItems((arr) => arr.map((i) => (i.id === item.id ? { ...i, modificado_em: data.modificado_em, modificado_por: data.modificado_por } : i)));
      setNomes(await getNomes([data.modificado_por]));
    }
  }

  async function removerItem(item: Item) {
    setItems((arr) => arr.filter((i) => i.id !== item.id));
    const { error } = await supabase.from("checklist_items").delete().eq("id", item.id);
    if (error) toast.error(error.message);
  }

  const concluidos = items.filter((i) => i.concluido).length;

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      <main className="mx-auto max-w-3xl px-4 py-8">
        <Link
          to="/obras/$id"
          params={{ id }}
          className="mb-4 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" /> Voltar à obra
        </Link>

        {carregando ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : !apt ? (
          <Card className="p-8 text-center text-muted-foreground">Apartamento não encontrado.</Card>
        ) : (
          <>
            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">{apt.nome}</h1>
                <p className="text-sm text-muted-foreground">
                  {concluidos} / {items.length} tarefas concluídas
                </p>
                {apt.modificado_em && (
                  <p className="text-xs text-muted-foreground">
                    Última alteração: {formatModificado(apt.modificado_por ? nomes.get(apt.modificado_por) : undefined, apt.modificado_em)}
                  </p>
                )}
              </div>
              <Select value={apt.estado} onValueChange={(v) => alterarEstado(v as Estado)}>
                <SelectTrigger className="w-full sm:w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {ESTADOS.map((e) => (
                    <SelectItem key={e.value} value={e.value}>{e.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <Card className="p-4">
              <h2 className="mb-3 text-lg font-semibold">Checklist</h2>
              <form onSubmit={adicionarItem} className="mb-4 flex gap-2">
                <Input
                  placeholder="Adicionar tarefa..."
                  value={novo}
                  onChange={(e) => setNovo(e.target.value)}
                  maxLength={200}
                />
                <Button type="submit" size="icon" disabled={!novo.trim()}>
                  <Plus className="h-4 w-4" />
                </Button>
              </form>

              {items.length === 0 ? (
                <p className="py-6 text-center text-sm text-muted-foreground">
                  Sem tarefas. Adiciona a primeira acima.
                </p>
              ) : (
                <ul className="space-y-1">
                  {items.map((it) => (
                    <li
                      key={it.id}
                      className="group flex items-center gap-3 rounded-md px-2 py-2 hover:bg-muted"
                    >
                      <Checkbox
                        checked={it.concluido}
                        onCheckedChange={() => toggleItem(it)}
                        id={`it-${it.id}`}
                      />
                      <label
                        htmlFor={`it-${it.id}`}
                        className={`flex-1 cursor-pointer text-sm ${
                          it.concluido ? "text-muted-foreground line-through" : ""
                        }`}
                      >
                        {it.descricao}
                        {it.modificado_em && (
                          <span className="ml-2 text-xs text-muted-foreground">
                            · {formatModificado(it.modificado_por ? nomes.get(it.modificado_por) : undefined, it.modificado_em)}
                          </span>
                        )}
                      </label>
                      <button
                        type="button"
                        onClick={() => removerItem(it)}
                        className="opacity-0 transition group-hover:opacity-100"
                        aria-label="Remover"
                      >
                        <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </>
        )}
      </main>
    </div>
  );
}