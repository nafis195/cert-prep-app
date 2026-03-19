-- Timestamp helpers and signup defaults

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_profiles_updated_at on public.profiles;
create trigger trg_profiles_updated_at
before update on public.profiles
for each row execute procedure public.set_updated_at();

drop trigger if exists trg_certifications_updated_at on public.certifications;
create trigger trg_certifications_updated_at
before update on public.certifications
for each row execute procedure public.set_updated_at();

drop trigger if exists trg_ratings_updated_at on public.ratings;
create trigger trg_ratings_updated_at
before update on public.ratings
for each row execute procedure public.set_updated_at();

-- When a user is created, auto-create a profile and default 'user' role.
-- For a self-managed app, this runs on public.users inserts.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
as $$
begin
  -- Make RLS policies that rely on `public.current_user_id()` work
  -- for inserts done inside this trigger.
  perform set_config('app.user_id', new.id::text, true);

  insert into public.profiles (user_id, full_name)
  values (new.id, split_part(new.email, '@', 1))
  on conflict (user_id) do nothing;

  insert into public.user_roles (user_id, role)
  values (new.id, 'user')
  on conflict (user_id, role) do nothing;

  return new;
end;
$$;

drop trigger if exists trg_users_handle_new_user on public.users;
create trigger trg_users_handle_new_user
after insert on public.users
for each row execute procedure public.handle_new_user();

