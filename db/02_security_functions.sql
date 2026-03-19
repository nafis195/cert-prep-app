-- Role/identity helpers for RLS
-- For a self-managed app, we read the current user id from a DB setting:
--   select set_config('app.user_id', '<uuid>', true);
-- Your API should set this per request/connection when using RLS.

create or replace function public.current_user_id()
returns uuid
language sql
stable
as $$
  nullif(current_setting('app.user_id', true), '')::uuid
$$;

create or replace function public.has_role(role_to_check public.app_role)
returns boolean
language sql
stable
as $$
  select exists (
    select 1
    from public.user_roles ur
    where ur.user_id = public.current_user_id()
      and ur.role = role_to_check
  );
$$;

