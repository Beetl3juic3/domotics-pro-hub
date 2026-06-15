
-- OBRAS: owner-only
DROP POLICY IF EXISTS "obras all auth select" ON public.obras;
DROP POLICY IF EXISTS "obras all auth insert" ON public.obras;
DROP POLICY IF EXISTS "obras all auth update" ON public.obras;
DROP POLICY IF EXISTS "obras all auth delete" ON public.obras;

CREATE POLICY "obras own select" ON public.obras
  FOR SELECT TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "obras own insert" ON public.obras
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "obras own update" ON public.obras
  FOR UPDATE TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "obras own delete" ON public.obras
  FOR DELETE TO authenticated USING (auth.uid() = user_id);

-- APARTAMENTOS: only when user owns the parent obra
DROP POLICY IF EXISTS "apt all auth select" ON public.apartamentos;
DROP POLICY IF EXISTS "apt all auth insert" ON public.apartamentos;
DROP POLICY IF EXISTS "apt all auth update" ON public.apartamentos;
DROP POLICY IF EXISTS "apt all auth delete" ON public.apartamentos;

CREATE POLICY "apt owner select" ON public.apartamentos
  FOR SELECT TO authenticated
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "apt owner insert" ON public.apartamentos
  FOR INSERT TO authenticated
  WITH CHECK (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "apt owner update" ON public.apartamentos
  FOR UPDATE TO authenticated
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()))
  WITH CHECK (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));
CREATE POLICY "apt owner delete" ON public.apartamentos
  FOR DELETE TO authenticated
  USING (EXISTS (SELECT 1 FROM public.obras o WHERE o.id = obra_id AND o.user_id = auth.uid()));

-- CHECKLIST_ITEMS: via apartamentos -> obras
DROP POLICY IF EXISTS "check all auth select" ON public.checklist_items;
DROP POLICY IF EXISTS "check all auth insert" ON public.checklist_items;
DROP POLICY IF EXISTS "check all auth update" ON public.checklist_items;
DROP POLICY IF EXISTS "check all auth delete" ON public.checklist_items;

CREATE POLICY "check owner select" ON public.checklist_items
  FOR SELECT TO authenticated
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "check owner insert" ON public.checklist_items
  FOR INSERT TO authenticated
  WITH CHECK (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "check owner update" ON public.checklist_items
  FOR UPDATE TO authenticated
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));
CREATE POLICY "check owner delete" ON public.checklist_items
  FOR DELETE TO authenticated
  USING (EXISTS (
    SELECT 1 FROM public.apartamentos a
    JOIN public.obras o ON o.id = a.obra_id
    WHERE a.id = apartamento_id AND o.user_id = auth.uid()
  ));

-- PROFILES: own only
DROP POLICY IF EXISTS "profiles select auth" ON public.profiles;
CREATE POLICY "profiles select self" ON public.profiles
  FOR SELECT TO authenticated USING (auth.uid() = user_id);
