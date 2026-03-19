-- Experimental seed data for local development
-- Inserts vendors + a few certifications.
-- Run as a DB superuser (or role with BYPASSRLS) because vendors/certifications
-- inserts are protected by RLS/admin policies.

begin;

insert into public.vendors (slug, name, description)
values
  ('aws', 'AWS', 'Amazon Web Services certifications')
on conflict (slug) do nothing;

insert into public.vendors (slug, name, description)
values
  ('azure', 'Microsoft Azure', 'Azure certifications')
on conflict (slug) do nothing;

insert into public.vendors (slug, name, description)
values
  ('cisco', 'Cisco', 'Cisco certifications')
on conflict (slug) do nothing;

insert into public.vendors (slug, name, description)
values
  ('oracle', 'Oracle', 'Oracle certifications')
on conflict (slug) do nothing;

insert into public.vendors (slug, name, description)
values
  ('gcp', 'Google Cloud', 'Google Cloud certifications')
on conflict (slug) do nothing;

-- AWS
insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'AWS Certified Solutions Architect - Associate',
  'SAA-C03',
  'intermediate',
  'Design secure, resilient, and cost-optimized AWS architectures.',
  'This certification validates your ability to design solutions on AWS with best practices for security and scalability.',
  'https://aws.amazon.com/certification/certified-solutions-architect-associate/',
  true
from public.vendors v
where v.slug = 'aws'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = 'SAA-C03'
  );

insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'AWS Certified Cloud Practitioner',
  'CLF-C02',
  'beginner',
  'Fundamentals of AWS cloud concepts and services.',
  'Covers core AWS concepts, basic pricing, architecture, security, and support.',
  'https://aws.amazon.com/certification/certified-cloud-practitioner/',
  true
from public.vendors v
where v.slug = 'aws'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = 'CLF-C02'
  );

-- Azure
insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'Microsoft Azure Administrator Associate',
  'AZ-104',
  'intermediate',
  'Manage identity, governance, storage, compute, and virtual networks in Azure.',
  'Validates skills for implementing, managing, and monitoring Azure services.',
  'https://learn.microsoft.com/en-us/credentials/certifications/',
  true
from public.vendors v
where v.slug = 'azure'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = 'AZ-104'
  );

-- Cisco
insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'Cisco Certified Network Associate',
  '200-301',
  'beginner',
  'Install, operate, and troubleshoot routed and switched networks.',
  'Covers networking fundamentals, IP services, security, automation concepts, and troubleshooting.',
  'https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/ccna.html',
  true
from public.vendors v
where v.slug = 'cisco'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = '200-301'
  );

-- Oracle
insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'Oracle Cloud Infrastructure Foundations Associate',
  '1Z0-1072-24',
  'beginner',
  'OCI cloud fundamentals and core services.',
  'Covers the foundations of Oracle Cloud Infrastructure and key concepts required for further OCI certifications.',
  'https://education.oracle.com/',
  true
from public.vendors v
where v.slug = 'oracle'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = '1Z0-1072-24'
  );

-- GCP
insert into public.certifications (
  vendor_id, name, exam_code, difficulty, summary, description, official_url, is_active
)
select
  v.id,
  'Google Cloud Associate Cloud Engineer',
  'ACE',
  'intermediate',
  'Deploy, monitor, and manage solutions on Google Cloud.',
  'Validates hands-on skills with GCP including deployment, monitoring, and operational best practices.',
  'https://cloud.google.com/certification',
  true
from public.vendors v
where v.slug = 'gcp'
  and not exists (
    select 1 from public.certifications c
    where c.vendor_id = v.id and c.exam_code = 'ACE'
  );

commit;

