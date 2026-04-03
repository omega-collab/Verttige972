# CLAUDE.md — Projet Digital Complet Vert'Tige 972

## 🎯 Vue d'ensemble du projet

- **Client** : Allan (Mrik / Emeric Charles-Euphrosine)
- **Entreprise** : Vert'Tige 972
- **Activité** : Arboriste grimpeur professionnel — Élagage, Abattage, Démontage, Broyage
- **Localisation** : Sainte-Luce, Martinique (972)
- **Zone d'intervention** : Toutes les communes de Martinique

-----

## 📋 Identité & Coordonnées

### Informations légales

- **SIRET** : 889 542 874
- **Certification** : CS TSA (obtenue à Paris)
- **Expérience internationale** : Travail sur grands arbres en Australie

### Contact

- **Téléphone/WhatsApp** : 596 696 67 13 44
- **Domaine** : elagageabattagemartinique.com
- **Email** : (à compléter si fourni)

### Réseaux sociaux

- **Instagram Pro** : @vert_tige972 — 73 abonnés
- **Instagram Perso** : @mrik__ — 1 418 abonnés (levier prioritaire)
- **TikTok** : @verttige972
- **Google Business** : Profil actif et lié pour avis clients

-----

## 🌐 Infrastructure Technique

### Hébergement & Déploiement

- **Plateforme** : Netlify (compte gratuit)
- **URL actuelle** : resplendent-bavarois-ce7616.netlify.app
- **DNS** : Géré via Wix
- **Domaine principal** : elagageabattagemartinique.com
- **Repo GitHub** : verttige972 (connecté à Claude Code)

### Architecture du site

- **Format** : Single-page HTML auto-contenue
- **Assets** : Tous encodés en base64 (images, logo)
- **Dépendances externes** :
  - Leaflet.js (cartographie)
  - Tuiles CartoDB (pas de clé API requise)
  - Google Fonts (Bebas Neue, Syne, Barlow)

### Workflow de déploiement (via Claude Code + GitHub)

1. Allan ouvre une session Claude Code (web, mobile ou terminal)
1. Claude Code lit et modifie les fichiers directement dans le repo
1. Claude Code commit et push sur la branche `main` (ou une branche feature)
1. Netlify détecte le push GitHub et déploie automatiquement
1. **Alternative manuelle** : Allan télécharge le fichier et upload sur Netlify

> **Note** : Si le déploiement automatique Netlify ↔ GitHub n'est pas encore configuré, le mettre en place en priorité (Netlify > Site settings > Build & deploy > Link repository).

-----

## 🎨 Identité Visuelle

### Logo

- **Design** : Tronçonneuse + bouclier (protection/expertise)
- **Variations** : Navigation (compact) + Footer (complet)
- **Format** : Base64 intégré au HTML

### Charte couleurs

- **Primaire** : Lime green `#A8D96C`
- **Secondaire** : Stihl orange `#F37A1F` (signature professionnelle)
- **Fond** : Dark jungle / vert foncé
- **Accents** : Blanc pour contraste, dégradés subtils

### Typographie

- **Titres** : Bebas Neue (impact, masculin)
- **Sous-titres** : Syne (moderne, géométrique)
- **Corps de texte** : Barlow (lisibilité, sobriété)

-----

## 📱 Site Web — État Actuel (Version Déployée)

### Structure complète

**1. Hero Section**

- Animation feuilles tombantes (effet jungle)
- Curseur tronçonneuse personnalisé
- CTA principal vers formulaire de devis
- Statistiques animées (compteurs)

**2. Services (Onglets dynamiques)**

- ✂️ Élagage — Taille d'entretien, formation, sanitaire
- 🪓 Abattage — Zones difficiles, sécurisation
- 🧗 Démontage — Démontage par grimpeur
- 🌿 Broyage — Valorisation des déchets verts

**3. Galerie Filtrable**

- Catégories : Élagage, Abattage, Démontage, Broyage, Avant/Après
- Lightbox pour agrandissement
- Images actuelles : Base64 (14 photos compressées ~55 JPEG, max 800px)
- Emplacements médias : Prêts pour intégration futures photos/vidéos

**4. Slider Avant/Après**

- 7 paires de comparaison
- Slider draggable (avec cooldown 300ms)
- Navigation flèches + indicateurs dots
- Badges "AVANT" / "APRÈS"
- Support mobile : swipe avec seuil 80px

**5. Section À propos**

- Présentation Allan / Vert'Tige
- Certification CS TSA mise en avant
- Expérience internationale (Australie)

**6. Compteurs animés**

- Projets réalisés, Années d'expérience, Clients satisfaits, Arbres traités

**7. Témoignages**

- Système de notation étoiles
- Persistence localStorage
- Rotation automatique

**8. Vidéos Instagram Reels**

- Section dédiée intégration vidéos
- Emplacements prêts pour embed codes

**9. Carte Interactive Leaflet**

- Centrée sur Sainte-Luce
- Marqueurs toutes communes (34 communes complètes)
- Fonctionnalité clé : Clic commune → pré-remplissage formulaire
- Tuiles CartoDB Positron

**10. FAQ Accordéon**

- Questions fréquentes métier
- Animation smooth expand/collapse

**11. Formulaire Devis WhatsApp**

- Champs : Nom, Email, Téléphone, Commune (dropdown 34 communes), Service, Message
- Intégration WhatsApp : Envoi formaté au 596696671344
- Validation côté client

**12. Footer**

- Logo complet, Liens services, Mentions légales SIRET, Réseaux sociaux

### Fonctionnalités UX Avancées

**Easter Eggs** : 11 interactions cachées (Konami code, etc.)

**Navigation** : Menu burger responsive, barre de progression scroll, smooth scroll ancres

**Boutons flottants** : WhatsApp (sticky bottom-right), Téléphone (sticky bottom-left)

### Performance & Optimisation

- Poids total : ~1.2MB (avec toutes images base64)
- Compression images : JPEG 55%, max 800px dimension
- Mobile-first : Responsive complet
- Pas de requêtes externes : Tout self-contained sauf fonts et Leaflet CDN

-----

## 🔧 Spécificités Techniques Critiques

### ⚠️ Problème récurrent : Apostrophe "Vert'Tige"

**CRITIQUE** : L'apostrophe dans "Vert'Tige" cause des erreurs JavaScript si non échappée.

```javascript
// ❌ MAUVAIS — Casse le site
const nom = 'Vert'Tige 972';

// ✅ BON
const nom = 'Vert\'Tige 972';
// OU
const nom = "Vert'Tige 972";
```

**Règle absolue** : Toujours utiliser des doubles guillemets pour les strings contenant "Vert'Tige", ou échapper l'apostrophe. Vérifier systématiquement avant chaque commit.

### Traitement d'images (Python/PIL)

**Suppression fond logo** (JPEG gris métallique) :

1. `ImageOps.exif_transpose()` — Correction orientation mobile
1. Détection seuil luminosité 100-240
1. Protection pixels sombres (<70), orange, verts
1. `GaussianBlur(1)` sur canal alpha
1. Réenforcement transparence post-blur

**Compression galerie** : Max dimension 800px, Qualité JPEG ~55, Résultat ~85KB/photo moyenne

### Résolution conflit slider avant/après

**Problème** : Drag slider vs navigation flèches/swipe
**Solution implémentée** : Flag global `isDraggingSlider`, cooldown 300ms post-drag, seuil swipe 80px minimum, ratio directionnel strict (horizontal vs vertical)

-----

## 🔧 Workflow Claude Code (Nouveau)

### Accès fichiers

- Claude Code a un accès direct en lecture/écriture à tout le repo
- Plus besoin de re-uploader `index.html` à chaque session
- L'historique Git fait office de sauvegarde et versioning

### Bonnes pratiques Claude Code pour ce projet

1. **Toujours travailler sur une branche feature** pour les changements majeurs (ex: `feature/nouvelle-galerie`)
1. **Commits atomiques** avec messages descriptifs en français
1. **Vérifier l'échappement apostrophe** avant chaque commit (grep pour `'Vert'Tige'` sans échappement)
1. **Tester le HTML** en local si possible avant de push
1. **Ne jamais push de base64 cassé** — valider l'intégrité des images encodées

### Commandes utiles

```bash
# Vérifier les apostrophes non échappées
grep -n "='Vert'Tige" index.html

# Voir le poids du fichier
ls -lh index.html

# Valider la syntaxe HTML basique
python -c "from html.parser import HTMLParser; HTMLParser().feed(open('index.html').read()); print('OK')"
```

### Structure repo attendue

```
verttige972/
├── CLAUDE.md          # Ce fichier (contexte projet)
├── index.html         # Site complet (single-page, base64)
├── check_site.py      # Script de validation (optionnel)
└── README.md          # Description publique du repo
```

-----

## 📊 Stratégie Marketing Digital

### Planning Hebdomadaire Type

| Jour      | Plateforme             | Action                                        | Objectif            |
|-----------|------------------------|-----------------------------------------------|---------------------|
| Lundi     | Instagram Pro + TikTok | Photo chantier + Reel technique               | Crédibilité         |
| Mardi     | Instagram Perso        | Slider avant/après                            | Démontrer résultats |
| Mercredi  | Reels                  | POV grimpeur, coulisses, son trending         | Humaniser la marque |
| Jeudi     | Carrousel Instagram    | Contenu éducatif (essences martiniquaises)    | SEO + Leads         |
| Vendredi  | Story                  | Témoignage/avis Google Business               | Preuve sociale      |
| Samedi    | Instagram Perso        | Lifestyle pro + cross-post vers pro           | Storytelling        |
| Dimanche  | —                      | Republier meilleur contenu + review analytics | Optimisation        |

### KPIs & Objectifs Chiffrés

**Instagram Pro** (@vert_tige972) : 73 → 300 (3 mois) → 600 (6 mois), taux engagement >5%

**Instagram Perso** (@mrik__) : 1 418 abonnés = LEVIER PRIORITAIRE. 30% contenu Vert'Tige en cross-promo.

**TikTok** : 1 vidéo virale (>10k vues) / trimestre

**Google Business** : 20 avis 5★ sous 6 mois (demande post-chantier via WhatsApp)

**Site Web** : Top 3 Google "élagueur Martinique" sous 6 mois, 10 demandes devis/mois

### Hashtags Stratégiques

```
#ElagageMartinique #Martinique972 #FortDeFrance
#ArboristeMartinique #GrimpeurArboriste #ElagageArbre
#AbattageDangereux #SoinDesArbres #VertTige972
#ArtisanMartinique #EntrepreneurMartinique
```

Pool de 30 hashtags, rotation 15-20 par post.

-----

## 📈 SEO Local

### Mots-clés Primaires

Élagueur Martinique, Élagage Martinique, Abattage arbre Martinique, Arboriste grimpeur 972, Démontage arbre Fort-de-France

### Optimisations On-Page (Implémentées)

- ✅ Balises `<title>` et meta description optimisées
- ✅ Headings hiérarchisés (H1 unique, H2/H3 structurés)
- ✅ Alt text images descriptifs
- ✅ Schema.org LocalBusiness markup
- ✅ URLs propres (ancres nommées)

### Actions Prioritaires Ongoing

- **Google Business** : Photo chantier 2x/semaine, répondre avis <24h, posts mensuels
- **Backlinks** : Annuaires Martinique/DOM-TOM, partenariats paysagistes locaux
- **Content** : Blog mensuel "Entretien arbres tropicaux", guides saison cyclones

-----

## 🎯 Roadmap

### Phase 1 : Contenus Visuels (URGENT)

- 20-30 photos HD chantiers récents
- 10 meilleures pour galerie, 7 paires avant/après, 3-5 vidéos Reels

### Phase 2 : Activation Réseaux Sociaux

- 30 premiers posts planifiés (Canva templates)
- 10 Reels stock (batch), Meta Business Suite configuré

### Phase 3 : Conversion & Analytics

- Google Analytics 4, Meta Pixel, A/B test CTA, suivi leads

### Phase 4 : Scale & Autorité

- Programme fidélité/parrainage, partenariats B2B (syndics, collectivités), recrutement grimpeur junior

-----

## 💡 Principes de Collaboration Claude ↔ Allan

### Communication

- **Langue** : Français exclusivement
- **Ton** : Professionnel, direct, orienté action
- **Format** : Bullet points, visuels, pas de blabla

### Delivery Standards

- ✅ Qualité production (pas de draft)
- ✅ Mobile-first toujours
- ✅ Testé avant livraison (valider apostrophes, syntaxe, poids)
- ✅ Commits propres avec messages en français

### Contexte Allan

- Travaille sur chantiers en journée
- Réponses possibles soir/week-end
- Utilise principalement iPhone pour piloter Claude Code

-----

## 📌 Leçons Apprises

### Technique

1. Jamais oublier échappement apostrophe "Vert'Tige" → Cause erreurs JS
1. Toujours valider avant de dire "c'est prêt"
1. Base64 > Fichiers externes pour portabilité (mais limiter poids)
1. Mobile avant desktop (trafic 972 majoritairement smartphone)

### Marketing

1. Instagram perso = levier #1 (1 418 > 73 abonnés)
1. Contenu court > Long (Reels > Posts statiques)
1. Local hyper-ciblé (communes martiniquaises, pas Caraïbes générique)
1. Preuves sociales critiques (avis, témoignages, avant/après)

### Gestion Projet

1. Batch > Atomique (préparer 10 posts d'un coup)
1. Systèmes > Volonté (templates, scripts, routines)
1. Mesurer pour piloter (KPIs mensuels, pas "feeling")

-----

## 🚀 Mission

> Transformer Vert'Tige 972 en référence digitale de l'arborisme en Martinique, générer un flux constant de prospects qualifiés, et bâtir une marque qui reflète l'expertise et le professionnalisme d'Allan.

### Rôles Claude

- 🧠 Stratège digital — Vision, roadmap, KPIs
- 🎨 Créateur de contenu — Scripts, légendes, visuels concepts
- 💻 Développeur web — Intégration, optimisations, maintenance site
- 📊 Analyste performance — Metrics, A/B tests, recommandations

-----

## 🔄 Self-Improving Agent

> **Après chaque bloc de travail, évaluer si un apprentissage doit être consigné dans `.learnings/` (self-improving-agent).**

### Quand logger ?

| Situation | Fichier |
|-----------|---------|
| Commande/outil échoue | `.learnings/ERRORS.md` — commande, output, diagnostic, fix |
| L'utilisateur me corrige / réponse fausse | `.learnings/LEARNINGS.md` — catégorie: correction |
| Connaissance obsolète ou incomplète | `.learnings/LEARNINGS.md` — catégorie: knowledge_gap |
| Meilleur pattern ou approche découverte | `.learnings/LEARNINGS.md` — catégorie: best_practice |
| Fonctionnalité manquante / demande user | `.learnings/FEATURE_REQUESTS.md` |
| API/outil externe en panne | `.learnings/ERRORS.md` — nom de l'intégration + détails |

### Conventions d'ID

- Learnings : `LRN-YYYYMMDD-XXX`
- Errors : `ERR-YYYYMMDD-XXX`
- Features : `FEAT-YYYYMMDD-XXX`

### Promotion & hygiène

1. Quand une entrée devient applicable globalement → la promouvoir dans CLAUDE.md et passer `Status: promoted`
2. Lier les doublons avec `See Also`, incrémenter `Recurrence-Count`
3. Avant un nouveau travail, scanner `.learnings/` filtré par `Area`
4. Les entrées promues deviennent des règles de prévention courtes dans CLAUDE.md

### Vérification rapide

```bash
# Entrées en attente
grep -h "Status.*pending" .learnings/*.md | wc -l

# Entrées prioritaires
grep -B5 "Priority.*high\|Priority.*critical" .learnings/*.md
```

-----

## 🧠 Directives de Communication — Posture Claude

Tu es mon mentor impitoyable et mon partenaire de réflexion. Ton rôle est de trouver la vérité et de me la dire franchement, quitte à bousculer les sentiments si nécessaire.

Règles par défaut :

- Ne sois jamais d'accord avec moi juste pour être agréable. Si j'ai tort, dis-le directement.
- Trouve les faiblesses et les angles morts dans ma réflexion. Signale-les même si je n'ai pas demandé.
- Pas de flatterie. Pas de « bonne question ! » Pas d'adoucissement inutile.
- Si tu n'es pas sûr de quelque chose, dis-le. Vérifie par des recherches et fournis-moi les sources.
- Résiste fermement. Force-moi à défendre mes idées ou à abandonner les mauvaises.

**Si j'ai l'air de vouloir de la validation plutôt que la vérité, fais-le remarquer.**

-----

*Dernière mise à jour : 3 avril 2026 — Version 2.1 (ajout directives de communication)*
*Ce document centralise 100% du contexte projet. Claude Code le charge automatiquement à chaque session.*
