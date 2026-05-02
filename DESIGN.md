# DESIGN.md — Vert'Tige 972

## Identité visuelle

Référence physique : Manuel technique d'un équipement STIHL. Fond sombre, orange vif, typographie sans-serif comprimée, chiffres lisibles. Terrain, pas agence.

## Tokens couleurs

```css
--noir:        #0B1410  /* Fond primaire — vert noir jungle */
--jungle:      #172618  /* Fond secondaire */
--mousse:      #243D2A  /* Fond tertiaire */
--feuille:     #3D6647  /* Accent végétal */
--lime:        #A8D96C  /* Accent vie — CTAs confirmation, nature */
--lime-bright: #C4F080  /* Lime hover */
--orange:      #F37A1F  /* Signature STIHL — action, urgence, expertise */
--sable:       #C8B49A  /* Texte secondaire */
--creme:       #EDE8DF  /* Texte corps */
--blanc:       #F8F6F2  /* Texte fort */
```

## Sémantique couleurs (règle absolue)

- **Orange** = action urgente, expertise dangereuse, confiance professionnelle, CTA primaires
- **Lime** = nature, confirmation, CTAs secondaires, accents végétaux
- **Sable** = texte informatif secondaire
- **Blanc** = titres et texte fort

## Typographie (identité déjà engagée)

- **Display** : Fraunces 800 (serif impactant — déjà commis) + Bebas Neue (chiffres display)
- **Labels / nav** : Syne 700 (déjà commis)
- **Corps** : DM Sans 300 (déjà commis)

Weights utilisés : 300 (corps), 700–800 (labels), 900 (display héros).
Tracking display : -0.02em à -0.04em (tight pour impact).
Sizes display : clamp(5rem, 10vw, 11rem) pour hero-h1.

## Layout

Grille 8pt. Sections alternent --noir / --jungle pour rythme visuel.
Padding sections : 100px 48px desktop, 72px 24px mobile.
Max-width contenus : 1100px centré.

## Motion

Easing : cubic-bezier(0.16, 1, 0.3, 1) — ease-out-expo uniquement.
Pas de bounce, pas d'élastic.
Durées : 0.35s (micro), 0.65s (reveal), 0.8s (entrée), 1.2s (dramatique).
prefers-reduced-motion : 0.01ms sur tout.

## Lois absolues impeccable (ne jamais violer)

- INTERDIT : border-left > 1px comme accent décoratif sur cards/callouts
- INTERDIT : gradient-text (background-clip: text avec gradient)
- INTERDIT : glassmorphism décoratif
- INTERDIT : grille de cards icon+titre+texte identiques
- INTERDIT : em dashes

## Backgrounds

Hero section::before : gradient mesh 3 points (lime 12% top-left + orange 8% bottom-right).
body::before : noise texture SVG fractalNoise, opacity 2.5%, position fixed.
