# sprezzature-ux-laws

[![Licence](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](https://github.com/warith-harchaoui/sprezzature-ux-laws/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

[🇬🇧 README.md](README.md) · 🇫🇷 LISEZMOI.md

[![logo](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/logo.png)](https://sprezzature.ai/)

Un auditeur statique des **Laws of UX (user experience, la manière dont une interface se vit à l'usage, comme le temps passé à trouver le bon bouton)**,
les lois de l'ergonomie cognitive, pour du HTML.

Les Laws of UX sont des heuristiques nommées, issues de la psychologie
et de la recherche en interaction homme-machine, rassemblées par Jon
YABLONSKI sur [lawsofux.com](https://lawsofux.com/). La loi de Hick, par
exemple, dit qu'un écran qui propose plus de choix demande plus de
temps pour se décider : un menu de navigation avec quarante liens est
mesurablement plus difficile à utiliser qu'un menu qui en propose sept.
Cet outil ne voit jamais la page une fois affichée, et n'observe jamais
un vrai utilisateur. Il lit le texte HTML brut et signale seulement
les manquements qu'on peut trancher à sa seule lecture, par exemple
compter les liens dans une balise `<nav>`. Ce choix le rend rapide et
assez prévisible pour tourner dans un crochet de pré-commit ou une
étape d'intégration continue (CI), au prix de ne détecter qu'une
fraction des violations de chaque loi, celle qu'une lecture de texte
peut effectivement voir. La définition complète et sourcée de chaque
loi vit dans [`references/laws-of-ux.md`](references/laws-of-ux.md).

## Comment ça marche

![Schéma de flux. En haut, une source HTML alimente deux voies. La voie de gauche contrôle : elle établit ce qu'un seul écran montre à partir des classes d'affichage Tailwind, retient le pire des deux décomptes, téléphone ou bureau, et tranche huit lois nommées, puis rend des constats avec un code de sortie non nul sur une erreur. La voie de droite fabrique : elle applique les quatre réparations mécaniques. Les deux se rejoignent en un seul résultat, un écran dont les fautes mesurables ont disparu.](https://raw.githubusercontent.com/warith-harchaoui/sprezzature-ux-laws/main/assets/comment-ca-marche.svg)

## Lois couvertes

Huit lois, dans l'ordre où les vérifications tournent. L'identifiant est le nom que
toutes les surfaces emploient.

| Identifiant | Loi | Sévérité | Ce qui la déclenche | Correcteur |
|---|---|---|---|---|
| `hick` | Loi de Hick | error | Un `<nav>` qui montre plus de 7 choix de premier niveau (`<a>` ou `<button>`) sur un même écran (voir plus bas) | non |
| `choice-overload` | Surcharge de choix | warning | Une `<section>` ou un `<div>` dont les classes contiennent `pricing` ou `plans` et `grid` ou `flex`, avec plus de 4 colonnes directes `<article>` ou `<div>` | non |
| `miller` | Loi de Miller | warning | Une suite visible de 8 lettres et chiffres ou plus, dont au moins un chiffre (codes, identifiants, numéros de carte) | oui |
| `jakob` | Loi de Jakob | error | Un `<div>` ou un `<span>` portant `onclick`, `role="button"` ou `cursor-pointer`, sans enfant `<button>`, `<a>`, `<input>`, `<select>` ou `<summary>` | oui |
| `fitts` | Loi de Fitts | warning | Un élément interactif sans classe `h-`, `min-h-` ou `size-` d'au moins `11` (44 px), ou `full`, `screen`, `auto` | oui |
| `aesthetic-usability` | Effet esthétique-utilisabilité | warning | Un élément interactif sans classe `focus-visible:ring-*` ni `focus:ring-*` | oui |
| `selective-attention` | Attention sélective | warning | Un `<span>` coloré `text-red-*`, `text-green-*`, `text-amber-*`, `text-yellow-*` ou `text-orange-*`, sans mot d'état (« error », « ok », « pending »…) ni enfant `<svg>` ou `<img>` | non |
| `tesler` | Loi de Tesler | warning | Une heure `HH:MM` sans marqueur de fuseau (`UTC`, `GMT`, `Z`, `+02:00`, `Europe/Paris`…) à moins de 40 caractères | non |

Les éléments interactifs sont `<button>`, `<a>`, `<input>`, `<select>`, `<textarea>` et
`<summary>`. Ce que chaque vérification laisse passer :

- **Miller** ne lit que le texte visible : il ignore les lignes d'un bloc `<script>`
  ou `<style>`, les balises elles-mêmes avec leurs attributs (et, sur une balise coupée
  en plusieurs lignes, les valeurs de `class`, `id`, `href` et `src`), les mots purement
  alphabétiques, et les noms formés d'au moins trois lettres suivies de chiffres
  seulement (`GMTED2010`, `LANDSAT8`, `ISO14001`) : ce sont des noms de normes ou de
  jeux de données, que le correcteur couperait sinon d'espaces insécables.
- **Jakob** laisse aussi passer un `<span>` ou un `<div>` stylé à l'intérieur d'un
  `<label>` qui contient un `<input>`, un `<select>` ou un `<textarea>` : c'est le
  contrôle de formulaire qui porte la sémantique.
- **Fitts** ignore `<input type="hidden">`, et traite un `<a>` comme un lien de texte
  plutôt que comme un bouton, sauf s'il porte `inline-flex`, `flex`, `block`, `btn`,
  `button`, ou une classe `bg-` ou `border-`.
- **Tesler** ignore une heure placée dans un contexte de durée : les mots `duration`,
  `elapsed`, `remaining`, `currentTime`, `runtime`, `length`, un attribut `data-ra-`, une
  classe `ra-time`, un curseur `type="range"`, `<progress>`, `<audio>` ou `<video>`. Une
  position de lecture n'a pas de fuseau horaire.

**Fitts et esthétique-utilisabilité lisent l'échelle de Tailwind**, donc elles
demandent d'abord si le document emploie Tailwind CSS (Cascading Style Sheets, les règles qui donnent à une page web ses couleurs, ses polices et sa mise en page) : des utilitaires propres à
Tailwind d'au moins deux sortes différentes (espacement, couleur, préfixe responsive ou
d'état, écart, dimension, arrondi), comme `px-4` et `bg-blue-600`. `px-4` et `py-2` sont
une seule sorte. Sinon, chacune des deux
rend un seul constat `info` pour tout le document au lieu d'un avertissement par
élément, et `--fix` n'y écrit aucune classe Tailwind.

## Comment il compte : des choix, pas des éléments

La loi de Hick mesure les choix qu'une personne affronte **au même instant**.
Compter les liens d'un fichier se trompe donc deux fois.

**Un en-tête responsive contient deux menus.** Une rangée marquée
`hidden sm:inline` et un bouton marqué `sm:hidden` ne s'affichent jamais
ensemble : le lecteur sur téléphone voit l'un, celui sur ordinateur voit
l'autre. Les additionner reproche au lecteur des choix qu'aucun écran ne lui
montre. L'auditeur résout donc la visibilité de chaque contrôle d'après ses
classes d'affichage Tailwind, en remontant les ancêtres (un conteneur qui
masque son sous-arbre l'emporte sur un enfant qui s'afficherait), puis retient
le pire des deux comptes en disant lequel.

**Un groupe vaut un choix.** Un `<details>`, un `<dialog>`, un `<menu>`, ou un
élément dont le `role` vaut `radiogroup`, `tablist`, `menubar`, `listbox` ou
`combobox` replie plusieurs contrôles en une seule décision. Chacun compte pour un,
quel que soit son contenu. Deux `<nav>` d'une même page sont comptés à part.

Quand les deux états sont ambigus, le compte monte plutôt qu'il ne descend :
un contrôle qui apparaît à `md` et disparaît à `lg` est traité comme réservé
au bureau. Signaler de trop envoie quelqu'un vérifier ; signaler trop peu
laisse passer.

---

## Installation

```bash
pip install sprezzature-ux-laws
```

Une seule installation donne toutes les surfaces : la bibliothèque, les deux
commandes, l'API (application programming interface, des adresses qu'un autre programme appelle pour se servir de l'outil sans personne qui clique)
HTTP (HyperText Transfer Protocol, le protocole par lequel un navigateur demande une page à un serveur, et un programme des données) et le serveur MCP
(Model Context Protocol, le protocole par lequel les agents IA appellent des outils en français). Les dépendances de base sont click (la ligne
de commande), FastAPI, uvicorn, fastapi-mcp et mcp. Il n'y a aucun extra de
fonctionnalité. Le seul extra, `[dev]`, est l'outillage de test (pytest, ruff, mypy,
httpx2).

L'auditeur lui-même n'emploie que la bibliothèque standard de Python (`html.parser`),
sans navigateur ni réseau, ce qui le rend assez bon marché pour un crochet de
pré-commit.

## Ligne de commande

```bash
# Auditer un fichier ou une arborescence complète
sprezzature-ux-laws public/index.html
sprezzature-ux-laws site/ --json

# Se restreindre à certaines lois, ou en écarter
sprezzature-ux-laws page.html --only fitts,jakob
sprezzature-ux-laws page.html --ignore tesler

# Réparer sur place les cas mécaniques, ou prévisualiser la réparation
sprezzature-ux-laws page.html --fix
sprezzature-ux-laws page.html --fix --dry-run
```

Deux commandes installées prennent les mêmes cibles et les mêmes drapeaux, et
appellent le même gestionnaire : `sprezzature-ux-laws` (click) et
`sprezzature-ux-laws-audit` (le script propre à l'outil). Depuis un clone, sans installer le paquet, `python scripts/audit_laws_of_ux.py page.html`
appelle ce même gestionnaire, pourvu que click soit importable.

| Drapeau | Effet |
|---|---|
| `--json` | Écrit un tableau JSON (JavaScript Object Notation, un format texte dans lequel les programmes rangent des données en champs nommés, comme « titre : Accueil »), un objet par constat (`law`, `severity`, `path`, `line`, `message`, `snippet`), au lieu du rapport texte. |
| `--strict` | Tout constat fait échouer l'exécution, quelle que soit sa sévérité. |
| `--only LOIS` | Identifiants à exécuter, séparés par des virgules. Par défaut : les huit. |
| `--ignore LOIS` | Identifiants à écarter, séparés par des virgules. |
| `--fix` | Applique sur place les corrections mécaniques. |
| `--dry-run` | Dit ce que `--fix` appliquerait, sans rien écrire. Implique `--fix`. |
| `-V`, `--version` | Affiche la version. |

Une cible est un fichier `.html` ou `.htm`, ou un dossier parcouru récursivement à la
recherche des deux suffixes, en majuscules comme en minuscules. Tout autre fichier existant est ignoré avec un avertissement.
Un chemin qui n'existe pas est refusé par les deux commandes (code `2`).

Codes de sortie :

- `0` : aucun constat `error` (avec `--strict`, aucun constat du tout), ou aucun
  fichier HTML trouvé. Un `--dry-run` sort toujours avec `0`.
- `1` : au moins un constat `error` (avec `--strict`, au moins un constat).
- `2` : un identifiant inconnu dans `--only` ou `--ignore`, un chemin qui n'existe
  pas, ou une autre erreur d'usage.

Les constats sortent dans l'ordre des vérifications, pas dans l'ordre des lignes.

### Ce que `--fix` modifie

Quatre lois ont un correcteur. Les quatre autres (`hick`, `choice-overload`,
`selective-attention`, `tesler`) demandent une décision de conception, pas une
retouche de texte.

| Loi | Retouche |
|---|---|
| `fitts` | Ajoute `min-h-11` à l'attribut `class` de l'élément. |
| `aesthetic-usability` | Ajoute `focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue`. |
| `miller` | Coupe la suite visible en groupes de quatre depuis la droite, joints par des espaces insécables. La même suite dans une balise (un `href`, une valeur `data-`) reste telle quelle. |
| `jakob` | Réécrit le `<div>` ou le `<span>` cliquable en `<button>`, et retire `role="button"`, s'il s'ouvre et se ferme sur la même ligne et ne contient aucun vrai contrôle. Un conteneur autour de lui reste intact. |

Le correcteur réaudite et recommence, jusqu'à cinq passes, parce que réécrire un
`<div>` en `<button>` crée de nouveaux constats Fitts et anneau de focus. Une seconde
exécution sur un fichier réparé n'applique aucune retouche. Un correcteur ne fait
qu'étendre un attribut `class` existant : un élément qui n'en a pas, ou dont le `class`
n'est pas sur la ligne où s'ouvre sa balise, est compté comme non corrigeable et reste parmi les constats restants. `--fix` n'écrit la page que si un
correcteur a changé quelque chose, et garde ses fins de ligne (un fichier dont les lignes finissent par retour chariot + saut de ligne,
en anglais carriage return line feed, CRLF, comme les écrit le Bloc-notes de Windows, reste CRLF). Il réécrit la page : relisez le diff avant de le committer.

## Depuis Python

```python
from pathlib import Path

import sprezzature_ux_laws as ux

for constat in ux.audit_html("<nav>" + '<a href="/">x</a>' * 12 + "</nav>"):
    print(constat.law, constat.severity, constat.message)

ux.audit_file(Path("public/index.html"), laws={"fitts", "jakob"})
appliquees, non_corrigeables, restants = ux.fix_file(Path("page.html"), laws=set(ux.LAWS), dry_run=True)
```

Le paquet exporte `audit_html`, `audit_file`, `fix_file`, `Finding`, `Walker`,
`Element`, `LAW_REGISTRY`, `LAWS` et `FITTS_FIX_TOKEN`. `ux.LAWS` est le tuple des
huit identifiants, dans l'ordre où les vérifications tournent : la ligne de commande
valide `--only` contre ce même registre, et l'API HTTP le publie.

## API HTTP

```bash
uvicorn sprezzature_ux_laws.api:app --host 127.0.0.1 --port 8000
```

| Méthode et chemin | `operation_id` | Réponse |
|---|---|---|
| `GET /health` | `health` | `{"status": "ok"}` |
| `GET /v1/laws` | `list_laws` | Les huit identifiants, chacun avec une ligne sur ce qu'il vérifie. |
| `POST /v1/audit` | `audit_interface` | Corps `{"html": "...", "laws": [...]}` ; une liste `laws` vide exécute les huit. Rend `findings` (`law`, `severity`, `line`, `message`) et les comptes `errors` et `warnings`. |

Un identifiant inconnu dans `laws` rend une erreur HTTP 400, plutôt qu'un rapport
propre pour des vérifications qui n'ont pas tourné. La documentation interactive est
servie sur `/docs` et `/redoc`. Lancé ainsi, uvicorn ne sert que les routes : le point
d'accès MCP est monté par `sprezzature-ux-laws-mcp` (plus bas), qui sert les mêmes
routes et `/mcp` ensemble.

### Docker

```bash
docker compose up -d
curl -s localhost:8000/health
docker compose run --rm api sprezzature-ux-laws-audit --json /work/index.html
```

L'image lance `sprezzature-ux-laws-mcp` : un seul processus, sur le port 8000, sert à la
fois les routes HTTP (`/health`, `/v1/...`) et le point d'accès MCP sur `/mcp`. Compose
monte `./work` sur `/work` pour les pages à auditer.

## Serveur MCP

Le Model Context Protocol (MCP) permet à un hôte d'agent d'appeler des outils
directement. Le serveur enveloppe la même application FastAPI avec fastapi-mcp, si bien
que l'`operation_id` de chaque route est le nom de l'outil : `health`, `list_laws`,
`audit_interface`.

```bash
sprezzature-ux-laws-mcp                      # 127.0.0.1:8000, point d'accès MCP sur /mcp
sprezzature-ux-laws-mcp --host 0.0.0.0 --port 9000
```

`--host` et `--port` prennent par défaut `SPREZZATURE_UX_LAWS_HOST` et
`SPREZZATURE_UX_LAWS_PORT` quand ces variables sont définies.
`python -m sprezzature_ux_laws.mcp` est équivalent.

## Skill pour agent

Le skill qui dit à un agent quand appliquer ces lois, `sprezzature-ux-laws`, est livré
depuis le dépôt central [sprezzature](https://github.com/warith-harchaoui/sprezzature).
Les règles d'aiguillage et le tableau des outils pour les agents sont dans
[`TRIGGERS.md`](TRIGGERS.md).

## Périmètre assumé

L'auditeur attrape les violations mécaniques, décidables à la lecture du source, de
huit lois sur les trente de lawsofux.com. Il ne juge pas si un écran répond à la bonne
question ni si un parcours a du sens : cela reste un jugement humain. Le temps de
réponse (le seuil de Doherty) n'est pas un fait du source, et n'est pas vérifié. C'est
un verrou rapide, pas un substitut à une revue de design.

## Licence

La licence Berkeley Software Distribution à trois clauses, BSD-3-Clause, une licence libre permissive : chacun peut réutiliser le code, même commercialement, à condition de garder cette mention : © Warith HARCHAOUI. Fait partie de la boîte à outils
[sprezzature](https://sprezzature.ai/).
