#!/usr/bin/env python3
"""
Scraper Google Reviews v6 — Vert'Tige 972.

Retour sur Google Maps (Search bloque avec CAPTCHA) mais SANS cliquer
sur l'onglet Avis (qui redirige). À la place :
- Charger la fiche via CID
- Consent cookies
- Scroller le panneau latéral gauche pour déclencher le lazy-load des avis
- Extraire avec des sélecteurs LARGES + fallback via texte brut du panneau
"""

import json
import signal
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

CID = "16485322727302760309"
URL = f"https://maps.google.com/?cid={CID}&hl=fr&gl=fr"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

GLOBAL_TIMEOUT_SEC = 150
DEBUG_DIR = Path("/tmp/scraper-debug")
DEBUG_DIR.mkdir(exist_ok=True)


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


signal.signal(signal.SIGALRM, lambda *_: sys.exit(3))
signal.alarm(GLOBAL_TIMEOUT_SEC)


def dump_debug(page, tag):
    try:
        page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"),
                        full_page=True, timeout=5000)
    except Exception:
        pass
    try:
        html = page.content()
        (DEBUG_DIR / f"{tag}.html").write_text(html[:400000], encoding="utf-8")
        log(f"  dump {tag}: {len(html)} chars, url={page.url[:80]}")
    except Exception:
        pass


EXTRACT_JS = r"""
() => {
  const debug = { selectors_tried: {} };

  // 1. Essai des sélecteurs de cartes review connus
  const cardSelectors = [
    '[data-review-id]',
    '.jftiEf',
    '.WMbnJf',
    'div.gws-localreviews__general-reviews-block',
    '[jsaction*="reviewChart"]',
  ];

  let cards = [];
  for (const sel of cardSelectors) {
    const found = document.querySelectorAll(sel);
    debug.selectors_tried[sel] = found.length;
    if (found.length > cards.length) {
      cards = Array.from(found);
    }
  }

  // 2. Extraction par carte
  const reviews = cards.map(c => {
    const id = c.getAttribute('data-review-id') || null;

    let name = null;
    for (const sel of ['div.d4r55', '.WNxzHc a', '.TSUbDb', 'a[href*="/contrib/"]']) {
      const el = c.querySelector(sel);
      const t = el && (el.innerText || '').trim();
      if (t && t.length < 80) { name = t; break; }
    }

    let rating = null;
    for (const el of c.querySelectorAll('span[role="img"][aria-label], span[aria-label*="/5"]')) {
      const lbl = el.getAttribute('aria-label') || '';
      const m = lbl.match(/(\d[\d,\.]*)/);
      if (m && (lbl.includes('étoile') || lbl.includes('star') || lbl.includes('/5'))) {
        rating = parseFloat(m[1].replace(',', '.'));
        break;
      }
    }

    let text = null;
    for (const sel of ['span.wiI7pd', '.MyEned span', 'div[data-expandable-section] span', 'div.Jtu6Td span']) {
      const el = c.querySelector(sel);
      const t = el && (el.innerText || '').trim();
      if (t && t.length > 3) { text = t; break; }
    }

    let date = null;
    for (const sel of ['span.rsqaWe', 'span.xRkPPb', 'span.DZSIDd', 'span.dehysf']) {
      const el = c.querySelector(sel);
      const t = el && (el.innerText || '').trim();
      if (t) { date = t; break; }
    }

    return { id, name, rating, text, date };
  }).filter(r => r.name && r.rating != null);

  return { reviews, debug };
}
"""


def scrape():
    log(f"URL: {URL}")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled",
                  "--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = browser.new_context(
            user_agent=UA, locale="fr-FR", timezone_id="Europe/Paris",
            viewport={"width": 1400, "height": 900},
        )
        ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )
        page = ctx.new_page()
        page.set_default_timeout(12000)

        log("1/5 : navigation Maps")
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=25000)
        except PWTimeout:
            log("  [!] goto timeout")
        page.wait_for_timeout(2500)

        log("2/5 : consent cookies")
        for sel in [
            'button:has-text("Tout accepter")',
            'button[aria-label*="Tout accepter"]',
            'button:has-text("Accept all")',
            'form[action*="consent"] button',
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible(timeout=1500):
                    loc.click(timeout=3000)
                    log(f"  ✓ consent via {sel!r}")
                    page.wait_for_timeout(2500)
                    break
            except Exception:
                continue

        dump_debug(page, "01-loaded")

        # Détection CAPTCHA
        if "/sorry/index" in page.url:
            log("[!] CAPTCHA détecté (sorry/index)")
            return []

        log("3/5 : attente panneau (h1)")
        try:
            page.wait_for_selector("h1", timeout=10000)
            log(f"  h1: {page.locator('h1').first.inner_text()}")
        except PWTimeout:
            log("  [!] pas de h1")

        # ─── SCROLL AGRESSIF DU PANNEAU LATÉRAL ────────────────────
        # Le panneau info Maps est à gauche. Il contient les avis en scroll infini.
        log("4/5 : scroll agressif du panneau info")

        # Trouve le panneau info (côté gauche)
        panel_selectors = [
            'div[role="main"]',
            'div.m6QErb.DxyBCb',
            'div.m6QErb.WNBkOb',
            '.aIFcqe',   # Nouveau container Maps
        ]
        panel = None
        for sel in panel_selectors:
            try:
                if page.locator(sel).count() > 0:
                    panel = sel
                    log(f"  panneau détecté: {sel!r}")
                    break
            except Exception:
                pass

        for i in range(15):
            try:
                if panel:
                    page.evaluate(
                        f"""() => {{
                            const el = document.querySelector({json.dumps(panel)});
                            if (el) el.scrollBy(0, 3000);
                        }}"""
                    )
                else:
                    page.mouse.wheel(0, 3000)
                page.wait_for_timeout(900)
                count = 0
                for s in ['[data-review-id]', '.jftiEf', '.WMbnJf']:
                    n = page.locator(s).count()
                    if n > count:
                        count = n
                log(f"  scroll {i+1}/15 → {count} cartes vues")
                if count >= 33:
                    log("  ✓ toutes les cartes chargées")
                    break
            except Exception as e:
                log(f"  scroll {i+1} exception: {e}")

        dump_debug(page, "02-after-scroll")

        log("5/5 : extraction")
        result = page.evaluate(EXTRACT_JS)
        reviews = result.get("reviews", [])
        debug = result.get("debug", {})
        log(f"  sélecteurs testés: {debug.get('selectors_tried', {})}")
        log(f"  → {len(reviews)} avis extraits")

        browser.close()
        return reviews


def main():
    log("=" * 55)
    log("Vert'Tige — Google Reviews Scraper v6 (Maps + scroll)")
    log("=" * 55)

    try:
        reviews = scrape()
    except SystemExit:
        raise
    except Exception as e:
        log(f"[FATAL] {type(e).__name__}: {e}")
        sys.exit(1)

    if not reviews:
        log("[FAIL] 0 avis")
        sys.exit(2)

    log(f"[OK] {len(reviews)} avis")
    for r in reviews[:10]:
        preview = (r.get('text') or '').replace('\n', ' ')[:70]
        log(f"  · {r['name']} ({r['rating']}★) {r.get('date','?')}: {preview}")

    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "reviews-google-raw.json").write_text(
        json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(reviews, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
