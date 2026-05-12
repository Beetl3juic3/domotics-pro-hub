import { supabase } from "@/integrations/supabase/client";

const cache = new Map<string, string>();

export async function getNomes(userIds: (string | null | undefined)[]): Promise<Map<string, string>> {
  const ids = Array.from(new Set(userIds.filter((x): x is string => !!x)));
  const missing = ids.filter((id) => !cache.has(id));
  if (missing.length) {
    const { data } = await supabase.from("profiles").select("user_id, nome").in("user_id", missing);
    (data ?? []).forEach((p: { user_id: string; nome: string }) => cache.set(p.user_id, p.nome));
    missing.forEach((id) => { if (!cache.has(id)) cache.set(id, "Desconhecido"); });
  }
  const out = new Map<string, string>();
  ids.forEach((id) => out.set(id, cache.get(id) ?? "Desconhecido"));
  return out;
}

export function formatModificado(nome: string | undefined, data: string | undefined | null): string {
  if (!data) return "";
  const d = new Date(data).toLocaleString("pt-PT", { dateStyle: "short", timeStyle: "short" });
  return nome ? `${nome} · ${d}` : d;
}
