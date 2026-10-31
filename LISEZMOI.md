# sprezzature-ux-laws

[![Licence](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇬🇧 README.md](README.md) · 🇫🇷 LISEZMOI.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://sprezzature.ai/)

Un auditeur statique des **Laws of UX** (lois de l'ergonomie
cognitive) pour du HTML.

Les Laws of UX sont des heuristiques nommées, issues de la psychologie
et de la recherche en interaction homme-machine. La loi de Hick, par
exemple, dit qu'un écran qui propose plus de choix demande plus de
temps pour se décider : un menu de navigation avec quarante liens est
mesurablement plus difficile à utiliser qu'un menu qui en propose sept.
Cet outil ne voit jamais la page une fois affichée, et n'observe jamais
un vrai utilisateur ; il lit le texte HTML brut et signale seulement
les manquements qu'on peut trancher à sa seule lecture, par exemple
compter les liens dans une balise `<nav>`. Ce choix le rend rapide et
suffisamment prévisible pour tourner dans un hook pre-commit ou une
étape de CI, au prix de ne détecter qu'une fraction des violations de
chaque loi, celle qu'une lecture de texte peut effectivement voir (la
définition complète et sourcée de chaque loi vit dans
[`references/laws-of-ux.md`](references/laws-of-ux.md)).

## Comment ça marche

![Schéma de flux. En haut, une source HTML alimente deux voies. La voie de gauche contrôle : elle établit ce qu'un seul écran montre à partir des classes d'affichage Tailwind, retient le pire des deux décomptes, téléphone ou bureau, et tranche huit lois nommées, puis rend des constats avec un code de sortie non nul sur une erreur. La voie de droite fabrique : elle applique les quatre réparations mécaniques. Les deux se rejoignent en un seul résultat, un écran dont les fautes mesurables ont disparu.](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/comment-ca-marche.svg)

## Lois couvertes

| Loi | Ce qu'elle détecte |
|---|---|
| **Loi de Hick** | Trop de choix présentés d'un coup (menu / nav trop long). |
| **Surcharge de choix** | Longues listes d'options sans regroupement ni valeur par défaut. |
| **Loi de Miller** | Suites de chiffres non regroupées (numéros de téléphone, codes) au-delà d'environ 7 éléments. |
| **Loi de Jakob** | Motifs non conventionnels là où un motif familier était attendu. |
| **Loi de Fitts** | Contrôles interactifs sans zone de clic d'au moins 44 px (`min-h-11`). |
| **Effet esthétique-utilisabilité** | Éléments interactifs sans anneau de focus visible. |
| **Attention sélective** | Éléments stylés comme des publicités mais porteurs d'un vrai contenu. |
| **Loi de Tesler** | Complexité irréductible reportée sur l'utilisateur. |

## Comment il compte : des choix, pas des éléments

La loi de Hick mesure les choix qu'une personne affronte **au même instant**.
Compter les liens d'un fichier se trompe donc deux fois.

**Un en-tête responsive contient deux menus.** Une rangée marquée
`hidden sm:inline` et un bouton marqué `sm:hidden` ne s'affichent jamais
ensemble : le lecteur sur téléphone voit l'un, celui sur ordinateur voit
l'autre. Les additionner reproche au lecteur des choix qu'aucun écran ne lui
montre. L'auditeur résout donc la visibilité de chaque contrôle d'après ses
classes d'affichage Tailwind, en remontant les ancêtres (un conteneur qui
masque son sous-arbre l'emporte sur un enfant qui s'afficherait), puis retient
le pire des deux comptes en disant lequel.

**Un groupe vaut un choix.** Un `<details>`, un `<menu>`, un
`role="radiogroup"` ou un `role="tablist"` replie plusieurs contrôles en une
seule décision. Chacun compte pour un, quel que soit son contenu.

Quand les deux états sont ambigus, le compte monte plutôt qu'il ne descend :
un contrôle qui apparaît à `md` et disparaît à `lg` est traité comme réservé
au bureau. Signaler de trop envoie quelqu'un vérifier ; signaler trop peu
laisse passer.

---

## Installation

```bash
pip install sprezzature-ux-laws               # l'auditeur, et click pour la ligne de commande
pip install "sprezzature-ux-laws[api,mcp]"    # + les surfaces HTTP et agent
```

Que l'auditeur lui-même tienne dans la **bibliothèque standard** est tout
son intérêt, et la raison pour laquelle il est assez bon marché pour un
crochet de pré-commit : quelques millisecondes, aucun navigateur. L'unique
dépendance de base est click, achetée exprès pour la ligne de commande,
puisqu'avec argparse parti plus aucun analyseur n'est livré avec Python. Tout
ce qui est plus lourd est un extra, nommé d'après ce qui en a besoin.

## Utilisation

```bash
# Auditer un fichier ou une arborescence complète
sprezzature-ux-laws-audit public/index.html
sprezzature-ux-laws-audit site/ --json

# Se restreindre à certaines lois, ou corriger automatiquement les cas mécaniques
sprezzature-ux-laws-audit page.html --only fitts,jakob
sprezzature-ux-laws-audit page.html --fix
```

`sprezzature-ux-laws` est la même chose à travers click, avec les mêmes
drapeaux et le même gestionnaire — prenez celle qui ressemble au reste de vos
outils. Depuis un clone, sans rien installer, ça s'écrit
`python scripts/audit_laws_of_ux.py page.html`.

Les constats sont de sévérité `error` ou `warning` ; le programme
sort avec un code non nul dès qu'une `error` est présente, ce qui
s'intègre proprement dans une CI.

## Depuis Python

```python
from pathlib import Path

import sprezzature_ux_laws as ux

for constat in ux.audit_html("<nav>" + '<a href="/">x</a>' * 12 + "</nav>"):
    print(constat.law, constat.message)

ux.audit_file(Path("public/index.html"), laws={"fitts", "jakob"})
ux.fix_file(Path("page.html"), laws=set(ux.LAWS), dry_run=True)
```

`ux.LAWS` est le tuple de toutes les lois connues, dans l'ordre où les
vérifications tournent — la même liste que la ligne de commande utilise pour
valider `--only` et que l'API HTTP publie, lue à un seul endroit pour que les
quatre surfaces ne puissent pas se contredire.

## Périmètre assumé

L'auditeur attrape les violations mécaniques, décidables à la lecture
du source. Il ne juge pas si un écran répond à la bonne question ni si
un parcours a du sens : cela reste un jugement humain. C'est un verrou
rapide, pas un substitut à une revue de design.

## Licence

BSD-3-Clause © Warith HARCHAOUI. Fait partie de la boîte à outils
[sprezzature](https://sprezzature.ai/).
