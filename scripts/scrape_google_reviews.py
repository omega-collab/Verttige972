#!/usr/bin/env python3
"""
Scraper Google Reviews v5 — Vert'Tige 972.

Change de stratégie : au lieu de Google Maps (qui redirige vers un
feature ID différent), utilise l'URL de Google Search avec ludocid,
qui ouvre le knowledge panel + fragment #lrd qui déclenche le
dialogue des avis.

URL cible :
  https://www.google.com/search?q=Abattage+Elagage+Vert+Tige+Martinique
  &hl=fr&gl=fr#lrd=0x8c6add01ef4e4deb:0xe4b5e93c13c428b5,1

Fragment #lrd=<feature_id>,1 → ouvre le dialogue "Reviews" au chargement.
"""

import json
import signal
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# URL Search (pas Maps) — même URL que le bouton "Voir 29 avis" du site
SEARCH_URL = (
    "https://www.google.com/search"
    "?q=Abattage+%C3%89lagage+Vert+Tige+Martinique"
    "&ludocid=16485322727302760309"
    "&hl=fr&gl=fr"
    "#lrd=0x8c6add01ef4e4deb:0xe4b5e93c13c428b5,1,,,,"
)

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
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
        log(f"  screenshot: {tag}.png")
    except Exception as e:
        log(f"  [!] screenshot fail: {e}")
    try:
        html = page.content()
        (DEBUG_DIR / f"{tag}.html").write_text(html[:300000], encoding="utf-8")
        log(f"  html: {tag}.html ({len(html)} chars)")
    except Exception:
        pass
    try:
        log(f"  URL: {page.url}")
        log(f"  title: {page.title()}")
    except Exception:
        pass


# JS d'extraction adapté au dialogue Reviews de Google Search
EXTRACT_JS = r"""
() => {
  const out = [];

  // Sélecteurs possibles pour les cartes review dans le dialogue Google Search
  const cardSelectors = [
    'div[data-review-id]',
    'div.gws-localreviews__general-reviews-block',
    '.WMbnJf',
    '.jftiEf',
  ];
  let cards = [];
  for (const sel of cardSelectors) {
    const found = document.querySelectorAll(sel);
    if (found.length > 0) { cards = Array.from(found); break; }
  }

  cards.forEach(c => {
    const id = c.getAttribute('data-review-id') || null;

    // Auteur : cherche un lien vers /contrib/ ou un div avec le nom
    let name = null;
    const nameEls = c.querySelectorAll(
      'a.yC3ZMb, div.TSUbDb, .d4r55, a[href*="/contrib/"] span, a[href*="/contrib/"] div'
    );
    for (const el of nameEls) {
      const t = (el.innerText || '').trim();
      if (t && t.length < 80) { name = t; break; }
    }

    // Note
    let rating = null;
    const starEls = c.querySelectorAll(
      'span[role="img"][aria-label], span[aria-label*="/5"], .Fam1ne'
    );
    for (const el of starEls) {
      const lbl = el.getAttribute('aria-label') || '';
      const m = lbl.match(/(\d[\d,\.]*)/);
      if (m && (lbl.includes('étoile') || lbl.includes('star') || lbl.includes('/5'))) {
        rating = parseFloat(m[1].replace(',', '.'));
        break;
      }
    }

    // Texte
    let text = null;
    for (const el of c.querySelectorAll('span.review-full-text, span.wiI7pd, .Jtu6Td span, .review-snippet')) {
      const t = (el.innerText || '').trim();
      if (t && t.length > 3) { text = t; break; }
    }

    // Date
    let date = null;
    for (const el of c.querySelectorAll('span.dehysf, .rsqaWe, .xRkPPb, .DZSIDd')) {
      const t = (el.innerText || '').trim();
      if (t) { date = t; break; }
    }

    if (name && rating != null) {
      out.push({ id, name, rating, text, date });
    }
  });

  return out;
}
"""


def scrape():
    log(f"URL: {SEARCH_URL}")
    log(f"Budget global: {GLOBAL_TIMEOUT_SEC}s")

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
        page.set_default_timeout(15000)

        log("Étape 1/4 : navigation vers Google Search")
        try:
            page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=25000)
        except PWTimeout:
            log("  [!] goto timeout")

        page.wait_for_timeout(2000)
        log(f"  URL après goto: {page.url}")

        # Consent cookies
        log("Étape 2/4 : consent cookies (Google Search)")
        for sel in [
            'button:has-text("Tout accepter")',
            'button[aria-label*="Tout accepter"]',
            'button:has-text("Accept all")',
            '#L2AGLb',                    # bouton consent Google standard
            'button[jsname="tWT92d"]',    # variante
        ]:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible(timeout=1500):
                    loc.click(timeout=3000)
                    log(f"  ✓ consent cliqué via {sel!r}")
                    page.wait_for_timeout(2500)
                    break
            except Exception:
                continue

        dump_debug(page, "01-after-consent")

        # Le fragment #lrd doit déclencher le dialogue reviews.
        # Attente que quelque chose ressemblant à des reviews apparaisse.
        log("Étape 3/4 : attente du dialogue reviews")

        selectors_to_wait = [
            'div[data-review-id]',
            '.gws-localreviews__general-reviews-block',
            '.WMbnJf',
            '.review-dialog-list',
        ]

        found_selector = None
        for sel in selectors_to_wait:
            try:
                page.wait_for_selector(sel, timeout=6000)
                found_selector = sel
                log(f"  ✓ trouvé: {sel!r}")
                break
            except PWTimeout:
                log(f"  ✗ pas trouvé: {sel!r}")

        dump_debug(page, "02-after-wait")

        # Scroll dans le dialogue si trouvé
        log("Étape 4/4 : scroll & extract")
        if found_selector:
            # Trouve le conteneur scrollable du dialogue
            try:
                for i in range(6):
                    page.evaluate("""() => {
                      const dialog = document.querySelector('.review-dialog-list, .gws-localreviews__general-reviews-block, div[role="dialog"] div[jscontroller]');
                      if (dialog) dialog.scrollBy(0, 3000);
                      else window.scrollBy(0, 2000);
                    }""")
                    page.wait_for_timeout(1200)
                    count = 0
                    for sel in ['div[data-review-id]', '.WMbnJf', '.jftiEf']:
                        c = page.locator(sel).count()
                        if c > count:
                            count = c
                    log(f"  scroll {i+1}: {count} cartes visibles")
            except Exception as e:
                log(f"  [!] scroll exception: {e}")

        dump_debug(page, "03-final")

        reviews = page.evaluate(EXTRACT_JS)
        log(f"→ {len(reviews)} avis extraits")

        browser.close()
        return reviews


def main():
    log("=" * 55)
    log("Vert'Tige — Google Reviews Scraper v5 (Search)")
    log("=" * 55)

    try:
        reviews = scrape()
    except SystemExit:
        raise
    except Exception as e:
        log(f"[FATAL] {type(e).__name__}: {e}")
        sys.exit(1)

    if not reviews:
        log("[FAIL] aucun avis extrait")
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
