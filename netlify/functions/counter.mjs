// ══════════════════════════════════════════════════════════════════
//  Compteur public de devis envoyés via le formulaire
//  Storage : Netlify Blobs (K/V persistant, gratuit, illimité)
//  Endpoint : /api/counter
//   - GET  → { count: N }
//   - POST → incrémente et retourne { count: N+1 }
// ══════════════════════════════════════════════════════════════════

import { getStore } from "@netlify/blobs";

const SEED = 31;               // devis reçus avant l'activation du compteur
const KEY  = "devis";
const STORE_NAME = "verttige-counters";

export default async (req) => {
  const store = getStore(STORE_NAME);

  // ─── GET : lecture du compteur ───────────────────────────────
  if (req.method === "GET") {
    const current = await store.get(KEY, { type: "json" });
    return Response.json(
      { count: current?.count ?? SEED },
      {
        headers: {
          "Cache-Control": "public, max-age=30, stale-while-revalidate=60",
        },
      }
    );
  }

  // ─── POST : incrément atomique ───────────────────────────────
  if (req.method === "POST") {
    const current = await store.get(KEY, { type: "json" });
    const newCount = (current?.count ?? SEED) + 1;
    await store.setJSON(KEY, {
      count: newCount,
      updatedAt: new Date().toISOString(),
    });
    return Response.json(
      { count: newCount },
      { headers: { "Cache-Control": "no-store" } }
    );
  }

  return new Response("Method not allowed", { status: 405 });
};

export const config = {
  path: "/api/counter",
};
