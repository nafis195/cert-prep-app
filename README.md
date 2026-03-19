# cert-prep-app

## Certification Preparation Application

## Database setup (PostgreSQL)

SQL files live in `db/` and are designed to match your ERD plus the required fields:

- `db/00_extensions.sql`
- `db/01_schema.sql`
- `db/02_security_functions.sql`
- `db/03_rls_policies.sql`
- `db/04_triggers.sql`

Run them in order on your Postgres database.

Example:

```bash
psql "$DATABASE_URL" -f db/00_extensions.sql
psql "$DATABASE_URL" -f db/01_schema.sql
psql "$DATABASE_URL" -f db/02_security_functions.sql
psql "$DATABASE_URL" -f db/03_rls_policies.sql
psql "$DATABASE_URL" -f db/04_triggers.sql
```

### RLS note (important)

The RLS policies use a session setting `app.user_id`. Your backend must set this per request/connection:

```sql
select set_config('app.user_id', '<current-user-uuid>', true);
```

If you later move to Supabase, we can switch `public.current_user_id()` to `auth.uid()` and drop the `users` table.
