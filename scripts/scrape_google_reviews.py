#!/usr/bin/env python3
"""
Scraper Google Reviews v3 — Vert'Tige 972.

Playwright headless avec BUDGET TEMPS STRICT (90 sec max) et logs
détaillés à chaque étape pour éviter les hangs silencieux.

Stratégie :
1. Naviguer vers Google Maps via CID
2. Passer le consent cookies au plus vite
3. Cliquer l'onglet Avis
4. Scroller pour charger les avis
5. Extraire — TOUJOURS écrire artefacts debug avant de sortir
"""

import json
import signal
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

CID = "16485322727302760309"
URL = f"https://maps.google.com/?cid={CID}&hl=fr&gl=fr"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

GLOBAL_TIMEOUT_SEC = 180
STEP_TIMEOUT_MS   = 10000
DEBUG_DIR = Path("/tmp/scraper-debug")
DEBUG_DIR.mkdir(exist_ok=True)


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def timeout_handler(signum, frame):
    log("[!] GLOBAL TIMEOUT hit — sauvegarde debug & exit")
    sys.exit(3)


signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(GLOBAL_TIMEOUT_SEC)


def dump_debug(page, tag):
    """Screenshot + HTML + URL courante."""
    try:
        page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"), full_page=True, timeout=5000)
        log(f"  screenshot: {tag}.png")
    except Exception as e:
        log(f"  [!] screenshot fail: {e}")
    try:
        html = page.content()
        (DEBUG_DIR / f"{tag}.html").write_text(html[:200000], encoding="utf-8")
        log(f"  html: {tag}.html ({len(html)} chars)")
    except Exception as e:
        log(f"  [!] html dump fail: {e}")
    try:
        log(f"  URL: {page.url}")
        log(f"  title: {page.title()}")
    except Exception:
        pass


def try_click(page, selectors, label, wait_ms=3000):
    """Essaie plusieurs sélecteurs, retourne True au premier qui marche."""
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            if loc.is_visible(timeout=1500):
                loc.click(timeout=wait_ms)
                log(f"  ✓ '{label}' cliqué via {sel!r}")
                return True
        except Exception:
            continue
    log(f"  ✗ '{label}' — aucun sélecteur ne match")
    return False


EXTRACT_JS = r"""
() => {
  const cards = document.querySelectorAll('[data-review-id]');
  const out = [];
  cards.forEach(c => {
    const id = c.getAttribute('data-review-id');
    let name = null;
    for (const el of c.querySelectorAll('div.d4r55, .WNxzHc a, button[jsaction*="reviewer"] div')) {
      const t = (el.innerText || '').trim();
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
    for (const el of c.querySelectorAll('span.wiI7pd, .MyEned span, div[data-expandable-section] span')) {
      const t = (el.innerText || '').trim();
      if (t && t.length > 3) { text = t; break; }
    }
    let date = null;
    for (const el of c.querySelectorAll('span.rsqaWe, span.xRkPPb, span.DZSIDd')) {
      const t = (el.innerText || '').trim();
      if (t) { date = t; break; }
    }
    if (name && rating != null) out.push({ id, name, rating, text, date });
  });
  return out;
}
"""


def scrape():
    log(f"URL: {URL}")
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
        page.set_default_timeout(STEP_TIMEOUT_MS)

        # 1. Navigate
        log("Étape 1/5 : navigation")
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=20000)
        except PWTimeout:
            log("  [!] goto timeout (on continue quand même)")

        # Redirect logging
        page.wait_for_timeout(1500)
        log(f"  URL après goto: {page.url}")

        # 2. Cookie consent
        log("Étape 2/5 : consent cookies")
        clicked = try_click(page, [
            'button[aria-label*="Tout accepter"]',
            'button:has-text("Tout accepter")',
            'button:has-text("Accept all")',
            'button[aria-label*="Accept all"]',
            'form[action*="consent"] button',
        ], "Cookie accept", wait_ms=3000)
        if clicked:
            page.wait_for_timeout(2000)

        dump_debug(page, "01-after-consent")

        # 3. Wait for h1
        log("Étape 3/5 : attente h1")
        try:
            page.wait_for_selector("h1", timeout=10000)
            log(f"  h1: {page.locator('h1').first.inner_text()}")
        except PWTimeout:
            log("  [!] pas de h1")

        # 4. Try clicking reviews tab
        log("Étape 4/5 : ouvrir onglet avis")
        try_click(page, [
            'button[jsaction*="reviewChart"]',
            'button[aria-label*="Avis"]',
            'button[aria-label*="avis"]',
            'button[aria-label*="Reviews"]',
            'button:has-text("avis")',
            'a[href*="reviews"]',
        ], "Onglet avis", wait_ms=3000)
        page.wait_for_timeout(2500)

        dump_debug(page, "02-after-reviews-click")

        # 5. Scroll + extract
        log("Étape 5/5 : scroll & extract")
        # Attendre au moins une review card
        try:
            page.wait_for_selector('[data-review-id]', timeout=8000)
            log("  ✓ [data-review-id] détecté")
        except PWTimeout:
            log("  [!] aucun [data-review-id] visible")

        # Compte initial
        initial = page.locator('[data-review-id]').count()
        log(f"  reviews initiales dans DOM: {initial}")

        # Scroll (max 8 fois, arrête si count stable 2 fois)
        prev = initial
        stable = 0
        for i in range(8):
            try:
                page.evaluate("""() => {
                  const feed = document.querySelector('div[role="feed"]') ||
                               document.querySelector('div.m6QErb.DxyBCb');
                  if (feed) feed.scrollBy(0, 5000);
                  else window.scrollBy(0, 5000);
                }""")
            except Exception:
                pass
            page.wait_for_timeout(1200)
            cur = page.locator('[data-review-id]').count()
            log(f"  scroll {i+1}: {cur} reviews")
            if cur == prev:
                stable += 1
                if stable >= 2:
                    log("  → count stable, arrêt scroll")
                    break
            else:
                stable = 0
            prev = cur

        dump_debug(page, "03-after-scroll")

        # Extract
        log("Extraction JS...")
        reviews = page.evaluate(EXTRACT_JS)
        log(f"→ {len(reviews)} avis extraits")

        browser.close()
        return reviews


def main():
    log("=" * 55)
    log("Vert'Tige — Google Reviews Scraper v3")
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
        # Le workflow uploadera quand même /tmp/scraper-debug
        sys.exit(2)

    log(f"[OK] {len(reviews)} avis")
    for r in reviews[:8]:
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
