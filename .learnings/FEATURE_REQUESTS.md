# Feature Requests — Vert'Tige 972

> Demandes de fonctionnalités, évolutions souhaitées.
> Convention ID : `FEAT-YYYYMMDD-XXX`

---

## [FEAT-20260403-001] mobile_ux_overhaul

**Logged**: 2026-04-03
**Priority**: high
**Status**: pending
**Area**: frontend

### Requested Capability
Refonte UX mobile complète : CTA WhatsApp full-width sticky, formulaire multi-étapes, galerie swipeable format stories, services en carousel cards, bandeau de confiance sticky.

### User Context
Allan trouve que la version mobile n'est pas aussi ergonomique que la version PC. Le trafic en Martinique est majoritairement smartphone.

### Complexity Estimate
complex

### Suggested Implementation
10 propositions détaillées dans l'audit du 2026-04-03 (session Claude Code). Prioriser : barre WhatsApp sticky (#8), CTA hero full-width (#2), formulaire multi-étapes (#6).

### Metadata
- Frequency: first_time
- Related Features: FEAT-20260403-002

---

## [FEAT-20260403-002] missing_seo_elements

**Logged**: 2026-04-03
**Priority**: high
**Status**: pending
**Area**: frontend

### Requested Capability
Ajouter les éléments SEO manquants : Schema.org JSON-LD, canonical URL, favicon, Google Analytics 4, Meta Pixel.

### User Context
Le CLAUDE.md indique "Schema.org implémenté" mais aucun JSON-LD n'existe dans le HTML. Pas de favicon ni de tracking analytics.

### Complexity Estimate
medium

### Suggested Implementation
1. Ajouter `<script type="application/ld+json">` LocalBusiness
2. Ajouter `<link rel="canonical">`
3. Créer et intégrer un favicon
4. Intégrer GA4 + Meta Pixel (quand les IDs seront fournis)

### Metadata
- Frequency: first_time
- Related Features: FEAT-20260403-001
