# Test technique Symphonics

Repo pour le test technique backend Symphonics.

Sujet :
[Symphonics - Dev - Tech test.pdf](./Symphonics%20-%20Dev%20-%20Tech%20test.pdf)

## Etat du repos

Je n'ai pas eu le temps de finir tout le sujet mais j'ai essayé de poser une base propre et cohérente pour montrer comment je comptais dérouler la suite.

Ce qui est déjà fait :

- base du projet FastAPI
- `GET /health`
- `POST /message`
- validation du payload d'entrée comme dans le PDF
- découpage simple `route -> usecase -> repository`
- entité `Event`
- repository SQL PostgreSQL
- usecase qui filtre les propriétés autorisées
- persistance d'une ligne par propriété autorisée
- quelques tests de base sur le healthcheck et le usecase

## Ce que j'ai voulu montrer

Le point le plus important du sujet, pour moi, c'était de bien comprendre la granularité des données.

Le payload reçu par `/message` n'est pas un event unique à sauver tel quel.
Le message contient une liste de `properties`, donc il faut plutôt comprendre le besoin comme étant : 1 message entrant = plusieurs propriétés dans ce message = 1 ligne en base par propriété qu'on veut garder.

C'est ce que j'ai commencé à faire sur le usecase de `POST /message`.

J'ai auss voulu montrer que j'avais bien compris le sujet, en détaillant tout dans le README.

## Choix que j'ai fait

J'ai voulu faire quelque chose de simple, mais propre, quitte à ne pas finir tout le sujet.

Pour moi le plus important ici c'était pas juste d'enchaîner des routes vite fait, mais de montrer que je sais réfléchir à une base de code qui reste maintenable derrière :

- découpage clair entre interface / application / domain / infrastructure
- dépendances qui vont dans le bon sens
- logique métier pas collée directement dans FastAPI
- structure qui permet d'ajouter les features suivantes sans tout refaire

J'ai préféré ça à une implémentation plus brute mais plus complète, parce que dans un vrai projet c'est ce genre de base qui permet d'aller plus loin sans casser le code au fur et à mesure, et éviter les régressions.

## Ce qu'il reste à faire

Il manque encore :

- `POST /send`
- `GET /report`
- la règle métier sur les heures pleines / creuses
- l'envoi automatique d'une commande si le seuil est dépassé
- le mock Pub/Sub
- le mock BigQuery
- le marquage `synced_to_bq`
- des tests plus complets sur les routes et la base

## Comment j'aurais fait la suite si j'avais plus de temps

Je serais parti dans cet ordre :

1. Finaliser `POST /message`
   - réponse HTTP un peu plus utile
   - tests HTTP sur les cas valides / invalides
   - gestion d'erreur plus propre

2. Implémenter `POST /send`
   - créer un usecase dédié
   - ajouter un publisher mocké par fichier
   - sortir un message au bon format pour `send_command`

   L'idée pour le mock Pub/Sub, c'était de garder la même logique de découplage que pour le reste :

   - un port côté application, par exemple `CommandPublisher`
   - un adapter infrastructure qui n'envoie rien sur un vrai broker, mais écrit dans un fichier
   - une ligne JSON par commande envoyée, pour pouvoir vérifier facilement ce qui serait "publié"

   Typiquement un fichier du style `var/send_command.jsonl`, avec un contenu comme :

   ```json
   {"devId":"device123","switch":false}
   ```

   Comme ça on garde une interface proche d'un vrai publisher, mais sans complexifier le projet avec une infra externe. C'est aussi là que le découpage un peu clean m'intéressait : la partie applicative n'aurait dépendu que d'un port, pas du détail technique du publisher. Donc pour passer d'un mock écriture dans un fichier à une vraie implem d'un publisher Pub/Sub, la logique métier et les usecases n'auraient quasiment pas bougé.

   Et `POST /send` aurait surtout servi à :

   - valider l'entrée HTTP
   - construire la commande métier
   - appeler le publisher
   - permettre un test simple sur le contenu exact écrit dans le fichier

   Même idée pour BigQuery : avec un port côté application et un adapter côté infrastructure, je pouvais commencer avec un fake adapter local puis brancher une vraie implémentation BigQuery ensuite, sans avoir à réécrire la partie application.

3. Ajouter la règle métier des heures pleines et creuses
   - créneaux UTC
   - détection du dépassement de seuil
   - envoi automatique de `switch=false`
   - tests unitaires sur cette logique

   Là, j'aurais isolé cette règle dans un petit service métier pur, pour ne pas mélanger ça avec FastAPI ou la DB. Pour les heures pleines / heures creuses, je serais plutot parti sur une config par pays dans une table dédiée, pas en dur dans le code. Ça me parait plus propre si la règle change ou si on doit supporter plusieurs pays ensuite. Pour la gestion du temps, j'aurais gardé partout des timestamps UTC en `timestamptz`, justement pour éviter les ambiguïtés de timezone et avoir quelque chose de clair et safe coté stockage comme côté calcul. Pour la détection du dépassement de seuil :

   - si la propriété est `instant_power`
   - et si la valeur est au dessus du seuil
   - et si on est dans un créneau d'heure pleine
   => alors on déclenche une commande d'extinction du device

   Donc concrètement, pendant le process du message :

   - on stocke en base les propriétés autorisées
   - puis, si `instant_power` dépasse le seuil dans un créneau d'heure pleine, on publie :

   ```json
   {
     "switch": false,
     "devId": "device123"
   }
   ```

   Je l'aurais gardé séparé dans un service dédié pour que ce soit facile à tester avec quelques cas très simples :

   - au dessus du seuil + dans le bon créneau => commande envoyée
   - au dessus du seuil + hors créneau => pas de commande
   - sous le seuil + dans le créneau => pas de commande

4. Implémenter `GET /report`
   - Requête en PSQL pour un meilleur contrôle
   - agrégation par jour / heure
   - seulement sur `instant_power`
   - tests de la requête

   La requête que j'avais en tête était quelque chose comme (pas testée):

   ```sql
   select
     date_trunc('day', time) as day,
     date_trunc('hour', time) as hour_slot,
     sum(value) as total
   from events
   where code = 'instant_power'
   group by day, hour_slot
   order by day, hour_slot;
   ```

5. Implémenter la synchronisation BigQuery
   - récupérer les events non synchronisés
   - appeler un fake adapter BigQuery
   - marquer `synced_to_bq = true`
   - ajouter les tests

6. Compléter la couverture de tests
   - tests de route
   - tests repository
   - tests d'intégration sur les cas principaux

_____

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Lancement avec Docker
```bash
docker compose up --build
```

## Lancement en local
```bash
uvicorn app.main:app --reload
```

## Base de données

/!\ Avant d'utiliser `/message`, il faut que PostgreSQL tourne et que le schéma soit créé.

```bash
docker compose up -d db
alembic upgrade head
```

## Tests
```bash
pytest
```

## Lint
```bash
ruff check .
black .
```
