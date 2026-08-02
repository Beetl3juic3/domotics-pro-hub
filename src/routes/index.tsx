import { createFileRoute, Navigate } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Smarthome SPNOS · Obras e Checklists" },
      { name: "description", content: "Gestão de obras, apartamentos e checklists de instalação para técnicos de domótica." },
      { property: "og:title", content: "Smarthome SPNOS · Obras e Checklists" },
      { property: "og:description", content: "Gestão de obras, apartamentos e checklists de instalação para técnicos de domótica." },
    ],
  }),
  component: Index,
});

function Index() {
  return <Navigate to="/obras" />;
}