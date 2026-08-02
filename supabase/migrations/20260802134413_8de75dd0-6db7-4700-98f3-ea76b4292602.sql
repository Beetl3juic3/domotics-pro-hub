-- obras.user_id no longer required (app has no login)
ALTER TABLE public.obras ALTER COLUMN user_id DROP NOT NULL;

-- Drop all existing policies on the three app tables
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT schemaname, tablename, policyname
    FROM pg_policies
    WHERE schemaname = 'public'
      AND tablename IN ('obras','apartamentos','checklist_items')
  LOOP
    EXECUTE format('DROP POLICY %I ON %I.%I', r.policyname, r.schemaname, r.tablename);
  END LOOP;
END $$;

GRANT SELECT, INSERT, UPDATE, DELETE ON public.obras TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.apartamentos TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.checklist_items TO anon, authenticated;
GRANT ALL ON public.obras TO service_role;
GRANT ALL ON public.apartamentos TO service_role;
GRANT ALL ON public.checklist_items TO service_role;

CREATE POLICY "Acesso publico a obras" ON public.obras FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Acesso publico a apartamentos" ON public.apartamentos FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Acesso publico a checklist_items" ON public.checklist_items FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);