# Errors — Vert'Tige 972

> Erreurs de commandes, outils, intégrations. Diagnostic et fix.
> Convention ID : `ERR-YYYYMMDD-XXX`

---

## [ERR-20260403-001] whatsapp_number_mismatch

**Logged**: 2026-04-03
**Priority**: high
**Status**: pending
**Area**: frontend

### Summary
Les liens WhatsApp dans index.html pointent vers `33698489837` (numéro métropole) alors que le CLAUDE.md indique `596 696 67 13 44` (Martinique).

### Error
```
href="https://wa.me/33698489837" ← numéro métropole
CLAUDE.md : 596 696 67 13 44    ← numéro Martinique
tel: 0696671344                 ← format local
```

### Context
Identifié lors de l'audit du site. Les 3 formats coexistent sans cohérence. Le bon numéro doit être confirmé par Allan.

### Suggested Fix
Confirmer le numéro exact avec Allan, puis harmoniser partout : liens `wa.me/`, `tel:`, et FABs flottants.

### Metadata
- Reproducible: yes
- Related Files: index.html (lignes 1741, 1847)
- Tags: whatsapp, contact, conversion
