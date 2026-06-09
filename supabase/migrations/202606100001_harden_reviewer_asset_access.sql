-- Version-controlled access boundary for the public desktop reviewer client.
-- Apply with the Supabase CLI or dashboard before a public review period.

alter table public.songs enable row level security;
alter table public.asset_objects enable row level security;
alter table public.model_artifacts enable row level security;
alter table public.user_preferences enable row level security;

revoke all on table public.songs from anon;
revoke all on table public.asset_objects from anon;
revoke all on table public.model_artifacts from anon;
revoke all on table public.user_preferences from anon;

grant select on table public.songs to authenticated;
grant select on table public.asset_objects to authenticated;
grant select on table public.model_artifacts to authenticated;
grant select, insert, update on table public.user_preferences to authenticated;

drop policy if exists reviewer_reads_active_songs on public.songs;
create policy reviewer_reads_active_songs
on public.songs
for select
to authenticated
using (is_active is true);

drop policy if exists reviewer_reads_active_model_artifacts on public.model_artifacts;
create policy reviewer_reads_active_model_artifacts
on public.model_artifacts
for select
to authenticated
using (status = 'active');

drop policy if exists reviewer_reads_active_asset_metadata on public.asset_objects;
create policy reviewer_reads_active_asset_metadata
on public.asset_objects
for select
to authenticated
using (
  exists (
    select 1
    from public.songs
    where songs.id = asset_objects.song_id
      and songs.is_active is true
  )
  or exists (
    select 1
    from public.model_artifacts
    where model_artifacts.asset_object_id = asset_objects.id
      and model_artifacts.status = 'active'
  )
);

drop policy if exists users_read_own_preferences on public.user_preferences;
create policy users_read_own_preferences
on public.user_preferences
for select
to authenticated
using (auth.uid() = user_id);

drop policy if exists users_insert_own_preferences on public.user_preferences;
create policy users_insert_own_preferences
on public.user_preferences
for insert
to authenticated
with check (auth.uid() = user_id);

drop policy if exists users_update_own_preferences on public.user_preferences;
create policy users_update_own_preferences
on public.user_preferences
for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

create or replace function public.authorize_asset_object_access(
  p_bucket_name text,
  p_object_key text,
  p_asset_group text
)
returns boolean
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  select
    auth.uid() is not null
    and case p_asset_group
      when 'music' then exists (
        select 1
        from public.asset_objects ao
        join public.songs s on s.id = ao.song_id
        where ao.bucket_name = p_bucket_name
          and ao.object_key = p_object_key
          and s.is_active is true
      )
      when 'models' then exists (
        select 1
        from public.asset_objects ao
        join public.model_artifacts ma on ma.asset_object_id = ao.id
        where ao.bucket_name = p_bucket_name
          and ao.object_key = p_object_key
          and ma.status = 'active'
      )
      else false
    end;
$$;

revoke all on function public.authorize_asset_object_access(text, text, text) from public;
revoke all on function public.authorize_asset_object_access(text, text, text) from anon;
grant execute on function public.authorize_asset_object_access(text, text, text) to authenticated;
