# Graph Report - .  (2026-05-01)

## Corpus Check
- 28 files · ~242,401 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 63 nodes · 110 edges · 11 communities detected
- Extraction: 37% EXTRACTED · 63% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Photos Terrain & Démontage|Photos Terrain & Démontage]]
- [[_COMMUNITY_Sections Site Principal|Sections Site Principal]]
- [[_COMMUNITY_Série Pro Abattage Troncs|Série Pro Abattage Troncs]]
- [[_COMMUNITY_Série TCA Tronçonneuse|Série TCA Tronçonneuse]]
- [[_COMMUNITY_Élagage & Palmiers|Élagage & Palmiers]]
- [[_COMMUNITY_Design System & Liens|Design System & Liens]]
- [[_COMMUNITY_Identité Allan  Entreprise|Identité Allan / Entreprise]]
- [[_COMMUNITY_Formulaire Devis|Formulaire Devis]]
- [[_COMMUNITY_Galerie & AvantAprès|Galerie & Avant/Après]]
- [[_COMMUNITY_Documentation & SEO|Documentation & SEO]]
- [[_COMMUNITY_Déploiement GitHubNetlify|Déploiement GitHub/Netlify]]

## God Nodes (most connected - your core abstractions)
1. `Site Principal Vert'Tige 972` - 16 edges
2. `Allan - Arborist / Tree Climber (Vert'Tige 972)` - 10 edges
3. `Chainsaw (Stihl-style orange)` - 7 edges
4. `Close-up action shot of chainsaw cutting into wood - sawdust flying, orange shirt worker, low angle through foliage` - 6 edges
5. `Arborist cutting large trunk with chainsaw at ground level, wearing orange PPE and yellow helmet with ear protection` - 6 edges
6. `Dynamic close-up of Stihl chainsaw cutting trunk - sawdust spray, orange shirt, palm trees in background, tropical setting` - 5 edges
7. `Overhead shot of arborist in orange cutting large log sections with chainsaw on grass` - 5 edges
8. `Two-person team dismantling tall tree near banana plantation, climber at height, ground person with umbrella` - 5 edges
9. `Arborist in orange PPE and yellow helmet cutting large fallen tree trunk with Stihl chainsaw, sawdust spraying` - 5 edges
10. `Personal Protective Equipment (helmet, ear muffs, harness)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `CLAUDE.md (contexte projet complet)` --documents--> `Site Principal Vert'Tige 972`  [EXTRACTED]
  CLAUDE.md → index.html
- `Skill Security (audit OWASP)` --audits--> `Site Principal Vert'Tige 972`  [INFERRED]
  skills/security.md → index.html
- `Arborist with safety helmet and ear protection cutting palm trunk at height - orange shirt, ocean and blue sky background, professional gear` --same_worker_depicted--> `Close-up action shot of chainsaw cutting into wood - sawdust flying, orange shirt worker, low angle through foliage`  [INFERRED]
  DSC09516.jpeg → _TCA0222.jpeg
- `Worker on tree stump with chainsaw performing sectional dismantling near residential building - ropes rigged, red shirt, ear protection` --same_photo_session--> `Worker on ladder pruning dead fronds from tall palm tree in narrow residential alley - chainsaw on ground, tropical plants`  [INFERRED]
  IMG_3662.jpeg → IMG_3675.jpeg
- `Page Liens (carte de visite digitale)` --links_to--> `Site Principal Vert'Tige 972`  [EXTRACTED]
  liens/index.html → index.html

## Hyperedges (group relationships)
- **Conversion Funnel (Hero → Services → Devis → WhatsApp)** — index_hero, index_services, index_contact, entity_whatsapp_devis [INFERRED 0.85]
- **Social Proof (Confiance + Témoignages + Galerie)** — index_confiance, index_temoignages, index_galerie, index_avantapres [INFERRED 0.80]
- **Deployment Pipeline (GitHub → Netlify → Site)** — platform_github, platform_netlify, index_site_principal, liens_page [EXTRACTED 1.00]

## Communities

### Community 0 - "Photos Terrain & Démontage"
Cohesion: 0.21
Nodes (14): Arborist with safety helmet and ear protection cutting palm trunk at height - orange shirt, ocean and blue sky background, professional gear, Banana Plantation (agricultural context), Crane Truck (lifting equipment), Ground Crew / Team Member, Tropical Vegetation / Martinique Setting, Professional safety equipment - helmet, ear protection, harness, Arborist climbing large tree near coast with chainsaw - rope-secured, red/black gear, palm trees and ocean in background, residential area, Arborist in orange shirt standing atop stripped tree trunk, tropical setting with blue sky (+6 more)

### Community 1 - "Sections Site Principal"
Cohesion: 0.2
Nodes (10): Section À Propos (Allan / CS TSA), Section Confiance (compteurs), Easter Eggs (11 interactions cachées), Section FAQ Accordéon, Hero Section, Section Services (Élagage, Abattage, Démontage, Broyage), Site Principal Vert'Tige 972, Section Témoignages / Avis (+2 more)

### Community 2 - "Série Pro Abattage Troncs"
Cohesion: 0.53
Nodes (9): Arborist in orange PPE and yellow helmet cutting large fallen tree trunk with Stihl chainsaw, sawdust spraying, Overhead shot of arborist in orange cutting large log sections with chainsaw on grass, Arborist cutting large trunk with chainsaw at ground level, wearing orange PPE and yellow helmet with ear protection, Overhead shot of arborist cross-cutting large log sections with chainsaw, geometric cuts visible, Allan - Arborist / Tree Climber (Vert'Tige 972), Chainsaw (Stihl-style orange), Personal Protective Equipment (helmet, ear muffs, harness), Tree climber in dense tropical canopy wearing red helmet and harness, pruning branches at height (+1 more)

### Community 3 - "Série TCA Tronçonneuse"
Cohesion: 0.54
Nodes (8): Dynamic close-up of Stihl chainsaw cutting trunk - sawdust spray, orange shirt, palm trees in background, tropical setting, Artistic macro detail of freshly cut log surface showing bark texture and precision cut line - blurred worker in orange background, Close-up action shot of chainsaw cutting into wood - sawdust flying, orange shirt worker, low angle through foliage, Freshly cut tree cross-section showing growth rings and wood grain detail - clean cut surface, tropical greenery background, Log pile after tree felling in open field - worker in orange sorting cut logs with debris and greenery surrounding, Stihl professional chainsaw - primary cutting tool, Professional photography session - _TCA series - action and detail shots of arborist work, Abattage - Tree felling and removal service

### Community 4 - "Élagage & Palmiers"
Cohesion: 0.6
Nodes (6): Majestic large tropical tree with spreading canopy backlit by sun - lush garden setting, Martinique vegetation, Worker on ladder pruning dead fronds from tall palm tree in narrow residential alley - chainsaw on ground, tropical plants, Arborist climbing tall coconut palm for maintenance - coconut clusters visible, tropical vegetation, cloudy sky, Martinique, Elagage - Tree pruning and trimming service, Martinique tropical environment - palms, coastal vegetation, residential areas, Vert'Tige 972 - Professional arborist services in Martinique

### Community 5 - "Design System & Liens"
Cohesion: 0.4
Nodes (5): Design System (Bebas Neue / Syne / Barlow + palette lime/noir), WhatsApp Public (596696671344), Barre Sticky Mobile (Appel + WhatsApp), Page Liens (carte de visite digitale), Skill Frontend Design (UI/UX)

### Community 6 - "Identité Allan / Entreprise"
Cohesion: 0.67
Nodes (3): Allan (Mrik / Emeric Charles-Euphrosine), Vert'Tige 972 (entreprise), Skill Know-Me (profil Allan)

### Community 7 - "Formulaire Devis"
Cohesion: 1.0
Nodes (2): WhatsApp Devis (33698489837 - caché), Formulaire Devis WhatsApp

### Community 8 - "Galerie & Avant/Après"
Cohesion: 1.0
Nodes (2): Carousel Avant/Après (7 slides), Galerie Filtrable (22 photos)

### Community 9 - "Documentation & SEO"
Cohesion: 1.0
Nodes (2): CLAUDE.md (contexte projet complet), SEO Local Martinique

### Community 10 - "Déploiement GitHub/Netlify"
Cohesion: 1.0
Nodes (2): GitHub Repo omega-collab/Verttige972, Netlify (hébergement)

## Knowledge Gaps
- **16 isolated node(s):** `Hero Section`, `Section Services (Élagage, Abattage, Démontage, Broyage)`, `Section À Propos (Allan / CS TSA)`, `Section Confiance (compteurs)`, `Section Témoignages / Avis` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Formulaire Devis`** (2 nodes): `WhatsApp Devis (33698489837 - caché)`, `Formulaire Devis WhatsApp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Galerie & Avant/Après`** (2 nodes): `Carousel Avant/Après (7 slides)`, `Galerie Filtrable (22 photos)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Documentation & SEO`** (2 nodes): `CLAUDE.md (contexte projet complet)`, `SEO Local Martinique`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Déploiement GitHub/Netlify`** (2 nodes): `GitHub Repo omega-collab/Verttige972`, `Netlify (hébergement)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Site Principal Vert'Tige 972` connect `Sections Site Principal` to `Galerie & Avant/Après`, `Documentation & SEO`, `Design System & Liens`, `Formulaire Devis`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `Allan - Arborist / Tree Climber (Vert'Tige 972)` connect `Série Pro Abattage Troncs` to `Photos Terrain & Démontage`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Two-person team dismantling tall tree near banana plantation, climber at height, ground person with umbrella` connect `Photos Terrain & Démontage` to `Série Pro Abattage Troncs`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Abattage - Tree felling and removal service` (e.g. with `Log pile after tree felling in open field - worker in orange sorting cut logs with debris and greenery surrounding` and `Close-up action shot of chainsaw cutting into wood - sawdust flying, orange shirt worker, low angle through foliage`) actually correct?**
  _`Abattage - Tree felling and removal service` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Demontage - Sectional tree dismantling service` (e.g. with `Arborist climbing large tree near coast with chainsaw - rope-secured, red/black gear, palm trees and ocean in background, residential area` and `Arborist with safety helmet and ear protection cutting palm trunk at height - orange shirt, ocean and blue sky background, professional gear`) actually correct?**
  _`Demontage - Sectional tree dismantling service` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Allan - Arborist / Tree Climber (Vert'Tige 972)` (e.g. with `Arborist cutting large trunk with chainsaw at ground level, wearing orange PPE and yellow helmet with ear protection` and `Arborist cutting massive tree stump with chainsaw near residential building, sawdust flying`) actually correct?**
  _`Allan - Arborist / Tree Climber (Vert'Tige 972)` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Martinique tropical environment - palms, coastal vegetation, residential areas` (e.g. with `Arborist climbing large tree near coast with chainsaw - rope-secured, red/black gear, palm trees and ocean in background, residential area` and `Majestic large tropical tree with spreading canopy backlit by sun - lush garden setting, Martinique vegetation`) actually correct?**
  _`Martinique tropical environment - palms, coastal vegetation, residential areas` has 7 INFERRED edges - model-reasoned connections that need verification._