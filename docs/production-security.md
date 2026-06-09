# Production Security Checklist

This project treats desktop clients as public clients. Anything shipped in the
app, `.env`, or installer can be copied from a reverse-engineered build.

## Enforced In Code

- R2 API credentials are never shipped to the desktop client.
- The Cloudflare Worker owns private R2 bucket bindings.
- Every asset request requires a valid Supabase bearer token.
- The Worker checks Supabase metadata before serving an object key.
- Supabase RLS policies and the Worker authorization RPC are version-controlled
  under `supabase/migrations/`.
- Unknown or inactive object keys return `403` before R2 is read.
- Malformed object keys return `400`.
- No-token requests return `401`.
- A missing or failing rate-limiter binding fails closed with `503`.
- Music and model objects over 64 MiB are rejected before streaming.
- Worker observability and structured denial/rate-limit logs are enabled.
- Cloudflare Worker rate limiting is enabled:
  - pre-auth IP/key group: 90 requests per 60 seconds
  - authenticated music assets: 120 requests per user per 60 seconds
  - authenticated model assets: 6 requests per user per 60 seconds
- Runtime model downloads are enabled only through the same authenticated,
  authorized Worker path and are limited to 6 requests per user per minute.

## Required Provider Settings Before Public Launch

Enable these in the provider dashboards before advertising the app publicly:

- Supabase Auth email confirmations.
- Supabase Auth CAPTCHA protection with Cloudflare Turnstile or hCaptcha.
- Supabase Auth rate limits tuned for public traffic.
- A custom SMTP provider if email confirmation volume needs more than the
  built-in email quota.
- Cloudflare billing notifications and usage alerts.
- Cloudflare WAF/rate limiting rules in front of the Worker route if the app
  moves to a custom domain.

Supabase Auth CAPTCHA and email confirmation must be enforced by Supabase itself.
Client-side CAPTCHA alone is not sufficient because a public client exposes the
Supabase publishable key and can be bypassed.

For a frictionless supervised demo, email confirmation can be disabled
temporarily, but that increases automated-signup risk. Check the live Auth
setting before every public review period.

## Model Access

The desktop app reads the active model manifest from Supabase, downloads only
the FER and heart-rate runtime models, verifies registered byte sizes and
SHA-256 checksums, and caches them outside the repository. It uses a fixed
heart-rate output-label order rather than deserializing the legacy label
encoder.

## Remaining Risk

No public client can make a publishable key secret. A bad actor can still see
the Supabase project URL, publishable key, Worker URL, and route shapes.
Authorized reviewers can also copy any media or model delivered to their
desktop; this design is an access-control boundary, not DRM.

Cloudflare's Worker rate-limit bindings reduce ordinary abuse but are not a
hard billing ceiling against distributed users or many valid accounts. Keep
provider billing alerts and account-level spend controls enabled, and only
publish media the project is licensed to distribute to authenticated reviewers.
