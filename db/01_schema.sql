-- Schema for Technical Certification Preparation Application
-- Notes:
-- - Uses UUID primary keys (gen_random_uuid()) to match your ERD
-- - Adds fields required by UI/workflow: exam_code, difficulty, request review metadata

begin;

create type public.difficulty_level as enum ('beginner', 'intermediate', 'advanced');
create type public.request_status as enum ('pending', 'approved', 'rejected');
create type public.app_role as enum ('user', 'admin');

-- USERS
-- If you use Supabase, DO NOT create this table; use auth.users instead.
-- For a self-managed FastAPI app, this is your auth table.
create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  password_hash text not null,
  created_at timestamptz not null default now()
);

-- PROFILES (1:1 with users)
create table if not exists public.profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null unique references public.users(id) on delete cascade,
  full_name text not null,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- USER_ROLES (many roles per user)
create table if not exists public.user_roles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  role public.app_role not null,
  created_at timestamptz not null default now(),
  unique (user_id, role)
);

create index if not exists user_roles_user_id_idx on public.user_roles(user_id);
create index if not exists user_roles_role_idx on public.user_roles(role);

-- VENDORS
create table if not exists public.vendors (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name text not null unique,
  description text,
  created_at timestamptz not null default now()
);

-- CERTIFICATIONS
create table if not exists public.certifications (
  id uuid primary key default gen_random_uuid(),
  vendor_id uuid not null references public.vendors(id) on delete restrict,
  name text not null,
  exam_code text not null,
  difficulty public.difficulty_level not null default 'beginner',
  summary text,
  description text,
  official_url text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (vendor_id, exam_code)
);

create index if not exists certifications_vendor_id_idx on public.certifications(vendor_id);
create index if not exists certifications_exam_code_idx on public.certifications(exam_code);
create index if not exists certifications_name_trgm_idx on public.certifications using gin (name gin_trgm_ops);
create index if not exists certifications_exam_code_trgm_idx on public.certifications using gin (exam_code gin_trgm_ops);

-- RATINGS (one per user per certification)
create table if not exists public.ratings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  certification_id uuid not null references public.certifications(id) on delete cascade,
  rating int not null check (rating between 1 and 5),
  comment text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, certification_id)
);

create index if not exists ratings_user_id_idx on public.ratings(user_id);
create index if not exists ratings_certification_id_idx on public.ratings(certification_id);

-- CERTIFICATION_REQUESTS (submitted by user, reviewed by admin)
create table if not exists public.certification_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,

  vendor_name text not null,
  vendor_slug text,
  cert_name text not null,
  exam_code text not null,
  difficulty public.difficulty_level not null default 'beginner',
  details text,
  official_url text,

  status public.request_status not null default 'pending',

  reviewed_at timestamptz,
  approved_by uuid references public.users(id),
  rejected_by uuid references public.users(id),
  admin_notes text,

  created_at timestamptz not null default now()
);

create index if not exists cert_requests_status_idx on public.certification_requests(status);
create index if not exists cert_requests_user_id_idx on public.certification_requests(user_id);
create index if not exists cert_requests_vendor_name_trgm_idx on public.certification_requests using gin (vendor_name gin_trgm_ops);
create index if not exists cert_requests_exam_code_trgm_idx on public.certification_requests using gin (exam_code gin_trgm_ops);

commit;

