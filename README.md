# Registre de reventes

Application de suivi des bénéfices d'achat-revente : chaque article acheté puis
revendu, avec sa photo, sa catégorie, son canal d'achat et son vendeur. L'appli
calcule les bénéfices mois par mois et sort les documents nécessaires aux
déclaratifs.

En ligne : **https://amandiine37.github.io/reventes/**

> Cette application **n'est pas utilisée par Amandine** mais par une autre
> personne. Les retours arrivent donc en différé : après chaque dépôt, vérifier
> soi-même le site en ligne plutôt que d'attendre un test.

## Lancer l'application en local

```bash
python serve.py
```

Puis ouvrir http://localhost:4173 dans le navigateur.
(Le port 4173 est celui de cette appli : 4174 pour Tribu, 4176 pour le potager,
4177 pour le cahier de clientèle.)

`serve.py` ne sert **qu'en local** et n'est volontairement **pas déposé** sur
GitHub, contrairement aux autres projets perso.

## Les deux écrans

| Écran | À quoi il sert |
|---|---|
| **Tableau de bord** | Les quatre chiffres clés, le graphique des six derniers mois, la répartition par catégorie, **la rentabilité par lieu d'achat**, le rapport mensuel, les impôts à provisionner, la sauvegarde et l'apparence. |
| **Articles** | La liste complète, avec filtres (tous / en stock / vendus / annulés) et huit tris. |

## Les quatre états d'un article

C'est le cœur de l'application, et la source des questions les plus fréquentes.

| État | Ce que ça veut dire | Effet sur les chiffres |
|---|---|---|
| **En stock** | Acheté, pas encore revendu | Compte dans le capital immobilisé |
| **Vendu** | Revendu | Compte dans le bénéfice, au mois de la vente |
| **Achat annulé** | *Je n'ai finalement pas acheté* (remboursé, retour au vendeur) | Ne compte **nulle part** : l'argent n'est jamais sorti |
| **Vente annulée par l'acheteur** | L'acheteur renvoie l'article | L'article **revient en stock** ; voir ci-dessous |

### Achat annulé ≠ vente annulée

Deux choses différentes, souvent confondues :

- **Achat annulé** est une case à cocher. L'article disparaît de tous les calculs
  mais reste visible, barré, avec un tampon « annulé ».
- **Vente annulée** est un bouton, disponible uniquement sur un article vendu :
  *« L'acheteur a annulé — remettre en stock »*.

### Comment est traitée une vente annulée

**La vente d'origine n'est jamais effacée.** Elle reste dans le mois où elle a eu
lieu, et le retour apparaît comme une ligne **négative** dans le mois où il a eu
lieu.

Exemple : vendu 110 € en juillet, retourné en septembre.
Le rapport de juillet continue d'afficher cette vente ; celui de septembre porte
la déduction. **Un rapport déjà édité et déclaré reste donc valable.**

C'est un choix explicite (16/08/2026), demandé après avoir vu l'autre option :
effacer la vente aurait modifié rétroactivement des mois déjà déclarés.

L'historique des ventes annulées est conservé sur l'article et visible en le
rouvrant. Un article peut être revendu et retourné plusieurs fois.

## Les lots

Un lot est un achat groupé : plusieurs objets pour un seul prix. À la saisie,
cocher **« Acheté en lot »** et indiquer le nombre d'unités. Deux façons de le
gérer, au choix :

- **Garder une seule ligne** — l'article porte une quantité. On vend ensuite tout
  ou partie du lot.
- **Créer un article par unité** — l'appli éclate le lot en autant d'articles, à
  renommer et réajuster individuellement. À préférer quand les objets ont des
  valeurs très inégales.

**Vendre une partie d'un lot** scinde l'enregistrement : une ligne vendue pour
les unités parties, et le lot d'origine réduit d'autant. Le coût d'achat est
réparti au centime près — la somme des parts est toujours exactement égale au
prix payé (60 € en 7 donnent 8,58 + 8,57 × 6).

## La rentabilité par lieu d'achat

Répond à la question : *« ce vide grenier vaut-il le déplacement l'an prochain ? »*

Le champ **Lieu d'achat** sert à la fois aux sites (Vinted, eBay, Le Bon Coin) et
aux endroits physiques. Pour un vide grenier ou une brocante, **préciser le
lieu** — « Vide grenier de Villandry » et non « Vide grenier » — sans quoi tous
les vide greniers se retrouvent dans la même ligne et la statistique ne distingue
plus rien. Les suggestions par défaut se terminent volontairement par « de » pour
y inviter.

La carte **Par lieu d'achat** du tableau de bord donne, pour chaque lieu et
toutes périodes confondues : le bénéfice, le nombre d'articles achetés, vendus et
encore en stock, le total investi, et surtout le **bénéfice moyen par vente** —
le vrai repère pour décider d'y retourner. Les lieux sont classés du plus
rentable au moins rentable.

Les achats annulés sont exclus (ils n'ont jamais eu lieu). Les ventes annulées
par l'acheteur se neutralisent d'elles-mêmes, puisque le bénéfice vient du
journal des mouvements.

L'export Excel reprend ces chiffres dans un bloc **PAR LIEU D'ACHAT**, et la
liste se trie par lieu.

## Le prix conseillé

L'appli propose un prix de revente à **+ 40 %** du prix d'achat
(`MARGE_CIBLE` dans `index.html`). Il s'affiche à la saisie, avec un bouton
« Utiliser », et dans la liste sous la forme « viser 21,00 € » — par unité s'il
s'agit d'un lot.

## Les rapports

### Rapport mensuel (PDF)

Carte **Rapport mensuel** → choisir la période → **Aperçu** → **Enregistrer en PDF**.

Le PDF passe par la fenêtre d'impression du navigateur (« Enregistrer au format
PDF »), sans bibliothèque externe : l'appli fonctionne donc hors connexion.

Il contient l'en-tête et la période, quatre chiffres clés (bénéfice, total des
ventes, coût d'achat, marge), le détail des ventes, les ventes annulées par
l'acheteur s'il y en a, la répartition par catégorie, la provision fiscale si un
taux est renseigné, et le stock restant en note.

La période proposée comprend chaque mois où il y a eu un mouvement, plus une
ligne par année.

**La palette d'impression est forcée en clair**, quel que soit le thème : sans
cela, un téléphone en thème sombre imprimerait un PDF noir.

Les achats annulés **n'apparaissent pas** dans le rapport — demandé le 16/08/2026.

### Export Excel (CSV)

Colonnes : Nom, Catégorie, Lieu d'achat, Vendeur, Quantité, Prix d'achat, Date
d'achat, Prix conseillé (+40 %), Prix de revente, Date de revente, Bénéfice, Mois
de revente, Statut, Ventes annulées.

Suivent trois blocs : **RÉCAPITULATIF MENSUEL** (avec une ligne TOTAL),
**VENTES ANNULÉES PAR L'ACHETEUR** s'il y en a, et **PAR LIEU D'ACHAT**.

Trois détails pour Excel français : séparateur `;`, virgules décimales, et un
marqueur d'encodage en tête sans lequel les accents s'affichent mal.

## Les impôts à provisionner

Un **calculateur**, pas un conseil fiscal. Le taux et sa base (le bénéfice ou le
total des ventes) sont renseignés à la main ; l'appli fait la multiplication et
affiche le montant à provisionner, la part du mois en cours et le bénéfice net
estimé.

Aucun taux n'est proposé par défaut, volontairement : le régime applicable dépend
de la situation et un chiffre inventé induirait en erreur. L'avertissement est
écrit dans l'appli et repris dans le rapport.

Une assiette négative (un mois dominé par des annulations) donne une provision de
0 €, jamais un montant négatif.

## L'apparence

Six thèmes et trois luminosités, réglés séparément dans la carte **Apparence** :

| Thème | Univers |
|---|---|
| **Livre de comptes** | Papier de registre, encre ferro-gallique, laiton (thème par défaut) |
| **Cahier d'écolier** | Papier Seyès, encre bleue, marge rouge |
| **Machine à écrire** | Papier pelure, carbone, ruban rouge, Courier |
| **Années 70** | Papier peint à chevrons, orange brûlé et moutarde, coins ronds |
| **Herbier** | Papier vergé, verts de feuillage, légendes en italique |
| **Art déco** | Or et bleu électrique, capitales espacées |

Luminosité : **selon le téléphone** (par défaut), **toujours clair** ou
**toujours sombre**.

Techniquement : deux attributs sur `<html>`, `data-skin` et `data-mode`, posés
par un script en tête de `<body>` pour éviter que l'appli clignote dans le thème
par défaut avant de basculer.

## Où sont les données ?

**Uniquement dans le navigateur du téléphone.** Rien n'est envoyé nulle part :
pas de compte, pas de serveur, pas de synchronisation — contrairement à Tribu et
au potager qui utilisent Firebase.

Clés de stockage :

| Clé | Contenu |
|---|---|
| `revente_items_v1` | Les articles (photos comprises, en base64) |
| `revente_categories_v1` | Les catégories ajoutées à la main |
| `revente_canaux_v1` | Les canaux d'achat ajoutés à la main |
| `revente_fiscal_v1` | Taux et base de la provision |
| `revente_sauvegarde_v1` | Date et empreinte de la dernière sauvegarde, fréquence du rappel |
| `revente_tri_v1` | Le tri choisi pour la liste |
| `revente_apparence_v1` | Thème et luminosité |

### Ce qui peut les effacer

Effacer les données de navigation de Chrome, désinstaller l'appli, changer de
téléphone, ou ouvrir l'appli depuis une autre adresse (les données sont liées à
l'adresse : `localhost:4173` et l'adresse GitHub Pages sont deux mondes séparés).

### La sauvegarde, seule vraie protection

Carte **Sauvegarde** → **Sauvegarde (fichier)** : un fichier `.json` à garder sur
un ordinateur ou un Drive. **Restaurer une sauvegarde** le relit.

⚠️ La restauration **ajoute** les articles à ceux déjà présents, elle ne les
remplace pas. Ne pas la lancer deux fois.

Un **rappel** s'affiche en haut de l'appli quand une sauvegarde s'impose. Il
s'appuie sur une empreinte des données : il ne se déclenche que si le contenu a
changé depuis le dernier export réussi — pas seulement parce que du temps a
passé. Fréquence réglable : chaque semaine (par défaut), tous les 15 jours,
chaque mois, ou jamais. « Plus tard » le met en veille 2 jours.

Le rappel ne se tait **que si le fichier est réellement sorti**.

⚠️ Une sauvegarde recopiée à la main (collée dans un mail) revient souvent
abîmée : le logiciel remplace les espaces d'indentation par des espaces
insécables. L'appli sait maintenant les nettoyer à la lecture, mais le fichier
téléchargé reste la voie fiable. (Incident du 17/08/2026, 649 espaces insécables.)

## Mettre l'application en ligne (GitHub Pages)

Le dépôt est `amandiine37/reventes`, sur un **compte GitHub personnel** — rien ne
passe par le compte OptimaHR, c'est un projet perso et il doit le rester.

1. Déposer les fichiers sur GitHub (interface web, pas de git en local).
2. **Settings → Pages → Source : `main` / dossier `/ (root)`**.
3. L'appli est à `https://amandiine37.github.io/reventes/`.
4. Sur le téléphone : ouvrir l'adresse dans Chrome → menu **⋮** →
   **« Installer l'application »**.

### ⚠️ À chaque mise à jour : incrémenter `VERSION` dans `sw.js`

C'est **la modification de `sw.js`** qui déclenche le bandeau *« Une nouvelle
version de l'appli est prête »* avec son bouton **Recharger**. Sans ce bump, le
navigateur ne voit aucune mise à jour et le bandeau n'apparaît jamais.

Donc : modifier `index.html` **et** incrémenter `VERSION` dans `sw.js`, puis
**déposer les deux fichiers**. Le numéro de version sert aussi de nom au cache
(`reventes-v1.8`), ce qui purge l'ancien.

### Vérifier le dépôt

Le cache de GitHub peut servir l'ancienne copie pendant quelques minutes : si un
changement semble absent, ajouter `?cb=123` à l'adresse du fichier avant de
conclure. Comparer les empreintes locales et en ligne est la méthode fiable :

```bash
sha256sum index.html sw.js
```

Le dépôt ne doit contenir que **cinq fichiers** : `index.html`,
`manifest.webmanifest`, `sw.js`, `icon-192.png`, `icon-512.png`.

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | Toute l'appli : structure, styles et code dans un seul fichier |
| `sw.js` | Fonctionnement hors connexion (stratégie « réseau d'abord ») et détection des mises à jour |
| `manifest.webmanifest` | Nom, icônes et couleurs pour l'installation sur le téléphone |
| `icon-192.png`, `icon-512.png` | Icônes, générées par un encodeur PNG écrit à la main (pas de bibliothèque d'images installée) |
| `serve.py` | Serveur local de test — **ne pas déposer en ligne** |
| `README.md` | Ce fichier |

## Pièges rencontrés, à ne pas réintroduire

1. **Les boutons n'héritent pas de la couleur du texte** : sans `color` explicite,
   ils retombent sur le noir du navigateur — invisible en thème sombre. Une règle
   de garde le corrige globalement. Après toute modification de couleurs,
   relancer un audit de contraste sur les deux luminosités.
2. **La palette d'impression doit rester plus spécifique que `[data-skin][data-mode]`**,
   sinon un thème sombre imprime un PDF noir.
3. **`confirm()` et les téléchargements directs sont bloqués** dans un cadre
   sécurisé (l'ancienne version publiée en artifact Claude). D'où la fenêtre de
   confirmation maison et le repli « copier le contenu ». Ne pas revenir aux
   appels natifs.
4. **Deux onglets ouverts en même temps** : l'appli garde une copie des données en
   mémoire ; un écouteur `storage` recharge cette copie pour éviter qu'un onglet
   écrase les ajouts de l'autre.
5. **`toISOString()` décale la date d'un jour en heure d'été** : formater à partir
   des composantes locales.

## Avertissement

Les chiffres produits par cette application sont un suivi personnel. Ils ne
constituent ni une comptabilité officielle ni un avis fiscal : faire valider le
régime et le taux applicables par un comptable ou sur impots.gouv.fr.
