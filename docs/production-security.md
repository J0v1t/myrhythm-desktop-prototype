# Production Security Checklist

This project treats desktop clients as public clients. Anything shipped in the
app, `.env`, or installer can be copied from a reverse-engineered build.

## Enforced In Code

- R2 API credentials are never shipped to the desktop client.
- The Cloudflare Worker owns private R2 bucket bindings.
- Every asset request requires a valid Supabase bearer token.
- The Worker checks Supabase metadata before serving an object key.
- Unknown or inactive object keys return `403` before R2 is read.
- Malformed object keys return `400`.
- No-token requests return `401`.
- Cloudflare Worker rate limiting is enabled:
  - pre-auth IP/key group: 90 requests per 60 seconds
  - authenticated music assets: 120 requests per user per 60 seconds
  - authenticated model assets: 6 requests per user per 60 seconds
- Model downloads are disabled by default with `ALLOW_MODEL_DOWNLOADS = "false"`.

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

## Model Access

The model artifacts are uploaded to R2 and recorded in Supabase metadata, but
the Worker blocks model downloads unless `ALLOW_MODEL_DOWNLOADS` is set to
`"true"` and redeployed. Keep this disabled for public demos unless the desktop
app has a real model-update workflow and the usage budget can absorb downloads.

## Remaining Risk

No public client can make a publishable key secret. A bad actor can still see
the Supabase project URL, publishable key, Worker URL, and route shapes. The
security goal is to make those values low-privilege and enforce authorization,
rate limits, and cost controls on the provider side.
