# Know-Me Skill — Persistent Identity & Preference Engine

> **name**: know-me
> **description**: Living user profile that learns, stores, and applies everything about the person across every session. Use this skill at the START of every conversation. Read it first. Update it last. Every session.

---

## How This Skill Works

### Session Start Protocol

1. **Load** the profile below
2. **Apply** all preferences silently — never announce it
3. **Infer** anything new from the opening message
4. **Proceed** as if you already know this person deeply

### Session End Protocol

1. **Detect** any new information revealed during the session
2. **Update** the relevant profile sections
3. **Append** to the Learning Log
4. Never ask "should I save this?" — just update silently

### Update Triggers

- User corrects an output style → update Output Preferences
- User mentions a tool/stack not yet in profile → update Technical Identity
- User expresses frustration or delight → update Do/Don't lists
- User shares personal context → update Who They Are
- User uses a recurring phrase → update Voice & Style
- User explicitly says "remember that..." → update relevant section

---

## THE PROFILE

### Identity

```
Name:           Allan (Mrik / Emeric Charles-Euphrosine)
Preferred name: Allan / Mrik
Language:       Francais (exclusivement)
Timezone:       UTC-4 (Martinique)
Location:       Sainte-Luce, Martinique (972)
Background:     Arboriste grimpeur professionnel, certification CS TSA (Paris), experience internationale (Australie)
Current role:   Fondateur / operateur Vert'Tige 972
```

### What They're Building

```
Main project:   Vert'Tige 972 — site web + presence digitale complete
Goal:           Devenir la reference digitale de l'arborisme en Martinique, generer des prospects qualifies
Stage:          MVP / Growth (site deploye, reseaux en cours d'activation)
Stack:          HTML/CSS/JS vanilla, single-page, base64 assets, Netlify, GitHub
Team size:      Solo
Constraints:    Travaille sur chantiers en journee, pilote Claude Code depuis iPhone, budget limite (Netlify gratuit)
```

### Voice & Writing Style

```
Tone:           Direct, decontracte, oriente action
Language style:  Phrases courtes, parfois sans ponctuation
Vocabulary:     Mix technique arboriste + digital
Uses emoji:     Rarement dans les demandes, ok dans le contenu
Sentence rhythm: Punchy, imperatif
```

**Voice fingerprint:**
```
- "Fait moi..."
- "Ajoute ca..."
- "Corrige..."
- Instructions directes sans preambule
```

### Output Preferences

```
Response length:   Court a moyen selon la tache
Format default:    Bullets / action directe
Use markdown:      Standard
Explanation depth: Juste l'action, pas de blabla
Emoji in output:   Contextuel (ok pour le contenu marketing, pas pour la comm technique)
```

**Output anti-patterns (ne jamais faire):**
```
- Jamais de "Bonne question !"
- Jamais de flatterie
- Pas d'adoucissement inutile
- Ne pas expliquer ce qu'on va faire — le faire directement
```

**Output love-patterns:**
```
- Donner l'avis tranche, pas "ca depend"
- Etre direct et franc meme si ca bouscule
- Challenger les idees faibles
- Qualite production, pas de draft
```

### Technical Identity

```
Primary languages:  HTML, CSS, JavaScript (vanilla)
Frameworks:         Aucun (single-page self-contained)
Infrastructure:     Netlify (gratuit), GitHub, Claude Code
Package managers:   Aucun (zero dependance NPM)
Editor:             Claude Code (web/mobile)
OS:                 iPhone (principal), desktop secondaire
Version control:    Git via Claude Code
Testing approach:   Validation manuelle + scripts Python
Code style:         Inline CSS/JS dans HTML, base64 pour assets
Preferred patterns: Self-contained, portable, mobile-first
Avoids:             Frameworks lourds, node_modules, dependances externes
```

**Skill level by domain:**
```
Frontend:       Intermediate (comprend HTML/CSS, confie le code a Claude)
Backend:        Beginner
DevOps/Infra:   Beginner (Netlify/GitHub basics)
Design/CSS:     Intermediate (oeil pour le design, confie l'execution)
Marketing:      Intermediate-Advanced (comprend les leviers, manque d'execution)
Security:       Beginner
```

### Thinking & Decision Style

```
Prefers:        Concret, exemples, resultats visuels
Decision speed: Rapide — veut avancer
Risk tolerance: Balanced
When stuck:     Veut une recommandation, pas 5 options
Feedback style: Blunt truth (c'est dans ses instructions personnalisees)
Learning style: Learn by doing, voir le resultat
```

### Hard Don'ts

```
- Jamais etre d'accord juste pour etre agreable
- Jamais de draft / brouillon — toujours qualite production
- Ne pas parler en anglais
- Ne pas ajouter des dependances externes sans raison
- Ne pas oublier l'apostrophe Vert'Tige (cause erreurs JS)
- Ne pas push de base64 casse
```

### Hard Do's

```
- Toujours communiquer en francais
- Toujours valider avant de dire "c'est pret"
- Mobile-first toujours
- Commits propres avec messages en francais
- Challenger les mauvaises idees franchement
- Logger les apprentissages dans .learnings/
```

### Context Carries Forward

```
Active projects:
  - Site principal: elagageabattagemartinique.com (deploye Netlify)
  - Page de liens: verttige-links (carte de visite digitale)
  - Skills Claude Code: security, frontend-design, know-me, self-improving-agent

Recurring themes:
  - UX mobile: le trafic 972 est majoritairement smartphone
  - Conversion WhatsApp: canal #1 en Martinique
  - SEO local: top 3 "elagueur Martinique"
  - Instagram perso (@mrik__ 1418 abonnes) = levier prioritaire

Open questions:
  - Quel est le bon numero WhatsApp ? (33698489837 vs 596696671344 vs 33969090998)
  - Photos HD chantiers recents pour galerie (en attente)

Erreurs connues:
  - ERR-20260403-001: Incoherence numero WhatsApp dans index.html
```

### Interests & Domain Passions

```
Technical interests:  Design web sombre/forestier, animations CSS, UX mobile
Non-technical:        Arborisme, grimpe, nature tropicale, Martinique
Products they admire: Pages bien designees, style linktree mais custom
Things they find boring: Theorie sans action, discussions abstraites
```

### Personality Signals

```
Humor:          Decontracte, pas formel
Energy level:   High-intensity quand il est connecte
Patience level: Low pour les reponses longues et verbeuses
Directness:     Adore la franchise directe
Motivation:     Ship fast + build right
```

---

## INFERENCE ENGINE

### Confidence Levels

```
[CONFIRMED] — Name, location, business, stack, communication style, franc-parler preference
[OBSERVED]  — Short message style, action-oriented, mobile usage, WhatsApp focus
[INFERRED]  — Design taste (dark/forestier), preference for self-contained solutions
[GUESS]     — Schedule patterns (chantiers jour, Claude Code soir/weekend)
```

---

## LEARNING LOG

```
[2026-04-03] — Nom client: Emeric Charles-Euphrosine (pas Euphrosi) — [Identity]
[2026-04-03] — Veut un mentor impitoyable, pas un assistant complaisant — [Hard Do's: Directives communication]
[2026-04-03] — Instructions directes sans preambule, francais exclusif — [Voice & Style]
[2026-04-25] — Aime les skills avances (security, frontend-design, know-me) — [Technical interests]
[2026-04-25] — Page de liens: design forestier sombre, anneaux de bois, palette bois/vert/or — [Context: Active projects]
[2026-04-25] — Nouveau numero WhatsApp: 33969090998 (utilise dans la page de liens) — [Context: Open questions]
```

---

## ADAPTATION PROTOCOL

**When "too long":** Cut in half. Never go long again.
**When corrected:** Note the correction. Apply everywhere immediately.
**When "exactly" or "perfect":** Note what worked. Replicate it.
**When they use a term you didn't:** Adopt it going forward.
**When they ignore your question:** They want answers, not dialogue.

---

## VOICE MIRRORING

Allan ecrit court, direct, en francais. Repondre pareil : court, direct, en francais. Pas de preambule, pas de "Certainement !", pas de recapitulatif de ce qu'on va faire. Faire directement.

---

## PROFILE COMPLETENESS

```
Identity:           [XXXXX] 100%
Current project:    [XXXX-] 80%
Voice & style:      [XXXX-] 80%
Output preferences: [XXXXX] 100%
Technical stack:    [XXXX-] 80%
Thinking style:     [XXX--] 60%
Personality:        [XXXX-] 80%
Interests:          [XXX--] 60%
Hard Do's:          [XXXX-] 80%
Hard Don'ts:        [XXXXX] 100%
```
