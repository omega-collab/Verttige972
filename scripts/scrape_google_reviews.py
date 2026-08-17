#!/usr/bin/env python3
"""
Scraper Google Reviews (Playwright) — Vert'Tige 972.

Approche : lance Chromium headless, ouvre la fiche Google Maps du lieu,
clique sur l'onglet Avis, trie par date récente, scroll pour charger
tous les avis, extrait du DOM.

CID Vert'Tige : 16485322727302760309
URL directe : https://maps.google.com/?cid=<CID>&hl=fr&gl=fr
"""

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

CID = "16485322727302760309"
URL = f"https://maps.google.com/?cid={CID}&hl=fr&gl=fr"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

MAX_SCROLLS = 30      # combien de fois on scroll pour charger de nouveaux avis
SCROLL_PAUSE = 1.2    # secondes entre chaque scroll


def log(msg):
    print(f"[scraper] {msg}", file=sys.stderr, flush=True)


def try_accept_cookies(page):
    """Google affiche une popup de consentement cookies au premier chargement."""
    selectors = [
        'button:has-text("Tout accepter")',
        'button:has-text("Accept all")',
        'button[aria-label*="Accepter tout"]',
        'button[aria-label*="Accept all"]',
        'form[action*="consent"] button:nth-child(2)',
    ]
    for sel in selectors:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=2000):
                btn.click()
                log(f"Cookies acceptés via '{sel}'")
                page.wait_for_timeout(1500)
                return True
        except PlaywrightTimeout:
            continue
        except Exception:
            continue
    log("Aucune popup cookies détectée (ou déjà passée)")
    return False


def click_reviews_tab(page):
    """Clique sur l'onglet Avis / bouton 'Voir tous les avis'."""
    selectors = [
        'button[aria-label*="Avis pour"]',
        'button[aria-label*="Reviews for"]',
        'button[jsaction*="reviewChart"]',
        'button:has-text("avis")',
        'button:has-text("reviews")',
        'a:has-text("Voir tous les avis")',
    ]
    for sel in selectors:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=3000):
                btn.click()
                log(f"Onglet avis ouvert via '{sel}'")
                page.wait_for_timeout(2000)
                return True
        except Exception:
            continue
    log("[!] Onglet avis non trouvé — peut-être déjà sur la page reviews")
    return False


def sort_by_newest(page):
    """Tente de trier les avis par 'Les plus récents'."""
    try:
        # Bouton de tri (souvent 'Les plus pertinents' par défaut)
        sort_btn = page.locator('button[aria-label*="Trier"], button:has-text("Trier"), button:has-text("Sort")').first
        sort_btn.click(timeout=5000)
        page.wait_for_timeout(800)

        # Option "Les plus récents"
        newest = page.locator('div[role="menuitemradio"]:has-text("récents"), div[role="menuitem"]:has-text("récents"), div:has-text("Les plus récents")').first
        newest.click(timeout=3000)
        log("Tri par plus récents appliqué")
        page.wait_for_timeout(2000)
        return True
    except Exception as e:
        log(f"[!] Tri non appliqué: {e}")
        return False


def find_scrollable_feed(page):
    """Trouve le conteneur scrollable des avis."""
    candidates = [
        'div[role="feed"]',
        'div.m6QErb.DxyBCb.kA9KIf',
        'div.review-dialog-list',
    ]
    for sel in candidates:
        try:
            el = page.locator(sel).first
            if el.count() > 0:
                return el
        except Exception:
            continue
    return None


def scroll_reviews(page, max_scrolls=MAX_SCROLLS):
    """Scroll le conteneur d'avis pour déclencher le lazy load."""
    scrollable = find_scrollable_feed(page)
    if not scrollable:
        log("[!] Conteneur scrollable non trouvé — fallback scroll page")
        for i in range(max_scrolls):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(int(SCROLL_PAUSE * 1000))
        return

    prev_count = 0
    stable = 0
    for i in range(max_scrolls):
        try:
            scrollable.evaluate('el => el.scrollBy(0, 3000)')
        except Exception:
            page.mouse.wheel(0, 3000)
        page.wait_for_timeout(int(SCROLL_PAUSE * 1000))

        try:
            count = page.locator('[data-review-id]').count()
        except Exception:
            count = 0
        log(f"Scroll {i+1}/{max_scrolls} — {count} cartes visibles")

        if count == prev_count:
            stable += 1
            if stable >= 3:
                log("Plus de nouveaux avis chargés — arrêt du scroll")
                break
        else:
            stable = 0
        prev_count = count


EXTRACT_JS = """
() => {
  const cards = document.querySelectorAll('[data-review-id]');
  return Array.from(cards).map(c => {
    const id = c.getAttribute('data-review-id');

    // Auteur
    let name = null;
    const nameEls = c.querySelectorAll('div.d4r55, .WNxzHc a, button[jsaction*="reviewerLink"] div');
    for (const el of nameEls) {
      const t = (el.innerText || '').trim();
      if (t && t.length < 80) { name = t; break; }
    }

    // Note (via aria-label des étoiles)
    let rating = null;
    const starEls = c.querySelectorAll('span[role="img"][aria-label*="étoile"], span[role="img"][aria-label*="star"], span[aria-label*="/5"]');
    for (const el of starEls) {
      const label = el.getAttribute('aria-label') || '';
      const m = label.match(/(\\d[\\d,\\.]*)/);
      if (m) { rating = parseFloat(m[1].replace(',', '.')); break; }
    }

    // Texte de l'avis
    let text = null;
    const textEls = c.querySelectorAll('span.wiI7pd, div[data-expandable-section] span, .MyEned span');
    for (const el of textEls) {
      const t = (el.innerText || '').trim();
      if (t && t.length > 5) { text = t; break; }
    }

    // Date relative
    let date = null;
    const dateEls = c.querySelectorAll('span.rsqaWe, span.xRkPPb, span.DZSIDd');
    for (const el of dateEls) {
      const t = (el.innerText || '').trim();
      if (t) { date = t; break; }
    }

    return { id, name, rating, text, date };
  }).filter(r => r.name && r.rating != null);
}
"""


def scrape():
    log(f"Cible: {URL}")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            user_agent=UA,
            locale="fr-FR",
            timezone_id="Europe/Paris",
            viewport={"width": 1400, "height": 900},
        )
        # Cache la propriété webdriver (basique anti-detection)
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()

        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        except PlaywrightTimeout:
            log("[!] Timeout navigation initiale")

        page.wait_for_timeout(2000)
        try_accept_cookies(page)

        # Attendre le chargement de la fiche
        try:
            page.wait_for_selector('h1', timeout=15000)
            title = page.locator('h1').first.inner_text()
            log(f"Fiche chargée: {title}")
        except Exception:
            log("[!] h1 pas trouvé")

        # Dump URL courante pour debug
        log(f"URL actuelle: {page.url}")

        click_reviews_tab(page)
        sort_by_newest(page)

        # Attendre au moins une review
        try:
            page.wait_for_selector('[data-review-id]', timeout=15000)
        except PlaywrightTimeout:
            log("[!] Aucune review-id détectée dans le DOM après clic")

        scroll_reviews(page)

        reviews = page.evaluate(EXTRACT_JS)
        log(f"Reviews extraites: {len(reviews)}")

        # Screenshot debug si peu/pas d'avis
        if len(reviews) < 3:
            page.screenshot(path="/tmp/debug-google.png", full_page=True)
            log("Screenshot debug écrit /tmp/debug-google.png")
            # Dump un extrait du HTML aussi
            html = page.content()[:5000]
            Path("/tmp/debug-google.html").write_text(html, encoding="utf-8")

        browser.close()
        return reviews


def main():
    print("=" * 60, file=sys.stderr)
    print("Vert'Tige — Google Reviews Playwright Scraper", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    try:
        reviews = scrape()
    except Exception as e:
        log(f"[FATAL] {type(e).__name__}: {e}")
        sys.exit(1)

    if not reviews:
        log("[FAIL] Aucun avis extrait")
        sys.exit(2)

    # Écriture
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "reviews-google-raw.json"
    out_file.write_text(json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"[OK] {len(reviews)} avis écrits dans {out_file}")
    for r in reviews[:10]:
        text_preview = (r.get('text') or '')[:60].replace('\n', ' ')
        log(f"  · {r['name']} ({r['rating']}★) {r.get('date') or '?'}: {text_preview}...")

    # Aussi sur stdout
    print(json.dumps(reviews, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
