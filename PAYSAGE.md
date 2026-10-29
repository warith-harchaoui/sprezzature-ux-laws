# Paysage

`sprezzature-ux-laws` est la brique d'audit de l'expérience utilisateur (UX) de la suite
[sprezzature](https://sprezzature.ai/), un ensemble de paquets Python pour fabriquer du
contenu web de qualité publication. Elle n'affiche jamais une page et ne regarde jamais
personne s'en servir : elle lit le texte HTML brut et tranche la part de huit lois
nommées qu'une lecture du texte peut honnêtement décider. Ce choix achète de la vitesse
et du déterminisme, au prix des vingt-deux autres lois et de tout ce qu'une loi ne
révèle qu'avec quelqu'un devant l'écran.

## Sa place dans l'écosystème

```
suite sprezzature
├── sprezzature-ux-laws       ← ce paquet (8 lois sur 30, depuis la source seule)
├── sprezzature-ui            (écrit l'écran que celle-ci audite, et les jetons de style)
├── sprezzature-accessibility (l'axe voisin : 20 règles, même pari sans navigateur)
├── sprezzature-colors        (contraste et déficience de la vision des couleurs)
├── sprezzature-figures       (167 types de graphiques, et la boucle visuelle)
├── sprezzature-publish       (transforme les pages auditées en site)
└── sprezzature-video         (vérifie ce qu'un film affirme sur tout ce qui précède)
```

**Ce qui vient avant.** `sprezzature-ui` produit le balisage : HTML sémantique,
utilitaires Tailwind, le jeton de focus de la maison, la règle typographique des trois
Roboto. Deux des huit contrôles lisent l'échelle propre à cette pile (`min-h-11` pour une
cible de 44 pixels, `focus-visible:ring-*` pour l'anneau de focus), ce qui explique que
l'auditeur demande d'abord si le document utilise Tailwind avant de rapporter quoi que
ce soit sur ces deux-là.

**Ce qui vient après.** `sprezzature-publish` transforme un dossier de Markdown en site,
et les pages qu'il produit sont exactement ce sur quoi cet auditeur est braqué dans un
crochet de pré-commit.

**La brique sœur qui fait le travail voisin.** `sprezzature-accessibility` demande si
tout lecteur peut se servir de la page, quel que soit son handicap. Celle-ci demande si
la page respecte le fonctionnement réel de l'attention, de la mémoire et du geste. Les
deux se recouvrent sur un seul point, la couleur comme unique canal d'état, et le
signalent sous des angles différents.

## Quand la choisir

- **Vous voulez un crochet de pré-commit, pas un rapport.** La page médiane du site de
  cette suite, environ 20 kilo-octets, s'audite en cinq millisecondes environ, sans
  navigateur à démarrer et sans rien à installer au-delà de Python et de click. Un
  verrou qui ne coûte rien tourne à chaque fois ; un verrou qui coûte trente secondes
  finit désactivé.
- **Vous avez besoin du même verdict deux fois.** Les contrôles sont de l'analyse de
  texte pure. Aucun modèle, aucun réseau, aucun échantillonnage. La construction qui a
  échoué hier échoue aujourd'hui pour la même raison, et un relecteur la reproduit sur
  son portable sans compte nulle part.
- **Vous générez du HTML avec un agent et vous voulez un plancher mécanique.** Un agent
  qui écrit un `<div>` cliquable l'écrira encore. `--fix` répare quatre des huit lois sur
  place, boucle jusqu'à un point fixe, et n'applique plus aucune modification à la
  deuxième passe sur un fichier déjà réparé.
- **Vous voulez la règle et son article dans le même dépôt.** `references/laws-of-ux.md`
  reformule l'ensemble canonique en nommant l'origine de chaque entrée : HICK 1952 et
  HYMAN 1953, MILLER 1956, DOHERTY et THADANI 1982, KUROSU et KASHIMURA 1995. Un constat
  pointe une loi, et la loi pointe une publication.

## Quand prendre autre chose

- **Baymard UX-Ray** gagne sur la couverture et sur la preuve. Il examine 209 paramètres
  d'UX contre une bibliothèque de plus de 700 recommandations publiées, et Baymard
  annonce 95 % d'accord avec la note qu'ont donnée ses propres auditeurs humains sur les
  mêmes sites. Rien ici n'est mesuré contre un jugement humain. Si la question est « ce
  tunnel de paiement est-il bon », c'est cet outil, et il est payant.
- **Maze, Lyssna, UXtweak et UserTesting** gagnent dès que la question devient : est-ce
  que quelqu'un comprend cet écran. Une lecture statique ne peut pas découvrir qu'un
  libellé est ambigu, qu'un parcours réclame un numéro que l'utilisateur n'a pas, ou que
  le bouton dont tout le monde a besoin est celui que personne ne trouve. Cinq à huit
  participants réels, si. Rien dans ce document ne remplace cette séance ; cet outil
  existe pour que les fautes mécaniques ne s'y rendent jamais.
- **axe-core et Pa11y** gagnent sur l'accessibilité, l'axe voisin, et de loin le plus
  mûr. Ils tournent contre un vrai modèle objet de document (DOM), ils rattachent chaque
  règle à un critère de succès des Web Content Accessibility Guidelines (WCAG), et Deque
  annonce qu'un verrou d'intégration continue (CI) bâti dessus attrape environ 57 % des
  défauts d'accessibilité. Ce paquet ne vérifie rien de tout cela, et on ne devrait pas
  le lui demander.
- **Lighthouse et les données de terrain** gagnent sur le seuil de Doherty, la loi que ce
  paquet ne peut explicitement pas contrôler : un temps de réponse n'est pas un fait
  sur le source. `references/laws-of-ux.md` le dit et désigne Lighthouse. Et Lighthouse
  ne gagne qu'à moitié, puisque l'Interaction to Next Paint (INP) exige des interactions
  réelles et que l'outillage de laboratoire rapporte le Total Blocking Time comme
  approximation ; c'est le Chrome User Experience Report (CrUX) qui porte le vrai
  chiffre.
- **ux-skill** gagne sur le nombre de règles dans la même niche : 152 règles
  déterministes hors ligne réparties en neuf catégories, un serveur Model Context
  Protocol (MCP), des installateurs pour dix-sept éditeurs, et une exécution sous
  200 millisecondes. C'est le concurrent frontal le plus proche que cette recherche a
  trouvé. Il est aussi plus jeune, et bien moins sourcé règle par règle, ce qui est
  l'échange en sens inverse.
- **Microsoft Clarity** gagne sur le prix, pour ce que cet outil ne peut
  structurellement pas voir. Il est gratuit sans plafond de sessions, et les clics de
  rage comme les clics morts sont des preuves sur des gens réels qu'aucune lecture du
  balisage ne produit.

## Les idées à prendre

Classées de la meilleure à la plus coûteuse au regard de ce qu'elle rapporte. Deux des
six sont des refus, avec leur raison, et c'est tout l'intérêt d'aller regarder.

**1. La sortie SARIF, prise à tout l'écosystème de l'analyse statique.** Le Static
Analysis Results Interchange Format
([SARIF 2.1.0](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning))
est le schéma JSON de l'OASIS qu'ingère le code scanning de GitHub, et ruff, clippy,
detekt et golangci-lint l'émettent tous. Un outil déclare ses règles une fois, puis
chaque résultat renvoie à un identifiant de règle et à un emplacement physique. Ici,
c'est un drapeau `--sarif` à côté de `--json` dans `scripts/audit_laws_of_ux.py`, où
`LAW_REGISTRY` devient le tableau `rules` et chaque `Finding` un `result` portant `path`
et `line`. Le gain : un constat Hick arrive en annotation sur le diff de la pull request,
juste à côté du `<nav>` fautif, lu par personne et vu par tout le monde. Le coût : une
après-midi, et aucune dépendance de plus, puisque c'est un `json.dumps` d'une autre
forme.

**2. Un commentaire de neutralisation par constat, pris à ESLint et au `hideElements`
d'axe-core.** Les deux permettent de faire taire une occurrence à un endroit, dans le
fichier, là où la raison peut s'écrire à côté. Ce paquet n'a que `--ignore tesler`, qui
abandonne la loi sur toutes les pages, y compris les heures d'horloge pour lesquelles
elle existe. Le dépôt le sait déjà : la docstring au-dessus de `RE_DURATION_CONTEXT` dit
que le seul remède proposé « fait taire la loi partout, y compris sur les heures
d'horloge pour lesquelles elle est faite ». La réparation est un commentaire HTML lu par
`Walker`, `<!-- ux-laws-disable-next-line tesler: ceci est une position de lecture -->`,
avec le texte après les deux-points obligatoire et non facultatif. Une demi-journée, et
cela aurait évité l'heuristique de durée écrite ligne à ligne qui est dans le fichier
aujourd'hui.

**3. Le `threshold` de Pa11y, et sa configuration par URL.**
[Pa11y](https://github.com/pa11y/pa11y) accepte un nombre de constats tolérés avant
l'échec, ce qui permet de le braquer sur un arbre hérité, d'épingler le compte où il en
est, et de le faire descendre cran par cran. Ici, c'est `--max-warnings N` sur les deux
portes d'entrée, plus un `.ux-laws.toml` tenant un budget par motif de chemin.
Aujourd'hui le choix est binaire : les erreurs échouent, les avertissements jamais, et
`--strict` échoue sur tout. Une après-midi pour le drapeau, une journée pour le fichier,
et c'est le fichier qui mérite l'hésitation, parce qu'un format de configuration est une
chose qu'on doit ensuite aux gens pour toujours.

**4. Les quatre catégories de résultat d'axe-core.** axe renvoie `violations`, `passes`,
`incomplete` et `inapplicable`, si bien que le silence n'est jamais ambigu : on
distingue une règle qui n'a rien trouvé d'une règle qui n'avait rien à regarder. Ce
paquet a déjà l'idée à moitié, dans `_not_a_tailwind_page`, qui dit une fois par document
qu'un contrôle d'échelle n'a pas pu lire une liste de classes Tailwind. La généraliser,
c'est un `--json` qui porte un bloc d'état par loi à côté des constats, pour qu'un
rapport propre dise aussi lesquelles des huit ont réellement tourné. Une demi-journée,
et le plus gros de la réflexion est fait.

**5. Le taux d'accord publié par Baymard, refusé pour l'instant.** Baymard annonce
[95 % d'accord](https://baymard.com/blog/ai-heuristic-evaluations) entre UX-Ray et ses
propres auditeurs humains sur les mêmes sites. C'est une meilleure revendication que
n'importe quel nombre de règles, et c'est la chose la plus crédible que fasse un
concurrent de ce domaine. La reproduire ici demande un corpus de pages étiquetées avec
soin, deux étiqueteurs à comparer l'un à l'autre, et un chiffre de précision et de rappel
par loi. C'est une semaine de travail avant la première ligne de code, et le corpus doit
être entretenu à mesure que les règles bougent. À faire le jour où l'ensemble des règles
cesse de changer ; pas avant, parce qu'un chiffre mesuré sur des règles mouvantes est un
chiffre sur le mois dernier.

**6. Un modèle de vision qui lit la page rendue, refusé avec une nuance.**
[uxlint](https://github.com/GyeongHoKim/uxlint) pilote Playwright, prend la page en
capture, et demande à un modèle multimodal de juger l'ergonomie depuis un persona
déclaré. Il obtient ce qu'aucune lecture de texte n'obtient : l'encombrement, la
hiérarchie visuelle, le fait que l'action principale ait l'air principale. Il coûte aussi
une installation de Chrome, un modèle, et le déterminisme, soit les trois choses que ce
paquet est fait de refuser. La nuance : la suite possède déjà le mécanisme, dans la
boucle Ralph Eyeball de `sprezzature-figures`, qui fait tourner un modèle local hors
ligne. L'énoncé honnête n'est donc pas « on ne peut pas » mais « pas dans la brique dont
tout l'argument est qu'un crochet de pré-commit peut se la payer ».

## Comment le domaine se découpe

**Par ce que l'outil a le droit de regarder.** Un *lecteur de source* analyse le balisage
qu'un développeur vient d'écrire : ce paquet, ux-skill, le ux-lint de Banno,
`@lapidist/design-lint`. Un *contrôleur d'exécution* a besoin que la page existe et
s'affiche, et c'est là que vivent axe-core, Pa11y et Lighthouse ; le saut de coût est
réel, puisqu'il faut démarrer un navigateur. Un *enregistreur de comportement* a besoin
de gens sur le site en ligne : Hotjar, Microsoft Clarity, LogRocket. Une *étude* a besoin
de participants recrutés : Maze, Lyssna, UXtweak, UserTesting, Optimal Workshop. Plus on
descend cette liste, plus l'outil en sait, et plus tard il vous le dit.

**Par la présence ou non d'un modèle dans la boucle.** Les entrants de 2025 et 2026 en
mettent presque tous un. Baymard UX-Ray est passé de 39 paramètres en octobre 2025 à 209
un an plus tard, UX Pilot relit un fichier de maquette dans l'outil de maquette, uxlint
pilote un navigateur et un modèle multimodal, et Attention Insight comme Neurons Predict
devinent où ira l'œil à partir de modèles entraînés sur des fixations oculométriques
enregistrées. Ceux-là voient des choses qu'un analyseur syntaxique ne voit pas. Ils
rendent aussi une réponse différente un autre jour, ce qui est tolérable dans une revue
de conception et pas dans un verrou.

**Par le fait de verrouiller ou de rapporter.** Un verrou tourne avant que le changement
n'atterrisse, sort avec un code non nul, et bloque. Un rapport tourne après, et dit ce
qui s'est déjà passé. La relecture de session et CrUX sont des rapports par
construction, puisqu'ils ont besoin d'un trafic qui n'existe qu'une fois la page en
ligne. Les études utilisateurs sont entre les deux : avant la mise en ligne, mais pas
avant chaque commit. Ce paquet est un verrou et rien d'autre, et l'essentiel de ce qu'il
ne sait pas faire découle de ce seul choix.

## Comparaison

Chaque outil est noté de 1 à 5 sur chaque critère, plus c'est haut mieux c'est, de ⭐
faible à ⭐⭐⭐⭐⭐ le plus fort. Les notes relèvent d'un jugement argumenté, pas d'un
banc d'essai, et chaque axe est orienté pour que plus d'étoiles veuille dire plus fort
sur ce trait : pour le coût, plus d'étoiles veut dire plus gratuit ou plus ouvert. Une
seule ⭐ signifie que l'outil ne fait pas du tout la chose mesurée, ce qui vaut 1 sur une
échelle de capacité. La source lisible par machine est
[`assets/paysage.csv`](assets/paysage.csv) : 25 outils sur 13 critères.

| Outil de qualité d'interface | Gratuit ou open source | Rapidité en intégration continue | Déterministe et reproductible | Lois de l'UX couvertes | Détecte les problèmes de compréhension et de parcours | Correction automatique | Aucun navigateur requis | Tourne entièrement sur votre machine | Aucun relecteur humain nécessaire | Aucun trafic réel nécessaire | Source publiée par règle | Maturité et écosystème | Sortie lisible par machine |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| sprezzature-ux-laws | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| ux-skill | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| uxlint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| Banno ux-lint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ |
| sprezzature-accessibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| axe-core | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Pa11y | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Lighthouse | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| @lapidist/design-lint | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Figma Design Lint | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ |
| Baymard UX-Ray | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| UX Pilot | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| Heurio | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Revue heuristique manuelle (NIELSEN) | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Maze | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Lyssna | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| UXtweak | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| UserTesting | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Optimal Workshop | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Hotjar | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Microsoft Clarity | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| LogRocket | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Attention Insight | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Neurons Predict | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| CrUX + web-vitals | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

![Carte de positionnement de 25 outils de qualité d'interface sur deux axes issus d'une analyse en composantes principales. En haut à droite, seul dans son coin, sprezzature-ux-laws, avec juste à côté Banno ux-lint, @lapidist/design-lint, sprezzature-accessibility et ux-skill : les outils qui lisent la source, n'ont besoin de rien, et tournent gratuitement. Le coin opposé, en bas à gauche, rassemble UserTesting, Maze, Hotjar, Microsoft Clarity et LogRocket, ceux qui réclament des participants recrutés ou du trafic en ligne. En haut à gauche, axe-core, Pa11y, Lighthouse et CrUX, mûrs et prêts pour une chaîne d'intégration. En bas à droite, la revue heuristique manuelle et Heurio, qui ne demandent aucune infrastructure et une personne. L'axe horizontal oppose n'avoir besoin de rien à être établi ; l'axe vertical oppose ce qu'une machine fait pour pas cher à ce que seul un humain trouve.](assets/paysage.svg)

La source est [`assets/paysage.csv`](assets/paysage.csv), la table en étoiles ci-dessus
et rien de plus, et la carte se régénère avec :

```sh
python ~/sprezzature/scripts/landscape_to_csv.py PAYSAGE.md --out assets/paysage.csv
standpoint assets/paysage.csv --outdir assets --stem paysage --check
```

La géométrie est une analyse en composantes principales (ACP) sur corrélations, et elle
est **déterministe** : la même table donne la même carte à chaque exécution. Les quatre
mots des bords viennent d'un modèle local, et ils sont plus vagues que les charges qui
les portent ; ce sont les charges qui font le contrôle. Voici donc de quoi les deux axes
sont faits.

**Horizontal, `Stabilité ↔ Autonomie`, 50,6 % de la variance.** Aucun trafic réel
nécessaire (+0,50), aucun navigateur requis (+0,40) et correction automatique (+0,37)
tirent à droite ; maturité et écosystème (−0,43) et sortie lisible par machine (−0,32)
tirent à gauche. L'axe oppose *n'avoir besoin de rien* à *être établi*.
`sprezzature-ux-laws` est tout à droite par construction : c'est la ligne de référence,
et `standpoint` ancre la référence en haut à droite. C'est une convention de dessin, pas
une prétention de qualité, et la lecture honnête de l'extrémité gauche est qu'axe-core,
Pa11y, Lighthouse et le Chrome User Experience Report ont un écosystème que ce paquet
n'a pas.

**Vertical, `Accessibilité ↔ Efficacité`, 14,4 % de la variance.** Sortie lisible par
machine (+0,43), rapidité en intégration continue (+0,38), gratuit ou open source
(+0,35) et aucun relecteur humain nécessaire (+0,32) chargent vers le haut ; lois de
l'UX couvertes (−0,35) et détection des problèmes de compréhension et de parcours
(−0,33) chargent vers le bas. C'est tout l'argument de ce document en un axe : ce qu'une
machine fait pour pas cher se tient à l'opposé de ce que seul un humain trouve. Le mot
« Accessibilité » est celui du modèle pour le pôle du bas, et il est à prendre au sens
de « ce qu'un humain atteint » et non au sens de la brique voisine ; la carte anglaise a
nommé le même pôle « Usability ». UserTesting est le point le plus bas de la carte, et
c'est l'outil qui vous en apprendrait le plus.

**Deux axes portent 65,0 % de la table.** Un tiers de ce que disent ces 13 critères
n'est pas sur cette page. La carte est une première orientation ; la table est la
preuve. `standpoint --check` signale aussi `readable: False` pour cette figure : à 25
points, cinq paires d'étiquettes risquent de se chevaucher (`sprezzature-ux-laws` avec
`Banno ux-lint`, `ux-skill` avec `sprezzature-accessibility`, `Lyssna` avec `UXtweak`,
`Hotjar` avec `Microsoft Clarity` puis avec `LogRocket`). Ces paires se superposent
parce qu'elles se notent presque pareil, ce qui est une information, mais l'encombrement
des étiquettes est un vrai défaut de l'image et les coordonnées de
[`assets/paysage.yaml`](assets/paysage.yaml) sont l'endroit où le lire exactement.
`standpoint` écrit également une interprétation en prose à côté de la figure ; elle
n'est pas reprise ici, parce qu'un modèle qui relit des notes écrites par quelqu'un
d'autre n'est pas un résultat.

## Sources

- Jon YABLONSKI, [lawsofux.com](https://lawsofux.com/), l'ensemble canonique de 30 lois,
  et *Laws of UX*, O'Reilly, 2e éd. 2024.
- Baymard Institute, [les évaluations heuristiques par IA à 95 % de
  justesse](https://baymard.com/blog/ai-heuristic-evaluations) et [UX-Ray
  2.0](https://baymard.com/research-articles/ux-ray-2-point-0-launch).
- [Pa11y](https://github.com/pa11y/pa11y), ses options `threshold`, `ignore` et
  `hideElements`, et ses cinq rapporteurs.
- [La prise en charge de SARIF par le code
  scanning](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning),
  documentation GitHub.
- [ux-skill](https://github.com/Laith0003/ux-skill), 152 règles déterministes hors ligne,
  et [uxlint](https://github.com/GyeongHoKim/uxlint), l'approche navigateur et modèle.
- [Heurio](https://www.heurio.co/guidelines), sa bibliothèque de référentiels : les dix
  heuristiques de NIELSEN, les huit règles d'or de SHNEIDERMAN, les dix principes de
  RAMS, ISO 9241-110, WCAG 2.2.
- [Attention Insight](https://attentioninsight.com/) et
  [Neurons Predict](https://www.neuronsinc.com/), le second ayant absorbé VisualEyes et
  Loceye ; tous deux entraînés sur des fixations oculométriques enregistrées.
- Nielsen Norman Group, [The Aesthetic-Usability
  Effect](https://www.nngroup.com/articles/aesthetic-usability-effect/), Kate MORAN et
  Kathryn WHITENTON, février 2024.
