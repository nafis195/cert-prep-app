-- Enable Row Level Security and create policies
-- Requires: db/02_security_functions.sql

begin;

alter table public.profiles enable row level security;
alter table public.user_roles enable row level security;
alter table public.vendors enable row level security;
alter table public.certifications enable row level security;
alter table public.ratings enable row level security;
alter table public.certification_requests enable row level security;

-- PROFILES: user can read/update own profile; admins can read all
drop policy if exists profiles_read_own on public.profiles;
create policy profiles_read_own
on public.profiles for select
using (user_id = public.current_user_id());

drop policy if exists profiles_insert_own on public.profiles;
create policy profiles_insert_own
on public.profiles for insert
with check (user_id = public.current_user_id());

drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own
on public.profiles for update
using (user_id = public.current_user_id())
with check (user_id = public.current_user_id());

drop policy if exists profiles_admin_read_all on public.profiles;
create policy profiles_admin_read_all
on public.profiles for select
using (public.has_role('admin'));

-- USER_ROLES: users can read their roles; only admins can write roles
drop policy if exists roles_read_own on public.user_roles;
create policy roles_read_own
on public.user_roles for select
using (user_id = public.current_user_id());

-- Allow a user to create only the default 'user' role for themselves.
-- Prevents privilege escalation to admin via inserts.
drop policy if exists roles_insert_default_user on public.user_roles;
create policy roles_insert_default_user
on public.user_roles for insert
with check (
  user_id = public.current_user_id()
  and role = 'user'
);

drop policy if exists roles_admin_write on public.user_roles;
create policy roles_admin_write
on public.user_roles for all
using (public.has_role('admin'))
with check (public.has_role('admin'));

-- VENDORS: public read; admin write/update
drop policy if exists vendors_public_read on public.vendors;
create policy vendors_public_read
on public.vendors for select
using (true);

drop policy if exists vendors_admin_insert on public.vendors;
create policy vendors_admin_insert
on public.vendors for insert
with check (public.has_role('admin'));

drop policy if exists vendors_admin_update on public.vendors;
create policy vendors_admin_update
on public.vendors for update
using (public.has_role('admin'))
with check (public.has_role('admin'));

-- CERTIFICATIONS: public read active; admin write/update
drop policy if exists certs_public_read on public.certifications;
create policy certs_public_read
on public.certifications for select
using (is_active = true);

drop policy if exists certs_admin_insert on public.certifications;
create policy certs_admin_insert
on public.certifications for insert
with check (public.has_role('admin'));

drop policy if exists certs_admin_update on public.certifications;
create policy certs_admin_update
on public.certifications for update
using (public.has_role('admin'))
with check (public.has_role('admin'));

-- RATINGS: public read; authenticated users can write their own
drop policy if exists ratings_public_read on public.ratings;
create policy ratings_public_read
on public.ratings for select
using (true);

drop policy if exists ratings_insert_own on public.ratings;
create policy ratings_insert_own
on public.ratings for insert
with check (user_id = public.current_user_id());

drop policy if exists ratings_update_own on public.ratings;
create policy ratings_update_own
on public.ratings for update
using (user_id = public.current_user_id())
with check (user_id = public.current_user_id());

drop policy if exists ratings_delete_own on public.ratings;
create policy ratings_delete_own
on public.ratings for delete
using (user_id = public.current_user_id());

-- CERTIFICATION_REQUESTS:
-- - authenticated users can insert
-- - users can read their own
-- - admins can read/update all
drop policy if exists requests_insert_auth on public.certification_requests;
create policy requests_insert_auth
on public.certification_requests for insert
with check (user_id = public.current_user_id());

drop policy if exists requests_read_own on public.certification_requests;
create policy requests_read_own
on public.certification_requests for select
using (user_id = public.current_user_id());

drop policy if exists requests_admin_read_all on public.certification_requests;
create policy requests_admin_read_all
on public.certification_requests for select
using (public.has_role('admin'));

drop policy if exists requests_admin_update on public.certification_requests;
create policy requests_admin_update
on public.certification_requests for update
using (public.has_role('admin'))
with check (public.has_role('admin'));

commit;

