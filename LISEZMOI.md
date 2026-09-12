# sprezzature-ux-laws

[![Licence](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇬🇧 README.md](README.md) · 🇫🇷 LISEZMOI.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://harchaoui.org/warith/sprezzature/)

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

## Utilisation

```bash
# Auditer un fichier ou une arborescence complète
python scripts/audit_laws_of_ux.py public/index.html
python scripts/audit_laws_of_ux.py site/ --json

# Se restreindre à certaines lois, ou corriger automatiquement les cas mécaniques
python scripts/audit_laws_of_ux.py page.html --only fitts,jakob
python scripts/audit_laws_of_ux.py page.html --fix
```

Les constats sont de sévérité `error` ou `warning` ; le programme
sort avec un code non nul dès qu'une `error` est présente, ce qui
s'intègre proprement dans une CI.

## Périmètre assumé

L'auditeur attrape les violations mécaniques, décidables à la lecture
du source. Il ne juge pas si un écran répond à la bonne question ni si
un parcours a du sens : cela reste un jugement humain. C'est un verrou
rapide, pas un substitut à une revue de design.

## Licence

BSD-3-Clause © Warith HARCHAOUI. Fait partie de la boîte à outils
[sprezzature](https://harchaoui.org/warith/sprezzature/).
