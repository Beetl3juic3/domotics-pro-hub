
-- profiles
CREATE TABLE public.profiles (
  user_id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nome text NOT NULL,
  email text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "profiles select auth" ON public.profiles
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "profiles insert self" ON public.profiles
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "profiles update self" ON public.profiles
  FOR UPDATE TO authenticated USING (auth.uid() = user_id);

CREATE TRIGGER profiles_touch BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();

-- auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (user_id, nome, email)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'nome', split_part(NEW.email, '@', 1)),
    NEW.email
  )
  ON CONFLICT (user_id) DO NOTHING;
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- backfill existing users
INSERT INTO public.profiles (user_id, nome, email)
SELECT id, COALESCE(raw_user_meta_data->>'nome', split_part(email, '@', 1)), email
FROM auth.users
ON CONFLICT (user_id) DO NOTHING;

-- audit columns
ALTER TABLE public.obras
  ADD COLUMN modificado_por uuid REFERENCES auth.users(id),
  ADD COLUMN modificado_em timestamptz NOT NULL DEFAULT now();

ALTER TABLE public.apartamentos
  ADD COLUMN modificado_por uuid REFERENCES auth.users(id),
  ADD COLUMN modificado_em timestamptz NOT NULL DEFAULT now();

ALTER TABLE public.checklist_items
  ADD COLUMN modificado_por uuid REFERENCES auth.users(id),
  ADD COLUMN modificado_em timestamptz NOT NULL DEFAULT now();

CREATE OR REPLACE FUNCTION public.set_modified()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = public
AS $$
BEGIN
  NEW.modificado_por = auth.uid();
  NEW.modificado_em = now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER obras_set_modified BEFORE INSERT OR UPDATE ON public.obras
  FOR EACH ROW EXECUTE FUNCTION public.set_modified();
CREATE TRIGGER apartamentos_set_modified BEFORE INSERT OR UPDATE ON public.apartamentos
  FOR EACH ROW EXECUTE FUNCTION public.set_modified();
CREATE TRIGGER checklist_items_set_modified BEFORE INSERT OR UPDATE ON public.checklist_items
  FOR EACH ROW EXECUTE FUNCTION public.set_modified();

-- Replace RLS: any authenticated user can do everything
DROP POLICY IF EXISTS "own obras select" ON public.obras;
DROP POLICY IF EXISTS "own obras insert" ON public.obras;
DROP POLICY IF EXISTS "own obras update" ON public.obras;
DROP POLICY IF EXISTS "own obras delete" ON public.obras;

CREATE POLICY "obras all auth select" ON public.obras
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "obras all auth insert" ON public.obras
  FOR INSERT TO authenticated WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "obras all auth update" ON public.obras
  FOR UPDATE TO authenticated USING (auth.uid() IS NOT NULL);
CREATE POLICY "obras all auth delete" ON public.obras
  FOR DELETE TO authenticated USING (auth.uid() IS NOT NULL);

DROP POLICY IF EXISTS "own apt select" ON public.apartamentos;
DROP POLICY IF EXISTS "own apt insert" ON public.apartamentos;
DROP POLICY IF EXISTS "own apt update" ON public.apartamentos;
DROP POLICY IF EXISTS "own apt delete" ON public.apartamentos;

CREATE POLICY "apt all auth select" ON public.apartamentos
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "apt all auth insert" ON public.apartamentos
  FOR INSERT TO authenticated WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "apt all auth update" ON public.apartamentos
  FOR UPDATE TO authenticated USING (auth.uid() IS NOT NULL);
CREATE POLICY "apt all auth delete" ON public.apartamentos
  FOR DELETE TO authenticated USING (auth.uid() IS NOT NULL);

DROP POLICY IF EXISTS "own check select" ON public.checklist_items;
DROP POLICY IF EXISTS "own check insert" ON public.checklist_items;
DROP POLICY IF EXISTS "own check update" ON public.checklist_items;
DROP POLICY IF EXISTS "own check delete" ON public.checklist_items;

CREATE POLICY "check all auth select" ON public.checklist_items
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "check all auth insert" ON public.checklist_items
  FOR INSERT TO authenticated WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "check all auth update" ON public.checklist_items
  FOR UPDATE TO authenticated USING (auth.uid() IS NOT NULL);
CREATE POLICY "check all auth delete" ON public.checklist_items
  FOR DELETE TO authenticated USING (auth.uid() IS NOT NULL);
