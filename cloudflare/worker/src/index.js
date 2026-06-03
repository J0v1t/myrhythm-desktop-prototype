const MUSIC_PREFIX = "/assets/music/";
const MODEL_PREFIX = "/assets/models/";

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(env) });
    }

    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/health") {
      return json({ ok: true, service: "myrhythm-assets-api" }, 200, env);
    }

    if (request.method !== "GET") {
      return json({ error: "method_not_allowed" }, 405, env);
    }

    const route = resolveAssetRoute(url.pathname, env);
    if (route?.error) {
      return json({ error: route.error }, 400, env);
    }
    if (!route) {
      return json({ error: "not_found" }, 404, env);
    }

    const authResult = await validateSupabaseToken(request, env);
    if (!authResult.ok) {
      return json({ error: authResult.error }, 401, env);
    }

    const object = await route.bucket.get(route.key);
    if (!object) {
      return json({ error: "asset_not_found" }, 404, env);
    }

    return new Response(object.body, {
      headers: {
        ...corsHeaders(env),
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
        "Content-Length": String(object.size),
        "Cache-Control": route.cacheControl,
      },
    });
  },
};

export function resolveAssetRoute(pathname, env) {
  if (pathname.startsWith(MUSIC_PREFIX)) {
    const key = safeObjectKey(pathname.slice(MUSIC_PREFIX.length));
    if (!key) {
      return { error: "invalid_object_key" };
    }

    return {
      bucket: env.MUSIC_ASSETS,
      key,
      cacheControl: "private, max-age=300",
    };
  }

  if (pathname.startsWith(MODEL_PREFIX)) {
    const key = safeObjectKey(pathname.slice(MODEL_PREFIX.length));
    if (!key) {
      return { error: "invalid_object_key" };
    }

    return {
      bucket: env.ML_MODELS,
      key,
      cacheControl: "private, no-store",
    };
  }

  return null;
}

export function safeObjectKey(rawKey) {
  let key = "";
  try {
    key = decodeURIComponent(rawKey || "").trim();
  } catch {
    return null;
  }
  if (!key || key.startsWith("/") || key.includes("..")) {
    return null;
  }
  return key;
}

export async function validateSupabaseToken(request, env) {
  const authHeader = request.headers.get("Authorization") || "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7).trim() : "";
  if (!token) {
    return { ok: false, error: "missing_bearer_token" };
  }

  if (!env.SUPABASE_URL || !env.SUPABASE_PUBLIC_KEY) {
    return { ok: false, error: "supabase_not_configured" };
  }

  const baseUrl = normalizeSupabaseUrl(env.SUPABASE_URL);
  const response = await fetch(`${baseUrl}/auth/v1/user`, {
    headers: {
      apikey: env.SUPABASE_PUBLIC_KEY,
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    return { ok: false, error: "invalid_supabase_session" };
  }

  return { ok: true };
}

export function normalizeSupabaseUrl(url) {
  let cleaned = String(url || "").trim().replace(/\/+$/, "");
  for (const suffix of ["/rest/v1", "/auth/v1"]) {
    if (cleaned.endsWith(suffix)) {
      cleaned = cleaned.slice(0, -suffix.length);
    }
  }
  return cleaned;
}

function json(payload, status, env) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      ...corsHeaders(env),
      "Content-Type": "application/json",
    },
  });
}

function corsHeaders(env) {
  return {
    "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
  };
}
