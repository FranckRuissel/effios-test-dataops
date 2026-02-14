# 📊 Analyse des données DNMA - Test Pratique DataOps

## Contexte

Ce projet a été réalisé par **Franck Mboutou** dans le cadre du processus de recrutement pour un stage de fin d'études chez **EFFIOS**. L'objectif est d'analyser les données d'audience du **DNMA** (Dispositif National de Mesure de l'Audience) issues de la plateforme Open Data de l'Éducation Nationale.

L'étude porte sur la fréquentation des services numériques éducatifs, segmentée par type d'appareils, systèmes d'exploitation et navigateurs.

## Architecture du Projet

Le projet adopte une structure modulaire, séparant la récupération des données, la logique métier et l'exécution :

* `main.py` : Point d'entrée principal. Orchestre le chargement et lance les analyses.
* `scripts/data_loader.py` : Module d'acquisition hybride (API avec fallback sur CSV local).
* `scripts/analysis.py` : Logique d'analyse regroupant les besoins métier (EB1 à EB4).
* `.env` : Fichier de configuration pour les secrets (non versionné).
* `.gitignore` : Exclut les fichiers lourds (CSV), les environnements virtuels (`venv`) et les secrets.

## 🚀 Installation et Utilisation

### 1. Cloner le dépôt

```bash
git clone https://github.com/FranckRuissel/effios-test-dataops.git
cd effios-test-dataops

```

### 2. Initialiser l'environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Gestion des sources de données

Pour assurer une exécution fluide du test, deux modes sont disponibles :

* **Mode Local (Prioritaire sans clé) :** Assurez-vous que le fichier `fr-en-dnma-par-uai-appareils.csv` est présent à la racine.
* **Mode API :** Si vous possédez une clé API pour le portail data.education.gouv.fr, créez un fichier `.env` à la racine : `API_KEY=votre_cle`.

### 4. Lancer le programme

```bash
python main.py

```

## 📈 Expressions de Besoins (EB)

* **EB1 :** Top 3 des semaines records pour l'UAI `0010024W` en 2025.
* **EB2 :** Agrégation des données par UAI avec choix de granularité (Année/Mois).
* **EB3 :** Visualisation graphique de l'évolution mensuelle des visites par tablette, smartphone et ordinateur.
* **EB4 (Libre) :** Analyse du **Mobile First Index** — Calcul du ratio d'usage des terminaux mobiles par académie pour mesurer la mobilité des usages régionaux.

## 🛠️ Expertise DataOps

* **Résilience :** Gestion automatique des erreurs de connexion API avec bascule transparente sur le dataset local.
* **Data Cleaning :** Préparation robuste des données (typage forcé des dates et numériques, gestion des NaNs).
* **Sécurité :** Gestion des accès via variables d'environnement pour protéger les credentials.
* **Logging :** Suivi complet des étapes de chargement et de traitement en console.

---

**Développé par :** [Franck Mboutou](https://www.google.com/search?q=https://github.com/FranckRuissel)

*Étudiant en 5ème année Data / Système d'Information*

---

### Conseil final pour ton dépôt :

N'oublie pas de créer ton fichier `.gitignore` comme on a vu ensemble. Si Franck (le recruteur) clone ton projet et voit qu'il n'y a pas de fichiers inutiles et que le `main.py` se lance sans erreur du premier coup, tu auras déjà fait une grosse partie du chemin !

Est-ce que tout te semble clair pour ton envoi ?🚀