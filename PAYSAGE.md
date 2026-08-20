# Paysage

On peut juger la qualité d'une interface de deux façons bien
différentes. La première consiste à confronter la page à des
principes nommés, issus de la psychologie et de la recherche en
interaction homme-machine (la loi de Hick, la loi de Fitts, et
d'autres) : on repère alors un schéma récurrent, pas un bogue
d'affichage précis. La seconde consiste à observer une vraie personne,
ou une simulation fidèle, se servir réellement de la page, et à noter
ce qui lui a concrètement posé problème. Voici où se situe
`sprezzature-ux-laws`, un outil statique de la première famille, par
rapport aux autres façons de vérifier qu'une interface respecte de
bons principes d'ergonomie.

## Comparaison des outils

| Outil | Type | Navigateur requis | Correctif auto | Compatible CI | Python |
|---|---|---|---|---|---|
| **sprezzature-ux-laws** | Linter statique heuristique | Non | Oui (4 lois) | Oui | Oui |
| Revue heuristique manuelle (10 heuristiques de Nielsen) | Expertise humaine | Non | Non | Non | N/A |
| Tests utilisateurs | Personnes réelles, modérés ou non | Oui | Non | Non | N/A |
| axe-core / Pa11y | DOM dynamique, axé accessibilité | Oui | Non | Oui (via CLI) | Non |
| Hotjar / FullStory (relecture de session) | Télémétrie utilisateur réelle | Oui | Non | Non | Non |

### Notes par dimension

| Dimension | sprezzature-ux-laws | Revue heuristique manuelle | Tests utilisateurs |
|---|---|---|---|
| Vitesse (CI) | ⭐⭐⭐⭐⭐ | ⭐ | N/A |
| Détecte les problèmes de flux ou de compréhension | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Installation sans dépendance | ⭐⭐⭐⭐⭐ | N/A | N/A |
| Correction automatique | ⭐⭐⭐ | ⭐ | N/A |
| Reproductible, déterministe | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

## Quand utiliser quoi

`sprezzature-ux-laws` sert de **verrou mécanique en pre-commit** : il
attrape la part de chaque loi qu'on peut trancher rien qu'en lisant le
texte HTML brut, un `<nav>` avec trop de liens, un `<div>` cliquable
qui joue le rôle d'un vrai `<button>`, en quelques millisecondes, sans
navigateur ni relecteur humain. Il ne peut en revanche pas dire si un
écran répond à la bonne question, si un parcours a du sens de bout en
bout, ou si les utilisateurs comprennent réellement ce que fait un
bouton : cela reste un jugement humain.

Une revue heuristique manuelle (un humain qui confronte le produit aux
dix heuristiques de Jakob Nielsen, ou à l'ensemble plus large des
Laws of UX détaillé dans `references/laws-of-ux.md`) attrape des
jugements que cet outil ne peut pas porter : est-ce vraiment la bonne
loi à appliquer ici, ce regroupement a-t-il un sens pour quelqu'un qui
découvre la page. On la mène avant une sortie, pas à chaque commit.

Les tests utilisateurs (observer cinq à huit personnes réelles tenter
des tâches réelles) restent la seule méthode qui révèle les échecs de
compréhension qu'aucune heuristique ne prédit. Rien ici ne les
remplace ; cet outil existe justement pour que les violations
mécaniques, décidables à la lecture du source, n'atteignent jamais
cette séance coûteuse.

axe-core et Pa11y vérifient l'accessibilité, un axe voisin mais
distinct (tout utilisateur peut-il se servir de la page, quel que
soit son handicap) de celui des Laws of UX que couvre cet outil (la
conception de la page respecte-t-elle le fonctionnement réel de la
cognition et de la perception humaines). `sprezzature-accessibility`,
outil statique compagnon de la même suite, couvre l'axe accessibilité
avec le même compromis zéro-navigateur.

Les outils de relecture de session (Hotjar, FullStory) montrent ce que
les utilisateurs réels ont fait une fois le produit livré. C'est une
boucle de rétroaction, pas un verrou : utile pour repérer ce que cet
outil et une revue heuristique ont tous deux manqué, trop tardif pour
remplacer l'un ou l'autre.
