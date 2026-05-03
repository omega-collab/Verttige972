#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('/home/user/Verttige972/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ═══════════════════════════════════════════
# 1. CSS Google Reviews
# ═══════════════════════════════════════════
new_css = """
    /* == GOOGLE REVIEWS == */
    .grev-wrap { max-width: 1100px; margin: 0 auto; padding: 80px 24px; }
    .grev-header { text-align: center; margin-bottom: 28px; }
    .grev-badge { display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); border-radius: 40px; padding: 10px 22px; margin-top: 18px; flex-wrap: wrap; justify-content: center; }
    .grev-score-num { font-family: 'Bebas Neue',sans-serif; font-size: 1.7rem; color: #fff; letter-spacing: .02em; line-height: 1; }
    .grev-stars-badge { color: #F5A623; font-size: 1rem; letter-spacing: 2px; }
    .grev-count-txt { font-family: 'Syne',sans-serif; font-size: .7rem; color: rgba(237,232,223,.45); letter-spacing: .12em; text-transform: uppercase; }
    .grev-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 24px; }
    .grev-card { background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.06); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 10px; transition: border-color .3s, transform .2s; }
    .grev-card:hover { border-color: rgba(168,217,108,.25); transform: translateY(-2px); }
    .grev-card.grev-hidden { display: none; }
    .grev-card-top { display: flex; align-items: center; gap: 10px; }
    .grev-avatar { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Syne',sans-serif; font-weight: 700; font-size: .82rem; color: #fff; flex-shrink: 0; }
    .grev-info { flex: 1; min-width: 0; }
    .grev-name { font-family: 'Syne',sans-serif; font-weight: 700; font-size: .8rem; color: var(--creme); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .grev-date { font-size: .66rem; color: rgba(237,232,223,.32); margin-top: 2px; }
    .grev-glogo { flex-shrink: 0; opacity: .65; }
    .grev-stars-row { color: #F5A623; font-size: .88rem; letter-spacing: 2px; }
    .grev-text { font-family: 'Barlow',sans-serif; font-size: .82rem; line-height: 1.65; color: rgba(237,232,223,.68); flex: 1; }
    .grev-more-btn { display: flex; align-items: center; gap: 8px; background: none; border: 1px solid rgba(237,232,223,.15); color: rgba(237,232,223,.55); font-family: 'Syne',sans-serif; font-size: .7rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; padding: 12px 24px; border-radius: 4px; cursor: pointer; margin: 0 auto 32px; transition: all .25s; }
    .grev-more-btn:hover { border-color: var(--lime); color: var(--lime); }
    .grev-cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
    .grev-btn-main { display: inline-flex; align-items: center; gap: 10px; background: var(--lime); color: #0d1410; font-family: 'Syne',sans-serif; font-weight: 700; font-size: .7rem; letter-spacing: .14em; text-transform: uppercase; padding: 16px 32px; border-radius: 4px; text-decoration: none; transition: opacity .2s, transform .2s; }
    .grev-btn-main:hover { opacity: .88; transform: translateY(-1px); }
    .grev-btn-outline { display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(168,217,108,.4); color: var(--lime); font-family: 'Syne',sans-serif; font-weight: 700; font-size: .7rem; letter-spacing: .14em; text-transform: uppercase; padding: 16px 32px; border-radius: 4px; text-decoration: none; transition: all .2s; }
    .grev-btn-outline:hover { background: rgba(168,217,108,.08); border-color: var(--lime); }
    @media (max-width: 900px) { .grev-grid { grid-template-columns: repeat(2,1fr); } }
    @media (max-width: 600px) { .grev-wrap { padding: 48px 16px; } .grev-grid { grid-template-columns: 1fr; } }
"""
content = content.replace('</style>', new_css + '</style>', 1)

# ═══════════════════════════════════════════
# 2. HTML Section
# ═══════════════════════════════════════════
GMAP = 'https://maps.google.com/?cid=16485322727302760309'

GSVG = '<svg class="grev-glogo" viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'

GSVG_BIG = '<svg viewBox="0 0 24 24" width="22" height="22"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'

def card(initials, color, name, date_txt, text, hidden=False):
    cls = 'grev-card grev-hidden' if hidden else 'grev-card'
    return (
        '      <div class="' + cls + '">\n'
        '        <div class="grev-card-top">\n'
        '          <div class="grev-avatar" style="background:' + color + '">' + initials + '</div>\n'
        '          <div class="grev-info">\n'
        '            <div class="grev-name">' + name + '</div>\n'
        '            <div class="grev-date">' + date_txt + '</div>\n'
        '          </div>\n'
        '          ' + GSVG + '\n'
        '        </div>\n'
        '        <div class="grev-stars-row">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
        '        <p class="grev-text">' + text + '</p>\n'
        '      </div>'
    )

# 3 visible d'abord, 6 cachees
reviews_html = '\n'.join([
    card('JL', '#2a7a5a', 'Juliette Labyt', 'il y a une semaine',
         "Emeric a élagué un grand tamarinier, un manguier, un flamboyant et évacué un immense bakoua de notre jardin. Travail rapide, soigné, de bons conseils, respectueux des arbres et de la nature. Il nous a découpé des planches pour faire de l'artisanat avec notre bois. Je recommande sans hésiter.",
         hidden=False),
    card('AJ', '#7b3a9e', 'Alexis Joli', 'il y a 4 semaines',
         "Très beau boulot ! Je travaille avec Vert'Tige Martinique depuis 5 ans ! Les travaux sont propres et ma clientèle est très satisfaite ! Je recommande.",
         hidden=False),
    card('SG', '#16a085', 'Sophie GUEHO', 'il y a 4 semaines',
         "Nous avons effectué l'abattage d'un figuier maudit d'environ 25–30 m de hauteur. C'est un excellent professionnel très sérieux et très qualifié. Je recommande vivement !",
         hidden=False),
    # --- cachees ---
    card('PE', '#1a5fa8', 'Pascal EUGENE', 'il y a 4 semaines',
         "Je leur ai confié un chantier important avec de grands arbres et une véritable forêt de bambous. Alors que d'autres prestataires hésitaient, ils ont relevé le défi avec efficacité. Tarifs justes et équipe jeune et sympathique. À recommander.",
         hidden=True),
    card('SM', '#c07830', 'Sandrine MONIN', 'il y a 4 semaines',
         "Il a réalisé 2 chantiers pour nous : nettoyage de hauts cocotiers au dessus d'une toiture et l'élagage d'un grand figuier maudit. Travail soigné et sérieux, en plus d'être très sympathique. Je recommande !",
         hidden=True),
    card('EF', '#6d3ab5', 'Eric Fagault', 'il y a 3 semaines',
         "Très bon travail. J'ai fait appel à cette entreprise plusieurs fois pour l'élagage de vieux Mahoganys, je l'ai également conseillé à mon voisin. Quand nous avons besoin, nous faisons appel à cette entreprise.",
         hidden=True),
    card('OC', '#27ae60', 'ocealilou', 'il y a 4 semaines',
         "J'avais un cocotier qui menaçait de tomber. Il a été rapide, efficace et propre. Rien à dire à part le recommander à 300 % !",
         hidden=True),
    card('PM', '#c0392b', 'pierre-leandre murielle', 'il y a 4 semaines',
         "Excellent travail \U0001f44d\U0001f44f très professionnel ! Ravie de constater le sérieux de ce jeune homme, je le recommande vivement \U0001f44f Abattage d'un très grand cocotier trop proche de l'habitation.",
         hidden=True),
    card('JA', '#e07b39', 'Jo Anna', 'il y a 3 semaines',
         "Merci Emeric pour ton super travail. Efficacité, rapidité et propreté !",
         hidden=True),
])

# JS toggle "Voir plus / Voir moins"
grev_js = """
    // == Google Reviews toggle ==
    (function() {
      var btn = document.getElementById('grev-toggle-btn');
      if (!btn) return;
      var hiddenCards = document.querySelectorAll('.grev-hidden');
      var expanded = false;
      btn.addEventListener('click', function() {
        expanded = !expanded;
        hiddenCards.forEach(function(c) {
          c.style.display = expanded ? 'flex' : 'none';
        });
        btn.innerHTML = expanded
          ? '<span>&#9652;</span> Voir moins'
          : '<span>&#9662;</span> Voir les 6 autres avis';
      });
    })();
"""
content = content.replace('</script>', grev_js + '</script>', 1)

new_section = (
    '  <section id="temoignages">\n'
    '    <div class="grev-wrap">\n'
    '\n'
    '      <div class="grev-header reveal">\n'
    '        <p class="section-tag">Ce qu&#39;ils disent</p>\n'
    '        <h2 class="section-h2">AVIS <em>GOOGLE</em></h2>\n'
    '        <div class="grev-badge">\n'
    '          ' + GSVG_BIG + '\n'
    '          <div class="grev-score-num">5,0</div>\n'
    '          <div class="grev-stars-badge">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
    '          <div class="grev-count-txt">22 avis Google</div>\n'
    '        </div>\n'
    '      </div>\n'
    '\n'
    '      <div class="grev-grid reveal">\n'
    + reviews_html + '\n'
    '      </div>\n'
    '\n'
    '      <button id="grev-toggle-btn" class="grev-more-btn">\n'
    '        <span>&#9662;</span> Voir les 6 autres avis\n'
    '      </button>\n'
    '\n'
    '      <div class="grev-cta reveal">\n'
    '        <a href="' + GMAP + '" target="_blank" rel="noopener" class="grev-btn-main">\n'
    '          ' + GSVG_BIG + '\n'
    '          Voir les 22 avis Google\n'
    '        </a>\n'
    '        <a href="' + GMAP + '" target="_blank" rel="noopener" class="grev-btn-outline">\n'
    '          &#9733; Laisser un avis\n'
    '        </a>\n'
    '      </div>\n'
    '\n'
    '    </div>\n'
    '  </section>'
)

content = re.sub(
    r'  <section id="temoignages">.*?</section>',
    new_section,
    content,
    flags=re.DOTALL
)

# ═══════════════════════════════════════════
# 3. Remove old JS comment system
# ═══════════════════════════════════════════
js_start_marker = '    // ══ ÉTOILES COMMENTAIRE ══'
js_end_marker = '    renderComments();\n'

idx_start = content.find(js_start_marker)
idx_end = content.find(js_end_marker)
if idx_start != -1 and idx_end != -1 and idx_end > idx_start:
    content = content[:idx_start] + content[idx_end + len(js_end_marker):]
    print("JS comment system removed")
else:
    print(f"WARNING: JS markers not found — start:{idx_start} end:{idx_end}")

with open('/home/user/Verttige972/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
