
-- Drop old tables (estrutura antiga)
DROP TABLE IF EXISTS public.checklist_items CASCADE;
DROP TABLE IF EXISTS public.obras CASCADE;

-- Nova tabela: obras (projetos / edifícios)
CREATE TABLE public.obras (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  nome TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Apartamentos dentro de uma obra
CREATE TABLE public.apartamentos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  obra_id UUID NOT NULL REFERENCES public.obras(id) ON DELETE CASCADE,
  nome TEXT NOT NULL,
  estado public.obra_estado NOT NULL DEFAULT 'pendente',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Checklist por apartamento
CREATE TABLE public.checklist_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  apartamento_id UUID NOT NULL REFERENCES public.apartamentos(id) ON DELETE CASCADE,
  descricao TEXT NOT NULL,
  concluido BOOLEAN NOT NULL DEFAULT false,
  ordem INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.apartamentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_items ENABLE ROW LEVEL SECURITY;

-- Políticas: obras
CREATE POLICY "own obras select" ON public.obras FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "own obras insert" ON public.obras FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "own obras update" ON public.obras FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "own obras delete" ON public.obras FOR DELETE USING (auth.uid() = user_id);

-- Políticas: apartamentos (via obra)
CREATE POLICY "own apt select" ON public.apartamentos FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own apt insert" ON public.apartamentos FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own apt update" ON public.apartamentos FOR UPDATE
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own apt delete" ON public.apartamentos FOR DELETE
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));

-- Políticas: checklist (via apartamento → obra)
CREATE POLICY "own check select" ON public.checklist_items FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "own check insert" ON public.checklist_items FOR INSERT
  WITH CHECK (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "own check update" ON public.checklist_items FOR UPDATE
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "own check delete" ON public.checklist_items FOR DELETE
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));

-- Triggers de updated_at
CREATE TRIGGER obras_touch BEFORE UPDATE ON public.obras
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();
CREATE TRIGGER apt_touch BEFORE UPDATE ON public.apartamentos
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();
