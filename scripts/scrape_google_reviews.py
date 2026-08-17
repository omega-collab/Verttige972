#!/usr/bin/env python3
"""
Scraper Google Reviews pour Vert'Tige 972.

Cible l'endpoint interne Google Maps `/maps/rpc/listentitiesreviews`
qui retourne les avis d'un lieu par son Feature ID.

Feature ID Vert'Tige : 0x8c6add01ef4e4deb:0xe4b5e93c13c428b5
- High : 10118824195470638059
- Low  : 16485322727302760309 (= ludocid)

Usage :
    python3 scrape_google_reviews.py

Sortie :
    - stdout : résumé + JSON des avis extraits
    - fichier data/reviews-google.json (si scrape réussi)
"""

import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────
FEATURE_HIGH = "10118824195470638059"   # 0x8c6add01ef4e4deb
FEATURE_LOW  = "16485322727302760309"   # 0xe4b5e93c13c428b5
MAX_REVIEWS  = 50                        # on demande 50 avis à Google
LANG         = "fr"
COUNTRY      = "fr"

# URL de l'endpoint (RPC interne Google Maps)
# Params :
#   !1m2!1yHIGH!2yLOW   → Feature ID du lieu
#   !2m2!1i0!2i50        → offset 0, limit 50
#   !3e1                 → sort : plus récent d'abord
#   !4m5!3b1!4b1!5b1!6b1!7b1 → include: rating, text, author, date, ...
#   !5m2!1sxxx!7e81      → session identifier (aléatoire OK)
URL_TEMPLATE = (
    "https://www.google.com/maps/rpc/listentitiesreviews"
    "?authuser=0&hl={lang}&gl={gl}"
    "&pb=!1m2!1y{high}!2y{low}"
    "!2m2!1i0!2i{limit}!3e1"
    "!4m5!3b1!4b1!5b1!6b1!7b1"
    "!5m2!1sscraper!7e81"
)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def fetch_google_reviews():
    """Récupère la réponse brute de l'endpoint Google Maps."""
    url = URL_TEMPLATE.format(
        high=FEATURE_HIGH, low=FEATURE_LOW,
        limit=MAX_REVIEWS, lang=LANG, gl=COUNTRY,
    )
    print(f"[*] Fetching: {url[:120]}...", file=sys.stderr)

    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/maps/",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            print(f"[*] HTTP {resp.status} — {len(raw)} bytes", file=sys.stderr)
            return raw
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP error {e.code}: {e.reason}", file=sys.stderr)
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"[!] Body: {body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] Fetch error: {e}", file=sys.stderr)
        return None


def parse_google_response(raw):
    """
    La réponse Google commence par `)]}'` puis contient un tableau JSON imbriqué.
    Les avis sont dans data[2] (liste de reviews).
    Chaque review est un array : [id, [author_info], rating, text, ...]
    """
    if not raw:
        return []

    # Retire le préfixe anti-XSSI de Google
    raw = raw.lstrip(")]}'\n\r ")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[!] JSON decode error: {e}", file=sys.stderr)
        print(f"[!] First 300 chars: {raw[:300]}", file=sys.stderr)
        return []

    # Structure typique : data = [meta, ?, [reviews_list], ...]
    # On explore pour trouver la liste des reviews (heuristique)
    reviews = []

    def walk(obj, depth=0):
        """Explore récursivement pour trouver les structures qui ressemblent à des reviews."""
        if depth > 8:
            return
        if isinstance(obj, list):
            # Heuristique : une review a typiquement [id_str, [author...], rating_int, text_str, ...]
            if (len(obj) >= 4
                and isinstance(obj[0], str) and len(obj[0]) > 10
                and isinstance(obj[1], list)):
                # Tentative d'extraction
                r = extract_review(obj)
                if r:
                    reviews.append(r)
                    return
            for item in obj:
                walk(item, depth + 1)

    walk(data)
    return reviews


def extract_review(review_array):
    """Extrait les champs d'un avis à partir de sa structure brute."""
    try:
        review_id = review_array[0] if isinstance(review_array[0], str) else None

        # Author info : souvent review[1][4] = nom, review[1][0][0] = url photo
        author_name = None
        if isinstance(review_array[1], list):
            author = review_array[1]
            # Cherche un nom lisible dans l'array author
            for x in author:
                if isinstance(x, str) and 2 < len(x) < 80 and not x.startswith("http"):
                    author_name = x
                    break
                if isinstance(x, list):
                    for y in x:
                        if isinstance(y, str) and 2 < len(y) < 80 and not y.startswith("http"):
                            author_name = y
                            break
                    if author_name:
                        break

        # Rating : chercher un int entre 1 et 5
        rating = None
        text = None
        date_relative = None
        for item in review_array[2:]:
            if isinstance(item, int) and 1 <= item <= 5 and rating is None:
                rating = item
            elif isinstance(item, str) and len(item) > 20 and text is None:
                text = item
            elif isinstance(item, list):
                for sub in item:
                    if isinstance(sub, str) and ("il y a" in sub.lower() or "ago" in sub.lower()):
                        date_relative = sub
                        break

        if not author_name or rating is None:
            return None

        return {
            "id": review_id,
            "author": author_name,
            "rating": rating,
            "text": text,
            "date_relative": date_relative,
        }
    except Exception:
        return None


def main():
    print("=" * 60, file=sys.stderr)
    print("Vert'Tige 972 — Google Reviews Scraper — Phase 1 test", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    raw = fetch_google_reviews()
    if raw is None:
        print("\n[FAIL] Requête bloquée ou erreur réseau", file=sys.stderr)
        sys.exit(1)

    reviews = parse_google_response(raw)
    print(f"\n[*] Avis extraits : {len(reviews)}", file=sys.stderr)

    if not reviews:
        print("\n[FAIL] Aucun avis parsé — Google a probablement retourné", file=sys.stderr)
        print("       une page CAPTCHA ou une structure inattendue.", file=sys.stderr)
        # Dump un extrait de la réponse pour debug
        print("\n[DEBUG] Extrait raw (500 premiers chars) :", file=sys.stderr)
        print(raw[:500] if raw else "(vide)", file=sys.stderr)
        sys.exit(2)

    # Affiche les avis (stdout — sera capté par le workflow)
    print(json.dumps(reviews, ensure_ascii=False, indent=2))

    # Persiste dans data/
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "reviews-google-raw.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Écrit : {out_file}", file=sys.stderr)

    # Résumé lisible
    print(f"\n[SUCCESS] {len(reviews)} avis récupérés", file=sys.stderr)
    for r in reviews[:5]:
        print(f"  - {r['author']} ({r['rating']}/5) : "
              f"{(r['text'] or '')[:60]}...", file=sys.stderr)


if __name__ == "__main__":
    main()
