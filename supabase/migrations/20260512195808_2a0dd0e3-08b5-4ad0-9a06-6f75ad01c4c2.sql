
CREATE TYPE public.obra_estado AS ENUM ('pendente', 'em_curso', 'concluida');

CREATE TABLE public.obras (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  apartamento TEXT NOT NULL,
  estado public.obra_estado NOT NULL DEFAULT 'pendente',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE public.checklist_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  obra_id UUID NOT NULL REFERENCES public.obras(id) ON DELETE CASCADE,
  descricao TEXT NOT NULL,
  concluido BOOLEAN NOT NULL DEFAULT false,
  ordem INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "own obras select" ON public.obras FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "own obras insert" ON public.obras FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "own obras update" ON public.obras FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "own obras delete" ON public.obras FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "own checklist select" ON public.checklist_items FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own checklist insert" ON public.checklist_items FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own checklist update" ON public.checklist_items FOR UPDATE
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "own checklist delete" ON public.checklist_items FOR DELETE
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));

CREATE OR REPLACE FUNCTION public.touch_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END $$;

CREATE TRIGGER obras_touch BEFORE UPDATE ON public.obras
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();
