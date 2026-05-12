export const ESTADOS = [
  { value: "pendente", label: "Pendente" },
  { value: "em_curso", label: "Em curso" },
  { value: "concluida", label: "Concluída" },
] as const;

export type Estado = (typeof ESTADOS)[number]["value"];

export function estadoBadgeClass(estado: Estado) {
  switch (estado) {
    case "pendente":
      return "bg-muted text-muted-foreground";
    case "em_curso":
      return "bg-accent text-accent-foreground";
    case "concluida":
      return "bg-primary text-primary-foreground";
  }
}

export function estadoLabel(estado: Estado) {
  return ESTADOS.find((e) => e.value === estado)?.label ?? estado;
}